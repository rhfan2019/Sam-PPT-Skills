"""Prepare a reference deck once, so runs start from it directly (step 1).

  python prepare_reference.py <reference.pptx> <library_dir>

Writes into <library_dir>:
  import/       ppt-master import workspace (--inheritance-mode both); pages to start from are
                import/authoring-svg-flat/slide_NN.svg
  renders/      PowerPoint renders slide-NN.png at 1600 px
  contact/      numbered contact sheets, 12 pages each, for choosing blueprints
  grid.txt      the content box between the header and footer rules and its 12-column grid (zones)
  start-check.txt  every page started with start_page.py and run through ppt-master's final
                checker: which pages pass as-is and what the others still need
  started-renders/ the passing started pages exported and rendered, slide-NN.png: what a page or module
                really looks like once imported (judge modules by these, not by renders/)
The module catalog (modules.json) is written next to these by reading both render sets, and approved
by the user.
"""
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from pm import ppt_master_dir  # noqa: E402
from start_page import strip  # noqa: E402


def run(args, **kw):
    print("$", " ".join(str(a) for a in args), flush=True)
    return subprocess.run([str(a) for a in args], **kw)


def contact_sheets(renders: Path, out: Path):
    from PIL import Image, ImageDraw, ImageFont
    out.mkdir(parents=True, exist_ok=True)
    pngs = sorted(renders.glob("slide-*.png"))
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/msyhbd.ttc", 28)
    except OSError:
        font = ImageFont.load_default()
    w, h = 533, 300
    for s in range(0, len(pngs), 12):
        sheet = Image.new("RGB", (w * 3, h * 4), "white")
        d = ImageDraw.Draw(sheet)
        for k, p in enumerate(pngs[s:s + 12]):
            x, y = (k % 3) * w, (k // 3) * h
            sheet.paste(Image.open(p).resize((w - 6, h - 6)), (x + 3, y + 3))
            num = re.findall(r"\d+", p.stem)[0]
            d.rectangle([x + 3, y + 3, x + 70, y + 40], fill="#FFD400")
            d.text((x + 8, y + 5), num, fill="black", font=font)
        sheet.save(out / f"sheet{s // 12 + 1}.png")


def start_check(pages: Path, out: Path, pm: Path):
    with tempfile.TemporaryDirectory(dir=out.parent) as tmp:
        run([sys.executable, pm / "scripts/project_manager.py", "init", "chk", "--format", "ppt169",
             "--dir", tmp, "--quick-generate"], capture_output=True)
        project = next(Path(tmp).glob("chk_*"))
        for svg in sorted(pages.glob("slide_*.svg")):
            text, _ = strip(svg.read_text(encoding="utf-8"), pages.parent / "images")
            (project / "svg_output" / svg.name).write_text(text, encoding="utf-8")
        res = run([sys.executable, pm / "scripts/svg_quality_checker.py", project, "--quick-generate",
                   "--canonical-authoring", "--stage", "final"], capture_output=True, text=True, encoding="utf-8")
        errors = write_start_check(res.stdout, pages, out)
        started_renders(project, errors, out.parent / "started-renders", pm)


def started_renders(project: Path, errors: dict, dst: Path, pm: Path):
    """Export the pages that pass as started and render them: what each page really looks like after
    import and start_page (some effects, such as 3D rotation, do not survive). Choose modules from these."""
    for p in errors:
        (project / "svg_output" / f"{p}.svg").unlink()
    run([sys.executable, pm / "scripts/stamp_native_fallbacks.py", project / "svg_output", "--write"], capture_output=True)
    run([sys.executable, pm / "scripts/svg_quality_checker.py", project, "--quick-generate", "--canonical-authoring",
         "--stage", "final", "--json"], capture_output=True)
    deck = project / "started.pptx"
    run([sys.executable, HERE / "export.py", project, "--quick-generate", "--no-notes", "--native-charts-and-tables",
         "-o", deck], check=True, capture_output=True)
    tmp = project / "renders"
    run(["powershell", "-ExecutionPolicy", "Bypass", "-File", HERE / "render.ps1", deck, tmp], check=True)
    if dst.exists():
        shutil.rmtree(dst)
    dst.mkdir(parents=True)
    for i, svg in enumerate(sorted((project / "svg_output").glob("slide_*.svg")), 1):
        num = re.findall(r"\d+", svg.stem)[0]
        shutil.copy(tmp / f"slide-{i:02d}.png", dst / f"slide-{num}.png")


def write_start_check(report: str, pages: Path, out: Path) -> dict:
    page, errors = None, {}
    for line in report.splitlines():
        m = re.search(r"(slide_\d+)\.svg - ", line)
        if m:
            page = m.group(1)
            continue
        if "[ERROR]" in line and page and "With errors" not in line:
            kind = "参考稿原文超出页面（换成大纲文字后消失）" if "exceeds the root viewBox" in line else line.strip()[8:90]
            errors.setdefault(page, set()).add(kind)
    total = len(list(pages.glob("slide_*.svg")))
    lines = [f"{total} 页起页后跑 ppt-master 最终检查：{total - len(errors)} 页直接通过。", ""]
    for p in sorted(errors):
        lines.append(f"{p}: " + "；".join(sorted(errors[p])))
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[:1]))
    return errors


def measure_grid(pages: Path, out: Path):
    """Content box between the reference's header rule and footer rule, split into 12 columns."""
    import collections
    top, bottom, left, right = collections.Counter(), collections.Counter(), collections.Counter(), collections.Counter()
    for svg in pages.glob("slide_*.svg"):
        for m in re.finditer(r'data-pptx-frame="([^"]+)"[^>]*data-pptx-prst="line"', svg.read_text(encoding="utf-8")):
            x, y, w, h = (float(v) for v in m.group(1).split())
            if w > 1000 and h < 2:
                (top if y < 130 else bottom if y > 600 else collections.Counter())[round(y)] += 1
                if y < 130:
                    left[round(x)] += 1
                    right[round(x + w)] += 1
    if not top or not bottom:
        out.write_text("no header/footer rule found: use 40,100,1240,670 as the content box\n", encoding="utf-8")
        return
    x0, x1 = left.most_common(1)[0][0], right.most_common(1)[0][0]
    y0, y1 = top.most_common(1)[0][0] + 18, bottom.most_common(1)[0][0] - 15
    gutter = 16
    col = (x1 - x0 - 11 * gutter) / 12
    lines = [f"content box: x {x0}-{x1}, y {y0}-{y1} (w {x1 - x0}, h {y1 - y0})",
             f"12 columns: width {col:.0f}, gutter {gutter}; column i starts at x = {x0} + {col + gutter:.0f}*i;"
             f" n columns span {col + gutter:.0f}*n - {gutter}",
             "starts: " + " ".join(f"{x0 + (col + gutter) * i:.0f}" for i in range(12))]
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(lines[0])


def main():
    ref, lib = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    pm = ppt_master_dir()
    lib.mkdir(parents=True, exist_ok=True)
    imp = lib / "import"
    if imp.exists():
        shutil.rmtree(imp)
    run([sys.executable, pm / "scripts/pptx_template_import.py", ref, "-o", imp, "--inheritance-mode", "both"],
        check=True, capture_output=True)
    run(["powershell", "-ExecutionPolicy", "Bypass", "-File", HERE / "render.ps1", ref, lib / "renders"], check=True)
    contact_sheets(lib / "renders", lib / "contact")
    measure_grid(imp / "authoring-svg-flat", lib / "grid.txt")
    start_check(imp / "authoring-svg-flat", lib / "start-check.txt", pm)
    print(f"reference library ready: {lib}")


if __name__ == "__main__":
    main()
