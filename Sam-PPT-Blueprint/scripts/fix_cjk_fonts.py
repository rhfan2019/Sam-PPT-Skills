"""Fix B: after export, give Chinese text the same OPPOSans face as its Latin text.

ppt-master only knows a fixed list of CJK faces. For "OPPOSans B, ..." it writes
latin=OPPOSans B but ea=Microsoft YaHei (and YaHei in the theme), so Chinese text
renders in YaHei. OPPOSans carries the CJK glyphs itself.

Pairing rule, applied per run-property element (rPr / defRPr / endParaRPr) in
slides, layouts, masters and charts: only when its latin face is OPPOSans* and its
ea slot is YaHei or a theme reference, ea becomes the latin face. Runs with any
other latin face, or an explicitly chosen ea face, are left alone. In the theme,
each major/minor font's ea (and Hans/Hant script) face follows that block's latin
face when the latter is OPPOSans*.

If fix A (export.py) already worked, this changes nothing.

Usage: python fix_cjk_fonts.py <deck.pptx> [-o out.pptx]   (default: rewrite in place)
"""
import argparse
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

FALLBACK = "Microsoft YaHei"
PARTS = ("ppt/slides/", "ppt/slideLayouts/", "ppt/slideMasters/", "ppt/charts/")

RUN_PROPS = re.compile(r"<a:(?:rPr|defRPr|endParaRPr)\b[^>]*?(?:/>|>.*?</a:(?:rPr|defRPr|endParaRPr)>)", re.S)
LATIN = re.compile(r'<a:latin typeface="(OPPOSans[^"]*)"')
EA = re.compile(r'(<a:ea typeface=")(?:' + re.escape(FALLBACK) + r'|\+mn-ea|\+mj-ea)"')


def fix_runs(xml):
    n = 0

    def one(m):
        nonlocal n
        props = m.group(0)
        latin = LATIN.search(props)
        if not latin:
            return props
        new, k = EA.subn(lambda e: e.group(1) + latin.group(1) + '"', props)
        n += k
        return new

    return RUN_PROPS.sub(one, xml), n


def fix_theme(xml):
    n = 0

    def one(m):
        nonlocal n
        body = m.group(0)
        latin = LATIN.search(body)
        if not latin:
            return body
        face = latin.group(1)
        other = r'(?!' + re.escape(face) + r'")[^"]*"'
        body, k1 = re.subn(r'(<a:ea typeface=")' + other, lambda e: e.group(1) + face + '"', body, count=1)
        body, k2 = re.subn(r'(<a:font script="(?:Hans|Hant)" typeface=")' + other, lambda e: e.group(1) + face + '"', body)
        n += k1 + k2
        return body

    return re.sub(r"<a:(majorFont|minorFont)>.*?</a:\1>", one, xml, flags=re.S), n


def fix_deck(src: Path, out: Path) -> tuple[int, int]:
    """Return (slots changed, YaHei slots left)."""
    changed = left = 0
    with tempfile.TemporaryDirectory() as tmp:
        tmp_out = Path(tmp) / "out.pptx"
        with zipfile.ZipFile(src) as zin, zipfile.ZipFile(tmp_out, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                name = item.filename
                if name.endswith(".xml") and (name.startswith(PARTS) or name.startswith("ppt/theme/")):
                    xml = data.decode("utf-8")
                    new, k = fix_theme(xml) if name.startswith("ppt/theme/") else fix_runs(xml)
                    changed += k
                    left += len(re.findall(r'<a:(?:ea|font script="Han[st]") typeface="' + re.escape(FALLBACK) + '"', new))
                    data = new.encode("utf-8")
                zout.writestr(item, data)
        shutil.copyfile(tmp_out, out)
    return changed, left


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("-o", "--output")
    a = ap.parse_args()
    src = Path(a.deck)
    out = Path(a.output) if a.output else src
    changed, left = fix_deck(src, out)
    print(f"fix_cjk_fonts: {changed} East Asian slot(s) set to OPPOSans, {left} YaHei slot(s) left -> {out}")


if __name__ == "__main__":
    main()
