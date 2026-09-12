"""Build og-image.png (1200x630 social card) from Greg's artwork, 'CURB WATCH.png'.

The lettering is pixel art, so it is scaled by whole numbers with nearest-neighbour
sampling — never resampled — and centred on a canvas painted in the artwork's own
background colour.
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
W, H, MARGIN = 1200, 630, 56

src = Image.open(ROOT / 'CURB WATCH.png').convert('RGBA')
bg = src.getpixel((4, 4))[:3]

flat = Image.new('RGB', src.size, bg)
flat.paste(src, (0, 0), src)
box = Image.eval(Image.new('RGB', src.size, bg), lambda v: v)
diff = Image.new('L', src.size)
diff.putdata([0 if px[:3] == bg else 255 for px in flat.convert('RGB').getdata()])
art = flat.crop(diff.getbbox())

scale = max(1, min((W - 2 * MARGIN) // art.width, (H - 2 * MARGIN) // art.height))
art = art.resize((art.width * scale, art.height * scale), Image.NEAREST)

canvas = Image.new('RGB', (W, H), bg)
canvas.paste(art, ((W - art.width) // 2, (H - art.height) // 2))
canvas.save(ROOT / 'og-image.png', optimize=True)
print(f'og-image.png {W}x{H} — artwork {art.width}x{art.height} at {scale}x on {bg}')
