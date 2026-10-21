# -*- coding: utf-8 -*-
"""Design tokens measured from the 参考模板 template. Layouts and components use only these names."""

# ---------------------------------------------------------------- colour (theme "红蓝配色" + recurring tints)
NAVY = "1C4274"        # accent1
RED = "A23424"         # accent2
NAVY_D = "0E213A"      # accent1 lumMod 50 % (section tag)
NAVY_M = "4A6A99"
NAVY_L = "9DB3D1"
NAVY_T = "EEF2F8"      # light card tint
NAVY_B = "A9B9D0"      # card border
RED_L = "E3A79D"
RED_T = "FBF0EE"
RED_B = "D9A39A"
RED_D = "5A1E15"       # text on pink zone labels
GREY = "404040"
GREY_M = "7F7F7F"
GREY_L = "D9D9D9"
GREY_T = "F2F2F2"
WHITE = "FFFFFF"
BLUE_Z = "D3DEEE"      # zone label / tag tint, navy side (accent1 20 %)
PINK_Z = "F2D9D4"      # zone label / tag tint, red side (accent2 20 %)
ON_DARK = "D6DEEA"     # secondary text on navy
ON_RED = "F6D9D3"      # secondary text on red
HILITE_DARK = "F7C3B9" # **highlight** inside a navy banner

GRAD_NAVY = [(0, "16365F", 100), (100, "2E5A94", 100)]
GRAD_RED = [(0, "8E2B1D", 100), (100, "C0503E", 100)]
GRAD_TAB = [(0, "D3DEEE", 100), (100, "FFFFFF", 100)]
GRAD_TAB_R = [(0, "F3D5CF", 100), (100, "FFFFFF", 100)]

# ---------------------------------------------------------------- type
H, B, M, R, LT = "OPPOSans H", "OPPOSans B", "OPPOSans M", "OPPOSans R", "OPPOSans L"
FS_BANNER = 17         # thesis banner
FS_ZONE = 15           # zone labels
FS_ITEM = 13           # item titles
FS_BODY = 10.5         # body
FS_SMALL = 9.5         # descriptions
FS_MICRO = 8           # units / footnotes inside evidence boxes (template uses 6–8)

# ---------------------------------------------------------------- page grid (inches, 13.333 x 7.5)
SLIDE_W, SLIDE_H = 13.333, 7.5
EL, ER = 0.37, 12.96   # content edges = template title rule / footer edges. Nothing may cross them.
CW = ER - EL
TOP = 1.0              # first content row under the title rule (rule sits at 0.86)
BOTTOM = 6.95          # last content pixel above the footer rule (7.16)
BANNER_Y, BANNER_H = 1.0, 0.5
ZONE_Y, ZONE_H = 1.62, 0.42
BODY_TOP = 2.1         # consulting layouts: body starts under the zone labels
STRIP_Y = 6.28         # consulting layouts: framework strip (0.5 high)
CARD_TOP = 1.15        # card layouts: first card row when there is no banner
GAP = 0.2


def cols(n, gap=GAP, x0=EL, x1=ER):
    """Split [x0, x1] into n equal columns -> list of (x, w)."""
    w = (x1 - x0 - gap * (n - 1)) / n
    return [(x0 + i * (w + gap), w) for i in range(n)]
