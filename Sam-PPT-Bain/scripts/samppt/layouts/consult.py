# -*- coding: utf-8 -*-
"""Consulting archetypes modelled on template slide 10:
thesis banner -> zone labels -> hero graphic with two wings -> evidence -> framework strip."""
import math

from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LABEL_POSITION
from pptx.enum.dml import MSO_LINE_DASH_STYLE as DASH
from pptx.enum.shapes import MSO_SHAPE

from ..charts import *
from ..components import *
from ..deck import grad, alpha, shadow
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


LAYOUTS = {"chart_phases": chart_phases, "funnel": funnel, "hub": hub}
