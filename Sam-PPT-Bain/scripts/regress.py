# -*- coding: utf-8 -*-
"""Regression: rebuild every examples/*.json, render with PowerPoint and pixel-compare with tests/baseline/.

    python scripts/regress.py            # compare, print changed slides, exit 1 if any slide changed
    python scripts/regress.py --update   # accept the current renders as the new baseline (after reviewing them)

Baselines are stored at 960x540 so they can live in git. A slide counts as changed when more than
0.05 % of its pixels differ by more than 40/255 on any channel.
"""
import argparse
import glob
import json
import os
import shutil
import subprocess
import sys

from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
BASE = os.path.join(SKILL, "tests", "baseline")
SIZE = (960, 540)
TOL = 0.0005


def build(example):
    out = subprocess.run([sys.executable, os.path.join(HERE, "build.py"), example], capture_output=True, text=True,
                         encoding="utf8", env={**os.environ, "PYTHONIOENCODING": "utf8"})
    print(out.stdout.strip())
    if out.returncode != 0:
        print(out.stderr)
        raise SystemExit(f"build failed: {example}")
    return next(l.split("run: ", 1)[1] for l in out.stdout.splitlines() if l.startswith("run: "))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--update", action="store_true")
    a = ap.parse_args()
    changed = 0
    for ex in sorted(glob.glob(os.path.join(SKILL, "examples", "*.json"))):
        name = os.path.splitext(os.path.basename(ex))[0]
        run = build(ex)
        bdir = os.path.join(BASE, name)
        renders = sorted(glob.glob(os.path.join(run, "render", "slide-*.png")))
        if a.update:
            shutil.rmtree(bdir, ignore_errors=True)
            os.makedirs(bdir)
            for r in renders:
                Image.open(r).convert("RGB").resize(SIZE).save(os.path.join(bdir, os.path.basename(r)), optimize=True)
            print(f"[{name}] baseline updated ({len(renders)} slides)")
            continue
        olds = sorted(glob.glob(os.path.join(bdir, "slide-*.png")))
        if len(olds) != len(renders):
            print(f"[{name}] slide count {len(olds)} -> {len(renders)}")
            changed += 1
        for r in renders:
            ref = os.path.join(bdir, os.path.basename(r))
            if not os.path.exists(ref):
                print(f"[{name}] {os.path.basename(r)}: new slide (no baseline)")
                changed += 1
                continue
            d = ImageChops.difference(Image.open(ref).convert("RGB"), Image.open(r).convert("RGB").resize(SIZE)).convert("L")
            d = d.point(lambda v: 255 if v > 40 else 0)
            frac = d.histogram()[255] / (SIZE[0] * SIZE[1])
            if frac > TOL:
                changed += 1
                bb = d.getbbox()
                print(f"[{name}] {os.path.basename(r)}: {frac:.2%} changed, region {bb} (of 960x540)  run: {run}")
    if not a.update:
        print("regression:", "no visual change" if not changed else f"{changed} slide(s) changed - review the renders,"
              " then run with --update if the change is intended")
        sys.exit(1 if changed else 0)


if __name__ == "__main__":
    main()
