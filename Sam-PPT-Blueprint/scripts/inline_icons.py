"""Turn the reference's small vector icons (<image href="../images/*.svg">, at most MAX_SIDE px) into
native editable paths, so the header hand and the reference's own icons survive start_page instead of
being deleted with the photos. Office icons are plain M/L/C/Z paths, rects and circles under scale /
matrix transforms with class-based fills; anything else is left as an <image> for strip to remove.
"""
import re
from pathlib import Path

from lxml import etree

SVG = "http://www.w3.org/2000/svg"
NUM = r"-?\d*\.?\d+(?:[eE][-+]?\d+)?"
MAX_SIDE = 64
K = 0.5522847498  # cubic Bezier circle constant


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def local(e):
    return etree.QName(e).localname if isinstance(e.tag, str) else ""


def mul(m, n):
    a, b, c, d, e, f = m
    a2, b2, c2, d2, e2, f2 = n
    return (a * a2 + c * b2, b * a2 + d * b2, a * c2 + c * d2, b * c2 + d * d2, a * e2 + c * f2 + e, b * e2 + d * f2 + f)


def parse_transform(t):
    m = (1, 0, 0, 1, 0, 0)
    for name, args in re.findall(r"(\w+)\(([^)]*)\)", t or ""):
        v = [float(x) for x in re.findall(NUM, args)]
        if name == "matrix" and len(v) == 6:
            n = tuple(v)
        elif name == "scale":
            n = (v[0], 0, 0, v[1] if len(v) > 1 else v[0], 0, 0)
        elif name == "translate":
            n = (1, 0, 0, 1, v[0], v[1] if len(v) > 1 else 0)
        else:
            raise ValueError(name)
        m = mul(m, n)
    return m


def pt(m, x, y):
    a, b, c, d, e, f = m
    return a * x + c * y + e, b * x + d * y + f


def map_d(d, m):
    out, cmd, buf = [], None, []
    for tok in re.findall(rf"[A-Za-z]|{NUM}", d):
        if tok.isalpha():
            if tok not in "MLCZz":
                raise ValueError(tok)
            cmd = tok
            out.append(tok.upper())
            continue
        buf.append(float(tok))
        if len(buf) == 2:
            x, y = pt(m, *buf)
            out += [fmt(x), fmt(y)]
            buf = []
    return " ".join(out)


def shape_d(e):
    n = lambda k: float(e.get(k, "0"))  # noqa: E731
    if local(e) == "path":
        return e.get("d", "")
    if local(e) == "rect":
        x, y, w, h = n("x"), n("y"), n("width"), n("height")
        return f"M {x} {y} L {x + w} {y} L {x + w} {y + h} L {x} {y + h} Z"
    if local(e) in ("circle", "ellipse"):
        cx, cy = n("cx"), n("cy")
        rx = n("r") if local(e) == "circle" else n("rx")
        ry = n("r") if local(e) == "circle" else n("ry")
        kx, ky = rx * K, ry * K
        return (f"M {cx + rx} {cy} C {cx + rx} {cy + ky} {cx + kx} {cy + ry} {cx} {cy + ry} "
                f"C {cx - kx} {cy + ry} {cx - rx} {cy + ky} {cx - rx} {cy} "
                f"C {cx - rx} {cy - ky} {cx - kx} {cy - ry} {cx} {cy - ry} "
                f"C {cx + kx} {cy - ry} {cx + rx} {cy - ky} {cx + rx} {cy} Z")
    return None


def icon_paths(icon_file: Path, x, y, w, h):
    root = etree.parse(str(icon_file)).getroot()
    vb = [float(v) for v in re.findall(NUM, root.get("viewBox", ""))]
    if len(vb) != 4:
        raise ValueError("viewBox")
    classes = {}
    for st in root.iter(f"{{{SVG}}}style"):
        for names, body in re.findall(r"([^{}]+)\{([^}]*)\}", st.text or ""):
            fill = re.search(r"fill\s*:\s*([^;]+)", body)
            for cname in re.findall(r"\.([\w-]+)", names):
                if fill:
                    classes[cname] = fill.group(1).strip()
    base = mul((1, 0, 0, 1, x, y), (w / vb[2], 0, 0, h / vb[3], -vb[0] * w / vb[2], -vb[1] * h / vb[3]))
    out = []

    def walk(e, m, fill, opacity):
        for c in e:
            if not isinstance(c.tag, str) or local(c) in ("style", "defs", "title", "desc", "metadata"):
                continue
            mm = mul(m, parse_transform(c.get("transform")))
            f = c.get("fill") or classes.get((c.get("class") or "").split(" ")[0]) or fill
            op = c.get("fill-opacity") or c.get("opacity") or opacity
            if local(c) == "g":
                walk(c, mm, f, op)
                continue
            d = shape_d(c)
            if d is None:
                raise ValueError(local(c))
            if f == "none":
                continue
            out.append((map_d(d, mm), f, op, c.get("fill-rule")))

    walk(root, base, "#000000", None)
    return out


def inline_icons(body: str, images_dir: Path, prefix="icon"):
    """Replace small vector <image> icons in an SVG body by groups of native paths. Returns (body, count)."""
    n = 0

    def one(mt):
        nonlocal n
        tag = mt.group(0)
        href = re.search(r'href="\.\./images/([^"]+\.svg)"', tag)
        frame = re.search(r'data-pptx-frame="([^"]+)"', tag)
        if not href or not frame or not images_dir:
            return tag
        x, y, w, h = [float(v) for v in frame.group(1).split()]
        f = Path(images_dir) / href.group(1)
        if max(w, h) > MAX_SIDE or not f.exists():
            return tag
        try:
            paths = icon_paths(f, x, y, w, h)
        except (ValueError, etree.XMLSyntaxError):
            return tag
        n += 1
        parts = []
        for k, (d, fill, op, rule) in enumerate(paths):
            extra = (f' fill-opacity="{op}"' if op else "") + (f' fill-rule="{rule}"' if rule else "")
            parts.append(f'<path id="{prefix}{n}-p{k}" d="{d}" fill="{fill}" stroke="none"{extra} />')
        return (f'<g id="{prefix}{n}" data-reference-icon="{href.group(1)}" data-pptx-frame="{fmt(x)} {fmt(y)} {fmt(w)} {fmt(h)}">'
                + "".join(parts) + "</g>")

    return re.sub(r"<image\b[^>]*?(?:/>|>.*?</image>)", one, body, flags=re.S), n
