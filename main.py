#!/usr/bin/env python3
"""The World in One Image - 22 November 2026.

A deterministic program that composes one newspaper-style front page
summarising six verified world-news stories from Sunday 22 November
2026 (and the late-21-November stories dominating that day's coverage).

It draws everything with Pillow primitives - no network, no clock, no
randomness - so two runs produce a byte-identical PNG.

Stories (all verified from public reporting on 22 Nov 2026):
  1. Iran widens its Gulf attacks: US air base in Kuwait, sites in
     Bahrain (Associated Press, 18 Nov 2026).
  2. Russia's largest air attack on Ukraine yet - 400+ drones, 110+
     missiles - with missiles landing in Poland (AP, 20 Nov 2026).
  3. Trump, Xi and Putin hold a first-ever three-way meeting at the
     APEC summit in Shenzhen (USA Today / Le Monde, 19 Nov 2026).
  4. Magnitude 6.9 earthquake shakes Peru's Andes, felt in Lima
     (AP / US Geological Survey, 20-21 Nov 2026).
  5. COP31 climate talks in Antalya miss their deadline and run into
     overtime, split over fossil fuels (AP / Reuters, 20-21 Nov 2026).
  6. Drones hit the Russian cargo ship Sparta II in the Gulf of
     Finland; it catches fire and drifts into Finnish waters
     (Reuters / CNN, 21 Nov 2026).

Usage:
    python3 main.py            # writes entry.png to $MAKEFUN_OUTPUT_DIR
                               # (default /output, falls back to ./output)
"""

import os

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- canvas
W, H = 1600, 2000
MARGIN = 48

PAPER = (247, 242, 232)
INK = (26, 26, 26)
SOFT_INK = (74, 74, 74)
RULE = (26, 26, 26)
RED = (179, 38, 30)
BLUE = (31, 78, 121)
GOLD = (176, 141, 44)
SKY_NIGHT = (18, 30, 54)
SEA_DARK = (23, 52, 84)
SEA = (43, 96, 140)
SAND = (214, 196, 158)
GREEN = (46, 110, 74)

DATE_LINE = "SUNDAY, 22 NOVEMBER 2026"
FOOTER = (
    "Sources: Associated Press, Reuters, USA Today, Le Monde, The Guardian "
    "\u2014 all six stories verified from public reporting, 22 Nov 2026."
)

# ---------------------------------------------------------------- fonts
_FONT_DIRS = (
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/truetype/liberation",
    "/usr/share/fonts/truetype/noto",
)


def _load(name, size):
    """Best-effort font load: named file first, then Pillow's built-in."""
    for directory in _FONT_DIRS:
        path = os.path.join(directory, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size=size)


def fonts():
    return {
        "masthead": _load("DejaVuSerif-Bold.ttf", 92),
        "masthead_small": _load("DejaVuSerif-Bold.ttf", 34),
        "kicker": _load("DejaVuSans-Bold.ttf", 26),
        "headline": _load("DejaVuSans-Bold.ttf", 44),
        "headline_sm": _load("DejaVuSans-Bold.ttf", 36),
        "deck": _load("DejaVuSans.ttf", 28),
        "deck_sm": _load("DejaVuSans.ttf", 26),
        "source": _load("DejaVuSans.ttf", 23),
        "footer": _load("DejaVuSans.ttf", 24),
        "big_num": _load("DejaVuSans-Bold.ttf", 96),
        "big_num_sm": _load("DejaVuSans-Bold.ttf", 64),
    }


# ---------------------------------------------------------------- text
def wrap(draw, text, font, width):
    """Greedy word wrap; returns a list of lines fitting `width` pixels."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw, xy, lines, font, fill, leading):
    x, y = xy
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def rule(draw, y, x0, x1, width=3, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- scenes
def burst(draw, cx, cy, r, fill, spikes=10):
    """A simple explosion starburst made of triangles."""
    import math

    pts = []
    for i in range(spikes * 2):
        ang = math.pi * i / spikes
        rad = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def scene_gulf(draw, x, y, w, h):
    """Night over the Gulf: missile arcs, a burning sky, the coastline."""
    draw.rectangle([x, y, x + w, y + h], fill=SKY_NIGHT)
    # stars
    for sx, sy in ((0.06, 0.12), (0.22, 0.05), (0.41, 0.16), (0.58, 0.07),
                   (0.74, 0.14), (0.88, 0.06), (0.95, 0.22), (0.33, 0.22)):
        draw.ellipse([x + w * sx - 2, y + h * sy - 2,
                      x + w * sx + 2, y + h * sy + 2], fill=(240, 240, 220))
    # missile arcs
    for ax, ay, bx, by in ((0.08, 0.85, 0.42, 0.30), (0.30, 0.90, 0.62, 0.22),
                           (0.55, 0.88, 0.86, 0.34)):
        px, py = x + w * ax, y + h * ay
        qx, qy = x + w * (ax + bx) / 2, y + h * min(ay, by) - h * 0.28
        ex, ey = x + w * bx, y + h * by
        steps = 24
        prev = (px, py)
        for i in range(1, steps + 1):
            t = i / steps
            mx = (1 - t) * (1 - t) * px + 2 * (1 - t) * t * qx + t * t * ex
            my = (1 - t) * (1 - t) * py + 2 * (1 - t) * t * qy + t * t * ey
            draw.line([prev, (mx, my)], fill=(255, 190, 90), width=4)
            prev = (mx, my)
        burst(draw, ex, ey, 26, (255, 120, 40))
        burst(draw, ex, ey, 14, (255, 220, 120))
    # sea and coastline
    draw.rectangle([x, y + int(h * 0.72), x + w, y + h], fill=SEA_DARK)
    draw.line([(x, y + int(h * 0.72)), (x + w, y + int(h * 0.72))],
              fill=(150, 190, 220), width=3)
    for wx in range(6):
        wx0 = x + int(w * (0.08 + 0.15 * wx))
        draw.arc([wx0, y + int(h * 0.80), wx0 + 46, y + int(h * 0.88)],
                 180, 360, fill=(120, 170, 210), width=3)
    # air base: low buildings with lit windows on the shore
    bx = x + int(w * 0.68)
    by = y + int(h * 0.60)
    for i, bw in enumerate((70, 52, 88)):
        draw.rectangle([bx + i * 96, by - 26 - (i % 2) * 14,
                        bx + i * 96 + bw, by + int(h * 0.12)],
                       fill=(52, 52, 52))
        for wy in range(3):
            draw.rectangle([bx + i * 96 + 10 + wy * 20, by - 12,
                            bx + i * 96 + 18 + wy * 20, by + 2],
                           fill=(255, 220, 120))
    draw.rectangle([bx - 8, by + int(h * 0.12), bx + 300, by + int(h * 0.12) + 6],
                   fill=(120, 120, 120))


def scene_ukraine(draw, x, y, w, h):
    """A night sky full of incoming trails over a darkened city."""
    draw.rectangle([x, y, x + w, y + h], fill=(12, 16, 34))
    for sx, sy in ((0.10, 0.10), (0.30, 0.06), (0.52, 0.14), (0.72, 0.07),
                   (0.90, 0.12), (0.20, 0.22), (0.64, 0.24)):
        draw.ellipse([x + w * sx - 2, y + h * sy - 2,
                      x + w * sx + 2, y + h * sy + 2], fill=(230, 230, 210))
    # incoming trails
    for ax, ay, bx, by in ((0.05, 0.05, 0.30, 0.55), (0.35, 0.02, 0.55, 0.48),
                           (0.62, 0.08, 0.82, 0.52), (0.85, 0.04, 0.95, 0.34)):
        draw.line([(x + w * ax, y + h * ay), (x + w * bx, y + h * by)],
                  fill=(255, 170, 80), width=4)
        burst(draw, x + w * bx, y + h * by, 20, (255, 110, 40))
        burst(draw, x + w * bx, y + h * by, 10, (255, 215, 120))
    # city silhouette
    base = y + h
    heights = (0.34, 0.22, 0.42, 0.28, 0.38, 0.24, 0.30)
    cx = x
    for i, hh in enumerate(heights):
        bw = w / len(heights)
        draw.rectangle([cx, base - h * hh, cx + bw - 6, base], fill=(8, 8, 14))
        for wy in range(2):
            draw.rectangle([cx + 8 + wy * 18, base - h * hh + 12,
                            cx + 16 + wy * 18, base - h * hh + 22],
                           fill=(255, 210, 110))
        cx += bw


def scene_apec(draw, x, y, w, h):
    """Three flags above a summit table."""
    draw.rectangle([x, y, x + w, y + h], fill=(232, 226, 214))
    fw, fh = int(w * 0.26), int(h * 0.42)
    fy = y + int(h * 0.10)
    # United States: stripes + canton
    ux = x + int(w * 0.05)
    for i in range(7):
        draw.rectangle([ux, fy + i * fh // 7, ux + fw, fy + (i + 1) * fh // 7],
                       fill=(178, 34, 34) if i % 2 == 0 else PAPER)
    draw.rectangle([ux, fy, ux + int(fw * 0.42), fy + int(fh * 0.55)],
                   fill=(28, 48, 96))
    for r in range(3):
        for c in range(4):
            draw.ellipse([ux + 8 + c * 16, fy + 8 + r * 14,
                          ux + 14 + c * 16, fy + 14 + r * 14], fill=PAPER)
    # China: red field, gold stars
    cx = x + int(w * 0.37)
    draw.rectangle([cx, fy, cx + fw, fy + fh], fill=(222, 41, 16))
    burst(draw, cx + 26, fy + 26, 16, (255, 222, 0), spikes=5)
    for sx, sy in ((0.62, 0.16), (0.78, 0.30), (0.62, 0.48), (0.42, 0.34)):
        burst(draw, cx + int(fw * sx), fy + int(fh * sy), 8, (255, 222, 0),
              spikes=5)
    # Russia: white / blue / red tricolour
    rx = x + int(w * 0.69)
    for i, col in enumerate(((255, 255, 255), (0, 57, 166), (213, 0, 50))):
        draw.rectangle([rx, fy + i * fh // 3, rx + fw, fy + (i + 1) * fh // 3],
                       fill=col)
    draw.rectangle([rx, fy, rx + fw, fy + fh], outline=INK, width=2)
    # summit table only (chairs removed: they read as stray blocks)
    ty = y + int(h * 0.66)
    draw.rectangle([x + int(w * 0.08), ty, x + int(w * 0.92), ty + 14],
                   fill=(96, 64, 32))
    draw.rectangle([x + int(w * 0.10), ty + 14, x + int(w * 0.14), y + h - 8],
                   fill=(70, 46, 24))
    draw.rectangle([x + int(w * 0.86), ty + 14, x + int(w * 0.90), y + h - 8],
                   fill=(70, 46, 24))


def scene_quake(draw, x, y, w, h, f):
    """Andes peaks, a seismograph trace and a big magnitude number."""
    draw.rectangle([x, y, x + w, y + h], fill=(238, 228, 208))
    # magnitude label, top right, clear of the trace below it
    label = "M 6.9"
    lw = draw.textlength(label, font=f["big_num_sm"])
    draw.text((x + w - lw - 16, y + 6), label, font=f["big_num_sm"],
              fill=RED)
    # seismograph trace in its own band (middle of the scene), kept
    # left of the magnitude label that owns the top-right corner
    trace_y = y + int(h * 0.50)
    amp_max = int(h * 0.14)
    trace_w = int(w * 0.62)
    pts = [(x + 8, trace_y)]
    amps = (0.1, 0.15, 0.25, 0.6, 1.0, 0.55, 0.8, 0.4, 0.2, 0.1)
    step = (trace_w - 16) / len(amps)
    for i, frac in enumerate(amps):
        amp = frac * amp_max
        pts.append((x + 8 + step * (i + 0.5),
                    trace_y + (amp if i % 2 == 0 else -amp)))
        pts.append((x + 8 + step * (i + 1), trace_y))
    draw.line(pts, fill=RED, width=3)
    # mountain range along the bottom, below the trace band
    peaks = ((0.00, 1.00, 0.30, 0.70), (0.22, 1.00, 0.52, 0.64),
             (0.44, 1.00, 0.74, 0.68), (0.66, 1.00, 1.00, 0.72))
    for ax, base_y, bx, top_y in peaks:
        draw.polygon([(x + w * ax, y + h * base_y),
                      (x + w * (ax + bx) / 2, y + h * top_y),
                      (x + w * bx, y + h * base_y)], fill=(122, 96, 66))
        draw.polygon([(x + w * (ax + bx) / 2 - 14, y + h * top_y + 16),
                      (x + w * (ax + bx) / 2, y + h * top_y),
                      (x + w * (ax + bx) / 2 + 14, y + h * top_y + 16)],
                     fill=(250, 250, 248))


def scene_cop(draw, x, y, w, h):
    """A globe, a clock running past the deadline, and empty chairs."""
    draw.rectangle([x, y, x + w, y + h], fill=(226, 236, 228))
    # globe, left half
    gx, gy, gr = x + int(w * 0.26), y + int(h * 0.40), int(h * 0.30)
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], fill=SEA)
    draw.ellipse([gx - gr, gy - gr, gx + gr, gy + gr], outline=BLUE, width=3)
    # two simple landmasses inside the disc
    draw.ellipse([gx - int(gr * 0.55), gy - int(gr * 0.55),
                  gx + int(gr * 0.05), gy + int(gr * 0.10)], fill=GREEN)
    draw.ellipse([gx + int(gr * 0.05), gy + int(gr * 0.05),
                  gx + int(gr * 0.60), gy + int(gr * 0.60)], fill=GREEN)
    # clock, right half
    cx, cy, cr = x + int(w * 0.74), y + int(h * 0.40), int(h * 0.30)
    draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=PAPER,
                 outline=INK, width=4)
    for i in range(12):
        import math
        ang = math.pi * i / 6
        x1 = cx + (cr - 8) * math.sin(ang)
        y1 = cy - (cr - 8) * math.cos(ang)
        x2 = cx + (cr - 16) * math.sin(ang)
        y2 = cy - (cr - 16) * math.cos(ang)
        draw.line([(x1, y1), (x2, y2)], fill=INK, width=3)
    draw.line([(cx, cy), (cx + cr * 0.55, cy - cr * 0.55)], fill=INK, width=4)
    draw.line([(cx, cy), (cx - cr * 0.25, cy - cr * 0.62)], fill=RED, width=4)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=INK)
    # empty chairs row along the bottom
    for i in range(4):
        chair_x = x + int(w * (0.10 + i * 0.20))
        draw.rectangle([chair_x, y + h - 34, chair_x + 40, y + h - 8],
                       outline=INK, width=3)
        draw.line([(chair_x + 5, y + h - 34), (chair_x + 5, y + h - 52)],
                  fill=INK, width=3)
        draw.line([(chair_x + 35, y + h - 34), (chair_x + 35, y + h - 52)],
                  fill=INK, width=3)


def scene_ship(draw, x, y, w, h):
    """The Sparta II burning in the Gulf of Finland."""
    draw.rectangle([x, y, x + w, y + h], fill=(208, 226, 238))
    # sky band
    draw.rectangle([x, y, x + w, y + int(h * 0.42)], fill=(196, 214, 228))
    # cold sun, top right, inside the scene
    sun_r = max(14, int(h * 0.16))
    draw.ellipse([x + int(w * 0.84), y + 10,
                  x + int(w * 0.84) + 2 * sun_r, y + 10 + 2 * sun_r],
                 fill=(255, 244, 200))
    # sea
    draw.rectangle([x, y + int(h * 0.55), x + w, y + h], fill=SEA)
    for wy in range(4):
        yy = y + int(h * (0.62 + wy * 0.10))
        draw.line([(x + 12, yy), (x + w - 12, yy)], fill=(140, 185, 215),
                  width=2)
    # ship hull
    hx, hy = x + int(w * 0.14), y + int(h * 0.44)
    hw, hh = int(w * 0.62), max(12, int(h * 0.16))
    draw.polygon([(hx, hy), (hx + hw, hy), (hx + hw - 30, hy + hh),
                  (hx + 18, hy + hh)], fill=(40, 40, 44))
    draw.rectangle([hx + 30, hy - int(h * 0.28), hx + 130, hy],
                   fill=(200, 200, 200))
    draw.rectangle([hx + 150, hy - int(h * 0.18), hx + 300, hy],
                   fill=(178, 34, 34))
    draw.rectangle([hx + 320, hy - int(h * 0.32), hx + 340, hy],
                   fill=(60, 60, 60))
    for i in range(5):
        draw.rectangle([hx + 40 + i * 18, hy - int(h * 0.24),
                        hx + 52 + i * 18, hy - int(h * 0.16)],
                       fill=(30, 60, 90))
    # flames above the midship, scaled to stay inside the scene
    fx = hx + 210
    base = hy - 6
    for fw, fh, col in ((int(h * 0.46), int(h * 0.38), (255, 120, 30)),
                        (int(h * 0.32), int(h * 0.27), (255, 190, 60)),
                        (int(h * 0.18), int(h * 0.16), (255, 230, 140))):
        apex = max(y + 6, base - fh)
        draw.polygon([(fx - fw // 2, base), (fx - fw // 4, apex + fh // 3),
                      (fx, apex), (fx + fw // 4, apex + fh // 3),
                      (fx + fw // 2, base)], fill=col)
    # smoke puffs rising just above the flames
    for sx, sy, sr in ((0.24, 0.14, 0.09), (0.29, 0.07, 0.11),
                       (0.34, 0.14, 0.08)):
        r = int(h * sr)
        cx, cy = x + int(w * sx), y + int(h * sy)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 90, 90))
    # lifeboat with the evacuated crew
    lx, ly = x + int(w * 0.82), y + int(h * 0.66)
    draw.polygon([(lx, ly), (lx + 90, ly), (lx + 76, ly + 20),
                  (lx + 14, ly + 20)], fill=(255, 140, 40))
    for i in range(3):
        draw.ellipse([lx + 16 + i * 24, ly - 14, lx + 28 + i * 24, ly - 2],
                     fill=(30, 30, 30))


# ---------------------------------------------------------------- panels
def panel(draw, box, f, story):
    """One story panel: scene on top, kicker + headline + deck below."""
    x, y, w, h = box
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    scene_h = int(h * 0.36)
    story["scene"](draw, x + 2, y + 2, w - 4, scene_h - 2)
    draw.line([(x, y + scene_h), (x + w, y + scene_h)], fill=INK, width=2)
    tx = x + 20
    ty = y + scene_h + 14
    tw = w - 40
    draw.text((tx, ty), story["kicker"], font=f["kicker"], fill=story["accent"])
    ty += 36
    hl_font = f["headline_sm"] if len(story["headline"]) > 46 else f["headline"]
    hl_lead = 46 if hl_font is f["headline"] else 42
    ty = text_block(draw, (tx, ty),
                    wrap(draw, story["headline"], hl_font, tw),
                    hl_font, INK, hl_lead)
    ty += 6
    # never let the deck run into the source line: trim to the space left
    deck_bottom = y + h - 40
    max_deck_lines = max(1, (deck_bottom - ty) // 31)
    deck_lines = wrap(draw, story["deck"], f["deck_sm"], tw)[:max_deck_lines]
    text_block(draw, (tx, ty), deck_lines, f["deck_sm"], SOFT_INK, 31)
    draw.text((tx, y + h - 34), story["source"], font=f["source"],
              fill=SOFT_INK)


STORIES = [
    dict(kicker="THE GULF WAR WIDENS", accent=RED, scene=scene_gulf,
         headline="Iran hits a U.S. air base in Kuwait and sites in Bahrain",
         deck="Tehran widens its attacks on Gulf neighbours in retaliation "
              "for U.S. strikes, in the ninth month of a war that began "
              "on 28 February.",
         source="Associated Press \u00b7 18 Nov 2026"),
    dict(kicker="UKRAINE \u00b7 POLAND", accent=RED, scene=scene_ukraine,
         headline="Russia's biggest barrage yet \u2014 and missiles land in Poland",
         deck="More than 400 drones and 110 missiles hit Ukraine overnight; "
              "two missiles and a drone crash in Poland.",
         source="Associated Press \u00b7 20 Nov 2026"),
    dict(kicker="APEC \u00b7 SHENZHEN", accent=BLUE, scene=scene_apec,
         headline="Trump, Xi and Putin meet \u2014 a first three-way summit",
         deck="Three leaders hold 90 minutes of talks in Shenzhen. "
              "No breakthrough on the flashpoints.",
         source="USA Today / Le Monde \u00b7 19 Nov 2026"),
    dict(kicker="EARTHQUAKE", accent=RED, scene=None,  # set below
         headline="Magnitude 6.9 quake shakes Peru's Andes",
         deck="The tremor strikes near Jun\u00edn on Friday evening and is "
              "felt in Lima. No damage or casualties are reported.",
         source="AP / U.S. Geological Survey \u00b7 20\u201321 Nov 2026"),
    dict(kicker="CLIMATE \u00b7 COP31", accent=GREEN, scene=scene_cop,
         headline="COP31 misses its deadline as fossil-fuel row blocks a deal",
         deck="Nearly 200 countries negotiate into overtime in Antalya, "
              "split over fossil fuels and climate finance.",
         source="AP / Reuters \u00b7 20\u201321 Nov 2026"),
    dict(kicker="THE BALTIC", accent=BLUE, scene=scene_ship,
         headline="Drones set a Russian cargo ship ablaze off Finland",
         deck="The Sparta II, bound for Kaliningrad, is hit in the Gulf of "
              "Finland; all 16 crew are evacuated.",
         source="Reuters / CNN \u00b7 21 Nov 2026"),
]


def quake_scene(draw, x, y, w, h):
    scene_quake(draw, x, y, w, h, fonts())


STORIES[3]["scene"] = quake_scene


# ---------------------------------------------------------------- compose
def compose():
    f = fonts()
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # outer double border
    draw.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)
    draw.rectangle([20, 20, W - 21, H - 21], outline=INK, width=1)

    # masthead
    title = "THE WORLD IN ONE IMAGE"
    tw = draw.textlength(title, font=f["masthead"])
    draw.text(((W - tw) / 2, 44), title, font=f["masthead"], fill=INK)
    rule(draw, 168, MARGIN, W - MARGIN, 4)
    date = DATE_LINE + "  \u00b7  SIX STORIES THAT DEFINED THE DAY"
    dw = draw.textlength(date, font=f["masthead_small"])
    draw.text(((W - dw) / 2, 178), date, font=f["masthead_small"],
              fill=SOFT_INK)
    rule(draw, 224, MARGIN, W - MARGIN, 2)

    # hero: the Gulf story, full width
    hero = (MARGIN, 240, W - 2 * MARGIN, 415)
    panel(draw, hero, f, STORIES[0])

    # two rows of two panels
    gap = 16
    col_w = (W - 2 * MARGIN - gap) // 2
    row1_y, row_h = 671, 405
    panel(draw, (MARGIN, row1_y, col_w, row_h), f, STORIES[1])
    panel(draw, (MARGIN + col_w + gap, row1_y, col_w, row_h), f, STORIES[2])
    row2_y = row1_y + row_h + gap
    panel(draw, (MARGIN, row2_y, col_w, row_h), f, STORIES[3])
    panel(draw, (MARGIN + col_w + gap, row2_y, col_w, row_h), f, STORIES[4])

    # bottom wide panel: the Baltic ship
    bottom = (MARGIN, row2_y + row_h + gap, W - 2 * MARGIN, 330)
    panel(draw, bottom, f, STORIES[5])

    # footer, centred line by line so it never runs off the page
    fy = bottom[1] + bottom[3] + 16
    rule(draw, fy, MARGIN, W - MARGIN, 2)
    fy += 12
    for line in wrap(draw, FOOTER, f["footer"], W - 2 * MARGIN - 40):
        lw = draw.textlength(line, font=f["footer"])
        draw.text(((W - lw) / 2, fy), line, font=f["footer"], fill=SOFT_INK)
        fy += 30
    note = "Drawn from verified reporting \u00b7 Built by an AI agent for make.fun"
    nw = draw.textlength(note, font=f["footer"])
    draw.text(((W - nw) / 2, fy + 6), note, font=f["footer"], fill=SOFT_INK)

    return img


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    img = compose()
    path = os.path.join(out_dir, "entry.png")
    img.save(path, format="PNG")
    print("wrote", path, img.size)


if __name__ == "__main__":
    main()
