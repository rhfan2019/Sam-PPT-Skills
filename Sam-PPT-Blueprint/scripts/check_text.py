"""List page text that does not come from the outline (steps 4 and 5).

  python check_text.py <outline.md> <page.svg> [<page.svg> ...]

Every <text> on a page must be outline wording: a whole item, a phrase cut from one (block titles,
dimension names, units), or a compressed label. Each text is split at spaces, punctuation, arrows and
brackets, and every phrase of 3 or more characters must appear in the outline (also compared without
punctuation), so joining two outline items in one box, or a label next to its value, is fine. Pure
numbers and 1–2 character marks (+, ×, %, "vs") are skipped.

Compressed labels (page-zoning.md §七): a long outline sentence may be shortened to a label by
deleting words, never by rewording: the label's characters must appear in order in ONE outline line,
in pieces of at least 2 characters ("统一数据口径" from "在现场统一数据口径，并把通用做法带回产品"). Such a
label is accepted only when its source sentence is kept for the reader: on the same page (a caption
or note text) or in that page's speaker notes (<project>/notes/total.md, section "# <page file stem>").
Labels without their sentence are printed with the sentence to restore.

Whatever is printed was added by the page author or left over from the reference: replace it with
outline wording, or delete it and let the diagram carry the meaning. Exit code 1 when anything is
printed.
"""
import re
import sys
from pathlib import Path

from lxml import etree

DROP = re.compile(r"[\s　，。、；：:;,.!！?？\"'“”‘’「」『』（）()\[\]【】<>《》｜|/\\→←↑↓⇒·•…—–\-~～=＝+＋×*#¦●▪■◆◇○◦]")
MARK = re.compile(r"[\d.%％万亿千百个份倍年月周天人家qQ]*")


def norm(s):
    return DROP.sub("", s).lower()


def texts(path):
    root = etree.parse(path).getroot()
    for t in root.iter("{http://www.w3.org/2000/svg}text"):
        s = "".join(t.itertext()).strip()
        if s:
            yield t.get("id") or t.getparent().get("id") or "?", s


def pieces_in_order(label, line, start=0):
    """True when `label` is chunks of at least 2 characters found in `line` in order (words deleted only)."""
    if not label:
        return True
    for k in range(len(label), 1, -1):
        if len(label) - k == 1:
            continue  # would leave a 1-character piece
        i = line.find(label[:k], start)
        while i >= 0:
            if pieces_in_order(label[k:], line, i + k):
                return True
            i = line.find(label[:k], i + 1)
    return False


def source_line(phrase, lines):
    best = None
    for raw, n in lines:
        if len(n) > len(phrase) and pieces_in_order(phrase, n):
            if best is None or len(n) < len(best[1]):
                best = (raw, n)
    return best


def notes_for(page):
    p = Path(page).resolve()
    total = p.parent.parent / "notes" / "total.md"
    if not total.exists():
        return ""
    body = total.read_text(encoding="utf-8")
    m = re.search(rf"^#\s*{re.escape(p.stem)}\s*$(.*?)(?=^#\s|\Z)", body, re.M | re.S)
    return norm(m.group(1)) if m else ""


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    raw = open(sys.argv[1], encoding="utf-8").read()
    outline = norm(raw)
    lines = [(ln.strip(" -#>"), norm(ln)) for ln in raw.splitlines() if len(norm(ln)) > 3]
    bad = labels = 0
    for page in sys.argv[2:]:
        name = page.replace(chr(92), "/").rsplit("/", 1)[-1]
        found = list(texts(page))
        on_page = norm(" ".join(s for _, s in found))
        notes = notes_for(page)
        for id_, s in found:
            missing, unsourced = [], []
            for n in (norm(x) for x in DROP.split(s)):
                if len(n) <= 2 or n in outline or MARK.fullmatch(n):
                    continue
                src = source_line(n, lines)
                if src is None:
                    missing.append(n)
                elif src[1] in on_page or src[1] in notes:
                    labels += 1
                else:
                    unsourced.append((n, src[0]))
            if missing:
                bad += 1
                print(f"{name}  {id_}  {s}  ← 不在大纲：{'、'.join(missing)}")
            for n, sentence in unsourced:
                bad += 1
                print(f"{name}  {id_}  {s}  ← 压缩标签「{n}」的原句不在本页说明或备注里：{sentence}")
    if bad:
        print(f"\n{bad} 处文字不是来自大纲：换成大纲原文、删掉让图示表达，或把压缩标签的原句放进本页说明或备注")
        sys.exit(1)
    print("全部文字都来自大纲" + (f"（含 {labels} 处压缩标签，原句都在本页或备注里）" if labels else ""))


if __name__ == "__main__":
    main()
