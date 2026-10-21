# -*- coding: utf-8 -*-
"""Cover and contents."""
from pptx.enum.dml import MSO_LINE_DASH_STYLE as DASH
from pptx.enum.shapes import MSO_SHAPE

from ..components import *
from ..deck import grad, radial, shadow
from ..tokens import *


def cover(D, s):
    D.new(header=False, notes=s.get("speaker_notes"))
    if s.get("background"):
        D.photo(s["background"], 6.2, 3.9, ER - 6.2, 3.1, opacity=45, feather=0.2)
    h = D.rect(7.0, 0.55, 5.9, 5.9, fill=NAVY_T, shape=MSO_SHAPE.OVAL)
    radial(h, [(0, "C9D7EA", 90), (65, "E4EBF5", 60), (100, "FFFFFF", 0)])
    D.rect(7.75, 1.3, 4.4, 4.4, line=NAVY_B, lw=1, shape=MSO_SHAPE.OVAL, dash=DASH.DASH)
    hero = s.get("hero", {})
    if hero.get("main"):
        v, lab = hero["main"]
        c1 = D.rect(8.55, 1.0, 2.75, 2.75, fill=NAVY, line=WHITE, lw=4, shape=MSO_SHAPE.OVAL)
        grad(c1, GRAD_NAVY, angle=90); shadow(c1, opacity=35, blur=14, dist=5)
        D.text(8.55, 1.6, 2.75, 0.85, v, size=50, color=WHITE, face=H, align="c")
        D.text(8.55, 2.5, 2.75, 0.32, lab, size=11.5, color=ON_DARK, face=M, align="c")
    if hero.get("red"):
        v, unit, lab = hero["red"]
        c2 = D.rect(7.25, 3.05, 1.85, 1.85, fill=RED, line=WHITE, lw=4, shape=MSO_SHAPE.OVAL)
        grad(c2, GRAD_RED, angle=90); shadow(c2, color=RED, opacity=35, blur=12, dist=4)
        D.text(7.25, 3.5, 1.85, 0.55, [(v, {}), (unit, {"size": 10, "face": M})], size=24, color=WHITE, face=H, align="c")
        D.text(7.25, 4.05, 1.85, 0.3, lab, size=10, color=ON_RED, face=M, align="c")
    if hero.get("white"):
        v, lab = hero["white"]
        c3 = D.rect(11.15, 2.85, 1.6, 1.6, fill=WHITE, line=NAVY_B, lw=1, shape=MSO_SHAPE.OVAL)
        shadow(c3, opacity=25, blur=10, dist=3)
        D.text(11.15, 3.18, 1.6, 0.55, v, size=24, color=RED, face=H, align="c")
        D.text(11.15, 3.75, 1.6, 0.3, lab, size=10, color=NAVY, face=M, align="c")
    if s.get("photo"):
        D.photo_fit(s["photo"], 8.0, 4.15, 4.6)
    x = 0.84
    if s.get("label"):
        t = D.box_text(x, 1.45, 1.55, 0.38, s["label"], RED, WHITE, 12, M, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.5)
        grad(t, GRAD_RED, angle=0)
    D.text(x, 2.1, 6.4, 1.6, s["title_lines"], size=40, color=NAVY, face=H, spacing=1.05)
    if s.get("subtitle"):
        D.text(x, 3.85, 6.2, 0.4, s["subtitle"], size=17, color=NAVY_D, face=M)
    for i, c in enumerate(s.get("chips", [])[:3]):
        cx = x + i * 1.95
        tone = c.get("tone", "navy")
        wcard(D, cx, 4.55, 1.8, 0.5, tone)
        gcircle(D, cx + 0.08, 4.6, 0.4, tone, icon=c.get("icon", "cube"), ring=1.5)
        D.text(cx + 0.55, 4.55, 1.2, 0.5, c["text"], size=12, color=col_of(tone), face=M, anchor="m")
    if s.get("byline"):
        D.text(x, 5.55, 5.0, 0.3, s["byline"], size=12, color=GREY_M, face=M)
    if s.get("note"):
        D.text(x, 5.95, 6.0, 0.25, s["note"], size=9.5, color=GREY_M)


def contents(D, s):
    D.new(s.get("title", "报告目录"), s.get("section", "CONTENTS"), notes=s.get("speaker_notes"))
    pw = 3.7
    pnl = D.rect(EL, 1.15, pw, 5.4, fill=NAVY)
    grad(pnl, [(0, "16365F", 100), (100, "2E5A94", 100)], angle=90)
    shadow(pnl, opacity=30, blur=10, dist=3)
    if s.get("photo", "city_dusk"):
        D.photo(s.get("photo", "city_dusk"), EL, 4.35, pw, 2.2, opacity=30, feather=0.12)
    p = s.get("panel", {})
    D.text(EL + 0.35, 1.5, 3.0, 0.45, "CONTENTS", size=22, color=NAVY_L, face=H)
    D.text(EL + 0.35, 1.95, 3.0, 0.85, "目录", size=44, color=WHITE, face=H)
    if p.get("kicker"):
        D.text(EL + 0.35, 3.2, 2.9, 0.3, p["kicker"], size=11, color=NAVY_L, face=M)
    if p.get("claim"):
        D.text(EL + 0.35, 3.5, 3.0, 1.0, p["claim"], size=22, color=WHITE, face=B, spacing=1.12)
    if p.get("text"):
        D.text(EL + 0.35, 4.65, 3.05, 0.9, p["text"], size=10.5, color=ON_DARK, spacing=1.25)
    chs = s["chapters"][:6]
    rh = 5.4 / max(len(chs), 5)
    nx = EL + pw + 0.3
    cx = nx + 0.4
    for i, c in enumerate(chs):
        y = 1.15 + i * rh
        tone = "navy" if i % 2 == 0 else "red"
        col = col_of(tone)
        wcard(D, cx, y + 0.05, ER - cx, rh - 0.2, tone)
        num = D.rect(nx, y + 0.13, 1.05, rh - 0.36, fill=col, shape=MSO_SHAPE.PENTAGON, adj=0.3)
        grad(num, GRAD_NAVY if tone == "navy" else GRAD_RED, angle=0)
        shadow(num, color=col, opacity=25)
        D.text(nx, y + 0.13, 0.9, rh - 0.36, f"{i + 1:02d}", size=22, color=WHITE, face=H, align="c", anchor="m")
        D.text(cx + 0.9, y + 0.15, 4.0, 0.4, c["title"], size=18, color=col, face=H)
        D.text(cx + 0.9, y + 0.56, 4.0, 0.3, c.get("sub", ""), size=11.5, color=GREY)
        D.text(ER - 3.5, y + 0.3, 1.0, 0.4, c.get("pages", ""), size=11, color=GREY_M, face=M)
        if c.get("kpi"):
            D.line(ER - 2.5, y + 0.25, ER - 2.5, y + rh - 0.35, NAVY_B, 0.75, DASH.DASH)
            D.text(ER - 2.35, y + 0.12, 2.15, 0.45, c["kpi"], size=20, color=col, face=H, align="c")
            D.text(ER - 2.35, y + 0.56, 2.15, 0.3, c.get("kpi_label", ""), size=9.5, color=GREY_M, align="c")


LAYOUTS = {"cover": cover, "contents": contents}
