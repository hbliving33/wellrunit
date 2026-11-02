"""Builds logo-combo.html: combinations Eric asked for on Nov 1 2026 from logo-r.html —
the underline from number 10, the spacing from number 8, and the upright letters from number 16 —
then the best of those paired with icons 1, 10 and 19 from logo-icons.html.
Run from the repo root:  python3 build/logo_combo_build.py"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
G, S, SKY, W, M = '#1b2430', '#2f5580', '#b9cde3', '#fff', '#7f9cbd'

def st(c, w=3.4): return f'fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'
ICONS = {   # the three picked from logo-icons.html, same drawings
 1:  lambda a,c,m: f'<circle cx="20" cy="20" r="16" {st(c,3.4)}/><path d="M12.5 20.5l5 5L28 15" {st(a,4.4)}/>',
 10: lambda a,c,m: f'<path d="M3 15h7M1 21h6" {st(m,3)}/><path d="M11 22l7 7L35 12" {st(a,5)}/><path d="M25 11.5h10.5V22" {st(a,5)}/>',
 19: lambda a,c,m: f'<rect x="4" y="28" width="32" height="7" rx="2" fill="{c}"/><rect x="13" y="19" width="23" height="7" rx="2" fill="{c}"/><rect x="22" y="10" width="14" height="7" rx="2" fill="{c}"/><path d="M4 22l9-8 6 4L31 5M24 5h7v7" {st(a,3)}/>',
}
ICON_NAMES = {1: 'check inside a ring', 10: 'check-to-arrow with speed lines', 19: 'stepped rack with arrow'}

# Wordmark settings: lean of "Run" and "IT", gap between Run and IT, underline style and what it sits under.
def wordmark(a, c, lean=0, gap=None, ul='fade', under='all', ulw='.07em', size=40):
    gap = gap or ('.03em' if not lean else f'{.03 + abs(lean) * .006:.3f}em')
    k = f'transform:skewX({lean}deg);transform-origin:50% 100%;' if lean else ''
    line = '' if not ul else (f'<span class="ul" style="--c:{a};height:{ulw};' + ('background:var(--c);' if ul == 'solid' else '') + '"></span>')
    run_it = f'<b style="color:{c};{k}">Run</b><i style="color:{a};margin-left:{gap};{k}">IT</i>'
    if under == 'runit':
        return f'<span class="wm" style="color:{a};font-size:{size}px">Well<span class="grp">{run_it}{line}</span></span>'
    return f'<span class="wm" style="color:{a};font-size:{size}px">Well{run_it}{line}</span>'

COMBOS = [
 ('Upright letters (16) with the underline from 10', dict()),
  ('"Run" and "IT" leaning a little, underline from 10', dict(lean=-8)),
 ('"Run" and "IT" leaning like 8, underline from 10', dict(lean=-14)),
 ('Upright, underline from 10 under "RunIT" only', dict(under='runit')),
 ('Leaning a little, underline under "RunIT" only', dict(lean=-8, under='runit')),
 ('Upright, solid slate underline (no fade)', dict(ul='solid')),
 ('Upright, heavier fading underline', dict(ulw='.11em')),
]

def row(fn, dark):
    a, c = (SKY, W) if dark else (S, G)
    return f'<div class="row {"dark" if dark else "light"}">{fn(a, c)}</div>'

cards = ''
for n, (name, kw) in enumerate(COMBOS, 1):
    fn = lambda a, c, kw=kw: wordmark(a, c, **kw)
    cards += f'<div class="opt"><div class="num">{n}</div><div class="name">{name}</div>{row(fn, False)}{row(fn, True)}</div>'

pairs, n = '', len(COMBOS)
ICON_STYLES = [('upright like 16', dict()), ('leaning a little', dict(lean=-8)), ('leaning like 8', dict(lean=-14))]
for sname, kw in ICON_STYLES:   # icon OR underline, never both: no underline here
    kw = dict(kw, ul=None)
    for ic in (1, 10, 19):
        n += 1
        def fn(a, c, kw=kw, ic=ic):
            m = M
            return f'<svg viewBox="0 0 40 40" width="40" height="40" aria-hidden="true" style="flex:none">{ICONS[ic](a, c, m)}</svg>' + wordmark(a, c, size=32, **kw)
        pairs += f'<div class="opt"><div class="num">{n}</div><div class="name">Icon {ic} ({ICON_NAMES[ic]}), letters {sname}, no underline</div>{row(fn, False)}{row(fn, True)}</div>'

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Logo combinations | Well Run IT</title>
<style>
@font-face{{font-family:Inter;font-weight:400;src:url(assets/fonts/inter-latin-400-normal.woff2) format("woff2")}}
@font-face{{font-family:Inter;font-weight:800;src:url(assets/fonts/inter-latin-800-normal.woff2) format("woff2")}}
body{{margin:0;background:#eef0f3;color:{G};font:400 16px/1.5 Inter,system-ui,sans-serif}}
.wrap{{max-width:1240px;margin:0 auto;padding:40px 20px 80px}}
h1{{font-size:34px;letter-spacing:-.02em;margin:0 0 8px}} h2{{font-size:20px;margin:40px 0 14px}}
p.lead{{margin:0;color:#3c4a5c;max-width:840px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:16px}}
.opt{{background:#fff;border:1px solid #c9d0da;border-top:4px solid {S};border-radius:16px;padding:18px;position:relative}}
.num{{position:absolute;top:14px;right:16px;font-weight:800;font-size:22px;color:{S}}}
.name{{font-size:14px;color:#3c4a5c;margin-bottom:12px;padding-right:44px;min-height:42px}}
.row{{display:flex;align-items:center;gap:10px;padding:24px 20px;border-radius:10px}}
.row.light{{background:#eef0f3}} .row.dark{{background:{G};margin-top:8px}}
.wm{{position:relative;display:inline-block;font:400 40px/1 Inter;letter-spacing:-.03em;white-space:nowrap}}
.wm b{{font-weight:800;display:inline-block}} .wm i{{font-style:normal;font-weight:800;letter-spacing:0;display:inline-block}}
.grp{{position:relative;display:inline-block}}
.ul{{position:absolute;left:0;right:0;bottom:-.2em;border-radius:1em;background:linear-gradient(90deg,transparent,var(--c) 40%)}}
</style></head><body><div class="wrap">
<h1>Logo combinations</h1>
<p class="lead">From <a href="logo-r.html">the forward R page</a>: the underline from number 10, the lean from number 8 and the upright letters from number 16, mixed a few ways.  It's one or the other: the top section has the underline and no icon, and the bottom section has an icon (your picks 1, 10 and 19) and no underline.  Same font and the same letter spacing as the live site throughout.  Tell me the number.</p>
<h2>Underline, no icon</h2><div class="grid">{cards}</div>
<h2>Icon, no underline</h2><div class="grid">{pairs}</div>
</div></body></html>'''
(ROOT / 'logo-combo.html').write_text(html)
print(f'built logo-combo.html with {n} options')
