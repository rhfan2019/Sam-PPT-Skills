"""Build the one file the meaning reviewer reads: plan rows, outline text and module parts, page by page.

  python review_packet.py <run>/plan.md <outline.md> <modules.json> -o <run>/review-packet.md

Pages are matched by number: plan headings "## P01 …" (or ###), outline headings "## 第 1 页…" /
"## P01…" (otherwise the outline's level-2 headings in order). Module ids (NN-X) are taken from each
plan block; their parts, not_for and start notes are printed once per page. A crop sheet of every
module used is written next to the packet (review-crops.png), for parts whose wording is unclear.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pick_modules import crop_sheet, show  # noqa: E402

MODULE = re.compile(r"\b(\d{2}-[A-Z])\b")


def blocks(text, heading):
    """{page number: block text} for headings matched by `heading` (group 1 = page number)."""
    out, cur = {}, None
    for line in text.splitlines():
        m = heading.match(line)
        if m:
            cur = int(next(g for g in m.groups() if g))
            out[cur] = [line]
        elif line.startswith("## ") and not heading.match(line):
            cur = None
        elif cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def outline_pages(text):
    pages = blocks(text, re.compile(r"^##\s*(?:第\s*(\d+)\s*页|P(\d+))"))
    if pages:
        return pages
    heads = [i for i, l in enumerate(text.splitlines()) if l.startswith("## ")]
    lines = text.splitlines()
    return {n: "\n".join(lines[s:e]).strip() for n, (s, e) in
            enumerate(zip(heads, heads[1:] + [len(lines)]), 1)}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("plan", type=Path)
    ap.add_argument("outline", type=Path)
    ap.add_argument("catalog", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    a = ap.parse_args()

    plan_text = a.plan.read_text(encoding="utf-8")
    plan = blocks(plan_text, re.compile(r"^#{2,3}\s*P(\d+)"))
    outline = outline_pages(a.outline.read_text(encoding="utf-8"))
    by = {m["module"]: m for m in json.loads(a.catalog.read_text(encoding="utf-8"))}
    if not plan:
        sys.exit("plan.md has no '## P01' / '### P01' page headings")

    conventions = re.split(r"^##\s.*全稿约定.*$", plan_text, maxsplit=1, flags=re.M)
    out = ["# 含义审查包", "",
           "每页三段：大纲原文、规划行、规划用到的模块（关系部件、不适合、起页说明）。",
           "部件描述看不懂时再看同目录的 review-crops.png。", ""]
    if len(conventions) > 1:
        out += ["## 全稿约定", conventions[1].split("\n## ", 1)[0].strip(), ""]
    used = []
    for n in sorted(plan):
        ids = list(dict.fromkeys(MODULE.findall(plan[n])))
        used += [i for i in ids if i not in used]
        page = re.sub(r"^#+\s*", "#### ", outline.get(n, "（大纲里没有找到这一页）"), flags=re.M)
        out += [f"## P{n:02d}", "", "### 大纲原文", "", page, "",
                "### 规划", "", plan[n], "", "### 用到的模块", ""]
        for i in ids:
            out += [show(by[i]) if i in by else f"! {i} 不在模块目录里", ""]
    a.out.write_text("\n".join(out), encoding="utf-8")
    crops = crop_sheet([by[i] for i in used if i in by], a.catalog.parent / "started-renders",
                       a.out.parent / "review-crops.png")
    print(f"{a.out}: {len(plan)} 页，{len(used)} 个模块" + (f"；裁切图 {crops}" if crops else ""))


if __name__ == "__main__":
    main()
