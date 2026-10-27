"""Start a page from its blueprint: copy the reference page's SVG into svg_output and
strip only what cannot carry over, so the page is edited from the blueprint, not redrawn.

Kept as native shapes: the reference's small vector icons (the header hand, icon badges), converted
from <image href="*.svg"> to editable paths by inline_icons.py.
Removed:
- other <image> elements and the nested <svg> picture-crop wrappers around them (reference
  logos, photos, product shots; never reused);
- connector bindings to other shapes (data-pptx-start/end-shape-*), which may point
  at removed pictures; the connector keeps its drawn geometry;
- data-pptx-geometry-kind="custom", whose source metadata stays in the import
  workspace; the path is exported as a plain freeform from its own d.
Everything else (coordinates, presets, gradients, shadows, alpha, text boxes with the
reference text) stays, to be edited in place.

Usage: python start_page.py <import_workspace>/authoring-svg-flat/slide_NN.svg <project>/svg_output/NN_name.svg
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from inline_icons import inline_icons  # noqa: E402


def strip(svg: str, images_dir: Path | None = None) -> tuple[str, dict]:
    head_end = svg.index(">", svg.index("<svg")) + 1
    head, body = svg[:head_end], svg[head_end:]
    stats = {}
    body, stats["icons_to_native"] = inline_icons(body, images_dir)
    body, stats["images"] = re.subn(r"<image\b[^>]*?(?:/>|>.*?</image>)", "", body, flags=re.S)
    body, stats["crop_wrappers"] = re.subn(r"<svg\b[^>]*?(?:/>|>.*?</svg>)", "", body, flags=re.S)
    body, stats["connector_bindings"] = re.subn(
        r'\s+data-pptx-(?:start|end)-(?:shape-id|shape-scope|site)="[^"]*"', "", body)
    body, stats["custom_geometry"] = re.subn(r'\s+data-pptx-geometry-kind="custom"', "", body)
    body, stats["imported_illustrations"] = re.subn(
        r'<use\b[^>]*data-icon="imported/[^"]*"[^>]*?(?:/>|>.*?</use>)', "", body, flags=re.S)
    body, stats["stroke_gradients_to_solid"] = solid_stroke_gradients(body)
    body, stats["group_filters_moved"] = move_group_filters(body)
    head, k1 = fix_fonts(head)
    body, k2 = fix_fonts(body)
    stats["fonts_to_opposans"] = k1 + k2
    return head + body, stats


THEME_FACE = {"+mj-lt": "OPPOSans H", "+mn-lt": "OPPOSans R"}


def fix_fonts(text):
    """Reference faces other than OPPOSans (Arial, 思源黑体, 阿里巴巴普惠体, theme refs) become OPPOSans."""
    n = 0

    def tag(m):
        nonlocal n
        t = m.group(0)
        fam = re.search(r'font-family="([^"]*)"', t)
        if not fam:
            return t
        first = fam.group(1).replace("&quot;", "").split(",")[0].strip()
        if first.startswith("OPPOSans"):
            return t
        if first in THEME_FACE:
            face = THEME_FACE[first]
        elif re.search(r"Bold|Heavy|Black|\bB$|\bH$", first) or 'font-weight="bold"' in t:
            face = "OPPOSans B"
        else:
            face = "OPPOSans R"
        n += 1
        return t.replace(fam.group(0), f'font-family="&quot;{face}&quot;, sans-serif"')

    return re.sub(r"<[^>]*\bfont-family=\"[^\"]*\"[^>]*>", tag, text), n


def solid_stroke_gradients(body):
    """Imported stroke gradients use userSpaceOnUse, which the checker rejects: use the first stop colour."""
    first = {}
    for m in re.finditer(r'<(?:linear|radial)Gradient\b[^>]*id="(mstrokegrad[^"]*)"[^>]*>(.*?)</(?:linear|radial)Gradient>', body, re.S):
        stop = re.search(r'stop-color="([^"]+)"', m.group(2))
        if stop:
            first[m.group(1)] = stop.group(1)
    n = 0
    for gid, colour in first.items():
        body, k = re.subn(r'stroke="url\(#' + re.escape(gid) + r'\)"', f'stroke="{colour}"', body)
        n += k
        body = re.sub(r'<(linear|radial)Gradient\b[^>]*id="' + re.escape(gid) + r'"[^>]*>.*?</\1Gradient>', "", body, flags=re.S)
    return body, n


def move_group_filters(body):
    """The checker rejects filter on <g>: put it on each drawable child instead."""
    n = 0

    def one(m):
        nonlocal n
        n += 1
        open_tag, flt, inner = m.group(1) + m.group(3), m.group(2), m.group(4)
        inner = re.sub(r"<(rect|circle|ellipse|path|polygon)\b(?![^>]*\bfilter=)", rf'<\1 filter="{flt}"', inner)
        return open_tag + inner + "</g>"

    pattern = r'(<g\b[^>]*?)\s+filter="([^"]+)"([^>]*>)((?:(?!<g\b).)*?)</g>'
    return re.sub(pattern, one, body, flags=re.S), n


def main():
    src, dst = Path(sys.argv[1]), Path(sys.argv[2])
    out, stats = strip(src.read_text(encoding="utf-8"), src.parent.parent / "images")
    dst.parent.mkdir(parents=True, exist_ok=True)
    root_end = out.index(">", out.index("<svg")) + 1
    out = out[:root_end] + f"\n<!-- blueprint: {src.name} -->" + out[root_end:]  # read by check_reuse.py
    dst.write_text(out, encoding="utf-8")
    texts = len(re.findall(r"<text\b", out))
    print(f"{dst.name}: from {src.name}; removed " + ", ".join(f"{k}={v}" for k, v in stats.items())
          + f"; {texts} reference text element(s) left to rewrite")


if __name__ == "__main__":
    main()
