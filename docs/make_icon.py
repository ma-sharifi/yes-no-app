#!/usr/bin/env python3
"""Generate the 1024x1024 App Store icon.

Matches the app: green "Yes" top half with a check, red "No" bottom half with
a cross. Full-bleed, no transparency, no rounded corners (App Store rounds the
corners itself) — which is exactly what App Store Connect requires.
"""
from PIL import Image, ImageDraw

GREEN = (52, 199, 89)
RED = (255, 59, 48)
WHITE = (255, 255, 255)

S = 1024
img = Image.new("RGB", (S, S), GREEN)
d = ImageDraw.Draw(img)

# Bottom half red.
d.rectangle([0, S // 2, S, S], fill=RED)

lw = 60  # stroke width

# Checkmark in the top (green) half.
cx, cy = S // 2, S // 4
d.line([(cx - 150, cy + 10), (cx - 40, cy + 110), (cx + 165, cy - 120)],
       fill=WHITE, width=lw, joint="curve")

# Cross in the bottom (red) half.
bx, by = S // 2, 3 * S // 4
r = 130
d.line([(bx - r, by - r), (bx + r, by + r)], fill=WHITE, width=lw)
d.line([(bx - r, by + r), (bx + r, by - r)], fill=WHITE, width=lw)

out = "YesNo/Assets.xcassets/AppIcon.appiconset/icon-1024.png"
img.save(out)
print("wrote", out)
