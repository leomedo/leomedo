# -*- coding: utf-8 -*-
"""Draws the LinkedIn banner (1584x396) in the same palette as the GitHub hero.

LinkedIn banners are static images, so this renders straight to PNG rather than
going through SVG. The bottom-left is deliberately left quiet: the profile photo
overlaps there on desktop, and mobile crops in toward the centre.
"""
import math
import pathlib

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

W, H = 1584, 396
FONTS = "C:/Windows/Fonts/"

# shared with gen_hero.py
BG0, BG1, BG2 = (8, 12, 24), (17, 26, 51), (10, 16, 36)
A1, A2, A3 = (108, 140, 255), (53, 214, 164), (255, 184, 107)
NAME, MUTED, SUB = (242, 246, 255), (147, 162, 198), (220, 228, 247)
GRID = (124, 141, 181)

SAFE_X = 470          # keep everything left of this clear for the profile photo
HUB = (1372, 178)     # constellation centre


def f(name, size):
    return ImageFont.truetype(FONTS + name, size)


def lerp(a, b, t):
    return tuple(int(round(a[i] + (b[i] - a[i]) * t)) for i in range(3))


def background():
    """Diagonal three-stop gradient, drawn per row then sheared by column."""
    img = Image.new("RGB", (W, H))
    px = img.load()
    for y in range(H):
        for x in range(0, W, 8):
            t = (x / W * 0.55) + (y / H * 0.45)
            c = lerp(BG0, BG1, t / 0.55) if t < 0.55 else lerp(BG1, BG2, (t - 0.55) / 0.45)
            for dx in range(8):
                if x + dx < W:
                    px[x + dx, y] = c
    return img


def add_glow(img, centre, radius, colour, strength):
    """Additive bloom: a blurred ellipse screened over the background."""
    layer = Image.new("RGB", (W, H), (0, 0, 0))
    cx, cy = centre
    ImageDraw.Draw(layer).ellipse(
        [cx - radius, cy - radius * 0.66, cx + radius, cy + radius * 0.66],
        fill=tuple(int(c * strength) for c in colour),
    )
    return ImageChops.add(img, layer.filter(ImageFilter.GaussianBlur(radius * 0.42)))


def main():
    img = background()

    # ambient glows
    for centre, r, col, s in (((240, 70), 430, A1, 0.16), ((1330, 330), 400, A2, 0.14)):
        img = add_glow(img, centre, r, col, s)

    d = ImageDraw.Draw(img, "RGBA")

    # grid
    for x in range(0, W + 1, 44):
        d.line([(x, 0), (x, H)], fill=GRID + (26,), width=1)
    for y in range(0, H + 1, 44):
        d.line([(0, y), (W, y)], fill=GRID + (26,), width=1)

    # constellation: one hub, six tenants
    hx, hy, r = HUB[0], HUB[1], 78
    for i in range(6):
        ang = math.radians(-90 + i * 60)
        nx, ny = hx + r * math.cos(ang), hy + r * math.sin(ang)
        d.line([(hx, hy), (nx, ny)], fill=A2 + (120,), width=2)
        d.ellipse([nx - 7, ny - 7, nx + 7, ny + 7], fill=A1)
    d.ellipse([hx - 23, hy - 23, hx + 23, hy + 23], outline=A2, width=3)
    d.ellipse([hx - 10, hy - 10, hx + 10, hy + 10], fill=A2)

    # ---- type ----------------------------------------------------------------
    d.line([(SAFE_X, 118), (SAFE_X + 38, 118)], fill=A2, width=3)
    d.text((SAFE_X + 54, 110), "BACKEND SOFTWARE ENGINEER",
           font=f("segoeui.ttf", 17), fill=A2, anchor="lm")

    d.text((SAFE_X, 172), "Multi-tenant SaaS,", font=f("segoeuib.ttf", 50), fill=NAME, anchor="lm")
    d.text((SAFE_X, 228), "shipped and enforced.", font=f("segoeuib.ttf", 50), fill=NAME, anchor="lm")

    d.text((SAFE_X, 279), "Python  \u00b7  Frappe / ERPNext  \u00b7  Stripe billing  \u00b7  ETA & ZATCA e-invoicing",
           font=f("segoeui.ttf", 21), fill=SUB, anchor="lm")

    d.text((SAFE_X, 316), "Giza, Egypt   \u00b7   github.com/leomedo   \u00b7   open to remote",
           font=f("consola.ttf", 17), fill=MUTED, anchor="lm")

    # accent rule along the bottom
    for x in range(W):
        t = x / W
        col = lerp(A1, A2, t / 0.5) if t < 0.5 else lerp(A2, A3, (t - 0.5) / 0.5)
        d.line([(x, H - 5), (x, H)], fill=col, width=1)

    out = pathlib.Path("assets/linkedin-banner.png")
    out.parent.mkdir(exist_ok=True)
    img.save(out, "PNG", optimize=True)
    print("wrote {}  {}x{}  ({:,} bytes)".format(out, img.width, img.height, out.stat().st_size))


if __name__ == "__main__":
    main()
