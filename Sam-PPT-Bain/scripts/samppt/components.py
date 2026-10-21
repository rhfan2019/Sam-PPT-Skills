# -*- coding: utf-8 -*-
"""Reusable building blocks. Each one owns its internal alignment (shared centre lines, edges),
so layouts never hand-tune a single row."""
from pptx.enum.dml import MSO_LINE_DASH_STYLE as DASH
from pptx.enum.shapes import MSO_SHAPE

from .deck import grad, radial, alpha, shadow
from .tokens import *

TONE = {"navy": NAVY, "red": RED}


def col_of(tone):
    return TONE[tone]


# ----------------------------------------------------------------------------- consulting frame (template slide 10)
def banner(D, text, y=BANNER_Y, h=BANNER_H, size=FS_BANNER):
    """Full-width navy thesis bar: the slide's so-what. '**x**' renders in light coral."""
    b = D.rect(EL, y, CW, h, fill=NAVY)
    grad(b, [(0, "16365F", 100), (55, "1C4274", 100), (100, "2A5791", 100)], angle=0)
    D.text(EL + 0.15, y, CW - 0.3, h, text, size=size, color=WHITE, face=M, align="c", anchor="m",
           hl={"face": H, "color": HILITE_DARK})


def zone(D, x, text, tone="navy", w=2.2, y=ZONE_Y, h=ZONE_H, size=FS_ZONE):
    """Light zone label telling the reader what this half of the page is about."""
    D.box_text(x, y, w, h, text, BLUE_Z if tone == "navy" else PINK_Z, NAVY_D if tone == "navy" else RED_D, size, R)


def tag(D, x, y, w, text, tone="red", h=0.3, size=11):
    D.box_text(x, y, w, h, text, PINK_Z if tone == "red" else BLUE_Z, RED_D if tone == "red" else NAVY_D, size, R)


def chip(D, x, y, w, text, tone="navy", h=0.28, size=10):
    """Gradient pill."""
    c = D.box_text(x, y, w, h, text, col_of(tone), WHITE, size, M, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.5)
    grad(c, GRAD_NAVY if tone == "navy" else GRAD_RED, angle=0)
    return c


def outline_pill(D, x, y, w, text, tone="navy", h=0.28, size=10, filled=False):
    col = col_of(tone)
    return D.box_text(x, y, w, h, text, col if filled else WHITE, WHITE if filled else col, size, B,
                      line=None if filled else (NAVY_B if tone == "navy" else RED_B),
                      shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.5)


def arrow_r(D, x, y, tone="red", w=0.28, h=0.18):
    return D.rect(x, y, w, h, fill=col_of(tone), shape=MSO_SHAPE.RIGHT_ARROW)


def curved_arrow(D, x, y, h=0.75):
    ca = D.rect(x, y, 0.26, h, fill=RED, shape=MSO_SHAPE.CURVED_RIGHT_ARROW)
    grad(ca, [(0, "C0503E", 100), (100, "8E2B1D", 100)], angle=90)


def dot_line(D, x1, y1, x2, y2, col=RED, dash=True, dot_end=True, dot_start=False, w=0.75):
    D.line(x1, y1, x2, y2, col, w, DASH.DASH if dash else None)
    for xx, yy, on in ((x2, y2, dot_end), (x1, y1, dot_start)):
        if on:
            D.rect(xx - 0.05, yy - 0.05, 0.1, 0.1, fill=WHITE, line=col, lw=1, shape=MSO_SHAPE.OVAL)


def module_head(D, x, y, w, text, tone="red", size=10):
    D.text(x, y, w, 0.24, text, size=size, color=col_of(tone), face=M, align="c")
    D.line(x, y + 0.27, x + w, y + 0.27, RED_B if tone == "red" else NAVY_B, 0.75)


def kpi_box(D, x, y, w, h, num, unit, label, up=True, tone="red"):
    """Dashed evidence box: big number + unit, micro label, gradient up/down arrow."""
    col = col_of(tone)
    D.rect(x, y, w, h, fill=WHITE, line=col, lw=1, dash=DASH.DASH)
    D.text(x + 0.12, y + 0.03, w - 0.6, 0.32, [(num, {}), (" " + unit, {"size": FS_MICRO, "face": M})], size=14, color=col, face=H)
    D.text(x + 0.12, y + h - 0.24, w - 0.55, 0.2, label, size=FS_MICRO, color=GREY_M)
    a = D.rect(x + w - 0.4, y + (h - 0.34) / 2, 0.26, 0.34, fill=RED if up else NAVY,
               shape=MSO_SHAPE.UP_ARROW if up else MSO_SHAPE.DOWN_ARROW)
    grad(a, GRAD_RED if up else GRAD_NAVY, angle=90)


def spaced(t):
    out = ""
    for i, ch in enumerate(t):
        out += ch
        if i < len(t) - 1 and "一" <= ch <= "鿿" and "一" <= t[i + 1] <= "鿿":
            out += " "
    return out


def strip(D, left, lboxes, right, rboxes, mid=("相互影响", "相互影响"), licon="group", ricon="city", y=STRIP_Y):
    """Bottom framework strip: icon+label | 2 blue boxes | ⇄ | 2 pink boxes | label+icon."""
    D.line(EL, y - 0.2, ER, y - 0.2, "BFBFBF", 0.75)
    D.icon(licon, EL, y + 0.07, 0.36, color=NAVY)
    D.text(EL + 0.42, y, 0.9, 0.5, left, size=15, color=NAVY, face=M, anchor="m")
    for i, (a, b) in enumerate(lboxes[:2]):
        x = 1.9 + i * 2.02
        D.rect(x, y, 1.9, 0.5, fill="E6ECF5", line=NAVY_B, lw=0.5, dash=DASH.DASH)
        D.text(x, y, 1.9, 0.5, [spaced(a), spaced(b)], size=9.5, color=NAVY, face=M, align="c", anchor="m", spacing=0.95)
    D.line(6.05, y + 0.16, 7.35, y + 0.16, NAVY, 1, arrow=True)
    D.line(7.35, y + 0.34, 6.05, y + 0.34, RED, 1, arrow=True)
    D.text(6.0, y - 0.07, 1.4, 0.2, mid[0], size=8.5, color=GREY, align="c")
    D.text(6.0, y + 0.42, 1.4, 0.2, mid[1], size=8.5, color=GREY, align="c")
    for i, (a, b) in enumerate(rboxes[:2]):
        x = 7.45 + i * 2.02
        D.rect(x, y, 1.9, 0.5, fill="F9E9E6", line=RED_B, lw=0.5, dash=DASH.DASH)
        D.text(x, y, 1.9, 0.5, [spaced(a), spaced(b)], size=9.5, color=RED, face=M, align="c", anchor="m", spacing=0.95)
    D.text(ER - 1.32, y, 0.9, 0.5, right, size=15, color=RED, face=M, align="r", anchor="m")
    D.icon(ricon, ER - 0.36, y + 0.07, 0.36, color=RED)


def item_right_aligned(D, x_right, y, icon, title, desc, tone="navy", w=2.14):
    """Item leaning on a hero graphic from the left: right-aligned title + description, icon circle at x_right."""
    gcircle(D, x_right - 0.46, y, 0.46, tone, icon=icon, ring=1.5)
    D.text(x_right - 0.56 - w, y - 0.04, w, 0.3, title, size=FS_ITEM, color=col_of(tone), face=B, align="r")
    D.text(x_right - 0.56 - w, y + 0.26, w, 0.45, desc, size=FS_SMALL, color=GREY, align="r", spacing=1.1)


# ----------------------------------------------------------------------------- cards & badges
def gbar(D, x, y, w, h, text, tone="navy", size=13, align="c"):
    sh = D.rect(x, y, w, h, fill=col_of(tone))
    grad(sh, GRAD_NAVY if tone == "navy" else GRAD_RED, angle=0)
    if text:
        D.text(x + (0.15 if align == "l" else 0), y, w - (0.3 if align == "l" else 0), h, text, size=size,
               color=WHITE, face=M, align=align, anchor="m", hl={"face": H, "color": HILITE_DARK})
    return sh


def wcard(D, x, y, w, h, tone="navy", fill=WHITE, lw=0.75, sh=10):
    c = D.rect(x, y, w, h, fill=fill, line=NAVY_B if tone == "navy" else RED_B, lw=lw)
    shadow(c, opacity=sh, blur=6, dist=1.5)
    return c


def gcircle(D, x, y, d, tone="navy", icon=None, text=None, size=12, ring=2.0):
    c = D.rect(x, y, d, d, fill=NAVY, line=WHITE, lw=ring, shape=MSO_SHAPE.OVAL)
    grad(c, GRAD_RED if tone == "red" else GRAD_NAVY, angle=90)
    shadow(c, color=col_of(tone), opacity=28, blur=7, dist=2)
    if icon:
        k = d * 0.58
        D.icon(icon, x + (d - k) / 2, y + (d - k) / 2, k, color="FFFFFF")
    if text:
        D.text(x, y, d, d, text, size=size, color=WHITE, face=H, align="c", anchor="m")
    return c


def num_badge(D, x, y, d, text, tone="navy", size=8):
    return D.box_text(x, y, d, d, text, WHITE, col_of(tone), size, B, line=col_of(tone), lw=1, shape=MSO_SHAPE.OVAL)


def callout(D, bx, by, bw, bh, tipx, tipy, text, tone="red", size=11):
    """Rounded call-out whose tip lands exactly on (tipx, tipy)."""
    c = D.rect(bx, by, bw, bh, fill=RED if tone == "red" else WHITE, line=None if tone == "red" else NAVY, lw=1,
               shape=MSO_SHAPE.ROUNDED_RECTANGULAR_CALLOUT,
               adj=[(tipx - bx - bw / 2) / bw, (tipy - by - bh / 2) / bh, 0.16667])
    shadow(c, color=col_of(tone), opacity=22)
    D.text(0, 0, 0, 0, text, size=size, color=WHITE if tone == "red" else NAVY, face=M, align="c", anchor="m", shape=c,
           hl={"face": H, "size": size + 3})
    return c


def tab_card(D, x, y, w, h, num, title, metric=None, tone="navy"):
    """White card with a light gradient header band; metric = big number | 'icon:key' | 'pill:text'."""
    col = col_of(tone)
    card = D.rect(x, y, w, h, fill=WHITE, line=NAVY_B if tone == "navy" else RED_B, lw=0.75)
    shadow(card, opacity=10, blur=6, dist=1.5)
    band = D.rect(x, y, w, 0.38, fill=WHITE)
    grad(band, GRAD_TAB if tone == "navy" else GRAD_TAB_R, angle=0)
    D.text(x + 0.14, y, w - 1.2, 0.38, [(num + "  ", {"face": H, "color": col}), (title, {})], size=12, color=col, face=M, anchor="m")
    if metric and metric.startswith("icon:"):
        D.icon(metric[5:], x + w - 0.42, y + 0.05, 0.28, color=RED)
    elif metric and metric.startswith("pill:"):
        D.box_text(x + w - 1.02, y + 0.07, 0.9, 0.24, metric[5:], WHITE, RED, 9.5, M, line=RED_B,
                   shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.5)
    elif metric:
        D.text(x + w - 1.25, y, 1.12, 0.38, metric, size=14, color=RED, face=H, align="r", anchor="m")
    return card


def bullets(D, x, y, w, items, size=FS_BODY, color=GREY, gap=0.3, tone="navy"):
    for i, t in enumerate(items):
        yy = y + i * gap
        D.rect(x, yy + gap / 2 - 0.035, 0.07, 0.07, fill=col_of(tone))
        D.text(x + 0.16, yy, w - 0.16, gap, t, size=size, color=color, anchor="m")


def findings(D, x, y, w, h, items, top_pad=0.5, gap=0.12):
    """Stack of tab_cards: items = [{title, metric?, tone?, points[]}], heights shared equally."""
    n = len(items)
    ch = (h - gap * (n - 1)) / n
    for i, it in enumerate(items):
        yy = y + i * (ch + gap)
        tone = it.get("tone", "red" if i == 1 else "navy")
        tab_card(D, x, yy, w, ch, f"{i + 1:02d}", it["title"], it.get("metric"), tone)
        pts = it.get("points", [])
        g = min(0.36, (ch - top_pad - 0.08) / max(len(pts), 1))
        bullets(D, x + 0.18, yy + top_pad - 0.04, w - 0.3, pts, size=FS_BODY, gap=g, tone=tone)


def summary(D, x, y, w, h, text, label="核心结论", size=11.5):
    b = D.rect(x, y, w, h, fill=RED_T, line=RED_B, lw=0.75)
    grad(b, [(0, "F8E3DF", 100), (100, "FFFFFF", 100)], angle=0)
    shadow(b, color=RED, opacity=10, blur=5, dist=1.5)
    t = D.box_text(x + 0.18, y + (h - 0.34) / 2, 1.05, 0.34, label, RED, WHITE, 11, M, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.5)
    grad(t, GRAD_RED, angle=0)
    D.text(x + 1.4, y, w - 1.6, h, text, size=size, color=GREY, anchor="m", spacing=1.15, hl={"face": M, "color": NAVY})


def progress(D, x, y, w, frac, col=NAVY, track="DCE3EC", h=0.08):
    D.rect(x, y, w, h, fill=track, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.5)
    D.rect(x, y, max(w * frac, h), h, fill=col, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.5)


def legend(D, x, y, names, colors, step=0.95, round_=False):
    for i, (n, c) in enumerate(zip(names, colors)):
        if round_:
            D.rect(x + i * step, y + 0.06, 0.15, 0.15, fill=c, shape=MSO_SHAPE.OVAL)
        else:
            D.rect(x + i * step, y + 0.07, 0.22, 0.12, fill=c)
        D.text(x + i * step + 0.27, y, step - 0.3, 0.26, n, size=9.5, color=GREY, anchor="m")


def halo(D, cx, cy, r):
    h = D.rect(cx - r, cy - r, 2 * r, 2 * r, fill=NAVY_T, shape=MSO_SHAPE.OVAL)
    radial(h, [(0, "C9D7EA", 95), (70, "E4EBF5", 70), (100, "FFFFFF", 0)])
    return h
