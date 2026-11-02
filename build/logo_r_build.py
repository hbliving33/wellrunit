"""Builds logo-r.html: the WellRunIT wordmark with the R in "Run" tipped forward, like it's in stride.
Run from the repo root:  python3 build/logo_r_build.py"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
G, S, SKY, W, M = '#1b2430', '#2f5580', '#b9cde3', '#fff', '#7f9cbd'

# Each option returns the wordmark HTML for (accent, core, soft) colors.
def wm(inner, a):
    return f'<span class="wm" style="color:{a}">{inner}</span>'

def lines(col, w=1):   # speed lines that sit just behind the R
    return f'<span class="sl" style="--c:{col};--w:{w}"><i></i><i></i><i></i></span>'

OPTS = [
 ('R tipped forward a little', lambda a,c,m: wm(f'Well<b style="color:{c}"><span class="tip" style="--k:-12deg">R</span>un</b><i style="color:{a}">IT</i>', a)),
 ('R tipped forward more', lambda a,c,m: wm(f'Well<b style="color:{c}"><span class="tip" style="--k:-20deg">R</span>un</b><i style="color:{a}">IT</i>', a)),
 ('R tipped forward, in slate blue', lambda a,c,m: wm(f'Well<b style="color:{c}"><span class="tip" style="--k:-16deg;color:{a}">R</span>un</b><i style="color:{a}">IT</i>', a)),
 ('R tipped forward with speed lines behind it', lambda a,c,m: wm(f'Well<b class="sp" style="color:{c}">{lines(m)}<span class="tip" style="--k:-16deg">R</span>un</b><i style="color:{a}">IT</i>', a)),
 ('R tipped forward with slate blue speed lines', lambda a,c,m: wm(f'Well<b class="sp" style="color:{c}">{lines(a)}<span class="tip" style="--k:-16deg">R</span>un</b><i style="color:{a}">IT</i>', a)),
 ('Whole word "Run" leaning forward', lambda a,c,m: wm(f'Well<b class="tip" style="--k:-14deg;color:{c}">Run</b><i style="color:{a}">IT</i>', a)),
 ('"Run" leaning forward with speed lines', lambda a,c,m: wm(f'Well<b class="sp" style="color:{c}">{lines(m)}<span class="tip" style="--k:-14deg">Run</span></b><i style="color:{a}">IT</i>', a)),
 ('R tipped forward, "Run" and "IT" both leaning', lambda a,c,m: wm(f'Well<b class="tip" style="--k:-14deg;color:{c}">Run</b><i class="tip" style="--k:-14deg;color:{a}">IT</i>', a)),
 ('R tipped forward, a little lift off the line', lambda a,c,m: wm(f'Well<b style="color:{c}"><span class="tip" style="--k:-16deg;--y:-.06em">R</span>un</b><i style="color:{a}">IT</i>', a)),
 ('R tipped forward, one speed line under the whole name', lambda a,c,m: wm(f'Well<b style="color:{c}"><span class="tip" style="--k:-16deg">R</span>un</b><i style="color:{a}">IT</i><span class="ul" style="--c:{a}"></span>', a)),
 ('R tipped forward, slate blue speed lines, slate blue R', lambda a,c,m: wm(f'Well<b class="sp" style="color:{c}">{lines(a)}<span class="tip" style="--k:-18deg;color:{a}">R</span>un</b><i style="color:{a}">IT</i>', a)),
 ('"Run" underlined', lambda a,c,m: wm(f'Well<b style="color:{c}"><span class="und" style="--c:{a}">Run</span></b><i style="color:{a}">IT</i>', a)),
 ('Just the R underlined', lambda a,c,m: wm(f'Well<b style="color:{c}"><span class="und" style="--c:{a}">R</span>un</b><i style="color:{a}">IT</i>', a)),
 ('R tipped forward with "Run" underlined', lambda a,c,m: wm(f'Well<b style="color:{c}"><span class="und" style="--c:{a}"><span class="tip" style="--k:-16deg">R</span>un</span></b><i style="color:{a}">IT</i>', a)),
 ('R tipped forward and just the R underlined', lambda a,c,m: wm(f'Well<b style="color:{c}"><span class="und" style="--c:{a}"><span class="tip" style="--k:-16deg">R</span></span>un</b><i style="color:{a}">IT</i>', a)),
 ('Today\'s wordmark, for comparison (nothing tipped)', lambda a,c,m: wm(f'Well<b style="color:{c}">Run</b><i style="color:{a}">IT</i>', a)),
]

cards = ''
for n, (name, fn) in enumerate(OPTS, 1):
    cards += f'''<div class="opt"><div class="num">{n}</div><div class="name">{name}</div>
<div class="row light">{fn(S, G, M)}</div><div class="row dark">{fn(SKY, W, M)}</div></div>'''

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Forward R options | Well Run IT</title>
<style>
@font-face{{font-family:Inter;font-weight:400;src:url(assets/fonts/inter-latin-400-normal.woff2) format("woff2")}}
@font-face{{font-family:Inter;font-weight:800;src:url(assets/fonts/inter-latin-800-normal.woff2) format("woff2")}}
body{{margin:0;background:#eef0f3;color:{G};font:400 16px/1.5 Inter,system-ui,sans-serif}}
.wrap{{max-width:1240px;margin:0 auto;padding:40px 20px 80px}}
h1{{font-size:34px;letter-spacing:-.02em;margin:0 0 8px}}
p.lead{{margin:0 0 28px;color:#3c4a5c;max-width:820px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:16px}}
.opt{{background:#fff;border:1px solid #c9d0da;border-top:4px solid {S};border-radius:16px;padding:18px;position:relative}}
.num{{position:absolute;top:14px;right:16px;font-weight:800;font-size:22px;color:{S}}}
.name{{font-size:14px;color:#3c4a5c;margin-bottom:12px;padding-right:44px;min-height:42px}}
.row{{display:flex;align-items:center;padding:22px 20px;border-radius:10px}}
.row.light{{background:#eef0f3}} .row.dark{{background:{G};margin-top:8px}}
.wm{{position:relative;font:400 40px/1 Inter;letter-spacing:-.03em;white-space:nowrap}}
.wm b{{font-weight:800;position:relative;display:inline-block}} .wm i{{font-style:normal;font-weight:800;margin-left:.03em;letter-spacing:0;display:inline-block}}
.tip{{display:inline-block;transform:translateY(var(--y,0)) skewX(var(--k));transform-origin:50% 100%}}
.wm b.sp{{margin-left:.42em}}
.sl{{position:absolute;left:-.4em;top:.2em;display:flex;flex-direction:column;gap:.11em;align-items:flex-end}}
.sl i{{display:block;height:.075em;border-radius:1em;background:var(--c);margin:0}}
.sl i:nth-child(1){{width:.32em}} .sl i:nth-child(2){{width:.22em}} .sl i:nth-child(3){{width:.14em}}
.und{{display:inline-block;position:relative}}.und::after{{content:'';position:absolute;left:.02em;right:.02em;bottom:-.14em;height:.08em;border-radius:1em;background:var(--c)}}
.ul{{position:absolute;left:0;right:0;bottom:-.2em;height:.07em;border-radius:1em;background:linear-gradient(90deg,transparent,var(--c) 40%)}}
</style></head><body><div class="wrap">
<h1>Forward R options</h1>
<p class="lead">The R in "Run" tipped forward, like it's in stride.  All of them use the same font as today's logo (Inter); only the lean, lines or underline change.  Each is shown on light (header) and dark (footer).  The last one is today's wordmark for comparison.  Any of these can be paired with an icon from <a href="logo-icons.html">the icon page</a>, or stand alone with no icon.  Tell me the number.</p>
<div class="grid">{cards}</div></div></body></html>'''
(ROOT / 'logo-r.html').write_text(html)
print(f'built logo-r.html with {len(OPTS)} options')
