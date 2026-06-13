#!/usr/bin/env python3
"""Render a side-by-side comparison of softer color palette options."""
from PIL import Image, ImageDraw, ImageFont

LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
BG = (245, 245, 248)
BEZEL = (40, 40, 44)
WHITE = (255, 255, 255)
ISLAND = (10, 10, 12)
LABEL = (60, 60, 66)
SUB = (140, 140, 148)

SCALE = 3
W, H = 240, 500          # one phone
PAD = 40
TOP = 110                # room for the title above each phone

PALETTES = [
    ("A  Pastel", "#8FD9B0 / #F4ABAB", (143, 217, 176), (244, 171, 171)),
    ("B  Sage & Clay", "#7FB58C / #D98C82", (127, 181, 140), (217, 140, 130)),
    ("C  Soft system", "#5FC689 / #F26B62", (95, 198, 137), (242, 107, 98)),
]


def font(size):
    return ImageFont.truetype(LATIN, size * SCALE)


def ctext(d, cx, cy, text, fnt, fill):
    b = d.textbbox((0, 0), text, font=fnt)
    d.text((cx * SCALE - (b[2] - b[0]) / 2 - b[0],
            cy * SCALE - (b[3] - b[1]) / 2 - b[1]), text, font=fnt, fill=fill)


cols = len(PALETTES)
CW = W + PAD * 2
total_w = CW * cols
total_h = H + TOP + PAD
img = Image.new("RGB", (total_w * SCALE, total_h * SCALE), BG)
d = ImageDraw.Draw(img)

for i, (name, hexes, green, red) in enumerate(PALETTES):
    ox = i * CW + PAD
    ctext(d, ox + W / 2, 34, name, font(22), LABEL)
    ctext(d, ox + W / 2, 66, hexes, font(15), SUB)

    sx0, sy0, sx1, sy1 = ox, TOP, ox + W, TOP + H
    mid = (sy0 + sy1) / 2
    d.rounded_rectangle([c * SCALE for c in (sx0 - 6, sy0 - 6, sx1 + 6, sy1 + 6)],
                        radius=42 * SCALE, fill=BEZEL)
    d.rounded_rectangle([c * SCALE for c in (sx0, sy0, sx1, mid)], radius=36 * SCALE,
                        fill=green, corners=(True, True, False, False))
    d.rounded_rectangle([c * SCALE for c in (sx0, mid, sx1, sy1)], radius=36 * SCALE,
                        fill=red, corners=(False, False, True, True))
    ctext(d, ox + W / 2, (sy0 + mid) / 2, "Yes", font(52), WHITE)
    ctext(d, ox + W / 2, (mid + sy1) / 2, "No", font(52), WHITE)
    d.rounded_rectangle([c * SCALE for c in (ox + W / 2 - 26, sy0 + 16, ox + W / 2 + 26, sy0 + 30)],
                        radius=7 * SCALE, fill=ISLAND)

img = img.resize((total_w * 2, total_h * 2), Image.LANCZOS)
img.save("docs/palette_options.png")
print("wrote docs/palette_options.png")
