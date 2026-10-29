"""Add reference-style parts to a page in one call (step 4, step 7): native arrows, chevrons, number
badges, icon discs, tag blocks, pills, tinted panels, label rows and marked bullet lists.

  python add_parts.py <page.svg> <group-id> [--under <id>] "<part> ; <part> ; ..."

All parts of one call go into one new root group <g id="<group-id>" data-pptx-bounds=...> (replacing a
group of that id from an earlier call), so the exporter keeps them (never inside an imported shape
group). --under puts the group just below element <id> in z-order (panels behind a module).
Block arrows, chevrons and triangles come from ppt-master's preset helper (native, editable, counted
as connectors); everything else is ordinary SVG the exporter maps natively. Solid circles and solid
blocks get the reference's shadow (shadowA, page-zoning.md 第六节第 5 条). Text must be outline wording
(check_text.py); "\\n" breaks a line. Colours: N = #1C4274 navy, R = #A23424 brick red, L = #C4D7F1 light
blue, P = #F4D1CC light pink, M = #89B0E3 mid blue, W = #FFFFFF, or any #RRGGBB.

  arrow  right|left|up|down|both|updown X Y W H [colour] solid block arrow (both = ↔, updown = ↕)
  chevron X Y W H colour "text" [size]                    chevron step with white bold text
  tri    down|up|right|left X Y W H [colour]              small solid triangle (pointer, "leads to")
  line   X1 Y1 X2 Y2 [colour] [width] [arrow|dot|none]    straight leader / connector, line-end marker
  badge  CX CY D colour "01" [size]                       solid number circle, white bold text
  icon   CX CY D colour lib/name [icon-colour]            solid disc with a library icon (D = disc size,
                                                          icon white); colour none = bare icon of size D
                                                          (navy unless icon-colour, e.g. W on a solid circle)
  tag    X Y W H colour "text" [size] [left]              solid title block, white bold text
  pill   X Y W H colour "text" [text-colour] [size]       rounded tag (tint fill), centred text
  panel  X Y W H colour [opacity]                         tinted panel, no outline
  label  X Y W H "label" "body" [colour] [label-w] [size] solid label block + tinted body row
  bullets X Y W "item|item|..." [size] [marker-colour] [line-step]
                                                          marked list, one marker per item
  text   X Y "text" [size] [colour] [bold] [start|middle|end]

Icons are copied into <project>/icons with ppt-master's icon_sync.py automatically.
Example:
  python add_parts.py 07_scope.svg p07-kit "badge 60 230 28 R 1 ; arrow right 590 300 24 20 N ; \\
      label 852 420 392 44 \"已启用审计\" \"以已有 UPL/SCMON、SUSG 聚合数据为主\" R"
"""
import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

from lxml import etree

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pm import ppt_master_dir  # noqa: E402

SVG = "http://www.w3.org/2000/svg"
S = "{%s}" % SVG
COL = {"N": "#1C4274", "R": "#A23424", "L": "#C4D7F1", "P": "#F4D1CC", "M": "#89B0E3", "W": "#FFFFFF",
       "G": "#595959", "K": "#262626"}
TINT = {"#1C4274": ("#C4D7F1", "0.35"), "#A23424": ("#F4D1CC", "0.55"), "#89B0E3": ("#C4D7F1", "0.35")}
REG, BOLD = '"OPPOSans R", sans-serif', '"OPPOSans B", sans-serif'


def c(v):
    v = v.strip()
    return COL.get(v.upper(), v) if v else v


def f(v):
    return f"{float(v):.2f}".rstrip("0").rstrip(".")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def text_el(x, y, s, size, fill, bold=False, anchor="start", step=None):
    lines = s.split("\\n") if "\\n" in s else s.split("\n")
    step = step or size * 1.45
    fam = BOLD if bold else REG
    out = (f'<text x="{f(x)}" y="{f(y)}" font-size="{f(size)}" fill="{fill}" text-anchor="{anchor}" '
           f'font-family="{esc(fam)}"' + (' font-weight="bold"' if bold else "") + f'>{esc(lines[0])}')
    for ln in lines[1:]:
        out += f'<tspan x="{f(x)}" dy="{f(step)}">{esc(ln)}</tspan>'
    return out + "</text>"


def centred_text(x, y, w, h, s, size, fill, bold=True, anchor="middle", pad=10):
    lines = (s.split("\\n") if "\\n" in s else s.split("\n"))
    step = size * 1.3
    top = y + h / 2 - step * (len(lines) - 1) / 2 + size * 0.36
    tx = x + w / 2 if anchor == "middle" else x + pad
    return text_el(tx, top, s, size, fill, bold, anchor, step)


class Kit:
    def __init__(self, gid):
        self.gid, self.n, self.xml, self.presets, self.boxes, self.icons = gid, 0, [], [], [], []

    def nid(self):
        self.n += 1
        return f"{self.gid}-{self.n}"

    def box(self, x, y, w, h):
        self.boxes.append((float(x), float(y), float(w), float(h)))

    def preset(self, prst, x, y, w, h, fill, shadow=False, rotate=0):
        i = self.nid()
        item = {"preset": prst, "id": i, "frame": [float(x), float(y), float(w), float(h)], "fill": fill, "stroke": "none"}
        if shadow:
            item["filter_id"] = "shadowA"
        self.presets.append(item)
        self.xml.append(("preset", i, rotate, (float(x) + float(w) / 2, float(y) + float(h) / 2)))
        self.box(x, y, w, h)

    def raw(self, s):
        self.xml.append(("raw", s))

    # ---------- parts ----------
    def arrow(self, d, x, y, w, h, col="N"):
        prst = {"right": "rightArrow", "left": "leftArrow", "up": "upArrow", "down": "downArrow",
                "both": "leftRightArrow", "updown": "upDownArrow"}[d]
        self.preset(prst, x, y, w, h, c(col))

    def chevron(self, x, y, w, h, col, s, size="14"):
        self.preset("chevron", x, y, w, h, c(col), shadow=True)
        x, y, w, h = map(float, (x, y, w, h))
        self.raw(centred_text(x + h * 0.25, y, w - h * 0.25, h, s, float(size), "#FFFFFF"))

    def tri(self, d, x, y, w, h, col="N"):
        if d == "down":
            self.preset("flowChartMerge", x, y, w, h, c(col))
        elif d == "up":
            self.preset("triangle", x, y, w, h, c(col))
        else:  # a right / left pointer is an up triangle turned on its centre (frame stays unrotated)
            x, y, w, h = map(float, (x, y, w, h))
            cx, cy = x + w / 2, y + h / 2
            self.preset("triangle", cx - h / 2, cy - w / 2, h, w, c(col), rotate=90 if d == "right" else 270)

    def line(self, x1, y1, x2, y2, col="N", width="1.5", end="arrow"):
        col = c(col)
        mk = ""
        if end in ("arrow", "dot"):
            mid = f"{self.gid}-m{self.n + 1}"
            shape = ('<polygon points="0,0 10,5 0,10" fill="%s"/>' % col) if end == "arrow" else \
                ('<circle cx="5" cy="5" r="4" fill="%s"/>' % col)
            self.raw(f'<defs><marker id="{mid}" viewBox="0 0 10 10" refX="{10 if end == "arrow" else 5}" refY="5" '
                     f'markerWidth="4" markerHeight="4" orient="auto" markerUnits="strokeWidth">{shape}</marker></defs>')
            mk = f' marker-end="url(#{mid})"'
        i = self.nid()
        self.raw(f'<line id="{i}" x1="{f(x1)}" y1="{f(y1)}" x2="{f(x2)}" y2="{f(y2)}" stroke="{col}" '
                 f'stroke-width="{f(width)}" fill="none"{mk}/>')
        x1, y1, x2, y2 = map(float, (x1, y1, x2, y2))
        self.box(min(x1, x2), min(y1, y2), abs(x2 - x1) or 1, abs(y2 - y1) or 1)

    def badge(self, cx, cy, d, col, s, size=None):
        cx, cy, d = map(float, (cx, cy, d))
        self.raw(f'<circle id="{self.nid()}" cx="{f(cx)}" cy="{f(cy)}" r="{f(d / 2)}" fill="{c(col)}" filter="url(#shadowA)"/>')
        size = float(size) if size else round(d * 0.46, 1)
        self.raw(text_el(cx, cy + size * 0.36, s, size, "#FFFFFF", True, "middle"))
        self.box(cx - d / 2, cy - d / 2, d, d)

    def icon(self, cx, cy, d, col, name, icol=None):
        cx, cy, d = map(float, (cx, cy, d))
        if col.lower() != "none":
            self.raw(f'<circle id="{self.nid()}" cx="{f(cx)}" cy="{f(cy)}" r="{f(d / 2)}" fill="{c(col)}" filter="url(#shadowA)"/>')
            s, icol = round(d * 0.56, 1), icol or "W"
        else:  # bare icon: navy unless a colour is given (W for an icon sitting on a solid shape)
            s, icol = d, icol or "N"
        self.raw(f'<use data-icon="{name}" x="{f(cx - s / 2)}" y="{f(cy - s / 2)}" width="{f(s)}" height="{f(s)}" fill="{c(icol)}"/>')
        self.icons.append(name)
        self.box(cx - d / 2, cy - d / 2, d, d)

    def tag(self, x, y, w, h, col, s, size="14", align="middle"):
        x, y, w, h = map(float, (x, y, w, h))
        self.raw(f'<rect id="{self.nid()}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{c(col)}" filter="url(#shadowA)"/>')
        self.raw(centred_text(x, y, w, h, s, float(size), "#FFFFFF", True, "start" if align == "left" else "middle"))
        self.box(x, y, w, h)

    def pill(self, x, y, w, h, col, s, tcol=None, size="12"):
        x, y, w, h = map(float, (x, y, w, h))
        col = c(col)
        light = col.upper() in ("#C4D7F1", "#F4D1CC", "#FFFFFF")
        op = "" if not light else (' fill-opacity="0.6"' if col.upper() != "#FFFFFF" else "")
        tcol = c(tcol) if tcol else ("#1C4274" if col.upper() in ("#C4D7F1", "#FFFFFF") else "#A23424" if col.upper() == "#F4D1CC" else "#FFFFFF")
        self.raw(f'<rect id="{self.nid()}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" rx="{f(h / 2)}" fill="{col}"{op}/>')
        self.raw(centred_text(x, y, w, h, s, float(size), tcol, True))
        self.box(x, y, w, h)

    def panel(self, x, y, w, h, col="L", op="0.3"):
        self.raw(f'<rect id="{self.nid()}" x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="{c(col)}" fill-opacity="{op}"/>')
        self.box(x, y, w, h)

    def label(self, x, y, w, h, lab, body, col="N", lw="96", size="12"):
        x, y, w, h, lw, size = map(float, (x, y, w, h, lw, size))
        col = c(col)
        tint, op = TINT.get(col.upper(), ("#C4D7F1", "0.35"))
        self.raw(f'<rect id="{self.nid()}" x="{f(x + lw)}" y="{f(y)}" width="{f(w - lw)}" height="{f(h)}" fill="{tint}" fill-opacity="{op}"/>')
        self.raw(f'<rect id="{self.nid()}" x="{f(x)}" y="{f(y)}" width="{f(lw)}" height="{f(h)}" fill="{col}" filter="url(#shadowA)"/>')
        self.raw(centred_text(x, y, lw, h, lab, size + 1, "#FFFFFF", True))
        self.raw(centred_text(x + lw, y, w - lw, h, body, size, "#262626", False, "start", 12))
        self.box(x, y, w, h)

    def bullets(self, x, y, w, items, size="12", mcol="N", step=None):
        x, y, w, size = map(float, (x, y, w, size))
        step = float(step) if step else size * 1.9
        cy = y
        for it in items.split("|"):
            lines = it.split("\\n") if "\\n" in it else it.split("\n")
            self.raw(f'<rect id="{self.nid()}" x="{f(x)}" y="{f(cy - size * 0.62)}" width="{f(size * 0.45)}" '
                     f'height="{f(size * 0.45)}" fill="{c(mcol)}"/>')
            self.raw(text_el(x + size * 1.1, cy, it, size, "#262626", False, "start", size * 1.45))
            cy += step + size * 1.45 * (len(lines) - 1)
        self.box(x, y - size, w, cy - y)

    def text(self, x, y, s, size="12", col="K", bold="", anchor="start"):
        self.raw(text_el(float(x), float(y), s, float(size), c(col), bold == "bold", anchor))
        self.box(float(x), float(y) - float(size), len(s) * float(size), float(size) * 1.4)


def render_presets(items):
    if not items:
        return {}
    pm = ppt_master_dir()
    r = subprocess.run([sys.executable, str(pm / "scripts" / "preset_shape_svg.py"), "render-batch", "--input", "-"],
                       input=json.dumps(items), capture_output=True, text=True, encoding="utf-8")
    if r.returncode or not r.stdout.strip():
        sys.exit("preset helper failed: " + (r.stderr or r.stdout))
    frags = {}
    for m in re.finditer(r'<g id="([^"]+)".*?</g>', r.stdout, re.S):
        frags[m.group(1)] = m.group(0)
    return frags


def ensure_defs(root):
    defs = root.find(S + "defs")
    if defs is None:
        defs = etree.Element(S + "defs")
        root.insert(0, defs)
    have = {e.get("id") for e in defs}
    for fid, op in (("shadowA", "0.4"), ("shadowB", "0.22")):
        if fid not in have:
            defs.append(etree.fromstring(
                f'<filter xmlns="{SVG}" id="{fid}" x="-10%" y="-20%" width="130%" height="160%">'
                f'<feDropShadow dx="2.8" dy="2.8" stdDeviation="2.7" flood-color="#000000" flood-opacity="{op}"/></filter>'))
    return defs


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if len(a) < 3:
        sys.exit(__doc__)
    page, gid = Path(a[0]), a[1]
    under = None
    if "--under" in a:
        i = a.index("--under")
        under = a[i + 1]
        del a[i:i + 2]
    kit = Kit(gid)
    for cmd in a[2].split(" ; "):
        tok = shlex.split(cmd.strip(), posix=True)
        if not tok:
            continue
        getattr(kit, tok[0])(*tok[1:])
    frags = render_presets(kit.presets)
    body = []
    for item in kit.xml:
        if item[0] == "raw":
            body.append(item[1])
        else:
            _, i, rot, (cx, cy) = item
            fr = frags[i]
            if rot:
                fr = f'<g transform="rotate({rot} {f(cx)} {f(cy)})">{fr}</g>'
            body.append(fr)
    xs = [b[0] for b in kit.boxes] + [b[0] + b[2] for b in kit.boxes]
    ys = [b[1] for b in kit.boxes] + [b[1] + b[3] for b in kit.boxes]
    bounds = f"{f(min(xs))} {f(min(ys))} {f(max(xs) - min(xs))} {f(max(ys) - min(ys))}"
    tree = etree.parse(str(page))
    root = tree.getroot()
    defs = ensure_defs(root)
    grp = etree.fromstring(f'<g xmlns="{SVG}" id="{gid}" data-pptx-bounds="{bounds}">' + "".join(body) + "</g>")
    for d in grp.findall(S + "defs"):  # markers go to the page defs
        for mk in d:
            defs.append(mk)
        grp.remove(d)
    for old in root.xpath(f'//*[@id="{gid}"]'):
        old.getparent().remove(old)
    if under:
        hit = root.xpath(f'//*[@id="{under}"]')
        if not hit:
            sys.exit(f"no element {under}")
        anchor = hit[0]
        while anchor.getparent() is not root:
            anchor = anchor.getparent()
        anchor.addprevious(grp)
    else:
        root.append(grp)
    tree.write(str(page), encoding="utf-8")
    if kit.icons:
        proj = page.resolve().parent.parent
        subprocess.run([sys.executable, str(ppt_master_dir() / "scripts" / "icon_sync.py"), str(proj), *sorted(set(kit.icons))],
                       capture_output=True, text=True, encoding="utf-8")
    print(f"{page.name}: {gid} with {kit.n} part(s), {len(kit.presets)} native preset(s), "
          f"{len(set(kit.icons))} icon(s); bounds {bounds}")


if __name__ == "__main__":
    main()
