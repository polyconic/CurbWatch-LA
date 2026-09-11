# CurbWatch LA

Street parking, block by block, from Echo Park to West Hollywood. Search an address or click any block to see its street-sweeping days, whether it's a permit street and when that's enforced, Dodger game-day restrictions, meters, nearby lots, plate-reader cameras, and where tickets actually get written.

Static site: `index.html` plus a data snapshot in `curb-data.js`. No build step to view it.

```
python3 -m http.server 8000
```

then open http://localhost:8000.

## Refreshing the data

```
python3 -m venv .venv && .venv/bin/pip install -r tools/requirements.txt
.venv/bin/python tools/fetch.py    # downloads everything into data/raw/ (a few minutes)
.venv/bin/python tools/build.py    # writes curb-data.js
```

## Sources

- **LA City:** StreetsLA posted sweeping routes, street centerlines, LADOT meter inventory and live occupancy, LADOT city lots, and LA parking citations (last 6 months for ticket history, last 18 months for permit streets)
- **West Hollywood:** city GIS permit blocks with posted hours, permit districts, sweeping lines, and public lots
- **LA County:** address points, city boundaries
- **OpenStreetMap:** streets, parks, parking lots, and plate-reader (ALPR) cameras, which is the same data DeFlock shows. © OpenStreetMap contributors
- **Dodger Stadium home dates:** hand-maintained in `tools/dodgers-home.json`

Terms differ by layer — see [DATA-LICENSE.md](DATA-LICENSE.md). The OSM-derived parts of
`curb-data.js` are a derivative database under ODbL 1.0.

City data isn't the curb. Red curbs, hydrants, driveways and temporary signs aren't mapped, and the posted sign always wins.
