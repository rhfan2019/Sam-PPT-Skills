"""Check that the locked visual style (references/style-lock.md) is intact.

    python style_guard.py            # check; exit 1 and list what changed
    python style_guard.py --update   # re-record the locked-file hashes (ONLY after the user approved a change)

Two kinds of checks:
  * locked files (page-frame templates, approved samples, style-lock.md) must match the hashes in
    references/style-lock.sha256.json;
  * locked clauses must still be present in the rules, the style spec and the scripts.
`sam_bain.py new` runs this before every run and the repo's pre-commit hook runs it before every commit.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
MANIFEST = SKILL / "references" / "style-lock.sha256.json"
LOCKED_GLOBS = ["template/templates/*.svg", "references/approved/*.png", "references/style-lock.md"]

# (file, text that must be present, which lock item)
CLAUSES = [
    ("references/rules.md", "**分区用色块，不用细线**", "L-2"),
    ("references/rules.md", "约 60–75%", "L-2"),
    ("references/rules.md", "**版面填满**", "L-3"),
    ("references/rules.md", "不允许出现高于 40 px 的白底空带", "L-3"),
    ("references/rules.md", "（英雄数字每页 1–2 个）", "L-5"),
    ("references/rules.md", "大区一般 3–5 个", "L-5"),
    ("template/templates/design_spec.style.sam-bain-consulting.md", "深色栏头与浅底面板拼成的色块大区", "L-2"),
    ("template/templates/design_spec.style.sam-bain-consulting.md", "白底细线框的轻量线框图", "L-2"),
    ("template/templates/design_spec.deck.sam-bain.md", "| Navy (primary) | #1C4274 |", "L-1"),
    ("template/templates/design_spec.deck.sam-bain.md", "| Brick red (accent) | #A23424 |", "L-1"),
    ("template/templates/design_spec.deck.sam-bain.md", "全宽海军蓝条（#1C4274），白字", "L-4"),
    ("references/page-patterns.md", "海军蓝实底，白字 OPPOSans M 26.67", "L-4"),
    ("references/approved/samples.md", "sample-13-strategy-house-heavy.png", "L-8"),
    ("scripts/sam_bain.py", '<linearGradient id="gNavyH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#16365F"/><stop offset="1" stop-color="#2E5A94"/>', "L-1"),
    ("scripts/sam_bain.py", '<linearGradient id="gRedH" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#8E2B1D"/><stop offset="1" stop-color="#C0503E"/>', "L-1"),
]


def digest(path):
    data = path.read_bytes()
    if path.suffix != ".png":                     # git may rewrite text files with CRLF on checkout
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def locked_files():
    return sorted({p for g in LOCKED_GLOBS for p in SKILL.glob(g)})


def check():
    problems = []
    try:
        recorded = json.loads(MANIFEST.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return [f"missing {MANIFEST.name}"]
    current = {p.relative_to(SKILL).as_posix(): digest(p) for p in locked_files()}
    for rel, h in recorded.items():
        if rel not in current:
            problems.append(f"locked file removed: {rel}")
        elif current[rel] != h:
            problems.append(f"locked file changed: {rel}")
    for rel in current.keys() - recorded.keys():
        if not rel.startswith("references/approved/"):        # new approved samples may only be appended
            problems.append(f"new file under a locked path, not recorded: {rel}")
    for rel, text, item in CLAUSES:
        f = SKILL / rel
        if not f.exists() or text not in f.read_text(encoding="utf-8"):
            problems.append(f"locked clause {item} missing from {rel}: {text[:40]}")
    comp = (SKILL / "scripts" / "components.py").read_text(encoding="utf-8")
    m = re.search(r"^MIN_COVER = ([0-9.]+)", comp, re.M)
    if not m or float(m.group(1)) < 0.5:
        problems.append("L-7: MIN_COVER lowered below 0.5")
    m = re.search(r"^MAX_BLOCKS = (\d+)", comp, re.M)
    if not m or int(m.group(1)) > 5:
        problems.append("L-7: MAX_BLOCKS raised above 5")
    if not re.search(r"if heroes > 2:", comp):
        problems.append("L-7: hero-number cap changed (expected `if heroes > 2:`)")
    return problems


def main():
    if "--update" in sys.argv:
        data = {p.relative_to(SKILL).as_posix(): digest(p) for p in locked_files()}
        MANIFEST.write_text(json.dumps(data, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"recorded {len(data)} locked files in {MANIFEST.name}; log the change in style-lock.md")
        return
    problems = check()
    if problems:
        print("[STYLE-LOCK] the locked visual style was changed (references/style-lock.md):")
        for p in problems:
            print("  -", p)
        print("Changing a locked item needs the user's explicit approval naming that item; "
              "then log it in style-lock.md and run style_guard.py --update.")
        sys.exit(1)
    print("STYLE-LOCK OK")


if __name__ == "__main__":
    main()
