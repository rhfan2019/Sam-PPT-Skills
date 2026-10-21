# -*- coding: utf-8 -*-
"""Native-chart styling in the template's manner. Every chart stays editable (right-click > Edit Data)."""
import copy

from lxml import etree
from pptx.oxml.ns import qn
from pptx.util import Pt
from pptx.enum.chart import XL_TICK_LABEL_POSITION

from .deck import rgb, A_NS
from .tokens import *

C_NS = "http://schemas.openxmlformats.org/drawingml/2006/chart"


def chart_text(chart, size=9, color="595959"):
    """OPPOSans R for latin + east-asian, no title, no frame."""
    chart.has_title = False
    cs = chart._chartSpace
    old = cs.find(qn("c:txPr"))
    if old is not None:
        cs.remove(old)
    el = etree.fromstring(
        f'<c:txPr xmlns:c="{C_NS}" xmlns:a="{A_NS}"><a:bodyPr/><a:lstStyle/><a:p><a:pPr><a:defRPr sz="{int(size * 100)}">'
        f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill><a:latin typeface="{R}"/><a:ea typeface="{R}"/>'
        f'<a:cs typeface="{R}"/></a:defRPr></a:pPr><a:endParaRPr lang="zh-CN"/></a:p></c:txPr>')
    anchor = cs.find(qn("c:externalData"))
    (anchor.addprevious(el) if anchor is not None else cs.append(el))
    sp = cs.find(qn("c:spPr"))
    if sp is None:
        sp = etree.SubElement(cs, qn("c:spPr"))
        cs.find(qn("c:chart")).addnext(sp)
    sp.clear()
    etree.SubElement(sp, qn("a:noFill"))
    etree.SubElement(etree.SubElement(sp, qn("a:ln")), qn("a:noFill"))
    chart.has_legend = False


def fill_series(ser, color, line=False, width=2.0):
    if line:
        ser.format.line.color.rgb = rgb(color)
        ser.format.line.width = Pt(width)
    else:
        ser.format.fill.solid()
        ser.format.fill.fore_color.rgb = rgb(color)


def ser_grad(ser, c_from, c_to, angle=90):
    """Gradient fill on a whole series (angle 90 = top->bottom, 0 = left->right)."""
    fill_series(ser, c_from)
    sp = ser._element.find(qn("c:spPr"))
    sf = sp.find(qn("a:solidFill"))
    sf.addprevious(etree.fromstring(
        f'<a:gradFill xmlns:a="{A_NS}" rotWithShape="1"><a:gsLst><a:gs pos="0"><a:srgbClr val="{c_from}"/></a:gs>'
        f'<a:gs pos="100000"><a:srgbClr val="{c_to}"/></a:gs></a:gsLst><a:lin ang="{int(angle * 60000)}" scaled="0"/></a:gradFill>'))
    sp.remove(sf)


def ser_alpha(ser, pct):
    clr = ser._element.find(qn("c:spPr")).find(".//" + qn("a:srgbClr"))
    etree.SubElement(clr, qn("a:alpha")).set("val", str(int(pct * 1000)))


def gridlines(axis, color="E3E8EF"):
    axis.has_major_gridlines = True
    axis.major_gridlines.format.line.color.rgb = rgb(color)
    axis.major_gridlines.format.line.width = Pt(0.5)


def axis_line(axis, color=NAVY_B, show=True):
    if show:
        axis.format.line.color.rgb = rgb(color)
        axis.format.line.width = Pt(0.75)
    else:
        axis.format.line.fill.background()


def hide_val_axis(ch):
    """Hide labels/line/grid but keep the axis: deleting an axis in a combo chart makes PowerPoint drop its scale."""
    va = ch.value_axis
    va.has_major_gridlines = False
    va.tick_label_position = XL_TICK_LABEL_POSITION.NONE
    axis_line(va, show=False)


def label_font(dl, size=9, color="595959", bold=False, face=R):
    f = dl.font
    f.size = Pt(size)
    f.bold = bold
    f.color.rgb = rgb(color)
    f.name = face
    rPr = f._element          # this label's own defRPr (never the first one in the series)
    if rPr.find(qn("a:ea")) is None:
        etree.SubElement(rPr, qn("a:ea")).set("typeface", face)


def hide_point_label(ser, idx):
    dls = ser._element.find(qn("c:dLbls"))
    el = etree.fromstring(f'<c:dLbl xmlns:c="{C_NS}"><c:idx val="{idx}"/><c:delete val="1"/></c:dLbl>')
    prev = dls.findall(qn("c:dLbl"))
    (prev[-1].addnext(el) if prev else dls.insert(0, el))


def plot_layout(ch, lx, ty, lw, th):
    """Pin the inner plot area (fractions of the chart frame) so overlays can be aligned to categories."""
    pa = ch._chartSpace.find(".//" + qn("c:plotArea"))
    lay = pa.find(qn("c:layout"))
    if lay is None:
        lay = etree.Element(qn("c:layout")); pa.insert(0, lay)
    lay.clear()
    lay.append(etree.fromstring(
        f'<c:manualLayout xmlns:c="{C_NS}"><c:layoutTarget val="inner"/><c:xMode val="edge"/><c:yMode val="edge"/>'
        f'<c:x val="{lx}"/><c:y val="{ty}"/><c:w val="{lw}"/><c:h val="{th}"/></c:manualLayout>'))


def hole(ch, pct):
    ch._chartSpace.find(".//" + qn("c:holeSize")).set("val", str(pct))


def bubble_scale(ch, pct):
    bc = ch._chartSpace.find(".//" + qn("c:bubbleChart"))
    bs = bc.find(qn("c:bubbleScale"))
    if bs is None:
        bs = etree.Element(qn("c:bubbleScale")); bc.find(qn("c:axId")).addprevious(bs)
    bs.set("val", str(pct))


def line_to_secondary(ch, idx, color=RED, vmin=-15, vmax=60, fmt='0.0"%"', below=()):
    """Move series `idx` of a clustered-column chart onto a line on a hidden secondary axis.
    A negative vmin floats the line above the bars. `below` = point indices whose label sits under the marker."""
    pa = ch._chartSpace.find(".//" + qn("c:plotArea"))
    bar = pa.find(qn("c:barChart"))
    s2 = bar.findall(qn("c:ser"))[idx]
    bar.remove(s2)
    for t in ("c:invertIfNegative", "c:spPr", "c:dLbls"):
        e = s2.find(qn(t))
        if e is not None:
            s2.remove(e)
    C, A = C_NS, A_NS
    fmt_x = fmt.replace('"', "&quot;")
    tx = (f'<c:txPr><a:bodyPr/><a:lstStyle/><a:p><a:pPr><a:defRPr sz="900"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
          f'<a:latin typeface="{B}"/><a:ea typeface="{B}"/></a:defRPr></a:pPr><a:endParaRPr lang="zh-CN"/></a:p></c:txPr>')
    flags = ('<c:showLegendKey val="0"/><c:showVal val="1"/><c:showCatName val="0"/><c:showSerName val="0"/>'
             '<c:showPercent val="0"/><c:showBubbleSize val="0"/>')
    one = "".join(f'<c:dLbl><c:idx val="{i}"/><c:numFmt formatCode="{fmt_x}" sourceLinked="0"/><c:spPr><a:noFill/></c:spPr>'
                  f'{tx}<c:dLblPos val="b"/>{flags}</c:dLbl>' for i in sorted(below))
    sp = etree.fromstring(f'<c:spPr xmlns:c="{C}" xmlns:a="{A}"><a:ln w="28575" cap="rnd"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:ln></c:spPr>')
    mk = etree.fromstring(f'<c:marker xmlns:c="{C}" xmlns:a="{A}"><c:symbol val="circle"/><c:size val="7"/><c:spPr><a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill><a:ln w="19050"><a:solidFill><a:srgbClr val="{color}"/></a:solidFill></a:ln></c:spPr></c:marker>')
    dl = etree.fromstring(f'<c:dLbls xmlns:c="{C}" xmlns:a="{A}">{one}<c:numFmt formatCode="{fmt_x}" sourceLinked="0"/><c:spPr><a:noFill/></c:spPr>{tx}<c:dLblPos val="t"/>{flags}</c:dLbls>')
    s2.find(qn("c:tx")).addnext(sp); sp.addnext(mk); mk.addnext(dl)
    etree.SubElement(s2, qn("c:smooth")).set("val", "0")
    line = etree.fromstring(f'<c:lineChart xmlns:c="{C}"><c:grouping val="standard"/><c:varyColors val="0"/></c:lineChart>')
    line.append(s2)
    etree.SubElement(line, qn("c:marker")).set("val", "1")
    etree.SubElement(line, qn("c:axId")).set("val", "50020")
    etree.SubElement(line, qn("c:axId")).set("val", "50030")
    bar.addnext(line)
    axes = etree.fromstring(
        f'<root xmlns:c="{C}" xmlns:a="{A}"><c:catAx><c:axId val="50020"/><c:scaling><c:orientation val="minMax"/></c:scaling>'
        f'<c:delete val="1"/><c:axPos val="b"/><c:majorTickMark val="none"/><c:minorTickMark val="none"/><c:tickLblPos val="nextTo"/>'
        f'<c:crossAx val="50030"/><c:crosses val="autoZero"/><c:auto val="1"/><c:lblAlgn val="ctr"/><c:lblOffset val="100"/>'
        f'<c:noMultiLvlLbl val="0"/></c:catAx><c:valAx><c:axId val="50030"/><c:scaling><c:orientation val="minMax"/>'
        f'<c:max val="{vmax}"/><c:min val="{vmin}"/></c:scaling><c:delete val="0"/><c:axPos val="r"/><c:majorTickMark val="none"/>'
        f'<c:minorTickMark val="none"/><c:tickLblPos val="none"/><c:spPr><a:ln><a:noFill/></a:ln></c:spPr><c:crossAx val="50020"/>'
        f'<c:crosses val="max"/><c:crossBetween val="between"/></c:valAx></root>')
    last = pa.findall(qn("c:valAx"))[-1]
    for a in reversed(list(axes)):
        last.addnext(a)
