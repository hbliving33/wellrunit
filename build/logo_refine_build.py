"""Builds logo-refine.html: refinements of the two custom directions Eric liked on Nov 1 2026 —
number 5 (the R in stride, tipped forward with motion marks) and number 8 (the W drawn as two joined check marks).
Uses the glyph and layout helpers from logo_custom_build.py.  Run from the repo root:  python3 build/logo_refine_build.py"""
import importlib.util, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('lc', ROOT / 'build' / 'logo_custom_build.py'); lc = importlib.util.module_from_spec(spec); spec.loader.exec_module(lc)
G, S, SKY, W, M = lc.G, lc.S, lc.SKY, lc.W, lc.M

def R_stride(lean=14, marks=2, mcol='a', taper=False, long=1.0):
    """R tipped forward with motion marks in the gap before it.  Returns (draw function, glyph width)."""
    import math
    t = math.tan(math.radians(lean))
    ys = [26, 46] if marks == 2 else [20, 38, 56]
    lens = [L * long for L in ([22, 15] if marks == 2 else [22, 16, 10])]
    shift = max(t * 100, max(t * y + 8 + L for y, L in zip(ys, lens))) + 12   # 12 units of air after the l in Well
    def fn(a, c):
        col = {'a': a, 'c': c, 'm': M}[mcol]
        g = f'<g transform="skewX({-lean}) translate({shift:.1f} 0)">{lc.R_base(c)}{lc.R_leg(c)}</g>'
        out = ''
        for y, L in zip(ys, lens):
            x1 = shift - t * (y + 4.5) - 7; x0 = x1 - L      # end just behind the R's leaning stem
            if taper:
                out += f'<path d="M{x0:.1f} {y+4.5}L{x1:.1f} {y}v9z" fill="{col}"/>'
            else:
                out += f'<rect x="{x0:.1f}" y="{y}" width="{L:.1f}" height="9" rx="4.5" fill="{col}"/>'
        return out + g
    return fn, round(shift + 66 - t * 20)

def W_checks(sw=11, two_tone=False, mid=26, first=44, tall=0, col='a'):
    """W as two check marks joined in one stroke.  mid = height of the middle peak, first = where the first (short) stroke starts."""
    def fn(a, c):
        cA = {'a': a, 'c': c}[col]
        cB = c if two_tone else cA
        top = -tall
        p1 = f'M5 {first}L22 96L50 {mid}'
        p2 = f'M50 {mid}L68 96L106 {top}'
        return (f'<path d="{p1}" fill="none" stroke="{cA}" stroke-width="{sw}" stroke-linejoin="miter" stroke-linecap="butt"/>'
                f'<path d="{p2}" fill="none" stroke="{cB if two_tone else cA}" stroke-width="{sw}" stroke-linejoin="miter" stroke-linecap="butt"/>')
    return fn

R_OPTS = [
 ('Number 5 as it was: 14 degree lean, two slate marks', R_stride()),
 ('Less lean (10 degrees)', R_stride(lean=10)),
 ('More lean (18 degrees)', R_stride(lean=18)),
 ('Three marks', R_stride(marks=3)),
 ('Tapered marks, like speed streaks', R_stride(taper=True)),
 ('Tapered, three marks', R_stride(marks=3, taper=True)),
 ('Light slate marks (quieter)', R_stride(mcol='m')),
 ('Graphite marks, same color as the R', R_stride(mcol='c')),
 ('Longer marks', R_stride(long=1.5)),
 ('Shorter marks, more lean', R_stride(lean=18, long=.7)),
]
W_OPTS = [
 ('Number 8 as it was', W_checks()),
 ('Heavier stroke', W_checks(sw=14)),
 ('Second check rises above the other letters', W_checks(tall=12)),
 ('Higher middle peak (reads more like a W)', W_checks(mid=12)),
 ('Lower middle peak (reads more like two checks)', W_checks(mid=40)),
 ('Shorter first stroke, crisper check', W_checks(first=58)),
 ('Two-tone: first check slate, second graphite', W_checks(two_tone=True)),
 ('Graphite W, rest of "Well" slate', W_checks(col='c')),
 ('Heavier, second check rising above', W_checks(sw=14, tall=12)),
 ('Higher middle peak, second check rising above', W_checks(mid=12, tall=12)),
]

def add_glyph(name, fn, width):
    lc.GLYPHS[name] = (width, fn)

body, n = '', 0
for title, opts, kind in (('Number 5: the R in stride', R_OPTS, 'R'), ('Number 8: the W as two check marks', W_OPTS, 'W')):
    body += f'<h2>{title}</h2><div class="grid">'
    for name, fn in opts:
        n += 1
        g = f'opt{n}'
        if kind == 'R': fn, width = fn
        else: width = 110
        add_glyph(g, fn, width)
        parts = ['w:Well', f'g:{g}', 'r:un', 'i:IT'] if kind == 'R' else [f'g:{g}', 'w:ell', 'r:Run', 'i:IT']
        w, f = lc.GLYPHS[g]
        mono = lambda a, c, sz, w=w, f=f: f'<svg viewBox="-10 -16 {w+20} 126" height="{sz}" aria-hidden="true" overflow="visible">{f(a, c)}</svg>'
        body += (f'<div class="opt"><div class="num">{n}</div><div class="name">{name}</div>'
                 f'<div class="row light">{lc.logo(parts, S, G)}</div><div class="row dark">{lc.logo(parts, SKY, W)}</div>'
                 f'<div class="small">{mono(S, G, 30)}{mono(S, G, 16)}<span>Alone, at tab and phone size</span></div></div>')
    body += '</div>'

html = (ROOT / 'logo-custom.html').read_text()
head = html[:html.index('<body>')].replace('Custom logo options', 'Logo refinements').replace(
    '</style>', '.small{display:flex;align-items:center;gap:12px;margin-top:12px;font-size:13px;color:#6b7787}</style>')
out = head + f'''<body><div class="wrap">
<h1>Logo refinements</h1>
<p class="lead">Variations on your two picks from <a href="logo-custom.html">the custom page</a>: number 5 (the R in stride) and number 8 (the W as two check marks).  Same font and spacing as the live site.  Each also shows the custom letter alone at tab and phone size.  Tell me the number.</p>
{body}</div></body></html>'''
(ROOT / 'logo-refine.html').write_text(out)
print(f'built logo-refine.html with {n} options')
