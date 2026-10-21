# -*- coding: utf-8 -*-
"""Card-based data pages: KPI rings, dashboard (dual_charts moved to consult.py). Panels are reusable chart blocks."""
import math

from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.dml import MSO_LINE_DASH_STYLE as DASH
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Pt

from ..charts import *
from ..components import *
from ..deck import grad, shadow, rgb
from ..tokens import *

SERIES_COLORS = [NAVY, RED, NAVY_L, NAVY_M, RED_L]
SERIES_GRADS = {0: ("2E5A94", "16365F"), 1: ("C0503E", "8E2B1D")}


def nice_max(v, steps=5):
    """Axis max a little above v, on a 1/2/2.5/5 x 10^n grid -> (max, major unit)."""
    raw = v / steps
    mag = 10 ** math.floor(math.log10(raw))
    unit = next(m * mag for m in (1, 2, 2.5, 5, 10) if raw <= m * mag)
    return math.ceil(v * 1.08 / unit) * unit, unit


def frame(D, s):
    D.new(s["title"], s.get("section", ""), notes=s.get("speaker_notes"))


# =================================================================================== kpi_rings
def kpi_rings(D, s):
    """3–4 donut KPI cards, each with a before/after comparison, and a conclusion bar."""
    frame(D, s)
    rings = s["rings"][:4]
    cards_h = 4.35 if s.get("summary") else 5.4
    for (x, w), r in zip(cols(len(rings)), rings):
        tone = r.get("tone", "navy")
        col = col_of(tone)
        wcard(D, x, CARD_TOP, w, cards_h, tone)
        gbar(D, x, CARD_TOP, w, 0.45, r["label"], tone, 12)
        if r.get("icon"):
            gcircle(D, x + w - 0.55, 1.42, 0.44, tone, icon=r["icon"], ring=1.5)
        v = r["value"]
        cd = CategoryChartData(); cd.categories = ["占比", "其余"]; cd.add_series("s", (v, 100 - v))
        ch = D.chart(XL_CHART_TYPE.DOUGHNUT, cd, x + (w - 2.2) / 2, 1.72, 2.2, 2.2)
        chart_text(ch)
        pts = ch.plots[0].series[0].points
        pts[0].format.fill.solid(); pts[0].format.fill.fore_color.rgb = rgb(col)
        pts[1].format.fill.solid(); pts[1].format.fill.fore_color.rgb = rgb("E3E8EF" if tone == "navy" else "F3DEDA")
        for p_ in (0, 1):
            pts[p_].format.line.fill.background()
        hole(ch, 72)
        D.text(x, 2.5, w, 0.6, f"{v:g}%", size=28, color=col, face=H, align="c")
        if r.get("note"):
            D.text(x + 0.2, 3.98, w - 0.4, 0.3, r["note"], size=10.5, color=col, face=M, align="c")
        cmp_ = r.get("compare")
        if cmp_:
            D.line(x + 0.25, 4.38, x + w - 0.25, 4.38, NAVY_B, 0.5, DASH.DASH)
            for k, (lab, val) in enumerate(cmp_[:2]):
                yy = 4.52 + k * 0.4
                D.text(x + 0.25, yy - 0.06, 0.6, 0.24, lab, size=9.5, color=GREY_M, face=M)
                progress(D, x + 0.85, yy + 0.02, w - 1.57, val / 100, col if k == 1 else NAVY_L, h=0.1)
                D.text(x + w - 0.67, yy - 0.06, 0.55, 0.24, f"{val:g}%", size=9.5, color=col if k == 1 else GREY, face=B)
    if s.get("summary"):
        summary(D, EL, 5.72, CW, 0.82, s["summary"], label=s.get("summary_label", "核心结论"))


# =================================================================================== panels
def panel_chart(D, p, x, y, w, h, tone):
    """Draw one chart block (donut | bar | area | stacked_column | stacked_area) inside (x, y, w, h).
    Returns the plot geometry for overlays."""
    t = p["type"]
    cats = p["categories"]
    if t == "donut":
        cd = CategoryChartData(); cd.categories = cats; cd.add_series("占比", [v / 100 for v in p["values"]])
        d = min(h, w * 0.62)
        ch = D.chart(XL_CHART_TYPE.DOUGHNUT, cd, x, y, d, d)
        chart_text(ch); hole(ch, 62)
        colors = p.get("colors", [NAVY_L, NAVY, RED, NAVY_M, RED_L])
        for j, c in enumerate(colors[:len(cats)]):
            pt_ = ch.plots[0].series[0].points[j]
            pt_.format.fill.solid(); pt_.format.fill.fore_color.rgb = rgb(c)
            pt_.format.line.color.rgb = rgb(WHITE)
        if p.get("center"):
            D.text(x, y + d / 2 - 0.25, d, 0.4, p["center"][0], size=20, color=NAVY, face=H, align="c")
            D.text(x, y + d / 2 + 0.12, d, 0.25, p["center"][1], size=9, color=GREY_M, align="c")
        lx = x + d + 0.07
        step = min(0.5, d / len(cats))
        for j, (n, v) in enumerate(zip(cats, p["values"])):
            c = colors[j]
            yy = y + 0.25 + j * step
            D.rect(lx, yy + 0.07, 0.14, 0.14, fill=c)
            D.text(lx + 0.2, yy, x + w - lx - 0.2, 0.28, n, size=9.5, color=GREY)
            D.text(lx + 0.2, yy + 0.22, 0.9, 0.26, f"{v:g}%", size=11, color=c if c != NAVY_L else NAVY_M, face=H)
        return None
    if t == "bar":
        cd = CategoryChartData(); cd.categories = cats; cd.add_series(p.get("name", "值"), p["values"])
        ch = D.chart(XL_CHART_TYPE.BAR_CLUSTERED, cd, x, y, w, h)
        chart_text(ch)
        ser = ch.plots[0].series[0]
        ser_grad(ser, "16365F", "2E5A94", angle=0)
        for j in p.get("highlight", [0]):
            ser.points[j].format.fill.solid(); ser.points[j].format.fill.fore_color.rgb = rgb(RED)
        ch.plots[0].gap_width = 50
        ch.category_axis.reverse_order = True
        hide_val_axis(ch); ch.value_axis.maximum_scale = max(p["values"]) * 1.24; ch.value_axis.minimum_scale = 0
        axis_line(ch.category_axis)
        ser.data_labels.show_value = True; ser.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
        label_font(ser.data_labels, 10, NAVY, face=B)
        return None
    n = len(cats)
    series = p["series"] if "series" in p else {p.get("name", "值"): p["values"]}
    totals = [sum(v[i] for v in series.values()) for i in range(n)]
    cd = CategoryChartData(); cd.categories = cats
    for k, v in series.items():
        cd.add_series(k, v)
    kind = {"area": XL_CHART_TYPE.AREA, "stacked_area": XL_CHART_TYPE.AREA_STACKED,
            "stacked_column": XL_CHART_TYPE.COLUMN_STACKED}[t]
    ch = D.chart(kind, cd, x, y, w, h)
    chart_text(ch)
    lx, ty, lw_, th = (0.1, 0.03, 0.86, 0.86) if t == "stacked_column" else (0.08, 0.04, 0.88, 0.84)
    plot_layout(ch, lx, ty, lw_, th)
    sers = ch.plots[0].series
    for i, ser in enumerate(sers):
        fill_series(ser, SERIES_COLORS[i % len(SERIES_COLORS)])
        if i in SERIES_GRADS:
            ser_grad(ser, *SERIES_GRADS[i])
    vmax, unit = nice_max(max(totals))
    va = ch.value_axis
    va.maximum_scale = vmax; va.minimum_scale = 0; va.major_unit = unit
    if t == "area" and len(series) == 1:
        ser_grad(sers[0], "7C97BF", "EEF2F8")
        sers[0].format.line.color.rgb = rgb(NAVY); sers[0].format.line.width = Pt(2)
    if t == "stacked_column":
        ch.plots[0].gap_width = 55
        hide_val_axis(ch)
        for i, ser in enumerate(sers):
            ser.data_labels.show_value = True
            ser.data_labels.position = XL_LABEL_POSITION.CENTER
            label_font(ser.data_labels, 9.5, WHITE if i < 2 else NAVY_D, face=M)
            for j, v in enumerate(list(series.values())[i]):
                if v < vmax * 0.045:      # segment too thin for a label
                    hide_point_label(ser, j)
    else:
        gridlines(va); axis_line(va, show=False)
    axis_line(ch.category_axis)
    pl, pw, pt, ph = x + lx * w, lw_ * w, y + ty * h, th * h
    if t == "stacked_column":
        px = [pl + (i + 0.5) * pw / n for i in range(n)]
    else:
        px = [pl + pw * i / (n - 1) for i in range(n)]
    py = [pt + ph * (1 - tot / vmax) for tot in totals]
    return {"px": px, "py": py, "pl": pl, "pw": pw, "pt": pt, "ph": ph}


def panel_callout(D, geo, co, x, y, w):
    if not (geo and co):
        return
    i = co["at"]
    bw, bh = co.get("w", 1.75), 0.46
    tipx, tipy = geo["px"][i] - (0.25 if i == len(geo["px"]) - 1 else 0), geo["py"][i] + 0.02
    bx = min(max(x + 0.2, tipx - bw - 0.6), x + w - bw - 0.1) if co.get("side", "left") == "left" else tipx + 0.4
    callout(D, bx, y + 0.08, bw, bh, tipx, tipy, co["text"], size=10)


# =================================================================================== dashboard
def dashboard(D, s):
    """4 KPI tiles on top, 3 chart panels below, each panel closed by a one-line read-out."""
    frame(D, s)
    for (x, w), k in zip(cols(len(s["kpis"][:4])), s["kpis"][:4]):
        tone = k.get("tone", "navy")
        col = col_of(tone)
        wcard(D, x, 1.2, w, 1.4, tone)
        gcircle(D, x + 0.18, 1.38, 0.66, tone, icon=k.get("icon", "trend"))
        D.text(x + 1.0, 1.27, 1.2, 0.28, k["label"], size=11, color=GREY, face=M)
        if k.get("growth"):
            D.box_text(x + w - 0.85, 1.3, 0.7, 0.26, k["growth"], RED, WHITE, 9.5, B, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.5)
        D.text(x + 1.0, 1.52, w - 1.05, 0.55, [(k["value"], {}), (" " + k.get("unit", ""), {"size": 10.5, "face": M, "color": GREY})],
               size=26, color=col, face=H)
        if k.get("share") is not None:
            progress(D, x + 0.2, 2.25, 1.55, k["share"], col, h=0.09)
        if k.get("caption"):
            D.text(x + 1.85, 2.15, w - 1.9, 0.28, k["caption"], size=9, color=GREY_M)
    for (x, w), p in zip(cols(3, 0.22), s["panels"][:3]):
        tone = p.get("tone", "navy")
        wcard(D, x, 2.8, w, 3.75, tone)
        gbar(D, x, 2.8, w, 0.42, p["title"], tone, 12.5)
        geo = panel_chart(D, p, x + 0.1, 3.3, w - 0.2, 2.65 if p["type"] != "area" else 2.65, tone)
        panel_callout(D, geo, p.get("callout"), x, 3.25, w)
        if p.get("note"):
            D.text(x + 0.15, 5.95, w - 0.3, 0.5, p["note"], size=10, color=GREY, anchor="m", hl={"face": H, "color": RED, "size": 13})


LAYOUTS = {"kpi_rings": kpi_rings, "dashboard": dashboard}
