#!/usr/bin/env python3
"""og.png generator — Jensing's Resale & Thrift (1200x630, shop identity only, no builder markers).
Poster matches the site: pale sage field + dashed marigold stitch frame + Georgia serif +
pine footer strip + hanging price tag with 'SUPER, SUPER CHEAP.'"""
import os, math
from PIL import Image, ImageDraw, ImageFont

OUT = os.environ.get("OG_OUT", "/Users/rleon/sites/jensings-resale-thrift/public/og.png")
W, H = 1200, 630
SAGE = (238, 241, 230); INK = (34, 48, 31); PINE = (36, 70, 58); PINE2 = (27, 54, 41)
CREAM = (244, 242, 228); MARIGOLD = (217, 144, 18); STITCH = (201, 135, 30)
GOLDBG = (247, 231, 192); BRICK = (164, 64, 47); INK2 = (78, 93, 71)

def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()

GEORGIA = "/System/Library/Fonts/Supplemental/Georgia.ttf"
GEORGIA_B = "/System/Library/Fonts/Supplemental/Georgia Bold.ttf"
GEORGIA_I = "/System/Library/Fonts/Supplemental/Georgia Italic.ttf"
MENLO = "/System/Library/Fonts/Menlo.ttc"

F_KICK = font(MENLO, 22)
F_DISP = font(GEORGIA_B, 150)
F_SUB = font(GEORGIA_B, 58)
F_STAR = font(GEORGIA_B, 34)
F_CHIP = font(MENLO, 21)
F_STRIP = font(MENLO, 21)
F_TAG = font(GEORGIA_I, 44)

img = Image.new("RGB", (W, H), SAGE)
d = ImageDraw.Draw(img)

# dashed stitch frame (marigold), inset 26px — manual dashes
x0, y0, x1, y1 = 26, 26, W - 26, H - 96 - 18
def dash_h(y, xa, xb, dash=16, gap=10):
    x = xa
    while x < xb:
        d.line([(x, y), (min(x + dash, xb), y)], fill=STITCH, width=3); x += dash + gap
def dash_v(x, ya, yb, dash=16, gap=10):
    y = ya
    while y < yb:
        d.line([(x, y), (x, min(y + dash, yb))], fill=STITCH, width=3); y += dash + gap
dash_h(y0, x0, x1); dash_h(y1, x0, x1)
dash_v(x0, y0, y1); dash_v(x1, y0, y1)

# kicker
d.text((70, 70), "DOWNTOWN LONGVIEW  \u00b7  TEXAS", font=F_KICK, fill=BRICK)

# wordmark "Jensing's" (Georgia bold, huge)
d.text((64, 108), "Jensing's", font=F_DISP, fill=INK)

# spaced caps "RESALE & THRIFT"
sp = 7
cx = 70
for ch in "RESALE & THRIFT":
    d.text((cx, 288), ch, font=F_SUB, fill=PINE)
    cx += d.textlength(ch, font=F_SUB) + sp

# chips row
chips = ["CURATED RESALE", "DEEP THRIFT", "VINTAGE = 20+ YRS"]
cx, cy, ch_h = 70, 380, 44
for txt in chips:
    tw = d.textlength(txt, font=F_CHIP)
    d.rounded_rectangle([cx, cy, cx + tw + 26, cy + ch_h], radius=6, fill=GOLDBG, outline=INK, width=2)
    d.text((cx + 13, cy + 11), txt, font=F_CHIP, fill=INK)
    cx += tw + 26 + 16

# stars + line
def star(dd, ccx, ccy, R=15, r=6.2):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = R if i % 2 == 0 else r
        pts.append((ccx + rr * math.cos(ang), ccy + rr * math.sin(ang)))
    dd.polygon(pts, fill=MARIGOLD)
sx = 78
for _ in range(5):
    star(d, sx, 486); sx += 38
d.text((sx + 12, 468), "5.0 on Google", font=F_STAR, fill=INK)

# hanging price tag (rotated card) with "SUPER, SUPER CHEAP."
tw, th = 340, 300
tag = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
td = ImageDraw.Draw(tag)
td.polygon([(34, 0), (tw, 0), (tw, th), (34, th), (0, th // 2)], fill=MARIGOLD, outline=INK, width=3)
td.ellipse([tw - 64, 18, tw - 34, 48], fill=PINE2)
for line, yy in (("SUPER,", 78), ("SUPER", 128), ("CHEAP.", 178)):
    lw = td.textlength(line, font=F_TAG)
    td.text(((tw + 34 - lw) / 2 + 17, yy), line, font=F_TAG, fill=PINE2)
tag = tag.rotate(8, expand=True, fillcolor=(0, 0, 0, 0))
img.paste(tag, (800, 96), tag)

# string from frame corner to tag hole (stitch)
d.line([(120, 26), (860, 132)], fill=STITCH, width=3)

# pine footer strip
d.rectangle([0, H - 96, W, H], fill=PINE2)
d.text((70, H - 63), "813 E METHVIN ST SUITE B  \u00b7  LONGVIEW, TX 75601  \u00b7  (903) 704-9393  \u00b7  TUE\u2013SAT 10\u20137", font=F_STRIP, fill=CREAM)

img.save(OUT, "PNG", optimize=True)
print("wrote", OUT, img.size)
