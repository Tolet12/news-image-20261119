"""Draw the 19 November 2026 world-news front page as entry.png.

Original flat-shape newspaper collage, drawn entirely with Pillow
primitives (rectangles, polygons, ellipses, lines and text).
No randomness: every run produces byte-identical output.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = 1024
H = 1024

PAPER = (247, 242, 231)
INK = (20, 16, 12)
WHITE = (255, 255, 255)
SKY = (176, 216, 235)
SKY2 = (203, 232, 245)
SEA = (38, 110, 168)
SEA_DARK = (24, 84, 136)
SMOKE = (138, 138, 138)
SMOKE_DARK = (95, 95, 95)
FIRE = (242, 110, 20)
FIRE_Y = (250, 190, 30)
RED = (198, 32, 40)
TABLE = (110, 72, 40)
WALL = (222, 208, 178)
SAND = (226, 199, 142)
HULL = (35, 35, 40)
DECK = (90, 90, 98)
GREEN = (30, 140, 70)
GREEN_D = (20, 100, 50)
GOLD = (212, 160, 40)
WOOD = (140, 95, 50)
BENCH = (96, 62, 34)

SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, start, max_width, min_size=14):
    size = start
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 1
    return font(path, min_size)


def centered(draw, cx, y, text, f, fill=INK):
    w = draw.textlength(text, font=f)
    draw.text((cx - w / 2, y), text, font=f, fill=fill)
    return f.size


def wrap_text(draw, text, f, max_width):
    words = text.split()
    lines = []
    cur = ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=f) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def smoke(draw, cx, cy, r):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=SMOKE)
    draw.ellipse([cx - r - 14, cy - r // 2, cx + r // 2, cy + r // 2], fill=SMOKE_DARK)
    draw.ellipse([cx, cy - r - 10, cx + r + 16, cy + r // 3], fill=SMOKE)


def flame(draw, cx, base_y, w, h):
    draw.polygon(
        [(cx - w // 2, base_y), (cx, base_y - h), (cx + w // 2, base_y)],
        fill=FIRE,
    )
    inner_w = max(8, w // 2)
    inner_h = max(10, int(h * 0.6))
    draw.polygon(
        [(cx - inner_w // 2, base_y), (cx, base_y - inner_h), (cx + inner_w // 2, base_y)],
        fill=FIRE_Y,
    )


def figure(draw, cx, top_y, suit):
    # Head.
    draw.ellipse([cx - 17, top_y, cx + 17, top_y + 34], fill=(232, 190, 150), outline=INK, width=2)
    # Body: bold trapezoid suit with a white shirt triangle.
    draw.polygon(
        [(cx - 34, top_y + 92), (cx - 22, top_y + 36), (cx + 22, top_y + 36), (cx + 34, top_y + 92)],
        fill=suit, outline=INK, width=2,
    )
    draw.polygon(
        [(cx - 9, top_y + 36), (cx + 9, top_y + 36), (cx, top_y + 62)],
        fill=WHITE,
    )


def flag_us(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=WHITE, outline=INK, width=2)
    stripe = h / 7
    for i in range(7):
        if i % 2 == 0:
            draw.rectangle([x, y + i * stripe, x + w, y + (i + 1) * stripe], fill=RED)
    draw.rectangle([x, y, x + w * 0.45, y + stripe * 4], fill=(40, 60, 140))
    for r in range(3):
        for c in range(4):
            sx = x + 6 + c * 11
            sy = y + 5 + r * 10
            draw.ellipse([sx, sy, sx + 4, sy + 4], fill=WHITE)


def flag_china(draw, x, y, w, h):
    draw.rectangle([x, y, x + w, y + h], fill=(222, 30, 40), outline=INK, width=2)
    for (dx, dy, r) in [(12, 10, 7), (30, 6, 3), (36, 16, 3), (30, 26, 3), (24, 34, 3)]:
        draw.ellipse([x + dx - r, y + dy - r, x + dx + r, y + dy + r], fill=FIRE_Y)


def flag_russia(draw, x, y, w, h):
    third = h / 3
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    draw.rectangle([x, y, x + w, y + third], fill=WHITE)
    draw.rectangle([x, y + third, x + w, y + 2 * third], fill=(30, 70, 170))
    draw.rectangle([x, y + 2 * third, x + w, y + h], fill=RED)


def scene_summit(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY2)
    # Shenzhen skyline silhouette behind the leaders.
    towers = [(8, 120, 44), (58, 86, 36), (100, 138, 50), (156, 70, 34),
              (196, 108, 42), (244, 60, 30), (280, 126, 46), (332, 82, 36),
              (374, 112, 40), (420, 92, 34)]
    for (tx, th, tw) in towers:
        draw.rectangle([x0 + tx, y0 + 168 - th, x0 + tx + tw, y0 + 168],
                       fill=(120, 150, 175))
        for wy in range(y0 + 176 - th, y0 + 160, 16):
            draw.rectangle([x0 + tx + 7, wy, x0 + tx + 13, wy + 7], fill=FIRE_Y)
            draw.rectangle([x0 + tx + tw - 13, wy, x0 + tx + tw - 7, wy + 7], fill=FIRE_Y)
    draw.rectangle([x0, y0 + 168, x1, y1], fill=WALL)
    draw.rectangle([x0, y1 - 40, x1, y1], fill=(150, 110, 70))
    # Three flags on poles, flying above the leaders' heads.
    pole_top = y0 + 116
    flag_specs = [(x0 + 62, flag_china), (x0 + 192, flag_russia), (x0 + 322, flag_us)]
    for fx, painter in flag_specs:
        draw.line([fx, pole_top, fx, y0 + 172], fill=INK, width=4)
        painter(draw, fx + 4, pole_top, 88, 46)
    # Three leaders standing shoulder to shoulder, arms joined in a handshake.
    figure(draw, x0 + 116, y0 + 170, (150, 28, 34))
    figure(draw, x0 + 240, y0 + 170, (52, 52, 58))
    figure(draw, x1 - 116, y0 + 170, (30, 40, 90))
    draw.line([x0 + 148, y0 + 236, x0 + 208, y0 + 236], fill=INK, width=5)
    draw.line([x0 + 272, y0 + 236, x1 - 148, y0 + 236], fill=INK, width=5)
    # APEC plaque on the floor band in front.
    draw.rectangle([x0 + 196, y1 - 34, x0 + 284, y1 - 10], fill=RED, outline=INK, width=2)
    pf = fit_font(draw, "APEC", SANS_BOLD, 19, 80)
    centered(draw, x0 + 240, y1 - 32, "APEC", pf, fill=WHITE)


def scene_court(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(232, 224, 205))
    # Pediment and columns of the Peace Palace courtroom.
    draw.polygon([(x0 + 30, y0 + 62), (x0 + 240, y0 + 12), (x1 - 30, y0 + 62)],
                 fill=(198, 186, 160), outline=INK, width=3)
    draw.rectangle([x0 + 24, y0 + 62, x1 - 24, y0 + 78], fill=(198, 186, 160), outline=INK, width=3)
    for cx in (x0 + 58, x0 + 128, x0 + 352, x0 + 422):
        draw.rectangle([cx, y0 + 78, cx + 22, y0 + 168], fill=(214, 204, 182), outline=INK, width=2)
    draw.rectangle([x0 + 24, y0 + 168, x1 - 24, y0 + 182], fill=(198, 186, 160), outline=INK, width=3)
    # Scales of justice in the middle.
    cx = x0 + 240
    draw.line([cx, y0 + 92, cx, y0 + 168], fill=INK, width=5)
    draw.line([cx - 62, y0 + 104, cx + 62, y0 + 104], fill=INK, width=4)
    for sx in (cx - 62, cx + 62):
        draw.line([sx, y0 + 104, sx - 16, y0 + 136], fill=INK, width=3)
        draw.line([sx, y0 + 104, sx + 16, y0 + 136], fill=INK, width=3)
        draw.pieslice([sx - 24, y0 + 128, sx + 24, y0 + 152], start=0, end=180, fill=GOLD, outline=INK, width=2)
    draw.polygon([(cx - 22, y0 + 182), (cx + 22, y0 + 182), (cx + 12, y0 + 168), (cx - 12, y0 + 168)],
                 fill=INK)
    # Judges' bench with three robed silhouettes.
    bench_y = y0 + 196
    draw.rectangle([x0 + 52, bench_y + 34, x1 - 52, y1 - 8], fill=BENCH, outline=INK, width=3)
    for jx in (x0 + 128, x0 + 240, x1 - 128):
        draw.ellipse([jx - 15, bench_y - 6, jx + 15, bench_y + 24], fill=(232, 190, 150), outline=INK, width=2)
        draw.rectangle([jx - 15, bench_y - 12, jx + 15, bench_y - 4], fill=WHITE, outline=INK, width=1)
        draw.polygon([(jx - 26, bench_y + 40), (jx - 18, bench_y + 22), (jx + 18, bench_y + 22),
                      (jx + 26, bench_y + 40)], fill=(30, 30, 40), outline=INK, width=2)
    # ICJ plaque on the bench front.
    draw.rectangle([x0 + 202, bench_y + 38, x0 + 278, bench_y + 58], fill=(30, 40, 90), outline=INK, width=2)
    pf = fit_font(draw, "ICJ", SANS_BOLD, 16, 68)
    centered(draw, x0 + 240, bench_y + 40, "ICJ", pf, fill=WHITE)
    # A gavel resting at the right end of the bench.
    gx, gy = x1 - 108, bench_y + 46
    draw.line([gx, gy + 22, gx + 30, gy - 6], fill=WOOD, width=6)
    draw.rectangle([gx + 22, gy - 16, gx + 44, gy + 2], fill=WOOD, outline=INK, width=2)
    draw.rectangle([gx - 8, gy + 22, gx + 26, gy + 30], fill=WOOD, outline=INK, width=2)


def scene_ipo(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(16, 26, 44))
    # Grid of the exchange board.
    for gx in range(x0 + 40, x1 - 10, 56):
        draw.line([gx, y0 + 16, gx, y1 - 90], fill=(40, 60, 90), width=2)
    for gy in range(y0 + 30, y1 - 80, 44):
        draw.line([x0 + 16, gy, x1 - 16, gy], fill=(40, 60, 90), width=2)
    # Green candles climbing to the right.
    candles = [(44, 196, 168), (108, 178, 140), (172, 158, 116), (236, 132, 88),
               (300, 104, 60), (364, 74, 30)]
    for (ox, top, bot) in candles:
        lo, hi = min(top, bot), max(top, bot)
        cx = x0 + ox + 18
        draw.line([cx, y0 + lo - 14, cx, y0 + hi + 14], fill=GREEN, width=3)
        draw.rectangle([x0 + ox, y0 + lo, x0 + ox + 36, y0 + hi], fill=GREEN, outline=GREEN_D, width=2)
    # Big rising arrow over the candles.
    draw.line([x0 + 40, y0 + 210, x0 + 330, y0 + 58], fill=FIRE_Y, width=8)
    draw.polygon([(x0 + 330, y0 + 34), (x0 + 366, y0 + 78), (x0 + 306, y0 + 84)],
                 fill=FIRE_Y, outline=INK, width=2)
    # Ticker banner: the listing and its price.
    draw.rectangle([x0 + 20, y1 - 84, x1 - 20, y1 - 44], fill=WHITE, outline=INK, width=3)
    tf = fit_font(draw, "ANTHROPIC  $83", SANS_BOLD, 26, (x1 - x0) - 60)
    centered(draw, x0 + 240, y1 - 78, "ANTHROPIC  $83", tf, fill=GREEN_D)
    # The opening bell on a stand, left; gold coins, right.
    bx, by = x0 + 66, y1 - 128
    draw.rectangle([bx - 8, by + 34, bx + 52, by + 42], fill=WOOD, outline=INK, width=2)
    draw.pieslice([bx, by, bx + 36, by + 30], start=180, end=360, fill=GOLD, outline=INK, width=2)
    draw.rectangle([bx + 14, by - 8, bx + 22, by + 2], fill=GOLD, outline=INK, width=2)
    for (ox, oy, r) in [(396, 196, 13), (428, 212, 10), (364, 220, 9)]:
        draw.ellipse([x0 + ox - r, y0 + oy - r, x0 + ox + r, y0 + oy + r], fill=GOLD, outline=INK, width=2)
        cf = fit_font(draw, "$", SANS_BOLD, r + 4, 2 * r - 4)
        centered(draw, x0 + ox, y0 + oy - r // 2 - 3, "$", cf, fill=(120, 84, 10))


def mine(draw, cx, cy, r):
    import math
    for k in range(8):
        a = k * math.pi / 4
        x2 = cx + int((r + 8) * math.cos(a))
        y2 = cy + int((r + 8) * math.sin(a))
        draw.line([cx, cy, x2, y2], fill=INK, width=4)
        draw.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=INK)
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(52, 58, 66), outline=INK, width=2)
    draw.ellipse([cx - 5, cy - 6, cx + 1, cy], fill=RED)


def scene_hormuz(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=SKY)
    sea_y = y0 + 138
    draw.rectangle([x0, sea_y, x1, y1], fill=SEA)
    for wy in (sea_y + 34, sea_y + 70, sea_y + 100):
        for wx in range(x0 + 18, x1 - 50, 96):
            draw.line([wx, wy, wx + 44, wy], fill=SEA_DARK, width=4)
    # The two shores of the strait.
    draw.polygon([(x0, y1), (x0, sea_y + 44), (x0 + 96, sea_y + 58), (x0 + 130, y1)],
                 fill=SAND, outline=INK, width=3)
    draw.polygon([(x1, y1), (x1, sea_y + 40), (x1 - 90, sea_y + 54), (x1 - 124, y1)],
                 fill=SAND, outline=INK, width=3)
    # Supertanker mid-strait: long hull, deck houses, loaded low in the water.
    hx0, hy = x0 + 118, sea_y + 52
    hx1 = x1 - 108
    draw.polygon([(hx0, hy), (hx1, hy), (hx1 - 26, hy + 34), (hx0 + 18, hy + 34)],
                 fill=HULL, outline=INK, width=3)
    draw.rectangle([hx0 + 8, hy - 10, hx1 - 8, hy], fill=RED, outline=INK, width=2)
    draw.rectangle([hx0 + 26, hy - 34, hx0 + 62, hy - 10], fill=DECK, outline=INK, width=2)
    draw.rectangle([hx1 - 66, hy - 40, hx1 - 34, hy - 10], fill=WHITE, outline=INK, width=2)
    for px in range(hx0 + 84, hx1 - 84, 34):
        draw.line([px, hy - 10, px, hy - 20], fill=INK, width=3)
    draw.line([hx0 + 84, hy - 20, hx1 - 84, hy - 20], fill=INK, width=3)
    # Blast and fire where a mine struck the bow; smoke over the ship.
    flame(draw, hx1 - 44, hy - 8, 52, 58)
    flame(draw, hx1 - 88, hy - 10, 30, 34)
    smoke(draw, hx1 - 90, y0 + 52, 26)
    smoke(draw, hx1 - 150, y0 + 36, 19)
    smoke(draw, x0 + 128, y0 + 66, 15)
    # Naval mines bobbing in the channel around the tanker.
    mine(draw, x0 + 168, sea_y + 116, 15)
    mine(draw, x0 + 300, sea_y + 128, 12)
    mine(draw, x1 - 176, sea_y + 112, 13)
    # A second tanker silhouette far behind, turning away.
    draw.polygon([(x0 + 56, sea_y + 8), (x0 + 196, sea_y + 8), (x0 + 182, sea_y + 24), (x0 + 66, sea_y + 24)],
                 fill=(70, 76, 86), outline=INK, width=2)
    draw.rectangle([x0 + 150, sea_y - 8, x0 + 172, sea_y + 8], fill=(70, 76, 86), outline=INK, width=2)


def panel(draw, box, scene_fn, headline, subline):
    x0, y0, x1, y1 = box
    cap_h = 96
    scene_box = (x0, y0, x1, y1 - cap_h)
    scene_fn(draw, scene_box)
    draw.rectangle(scene_box, outline=INK, width=4)
    cap_y = y1 - cap_h
    draw.rectangle([x0, cap_y, x1, y1], fill=PAPER, outline=INK, width=4)
    cx = (x0 + x1) // 2
    hf = fit_font(draw, headline, SANS_BOLD, 31, (x1 - x0) - 20)
    centered(draw, cx, cap_y + 10, headline, hf)
    sf = fit_font(draw, subline, SANS_BOLD, 20, (x1 - x0) - 20)
    centered(draw, cx, cap_y + 52, subline, sf, fill=(70, 60, 48))


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- Masthead -------------------------------------------------------
    draw.line([24, 18, W - 24, 18], fill=INK, width=5)
    draw.line([24, 28, W - 24, 28], fill=INK, width=2)
    title = "THE WORLD IN ONE DAY"
    tf = fit_font(draw, title, SERIF_BOLD, 66, W - 48)
    centered(draw, W // 2, 36, title, tf)
    sub = "THURSDAY \u00b7 19 NOVEMBER 2026 \u00b7 THE DAY IN ONE PICTURE"
    sf = fit_font(draw, sub, SANS_BOLD, 24, W - 80)
    centered(draw, W // 2, 112, sub, sf)
    draw.line([24, 146, W - 24, 146], fill=INK, width=2)
    draw.line([24, 152, W - 24, 152], fill=INK, width=5)

    # ---- 2x2 panel grid --------------------------------------------------
    gx, gy, gap = 24, 168, 16
    pw = (W - 2 * gx - gap) // 2
    ph = 352
    panels = [
        ((gx, gy, gx + pw, gy + ph), scene_summit,
         "THREE LEADERS, ONE TABLE", "FIRST TRILATERAL SUMMIT \u2014 NO BIG DEAL"),
        ((gx + pw + gap, gy, gx + 2 * pw + gap, gy + ph), scene_court,
         "WORLD COURT: GENOCIDE", "MYANMAR RULED AGAINST OVER ROHINGYA"),
        ((gx, gy + ph + gap, gx + pw, gy + 2 * ph + gap), scene_ipo,
         "ANTHROPIC'S RECORD IPO", "$83 A SHARE \u2014 $81 BILLION RAISED"),
        ((gx + pw + gap, gy + ph + gap, gx + 2 * pw + gap, gy + 2 * ph + gap), scene_hormuz,
         "TANKERS HIT MINES IN HORMUZ", "SUPERTANKERS STRUCK IN THE STRAIT"),
    ]
    for box, scene_fn, headline, subline in panels:
        panel(draw, box, scene_fn, headline, subline)

    # ---- Bottom ticker ---------------------------------------------------
    tick_y = gy + 2 * ph + gap + 16
    draw.rectangle([0, tick_y, W, H], fill=INK)
    ticker = (
        "CRIMEA BRIDGE HIT A THIRD TIME \u2014 RAIL SPAN DOWN, TRAINS HALTED \u2022 "
        "US SENATE REJECTS IRAN WAR-POWERS CURB 51\u201348 \u2022 ISRAELI TANKS PUSH "
        "INTO CENTRAL GAZA \u2022 COP31 FINAL TALKS SPLIT ON FOSSIL FUELS \u2022 "
        "MIGRANT BOAT CAPSIZES OFF SENEGAL \u2014 DOZENS MISSING \u2022 DENMARK "
        "BACKS GREENLAND PACT 109\u20130"
    )
    tf2 = font(SANS_BOLD, 25)
    lines = wrap_text(draw, ticker, tf2, W - 56)
    while len(lines) > 2 and tf2.size > 16:
        tf2 = font(SANS_BOLD, tf2.size - 1)
        lines = wrap_text(draw, ticker, tf2, W - 56)
    line_h = tf2.size + 12
    total_h = len(lines) * line_h
    ly = tick_y + ((H - tick_y) - total_h) // 2
    for line in lines:
        centered(draw, W // 2, ly, line, tf2, fill=PAPER)
        ly += line_h

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=False)
    print(f"wrote {out} ({out.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
