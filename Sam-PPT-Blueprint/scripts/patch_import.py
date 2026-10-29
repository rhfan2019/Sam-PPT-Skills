"""Put back what ppt-master's importer loses from the reference pptx (D; run once per library).

  python patch_import.py <参考稿库> [--dry-run]

prepare_reference.py runs this after the import. It rewrites <lib>/import/authoring-svg-flat/ in
place, keeping the importer's output once in authoring-svg-flat.orig/ (later runs start from that
copy, so running it again after this script improves is safe). Measured on rnb-core with the
round-trip ladder (D:/tmp/work/diagnosis): these are the import losses that made a page look wrong
before anything else touched it.

  3d      a shape with a 3D camera rotation (<a:scene3d><a:camera><a:rot lat lon>) is drawn flat and
          full size by the importer: the AISAS ring of slide 33 became a disc over half the page.
          The geometry is squashed about its centre by |cos(lat)| vertically and |cos(lon)|
          horizontally, which is what the camera shows (perspective narrowing is not modelled).
          Isometric presets without a rotation are listed, not changed.
  vert    vertical text (bodyPr vert="eaVert" etc.) arrives horizontal: rewritten one character
          per line, centred in its frame.
  wrap    a one-line text wider than its frame whose shape wraps (bodyPr wrap is not "none") was
          wrapped by PowerPoint, e.g. "漏斗测试" stacked in a 37 px wide box; it is re-wrapped to the
          frame width with textmodel.py.
  hidden  text wholly outside the slide (kept off-canvas in the source) is removed with its shape;
          the final check rejects it and it is never visible.
  table   cells covered by a merge are reduced to {"text": "", "merge_continuation": true}; the
          importer leaves alignment keys on them and the native-table check rejects that.
  chart   a native chart ppt-master cannot rebuild (data-pptx-replacement-status="unsupported-…",
          e.g. a date axis) is tagged data-sam-unsupported; start_page.py / compose_page.py report it
          so the page draws that chart again with a native chart template.
"""
import json
import math
import re
import shutil
import sys
import zipfile
from pathlib import Path

from lxml import etree

sys.path.insert(0, str(Path(__file__).resolve().parent))
import textmodel  # noqa: E402

SVG = "http://www.w3.org/2000/svg"
A = "http://schemas.openxmlformats.org/drawingml/2006/main"
P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NUM = r"-?\d*\.?\d+(?:[eE][-+]?\d+)?"
W, H = 1280.0, 720.0


def nums(s):
    return [float(v) for v in re.findall(NUM, s or "")]


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


# ---------- what the pptx says ----------

def pptx_facts(pptx):
    """{slide_no: {shape_id: {"lat":deg, "lon":deg, "iso":preset, "vert":str, "wrap":str}}}"""
    out = {}
    with zipfile.ZipFile(pptx) as z:
        for name in z.namelist():
            m = re.fullmatch(r"ppt/slides/slide(\d+)\.xml", name)
            if not m:
                continue
            root = etree.fromstring(z.read(name))
            facts = {}
            for sp in root.iter(f"{{{P}}}sp", f"{{{P}}}cxnSp", f"{{{P}}}grpSp", f"{{{P}}}pic"):
                c = sp.find(f".//{{{P}}}cNvPr")
                if c is None:
                    continue
                f = {}
                cam = sp.find(f"./{{{P}}}spPr/{{{A}}}scene3d/{{{A}}}camera")
                if cam is None:
                    cam = sp.find(f"./{{{P}}}grpSpPr/{{{A}}}scene3d/{{{A}}}camera")
                if cam is not None:
                    rot = cam.find(f"{{{A}}}rot")
                    if rot is not None:
                        f["lat"] = int(rot.get("lat", "0")) / 60000.0
                        f["lon"] = int(rot.get("lon", "0")) / 60000.0
                    elif cam.get("prst", "").startswith("isometric"):
                        f["iso"] = cam.get("prst")
                body = sp.find(f"./{{{P}}}txBody/{{{A}}}bodyPr")
                if body is not None:
                    f["vert"] = body.get("vert", "horz")
                    f["wrap"] = body.get("wrap", "square")
                    # insets in px (12192000 EMU = 1280 px); PowerPoint's default is 91440 EMU = 9.6 px
                    f["ins"] = (int(body.get("lIns", "91440")) + int(body.get("rIns", "91440"))) / 9525.0
                if f:
                    facts[c.get("id")] = f
            out[int(m.group(1))] = facts
    return out


# ---------- geometry ----------

def map_path(d, fx, fy):
    """Apply x -> fx(x), y -> fy(y) to an absolute-or-relative path; relative steps are scaled only."""
    toks = re.findall(rf"[A-Za-z]|{NUM}", d)
    out, cmd, vals = [], None, []
    sx = fx(1.0) - fx(0.0)
    sy = fy(1.0) - fy(0.0)

    def flush():
        if cmd is None:
            return
        absl, c = cmd.isupper(), cmd.upper()
        px = fx if absl else (lambda v: v * sx)
        py = fy if absl else (lambda v: v * sy)
        res = []
        if c in "MLTSCQ":
            for i, v in enumerate(vals):
                res.append(px(v) if i % 2 == 0 else py(v))
        elif c == "H":
            res = [px(v) for v in vals]
        elif c == "V":
            res = [py(v) for v in vals]
        elif c == "A":
            for i in range(0, len(vals), 7):
                rx, ry, rot, la, sw, x, y = vals[i:i + 7]
                res += [abs(rx * sx), abs(ry * sy), rot, la, sw, px(x), py(y)]
        else:
            res = vals
        out.append(cmd + " " + " ".join(fmt(v) for v in res) if res else cmd)

    for tok in toks:
        if tok.isalpha():
            flush()
            cmd, vals = tok, []
        else:
            vals.append(float(tok))
    flush()
    return " ".join(out)


def squash(g, kx, ky):
    f = nums(g.get("data-pptx-frame"))
    cx, cy = f[0] + f[2] / 2, f[1] + f[3] / 2
    fx = lambda v: cx + (v - cx) * kx  # noqa: E731
    fy = lambda v: cy + (v - cy) * ky  # noqa: E731
    for d in g.iter():
        if not isinstance(d.tag, str):
            continue
        if d.get("d"):
            d.set("d", map_path(d.get("d"), fx, fy))
        for a, fn in (("x", fx), ("cx", fx), ("x1", fx), ("x2", fx), ("y", fy), ("cy", fy), ("y1", fy), ("y2", fy)):
            if d.get(a) and len(nums(d.get(a))) == 1 and etree.QName(d).localname != "text":
                d.set(a, fmt(fn(nums(d.get(a))[0])))
        fr = nums(d.get("data-pptx-frame"))
        if len(fr) == 4:
            d.set("data-pptx-frame", " ".join(fmt(v) for v in (fx(fr[0]), fy(fr[1]), fr[2] * kx, fr[3] * ky)))


# ---------- text ----------

def own_text(g):
    return [t for t in g.iter(f"{{{SVG}}}text")]


def stack_vertical(t, f):
    chars = [c for c in "".join(p.text for p in textmodel.parse(t)) if not c.isspace()]
    if len(chars) < 2:
        return False
    t.set("text-anchor", "middle")
    t.set("x", fmt(f[0] + f[2] / 2))
    size = textmodel.style_of(t, {})[0]
    lh = round(size * 1.15, 2)
    top = f[1] + (f[3] - ((len(chars) - 1) * lh + size)) / 2
    t.set("y", fmt(top + size * 0.88))
    for a in ("data-pptx-text-model", "data-paragraph-line-height"):
        t.attrib.pop(a, None)
    for c in list(t):
        t.remove(c)
    t.text = None
    t.set("data-paragraph-line-height", fmt(lh))
    t.set("data-pptx-text-model", "paragraphs")
    attrs = textmodel.run_attrs(t)
    for ch in chars:
        ln = etree.SubElement(t, f"{{{SVG}}}tspan")
        etree.SubElement(ln, f"{{{SVG}}}tspan").text = ch
    return True


def needs_wrap(t, f, ins):
    """The width PowerPoint wrapped this one-line text to, when it did: frame width less the shape's own
    insets, and the estimated line clearly wider than that (estimates run a few % over real glyphs)."""
    if t.get("data-paragraph-line-height") and len([c for c in t if etree.QName(c).localname == "tspan"]) > 1:
        return None
    paras = textmodel.parse(t)
    if len(paras) != 1:
        return None
    aw = max(f[2] - ins, 1.0)
    w = textmodel.line_width(t, paras[0].runs)
    return aw if w > aw * 1.15 + 2 and w > 0 else None


def outside(t):
    size = textmodel.style_of(t, {})[0]
    x, y = (nums(t.get("x")) or [0])[0], (nums(t.get("y")) or [0])[0]
    w = textmodel.line_width(t, [r for p in textmodel.parse(t) for r in p.runs])
    anchor = t.get("text-anchor") or "start"
    x0 = x - w / 2 if anchor == "middle" else x - w if anchor == "end" else x
    return x0 + w < 0 or x0 > W or y < 0 or y - size > H


# ---------- one page ----------

def patch_page(path, facts, log):
    tree = etree.parse(str(path))
    root = tree.getroot()
    n = {k: 0 for k in ("3d", "vert", "wrap", "hidden", "table", "chart")}
    for g in list(root.iter(f"{{{SVG}}}g")):
        ref = g.get("data-pptx-source-ref") or ""
        sid = ref.split(":", 1)[1] if ref.startswith("slide:") else None
        fact = facts.get(sid, {})
        f = nums(g.get("data-pptx-frame"))
        if ("lat" in fact or "lon" in fact) and len(f) == 4:
            ky = abs(math.cos(math.radians(fact.get("lat", 0.0))))
            kx = abs(math.cos(math.radians(fact.get("lon", 0.0))))
            if ky < 0.98 or kx < 0.98:
                squash(g, max(kx, 0.05), max(ky, 0.05))
                n["3d"] += 1
                log.append(f"{path.name} {g.get('id')}: 3D camera lat {fact.get('lat', 0):.1f}° lon {fact.get('lon', 0):.1f}° -> squashed x{kx:.2f} y{ky:.2f}")
        elif "iso" in fact:
            log.append(f"{path.name} {g.get('id')}: isometric camera {fact['iso']} left as drawn (not modelled)")
        if len(f) == 4 and g.get("data-pptx-object") == "shape":
            for t in own_text(g):
                if fact.get("vert", "horz") not in ("horz", None) and stack_vertical(t, f):
                    n["vert"] += 1
                elif fact.get("wrap", "square") != "none":
                    aw = needs_wrap(t, f, fact.get("ins", 19.2))
                    if aw:
                        text = "\n".join(p.text for p in textmodel.parse(t))
                        textmodel.replace(t, text, width_override=aw)
                        n["wrap"] += 1
        if g.get("data-pptx-replacement-status", "").startswith("unsupported"):
            g.set("data-sam-unsupported", g.get("data-pptx-replacement-status"))
            n["chart"] += 1
    for img in root.iter(f"{{{SVG}}}image"):
        if (img.get("data-pptx-replacement-status") or "").startswith("unsupported"):
            img.set("data-sam-unsupported", img.get("data-pptx-replacement-status"))
            n["chart"] += 1
    for t in list(root.iter(f"{{{SVG}}}text")):
        if t.getparent() is None or any(etree.QName(a).localname == "metadata" for a in t.iterancestors()):
            continue
        if outside(t):
            top = t
            while top.getparent() is not None and top.getparent() is not root:
                top = top.getparent()
            if top.getparent() is root and not "".join(
                    x for x in top.itertext() if x not in "".join(t.itertext())).strip():
                root.remove(top)
            else:
                t.getparent().remove(t)
            n["hidden"] += 1
    for m in root.iter(f"{{{SVG}}}metadata"):
        try:
            d = json.loads(m.text or "")
        except ValueError:
            continue
        if "semantic-table" not in str(d.get("schema", "")):
            continue
        changed = False
        for row in d.get("rows", []):
            for j, c in enumerate(row):
                if isinstance(c, dict) and c.get("merge_continuation") and set(c) - {"text", "merge_continuation"}:
                    row[j] = {"text": "", "merge_continuation": True}
                    changed = True
        if changed:
            m.text = json.dumps(d, ensure_ascii=False)
            n["table"] += 1
    tree.write(str(path), encoding="utf-8")
    return n


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if not args:
        sys.exit(__doc__)
    lib = Path(args[0])
    flat = lib / "import" / "authoring-svg-flat"
    orig = lib / "import" / "authoring-svg-flat.orig"
    pptx = next((p for p in (lib / "reference.pptx", *lib.glob("*.pptx")) if p.exists()), None)
    if pptx is None:
        sys.exit(f"no reference pptx in {lib}")
    if not orig.exists():
        shutil.copytree(flat, orig)
    if "--dry-run" in sys.argv:
        flat = lib / "import" / "authoring-svg-flat.dry"
    shutil.rmtree(flat, ignore_errors=True)
    shutil.copytree(orig, flat)
    facts = pptx_facts(pptx)
    log, total = [], {}
    for p in sorted(flat.glob("slide_*.svg")):
        no = int(re.findall(r"\d+", p.stem)[0])
        n = patch_page(p, facts.get(no, {}), log)
        for k, v in n.items():
            total[k] = total.get(k, 0) + v
        if any(n.values()):
            log.append(f"{p.name}: " + ", ".join(f"{k} {v}" for k, v in n.items() if v))
    (lib / "import-patches.txt").write_text("\n".join(log) + "\n", encoding="utf-8")
    print(f"patched {flat}: " + ", ".join(f"{k} {v}" for k, v in total.items()) + f"; details in {lib / 'import-patches.txt'}")


if __name__ == "__main__":
    main()
