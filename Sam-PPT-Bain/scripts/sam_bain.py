"""Thin wrapper that runs ppt-master's Quick Generate route with the Sam Bain template.

ppt-master does the work (project layout, template install, typography calibration,
SVG checks, native PPTX export); this script only fixes the Sam-PPT-Bain choices:
the run folder convention (outside the repo, under the test workspace's runs
folder, the system temp dir or $SAM_PPT_RUNS), the installed template, the recurring type roles, the
OPPOSans CJK repair after export, and the PowerPoint render check.

  python sam_bain.py start                                 mark the start of a run (reading the docs is timed too)
  python sam_bain.py new <slug> [--source outline.md ...]   create <runs>/run-*/<slug>_<date>/
  python sam_bain.py photos <project> city_tech.png ...     copy stock photos into images/
  python sam_bain.py icons <project> chunk-filled/bolt ...  sync library icons into icons/
  python sam_bain.py scaffold <project> 03_name --title ... [--thesis ...]  page frame only, body left empty
  python sam_bain.py put <project> 03_name [body.svg]      paste the hand-written body (<!--C/T/P ...--> markers expanded,
                                                            bounds="auto" measured, body lint), then preview
  python sam_bain.py preview <project> [03_name ...]        quick browser screenshots into preview/ + single-page check
  python sam_bain.py measure "文字" ... --role body [--max-width 300]  rendered width / wrapped lines
  python sam_bain.py check <project> [--early]              ppt-master SVG quality gate
  python sam_bain.py finish <project> [--name 文件名]        check, export, fix fonts, render
"""
import argparse
import datetime as dt
import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from xml.sax.saxutils import escape

import components

SKILL = Path(__file__).resolve().parent.parent
TEMPLATE = SKILL / "template"
PHOTOS = SKILL / "assets" / "photos"
# Run folders live outside the repo so a run never sits next to the rules
# (and blind runs cannot browse each other through the Skill tree). The test
# workspace's runs folder is the default; the system temp dir is the fallback
# on machines without it.
TEST_RUNS = Path(r"D:\Workspace\Sam-PPT-Skills-Test\runs")
RUNS = Path(os.environ.get("SAM_PPT_RUNS")
            or (TEST_RUNS if TEST_RUNS.is_dir()
                else Path(tempfile.gettempdir()) / "claude" / "Sam-PPT-Runs") / "Sam-PPT-Bain")

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
    <filter id="tileShadow" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="2" dy="3" stdDeviation="5" flood-color="#000000" flood-opacity="0.08"/></filter>
    <linearGradient id="gFadeRedUp" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#F4D1CC"/><stop offset="1" stop-color="#F4D1CC" stop-opacity="0"/></linearGradient>
    <linearGradient id="gFadeNavyUp" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#C4D7F1"/><stop offset="1" stop-color="#C4D7F1" stop-opacity="0"/></linearGradient>
    <linearGradient id="gBoardRed" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#FBEFED"/></linearGradient>
    <linearGradient id="gBoardNavy" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFFFFF"/><stop offset="1" stop-color="#EEF3FA"/></linearGradient>
    <filter id="nodeShadow" x="-30%" y="-30%" width="170%" height="170%"><feDropShadow dx="2.83" dy="2.83" stdDeviation="2.67" flood-color="#000000" flood-opacity="0.40"/></filter>
    <filter id="glowRed" x="-80%" y="-80%" width="260%" height="260%"><feDropShadow dx="2.83" dy="2.83" stdDeviation="13.3" flood-color="#A23424" flood-opacity="0.29"/></filter>
    <filter id="glowNavy" x="-80%" y="-80%" width="260%" height="260%"><feDropShadow dx="2.83" dy="2.83" stdDeviation="13.3" flood-color="#1C4274" flood-opacity="0.29"/></filter>
    <linearGradient id="gColumnTop" x1="0" y1="0" x2="0" y2="1"><stop offset="0.14" stop-color="#C4D7F1" stop-opacity="0"/><stop offset="0.67" stop-color="#C4D7F1" stop-opacity="0.15"/><stop offset="1" stop-color="#C4D7F1" stop-opacity="0"/></linearGradient>
    <linearGradient id="gColumnBody" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#C4D7F1" stop-opacity="0"/><stop offset="0.85" stop-color="#C4D7F1" stop-opacity="0.30"/></linearGradient>
    <linearGradient id="gBeamUp" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#C4D7F1" stop-opacity="0.08"/><stop offset="1" stop-color="#C4D7F1"/></linearGradient>
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
components.init(PM)


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


START_MARK = RUNS / ".start"


def cmd_start(a):
    """Remember when the run began, so the doc reading before `new` lands in timing.log."""
    RUNS.mkdir(parents=True, exist_ok=True)
    START_MARK.write_text(dt.datetime.now().isoformat(timespec="seconds"), encoding="utf-8")
    print(f"START={START_MARK.read_text(encoding='utf-8')}")


def cmd_new(a):
    started = None
    if START_MARK.exists():
        started = dt.datetime.fromisoformat(START_MARK.read_text(encoding="utf-8").strip())
        START_MARK.unlink()
        if dt.datetime.now() - started > dt.timedelta(hours=6):
            started = None
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
    if started:
        with open(run_dir / TIMING, "a", encoding="utf-8") as f:
            f.write(f"{started.isoformat(timespec='seconds')}\t{a.started.isoformat(timespec='seconds')}\t"
                    f"{(a.started - started).total_seconds():.0f}\tstart\tok\tread docs + plan\n")
    print(f"\nRUN_DIR={run_dir}\nPROJECT={project}")


# Every command appends one tab-separated line to <run_dir>/timing.log:
# start, end (ISO seconds), seconds, command, status, detail (slug / page stems / file name).
TIMING = "timing.log"


def log_timing(run_dir, a, start, end, status):
    detail = {"new": lambda: a.slug, "scaffold": lambda: a.page, "finish": lambda: a.name or "",
              "preview": lambda: " ".join(n.removesuffix(".svg") for n in a.pages) or "all",
              "icons": lambda: f"{len(a.icons)} icons", "photos": lambda: " ".join(a.names),
              "check": lambda: "early" if a.early else "final",
              "put": lambda: a.page.removesuffix(".svg"), "start": lambda: ""}.get(a.cmd, lambda: "")()
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
    start = next((r for r in rows if r[3] == "start"), None)
    head = ["", "=" * 72]
    if start:
        head += ["耗时（timing.log，从 start 起）",
                 f"总计（start → 本次 finish 结束）：{mins(finishes[-1][1] - start[0])}",
                 f"  读文档 + 规划（start → new）：{mins(start[1] - start[0])}"]
    else:
        head += ["耗时（timing.log；没有跑 start，不含 new 之前读文档的时间）",
                 f"总计（new 开始 → 本次 finish 结束）：{mins(finishes[-1][1] - new[0])}"]
    out = head + [f"  建项目 new：{new[2]} 秒",
           f"  逐页编写（new 结束 → 第一次 finish 开始）：{mins(finishes[0][0] - new[1])}"]
    # A page's authoring time = its first preview minus the previous page's first preview (or the end of new).
    first_seen, last = {}, new[1]
    for r in rows:
        if r[3] in ("preview", "put") and r[1] <= finishes[0][0]:
            for stem in r[5].split():
                first_seen.setdefault(stem, r[1])
    for stem, t in sorted(first_seen.items(), key=lambda kv: kv[1]):
        out.append(f"    {stem}：{mins(t - last)}")
        last = t
    checks = [r for r in rows if r[3] == "check"]
    previews = [r for r in rows if r[3] in ("preview", "put")]
    out.append(f"  其中 put/preview {len(previews)} 次共 {sum(r[2] for r in previews)} 秒，"
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
    """Sync the icons that exist; a misspelt name is reported with near matches instead of failing the batch."""
    lib_root = PM / "templates" / "icons"
    found, missing = [], []
    for name in a.icons:
        (found if (lib_root / f"{name}.svg").exists() else missing).append(name)
    if found:
        pm("icon_sync.py", a.project, *found)
    for name in missing:
        near = components.suggest_icons(name, lib_root / (name.split("/")[0] if "/" in name else "chunk-filled"))
        print(f"[MISSING] {name}: not in the library" + (f"; near: {', '.join(near)}" if near else ""))


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
    svg = svg.replace("</svg>", f"\n  {BODY_ANCHOR}{BODY_HINT}\n</svg>")
    out.write_text(svg, encoding="utf-8")
    cjk = len(re.findall(r"[\u3000-\u9fff\uff00-\uffef]", a.title))
    if cjk > 20:
        print(f"[WARN] title has {cjk} CJK characters (> 20): follow page-patterns 四 for long titles")
    print(f"PAGE={out}  (layout {layout}; section={values['{{SECTION_NAME}}']!r}, footer={footer!r})")


BODY_ANCHOR = "<!-- body: Slide-local groups"
BODY_HINT = " from here (y 166–672 with thesis, 96–672 without) -->"
# One preset per marker line in a hand-written body:
#   <!--P chevron st1 360 204 165.67 52 #16365F [stroke=#HEX sw=1 op=0.5 adj=val 15000 adj1=val -56000] -->
# preset, id, frame x y w h, fill; stroke / sw (stroke width) / op (fill opacity); anything else is a DrawingML adjustment.
PRESET_MARK = re.compile(r"<!--P (\S+) (\S+) ([\d.\-]+) ([\d.\-]+) ([\d.]+) ([\d.]+) (\S+)(.*?) *-->")


def expand_presets(body):
    """Replace every preset marker with the verbatim fragment printed by preset_shape_svg.py render-batch."""
    items = []
    for m in PRESET_MARK.finditer(body):
        preset, pid, x, y, w, h, fill, rest = m.groups()
        item = {"preset": preset, "id": pid, "frame": [float(v) for v in (x, y, w, h)], "fill": fill}
        adjust = {}
        for key, value in re.findall(r" ([^=\s]+)=(.+?)(?= [^=\s]+=|$)", rest):
            value = value.strip()
            if key == "stroke":
                item["stroke"] = value
            elif key == "sw":
                item["stroke_width"] = float(value)
            elif key == "op":
                item["fill_opacity"] = float(value)
            else:
                adjust[key] = value
        if adjust:
            item["adjustments"] = adjust
        items.append(item)
    if not items:
        return body, 0
    ids = [i["id"] for i in items]
    if len(set(ids)) != len(ids):
        sys.exit(f"duplicate preset ids: {sorted({i for i in ids if ids.count(i) > 1})}")
    res = subprocess.run([sys.executable, PM / "scripts" / "preset_shape_svg.py", "render-batch", "--input", "-"],
                         input=json.dumps(items), capture_output=True, text=True, encoding="utf-8")
    if res.returncode or not res.stdout.strip():
        sys.exit(f"preset render failed:\n{res.stderr}")
    frags = {re.match(r'<g id="([^"]+)"', f).group(1): f
             for f in re.findall(r'<g id="[^"]+" data-pptx-authoring="preset".*?</g>', res.stdout, re.S)}
    return PRESET_MARK.sub(lambda m: frags[m.group(2)], body), len(items)


def cmd_put(a):
    """Paste a hand-written body after the scaffolded frame (replacing any earlier body), presets expanded."""
    project = Path(a.project).resolve()
    stem = a.page.removesuffix(".svg")
    page = project / "svg_output" / f"{stem}.svg"
    src = Path(a.body) if a.body else project / "body" / f"{stem}.svg"
    if not page.exists():
        sys.exit(f"{page.name} not found; run scaffold first")
    if not src.exists():
        sys.exit(f"body file not found: {src}")
    source = src.read_text(encoding="utf-8")
    try:
        body, nc = components.expand_components(source)
        body, n = expand_presets(body)
        body, nb = components.auto_bounds(body)
    except components.BodyError as e:
        sys.exit(f"[ERROR] {e}")
    svg = page.read_text(encoding="utf-8")
    if BODY_ANCHOR not in svg:
        sys.exit(f"{page.name} has no body anchor comment; re-run scaffold --force")
    head, tail = svg.split(BODY_ANCHOR, 1)
    page.write_text(f"{head}{BODY_ANCHOR}{tail.split(chr(10), 1)[0]}\n{body.rstrip()}\n</svg>\n", encoding="utf-8")
    print(f"PUT={page}  ({n} preset(s), {nc} component marker(s), {nb} auto bound(s) from {src.name})")
    for finding in components.lint_body(source, body, 'data-pptx-layout="content_thesis"' in svg):
        print(f"LINT {stem}: {finding}")
    if not a.no_preview:
        a.pages = [stem]
        cmd_preview(a)


def page_check(project, page):
    """Single-page ppt-master gate plus a missing-icon scan; prints only what needs attention."""
    res = subprocess.run([sys.executable, PM / "scripts" / "svg_quality_checker.py", project, "--quick-generate",
                          "--canonical-authoring", "--stage", "page", "--page", page.name],
                         capture_output=True, text=True, encoding="utf-8", errors="replace",
                         env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    # Expected on every page: the OPPOSans font notice (repaired after export) and compact-style advice;
    # the summary counters are dropped too. A missing icon shows up as "Project-local icon not found" (fix: icons).
    noise = ("non-PPT-safe typeface", "Noncanonical compact authoring", "unsafe_exported_faces", "portability",
             "With warnings:", "With errors:", "Fully passed:")
    findings = [ln.strip() for ln in res.stdout.splitlines()
                if re.match(r"\s+\[(ERROR|WARN)\]", ln) and not any(n in ln for n in noise)]
    if res.returncode and not any(f.startswith("[ERROR]") for f in findings):
        findings.append(f"[ERROR] checker exit {res.returncode}; run `sam_bain.py check` for the full report")
    status = "ERROR" if any(f.startswith("[ERROR]") for f in findings) else "WARN" if findings else "OK"
    print(f"CHECK {page.stem}: {status}" + "".join(f"\n   {f}" for f in findings))


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
    if not getattr(a, "no_check", False):
        for page in pages:
            page_check(project, page)


def cmd_measure(a):
    """Rendered width of each text (checker's estimator); with --max-width, the wrapped lines of one paragraph."""
    if a.role:
        roles = {r.split(":")[0]: r.split(":")[1:] for r in ROLES}
        if a.role not in roles:
            sys.exit(f"unknown role {a.role}; choose from {', '.join(roles)}")
        family, size = roles[a.role][0], roles[a.role][1]
    else:
        family, size = a.font, a.size
    if not size:
        sys.exit("give --role or --size (with --font, default OPPOSans R)")
    style = ["--size", str(size), "--family", family]
    if family.endswith((" B", " H")):
        style += ["--weight", "bold"]
    script = PM / "scripts" / "text_measure.py"
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    if a.max_width and len(a.text) == 1:
        res = subprocess.run([sys.executable, script, "wrap", "--json", "--max-width", str(a.max_width), "--x", "0",
                              "--dy", "1", *style, a.text[0]], capture_output=True, text=True, encoding="utf-8", env=env)
        if res.returncode:
            sys.exit(res.stderr)
        data = json.loads(res.stdout)
        print(f"{family} {size}px, max {a.max_width}px → {len(data['lines'])} line(s)")
        for line, width in zip(data["lines"], data["widths"]):
            print(f"{width:8.1f}  {line}")
        return
    res = subprocess.run([sys.executable, script, "measure", "--json", *style, *a.text],
                         capture_output=True, text=True, encoding="utf-8", env=env)
    if res.returncode:
        sys.exit(res.stderr)
    print(f"{family} {size}px")
    for item in json.loads(res.stdout):
        over = f"  OVER by {item['width'] - a.max_width:.1f}" if a.max_width and item["width"] > a.max_width else ""
        print(f"{item['width']:8.1f}  {item['text']}{over}")


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
    for names in components.skeleton_report(sorted((project / "svg_output").glob("*.svg"))):
        print(f"[WARN] same root-group skeleton on {len(names)} pages ({', '.join(names)}): "
              f"the deck starts to read as a template — vary the construction (page-patterns 三B)")
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
    p = sub.add_parser("start")
    p.set_defaults(fn=cmd_start)
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
    p.add_argument("--no-check", action="store_true", help="skip the single-page quality check")
    p.set_defaults(fn=cmd_preview)
    p = sub.add_parser("put")
    p.add_argument("project")
    p.add_argument("page", help="page stem in svg_output/ (already scaffolded)")
    p.add_argument("body", nargs="?", help="hand-written body file (default: <project>/body/<page>.svg)")
    p.add_argument("--no-preview", action="store_true", help="paste only; skip preview and page check")
    p.add_argument("--no-check", action="store_true", help="preview without the page check")
    p.set_defaults(fn=cmd_put)
    p = sub.add_parser("measure")
    p.add_argument("text", nargs="+", help="one or more strings (one paragraph when --max-width wraps)")
    p.add_argument("--role", help="type role from the calibration table: " + ", ".join(r.split(":")[0] for r in ROLES))
    p.add_argument("--font", default="OPPOSans R", help="family when --role is not given, e.g. 'OPPOSans M'")
    p.add_argument("--size", type=float, help="px when --role is not given")
    p.add_argument("--max-width", type=float, help="flag strings wider than this; with one string, wrap it")
    p.set_defaults(fn=cmd_measure)
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
    a.started = start
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
