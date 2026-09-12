# CurbWatch LA

Street-parking map for Echo Park → West Hollywood (plus Koreatown/Hollywood in the
bbox `-118.395,34.045,-118.230,34.115`). `README.md` is the public face; this file is
the working document.

Not deployed yet. Planned as a website (GitHub Pages like Greg's other sites), maybe an
app later — `site.webmanifest` already makes it installable. Greg is designing the
visual identity, and both images in the repo are his: `FAVICON2.png` (512×512) is the only
icon — favicon, apple-touch-icon and manifest all point at it — and `og-image.png`
(1200×630) is the social card. Replace either by overwriting the file; nothing generates
them. Keep og-image.png at 1200×630, the ratio link previews expect.

## Layout

- `index.html` — the whole app: one file, inline CSS + JS, deck.gl 9.1.14 from jsDelivr,
  Fraunces + Figtree from Google Fonts. The basemap is drawn from embedded data (no tiles).
- `curb-data.js` — `window.CURB = {...}`, ~5 MB, generated. Don't hand-edit.
- `tools/fetch.py` → `data/raw/*.json` (gitignored), `tools/build.py` → `curb-data.js`.
- `tools/make_artifact.py` → `data/artifact.html`, a body-only copy for publishing as a
  Claude artifact preview (the artifact host adds its own `<head>` and blocks
  third-party fetches, so live meter occupancy only works on the real site).

Coordinates in `curb-data.js` are ints in 1e-5° offsets from `(-118.40, 34.04)`, lines
delta-encoded. Block rows are positional arrays — see the `bout.append` in `build.py`
and the `blocks` decode in `index.html` before changing either.

## Before launch

- Replace `https://curbwatch.example/` with the real domain in `index.html` (canonical,
  `og:url`, `og:image`, `twitter:image`, JSON-LD), `robots.txt` and `sitemap.xml`.
  Add `CNAME` for Pages. See `quietbroadcast/CLAUDE.md` for the HTTPS/DNS ordering gotcha.
- Page title/description live in `index.html` `<head>`; keep `og:`/`twitter:` copies in sync.

## Data decisions (hard-won — read before changing)

- **No LA permit-district polygons.** LADOT's only published PPD map is from Aug 2015 and
  is wrong on the ground (W Lanewood Ave sits inside a 2015 district, has no permit
  signs). Every public source was checked; nothing newer exists.
- **LA permit streets come from tickets**, matched by the *address the officer wrote*,
  not GPS: a block counts if ≥3 `PREFERENTIAL PARKING` / `OVNIGHT PRK W/OUT PE` tickets
  on ≥2 days in 18 months have a location on that street within its number range.
  GPS-only snapping pulled cross-street tickets onto the wrong block (that was the
  Lanewood bug). All ticket stats use the same address matcher (`match_blocks`).
- A permit verdict for the user's window needs ≥3 tickets in those hours **and** ≥5% of
  the block's permit tickets (Sycamore 1700 had 36 of 1,164 at 8–10 PM — noise).
- **District D** (Dodger Stadium special-event permit zone: no parking 4 hrs before and
  during events, District D permits exempt) is in no dataset. `ZONE_D` in `build.py` is
  Greg's street list: Douglas north of Sunset, Quintero, Sutherland, Macbeth,
  Elysian Park Dr, Montana, Scott east of Portia. Extra blocks are inferred where ≥85%
  of address-matched no-parking tickets fall on home-game days, and are labelled as
  inferred. Concerts and other stadium events trigger it too but aren't in any feed.
- WeHo data is the city's own and has posted hours — trust it over inference.
- LA sweeping routes are polygons with paired routes (e.g. `5P223 Th` / `5P223 F`):
  one side each day, and the data doesn't say which side.
- LA's occupancy feed timestamps are UTC; display converts to LA time.
- Parkopedia was tried and rejected (403, client-rendered, proprietary).
- Dodger dates live in `tools/dodgers-home.json`, hand-maintained on purpose: MLB's Stats
  API limits use to individual, non-commercial, non-bulk. Add next season by hand.
- `curb-data.js` mixes ODbL (OSM) and city-open-data fields and carries a notice saying
  which is which — see `DATA-LICENSE.md`. Keep the OSM attribution in the page footer.

## Sweeping-ticket anomalies (checked 2026-09-11, don't republish the first number)

A first pass said 2,473 street-cleaning tickets (~$168k/6mo) didn't match the posted
schedule. Verifying per block killed most of it:

- 19% of tickets sit on blocks where our route assignment itself looks wrong — excluded.
- Of tickets on well-modelled blocks (≥90% matching), the residue is 1,377, and most of
  that is method noise: 591 where no route polygon covers the point, 650 wrong-day and 93
  wrong-week cases that two-sided routes and polygon edges can explain.
- What survives: **43 tickets (~$2.7k) written on the correct posted day but outside the
  posted hours**, spread over 32 blocks.
- Holiday claim was wrong: the 14 "holiday" hits were 2026-04-03, Good Friday, which is
  not an LA city holiday. Zero confirmed holiday tickets.

So the "they ticket when no sweeper came" story is NOT provable from open data — LA
publishes no sweeper GPS or completion records. Per-ticket schedule mismatch is real but
rare. Any public number must come from the verified column, not the first pass.
