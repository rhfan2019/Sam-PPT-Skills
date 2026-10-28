"""Find the reference library for a run, so the user never has to point at it (step 0).

  python find_library.py                      the default installed library
  python find_library.py <name>               an installed library by name, e.g. rnb
  python find_library.py <reference.pptx>     the library prepared from this deck

Installed libraries live under ~/.claude/sam-ppt/references/<name>/ (override the root with the
SAM_PPT_REFERENCES environment variable); each holds the prepare_reference.py output, modules.json
and the deck itself as reference.pptx. install.py puts them there. The default is the one named in
<root>/default, or the only library when there is just one.

For a deck path it looks, in order, for a sibling folder with modules.json whose name shares the
deck's prefix (rnb-core.pptx -> rnb-blueprint), then for an installed library whose reference.pptx
is the same file. Prints "library: <dir>" and "reference: <pptx>"; exit code 2 and the command to
prepare one when nothing is found.
"""
import filecmp
import os
import sys
from pathlib import Path


def root():
    return Path(os.environ.get("SAM_PPT_REFERENCES") or Path.home() / ".claude/sam-ppt/references")


def installed():
    r = root()
    return sorted(p for p in r.iterdir() if (p / "modules.json").exists()) if r.exists() else []


def default():
    libs = installed()
    named = root() / "default"
    if named.exists():
        want = named.read_text(encoding="utf-8").strip()
        return next((p for p in libs if p.name == want), None)
    return libs[0] if len(libs) == 1 else None


def for_deck(deck: Path):
    prefix = deck.stem.split("-")[0].split("_")[0].lower()
    siblings = [p for p in deck.parent.iterdir() if p.is_dir() and (p / "modules.json").exists()]
    hit = [p for p in siblings if p.name.lower().startswith(prefix)] or (siblings if len(siblings) == 1 else [])
    if hit:
        return hit[0], deck
    for p in installed():
        ref = p / "reference.pptx"
        if ref.exists() and ref.stat().st_size == deck.stat().st_size and filecmp.cmp(ref, deck, shallow=False):
            return p, ref
    return None, deck


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg and arg.lower().endswith(".pptx"):
        lib, ref = for_deck(Path(arg).resolve())
    elif arg:
        lib = next((p for p in installed() if p.name.lower().startswith(arg.lower())), None)
        ref = lib / "reference.pptx" if lib else None
    else:
        lib = default()
        ref = lib / "reference.pptx" if lib else None
    if not lib:
        names = ", ".join(p.name for p in installed()) or "none"
        print(f"no reference library found (installed under {root()}: {names})")
        if arg and arg.lower().endswith(".pptx"):
            d = Path(arg).resolve()
            print(f"prepare one: python scripts/prepare_reference.py {d} {d.parent / (d.stem + '-blueprint')}")
        else:
            print("ask the user which reference deck to follow")
        sys.exit(2)
    print(f"library: {lib}")
    print(f"reference: {ref}")


if __name__ == "__main__":
    main()
