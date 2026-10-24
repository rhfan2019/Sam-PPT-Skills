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


# ---------- layout lint (2026-10-23): what the written rules kept missing ----------
# Every finding is a WARN for the author to look at; nothing here moves or resizes anything.

SMALL_PX = 12.01          # below the rules' 13.33 px caption floor
SMALL_SHARE_MAX = 0.40    # reference deck: ≈ 30–35 % of characters at ≤ 12 px
MAX_BLOCKS = 5
MIN_COVER = 0.5          # share of the body under coloured panels / bars (rules 二.8: about 60–75 %)
CARD_EMPTY_MAX = 1 / 3


def _lum(color):
    m = re.fullmatch(r"#([0-9a-fA-F]{6})", (color or "").strip())
    if not m:
        return None
    r, g, b = (int(m.group(1)[i:i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _prims(body):
    """Flatten the expanded body: one record per drawn element, in paint order, slide coordinates."""
    out = []

    def walk(el, inh, m, root, prst):
        tag = el.tag.split("}")[-1]
        m = _matmul(m, _affine(el.get("transform")))
        op = inh["opacity"] * float(el.get("opacity", 1))
        inh = dict(inh, size=el.get("font-size", inh["size"]), font=el.get("font-family", inh["font"]),
                   anchor=el.get("text-anchor", inh["anchor"]), fill=el.get("fill", inh["fill"]),
                   fop=float(el.get("fill-opacity", inh["fop"])), stroke=el.get("stroke", inh["stroke"]),
                   sw=float(el.get("stroke-width", inh["sw"])), opacity=op)
        prst = el.get("data-pptx-prst") or prst
        if tag == "g":
            for child in el:
                walk(child, inh, m, root, prst)
            return
        if tag in ("defs", "title", "desc"):
            return
        local = dict(inh)
        local.pop("fill"), local.pop("fop"), local.pop("stroke"), local.pop("sw"), local.pop("opacity")
        pts = [_apply(m, x, y) for x, y in _bbox(el, local, IDENT)]
        if not pts:
            return
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        rec = {"tag": tag, "box": (min(xs), min(ys), max(xs), max(ys)), "root": root, "prst": prst,
               "fill": inh["fill"], "fop": inh["fop"] * op, "stroke": inh["stroke"], "sw": inh["sw"], "el": el,
               "m": m, "icon": tag == "use"}
        if tag == "text":
            runs = [(el.text or "", float(inh["size"]))]
            for t in el:
                runs.append((t.text or "", float(t.get("font-size", inh["size"]))))
                runs.append((t.tail or "", float(inh["size"])))
            rec["runs"] = [(s, sz) for s, sz in runs if s.strip()]
            rec["base"] = _apply(m, float(el.get("x", 0)), float(el.get("y", 0)))[1]
            rec["size"] = max([sz for _, sz in rec["runs"]] or [float(inh["size"])])
        out.append(rec)

    root_inh = dict(ROOT, fill="#000000", fop=1.0, stroke="none", sw=1.0, opacity=1.0)
    for child in _parse(body):
        walk(child, root_inh, IDENT, child.get("id") or "(root)", None)
    for i, r in enumerate(out):
        r["z"] = i
    return out


def _segments(p):
    """Thin straight strokes of a primitive as ((x1, y1), (x2, y2)) in slide coordinates."""
    el, m, tag = p["el"], p["m"], p["tag"]
    if p["stroke"] in (None, "none") or p["sw"] > 3:
        return []
    f = lambda k: float(el.get(k, 0))
    if tag == "line":
        return [(_apply(m, f("x1"), f("y1")), _apply(m, f("x2"), f("y2")))]
    if tag == "rect":
        x, y, w, h = f("x"), f("y"), f("width"), f("height")
        c = [_apply(m, *q) for q in ((x, y), (x + w, y), (x + w, y + h), (x, y + h))]
        return [(c[i], c[(i + 1) % 4]) for i in range(4)]
    if tag in ("path", "polyline") and (p["fill"] in ("none", None) or tag == "polyline"):
        d = el.get("d", "") if tag == "path" else "M " + el.get("points", "")
        if re.search(r"[CSQTAcsqta]", d):
            return []
        try:
            pts = [_apply(m, *q) for q in _path_points(d)]
        except BodyError:
            return []
        return list(zip(pts, pts[1:]))
    return []


def _seg_hits_box(a, b, box):
    """A point where segment a-b passes through the box interior, or None (Liang–Barsky clip)."""
    x0, y0, x1, y1 = box
    dx, dy = b[0] - a[0], b[1] - a[1]
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
        if p == 0:
            if q < 0:
                return None
        else:
            t = q / p
            if p < 0:
                t0 = max(t0, t)
            else:
                t1 = min(t1, t)
    if t0 >= t1:
        return None
    t = (t0 + t1) / 2
    return a[0] + dx * t, a[1] + dy * t


def _opaque(p):
    return p["tag"] in ("rect", "circle", "ellipse", "path", "polygon") and p["fill"] not in (None, "none") \
        and not str(p["fill"]).startswith("url") and p["fop"] >= 0.95


def _inside(pt, box, pad=0):
    return box[0] - pad <= pt[0] <= box[2] + pad and box[1] - pad <= pt[1] <= box[3] + pad


def _centre(box):
    return (box[0] + box[2]) / 2, (box[1] + box[3]) / 2


def layout_lint(body, thesis):
    """Findings on the expanded body: block count, big numbers, small text, crossings, empty cards, decoration."""
    out = []
    try:
        prims = _prims(body)
    except (BodyError, ET.ParseError, ValueError) as e:
        return [f"[WARN] layout lint skipped: {e}"]
    top = 166 if thesis else 96
    body_area = (BODY_RIGHT - BODY_LEFT) * (BODY_BOTTOM - top)
    texts = [p for p in prims if p["tag"] == "text" and p.get("runs")]

    # 1. blocks: root modules that touch (gap ≤ 6 px) read as one block; small connectors do not count
    boxes = [(b[0], b[1], b[0] + b[2], b[1] + b[3]) for b in group_boxes(body).values()
             if b[2] * b[3] >= 0.02 * body_area]
    boxes += [p["box"] for p in prims if p["tag"] == "rect" and p["el"].get("data-pptx-role") == "decoration"]
    parent = list(range(len(boxes)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for i, a in enumerate(boxes):
        for j in range(i + 1, len(boxes)):
            b = boxes[j]
            if not (a[0] > b[2] + 6 or b[0] > a[2] + 6 or a[1] > b[3] + 6 or b[1] > a[3] + 6):
                parent[find(i)] = find(j)
    blocks = len({find(i) for i in range(len(boxes))})
    if blocks > MAX_BLOCKS:
        out.append(f"[WARN] {blocks} separate blocks in the body (> {MAX_BLOCKS}): merge related content groups into "
                   f"3–5 zones and keep every group title (rules 二.12)")

    # 2. big numbers
    def numeric(p, size):
        return any(re.search(r"\d", s) and sz >= size for s, sz in p["runs"])
    def focal(items):
        """An equal-weight row (3+ numbers at one size) counts as one focus (rules 二.9)."""
        sizes = {}
        for p in items:
            sizes.setdefault(round(p["size"]), []).append(p)
        return sum(1 if len(g) >= 3 else len(g) for g in sizes.values())
    heroes = focal([p for p in texts if numeric(p, 40)])
    if heroes > 2:
        out.append(f"[WARN] {heroes} hero numbers (≥ 40 px): keep one or two, set the rest at 28–32 px (rules 二.9)")

    # 2b. colour-block coverage: panels, header bars and dark blocks should fill most of the body
    cell = 8
    cols, rows = int((BODY_RIGHT - BODY_LEFT) // cell), int((BODY_BOTTOM - top) // cell)
    hit = set()
    for p in prims:
        if p["tag"] not in ("rect", "path", "polygon") or p["fill"] in (None, "none") or p["fop"] < 0.3:
            continue
        lum = _lum(p["fill"])
        if lum is not None and lum > 0.985:          # white tiles do not count as colour blocks
            continue
        x0, y0, x1, y1 = p["box"]
        if (x1 - x0) * (y1 - y0) < 400:
            continue
        for cx in range(max(0, int((x0 - BODY_LEFT) // cell)), min(cols, int((x1 - BODY_LEFT) // cell) + 1)):
            for cy in range(max(0, int((y0 - top) // cell)), min(rows, int((y1 - top) // cell) + 1)):
                hit.add((cx, cy))
    cover = len(hit) / max(cols * rows, 1)
    if cover < MIN_COVER:
        out.append(f"[WARN] colour blocks cover {cover:.0%} of the body (< {MIN_COVER:.0%}; target about 60–75 %): "
                   f"give each zone a dark header bar and a tinted panel instead of hairline boxes on white (rules 二.8)")

    # 3. small-text share (characters at ≤ 10 pt)
    total = small = 0
    for p in texts:
        for s, sz in p["runs"]:
            n = len(re.sub(r"\s", "", s))
            total += n
            small += n if sz <= SMALL_PX else 0
    if total >= 80 and small / total > SMALL_SHARE_MAX:
        out.append(f"[WARN] {small / total:.0%} of the body text is ≤ 12 px (> {SMALL_SHARE_MAX:.0%}; reference "
                   f"≈ 30–35%): merge modules or change the construction instead of shrinking type (page-patterns 一)")
    tiny = [p for p in texts if any(sz < 10.6 for _, sz in p["runs"])]
    if tiny:
        out.append(f"[WARN] {len(tiny)} text(s) under 10.67 px in the body, e.g. '{''.join(s for s, _ in tiny[0]['runs'])[:16]}': "
                   f"8–9 px is for the page footer only; sources go into the footer (SKILL.md 第 4 步)")

    # 4. thin lines running through text, unless something opaque is painted over the crossing
    crossed = []
    for t in texts:
        x0, _, x1, _ = t["box"]
        size = t["size"]
        inner = (x0 + 2, t["base"] - 0.68 * size, x1 - 2, t["base"] - 0.08 * size)
        if inner[2] <= inner[0]:
            continue
        for p in prims:
            if p["z"] >= t["z"]:
                continue
            hit = next((h for a, b in _segments(p) for h in [_seg_hits_box(a, b, inner)] if h), None)
            if not hit:
                continue
            if any(p["z"] < q["z"] < t["z"] and _opaque(q) and _inside(hit, q["box"]) for q in prims):
                continue
            crossed.append(f"'{''.join(s for s, _ in t['runs'])[:16]}' ({p['tag']} of {p['root']})")
            break
    for c in list(dict.fromkeys(crossed))[:6]:
        out.append(f"[WARN] a line runs through text {c}: move the text or the line")

    # 5. cards with an empty bottom, and filled boxes with nothing in them
    for r in prims:
        if r["tag"] != "rect":
            continue
        x0, y0, x1, y1 = r["box"]
        w, h = x1 - x0, y1 - y0
        filled = r["fill"] not in (None, "none")
        if w < 60 or h < 30 or not (0.004 * body_area <= w * h <= 0.3 * body_area):
            continue
        if not filled and r["stroke"] in (None, "none"):
            continue
        # a series of equal-width rects in one module is a bar chart, not a set of cards
        if sum(1 for q in prims if q is not r and q["tag"] == "rect" and q["root"] == r["root"]
               and abs((q["box"][2] - q["box"][0]) - w) < 1) >= 2:
            continue
        inner = [q for q in prims if q["z"] > r["z"] and _inside(_centre(q["box"]), r["box"])
                 and (q["box"][2] - q["box"][0]) * (q["box"][3] - q["box"][1]) < w * h * 0.9]
        if not inner:
            lum = _lum(r["fill"])
            segment = any(q is not r and q["tag"] == "rect" and abs(q["box"][1] - y0) < 1.5 and abs(q["box"][3] - y1) < 1.5
                          and (abs(q["box"][0] - x1) < 3 or abs(q["box"][2] - x0) < 3) for q in prims)
            if filled and lum is not None and lum < 0.97 and not segment:  # bar segments stay unlabeled
                out.append(f"[WARN] filled box {w:.0f}×{h:.0f} at ({x0:.0f}, {y0:.0f}) in {r['root']} has nothing in "
                           f"it: give it its own content or drop it (no placeholder blocks)")
            continue
        gap = y1 - max(q["box"][3] for q in inner)
        head = min(q["box"][1] for q in inner) - y0
        if h >= 50 and gap > h * CARD_EMPTY_MAX and gap > 40 and head < 0.6 * gap:
            out.append(f"[WARN] box {w:.0f}×{h:.0f} at ({x0:.0f}, {y0:.0f}) in {r['root']} is empty in its bottom "
                       f"{gap:.0f} px (> 1/3 of its height): shorten it or spread the content (rules 二.10)")

    # 6. decoration used as filler: big pale icons or arrows with nothing on them, pale watermark-size text
    for p in prims:
        x0, y0, x1, y1 = p["box"]
        big = max(x1 - x0, y1 - y0)
        lum = _lum(p["fill"])
        pale = (lum is not None and lum > 0.72) or p["fop"] < 0.5
        if p["icon"] and big >= 64 and pale:
            out.append(f"[WARN] large pale icon ({big:.0f} px) in {p['root']}: decorative filler is not allowed "
                       f"(rules 二.10)")
        elif p["prst"] and re.search(r"Arrow|chevron", p["prst"]) and big >= 80 and pale \
                and not any(t["root"] == p["root"] and t["size"] >= 40 for t in texts) \
                and not any(_inside(_centre(t["box"]), p["box"]) for t in texts):
            out.append(f"[WARN] large pale {p['prst']} ({big:.0f} px) with nothing on it in {p['root']}: decorative "
                       f"filler is not allowed (rules 二.10)")
        elif p["tag"] == "text" and p.get("runs") and p["size"] >= 36 and pale and not any(
                q["z"] < p["z"] and q["tag"] != "text" and q["fill"] not in (None, "none")
                and (str(q["fill"]).startswith("url") or (_lum(q["fill"]) or 1) < 0.6)
                and _inside(_centre(p["box"]), q["box"]) for q in prims):
            out.append(f"[WARN] pale {p['size']:.0f} px text '{''.join(s for s, _ in p['runs'])[:10]}' in "
                       f"{p['root']} reads as a watermark or filler number")
    return list(dict.fromkeys(out))
