#!/usr/bin/env python3
"""Render the entry image for make.fun's 17 November 2026 world-news bounty.

The layout is a one-page news poster: a masthead naming the day, ten story
cards in two columns, and a short ticker of further events. Everything is
drawn with Pillow primitives; no external assets or network are used.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W = 1024
S = 2  # render at 2048 px, then downsample for clean edges
CANVAS = W * S

BG = "#f4ecdc"
INK = "#172033"
MUTED = "#5d6675"
HEADER = "#111827"
GOLD = "#e0b354"
RED = "#b42318"
CARD = "#fffaf1"
BORDER = "#d8cbb2"

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_BOLD = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_BOLD = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, px):
    return ImageFont.truetype(path, px * S)


def wrap(text, f, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        candidate = word if not current else current + " " + word
        if f.getlength(candidate) <= max_width:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def paragraph(draw, text, f, x, y, max_width, line_height, fill, max_lines=None):
    lines = wrap(text, f, max_width)
    if max_lines is not None:
        lines = lines[:max_lines]
    for i, line in enumerate(lines):
        draw.text((x * S, (y + i * line_height) * S), line, font=f, fill=fill)
    return len(lines)


def rr(draw, box, radius, fill=None, outline=None, width=1):
    x1, y1, x2, y2 = [v * S for v in box]
    draw.rounded_rectangle((x1, y1, x2, y2), radius=radius * S, fill=fill, outline=outline, width=width * S)


def line(draw, xy, fill, width=2):
    draw.line([(xy[0] * S, xy[1] * S), (xy[2] * S, xy[3] * S)], fill=fill, width=width * S)


def ellipse(draw, box, fill=None, outline=None, width=2):
    x1, y1, x2, y2 = [v * S for v in box]
    draw.ellipse((x1, y1, x2, y2), fill=fill, outline=outline, width=width * S)


def polygon(draw, pts, fill=None, outline=None, width=2):
    draw.polygon([(x * S, y * S) for x, y in pts], fill=fill, outline=outline, width=width * S)


def star(draw, cx, cy, r, fill=RED, points=8):
    import math
    pts = []
    for i in range(points * 2):
        ang = -math.pi / 2 + i * math.pi / points
        rr_ = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr_ * math.cos(ang), cy + rr_ * math.sin(ang)))
    polygon(draw, pts, fill=fill)


# --- icons ---------------------------------------------------------------
def icon_bridge(d, x, y, z):
    # water
    d.rectangle((x * S, (y + z * 0.62) * S, (x + z) * S, (y + z) * S), fill="#d9e7ef")
    for k in range(3):
        yy = y + z * (0.70 + 0.1 * k)
        line(d, (x + z * 0.03, yy, x + z * 0.97, yy), "#8aa9bd", 1)
    # bridge deck and towers
    line(d, (x + z * 0.03, y + z * 0.42, x + z * 0.97, y + z * 0.42), "#445266", 4)
    line(d, (x + z * 0.28, y + z * 0.16, x + z * 0.28, y + z * 0.66), "#445266", 3)
    line(d, (x + z * 0.72, y + z * 0.16, x + z * 0.72, y + z * 0.66), "#445266", 3)
    d.arc(((x + z * 0.12) * S, (y + z * 0.12) * S, (x + z * 0.88) * S, (y + z * 0.82) * S),
          start=180, end=360, fill="#445266", width=2 * S)
    star(d, x + z * 0.50, y + z * 0.30, z * 0.16)


def icon_drone(d, x, y, z):
    # drone body and rotors
    polygon(d, [(x + z * 0.28, y + z * 0.30), (x + z * 0.5, y + z * 0.18),
                (x + z * 0.72, y + z * 0.30), (x + z * 0.5, y + z * 0.42)], fill="#334155")
    line(d, (x + z * 0.28, y + z * 0.30, x + z * 0.12, y + z * 0.16), "#334155", 2)
    line(d, (x + z * 0.72, y + z * 0.30, x + z * 0.88, y + z * 0.16), "#334155", 2)
    ellipse(d, (x + z * 0.05, y + z * 0.10, x + z * 0.19, y + z * 0.22), outline="#334155", width=2)
    ellipse(d, (x + z * 0.81, y + z * 0.10, x + z * 0.95, y + z * 0.22), outline="#334155", width=2)
    # missile trail and burst
    line(d, (x + z * 0.10, y + z * 0.66, x + z * 0.42, y + z * 0.52), "#b42318", 3)
    star(d, x + z * 0.78, y + z * 0.58, z * 0.14)
    # radar arcs
    d.arc(((x + z * 0.35) * S, (y + z * 0.45) * S, (x + z * 0.65) * S, (y + z * 0.75) * S),
          start=200, end=340, fill="#1d4ed8", width=2 * S)


def icon_gaza(d, x, y, z):
    # broken house
    polygon(d, [(x + z * 0.10, y + z * 0.46), (x + z * 0.50, y + z * 0.20),
                (x + z * 0.90, y + z * 0.46), (x + z * 0.90, y + z * 0.82),
                (x + z * 0.10, y + z * 0.82)], fill="#e8e2d2", outline="#445266", width=2)
    d.rectangle(((x + z * 0.24) * S, (y + z * 0.55) * S, (x + z * 0.38) * S, (y + z * 0.82) * S), fill="#445266")
    line(d, (x + z * 0.55, y + z * 0.40, x + z * 0.68, y + z * 0.64), "#b42318", 3)
    star(d, x + z * 0.66, y + z * 0.56, z * 0.12)
    # olive sprig
    line(d, (x + z * 0.08, y + z * 0.94, x + z * 0.42, y + z * 0.94), "#15803d", 2)
    for k in range(3):
        ellipse(d, (x + z * (0.14 + k * 0.10) - z * 0.04, y + z * 0.90,
                    x + z * (0.14 + k * 0.10) + z * 0.04, y + z * 0.94), fill="#15803d")


def icon_disasters(d, x, y, z):
    # plane
    polygon(d, [(x + z * 0.08, y + z * 0.30), (x + z * 0.44, y + z * 0.30),
                (x + z * 0.50, y + z * 0.20), (x + z * 0.54, y + z * 0.30),
                (x + z * 0.52, y + z * 0.38), (x + z * 0.12, y + z * 0.38)], fill="#334155")
    line(d, (x + z * 0.22, y + z * 0.30, x + z * 0.10, y + z * 0.12), "#334155", 2)
    line(d, (x + z * 0.38, y + z * 0.30, x + z * 0.50, y + z * 0.12), "#334155", 2)
    # train
    rr(d, (x + z * 0.10, y + z * 0.60, x + z * 0.82, y + z * 0.88), z * 0.05, fill="#dbeafe", outline="#1d4ed8", width=2)
    d.rectangle(((x + z * 0.18) * S, (y + z * 0.66) * S, (x + z * 0.30) * S, (y + z * 0.74) * S), fill="#1d4ed8")
    d.rectangle(((x + z * 0.34) * S, (y + z * 0.66) * S, (x + z * 0.46) * S, (y + z * 0.74) * S), fill="#1d4ed8")
    d.rectangle(((x + z * 0.50) * S, (y + z * 0.66) * S, (x + z * 0.62) * S, (y + z * 0.74) * S), fill="#1d4ed8")
    ellipse(d, (x + z * 0.18, y + z * 0.84, x + z * 0.26, y + z * 0.92), fill="#334155")
    ellipse(d, (x + z * 0.62, y + z * 0.84, x + z * 0.70, y + z * 0.92), fill="#334155")


def icon_measles(d, x, y, z):
    cx, cy, r = x + z * 0.5, y + z * 0.5, z * 0.26
    import math
    for i in range(12):
        ang = i * math.pi / 6
        x1, y1 = cx + r * math.cos(ang), cy + r * math.sin(ang)
        x2, y2 = cx + (r * 1.35) * math.cos(ang), cy + (r * 1.35) * math.sin(ang)
        line(d, (x1, y1, x2, y2), "#b42318", 2)
    ellipse(d, (cx - r, cy - r, cx + r, cy + r), fill="#fecaca", outline="#b42318", width=3)
    for dx, dy in [(-0.12, -0.1), (0.1, 0.12), (-0.08, 0.18)]:
        ellipse(d, (cx + dx * z - z * 0.045, cy + dy * z - z * 0.045,
                    cx + dx * z + z * 0.045, cy + dy * z + z * 0.045), fill="#b42318")


def icon_bangladesh(d, x, y, z):
    # factory blocks and smoke
    rr(d, (x + z * 0.08, y + z * 0.50, x + z * 0.52, y + z * 0.88), z * 0.04, fill="#dbeafe", outline="#1d4ed8", width=2)
    rr(d, (x + z * 0.56, y + z * 0.60, x + z * 0.92, y + z * 0.88), z * 0.04, fill="#dbeafe", outline="#1d4ed8", width=2)
    line(d, (x + z * 0.18, y + z * 0.50, x + z * 0.18, y + z * 0.28), "#1d4ed8", 3)
    line(d, (x + z * 0.34, y + z * 0.60, x + z * 0.34, y + z * 0.30), "#1d4ed8", 3)
    for k in range(2):
        ellipse(d, (x + z * (0.14 + k * 0.17) - z * 0.06, y + z * 0.18,
                    x + z * (0.14 + k * 0.17) + z * 0.06, y + z * 0.30), fill="#9ca3af")
    # protest flag/fist
    line(d, (x + z * 0.72, y + z * 0.62, x + z * 0.72, y + z * 0.28), "#b42318", 3)
    polygon(d, [(x + z * 0.72, y + z * 0.28), (x + z * 0.94, y + z * 0.34),
                (x + z * 0.72, y + z * 0.42)], fill="#b42318")


def icon_trade(d, x, y, z):
    # container ship
    polygon(d, [(x + z * 0.05, y + z * 0.62), (x + z * 0.95, y + z * 0.62),
                (x + z * 0.86, y + z * 0.86), (x + z * 0.14, y + z * 0.86)], fill="#1e3a5f")
    for i in range(4):
        rr(d, (x + z * (0.16 + i * 0.14), y + z * 0.48, x + z * (0.28 + i * 0.14), y + z * 0.60),
           z * 0.02, fill=["#b42318", "#e0b354", "#1d4ed8", "#15803d"][i])
    line(d, (x + z * 0.05, y + z * 0.30, x + z * 0.42, y + z * 0.30), "#334155", 3)
    polygon(d, [(x + z * 0.42, y + z * 0.22), (x + z * 0.58, y + z * 0.30),
                (x + z * 0.42, y + z * 0.38)], fill="#334155")
    ellipse(d, (x + z * 0.72, y + z * 0.18, x + z * 0.92, y + z * 0.38), outline="#334155", width=2)


def icon_politics(d, x, y, z):
    # ballot box
    rr(d, (x + z * 0.08, y + z * 0.42, x + z * 0.52, y + z * 0.88), z * 0.04, fill="#ede9fe", outline="#6d28d9", width=2)
    d.rectangle(((x + z * 0.18) * S, (y + z * 0.36) * S, (x + z * 0.42) * S, (y + z * 0.46) * S), fill="#fffaf1", outline="#6d28d9", width=2)
    line(d, (x + z * 0.30, y + z * 0.34, x + z * 0.30, y + z * 0.20), "#6d28d9", 3)
    # parliament columns
    for k in range(3):
        xx = x + z * (0.62 + k * 0.10)
        line(d, (xx, y + z * 0.55, xx, y + z * 0.88), "#334155", 3)
        polygon(d, [(xx - z * 0.04, y + z * 0.55), (xx + z * 0.04, y + z * 0.55),
                    (xx, y + z * 0.44)], fill="#334155")


def icon_diplomacy(d, x, y, z):
    # two hands meeting
    polygon(d, [(x + z * 0.04, y + z * 0.55), (x + z * 0.36, y + z * 0.42),
                (x + z * 0.48, y + z * 0.56), (x + z * 0.18, y + z * 0.72)], fill="#f5d6c6", outline="#92400e", width=2)
    polygon(d, [(x + z * 0.96, y + z * 0.55), (x + z * 0.64, y + z * 0.42),
                (x + z * 0.52, y + z * 0.56), (x + z * 0.82, y + z * 0.72)], fill="#f5d6c6", outline="#92400e", width=2)
    # rare-earth crystal
    polygon(d, [(x + z * 0.66, y + z * 0.10), (x + z * 0.86, y + z * 0.24),
                (x + z * 0.76, y + z * 0.40), (x + z * 0.58, y + z * 0.24)], fill="#0f766e")


def icon_justice(d, x, y, z):
    # gavel
    line(d, (x + z * 0.10, y + z * 0.70, x + z * 0.38, y + z * 0.52), "#334155", 4)
    rr(d, (x + z * 0.34, y + z * 0.42, x + z * 0.56, y + z * 0.58), z * 0.03, fill="#334155")
    # marching figures
    for k in range(3):
        xx = x + z * (0.60 + k * 0.12)
        yy = y + z * (0.55 - k * 0.04)
        ellipse(d, (xx - z * 0.03, yy - z * 0.13, xx + z * 0.03, yy - z * 0.05), fill="#334155")
        line(d, (xx, yy - z * 0.05, xx, yy + z * 0.18), "#334155", 3)
        line(d, (xx, yy + z * 0.18, xx - z * 0.06, yy + z * 0.30), "#334155", 2)
        line(d, (xx, yy + z * 0.18, xx + z * 0.06, yy + z * 0.30), "#334155", 2)
        line(d, (xx, yy + z * 0.02, xx + z * 0.07, yy - z * 0.10), "#334155", 2)


ICONS = [icon_bridge, icon_drone, icon_gaza, icon_disasters, icon_measles,
         icon_bangladesh, icon_trade, icon_politics, icon_diplomacy, icon_justice]

CARDS = [
    ("UKRAINE · WAR", RED, "Kerch Bridge hit for a second day",
     "Ukrainian drones struck the Crimea bridge again; two people were killed and a road span collapsed into the Kerch Strait."),
    ("MIDDLE EAST · WAR", RED, "US strikes Qeshm; Bahrain downs drones",
     "US Air Force hit Qeshm Island at least six times; Bahrain intercepted IRGC drones aimed at Sheikh Isa Air Base."),
    ("GAZA & WEST BANK · HUMANITARIAN", "#c2410c", "Five killed in Gaza; settler attack",
     "Israeli strikes killed five Palestinians, including a child. Israeli settlers killed a 72-year-old woman near Jericho; the UK sanctioned eight settlement firms and Tzav 9."),
    ("EUROPE · DISASTERS", "#c2410c", "19 die in An-12 crash; 46 hurt in Prague",
     "A Russian Air Force Antonov An-12 crashed near Kemerovo, killing all 19 aboard. Two trains collided in Prague, injuring 46 people."),
    ("AMERICAS · HEALTH", "#15803d", "US loses measles-free status",
     "PAHO revoked the measles elimination status of the United States, Mexico and Bolivia; US cases passed 5,700 with multiple deaths in 2026."),
    ("BANGLADESH · ECONOMY", "#1d4ed8", "Garment workers wage protests",
     "Police clashed with thousands of garment workers demanding a minimum wage rise; 37 factories closed and the wage board meets on 23 November."),
    ("ASIA-PACIFIC · ECONOMY", "#1d4ed8", "Canada-China tariff cuts agreed",
     "Mark Carney and Xi Jinping agreed further tariff cuts before APEC in Shenzhen; China cut tariffs on C$400 million of Canadian exports."),
    ("POLITICS · NORTH AMERICA & ASIA", "#6d28d9", "Peltola wins Alaska; Mongolia president resigns",
     "Mary Peltola defeated Dan Sullivan for Alaska's Senate seat. Mongolia's president Ukhnaagiin Khürelsükh resigned over embezzlement allegations."),
    ("EUROPE-ASIA · DIPLOMACY", "#0f766e", "France and Malaysia sign partnership",
     "Macron and Malaysia agreed a strategic partnership on defence, energy and technology; Malaysia will allow limited rare-earth exports to France."),
    ("AFRICA & CARIBBEAN · JUSTICE", "#92400e", "Guinea jails 200 miners; Haiti marches",
     "A Conakry court sentenced 22 former administrators and 202 others over illegal gold mining. Haitians marched for Salvadoran troops deployed against gangs."),
]


def main():
    img = Image.new("RGB", (CANVAS, CANVAS), BG)
    d = ImageDraw.Draw(img)

    # masthead
    d.rectangle((0, 0, CANVAS, 106 * S), fill=HEADER)
    d.text((40 * S, 15 * S), "THE WORLD IN ONE DAY", font=font(SANS_BOLD, 15), fill=GOLD)
    d.text((40 * S, 36 * S), "17 NOVEMBER 2026", font=font(SERIF_BOLD, 44), fill="#ffffff")
    d.text((980 * S, 20 * S), "TUESDAY", font=font(SERIF_BOLD, 26), fill=GOLD, anchor="ra")
    d.text((980 * S, 62 * S), "WORLD NEWS", font=font(SANS_BOLD, 13), fill="#e5e7eb", anchor="ra")
    d.rectangle((0, 104 * S, CANVAS, 108 * S), fill=RED)

    # deck
    d.text((40 * S, 116 * S), "Ten stories that shaped the day - from war and disaster to health, trade and politics.",
           font=font(SANS, 17), fill=MUTED)

    card_w, card_h = 470, 150
    x0, y0 = 36, 150
    gap_x, gap_y = 18, 6
    for i, (cat, cat_color, headline, body) in enumerate(CARDS):
        col = i % 2
        row = i // 2
        cx = x0 + col * (card_w + gap_x)
        cy = y0 + row * (card_h + gap_y)
        rr(d, (cx, cy, cx + card_w, cy + card_h), 6, fill=CARD, outline=BORDER, width=1)
        # category pill
        f_cat = font(SANS_BOLD, 10)
        pill_w = f_cat.getlength(cat) + 14
        rr(d, (cx + 10, cy + 9, cx + 10 + pill_w, cy + 26), 4, fill=cat_color)
        d.text(((cx + 10 + pill_w / 2) * S, (cy + 12) * S), cat, font=f_cat, fill="#ffffff", anchor="ma")
        # icon
        ICONS[i](d, cx + 12, cy + 34, 84)
        # headline
        tx = cx + 108
        tw = card_w - 108 - 12
        f_head = font(SERIF_BOLD, 22)
        n_head = paragraph(d, headline, f_head, tx, cy + 26, tw, 23, INK, max_lines=2)
        body_y = cy + 26 + n_head * 23 + 4
        f_body = font(SANS, 14)
        avail = cy + card_h - body_y - 8
        max_lines = max(1, avail // 16)
        paragraph(d, body, f_body, tx, body_y, tw, 16, "#374151", max_lines=max_lines)

    # footer ticker
    line(d, (36, 938, 988, 938), "#cbbca3", 1)
    d.text((36 * S, 948 * S), "ALSO ON 17 NOVEMBER", font=font(SANS_BOLD, 12), fill=RED)
    ticker = ("Apple Pay, iCloud, App Store and AppleCare went down; Bangladesh protesters stormed a police station; "
              "North Macedonia arrested five in an alleged Iran-linked plot in Greece.")
    f_tick = font(SANS, 13)
    lines = wrap(ticker, f_tick, 800)
    for j, ln in enumerate(lines[:2]):
        d.text((36 * S, (968 + j * 15) * S), ln, font=f_tick, fill=MUTED)
    d.text((988 * S, 1006 * S), "Sources: AP · Reuters · AFP · BBC · Al Jazeera", font=font(SANS, 10), fill="#8a7762", anchor="ra")

    out = img.resize((W, W), Image.LANCZOS)
    out.save("entry.png", optimize=True)


if __name__ == "__main__":
    main()
