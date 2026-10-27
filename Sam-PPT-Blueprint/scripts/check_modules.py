"""Check a module catalog against the reference pages: what compose_page.py would really take.

  python check_modules.py <modules.json> <import_workspace>/authoring-svg-flat

For every module: how many top-level elements compose_page takes (centred in the bbox or bbox_extra
with at least 60% of their area inside), and which are centred inside but left behind because most
of them lies outside (a backplate shared with neighbours, or a box drawn too tight). Lists empty
modules, left-behind elements and logic values that are not relation codes of logic-diagrams.md;
a shared backplate is fine once the module's "dependency" says so.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compose_page import is_background, inside, local, nums, parse  # noqa: E402

CODES = {f"{f}{i}" for f, n in (("A", 4), ("B", 8), ("C", 4), ("D", 7), ("E", 6), ("F", 5)) for i in range(1, n + 1)} | {"K", "S"}


def frame(e):
    f = nums(e.get("data-pptx-frame"))
    return f if len(f) == 4 else None


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    cat, lib = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")), Path(sys.argv[2])
    pages, bad = {}, 0
    for m in cat:
        n = int(m["page"])
        if n not in pages:
            pages[n] = parse(lib / f"slide_{n:02d}.svg")
        boxes = [m["bbox"]] + ([m["bbox_extra"]] if m.get("bbox_extra") else [])
        took, left = 0, []
        for e in pages[n]:
            if not isinstance(e.tag, str) or local(e) in ("defs", "metadata", "title", "desc") or is_background(e):
                continue
            if any(inside(e, *b) for b in boxes):
                took += 1
            elif any(inside(e, *b, share=0) for b in boxes):
                f = frame(e)
                left.append(f"{e.get('id')}[{' '.join(str(round(v)) for v in f)}]")
        codes = [c for c in m.get("logic", []) if c not in CODES]
        flag = took == 0 or left or codes
        bad += bool(flag)
        line = f"{m['module']:7} took {took:3}"
        if left:
            line += f"; left behind {len(left)}: " + " ".join(left[:6]) + (" ..." if len(left) > 6 else "")
        if codes:
            line += f"; logic not a code: {codes}"
        if flag:
            print(line)
    print(f"{len(cat)} module(s), {bad} to look at")


if __name__ == "__main__":
    main()
