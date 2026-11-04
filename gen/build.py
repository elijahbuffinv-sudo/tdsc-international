#!/usr/bin/env python3
"""TDSC International — static site generator.
Renders jurisdiction pages (content/countries/*.json) and hub city pages (content/cities/*.json)
into ../site for intl.thieldetectiveagency.com. Design system: brand/base.css + brand/intl.css.
Run:  python3 -I gen/build.py  (from repo root, or any cwd)"""
import os, sys, json, re, html, hashlib, math, datetime, unicodedata, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'brand')); sys.path.insert(0, HERE)
from components import monogram_svg, seal_svg, icon, ARROW, ld, SITE, PHONE_DISPLAY, PHONE_TEL, EMAIL, DELATOR, ORG_ID
import maps
from zoneinfo import ZoneInfo

ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, 'data'); CONTENT = os.path.join(ROOT, 'content')
OUT = os.environ.get('TDSC_OUT', os.path.join(ROOT, 'sq'))
INTL = SITE  # pages live on the main Squarespace site under /international
M = ''  # prefix for main-site links (relative on Squarespace)
IDX_URL = os.environ.get('TDSC_IDX_URL', 'https://cdn.jsdelivr.net/gh/elijahbuffinv-sudo/tdsc-international@main/sq/assets/search-index.json')
def jur_url(slug): return f'/international/{slug}'
def slugify(x):
    x = unicodedata.normalize('NFKD', x).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', x).strip('-')

BUILD_DATE = os.environ.get('TDSC_DATE', datetime.date.today().isoformat())
MIN_SOURCES = 5
e = lambda s: html.escape(str(s), quote=True)

# ---------------------------------------------------------------- data
JUR = {j['cc']: j for j in json.load(open(os.path.join(DATA, 'jurisdictions.json')))}
CCA3 = {j['cca3']: j['cc'] for j in JUR.values()}
G = json.load(open(os.path.join(CONTENT, 'global', 'global.json')))
HUBS = json.load(open(os.path.join(DATA, 'hubs300.json')))
SIDX = json.load(open(os.path.join(DATA, 'search-index.json')))
HUB_BY_SLUG = None
OUTLINES = maps.load_outlines(os.path.join(DATA, 'countries.geojson'))
TERR = {'GF': 'FR', 'GP': 'FR', 'MQ': 'FR', 'RE': 'FR', 'YT': 'FR', 'NC': 'FR', 'PF': 'FR', 'VI': 'US', 'GU': 'US', 'CW': 'NL', 'AW': 'NL', 'SX': 'NL', 'GI': 'GB', 'JE': 'GB', 'GG': 'GB', 'IM': 'GB', 'BM': 'GB', 'VG': 'GB'}
COMPREHENSIVE = {'CU', 'IR', 'KP', 'SY'}
EXTENSIVE = {'RU', 'BY', 'VE'}
NASHVILLE = ZoneInfo('America/Chicago')

def load_capitals():
    """Capital coordinates and time zones (GeoNames PPLC, extracted to data/capitals.json)."""
    return {k: tuple(v) for k, v in json.load(open(os.path.join(DATA, 'capitals.json'))).items()}
CAPS = load_capitals()

def load_countries():
    out = {}
    d = os.path.join(CONTENT, 'countries')
    for f in sorted(os.listdir(d)):
        if f.endswith('.json'):
            x = json.load(open(os.path.join(d, f)))
            out[x['cc']] = x
    return out

def publishable(x):
    return len(x.get('sources', [])) >= MIN_SOURCES and len(x.get('faqs', [])) == 5 and len(x.get('matters', [])) == 5

# ---------------------------------------------------------------- variation
def seed(key, n, salt=''):
    return int(hashlib.sha256((salt + key).encode()).hexdigest(), 16) % n
ACCENTS = ['brass', 'silver', 'champagne', 'walnut', 'steel']

def title_for(name, kind='jur'):
    opts = [f'{name} Investigative Consulting | TDSC · Since 1873',
            f'{name} Investigations | TDSC · Since 1873',
            f'{name} Investigations | TDSC 1873',
            f'{name} | TDSC Investigations Since 1873']
    for t in opts:
        if len(t) <= 60: return t
    return f'{name[:40]} | TDSC 1873'

# ---------------------------------------------------------------- chrome
SEARCH_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6.5"/><path d="m16 16 4.5 4.5"/></svg>'
def search_box(sid, big=False):
    return (f'<div class="v-search" role="search" data-search><label class="v-search-label" for="{sid}">Search by city internationally</label>{SEARCH_ICON}'
            f'<input id="{sid}" type="search" autocomplete="off" spellcheck="false" placeholder="Search by city internationally" '
            f'role="combobox" aria-expanded="false" aria-controls="{sid}-r" aria-autocomplete="list">'
            f'<ul class="v-results" id="{sid}-r" role="listbox" hidden></ul></div>')

def header():
    return f'''<header class="tdsc-hdr tdsc-chrome" id="tdsc-hdr"><div class="tdsc-hdr__in">
<a class="tdsc-brand" href="{M}/" aria-label="Thiel Detective Service Company — home">{monogram_svg('', 'TDSC')}<span class="tdsc-brand__t"><span class="tdsc-brand__n">THIEL DETECTIVE SERVICE CO.</span><span class="tdsc-brand__s">INVESTIGATIONS SINCE 1873</span></span></a>
<nav class="tdsc-nav" aria-label="Primary">
<a href="{M}/about" class="tdsc-nav__hide-md">About TDSC</a>
<a href="{M}/consulting">Consulting</a>
<a href="/">International</a>
<a href="{M}/contact">Contact</a>
</nav>
<div class="v-hdr-search">{search_box('tdsc-q')}</div>
<a class="tdsc-btn tdsc-btn--brass" href="{M}/contact">Discuss an Engagement</a>
<button class="tdsc-burger" type="button" aria-label="Open menu" aria-expanded="false" aria-controls="tdsc-mob"><span></span></button>
</div>
<nav class="tdsc-mob" id="tdsc-mob" aria-label="Mobile">
{search_box('tdsc-qm')}
<a href="{M}/">Home</a><a href="{M}/about">About TDSC</a><a href="{M}/consulting">Consulting Disciplines</a>
<a href="/international">International Directory</a><a href="{M}/contact">Contact</a>
<a class="tdsc-btn tdsc-btn--brass" href="{M}/contact">Discuss an Engagement</a>
</nav></header>'''

DISCLOSURE = ('Thiel Detective Service Company (TDSC) traces its historical origins to 1873. The original business was subsequently dissolved, '
              'and the present-day TDSC brand was later adopted and reintroduced by Delator Group. The current organization has not operated '
              'continuously since 1873, and references to 1873 describe the origin of the name, not the age of the present company. '
              'TDSC is a subsidiary and DBA of Delator Group and operates as part of the Delator Group corporate organization.')

def footer():
    return f'''<footer class="tdsc-ftr tdsc-chrome" id="tdsc-ftr"><div class="tdsc-wrap">
<div class="tdsc-ftr__top">
<div class="tdsc-ftr__brand">{seal_svg('tdsc-ftr__seal', label='Thiel Detective Service Company seal')}<p>Thiel Detective Service Company</p><span class="tdsc-brand__s">INVESTIGATIONS SINCE 1873 · A NEW ERA OF INTELLIGENCE</span></div>
<div><h2>International</h2><ul><li><a href="/international">Jurisdiction Directory</a></li><li><a href="/international#hubs">Major Business Hubs</a></li><li><a href="{M}/consulting/international-investigative-strategy-consulting">International Strategy</a></li><li><a href="{M}/consulting/due-diligence-consulting">Cross-Border Due Diligence</a></li></ul></div>
<div><h2>Consulting</h2><ul><li><a href="{M}/consulting">All Disciplines</a></li><li><a href="{M}/consulting/corporate-investigative-consulting">Corporate Investigations</a></li><li><a href="{M}/consulting/fraud-investigation-consulting">Fraud Investigation</a></li><li><a href="{M}/consulting/asset-intelligence-recovery-consulting">Asset Intelligence</a></li><li><a href="{M}/consulting/corporate-compliance-consulting">Corporate Compliance</a></li></ul></div>
<div><h2>Headquarters</h2><address>Nashville, Tennessee, USA<br><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></address>
<h2 style="margin-top:26px">Company</h2><ul><li><a href="{M}/about">About TDSC</a></li><li><a href="{DELATOR}" rel="noopener">Delator Group</a></li></ul></div>
</div>
<section class="tdsc-disc" aria-labelledby="tdsc-disc-h">{icon('document','')}<div><h2 id="tdsc-disc-h">Historical and Corporate Disclosure</h2><p>{e(DISCLOSURE)} <a href="{M}/about">Read the TDSC history</a> · <a href="{DELATOR}" rel="noopener">Visit Delator Group</a></p>
<p style="margin-top:12px">TDSC operates from Nashville, Tennessee and maintains no offices outside the United States. International engagements are scoped from headquarters and, where local work requires it, coordinated with appropriately licensed local professionals. Jurisdiction pages are general information, not legal advice. City data: <a href="https://www.geonames.org/" rel="noopener">GeoNames</a> (CC BY 4.0). Country outlines: Natural Earth (public domain).</p></div></section>
<div class="tdsc-ftr__base"><span>© <span data-tdsc-year>2026</span> Thiel Detective Service Company, a DBA of Delator Group. All rights reserved.</span>
<nav aria-label="Legal"><a href="{M}/privacy-policy">Privacy Policy</a><a href="{M}/terms-of-use">Terms of Use</a><a href="{M}/contact">Contact</a></nav></div>
</div></footer>'''

def cta(title, text):
    return f'''<section class="tdsc-cta tdsc-center" aria-labelledby="tdsc-cta-h"><div class="tdsc-wrap tdsc-narrow tdsc-rv">
{seal_svg('tdsc-cta__seal', label='TDSC seal')}
<p class="tdsc-eyebrow">Thiel Detective Service Company</p>
<h2 id="tdsc-cta-h">{e(title)}</h2><p class="tdsc-lede">{e(text)}</p>
<div class="tdsc-btns"><a class="tdsc-btn tdsc-btn--brass" href="{M}/contact">Request a Consultation {ARROW}</a><a class="tdsc-btn tdsc-btn--ghost" href="{M}/consulting">Explore Our Capabilities</a></div>
<div class="tdsc-cta__contact"><span>Headquarters: Nashville, Tennessee</span><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
</div></section>'''

def crumbs(items):
    lis = []
    for i, (n, u) in enumerate(items):
        lis.append(f'<li><span aria-current="page">{e(n)}</span></li>' if i == len(items) - 1 else f'<li><a href="{u}">{e(n)}</a></li>')
    return f'<nav class="tdsc-crumbs" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'

def crumbs_ld(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': (u if u.startswith('http') else INTL + u)} for i, (n, u) in enumerate(items)]}

PAGES = []  # manifest rows for the Squarespace loader
def doc(path, title, desc, body, schema, accent='brass', og_type='website', nav=None):
    key = 'intl' + (path.replace('/international', '').replace('/', '-') or '-index')
    frag = (f'<!-- TDSC PAGE: {key} | generated by TDSC international build — edit source, not this block -->\n'
            f'<div class="tdsc-page tdsc-intl" data-tdsc-page="{key}" data-accent="{accent}">\n{body}\n</div>\n{ld(schema)}\n')
    PAGES.append({'key': key, 'path': path, 'title': title, 'desc': desc, 'nav': nav or title, 'bytes': len(frag.encode())})
    return frag

# ---------------------------------------------------------------- pieces
def fmt_pop(n):
    return f'{n/1e6:.1f} million' if n >= 1e6 else f'{n:,}'

def offset_vs_nashville(tz):
    if not tz: return None
    now = datetime.datetime(int(BUILD_DATE[:4]), int(BUILD_DATE[5:7]), int(BUILD_DATE[8:10]), 15, tzinfo=datetime.timezone.utc)
    d = (now.astimezone(ZoneInfo(tz)).utcoffset() - now.astimezone(NASHVILLE).utcoffset()).total_seconds() / 3600
    if d == 0: return 'Same as Nashville'
    h = f'{abs(d):g}'
    return f'{h} h {"ahead of" if d > 0 else "behind"} Nashville'

def map_plate(cc, jur, markers, parch=False, cap_line=''):
    W, H = 560, 420
    rings = OUTLINES.get(cc)
    if not rings:
        # fallback: locator square around the country centroid
        lat, lng = jur['latlng']
        d = 1.2
        rings = [[(lng - d, lat - d), (lng + d, lat - d), (lng + d, lat + d), (lng - d, lat + d), (lng - d, lat - d)]]
        outline_known = False
    else:
        outline_known = True
    path, P, bbox = maps.plate(rings, W, H)
    grat, step = maps.graticule(P, bbox, W, H)
    ink = '#9C7A45' if parch else '#C2A06A'
    fill = 'rgba(156,122,69,.14)' if parch else 'rgba(194,160,106,.12)'
    gcol = 'rgba(122,82,52,.18)' if parch else 'rgba(246,241,230,.08)'
    lab = '#3a2a1a' if parch else '#F3ECDD'
    marks = []
    for i, (name, lat, lng, kind) in enumerate(markers):
        x, y = P(lng, lat)
        if not (-10 < x < W + 10 and -10 < y < H + 10): continue
        if kind == 'capital':
            from components import star
            marks.append(f'<path d="{star(x, y, 9, 3.2)}" fill="{ink}" stroke="{lab}" stroke-width=".6"/>')
        else:
            marks.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="none" stroke="{ink}" stroke-width="1.6"/><circle cx="{x:.1f}" cy="{y:.1f}" r="1.4" fill="{ink}"/>')
        anchor = 'end' if x > W * 0.7 else 'start'
        dx = -12 if anchor == 'end' else 12
        marks.append(f'<text x="{x+dx:.1f}" y="{y+4:.1f}" text-anchor="{anchor}" font-family="Inter,sans-serif" font-size="12" font-weight="600" fill="{lab}" paint-order="stroke" stroke="{"#F2EBDD" if parch else "#0B1422"}" stroke-width="3">{e(name)}</text>')
    shape = (f'<path d="{path}" fill="{fill}" stroke="{ink}" stroke-width="1.3" stroke-linejoin="round" vector-effect="non-scaling-stroke"/>' if outline_known
             else f'<path d="{path}" fill="none" stroke="{ink}" stroke-width="1" stroke-dasharray="4 4"/>')
    lat, lng = jur['latlng']
    coord = f'{abs(lat):.0f}°{"N" if lat >= 0 else "S"} · {abs(lng):.0f}°{"E" if lng >= 0 else "W"}'
    svg = (f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Outline map of {e(jur["name"])} marking {e(", ".join(m[0] for m in markers)) or "its location"}">'
           f'<defs><clipPath id="clip-{cc}"><rect width="{W}" height="{H}"/></clipPath></defs><g clip-path="url(#clip-{cc})">'
           f'<path d="{grat}" stroke="{gcol}" stroke-width="1" fill="none"/>{shape}{"".join(marks)}</g>'
           f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" fill="none" stroke="{gcol}"/></svg>')
    return (f'<figure class="v-plate{" v-plate--parch" if parch else ""}">{svg}'
            f'<figcaption class="v-plate__cap"><span>Plate · {e(jur["cca3"])}</span><span>{coord}</span><span>Graticule {step}°</span></figcaption></figure>')

def yn(v):
    if v is None: return '<span>Not recorded</span>'
    return '<span class="v-yes">Party</span>' if v else '<span class="v-no">Not a party</span>'

def ledger(cc, jur, d, cap, dark=False):
    gc = G['countries'].get(cc, {})
    pop = d.get('population') or {}
    rows = [('Population', f'{pop.get("value","—")} ({pop.get("year","")})' if pop else '—'),
            ('Capital', jur.get('capital') or '—'),
            ('Region', jur.get('subregion') or jur.get('region') or '—'),
            ('Official languages', ', '.join(jur.get('languages', [])[:4]) or '—'),
            ('Currency', ', '.join(jur.get('currencies', [])[:2]) or '—'),
            ('Dialling code · Domain', f'{jur.get("idd","")} · {jur.get("tld","")}'),
            ('Capital time vs HQ', offset_vs_nashville(cap[3]) if cap else '—'),
            ('Corruption Perceptions Index', f'{gc["cpi_score"]}/100 · rank {gc["cpi_rank"]}' if gc.get('cpi_score') is not None else 'Not ranked'),
            ('New York Convention', yn(gc.get('ny_convention'))),
            ('Hague Service Convention', yn(gc.get('hague_service'))),
            ('Hague Evidence Convention', yn(gc.get('hague_evidence'))),
            ('Apostille Convention', yn(gc.get('apostille')))]
    fatf = G['fatf']
    fs = 'Call for action (black list)' if cc in fatf['black'] else 'Increased monitoring (grey list)' if cc in fatf['grey'] else 'Not listed'
    rows.append(('FATF status', f'{fs} · {fatf["as_of"]}'))
    ofac = G['ofac_programs'].get(cc)
    rows.append(('US sanctions (OFAC)', 'Comprehensive program' if cc in COMPREHENSIVE else ('Program in force' if ofac else 'No country program')))
    rows += [('Landlocked', 'Yes' if jur.get('landlocked') else 'No'), ('Area', f'{jur["area"]:,.0f} km²' if jur.get('area') else '—')]
    items = ''.join(f'<div><dt>{e(k)}</dt><dd>{v if k in ("New York Convention","Hague Service Convention","Hague Evidence Convention","Apostille Convention") else e(v)}</dd></div>' for k, v in rows)
    return f'<dl class="v-ledger{" v-ledger--dark" if dark else ""}">{items}</dl>'

def faq_html(faqs):
    return ''.join(f'<details><summary><h3>{e(f["q"])}</h3></summary><div class="tdsc-faq__a"><p>{e(f["a"])}</p></div></details>' for f in faqs)

def sources_html(srcs):
    return '<ol class="v-sources">' + ''.join(f'<li><a href="{e(s["url"])}" rel="noopener nofollow" target="_blank">{e(s["title"])}</a></li>' for s in srcs) + '</ol>'

def sanction_notice(cc, name):
    if cc in COMPREHENSIVE:
        t = f'{name} is subject to comprehensive United States sanctions. As a US company, TDSC screens every matter for sanctions compliance and does not accept engagements that would violate US or other applicable sanctions. Work touching {name} is generally limited to lawful due diligence and risk advisory for clients outside the jurisdiction, and only where permitted.'
    elif cc in EXTENSIVE or cc in G['fatf']['black']:
        t = f'Matters touching {name} carry elevated sanctions and financial-crime risk. TDSC screens every engagement against US and other applicable sanctions and export controls, and declines work that would breach them. Scope is confirmed in writing before any activity.'
    else:
        return ''
    return f'<section class="tdsc-sec tdsc-sec--paper tdsc-sec--tight"><div class="tdsc-wrap"><div class="v-alert" role="note"><b>SANCTIONS SCREENING</b>{e(t)}</div></div></section>'

# ---------------------------------------------------------------- jurisdiction page
H1_FORMS = ['Investigative Consulting Involving {n}', '{n}: Investigative Consulting', 'Investigations Touching {n}']
LEGAL_HEADS = [('Legal Environment', 'How the law shapes investigative work involving {n}'),
               ('Jurisdictional Framework', 'The rules that govern lawful inquiry in {n}'),
               ('Law & Regulation', 'What applies before any work touching {n} begins')]

def hubs_for(cc):
    return [h for h in HUBS if h['cc'] == cc]

def top_cities(cc, n=14):
    rows = [c for c in SIDX['cities'] if c[2] == cc]
    rows.sort(key=lambda c: -c[3])
    return rows[:n]

def hub_slug(h):
    s = unicodedata.normalize('NFKD', h['name']).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-') + '-' + h['cc'].lower()

def city_url(h):
    cc = h['cc']; j = JUR.get(cc) or JUR.get(TERR.get(cc, ''))
    return f"/international/{j['slug'] if j else cc.lower()}/{slugify(h['name'])}"
def city_url_by_slug(hs):
    return city_url(HUB_BY_SLUG[hs])

def render_jurisdiction(cc, d, published, hub_pages):
    jur = JUR[cc]; name = jur['name']; slug = jur['slug']
    path = jur_url(slug)
    accent = ACCENTS[seed(cc, 5, 'acc')]
    hero_v = ['', ' v-hero--right', ' v-hero--split'][seed(cc, 3, 'hero')]
    topic_v = ['cards', 'ledger', 'tabs'][seed(cc, 3, 'topic')]
    parch = seed(cc, 2, 'plate') == 1
    dark_ledger = seed(cc, 2, 'ledg') == 1
    h1 = H1_FORMS[seed(cc, 3, 'h1')].format(n=name)
    lh = LEGAL_HEADS[seed(cc, 3, 'lh')]
    cap = CAPS.get(cc)
    markers = []
    if cap: markers.append((jur.get('capital') or cap[0], cap[1], cap[2], 'capital'))
    hubs = hubs_for(cc)
    for h in hubs[:5]:
        if not cap or abs(h['lat'] - cap[1]) + abs(h['lng'] - cap[2]) > 0.3:
            markers.append((h['name'], h['lat'], h['lng'], 'hub'))
    plate = map_plate(cc, jur, markers, parch=parch)
    title = title_for(name)
    desc = d['meta_description']
    cr = [('TDSC', '/'), ('International', '/international'), (name, path)]

    # --- hero
    meta = [('Capital', jur.get('capital') or '—'), ('Region', jur.get('subregion') or jur.get('region')), ('HQ', 'Nashville, Tennessee')]
    hero = f'''<section class="tdsc-hero v-hero{hero_v}" aria-labelledby="tdsc-h1"><div class="tdsc-glassgrid"></div><div class="tdsc-wrap"><div class="tdsc-hero__in">
<div>{crumbs(cr)}<p class="tdsc-eyebrow">{e(d["eyebrow"])}</p><h1 id="tdsc-h1">{e(h1)}</h1><p class="tdsc-lede">{e(d["hero_lede"])}</p>
<div class="tdsc-btns"><a class="tdsc-btn tdsc-btn--brass" href="{M}/contact">Discuss a Matter {ARROW}</a><a class="tdsc-btn tdsc-btn--ghost" href="#framework">Review the Framework</a></div>
<div class="tdsc-hero-meta">{''.join(f'<span><b>{e(k)}</b> {e(v)}</span>' for k, v in meta)}</div></div>
<div class="tdsc-hero__art">{plate}</div>
</div></div></section>'''

    # --- overview
    overview = f'''<section class="tdsc-sec tdsc-sec--ivory" aria-labelledby="ov-h"><div class="tdsc-wrap">
<div class="tdsc-head tdsc-rv"><p class="tdsc-eyebrow">Overview</p><h2 id="ov-h">{e(name)} at a Glance</h2></div>
<div class="tdsc-prose tdsc-rv" style="max-width:860px">{''.join(f'<p>{e(p)}</p>' for p in d["intro"])}</div>
<div class="tdsc-rv" style="margin-top:40px">{ledger(cc, jur, d, cap, dark=False)}</div>
<p class="tdsc-updated" style="margin-top:14px">Population: <a href="{e(d["population"].get("source_url",""))}" rel="noopener nofollow">source</a>. Treaty status, CPI ({e(G["sources"].get("cpi_year","2025"))}), FATF and OFAC entries compiled {e(G["as_of"])}; confirm current status before relying on them.</p>
</div></section>'''

    # --- matters
    mi = ['search', 'shield', 'network', 'document', 'globe', 'scale', 'eye', 'lock']
    mcards = ''.join(f'<article class="tdsc-card tdsc-card--light tdsc-rv"><span class="tdsc-card__n">{i+1:02d}</span><h3>{e(m["title"])}</h3><p>{e(m["text"])}</p></article>' for i, m in enumerate(d['matters']))
    matters = f'''<section class="tdsc-sec {"tdsc-sec--paper" if not dark_ledger else "tdsc-sec--parchment"}" aria-labelledby="mt-h"><div class="tdsc-wrap">
<div class="tdsc-head tdsc-rv"><p class="tdsc-eyebrow">Typical Matters</p><h2 id="mt-h">Where Investigative Work Involving {e(name)} Concentrates</h2></div>
<div class="tdsc-grid-3">{mcards}</div></div></section>'''

    # --- legal framework
    dp = d['data_protection']
    topics = [('Legal system', None, d['legal_system']),
              ('Data protection', f'{dp["law"]} · Regulator: {dp["regulator"]}', dp['summary']),
              ('Private investigators', None, d['investigator_regulation']),
              ('Corporate & public records', None, d['corporate_records']),
              ('Anti-corruption & AML', None, d['anti_corruption'])]
    tb = ''.join(f'<div class="v-topic tdsc-rv" data-n="{["I","II","III","IV","V"][i]}"><h3>{e(t)}</h3><div>{f"<span class=v-law>{e(law)}</span>" if law else ""}<p>{e(x)}</p></div></div>' for i, (t, law, x) in enumerate(topics))
    legal = f'''<section class="tdsc-sec tdsc-sec--ivory" id="framework" aria-labelledby="lg-h"><div class="tdsc-wrap">
<div class="tdsc-head tdsc-rv"><p class="tdsc-eyebrow">{e(lh[0])}</p><h2 id="lg-h">{e(lh[1].format(n=name))}</h2></div>
<div class="v-topics v-topics--{topic_v}">{tb}</div>
<p class="tdsc-updated" style="margin-top:22px">General information compiled {e(d.get("researched",""))} from the sources listed below. It is not legal advice; TDSC works with qualified local counsel on questions of law.</p></div></section>'''

    # --- practical
    pr = ''.join(f'<div><dt>{e(p["label"])}</dt><dd>{e(p["value"])}</dd></div>' for p in d['practical'])
    practical = f'''<section class="tdsc-sec tdsc-sec--midnight" aria-labelledby="pr-h"><div class="tdsc-wrap">
<div class="tdsc-head tdsc-rv"><p class="tdsc-eyebrow">Working Notes</p><h2 id="pr-h">Practical Considerations for {e(name)}</h2></div>
<dl class="v-ledger v-ledger--dark tdsc-rv">{pr}</dl></div></section>'''

    # --- approach
    approach = f'''<section class="tdsc-sec tdsc-sec--parchment" aria-labelledby="ap-h"><div class="tdsc-wrap"><div class="tdsc-notice tdsc-rv">
<span class="tdsc-notice__label">Engagement Standard</span><h2 id="ap-h">How TDSC Scopes Matters Touching {e(name)}</h2><p>{e(d["tdsc_approach"])}</p>
<p>TDSC has no office in {e(name)}. Engagements are directed from Nashville, Tennessee; where work on the ground is needed, it is performed by appropriately licensed local professionals under a written scope. TDSC does not provide legal advice.</p>
<div class="tdsc-btns" style="margin-top:22px"><a class="tdsc-btn tdsc-btn--navy" href="{M}/consulting/international-investigative-strategy-consulting">International Investigative Strategy {ARROW}</a><a class="tdsc-btn tdsc-btn--line" href="{M}/consulting/due-diligence-consulting">Cross-Border Due Diligence</a></div>
</div></div></section>'''

    # --- cities
    tc = top_cities(cc)
    def city_link(c):
        hs = c[4]
        if hs and hs in hub_pages: return f'<a href="{city_url_by_slug(hs)}">{e(c[0])}</a>'
        return f'<span>{e(c[0])}</span>'
    city_rows = ''.join(f'<li>{city_link(c)} <small>{e(fmt_pop(c[3]))}</small></li>' for c in tc)
    hub_line = ''
    if hubs:
        hub_line = '<p class="tdsc-lede" style="max-width:860px">' + e(f'{name} is home to ' + (f'{len(hubs)} of the world business hubs TDSC profiles: ' if len(hubs) > 1 else 'one of the world business hubs TDSC profiles: ') + ', '.join(h['name'] for h in hubs) + '.') + '</p>'
    cities = ''
    if tc:
        cities = f'''<section class="tdsc-sec tdsc-sec--paper" aria-labelledby="ct-h"><div class="tdsc-wrap">
<div class="tdsc-head tdsc-rv"><p class="tdsc-eyebrow">Cities</p><h2 id="ct-h">Largest Cities in {e(name)}</h2></div>{hub_line}
<ul class="v-citylist tdsc-rv">{city_rows}</ul>
<p class="tdsc-updated">Populations from GeoNames (CC BY 4.0); figures are approximate and vary by boundary definition. Use the city search in the header to find any city of 50,000 or more.</p></div></section>'''

    # --- neighbours
    nb = [CCA3[b] for b in jur.get('borders', []) if b in CCA3]
    nbl = ''.join((f'<a class="tdsc-chip" href="{jur_url(JUR[n]["slug"])}">{e(JUR[n]["name"])}</a>' if n in published else f'<span class="tdsc-chip">{e(JUR[n]["name"])}</span>') for n in nb)
    neighbours = f'<div class="tdsc-rv" style="margin-top:34px"><p class="tdsc-eyebrow">Neighbouring jurisdictions</p><div class="tdsc-chips">{nbl}</div></div>' if nb else ''

    faq = f'''<section class="tdsc-sec tdsc-sec--ivory" aria-labelledby="fq-h"><div class="tdsc-wrap tdsc-narrow">
<div class="tdsc-head tdsc-rv"><p class="tdsc-eyebrow">Questions</p><h2 id="fq-h">{e(name)}: Frequently Asked Questions</h2></div>
<div class="tdsc-faq tdsc-rv">{faq_html(d["faqs"])}</div></div></section>'''

    srcs = f'''<section class="tdsc-sec tdsc-sec--paper tdsc-sec--tight" aria-labelledby="sr-h"><div class="tdsc-wrap">
<div class="tdsc-head"><p class="tdsc-eyebrow">References</p><h2 id="sr-h">Sources</h2></div>{sources_html(d["sources"])}{neighbours}
<p class="tdsc-updated" style="margin-top:22px">Page reviewed {e(d.get("researched", BUILD_DATE))}. Laws and lists change; verify before relying on any item.</p></div></section>'''

    citybar = f'<div class="v-citybar" data-citybar hidden><div class="tdsc-wrap"></div></div>'
    order = seed(cc, 4, 'order')
    mid = [[matters, legal, practical, approach], [legal, matters, approach, practical], [matters, practical, legal, approach], [legal, approach, matters, practical]][order]
    body = citybar + hero + sanction_notice(cc, name) + overview + ''.join(mid) + cities + faq + srcs + cta(
        f'Discuss a Matter Involving {name}',
        f'Describe the matter in general terms. TDSC leadership will review jurisdiction, authorization and scope for work touching {name} before any engagement begins.')

    schema = [
        {'@type': 'WebPage', '@id': INTL + path + '#webpage', 'url': INTL + path, 'name': title, 'description': desc, 'inLanguage': 'en',
         'isPartOf': {'@type': 'WebSite', '@id': INTL + '/#website', 'url': INTL + '/', 'name': 'TDSC International', 'publisher': {'@id': ORG_ID}},
         'about': {'@type': 'Country', 'name': name}, 'publisher': {'@id': ORG_ID}, 'dateModified': d.get('researched', BUILD_DATE),
         'breadcrumb': crumbs_ld(cr)},
        {'@type': 'Service', '@id': INTL + path + '#service', 'name': f'Investigative consulting involving {name}', 'serviceType': 'Investigative consulting',
         'provider': {'@type': 'Organization', '@id': ORG_ID, 'name': 'Thiel Detective Service Company', 'url': SITE + '/'},
         'areaServed': {'@type': 'Country', 'name': name}, 'description': d['hero_lede']},
        {'@type': 'FAQPage', '@id': INTL + path + '#faq', 'mainEntity': [{'@type': 'Question', 'name': f['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}} for f in d['faqs']]}]
    return path, doc(path, title, desc, body, schema, accent, nav=name)

# ---------------------------------------------------------------- hub city page
def render_city(h, d, published):
    cc = h['cc']; jur = JUR.get(cc) or JUR.get(TERR.get(cc, ''), {})
    slug = hub_slug(h); path = city_url(h)
    name = d.get('name', h['name']); cname = jur.get('name', cc)
    accent = ACCENTS[seed(slug, 5, 'acc')]
    title = title_for(name)
    desc = d['meta_description']
    cr = [('TDSC', '/'), ('International', '/international')]
    if cc in published: cr.append((cname, jur_url(jur['slug'])))
    cr.append((name, path))
    # local plate: country outline with this hub
    markers = [(name, h['lat'], h['lng'], 'capital' if (CAPS.get(cc) and CAPS[cc][0] == h['gname']) else 'hub')]
    plate = map_plate(cc, jur, markers, parch=seed(slug, 2, 'pl') == 1) if jur else ''
    tz = h.get('tz')
    meta = [('Country', cname), ('GaWC 2024', h['tier']), ('Local time', offset_vs_nashville(tz) or '—')]
    hero = f'''<section class="tdsc-hero v-hero{["", " v-hero--right", " v-hero--split"][seed(slug, 3, "hero")]}" aria-labelledby="tdsc-h1"><div class="tdsc-glassgrid"></div><div class="tdsc-wrap"><div class="tdsc-hero__in">
<div>{crumbs(cr)}<p class="tdsc-eyebrow">{e(d["eyebrow"])}</p><h1 id="tdsc-h1">{e(d.get("h1") or f"Investigative Consulting Involving {name}")}</h1><p class="tdsc-lede">{e(d["hero_lede"])}</p>
<div class="tdsc-btns"><a class="tdsc-btn tdsc-btn--brass" href="{M}/contact">Discuss a Matter {ARROW}</a>{f'<a class="tdsc-btn tdsc-btn--ghost" href="{jur_url(jur["slug"])}">{e(cname)} Framework</a>' if cc in published else ''}</div>
<div class="tdsc-hero-meta">{''.join(f'<span><b>{e(k)}</b> {e(v)}</span>' for k, v in meta)}</div></div>
<div class="tdsc-hero__art">{plate}</div></div></div></section>'''
    secs = []
    secs.append(f'''<section class="tdsc-sec tdsc-sec--ivory"><div class="tdsc-wrap"><div class="tdsc-head tdsc-rv"><p class="tdsc-eyebrow">Overview</p><h2>{e(name)} as a Business Centre</h2></div>
<div class="tdsc-prose tdsc-rv" style="max-width:860px">{''.join(f'<p>{e(p)}</p>' for p in d["intro"])}</div></div></section>''')
    if d.get('economy'):
        rows = ''.join(f'<div><dt>{e(x["label"])}</dt><dd>{e(x["value"])}</dd></div>' for x in d['economy'])
        secs.append(f'<section class="tdsc-sec tdsc-sec--midnight"><div class="tdsc-wrap"><div class="tdsc-head tdsc-rv"><p class="tdsc-eyebrow">Ledger</p><h2>{e(name)} in Figures and Institutions</h2></div><dl class="v-ledger v-ledger--dark tdsc-rv">{rows}</dl></div></section>')
    mcards = ''.join(f'<article class="tdsc-card tdsc-card--light tdsc-rv"><span class="tdsc-card__n">{i+1:02d}</span><h3>{e(m["title"])}</h3><p>{e(m["text"])}</p></article>' for i, m in enumerate(d['matters']))
    secs.append(f'<section class="tdsc-sec tdsc-sec--paper"><div class="tdsc-wrap"><div class="tdsc-head tdsc-rv"><p class="tdsc-eyebrow">Typical Matters</p><h2>Investigative Work Connected to {e(name)}</h2></div><div class="tdsc-grid-3">{mcards}</div></div></section>')
    if d.get('local_context'):
        tb = ''.join(f'<div class="v-topic tdsc-rv" data-n="{["I","II","III","IV","V","VI"][i]}"><h3>{e(t["title"])}</h3><p>{e(t["text"])}</p></div>' for i, t in enumerate(d['local_context']))
        secs.append(f'<section class="tdsc-sec tdsc-sec--ivory"><div class="tdsc-wrap"><div class="tdsc-head tdsc-rv"><p class="tdsc-eyebrow">Local Context</p><h2>Courts, Records and Institutions in {e(name)}</h2></div><div class="v-topics v-topics--{["cards","ledger","tabs"][seed(slug,3,"tp")]}">{tb}</div></div></section>')
    secs.append(f'''<section class="tdsc-sec tdsc-sec--parchment"><div class="tdsc-wrap"><div class="tdsc-notice tdsc-rv"><span class="tdsc-notice__label">Engagement Standard</span><h2>How TDSC Scopes Matters in {e(name)}</h2><p>{e(d["tdsc_approach"])}</p>
<p>TDSC has no office in {e(name)}. Engagements are directed from Nashville, Tennessee; where work on the ground is needed, it is performed by appropriately licensed local professionals under a written scope.</p></div></div></section>''')
    secs.append(f'<section class="tdsc-sec tdsc-sec--ivory"><div class="tdsc-wrap tdsc-narrow"><div class="tdsc-head tdsc-rv"><p class="tdsc-eyebrow">Questions</p><h2>{e(name)}: Frequently Asked Questions</h2></div><div class="tdsc-faq tdsc-rv">{faq_html(d["faqs"])}</div></div></section>')
    secs.append(f'<section class="tdsc-sec tdsc-sec--paper tdsc-sec--tight"><div class="tdsc-wrap"><div class="tdsc-head"><p class="tdsc-eyebrow">References</p><h2>Sources</h2></div>{sources_html(d["sources"])}<p class="tdsc-updated" style="margin-top:22px">Page reviewed {e(d.get("researched", BUILD_DATE))}. General information, not legal advice.</p></div></section>')
    body = hero + sanction_notice(cc, cname) + ''.join(secs) + cta(f'Discuss a Matter Involving {name}', f'Describe the matter in general terms. TDSC leadership will review jurisdiction, authorization and scope for work connected to {name} before any engagement begins.')
    schema = [{'@type': 'WebPage', '@id': INTL + path + '#webpage', 'url': INTL + path, 'name': title, 'description': desc, 'inLanguage': 'en',
               'about': {'@type': 'City', 'name': name, 'containedInPlace': {'@type': 'Country', 'name': cname}}, 'publisher': {'@id': ORG_ID}, 'breadcrumb': crumbs_ld(cr)},
              {'@type': 'Service', 'name': f'Investigative consulting involving {name}', 'serviceType': 'Investigative consulting',
               'provider': {'@type': 'Organization', '@id': ORG_ID, 'name': 'Thiel Detective Service Company', 'url': SITE + '/'}, 'areaServed': {'@type': 'City', 'name': name}},
              {'@type': 'FAQPage', 'mainEntity': [{'@type': 'Question', 'name': f['q'], 'acceptedAnswer': {'@type': 'Answer', 'text': f['a']}} for f in d['faqs']]}]
    return path, doc(path, title, desc, body, schema, accent, nav=name)

# ---------------------------------------------------------------- index page
def render_index(published, hub_pages):
    regions = {}
    for cc, j in sorted(JUR.items(), key=lambda kv: kv[1]['name']):
        regions.setdefault(j['region'] or 'Other', []).append(cc)
    dir_html = ''
    for r in sorted(regions):
        items = ''.join((f'<a href="{jur_url(JUR[c]["slug"])}">{e(JUR[c]["name"])}</a>' if c in published else f'<span class="v-pending">{e(JUR[c]["name"])}</span>') for c in regions[r])
        dir_html += f'<h3>{e(r)}</h3>{items}'
    hubs = ''.join(f'<a href="{city_url(h)}">{e(h["name"])}</a>' for h in HUBS if hub_slug(h) in hub_pages)
    hub_sec = ''
    if hubs:
        hub_sec = f'''<section class="tdsc-sec tdsc-sec--paper" id="hubs" aria-labelledby="hb-h"><div class="tdsc-wrap"><div class="tdsc-head tdsc-rv"><p class="tdsc-eyebrow">Business Hubs</p><h2 id="hb-h">Major International Business Hubs</h2></div><div class="v-dir">{hubs}</div></div></section>'''
    path = '/international'
    title = 'International Investigative Consulting | TDSC · Since 1873'
    desc = 'Investigative consulting across 200 jurisdictions from Thiel Detective Service Company: legal frameworks, records, data protection and how TDSC scopes cross-border work.'
    body = f'''<div class="v-citybar" data-citybar hidden><div class="tdsc-wrap"></div></div>
<section class="tdsc-hero" aria-labelledby="tdsc-h1"><div class="tdsc-glassgrid"></div><div class="tdsc-wrap"><div class="tdsc-hero__in"><div>
<p class="tdsc-eyebrow">TDSC International</p><h1 id="tdsc-h1">Investigative Consulting Across Borders</h1>
<p class="tdsc-lede">Jurisdiction-by-jurisdiction guidance on the legal environment, public records, data protection and investigator regulation that shape cross-border inquiries, and on how TDSC scopes engagements from its Nashville headquarters.</p>
<div class="v-big-search">{search_box('tdsc-qb', True)}</div>
<div class="tdsc-hero-meta"><span><b>{len(JUR)}</b> Jurisdictions</span><span><b>{len(SIDX["cities"]):,}</b> Cities searchable</span><span><b>HQ</b> Nashville, Tennessee</span></div></div>
<div class="tdsc-hero__art">{__import__("components").globe_svg()}</div></div></div></section>
<section class="tdsc-sec tdsc-sec--ivory" aria-labelledby="dr-h"><div class="tdsc-wrap"><div class="tdsc-head tdsc-rv"><p class="tdsc-eyebrow">Directory</p><h2 id="dr-h">Jurisdictions</h2>
<p class="tdsc-lede">{len(published)} jurisdiction profiles are published; the remainder are in research and appear as they are verified.</p></div><div class="v-dir">{dir_html}</div></div></section>
{hub_sec}
{cta("Discuss an International Matter", "Describe the matter in general terms. TDSC leadership will review jurisdiction, authorization and scope before any engagement begins.")}'''
    schema = [{'@type': 'WebSite', '@id': INTL + '/#website', 'url': INTL + '/', 'name': 'TDSC International', 'publisher': {'@id': ORG_ID}, 'inLanguage': 'en'},
              {'@type': 'CollectionPage', '@id': INTL + '/#webpage', 'url': INTL + '/', 'name': title, 'description': desc, 'isPartOf': {'@id': INTL + '/#website'},
               'publisher': {'@type': 'Organization', '@id': ORG_ID, 'name': 'Thiel Detective Service Company', 'url': SITE + '/'}}]
    return path, doc(path, title, desc, body, schema, 'brass', nav='International')

# ---------------------------------------------------------------- assets
JS = r'''<script>
/* TDSC International city search + city banner (v1). Index: GeoNames cities >= 50k (CC BY 4.0). */
(function(){
var d=document,IDX=null,loading=null,URL_IDX='__IDX__';
function ready(f){d.readyState!=='loading'?f():d.addEventListener('DOMContentLoaded',f)}
function norm(s){return (s||'').normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase().replace(/[^a-z0-9 ]+/g,' ').replace(/\s+/g,' ').trim()}
function load(){if(IDX)return Promise.resolve(IDX);if(loading)return loading;
 loading=fetch(URL_IDX).then(function(r){return r.json()}).then(function(j){
  j.n=j.t.map(function(c){return [norm(c[0]),norm(c[1])]});j.cn={};for(var k in j.c){j.cn[k]=norm(j.c[k][0])}
  IDX=j;return j});return loading}
function target(c,j){var hub=c[4];
 if(hub&&j.h[hub])return j.h[hub];
 var cj=j.c[j.t2[c[2]]||c[2]];
 if(cj&&cj[1])return cj[1]+'?city='+encodeURIComponent(c[0]);
 return '/international?city='+encodeURIComponent(c[0])}
function search(q,j){q=norm(q);if(q.length<2)return [];var out=[],i,n;
 for(var k in j.c){if(j.c[k][1]&&j.cn[k].indexOf(q)===0)out.push({s:3e9,label:j.c[k][0],sub:'Jurisdiction',href:j.c[k][1],hub:1})}
 for(i=0;i<j.t.length;i++){n=j.n[i];var c=j.t[i],sc=-1;
  if(n[0]===q||n[1]===q)sc=2e9;else if(n[0].indexOf(q)===0||n[1].indexOf(q)===0)sc=1e9;else if(q.length>3&&n[0].indexOf(' '+q)>-1)sc=0;
  if(sc>-1)out.push({s:sc+c[3],label:c[0],sub:(j.c[c[2]]?j.c[c[2]][0]:c[2]),href:target(c,j),hub:!!(c[4]&&j.h[c[4]])})}
 out.sort(function(a,b){return b.s-a.s});return out.slice(0,9)}
function wire(box){var inp=box.querySelector('input'),ul=box.querySelector('.v-results'),sel=-1,res=[];
 function close(){ul.hidden=true;inp.setAttribute('aria-expanded','false');sel=-1}
 function draw(){ul.innerHTML='';res.forEach(function(r,i){var li=d.createElement('li'),a=d.createElement('a');a.href=r.href;a.setAttribute('role','option');a.id=inp.id+'-o'+i;
   if(r.hub)a.className='v-hub';a.appendChild(d.createTextNode(r.label));var s=d.createElement('span');s.textContent=r.sub;a.appendChild(s);li.appendChild(a);ul.appendChild(li)});
  if(!res.length&&inp.value.trim().length>1){var li=d.createElement('li'),a=d.createElement('a');a.href='/international';a.textContent='No city of 50,000+ found \u2014 browse jurisdictions';li.appendChild(a);ul.appendChild(li)}
  ul.hidden=!ul.children.length;inp.setAttribute('aria-expanded',ul.hidden?'false':'true')}
 function mark(){[].forEach.call(ul.querySelectorAll('a'),function(a,i){a.setAttribute('aria-selected',i===sel?'true':'false')});if(sel>-1)inp.setAttribute('aria-activedescendant',inp.id+'-o'+sel)}
 inp.addEventListener('focus',load);
 inp.addEventListener('input',function(){var v=inp.value;load().then(function(j){if(inp.value!==v)return;res=search(v,j);sel=-1;draw()})});
 inp.addEventListener('keydown',function(ev){if(ev.key==='ArrowDown'){sel=Math.min(sel+1,res.length-1);mark();ev.preventDefault()}
  else if(ev.key==='ArrowUp'){sel=Math.max(sel-1,0);mark();ev.preventDefault()}
  else if(ev.key==='Enter'){var r=res[sel>-1?sel:0];if(r){location.href=r.href;ev.preventDefault()}}
  else if(ev.key==='Escape'){close()}});
 d.addEventListener('click',function(ev){if(!box.contains(ev.target))close()})}
ready(function(){
 d.querySelectorAll('[data-search]').forEach(wire);
 var qs=new URLSearchParams(location.search),city=qs.get('city'),bar=d.querySelector('[data-citybar]');
 if(city&&bar){city=city.slice(0,80);var w=bar.firstElementChild,b=d.createElement('b');b.textContent=city;
  w.appendChild(d.createTextNode('Matters involving '));w.appendChild(b);
  w.appendChild(d.createTextNode(/^\/international\/?$/.test(location.pathname)?': a dedicated profile for this jurisdiction is in research. Contact TDSC to discuss the matter directly.':' are scoped under the jurisdictional framework set out on this page.'));
  bar.hidden=false}
});
})();
</script>'''

EXTRA_CSS = '''
.v-citylist{list-style:none;margin:26px 0 18px;padding:0;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:0 28px}
.v-citylist li{padding:10px 0;border-bottom:1px solid var(--tdsc-hair);display:flex;justify-content:space-between;gap:10px}
.v-citylist a{color:var(--tdsc-navy);font-weight:600;text-decoration:none}.v-citylist a:hover{color:var(--tdsc-brass)}
.v-citylist small{color:var(--tdsc-muted);font-variant-numeric:tabular-nums}
.tdsc-chips{display:flex;flex-wrap:wrap;gap:8px}.tdsc-chip{display:inline-block;padding:6px 12px;border:1px solid var(--tdsc-hair);font-size:.86rem;color:var(--tdsc-ink);text-decoration:none;background:#fff}
a.tdsc-chip:hover{border-color:var(--tdsc-brass)}
@media(max-width:1024px){.v-citylist{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(max-width:560px){.v-citylist{grid-template-columns:1fr}}
.tdsc-hdr__in{gap:18px}
.v-dir .v-pending{display:block}
@media(max-width:1440px){.v-hdr-search .v-search{width:210px}}
@media(max-width:1280px){.tdsc-hdr__in>.tdsc-btn{display:none}}
'''

def minify_css(s):
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    return re.sub(r'\s*\n\s*', '', s)

FAVICON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="10" fill="#0B1422"/><circle cx="32" cy="32" r="22" fill="none" stroke="#C2A06A" stroke-width="2.5"/><text x="32" y="40" text-anchor="middle" font-family="Georgia,serif" font-size="22" font-weight="700" fill="#E2CFA4">T</text></svg>'

def write(path, text):
    full = os.path.join(OUT, path.lstrip('/'))
    os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'w', encoding='utf-8').write(text)

def main():
    global HUB_BY_SLUG
    css = minify_css(open(os.path.join(HERE, 'brand', 'intl.css')).read() + EXTRA_CSS)
    countries = load_countries()
    published = {cc for cc, x in countries.items() if cc in JUR and publishable(x)}
    held = sorted(set(countries) - published)
    cdir = os.path.join(CONTENT, 'cities'); cities = {}
    if os.path.isdir(cdir):
        for f in os.listdir(cdir):
            if f.endswith('.json'):
                x = json.load(open(os.path.join(cdir, f)))
                if len(x.get('sources', [])) >= MIN_SOURCES: cities[x['slug']] = x
    HUB_BY_SLUG = {hub_slug(h): h for h in HUBS}
    hub_pages = {s for s in cities if s in HUB_BY_SLUG}
    PAGES.clear()
    def emit(path, frag):
        write('pages/' + PAGES[-1]['key'] + '.html', frag)
    emit(*render_index(published, hub_pages))
    for cc in sorted(published):
        emit(*render_jurisdiction(cc, countries[cc], published, hub_pages))
    for s_ in sorted(hub_pages):
        emit(*render_city(HUB_BY_SLUG[s_], cities[s_], published))
    write('assets/intl.css', css)
    write('assets/search.js', JS.replace('__IDX__', IDX_URL))
    idx = {'c': {}, 't': SIDX['cities'], 'h': {s_: city_url(HUB_BY_SLUG[s_]) for s_ in sorted(hub_pages)}, 't2': TERR}
    for cc, v in SIDX['countries'].items():
        idx['c'][cc] = [v[0], jur_url(v[1]) if cc in published else '']
    write('assets/search-index.json', json.dumps(idx, ensure_ascii=False, separators=(',', ':')))
    write('manifest.json', json.dumps(PAGES, ensure_ascii=False, indent=1))
    print(f'built {len(PAGES)} fragments -> {OUT}; jurisdictions {len(published)}, held back {held}, hubs {len(hub_pages)}; max fragment {max(p["bytes"] for p in PAGES)//1024} KB')

if __name__ == '__main__':
    main()
