"""Thin wrapper that runs ppt-master's Quick Generate route with the Sam Bain template.

ppt-master does the work (project layout, template install, typography calibration,
SVG checks, native PPTX export); this script only fixes the Sam-PPT-Bain choices:
the run folder convention, the installed template, the recurring type roles, the
OPPOSans CJK repair after export, and the PowerPoint render check.

  python sam_bain.py new <slug> [--source outline.md ...]   create runs/run-*/<slug>_<date>/
  python sam_bain.py photos <project> city_tech.png ...     copy stock photos into images/
  python sam_bain.py icons <project> chunk-filled/bolt ...  sync library icons into icons/
  python sam_bain.py check <project> [--early]              ppt-master SVG quality gate
  python sam_bain.py finish <project> [--name 文件名]        check, export, fix fonts, render
"""
import argparse
import datetime as dt
import glob
import os
import shutil
import subprocess
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL / "template"
PHOTOS = SKILL / "assets" / "photos"
RUNS = SKILL / "runs"

# Recurring type roles of the Sam Bain deck (family:size in px on the 1280x720 canvas).
ROLES = [
    "title:OPPOSans H:37.33",
    "thesis:OPPOSans M:26.67",
    "thesis_small:OPPOSans M:22.67",
    "thesis_xs:OPPOSans M:21.33",
    "zone:OPPOSans M:24",
    "item:OPPOSans M:17.33",
    "label:OPPOSans M:14.67",
    "body:OPPOSans R:13.33",
    "note:OPPOSans R:10.67",
    "num:OPPOSans B:21.33",
    "bignum:OPPOSans B:32",
    "hero:OPPOSans B:56",
]


def ppt_master_dir():
    env = os.environ.get("PPT_MASTER_DIR")
    if env:
        return Path(env)
    pattern = str(Path.home() / ".claude/plugins/cache/ppt-master/ppt-master/*/ppt-master/SKILL.md")
    found = sorted(glob.glob(pattern), key=os.path.getmtime)
    if not found:
        sys.exit("ppt-master not found; install the ppt-master plugin or set PPT_MASTER_DIR")
    return Path(found[-1]).parent


PM = ppt_master_dir()


def run(args, check=True):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    print("$", " ".join(str(a) for a in args), flush=True)
    res = subprocess.run([str(a) for a in args], env=env)
    if check and res.returncode != 0:
        sys.exit(f"command failed with exit code {res.returncode}")
    return res.returncode


def pm(script, *args, check=True):
    return run([sys.executable, PM / "scripts" / script, *args], check=check)


def cmd_new(a):
    pm("attribution_guard.py")
    now = dt.datetime.now()
    run_dir = RUNS / f"run-{now:%Y%m%d-%H%M%S}-{now.microsecond // 1000:03d}"
    run_dir.mkdir(parents=True)
    pm("project_manager.py", "init", f"{a.slug}_{now:%Y%m%d}", "--format", "ppt169",
       "--dir", run_dir, "--quick-generate")
    project = next(p for p in run_dir.iterdir() if p.is_dir())
    pm("apply_template.py", project, "--root", TEMPLATE)
    if a.source:
        pm("project_manager.py", "import-sources", project, *a.source, "--copy")
    pm("text_measure.py", "calibrate", project, *[x for r in ROLES for x in ("--role", r)])
    print(f"\nRUN_DIR={run_dir}\nPROJECT={project}")


def cmd_photos(a):
    project = Path(a.project)
    for name in a.names:
        src = PHOTOS / name
        if not src.exists():
            sys.exit(f"no stock photo {name}; available: {', '.join(sorted(p.name for p in PHOTOS.iterdir()))}")
        shutil.copy2(src, project / "images" / name)
    pm("analyze_images.py", project / "images")


def cmd_icons(a):
    pm("icon_sync.py", a.project, *a.icons)


def checker(project, stage):
    return pm("svg_quality_checker.py", project, "--quick-generate", "--canonical-authoring",
              "--stage", stage, "--json", check=False)


def cmd_check(a):
    sys.exit(checker(a.project, "early" if a.early else "final"))


def contact_sheet(render_dir, out):
    from PIL import Image
    pages = sorted(render_dir.glob("slide-*.png"))
    if not pages:
        return
    cols, w = 4, 480
    h = round(w * 9 / 16)
    rows = (len(pages) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * w + (cols + 1) * 12, rows * h + (rows + 1) * 12), "#7F7F7F")
    for i, p in enumerate(pages):
        im = Image.open(p).convert("RGB").resize((w, h), Image.LANCZOS)
        sheet.paste(im, (12 + (i % cols) * (w + 12), 12 + (i // cols) * (h + 12)))
    sheet.save(out)


def cmd_finish(a):
    project = Path(a.project).resolve()
    run_dir = project.parent
    if checker(project, "final") != 0:
        sys.exit("final SVG check failed; fix the reported pages and rerun finish")
    export_args = ["--quick-generate", "--no-notes"]
    if a.native_charts:
        export_args.append("--native-charts-and-tables")
    pm("svg_to_pptx.py", project, *export_args)
    raw = max((project / "exports").glob("*.pptx"), key=os.path.getmtime)
    deck = run_dir / f"{a.name or project.name}.pptx"
    run([sys.executable, SKILL / "scripts" / "fix_cjk_fonts.py", raw, "-o", deck])
    if not a.no_render:
        render_dir = run_dir / "renders"
        if render_dir.exists():
            shutil.rmtree(render_dir)
        run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
             SKILL / "scripts" / "render.ps1", deck, render_dir])
        contact_sheet(render_dir, run_dir / "contact.png")
    print(f"\nDECK={deck}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("new")
    p.add_argument("slug", help="ASCII project slug, e.g. nev-report")
    p.add_argument("--source", nargs="*", help="outline or source files to import into sources/")
    p.set_defaults(fn=cmd_new)
    p = sub.add_parser("photos")
    p.add_argument("project")
    p.add_argument("names", nargs="+")
    p.set_defaults(fn=cmd_photos)
    p = sub.add_parser("icons")
    p.add_argument("project")
    p.add_argument("icons", nargs="+")
    p.set_defaults(fn=cmd_icons)
    p = sub.add_parser("check")
    p.add_argument("project")
    p.add_argument("--early", action="store_true")
    p.set_defaults(fn=cmd_check)
    p = sub.add_parser("finish")
    p.add_argument("project")
    p.add_argument("--name", help="deliverable file name without .pptx (default: project name)")
    p.add_argument("--native-charts", action="store_true", help="export marked charts/tables as native objects")
    p.add_argument("--no-render", action="store_true")
    p.set_defaults(fn=cmd_finish)
    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
