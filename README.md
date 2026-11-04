# TDSC International

Source for the **/international** section of www.thieldetectiveagency.com (Squarespace) — jurisdiction profiles and major business-hub pages for Thiel Detective Service Company (TDSC), a subsidiary and DBA of Delator Group. The main site lives on Squarespace at www.thieldetectiveagency.com.

## Layout
- `content/countries/<CC>.json` — researched jurisdiction profiles (schema in `content/COUNTRY_BRIEF.md`)
- `content/cities/<slug>.json` — hub city pages (in progress)
- `content/global/global.json` — centrally compiled treaty, CPI, FATF and OFAC data
- `data/` — reference data (jurisdictions, 300 GaWC hubs, city search index, outlines, capitals)
- `gen/` — generator (`build.py`, `maps.py`, `brand/` design system)
- `sq/` — generated output: `pages/*.html` code-block fragments, `manifest.json` (path, SEO title, description), `assets/intl.css` (header injection), `assets/search.js` (footer injection), `assets/search-index.json` (served via jsDelivr)

## Build
```
python3 -I gen/build.py          # writes ./sq
```
Pages with fewer than 5 sources are held back automatically. No dependencies beyond Python 3.9+.

## Publishing
Pages are created in Squarespace by duplicating the template page and writing the fragment into its code block through the site editor's page API; SEO title, description and URL come from `sq/manifest.json`.

## Attribution
City data © GeoNames (CC BY 4.0). Country data: mledoze/countries (ODbL). Country outlines: Natural Earth (public domain). World city tiers: GaWC 2024.
