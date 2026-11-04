# TDSC hub city page research brief

Read `/home/claude/intl/content/COUNTRY_BRIEF.md` first: the company facts, accuracy rules, voice and sanctions rules there apply here too. The country page for the city's jurisdiction (`/home/claude/intl/content/countries/<CC>.json`) already covers national law; read it if it exists and do NOT repeat its national-law material. City pages must add what is specific to the city.

TDSC has no office in any of these cities. Never imply local presence, history in the city, or operation since 1873.

## Your job
For each assigned city write `/home/claude/intl/content/cities/<slug>.json` (slug given to you) and validate with `python3 -m json.tool`.

## What makes a city page useful (and unique)
- The city's economic role: main industries, major employers or sectors, financial centre status, ports, free zones, stock exchange, international organisations.
- Local institutions relevant to investigations: the courts that sit in the city (commercial courts, high courts, specialised tribunals), arbitration centres located there, the local company/commercial registry office or chamber of commerce, land/property registry arrangements if city-specific, the financial regulator if headquartered there, state/provincial laws if the city sits in a state with its own regime (e.g. US states, Australian states, Canadian provinces, Indian states, German Länder, Swiss cantons, Emirates).
- The typical investigative exposures connected to the city (e.g. trade finance fraud in a port city, real estate and ownership opacity in a wealth hub, procurement risk in a capital).

## JSON schema (all fields required unless noted; plain text)
{
  "slug": "london-gb",
  "name": "London",
  "cc": "GB",
  "meta_description": "140-158 chars, starts 'TDSC investigative consulting in matters touching <City>:'",
  "eyebrow": "2-5 words, e.g. 'Greater London, United Kingdom'",
  "hero_lede": "35-50 words",
  "intro": ["p1 90-130 words: the city as a business centre", "p2 90-130 words: why organisations commission investigative work connected to it"],
  "economy": [{"label": "short", "value": "short"}],          // 6-8 items: population (with year), metro area, key sectors, exchange/regulator, port/airport hub, time zone (IANA + offset), languages of business
  "matters": [{"title": "3-7 words", "text": "35-55 words"}],  // exactly 5, specific to the city
  "local_context": [{"title": "3-6 words", "text": "60-100 words"}],  // 4-5: courts in the city, arbitration centre, registries/chambers, state/provincial rules, notable regulatory bodies
  "tdsc_approach": "80-120 words, specific to the city",
  "faqs": [{"q": "...", "a": "45-75 words"}],  // exactly 5, city-specific
  "sources": [{"title": "...", "url": "https://..."}],  // 5-10 real URLs you opened
  "review_flags": [],
  "researched": "YYYY-MM-DD"
}

Target 1,000-1,300 words. Write each file as soon as it is done. Reply only with files written and review_flags worth a human's attention.
