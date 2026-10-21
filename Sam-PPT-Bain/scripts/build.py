# -*- coding: utf-8 -*-
"""Sam-PPT-Bain: deck.json -> editable PPTX in the 参考模板-template consulting style.

Every run gets its own folder:  <skill>/runs/run-yyyymmdd-hhmmss-fff/
    deck.json        the input that was built (copied)
    <title>.pptx     the deck
    render/          PowerPoint renders, one PNG per slide
    contact.png      all slides on one sheet
    qa.md            automatic check results

Usage:
    python build.py deck.json                 # new run folder
    python build.py deck.json --run <dir>     # rebuild into an existing run folder
    python build.py deck.json --no-render     # skip PowerPoint rendering
"""
import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
sys.path.insert(0, HERE)

from samppt.deck import Deck              # noqa: E402
from samppt.layouts import REGISTRY       # noqa: E402
from samppt import qa                     # noqa: E402


def new_run_dir():
    ts = datetime.datetime.now()
    name = ts.strftime("run-%Y%m%d-%H%M%S-") + f"{ts.microsecond // 1000:03d}"
    path = os.path.join(SKILL, "runs", name)
    os.makedirs(path)
    return path


def build(spec, out_path):
    D = Deck(spec.get("meta", {}))
    for i, s in enumerate(spec["slides"], 1):
        lay = s.get("layout")
        if lay not in REGISTRY:
            raise SystemExit(f"slide {i}: unknown layout '{lay}'. Known: {', '.join(sorted(REGISTRY))}")
        try:
            REGISTRY[lay](D, s)
        except KeyError as e:
            raise SystemExit(f"slide {i} ({lay}): missing field {e}")
    D.save(out_path)


def render(pptx, out_dir):
    ps = os.path.join(HERE, "render.ps1")
    r = subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", ps, "-Deck", pptx, "-OutDir", out_dir],
                       capture_output=True, text=True)
    return r.returncode == 0, (r.stdout + r.stderr).strip()


def contact_sheet(render_dir, out, cols=3, w=640):
    from PIL import Image, ImageDraw
    files = sorted(f for f in os.listdir(render_dir) if f.endswith(".png"))
    if not files:
        return
    h = int(w * 9 / 16)
    rows = (len(files) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (w + 12) + 12, rows * (h + 12) + 12), "white")
    d = ImageDraw.Draw(sheet)
    for k, f in enumerate(files):
        im = Image.open(os.path.join(render_dir, f)).convert("RGB").resize((w, h))
        x, y = 12 + (k % cols) * (w + 12), 12 + (k // cols) * (h + 12)
        sheet.paste(im, (x, y))
        d.rectangle([x, y, x + w - 1, y + h - 1], outline="#BFBFBF")
        d.rectangle([x, y, x + 34, y + 20], fill="#1C4274")
        d.text((x + 6, y + 4), f"{k + 1:02d}", fill="white")
    sheet.save(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("--run")
    ap.add_argument("--no-render", action="store_true")
    a = ap.parse_args()
    with open(a.deck, encoding="utf8") as f:
        spec = json.load(f)
    run = a.run or new_run_dir()
    os.makedirs(run, exist_ok=True)
    if os.path.abspath(a.deck) != os.path.abspath(os.path.join(run, "deck.json")):
        shutil.copyfile(a.deck, os.path.join(run, "deck.json"))
    title = spec.get("meta", {}).get("file_name") or spec.get("meta", {}).get("title", "deck")
    out = os.path.join(run, f"{title}.pptx")
    build(spec, out)
    prs, findings = qa.run_all(out)
    rendered, msg = (False, "skipped")
    if not a.no_render:
        rendered, msg = render(out, os.path.join(run, "render"))
        if rendered:
            contact_sheet(os.path.join(run, "render"), os.path.join(run, "contact.png"))
    lines = [f"# QA – {title}", "", f"- slides: {len(prs.slides)}",
             f"- PowerPoint render: {'OK' if rendered else 'FAILED / skipped'} ({msg})",
             f"- automatic findings: {len(findings)}", ""]
    if findings:
        lines += ["| slide | check | shape | detail |", "|---|---|---|---|"]
        lines += [f"| {x['slide']} | {x['check']} | {x['shape']} | {x['detail']} |" for x in findings]
    lines += ["", "Next: open contact.png / render/*.png and walk the visual checklist in references/qa-checklist.md."]
    with open(os.path.join(run, "qa.md"), "w", encoding="utf8") as f:
        f.write("\n".join(lines))
    print(f"run: {run}\npptx: {out}\nrender: {msg}\nfindings: {len(findings)}")
    for x in findings:
        print(f"  [{x['check']}] slide {x['slide']} {x['shape']}: {x['detail']}")
    if not a.no_render and not rendered:
        sys.exit(2)


if __name__ == "__main__":
    main()
