# -*- coding: utf-8 -*-
"""Maintainer tool: cut assets/kit.pptx out of the original 参考模板 template.

The kit keeps the template's master, layout and theme, plus three harvest slides:
  1. header  – title text box, hand icon, section tag, title rule, footer rule, disclaimer, signature
  2. icons   – the template's own icon graphics (svg + png fallback), one picture per key
  3. photos  – template photos, downscaled, one picture per key
Every harvested element is named "<kind>:<key>" so the engine can find it.

Usage:  python make_kit.py "参考模板" ../assets/kit.pptx
"""
import copy
import io
import re
import sys

from lxml import etree
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.oxml.ns import qn
from pptx.opc.constants import RELATIONSHIP_TYPE as RT
from pptx.util import Inches, Pt

# (template slide no., shape id) of every icon the layouts may use
ICONS = {
    "battery": (56, 349), "home": (46, 1029), "growth": (11, 288), "coin": (3, 259),
    "ai": (10, 285), "city": (11, 289), "globe": (7, 264), "storm": (13, 227),
    "family": (67, 382), "man": (67, 370), "target": (39, 347), "check": (1, 1087),
    "box": (1, 1085), "cycle": (3, 400), "trend": (3, 394), "improve": (43, 34),
    "cart": (79, 79), "warn": (80, 218), "cube": (7, 185), "crown": (14, 47),
    "star": (23, 1058), "chat": (3, 399), "computer": (43, 33), "tag": (3, 257),
    "group": (77, 134), "women": (67, 417), "kid": (67, 413),
}
PHOTOS = {"car3d": (20, 31), "sedan": (22, 3074), "dealer": (22, 1042), "city_sun": (34, 3078),
          "city_dusk": (34, 3074), "city_tech": (35, 1051), "tower": (35, 1050)}
HEADER_SLIDE, RULE_SLIDE = 13, 10
HEADER_NAMES = {"文本框 2": "title", "图形 12": "icon", "文本框 1": "tag", "textbox 292": "sign"}
RULE_NAMES = {"直线连接符 4": "rule", "Grey bottom line": "foot_rule"}
PHOTO_MAX_PX = 1600


def find(shapes, sid):
    for sh in shapes:
        if sh.shape_type == 6:
            r = find(sh.shapes, sid)
            if r is not None:
                return r
        elif sh.shape_id == sid:
            return sh._element
    return None


PLACEHOLDER = {"title": "{页面标题}", "tag": "{章节标签}", "sign": "{署名 meta.sign}", "disc": "{免责声明 meta.disclaimer}"}
NOTE_HEADER = [
    "这是 Sam-PPT-Bain 的素材包，不是演示文稿模板。",
    "程序按形状名称读取素材：hdr:*（本页的页头页脚）、icon:*（第 2 页图标）、photo:*（第 3 页图片）。",
    "本页的页头页脚就是每一页生成后的样子：花括号里的文字在生成时由 deck.json 替换，位置和样式完全保留。",
    "灰色说明文字和底色块（note:*）只供人阅读，程序会忽略。",
    "重新生成本文件：python scripts/make_kit.py <参考模板> assets/kit.pptx",
]


def note(slide, x, y, w, h, text, size=12, bold=False, align="l"):
    """Human-readable label; named note:* so the engine ignores it."""
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tb.name = "note:label"
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate([text] if isinstance(text, str) else text):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = {"l": PP_ALIGN.LEFT, "c": PP_ALIGN.CENTER}[align]
        p.space_after = Pt(6)
        r = p.add_run()
        r.text = line
        r.font.size = Pt(size); r.font.bold = bold
        r.font.color.rgb = RGBColor.from_string("1C4274" if bold else "595959")
        rPr = r._r.get_or_add_rPr()
        for tag in ("a:latin", "a:ea"):
            etree.SubElement(rPr, qn(tag)).set("typeface", "OPPOSans R")
    return tb


def place(el, x, y, w, h):
    xfrm = el.find(".//" + qn("a:xfrm"))
    xfrm.find(qn("a:off")).set("x", str(int(Inches(x)))); xfrm.find(qn("a:off")).set("y", str(int(Inches(y))))
    xfrm.find(qn("a:ext")).set("cx", str(int(Inches(w)))); xfrm.find(qn("a:ext")).set("cy", str(int(Inches(h))))


def is_white_icon(el, part):
    for node in el.iter():
        rid = node.get(qn("r:embed"))
        if rid:
            p = part.related_part(rid)
            if p.content_type == "image/svg+xml":
                svg = p.blob.decode("utf8", "ignore")
                if "MsftOfcThm_Background" in svg:      # PowerPoint repaints these with a pale theme colour
                    return True
                ops = [float(v) for v in re.findall(r'fill-opacity="([0-9.]+)"', svg)]
                if ops and max(ops) < 0.5:              # drawn semi-transparent -> reads as pale
                    return True
                cols = re.findall(r"#([0-9A-Fa-f]{6})\b", svg)
                # light icon (white / pale grey) -> needs a dark tile to be visible
                return bool(cols) and all(min(int(c[i:i + 2], 16) for i in (0, 2, 4)) >= 0xB0 for c in cols)
    return False


def paste(dst_slide, el, src_part, name):
    el = copy.deepcopy(el)
    for node in el.iter():
        for attr in (qn("r:embed"), qn("r:link")):
            rid = node.get(attr)
            if rid:
                node.set(attr, dst_slide.part.relate_to(src_part.related_part(rid), RT.IMAGE))
    el.find(".//" + qn("p:cNvPr")).set("name", name)
    dst_slide.shapes._spTree.append(el)


def main(src, dst):
    prs = Presentation(src)
    slides = list(prs.slides)
    layout = prs.slide_layouts[0]
    hdr, ico, pho = (prs.slides.add_slide(layout) for _ in range(3))

    s = slides[HEADER_SLIDE - 1]
    for sh in s.shapes:
        if sh.name in HEADER_NAMES:
            paste(hdr, sh._element, s.part, "hdr:" + HEADER_NAMES[sh.name])
        elif sh.name == "Disclaimer" and sh.has_text_frame and "本报告" in sh.text_frame.text:
            paste(hdr, sh._element, s.part, "hdr:disc")
    s = slides[RULE_SLIDE - 1]
    for sh in s.shapes:
        if sh.name in RULE_NAMES:
            paste(hdr, sh._element, s.part, "hdr:" + RULE_NAMES[sh.name])

    # header texts become placeholders (the engine replaces them on every slide)
    for sh in hdr.shapes:
        key = sh.name.partition(":")[2]
        if key in PLACEHOLDER:
            runs = sh._element.findall(".//" + qn("a:r"))
            runs[0].find(qn("a:t")).text = PLACEHOLDER[key]
            for r in runs[1:]:
                r.getparent().remove(r)
    note(hdr, 0.84, 2.4, 11.6, 2.6, NOTE_HEADER, 14)

    note(ico, 0.37, 0.25, 12.6, 0.5, "图标（%d 个）：生成时由程序按需着色；形状名 icon:<键> 是程序读取的依据，请勿改名" % len(ICONS), 16, bold=True)
    for i, (key, (sno, sid)) in enumerate(ICONS.items()):
        sl = slides[sno - 1]
        el = find(sl.shapes, sid)
        if el is None:
            raise SystemExit(f"icon {key} not found on slide {sno}")
        x, y = 0.37 + (i % 9) * 1.4, 1.0 + (i // 9) * 2.05
        white = is_white_icon(el, sl.part)
        tile = ico.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(1.2), Inches(1.2))
        tile.name = "note:tile"
        tile.fill.solid(); tile.fill.fore_color.rgb = RGBColor.from_string("1C4274" if white else "EEF2F8")
        tile.line.fill.background(); tile.shadow.inherit = False
        paste(ico, el, sl.part, "icon:" + key)
        place(ico.shapes._spTree[-1], x + 0.25, y + 0.25, 0.7, 0.7)
        note(ico, x - 0.1, y + 1.25, 1.4, 0.3, key, 11, align="c")

    note(pho, 0.37, 0.25, 12.6, 0.5, "图片（%d 张，已缩至 %dpx）：形状名 photo:<键> 是程序读取的依据，请勿改名" % (len(PHOTOS), PHOTO_MAX_PX), 16, bold=True)
    for i, (key, (sno, sid)) in enumerate(PHOTOS.items()):
        sl = slides[sno - 1]
        el = find(sl.shapes, sid)
        blob = sl.part.related_part(el.find(".//" + qn("a:blip")).get(qn("r:embed"))).blob
        im = Image.open(io.BytesIO(blob))
        im.thumbnail((PHOTO_MAX_PX, PHOTO_MAX_PX))
        buf = io.BytesIO()
        if im.mode in ("RGBA", "LA", "P"):
            im.convert("RGBA").save(buf, "PNG", optimize=True)
        else:
            im.convert("RGB").save(buf, "JPEG", quality=88)
        buf.seek(0)
        x, y = 0.37 + (i % 4) * 3.2, 1.0 + (i // 4) * 3.0
        iw, ih = im.size
        w, h = (2.9, 2.9 * ih / iw) if iw / ih >= 2.9 / 2.2 else (2.2 * iw / ih, 2.2)
        if im.mode in ("RGBA", "LA", "P"):        # cut-outs: show them on a tint so the outline is visible
            t = pho.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(2.9), Inches(2.2))
            t.name = "note:tile"; t.fill.solid(); t.fill.fore_color.rgb = RGBColor.from_string("EEF2F8")
            t.line.fill.background(); t.shadow.inherit = False
        pic = pho.shapes.add_picture(buf, Inches(x + (2.9 - w) / 2), Inches(y + (2.2 - h) / 2), Inches(w), Inches(h))
        pic.name = "photo:" + key
        note(pho, x, y + 2.28, 2.9, 0.3, f"{key}  ({iw}×{ih}{'，透明底' if im.mode in ('RGBA', 'LA', 'P') else ''})", 11, align="c")

    lst = prs.slides._sldIdLst
    for sid in list(lst)[:len(slides)]:
        prs.part.drop_rel(sid.rId)
        lst.remove(sid)
    prs.save(dst)
    print("kit written:", dst)


if __name__ == "__main__":
    main(*sys.argv[1:3])
