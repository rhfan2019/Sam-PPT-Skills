"""Put each finished page next to the reference pages its modules came from (step 7).

  python compare_pages.py <project>/svg_output <renders_dir> <library_dir> -o <run_dir>/work/compare

For page NN it reads the "composed:" comment that compose_page.py writes (or the "blueprint:" comment of
start_page.py), and writes <out>/compare-NN.png: the deck's render on the left, the source reference
pages (renders/slide-NN.png, module boxes outlined in red) on the right. Look at each pair at the same
size and ask: does my page carry as many drawn parts, icons, tinted panels, solid circles and red as
the reference page does in the same area? Text that sits as long paragraphs on white, where the
reference has labelled chunks, is the usual gap. renders are 1600 px wide; SVG coordinates are px × 0.8.
"""
import argparse
import re
from pathlib import Path

from PIL import Image, ImageDraw

W, H = 800, 450


def sources(svg: Path):
    s = svg.read_text(encoding="utf-8")[:6000]
    mods = re.findall(r"module \d+: slide_(\d+)\.svg ([\d.]+),([\d.]+),([\d.]+),([\d.]+)", s)
    if mods:
        out = {}
        for page, *box in mods:
            out.setdefault(page, []).append([float(v) for v in box])
        return out
    m = re.search(r"blueprint: slide_(\d+)\.svg", s)
    return {m.group(1): []} if m else {}


def thumb(png: Path, boxes=()):
    im = Image.open(png).convert("RGB").resize((1600, 900))
    d = ImageDraw.Draw(im)
    for x, y, w, h in boxes:
        k = 1600 / 1280
        d.rectangle((x * k, y * k, (x + w) * k, (y + h) * k), outline="#E02020", width=5)
    return im.resize((W, H))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svg_dir", type=Path)
    ap.add_argument("renders", type=Path)
    ap.add_argument("library", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    pages = sorted(a.svg_dir.glob("*.svg"))
    n = 0
    for i, svg in enumerate(pages, 1):
        mine = a.renders / f"slide-{i:02d}.png"
        src = sources(svg)
        if not mine.exists() or not src:
            continue
        refs = [thumb(a.library / "renders" / f"slide-{p}.png", boxes) for p, boxes in list(src.items())[:3]
                if (a.library / "renders" / f"slide-{p}.png").exists()]
        sheet = Image.new("RGB", (W * (1 + len(refs)) + 12 * len(refs), H + 30), "white")
        d = ImageDraw.Draw(sheet)
        sheet.paste(thumb(mine), (0, 30))
        d.text((6, 6), f"P{i:02d} {svg.stem}", fill="black")
        for k, (im, p) in enumerate(zip(refs, src)):
            x = (W + 12) * (k + 1)
            sheet.paste(im, (x, 30))
            d.text((x + 6, 6), f"reference slide {p}", fill="black")
        sheet.save(a.out / f"compare-{i:02d}.png")
        n += 1
    print(f"{n} comparison sheet(s) -> {a.out}")


if __name__ == "__main__":
    main()
