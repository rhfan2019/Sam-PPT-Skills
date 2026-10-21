"""Point the East Asian font slots of a ppt-master export at OPPOSans.

ppt-master only recognises a fixed list of CJK faces, so for an SVG stack like
"OPPOSans M, Microsoft YaHei" it writes latin=OPPOSans M but ea=Microsoft YaHei,
and its theme uses Microsoft YaHei for every East Asian slot. OPPOSans carries the
CJK glyphs itself, so Chinese text must use the same face as the Latin text.

Usage: python fix_cjk_fonts.py <deck.pptx> [-o out.pptx]   (default: rewrite in place)
"""
import argparse
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

FALLBACK = "Microsoft YaHei"
THEME_FACES = {"majorFont": "OPPOSans H", "minorFont": "OPPOSans R"}

RUN_PROPS = re.compile(r"<a:(?:rPr|defRPr|endParaRPr)\b[^>]*?(?:/>|>.*?</a:(?:rPr|defRPr|endParaRPr)>)", re.S)
LATIN = re.compile(r'<a:latin typeface="(OPPOSans [A-Z])"')
# The ea slot is either the fallback face or a theme reference (+mn-ea is the Regular
# weight), both of which lose the run's explicit OPPOSans weight for Chinese text.
EA = re.compile(r'(<a:ea typeface=")(?:' + re.escape(FALLBACK) + r'|\+mn-ea|\+mj-ea)"')


def fix_runs(xml):
    def one(m):
        props = m.group(0)
        latin = LATIN.search(props)
        return EA.sub(r'\g<1>' + latin.group(1) + '"', props) if latin else props
    return RUN_PROPS.sub(one, xml)


def fix_theme(xml):
    for block, face in THEME_FACES.items():
        def one(m, face=face):
            body = m.group(0)
            body = re.sub(r'(<a:ea typeface=")[^"]*"', r'\g<1>' + face + '"', body, count=1)
            return re.sub(r'(<a:font script="(?:Hans|Hant)" typeface=")[^"]*"', r'\g<1>' + face + '"', body)
        xml = re.sub(rf"<a:{block}>.*?</a:{block}>", one, xml, flags=re.S)
    return xml


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck")
    ap.add_argument("-o", "--output")
    a = ap.parse_args()
    src = Path(a.deck)
    out = Path(a.output) if a.output else src
    changed = 0
    with tempfile.TemporaryDirectory() as tmp:
        tmp_out = Path(tmp) / "out.pptx"
        with zipfile.ZipFile(src) as zin, zipfile.ZipFile(tmp_out, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                name = item.filename
                if name.endswith(".xml") and (name.startswith("ppt/slides/") or name.startswith("ppt/slideLayouts/")
                                              or name.startswith("ppt/slideMasters/") or name.startswith("ppt/theme/")):
                    xml = data.decode("utf-8")
                    new = fix_theme(xml) if name.startswith("ppt/theme/") else fix_runs(xml)
                    if new != xml:
                        changed += 1
                        data = new.encode("utf-8")
                zout.writestr(item, data)
        shutil.copyfile(tmp_out, out)
    print(f"fix_cjk_fonts: {changed} part(s) updated -> {out}")


if __name__ == "__main__":
    main()
