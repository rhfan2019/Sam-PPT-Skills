"""Resize imported shapes in place: python resize_shape.py <page.svg> <id> <x> <y> <w> <h> [<id> x y w h ...]

Works on imported shape groups whose data-pptx-prst is rect / roundRect / ellipse (rewrites
data-pptx-frame and the geometry path; roundRect keeps its corner radius). Text inside is left
where it is: move or retype it with edit_page.py afterwards. Use "-" to keep a value.
"""
import re
import sys
from lxml import etree

SVG = "http://www.w3.org/2000/svg"


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def rect_d(x, y, w, h):
    return f"M {f(x)} {f(y)} L {f(x + w)} {f(y)} L {f(x + w)} {f(y + h)} L {f(x)} {f(y + h)} Z"


def rrect_d(x, y, w, h, r):
    r = min(r, w / 2, h / 2)
    return (f"M {f(x)} {f(y + r)} A {f(r)} {f(r)} 0 0 1 {f(x + r)} {f(y)} L {f(x + w - r)} {f(y)} "
            f"A {f(r)} {f(r)} 0 0 1 {f(x + w)} {f(y + r)} L {f(x + w)} {f(y + h - r)} "
            f"A {f(r)} {f(r)} 0 0 1 {f(x + w - r)} {f(y + h)} L {f(x + r)} {f(y + h)} "
            f"A {f(r)} {f(r)} 0 0 1 {f(x)} {f(y + h - r)} Z")


def ell_d(x, y, w, h):
    rx, ry = w / 2, h / 2
    cx, cy = x + rx, y + ry
    return (f"M {f(x)} {f(cy)} A {f(rx)} {f(ry)} 0 0 1 {f(cx)} {f(y)} A {f(rx)} {f(ry)} 0 0 1 {f(x + w)} {f(cy)} "
            f"A {f(rx)} {f(ry)} 0 0 1 {f(cx)} {f(y + h)} A {f(rx)} {f(ry)} 0 0 1 {f(x)} {f(cy)} Z")


def main():
    path, args = sys.argv[1], sys.argv[2:]
    tree = etree.parse(path)
    root = tree.getroot()
    for i in range(0, len(args), 5):
        id_, vals = args[i], args[i + 1:i + 5]
        g = root.xpath(f'//*[@id="{id_}"]')
        if not g:
            sys.exit(f"no element {id_}")
        g = g[0]
        old = [float(v) for v in g.get("data-pptx-frame").split()]
        x, y, w, h = [old[k] if vals[k] == "-" else float(vals[k]) for k in range(4)]
        prst = g.get("data-pptx-prst")
        geo = g.find(f'{{{SVG}}}path[@data-pptx-part="geometry"]')
        if geo is None:
            geo = g.find(f"{{{SVG}}}path")
        if prst == "rect":
            d = rect_d(x, y, w, h)
        elif prst == "roundRect":
            m = re.search(r"A ([\d.]+)", geo.get("d"))
            d = rrect_d(x, y, w, h, float(m.group(1)) if m else 0)
        elif prst == "ellipse":
            d = ell_d(x, y, w, h)
        else:
            sys.exit(f"{id_}: prst {prst} not supported; use edit_page.py movebox or redraw")
        geo.set("d", d)
        g.set("data-pptx-frame", " ".join(f(v) for v in (x, y, w, h)))
        print(f"{id_}: {prst} -> {f(x)} {f(y)} {f(w)} {f(h)}")
    tree.write(path, encoding="utf-8")


main()
