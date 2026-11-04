"""Country outline plates from Natural Earth (datasets/geo-countries, public domain)."""
import json, math

def _rings(geom):
    if geom['type'] == 'Polygon':
        return [geom['coordinates'][0]]
    return [p[0] for p in geom['coordinates']]

def _area(r):
    a = 0
    for i in range(len(r) - 1):
        a += r[i][0] * r[i + 1][1] - r[i + 1][0] * r[i][1]
    return abs(a) / 2

def load_outlines(path):
    gj = json.load(open(path))
    out = {}
    for f in gj['features']:
        cc = f['properties'].get('ISO3166-1-Alpha-2')
        if cc and cc != '-99':
            out[cc] = _rings(f['geometry'])
    return out

def plate(rings, W=560, H=420, pad=34, markers=(), cap=None):
    """Return (svg_inner_path_d, project_fn, bbox) for a set of lon/lat rings."""
    rings = [r for r in rings if len(r) > 3]
    # antimeridian: if spread > 180, shift western lons
    lons = [p[0] for r in rings for p in r]
    shift = (max(lons) - min(lons)) > 180
    def norm(lon): return lon + 360 if (shift and lon < 0) else lon
    rings = [[(norm(x), y) for x, y in r] for r in rings]
    big = max(_area(r) for r in rings)
    core = [r for r in rings if _area(r) >= big * 0.04] or rings
    xs = [p[0] for r in core for p in r]; ys = [p[1] for r in core for p in r]
    minx, maxx, miny, maxy = min(xs), max(xs), min(ys), max(ys)
    midlat = (miny + maxy) / 2
    kx = math.cos(math.radians(midlat))
    w = max((maxx - minx) * kx, 0.05); h = max(maxy - miny, 0.05)
    s = min((W - 2 * pad) / w, (H - 2 * pad) / h)
    ox = (W - w * s) / 2; oy = (H - h * s) / 2
    def P(lon, lat):
        lon = norm(lon)
        return ox + (lon - minx) * kx * s, oy + (maxy - lat) * s
    d = []
    for r in rings:
        pts = [P(x, y) for x, y in r]
        xs_ = [q[0] for q in pts]; ys_ = [q[1] for q in pts]
        if max(xs_) < 0 or min(xs_) > W or max(ys_) < 0 or min(ys_) > H:
            continue
        if (max(xs_) - min(xs_)) < 1.6 and (max(ys_) - min(ys_)) < 1.6:
            continue  # sub-pixel islet
        keep = [pts[0]]
        for q in pts[1:]:
            if abs(q[0] - keep[-1][0]) + abs(q[1] - keep[-1][1]) >= 1.8:
                keep.append(q)
        if len(keep) < 3: continue
        d.append('M' + 'L'.join(f'{x:.0f},{y:.0f}' for x, y in keep) + 'Z')
    return ''.join(d), P, (minx, maxx, miny, maxy)

def graticule(P, bbox, W, H, every=None):
    minx, maxx, miny, maxy = bbox
    span = max(maxx - minx, maxy - miny)
    every = every or (1 if span < 6 else 2 if span < 14 else 5 if span < 35 else 10)
    lines = []
    lon = math.floor(minx / every) * every
    while lon <= maxx + every:
        a = P(lon, miny - every); b = P(lon, maxy + every)
        lines.append(f'M{a[0]:.1f},{a[1]:.1f}L{b[0]:.1f},{b[1]:.1f}')
        lon += every
    lat = math.floor(miny / every) * every
    while lat <= maxy + every:
        a = P(minx - every, lat); b = P(maxx + every, lat)
        lines.append(f'M{a[0]:.1f},{a[1]:.1f}L{b[0]:.1f},{b[1]:.1f}')
        lat += every
    return ''.join(lines), every
