"""Round-trip regression ladder: how much of a reference page each pipeline step keeps.

  python ladder.py <参考稿库> <work-dir> [--pages 33,34,35,37] [--levels L0,L1,L2,L3,L4]

Every level adds one step to the one before, passes ppt-master's final check, exports with
export.py and renders with PowerPoint; the render is compared with the reference page's own render
(<lib>/renders/slide-NN.png) by SSIM (1 = identical) and mean absolute grey difference.

  L0  the imported page as it is (after patch_import.py)       ppt-master conversion
  L1  start_page.py + sweep, icon slots deleted                what starting a page strips
  L2  L1 + every text rewritten with the SAME words            edit_page.py text (textmodel.py)
  L3  L1 + every body text 1.8x longer                         wrapping and overflow reporting
  L4  page rebuilt from two modules (top / bottom of the body)  compose_page.py cutting at the
      put back where they were                                 module edge

Acceptance (printed as PASS / FAIL; exit code 1 on any FAIL):
  L2  |SSIM(L2) - SSIM(L1)| <= 0.005 on every page      rewriting the same words changes nothing
  L4  SSIM(L4 vs L1) >= 0.99 on every page              cutting into modules loses nothing
  L3  passes the final check; the overflow reports are printed, not judged
L0 and L1 are reported only (L0 measures ppt-master itself, L1 removes pictures by design).
Output: <work>/ladder.md (the table), <work>/ladder.png (reference | levels), per level a project
directory, its .pptx and its renders. Re-run it after any change to the page scripts.
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from lxml import etree
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import edit_page  # noqa: E402
import textmodel  # noqa: E402
from pm import ppt_master_dir  # noqa: E402

SVG = "http://www.w3.org/2000/svg"
PY = sys.executable


def sh(*args, check=True):
    r = subprocess.run([str(a) for a in args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and r.returncode:
        raise RuntimeError(f"{' '.join(map(str, args))}\n{r.stdout[-3000:]}\n{r.stderr[-3000:]}")
    return r.stdout


# ---------- image comparison ----------

def _box(x, k=7):
    c = np.cumsum(np.cumsum(np.pad(x, ((1, 0), (1, 0))), 0), 1)
    return (c[k:, k:] - c[:-k, k:] - c[k:, :-k] + c[:-k, :-k]) / (k * k)


def ssim(a, b):
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    ma, mb = _box(a), _box(b)
    va, vb, cov = _box(a * a) - ma * ma, _box(b * b) - mb * mb, _box(a * b) - ma * mb
    return float((((2 * ma * mb + c1) * (2 * cov + c2)) / ((ma * ma + mb * mb + c1) * (va + vb + c2))).mean())


def grey(p):
    return np.asarray(Image.open(p).convert("L").resize((1280, 720)), float)


# ---------- building one level ----------

def project(work, name, lib):
    d = work / name
    shutil.rmtree(d, ignore_errors=True)
    (d / "svg_output").mkdir(parents=True)
    (d / "icons").mkdir()
    shutil.copytree(lib / "import" / "images", d / "images")
    return d


def finish(d, lib):
    pm = ppt_master_dir()
    pages = sorted((d / "svg_output").glob("*.svg"))
    sh(PY, HERE / "group_page.py", lib / "grid.txt", *pages)
    sh(PY, pm / "scripts" / "stamp_native_fallbacks.py", d / "svg_output", "--write")
    r = subprocess.run([PY, pm / "scripts" / "svg_quality_checker.py", d, "--quick-generate", "--canonical-authoring",
                        "--stage", "final"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        errs = [ln.strip() for ln in r.stdout.splitlines() if "[ERROR]" in ln and "Failed" not in ln][:12]
        return "final check failed: " + " | ".join(errs)
    sh(PY, pm / "scripts" / "svg_quality_checker.py", d, "--quick-generate", "--canonical-authoring", "--stage", "final",
       "--json", check=False)
    out = sh(PY, HERE / "export.py", d, "--quick-generate", "--no-notes", "--native-charts-and-tables",
             "-o", d.with_suffix(".pptx"))
    if "0 YaHei slot(s) left" not in out:
        return "export: " + out[-300:]
    sh("powershell", "-ExecutionPolicy", "Bypass", "-File", HERE / "render.ps1", d.with_suffix(".pptx"),
       d.parent / ("r" + d.name))
    return ""


def drop_icon_slots(page):
    t = etree.parse(str(page))
    for u in list(t.getroot().iter(f"{{{SVG}}}use")):
        if u.get("data-icon") == "sam/icon-slot":
            u.getparent().remove(u)
    t.write(str(page), encoding="utf-8")


def in_chrome(t):
    """Header or footer text (above y=95 or below y=675, as compose_page.py's chrome bands)."""
    y = textmodel.nums(t.get("y"))
    return bool(y) and (y[0] < 95 or y[0] > 675)


def rewrite(page, factor, log):
    """Every body <text> through textmodel.replace: same words (factor 1) or lengthened."""
    tree = etree.parse(str(page))
    root = tree.getroot()
    n = over = 0
    for t in list(root.iter(f"{{{SVG}}}text")):
        if any(etree.QName(a).localname == "metadata" for a in t.iterancestors()):
            continue
        paras = textmodel.parse(t)
        words = [p.text for p in paras]
        if not "".join(words).strip():
            continue
        if factor != 1:
            if in_chrome(t):
                continue
            words = [(w * 3)[:max(len(w), round(len(w) * factor))] for w in words]
        rep = textmodel.replace(t, "\n".join(words))
        n += 1
        if textmodel.describe(rep):
            over += 1
    tree.write(str(page), encoding="utf-8")
    log.append(f"{page.name}: {n} texts rewritten, {over} reported as not fitting")


def build(level, work, lib, pages, log):
    flat = lib / "import" / "authoring-svg-flat"
    d = project(work, level, lib)
    out = d / "svg_output"
    for i, n in enumerate(pages, 1):
        dst = out / f"{i:02d}_p{n}.svg"
        if level == "L0":
            shutil.copy(flat / f"slide_{n:02d}.svg", dst)
            continue
        if level == "L4":
            sh(PY, HERE / "compose_page.py", dst, flat, f"shell={n}",
               f"{n}:0,95,1280,290@0,95", f"{n}:0,385,1280,290@0,385")
        else:
            sh(PY, HERE / "start_page.py", flat / f"slide_{n:02d}.svg", dst)
        sh(PY, HERE / "edit_page.py", "sweep", dst)
        drop_icon_slots(dst)
        if level == "L2":
            rewrite(dst, 1, log)
        elif level == "L3":
            rewrite(dst, 1.8, log)
    return finish(d, lib)


# ---------- main ----------

def main():
    sys.stdout.reconfigure(encoding="utf-8")
    args = sys.argv[1:]
    opt = lambda k, dflt: args[args.index(k) + 1] if k in args else dflt  # noqa: E731
    pos = [a for i, a in enumerate(args) if not a.startswith("--") and (i == 0 or not args[i - 1].startswith("--"))]
    if len(pos) < 2:
        sys.exit(__doc__)
    lib, work = Path(pos[0]), Path(pos[1])
    pages = [int(p) for p in opt("--pages", "33,34,35,37").split(",")]
    levels = opt("--levels", "L0,L1,L2,L3,L4").split(",")
    work.mkdir(parents=True, exist_ok=True)
    log, status = [], {}
    for lv in levels:
        status[lv] = build(lv, work, lib, pages, log)
        print(f"{lv}: {'built' if not status[lv] else status[lv]}", flush=True)
    score = {}
    for lv in levels:
        if status[lv]:
            continue
        for i, n in enumerate(pages, 1):
            img = work / f"r{lv}" / f"slide-{i:02d}.png"
            ref = grey(lib / "renders" / f"slide-{n:02d}.png")
            score[(lv, n)] = (ssim(ref, grey(img)), float(np.abs(ref - grey(img)).mean()))
    fails = []
    lines = ["| 页 | " + " | ".join(levels) + " |", "|---|" + "---|" * len(levels)]
    for n in pages:
        cells = [f"{score[(lv, n)][0]:.3f}" if (lv, n) in score else "失败" for lv in levels]
        lines.append(f"| {n} | " + " | ".join(cells) + " |")
    lines.append("")
    for n in pages:
        i = pages.index(n) + 1
        if ("L2", n) in score and ("L1", n) in score:
            d = score[("L2", n)][0] - score[("L1", n)][0]
            ok = abs(d) <= 0.005
            fails += [] if ok else [f"L2 p{n}"]
            lines.append(f"- L2 p{n}: SSIM 与 L1 相差 {d:+.4f} → {'PASS' if ok else 'FAIL'}（标准 ≤ 0.005）")
        if not status.get("L4") and not status.get("L1") and "L4" in levels and "L1" in levels:
            v = ssim(grey(work / "rL1" / f"slide-{i:02d}.png"), grey(work / "rL4" / f"slide-{i:02d}.png"))
            ok = v >= 0.99
            fails += [] if ok else [f"L4 p{n}"]
            lines.append(f"- L4 p{n}: 与 L1 的 SSIM {v:.4f} → {'PASS' if ok else 'FAIL'}（标准 ≥ 0.99）")
    for lv in levels:
        if status[lv]:
            fails.append(lv)
            lines.append(f"- {lv}: FAIL {status[lv]}")
    lines += ["", "改字记录：", *[f"- {x}" for x in log]]
    (work / "ladder.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    # sheet: reference | each level
    w, h = 480, 270
    sheet = Image.new("RGB", (w * (len(levels) + 1), (h + 20) * len(pages)), "white")
    dr = ImageDraw.Draw(sheet)
    for r, n in enumerate(pages):
        sheet.paste(Image.open(lib / "renders" / f"slide-{n:02d}.png").convert("RGB").resize((w, h)), (0, r * (h + 20) + 20))
        dr.text((4, r * (h + 20) + 4), f"rnb {n}", fill="black")
        for c, lv in enumerate(levels, 1):
            img = work / f"r{lv}" / f"slide-{r + 1:02d}.png"
            if (lv, n) in score and img.exists():
                sheet.paste(Image.open(img).convert("RGB").resize((w, h)), (c * w, r * (h + 20) + 20))
                dr.text((c * w + 4, r * (h + 20) + 4), f"{lv} SSIM {score[(lv, n)][0]:.3f}", fill="black")
    sheet.save(work / "ladder.png")
    (work / "ladder.json").write_text(json.dumps({f"{k[0]}-{k[1]}": v for k, v in score.items()}, indent=1), encoding="utf-8")
    print("\n".join(lines))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
