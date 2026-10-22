"""Thin wrapper that runs ppt-master's Quick Generate route with the Sam Bain template.

ppt-master does the work (project layout, template install, typography calibration,
SVG checks, native PPTX export); this script only fixes the Sam-PPT-Bain choices:
the run folder convention (outside the Skill folder, under the system temp dir
or $SAM_PPT_RUNS), the installed template, the recurring type roles, the
OPPOSans CJK repair after export, and the PowerPoint render check.

  python sam_bain.py new <slug> [--source outline.md ...]   create <runs>/run-*/<slug>_<date>/
  python sam_bain.py photos <project> city_tech.png ...     copy stock photos into images/
  python sam_bain.py icons <project> chunk-filled/bolt ...  sync library icons into icons/
  python sam_bain.py scaffold <project> 03_name --title ... [--thesis ...]  page frame only, body left empty
  python sam_bain.py preview <project> [03_name ...]        quick browser screenshots into preview/
  python sam_bain.py check <project> [--early]              ppt-master SVG quality gate
  python sam_bain.py finish <project> [--name 文件名]        check, export, fix fonts, render
"""
import argparse
import datetime as dt
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from xml.sax.saxutils import escape

SKILL = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL / "template"
PHOTOS = SKILL / "assets" / "photos"
# Run folders live outside the Skill folder so a run never sits next to the rules
# (and blind runs cannot browse each other through the Skill tree).
RUNS = Path(os.environ.get("SAM_PPT_RUNS")
            or Path(tempfile.gettempdir()) / "claude" / "Sam-PPT-Runs" / "Sam-PPT-Bain")

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


# ppt-master version that references/ppt-master-digest.md was distilled from.
DIGEST_VERSION = "6.7.2"

# Shared paint every content page may reference: same-hue gradients, line-end markers
# (one per stroke colour, the marker fill must equal the line stroke) and the soft shadow.
PAGE_DEFS = """  <defs>
    <linearGradient id="gNavyV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2E5A94"/><stop offset="1" stop-color="#16365F"/></linearGradient>
    <linearGradient id="gNavyH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#16365F"/><stop offset="1" stop-color="#2E5A94"/></linearGradient>
    <linearGradient id="gRedV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C0503E"/><stop offset="1" stop-color="#8E2B1D"/></linearGradient>
    <linearGradient id="gRedH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8E2B1D"/><stop offset="1" stop-color="#C0503E"/></linearGradient>
    <linearGradient id="gBlueRed" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#1C4274"/><stop offset="1" stop-color="#A23424"/></linearGradient>
    <marker id="arrNavy" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><polygon points="0,0 10,5 0,10" fill="#1C4274"/></marker>
    <marker id="arrRed" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><polygon points="0,0 10,5 0,10" fill="#A23424"/></marker>
    <marker id="arrGray" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><polygon points="0,0 10,5 0,10" fill="#8EA9CF"/></marker>
    <marker id="arrPink" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><polygon points="0,0 10,5 0,10" fill="#E3A79C"/></marker>
    <marker id="arrWhite" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><polygon points="0,0 10,5 0,10" fill="#FFFFFF"/></marker>
    <filter id="softShadow" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="4" stdDeviation="6" flood-color="#000000" flood-opacity="0.14"/></filter>
  </defs>
"""

SAMPLE_DATA_FOOTER = "示例数据，不作为真实统计引用"


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


def ppt_master_version():
    m = re.search(r'^\s*version:\s*"?([\w.]+)', (PM / "SKILL.md").read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else "unknown"


def cmd_new(a):
    pm("attribution_guard.py")
    version = ppt_master_version()
    if version != DIGEST_VERSION:
        print(f"[WARN] ppt-master is {version}, references/ppt-master-digest.md was written for "
              f"{DIGEST_VERSION}: read the original execution docs this run and refresh the digest",
              flush=True)
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
    a.run_dir = run_dir
    print(f"\nRUN_DIR={run_dir}\nPROJECT={project}")


# Every command appends one tab-separated line to <run_dir>/timing.log:
# start, end (ISO seconds), seconds, command, status, detail (slug / page stems / file name).
TIMING = "timing.log"


def log_timing(run_dir, a, start, end, status):
    detail = {"new": lambda: a.slug, "scaffold": lambda: a.page, "finish": lambda: a.name or "",
              "preview": lambda: " ".join(n.removesuffix(".svg") for n in a.pages) or "all",
              "icons": lambda: f"{len(a.icons)} icons", "photos": lambda: " ".join(a.names),
              "check": lambda: "early" if a.early else "final"}[a.cmd]()
    with open(Path(run_dir) / TIMING, "a", encoding="utf-8") as f:
        f.write(f"{start.isoformat(timespec='seconds')}\t{end.isoformat(timespec='seconds')}\t"
                f"{(end - start).total_seconds():.0f}\t{a.cmd}\t{status}\t{detail}\n")


def timing_summary(run_dir):
    """Phase breakdown of one run, read back from timing.log (reading the docs before `new` is not logged)."""
    rows = []
    for line in (Path(run_dir) / TIMING).read_text(encoding="utf-8").splitlines():
        s, e, sec, cmd, status, detail = (line.split("\t") + [""] * 6)[:6]
        rows.append((dt.datetime.fromisoformat(s), dt.datetime.fromisoformat(e), int(sec), cmd, status, detail))
    mins = lambda td: f"{int(td.total_seconds()) // 60} 分 {int(td.total_seconds()) % 60} 秒"
    new = next((r for r in rows if r[3] == "new"), None)
    finishes = [r for r in rows if r[3] == "finish" and r[4] == "ok"]
    if not new or not finishes:
        return ""
    out = ["", "=" * 72, f"耗时（timing.log；不含 new 之前读文档的时间）",
           f"总计（new 开始 → 本次 finish 结束）：{mins(finishes[-1][1] - new[0])}",
           f"  建项目 new：{new[2]} 秒",
           f"  逐页编写（new 结束 → 第一次 finish 开始）：{mins(finishes[0][0] - new[1])}"]
    # A page's authoring time = its first preview minus the previous page's first preview (or the end of new).
    first_seen, last = {}, new[1]
    for r in rows:
        if r[3] == "preview" and r[1] <= finishes[0][0]:
            for stem in r[5].split():
                first_seen.setdefault(stem, r[1])
    for stem, t in sorted(first_seen.items(), key=lambda kv: kv[1]):
        out.append(f"    {stem}：{mins(t - last)}")
        last = t
    checks = [r for r in rows if r[3] == "check"]
    previews = [r for r in rows if r[3] == "preview"]
    out.append(f"  其中 preview {len(previews)} 次共 {sum(r[2] for r in previews)} 秒，"
               f"check {len(checks)} 次共 {sum(r[2] for r in checks)} 秒")
    out.append(f"  finish {len(finishes)} 次：" + "、".join(f"{r[2]} 秒" for r in finishes))
    if len(finishes) > 1:
        out.append(f"  看渲染图 + 返修（第一次 finish 结束 → 最后一次结束）：{mins(finishes[-1][1] - finishes[0][1])}")
    out.append("=" * 72)
    return "\n".join(out)


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


def outline_header(project):
    """`- 键：值` lines above the first `---` of the imported outline (机构 / 页眉标签 / 说明 / 日期 ...)."""
    header = {}
    for md in sorted((project / "sources").glob("*.md")):
        for line in md.read_text(encoding="utf-8").splitlines():
            if line.strip() == "---":
                break
            m = re.match(r"^\s*-\s*([^：:]+)[：:]\s*(.+?)\s*$", line)
            if m:
                header.setdefault(m.group(1).strip(), m.group(2))
        if header:
            break
    return header


def cmd_scaffold(a):
    """Write the fixed page frame of one content page; the body stays for hand authoring."""
    project = Path(a.project).resolve()
    out = project / "svg_output" / f"{a.page}.svg"
    if out.exists() and not a.force:
        sys.exit(f"{out.name} already exists; pass --force to overwrite it")
    header = outline_header(project)
    layout = "04b_content_thesis" if a.thesis else "04a_content_frame"
    footer = SAMPLE_DATA_FOOTER if a.sample_data else (a.footer if a.footer is not None else header.get("说明", ""))
    if a.source_note:
        footer += a.source_note
    values = {
        "{{PAGE_TITLE}}": a.title,
        "{{SECTION_NAME}}": a.section if a.section is not None else header.get("页眉标签", ""),
        "{{KEY_MESSAGE}}": a.thesis or "",
        "{{SOURCE}}": footer,
        "{{AUTHOR}}": a.author if a.author is not None else header.get("机构", ""),
    }
    svg = (project / "templates" / f"{layout}.svg").read_text(encoding="utf-8")
    for key, value in values.items():
        svg = svg.replace(key, escape(value))
    svg = svg.replace('viewBox="0 0 1280 720"', 'viewBox="0 0 1280 720" lang="zh-CN"', 1)
    svg = svg.replace('  <rect id="master-background"', PAGE_DEFS + '  <rect id="master-background"', 1)
    svg = svg.replace("</svg>", "\n  <!-- body: Slide-local groups from here (y 166–672 with thesis, 96–672 without) -->\n</svg>")
    out.write_text(svg, encoding="utf-8")
    cjk = len(re.findall(r"[\u3000-\u9fff\uff00-\uffef]", a.title))
    if cjk > 20:
        print(f"[WARN] title has {cjk} CJK characters (> 20): follow page-patterns 四 for long titles")
    print(f"PAGE={out}  (layout {layout}; section={values['{{SECTION_NAME}}']!r}, footer={footer!r})")


def find_browser():
    for p in (os.environ.get("SAM_PPT_BROWSER"),
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe"):
        if p and Path(p).exists():
            return p
    sys.exit("no Edge/Chrome found for preview; set SAM_PPT_BROWSER to a Chromium browser executable")


def cmd_preview(a):
    """Browser screenshots of draft pages, icons expanded; PowerPoint rendering stays in finish."""
    project = Path(a.project).resolve()
    pages = [project / "svg_output" / f"{n.removesuffix('.svg')}.svg" for n in a.pages] \
        or sorted((project / "svg_output").glob("*.svg"))
    missing = [p.name for p in pages if not p.exists()]
    if missing:
        sys.exit(f"not found in svg_output/: {', '.join(missing)}")
    # The working copy sits beside svg_output/ under a folder name ppt-master maps back to the
    # project root, so ../images and the project icon pool resolve exactly as they do for export.
    work = project / ".svg_final.candidate-preview"
    out = project / "preview"
    shutil.rmtree(work, ignore_errors=True)
    work.mkdir()
    out.mkdir(exist_ok=True)
    copies = [work / p.name for p in pages]
    for src, dst in zip(pages, copies):
        shutil.copy2(src, dst)
    pm("svg_finalize/embed_icons.py", *copies, check=False)
    browser = find_browser()
    for svg in copies:
        png = out / f"{svg.stem}.png"
        png.unlink(missing_ok=True)
        subprocess.run([browser, "--headless=new", "--disable-gpu", "--hide-scrollbars",
                        "--window-size=1280,720", f"--screenshot={png}", svg.as_uri()],
                       capture_output=True)
        # Edge may hand the screenshot off to a background process and return before it is written.
        for _ in range(60):
            if png.exists() and png.stat().st_size > 0:
                break
            time.sleep(0.25)
        print(f"PREVIEW={png}" if png.exists() else f"[WARN] no screenshot for {svg.name}")
    shutil.rmtree(work, ignore_errors=True)


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


def free_deck_path(run_dir, stem):
    """The deck path, or <stem>-v2/-v3... when an earlier copy is held open by PowerPoint."""
    deck, n = run_dir / f"{stem}.pptx", 1
    while deck.exists():
        try:
            with open(deck, "r+b"):
                break
        except PermissionError:
            n += 1
            deck = run_dir / f"{stem}-v{n}.pptx"
    if n > 1:
        print(f"[NOTE] {stem}.pptx is open in another program; writing {deck.name} instead", flush=True)
    return deck


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
    deck = free_deck_path(run_dir, a.name or project.name)
    run([sys.executable, SKILL / "scripts" / "fix_cjk_fonts.py", raw, "-o", deck])
    if not a.no_render:
        render_dir = run_dir / "renders"
        if render_dir.exists():
            shutil.rmtree(render_dir)
        run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
             SKILL / "scripts" / "render.ps1", deck, render_dir])
        contact_sheet(render_dir, run_dir / "contact.png")
    bar = "=" * 72
    print(f"\n{bar}\n成品 PPTX：{deck}")
    if not a.no_render:
        print(f"渲染图目录：{render_dir}\n总览图：{run_dir / 'contact.png'}")
    print("提示：成品位于系统临时目录，可能被系统清理；需要保留请另存到其他位置。")
    print(f"{bar}\nDECK={deck}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("new")
    p.add_argument("slug", help="ASCII project slug, e.g. demo-report")
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
    p = sub.add_parser("scaffold")
    p.add_argument("project")
    p.add_argument("page", help="file stem in svg_output/, e.g. 03_three_stage_plan")
    p.add_argument("--title", required=True)
    p.add_argument("--thesis", help="结论/发现原句; selects 04b_content_thesis")
    p.add_argument("--section", help="右上章节标签 (default: outline 页眉标签)")
    p.add_argument("--footer", help="左下页脚 (default: outline 说明)")
    p.add_argument("--sample-data", action="store_true", help="page marked 示例数据")
    p.add_argument("--source-note", help="text appended to the footer, e.g. 数据来源：...")
    p.add_argument("--author", help="右下署名 (default: outline 机构)")
    p.add_argument("--force", action="store_true")
    p.set_defaults(fn=cmd_scaffold)
    p = sub.add_parser("preview")
    p.add_argument("project")
    p.add_argument("pages", nargs="*", help="page stems; default: every page in svg_output/")
    p.set_defaults(fn=cmd_preview)
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
    start, status = dt.datetime.now(), "ok"
    try:
        a.fn(a)
    except BaseException as e:
        if not (isinstance(e, SystemExit) and e.code in (0, None)):
            status = "fail"
        raise
    finally:
        run_dir = getattr(a, "run_dir", None) or (Path(a.project).resolve().parent if getattr(a, "project", None) else None)
        if run_dir and run_dir.exists():
            log_timing(run_dir, a, start, dt.datetime.now(), status)
            if a.cmd == "finish" and status == "ok":
                print(timing_summary(run_dir))


if __name__ == "__main__":
    main()
