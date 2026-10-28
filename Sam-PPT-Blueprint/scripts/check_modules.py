"""Check a module catalog against the reference pages, measure each module's texture, write an index.

  python check_modules.py <modules.json> <import_workspace>/authoring-svg-flat [--write]

For every module, what compose_page.py would really take (elements centred in bbox / bbox_extra with
at least 60% of their on-page area inside, plus shared backplates cut to the box), which elements are
left behind, and logic values that are not relation codes of logic-diagrams.md.

With --write: store per module "texture" (gradients, shadows, translucent elements, element count
among what it takes) and "texture_level" (高 / 中 / 低 against the whole catalog), and write
modules-index.txt next to modules.json: one line per module, the overview read in step 1.
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from compose_page import inside, is_background, local, parse, select, shown_frame  # noqa: E402

CODES = {f"{f}{i}" for f, n in (("A", 4), ("B", 8), ("C", 4), ("D", 7), ("E", 6), ("F", 5)) for i in range(1, n + 1)} | {"K", "S"}


def texture(elements, src):
    grads = {d.get("id") for d in src.iter() if isinstance(d.tag, str) and local(d) in ("linearGradient", "radialGradient")}
    g = s = a = n = 0
    for e in elements:
        for d in e.iter():
            if not isinstance(d.tag, str) or local(d) in ("g", "text", "tspan"):
                continue
            n += 1
            refs = re.findall(r"url\(#([^)]+)\)", " ".join(d.attrib.values()))
            g += any(r in grads for r in refs)
            s += bool(d.get("filter"))
            a += any(float(re.findall(r"[\d.]+", d.get(k))[0] or 1) < 0.99
                     for k in ("fill-opacity", "opacity", "stroke-opacity") if d.get(k) and re.findall(r"[\d.]+", d.get(k)))
    return {"grad": g, "shadow": s, "alpha": a, "shapes": n}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    path, lib = Path(sys.argv[1]), Path(sys.argv[2])
    cat, write = json.loads(path.read_text(encoding="utf-8")), "--write" in sys.argv
    pages, bad = {}, 0
    for m in cat:
        n = int(m["page"])
        if n not in pages:
            pages[n] = parse(lib / f"slide_{n:02d}.svg")
        boxes = [m["bbox"]] + ([m["bbox_extra"]] if m.get("bbox_extra") else [])
        picked, plates = select(pages[n], boxes)
        left = []
        for e in pages[n]:
            if not isinstance(e.tag, str) or local(e) in ("defs", "metadata", "title", "desc") or is_background(e):
                continue
            if not any(inside(e, *b) for b in boxes) and any(inside(e, *b, share=0) for b in boxes) \
                    and not any(p.get("id") == e.get("id") for p in plates):
                f = shown_frame(e) or []
                left.append(f"{e.get('id')}[{' '.join(str(round(v)) for v in f)}]")
        m["texture"] = texture(picked, pages[n])
        m["backplates"] = len(plates)
        codes = [c for c in m.get("logic", []) if c not in CODES]
        flag = len(picked) == len(plates) or left or codes
        bad += bool(flag)
        line = f"{m['module']:7} took {len(picked):3} (backplates {len(plates)})"
        if left:
            line += f"; left behind {len(left)}: " + " ".join(left[:6]) + (" ..." if len(left) > 6 else "")
        if codes:
            line += f"; logic not a code: {codes}"
        if flag:
            print(line)
    print(f"{len(cat)} module(s), {bad} to look at")
    if not write:
        return
    score = lambda m: 3 * m["texture"]["grad"] + 3 * m["texture"]["shadow"] + 0.5 * m["texture"]["alpha"]  # noqa: E731
    ranked = sorted(score(m) for m in cat)
    lo, hi = ranked[len(ranked) // 3], ranked[2 * len(ranked) // 3]
    for m in cat:
        m["texture_level"] = "高" if score(m) > hi else "低" if score(m) <= lo else "中"
    path.write_text(json.dumps(cat, ensure_ascii=False, indent=1), encoding="utf-8")
    rows = ["模块 | 角色 | 图示 | 关系 | 单元 | 起页 | 质感(渐变/阴影/半透明) | 适合"]
    for m in cat:
        t = m["texture"]
        rows.append(f"{m['module']} | {m['role']} | {m['diagram']} | {','.join(m['logic'])} | {m['units']} | "
                    f"{m.get('start_level', '')} | {m['texture_level']} {t['grad']}/{t['shadow']}/{t['alpha']} | {m['fits']}")
    (path.parent / "modules-index.txt").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"texture written; levels: 低 <= {lo} < 中 <= {hi} < 高 (score = 3*grad + 3*shadow + 0.5*alpha); "
          f"index: {path.parent / 'modules-index.txt'}")


if __name__ == "__main__":
    main()
