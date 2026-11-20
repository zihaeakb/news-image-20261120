#!/usr/bin/env python3
"""Draw the news-image-20261120 entry: a 1024x1024 newspaper front page.

Eight stories from Friday 20 November 2026, drawn with PIL (Noto Serif
Black headlines, Noto Sans body) so every word is pixel-perfect — no
AI-generated text. Renders to entry.png (1024x1024, under 1 MiB).

Usage: python3 draw.py [output.png]   (default: entry.png next to this file)
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/noto/"

# Palette (matched to the v2 front page)
BG = (247, 243, 232)        # warm cream paper
NAVY = (27, 42, 74)         # masthead / icon ink
NAVY_DARK = (22, 34, 60)
GOLD = (201, 162, 39)       # masthead rule / date / headline underline
GOLD_DARK = (180, 140, 30)
RED = (185, 28, 28)         # kickers / chart line
INK = (17, 24, 39)          # headlines
BODY = (51, 51, 51)         # summary text
GRAY = (100, 110, 125)      # footer
CARD = (255, 255, 255)      # card fill
CARD_EDGE = (213, 220, 230) # card border
TILE = (232, 237, 243)      # icon tile fill
GREEN = (46, 125, 50)       # small accent (leaf)
ORANGE = (234, 130, 20)     # flame / burst accent
YELLOW = (245, 190, 40)     # inner flame / pivot dot


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_BLACK = "NotoSerif-Black.ttf"
SERIF_BOLD = "NotoSerif-Bold.ttf"
SANS = "NotoSans-Regular.ttf"
SANS_BOLD = "NotoSans-Bold.ttf"
SANS_BLACK = "NotoSans-Black.ttf"


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_lines(draw, x, y, lines, fnt, fill, leading):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


# ---------------------------------------------------------------- icons
# Each takes (draw, x, y, s) where (x, y) is the tile's top-left and s is
# the tile size. Icons are navy line art with gold/red/orange accents.

def icon_scales(d, x, y, s):
    """Scales of justice (lead)."""
    cx, top = x + s // 2, y + int(s * 0.10)
    base_y = y + int(s * 0.86)
    # base
    d.polygon([(cx - s * 0.16, base_y), (cx + s * 0.16, base_y),
               (cx + s * 0.10, base_y - s * 0.07),
               (cx - s * 0.10, base_y - s * 0.07)], fill=NAVY)
    # post
    d.line([(cx, top + s * 0.06), (cx, base_y - s * 0.07)],
           fill=NAVY, width=max(3, s // 28))
    # beam
    d.line([(x + s * 0.08, top + s * 0.06), (x + s * 0.92, top + s * 0.06)],
           fill=NAVY, width=max(3, s // 24))
    # pivot dot
    r = max(4, s // 22)
    d.ellipse([cx - r, top + s * 0.06 - r, cx + r, top + s * 0.06 + r],
              fill=GOLD)
    # pans
    for side in (-1, 1):
        px = cx + side * s * 0.36
        d.line([(px, top + s * 0.06), (px, top + s * 0.52)],
               fill=NAVY, width=max(2, s // 40))
        d.line([(px - s * 0.13, top + s * 0.52), (px + s * 0.13, top + s * 0.52)],
               fill=NAVY, width=max(2, s // 40))
        d.arc([px - s * 0.13, top + s * 0.40, px + s * 0.13, top + s * 0.66],
              0, 180, fill=NAVY, width=max(3, s // 28))


def icon_globe(d, x, y, s):
    """Globe with three dots (summit)."""
    cx, cy, r = x + s // 2, y + s // 2, int(s * 0.36)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=NAVY,
              width=max(3, s // 26))
    d.ellipse([cx - int(r * 0.45), cy - r, cx + int(r * 0.45), cy + r],
              outline=NAVY, width=max(2, s // 40))
    d.line([(cx - r, cy), (cx + r, cy)], fill=NAVY, width=max(2, s // 40))
    d.arc([cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)],
          200, 340, fill=NAVY, width=max(2, s // 40))
    d.arc([cx - r, cy - int(r * 0.55), cx + r, cy + int(r * 0.55)],
          20, 160, fill=NAVY, width=max(2, s // 40))
    for dx, dy, col in ((-0.45, -0.35, (37, 99, 235)),
                        (0.42, -0.42, RED),
                        (0.30, 0.45, (120, 125, 135))):
        px, py = cx + int(r * dx), cy + int(r * dy)
        rr = max(3, s // 24)
        d.ellipse([px - rr, py - rr, px + rr, py + rr], fill=col)


def icon_bridge(d, x, y, s):
    """Bridge with an explosion starburst above (Kyiv)."""
    base = y + int(s * 0.78)
    # towers
    for tx in (x + int(s * 0.22), x + int(s * 0.62)):
        d.rectangle([tx, y + int(s * 0.34), tx + int(s * 0.10), base],
                    fill=NAVY)
    # deck
    d.line([(x + s * 0.08, base), (x + s * 0.92, base)],
           fill=NAVY, width=max(3, s // 24))
    # cables
    d.line([(x + int(s * 0.27), y + int(s * 0.34)), (x + int(s * 0.50), base)], fill=NAVY, width=max(2, s // 40))
    d.line([(x + int(s * 0.67), y + int(s * 0.34)), (x + int(s * 0.50), base)], fill=NAVY, width=max(2, s // 40))
    # starburst
    cx, cy, r1, r2 = x + s // 2, y + int(s * 0.20), int(s * 0.20), int(s * 0.09)
    import math
    pts = []
    for i in range(16):
        ang = math.pi * i / 8 - math.pi / 2
        r = r1 if i % 2 == 0 else r2
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=ORANGE)
    d.ellipse([cx - r2 // 2, cy - r2 // 2, cx + r2 // 2, cy + r2 // 2],
              fill=YELLOW)


def icon_tower(d, x, y, s):
    """Tapered tower with spire and a burst (Riyadh)."""
    cx = x + int(s * 0.38)
    base = y + int(s * 0.86)
    top = y + int(s * 0.18)
    # tapered tower
    d.polygon([(cx - int(s * 0.16), base), (cx + int(s * 0.16), base),
               (cx + int(s * 0.07), top), (cx - int(s * 0.07), top)],
              fill=NAVY)
    # spire
    d.polygon([(cx - 2, top), (cx + 2, top), (cx, top - int(s * 0.10))],
              fill=NAVY)
    # floor lines
    for f in (0.30, 0.48, 0.66):
        fy = top + int((base - top) * f)
        w = int(s * (0.16 - 0.09 * f))
        d.line([(cx - w, fy), (cx + w, fy)], fill=(255, 255, 255),
               width=max(2, s // 44))
    # burst top-right
    import math
    bx, by = x + int(s * 0.74), y + int(s * 0.26)
    r1, r2 = int(s * 0.15), int(s * 0.07)
    pts = []
    for i in range(16):
        ang = math.pi * i / 8 - math.pi / 2
        r = r1 if i % 2 == 0 else r2
        pts.append((bx + r * math.cos(ang), by + r * math.sin(ang)))
    d.polygon(pts, fill=ORANGE)


def icon_tanker(d, x, y, s):
    """Tanker with flame above and waves below (Hormuz)."""
    # flame (teardrop)
    fx, fy = x + int(s * 0.52), y + int(s * 0.16)
    fr = int(s * 0.11)
    d.polygon([(fx, fy - fr), (fx + fr, fy + int(fr * 0.7)),
               (fx, fy + int(fr * 1.1)), (fx - fr, fy + int(fr * 0.7))],
              fill=ORANGE)
    d.polygon([(fx, fy - int(fr * 0.4)), (fx + int(fr * 0.55), fy + int(fr * 0.7)),
               (fx, fy + int(fr * 0.9)), (fx - int(fr * 0.55), fy + int(fr * 0.7))],
              fill=YELLOW)
    # hull (trapezoid, wider at top)
    hy = y + int(s * 0.44)
    d.polygon([(x + int(s * 0.06), hy), (x + int(s * 0.94), hy),
               (x + int(s * 0.84), hy + int(s * 0.22)),
               (x + int(s * 0.16), hy + int(s * 0.22))], fill=NAVY)
    # deck line + superstructure
    d.line([(x + int(s * 0.10), hy), (x + int(s * 0.90), hy)],
           fill=(255, 255, 255), width=max(2, s // 44))
    d.rectangle([x + int(s * 0.68), hy - int(s * 0.14),
                 x + int(s * 0.86), hy], fill=NAVY)
    d.line([(x + int(s * 0.72), hy - int(s * 0.14)), (x + int(s * 0.72), hy - int(s * 0.22))], fill=NAVY,
           width=max(2, s // 44))
    # waves
    for wy in (0.74, 0.84):
        yy = y + int(s * wy)
        d.arc([x + int(s * 0.10), yy, x + int(s * 0.45), yy + int(s * 0.10)],
              180, 360, fill=NAVY, width=max(2, s // 44))
        d.arc([x + int(s * 0.55), yy, x + int(s * 0.90), yy + int(s * 0.10)],
              180, 360, fill=NAVY, width=max(2, s // 44))


def icon_missile(d, x, y, s):
    """Cruise missile flying right with a dashed path (Poland)."""
    cy = y + int(s * 0.52)
    # dashed flight path (arc above)
    for i in range(9):
        t0 = 0.15 + i * 0.075
        t1 = t0 + 0.045
        x0 = x + int(s * t0)
        x1 = x + int(s * t1)
        y0 = y + int(s * (0.30 - 0.10 * ((t0 - 0.5) ** 2) * 4))
        y1 = y + int(s * (0.30 - 0.10 * ((t1 - 0.5) ** 2) * 4))
        d.line([(x0, y0), (x1, y1)], fill=NAVY, width=max(2, s // 44))
    # body
    bx0, bx1 = x + int(s * 0.14), x + int(s * 0.78)
    bh = max(5, s // 12)
    d.rectangle([bx0, cy - bh // 2, bx1, cy + bh // 2], fill=NAVY)
    # nose
    d.polygon([(bx1, cy - bh // 2), (bx1, cy + bh // 2),
               (bx1 + int(s * 0.14), cy)], fill=NAVY)
    # tail fins
    d.polygon([(bx0, cy - bh // 2), (bx0 - int(s * 0.10), cy - int(s * 0.20)),
               (bx0 + int(s * 0.07), cy - bh // 2)], fill=NAVY)
    d.polygon([(bx0, cy + bh // 2), (bx0 - int(s * 0.10), cy + int(s * 0.20)),
               (bx0 + int(s * 0.07), cy + bh // 2)], fill=NAVY)
    # tail flame
    d.polygon([(bx0, cy - bh // 2), (bx0, cy + bh // 2),
               (bx0 - int(s * 0.12), cy)], fill=ORANGE)


def icon_thermometer(d, x, y, s):
    """Thermometer, mercury high (COP31 overshoot)."""
    cx = x + s // 2
    top = y + int(s * 0.12)
    bot = y + int(s * 0.72)
    w = max(6, s // 9)
    # tube
    d.rounded_rectangle([cx - w // 2, top, cx + w // 2, bot],
                        radius=w // 2, outline=NAVY, width=max(3, s // 28))
    # bulb
    br = int(s * 0.14)
    d.ellipse([cx - br, bot - br // 2, cx + br, bot + br // 2],
              outline=NAVY, width=max(3, s // 28), fill=RED)
    # mercury (up to ~70% of tube)
    mh = int((bot - top) * 0.70)
    d.rectangle([cx - w // 4, bot - mh, cx + w // 4, bot], fill=RED)
    d.ellipse([cx - br // 2, bot - br // 2, cx + br // 2, bot + br // 2],
              fill=RED)
    # tick marks
    for i in range(4):
        ty = top + int((bot - top) * (0.2 + i * 0.2))
        d.line([(cx + w // 2 + 2, ty), (cx + w // 2 + int(s * 0.10), ty)],
               fill=NAVY, width=max(2, s // 44))


def icon_chart(d, x, y, s, pct="-4.8%"):
    """Declining market chart with red pct label (Markets)."""
    # axes
    ax, ay = x + int(s * 0.12), y + int(s * 0.62)
    d.line([(ax, y + int(s * 0.10)), (ax, ay)], fill=NAVY, width=max(2, s // 40))
    d.line([(ax, ay), (x + int(s * 0.88), ay)], fill=NAVY, width=max(2, s // 40))
    # declining polyline
    pts = [(x + int(s * 0.14), y + int(s * 0.22)),
           (x + int(s * 0.32), y + int(s * 0.30)),
           (x + int(s * 0.48), y + int(s * 0.26)),
           (x + int(s * 0.64), y + int(s * 0.44)),
           (x + int(s * 0.82), y + int(s * 0.56))]
    d.line(pts, fill=RED, width=max(3, s // 26), joint="curve")
    # arrowhead
    ex, ey = pts[-1]
    d.polygon([(ex, ey), (ex - int(s * 0.09), ey - int(s * 0.02)),
               (ex - int(s * 0.03), ey + int(s * 0.08))], fill=RED)
    # pct label
    fnt = font(SANS_BOLD, max(14, int(s * 0.20)))
    tw = d.textlength(pct, font=fnt)
    d.text((x + (s - tw) / 2, y + int(s * 0.68)), pct, font=fnt, fill=RED)


# ---------------------------------------------------------------- cards

def draw_card(d, x, y, w, h, icon, kicker, headline, summary,
              icon_s, kick_size, head_size, body_size, head_lines=2):
    """One story card: white rounded rect, icon tile left, text right."""
    d.rounded_rectangle([x, y, x + w, y + h], radius=10,
                        fill=CARD, outline=CARD_EDGE, width=2)
    # icon tile
    tx, ty = x + 12, y + 12
    d.rounded_rectangle([tx, ty, tx + icon_s, ty + icon_s], radius=8,
                        fill=TILE)
    icon(d, tx, ty, icon_s)
    # text
    txx = tx + icon_s + 12
    tw = x + w - 12 - txx
    yy = y + 12
    kf = font(SANS_BOLD, kick_size)
    d.text((txx, yy), kicker, font=kf, fill=RED)
    yy += int(kick_size * 1.35)
    hf = font(SERIF_BLACK, head_size)
    hlines = wrap(d, headline, hf, tw)[:head_lines]
    yy = text_lines(d, txx, yy, hlines, hf, INK, int(head_size * 1.08))
    yy += 4
    bf = font(SANS, body_size)
    blines = wrap(d, summary, bf, tw)
    text_lines(d, txx, yy, blines, bf, BODY, int(body_size * 1.28))
    return y + h


def build(out_path):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- masthead (navy band, full bleed)
    d.rectangle([0, 0, W, 96], fill=NAVY)
    d.text((28, 12), "THE WORLD", font=font(SERIF_BLACK, 56), fill=(255, 255, 255))
    date = "FRIDAY \u2022 20 NOVEMBER 2026"
    df = font(SANS_BOLD, 26)
    d.text((W - 28 - d.textlength(date, font=df), 26), date, font=df, fill=GOLD)
    d.text((28, 70), "ONE DAY \u2022 EIGHT STORIES THAT DEFINED IT",
           font=font(SANS, 18), fill=(210, 215, 225))
    d.rectangle([0, 96, W, 100], fill=GOLD)

    # ---- lead story (full width)
    lead_y, lead_h = 112, 252
    d.rounded_rectangle([12, lead_y, W - 12, lead_y + lead_h], radius=10,
                        fill=CARD, outline=CARD_EDGE, width=2)
    # lead icon tile
    tx, ty, ts = 30, lead_y + 18, 200
    d.rounded_rectangle([tx, ty, tx + ts, ty + ts], radius=8, fill=TILE)
    icon_scales(d, tx, ty, ts)
    # lead text
    txx = tx + ts + 20
    tw = W - 12 - 16 - txx
    yy = lead_y + 14
    d.text((txx, yy), "THE HAGUE \u2022 WORLD COURT",
           font=font(SANS_BOLD, 20), fill=RED)
    yy += 28
    hf = font(SERIF_BLACK, 44)
    hlines = wrap(d, "MYANMAR GUILTY OF ROHINGYA GENOCIDE", hf, tw)
    yy = text_lines(d, txx, yy, hlines, hf, INK, 48)
    # gold underline under headline
    d.rectangle([txx, yy + 2, txx + 120, yy + 7], fill=GOLD)
    yy += 16
    bf = font(SANS, 22)
    blines = wrap(
        d,
        "The International Court of Justice rules 9-6 \u2014 the first genocide "
        "finding against a state. Some 10,000 Rohingya were killed in 2016-17; "
        "400 villages destroyed. The court ordered reparations and prosecution.",
        bf, tw)
    text_lines(d, txx, yy, blines, bf, BODY, 28)

    # ---- navy divider
    d.rectangle([12, 376, W - 12, 379], fill=NAVY)

    # ---- Row A: 2 cards (Shenzhen, Kyiv)
    y = 390
    card_w, card_h = 486, 180
    draw_card(d, 12, y, card_w, card_h, icon_globe,
              "SHENZHEN \u2022 SUMMIT",
              "Trump, Xi & Putin sign peace pledge",
              "First three-way summit ends in a 4-point declaration \u2014 no "
              "breakthrough on Ukraine or Iran. Trump: '12' out of 10.",
              100, 19, 28, 18)
    draw_card(d, 12 + card_w + 16, y, card_w, card_h, icon_bridge,
              "KYIV \u2022 WAR",
              "Russia strikes Kyiv overnight",
              "110+ missiles and 400+ drones; 3 Dnipro bridges hit. "
              "8 killed, 28 hurt across nine regions.",
              100, 19, 28, 18)

    # ---- Row B: 3 cards (Riyadh, Hormuz, Poland)
    y = 580
    card_w, card_h = 317, 194
    draw_card(d, 12, y, card_w, card_h, icon_tower,
              "RIYADH \u2022 MIDDLE EAST",
              "Missile hits Riyadh tower",
              "Blast damages the 80-storey PIF Tower, the capital's tallest. "
              "No injuries; district evacuated.",
              92, 16, 22, 16)
    draw_card(d, 12 + card_w + 16, y, card_w, card_h, icon_tanker,
              "HORMUZ \u2022 TANKER",
              "Tanker ablaze off Oman",
              "Projectile strike 8 miles off Khasab; no casualties. "
              "Iran's mine claim is unverified.",
              92, 16, 22, 16)
    draw_card(d, 12 + 2 * (card_w + 16), y, card_w, card_h, icon_missile,
              "POLAND \u2022 NATO AIRSPACE",
              "Missiles breach NATO airspace",
              "A Kh-101 spent 3 minutes over Poland; F-16s scrambled. "
              "Tusk: 'intentional provocation'.",
              92, 16, 22, 16)

    # ---- Row C: 2 cards (COP31, Markets)
    y = 784
    card_w, card_h = 486, 180
    draw_card(d, 12, y, card_w, card_h, icon_thermometer,
              "ANTALYA \u2022 COP31",
              "COP31 drops fossil fuels",
              "Draft strips all phase-out language; first COP to admit the "
              "1.5\u00b0C overshoot. Talks run into overtime.",
              100, 19, 28, 18)
    draw_card(d, 12 + card_w + 16, y, card_w, card_h, icon_chart,
              "MARKETS \u2022 ECONOMY",
              "Nikkei dives 4.8% as stocks slide",
              "Stocks slide again; SoftBank -16%. Anthropic jumps 17% on a "
              "record $81B Nasdaq debut.",
              100, 19, 28, 18)

    # ---- footer
    ff = font(SANS, 18)
    foot = "THE WORLD \u2022 FRIDAY, 20 NOVEMBER 2026 \u2022 EIGHT STORIES THAT DEFINED THE DAY"
    d.text(((W - d.textlength(foot, font=ff)) / 2, 978), foot, font=ff, fill=GRAY)

    img.save(out_path, "PNG", optimize=True)
    return out_path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    build(out)
    print("wrote", out)
