"""Measure how far a finished deck is from the reference's look, page by page (step 7).

  python style_gap.py baseline <reference.pptx> <library_dir>
  python style_gap.py check <library_dir> <deck.pptx> <renders_dir>

baseline (run once by prepare_reference.py) reads the reference's content pages (pages with at least
40 shapes; covers, contents and section pages fall out) and writes <library_dir>/style-baseline.json:
the reference's two main hues and, for each metric, its 25th percentile, median and 75th percentile.

check measures every page of the deck the same way and flags pages outside the reference's range:
  次色面积   area of the second main hue over the first (rnb-core: brick red over navy) < p25
  留白       share of 40 px tiles in the content box that are entirely white > p75
  连接件     arrows, chevrons, triangles and arrow-ended lines < p25
  质感       gradients + shadows < p25
Flags are prompts for the one fix round in step 7, not hard gates: a page whose outline content is
genuinely thin can stay below the reference's density, but it must not stay pale, empty or disconnected.
"""
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image

ARROWS = re.compile(r'prst="(?:rightArrow|leftArrow|upArrow|downArrow|leftRightArrow|upDownArrow|chevron|homePlate|'
                    r'triangle|curvedRightArrow|curvedLeftArrow|curvedUpArrow|curvedDownArrow|circularArrow|'
                    r'uturnArrow|bentArrow|notchedRightArrow|stripedRightArrow|flowChartMerge)"')
LINE_ENDS = re.compile(r'<a:(?:tailEnd|headEnd) type="(?:triangle|arrow|stealth)"')
SHAPES = re.compile(r"<p:(?:sp|cxnSp|graphicFrame|pic)>")


def content_box(lib: Path):
    """Content box in render pixels (renders are 1600 px wide, SVG pages 1280)."""
    t = (lib / "grid.txt").read_text(encoding="utf-8")
    x0, x1, y0, y1 = map(int, re.search(r"x (\d+)-(\d+), y (\d+)-(\d+)", t).groups())
    k = 1600 / 1280
    return int(x0 * k), int(y0 * k), int(x1 * k), int(y1 * k)


def slides_xml(pptx: Path):
    z = zipfile.ZipFile(pptx)
    names = sorted((n for n in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)),
                   key=lambda n: int(re.search(r"(\d+)", n).group(1)))
    return [z.read(n).decode("utf-8") for n in names]


def xml_metrics(x):
    return {"shapes": len(SHAPES.findall(x)),
            "connectors": len(ARROWS.findall(x)) + len(LINE_ENDS.findall(x)),
            "texture": x.count("<a:gradFill") + x.count("<a:outerShdw")}


def pixels(png: Path, box):
    a = np.asarray(Image.open(png).convert("RGB").resize((1600, 900)))[box[1]:box[3], box[0]:box[2]].astype(float) / 255
    mx, mn = a.max(-1), a.min(-1)
    sat = mx - mn
    hue = np.zeros_like(mx)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    d = np.where(sat == 0, 1, sat)
    hue = np.where(mx == r, (g - b) / d % 6, np.where(mx == g, (b - r) / d + 2, (r - g) / d + 4)) * 60
    return hue, (sat > 0.18) & (mx > 0.25), mn > 0.94


def hue_share(hue, colored, center, width=20):
    dist = np.abs((hue - center + 180) % 360 - 180)
    return float((colored & (dist <= width)).mean() * 100)


def empty_tiles(white, t=50):
    h, w = white.shape
    tiles = [white[y:y + t, x:x + t].all() for y in range(0, h - t + 1, t) for x in range(0, w - t + 1, t)]
    return float(np.mean(tiles) * 100)


def main_hues(samples):
    hist = np.zeros(36)
    for hue, colored in samples:
        hist += np.histogram(hue[colored], bins=36, range=(0, 360))[0]
    order = np.argsort(hist)[::-1]
    first = order[0]
    second = next(i for i in order[1:] if min(abs(i - first), 36 - abs(i - first)) >= 5)
    return [float(first * 10 + 5), float(second * 10 + 5)]


def page_metrics(xml, png, box, hues):
    hue, colored, white = pixels(png, box)
    m = xml_metrics(xml)
    a, b = hue_share(hue, colored, hues[0]), hue_share(hue, colored, hues[1])
    m.update({"primary_pct": round(a, 1), "secondary_pct": round(b, 1),
              "secondary_ratio": round(b / a, 2) if a > 0.5 else 0.0, "empty_pct": round(empty_tiles(white), 1)})
    return m


KEYS = ["secondary_ratio", "empty_pct", "connectors", "texture", "shapes"]


def shadow_recipes(lib: Path, top=2):
    """The reference's most used drop shadows, as SVG filters."""
    from collections import Counter
    from lxml import etree
    recipes = Counter()
    for f in sorted((lib / "import/authoring-svg-flat").glob("slide_*.svg")):
        root = etree.parse(str(f)).getroot()
        filters = {}
        for flt in root.iter("{http://www.w3.org/2000/svg}filter"):
            d = flt.find("{http://www.w3.org/2000/svg}feDropShadow")
            if d is not None:
                key = tuple(round(float(d.get(a, 0)), 1) for a in ("dx", "dy", "stdDeviation")) + (
                    (d.get("flood-color") or "#000000").upper(), round(float(d.get("flood-opacity", 1)), 2))
                filters[flt.get("id")] = key
        for e in root.iter():
            m = re.search(r"url\(#([^)]+)\)", e.get("filter") or "") if isinstance(e.tag, str) else None
            if m and m.group(1) in filters:
                recipes[filters[m.group(1)]] += 1
    return ([{"count": n, "svg": f'<feDropShadow dx="{k[0]}" dy="{k[1]}" stdDeviation="{k[2]}" '
                                 f'flood-color="{k[3]}" flood-opacity="{k[4]}"/>'}
             for k, n in recipes.most_common(top)])


def baseline(ref: Path, lib: Path):
    box = content_box(lib)
    xmls = slides_xml(ref)
    pages = [i for i, x in enumerate(xmls, 1) if xml_metrics(x)["shapes"] >= 40 and (lib / f"renders/slide-{i:02d}.png").exists()]
    hues = main_hues([pixels(lib / f"renders/slide-{i:02d}.png", box)[:2] for i in pages])
    rows = [page_metrics(xmls[i - 1], lib / f"renders/slide-{i:02d}.png", box, hues) for i in pages]
    out = {"pages": pages, "hues": hues,
           "metrics": {k: {q: round(float(np.percentile([r[k] for r in rows], p)), 2) for q, p in (("p25", 25), ("median", 50), ("p75", 75))}
                       for k in KEYS + ["primary_pct", "secondary_pct"]}}
    out["shadows"] = shadow_recipes(lib)
    names = {"ellipse": "圆", "flowChartConnector": "圆", "rect": "矩形", "roundRect": "圆角矩形"}
    carriers = {}
    for i in pages:
        for sp in re.findall(r"<p:sp>.*?</p:sp>", xmls[i - 1], re.S):
            if "<a:outerShdw" in sp:
                m = re.search(r'prst="(\w+)"', sp)
                k = names.get(m.group(1), "其他") if m else "其他"
                carriers[k] = carriers.get(k, 0) + 1
    out["shadow_carriers"] = dict(sorted(carriers.items(), key=lambda kv: -kv[1]))
    (lib / "style-baseline.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(pages)} content pages; main hues {hues[0]:.0f}° / {hues[1]:.0f}°")
    for k, v in out["metrics"].items():
        print(f"  {k}: p25 {v['p25']}  median {v['median']}  p75 {v['p75']}")
    for s in out["shadows"]:
        print(f"  shadow x{s['count']}: {s['svg']}")
    print(f"  shadow carriers: {out['shadow_carriers']}")


def check(lib: Path, deck: Path, renders: Path):
    base = json.loads((lib / "style-baseline.json").read_text(encoding="utf-8"))
    box, hues, ref = content_box(lib), base["hues"], base["metrics"]
    rules = [("secondary_ratio", "lt", "次色面积"), ("empty_pct", "gt", "留白"),
             ("connectors", "lt", "连接件"), ("texture", "lt", "质感")]
    print("| 页 | 次色/主色 | 留白% | 连接件 | 渐变+阴影 | 形状 | 超出参考稿范围 |\n|---|---:|---:|---:|---:|---:|---|")
    rows = []
    for i, x in enumerate(slides_xml(deck), 1):
        png = renders / f"slide-{i:02d}.png"
        if not png.exists():
            continue
        m = page_metrics(x, png, box, hues)
        rows.append(m)
        flags = [name for k, how, name in rules
                 if (how == "lt" and m[k] < ref[k]["p25"]) or (how == "gt" and m[k] > ref[k]["p75"])]
        print(f"| P{i:02d} | {m['secondary_ratio']} | {m['empty_pct']} | {m['connectors']} | {m['texture']} | {m['shapes']} | {'、'.join(flags) or '无'} |")
    if rows:
        avg = {k: round(float(np.mean([r[k] for r in rows])), 2) for k in KEYS}
        print(f"| 平均 | {avg['secondary_ratio']} | {avg['empty_pct']} | {avg['connectors']} | {avg['texture']} | {avg['shapes']} | |")
    print(f"| 参考稿 p25–p75 | {ref['secondary_ratio']['p25']}–{ref['secondary_ratio']['p75']} "
          f"| {ref['empty_pct']['p25']}–{ref['empty_pct']['p75']} | {ref['connectors']['p25']}–{ref['connectors']['p75']} "
          f"| {ref['texture']['p25']}–{ref['texture']['p75']} | {ref['shapes']['p25']}–{ref['shapes']['p75']} | |")
    if base.get("shadows"):
        print("\n质感低的页，按参考稿的阴影配方给实心圆、实色标题块、结论条加阴影（page-zoning.md 第六节第 5 条）：")
        for s in base["shadows"]:
            print(f"  {s['svg']}  （参考稿用了 {s['count']} 次）")
        print(f"  参考稿带阴影的元素：{base.get('shadow_carriers')}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) == 4 and sys.argv[1] == "baseline":
        baseline(Path(sys.argv[2]), Path(sys.argv[3]))
    elif len(sys.argv) == 5 and sys.argv[1] == "check":
        check(Path(sys.argv[2]), Path(sys.argv[3]), Path(sys.argv[4]))
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
