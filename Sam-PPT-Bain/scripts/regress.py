# -*- coding: utf-8 -*-
"""Regression: rebuild every examples/*.json, render with PowerPoint and pixel-compare with tests/baseline/.

Each baseline slide has a status (tests/baseline/STATUS.json):
  approved     – the user confirmed this look. Any visual change FAILS the run until the user re-approves it.
  provisional  – a snapshot only; the look has NOT been accepted and is expected to change. Changes are listed
                 for review but do not fail the run.

    python scripts/regress.py                       # compare
    python scripts/regress.py --update              # refresh provisional snapshots only
    python scripts/regress.py --approve nev-report:5,6   # after the USER confirmed these slides: store and mark approved
    python scripts/regress.py --update-approved nev-report:4  # user confirmed a change to an already-approved slide

Baselines are 960x540 so they can live in git. A slide counts as changed when more than 0.05 % of its pixels
differ by more than 40/255.
"""
import argparse
import glob
import json
import os
import subprocess
import sys

from PIL import Image, ImageChops

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
BASE = os.path.join(SKILL, "tests", "baseline")
STATUS = os.path.join(BASE, "STATUS.json")
SIZE = (960, 540)
TOL = 0.0005


def build(example):
    out = subprocess.run([sys.executable, os.path.join(HERE, "build.py"), example], capture_output=True, text=True,
                         encoding="utf8", env={**os.environ, "PYTHONIOENCODING": "utf8"})
    if out.returncode != 0:
        print(out.stdout, out.stderr)
        raise SystemExit(f"build failed: {example}")
    return next(l.split("run: ", 1)[1] for l in out.stdout.splitlines() if l.startswith("run: "))


def parse_spec(spec):
    """'deck:1,2;deck2:3' -> {deck: {1, 2}, deck2: {3}}"""
    out = {}
    for part in filter(None, (spec or "").split(";")):
        name, _, nums = part.partition(":")
        out[name] = {int(n) for n in nums.split(",") if n}
    return out


def diff(ref, cur):
    d = ImageChops.difference(Image.open(ref).convert("RGB"), Image.open(cur).convert("RGB").resize(SIZE)).convert("L")
    d = d.point(lambda v: 255 if v > 40 else 0)
    return d.histogram()[255] / (SIZE[0] * SIZE[1]), d.getbbox()


def save(cur, dst):
    Image.open(cur).convert("RGB").resize(SIZE).save(dst, optimize=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--update", action="store_true", help="refresh provisional snapshots")
    ap.add_argument("--approve", help="deck:slides the user has just confirmed, e.g. nev-report:5,6")
    ap.add_argument("--update-approved", help="deck:slides whose CHANGE the user has confirmed")
    a = ap.parse_args()
    status = json.load(open(STATUS, encoding="utf8"))
    approve, reapprove = parse_spec(a.approve), parse_spec(a.update_approved)
    fails, infos = [], []
    for ex in sorted(glob.glob(os.path.join(SKILL, "examples", "*.json"))):
        name = os.path.splitext(os.path.basename(ex))[0]
        run = build(ex)
        print(f"[{name}] run: {run}")
        st = status.setdefault(name, {"approved": []})
        approved = set(st["approved"])
        bdir = os.path.join(BASE, name)
        os.makedirs(bdir, exist_ok=True)
        renders = sorted(glob.glob(os.path.join(run, "render", "slide-*.png")))
        for k, cur in enumerate(renders, 1):
            ref = os.path.join(bdir, os.path.basename(cur))
            if k in approve.get(name, set()) or k in reapprove.get(name, set()):
                save(cur, ref)
                approved.add(k)
                infos.append(f"[{name}] slide {k:02d}: stored as APPROVED")
                continue
            if not os.path.exists(ref):
                save(cur, ref)
                infos.append(f"[{name}] slide {k:02d}: new provisional snapshot")
                continue
            frac, bb = diff(ref, cur)
            if frac <= TOL:
                continue
            msg = f"[{name}] slide {k:02d}: {frac:.2%} changed, region {bb} of 960x540"
            if k in approved:
                fails.append(msg + "  <- APPROVED slide changed: show the user before accepting")
            else:
                infos.append(msg + "  (provisional)")
                if a.update:
                    save(cur, ref)
        st["approved"] = sorted(approved)
    json.dump(status, open(STATUS, "w", encoding="utf8"), ensure_ascii=False, indent=2)
    for m in infos:
        print(m)
    for m in fails:
        print(m)
    if fails:
        print(f"regression FAILED: {len(fails)} approved slide(s) changed. If the user confirmed the change, "
              f"rerun with --update-approved <deck>:<slides>.")
        sys.exit(1)
    print("regression OK: no approved slide changed" + ("" if a.update else
          " (provisional changes are listed above; refresh them with --update)"))


if __name__ == "__main__":
    main()
