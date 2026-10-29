"""Replace and fit the text of one <text> element without losing its typography (A and B).

Used by edit_page.py text; also importable. Reference pages arrive in ppt-master's import text
model: each top-level <tspan> is a visual line, a plain one starts a paragraph (it may carry
data-paragraph-space-before), one with data-paragraph-line-break="1" continues the paragraph on a
new line, and nested <tspan>s are runs with their own size, colour, weight. Replacing text by hand
used to keep only the first run's style, so bullets, "label: body" colouring, big number + small
unit and paragraph spacing were lost, and nothing re-wrapped the new text to its box.

  parse(text_el)              -> [Para(attrs, [Run(text, attrs)])]
  replace(text_el, new, ...)  -> report dict; rewrites text_el in place

New text: "\\n" (or a real newline) separates paragraphs; paragraph i takes the style of the old
paragraph i (extra ones copy the last). Inside a paragraph the old runs are matched like this:
  - an explicit "¦" splits the new text into runs, taking the old runs' styles in order;
  - a bullet run ("●  ") is kept, unless the new text brings its own bullet;
  - old runs that the new text still starts with ("人群特点", ": ") or ends with ("万元") are kept;
  - an old numeric run ("108") takes the new text's leading number, the next run the rest;
  - an old "label:" run takes the new text up to its first ":"/"：", the next run the rest;
  - otherwise the whole paragraph takes the style of the longest old run (the body, not the label).
Then every paragraph is wrapped to the box width with ppt-master's own width estimator (the one the
checker uses), CJK by character, Latin and numbers by word, no closing punctuation at a line start.
The box is the text's shape frame (data-pptx-frame of the enclosing shape group) when the old text
fitted it, so text that was allowed to run past a small frame (wrap none in PowerPoint) is not
squeezed. A block that was centred in its frame stays centred. Too tall for the frame is reported,
not hidden: shorten the wording to a label (page-zoning.md §七), or pass fit=True to step the font
down to max(10px, 0.85 × the old size) as a last resort.
"""
from __future__ import annotations

import copy
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

from lxml import etree

sys.path.insert(0, str(Path(__file__).resolve().parent))
from pm import ppt_master_dir  # noqa: E402

sys.path.insert(0, str(Path(ppt_master_dir()) / "scripts"))
from text_measure import measure_text  # noqa: E402

SVG = "http://www.w3.org/2000/svg"
TSPAN = f"{{{SVG}}}tspan"
NUM = r"-?\d*\.?\d+(?:[eE][-+]?\d+)?"
RUN_SEP = "¦"
POS = ("x", "y", "dx", "dy")
BULLET_RUN = re.compile(r"^\s*[●•▪■◆◇○◦·▶►✓✔√]\s*$")
BULLET_HEAD = re.compile(r"^\s*[●•▪■◆◇○◦·▶►✓✔√]")
NUMBERED = re.compile(r"^\s*(?:\d{1,2}[.、)）]|[①-⑳]|[（(]\d{1,2}[)）])")
NUMERIC_RUN = re.compile(r"^[+\-−±~约]?\d[\d,.]*[%％]?$")
NUM_HEAD = re.compile(r"^[+\-−±~约]?\d[\d,.]*[%％]?")
NO_LINE_START = set("，。、；：！？）》」』】〕…%％,.;:!?)]}·”’")
NO_LINE_END = set("（《「『【〔“‘([{")
LATIN = re.compile(r"[A-Za-z0-9.,%+\-/_#&@'’]")


@dataclass
class Run:
    text: str
    attrs: dict = field(default_factory=dict)


@dataclass
class Para:
    attrs: dict = field(default_factory=dict)
    runs: list = field(default_factory=list)
    breaks: list = field(default_factory=list)  # character offsets of the source's own line breaks

    @property
    def text(self):
        return "".join(r.text for r in self.runs)


def nums(s):
    return [float(v) for v in re.findall(NUM, s or "")]


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def run_attrs(el):
    return {k: v for k, v in el.attrib.items() if k not in POS and not k.startswith("data-paragraph")}


def para_attrs(el):
    return {k: v for k, v in el.attrib.items()
            if k.startswith("data-paragraph") and k not in ("data-paragraph-line-break", "data-paragraph-soft-break")}


def runs_of(line):
    """Runs of one line <tspan>: its own text, nested tspans (inheriting the line's style), tails."""
    base = run_attrs(line)
    out = []
    if line.text:
        out.append(Run(line.text, dict(base)))
    for c in line:
        if c.tag != TSPAN:
            continue
        inner = runs_of(c)
        for r in inner:
            r.attrs = {**base, **r.attrs}
        out.extend(inner)
        if c.tail:
            out.append(Run(c.tail, dict(base)))
    return out


def join(prev, nxt):
    """Join a wrapped continuation onto its paragraph: Latin words need a space, CJK does not."""
    if prev.runs and nxt and prev.runs[-1].text[-1:].isascii() and prev.runs[-1].text[-1:].isalnum() \
            and nxt[0].text[:1].isascii() and nxt[0].text[:1].isalnum():
        nxt[0].text = " " + nxt[0].text
    prev.runs.extend(nxt)


def parse(t):
    lines = [c for c in t if c.tag == TSPAN]
    paras = []
    if t.get("data-paragraph-line-height") and lines:
        for c in lines:
            rs = runs_of(c)
            cont = c.get("data-paragraph-line-break") == "1" or c.get("data-paragraph-soft-break") == "1"
            if cont and paras:
                paras[-1].breaks.append(len(paras[-1].text))
                join(paras[-1], rs)
            else:
                paras.append(Para(para_attrs(c), rs))
    elif any(c.get(a) is not None for c in lines for a in ("dy", "y")):
        paras.append(Para({}, [Run(t.text, {})] if t.text else []))
        for c in lines:
            rs = runs_of(c)
            if (c.get("dy") or (c.get("y") and c.get("y") != t.get("y"))) and paras[-1].runs:
                # a positioned line continues its paragraph (the exporter joins them, a bullet keeps its
                # hanging indent) unless it starts a new bullet or number
                if rs and (BULLET_HEAD.match(rs[0].text) or NUMBERED.match(rs[0].text)):
                    paras.append(Para({}, rs))
                else:
                    paras[-1].breaks.append(len(paras[-1].text))
                    join(paras[-1], rs)
            else:
                paras[-1].runs.extend(rs)
    else:
        p = Para({}, [Run(t.text, {})] if t.text else [])
        for c in lines:
            p.runs.extend(runs_of(c))
            if c.tail:
                p.runs.append(Run(c.tail, {}))
        paras.append(p)
    for p in paras:
        p.runs = [r for r in p.runs if r.text]
    return [p for p in paras if p.runs] or [Para({}, [Run("", {})])]


# ---------- mapping new text onto old runs ----------

def fill(tpl, s):
    runs = [Run(r.text, dict(r.attrs)) for r in tpl.runs if r.text]
    if RUN_SEP in s:
        segs = s.split(RUN_SEP)
        return Para(dict(tpl.attrs), [Run(seg, dict(runs[min(i, len(runs) - 1)].attrs) if runs else {})
                                      for i, seg in enumerate(segs) if seg])
    out = []
    if len(runs) > 1 and BULLET_RUN.match(runs[0].text):
        b = runs.pop(0)
        if s.startswith(b.text):
            s = s[len(b.text):]
            out.append(b)
        elif not BULLET_HEAD.match(s):
            out.append(b)
    if not runs:
        return Para(dict(tpl.attrs), out + [Run(s, {})])
    if len(runs) == 1:
        return Para(dict(tpl.attrs), out + [Run(s, runs[0].attrs)])
    i = 0
    while i < len(runs) - 1 and runs[i].text.strip() and s.startswith(runs[i].text):
        out.append(runs[i])
        s = s[len(runs[i].text):]
        i += 1
    rest, tail = runs[i:], []
    while len(rest) > 1 and rest[-1].text.strip() and len(s) > len(rest[-1].text) and s.endswith(rest[-1].text):
        tail.insert(0, rest.pop())
        s = s[:-len(tail[0].text)]
    if not s:
        pass
    elif len(rest) == 1:
        out.append(Run(s, rest[0].attrs))
    elif NUMERIC_RUN.match(rest[0].text.strip()) and NUM_HEAD.match(s):
        m = NUM_HEAD.match(s)
        out.append(Run(m.group(0), rest[0].attrs))
        if s[m.end():]:
            out.append(Run(s[m.end():], rest[1].attrs))
    else:
        sep = next((k for k, r in enumerate(rest[:-1]) if r.text.rstrip().endswith((":", "："))), None)
        m = re.search(r"[:：]\s*", s)
        if sep is not None and m:
            head, colon, body = s[:m.start()], m.group(0), s[m.end():]
            if rest[sep].text.strip() in (":", "：") and sep > 0:
                out += [Run(head, rest[0].attrs), Run(colon, rest[sep].attrs)]
            else:
                out.append(Run(head + colon, rest[sep].attrs))
            if body:
                out.append(Run(body, rest[sep + 1].attrs))
        else:
            out.append(Run(s, max(rest, key=lambda r: len(r.text)).attrs))
    return Para(dict(tpl.attrs), [r for r in out + tail if r.text])


# ---------- measuring ----------

def inherited(el, name):
    for a in [el, *el.iterancestors()]:
        if a.get(name):
            return a.get(name)
    return None


def style_of(t, attrs):
    size = nums(attrs.get("font-size") or inherited(t, "font-size") or "14")[0]
    fam = (attrs.get("font-family") or inherited(t, "font-family") or "OPPOSans M").split(",")[0].strip().strip('"\'')
    weight = attrs.get("font-weight") or t.get("font-weight") or ("bold" if re.search(r"\b(B|H|Bold|Heavy)\b", fam) else "normal")
    ls = nums(attrs.get("letter-spacing") or t.get("letter-spacing") or "0")
    return size, fam, weight, ls[0] if ls else 0.0


def width(t, text, attrs):
    if not text:
        return 0.0
    size, fam, weight, ls = style_of(t, attrs)
    return measure_text(text, size=size, family=fam, weight=weight, letter_spacing=ls, include_headroom=False)


def units(para):
    """Break units [text, attrs, glued]: one CJK character, or a Latin/number word; closing marks glue
    to what is before them and opening marks to what follows, so neither starts or ends a line."""
    out = []
    for r in para.runs:
        for ch in r.text:
            if out:
                prev = out[-1]
                same = prev[1] is r.attrs
                if same and LATIN.match(ch) and LATIN.match(prev[0][-1]):
                    prev[0] += ch
                    continue
                if ch in NO_LINE_START or prev[0][-1] in NO_LINE_END:
                    if same:
                        prev[0] += ch
                    else:
                        out.append([ch, r.attrs, True])
                    continue
            out.append([ch, r.attrs, False])
    return out


def split_at(para, offsets):
    lines, cur, pos, cuts = [], [], 0, sorted(offsets)
    for r in para.runs:
        text = r.text
        while cuts and pos + len(text) > cuts[0] - 0 and cuts[0] >= pos:
            k = cuts.pop(0) - pos
            if text[:k]:
                cur.append(Run(text[:k], r.attrs))
            lines.append(cur)
            cur, pos, text = [], pos + k, text[k:].lstrip(" ")
        if text:
            cur.append(Run(text, r.attrs))
        pos += len(text)
    lines.append(cur)
    return [ln for ln in lines if ln]


def wrap(t, para, max_w, keep=None):
    """Greedy wrap of one paragraph into lines of runs; `keep` = the source's break offsets, used as they
    are when the paragraph's words did not change (rewriting the same words must not re-flow them)."""
    if keep:
        return split_at(para, keep)
    lines, cur, cur_w = [], [], 0.0
    for text, attrs, glued in units(para):
        w = width(t, text, attrs)
        if max_w and cur and cur_w + w > max_w + 0.5 and not glued and text.strip():
            lines.append(cur)
            cur, cur_w = [], 0.0
        if not cur and not text.strip():
            continue
        cur.append((text, attrs))
        cur_w += w
    if cur or not lines:
        lines.append(cur)
    merged = []
    for ln in lines:
        rs = []
        for text, attrs in ln:
            if rs and rs[-1].attrs is attrs:
                rs[-1].text += text
            else:
                rs.append(Run(text, attrs))
        if rs:
            rs[-1].text = rs[-1].text.rstrip()
        merged.append([r for r in rs if r.text])
    return merged


def line_width(t, runs):
    return sum(width(t, r.text, r.attrs) for r in runs)


# ---------- the box ----------

def frame_of(t):
    for a in t.iterancestors():
        f = nums(a.get("data-pptx-frame"))
        if len(f) == 4 and a.get("data-pptx-object") != "group":
            return f
        if a.getparent() is None:
            break
    return None


def avail_width(t, f):
    x = nums(t.get("x"))[0] if nums(t.get("x")) else f[0]
    anchor = t.get("text-anchor") or "start"
    if anchor == "middle":
        inset = max(0.0, min(abs(x - (f[0] + f[2] / 2)), f[2] / 2))
        return max(f[2] - 2 * max(7.2, inset), f[2] * 0.6)
    left = max(0.0, x - f[0]) if anchor == "start" else max(0.0, f[0] + f[2] - x)
    room = (f[0] + f[2] - x) if anchor == "start" else (x - f[0])
    return max(room - min(left, 10.0), 1.0)


def line_height(t, size):
    lh = nums(t.get("data-paragraph-line-height"))
    if lh:
        return lh[0]
    lines = [c for c in t if c.tag == TSPAN and c.get("dy")]
    if lines and nums(lines[0].get("dy")):
        return nums(lines[0].get("dy"))[0]
    return round(size * 1.3, 2)


def visual_lines(t):
    if t.get("data-paragraph-line-height"):
        return max(1, len([c for c in t if c.tag == TSPAN]))
    return 1 + len([c for c in t if c.tag == TSPAN and (c.get("dy") or (c.get("y") and c.get("y") != t.get("y")))])


def space_before(p):
    v = nums(p.attrs.get("data-paragraph-space-before"))
    return v[0] if v else 0.0


# ---------- writing ----------

def write(t, laid, lh, model):
    for c in list(t):
        t.remove(c)
    t.text = None
    single = len(laid) == 1 and len(laid[0][1]) == 1
    for a in ("data-pptx-text-model", "data-paragraph-line-height"):
        t.attrib.pop(a, None)
    if single and not laid[0][0].attrs:
        runs = laid[0][1][0]
        if len(runs) == 1 and not runs[0].attrs:
            t.text = runs[0].text
            return
        for r in runs:
            etree.SubElement(t, TSPAN, r.attrs).text = r.text
        return
    t.set("data-pptx-text-model", model)
    t.set("data-paragraph-line-height", lh if isinstance(lh, str) else fmt(lh))
    for p, lines in laid:
        for i, runs in enumerate(lines):
            ln = etree.SubElement(t, TSPAN, dict(p.attrs) if i == 0 else {"data-paragraph-line-break": "1"})
            for r in runs:
                etree.SubElement(ln, TSPAN, r.attrs).text = r.text


def replace(t, new, fit=False, width_override=None):
    """Rewrite text element t with `new`, keeping its paragraph and run styles; returns a report."""
    old = parse(t)
    base_size = style_of(t, {})[0]
    lh = line_height(t, base_size)
    n_old = visual_lines(t)
    f = frame_of(t)
    old_w = max((line_width(t, r) for r in [p.runs for p in old]), default=0.0)
    max_w = width_override
    if max_w is None and f:
        aw = avail_width(t, f)
        if t.get("data-paragraph-line-height") and n_old > 1:
            # imported wrapped text: its longest visual line shows the width it was wrapped to
            vis = [runs_of(c) for c in t if c.tag == TSPAN]
            aw = max(aw, max(line_width(t, r) for r in vis))
        # the old text proves its own width fits: never wrap tighter than its widest line
        max_w = max(aw, old_w if n_old == 1 else 0.0) if old_w <= aw * 1.08 or n_old > 1 else None
    if max_w is None and n_old > 1:
        # no frame to wrap to, but the source wrapped itself (a stacked vertical label, a hand-broken
        # line): its own widest line is the width, so a vertical label stays one character per line
        own = [line_width(t, ln) for p in old for ln in (split_at(p, p.breaks) if p.breaks else [p.runs])]
        max_w = max(own) if own else None
    texts = new.replace("\\n", "\n").split("\n")

    def keep(i, p):
        return old[i].breaks if i < len(old) and old[i].breaks and p.text == old[i].text and scale == 1.0 else None

    paras = [fill(old[min(i, len(old) - 1)], s) for i, s in enumerate(texts)]
    if len(paras) > len(old) and len(old) == 1:
        for p in paras[1:]:
            p.attrs.setdefault("data-paragraph-space-before", fmt(max(2.0, lh * 0.2)))
    old_block = (n_old - 1) * lh + base_size
    report = {}
    sizes = [(r, nums(r.attrs["font-size"])[0] if r.attrs.get("font-size") else None) for p in paras for r in p.runs]
    floor = max(10.0, base_size * 0.85)
    lh0, scale = lh, 1.0
    while True:
        laid = [(p, wrap(t, p, max_w, keep(i, p))) for i, p in enumerate(paras)]
        n_new = sum(len(ls) for _, ls in laid)
        block_h = (n_new - 1) * lh + sum(space_before(p) for p, _ in laid[1:]) + base_size * scale
        widest = max((line_width(t, r) for _, ls in laid for r in ls), default=0.0)
        # only what the new words add is reported: a source that already ran past its frame is not news
        too_tall = bool(f) and block_h > max(f[3], old_block) + 0.3 * lh
        too_wide = bool(max_w) and widest > max(max_w, old_w) + 1
        if not fit or not (too_tall or too_wide) or base_size * scale <= floor + 0.01:
            break
        scale = max(floor / base_size, scale - 0.05)
        t.set("font-size", fmt(base_size * scale))
        for r, sz in sizes:
            if sz:
                r.attrs["font-size"] = fmt(sz * scale)
        lh = lh0 * scale
    model = "lines" if any(len(ls) > 1 for _, ls in laid) else "paragraphs"
    if lh == lh0 and t.get("data-paragraph-line-height"):
        lh_out = t.get("data-paragraph-line-height")  # unchanged: keep the source's exact value
    else:
        lh_out = lh
    # keep a centred block centred: compare the old block's middle with the frame's middle
    y = nums(t.get("y"))
    if f and y and n_new != n_old:
        old_mid = y[0] - base_size * 0.8 + ((n_old - 1) * lh + base_size) / 2
        if abs(old_mid - (f[1] + f[3] / 2)) < 0.2 * f[3]:
            t.set("y", fmt(y[0] - (n_new - n_old) * lh / 2))
    write(t, laid, lh_out, model)
    report.update(lines=n_new, width=round(widest, 1), max_width=round(max_w, 1) if max_w else None,
                  frame_h=round(f[3], 1) if f else None, block_h=round(block_h, 1),
                  too_tall=too_tall, too_wide=too_wide, scale=round(scale, 2))
    return report


def describe(rep):
    bits = []
    if rep["too_wide"]:
        bits.append(f"a word wider than the box ({rep['width']} > {rep['max_width']} px)")
    if rep["too_tall"]:
        bits.append(f"{rep['lines']} lines, {rep['block_h']} px tall in a {rep['frame_h']} px frame")
    if not bits:
        return ""
    return "; ".join(bits) + " — shorten to a label (page-zoning.md §七) or use --fit"


if __name__ == "__main__":
    sys.exit(__doc__)
