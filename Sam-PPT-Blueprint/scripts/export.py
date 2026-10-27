"""Export with fix A, then run fix B as a fallback.

A: run ppt-master's own svg_to_pptx exporter in this process after adding the
OPPOSans faces to its East Asian font list in memory. No ppt-master file changes.
B: fix_cjk_fonts.py on the written deck; a no-op when A worked.

Usage: python export.py <project_path> -o <deck.pptx> [other svg_to_pptx flags]
e.g.   python export.py <project> --quick-generate --no-notes --native-charts-and-tables -o deck.pptx
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from fix_cjk_fonts import fix_deck  # noqa: E402
from pm import ppt_master_dir  # noqa: E402

OPPOSANS = {"OPPOSans", "OPPOSans H", "OPPOSans B", "OPPOSans M", "OPPOSans R", "OPPOSans L"}


def output_path(argv):
    for i, a in enumerate(argv):
        if a in ("-o", "--output") and i + 1 < len(argv):
            return Path(argv[i + 1])
        if a.startswith("--output="):
            return Path(a.split("=", 1)[1])
    sys.exit("export.py needs -o <deck.pptx> so fix B knows which file to check")


def main():
    argv = sys.argv[1:]
    out = output_path(argv)
    scripts = ppt_master_dir() / "scripts"
    sys.path.insert(0, str(scripts))
    from attribution_guard import require_skill_integrity
    from console_encoding import configure_utf8_stdio
    from svg_to_pptx.drawingml import utils
    from svg_to_pptx import main as export_main

    configure_utf8_stdio()
    require_skill_integrity()
    utils.EA_FONTS.update(OPPOSANS)  # fix A, in memory only
    code = export_main(argv)
    if code:
        return code
    changed, left = fix_deck(out, out)
    print(f"[Sam-PPT-Blueprint] fix A: OPPOSans added to EA_FONTS in memory; "
          f"fix B: {changed} slot(s) changed (0 means A covered everything), {left} YaHei slot(s) left")
    return 1 if left else 0


if __name__ == "__main__":
    raise SystemExit(main())
