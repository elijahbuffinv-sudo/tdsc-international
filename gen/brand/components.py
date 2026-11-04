"""TDSC shared components: tokens, icons, SVG artwork, chrome (header/footer), schema helpers."""
import html, json, math, hashlib, re

SITE = 'https://www.thieldetectiveagency.com'
PHONE_DISPLAY = '+1 (629) 310-8667'
PHONE_TEL = '+16293108667'
EMAIL = 'contact@delatorgroup.com'
DELATOR = 'https://www.delatorgroup.com'
ORG_ID = SITE + '/#organization'
CONSULT = '/consulting'
def U(key): return f'{CONSULT}/{key}'
e = lambda s: html.escape(str(s), quote=True)

CATS = {
  'investigative': dict(name='Investigative and Corporate Consulting', short='Investigative & Corporate', anchor='investigative-corporate',
     blurb='Structured investigative consulting for organizations confronting allegations, transactions, disputes and questions of integrity.'),
  'cyber': dict(name='Cyber and Digital Consulting', short='Cyber & Digital', anchor='cyber-digital',
     blurb='Advisory and coordinated technical support for incidents, digital evidence, security posture and open-source intelligence.'),
  'risk': dict(name='Risk, Compliance, and Strategic Consulting', short='Risk & Strategy', anchor='risk-compliance-strategy',
     blurb='Investigative perspective applied to compliance programs, third parties, controls, executive exposure and cross-border strategy.'),
}

# ---------------------------------------------------------------- icons (24x24 line)
ICONS = {
 'ledger':'<path d="M5 3.5h11.5a2 2 0 0 1 2 2V20.5H7a2 2 0 0 1-2-2z"/><path d="M5 18.5a2 2 0 0 1 2-2h11.5"/><path d="M9 7.5h6M9 10.5h6M9 13.5h3.5"/>',
 'network':'<circle cx="12" cy="5" r="2"/><circle cx="5" cy="18" r="2"/><circle cx="19" cy="18" r="2"/><circle cx="12" cy="12.5" r="1.6"/><path d="M12 7v3.9M10.7 13.6 6.5 16.8M13.3 13.6l4.2 3.2M7 18h10"/>',
 'shield':'<path d="M12 3 4.5 6v5.5c0 4.6 3.1 8.2 7.5 9.5 4.4-1.3 7.5-4.9 7.5-9.5V6z"/><path d="m8.8 12 2.3 2.3 4.3-4.6"/>',
 'scale':'<path d="M12 3.5v17M7 20.5h10M5 7h14M12 5l-7 2M12 5l7 2"/><path d="m5 7-2.6 6.2a2.8 2.8 0 0 0 5.2 0z"/><path d="m19 7-2.6 6.2a2.8 2.8 0 0 0 5.2 0z"/>',
 'globe':'<circle cx="12" cy="12" r="8.5"/><path d="M3.5 12h17M12 3.5c2.6 2.6 3.6 5.3 3.6 8.5s-1 5.9-3.6 8.5c-2.6-2.6-3.6-5.3-3.6-8.5s1-5.9 3.6-8.5z"/>',
 'fingerprint':'<path d="M7.5 5.5A7.5 7.5 0 0 1 19.5 11v2"/><path d="M4.5 9.5a7.6 7.6 0 0 0-.5 2.7c0 2 .5 3.8 1.4 5.4"/><path d="M8.5 19.5c-.9-1.8-1.5-4-1.5-6.5a5 5 0 0 1 10 0c0 1.3-.1 2.6-.3 3.8"/><path d="M12 13c0 2.9.6 5.4 1.8 7.5M15.6 19.8c.3-.9.5-1.8.6-2.8"/>',
 'terminal':'<rect x="3" y="4.5" width="18" height="15" rx="1.5"/><path d="m7 9.5 3 2.5-3 2.5M12 15h5"/>',
 'lock':'<rect x="5" y="10.5" width="14" height="10" rx="1.5"/><path d="M8 10.5V7.5a4 4 0 0 1 8 0v3"/><path d="M12 14.5v2.5"/>',
 'eye':'<path d="M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z"/><circle cx="12" cy="12" r="3"/>',
 'compass':'<circle cx="12" cy="12" r="8.5"/><path d="m15.5 8.5-2.1 4.9-4.9 2.1 2.1-4.9z"/>',
 'document':'<path d="M6 3h8.5L19 7.5V21H6z"/><path d="M14 3v5h5M9 12h7M9 15h7M9 18h4"/>',
 'chart':'<path d="M4 4v16h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
 'building':'<path d="M5 21V4.5l9-1.5V21M14 8l5 1.5V21M3 21h18"/><path d="M8 7.5h3M8 10.5h3M8 13.5h3M8 16.5h3"/>',
 'key':'<circle cx="8" cy="15" r="4"/><path d="m10.8 12.2 8.7-8.7M16.5 6.5l2.5 2.5M14 9l2 2"/>',
 'radar':'<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.3"/><path d="M12 12 18 6"/>',
 'people':'<circle cx="9" cy="8" r="3.2"/><path d="M3 20c.4-3.4 2.9-5.5 6-5.5s5.6 2.1 6 5.5"/><circle cx="17" cy="9" r="2.5"/><path d="M16.5 14.6c2.5.2 4.1 2 4.5 4.9"/>',
}
def icon(name, cls='tdsc-ico'):
    return f'<span class="{cls}" aria-hidden="true"><svg viewBox="0 0 24 24">{ICONS[name]}</svg></span>'
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'

# ---------------------------------------------------------------- monogram & seal
def star(cx, cy, R, r, n=4, rot=0.0):
    pts = []
    for i in range(n * 2):
        a = rot + math.pi * i / n; rr = R if i % 2 == 0 else r
        pts.append(f'{cx + rr*math.sin(a):.1f},{cy - rr*math.cos(a):.1f}')
    return 'M' + 'L'.join(pts) + 'Z'

_MONO_T = None
def monogram_svg(cls='', label='TDSC monogram'):
    global _MONO_T
    if _MONO_T is None:
        s = open(__import__('os').path.join(__import__('os').path.dirname(__file__),'tdsc-monogram-dark.svg')).read()
        # keep the T glyph path from the generated outline file
        _MONO_T = re.findall(r'<path d="([^"]+)" fill="#F3ECDD"/>', s)[0]
    stars = ''.join(f'<path d="{star(64+52*math.sin(math.pi/2*i), 64-52*math.cos(math.pi/2*i), 6, 2)}" fill="#C2A06A"/>' for i in range(4))
    return (f'<svg class="{cls}" viewBox="0 0 128 128" role="img" aria-label="{label}"><circle cx="64" cy="64" r="56" fill="none" stroke="#C2A06A" stroke-width="4"/>'
            f'<circle cx="64" cy="64" r="48" fill="none" stroke="#9C7A45" stroke-width="1.6"/>{stars}<path d="{_MONO_T}" fill="#F3ECDD"/></svg>')

_sealn = [0]
def seal_svg(cls='', ring='#C2A06A', fine='#9C7A45', text='#F3ECDD', accent='#C2A06A', bg='#0B1422', label='Thiel Detective Service Company seal, established 1873'):
    """Seal using live web fonts (Cinzel / Cormorant) via textPath — tiny and crisp."""
    _sealn[0] += 1; n = _sealn[0]; cx = cy = 250
    beads = ''.join(f'<circle cx="{cx+229*math.sin(2*math.pi*i/90):.1f}" cy="{cy-229*math.cos(2*math.pi*i/90):.1f}" r="1.7"/>' for i in range(90))
    ticks = ''.join(f'<line x1="{cx+(146-(8 if i%9==0 else 4))*math.sin(2*math.pi*i/72):.1f}" y1="{cy-(146-(8 if i%9==0 else 4))*math.cos(2*math.pi*i/72):.1f}" x2="{cx+146*math.sin(2*math.pi*i/72):.1f}" y2="{cy-146*math.cos(2*math.pi*i/72):.1f}"/>' for i in range(72))
    seps = ''.join(f'<path d="{star(cx+186*math.sin(math.radians(d)), cy-186*math.cos(math.radians(d)), 9, 2.6, 4, math.radians(d))}"/>' for d in (-112, 112))
    return f'''<svg class="{cls}" viewBox="0 0 500 500" role="img" aria-label="{label}"><defs><path id="tdsc-st{n}" d="M {cx-175},{cy} A 175 175 0 0 1 {cx+175},{cy}"/><path id="tdsc-sb{n}" d="M {cx-206},{cy} A 206 206 0 0 0 {cx+206},{cy}"/></defs>
<g fill="none" stroke="{ring}"><circle cx="{cx}" cy="{cy}" r="244" stroke-width="3.5"/><circle cx="{cx}" cy="{cy}" r="236" stroke-width="1"/><circle cx="{cx}" cy="{cy}" r="221" stroke-width="1.25"/><circle cx="{cx}" cy="{cy}" r="153" stroke-width="1.25"/><circle cx="{cx}" cy="{cy}" r="146" stroke-width="3"/></g>
<g fill="{fine}">{beads}</g><g stroke="{fine}" stroke-width=".9">{ticks}</g>
<g fill="none" stroke="{fine}"><path d="{star(cx,cy,138,9,4)}" stroke-width="1"/><path d="{star(cx,cy,96,7,4,math.pi/4)}" stroke-width=".8" opacity=".8"/></g>
<text font-family="Cinzel,Georgia,serif" font-weight="700" font-size="25" letter-spacing="1.9" fill="{text}"><textPath href="#tdsc-st{n}" startOffset="50%" text-anchor="middle">THIEL DETECTIVE SERVICE COMPANY</textPath></text>
<text font-family="Cinzel,Georgia,serif" font-weight="600" font-size="20" letter-spacing="3" fill="{accent}"><textPath href="#tdsc-sb{n}" startOffset="50%" text-anchor="middle">ESTABLISHED  MDCCCLXXIII</textPath></text>
<g fill="{accent}">{seps}</g>
<circle cx="{cx}" cy="{cy}" r="74" fill="{bg}" stroke="{ring}" stroke-width="2"/><circle cx="{cx}" cy="{cy}" r="68" fill="none" stroke="{fine}" stroke-width=".8"/>
<text x="{cx}" y="{cy+33}" text-anchor="middle" font-family="'Cormorant Garamond',Georgia,serif" font-weight="600" font-size="96" fill="{text}">T</text>
<line x1="{cx-22}" y1="{cy+37}" x2="{cx+22}" y2="{cy+37}" stroke="{accent}"/>
<text x="{cx}" y="{cy+55}" text-anchor="middle" font-family="Cinzel,Georgia,serif" font-weight="700" font-size="15" letter-spacing="3" fill="{accent}">1873</text></svg>'''

# ---------------------------------------------------------------- deterministic RNG
class R:
    def __init__(self, key): self.s = int(hashlib.md5(key.encode()).hexdigest()[:8], 16)
    def r(self):
        self.s = (1103515245 * self.s + 12345) & 0x7fffffff; return self.s / 0x7fffffff
    def u(self, a, b): return a + (b - a) * self.r()

# ---------------------------------------------------------------- hero art: home "collision"
def tower_svg():
    """Glass curtain-wall tower in two-point perspective."""
    g = []
    # left face & right face polygons
    L = [(210,40),(330,10),(330,640),(210,640)]
    Rf = [(330,10),(470,62),(470,640),(330,640)]
    g.append(f'<polygon points="{" ".join(f"{x},{y}" for x,y in L)}" fill="url(#tdsc-gl1)"/>')
    g.append(f'<polygon points="{" ".join(f"{x},{y}" for x,y in Rf)}" fill="url(#tdsc-gl2)"/>')
    for i in range(1, 7):  # mullions left
        x = 210 + 120 * i / 7; y = 40 - 30 * i / 7
        g.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="640" stroke="rgba(194,160,106,.22)" stroke-width="1"/>')
    for i in range(1, 8):
        x = 330 + 140 * i / 8; y = 10 + 52 * i / 8
        g.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="640" stroke="rgba(194,160,106,.18)" stroke-width="1"/>')
    for j in range(1, 26):  # floors
        t = j / 26
        yl = 40 + (640 - 40) * t; ym = 10 + (640 - 10) * t; yr = 62 + (640 - 62) * t
        g.append(f'<polyline points="210,{yl:.1f} 330,{ym:.1f} 470,{yr:.1f}" fill="none" stroke="rgba(169,177,188,.16)" stroke-width="1"/>')
    g.append('<polygon points="330,10 470,62 470,300 330,170" fill="url(#tdsc-gl3)" opacity=".55"/>')
    g.append('<line x1="330" y1="10" x2="330" y2="640" stroke="rgba(217,199,160,.55)" stroke-width="1.2"/>')
    return ''.join(g)

def home_hero_svg():
    seal = seal_svg('', label='TDSC seal')
    seal_inner = seal[seal.index('>') + 1: seal.rindex('</svg>')]
    return f'''<svg viewBox="0 0 600 660" role="img" aria-label="Thiel Detective Service Company — Victorian investigative archive meets modern glass headquarters">
<defs>
<linearGradient id="tdsc-gl1" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1D3150"/><stop offset=".55" stop-color="#15243A"/><stop offset="1" stop-color="#0E1A2B"/></linearGradient>
<linearGradient id="tdsc-gl2" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2A4366"/><stop offset=".5" stop-color="#1A2C47"/><stop offset="1" stop-color="#0E1A2B"/></linearGradient>
<linearGradient id="tdsc-gl3" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9C7A0" stop-opacity=".55"/><stop offset="1" stop-color="#D9C7A0" stop-opacity="0"/></linearGradient>
<radialGradient id="tdsc-glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#C2A06A" stop-opacity=".35"/><stop offset="1" stop-color="#C2A06A" stop-opacity="0"/></radialGradient>
<linearGradient id="tdsc-parch" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F1E8D4"/><stop offset=".6" stop-color="#E4D7BA"/><stop offset="1" stop-color="#D5C39E"/></linearGradient>
<filter id="tdsc-rough"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" result="n"/><feColorMatrix in="n" values="0 0 0 0 .4 0 0 0 0 .3 0 0 0 0 .15 0 0 0 .22 0" result="c"/><feComposite in="c" in2="SourceGraphic" operator="in" result="t"/><feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="t"/></feMerge></filter>
</defs>
<circle cx="372" cy="150" r="270" fill="url(#tdsc-glow)"/>
<g class="tdsc-tower">{tower_svg()}</g>
<g transform="translate(18,258) rotate(-4)">
 <rect width="300" height="372" fill="url(#tdsc-parch)" stroke="#9C7A45" stroke-opacity=".6"/>
 <rect x="9" y="9" width="282" height="354" fill="none" stroke="#9C7A45" stroke-opacity=".45"/>
 <text x="150" y="50" text-anchor="middle" font-family="Cinzel,Georgia,serif" font-size="11" letter-spacing="3" fill="#3A2A1E">THE</text>
 <text x="150" y="80" text-anchor="middle" font-family="Cinzel,Georgia,serif" font-weight="700" font-size="22" letter-spacing="1.5" fill="#0E1A2B">THIEL DETECTIVE</text>
 <text x="150" y="106" text-anchor="middle" font-family="Cinzel,Georgia,serif" font-weight="700" font-size="18" letter-spacing="1.5" fill="#0E1A2B">SERVICE CO.</text>
 <line x1="70" y1="122" x2="230" y2="122" stroke="#9C7A45"/><path d="{star(150,122,6,1.8)}" fill="#9C7A45"/>
 <text x="150" y="146" text-anchor="middle" font-family="'Cormorant Garamond',Georgia,serif" font-style="italic" font-size="17" fill="#3A2A1E">Established 1873</text>
 <g font-family="'Courier New',Courier,monospace" font-size="11" fill="#3A2A1E" letter-spacing=".5">
  <text x="30" y="190">ORIGIN ........ ST. LOUIS, MO.</text>
  <text x="30" y="212">CABLE ADDRESS . "THIELON"</text>
  <text x="30" y="234">FOUNDER ....... G. H. THIEL</text>
  <text x="30" y="270">REINTRODUCED .. DELATOR GROUP</text>
  <text x="30" y="292">HEADQUARTERS .. NASHVILLE, TN</text>
 </g>
 <g transform="translate(196,300) rotate(-9)"><rect width="84" height="34" fill="none" stroke="#9C7A45" stroke-width="1.5"/><text x="42" y="22" text-anchor="middle" font-family="Cinzel,Georgia,serif" font-weight="700" font-size="10" letter-spacing="2" fill="#9C7A45">ARCHIVE</text></g>
</g>
<g transform="translate(372,214) scale(.42)" opacity=".98">{seal_inner}</g>
<g stroke="#C2A06A" stroke-opacity=".5" fill="none"><path d="M300 560 C 420 520, 500 470, 560 380" stroke-dasharray="2 6"/><circle cx="560" cy="380" r="3" fill="#C2A06A"/></g>
</svg>'''

# ---------------------------------------------------------------- service dossier art (unique per page)
def dossier_svg(d, idx):
    rnd = R(d['key']); cat = d['category']
    nodes = [(rnd.u(300, 480), rnd.u(250, 470)) for _ in range(7)]
    edges = ''.join(f'<line x1="{nodes[i][0]:.0f}" y1="{nodes[i][1]:.0f}" x2="{nodes[j][0]:.0f}" y2="{nodes[j][1]:.0f}"/>' for i in range(7) for j in range(i+1, 7) if rnd.r() < .32)
    dots = ''.join(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.u(2.5,5):.1f}"/>' for x, y in nodes)
    spark = ' '.join(f'{300 + i*9},{520 - rnd.u(4, 34):.0f}' for i in range(21))
    bars = ''.join(f'<rect x="{306 + i*20}" y="{520 - h:.0f}" width="9" height="{h:.0f}"/>' for i, h in enumerate([rnd.u(10, 44) for _ in range(9)]))
    hexes = ''
    if cat == 'cyber':
        for r_ in range(4):
            for c in range(5):
                x = 312 + c * 34 + (17 if r_ % 2 else 0); y = 268 + r_ * 30
                if rnd.r() < .6:
                    hexes += f'<path d="M{x},{y-15} l13,7.5 v15 l-13,7.5 l-13,-7.5 v-15z" opacity="{rnd.u(.25,.9):.2f}"/>'
    lines = ''.join(f'<rect x="34" y="{246 + i*22}" width="{rnd.u(90, 196):.0f}" height="6" rx="1" fill="#3A2A1E" opacity=".22"/>' for i in range(7))
    num = f'{idx:02d}'
    short = d['short'].upper()
    fsz = 15 if len(short) <= 18 else (12.5 if len(short) <= 24 else 10.5)
    glass_vis = {'investigative': f'<g stroke="#C2A06A" stroke-opacity=".55" stroke-width="1">{edges}</g><g fill="#D9C7A0">{dots}</g>',
                 'cyber': f'<g fill="none" stroke="#C2A06A" stroke-width="1">{hexes}</g><polyline points="{spark}" fill="none" stroke="#D9C7A0" stroke-width="1.4"/>',
                 'risk': f'<g fill="#C2A06A" opacity=".75">{bars}</g><polyline points="{spark}" fill="none" stroke="#D9C7A0" stroke-width="1.2" opacity=".7"/><g stroke="#C2A06A" stroke-opacity=".4">{edges}</g>'}[cat]
    return f'''<svg viewBox="0 0 520 580" role="img" aria-label="{e(d['image_alt'])}">
<defs><linearGradient id="tdsc-dp{num}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#F1E8D4"/><stop offset="1" stop-color="#D8C7A3"/></linearGradient>
<linearGradient id="tdsc-dg{num}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2A4366" stop-opacity=".92"/><stop offset="1" stop-color="#0E1A2B" stop-opacity=".88"/></linearGradient></defs>
<g transform="translate(10,40) rotate(-3)">
<rect width="300" height="420" fill="url(#tdsc-dp{num})" stroke="#9C7A45" stroke-opacity=".6"/>
<rect x="9" y="9" width="282" height="402" fill="none" stroke="#9C7A45" stroke-opacity=".4"/>
<text x="26" y="44" font-family="'Courier New',Courier,monospace" font-size="11" letter-spacing="1.5" fill="#3A2A1E">TDSC · DOSSIER Nº {num}</text>
<text x="274" y="44" text-anchor="end" font-family="'Courier New',Courier,monospace" font-size="11" fill="#3A2A1E">{cat[:5].upper()}</text>
<line x1="26" y1="56" x2="274" y2="56" stroke="#3A2A1E" stroke-opacity=".35" stroke-dasharray="3 3"/>
<circle cx="150" cy="140" r="58" fill="none" stroke="#9C7A45" stroke-width="1.5"/><circle cx="150" cy="140" r="50" fill="none" stroke="#9C7A45" stroke-opacity=".5"/>
<g transform="translate(118,108) scale(2.66)" fill="none" stroke="#0E1A2B" stroke-width=".9" stroke-linecap="round" stroke-linejoin="round">{ICONS[d['icon']]}</g>
<text x="150" y="226" text-anchor="middle" font-family="Cinzel,Georgia,serif" font-weight="700" font-size="{fsz}" letter-spacing="1.6" fill="#0E1A2B">{e(short)}</text>
{lines}
<g transform="translate(176,372) rotate(-8)"><rect width="100" height="30" fill="none" stroke="#9C7A45" stroke-width="1.5"/><text x="50" y="20" text-anchor="middle" font-family="Cinzel,Georgia,serif" font-weight="700" font-size="9" letter-spacing="1.8" fill="#9C7A45">SINCE 1873</text></g>
</g>
<g><rect x="280" y="222" width="226" height="330" rx="6" fill="url(#tdsc-dg{num})" stroke="#C2A06A" stroke-opacity=".45"/>
<text x="300" y="250" font-family="Inter,Arial,sans-serif" font-size="9.5" letter-spacing="2.2" fill="#C2A06A">ANALYSIS · {num}</text>
<line x1="300" y1="260" x2="486" y2="260" stroke="#C2A06A" stroke-opacity=".25"/>
{glass_vis}
<line x1="300" y1="524" x2="486" y2="524" stroke="#C2A06A" stroke-opacity=".25"/>
<text x="300" y="542" font-family="Inter,Arial,sans-serif" font-size="9" letter-spacing="1.6" fill="rgba(246,241,230,.6)">NASHVILLE · INTERNATIONAL</text></g>
</svg>'''

# ---------------------------------------------------------------- globe
def globe_svg(label='Stylized globe showing international consulting reach from TDSC headquarters in Nashville, Tennessee', size=520):
    lon0, lat0 = math.radians(-40), math.radians(28); R_ = 230; cx = cy = 260
    def proj(lat, lon):
        lat, lon = math.radians(lat), math.radians(lon)
        cosc = math.sin(lat0)*math.sin(lat) + math.cos(lat0)*math.cos(lat)*math.cos(lon-lon0)
        x = R_*math.cos(lat)*math.sin(lon-lon0)
        y = R_*(math.cos(lat0)*math.sin(lat) - math.sin(lat0)*math.cos(lat)*math.cos(lon-lon0))
        return cx + x, cy - y, cosc > 0
    paths = []
    for lat in range(-75, 90, 15):
        seg = []; out = []
        for lon in range(-180, 181, 6):
            x, y, v = proj(lat, lon)
            if v: seg.append(f'{x:.1f},{y:.1f}')
            elif seg: out.append(seg); seg = []
        if seg: out.append(seg)
        paths += ['M' + 'L'.join(s) for s in out if len(s) > 1]
    for lon in range(-180, 180, 20):
        seg = []; out = []
        for lat in range(-88, 89, 6):
            x, y, v = proj(lat, lon)
            if v: seg.append(f'{x:.1f},{y:.1f}')
            elif seg: out.append(seg); seg = []
        if seg: out.append(seg)
        paths += ['M' + 'L'.join(s) for s in out if len(s) > 1]
    hq = proj(36.16, -86.78)
    # abstract destinations (unlabeled) — illustrate reach, not offices
    dests = [(51.5, -0.1), (48.9, 2.3), (40.4, -3.7), (25.2, 55.3), (-23.5, -46.6), (19.4, -99.1), (43.7, -79.4), (6.5, 3.4), (52.5, 13.4)]
    arcs = ''
    for la, lo in dests:
        x, y, v = proj(la, lo)
        if not v: continue
        mx, my = (hq[0] + x) / 2, (hq[1] + y) / 2 - math.hypot(x - hq[0], y - hq[1]) * .28
        arcs += f'<path d="M{hq[0]:.1f},{hq[1]:.1f} Q{mx:.1f},{my:.1f} {x:.1f},{y:.1f}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" class="tdsc-gd"/>'
    return f'''<svg viewBox="0 0 520 520" role="img" aria-label="{e(label)}"><defs><radialGradient id="tdsc-gb" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#1D3150"/><stop offset="1" stop-color="#0B1422"/></radialGradient></defs>
<circle cx="{cx}" cy="{cy}" r="{R_+16}" fill="none" stroke="#C2A06A" stroke-opacity=".25"/><circle cx="{cx}" cy="{cy}" r="{R_}" fill="url(#tdsc-gb)" stroke="#C2A06A" stroke-opacity=".6"/>
<path d="{"".join(paths)}" fill="none" stroke="#A9B1BC" stroke-opacity=".18" stroke-width=".8"/>
<g fill="none" stroke="#C2A06A" stroke-width="1.2" stroke-opacity=".8" stroke-dasharray="3 4">{arcs.replace('class="tdsc-gd"','fill="#D9C7A0" stroke="none"')}</g>
<circle cx="{hq[0]:.1f}" cy="{hq[1]:.1f}" r="12" fill="none" stroke="#C2A06A" stroke-opacity=".5"/><circle cx="{hq[0]:.1f}" cy="{hq[1]:.1f}" r="5.5" fill="#C2A06A"/>
<text x="{hq[0]-14:.1f}" y="{hq[1]+30:.1f}" text-anchor="end" font-family="Cinzel,Georgia,serif" font-size="12" letter-spacing="2.5" fill="#F3ECDD">NASHVILLE HQ</text></svg>'''

# ---------------------------------------------------------------- shared blocks
def crumbs(items):
    lis = []
    for i, (name, url) in enumerate(items):
        if i == len(items) - 1: lis.append(f'<li><span aria-current="page">{e(name)}</span></li>')
        else: lis.append(f'<li><a href="{url}">{e(name)}</a></li>')
    return f'<nav class="tdsc-crumbs" aria-label="Breadcrumb"><ol>{"".join(lis)}</ol></nav>'

def crumbs_ld(items):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i + 1, 'name': n, 'item': SITE + (u if u != '/' else '/')} for i, (n, u) in enumerate(items)]}

def ld(graph):
    data = {'@context': 'https://schema.org', '@graph': graph}
    return '<script type="application/ld+json">' + json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/') + '</script>'

def cta_band(title='Discuss an Engagement', text='Initial inquiries are reviewed by TDSC leadership. Describe the matter in general terms; we will respond to arrange a confidential consultation and assess scope, jurisdiction and authorization before any work begins.', btn2=('Explore Our Capabilities', CONSULT)):
    return f'''<section class="tdsc-cta tdsc-center" aria-labelledby="tdsc-cta-h"><div class="tdsc-wrap tdsc-narrow tdsc-rv">
{seal_svg('tdsc-cta__seal', label='TDSC seal')}
<p class="tdsc-eyebrow">Thiel Detective Service Company</p>
<h2 id="tdsc-cta-h">{e(title)}</h2><p class="tdsc-lede">{e(text)}</p>
<div class="tdsc-btns"><a class="tdsc-btn tdsc-btn--brass" href="/contact">Request a Consultation {ARROW}</a><a class="tdsc-btn tdsc-btn--ghost" href="{btn2[1]}">{e(btn2[0])}</a></div>
<div class="tdsc-cta__contact"><span>Headquarters: Nashville, Tennessee</span><a href="tel:{PHONE_TEL}">{PHONE_DISPLAY}</a><a href="mailto:{EMAIL}">{EMAIL}</a></div>
</div></section>'''

def page_wrap(slug, body, schema):
    return (f'<!-- TDSC PAGE: {slug} | generated by TDSC build system v1.0 — edit source, not this block -->\n'
            f'<div class="tdsc-page" data-tdsc-page="{slug}">\n{body}\n</div>\n{ld(schema)}\n')

def webpage_ld(url, name, desc, typ='WebPage', crumb=None, extra=None):
    d = {'@type': typ, '@id': SITE + url + '#webpage', 'url': SITE + url, 'name': name, 'description': desc,
         'isPartOf': {'@id': SITE + '/#website'}, 'about': {'@id': ORG_ID}, 'publisher': {'@id': ORG_ID}, 'inLanguage': 'en-US'}
    if crumb: d['breadcrumb'] = crumb
    if extra: d.update(extra)
    return d
