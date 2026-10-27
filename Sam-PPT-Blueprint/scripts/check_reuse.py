"""How much of each page still stands on the reference.

A page started by start_page.py carries "<!-- blueprint: slide_NN.svg -->"; a page built by
compose_page.py carries "<!-- composed: shell: slide_NN.svg | ... -->" and one
"<!-- module K: slide_NN.svg x,y,w,h -> X,Y,W -->" per module. Count the page's shape anchors
(rect/ellipse/circle/line start, first point of path/polygon) that lie within 3 px of an anchor on
the reference: the started page, or the shell's header/footer plus every module's anchors moved and
scaled to where the module now sits. A fresh page scores about 100%; a page redrawn from scratch
about 5-10%. The share is a hint, not a gate: deleting parts whose meaning does not fit the content
lowers it, and that is correct.

Usage: python check_reuse.py <project>/svg_output <import_workspace>/authoring-svg-flat
"""
import math
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from start_page import strip  # noqa: E402

NS = "{http://www.w3.org/2000/svg}"
TOL = 3
NUM = r"-?\d*\.?\d+(?:[eE][-+]?\d+)?"
CHROME_TOP, CHROME_BOTTOM = 95, 675


def num(attrs, key):
    found = re.findall(NUM, attrs.get(key, ""))
    return float(found[0]) if found else None


def anchors_of(root):
    pts = []
    for e in root.iter():
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
            n = re.findall(NUM, a.get("d") or a.get("points") or "")
            if len(n) >= 2:
                pts.append((float(n[0]), float(n[1])))
    return pts


def ref_anchors(path):
    text, _ = strip(Path(path).read_text(encoding="utf-8"), Path(path).parent.parent / "images")
    return anchors_of(ET.fromstring(text))


def composed_ref(text, ref_dir):
    shell = re.search(r"shell: (slide_\d+\.svg)", text).group(1)
    pts = [p for p in ref_anchors(ref_dir / shell) if p[1] < CHROME_TOP or p[1] > CHROME_BOTTOM]
    for m in re.finditer(rf"module \d+: (slide_\d+\.svg) ({NUM}),({NUM}),({NUM}),({NUM}) -> ({NUM}),({NUM}),({NUM})"
                         rf"(?: \+({NUM}),({NUM}),({NUM}),({NUM}))?", text):
        x, y, w, h, X, Y, W = (float(v) for v in m.groups()[1:8])
        boxes = [(x, y, w, h)] + ([tuple(float(v) for v in m.groups()[8:])] if m.group(9) else [])
        s = W / w
        pts += [(px * s + X - x * s, py * s + Y - y * s) for px, py in ref_anchors(ref_dir / m.group(1))
                if any(bx - 6 <= px <= bx + bw + 6 and by - 6 <= py <= by + bh + 6 for bx, by, bw, bh in boxes)]
    return pts, "composed"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    pages, ref_dir = Path(sys.argv[1]), Path(sys.argv[2])
    for svg in sorted(pages.glob("*.svg")):
        text = svg.read_text(encoding="utf-8")
        m = re.search(r"<!-- blueprint: (\S+) -->", text)
        if m:
            ref, label = ref_anchors(ref_dir / m.group(1)), m.group(1)
        elif "composed: shell:" in text:
            ref, label = composed_ref(text, ref_dir)
        else:
            print(f"{svg.name}: no blueprint or composed comment (not started from the reference)")
            continue
        new = anchors_of(ET.parse(svg).getroot())
        kept = sum(any(math.dist(p, q) <= TOL for q in ref) for p in new)
        share = kept / len(new) if new else 0
        print(f"{svg.name}: {share:4.0%} of {len(new)} shape anchors from {label}")


if __name__ == "__main__":
    main()
