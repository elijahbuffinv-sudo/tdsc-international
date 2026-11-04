# TDSC jurisdiction page research brief

You are researching jurisdiction pages for **Thiel Detective Service Company (TDSC)**, an international investigative consulting organization headquartered in Nashville, Tennessee, USA, a subsidiary and DBA of Delator Group. The TDSC name dates to 1873 (founded in St. Louis; the original business was dissolved; Delator Group reintroduced the name). The present organization has NOT operated continuously since 1873.

TDSC has NO offices, staff, phone numbers or addresses outside Nashville. In every country it works through scoped consulting engagements from Nashville and, where local work requires it, coordinates qualified and appropriately licensed local professionals. It never claims licensure abroad, access to restricted databases or government systems, or pretexting. It does not provide legal advice.

## Your job
For each assigned jurisdiction, research with WebSearch/WebFetch and write ONE JSON file to `/home/claude/intl/content/countries/<CC>.json` (CC = ISO alpha-2 given to you, uppercase). Validate each with `python3 -m json.tool <file> > /dev/null`.

Accuracy is the top priority. Every factual claim about laws, regulators, registries, licensing and statistics must come from a source you actually opened or saw in search results, and that source goes in `sources`. Prefer official sources (government, regulator, legislature, court), then DLA Piper Data Protection Laws of the World, ICLG, OECD, World Bank, UNCTAD, reputable law-firm guides. If you cannot verify something, say so plainly in the text ("we have not identified a dedicated licensing regime for private investigators; engagements are scoped with local counsel") and add a note to `review_flags`. Never invent law names, years, regulator names or numbers. Use present tense carefully and include years ("as of 2025").

Do NOT research these (they are compiled centrally): New York Convention / Hague Service / Hague Evidence / Apostille status, FATF lists, Transparency International CPI scores, US sanctions programs. Do not mention them unless essential.

## Voice
Direct, institutional, discreet, international. No hype, no "elite", no exclamation marks, no clichés. Specific to the country — a reader from that country should recognise the content as informed. Never write as if TDSC is located in or has history in the country. Never imply TDSC has operated there since 1873.

## Sanctioned / restricted jurisdictions
For jurisdictions subject to comprehensive or extensive US sanctions or embargoes (e.g., Cuba, Iran, North Korea, Syria, Russia, Belarus, Venezuela, and regions such as Crimea), write the page factually but make clear in `tdsc_approach` that TDSC, as a US company, screens every matter for sanctions compliance and does not accept engagements that would violate US or other applicable sanctions; many engagements involving the jurisdiction are therefore limited to lawful due diligence and risk advisory for clients outside it. Do not suggest workarounds. Research the current status before writing (sanctions change).

## JSON schema (all fields required; strings plain text, no HTML/markdown)
{
  "cc": "DE",
  "name": "Germany",
  "meta_description": "140-158 chars, specific to this country and investigative consulting",
  "eyebrow": "2-5 words, e.g. 'Federal Republic of Germany'",
  "hero_lede": "35-50 words: what investigative consulting for matters touching this country involves, specific to it",
  "intro": ["p1 90-130 words: the country's business/legal environment as it bears on investigations", "p2 90-130 words: why organisations commission investigative work involving this country (sectors, trade links, typical exposures)"],
  "population": {"value": "84.5 million", "year": "2024", "source_url": "https://..."},
  "legal_system": "60-100 words: type (civil/common/mixed/religious), codes or principles, court structure for commercial disputes, any specialised commercial courts or arbitration centres (name them).",
  "data_protection": {"law": "official short name and year, e.g. 'General Data Protection Regulation (EU) 2016/679 and Federal Data Protection Act (BDSG, 2017)'", "regulator": "name", "summary": "80-120 words: what this means for investigative work involving personal data — lawful basis, employee data, cross-border transfer rules, any localisation. If no comprehensive law, say so and describe sectoral rules."},
  "investigator_regulation": "70-110 words: whether private investigators / detective agencies are licensed or regulated, under what law and by which authority; restrictions (e.g., on surveillance, recording, access to records). If unclear, say so honestly.",
  "corporate_records": "70-110 words: name of the company registry, what is publicly available (officers, shareholders, filings), any beneficial ownership register and its public/restricted status, land/court record availability where well documented.",
  "anti_corruption": "50-90 words: principal anti-bribery/anti-corruption and AML laws (names, years) and main enforcement bodies.",
  "matters": [{"title": "3-7 words", "text": "35-55 words specific to this country's economy/risk"}],   // exactly 5
  "practical": [{"label": "short label", "value": "short value"}],   // 6-8 items, e.g. Business languages; Working week; Time zone(s) (IANA name and UTC offset); Business culture note; Document formalities; Courts language; Main business centres
  "tdsc_approach": "90-130 words: how TDSC scopes engagements touching this country — jurisdictional review, lawful sources, coordination with licensed local professionals and local counsel, data handling. Specific, not boilerplate.",
  "faqs": [{"q": "...", "a": "45-75 words"}],   // exactly 5, country-specific, no duplicates of other countries' wording
  "sources": [{"title": "...", "url": "https://..."}],   // 5-12 real URLs you used
  "review_flags": ["anything uncertain or likely to change; empty list if none"],
  "researched": "2026-11-04"
}

Target 1,100-1,500 words of copy per country. Write each file as soon as its research is done (do not hold several in memory). When finished, reply with only: the files written and any review_flags worth a human's attention.
