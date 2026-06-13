#!/usr/bin/env python3
"""Render marketing-style mockups of the Yes / No app screen.

These are NOT iOS Simulator captures (this build host has no macOS/Xcode).
They are faithful renders of the same design the SwiftUI code produces: two
full-screen halves — a green "Yes" on top and a red "No" on the bottom — with
a small "Tap to decide" prompt chip on the divider, the real localized
strings, and automatic right-to-left mirroring for RTL languages.

Requires Pillow built with raqm (complex text shaping + bidi).
"""
from PIL import Image, ImageDraw, ImageFont, features

assert features.check("raqm"), "Pillow needs raqm for Arabic/Persian shaping"

# --- Fonts ------------------------------------------------------------------
LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
ARABIC = "/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf"
CJK = "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc"

# --- Palette (Apple system colors, light mode) ------------------------------
BG = (242, 242, 247)
BEZEL = (28, 28, 30)
GREEN = (52, 199, 89)
RED = (255, 59, 48)
WHITE = (255, 255, 255)
ISLAND = (10, 10, 12)
CHIP = (0, 0, 0)

SCALE = 3  # supersample then downscale for crisp anti-aliasing
W, H = 300, 640  # logical screen size (points)


def font(path, size):
    return ImageFont.truetype(path, size * SCALE)


def center_text(draw, cx, cy, text, fnt, fill, rtl=False, anchor=None):
    kw = dict(direction="rtl", language="ar") if rtl else {}
    bbox = draw.textbbox((0, 0), text, font=fnt, **kw)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx * SCALE - w / 2 - bbox[0], cy * SCALE - h / 2 - bbox[1]),
              text, font=fnt, fill=fill, **kw)


def render(filename, *, prompt, yes, no, font_path=LATIN, rtl=False):
    img = Image.new("RGB", (W * SCALE, H * SCALE), BG)
    d = ImageDraw.Draw(img)

    sx0, sy0, sx1, sy1 = 16, 16, W - 16, H - 16
    mid = (sy0 + sy1) / 2
    radius = 40

    # Phone bezel
    d.rounded_rectangle([c * SCALE for c in (10, 10, W - 10, H - 10)],
                        radius=46 * SCALE, fill=BEZEL)

    # Top half = green "Yes" (round only the top screen corners).
    d.rounded_rectangle([c * SCALE for c in (sx0, sy0, sx1, mid)],
                        radius=radius * SCALE, fill=GREEN,
                        corners=(True, True, False, False))
    # Bottom half = red "No" (round only the bottom screen corners).
    d.rounded_rectangle([c * SCALE for c in (sx0, mid, sx1, sy1)],
                        radius=radius * SCALE, fill=RED,
                        corners=(False, False, True, True))

    label = font(font_path, 62)
    center_text(d, W / 2, (sy0 + mid) / 2, yes, label, WHITE, rtl=rtl)
    center_text(d, W / 2, (mid + sy1) / 2, no, label, WHITE, rtl=rtl)

    # "Tap to decide" chip on the divider.
    chip_font = font(font_path, 15 if not rtl else 14)
    kw = dict(direction="rtl", language="ar") if rtl else {}
    bbox = d.textbbox((0, 0), prompt, font=chip_font, **kw)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    px, py = 14, 9
    cw, ch = tw / SCALE + px * 2, th / SCALE + py * 2
    d.rounded_rectangle(
        [c * SCALE for c in (W / 2 - cw / 2, mid - ch / 2, W / 2 + cw / 2, mid + ch / 2)],
        radius=(ch / 2) * SCALE, fill=CHIP)
    center_text(d, W / 2, mid, prompt, chip_font, WHITE, rtl=rtl)

    # Dynamic Island (drawn last so it sits above the green).
    d.rounded_rectangle([c * SCALE for c in (W / 2 - 32, 30, W / 2 + 32, 48)],
                        radius=9 * SCALE, fill=ISLAND)

    img = img.resize((W * 2, H * 2), Image.LANCZOS)
    img.save(filename)
    print("wrote", filename)


render("docs/screenshots/en.png", prompt="Tap to decide", yes="Yes", no="No")
render("docs/screenshots/ar.png", prompt="اضغط لتقرر", yes="نعم", no="لا",
       font_path=ARABIC, rtl=True)
render("docs/screenshots/fa.png", prompt="برای تصمیم‌گیری ضربه بزنید",
       yes="بله", no="خیر", font_path=ARABIC, rtl=True)
render("docs/screenshots/zh-Hans.png", prompt="点击以决定", yes="是", no="否",
       font_path=CJK)
