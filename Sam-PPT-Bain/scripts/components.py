"""Body helpers for `sam_bain.py put`: component markers, automatic group bounds and body lint.

Component markers only spell out the small atoms the deck repeats on every page; where they sit and
how big they are is still decided by hand, page by page. They never place a layout:

  <!--C pill x y w h "文字" [fill=#FFFFFF stroke=#8EA9CF color=#1C4274 size=12 font=R rx=h/2] -->
  <!--C head x y w h "栏头" [fill=#1C4274 color=#FFFFFF size=20 font=M anchor=middle sub="（…）" subsize=13.33] -->
  <!--C num cx cy r "1" [fill=#1C4274 color=#FFFFFF size=r×1.1 font=M] -->
  <!--T x y w size "长句，\\n 强制换行" [font=R fill=#404040 lh=1.45 anchor=start] -->

T wraps with the checker's own estimator (ppt-master text_measure) and writes fixed lines, so the
SVG stays explicit. Anti-template guards (see lint_body / skeleton_report): every page names its main
visual with <!--MAIN group-id-->, the main visual may not be built mostly from component markers, and
pages whose root-group skeleton repeats are reported.
"""
import difflib
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from xml.sax.saxutils import escape

FAMILIES = {"R": "OPPOSans R", "M": "OPPOSans M", "B": "OPPOSans B", "H": "OPPOSans H", "L": "OPPOSans L"}
STACK = ", Microsoft YaHei, sans-serif"
BODY_LEFT, BODY_RIGHT, BODY_BOTTOM = 35.93, 1244.07, 672

COMPONENT_MARK = re.compile(r"<!--([CT]) (.*?) ?-->")
MAIN_MARK = re.compile(r"<!--MAIN (\S+)( lean)? ?-->")
TOKEN = re.compile(r'(\w+)="((?:[^"\\]|\\.)*)"|"((?:[^"\\]|\\.)*)"|(\S+)')
SHAPES = re.compile(r"<(rect|circle|ellipse|path|polygon|polyline|line|use)\b")


class BodyError(Exception):
    pass


_PM_SCRIPTS = None


def init(pm_dir):
    """Point the helpers at ppt-master's scripts/ (for its text_measure estimator)."""
    global _PM_SCRIPTS
    _PM_SCRIPTS = str(Path(pm_dir) / "scripts")


def _measure():
    """ppt-master's text_measure module (the checker's estimator), imported once."""
    if "text_measure" not in sys.modules:
        sys.path.insert(0, _PM_SCRIPTS)
    import text_measure
    return text_measure


def text_width(text, size, font="R"):
    family = FAMILIES.get(font, font)
    weight = "bold" if family.endswith((" B", " H")) else "normal"
    return _measure().measure_text(text, size=size, family=family, weight=weight)


def wrap(text, size, width, font="R"):
    family = FAMILIES.get(font, font)
    weight = "bold" if family.endswith((" B", " H")) else "normal"
    lines = []
    for part in text.split("\\n"):
        got, _, oversized = _measure().wrap_text(part.strip(), size=size, max_width=width, family=family, weight=weight)
        if oversized:
            raise BodyError(f"T: '{oversized[0][0]}' is wider than {width}px at {size}px")
        lines += got
    return lines


def _tokens(s):
    pos, kw = [], {}
    for m in TOKEN.finditer(s):
        k, kv, q, bare = m.groups()
        if k:
            kw[k] = kv.replace('\\"', '"')
        elif q is not None:
            pos.append(q.replace('\\"', '"'))
        elif "=" in bare:
            k, v = bare.split("=", 1)
            kw[k] = v
        else:
            pos.append(bare)
    return pos, kw


def _num(v):
    return f"{float(v):.2f}".rstrip("0").rstrip(".")


def _font_attr(font):
    return "" if font == "R" else f' font-family="{FAMILIES[font]}{STACK}"'


def _label(cx, baseline, text, size, color, font, anchor="middle"):
    return (f'<text x="{_num(cx)}" y="{_num(baseline)}" text-anchor="{anchor}" fill="{color}"{_font_attr(font)} '
            f'font-size="{_num(size)}">{escape(text)}</text>')


def _fit(kind, text, size, font, room):
    w = text_width(text, size, font)
    if w > room:
        raise BodyError(f"{kind} '{text}': text {w:.0f}px wider than the {room:.0f}px it has; widen the box or shorten")


def expand_component(kind, args):
    pos, kw = _tokens(args)
    if kind == "T":
        x, y, w, size = (float(v) for v in pos[:4])
        text, font = pos[4], kw.get("font", "R")
        lines = wrap(text, size, w, font)
        if size <= 12 and len(lines) > 3:
            raise BodyError(f"T at {x},{y}: {len(lines)} lines of {size}px (12px text is capped at 3 lines)")
        dy = size * float(kw.get("lh", 1.45))
        anchor = kw.get("anchor", "start")
        attrs = f'x="{_num(x)}" y="{_num(y)}" fill="{kw.get("fill", "#404040")}"{_font_attr(font)} font-size="{_num(size)}"'
        if anchor != "start":
            attrs += f' text-anchor="{anchor}"'
        rest = "".join(f'<tspan x="{_num(x)}" dy="{_num(dy)}">{escape(l)}</tspan>' for l in lines[1:])
        return f"<text {attrs}>{escape(lines[0])}{rest}</text>"
    name, rest = pos[0], pos[1:]
    if name == "pill":
        x, y, w, h = (float(v) for v in rest[:4])
        text, size, font = rest[4], float(kw.get("size", 12)), kw.get("font", "R")
        rx = float(kw.get("rx", h / 2))
        _fit("pill", text, size, font, w - min(rx, h / 2) - 4)
        stroke = kw.get("stroke", "#8EA9CF")
        sa = "" if stroke == "none" else f' stroke="{stroke}" stroke-width="1"'
        return (f'<rect x="{_num(x)}" y="{_num(y)}" width="{_num(w)}" height="{_num(h)}" rx="{_num(rx)}" '
                f'fill="{kw.get("fill", "#FFFFFF")}"{sa}/>'
                + _label(x + w / 2, y + h / 2 + 0.35 * size, text, size, kw.get("color", "#1C4274"), font))
    if name == "head":
        x, y, w, h = (float(v) for v in rest[:4])
        text, size, font = rest[4], float(kw.get("size", 20)), kw.get("font", "M")
        if not 28 <= h <= 42:
            raise BodyError(f"head '{text}': height {h} outside the 28–42 header band (page-patterns 二 栏头条)")
        sub, subsize = kw.get("sub", ""), float(kw.get("subsize", 13.33))
        need = text_width(text, size, font) + (text_width(sub, subsize, font) if sub else 0)
        if need > w - 16:
            raise BodyError(f"head '{text}{sub}': {need:.0f}px wider than the {w - 16:.0f}px it has")
        anchor = kw.get("anchor", "middle")
        cx = x + w / 2 if anchor == "middle" else x + 14
        label = _label(cx, y + h / 2 + 0.35 * size, text, size, kw.get("color", "#FFFFFF"), font, anchor)
        if sub:
            label = label.replace("</text>", f'<tspan font-size="{_num(subsize)}">{escape(sub)}</tspan></text>')
        return (f'<rect x="{_num(x)}" y="{_num(y)}" width="{_num(w)}" height="{_num(h)}" '
                f'fill="{kw.get("fill", "#1C4274")}"/>' + label)
    if name == "num":
        cx, cy, r = (float(v) for v in rest[:3])
        text, font = rest[3], kw.get("font", "M")
        # Default to an existing type tier so markers never add a font size of their own.
        size = float(kw.get("size", 12 if r <= 12 else 13.33 if r <= 16 else 16))
        _fit("num", text, size, font, 2 * r - 2)
        return (f'<circle cx="{_num(cx)}" cy="{_num(cy)}" r="{_num(r)}" fill="{kw.get("fill", "#1C4274")}"/>'
                + _label(cx, cy + 0.35 * size, text, size, kw.get("color", "#FFFFFF"), font))
    raise BodyError(f"unknown component '{name}' (pill / head / num)")


def expand_components(body):
    n = 0

    def sub(m):
        nonlocal n
        n += 1
        try:
            return expand_component(m.group(1), m.group(2))
        except (IndexError, ValueError) as e:
            raise BodyError(f"bad marker <!--{m.group(1)} {m.group(2)}-->: {e}")
    return COMPONENT_MARK.sub(sub, body), n


# ---------- automatic bounds ----------

def _affine(t):
    m = [1, 0, 0, 1, 0, 0]
    for fn, args in re.findall(r"(\w+)\s*\(([^)]*)\)", t or ""):
        v = [float(x) for x in re.split(r"[\s,]+", args.strip()) if x]
        if fn == "translate":
            n = [1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0]
        elif fn == "scale":
            n = [v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0]
        elif fn == "matrix":
            n = v
        elif fn == "rotate":
            a = math.radians(v[0])
            c, s = math.cos(a), math.sin(a)
            cx, cy = (v[1], v[2]) if len(v) == 3 else (0, 0)
            n = [c, s, -s, c, cx - c * cx + s * cy, cy - s * cx - c * cy]
        else:
            raise BodyError(f"transform {fn}() not supported by auto bounds")
        m = [m[0] * n[0] + m[2] * n[1], m[1] * n[0] + m[3] * n[1], m[0] * n[2] + m[2] * n[3],
             m[1] * n[2] + m[3] * n[3], m[0] * n[4] + m[2] * n[5] + m[4], m[1] * n[4] + m[3] * n[5] + m[5]]
    return m


def _apply(m, x, y):
    return m[0] * x + m[2] * y + m[4], m[1] * x + m[3] * y + m[5]


def _path_points(d):
    pts, x, y = [], 0.0, 0.0
    for cmd, nums in re.findall(r"([MLHVCSQTAZmlhvcsqtaz])([^MLHVCSQTAZmlhvcsqtaz]*)", d):
        v = [float(n) for n in re.findall(r"-?\d*\.?\d+(?:e-?\d+)?", nums)]
        if cmd.islower() and cmd != "z":
            raise BodyError("relative path commands are not supported by auto bounds; give bounds by hand")
        if cmd in "MLT":
            for i in range(0, len(v) - 1, 2):
                x, y = v[i], v[i + 1]
                pts.append((x, y))
        elif cmd == "H":
            for n in v:
                x = n
                pts.append((x, y))
        elif cmd == "V":
            for n in v:
                y = n
                pts.append((x, y))
        elif cmd in "CSQ":
            for i in range(0, len(v) - 1, 2):
                pts.append((v[i], v[i + 1]))
            x, y = pts[-1]
        elif cmd == "A":
            for i in range(0, len(v), 7):
                rx, ry, x, y = v[i], v[i + 1], v[i + 5], v[i + 6]
                pts += [(x - rx, y - ry), (x + rx, y + ry)]
    return pts


def _text_box(el, inh):
    size = float(el.get("font-size", inh["size"]))
    font = el.get("font-family", inh["font"])
    anchor = el.get("text-anchor", inh["anchor"])
    x0, y0 = float(el.get("x", 0)), float(el.get("y", 0))
    lines = [[x0, y0, [(el.text or "", size)]]]
    for t in el:
        if t.tag.endswith("tspan"):
            tsize = float(t.get("font-size", size))
            if t.get("x") is not None:
                lines.append([float(t.get("x")), lines[-1][1] + float(t.get("dy", 0)), [(t.text or "", tsize)]])
            else:
                lines[-1][2].append((t.text or "", tsize))
                for tt in t:
                    lines[-1][2].append((tt.text or "", tsize))
                    lines[-1][2].append((tt.tail or "", tsize))
            lines[-1][2].append((t.tail or "", size))
    short = font.split(",")[0].strip()
    pts = []
    for x, y, runs in lines:
        w = sum(text_width(s, sz, short) for s, sz in runs if s.strip())
        big = max(sz for _, sz in runs)
        left = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
        pts += [(left, y - 0.85 * big), (left + w, y + 0.35 * big)]
    return pts


def _bbox(el, inh, m):
    tag = el.tag.split("}")[-1]
    inh = dict(inh, size=el.get("font-size", inh["size"]), font=el.get("font-family", inh["font"]),
               anchor=el.get("text-anchor", inh["anchor"]))
    m = _matmul(m, _affine(el.get("transform")))
    f = lambda k: float(el.get(k, 0))
    pts = []
    if tag in ("rect", "use", "image"):
        pts = [(f("x"), f("y")), (f("x") + f("width"), f("y") + f("height"))]
        pts += [(pts[0][0], pts[1][1]), (pts[1][0], pts[0][1])]
    elif tag in ("circle", "ellipse"):
        rx, ry = (f("r"), f("r")) if tag == "circle" else (f("rx"), f("ry"))
        pts = [(f("cx") - rx, f("cy") - ry), (f("cx") + rx, f("cy") + ry), (f("cx") - rx, f("cy") + ry), (f("cx") + rx, f("cy") - ry)]
    elif tag == "line":
        pts = [(f("x1"), f("y1")), (f("x2"), f("y2"))]
    elif tag in ("polygon", "polyline"):
        v = [float(n) for n in re.split(r"[\s,]+", el.get("points", "").strip()) if n]
        pts = list(zip(v[::2], v[1::2]))
    elif tag == "path":
        pts = _path_points(el.get("d", ""))
    elif tag == "text":
        pts = _text_box(el, inh)
    out = [_apply(m, x, y) for x, y in pts]
    if tag not in ("text", "tspan"):
        for child in el:
            out += _bbox(child, inh, m)
    return out


def _matmul(a, b):
    return [a[0] * b[0] + a[2] * b[1], a[1] * b[0] + a[3] * b[1], a[0] * b[2] + a[2] * b[3],
            a[1] * b[2] + a[3] * b[3], a[0] * b[4] + a[2] * b[5] + a[4], a[1] * b[4] + a[3] * b[5] + a[5]]


def _parse(body):
    xml = ('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">'
           + re.sub(r"<!--.*?-->", "", body, flags=re.S) + "</svg>")
    try:
        return ET.fromstring(xml)
    except ET.ParseError as e:
        raise BodyError(f"body is not well-formed XML: {e}")


ROOT = {"size": 16, "font": "OPPOSans R", "anchor": "start"}
IDENT = [1, 0, 0, 1, 0, 0]


def group_boxes(body):
    """{root group id: (x, y, w, h)} measured from content."""
    boxes = {}
    for g in _parse(body):
        if g.tag.endswith("}g") and g.get("id"):
            pts = _bbox(g, ROOT, IDENT)
            if pts:
                xs, ys = [p[0] for p in pts], [p[1] for p in pts]
                boxes[g.get("id")] = (min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))
    return boxes


def auto_bounds(body):
    """Replace data-pptx-bounds="auto" on root groups with the measured content box (+1 px)."""
    if 'data-pptx-bounds="auto"' not in body:
        return body, 0
    boxes, n = group_boxes(body), 0

    def sub(m):
        nonlocal n
        gid = m.group(1)
        if gid not in boxes:
            raise BodyError(f"auto bounds: group {gid} has no measurable content")
        x, y, w, h = boxes[gid]
        n += 1
        return f'<g id="{gid}"{m.group(2)}data-pptx-bounds="{_num(x - 1)} {_num(y - 1)} {_num(w + 2)} {_num(h + 2)}"'
    return re.sub(r'<g id="([^"]+)"([^>]*?)data-pptx-bounds="auto"', sub, body), n


# ---------- lint ----------

def _root_groups(src):
    """(id, text) of each root-level <g> in the hand-written source, markers kept."""
    out, depth, start, gid = [], 0, 0, None
    for m in re.finditer(r'<g\b[^>]*?(/?)>|</g>', src):
        tok = m.group(0)
        if tok.startswith("</g"):
            depth -= 1
            if depth == 0:
                out.append((gid, src[start:m.end()]))
        elif not m.group(1):
            if depth == 0:
                start = m.start()
                gid = (re.search(r'id="([^"]+)"', tok) or [None, None])[1]
            depth += 1
    return out


def _marker_share(text):
    comps = len(re.findall(r"<!--C ", text))
    hand = len(SHAPES.findall(re.sub(r"<!--.*?-->", "", text, flags=re.S))) + len(re.findall(r"<!--P ", text))
    total = comps + hand
    return comps / total if total else 0.0, comps, total


def lint_body(src, expanded, thesis):
    """Findings for one page; src is the hand-written body (markers intact), expanded is after expansion."""
    out = []
    for d in re.findall(r'<path\b[^>]*\bd="([^"]+)"[^>]*marker-(?:start|end)=', expanded) + \
            re.findall(r'<path\b[^>]*marker-(?:start|end)=[^>]*\bd="([^"]+)"', expanded):
        if len(re.findall(r"[Mm]", d)) > 1:
            out.append(f"[ERROR] path with several sub-paths carries an arrow marker (PowerPoint draws one head per "
                       f"sub-path): split it into a plain path plus one marked line — d=\"{d[:60]}\"")
    for g in re.findall(r"<g\b[^>]*marker-(?:start|end)=", expanded):
        out.append("[ERROR] marker-start/end written on <g>; put it on the <line>/<path> itself")
    share, comps, total = _marker_share(src)
    mains = MAIN_MARK.findall(src)
    if not mains:
        out.append("[WARN] no <!--MAIN group-id--> naming this page's main visual (anti-template guard)")
        return out
    gid, lean = mains[0]
    groups = dict(_root_groups(src))
    if gid not in groups:
        out.append(f"[WARN] MAIN names '{gid}', which is not a root group")
        return out
    gshare, gc, gt = _marker_share(groups[gid])
    if gshare >= 0.5 and gt:
        out.append(f"[WARN] main visual '{gid}' is {gc}/{gt} component markers: build the main construction by hand "
                   f"(page-patterns 三B), markers are only for the small atoms around it")
    if total and share > 0.6:
        out.append(f"[WARN] {comps}/{total} shapes on this page come from component markers: the page reads as "
                   f"pills and bars only — re-check the construction (rules 五 返工时先换构造)")
    if not lean:
        box = group_boxes(expanded).get(gid)
        top = 166 if thesis else 96
        if box:
            share_area = box[2] * box[3] / ((BODY_RIGHT - BODY_LEFT) * (BODY_BOTTOM - top))
            if share_area < 0.35:
                out.append(f"[WARN] main visual '{gid}' covers {share_area:.0%} of the body area (< 35%; "
                           f"normal pages 45–60%, dense pages ≥ 35–40%); mark lean pages with <!--MAIN id lean-->")
    return out


def skeleton_report(pages):
    """Pages whose root-group layout repeats (bounds snapped to a 60 px grid, 3+ pages alike)."""
    sigs = {}
    for page in pages:
        svg = page.read_text(encoding="utf-8")
        body = svg.split("<!-- body:", 1)[-1]
        boxes = re.findall(r'<g id="[^"]+"[^>]*data-pptx-bounds="([\d.\- ]+)"', body)
        sig = tuple(sorted(tuple(round(float(v) / 60) for v in b.split()) for b in boxes))
        sigs.setdefault(sig, []).append(page.stem)
    return [names for sig, names in sigs.items() if sig and len(names) >= 3]


def suggest_icons(name, lib_dir):
    """Closest names in the icon library for a missing one."""
    stems = [p.stem for p in Path(lib_dir).glob("*.svg")]
    base = name.split("/")[-1]
    return difflib.get_close_matches(base, stems, n=4, cutoff=0.5) or [s for s in stems if base.split("-")[0] in s][:4]
