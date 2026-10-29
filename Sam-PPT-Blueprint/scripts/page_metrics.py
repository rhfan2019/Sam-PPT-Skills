"""Measure a page's visual density from its SVG, before export, against the reference (steps 4, 5, 7).

  python page_metrics.py baseline <library_dir>
  python page_metrics.py check <library_dir> <page.svg> [<page.svg> ...] [--report]

baseline (run once by prepare_reference.py) measures the reference's content pages (the pages listed
in style-baseline.json) from <library>/import/authoring-svg-flat and writes <library>/svg-baseline.json
with the 25th percentile, median and 75th percentile of each metric.

check measures each page the same way and flags what is outside the reference's range. The metrics
are what makes rnb-core look rich rather than "boxes of text" (a page with a third of the reference's
shapes and twice its chars per text block reads as text boxes):
  形状     drawn objects in the content box (shapes, connectors, pictures, icons, primitives)   < p25
  文字块   non-empty <text> elements                                                           < p25
  字/块    characters per text element                                                         > p75
  长段     share of text elements with 36+ characters                                          > p75
  裸字     share of characters whose text does not sit on any filled shape (text on white)     > p75
  次色     solid secondary-colour area over the content box, %                                  < p25
  浅底     light tint area (panels, pills, tinted cards) over the content box, %                 < p25
  连接件   block arrows, chevrons, triangles, arrow-ended lines                                 < p25
  图标     icons (library icons, inlined reference icons, small pictures)                       < p25
  实心圆   solid-filled circles (number badges, icon discs, nodes)                              < p25
  图标位   unfilled icon slots left by start_page / compose_page (sam/icon-slot)                > 0
Exit code 1 when a page is flagged (use --report to only print). Each flag prints the fix to apply.
"""
import json
import re
import statistics
import sys
from pathlib import Path

from lxml import etree

SVG = "http://www.w3.org/2000/svg"
S = "{%s}" % SVG
NUM = r"-?\d*\.?\d+(?:[eE][-+]?\d+)?"
DRAW = {"rect", "circle", "ellipse", "line", "path", "polygon", "polyline", "use"}
ARROW_PRST = {"rightArrow", "leftArrow", "upArrow", "downArrow", "leftRightArrow", "upDownArrow", "chevron",
              "homePlate", "triangle", "notchedRightArrow", "stripedRightArrow", "curvedRightArrow",
              "curvedLeftArrow", "curvedUpArrow", "curvedDownArrow", "circularArrow", "uturnArrow", "bentArrow",
              "flowChartMerge", "flowChartExtract"}
ROUND_PRST = {"ellipse", "flowChartConnector", "donut"}
LONG = 36

# metric, direction ("lt": flag below p25, "gt": flag above p75), label, fix
RULES = [
    ("shapes", "lt", "形状", "按 page-zoning.md 第七节补部件：标题块配图标圆、要点配标记、编号配编号圆（add_parts.py）"),
    ("texts", "lt", "文字块", "按第七节拆块：一条大纲条目拆成 标签 + 短句，分号处分行，每行一个标记"),
    ("chars_per_text", "gt", "字/块", "同上：长句在标点处拆开，标签（冒号前的词）单独放进标签块或胶囊"),
    ("long_share", "gt", "长段", "36 字以上的段落拆成要点行（add_parts.py bullets），或放进带标签的卡片"),
    ("bare_text", "gt", "裸字", "白底上的文字放进浅底面板、胶囊或卡片（add_parts.py panel / pill / label）"),
    ("red_pct", "lt", "次色", "按 page-zoning.md 第六节第 1 条加结构次色：对比一方、终点阶段、编号圆、分区标签交替"),
    ("tint_pct", "lt", "浅底", "卡片正文区、分区底板用浅蓝 / 浅粉实底，不用白底加线框或虚线框"),
    ("connectors", "lt", "连接件", "补 plan.md 写的分区间连接件，用原生箭头（add_parts.py arrow / chevron / tri / line）"),
    ("icons", "lt", "图标", "标题块、节点、卡片标题配图标（add_parts.py icon，icon_sync.py 同步）"),
    ("solid_round", "lt", "实心圆", "编号、图标底、节点用实心圆加阴影（add_parts.py badge / icon）"),
]
KEYS = [r[0] for r in RULES]


def nums(s):
    return [float(v) for v in re.findall(NUM, s or "")]


def local(e):
    return etree.QName(e).localname if isinstance(e.tag, str) else ""


def content_box(lib: Path):
    t = (lib / "grid.txt").read_text(encoding="utf-8")
    x0, x1, y0, y1 = map(int, re.search(r"x (\d+)-(\d+), y (\d+)-(\d+)", t).groups())
    return x0, y0, x1, y1


def hex_rgb(c):
    c = (c or "").strip()
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", c):
        return None
    return tuple(int(c[i:i + 2], 16) / 255 for i in (1, 3, 5))


def hsv(rgb):
    r, g, b = rgb
    mx, mn = max(rgb), min(rgb)
    d = mx - mn
    if d == 0:
        h = 0.0
    elif mx == r:
        h = ((g - b) / d) % 6
    elif mx == g:
        h = (b - r) / d + 2
    else:
        h = (r - g) / d + 4
    return h * 60, (d / mx if mx else 0), mx


def bbox(e):
    """Frame of a drawn object: data-pptx-frame on an object group, else the primitive's own geometry."""
    if e.get("data-pptx-frame"):
        v = nums(e.get("data-pptx-frame"))
        if len(v) == 4:
            return v
    n = local(e)
    try:
        if n in ("rect", "use"):
            return [float(e.get("x", 0)), float(e.get("y", 0)), float(e.get("width", 0)), float(e.get("height", 0))]
        if n == "circle":
            r = float(e.get("r", 0))
            return [float(e.get("cx", 0)) - r, float(e.get("cy", 0)) - r, 2 * r, 2 * r]
        if n == "ellipse":
            rx, ry = float(e.get("rx", 0)), float(e.get("ry", 0))
            return [float(e.get("cx", 0)) - rx, float(e.get("cy", 0)) - ry, 2 * rx, 2 * ry]
        if n == "line":
            x1, y1, x2, y2 = (float(e.get(k, 0)) for k in ("x1", "y1", "x2", "y2"))
            return [min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1)]
    except ValueError:
        return None
    v = nums(e.get("d") or e.get("points"))
    if n == "path" and re.search(r"[aA]", e.get("d") or ""):
        v = []  # arcs: fall back to the object frame only
    if len(v) >= 4:
        xs, ys = v[0::2], v[1::2]
        return [min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)]
    return None


def paint(e, key):
    """Effective fill / stroke and opacity of a drawable (own attribute, else nearest ancestor)."""
    p = e
    while p is not None:
        if p.get(key):
            op = p.get(f"{key}-opacity") or p.get("opacity") or e.get(f"{key}-opacity") or "1"
            try:
                return p.get(key), float(op)
            except ValueError:
                return p.get(key), 1.0
        p = p.getparent()
    return None, 1.0


def object_leaves(root):
    """One entry per drawn object: an imported/authored object group counts once; loose primitives count each."""
    out = []
    for e in root.iter():
        n = local(e)
        if n == "g" and e.get("data-pptx-object") in ("shape", "connector", "picture"):
            if any(a.get("data-pptx-object") in ("shape", "connector", "picture") for a in e.iterancestors(S + "g")):
                continue
            out.append(("obj", e))
        elif n in DRAW:
            if any(a.get("data-pptx-object") in ("shape", "connector", "picture") for a in e.iterancestors(S + "g")):
                continue
            if any(local(a) in ("defs", "marker", "clipPath", "symbol", "pattern", "mask") for a in e.iterancestors()):
                continue
            out.append(("prim", e))
    return out


def geometry_of(kind, e):
    if kind == "prim":
        return e
    p = e.find(S + "path")
    if p is None:
        p = next((c for c in e.iter() if local(c) in DRAW), None)
    return p


def measure(path: Path, box, hues):
    root = etree.parse(str(path)).getroot()
    x0, y0, x1, y1 = box
    area = (x1 - x0) * (y1 - y0)
    m = dict.fromkeys(KEYS, 0)
    m["slots"] = 0
    red = tint = 0.0
    filled = []

    def inside(b):
        cx, cy = b[0] + b[2] / 2, b[1] + b[3] / 2
        return x0 <= cx <= x1 and y0 <= cy <= y1

    for kind, e in object_leaves(root):
        b = bbox(e)
        if not b or not inside(b):
            continue
        w, h = b[2], b[3]
        if local(e) == "use" and (e.get("data-icon") or "").startswith("sam/icon-slot"):
            m["slots"] += 1
            continue
        m["shapes"] += 1
        prst = e.get("data-pptx-prst") if kind == "obj" else None
        geo = geometry_of(kind, e)
        is_icon = (local(e) == "use" and e.get("data-icon")) or e.get("data-reference-icon") \
            or (kind == "obj" and e.get("data-pptx-object") == "picture" and max(w, h) <= 80)
        if not is_icon and kind == "obj" and e.find(f".//{S}g[@data-reference-icon]") is not None:
            is_icon = True
        if is_icon:
            m["icons"] += 1
            continue
        if prst in ARROW_PRST:
            m["connectors"] += 1
        if geo is not None and (geo.get("marker-end") or geo.get("marker-start")):
            m["connectors"] += 1
        if geo is None:
            continue
        fill, op = paint(geo, "fill")
        rgb = hex_rgb(fill)
        if rgb is None or w * h <= 0:
            continue
        hue, sat, val = hsv(rgb)
        eff = op
        round_ = prst in ROUND_PRST or local(geo) in ("circle", "ellipse")
        if eff >= 0.6 and sat >= 0.35 and val >= 0.2:
            if min(abs(hue - hues[1]), 360 - abs(hue - hues[1])) <= 20:
                red += w * h
            if round_ and w >= 16:
                m["solid_round"] += 1
            filled.append(b)
        elif (eff >= 0.6 and 0.03 <= sat < 0.35 and val > 0.85) or (0 < eff < 0.6 and sat >= 0.1):
            tint += w * h * (1 if eff >= 0.6 else max(eff, 0.25) / 0.6)
            filled.append(b)
        elif round_ and eff >= 0.6 and w >= 16 and sat >= 0.35:
            m["solid_round"] += 1
    chars = bare = 0
    for t in root.iter(S + "text"):
        s = "".join(t.itertext()).strip()
        if not s:
            continue
        try:
            tx, ty = float(t.get("x", 0) or 0), float(t.get("y", 0) or 0)
        except ValueError:
            continue
        if not (x0 <= tx <= x1 and y0 <= ty <= y1):
            continue
        anchor = t.get("text-anchor") or "start"
        size = float(t.get("font-size") or 12)
        px = tx + (size if anchor == "start" else 0)
        py = ty - size * 0.35
        m["texts"] += 1
        chars += len(s)
        if len(s) >= LONG:
            m["long_share"] += 1
        if not any(b[0] <= px <= b[0] + b[2] and b[1] <= py <= b[1] + b[3] for b in filled):
            bare += len(s)
    m["chars_per_text"] = round(chars / m["texts"], 1) if m["texts"] else 0
    m["long_share"] = round(m["long_share"] / m["texts"], 2) if m["texts"] else 0
    m["bare_text"] = round(bare / chars, 2) if chars else 0
    m["red_pct"] = round(red / area * 100, 1)
    m["tint_pct"] = round(tint / area * 100, 1)
    return m


def pct(vals, q):
    vals = sorted(vals)
    k = (len(vals) - 1) * q
    lo, hi = int(k), min(int(k) + 1, len(vals) - 1)
    return round(vals[lo] + (vals[hi] - vals[lo]) * (k - lo), 2)


def baseline(lib: Path):
    b = json.loads((lib / "style-baseline.json").read_text(encoding="utf-8"))
    flat = lib / "import" / "authoring-svg-flat"
    box = content_box(lib)
    rows = [measure(flat / f"slide_{p:02d}.svg", box, b["hues"]) for p in b["pages"]]
    out = {k: {"p25": pct([r[k] for r in rows], 0.25), "median": round(statistics.median([r[k] for r in rows]), 2),
               "p75": pct([r[k] for r in rows], 0.75)} for k in KEYS}
    out["hues"] = b["hues"]
    (lib / "svg-baseline.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"svg-baseline.json: {len(rows)} reference pages")
    for k, label in ((r[0], r[2]) for r in RULES):
        print(f"  {label}: p25 {out[k]['p25']} / 中位 {out[k]['median']} / p75 {out[k]['p75']}")


def check(lib: Path, pages, report_only=False):
    sys.stdout.reconfigure(encoding="utf-8")
    ref = json.loads((lib / "svg-baseline.json").read_text(encoding="utf-8"))
    box = content_box(lib)
    labels = [r[2] for r in RULES]
    print("| 页 | " + " | ".join(labels) + " | 图标位 | 超出项 |")
    print("|---" * (len(labels) + 3) + "|")
    bad, hints = 0, {}
    for p in pages:
        m = measure(Path(p), box, ref["hues"])
        flags = []
        for k, d, label, fix in RULES:
            lim = ref[k]["p25"] if d == "lt" else ref[k]["p75"]
            if (d == "lt" and m[k] < lim) or (d == "gt" and m[k] > lim):
                flags.append(label)
                hints[label] = fix
        if m["slots"]:
            flags.append("图标位")
            hints["图标位"] = "start_page / compose_page 留下的 sam/icon-slot：换成意思对应的图标库图标（add_parts.py icon，或改 data-icon），用不上的删掉"
        bad += bool(flags)
        print(f"| {Path(p).stem[:18]} | " + " | ".join(str(m[k]) for k in KEYS) + f" | {m['slots']} | {'、'.join(flags) or '无'} |")
    print("| 参考稿 p25–p75 | " + " | ".join(f"{ref[k]['p25']}–{ref[k]['p75']}" for k in KEYS) + " | 0 | |")
    if hints:
        print("\n怎么改：")
        for label, fix in hints.items():
            print(f"  {label}：{fix}")
    return 1 if bad and not report_only else 0


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]
    if a[:1] == ["baseline"] and len(a) == 2:
        baseline(Path(a[1]))
    elif a[:1] == ["check"] and len(a) >= 3:
        report = "--report" in a
        a = [x for x in a if x != "--report"]
        sys.exit(check(Path(a[1]), a[2:], report))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
