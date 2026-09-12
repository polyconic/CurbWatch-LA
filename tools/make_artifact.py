"""Turn index.html into a body-only page for publishing as a Claude artifact preview (writes data/artifact.html)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / 'index.html').read_text()
title = re.search(r'<title>.*?</title>', src, re.S).group(0).replace(' · Street parking rules from Echo Park to West Hollywood', '')
fonts = ('<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT@9..144,500..700,100&family=Figtree:wght@400..800&display=swap">')
style = re.search(r'<style>.*?</style>', src, re.S).group(0)
body = re.search(r'<body>(.*)</body>', src, re.S).group(1).strip()
body = body.replace('<script src="vendor/deck.gl-9.1.14.min.js"></script>', '<script src="https://cdn.jsdelivr.net/npm/deck.gl@9.1.14/dist.min.js"></script>')
out = ROOT / 'data' / 'artifact.html'
out.parent.mkdir(exist_ok=True)
out.write_text(f'<meta charset="utf-8">\n{title}\n{fonts}\n{style}\n\n{body}\n')
print(out)
