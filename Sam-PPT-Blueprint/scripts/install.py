"""Install the Skill and a reference library for everyday use (once per machine, or after an update).

  python install.py                                         the Skill only
  python install.py <reference.pptx> <library_dir> --name rnb [--default]

Copies this Skill to ~/.claude/skills/Sam-PPT-Blueprint (replacing an older copy), so every session
on the machine has it. With a reference deck and its prepared library (prepare_reference.py output
plus modules.json), also copies the library to ~/.claude/sam-ppt/references/<name>/ with the deck as
reference.pptx; --default (or being the first library) makes it the one used when the user names no
reference. After this a user only says "用 Sam-PPT-Blueprint 把 <大纲> 做成 PPT" in any folder.
"""
import argparse
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from find_library import root  # noqa: E402

SKIP = shutil.ignore_patterns("__pycache__", "*.pyc", "*-superseded.*")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("reference", nargs="?", type=Path)
    ap.add_argument("library", nargs="?", type=Path)
    ap.add_argument("--name")
    ap.add_argument("--default", action="store_true")
    a = ap.parse_args()

    skill = HERE.parent
    dst = Path.home() / ".claude/skills" / skill.name
    if dst.resolve() != skill:
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(skill, dst, ignore=SKIP)
        print(f"skill: {dst}")

    if a.reference or a.library:
        if not (a.reference and a.library and a.name):
            ap.error("a library install needs <reference.pptx> <library_dir> --name")
        if not (a.library / "modules.json").exists():
            sys.exit(f"{a.library} has no modules.json: prepare and catalogue it first (module-catalog.md)")
        r = root()
        first = not any(r.glob("*/modules.json")) if r.exists() else True
        lib = r / a.name
        if lib.exists():
            shutil.rmtree(lib)
        shutil.copytree(a.library, lib, ignore=SKIP)
        shutil.copy2(a.reference, lib / "reference.pptx")
        if a.default or first:
            (r / "default").write_text(a.name, encoding="utf-8")
        print(f"library: {lib}{'  (default)' if a.default or first else ''}")


if __name__ == "__main__":
    main()
