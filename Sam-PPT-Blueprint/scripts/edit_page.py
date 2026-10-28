"""Edit a started page in place, by element id (step 4). Keeps every other attribute.

  python edit_page.py list  <page.svg>                      top-level modules: id, kind, frame, text
  python edit_page.py text  <page.svg> <id> "new text" [--index N]
                            replace the N-th (default 0) <text> inside <id>; "\\n" starts a new line
  python edit_page.py del   <page.svg> <id> [<id> ...]      delete whole modules
  python edit_page.py move  <page.svg> <id> <dx> <dy>       shift a module (rewrites coordinates)
  python edit_page.py clone <page.svg> <id> <dx> <dy>       copy a module next to itself, ids get a -cN suffix
  python edit_page.py color <page.svg> <id> <#OLD> <#NEW>   swap one colour inside a module (fill/stroke/stop)
  python edit_page.py sweep <page.svg>                      after deleting parts: give text-only shapes a
                            transparent frame, drop shapes and groups left with nothing to draw

Several commands can run in one call, separated by " ; " inside one quoted argument:
  python edit_page.py batch <page.svg> "del shape-12 shape-13 ; text shape-3 标题 ; move shape-40 0 -20"
"""
import copy
import re
import shlex
import sys

from lxml import etree

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

def cmd_text(root, id_, new, index=0):
    el = find(root, id_)
    texts = [el] if local(el) == "text" else list(el.iter(f"{{{SVG}}}text"))
    if index >= len(texts):
        sys.exit(f"{id_} has {len(texts)} <text> element(s); --index {index} is out of range")
    t = texts[index]
    first = next(iter(t.iter(f"{{{SVG}}}tspan")), None)
    style = {k: v for k, v in (first.attrib.items() if first is not None else []) if k not in ("x", "y", "dx", "dy")}
    size = float(re.findall(NUM, t.get("font-size") or style.get("font-size") or "14")[0])
    for c in list(t):
        t.remove(c)
    lines = new.replace("\\n", "\n").split("\n")
    if len(lines) == 1 and not style:
        t.text = lines[0]
        return
    t.text = None
    for i, line in enumerate(lines):
        sp = etree.SubElement(t, f"{{{SVG}}}tspan", style)
        sp.set("x", t.get("x", "0"))
        if i:
            sp.set("dy", fmt(size * 1.3))
        sp.text = line


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
        idx = 0
        if "--index" in rest:
            i = rest.index("--index")
            idx = int(rest[i + 1])
            rest = rest[:i] + rest[i + 2:]
        cmd_text(root, rest[0], " ".join(rest[1:]), idx)
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
    if changed:
        tree.write(path, encoding="utf-8", xml_declaration=False)


if __name__ == "__main__":
    main()
