"""List page text that does not come from the outline (steps 4 and 5).

  python check_text.py <outline.md> <page.svg> [<page.svg> ...]

Every <text> on a page must be outline wording: a whole item, or a phrase cut from one (block
titles, dimension names, units). Each text is split at spaces, punctuation, arrows and brackets, and
every phrase of 3 or more characters must appear in the outline (also compared without punctuation),
so joining two outline items in one box, or a label next to its value, is fine. Pure numbers and
1–2 character marks (+, ×, %, "vs") are skipped. Whatever is printed was added by the page author or
left over from the reference: replace it with outline wording, or delete it and let the diagram carry
the meaning. Exit code 1 when anything is printed.
"""
import re
import sys

from lxml import etree

DROP = re.compile(r"[\s　，。、；：:;,.!！?？\"'“”‘’「」『』（）()\[\]【】<>《》｜|/\\→←↑↓⇒·•…—–\-~～=＝+＋×*#]")


def norm(s):
    return DROP.sub("", s).lower()


def texts(path):
    root = etree.parse(path).getroot()
    for t in root.iter("{http://www.w3.org/2000/svg}text"):
        s = "".join(t.itertext()).strip()
        if s:
            yield t.get("id") or t.getparent().get("id") or "?", s


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    outline = norm(open(sys.argv[1], encoding="utf-8").read())
    bad = 0
    for page in sys.argv[2:]:
        for id_, s in texts(page):
            phrases = [norm(x) for x in DROP.split(s)]
            missing = [n for n in phrases if len(n) > 2 and n not in outline
                       and not re.fullmatch(r"[\d.%％万亿千百个份倍年月周天人家qQ]*", n)]
            if missing:
                bad += 1
                print(f"{page.replace(chr(92), '/').rsplit('/', 1)[-1]}  {id_}  {s}  ← 不在大纲：{'、'.join(missing)}")
    if bad:
        print(f"\n{bad} 处文字不是来自大纲：换成大纲原文，或删掉、让图示表达")
        sys.exit(1)
    print("全部文字都来自大纲")


if __name__ == "__main__":
    main()
