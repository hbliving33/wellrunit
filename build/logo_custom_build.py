"""Builds logo-custom.html: custom letterform logos for Well Run IT.  No stock icons:
the idea is drawn into the letters themselves (the R, the W, the IT), so it's one element, never a line plus an icon.
Spacing matches the live site's wordmark exactly (IT sits .03em after Run).  Same font (Inter) for every letter that isn't custom-drawn.
Run from the repo root:  python3 build/logo_custom_build.py"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
G, S, SKY, W, M = '#1b2430', '#2f5580', '#b9cde3', '#fff', '#7f9cbd'

# ---------- custom glyphs, drawn on a 100-unit cap height (baseline at y=100) ----------
# Heavy R matches Inter 800 (stem about 21 units).  Light W matches Inter 400 (stem about 11 units).
def R_base(c):
    return (f'<rect x="0" y="0" width="21" height="100" fill="{c}"/>'
            f'<path d="M10 10.5H39a22.5 22.5 0 010 45H10" fill="none" stroke="{c}" stroke-width="21"/>')

def R_leg(c):
    return f'<path d="M27 56h22l21 44H47z" fill="{c}"/>'

GLYPHS = {
 # R variations (width 72, extra width where the leg runs on)
 'R':          (72,  lambda a,c: R_base(c) + R_leg(c)),
 'R_check':    (100, lambda a,c: R_base(c) + f'<path d="M29 57l22 36L90 30" fill="none" stroke="{a}" stroke-width="18" stroke-linejoin="miter"/>'),
 'R_check_c':  (100, lambda a,c: R_base(c) + f'<path d="M29 57l22 36L90 30" fill="none" stroke="{c}" stroke-width="18" stroke-linejoin="miter"/>'),
 'R_arrowleg': (92,  lambda a,c: R_base(c) + f'<path d="M27 56h22l43 44H66z" fill="{a}"/>'),
 'R_ring':     (74,  lambda a,c: f'<rect x="0" y="0" width="21" height="100" fill="{c}"/><circle cx="38" cy="31" r="21" fill="none" stroke="{a}" stroke-width="19"/>' + R_leg(c)),
 'R_stride':   (86,  lambda a,c: f'<g transform="skewX(-14) translate(25 0)">' + R_base(c) + R_leg(c) + '</g>'
                                  + f'<rect x="0" y="30" width="12" height="6" rx="3" fill="{a}"/><rect x="4" y="46" width="9" height="6" rx="3" fill="{a}"/>'),
 'R_steps':    (72,  lambda a,c: f'<rect x="0" y="0" width="21" height="100" fill="{c}"/>'
                                  f'<rect x="0" y="0" width="50" height="19" fill="{c}"/><rect x="0" y="40" width="50" height="19" fill="{c}"/><rect x="44" y="0" width="17" height="59" rx="0" fill="{c}"/>'
                                  + f'<path d="M27 59h22l21 41H47z" fill="{a}"/>'),
 'R_light':    (72,  lambda a,c: R_base(c) + R_leg(c) + f'<circle cx="38" cy="33" r="9.5" fill="{a}"/>'),
 # W variations (light weight, width 112)
 'W_checks':   (110, lambda a,c: f'<path d="M5 44l17 52L50 26l18 70L106 0" fill="none" stroke="{a}" stroke-width="11" stroke-linejoin="miter"/>'),
 'W_arrow':    (116, lambda a,c: f'<path d="M4 0l22 96L50 20l24 76L106 2" fill="none" stroke="{a}" stroke-width="11" stroke-linejoin="miter"/><path d="M90 2h17v17" fill="none" stroke="{a}" stroke-width="11" stroke-linejoin="miter"/>'),
 # IT variations (heavy)
 'IT_arrow':   (96,  lambda a,c: f'<rect x="0" y="0" width="21" height="100" fill="{a}"/><rect x="58" y="19" width="21" height="81" fill="{a}"/><path d="M30 9.5h56" stroke="{a}" stroke-width="19"/><path d="M80-6l16 15.5L80 25" fill="none" stroke="{a}" stroke-width="10" stroke-linejoin="miter"/>'),
 'IT_light':   (84,  lambda a,c: f'<rect x="0" y="26" width="21" height="74" fill="{a}"/><circle cx="10.5" cy="9" r="9" fill="{c}"/><rect x="30" y="0" width="54" height="19" fill="{a}"/><rect x="46.5" y="0" width="21" height="100" fill="{a}"/>'),
}

def glyph(name, a, c):
    w, fn = GLYPHS[name]
    return f'<svg class="gl" viewBox="0 0 {w} 100" style="width:{w*0.727/100:.4f}em" aria-hidden="true" overflow="visible">{fn(a, c)}</svg>'

# A logo is a list of parts: plain text in Inter (light "Well", heavy "un"/"Run", heavy "IT") or a custom glyph.
def logo(parts, a, c, lean=0):
    out = ''
    for p in parts:
        if p.startswith('g:'):
            out += glyph(p[2:], a, c)
        elif p.startswith('w:'):
            out += f'<span style="font-weight:400;color:{a}">{p[2:]}</span>'
        elif p.startswith('r:'):
            out += f'<b style="color:{c}">{p[2:]}</b>'
        elif p.startswith('i:'):
            out += f'<b style="color:{a};margin-left:.03em">{p[2:]}</b>'
        elif p == 'gap':
            out += '<span style="margin-left:.03em"></span>'
    sk = f' style="display:inline-block;transform:skewX({lean}deg);transform-origin:50% 100%"' if lean else ''
    return f'<span class="wm"><span{sk}>{out}</span></span>'

OPTS = [
 ('In the R', [
   ('The R\'s leg becomes a check mark, in slate blue', ['w:Well', 'g:R_check', 'r:un', 'i:IT']),
   ('The R\'s leg becomes a check mark, all graphite', ['w:Well', 'g:R_check_c', 'r:un', 'i:IT']),
   ('The R\'s leg kicks long and forward, in slate blue', ['w:Well', 'g:R_arrowleg', 'r:un', 'i:IT']),
   ('The R\'s bowl is a ring (the circle from icon 1, built into the letter)', ['w:Well', 'g:R_ring', 'r:un', 'i:IT']),
   ('The R in stride: tipped forward with two small motion marks', ['w:Well', 'g:R_stride', 'r:un', 'i:IT']),
   ('The R built like a server rack: square bowl, two rails, slate blue leg', ['w:Well', 'g:R_steps', 'r:un', 'i:IT']),
   ('A slate blue status light inside the R', ['w:Well', 'g:R_light', 'r:un', 'i:IT']),
 ]),
 ('In the W', [
   ('The W drawn as two check marks joined in one stroke', ['g:W_checks', 'w:ell', 'r:Run', 'i:IT']),
   ('The W\'s last stroke rises into an arrow', ['g:W_arrow', 'w:ell', 'r:Run', 'i:IT']),
 ]),
 ('In the IT', [
   ('The T\'s crossbar points forward like an arrow', ['w:Well', 'r:Run', 'gap', 'g:IT_arrow']),
   ('The I\'s dot is a status light (graphite, "on")', ['w:Well', 'r:Run', 'gap', 'g:IT_light']),
 ]),
 ('Two ideas together (still one element, no icon, no line)', [
   ('W as two checks, and the R\'s leg as a check', ['g:W_checks', 'w:ell', 'g:R_check', 'r:un', 'i:IT']),
   ('R\'s leg as a check, and the T pointing forward', ['w:Well', 'g:R_check', 'r:un', 'gap', 'g:IT_arrow']),
 ]),
]

MONOS = [   # standalone marks for the browser tab and phone icon, built from the same letters
 ('R with the check-mark leg', 'R_check'),
 ('W as two check marks', 'W_checks'),
 ('R with the ring bowl', 'R_ring'),
 ('R in stride', 'R_stride'),
]

body, n = '', 0
for section, items in OPTS:
    body += f'<h2>{section}</h2><div class="grid">'
    for name, parts in items:
        n += 1
        body += (f'<div class="opt"><div class="num">{n}</div><div class="name">{name}</div>'
                 f'<div class="row light">{logo(parts, S, G)}</div><div class="row dark">{logo(parts, SKY, W)}</div></div>')
    body += '</div>'
body += '<h2>The same letters as a standalone mark (browser tab, phone icon, social profile)</h2><div class="grid">'
for name, g in MONOS:
    n += 1
    w, fn = GLYPHS[g]
    svg = lambda a, c, sz: f'<svg viewBox="-8 -8 {w+16} 116" height="{sz}" aria-hidden="true" overflow="visible">{fn(a, c)}</svg>'
    body += (f'<div class="opt"><div class="num">{n}</div><div class="name">{name}</div>'
             f'<div class="row light mono">{svg(S, G, 56)}{svg(S, G, 30)}{svg(S, G, 16)}</div><div class="row dark mono">{svg(SKY, W, 56)}{svg(SKY, W, 30)}{svg(SKY, W, 16)}</div></div>')
body += '</div>'

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Custom logo options | Well Run IT</title>
<style>
@font-face{{font-family:Inter;font-weight:400;src:url(assets/fonts/inter-latin-400-normal.woff2) format("woff2")}}
@font-face{{font-family:Inter;font-weight:800;src:url(assets/fonts/inter-latin-800-normal.woff2) format("woff2")}}
body{{margin:0;background:#eef0f3;color:{G};font:400 16px/1.5 Inter,system-ui,sans-serif}}
.wrap{{max-width:1240px;margin:0 auto;padding:40px 20px 80px}}
h1{{font-size:34px;letter-spacing:-.02em;margin:0 0 8px}} h2{{font-size:20px;margin:40px 0 14px}}
p.lead{{margin:0;color:#3c4a5c;max-width:860px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:16px}}
.opt{{background:#fff;border:1px solid #c9d0da;border-top:4px solid {S};border-radius:16px;padding:18px;position:relative}}
.num{{position:absolute;top:14px;right:16px;font-weight:800;font-size:22px;color:{S}}}
.name{{font-size:14px;color:#3c4a5c;margin-bottom:12px;padding-right:44px;min-height:42px}}
.row{{display:flex;align-items:center;padding:26px 22px;border-radius:10px;overflow:visible}}
.row.light{{background:#eef0f3}} .row.dark{{background:{G};margin-top:8px}}
.row.mono{{gap:22px}}
.wm{{font:400 44px/1 Inter;letter-spacing:-.03em;white-space:nowrap}}
.wm b{{font-weight:800}}
.gl{{display:inline-block;height:.727em;vertical-align:baseline;overflow:visible}}
</style></head><body><div class="wrap">
<h1>Custom logo options</h1>
<p class="lead">No stock icons.  Each idea is drawn into the letters themselves, so the logo is one piece, with no separate icon and no underline.  Spacing matches the live site exactly, and every letter that isn't custom-drawn is the same font as today.  The last section shows the custom letter on its own, for the browser tab and phone icon.  Tell me the number.</p>
{body}</div></body></html>'''
(ROOT / 'logo-custom.html').write_text(html)
print(f'built logo-custom.html with {n} options')
