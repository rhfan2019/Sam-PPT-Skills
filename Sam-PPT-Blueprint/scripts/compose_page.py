"""Compose one page from modules of several reference pages (step 3).

  python compose_page.py <out.svg> <authoring-svg-flat> shell=NN  NN:x,y,w,h@X,Y[,W] ...

shell=NN            keep page NN's background, header and footer (top-level elements centred above
                    y=CHROME_TOP or below y=CHROME_BOTTOM); everything else on it is dropped
NN:x,y,w,h[+x,y,w,h]@X,Y[,W]
                    take from page NN every top-level element centred in the box x,y,w,h with at least
                    60% of its area inside (a backplate shared with neighbouring modules stays behind;
                    a second box after "+" adds an L-shaped part) and place the box's top-left corner at X,Y; with W the module is scaled
                    uniformly to width W (coordinates, sizes, font sizes, strokes are rewritten, no
                    transform is added)

Each source page goes through start_page.strip first (pictures, crop wrappers, bindings to removed
shapes and so on). A module's ids get an "mK-" prefix and the defs it uses (gradients, filters,
markers, clip paths) are copied with the same prefix, so modules from different pages never clash.
A comment <!-- module K: slide_NN.svg x,y,w,h -> X,Y,W --> per module is read by check_reuse.py.
"""
import copy
import re
import sys
from pathlib import Path

from lxml import etree

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from start_page import strip  # noqa: E402

SVG = "http://www.w3.org/2000/svg"
XLINK = "http://www.w3.org/1999/xlink"
NUM = r"-?\d*\.?\d+(?:[eE][-+]?\d+)?"
CHROME_TOP, CHROME_BOTTOM = 95, 675
XS = ("x", "x1", "x2", "cx", "fx")
YS = ("y", "y1", "y2", "cy", "fy")
LENGTHS = ("width", "height", "r", "rx", "ry", "font-size", "stroke-width", "dx", "dy", "letter-spacing")


def local(e):
    return etree.QName(e).localname if isinstance(e.tag, str) else ""


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def nums(s):
    return [float(v) for v in re.findall(NUM, s or "")]


def parse(path):
    text, _ = strip(Path(path).read_text(encoding="utf-8"), Path(path).parent.parent / "images")
    return etree.fromstring(text.encode("utf-8"), etree.XMLParser(remove_blank_text=False, huge_tree=True))


# ---------- where an element sits ----------

def inside(e, x, y, w, h, share=0.6):
    """Centre inside the box and at least `share` of the frame's area inside it: a module keeps its own
    panels even when the box is a few px off, and leaves behind backplates shared with neighbours."""
    c = centre(e)
    if not c or not (x <= c[0] <= x + w and y <= c[1] <= y + h):
        return False
    f = nums(e.get("data-pptx-frame"))
    if len(f) != 4:
        return True
    fw, fh = max(f[2], 1), max(f[3], 1)
    ox = max(0, min(f[0] + fw, x + w) - max(f[0], x))
    oy = max(0, min(f[1] + fh, y + h) - max(f[1], y))
    return ox * oy >= share * fw * fh


def centre(e):
    f = nums(e.get("data-pptx-frame"))
    if len(f) == 4:
        return f[0] + f[2] / 2, f[1] + f[3] / 2
    for d in e.iter():
        if not isinstance(d.tag, str):
            continue
        f = nums(d.get("data-pptx-frame"))
        if len(f) == 4:
            return f[0] + f[2] / 2, f[1] + f[3] / 2
        if d.get("x") is not None and d.get("y") is not None:
            x, y = nums(d.get("x")), nums(d.get("y"))
            if x and y:
                return x[0], y[0]
    return None


def is_background(e):
    f = nums(e.get("data-pptx-frame"))
    w = nums(e.get("width"))
    return (len(f) == 4 and f[2] >= 1270) or (w and w[0] >= 1270) or (not f and local(e) == "rect")


# ---------- affine rewrite p -> s*p + (tx, ty) ----------

def map_path(d, s, tx, ty):
    out, cmd, i = [], None, 0
    for tok in re.findall(rf"[A-Za-z]|{NUM}", d):
        if tok.isalpha():
            cmd, i = tok, 0
            out.append(tok)
            continue
        v = float(tok)
        if cmd in "MLTCSQ":
            v = v * s + (tx if i % 2 == 0 else ty)
        elif cmd == "H":
            v = v * s + tx
        elif cmd == "V":
            v = v * s + ty
        elif cmd == "A":
            k = i % 7
            v = v * s if k < 2 else v if k < 5 else v * s + (tx if k == 5 else ty)
        elif cmd and cmd.islower():
            k = i % 7
            v = v if cmd == "a" and 2 <= k <= 4 else v * s
        out.append(fmt(v))
        i += 1
    return " ".join(out)


def map_transform(t, s, tx, ty):
    def rot(m):
        a, cx, cy = nums(m.group(1))
        return f"rotate({fmt(a)} {fmt(cx * s + tx)} {fmt(cy * s + ty)})"

    def flip(m):
        x, y = nums(m.group(1))
        sc = m.group(2)
        return f"translate({fmt(x * s + tx)} {fmt(y * s + ty)}) scale({sc}) translate({fmt(-(x * s + tx))} {fmt(-(y * s + ty))})"

    t = re.sub(r"rotate\(([^)]*)\)", rot, t)
    return re.sub(r"translate\(([^)]*)\)\s*scale\(([^)]*)\)\s*translate\([^)]*\)", flip, t)


def map_el(e, s, tx, ty):
    for k in XS:
        if e.get(k) is not None and re.fullmatch(NUM, e.get(k).strip()):
            e.set(k, fmt(float(e.get(k)) * s + tx))
    for k in YS:
        if e.get(k) is not None and re.fullmatch(NUM, e.get(k).strip()):
            e.set(k, fmt(float(e.get(k)) * s + ty))
    if s != 1:
        for k in LENGTHS:
            v = e.get(k)
            if v is not None and re.fullmatch(rf"\s*{NUM}\s*(px)?\s*", v):
                e.set(k, fmt(nums(v)[0] * s))
        if e.get("stroke-dasharray") and e.get("stroke-dasharray") != "none":
            e.set("stroke-dasharray", " ".join(fmt(v * s) for v in nums(e.get("stroke-dasharray"))))
        if e.get("stdDeviation"):
            e.set("stdDeviation", " ".join(fmt(v * s) for v in nums(e.get("stdDeviation"))))
    if e.get("d"):
        e.set("d", map_path(e.get("d"), s, tx, ty))
    if e.get("points"):
        p = nums(e.get("points"))
        e.set("points", " ".join(fmt(v * s + (tx if i % 2 == 0 else ty)) for i, v in enumerate(p)))
    for k in ("data-pptx-frame", "data-pptx-bounds"):
        f = nums(e.get(k))
        if len(f) == 4:
            e.set(k, " ".join(fmt(v) for v in (f[0] * s + tx, f[1] * s + ty, f[2] * s, f[3] * s)))
    if e.get("transform"):
        e.set("transform", map_transform(e.get("transform"), s, tx, ty))


# ---------- ids and defs ----------

REF = re.compile(r"url\(#([^)]+)\)")


def refs_of(e):
    out = set()
    for d in e.iter():
        if not isinstance(d.tag, str):
            continue
        for k, v in d.attrib.items():
            out.update(REF.findall(v))
            if k in ("href", f"{{{XLINK}}}href") and v.startswith("#"):
                out.add(v[1:])
    return out


def rename(e, prefix, ids):
    for d in e.iter():
        if not isinstance(d.tag, str):
            continue
        for k, v in list(d.attrib.items()):
            if k == "id":
                d.set(k, prefix + v)
            elif k in ("href", f"{{{XLINK}}}href") and v.startswith("#") and v[1:] in ids:
                d.set(k, "#" + prefix + v[1:])
            elif k in ("data-pptx-start-shape-id", "data-pptx-end-shape-id"):
                d.set(k, prefix + v)
            elif "url(#" in v:
                d.set(k, REF.sub(lambda m: f"url(#{prefix + m.group(1)})" if m.group(1) in ids else m.group(0), v))


def take_defs(src_root, wanted):
    """Defs the module uses, closed over references between defs (gradient href, marker fill url)."""
    by_id = {d.get("id"): d for d in src_root.iter() if isinstance(d.tag, str) and d.get("id")
             and any(local(a) == "defs" for a in d.iterancestors())}
    out, todo = {}, list(wanted)
    while todo:
        i = todo.pop()
        if i in out or i not in by_id:
            continue
        out[i] = copy.deepcopy(by_id[i])
        todo.extend(refs_of(out[i]))
    return out


def user_space(d):
    return d.get("gradientUnits") == "userSpaceOnUse" or (local(d) == "clipPath" and d.get("clipPathUnits") != "objectBoundingBox")


# ---------- main ----------

def parse_module(tok):
    m = re.fullmatch(rf"(\d+):({NUM}),({NUM}),({NUM}),({NUM})(?:\+({NUM}),({NUM}),({NUM}),({NUM}))?@({NUM}),({NUM})(?:,({NUM}))?", tok)
    if not m:
        sys.exit(f"bad module spec {tok!r}; expected NN:x,y,w,h[+x,y,w,h]@X,Y[,W]")
    g = m.groups()
    extra = [float(v) for v in g[5:9]] if g[5] else None
    return int(g[0]), [float(v) for v in g[1:5]], extra, float(g[9]), float(g[10]), float(g[11]) if g[11] else None


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    out, lib, specs = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
    shell_no = next((int(t.split("=")[1]) for t in specs if t.startswith("shell=")), None)
    if shell_no is None:
        sys.exit("give shell=NN: the page whose background, header and footer the new page keeps")
    page = lambda n: lib / f"slide_{n:02d}.svg"  # noqa: E731
    root = parse(page(shell_no))
    defs = root.find(f"{{{SVG}}}defs")
    if defs is None:
        defs = etree.SubElement(root, f"{{{SVG}}}defs")
        root.insert(0, defs)
    for e in list(root):
        if local(e) in ("defs", "metadata", "title", "desc") or not isinstance(e.tag, str):
            continue
        c = centre(e)
        if is_background(e) or (c and (c[1] < CHROME_TOP or c[1] > CHROME_BOTTOM)):
            continue
        root.remove(e)
    notes = [f"shell: slide_{shell_no:02d}.svg"]

    for k, tok in enumerate([t for t in specs if not t.startswith("shell=")], 1):
        n, (x, y, w, h), extra, X, Y, W = parse_module(tok)
        src = parse(page(n))
        s = W / w if W else 1.0
        tx, ty = X - x * s, Y - y * s
        picked = []
        for e in src:
            if not isinstance(e.tag, str) or local(e) in ("defs", "metadata", "title", "desc") or is_background(e):
                continue
            if inside(e, x, y, w, h) or (extra and inside(e, *extra)):
                picked.append(copy.deepcopy(e))
        if not picked:
            sys.exit(f"module {k} ({tok}): no top-level element lies inside the box")
        used = set()
        for e in picked:
            used |= refs_of(e)
        mdefs = take_defs(src, used)
        prefix = f"m{k}-"
        ids = set(mdefs) | {d.get("id") for e in picked for d in e.iter() if isinstance(d.tag, str) and d.get("id")}
        for e in picked:
            for d in e.iter():
                if isinstance(d.tag, str):
                    map_el(d, s, tx, ty)
            rename(e, prefix, ids)
        for i, d in mdefs.items():
            if user_space(d):
                for c in d.iter():
                    if isinstance(c.tag, str):
                        map_el(c, s, tx, ty)
            elif local(d) == "filter":  # region is in %, only offsets and blur scale
                for c in d.iter():
                    if isinstance(c.tag, str) and c is not d:
                        map_el(c, s, 0, 0)
            rename(d, prefix, ids)
            defs.append(d)
        own = {d.get("id") for e in picked for d in e.iter() if isinstance(d.tag, str) and d.get("id")}
        dangling = 0
        for e in picked:
            for d in e.iter():
                if not isinstance(d.tag, str):
                    continue
                for a in ("start", "end"):
                    if d.get(f"data-pptx-{a}-shape-id") and d.get(f"data-pptx-{a}-shape-id") not in own:
                        for suffix in ("shape-id", "shape-scope", "site"):
                            d.attrib.pop(f"data-pptx-{a}-{suffix}", None)
                        dangling += 1
        spec = f"slide_{n:02d}.svg {fmt(x)},{fmt(y)},{fmt(w)},{fmt(h)} -> {fmt(X)},{fmt(Y)},{fmt(w * s)}"
        if extra:
            spec += f" +{','.join(fmt(v) for v in extra)}"
        root.append(etree.Comment(f" module {k}: {spec} "))
        for e in picked:
            root.append(e)
        warn = f"; font sizes x{s:.2f}" if s < 0.85 else ""
        notes.append(f"module {k}: {spec}: {len(picked)} element(s), {len(mdefs)} def(s){warn}"
                     + (f", {dangling} binding(s) to shapes outside the box dropped" if dangling else ""))

    root.insert(0, etree.Comment(" composed: " + " | ".join(notes) + " "))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(etree.tostring(root, encoding="utf-8"))
    print("\n".join(notes))


if __name__ == "__main__":
    main()
