"""Turn index.html into a body-only page for publishing as a Claude artifact preview (writes data/artifact.html)."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = (ROOT / 'index.html').read_text()
title = re.search(r'<title>.*?</title>', src, re.S).group(0).replace(' · Street parking rules from Echo Park to West Hollywood', '')
fonts = '\n'.join(re.findall(r'<link rel="(?:preconnect|stylesheet)"[^>]*fonts\.g[^>]*>', src))
style = re.search(r'<style>.*?</style>', src, re.S).group(0)
body = re.search(r'<body>(.*)</body>', src, re.S).group(1).strip()
out = ROOT / 'data' / 'artifact.html'
out.parent.mkdir(exist_ok=True)
out.write_text(f'<meta charset="utf-8">\n{title}\n{fonts}\n{style}\n\n{body}\n')
print(out)
