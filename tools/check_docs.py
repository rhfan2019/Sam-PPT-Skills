"""Check the repository layout against docs/architecture/repository-contract.md (section 8).

    python tools/check_docs.py              check this repository; prints violations, exit 1 if any
    python tools/check_docs.py --selftest   build a broken copy for each rule and confirm it is caught

Run before every commit. To change a rule, change the contract first, then this file.
"""
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT_ALLOWED = {".git", ".gitignore", ".gitattributes", "CLAUDE.md", "README.md", "docs", "tools"}
DOCS_ALLOWED = {"README.md", "architecture", "plans", "guides", "samples", "archive"}
SKILL_FORBIDDEN = re.compile(r"(docs|handover|backlog|findings|outline)", re.I)
VERSIONED = re.compile(r"(^|/)v\d+(/|$)|-(new|final|superseded)\.", re.I)
LINK = re.compile(r"\]\(([^)\s]+)\)")


def skills(root):
    return [p for p in root.iterdir() if p.is_dir() and (p / "SKILL.md").exists()]


def check(root):
    errs = []
    names = {s.name for s in skills(root)}
    for p in root.iterdir():
        if p.name not in ROOT_ALLOWED | names:
            errs.append(f"root: {p.name} is not allowed (contract 2)")
    docs = root / "docs"
    if docs.exists():
        for p in docs.iterdir():
            if p.name not in DOCS_ALLOWED:
                errs.append(f"docs: {p.name} is not allowed (contract 3)")
    for s in skills(root):
        for p in s.rglob("*"):
            if SKILL_FORBIDDEN.search(p.name):
                errs.append(f"skill: {p.relative_to(root).as_posix()} looks like a dev doc or case file (contract 4)")
    files = [p for p in root.rglob("*") if ".git" not in p.relative_to(root).parts]
    for p in files:
        if VERSIONED.search(p.relative_to(root).as_posix()):
            errs.append(f"version: {p.relative_to(root).as_posix()} (contract 3, one version only)")
    for md in (p for p in files if p.suffix == ".md"):
        text = re.sub(r"```.*?```", "", md.read_text(encoding="utf-8"), flags=re.S)
        for target in LINK.findall(text):
            if re.match(r"[a-z]+:", target) or target.startswith("#"):
                continue
            path = target.split("#")[0]
            if not (md.parent / path).exists():
                errs.append(f"link: {md.relative_to(root).as_posix()} -> {target} does not exist")
    return errs


def selftest(root):
    cases = {
        "root": lambda r: (r / "notes.md").write_text("x", encoding="utf-8"),
        "docs": lambda r: (r / "docs/tmp").mkdir(),
        "skill": lambda r: (skills(r)[0] / "handover.md").write_text("x", encoding="utf-8"),
        "version": lambda r: (r / "docs/plans/plan-final.md").write_text("x", encoding="utf-8"),
        "link": lambda r: (r / "docs/plans/x.md").write_text("[a](missing.md)", encoding="utf-8"),
    }
    ok = True
    for rule, breaks in cases.items():
        with tempfile.TemporaryDirectory() as t:
            copy = Path(t) / "repo"
            shutil.copytree(root, copy, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            before = check(copy)
            breaks(copy)
            caught = [e for e in check(copy) if e.startswith(rule + ":") and e not in before]
            print(f"{rule}: {'caught' if caught else 'MISSED'}")
            ok &= bool(caught)
    return ok


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    root = Path(__file__).resolve().parent.parent
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest(root) else 1)
    errs = check(root)
    print("\n".join(errs) if errs else "ok")
    sys.exit(1 if errs else 0)


if __name__ == "__main__":
    main()
