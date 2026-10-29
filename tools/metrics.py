"""Pixel metrics for rendered slides (1600x900 PNG), and comparison against the R&B baseline.

    python metrics.py <png-folder> [--out <csv>]                      measure every *.png
    python metrics.py <png-folder> --baseline <csv> [--out <csv>]     measure and flag pages outside
                                                                      the baseline's P5-P95 range

Metrics, each a share of the whole page (0-1):
  coverage     share of 25x25 cells holding visible content (>2% of the cell's pixels not near-white,
               min channel < 250); low = sparse page
  solid        share of pixels in filled areas: min channel < 235, kept only where a 5x5 window is
               entirely filled (erosion), so text strokes and thin lines drop out
  dark_solid   same as solid, for dark pixels only (luminance < 110): navy/brick bars, dark cards
  colour       share of strongly coloured pixels (max - min channel > 60), text included
"""
import argparse
import csv
import sys
from pathlib import Path

import numpy as np
from PIL import Image

METRICS = ["coverage", "solid", "dark_solid", "colour"]
CELL = 25


def erode5(mask):
    """True where the 5x5 window centred on the pixel is entirely True."""
    m = np.pad(mask.astype(np.int32), 2)
    s = m.cumsum(0).cumsum(1)
    s = np.pad(s, ((1, 0), (1, 0)))
    win = s[5:, 5:] - s[:-5, 5:] - s[5:, :-5] + s[:-5, :-5]
    return win == 25


def measure(path):
    im = np.asarray(Image.open(path).convert("RGB")).astype(np.int32)
    if im.shape[:2] != (900, 1600):
        im = np.asarray(Image.open(path).convert("RGB").resize((1600, 900))).astype(np.int32)
    lo, hi = im.min(2), im.max(2)
    lum = im @ np.array([0.299, 0.587, 0.114])
    visible = lo < 250
    cells = visible.reshape(900 // CELL, CELL, 1600 // CELL, CELL).mean((1, 3)) > 0.02
    filled = erode5(lo < 235)
    dark = erode5(lum < 110)
    return {
        "coverage": cells.mean(),
        "solid": filled.mean(),
        "dark_solid": dark.mean(),
        "colour": ((hi - lo) > 60).mean(),
    }


def load_baseline(path):
    with open(path, encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f)]
    return {k: np.percentile([float(r[k]) for r in rows], [5, 50, 95]) for k in METRICS}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder")
    ap.add_argument("--baseline")
    ap.add_argument("--out")
    args = ap.parse_args()
    pngs = sorted(Path(args.folder).glob("*.png"))
    if not pngs:
        sys.exit(f"no PNG in {args.folder}")
    rows = [{"page": p.stem, **{k: round(float(v), 4) for k, v in measure(p).items()}} for p in pngs]
    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, ["page"] + METRICS)
            w.writeheader()
            w.writerows(rows)
    base = load_baseline(args.baseline) if args.baseline else None
    print("page      " + "".join(f"{k:>12}" for k in METRICS))
    for r in rows:
        cols = []
        for k in METRICS:
            flag = ""
            if base is not None:
                p5, _, p95 = base[k]
                flag = "-" if r[k] < p5 else "+" if r[k] > p95 else ""
            cols.append(f"{r[k]:>11.3f}{flag or ' '}")
        print(f"{r['page']:<10}" + "".join(cols))
    vals = {k: np.array([r[k] for r in rows]) for k in METRICS}
    for name, q in (("P5", 5), ("median", 50), ("P95", 95)):
        print(f"{name:<10}" + "".join(f"{np.percentile(vals[k], q):>11.3f} " for k in METRICS))
    if base is not None:
        print("baseline  " + "".join(f"{base[k][0]:>5.3f}-{base[k][2]:<5.3f} " for k in METRICS))
        print("flags: - below baseline P5, + above baseline P95")


if __name__ == "__main__":
    main()
