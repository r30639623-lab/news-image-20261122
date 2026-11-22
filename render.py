#!/usr/bin/env python3
"""Render THE WORLD TODAY - Sunday, 22 November 2026. PIL only, deterministic.
Writes news.png (1024x1024) in the repo root.

Professional upgrade (v2): navy masthead band + oversized date, richer panel
illustrations (night Kyiv drone raid, COP31 negotiation table, Bahrain radar),
illustrated strips on every medium card, dot-grid world map, REPORTED/CLAIM
certainty labels with a footer legend, 186-drone reframe of panel 1, and two
date-corrected card swaps (Gaza aid-vehicle strike and EU digital-tax proposal
were both first reported Saturday 21 November, so they are out; Verstappen's
Las Vegas win and the Belgian air strike are in). No UTC timeline strip: no
story carried enough verified clock times to build one honestly.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (185, 28, 28)
NAVY = (24, 38, 68)
GRAY = (100, 100, 100)
MAP_BG = (240, 234, 216)
CHIP_BG = (242, 225, 225)
CHIP_SRC_BG = (232, 228, 218)
GREEN_TXT = (34, 139, 34)
AMBER_TXT = (176, 116, 0)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def F(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"


def wrap(d, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, x, y, lines, fnt, fill, lh):
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def fit_lines(d, text, fnt_name, size, max_w, max_lines, min_size=8):
    """Shrink font until text wraps into max_lines (or min_size reached)."""
    s = size
    while s >= min_size:
        f = F(fnt_name, s)
        lines = wrap(d, text, f, max_w)
        if len(lines) <= max_lines:
            return f, lines
        s -= 1
    f = F(fnt_name, min_size)
    return f, wrap(d, text, f, max_w)


# ---------------------------------------------------------------- stories
# cert: REPORTED = carried by the day's wires; CLAIM = one side's account.
PANELS = [
    {
        "num": "1", "cat": "CONFLICT", "place": "DYMER, UKRAINE", "cert": "REPORTED",
        "headline": "Russia fires 186 drones at Ukraine overnight",
        "summary": "Kyiv says 186 drones were fired overnight; one hit a five-story block in Dymer, leaving 14 missing.",
        "chip": "161 downed · 14 missing", "src": "Air Force · Euronews",
        "art": "kyiv",
    },
    {
        "num": "2", "cat": "CLIMATE", "place": "ANTALYA, TÜRKIYE", "cert": "REPORTED",
        "headline": "Climate summit runs into a second day of overtime",
        "summary": "COP31 missed its close again; a new draft drops fossil fuels and a $120bn adaptation target.",
        "chip": "No deal · day 2 of overtime", "src": "AFP · Tagesschau",
        "art": "cop",
    },
    {
        "num": "3", "cat": "CONFLICT", "place": "BAHRAIN · MIDDLE EAST", "cert": "CLAIM",
        "headline": "Iran strikes Bahrain as US blockade hits 130 days",
        "summary": "Bahrain says an industrial site was hit and two tankers struck in Hormuz; Iran rations power.",
        "chip": "130 days of blockade", "src": "France 24 · Al Jazeera",
        "art": "bahrain",
    },
]

# (num, cat, place, headline, summary, src, cert, art)
CARDS = [
    ("4", "CONFLICT", "RIYADH, SAUDI ARABIA", "Houthis fire missiles at Saudi Arabia",
     "Saudi Arabia says it intercepted three missiles aimed at Riyadh.", "Wire reports", "CLAIM", "missiles"),
    ("5", "SOCIETY", "SEOUL, SOUTH KOREA", "Education minister resigns over AI cheating scandal",
     "Choi Kyo-jin quits days before college entrance exams.", "BBC", "REPORTED", "exam"),
    ("6", "DISASTER", "BANTEN, INDONESIA", "Candy factory fire leaves 3 dead, dozens missing",
     "Fire at a sweets factory; about 50 workers missing.", "BBC", "REPORTED", "fire"),
    ("7", "CONFLICT", "WEST BANK", "Settler attacks rise in the West Bank",
     "Settlers burn 12 vehicles overnight; inquiry opened.", "Le Monde", "REPORTED", "westbank"),
    ("8", "SPORTS", "LAS VEGAS, USA", "Verstappen wins Las Vegas Grand Prix",
     "Verstappen wins in Las Vegas, his third win there in four years.", "Al Jazeera", "REPORTED", "vegas"),
    ("9", "POLITICS", "JERUSALEM, ISRAEL", "Eisenkot invites Likud to coalition talks",
     "Former army chief seeks a government after a hung vote.", "Euronews", "REPORTED", "jerusalem"),
    ("10", "POLITICS", "SHENZHEN, CHINA", "Trump, Xi and Putin summit fallout",
     "Trump again calls Putin a friend; Zelensky calls him a killer.", "CBS", "REPORTED", "shenzhen"),
    ("11", "CONFLICT", "GULF OF FINLAND", "Russian ship still burning after drone attack",
     "Ship drifts into Finnish waters; Helsinki limits air and sea access.", "Al Jazeera", "REPORTED", "ship"),
    ("12", "JUSTICE", "GUASAVE, MEXICO", "Violence follows cartel boss capture",
     "Burned vehicles and a hospital briefly held after the raid.", "BBC", "REPORTED", "roadblock"),
    ("13", "ECONOMY", "BRUSSELS, BELGIUM", "Belgian air strike to ground all flights",
     "Controllers join a Monday strike; all flights in Belgium face cancellation.", "Straits Times", "REPORTED", "brussels"),
]

# (num, place, headline, source, lon, lat, region)
LIST = [
    ("14", "US", "CRISPR cuts bad cholesterol 52%", "Good News Network", -100, 40, "Americas"),
    ("15", "GENEVA", "UN AI weapons talks end, no rules", "CBC", 6, 46, "Europe"),
    ("16", "WASHINGTON", "FBI probes reported crime DB hack", "BBC", -77, 39, "Americas"),
    ("17", "TEHRAN", "Iran begins rationing electricity", "Straits Times", 51, 36, "Middle East"),
    ("18", "KIGALI", "EU strikes Rwanda deportation deal", "El País", 30, -2, "Africa"),
    ("19", "WASHINGTON", "Trump tells contractors to report Congress", "Guardian", -77, 39, "Americas"),
    ("20", "BEIRUT", "Lebanon's Aoun blames Israel and Iran", "Al Jazeera", 35, 34, "Middle East"),
    ("21", "SEATTLE", "ICE arrests on Seattle jet bridge", "Straits Times", -122, 48, "Americas"),
    ("22", "SAVAR", "Garment strikes close 80 factories", "Business Standard", 90, 24, "Asia"),
    ("23", "OCEAN", "Whale genome read from drone breath", "Good News Network", -150, 0, "Global"),
    ("24", "MANIPUR", "Fake liquor kills 11 in Manipur", "Yonhap", 94, 25, "Asia"),
    ("25", "KANSAS CITY", "Current win first NWSL title", "Al Jazeera", -94, 39, "Americas"),
    ("26", "COOK IS.", "Cyclone Xavier weakens near Cook Is.", "RNZ", -160, -21, "Oceania"),
    ("27", "HONG KONG", "Hong Kong holds Election Committee vote", "SCMP", 114, 22, "Asia"),
    ("28", "GENEVA", "World chess title match begins", "Al Jazeera", 6, 46, "Global"),
    ("29", "SANXINGDUI", "Silk find hints at ancient writing", "SCMP", 104, 31, "Asia"),
    ("30", "OKINAWA", "Shuri Castle main hall restored", "Japan Times", 128, 26, "Asia"),
    ("31", "SAITAMA", "200 mascots gather in Saitama", "Euronews", 139, 36, "Asia"),
    ("32", "HARARE", "Zimbabwe author cleared of AI use", "Africanews", 31, -18, "Africa"),
    ("33", "LONDON", "Roman coffin mystery may be solved", "ScienceDaily", 0, 51, "Europe"),
    ("34", "HORMUZ", "Lewis Pugh swims Strait of Hormuz", "Euronews", 56, 27, "Global"),
    ("35", "MELBOURNE", "Study may rewrite human family tree", "ScienceDaily", 145, -38, "Oceania"),
]

REGIONS = [
    ("AMERICAS", 7, (37, 99, 235)),
    ("EUROPE", 6, (124, 58, 237)),
    ("MIDDLE EAST", 6, (220, 38, 38)),
    ("ASIA", 9, (5, 150, 105)),
    ("AFRICA", 2, (217, 119, 6)),
    ("OCEANIA", 2, (8, 145, 178)),
    ("GLOBAL", 3, (100, 116, 139)),
]

STATS = [
    ("186", "drones fired overnight"),
    ("130", "days of US blockade of Iran"),
    ("3", "missiles fired at Riyadh"),
    ("50", "missing in Banten factory fire"),
    ("$120bn", "adaptation target cut at COP31"),
    ("2nd", "day of COP31 overtime"),
]

DATE_CHECK = ("Left out as earlier news: the US stock market's AI sell-off "
              "(Friday 20 November), the ICJ Myanmar ruling (19–20 November), the EU–Indonesia "
              "trade deal signing (Saturday 21 November), the Chapo Isidro capture (Saturday "
              "21 November), the Gaza aid-vehicle strike (Saturday 21 November), the EU "
              "digital-tax proposal (Saturday 21 November), and BepiColombo's Mercury orbit "
              "insertion (Saturday 21 November). Every story here happened, or was first "
              "reported, on Sunday 22 November 2026.")


# ---------------------------------------------------------------- panel art
def art_kyiv(d, x, y, w, h):
    # night sky gradient
    for i in range(h):
        t = i / max(1, h - 1)
        d.line([(x, y + i), (x + w, y + i)],
               fill=(int(16 + (38 - 16) * t), int(24 + (52 - 24) * t), int(54 + (96 - 54) * t)))
    # stars (fixed positions, deterministic)
    for sx, sy in [(12, 10), (40, 6), (70, 14), (100, 8), (130, 12), (160, 6), (190, 12),
                   (220, 8), (240, 16), (30, 26), (90, 24), (150, 26), (200, 24), (230, 30),
                   (55, 18), (175, 20)]:
        d.ellipse([x + sx - 1, y + sy - 1, x + sx + 1, y + sy + 1], fill=(235, 235, 245))
    # moon
    d.ellipse([x + w - 46, y + 6, x + w - 28, y + 24], fill=(235, 230, 200))
    # small drone silhouette with a red light, upper middle
    dx, dy = x + 178, y + 16
    d.rectangle([dx - 5, dy - 2, dx + 5, dy + 2], fill=(10, 10, 14))
    d.line([(dx - 12, dy - 4), (dx + 12, dy - 4)], fill=(10, 10, 14), width=2)
    d.ellipse([dx - 14, dy - 7, dx - 8, dy - 1], outline=(180, 180, 190), width=1)
    d.ellipse([dx + 8, dy - 7, dx + 14, dy - 1], outline=(180, 180, 190), width=1)
    d.ellipse([dx - 2, dy + 3, dx + 2, dy + 7], fill=(220, 40, 40))
    # searchlight beam from the ground, pale wedge
    d.polygon([(x + 208, y + h), (x + 226, y + h), (x + 168, y + 8)], fill=(214, 204, 158))
    # buildings (dark silhouettes, some windows lit)
    d.rectangle([x + 8, y + 52, x + 78, y + h - 14], fill=(58, 56, 66))
    d.rectangle([x + 88, y + 34, x + 168, y + h - 14], fill=(46, 44, 54))
    d.rectangle([x + 178, y + 62, x + 248, y + h - 14], fill=(68, 64, 74))
    # damaged top of middle building (jagged)
    d.polygon([(x + 88, y + 34), (x + 108, y + 46), (x + 128, y + 36), (x + 148, y + 48),
               (x + 168, y + 34), (x + 168, y + 20), (x + 88, y + 20)], fill=(46, 44, 54))
    # windows: lit ones warm yellow, the rest dark (rel = (building x, row y))
    lit = {(8, 58), (88, 72), (178, 58), (178, 72)}
    for bx in (8, 88, 178):
        for wy in range(y + 58, y + h - 22, 14):
            for wx in range(x + bx + 8, x + bx + 62, 14):
                rel = (bx, wy - y)
                col = (250, 210, 110) if rel in lit else (28, 28, 38)
                d.rectangle([wx, wy, wx + 7, wy + 8], fill=col)
    # smoke from middle building: small, dark, hugging the damaged roof
    d.ellipse([x + 112, y + 16, x + 132, y + 30], fill=(96, 104, 132))
    d.ellipse([x + 128, y + 8, x + 146, y + 22], fill=(112, 120, 148))
    # rescue ladder leaning on middle building: two parallel rails + rungs.
    # Rungs are computed by interpolating BOTH rails at the same fraction,
    # so every rung lands exactly on both rails (no zigzag, no lightning look).
    LAD = (240, 175, 30)  # warm orange-yellow
    r1b, r1t = (x + 116, y + h - 14), (x + 130, y + 64)
    r2b, r2t = (x + 126, y + h - 14), (x + 140, y + 64)
    d.line([r1b, r1t], fill=LAD, width=3)
    d.line([r2b, r2t], fill=LAD, width=3)
    for t in (0.12, 0.27, 0.42, 0.57, 0.72, 0.87):
        ax = r1b[0] + (r1t[0] - r1b[0]) * t
        ay = r1b[1] + (r1t[1] - r1b[1]) * t
        bx = r2b[0] + (r2t[0] - r2b[0]) * t
        by = r2b[1] + (r2t[1] - r2b[1]) * t
        d.line([(ax, ay), (bx, by)], fill=LAD, width=2)
    # small rescuer on the ladder, halfway up (red helmet, navy body)
    cx = (r1b[0] + r2b[0]) / 2 + ((r1t[0] + r2t[0]) / 2 - (r1b[0] + r2b[0]) / 2) * 0.55
    cy = (r1b[1] + r2b[1]) / 2 + ((r1t[1] + r2t[1]) / 2 - (r1b[1] + r2b[1]) / 2) * 0.55
    d.ellipse([cx - 4, cy - 10, cx + 4, cy - 2], fill=(200, 40, 40))
    d.rounded_rectangle([cx - 4, cy - 1, cx + 4, cy + 11], radius=2, fill=(30, 60, 120))
    # ground
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(38, 38, 46))


def art_cop(d, x, y, w, h):
    # back wall gradient
    for i in range(h):
        t = i / max(1, h - 1)
        d.line([(x, y + i), (x + w, y + i)],
               fill=(int(198 + (232 - 198) * t), int(226 + (238 - 226) * t), int(212 + (224 - 212) * t)))
    # thermometer on the wall, upper right (clear of the delegates)
    d.rounded_rectangle([x + 212, y + 8, x + 230, y + 40], radius=8, fill=(250, 250, 250), outline=(60, 60, 60))
    d.rectangle([x + 218, y + 18, x + 224, y + 36], fill=(220, 40, 40))
    d.ellipse([x + 212, y + 32, x + 230, y + 44], fill=(220, 40, 40))
    # clock on the wall, upper right
    d.ellipse([x + 240, y + 8, x + 260, y + 28], fill=(250, 250, 250), outline=(60, 60, 60))
    d.line([(x + 250, y + 18), (x + 250, y + 11)], fill=(26, 26, 26), width=2)
    d.line([(x + 250, y + 18), (x + 256, y + 21)], fill=(26, 26, 26), width=2)
    # delegates seated in a row behind the table (heads + shoulders)
    suits = [(40, 60, 120), (90, 90, 95), (60, 110, 70), (140, 50, 50)]
    skins = [(235, 200, 170), (200, 160, 120), (240, 210, 180), (210, 170, 135)]
    for i in range(4):
        cx = x + 40 + i * 48
        d.rounded_rectangle([cx - 13, y + 52, cx + 13, y + 66], radius=5, fill=suits[i])
        d.ellipse([cx - 7, y + 36, cx + 7, y + 50], fill=skins[i])
        d.arc([cx - 7, y + 36, cx + 7, y + 50], 180, 360, fill=(60, 50, 40), width=2)
    # negotiation table
    d.rectangle([x + 6, y + 66, x + w - 6, y + h - 4], fill=(122, 86, 52))
    d.rectangle([x + 6, y + 66, x + w - 6, y + 70], fill=(150, 112, 72))
    # name plates on the table
    for i in range(4):
        cx = x + 40 + i * 48
        d.rectangle([cx - 9, y + 72, cx + 9, y + 78], fill=(250, 250, 245), outline=(120, 120, 120))
    # small globe sitting on the table, left end (drawn after the table)
    gx, gy, gr = x + 20, y + 75, 9
    d.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=(70, 130, 200))
    d.ellipse([gx - 6, gy - 5, gx + 1, gy + 1], fill=(80, 170, 90))
    d.ellipse([gx + 1, gy + 2, gx + 7, gy + 8], fill=(80, 170, 90))
    # papers on the table
    d.rectangle([x + w - 52, y + 72, x + w - 14, y + 82], fill=(250, 250, 245))


def art_bahrain(d, x, y, w, h):
    # dusk sky gradient
    for i in range(h):
        t = i / max(1, h - 1)
        d.line([(x, y + i), (x + w, y + i)],
               fill=(int(240 - (240 - 150) * t), int(170 - (170 - 110) * t), int(110 + (140 - 110) * t)))
    # low sun
    d.ellipse([x + w - 52, y + 6, x + w - 28, y + 30], fill=(250, 200, 100))
    # radar tower: mast + rotating dish + sweep rings
    d.rectangle([x + 18, y + 30, x + 24, y + h - 28], fill=(60, 60, 68))
    d.ellipse([x + 6, y + 12, x + 36, y + 34], outline=(240, 240, 240), width=2)
    d.line([(x + 21, y + 23), (x + 34, y + 14)], fill=(240, 240, 240), width=2)
    d.arc([x - 8, y - 6, x + 50, y + 52], 300, 60, fill=(120, 200, 130), width=2)
    d.arc([x + 2, y + 4, x + 40, y + 42], 300, 60, fill=(120, 200, 130), width=2)
    d.polygon([(x + 21, y + 23), (x + 44, y + 6), (x + 48, y + 18)], fill=(120, 200, 130))
    # refinery towers with flames
    d.rectangle([x + 58, y + 46, x + 78, y + h - 28], fill=(90, 90, 95))
    d.rectangle([x + 84, y + 30, x + 100, y + h - 28], fill=(110, 105, 100))
    d.rectangle([x + 106, y + 56, x + 132, y + h - 28], fill=(80, 80, 85))
    for fx, fy, fs in [(68, 46, 8), (92, 30, 9)]:
        d.polygon([(x + fx, y + fy - fs), (x + fx + fs, y + fy), (x + fx + fs // 2, y + fy + 3),
                   (x + fx - fs // 2, y + fy + 3), (x + fx - fs, y + fy)], fill=(250, 140, 30))
        d.polygon([(x + fx, y + fy - fs // 2), (x + fx + fs // 2, y + fy),
                   (x + fx - fs // 2, y + fy)], fill=(250, 210, 80))
    # smoke
    d.ellipse([x + 86, y + 8, x + 104, y + 22], fill=(210, 210, 210))
    d.ellipse([x + 98, y + 2, x + 116, y + 16], fill=(225, 225, 225))
    # sea
    d.rectangle([x, y + h - 28, x + w, y + h], fill=(50, 110, 170))
    # tanker: proper hull (rectangle + sloped bow) with containers + bridge
    d.rectangle([x + 140, y + h - 26, x + 252, y + h - 10], fill=(40, 40, 48))
    d.polygon([(x + 252, y + h - 26), (x + 266, y + h - 18), (x + 252, y + h - 10)], fill=(40, 40, 48))
    for i, c in enumerate([(220, 60, 50), (240, 180, 40), (60, 140, 90), (70, 110, 200)]):
        d.rectangle([x + 146 + i * 26, y + h - 46, x + 168 + i * 26, y + h - 26], fill=c)
    d.rectangle([x + 250, y + h - 48, x + 264, y + h - 26], fill=(240, 240, 240))
    d.rectangle([x + 254, y + h - 44, x + 260, y + h - 38], fill=(70, 130, 200))


# ---------------------------------------------------------------- card art strips
def card_art(d, kind, x, y, w, h):
    if kind == "missiles":
        d.rectangle([x, y, x + w, y + h], fill=(24, 38, 68))
        for i, my in enumerate((6, 13, 20)):
            sx = x + 14 + i * 52
            d.line([(sx, y + my + 6), (sx + 34, y + my)], fill=(250, 220, 120), width=2)
            d.ellipse([sx + 32, y + my - 2, sx + 38, y + my + 4], fill=(250, 220, 120))
        d.rectangle([x, y + h - 6, x + w, y + h], fill=(40, 40, 52))
        for bx in range(x + 8, x + w - 10, 22):
            d.rectangle([bx, y + h - 12, bx + 12, y + h - 6], fill=(60, 60, 76))
    elif kind == "exam":
        d.rectangle([x, y, x + w, y + h], fill=(214, 196, 160))
        d.rectangle([x, y + h - 7, x + w, y + h], fill=(140, 100, 60))
        d.rectangle([x + 14, y + 4, x + 74, y + h - 8], fill=(255, 255, 255), outline=(150, 150, 150))
        for ly in range(y + 9, y + h - 10, 4):
            d.line([(x + 19, ly), (x + 69, ly)], fill=(170, 170, 170), width=1)
        d.line([(x + 84, y + 6), (x + 108, y + h - 10)], fill=(240, 200, 60), width=3)
        d.polygon([(x + 108, y + h - 10), (x + 114, y + h - 8), (x + 110, y + h - 4)], fill=(220, 160, 120))
        d.rectangle([x + w - 34, y + 4, x + w - 14, y + 18], fill=(90, 90, 100))
        d.ellipse([x + w - 31, y + 7, x + w - 17, y + 15], fill=(120, 200, 220))
        d.line([(x + w - 34, y + 4), (x + w - 14, y + 18)], fill=(220, 40, 40), width=2)
        d.line([(x + w - 14, y + 4), (x + w - 34, y + 18)], fill=(220, 40, 40), width=2)
    elif kind == "fire":
        d.rectangle([x, y, x + w, y + h], fill=(60, 50, 48))
        d.rectangle([x + 10, y + 10, x + 70, y + h - 2], fill=(110, 105, 100))
        d.rectangle([x + 76, y + 4, x + 84, y + h - 2], fill=(90, 88, 86))
        for fx, fy, fs in [(30, 12, 9), (52, 14, 7), (96, 10, 8), (130, 12, 9), (160, 10, 7)]:
            d.polygon([(x + fx, y + fy - fs), (x + fx + fs, y + fy + 4), (x + fx - fs, y + fy + 4)],
                      fill=(250, 140, 30))
            d.polygon([(x + fx, y + fy - fs // 2), (x + fx + fs // 2, y + fy + 4),
                       (x + fx - fs // 2, y + fy + 4)], fill=(250, 210, 80))
        d.ellipse([x + 96, y - 2, x + 116, y + 10], fill=(190, 190, 190))
    elif kind == "westbank":
        d.rectangle([x, y, x + w, y + h], fill=(30, 28, 44))
        d.rectangle([x, y + h - 8, x + w, y + h], fill=(70, 70, 78))
        d.rectangle([x + 30, y + 12, x + 110, y + h - 8], fill=(90, 30, 30))
        d.rectangle([x + 40, y + 6, x + 96, y + 12], fill=(110, 40, 40))
        d.ellipse([x + 44, y + h - 10, x + 54, y + h], fill=(20, 20, 20))
        d.ellipse([x + 88, y + h - 10, x + 98, y + h], fill=(20, 20, 20))
        d.polygon([(x + 66, y + 2), (x + 74, y + 10), (x + 62, y + 10)], fill=(250, 160, 40))
        d.ellipse([x + w - 30, y + 3, x + w - 14, y + 19], fill=(235, 230, 200))
    elif kind == "vegas":
        d.rectangle([x, y, x + w, y + h], fill=(40, 24, 68))
        for bx, bh in [(10, 16), (30, 20), (52, 14), (74, 18), (96, 12)]:
            d.rectangle([x + bx, y + h - bh, x + bx + 16, y + h], fill=(70, 60, 100))
            d.rectangle([x + bx + 3, y + h - bh + 3, x + bx + 7, y + h - bh + 7], fill=(250, 220, 120))
            d.rectangle([x + bx + 10, y + h - bh + 8, x + bx + 13, y + h - bh + 11], fill=(250, 220, 120))
        # checkered flag on a pole
        d.line([(x + w - 26, y + 2), (x + w - 26, y + h - 2)], fill=(220, 220, 220), width=2)
        for r in range(3):
            for c in range(4):
                col = (20, 20, 20) if (r + c) % 2 == 0 else (255, 255, 255)
                d.rectangle([x + w - 24 + c * 5, y + 2 + r * 5, x + w - 20 + c * 5, y + 6 + r * 5], fill=col)
    elif kind == "jerusalem":
        d.rectangle([x, y, x + w, y + h], fill=(232, 226, 210))
        d.rectangle([x + 60, y + 6, x + 130, y + h - 4], fill=(250, 248, 240), outline=(150, 140, 120))
        d.polygon([(x + 58, y + 6), (x + 95, y - 2), (x + 132, y + 6)], fill=(200, 190, 170))
        for cx in (72, 88, 104, 120):
            d.rectangle([x + cx, y + 8, x + cx + 4, y + h - 4], fill=(180, 170, 150))
        d.line([(x + 16, y + 4), (x + 16, y + h - 4)], fill=(120, 120, 120), width=2)
        d.rectangle([x + 16, y + 4, x + 34, y + 12], fill=(40, 90, 160))
        d.line([(x + 40, y + 4), (x + 40, y + h - 4)], fill=(120, 120, 120), width=2)
        d.rectangle([x + 40, y + 4, x + 58, y + 12], fill=(255, 255, 255), outline=(40, 90, 160))
    elif kind == "shenzhen":
        d.rectangle([x, y, x + w, y + h], fill=(196, 216, 232))
        for bx in range(x + 8, x + w - 10, 24):
            d.rectangle([bx, y + h - 10, bx + 14, y + h], fill=(90, 95, 110))
        for i, col in enumerate([(200, 40, 40), (40, 60, 160), (240, 240, 240)]):
            px = x + 120 + i * 20
            d.line([(px, y + 2), (px, y + h - 2)], fill=(90, 90, 90), width=2)
            d.rectangle([px, y + 2, px + 16, y + 10], fill=col, outline=(60, 60, 60))
    elif kind == "ship":
        d.rectangle([x, y, x + w, y + h], fill=(168, 196, 222))
        d.rectangle([x, y + h - 10, x + w, y + h], fill=(50, 110, 170))
        d.rectangle([x + 40, y + h - 18, x + 140, y + h - 10], fill=(40, 40, 48))
        d.polygon([(x + 140, y + h - 18), (x + 152, y + h - 14), (x + 140, y + h - 10)], fill=(40, 40, 48))
        d.rectangle([x + 128, y + h - 26, x + 142, y + h - 18], fill=(240, 240, 240))
        d.ellipse([x + 70, y + 2, x + 90, y + 12], fill=(200, 200, 200))
        d.ellipse([x + 84, y - 2, x + 102, y + 8], fill=(215, 215, 215))
    elif kind == "roadblock":
        d.rectangle([x, y, x + w, y + h], fill=(52, 52, 60))
        d.rectangle([x, y + h - 8, x + w, y + h], fill=(90, 90, 96))
        d.line([(x, y + h - 4), (x + w, y + h - 4)], fill=(250, 220, 120), width=2)
        d.rectangle([x + 20, y + 12, x + 90, y + h - 8], fill=(120, 30, 30))
        d.rectangle([x + 30, y + 6, x + 76, y + 12], fill=(140, 40, 40))
        d.ellipse([x + 32, y + h - 10, x + 42, y + h], fill=(20, 20, 20))
        d.ellipse([x + 68, y + h - 10, x + 78, y + h], fill=(20, 20, 20))
        d.polygon([(x + 52, y + 2), (x + 60, y + 10), (x + 46, y + 10)], fill=(250, 160, 40))
        for i in range(4):
            col = (250, 220, 120) if i % 2 == 0 else (220, 60, 40)
            d.rectangle([x + 110 + i * 16, y + 8, x + 124 + i * 16, y + 16], fill=col)
    elif kind == "brussels":
        d.rectangle([x, y, x + w, y + h], fill=(30, 60, 130))
        for i in range(10):
            import math
            a = math.radians(i * 36 - 90)
            sx = x + w - 34 + 9 * math.cos(a)
            sy = y + 13 + 9 * math.sin(a)
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(250, 220, 80))
        d.rectangle([x + 10, y + h - 10, x + 60, y + h], fill=(90, 95, 110))
        d.rectangle([x + 66, y + h - 14, x + 100, y + h], fill=(110, 115, 130))
        d.rectangle([x + 106, y + h - 8, x + 130, y + h], fill=(90, 95, 110))


# ---------------------------------------------------------------- map (dot grid)
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60), (-55, 47),
     (-70, 42), (-75, 35), (-80, 25), (-90, 20), (-105, 20), (-115, 30), (-125, 40),
     (-130, 50), (-150, 60)],
    # South America
    [(-80, 10), (-60, 5), (-50, -5), (-40, -10), (-35, -20), (-40, -30), (-55, -35),
     (-65, -40), (-70, -50), (-70, -30), (-75, -15), (-80, 5)],
    # Europe
    [(-10, 36), (0, 36), (10, 38), (20, 40), (28, 36), (30, 42), (25, 45), (20, 45),
     (15, 44), (10, 44), (5, 43), (0, 44), (-5, 48), (-10, 50), (-5, 55), (0, 58),
     (5, 60), (10, 62), (5, 65), (10, 70), (20, 70), (30, 70), (25, 65), (20, 60),
     (15, 55), (10, 52), (5, 50), (0, 48), (-5, 45), (-10, 40)],
    # Africa
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31), (35, 28), (40, 15),
     (48, 11), (51, 10), (45, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -30),
     (12, -18), (8, -5), (9, 4), (-8, 5), (-15, 10)],
    # Asia
    [(30, 70), (40, 68), (60, 70), (80, 73), (100, 77), (120, 73), (140, 72), (160, 70),
     (170, 66), (180, 65), (170, 60), (160, 60), (150, 55), (140, 45), (135, 35), (130, 33),
     (127, 35), (122, 30), (120, 25), (110, 20), (105, 10), (100, 8), (95, 15), (90, 22),
     (85, 20), (80, 15), (75, 8), (70, 20), (65, 25), (60, 25), (55, 25), (50, 29),
     (48, 30), (44, 29), (40, 35), (35, 36), (30, 36), (28, 40), (25, 40), (30, 45),
     (30, 55), (30, 65)],
    # Australia
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32), (135, -35),
     (140, -38), (145, -38), (150, -37), (153, -32), (153, -27), (150, -22), (146, -19),
     (142, -15), (142, -11), (137, -12), (135, -15), (132, -12), (130, -13), (126, -14),
     (122, -17), (118, -20)],
]


def point_in_poly(lon, lat, poly):
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > lat) != (yj > lat):
            xinters = (xj - xi) * (lat - yi) / (yj - yi) + xi
            if lon < xinters:
                inside = not inside
        j = i
    return inside


# ---------------------------------------------------------------- build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 24
    CW = W - 2 * M

    # navy masthead band
    d.rectangle([0, 0, W, 24], fill=NAVY)
    f_band = F(SANS_B, 11)
    d.text((M, 5), "THE WORLD IN ONE DAY", font=f_band, fill=(255, 255, 255))
    t = "SUNDAY EDITION · No. 326"
    f_band_r = F(SANS, 10)
    d.text((W - M - d.textlength(t, font=f_band_r), 6), t, font=f_band_r, fill=(200, 205, 220))

    # masthead
    f_mast = F(SERIF_B, 58)
    t = "THE WORLD TODAY"
    d.text(((W - d.textlength(t, font=f_mast)) / 2, 30), t, font=f_mast, fill=INK)
    d.line([(M, 92), (W - M, 92)], fill=INK, width=2)

    # oversized date
    f_date = F(SERIF_B, 28)
    t = "SUNDAY 22 NOVEMBER 2026"
    d.text(((W - d.textlength(t, font=f_date)) / 2, 98), t, font=f_date, fill=INK)
    f_red = F(SANS_B, 11)
    t = "35 STORIES · 7 REGIONS · EVERY ONE DATED SUNDAY 22 NOVEMBER 2026"
    d.text(((W - d.textlength(t, font=f_red)) / 2, 130), t, font=f_red, fill=RED)

    # sub-headline (red)
    f_sub = F(SERIF, 14)
    t = "186 drones fired at Ukraine · COP31 runs into overtime · Iran strikes Bahrain"
    d.text(((W - d.textlength(t, font=f_sub)) / 2, 146), t, font=f_sub, fill=RED)
    d.line([(M, 166), (W - M, 166)], fill=INK, width=1)

    # stat strip: 6 boxes
    y0, bh = 172, 44
    bw = (CW - 5 * 4) / 6
    for i, (num, label) in enumerate(STATS):
        x = M + i * (bw + 4)
        d.rectangle([x, y0, x + bw, y0 + bh], outline=INK, width=1)
        f_num = F(SERIF_B, 22)
        d.text((x + (bw - d.textlength(num, font=f_num)) / 2, y0 + 2), num, font=f_num, fill=INK)
        f_lab = F(SANS, 8)
        lines = wrap(d, label, f_lab, bw - 8)
        draw_lines(d, x + 4, y0 + 25, lines, f_lab, INK, 10)

    # region bar
    y0 = 222
    total = sum(c for _, c, _ in REGIONS)
    x = M
    for name, count, color in REGIONS:
        seg = CW * count / total
        d.rectangle([x, y0, x + seg, y0 + 18], fill=color)
        f_rb = F(SANS_B, 8)
        lab = "%s %d" % (name, count)
        tw = d.textlength(lab, font=f_rb)
        if tw <= seg - 4:
            d.text((x + (seg - tw) / 2, y0 + 4), lab, font=f_rb, fill=(255, 255, 255))
        x += seg
    d.rectangle([M, y0, M + CW, y0 + 18], outline=INK, width=1)

    # 3 big panels
    py, ph = 248, 244
    pw = (CW - 2 * 8) / 3
    art_fn = {"kyiv": art_kyiv, "cop": art_cop, "bahrain": art_bahrain}
    for i, p in enumerate(PANELS):
        x = M + i * (pw + 8)
        d.rectangle([x, py, x + pw, py + ph], outline=INK, width=1)
        # illustration (100 px tall)
        art_fn[p["art"]](d, int(x + 1), py + 1, int(pw - 2), 100)
        # red banner with certainty chip
        by = py + 102
        d.rectangle([x, by, x + pw, by + 20], fill=RED)
        f_ban = F(SANS_B, 10)
        d.text((x + 6, by + 4), "%s · %s — %s" % (p["num"], p["cat"], p["place"]),
               font=f_ban, fill=(255, 255, 255))
        f_cert = F(SANS_B, 8)
        cert = p["cert"]
        cw2 = d.textlength(cert, font=f_cert) + 10
        cx = x + pw - 6 - cw2
        d.rounded_rectangle([cx, by + 3, cx + cw2, by + 17], radius=7, fill=(255, 255, 255))
        d.text((cx + 5, by + 5),
               cert, font=f_cert,
               fill=GREEN_TXT if cert == "REPORTED" else AMBER_TXT)
        # headline
        f_h, lines = fit_lines(d, p["headline"], SERIF_B, 16, pw - 12, 2)
        hy = by + 24
        draw_lines(d, x + 6, hy, lines, f_h, INK, 19)
        # summary
        f_s, slines = fit_lines(d, p["summary"], SANS, 11, pw - 12, 2)
        sy = hy + len(lines) * 19 + 4
        draw_lines(d, x + 6, sy, slines, f_s, INK, 13)
        # chips
        cy = py + ph - 24
        f_chip = F(SANS_B, 9)
        chip_w = d.textlength(p["chip"], font=f_chip) + 12
        d.rounded_rectangle([x + 6, cy, x + 6 + chip_w, cy + 16], radius=8, fill=CHIP_BG)
        d.text((x + 12, cy + 3), p["chip"], font=f_chip, fill=RED)
        src_w = d.textlength(p["src"], font=f_chip) + 12
        sx = x + pw - 6 - src_w
        d.rounded_rectangle([sx, cy, sx + src_w, cy + 16], radius=8, fill=CHIP_SRC_BG)
        d.text((sx + 6, cy + 3), p["src"], font=f_chip, fill=INK)

    # medium cards 4-13: 5 cols x 2 rows, each with an illustrated strip
    cy0, ch, cgap = 500, 102, 8
    cw = (CW - 4 * cgap) / 5
    for i, (num, cat, place, headline, summary, src, cert, art) in enumerate(CARDS):
        row, col = divmod(i, 5)
        x = M + col * (cw + cgap)
        y = cy0 + row * (ch + 4)
        d.rectangle([x, y, x + cw, y + ch], outline=INK, width=1)
        # banner: num · cat · cert (left), source (right)
        d.rectangle([x, y, x + cw, y + 14], fill=RED)
        f_ban = F(SANS_B, 8)
        d.text((x + 4, y + 3), "%s · %s · " % (num, cat), font=f_ban, fill=(255, 255, 255))
        bx = x + 4 + d.textlength("%s · %s · " % (num, cat), font=f_ban)
        d.text((bx, y + 3), cert, font=f_ban,
               fill=(180, 230, 180) if cert == "REPORTED" else (255, 220, 100))
        f_src = F(SANS, 7)
        sw = d.textlength(src, font=f_src)
        d.text((x + cw - 4 - sw, y + 4), src, font=f_src, fill=(255, 255, 255))
        # illustrated strip
        card_art(d, art, int(x + 1), y + 15, int(cw - 2), 26)
        # headline (max 2 lines)
        f_h, lines = fit_lines(d, headline, SERIF_B, 11, cw - 8, 2, min_size=9)
        hy = y + 44
        draw_lines(d, x + 4, hy, lines, f_h, INK, 13)
        # summary (max 2 lines)
        f_s, slines = fit_lines(d, summary, SANS, 9, cw - 8, 2, min_size=8)
        sy = hy + len(lines) * 13 + 2
        draw_lines(d, x + 4, sy, slines, f_s, INK, 11)

    # WHERE IT HAPPENED
    wy = 716
    f_sec = F(SANS_B, 14)
    d.text((M, wy), "WHERE IT HAPPENED", font=f_sec, fill=INK)
    d.line([(M, wy + 20), (W - M, wy + 20)], fill=INK, width=2)

    map_x, map_y, map_w, map_h = M, wy + 28, 340, 160
    d.rectangle([map_x, map_y, map_x + map_w, map_y + map_h], fill=MAP_BG, outline=INK, width=1)

    def ll_to_xy(lon, lat):
        return (map_x + (lon + 180) / 360 * map_w,
                map_y + (90 - lat) / 180 * map_h)

    # dot-grid continents: dots only where a grid point falls on land
    dot_col = (198, 184, 148)
    step = 7
    gx = map_x + 3
    while gx < map_x + map_w - 2:
        gy = map_y + 3
        while gy < map_y + map_h - 2:
            lon = (gx - map_x) / map_w * 360 - 180
            lat = 90 - (gy - map_y) / map_h * 180
            if any(point_in_poly(lon, lat, poly) for poly in CONTINENTS):
                d.ellipse([gx - 2, gy - 2, gx + 2, gy + 2], fill=dot_col)
            gy += step
        gx += step

    # pins, fanned out where true points cluster
    pin_offsets = {
        "21": (-7, -11), "14": (-8, 14), "25": (7, -19), "16": (9, 13), "19": (19, -13),
        "15": (-12, -13), "28": (12, -13), "33": (0, 19),
        "17": (10, -12), "20": (-11, -12), "34": (3, 14),
        "22": (-11, 11), "24": (5, 12), "27": (4, 14), "29": (0, -14), "30": (1, 15), "31": (7, -14),
        "18": (-12, 6), "32": (11, 8),
        "23": (0, 0), "26": (1, 13), "35": (1, 14),
    }
    f_pin = F(SANS_B, 8)
    for num, place, headline, src, lon, lat, region in LIST:
        px, py2 = ll_to_xy(lon, lat)
        ox, oy = pin_offsets.get(num, (0, 0))
        qx, qy = px + ox, py2 + oy
        if (ox, oy) != (0, 0):
            d.line([(px, py2), (qx, qy)], fill=(120, 120, 120), width=1)
        d.ellipse([qx - 8, qy - 8, qx + 8, qy + 8], fill=RED, outline=(255, 255, 255), width=1)
        tw = d.textlength(num, font=f_pin)
        d.text((qx - tw / 2, qy - 5), num, font=f_pin, fill=(255, 255, 255))

    # list, 2 columns x 11 rows
    list_x = map_x + map_w + 12
    list_w = W - M - list_x
    col_w = (list_w - 8) / 2
    f_list = F(SANS, 9)
    f_list_s = F(SANS, 8)
    for i, (num, place, headline, src, lon, lat, region) in enumerate(LIST):
        col, row = divmod(i, 11)
        x = list_x + col * (col_w + 8)
        y = map_y + 1 + row * 15
        line = "%s %s · %s (%s)" % (num, place, headline, src)
        fnt = f_list
        if d.textlength(line, font=fnt) > col_w:
            fnt = f_list_s
        f_b = F(SANS_B, 9 if fnt is f_list else 8)
        prefix = "%s %s · " % (num, place)
        d.text((x, y), prefix, font=f_b, fill=RED)
        rest = "%s (%s)" % (headline, src)
        d.text((x + d.textlength(prefix, font=f_b), y), rest, font=fnt, fill=INK)
        d.line([(x, y + 12), (x + col_w, y + 12)], fill=(210, 205, 190), width=1)

    # DATE CHECK
    dy = 912
    d.rectangle([M, dy, W - M, dy + 62], outline=RED, width=2)
    f_dc_t = F(SANS_B, 11)
    d.text((M + 8, dy + 5), "DATE CHECK", font=f_dc_t, fill=RED)
    f_dc = F(SANS, 10)
    lines = wrap(d, DATE_CHECK, f_dc, CW - 16)
    draw_lines(d, M + 8, dy + 21, lines, f_dc, INK, 13)

    # footer: certainty legend + compiled line
    f_ft = F(SANS, 9)
    t = ("CERTAINTY: REPORTED = carried by the day's wires · "
         "CLAIM = one side's account, labelled as such")
    d.text(((W - d.textlength(t, font=f_ft)) / 2, 982), t, font=f_ft, fill=GRAY)
    t = "Compiled from major wire reports · 22 November 2026 · PAGE 1 OF 1"
    d.text(((W - d.textlength(t, font=f_ft)) / 2, 996), t, font=f_ft, fill=GRAY)

    img.save("news.png", format="PNG")
    print("wrote news.png", img.size)


if __name__ == "__main__":
    build()
