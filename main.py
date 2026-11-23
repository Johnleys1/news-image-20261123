#!/usr/bin/env python3
"""THE WORLD — Monday 23 November 2026.

Renders one newspaper front page summarising the world's news of
Monday 23 November 2026 to /output/entry.png (or $MAKEFUN_OUTPUT_DIR).
Deterministic: same input, same output. All artwork is drawn with PIL;
no external images, no network access at render time.
"""
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

BASE = Path(__file__).resolve().parent
OUT_DIR = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")

W, H = 2400, 3400
PAPER = (247, 243, 232)
INK = (26, 26, 26)
RED = (176, 42, 30)
OCHRE = (200, 138, 45)
TEAL = (46, 110, 106)
GRAY = (107, 107, 107)
RULE = (201, 194, 176)
LIGHT = (236, 231, 218)
DARK_TEAL = (28, 74, 72)

# ---------------------------------------------------------------- fonts
def _font(paths, size):
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


SERIF_B = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf",
]
SERIF = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
]
SERIF_I = [
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
]
SANS = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
]
SANS_B = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
]


def fb(size):
    return _font(SERIF_B, size)


def fs(size):
    return _font(SERIF, size)


def fi(size):
    return _font(SERIF_I, size)


def sn(size):
    return _font(SANS, size)


def sb(size):
    return _font(SANS_B, size)


# ---------------------------------------------------------------- data
# 34 real stories, all verified against reporting published 23 Nov 2026.
# kind: hero art kind / grid motif kind. lon/lat used for the map dots (top 13).
HEROES = [
    {
        "n": 1, "region": "CLIMATE", "kicker": "COP31 · TURKIYE",
        "headline": "COP31 collapses without a deal",
        "deck": "Turkiye's final draft drops the words \u2018fossil fuels\u2019 \u2014 and the talks fall apart.",
        "dateline": "ANTALYA, TURKIYE", "art": "smoke", "lon": 30.7, "lat": 36.9,
    },
    {
        "n": 2, "region": "MIDDLE EAST", "kicker": "THE GULF",
        "headline": "Iran hits US bases in Bahrain",
        "deck": "The Strait of Hormuz conflict engulfs Saudi Arabia and Bahrain as the Gulf slides toward war.",
        "dateline": "MANAMA, BAHRAIN", "art": "strait", "lon": 50.6, "lat": 26.2,
    },
    {
        "n": 3, "region": "MARKETS", "kicker": "THE AI ROUT",
        "headline": "Wall Street\u2019s worst week since April 2025",
        "deck": "S&P 500 falls 3.7% to 6,910 as the AI rout wipes out the Nasdaq\u2019s 2026 gains.",
        "dateline": "NEW YORK, USA", "art": "chart", "lon": -74.0, "lat": 40.7,
    },
]

GRID = [
    {
        "n": 4, "region": "EUROPE",
        "headline": "Drone hits Kyiv block; 14 missing",
        "deck": "Zelenskiy says rescuers are digging through the ruins after the overnight strike.",
        "dateline": "KYIV, UKRAINE", "motif": "drone", "lon": 30.5, "lat": 50.4,
    },
    {
        "n": 5, "region": "EUROPE",
        "headline": "Russian ship still burning off Finland",
        "deck": "Cargo vessel ablaze in the Baltic after a drone attack; Moscow blames Kyiv.",
        "dateline": "HELSINKI, FINLAND", "motif": "ship", "lon": 21.0, "lat": 60.0,
    },
    {
        "n": 6, "region": "NORTH AMERICA",
        "headline": "Mexico seizes FBI\u2019s most-wanted boss",
        "deck": "\u2018El Chapo Isidro\u2019 captured in Sinaloa after gunfights leave 11 dead.",
        "dateline": "CULIAC\u00c1N, MEXICO", "motif": "badge", "lon": -107.4, "lat": 24.8,
    },
    {
        "n": 7, "region": "SPORT",
        "headline": "Verstappen wins wild Las Vegas GP",
        "deck": "Thirty-four lead changes \u2014 and the Ferraris collide, both collecting penalties.",
        "dateline": "LAS VEGAS, USA", "motif": "trophy", "lon": -115.1, "lat": 36.2,
    },
    {
        "n": 8, "region": "EAST ASIA",
        "headline": "Minister quits over AI exam cheating",
        "deck": "South Korea\u2019s education chief resigns after anti-cheating measures cause chaos.",
        "dateline": "SEOUL, SOUTH KOREA", "motif": "cap", "lon": 127.0, "lat": 37.5,
    },
    {
        "n": 9, "region": "SOUTH ASIA",
        "headline": "Nepal PM holds talks with Modi",
        "deck": "Balendra Shah\u2019s state visit to India centres on trade, power and the border.",
        "dateline": "NEW DELHI, INDIA", "motif": "flags", "lon": 77.2, "lat": 28.6,
    },
    {
        "n": 10, "region": "GLOBAL",
        "headline": "UN to keep talking on killer robots",
        "deck": "Nations agree to continue negotiations on lethal autonomous weapons.",
        "dateline": "GENEVA, SWITZERLAND", "motif": "gavel", "lon": 6.1, "lat": 46.2,
    },
    {
        "n": 11, "region": "EAST ASIA",
        "headline": "Dozens missing after factory fire",
        "deck": "Rescuers search the ruins in Indonesia as the death toll climbs.",
        "dateline": "JAKARTA, INDONESIA", "motif": "flame", "lon": 106.8, "lat": -6.2,
    },
    {
        "n": 12, "region": "SPORT",
        "headline": "India post record 720 in Wellington",
        "deck": "The tourists pile up the highest Test total on New Zealand soil.",
        "dateline": "WELLINGTON, NEW ZEALAND", "motif": "bat", "lon": 174.8, "lat": -41.3,
    },
    {
        "n": 13, "region": "NORTH AMERICA",
        "headline": "FBI crime database hacked, Trump confirms",
        "deck": "The National Crime Information Center breach is under investigation.",
        "dateline": "WASHINGTON, USA", "motif": "chip", "lon": -77.0, "lat": 38.9,
    },
]

RAIL = [
    (14, "Kim: security, not supremacy", "PYONGYANG"),
    (15, "24 killed in fresh South Sudan violence", "JUBA"),
    (16, "Drones hit homes, UN site in Khartoum", "KHARTOUM"),
    (17, "35 killed in revenge attacks in Nigeria", "KANO"),
    (18, "WHO pleads for peace in Ebola-hit Congo", "GENEVA"),
    (19, "Bolsonaro \u2018stable\u2019 in intensive care", "BRAS\u00cdLIA"),
    (20, "Israel coalition talks collapse", "JERUSALEM"),
    (21, "Myanmar junta calls ASEAN ruling unfair", "NAYPYIDAW"),
    (22, "Lisbon marches over living costs", "LISBON"),
    (23, "Nvidia chips diverted to China", "WASHINGTON"),
    (24, "Cursor may drop Chinese AI models", "SAN FRANCISCO"),
    (25, "BepiColombo enters Mercury orbit", "DARMSTADT"),
    (26, "China unveils wingless flying car", "BEIJING"),
    (27, "Pochettino era begins at Man Utd", "MANCHESTER"),
    (28, "Anupama keeps world snooker crown", "NEW DELHI"),
    (29, "Jeweller Paolo Bulgari dies at 89", "ROME"),
    (30, "IFFI hosts BRICS film roundtable", "GOA"),
    (31, "India, Bulgaria talk IMEC and Black Sea", "NEW DELHI"),
    (32, "Shah launches \u20b94,000-crore Arunachal push", "ITANAGAR"),
    (33, "Australia PMI hits five-year low", "SYDNEY"),
    (34, "Three Russian missiles hit Poland", "WARSAW"),
]

STATS = [
    ("S&P 500", "6,910.39", "\u22123.70%"),
    ("NASDAQ", "22,617.73", "\u22125.28%"),
    ("NIKKEI 225", "56,436.65", "\u22125.06%"),
    ("FTSE 100", "10,346.34", "\u22121.02%"),
    ("GOLD", "$3,515.40", "\u22124.62%"),
    ("WTI OIL", "$83.41", "+1.18%"),
]

DATA_CHECK = [
    ("\u22128.6%", "S&P 500\u2019s weekly fall \u2014 worst since April 2025.", "CNBC"),
    ("35.9", "VIX fear gauge at Friday\u2019s close, up 7.45.", "CBOE"),
    ("34", "lead changes in the Las Vegas Grand Prix.", "FORMULA 1"),
    ("720/9", "India\u2019s record Test total in Wellington.", "MATCH REPORT"),
]

QUOTE = "\u201cA sign of difficult geopolitical times\u201d \u2014 Anthony Albanese, PM of Australia, on the COP31 failure."

STANDFIRST = (
    "Climate talks collapse in Turkiye as the Gulf slides toward war \u2014 "
    "and Wall Street suffers its worst week since April 2025."
)

# ---------------------------------------------------------------- helpers
def wrap(d, text, font, width):
    """Greedy word wrap; returns a list of lines that fit `width` px."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(d, lines, x, y, font, fill, leading):
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def fit_font(text, font_fn, size, width):
    """Largest size <= `size` at which `text` fits `width` on one line."""
    while size > 10:
        f = font_fn(size)
        if ImageDraw.Draw(Image.new("RGB", (8, 8))).textlength(text, font=f) <= width:
            return f, size
        size -= 2
    return font_fn(size), size


def rule(d, x0, x1, y, fill=INK, width=3):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


def section_label(d, text, x, y, width):
    f = sb(30)
    d.text((x, y), text, font=f, fill=RED)
    rule(d, x, x + width, y + 40, fill=RULE, width=2)
    return y + 52


# ---------------------------------------------------------------- masthead
def draw_masthead(d):
    # Title, centred, fit to the full page width minus margins.
    f, _ = fit_font("THE WORLD", fb, 205, W - 140)
    tw = d.textlength("THE WORLD", font=f)
    d.text(((W - tw) / 2, 44), "THE WORLD", font=f, fill=INK)
    rule(d, 70, W - 70, 268, fill=RED, width=6)
    # Dateline row.
    f1 = sb(30)
    d.text((70, 282), "MONDAY 23 NOVEMBER 2026", font=f1, fill=INK)
    right = "34 STORIES  \u00b7  8 REGIONS  \u00b7  PRICE $2.50"
    d.text((W - 70 - d.textlength(right, font=f1), 282), right, font=f1, fill=GRAY)
    # Standfirst, centred italic, two lines max.
    f2 = fi(40)
    lines = wrap(d, STANDFIRST, f2, W - 320)
    y = 326
    for line in lines[:2]:
        lw = d.textlength(line, font=f2)
        d.text(((W - lw) / 2, y), line, font=f2, fill=INK)
        y += 52
    return y + 8


# ---------------------------------------------------------------- stat strip
def draw_stats(d, y):
    label = "MARKETS \u00b7 FRIDAY\u2019S CLOSE, 20 NOV 2026"
    f = sb(26)
    d.text((70, y), label, font=f, fill=GRAY)
    y += 40
    box_w = (W - 140 - 5 * 24) / 6
    for i, (name, val, chg) in enumerate(STATS):
        x = 70 + i * (box_w + 24)
        d.rectangle([x, y, x + box_w, y + 96], outline=RULE, width=2)
        d.text((x + 16, y + 12), name, font=sb(26), fill=GRAY)
        d.text((x + 16, y + 42), val, font=sb(32), fill=INK)
        col = RED if chg.startswith("\u2212") else TEAL
        d.text((x + 16, y + 74), chg, font=sb(26), fill=col)
    return y + 96

# ---------------------------------------------------------------- hero art
def art_smoke(d, x, y, w, h):
    """COP31: smokestacks under a low ochre sun, cracked earth."""
    d.rectangle([x, y, x + w, y + h], fill=DARK_TEAL)
    d.ellipse([x + w - 190, y + 26, x + w - 60, y + 156], fill=OCHRE)
    d.ellipse([x + w - 170, y + 46, x + w - 80, y + 136], fill=(226, 178, 92))
    # Smokestacks.
    for i, sx in enumerate((x + 70, x + 190, x + 310)):
        d.rectangle([sx, y + h - 190, sx + 64, y + h - 60], fill=(38, 38, 38))
        d.rectangle([sx - 8, y + h - 204, sx + 72, y + h - 190], fill=(58, 58, 58))
        # Smoke curls.
        for j in range(3):
            cy = y + h - 250 - j * 34 - i * 6
            cx = sx + 32 + (j % 2) * 26 - 12
            d.ellipse([cx, cy, cx + 74, cy + 40], fill=(210, 205, 190))
    # Cracked ground.
    d.rectangle([x, y + h - 60, x + w, y + h], fill=(24, 24, 24))
    d.line([(x + 40, y + h - 60), (x + 200, y + h - 18), (x + 420, y + h - 44),
            (x + 640, y + h - 10)], fill=(120, 110, 95), width=4)


def art_strait(d, x, y, w, h):
    """The Gulf: a strait between two shores, ships, one explosion burst."""
    d.rectangle([x, y, x + w, y + h], fill=(232, 222, 190))
    # Sea bands.
    for i in range(5):
        yy = y + 150 + i * 34
        d.rectangle([x, yy, x + w, yy + 16], fill=TEAL if i % 2 == 0 else (64, 138, 132))
    # Shores.
    d.polygon([(x, y + h), (x, y + 120), (x + 150, y + 150), (x + 60, y + h)], fill=OCHRE)
    d.polygon([(x + w, y + h), (x + w, y + 110), (x + w - 170, y + 150), (x + w - 50, y + h)], fill=(176, 120, 60))
    # Two ships.
    for sx, sy, sc in ((x + 210, y + 210, 1.0), (x + 430, y + 260, 0.8)):
        sw = int(150 * sc)
        d.polygon([(sx, sy), (sx + sw, sy), (sx + sw - 18, sy + 34), (sx + 18, sy + 34)], fill=INK)
        d.rectangle([sx + sw / 2 - 6, sy - 52, sx + sw / 2 + 6, sy], fill=INK)
        d.polygon([(sx + sw / 2 + 6, sy - 52), (sx + sw / 2 + 52, sy - 20), (sx + sw / 2 + 6, sy - 16)], fill=RED)
    # Explosion burst over the strait.
    cx, cy = x + w - 170, y + 110
    for r, col in ((74, RED), (52, OCHRE), (30, (240, 200, 120))):
        pts = []
        for k in range(12):
            import math
            ang = k * math.pi / 6
            rr = r if k % 2 == 0 else r * 0.55
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        d.polygon(pts, fill=col)


def art_chart(d, x, y, w, h):
    """Markets: a falling red line over gridlines, with a down arrow."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 26, 30))
    for i in range(1, 6):
        yy = y + i * h // 6
        d.line([(x + 30, yy), (x + w - 30, yy)], fill=(64, 66, 70), width=2)
    pts = [(x + 40, y + 70), (x + 160, y + 110), (x + 260, y + 96), (x + 360, y + 170),
           (x + 470, y + 150), (x + 570, y + 240), (x + 670, y + 300)]
    d.line(pts, fill=RED, width=10, joint="curve")
    for px, py in pts:
        d.ellipse([px - 9, py - 9, px + 9, py + 9], fill=(240, 240, 240))
    d.polygon([(x + 640, y + 250), (x + 700, y + 250), (x + 670, y + 320)], fill=RED)
    d.text((x + 36, y + h - 74), "\u22123.7%", font=sb(64), fill=RED)
    d.text((x + 300, y + h - 66), "S&P 500", font=sn(36), fill=(200, 200, 200))


ART = {"smoke": art_smoke, "strait": art_strait, "chart": art_chart}


def draw_hero(d, s, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    ART[s["art"]](d, x + 2, y + 2, w - 4, 280)
    ty = y + 300
    d.text((x + 24, ty), s["kicker"], font=sb(24), fill=RED)
    ty += 36
    hl = wrap(d, s["headline"], fb(54), w - 48)
    ty = draw_lines(d, hl[:3], x + 24, ty, fb(54), INK, 60)
    ty += 6
    dk = wrap(d, s["deck"], sn(28), w - 48)
    if len(hl) > 2:
        dk = dk[:2]
    ty = draw_lines(d, dk[:3], x + 24, ty, sn(28), INK, 38)
    ty += 8
    d.text((x + 24, ty), s["dateline"], font=sb(24), fill=GRAY)


def draw_heroes(d, y):
    y = section_label(d, "TOP STORIES", 70, y, W - 140)
    card_w = (W - 140 - 2 * 30) / 3
    for i, s in enumerate(HEROES):
        draw_hero(d, s, 70 + i * (card_w + 30), y, card_w, 620)
    return y + 620


# ---------------------------------------------------------------- motifs
def motif(d, kind, x, y, s):
    """Small flat icon, s x s box at (x, y)."""
    if kind == "drone":
        d.ellipse([x, y, x + s * 0.28, y + s * 0.28], outline=INK, width=4)
        d.ellipse([x + s * 0.72, y, x + s, y + s * 0.28], outline=INK, width=4)
        d.ellipse([x, y + s * 0.72, x + s * 0.28, y + s], outline=INK, width=4)
        d.ellipse([x + s * 0.72, y + s * 0.72, x + s, y + s], outline=INK, width=4)
        d.rectangle([x + s * 0.3, y + s * 0.3, x + s * 0.7, y + s * 0.7], fill=RED)
    elif kind == "ship":
        d.polygon([(x, y + s * 0.55), (x + s, y + s * 0.55), (x + s * 0.85, y + s * 0.9),
                   (x + s * 0.15, y + s * 0.9)], fill=INK)
        d.rectangle([x + s * 0.45, y + s * 0.1, x + s * 0.55, y + s * 0.55], fill=INK)
        d.polygon([(x + s * 0.55, y + s * 0.1), (x + s * 0.9, y + s * 0.4), (x + s * 0.55, y + s * 0.4)], fill=RED)
    elif kind == "badge":
        d.polygon([(x + s * 0.5, y), (x + s * 0.95, y + s * 0.2), (x + s * 0.95, y + s * 0.55),
                   (x + s * 0.5, y + s), (x + s * 0.05, y + s * 0.55), (x + s * 0.05, y + s * 0.2)], fill=TEAL)
        d.text((x + s * 0.32, y + s * 0.28), "\u2605", font=sb(int(s * 0.42)), fill=PAPER)
    elif kind == "trophy":
        d.polygon([(x + s * 0.25, y + s * 0.05), (x + s * 0.75, y + s * 0.05), (x + s * 0.65, y + s * 0.55),
                   (x + s * 0.35, y + s * 0.55)], fill=OCHRE)
        d.arc([x, y, x + s * 0.35, y + s * 0.4], 90, 270, fill=OCHRE, width=6)
        d.arc([x + s * 0.65, y, x + s, y + s * 0.4], -90, 90, fill=OCHRE, width=6)
        d.rectangle([x + s * 0.4, y + s * 0.55, x + s * 0.6, y + s * 0.75], fill=OCHRE)
        d.rectangle([x + s * 0.3, y + s * 0.75, x + s * 0.7, y + s * 0.85], fill=OCHRE)
    elif kind == "cap":
        d.polygon([(x, y + s * 0.4), (x + s * 0.5, y + s * 0.15), (x + s, y + s * 0.4),
                   (x + s * 0.5, y + s * 0.65)], fill=INK)
        d.polygon([(x + s * 0.3, y + s * 0.5), (x + s * 0.7, y + s * 0.5), (x + s * 0.7, y + s * 0.8),
                   (x + s * 0.3, y + s * 0.8)], fill=INK)
        d.line([(x + s * 0.92, y + s * 0.4), (x + s * 0.92, y + s * 0.85)], fill=RED, width=5)
    elif kind == "flags":
        d.line([(x + s * 0.3, y + s * 0.05), (x + s * 0.3, y + s * 0.95)], fill=INK, width=5)
        d.line([(x + s * 0.65, y + s * 0.05), (x + s * 0.65, y + s * 0.95)], fill=INK, width=5)
        d.polygon([(x + s * 0.3, y + s * 0.05), (x + s * 0.62, y + s * 0.18), (x + s * 0.3, y + s * 0.32)], fill=RED)
        d.polygon([(x + s * 0.65, y + s * 0.05), (x + s * 0.97, y + s * 0.18), (x + s * 0.65, y + s * 0.32)], fill=TEAL)
    elif kind == "gavel":
        d.rectangle([x + s * 0.15, y + s * 0.2, x + s * 0.75, y + s * 0.42], fill=INK)
        d.line([(x + s * 0.55, y + s * 0.3), (x + s * 0.9, y + s * 0.75)], fill=INK, width=8)
        d.rectangle([x + s * 0.15, y + s * 0.78, x + s * 0.75, y + s * 0.9], fill=OCHRE)
    elif kind == "flame":
        d.polygon([(x + s * 0.5, y), (x + s * 0.85, y + s * 0.45), (x + s * 0.7, y + s * 0.7),
                   (x + s * 0.85, y + s * 0.95), (x + s * 0.15, y + s * 0.95), (x + s * 0.3, y + s * 0.7),
                   (x + s * 0.15, y + s * 0.45)], fill=RED)
        d.polygon([(x + s * 0.5, y + s * 0.4), (x + s * 0.7, y + s * 0.65), (x + s * 0.5, y + s * 0.95),
                   (x + s * 0.3, y + s * 0.65)], fill=OCHRE)
    elif kind == "bat":
        d.rectangle([x + s * 0.42, y + s * 0.05, x + s * 0.58, y + s * 0.5], fill=OCHRE)
        d.rectangle([x + s * 0.3, y + s * 0.5, x + s * 0.7, y + s * 0.95], fill=INK)
        d.ellipse([x + s * 0.72, y + s * 0.1, x + s * 0.98, y + s * 0.36], fill=RED)
    elif kind == "chip":
        d.rectangle([x + s * 0.2, y + s * 0.2, x + s * 0.8, y + s * 0.8], fill=INK)
        d.rectangle([x + s * 0.38, y + s * 0.38, x + s * 0.62, y + s * 0.62], fill=TEAL)
        for k in range(3):
            d.line([(x + s * (0.3 + k * 0.2), y), (x + s * (0.3 + k * 0.2), y + s * 0.2)], fill=INK, width=4)
            d.line([(x + s * (0.3 + k * 0.2), y + s * 0.8), (x + s * (0.3 + k * 0.2), y + s)], fill=INK, width=4)


def draw_grid(d, y):
    y = section_label(d, "THE DAY IN BRIEF", 70, y, W - 140)
    card_w = (W - 140 - 30) / 2
    card_h = 186
    for i, s in enumerate(GRID):
        cx = 70 + (i % 2) * (card_w + 30)
        cy = y + (i // 2) * (card_h + 16)
        d.rectangle([cx, cy, cx + card_w, cy + card_h], outline=RULE, width=2)
        # Number badge.
        d.ellipse([cx + 18, cy + 18, cx + 66, cy + 66], fill=RED)
        nt = str(s["n"])
        d.text((cx + 42 - d.textlength(nt, font=sb(30)) / 2, cy + 24), nt, font=sb(30), fill=PAPER)
        motif(d, s["motif"], cx + 84, cy + 46, 84)
        tx = cx + 196
        tw = card_w - 196 - 24
        d.text((tx, cy + 16), s["region"], font=sb(24), fill=RED)
        hl = wrap(d, s["headline"], fb(38), tw)
        yy = draw_lines(d, hl[:2], tx, cy + 48, fb(38), INK, 46)
        dk = wrap(d, s["deck"], sn(26), tw)
        if len(hl) > 1:
            dk = dk[:1]
        yy = draw_lines(d, dk[:2], tx, yy + 4, sn(26), INK, 32)
        d.text((tx, yy + 6), s["dateline"], font=sb(22), fill=GRAY)
    return y + 5 * (card_h + 16) - 16

# ---------------------------------------------------------------- world map
CONTINENTS = [
    # North America
    [(-170, 70), (-140, 70), (-120, 72), (-95, 80), (-80, 73), (-60, 60), (-55, 47),
     (-70, 42), (-75, 35), (-80, 25), (-85, 20), (-95, 18), (-105, 22), (-115, 30),
     (-125, 40), (-125, 50), (-150, 60), (-170, 65)],
    # South America
    [(-80, 10), (-60, 5), (-50, 0), (-35, -5), (-40, -20), (-50, -30), (-60, -40),
     (-70, -50), (-75, -35), (-80, -20), (-80, -5)],
    # Europe
    [(-10, 36), (0, 38), (10, 38), (20, 40), (28, 36), (30, 42), (25, 45), (20, 50),
     (10, 55), (5, 58), (0, 60), (-5, 58), (-10, 50), (-10, 43)],
    # Africa
    [(-10, 35), (0, 35), (10, 32), (20, 32), (32, 31), (35, 28), (40, 15), (48, 11),
     (51, 10), (45, 0), (40, -10), (35, -20), (30, -30), (20, -35), (15, -30),
     (12, -18), (9, -5), (9, 4), (-8, 5), (-15, 12), (-17, 20), (-15, 28)],
    # Asia
    [(30, 42), (40, 45), (50, 47), (60, 50), (70, 55), (80, 60), (90, 65), (100, 70),
     (110, 73), (130, 72), (150, 70), (160, 65), (170, 66), (162, 60), (158, 52),
     (142, 45), (135, 35), (130, 33), (127, 35), (122, 38), (120, 30), (110, 20),
     (105, 10), (100, 8), (95, 15), (90, 22), (85, 20), (80, 15), (77, 8), (75, 12),
     (70, 20), (65, 25), (60, 25), (55, 26), (50, 29), (48, 30), (44, 29), (40, 36), (35, 36), (30, 36)],
    # Australia
    [(113, -22), (114, -30), (120, -34), (130, -32), (140, -38), (147, -39), (150, -37),
     (153, -27), (150, -22), (146, -19), (142, -15), (142, -11), (137, -12), (132, -12),
     (130, -13), (126, -14), (122, -17), (118, -20), (113, -22)],
]


def project(lon, lat, x, y, w, h):
    px = x + (lon + 180) / 360 * w
    py = y + (85 - lat) / 145 * h
    return px, py


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=RULE, width=2)
    d.text((x + 20, y + 14), "WHERE IT HAPPENED \u2014 STORIES 1\u201313", font=sb(26), fill=RED)
    mx, my, mw, mh = x + 20, y + 56, w - 40, h - 140
    for poly in CONTINENTS:
        pts = [project(lon, lat, mx, my, mw, mh) for lon, lat in poly]
        d.polygon(pts, fill=LIGHT, outline=(150, 143, 125))
    for s in HEROES + GRID:
        px, py = project(s["lon"], s["lat"], mx, my, mw, mh)
        r = 17
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED, outline=PAPER, width=3)
        nt = str(s["n"])
        d.text((px - d.textlength(nt, font=sb(20)) / 2, py - 11), nt, font=sb(20), fill=PAPER)
    # Pull-quote along the bottom of the map box.
    rule(d, x + 20, x + w - 20, y + h - 78, fill=RULE, width=2)
    qlines = wrap(d, QUOTE, fi(28), w - 40)
    draw_lines(d, qlines[:2], x + 20, y + h - 64, fi(28), INK, 34)


def draw_data_check(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], outline=INK, width=3)
    d.text((x + 24, y + 18), "DATA CHECK", font=sb(30), fill=RED)
    rule(d, x + 24, x + w - 24, y + 58, fill=RULE, width=2)
    yy = y + 76
    for big, text, src in DATA_CHECK:
        bf = sb(40)
        d.text((x + 24, yy + 2), big, font=bf, fill=INK)
        tlines = wrap(d, text, sn(26), w - 48 - 210)
        ty = draw_lines(d, tlines[:2], x + 24 + 210, yy, sn(26), INK, 32)
        d.text((x + 24 + 210, ty + 2), "SOURCE: " + src, font=sb(20), fill=GRAY)
        yy = max(yy + 58, ty + 22) + 10
        if yy < y + h - 30:
            rule(d, x + 24, x + w - 24, yy, fill=RULE, width=1)
            yy += 14


# ---------------------------------------------------------------- also-on rail
def draw_rail(d, y):
    y = section_label(d, "ALSO ON \u2014 THE REST OF THE DAY", 70, y, W - 140)
    col_w = (W - 140 - 2 * 40) / 3
    for i, (n, headline, city) in enumerate(RAIL):
        col = i // 7
        row = i % 7
        x = 70 + col * (col_w + 40)
        ry = y + row * 52
        d.ellipse([x, ry + 4, x + 34, ry + 38], fill=RED)
        nt = str(n)
        d.text((x + 17 - d.textlength(nt, font=sb(22)) / 2, ry + 8), nt, font=sb(22), fill=PAPER)
        tx = x + 46
        hl = wrap(d, headline, sb(25), col_w - 46)
        yy = draw_lines(d, hl[:2], tx, ry, sb(25), INK, 29)
        d.text((tx, yy + 1), city, font=sb(22), fill=GRAY)
    return y + 7 * 52


# ---------------------------------------------------------------- build page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    y = draw_masthead(d)
    y = draw_stats(d, y + 18)
    y = draw_heroes(d, y + 26)
    y = draw_grid(d, y + 26)

    # Map (left) + data check (right).
    map_w = 1440
    dc_w = W - 140 - map_w - 30
    draw_map(d, 70, y + 26, map_w, 480)
    draw_data_check(d, 70 + map_w + 30, y + 26, dc_w, 480)
    y = y + 26 + 480

    y = draw_rail(d, y + 26)

    # Footer.
    rule(d, 70, W - 70, H - 78, fill=INK, width=3)
    f = sn(24)
    foot = ("THE WORLD \u00b7 Monday 23 November 2026 \u00b7 All 34 stories verified against "
            "reporting published 23 November 2026")
    d.text((70, H - 62), foot, font=f, fill=GRAY)
    right = "news-image-20261123"
    d.text((W - 70 - d.textlength(right, font=f), H - 62), right, font=f, fill=GRAY)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "entry.png"
    # Quantize to a 256-colour palette: the page is flat editorial colour,
    # and this keeps the file in the 200-400 KB range the winners sit in.
    img_q = img.convert("P", palette=Image.ADAPTIVE, colors=256)
    img_q.save(out, "PNG", optimize=True)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
