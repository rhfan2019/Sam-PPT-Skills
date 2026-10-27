"""Print a reference page's geometry and paint as a compact list, for use as a blueprint.

Reads one self-contained slide SVG from a ppt-master import workspace
(svg-flat/slide_NN.svg). Text is cut to 60 characters: it shows where text sits
and how big it is, not what to write.

Usage: python dump_blueprint.py <slide_NN.svg>
"""
import sys
import xml.etree.ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"
KEYS = ["d", "x", "y", "width", "height", "fill", "fill-opacity", "stroke", "stroke-width",
        "stroke-dasharray", "filter", "href", "{http://www.w3.org/1999/xlink}href", "points",
        "cx", "cy", "r", "rx", "ry", "opacity", "transform", "font-size", "font-family",
        "font-weight", "writing-mode", "x1", "y1", "x2", "y2"]


def short(e):
    tag = e.tag.replace(NS, "")
    attrs = " ".join(f'{k.split("}")[-1]}={e.attrib[k][:70]}' for k in KEYS if k in e.attrib)
    text = "".join(e.itertext()).strip()
    return f"{tag} {attrs}" + (f' TEXT="{text[:60]}"' if tag == "text" else "")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    root = ET.parse(sys.argv[1]).getroot()
    for c in root:
        tag = c.tag.replace(NS, "")
        if tag == "defs":
            ids = [d.get("id") for d in c if d.get("id")]
            print("## defs", " ".join(ids))
            continue
        print("##", tag, c.get("id") or "", c.get("data-pptx-bounds") or "")
        if tag == "g":
            for d in c.iter():
                if d is c or d.tag.replace(NS, "") in ("tspan", "g"):
                    continue
                print("   ", short(d))
        else:
            print("   ", short(c))


if __name__ == "__main__":
    main()
