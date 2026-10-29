"""Edit a started page in place, by element id (step 4). Keeps every other attribute.

  python edit_page.py list  <page.svg>                      top-level modules: id, kind, frame, text
  python edit_page.py text  <page.svg> <id> "new text" [--index N]
                            replace the N-th (default 0) <text> inside <id>; "\\n" starts a new line
  python edit_page.py del   <page.svg> <id> [<id> ...]      delete whole modules
  python edit_page.py move  <page.svg> <id> <dx> <dy>       shift a module (rewrites coordinates)
  python edit_page.py clone <page.svg> <id> <dx> <dy>       copy a module next to itself, ids get a -cN suffix
  python edit_page.py color <page.svg> <id> <#OLD> <#NEW>   swap one colour inside a module (fill/stroke/stop)
  python edit_page.py movebox <page.svg> <x> <y> <w> <h> <dx> <dy>
                            shift every drawn object (shape, connector, picture, loose primitive, text) whose
                            centre lies in the box: re-spaces one unit of a module after deleting or cloning
                            (within one batch an object is moved by the first movebox that catches it only)
  python edit_page.py delbox <page.svg> <x> <y> <w> <h>     delete every drawn object centred in the box
  python edit_page.py style <page.svg> <id> key=value [key=value ...]
                            set paint attributes on the geometry of <id> (fill, fill-opacity, stroke,
                            stroke-width, stroke-dasharray; value "none" for dasharray removes it), e.g. turn a
                            dashed white card into a tinted panel: style m2-shape-9 stroke=none stroke-dasharray=none fill=#C4D7F1 fill-opacity=0.3
  python edit_page.py shadow <page.svg> <id> [A|B|none]     put the reference shadow (shadowA strong, shadowB light)
                            on the filled geometry of <id> (solid circles, solid blocks; never on <g>)
  python edit_page.py boxes <page.svg> <x> <y> <w> <h>      list the objects centred in the box (dry run)
  python edit_page.py sweep <page.svg>                      after deleting parts: give text-only shapes a
                            transparent frame, drop shapes and groups left with nothing to draw

Several commands can run in one call, separated by " ; " inside one quoted argument:
  python edit_page.py batch <page.svg> "del shape-12 shape-13 ; text shape-3 标题 ; move shape-40 0 -20"
"""
import copy
import os
import re
import shlex
import sys

from lxml import etree

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import textmodel  # noqa: E402

SVG = "http://www.w3.org/2000/svg"
NS = {"s": SVG}
DRAW = {"rect", "circle", "ellipse", "line", "path", "polygon", "polyline"}
NUM = r"-?\d*\.?\d+(?:[eE][-+]?\d+)?"


def local(e):
    return etree.QName(e).localname if isinstance(e.tag, str) else ""


def find(root, id_):
    hit = root.xpath(f'//*[@id="{id_}"]')
    if not hit:
        sys.exit(f"no element with id {id_}")
    return hit[0]


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


# ---------- list ----------

def cmd_list(root):
    for g in root:
        if not isinstance(g.tag, str) or local(g) in ("defs", "metadata"):
            continue
        texts = ["".join(t.itertext()).strip() for t in g.iter(f"{{{SVG}}}text")]
        text = " | ".join(t for t in texts if t)[:60]
        kind = g.get("data-pptx-object") or local(g)
        print(f"{g.get('id', '-'):14} {kind:10} frame={g.get('data-pptx-frame', '')}  {text}")


# ---------- text ----------

def cmd_text(root, id_, new, index=0, fit=False, width=None):
    el = find(root, id_)
    texts = [el] if local(el) == "text" else list(el.iter(f"{{{SVG}}}text"))
    if index >= len(texts):
        sys.exit(f"{id_} has {len(texts)} <text> element(s); --index {index} is out of range")
    rep = textmodel.replace(texts[index], new, fit=fit, width_override=width)
    note = textmodel.describe(rep)
    if note:
        print(f"text {id_}: {note}")


# ---------- move / clone ----------

def shift_path(d, dx, dy):
    out, cmd, first = [], None, True
    for tok in re.findall(rf"[A-Za-z]|{NUM}", d):
        if tok.isalpha():
            cmd, i = tok, 0
            out.append(tok)
            continue
        v = float(tok)
        if cmd in "MLTCSQ":
            v += dx if i % 2 == 0 else dy
        elif cmd == "H":
            v += dx
        elif cmd == "V":
            v += dy
        elif cmd == "A" and i % 7 in (5, 6):
            v += dx if i % 7 == 5 else dy
        elif cmd == "m" and first and i < 2:
            v += dx if i == 0 else dy
        if cmd == "m" and i == 1:
            first = False
        out.append(fmt(v))
        i += 1
    return " ".join(out)


def shift_pairs(s, dx, dy):
    vals = [float(v) for v in re.findall(NUM, s)]
    return " ".join(fmt(v + (dx if i % 2 == 0 else dy)) for i, v in enumerate(vals))


def shift_frame(s, dx, dy):
    v = [float(x) for x in re.findall(NUM, s)]
    return " ".join(fmt(x) for x in [v[0] + dx, v[1] + dy] + v[2:]) if len(v) >= 2 else s


def shift_el(e, dx, dy):
    for k in ("x", "x1", "x2", "cx"):
        if e.get(k) is not None and re.fullmatch(NUM, e.get(k)):
            e.set(k, fmt(float(e.get(k)) + dx))
    for k in ("y", "y1", "y2", "cy"):
        if e.get(k) is not None and re.fullmatch(NUM, e.get(k)):
            e.set(k, fmt(float(e.get(k)) + dy))
    if e.get("d"):
        e.set("d", shift_path(e.get("d"), dx, dy))
    if e.get("points"):
        e.set("points", shift_pairs(e.get("points"), dx, dy))
    for k in ("data-pptx-frame", "data-pptx-bounds"):
        if e.get(k) and e.get(k) != "auto":
            e.set(k, shift_frame(e.get(k), dx, dy))
    tf = e.get("transform")
    if tf:
        tf = re.sub(rf"rotate\(\s*({NUM})[\s,]+({NUM})[\s,]+({NUM})\s*\)",
                    lambda m: f"rotate({m.group(1)} {fmt(float(m.group(2)) + dx)} {fmt(float(m.group(3)) + dy)})", tf)
        e.set("transform", tf)


def cmd_move(root, id_, dx, dy):
    for e in find(root, id_).iter():
        if isinstance(e.tag, str):
            shift_el(e, dx, dy)


def cmd_clone(root, id_, dx, dy):
    src = find(root, id_)
    n = 1
    while root.xpath(f'//*[@id="{id_}-c{n}"]'):
        n += 1
    dup = copy.deepcopy(src)
    for e in dup.iter():
        if isinstance(e.tag, str) and e.get("id"):
            e.set("id", f"{e.get('id')}-c{n}")
        if isinstance(e.tag, str):
            shift_el(e, dx, dy)
    src.addnext(dup)
    print(f"cloned {id_} -> {id_}-c{n}")


# ---------- box commands ----------

OBJ = ("shape", "connector", "picture")


def centre(e):
    fr = e.get("data-pptx-frame")
    if fr:
        v = [float(x) for x in re.findall(NUM, fr)]
        if len(v) == 4:
            return v[0] + v[2] / 2, v[1] + v[3] / 2
    n = local(e)
    try:
        if n in ("rect", "use", "image"):
            return float(e.get("x", 0)) + float(e.get("width", 0)) / 2, float(e.get("y", 0)) + float(e.get("height", 0)) / 2
        if n in ("circle", "ellipse"):
            return float(e.get("cx", 0)), float(e.get("cy", 0))
        if n == "text":
            return float(e.get("x", 0)), float(e.get("y", 0))
        if n == "line":
            return (float(e.get("x1", 0)) + float(e.get("x2", 0))) / 2, (float(e.get("y1", 0)) + float(e.get("y2", 0))) / 2
    except ValueError:
        return None
    v = [float(x) for x in re.findall(NUM, e.get("d") or e.get("points") or "")]
    if len(v) >= 2:
        xs, ys = v[0::2], v[1::2]
        return (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    return None


def in_box(root, x, y, w, h):
    """Top-most drawn objects centred in the box (an object group counts once, its children are not listed)."""
    hits = []
    for e in root.iter():
        if not isinstance(e.tag, str):
            continue
        n = local(e)
        is_obj = n == "g" and e.get("data-pptx-object") in OBJ
        if not (is_obj or n in DRAW | {"text", "use", "image"}):
            continue
        if any(a.get("data-pptx-object") in OBJ for a in e.iterancestors(f"{{{SVG}}}g")):
            continue
        if any(local(a) in ("defs", "marker", "clipPath", "mask", "pattern") for a in e.iterancestors()):
            continue
        if root.find(".//{%s}*[@id='page-header']" % SVG) is not None and any(
                a.get("id") in ("page-header", "page-footer") for a in e.iterancestors()):
            continue
        c = centre(e)
        if c and x <= c[0] <= x + w and y <= c[1] <= y + h:
            hits.append(e)
    return hits


MOVED = "data-sam-moved"  # marks objects a movebox already moved in this call (removed before writing)


def cmd_movebox(root, x, y, w, h, dx, dy):
    hits = [e for e in in_box(root, x, y, w, h) if e.get(MOVED) is None]
    for e in hits:
        e.set(MOVED, "1")
    for e in hits:
        for sub in e.iter():
            if isinstance(sub.tag, str):
                shift_el(sub, dx, dy)
    print(f"movebox: {len(hits)} object(s) moved by {fmt(dx)},{fmt(dy)}")


def cmd_delbox(root, x, y, w, h):
    hits = in_box(root, x, y, w, h)
    for e in hits:
        if e.getparent() is not None:
            e.getparent().remove(e)
    print(f"delbox: {len(hits)} object(s) deleted")


def cmd_boxes(root, x, y, w, h):
    for e in in_box(root, x, y, w, h):
        t = "".join(e.itertext()).strip()[:30] if local(e) in ("g", "text") else ""
        print(f"{e.get('id', '-'):16} {local(e):6} {e.get('data-pptx-prst', ''):12} {t}")


PAINT = ("fill", "fill-opacity", "stroke", "stroke-width", "stroke-dasharray", "stroke-opacity", "opacity")


def cmd_style(root, id_, *pairs):
    n = 0
    geo = [e for e in find(root, id_).iter() if isinstance(e.tag, str) and local(e) in DRAW
           and (e.get("data-pptx-part") == "geometry" or e.getparent().get("data-pptx-object") is None)]
    for e in geo:
        for kv in pairs:
            k, v = kv.split("=", 1)
            if k not in PAINT:
                sys.exit(f"style: {k} is not a paint attribute ({', '.join(PAINT)})")
            if k == "stroke-dasharray" and v == "none":
                e.attrib.pop(k, None)
            else:
                e.set(k, v)
        n += 1
    print(f"{id_}: style {' '.join(pairs)} on {n} geometry element(s)")


def cmd_shadow(root, id_, kind="A"):
    defs = root.find(f"{{{SVG}}}defs")
    if defs is None:
        defs = etree.Element(f"{{{SVG}}}defs")
        root.insert(0, defs)
    fid = f"shadow{kind}"
    if kind != "none" and not root.xpath(f'//*[@id="{fid}"]'):
        op = "0.4" if kind == "A" else "0.22"
        defs.append(etree.fromstring(
            f'<filter xmlns="{SVG}" id="{fid}" x="-10%" y="-20%" width="130%" height="160%">'
            f'<feDropShadow dx="2.8" dy="2.8" stdDeviation="2.7" flood-color="#000000" flood-opacity="{op}"/></filter>'))
    n = 0
    for e in find(root, id_).iter():
        if isinstance(e.tag, str) and local(e) in DRAW and (e.get("fill") or "none") != "none":
            if kind == "none":
                e.attrib.pop("filter", None)
            else:
                e.set("filter", f"url(#{fid})")
            n += 1
    print(f"{id_}: shadow {kind} on {n} filled element(s)")


# ---------- color / del / sweep ----------

def cmd_color(root, id_, old, new):
    n = 0
    for e in find(root, id_).iter():
        if not isinstance(e.tag, str):
            continue
        for k in ("fill", "stroke", "stop-color", "flood-color"):
            if (e.get(k) or "").upper() == old.upper():
                e.set(k, new)
                n += 1
    print(f"{id_}: {n} colour value(s) {old} -> {new}")


def cmd_del(root, *ids):
    for id_ in ids:
        e = find(root, id_)
        e.getparent().remove(e)


def cmd_sweep(root):
    fixed = dropped = 0
    for g in list(root.iter(f"{{{SVG}}}g")):
        if g.getparent() is None:
            continue
        if g.get("data-pptx-semantic-object") == "shape":
            carriers = [c for c in g if local(c) in DRAW and c.get("data-pptx-part") == "geometry"]
            if carriers:
                continue
            has_text = any("".join(t.itertext()).strip() for t in g.iter(f"{{{SVG}}}text"))
            frame = [float(v) for v in re.findall(NUM, g.get("data-pptx-frame", ""))]
            if has_text and len(frame) == 4:
                x, y, w, h = frame
                r = etree.Element(f"{{{SVG}}}path", {
                    "d": f"M {fmt(x)} {fmt(y)} L {fmt(x + w)} {fmt(y)} L {fmt(x + w)} {fmt(y + h)} L {fmt(x)} {fmt(y + h)} Z",
                    "fill": "none", "stroke": "none", "data-pptx-part": "geometry"})
                g.insert(0, r)
                fixed += 1
                continue
            g.getparent().remove(g)
            dropped += 1
        elif g.get("data-pptx-replace-with") or g.get("data-pptx-native-authority"):
            continue  # a native chart / table: its content is the JSON <metadata>, never empty
        elif not any(isinstance(c.tag, str) and local(c) not in ("metadata", "title", "desc") for c in g):
            g.getparent().remove(g)
            dropped += 1
    print(f"sweep: {fixed} text-only shape(s) given a frame, {dropped} empty shape(s)/group(s) dropped")


# ---------- main ----------

def run(root, args):
    op, rest = args[0], args[1:]
    if op == "list":
        cmd_list(root)
    elif op == "text":
        idx, fit, width = 0, False, None
        if "--index" in rest:
            i = rest.index("--index")
            idx = int(rest[i + 1])
            rest = rest[:i] + rest[i + 2:]
        if "--width" in rest:
            i = rest.index("--width")
            width = float(rest[i + 1])
            rest = rest[:i] + rest[i + 2:]
        if "--fit" in rest:
            fit = True
            rest.remove("--fit")
        cmd_text(root, rest[0], " ".join(rest[1:]), idx, fit, width)
    elif op == "del":
        cmd_del(root, *rest)
    elif op == "move":
        cmd_move(root, rest[0], float(rest[1]), float(rest[2]))
    elif op == "clone":
        cmd_clone(root, rest[0], float(rest[1]), float(rest[2]))
    elif op == "color":
        cmd_color(root, *rest[:3])
    elif op == "sweep":
        cmd_sweep(root)
    elif op == "style":
        cmd_style(root, *rest)
    elif op == "shadow":
        cmd_shadow(root, *rest[:2])
    elif op in ("movebox", "delbox", "boxes"):
        v = [float(t) for t in rest]
        {"movebox": cmd_movebox, "delbox": cmd_delbox, "boxes": cmd_boxes}[op](root, *v)
        return op != "boxes"
    else:
        sys.exit(f"unknown command {op}")
    return op != "list"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    op, path = sys.argv[1], sys.argv[2]
    tree = etree.parse(path, etree.XMLParser(remove_blank_text=False))
    root = tree.getroot()
    if op == "batch":
        # posix shlex would turn the "\n" line break into a plain "n"
        steps = [[t.replace("\x00", "\\n") for t in shlex.split(s.replace("\\n", "\x00"), posix=True)]
                 for s in sys.argv[3].split(" ; ") if s.strip()]
    else:
        steps = [[op] + sys.argv[3:]]
    changed = False
    for step in steps:
        changed |= run(root, step)
    for e in root.xpath(f"//*[@{MOVED}]"):
        del e.attrib[MOVED]
    if changed:
        tree.write(path, encoding="utf-8", xml_declaration=False)


if __name__ == "__main__":
    main()
