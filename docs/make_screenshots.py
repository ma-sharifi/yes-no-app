#!/usr/bin/env python3
"""Render marketing-style mockups of the Yes / No app screen.

These are NOT iOS Simulator captures (this build host has no macOS/Xcode).
They are faithful renders of the same design the SwiftUI code produces:
system green / red capsule buttons, a centered prompt-or-result, the real
localized strings, and automatic right-to-left mirroring for RTL languages.

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
SCREEN = (255, 255, 255)
BEZEL = (28, 28, 30)
GREEN = (52, 199, 89)
RED = (255, 59, 48)
WHITE = (255, 255, 255)
PRIMARY = (28, 28, 30)
SECONDARY = (142, 142, 147)
ISLAND = (10, 10, 12)

SCALE = 3  # supersample then downscale for crisp anti-aliasing

# Logical screen size (points), roughly an iPhone aspect ratio.
W, H = 300, 640


def font(path, size):
    return ImageFont.truetype(path, size * SCALE)


def rounded(draw, box, radius, fill):
    draw.rounded_rectangle([c * SCALE for c in box], radius=radius * SCALE, fill=fill)


def center_text(draw, cx, cy, text, fnt, fill, rtl=False):
    kw = {}
    if rtl:
        kw = dict(direction="rtl", language="ar")
    bbox = draw.textbbox((0, 0), text, font=fnt, **kw)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    draw.text((cx * SCALE - w / 2 - bbox[0], cy * SCALE - h / 2 - bbox[1]),
              text, font=fnt, fill=fill, **kw)


def render(filename, *, prompt, yes, no, result=None, font_path=LATIN, rtl=False):
    img = Image.new("RGB", (W * SCALE, H * SCALE), BG)
    d = ImageDraw.Draw(img)

    # Phone bezel + screen
    rounded(d, (10, 10, W - 10, H - 10), 46, BEZEL)
    rounded(d, (16, 16, W - 16, H - 16), 40, SCREEN)

    # Dynamic Island
    rounded(d, (W / 2 - 32, 30, W / 2 + 32, 48), 9, ISLAND)

    # Center area: large result if chosen, else the prompt.
    if result is not None:
        center_text(d, W / 2, H * 0.40, result, font(font_path, 96), PRIMARY, rtl=rtl)
    else:
        prompt_font = font(font_path, 24 if not rtl else 22)
        center_text(d, W / 2, H * 0.40, prompt, prompt_font, SECONDARY, rtl=rtl)

    # Two full-width capsule buttons near the bottom.
    pad = 30
    btn_h = 70
    gap = 18
    y_no_top = H - 40 - btn_h
    y_yes_top = y_no_top - gap - btn_h
    label_font = font(font_path, 34)

    rounded(d, (pad, y_yes_top, W - pad, y_yes_top + btn_h), btn_h / 2, GREEN)
    center_text(d, W / 2, y_yes_top + btn_h / 2, yes, label_font, WHITE, rtl=rtl)

    rounded(d, (pad, y_no_top, W - pad, y_no_top + btn_h), btn_h / 2, RED)
    center_text(d, W / 2, y_no_top + btn_h / 2, no, label_font, WHITE, rtl=rtl)

    img = img.resize((W * 2, H * 2), Image.LANCZOS)
    img.save(filename)
    print("wrote", filename)


render("docs/screenshots/en.png",
       prompt="Tap to decide", yes="Yes", no="No")

render("docs/screenshots/ar.png",
       prompt="اضغط لتقرر", yes="نعم", no="لا",
       result="نعم", font_path=ARABIC, rtl=True)

render("docs/screenshots/fa.png",
       prompt="برای تصمیم‌گیری ضربه بزنید", yes="بله", no="خیر",
       font_path=ARABIC, rtl=True)

render("docs/screenshots/zh-Hans.png",
       prompt="点击以决定", yes="是", no="否", font_path=CJK)
