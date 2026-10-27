"""How much of each page still stands on its blueprint.

For every page started by start_page.py (it carries a "<!-- blueprint: slide_NN.svg -->"
comment), count the page's shape anchors (rect/ellipse/circle/line start, first point of
path/polygon) that lie within 3 px of an anchor on the blueprint page. A freshly started
page scores about 100%; a page redrawn from scratch scores about 5-10%.

Usage: python check_reuse.py <project>/svg_output <import_workspace>/authoring-svg-flat
"""
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

NS = "{http://www.w3.org/2000/svg}"
TOL = 3


def num(attrs, key):
    found = re.findall(r"-?\d+\.?\d*", attrs.get(key, ""))
    return float(found[0]) if found else None


def anchors(path):
    pts = []
    for e in ET.parse(path).getroot().iter():
        tag, a = e.tag.replace(NS, ""), e.attrib
        if tag == "rect" and num(a, "x") is not None:
            if (num(a, "width") or 0) >= 1279:
                continue  # page background
            pts.append((num(a, "x"), num(a, "y") or 0))
        elif tag in ("circle", "ellipse") and num(a, "cx") is not None:
            pts.append((num(a, "cx"), num(a, "cy") or 0))
        elif tag == "line" and num(a, "x1") is not None:
            pts.append((num(a, "x1"), num(a, "y1") or 0))
        elif tag in ("path", "polygon"):
            n = re.findall(r"-?\d+\.?\d*", a.get("d") or a.get("points") or "")
            if len(n) >= 2:
                pts.append((float(n[0]), float(n[1])))
    return pts


def main():
    pages, ref_dir = Path(sys.argv[1]), Path(sys.argv[2])
    for svg in sorted(pages.glob("*.svg")):
        m = re.search(r"<!-- blueprint: (\S+) -->", svg.read_text(encoding="utf-8"))
        if not m:
            print(f"{svg.name}: no blueprint comment (not started with start_page.py)")
            continue
        new, ref = anchors(svg), anchors(ref_dir / m.group(1))
        kept = sum(any(math.dist(p, q) <= TOL for q in ref) for p in new)
        share = kept / len(new) if new else 0
        print(f"{svg.name}: {share:4.0%} of {len(new)} shape anchors from {m.group(1)}")


if __name__ == "__main__":
    main()
