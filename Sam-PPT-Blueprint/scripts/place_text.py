"""Reposition/resize text inside a module (step 4): python place_text.py <page.svg> <id> <x> <y> <size> [<line-step>] [--index N] [--anchor start|middle|end] [--fill #HEX] [--bold]

Sets the N-th <text> in <id> to baseline (x, y), font-size, and every line-break <tspan> to the same x
with dy = line-step (default 1.45 x size). "-" keeps x or y.
"""
import sys
from lxml import etree

SVG = "http://www.w3.org/2000/svg"


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


a = sys.argv[1:]
opts = {}
for k in ("--index", "--anchor", "--fill"):
    if k in a:
        i = a.index(k)
        opts[k] = a[i + 1]
        del a[i:i + 2]
bold = "--bold" in a
if bold:
    a.remove("--bold")
path, id_, x, y, size = a[:5]
step = float(a[5]) if len(a) > 5 else None
tree = etree.parse(path)
g = tree.getroot().xpath(f'//*[@id="{id_}"]')[0]
texts = [g] if etree.QName(g).localname == "text" else list(g.iter(f"{{{SVG}}}text"))
t = texts[int(opts.get("--index", 0))]
size = float(size)
step = step or 1.45 * size
if x != "-":
    t.set("x", x)
if y != "-":
    t.set("y", y)
t.set("font-size", f(size))
for k in ("data-paragraph-line-height",):
    t.attrib.pop(k, None)
if "--anchor" in opts:
    t.set("text-anchor", opts["--anchor"])
if "--fill" in opts:
    t.set("fill", opts["--fill"])
if bold:
    t.set("font-weight", "bold")
for ts in t.findall(f"{{{SVG}}}tspan"):
    if ts.get("x") is not None or ts.get("dy") is not None:
        ts.set("x", t.get("x"))
        if ts.get("dy") is not None:
            ts.set("dy", f(step))
    for k in ("data-paragraph-space-before",):
        ts.attrib.pop(k, None)
    for sub in ts.iter(f"{{{SVG}}}tspan"):
        if sub is not ts and sub.get("font-size"):
            sub.set("font-size", f(size))
tree.write(path, encoding="utf-8")
print(f"{id_}: text at {t.get('x')},{t.get('y')} size {f(size)} step {f(step)}")
