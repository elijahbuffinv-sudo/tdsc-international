# TDSC International

Static site for **intl.thieldetectiveagency.com** — jurisdiction profiles and major business-hub pages for Thiel Detective Service Company (TDSC), a subsidiary and DBA of Delator Group. The main site lives on Squarespace at www.thieldetectiveagency.com.

## Layout
- `content/countries/<CC>.json` — researched jurisdiction profiles (schema in `content/COUNTRY_BRIEF.md`)
- `content/cities/<slug>.json` — hub city pages (in progress)
- `content/global/global.json` — centrally compiled treaty, CPI, FATF and OFAC data
- `data/` — reference data (jurisdictions, 300 GaWC hubs, city search index, outlines, capitals)
- `gen/` — generator (`build.py`, `maps.py`, `brand/` design system)
- `site/` — generated output, deployed by Cloudflare Pages

## Build
```
python3 -I gen/build.py          # writes ./site
```
Pages with fewer than 5 sources are held back automatically. No dependencies beyond Python 3.9+.

## Cloudflare Pages
Build command: `python3 gen/build.py` · Output directory: `site` (or no build command, output `site`, since the built output is committed).

## Attribution
City data © GeoNames (CC BY 4.0). Country data: mledoze/countries (ODbL). Country outlines: Natural Earth (public domain). World city tiers: GaWC 2024.
