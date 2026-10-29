"""Give composed pages the root structure ppt-master's final check requires (step 5).

  python group_page.py <grid.txt> <page.svg> [<page.svg> ...] [--role content]

ppt-master's flat pages declare one data-pptx-page-role on the root, and once a page does, every
visible root <g> must carry data-pptx-bounds and root groups must not overlap (shared-standards-core
§4.3). Pages composed from reference modules start as dozens of loose imported shapes, so this:
  - sets data-pptx-page-role on the root (default content) when it is missing;
  - wraps shell items above the content box into <g id="page-header" data-pptx-role="header">, those
    below it into "page-footer", and shell items inside it into "page-frame" (role decoration);
  - wraps each module's root items (ids "mK-…" from compose_page.py) into <g id="mK-module">;
  - gives every other root group without bounds (shapes drawn in step 4) bounds from its contents;
  - nests a bounded group into an earlier one it overlaps, so the page keeps one group per region;
  - marks a module group that overlaps a native chart or table carrier as decoration (overlap-exempt).
Paint order is kept: a module group spans from its first to its last item, so parts added between
them (add_parts.py --under) stay where they were in z-order; overlapping groups are merged together
with every ordinary root group drawn between them, in order (merging the later group into the earlier
one alone would push it under everything in between: icons and white text vanished under circles).
Running it twice changes nothing. Content-box coordinates come from <参考稿库>/grid.txt.
"""
import re
import sys

from lxml import etree

SVG = "http://www.w3.org/2000/svg"
NUM = re.compile(r"-?\d*\.?\d+(?:[eE][-+]?\d+)?")
W, H = 1280.0, 720.0


def local(e):
    return etree.QName(e).localname if isinstance(e.tag, str) else ""


def nums(v):
    return [float(x) for x in NUM.findall(v or "")]


def union(a, b):
    if a is None or b is None:
        return a or b
    x0, y0 = min(a[0], b[0]), min(a[1], b[1])
    return [x0, y0, max(a[0] + a[2], b[0] + b[2]) - x0, max(a[1] + a[3], b[1] + b[3]) - y0]


def own_box(d):
    """Rough root-coordinate box of one drawing element (frames first, then geometry)."""
    for a in ("data-pptx-bounds", "data-pptx-frame"):
        n = nums(d.get(a))
        if len(n) == 4:
            return n
    t, g = local(d), lambda k: float(d.get(k) or 0)
    if t == "rect":
        return [g("x"), g("y"), g("width"), g("height")]
    if t in ("circle", "ellipse"):
        rx = g("r") or g("rx")
        ry = g("r") or g("ry")
        return [g("cx") - rx, g("cy") - ry, 2 * rx, 2 * ry]
    if t == "line":
        return [min(g("x1"), g("x2")), min(g("y1"), g("y2")), abs(g("x2") - g("x1")), abs(g("y2") - g("y1"))]
    if t in ("polygon", "polyline", "path"):
        n = nums(d.get("points") or d.get("d"))
        xs, ys = n[0::2], n[1::2]
        if xs and ys:
            return [min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys)]
    if t == "text":
        size = float(nums(d.get("font-size") or "14")[0]) if nums(d.get("font-size")) else 14.0
        chars = len("".join(d.itertext()))
        return [g("x"), g("y") - size, chars * size, size * 1.3]
    if t == "use":
        return [g("x"), g("y"), g("width"), g("height")]
    return None


def box_of(e):
    b = own_box(e)
    if b:
        return b
    for d in e.iter():
        if d is not e and isinstance(d.tag, str):
            b = union(b, own_box(d) if d.get("data-pptx-frame") or local(d) != "g" else None)
    return b


def clamp(b):
    x0, y0 = max(0.0, b[0]), max(0.0, b[1])
    return [x0, y0, max(1.0, min(W, b[0] + b[2]) - x0), max(1.0, min(H, b[1] + b[3]) - y0)]


def fmt(b):
    return " ".join(f"{v:.2f}".rstrip("0").rstrip(".") for v in b)


def overlap(a, b):
    return (min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]) > 1
            and min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]) > 1)


def wrap(root, gid, items, role=None):
    g = etree.Element(f"{{{SVG}}}g", {"id": gid})
    items[0].addprevious(g)
    b = None
    for c in items:
        b = union(b, box_of(c))
        g.append(c)
    if role:
        g.set("data-pptx-role", role)
    if b:
        g.set("data-pptx-bounds", fmt(clamp(b)))
    return g


def run(path, y0, y1, role):
    tree = etree.parse(path)
    root = tree.getroot()
    if root.get("data-pptx-page-role") is None:
        root.set("data-pptx-page-role", role)
    kids = [c for c in root if local(c) not in ("", "defs", "style", "title", "desc")]
    buckets, order = {}, []
    for c in kids:
        i = c.get("id") or ""
        if c.get("data-pptx-bounds") or c.get("data-pptx-role") or c.get("data-pptx-replace-with"):
            continue
        m = re.match(r"(m\d+)-", i)
        if m:
            key, r = m.group(1) + "-module", None
        elif local(c) != "g" and not i.startswith("shape-"):
            continue  # an authored root primitive, e.g. the page background: exempt
        else:
            b = box_of(c)
            if b is None:
                continue
            mid = b[1] + b[3] / 2
            if i.startswith("shape-"):
                key, r = ("page-header", "header") if mid < y0 else ("page-footer", "footer") if mid > y1 else ("page-frame", "decoration")
            else:
                c.set("data-pptx-bounds", fmt(clamp(b)))
                continue
        if key not in buckets:
            buckets[key] = (r, [])
            order.append(key)
        buckets[key][1].append(c)
    for key in order:
        if root.xpath(f'./*[@id="{key}"]'):
            continue
        r, items = buckets[key]
        if key.endswith("-module"):
            kids_now = list(root)
            lo, hi = kids_now.index(items[0]), kids_now.index(items[-1])
            items = [c for c in kids_now[lo:hi + 1] if local(c) not in ("", "defs", "style", "title", "desc")
                     and not c.get("data-pptx-role") and not c.get("data-pptx-replace-with")
                     and not (c.get("id") or "").startswith("shape-")]
        wrap(root, key, items, r)

    def groups(pred):
        return [c for c in root if local(c) == "g" and c.get("data-pptx-bounds") and pred(c)]

    charts = groups(lambda c: c.get("data-pptx-replace-with"))
    ordinary = lambda c: not c.get("data-pptx-role") and not c.get("data-pptx-replace-with")
    changed = True
    while changed:
        changed = False
        gs = groups(ordinary)
        for i, a in enumerate(gs):
            ba = nums(a.get("data-pptx-bounds"))
            for b in gs[i + 1:]:
                bb = nums(b.get("data-pptx-bounds"))
                if overlap(ba, bb):
                    kids_now = list(root)
                    between = [c for c in kids_now[kids_now.index(a) + 1:kids_now.index(b) + 1]
                               if c in gs]  # ordinary bounded groups from a to b, in paint order
                    box = ba
                    for c in between:
                        box = union(box, nums(c.get("data-pptx-bounds")))
                        c.attrib.pop("data-pptx-bounds")
                        a.append(c)
                    a.set("data-pptx-bounds", fmt(clamp(box)))
                    changed = True
                    break
            if changed:
                break
    for g in groups(ordinary):
        if any(overlap(nums(g.get("data-pptx-bounds")), nums(c.get("data-pptx-bounds"))) for c in charts):
            g.set("data-pptx-role", "decoration")
    tree.write(path, encoding="utf-8")
    top = [c.get("id") for c in root if local(c) == "g"]
    print(f"{path}: {len(top)} root groups: {', '.join(top)}")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    role = "content"
    if "--role" in args:
        k = args.index("--role")
        role = args[k + 1]
        del args[k:k + 2]
    if len(args) < 2:
        sys.exit(__doc__)
    t = open(args[0], encoding="utf-8").read()
    y0, y1 = map(float, re.search(r"y (\d+)-(\d+)", t).groups())
    for p in args[1:]:
        run(p, y0, y1, role)


if __name__ == "__main__":
    main()
