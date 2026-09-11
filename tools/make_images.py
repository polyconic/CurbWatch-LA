"""Placeholder icons and share image. Replace with final artwork when the identity is designed."""
import json, math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
MOSS, PAPER, RED, STONE, INK = (78, 122, 82), (251, 250, 246), (224, 98, 90), (238, 234, 225), (42, 41, 38)


def icon(size, pad=0.0, radius=0.235):
    S = size * 8
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    inset = round(S * pad)
    d.rounded_rectangle([inset, inset, S - inset, S - inset], radius=round((S - 2 * inset) * radius) if radius else 0, fill=MOSS)
    c, r, w = S / 2, (S - 2 * inset) * 0.234, (S - 2 * inset) * 0.117
    d.arc([c - r, c - r, c + r, c + r], 45, 315, fill=PAPER, width=round(w))
    for a in (45, 315):
        x, y = c + r * math.cos(math.radians(a)) - w / 2 * math.cos(math.radians(a)), c + r * math.sin(math.radians(a)) - w / 2 * math.sin(math.radians(a))
        d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=PAPER)
    dr = (S - 2 * inset) * 0.07
    d.ellipse([c + r * 0.87 - dr, c - dr, c + r * 0.87 + dr, c + dr], fill=RED)
    return im.resize((size, size), Image.LANCZOS)


icon(32).save(ROOT / 'favicon-32.png')
icon(180, radius=0).convert('RGB').save(ROOT / 'apple-touch-icon.png')
icon(192).save(ROOT / 'icon-192.png')
icon(512).save(ROOT / 'icon-512.png')
icon(512, pad=0.1, radius=0).save(ROOT / 'icon-maskable-512.png')
Image.alpha_composite(Image.new('RGBA', (512, 512), MOSS + (255,)), icon(512, pad=0.1, radius=0)).save(ROOT / 'icon-maskable-512.png')

# share image: the real street network, colored like the app
C = json.loads((ROOT / 'curb-data.js').read_text()[len('window.CURB='):-1])
W, H, SS = 1200, 630, 2
im = Image.new('RGB', (W * SS, H * SS), STONE); d = ImageDraw.Draw(im)
lon0, lat0 = C['meta']['lon0'], C['meta']['lat0']
x0, x1, y0, y1 = -118.392, -118.232, 34.047, 34.113
k = math.cos(math.radians(34.08))
scale = min((W * 0.58) / ((x1 - x0) * k), (H - 90) / (y1 - y0)) * SS
ox, oy = W * 0.43 * SS, (H * SS - (y1 - y0) * scale) / 2


def xy(lon, lat):
    return ox + (lon - x0) * k * scale, oy + (y1 - lat) * scale


def dec(a, s=0):
    x = y = 0; out = []
    for i in range(s, len(a), 2):
        x += a[i]; y += a[i + 1]; out.append(xy(lon0 + x / 1e5, lat0 + y / 1e5))
    return out


for g in C['green']:
    pts = dec(g, 1)
    if len(pts) > 2: d.polygon(pts, fill=(196, 213, 220) if g[0] else (213, 221, 195))
for r in C['roads']:
    d.line(dec(r, 1), fill=(255, 255, 255) if r[0] <= 2 else (250, 248, 243), width=(5 if r[0] <= 2 else 2) * SS // 2)
for b in C['blocks']:
    col = (75, 111, 176) if b[11] else (78, 138, 90) if b[6] else (200, 67, 59) if b[4] and b[8] and b[8][0][0].startswith('NO PARK/STREET') else None
    if col: d.line(dec(b[9]), fill=col, width=3 * SS // 2)
fade = Image.new('L', (W * SS, 1)); fade.putdata([max(0, min(255, int(255 * (1 - (x / (W * SS) - 0.40) / 0.16)))) for x in range(W * SS)])
im.paste(Image.new('RGB', im.size, STONE), (0, 0), fade.resize(im.size))
d = ImageDraw.Draw(im)
serif = '/System/Library/Fonts/Supplemental/Georgia Bold.ttf'
sans = '/System/Library/Fonts/HelveticaNeue.ttc'
d.text((72 * SS, 196 * SS), 'CurbWatch', font=ImageFont.truetype(serif, 92 * SS), fill=INK)
d.text((72 * SS, 300 * SS), 'LA', font=ImageFont.truetype(serif, 92 * SS), fill=MOSS)
body = ImageFont.truetype(sans, 27 * SS)
for i, line in enumerate(['Sweeping days, permit streets and', 'where tickets get written, block by block.']):
    d.text((74 * SS, (420 + i * 38) * SS), line, font=body, fill=(107, 103, 95))
for i, col in enumerate([(200, 67, 59), (196, 143, 44), (78, 138, 90), (75, 111, 176), (138, 79, 163)]):
    d.rounded_rectangle([(74 + i * 46) * SS, 520 * SS, (110 + i * 46) * SS, 528 * SS], radius=4 * SS, fill=col)
im.resize((W, H), Image.LANCZOS).save(ROOT / 'og-image.png', optimize=True)
print('icons + og-image.png written')
