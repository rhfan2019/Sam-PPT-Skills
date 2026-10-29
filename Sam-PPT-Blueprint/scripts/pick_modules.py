"""Print the best catalog candidates for one zone, so step 2 never reads the whole catalog.

  python pick_modules.py <modules.json> --logic B7 [--logic E2] [--units 4] [--zone 800[x420]]
                         [--chars 260] [--role 主图示] [--top 5] [--crops <out.png>] [--include-unverified]

Applies page-zoning.md section 4: keeps start_level 完好 / 可用 (未验证 only with the flag) whose
logic holds a requested code, then ranks by unit count (parsed from "N（a–b）"; unparsable ranges are
marked 未知), scale inside 0.8–1.25 (zone width over module width, or the tighter of width and height
with WxH), texture_level (高 > 中 > 低), the code being the module's first (native) relation, and
完好 before 可用. Scale and texture come before the first-relation tie-break: a module whose first
code differs still expresses the relation, while a weak or shrunken one visibly loses the reference's look. parts and not_for are printed in full: reading them is still the
agent's job. --crops tiles the candidates cut from started-renders/ into one labelled sheet.

  python pick_modules.py <modules.json> --ids 49-B,09-B --crops <out.png>

Scale is a gate, not a preference: a module that must be scaled outside 0.8–1.25 to fill the zone
keeps the reference's look only at the wrong density (stretched 2x it carries a quarter of the shapes
per area, shrunk to 0.5 its text drops below the size floor; a deck built from modules outside the
range comes out about half as dense as the reference). Such modules are listed separately as
"缩放超出" with the fix: clone units, put two modules side by side, or resize the zone.
--chars is the outline's character count for the zone; a module whose own text ("chars", what the
reference fitted into it) is under 1/2.5 of that is ranked after the others and marked 容量不足 (the
text would end up in added plain text boxes instead of the module's carriers).

prints and crops exactly those modules (the review packet uses this).

  python pick_modules.py <modules.json> --batch <zones.txt> --crops-dir <dir> [--top 3]

does every zone of the deck in one call. Each line of zones.txt is "<page> <zone> <options>", e.g.
"P02 主图 --logic E2 --units 5 --zone 800x420"; blank lines and # comments are skipped. Output is
grouped by page, with one crop sheet per page (<dir>/pick-P02.png) holding every zone's candidates.
"""
import argparse
import json
import re
import shlex
import sys
from pathlib import Path

LEVEL = {"高": 0, "中": 1, "低": 2}
RANGE = re.compile(r"(\d+)\s*[（(](\d+)\s*[–\-~～]\s*(\d+)[)）]")


def unit_fit(text, n):
    """'符合' / '不符' / '未知' for n units against the module's units text."""
    ranges = [(int(a), int(b)) for _, a, b in RANGE.findall(text)]
    if not ranges:
        return "未知"
    return "符合" if any(a <= n <= b for a, b in ranges) else "不符"


def boxes(m):
    return [m["bbox"]] + ([m["bbox_extra"]] if m.get("bbox_extra") else [])


def scale_of(m, zone):
    """Uniform scale that fits the module into the zone (width only, or the tighter of width and height)."""
    if not zone:
        return None
    w, h = zone
    return round(min(w / m["bbox"][2], h / m["bbox"][3]) if h else w / m["bbox"][2], 2)


def coverage(m, zone):
    """Share of the zone's width and height the scaled module covers (WxH zones only)."""
    if not zone or not zone[1]:
        return None
    s = scale_of(m, zone)
    return round(m["bbox"][2] * s / zone[0], 2), round(m["bbox"][3] * s / zone[1], 2)


def capacity(m, chars):
    """Outline characters for the zone over the module's own reference text; None when unknown."""
    cap = m.get("chars") or 0
    return round(chars / cap, 1) if chars and cap else None


def show(m, rank=None, fit=None, scale=None, need=None):
    t = m.get("texture", {})
    head = (f"{rank}. " if rank else "") + (f"{m['module']}  {m['role']}｜{m['diagram']}｜关系 {','.join(m['logic'])}｜"
            f"质感 {m.get('texture_level', '?')} {t.get('grad', 0)}/{t.get('shadow', 0)}/{t.get('alpha', 0)}｜"
            f"起页 {m['start_level']}")
    if scale is not None:
        head += f"｜缩放 {scale}{'' if 0.8 <= scale <= 1.25 else '（超出 0.8–1.25）'}"
    if fit:
        head += f"｜单元 {fit}"
    if need is not None:
        head += f"｜字数 {need} 倍" + ("（容量不足：拆块后仍放不下的要换模块或拆分区）" if need > 2.5 else "")
    lines = [head,
             f"   bbox {','.join(str(v) for v in m['bbox'])}"
             + (f" + {','.join(str(v) for v in m['bbox_extra'])}" if m.get("bbox_extra") else "")
             + f"｜单元 {m['units']}｜字数 {m.get('chars', '?')}｜底板 {m.get('backplates', 0)}",
             f"   适合：{m['fits']}",
             f"   不适合：{m['not_for']}",
             f"   风格：{m['style']}"]
    if m.get("start_note") and m["start_note"] != "无":
        lines.append(f"   起页：{m['start_note']}")
    if m.get("dependency") and m["dependency"] != "无":
        lines.append(f"   依赖：{m['dependency']}")
    for p in m.get("parts", []):
        lines.append(f"   - {p['part']} → {p['means']}；不成立时：{p['if_not_true']}")
    return "\n".join(lines)


def crop_sheet(mods, renders, out):
    from PIL import Image, ImageDraw, ImageFont

    k, tiles = 1600 / 1280, []
    for m in mods:
        src = renders / f"slide-{m['page']}.png"
        if not src.exists():
            continue
        page = Image.open(src).convert("RGB")
        bs = boxes(m)
        x0, y0 = min(b[0] for b in bs), min(b[1] for b in bs)
        x1, y1 = max(b[0] + b[2] for b in bs), max(b[1] + b[3] for b in bs)
        tile = page.crop((int(x0 * k), int(y0 * k), int(x1 * k), int(y1 * k)))
        tile.thumbnail((760, 520))
        tiles.append((m["module"], tile))
    if not tiles:
        return None
    try:
        font = ImageFont.truetype("msyh.ttc", 22)
    except OSError:
        font = ImageFont.load_default()
    cols, cw, ch = min(3, len(tiles)), 780, 560
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, rows * ch), "white")
    draw = ImageDraw.Draw(sheet)
    for i, (name, tile) in enumerate(tiles):
        x, y = (i % cols) * cw + 10, (i // cols) * ch + 34
        sheet.paste(tile, (x, y))
        draw.rectangle((x, y, x + tile.width - 1, y + tile.height - 1), outline="#999999")
        draw.text((x, y - 30), name, fill="black", font=font)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out)
    return out


def rank(cat, logic, units=None, zone=None, roles=(), unverified=False, chars=None, out_of_scale=None):
    levels = {"完好", "可用"} | ({"未验证"} if unverified else set())
    ranked = []
    for m in cat:
        if m["start_level"] not in levels or not set(m["logic"]) & set(logic) or (roles and m["role"] not in roles):
            continue
        fit = unit_fit(m["units"], units) if units else None
        sc = scale_of(m, zone)
        cov = coverage(m, zone)
        if sc is not None and (not 0.8 <= sc <= 1.25 or (cov and min(cov) < 0.6)):
            if out_of_scale is not None:
                out_of_scale.append((m, fit, sc))
            continue
        need = capacity(m, chars)
        key = ({"符合": 0, "未知": 1, "不符": 2}.get(fit, 0),
               1 if need and need > 2.5 else 0,
               LEVEL.get(m.get("texture_level"), 3),
               0 if m["logic"][0] in logic else 1,
               0 if m["start_level"] == "完好" else 1,
               abs(1 - sc) if sc else 0)
        ranked.append((key, m, fit, sc, need))
    ranked.sort(key=lambda r: r[0])
    return ranked


def parse_zone(text):
    if not text:
        return None
    wh = [float(v) for v in text.lower().split("x")]
    return (wh[0], wh[1] if len(wh) > 1 else None)


NONE_FOUND = ("没有过门槛的模块：这个分区改用 ppt-master 原生图表或表格（chart/<key>、table/<key>），"
              "或用 executor-structure.md 的关系原子手写（page-zoning.md 第四节）。")


SCALE_FIX = ("缩放超出 0.8–1.25、或放进去只铺满分区宽或高不到 60% 的同类模块（不直接用）：分区比模块大时，按原间距克隆单元、或把两个模块并排铺满；"
             "分区比模块小时，删单元或把分区改到模块尺寸附近（page-zoning.md 第四节第 7 条）。")


def report(a, top_n):
    zone = parse_zone(a.zone)
    far = []
    ranked = rank(a.cat, a.logic, a.units, zone, a.role, a.include_unverified, a.chars, far)
    head = (f"条件：关系 {','.join(a.logic)}" + (f"｜单元 {a.units}" if a.units else "")
            + (f"｜分区 {a.zone}" if zone else "") + (f"｜字数 {a.chars}" if a.chars else "")
            + (f"｜角色 {','.join(a.role)}" if a.role else "")
            + f"｜过门槛 {len(ranked)} 个，列前 {min(top_n, len(ranked))} 个\n")
    tail = ""
    if far:
        far.sort(key=lambda r: (LEVEL.get(r[0].get("texture_level"), 3), abs(1 - r[2])))
        tail = "\n" + SCALE_FIX + "\n" + "\n".join(
            f"   {m['module']} 缩放 {sc}" + (f"，铺满宽 {coverage(m, zone)[0]:.0%} 高 {coverage(m, zone)[1]:.0%}" if coverage(m, zone) else "") + f"｜{m['diagram']}｜单元 {m['units']}｜质感 {m.get('texture_level', '?')}"
            for m, fit, sc in far[:3])
    if not ranked:
        return head + NONE_FOUND + tail, []
    top = ranked[:top_n]
    return (head + "\n".join(show(m, r, fit, sc, need) + "\n" for r, (_, m, fit, sc, need) in enumerate(top, 1)) + tail,
            [m for _, m, _, _, _ in top])


def parser():
    ap = argparse.ArgumentParser()
    ap.add_argument("--logic", action="append", default=[])
    ap.add_argument("--units", type=int)
    ap.add_argument("--zone", help="zone width, or WxH")
    ap.add_argument("--chars", type=int, help="outline characters the zone has to carry")
    ap.add_argument("--role", action="append", default=[])
    ap.add_argument("--include-unverified", action="store_true")
    return ap


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = parser()
    ap.add_argument("catalog", type=Path)
    ap.add_argument("--top", type=int)
    ap.add_argument("--crops", type=Path)
    ap.add_argument("--crops-dir", type=Path)
    ap.add_argument("--ids")
    ap.add_argument("--batch", type=Path)
    a = ap.parse_args()
    cat = json.loads(a.catalog.read_text(encoding="utf-8"))
    renders = a.catalog.parent / "started-renders"

    if a.ids:
        want = [i.strip() for i in a.ids.split(",") if i.strip()]
        by = {m["module"]: m for m in cat}
        mods = [by[i] for i in want if i in by]
        for i in want:
            if i not in by:
                print(f"! {i} 不在目录里")
        for r, m in enumerate(mods, 1):
            print(show(m, r))
        if a.crops and crop_sheet(mods, renders, a.crops):
            print(f"\n裁切图：{a.crops}")
        return

    if a.batch:
        pages = {}
        for line in a.batch.read_text(encoding="utf-8").splitlines():
            line = line.split("#", 1)[0].strip()
            if not line:
                continue
            page, zname, *opts = shlex.split(line)
            z = parser().parse_args(opts)
            z.cat = cat
            if not z.logic:
                print(f"! {page} {zname} 缺 --logic，跳过")
                continue
            text, mods = report(z, a.top or 3)
            pages.setdefault(page, []).append((zname, text, mods))
        for page, zones in pages.items():
            print(f"==================== {page} ====================")
            for zname, text, _ in zones:
                print(f"--- {zname} ---\n{text}")
            if a.crops_dir:
                seen, mods = set(), []
                for _, _, ms in zones:
                    for m in ms:
                        if m["module"] not in seen:
                            seen.add(m["module"])
                            mods.append(m)
                out = a.crops_dir / f"pick-{page}.png"
                if crop_sheet(mods, renders, out):
                    print(f"裁切图：{out}\n")
        return

    if not a.logic:
        ap.error("--logic, --ids or --batch is required")
    a.cat = cat
    text, mods = report(a, a.top or 5)
    print(text)
    if a.crops and mods and crop_sheet(mods, renders, a.crops):
        print(f"裁切图：{a.crops}")


if __name__ == "__main__":
    main()
