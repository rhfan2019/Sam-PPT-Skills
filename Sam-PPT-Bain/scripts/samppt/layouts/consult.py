# -*- coding: utf-8 -*-
"""Consulting archetypes modelled on template slide 10:
thesis banner -> zone labels -> hero graphic with two wings -> evidence -> framework strip."""
import math

from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.dml import MSO_LINE_DASH_STYLE as DASH
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Pt

from ..charts import *
from ..components import *
from ..deck import grad, alpha, shadow, rgb
from ..tokens import *


def frame(D, s):
    """Title frame + banner + zone labels shared by every consulting layout."""
    D.new(s["title"], s.get("section", ""), notes=s.get("speaker_notes"))
    if s.get("thesis"):
        banner(D, s["thesis"])


def do_strip(D, st):
    if st:
        strip(D, st["left"], st["left_boxes"], st["right"], st["right_boxes"], tuple(st.get("mid", ["相互影响", "相互影响"])),
              st.get("left_icon", "group"), st.get("right_icon", "city"))


def evidence(D, x, y, w, spec):
    """Small evidence module under a wing. Types: kpis | split_bar | bars."""
    if not spec:
        return
    t = spec.get("type", "kpis")
    if spec.get("title"):
        module_head(D, x, y, w, spec["title"], spec.get("tone", "red"))
        y += 0.35
    if t == "kpis":
        n = len(spec["items"])
        kw = (w - 0.1 * (n - 1)) / n
        for i, k in enumerate(spec["items"]):
            kpi_box(D, x + i * (kw + 0.1), y, kw, 0.58, k["value"], k.get("unit", ""), k["label"], k.get("up", True),
                    k.get("tone", "red"))
    elif t == "split_bar":
        x0 = x
        tot = sum(p["value"] for p in spec["parts"])
        for i, p in enumerate(spec["parts"]):
            pw = w * p["value"] / tot
            b = D.rect(x0, y, pw, 0.26, fill=NAVY if i == 0 else RED)
            grad(b, GRAD_NAVY if i == 0 else GRAD_RED, angle=0)
            D.text(x0 + 0.08, y, pw - 0.1, 0.26, f'{p["label"]} {p["value"]:g}%', size=9, color=WHITE, face=M, anchor="m")
            if p.get("note"):
                D.text(x0, y + 0.28, pw, 0.2, p["note"], size=8.5, color=NAVY if i == 0 else RED, face=M)
            x0 += pw
    elif t == "bars":
        rows = spec["rows"]
        mx = max(r["value"] for r in rows)
        lw = 0.98
        bw = w - lw - 0.45
        step = min(0.105, 0.42 / len(rows))
        for k, r in enumerate(rows):
            yy = y - 0.03 + k * step
            c = {"red": RED, "navy": NAVY, "mid": NAVY_M}[r.get("tone", "navy")]
            D.text(x, yy - 0.04, lw - 0.05, 0.18, r["label"], size=7.5, color=GREY, align="r")
            D.rect(x + lw, yy, max(bw * r["value"] / mx, 0.06), 0.09, fill=c)
            D.text(x + lw + bw * r["value"] / mx + 0.04, yy - 0.05, 0.4, 0.18, f'{r["value"]:g}', size=7.5, color=c, face=B)


# =================================================================================== chart_phases
def chart_phases(D, s):
    """Column + line (secondary) chart split into phases on the left, phase diagnosis chain on the right."""
    frame(D, s)
    z = s.get("zones", ["", ""])
    zone(D, EL, z[0], "navy", w=2.4)
    zone(D, 7.95, z[1], "red", w=2.1)
    cats = s["categories"]
    bars, line = s["bars"], s.get("line")
    n = len(cats)
    cx_, cy_, cw_, chh = EL, 2.15, 7.38, 3.45
    lx, ty, lw_, th = 0.02, 0.06, 0.96, 0.84
    pl, pw, pt, ph = cx_ + lx * cw_, lw_ * cw_, cy_ + ty * chh, th * chh
    step = pw / n
    ccx = [pl + (i + 0.5) * step for i in range(n)]
    tints = {"navy": ("F3F6FA", "EAF0F7"), "red": ("FBEDEA", "FBEDEA")}
    for k, p in enumerate(s.get("phases", [])):
        a, b = p["from"], p["to"] + 1
        tone = p.get("tone", "navy")
        D.rect(pl + a * step + 0.03, pt - 0.02, (b - a) * step - 0.06, ph + 0.02, fill=tints[tone][k % 2])
        D.text(pl + a * step, 2.08, (b - a) * step, 0.24, p["name"], size=10, color=RED if tone == "red" else NAVY_M, face=M, align="c")
    if line:
        vmax = max(line["values"]) * 1.11
        vmin = -vmax * 0.25
        yof = lambda v: pt + ph * (1 - (v - vmin) / (vmax - vmin))
        if line.get("ref") is not None:
            yr = yof(line["ref"])
            D.line(pl, yr, pl + pw, yr, RED, 1, DASH.DASH)
            D.text(pl + 0.05, yr - 0.22, 1.6, 0.2, line.get("ref_label", ""), size=8.5, color=RED, face=M)
    cd = CategoryChartData(); cd.categories = cats
    cd.add_series(bars["name"], bars["values"])
    if line:
        cd.add_series(line["name"], line["values"])
    ch = D.chart(XL_CHART_TYPE.COLUMN_CLUSTERED, cd, cx_, cy_, cw_, chh)
    chart_text(ch, 9)
    plot_layout(ch, lx, ty, lw_, th)
    ch.plots[0].gap_width = 60
    s0 = ch.plots[0].series[0]
    ser_grad(s0, "2E5A94", "16365F")
    bmax = max(bars["values"])
    ch.value_axis.maximum_scale = bmax * 1.15; ch.value_axis.minimum_scale = 0
    hide_val_axis(ch); axis_line(ch.category_axis)
    s0.data_labels.show_value = True; s0.data_labels.position = XL_LABEL_POSITION.INSIDE_END
    label_font(s0.data_labels, 9, WHITE, face=M)
    for j, v in enumerate(bars["values"]):
        if v < bmax * 0.15:        # too short for an inside label
            pdl = s0.points[j].data_label; pdl.position = XL_LABEL_POSITION.OUTSIDE_END; label_font(pdl, 9, NAVY, face=M)
    co = s.get("callout")
    if line:
        line_to_secondary(ch, 1, RED, vmin=round(vmin, 2), vmax=round(vmax, 2), fmt=line.get("format", '0.0"%"'),
                          below=[co["at"]] if co else [])
    if co:
        i = co["at"]
        tipy = yof(line["values"][i]) if line else pt + ph * (1 - bars["values"][i] / (bmax * 1.15))
        callout(D, ccx[max(i - 1, 0)] - 0.75, pt + 0.62, 1.4, 0.4, ccx[i] - 0.08, tipy, co["text"], size=9)
    gr = s.get("growth", "auto")
    if gr:
        vals = bars["values"]
        if gr == "auto":
            gr = ["—"] + [f"{(vals[i] / vals[i - 1] - 1) * 100:+.0f}%" for i in range(1, n)]
        gy = cy_ + chh + 0.02
        for i, t in enumerate(gr):
            hot = t.startswith("+") and float(t[1:-1]) >= s.get("growth_hot", 50)
            outline_pill(D, ccx[i] - 0.32, gy, 0.64, t, "red" if hot else "navy", h=0.24, size=9, filled=hot)
        if s.get("note"):
            D.text(EL, gy + 0.3, 7.3, 0.22, s["note"], size=8.5, color=GREY_M)
    # right wing: phase chain
    rx = 8.05
    phases = s.get("phases", [])[:3]
    for k, p in enumerate(phases):
        y = 2.2 + k * 1.02
        tone = p.get("tone", "navy")
        gcircle(D, rx, y, 0.5, tone, icon=p.get("icon", "trend"), ring=1.5)
        D.text(rx + 0.62, y - 0.01, 1.0, 0.32, p["name"], size=14, color=col_of(tone), face=B, anchor="m")
        D.text(rx + 1.45, y - 0.01, 1.2, 0.32, p.get("years", ""), size=9, color=GREY_M, anchor="m")
        if p.get("tag"):
            arrow_r(D, ER - 1.25 - 0.4, y + 0.06, tone)
            tag(D, ER - 1.25, y - 0.01, 1.25, p["tag"], tone, h=0.32, size=11)
        D.text(rx + 0.62, y + 0.34, ER - rx - 0.62, 0.5, p.get("points", []), size=FS_SMALL, color=GREY, spacing=1.1)
        if k < len(phases) - 1:
            curved_arrow(D, rx - 0.33, y + 0.4, 0.7)
    if s.get("kpis"):
        evidence(D, 7.95, 5.32, ER - 7.95, {"type": "kpis", "items": s["kpis"]})
    do_strip(D, s.get("strip"))


def short(stage):
    return stage.get("short", stage["name"] if len(stage["name"]) <= 2 else stage["name"][-2:])


# =================================================================================== funnel
def funnel(D, s):
    """Faceted funnel in the middle; stage definitions on the left wing; conversion diagnosis on the right."""
    frame(D, s)
    z = s.get("zones", ["", ""])
    zone(D, EL, z[0], "navy", w=2.1)
    zone(D, 7.15, z[1], "red", w=2.1)
    st = s["stages"][:5]
    n = len(st)
    vals = [x["value"] for x in st]
    conv = [vals[i + 1] / vals[i] for i in range(n - 1)]
    hot_t = conv.index(min(conv))                 # weakest transition
    hot = s.get("hot_stage", hot_t + 1)
    cx, top = 5.25, 2.12
    lh = min(0.72, (3.95 - 0.07 * (n - 1)) / n)
    g = 0.07
    widths = [3.2 - k * (2.78 / n) for k in range(n + 1)]
    shades = [("16365F", "2E5A94"), ("244C82", "4A6FA5"), ("3E68A3", "7C97BF"), ("6E8FC0", "A9BEDC"), ("8FA8CB", "C3D2E6")]
    nv = 0
    for i, x in enumerate(st):
        y0, y1 = top + i * (lh + g), top + i * (lh + g) + lh
        tw, bw = widths[i], widths[i + 1]
        if i == hot:
            dark, light = "8E2B1D", "C0503E"
        else:
            dark, light = shades[min(nv, 4)]; nv += 1
        D.poly([(cx - tw / 2, y0), (cx, y0), (cx, y1), (cx - bw / 2, y1)], dark, [(0, dark, 100), (100, light, 100)], angle=0)
        D.poly([(cx, y0), (cx + tw / 2, y0), (cx + bw / 2, y1), (cx, y1)], light,
               [(0, light, 100), (100, "E3A79D" if i == hot else "D3DEEE", 100)], angle=0)
        small = tw < 1.7
        dark_txt = i >= n - 1 and i != hot
        D.text(cx - tw / 2, y0, tw / 2 - 0.05, lh, x["name"], size=9.5 if small else 11, color=NAVY_D if dark_txt else WHITE,
               face=M, align="r", anchor="m")
        D.text(cx + 0.06, y0, tw / 2, lh, f'{x["value"]:g}%', size=11 if small else 15, color=NAVY_D if dark_txt else WHITE, face=H, anchor="m")
        ym = (y0 + y1) / 2
        tone = "red" if i == hot else "navy"
        item_right_aligned(D, 3.45, ym - 0.24, x.get("icon", "target"), f'{x["name"]}  {x["value"]:g}%', x.get("desc", ""), tone)
        dot_line(D, 3.48, ym - 0.01, cx - (tw + bw) / 4 - 0.04, ym - 0.01, RED if i == hot else NAVY_B)
    rx = 7.15
    notes = s.get("transition_notes", [""] * (n - 1))
    for k in range(n - 1):
        ym = top + (k + 1) * (lh + g) + lh / 2
        h_ = k == hot_t
        tone = "red" if h_ else "navy"
        gcircle(D, rx, ym - 0.3, 0.5, tone, text=f"{conv[k] * 100:.0f}%", size=11, ring=1.5)
        D.text(rx + 0.62, ym - 0.33, 1.6, 0.3, f'{short(st[k])} → {short(st[k + 1])}', size=FS_ITEM, color=col_of(tone), face=B, anchor="m")
        arrow_r(D, rx + 1.85, ym - 0.27, tone)
        tag(D, rx + 2.2, ym - 0.33, 0.95, "最大断点" if h_ else f"流失 {(1 - conv[k]) * 100:.0f}%", tone, h=0.3, size=10)
        D.text(rx + 0.62, ym, 2.6, 0.26, notes[k] if k < len(notes) else "", size=FS_SMALL, color=GREY)
        if k < n - 2:
            curved_arrow(D, rx - 0.32, ym - 0.05, 0.75)
    if s.get("start_note"):
        D.text(rx + 0.62, top + 0.14, 2.8, 0.45, s["start_note"], size=FS_SMALL, color=GREY_M, spacing=1.1)
    ex, ew = 10.6, ER - 10.6
    kp = s.get("kpis", [])
    if kp:
        module_head(D, ex, 2.1, ew, s.get("kpi_title", "关键指标"))
        for i, k in enumerate(kp[:3]):
            kpi_box(D, ex, 2.5 + i * 0.62, ew, 0.55, k["value"], k.get("unit", ""), k["label"], k.get("up", True), k.get("tone", "red"))
        y_hot = top + (hot_t + 1) * (lh + g) + lh / 2
        dot_line(D, rx + 3.18, y_hot - 0.18, ex - 0.02, 2.5 + 0.62 + 0.28, RED, dot_start=True)
    mc = s.get("mini_chart")
    if mc:
        module_head(D, ex, 4.45, ew, mc.get("title", "每 100 人剩余人数"))
        cd = CategoryChartData(); cd.categories = [short(x) for x in st]
        cd.add_series("剩余", vals)
        ch = D.chart(XL_CHART_TYPE.AREA, cd, ex, 4.75, ew, 1.25)
        chart_text(ch, 8)
        ser_grad(ch.plots[0].series[0], "2E5A94", "D3DEEE")
        ch.value_axis.maximum_scale = max(vals) * 1.2; ch.value_axis.minimum_scale = 0
        gridlines(ch.value_axis); axis_line(ch.value_axis, show=False); axis_line(ch.category_axis)
        if mc.get("label"):
            D.box_text(ex + 0.95, 4.82, 1.15, 0.22, mc["label"], NAVY, WHITE, 8, M, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.3)
    if s.get("axis_label"):
        D.line(EL + 0.15, 2.15, EL + 0.15, 5.9, NAVY, 1, arrow=True)
        D.rect(EL, 3.0, 0.3, 2.0, fill=WHITE)
        D.text(EL, 3.0, 0.3, 2.0, s["axis_label"], size=10.5, color=NAVY, face=M, align="c", anchor="m", vert=True)
    do_strip(D, s.get("strip"))


# =================================================================================== hub
def hub(D, s):
    """Centre node ringed by 4–6 satellites; satellites described in open (card-less) items on both wings."""
    frame(D, s)
    z = s.get("zones", ["", ""])
    zone(D, EL, z[0], "navy", w=2.0)
    zone(D, ER - 2.0, z[1], "red", w=2.0)
    cx0, cy0 = 6.665, 3.85
    if s.get("background"):
        D.photo(s["background"], 4.2, 4.0, 4.93, 2.0, opacity=50, feather=0.2)
    halo(D, cx0, cy0, 2.05)
    D.rect(cx0 - 1.5, cy0 - 1.5, 3.0, 3.0, line=NAVY_B, lw=1, shape=MSO_SHAPE.OVAL, dash=DASH.DASH)
    alpha(D.rect(cx0 - 1.0, cy0 - 1.0, 2.0, 2.0, fill=NAVY_L, shape=MSO_SHAPE.OVAL), 35)
    core = D.rect(cx0 - 0.72, cy0 - 0.72, 1.44, 1.44, fill=NAVY, line=WHITE, lw=3, shape=MSO_SHAPE.OVAL)
    grad(core, GRAD_NAVY, angle=90); shadow(core, opacity=35, blur=12, dist=4)
    c1, c2 = (s.get("center", ["", ""]) + [""])[:2]
    D.text(cx0 - 0.72, cy0 - 0.33, 1.44, 0.38, c1, size=15, color=WHITE, face=H, align="c")
    D.text(cx0 - 0.72, cy0 + 0.06, 1.44, 0.26, c2, size=9, color=ON_DARK, align="c")
    if s.get("hero_photo", "car3d"):
        D.photo_fit(s.get("hero_photo", "car3d"), cx0 - 0.75, cy0 + 0.9, 1.5)
    nodes = s["nodes"][:6]
    half = (len(nodes) + 1) // 2
    sides = [nodes[:half], nodes[half:]]
    ang = {3: ([150, 180, 210], [30, 0, 330]), 2: ([160, 200], [20, 340]), 1: ([180], [0])}
    k = 0
    for side, items in enumerate(sides):
        angles = ang[len(items)][side] if items else []
        for row, (nd, a) in enumerate(zip(items, angles)):
            k += 1
            num = f"{k:02d}"
            tone = nd.get("tone", "navy")
            col = col_of(tone)
            r = math.radians(a)
            nx, ny = cx0 + 1.5 * math.cos(r), cy0 - 1.5 * math.sin(r)
            gcircle(D, nx - 0.34, ny - 0.34, 0.68, tone, icon=nd.get("icon", "cube"), ring=2.5)
            num_badge(D, nx + 0.12, ny - 0.42, 0.28, num, tone)
            y = 2.3 + row * 1.03
            m = nd.get("metric", "")
            msz = 15 if len(m) < 5 else 12.5
            if side == 0:
                D.text(EL, y - 0.02, 2.4, 0.36, [(num + " ", {"face": H}), (nd["name"], {})], size=13.5, color=col, face=B, anchor="m")
                D.text(2.6, y - 0.02, 1.25, 0.36, m, size=msz, color=RED, face=H, align="r", anchor="m")
                D.line(EL, y + 0.38, 3.85, y + 0.38, NAVY_B, 0.5)
                tag(D, EL, y + 0.48, 0.95, nd.get("group", ""), tone, h=0.26, size=9.5)
                D.text(EL + 1.07, y + 0.48, 2.4, 0.26, nd.get("desc", ""), size=FS_SMALL, color=GREY, anchor="m")
                dot_line(D, 3.9, y + 0.38, nx - 0.36, ny, col if tone == "red" else NAVY_B, dot_start=True)
            else:
                D.text(9.45, y - 0.02, 2.4, 0.36, [(num + " ", {"face": H}), (nd["name"], {})], size=13.5, color=col, face=B, anchor="m")
                D.text(ER - 1.3, y - 0.02, 1.3, 0.36, m, size=msz, color=RED, face=H, align="r", anchor="m")
                D.line(9.45, y + 0.38, ER, y + 0.38, RED_B if tone == "red" else NAVY_B, 0.5)
                tag(D, 9.45, y + 0.48, 0.95, nd.get("group", ""), tone, h=0.26, size=9.5)
                D.text(9.45 + 1.07, y + 0.48, 2.4, 0.26, nd.get("desc", ""), size=FS_SMALL, color=GREY, anchor="m")
                dot_line(D, 9.4, y + 0.38, nx + 0.36, ny, col if tone == "red" else NAVY_B, dot_start=True)
    evidence(D, EL, 5.25, 3.85 - EL, s.get("evidence_left"))
    evidence(D, 9.45, 5.25, ER - 9.45, s.get("evidence_right"))
    do_strip(D, s.get("strip"))


def caption(D, x, y, w, text, align="l"):
    """Micro method / source note that belongs to the module right above it (never a page-wide '注' line:
    it competes with the footer disclaimer)."""
    if text:
        D.text(x, y, w, 0.2, text, size=8, color=GREY_M, align=align, anchor="m")


def mini_bars(D, x, y, w, rows, step=0.3, lw=0.9, unit=""):
    """Labelled horizontal bars for evidence modules: rows = [{label, value, tone: navy|red|mid}]."""
    mx = max(r["value"] for r in rows)
    bw = w - lw - 0.5
    for k, r in enumerate(rows):
        yy = y + k * step
        c = {"red": RED, "navy": NAVY, "mid": NAVY_L}[r.get("tone", "navy")]
        D.text(x, yy, lw - 0.08, 0.22, r["label"], size=9, color=GREY, align="r", anchor="m")
        b = D.rect(x + lw, yy + 0.04, max(bw * r["value"] / mx, 0.06), 0.14, fill=c)
        if r.get("tone", "navy") != "mid":
            grad(b, GRAD_NAVY if c == NAVY else GRAD_RED, angle=0)
        D.text(x + lw + bw * r["value"] / mx + 0.06, yy, 0.42, 0.22, f'{r["value"]:g}{unit}', size=9.5,
               color=NAVY_M if c == NAVY_L else c, face=B, anchor="m")


# =================================================================================== dual_charts
SER_COLS = [NAVY, RED, NAVY_L, NAVY_M]
SER_GRADS = {0: ("2E5A94", "16365F"), 1: ("C0503E", "8E2B1D"), 2: ("C3D2E6", "9DB3D1")}


def _ser_outline(ser, color=WHITE, width=0.75):
    ser.format.line.color.rgb = rgb(color)
    ser.format.line.width = Pt(width)


def _stack_chart(D, p, x, y, w, h, plot):
    """Stacked column / stacked area without legend: series are labelled directly at the right end.
    Returns plot geometry (category x, stack tops, segment mid-points of the last category)."""
    from .cards import nice_max
    cats, series = p["categories"], p["series"]
    n = len(cats)
    names = list(series)
    totals = [sum(v[i] for v in series.values()) for i in range(n)]
    cd = CategoryChartData(); cd.categories = cats
    for k, v in series.items():
        cd.add_series(k, v)
    col = p["type"] == "stacked_column"
    ch = D.chart(XL_CHART_TYPE.COLUMN_STACKED if col else XL_CHART_TYPE.AREA_STACKED, cd, x, y, w, h)
    chart_text(ch, 9 if col else 8.5)
    lx, ty, lw_, th = plot
    plot_layout(ch, lx, ty, lw_, th)
    for i, ser in enumerate(ch.plots[0].series):
        fill_series(ser, SER_COLS[i % 4])
        if i in SER_GRADS:
            ser_grad(ser, *SER_GRADS[i])
        _ser_outline(ser, WHITE, 0.75 if col else 1.25)     # crisp white seams between stacked segments / bands
    vmax, unit = nice_max(max(totals))
    va = ch.value_axis
    va.maximum_scale = vmax; va.minimum_scale = 0; va.major_unit = unit
    if col:
        ch.plots[0].gap_width = 65
        series_lines(ch)
        hide_val_axis(ch)
        for i, ser in enumerate(ch.plots[0].series):
            ser.data_labels.show_value = True
            ser.data_labels.position = XL_LABEL_POSITION.CENTER
            label_font(ser.data_labels, 9, WHITE if i < 2 else NAVY_D, face=M)
            for j, v in enumerate(series[names[i]]):
                if v < vmax * 0.045:
                    hide_point_label(ser, j)
    else:
        gridlines(va, "E9EDF3"); axis_line(va, show=False)
    axis_line(ch.category_axis)
    pl, pw, pt, ph = x + lx * w, lw_ * w, y + ty * h, th * h
    px = [pl + (i + 0.5) * pw / n for i in range(n)] if col else [pl + pw * i / (n - 1) for i in range(n)]
    yof = lambda v: pt + ph * (1 - v / vmax)
    cum, mids = 0, []
    for k in names:
        v = series[k][-1]
        mids.append(yof(cum + v / 2)); cum += v
    return {"px": px, "py": [yof(t) for t in totals], "mids": mids, "names": names, "step": pw / n,
            "bw": pw / n / 1.65, "pt": pt, "ph": ph}


def _end_labels(D, x, mids, names, tags=None, w=1.0):
    """Series names written next to the last data point, in series colour; optional pill (growth, share)."""
    ys = list(mids)
    for k in range(1, len(ys)):           # keep labels at least one line apart
        ys[k] = min(ys[k], ys[k - 1] - 0.3)
    for k, (yy, n) in enumerate(zip(ys, names)):
        c = SER_COLS[k % 4]
        c = NAVY_M if c == NAVY_L else c
        D.rect(x, yy - 0.04, 0.08, 0.08, fill=c, shape=MSO_SHAPE.OVAL)
        D.text(x + 0.12, yy - 0.12, 0.5, 0.24, n, size=10, color=c, face=B, anchor="m")
        if tags:
            outline_pill(D, x + w - 0.5, yy - 0.12, 0.5, tags[k], "red" if k else "navy", h=0.24, size=9)


def dual_charts(D, s):
    """Three equal columns split by hairline dividers: annual structure (stacked columns + series lines +
    share pills) | monthly trend (stacked area, direct labels + growth pills) | evidence (growth KPIs, split
    of the increment). Each column carries its own micro caption on one shared baseline."""
    frame(D, s)
    z = s.get("zones", ["", "", ""])
    L, Rp = s["left"], s["right"]
    (c1, w), (c2, _), (c3, _) = cols(3, 0.4)
    top, bot, cap_y = 2.12, 6.5, 6.3
    for xd in (c1 + w + 0.2, c2 + w + 0.2):
        D.line(xd, top, xd, bot, GREY_L, 0.75)
    for x, t, tone in ((c1, z[0], "navy"), (c2, z[1], "navy"), (c3, z[2] if len(z) > 2 else "", "red")):
        zone(D, x, t, tone, w=w)
    cy, chh = 2.5, 3.42
    for x, p in ((c1, L), (c2, Rp)):
        D.text(x, top, w, 0.26, p["title"], size=10, color=NAVY, face=M, anchor="m")
    # column 1: annual stacked columns, latest year on a tinted band
    lab_w = 0.68
    plot = (0.0, 0.08, (w - lab_w) / w, 0.84)
    pl, pw = c1, w - lab_w
    n = len(L["categories"])
    st = pw / n
    D.rect(pl + (n - 1) * st + 0.02, cy + 0.02, st - 0.04, chh + 0.34, fill="FBEFEC")
    g = _stack_chart(D, L, c1, cy, w, chh, plot)
    _end_labels(D, pl + pw + 0.04, g["mids"], g["names"])
    co = L.get("callout")
    if co:
        i = co["at"]
        callout(D, g["px"][i] - 2.55, cy + 0.06, 1.65, 0.4, g["px"][i] - g["bw"] / 2 + 0.04, g["py"][i] + 0.04, co["text"], size=10)
    row = L.get("pill_row")
    if row:
        gy = cy + chh + 0.06
        pw_ = min(0.6, st - 0.08)
        for i, v in enumerate(row["values"]):
            hot = v >= row.get("hot", 1e9)
            outline_pill(D, g["px"][i] - pw_ / 2, gy, pw_, f'{v:g}{row.get("suffix", "")}', "red", h=0.26, size=9.5, filled=hot)
        D.text(pl + pw + 0.04, gy, lab_w, 0.26, row["label"], size=9, color=RED, face=M, anchor="m")
    caption(D, c1, cap_y, w, L.get("caption"))
    # column 2: monthly stacked area, last month marked
    tag_w = 1.22
    plot = (0.1, 0.08, (w - tag_w) / w - 0.1, 0.84)
    g2 = _stack_chart(D, Rp, c2, cy, w, chh, plot)
    xl = g2["px"][-1]
    D.line(xl, g2["pt"] - 0.05, xl, g2["pt"] + g2["ph"], RED, 0.75, DASH.DASH)
    _end_labels(D, xl + 0.08, g2["mids"], g2["names"], Rp.get("end_tags"), w=c2 + w - xl - 0.08)
    co = Rp.get("callout")
    if co:
        i = co["at"]
        callout(D, g2["px"][i] - 2.3, cy + 0.06, 1.8, 0.4, g2["px"][i] - 0.05, g2["py"][i] + 0.02, co["text"], size=10)
    caption(D, c2, cap_y, w, Rp.get("caption"))
    # column 3: evidence
    ev = s.get("evidence", {})
    y = top
    if ev.get("kpis"):
        module_head(D, c3, y, w, ev.get("kpi_title", "关键指标"))
        for k, kp in enumerate(ev["kpis"][:3]):
            kpi_box(D, c3, y + 0.42 + k * 0.68, w, 0.6, kp["value"], kp.get("unit", ""), kp["label"], kp.get("up", True),
                    kp.get("tone", "red"))
        y += 0.42 + 3 * 0.68 + 0.2
    sp = ev.get("split")
    if sp:
        module_head(D, c3, y, w, sp["title"], "red")
        y += 0.44
        x0, tot = c3, sum(pt_["value"] for pt_ in sp["parts"])
        for i, pt_ in enumerate(sp["parts"]):
            pw_ = w * pt_["value"] / tot
            b = D.rect(x0, y, pw_, 0.32, fill=NAVY if i == 0 else RED)
            grad(b, GRAD_NAVY if i == 0 else GRAD_RED, angle=0)
            D.text(x0 + 0.1, y, pw_ - 0.2, 0.32, f'{pt_["label"]} {pt_["value"]:g}%', size=9.5, color=WHITE, face=M, anchor="m")
            if pt_.get("note"):
                D.text(x0 + 0.02, y + 0.36, pw_ - 0.04, 0.22, pt_["note"], size=9, color=NAVY if i == 0 else RED, face=M, anchor="m")
            x0 += pw_
        if sp.get("caption"):
            D.text(c3, y + 0.68, w, 0.3, sp["caption"], size=10.5, color=GREY, anchor="m", hl={"face": B, "color": RED})
    caption(D, c3, cap_y, w, ev.get("caption"))


# =================================================================================== versus
def versus(D, s):
    """Three-column grid: wing | metric duel | wing. Each of the 5 rows lines up one strength / weakness of each
    side with the metric that proves it (item `ref` = row number), so the eye reads row by row.
    Framework strip closes the page."""
    frame(D, s)
    sides = s["sides"][:2]
    m = s["metrics"]
    rows = m["rows"][:5]
    nr = len(rows)
    better = [((r["a"] < r["b"]) if r.get("better", "low") == "low" else (r["a"] > r["b"])) for r in rows]
    wins = [sum(better), nr - sum(better)]
    ww, gap = 3.85, 0.3
    c0, c1 = EL + ww + gap, ER - ww - gap
    cx = (EL + ER) / 2
    z = s.get("zones") or [sd.get("claim", "") for sd in sides]
    zone(D, EL, z[0], "navy", w=ww)
    zone(D, ER - ww, z[1], "red", w=ww)
    gcircle(D, cx - 0.32, ZONE_Y + ZONE_H / 2 - 0.32, 0.64, "red", text="VS", size=15, ring=2.5)
    # column headers, each closed by a heavy rule in its own colour
    hy, hh = 2.16, 0.56
    for i, sd in enumerate(sides):
        tone = sd.get("tone", "navy" if i == 0 else "red")
        col = col_of(tone)
        left = i == 0
        x0 = EL if left else ER - ww
        gcircle(D, x0 if left else ER - 0.5, hy + 0.03, 0.5, tone, icon=sd.get("icon", "battery"), ring=1.5)
        D.text(x0 + (0.62 if left else 1.1), hy, ww - 1.72, hh, sd["name"], size=16, color=col, face=H,
               align="l" if left else "r", anchor="m")
        outline_pill(D, x0 + ww - 1.0 if left else x0, hy + 0.14, 1.0, f"{wins[i]} 项占优", tone, h=0.28, size=9.5,
                     filled=wins[i] > wins[1 - i])
        D.line(x0, hy + hh + 0.06, x0 + ww, hy + hh + 0.06, col, 1.5)
    D.text(c0, hy, c1 - c0, hh, [("◀ " + m.get("left", "纯电") + "    ", {"color": NAVY}), (m["title"], {"color": GREY}),
                                 ("    " + m.get("right", "混动") + " ▶", {"color": RED})], size=11, face=M, align="c", anchor="m")
    D.line(c0, hy + hh + 0.06, c1, hy + hh + 0.06, GREY_M, 1.5)
    # row grid
    top, pitch, chh = hy + hh + 0.18, 0.6, 0.54
    tints = ("F1F5FA", "F6F7F9", "FBF2F0")
    for j in range(nr):
        y = top + j * pitch
        for x, w_, t in ((EL, ww, tints[0]), (c0, c1 - c0, tints[1]), (ER - ww, ww, tints[2])):
            D.rect(x, y, w_, chh, fill=t)
    # wing items placed on the row of the metric they refer to
    for i, sd in enumerate(sides):
        tone = sd.get("tone", "navy" if i == 0 else "red")
        left = i == 0
        x0 = EL if left else ER - ww
        slots, free = {}, []
        items = [(it if isinstance(it, dict) else {"text": it}, k) for k, lst in enumerate((sd.get("pros", []), sd.get("cons", [])))
                 for it in lst[:2]]
        for it, k in items:
            r = it.get("ref")
            if r and 1 <= r <= nr and r - 1 not in slots:
                slots[r - 1] = (it, k)
            else:
                free.append((it, k))
        for it_k in free:
            j = next(j for j in range(nr) if j not in slots)
            slots[j] = it_k
        for j, (it, k) in slots.items():
            y = top + j * pitch
            pro = k == 0
            px = x0 + 0.12 if left else x0 + ww - 0.12 - 0.56
            D.box_text(px, y + (chh - 0.26) / 2, 0.56, 0.26, "优势" if pro else "劣势", col_of(tone) if pro else WHITE,
                       WHITE if pro else GREY_M, 9.5, M, line=None if pro else GREY_L, shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.5)
            tx = x0 + 0.8 if left else x0 + 0.15
            D.text(tx, y, ww - 0.95, chh, it["text"], size=11, color=GREY if pro else GREY_M, face=M if pro else R,
                   align="l" if left else "r", anchor="m")
    # centre: metric duel
    half = (c1 - c0) / 2 - 0.6
    for j, r in enumerate(rows):
        y = top + j * pitch
        mx = max(r["a"], r["b"])
        D.text(c0, y + 0.03, c1 - c0, 0.24, [(f'{j + 1:02d}  ', {"face": H, "color": RED}), (r["label"], {})],
               size=9.5, color=NAVY_D, face=M, align="c", anchor="m")
        yb = y + 0.3
        for side, v, win in ((0, r["a"], better[j]), (1, r["b"], not better[j])):
            bw = max(half * v / mx, 0.05)
            c = (NAVY, RED)[side] if win else (NAVY_L, RED_L)[side]
            bx = cx - 0.04 - bw if side == 0 else cx + 0.04
            b = D.rect(bx, yb, bw, 0.15, fill=c)
            if win:
                grad(b, [(0, "2E5A94", 100), (100, "16365F", 100)] if side == 0 else GRAD_RED, angle=0)
            vx = bx - 0.5 if side == 0 else bx + bw + 0.05
            D.text(vx, yb - 0.05, 0.45, 0.25, f"{v:g}", size=10.5 if win else 9.5, color=(NAVY, RED)[side] if win else GREY_M,
                   face=H if win else R, align="r" if side == 0 else "l", anchor="m")
    do_strip(D, s.get("strip"))


# =================================================================================== matrix
def matrix(D, s):
    """Open 2x2 matrix (tinted quadrants, numbered, one row framed as the highlighted band) on the left;
    hero statistic with its split bar and two evidence modules on the right, linked to the band."""
    frame(D, s)
    z = s.get("zones", ["", ""])
    rx = 8.0
    zone(D, EL, z[0], "navy", w=2.2)
    zone(D, rx, z[1], "red", w=2.2)
    ax_ = s.get("axes", {})
    mx0, mx1, my0, my1, g = 0.9, 7.6, 2.2, 6.2, 0.08
    qw, qh = (mx1 - mx0 - g) / 2, (my1 - my0 - g) / 2
    xa = mx0 - 0.12
    D.line(xa, my1 + 0.1, mx1 + 0.05, my1 + 0.1, NAVY, 1.5, arrow=True)
    D.line(xa, my1 + 0.1, xa, my0 - 0.08, NAVY, 1.5, arrow=True)
    D.text(mx0, my1 + 0.15, mx1 - mx0, 0.26, ax_.get("x", ""), size=10.5, color=NAVY, face=M, align="c", anchor="m")
    D.text(EL, my0 + 0.4, 0.3, my1 - my0 - 0.8, ax_.get("y", ""), size=10.5, color=NAVY, face=M, align="c", anchor="m", vert=True)
    lo, hi = ax_.get("ends", ["低", "高"])
    D.text(mx0, my1 + 0.15, 0.4, 0.26, lo, size=9.5, color=GREY_M, face=M, anchor="m")
    D.text(mx1 - 0.4, my1 + 0.15, 0.4, 0.26, hi, size=9.5, color=GREY_M, face=M, align="r", anchor="m")
    D.text(EL, my0 - 0.02, 0.3, 0.26, hi, size=9.5, color=GREY_M, face=M, align="c", anchor="m")
    D.text(EL, my1 - 0.26, 0.3, 0.26, lo, size=9.5, color=GREY_M, face=M, align="c", anchor="m")
    band = s.get("band")
    for k, q in enumerate(s["quads"][:4]):
        x, y = mx0 + (k % 2) * (qw + g), my0 + (k // 2) * (qh + g)
        tone = q.get("tone", "navy")
        col = col_of(tone)
        qd = D.rect(x, y, qw, qh, fill=NAVY_T)
        grad(qd, [(0, "E6EDF6" if tone == "navy" else "F9E6E2", 100), (100, "FAFBFD" if tone == "navy" else "FEF9F8", 100)], angle=45)
        gcircle(D, x + 0.22, y + 0.22, 0.6, tone, icon=q.get("icon", "target"), ring=1.5)
        num_badge(D, x + 0.62, y + 0.14, 0.26, f"{k + 1:02d}", tone)
        D.text(x + 0.98, y + 0.14, qw - 1.1, 0.4, q["title"], size=17, color=col, face=H, anchor="m")
        if q.get("label"):
            tag(D, x + 0.98, y + 0.56, 1.4, q["label"], tone, h=0.26, size=9.5)
        D.line(x + 0.22, y + 0.98, x + qw - 0.22, y + 0.98, NAVY_B if tone == "navy" else RED_B, 0.5, DASH.DASH)
        D.text(x + 0.22, y + 1.0, qw - 0.44, qh - 1.0, q.get("desc", ""), size=12.5, color=GREY, spacing=1.15, anchor="m")
    if band:
        by = my0 + band.get("row", 1) * (qh + g)
        D.rect(mx0 - 0.06, by - 0.06, mx1 - mx0 + 0.12, qh + 0.12, line=RED, lw=1.5, dash=DASH.DASH,
               shape=MSO_SHAPE.ROUNDED_RECTANGLE, adj=0.04)
        if band.get("label"):
            chip(D, mx1 - 1.75, by - 0.2, 1.75, band["label"], "red", h=0.28, size=9.5)
    # right wing: hero number + its split bar
    h = s.get("hero")
    if h:
        gcircle(D, rx, 2.25, 0.82, "red", icon=h.get("icon", "home"), ring=2)
        D.text(rx + 0.95, 2.12, 1.9, 0.95, [(h["value"], {}), (h.get("unit", ""), {"size": 20})], size=44, color=RED, face=H, anchor="m")
        D.text(rx + 2.7, 2.28, ER - rx - 2.7, 0.32, h.get("title", ""), size=14, color=NAVY, face=B, anchor="m")
        D.text(rx + 2.7, 2.62, ER - rx - 2.7, 0.28, h.get("sub", ""), size=11, color=GREY, anchor="m")
    sp = s.get("split")
    if sp:
        y = 3.3
        if sp.get("title"):
            module_head(D, rx, y, ER - rx, sp["title"], "red")
            y += 0.42
        x0, tot, w_ = rx, sum(p["value"] for p in sp["parts"]), ER - rx
        for i, p in enumerate(sp["parts"]):
            pw_ = w_ * p["value"] / tot
            tone = p.get("tone", "red" if i == 0 else "navy")
            b = D.rect(x0, y, pw_, 0.32, fill=col_of(tone))
            grad(b, GRAD_RED if tone == "red" else GRAD_NAVY, angle=0)
            lab = p["label"] + (f'  {p["value"]:g}%' if p.get("show_value", True) else "")
            D.text(x0 + 0.1, y, pw_ - 0.2, 0.32, lab, size=10, color=WHITE, face=M, anchor="m")
            if p.get("note"):
                D.text(x0 + 0.02, y + 0.36, pw_ - 0.04, 0.22, p["note"], size=9, color=col_of(tone), face=M, anchor="m")
            x0 += pw_
        caption(D, rx, y + 0.64, ER - rx, sp.get("caption"), align="r")
        if band:
            by = my0 + band.get("row", 1) * (qh + g)
            dot_line(D, rx - 0.02, y + 0.16, mx1 + 0.08, by + qh / 2, RED, dot_start=True)
    mods = s.get("evidence", [])[:2]
    if mods:
        mw = (ER - rx - 0.25 * (len(mods) - 1)) / len(mods)
        for k, md in enumerate(mods):
            x = rx + k * (mw + 0.25)
            module_head(D, x, 4.55, mw, md["title"], md.get("tone", "navy"))
            mini_bars(D, x, 4.98, mw, md["rows"], step=0.38, lw=md.get("label_w", 0.85), unit=md.get("unit", ""))
            caption(D, x, 6.3, mw, md.get("caption"), align="r")


LAYOUTS = {"chart_phases": chart_phases, "funnel": funnel, "hub": hub,
           "dual_charts": dual_charts, "versus": versus, "matrix": matrix}
