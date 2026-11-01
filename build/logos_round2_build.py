"""Builds logos.html, round two: variations on IT in a box, plus a few unboxed versions with a hair of space.
Run from the repo root:  python3 build/logos_build.py   (round one lives in logos-round1.html)"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
NAVY, STEEL, SKY, INK2 = '#0f1c2d', '#2f5d8a', '#8fb3d9', '#3c4a5c'

MARKS = {
 'pulse': '<path d="M2 12.5h5l2-4.5 3.5 9 2.5-6 1.5 1.5H22" fill="none" stroke="{c}" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/>',
 'gauge': '<path d="M3.5 16a8.5 8.5 0 0117 0" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/><path d="M12 16l5-5.2" stroke="{a}" stroke-width="2.4" stroke-linecap="round"/><circle cx="12" cy="16" r="2" fill="{c}"/>',
 'wcheck': '<path d="M2.5 9l4 8 4.5-8 4.5 8 6-12" fill="none" stroke="{c}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>',
 'status': '<circle cx="12" cy="12" r="9.5" fill="none" stroke="{c}" stroke-width="2"/><circle cx="12" cy="12" r="5" fill="{a}"/>',
 'bars': '<rect x="3" y="14" width="4" height="7" rx="1.2" fill="{c}"/><rect x="10" y="9.5" width="4" height="11.5" rx="1.2" fill="{c}"/><rect x="17" y="4" width="4" height="17" rx="1.2" fill="{a}"/>',
}
MNAME = {'pulse': 'pulse', 'gauge': 'gauge', 'wcheck': 'W check', 'status': 'status dot', 'bars': 'rising bars'}
def mark(name, dark):
    c, a = ('#fff', SKY) if dark else (NAVY, STEEL)
    return f'<svg viewBox="0 0 24 24" class="mk" aria-hidden="true">{MARKS[name].replace("{c}", c).replace("{a}", a)}</svg>'

# Each box style: (label, function(dark) -> css for the IT span, IT text color)
def box(dark, **o):
    bg = o.get('bg', SKY if dark else STEEL)
    fg = o.get('fg', NAVY if dark else '#fff')
    css = f"display:inline-block;background:{bg};color:{fg};border-radius:{o.get('r', '.2em')};padding:{o.get('pad', '.04em .14em .06em')};margin-left:{o.get('ml', '.07em')};font-size:{o.get('fs', '.86em')};vertical-align:{o.get('va', '.06em')};letter-spacing:0;line-height:1;{o.get('extra', '')}"
    return css

BOXES = {
 'tab':      ('Rounded tab (your pick)', lambda d: box(d)),
 'square':   ('Square corners', lambda d: box(d, r='.04em')),
 'pill':     ('Fully round pill', lambda d: box(d, r='1em', pad='.04em .3em .06em')),
 'soft':     ('Softer, larger corners', lambda d: box(d, r='.32em', pad='.06em .18em .08em')),
 'gap':      ('A little more space before the box', lambda d: box(d, ml='.14em')),
 'full':     ('Full height, same size as Run', lambda d: box(d, fs='1em', va='0', pad='0 .12em .02em')),
 'small':    ('Smaller, raised box', lambda d: box(d, fs='.7em', va='.32em', pad='.06em .14em .08em')),
 'baseline': ('Sits on the baseline', lambda d: box(d, va='0', pad='.06em .14em .04em')),
 'navy':     ('Navy box, light IT', lambda d: box(d, bg='#fff' if d else NAVY, fg=NAVY if d else SKY)),
 'skybox':   ('Light blue box, navy IT', lambda d: box(d, bg=SKY, fg=NAVY)),
 'outline':  ('Outline box', lambda d: box(d, bg='transparent', fg=SKY if d else STEEL, extra=f"box-shadow:inset 0 0 0 .07em {SKY if d else STEEL}")),
 'outfill':  ('Outline with a light fill', lambda d: box(d, bg='rgba(143,179,217,.18)' if d else '#e8eef5', fg=SKY if d else STEEL, extra=f"box-shadow:inset 0 0 0 .06em {SKY if d else STEEL}")),
 'slant':    ('Slanted box, forward motion', lambda d: box(d, extra='transform:skewX(-10deg)')),
 'tag':      ('Tag shape pointing forward', lambda d: box(d, r='.12em', pad='.04em .32em .06em .14em', extra='clip-path:polygon(0 0,82% 0,100% 50%,82% 100%,0 100%)')),
 'notch':    ('Clipped corner', lambda d: box(d, r='0', extra='clip-path:polygon(0 0,100% 0,100% 72%,80% 100%,0 100%)')),
 'key':      ('Keyboard key', lambda d: box(d, r='.16em', extra=f"box-shadow:0 .08em 0 {'#5a7fa6' if d else '#1d3d5e'}")),
 'shadow':   ('Offset outline behind', lambda d: box(d, extra=f"box-shadow:.09em .09em 0 0 {'#fff' if d else NAVY}")),
 'dot':      ('Status dot on the corner', lambda d: box(d, extra=f"position:relative;background-image:radial-gradient(circle at 88% 16%,{'#fff' if d else SKY} .07em,transparent .08em)")),
 'under':    ('Box with an underline under Well Run', lambda d: box(d)),
 'gradient': ('Steel to light blue', lambda d: box(d, bg=f'linear-gradient(135deg,{STEEL},{SKY})', fg='#fff')),
 'bracket':  ('Brackets instead of a box', None),
}

def word(style, dark, it_css, text='Well Run', weight=800, ls='-.035em', extra_outer=''):
    ink = '#fff' if dark else NAVY
    if style == 'onewell':
        lead = f'<span style="font-weight:400">Well</span><span style="font-weight:800">Run</span>'
    elif style == 'stack':
        lead = None
    else:
        lead = text
    it = f'<span style="{it_css}">IT</span>'
    if style == 'stack':
        return f'<span style="display:inline-flex;flex-direction:column;line-height:.95;font-weight:800;letter-spacing:{ls};color:{ink}"><span style="font-weight:500;font-size:.6em">Well</span><span>Run{it}</span></span>'
    return f'<span style="font-weight:{weight};letter-spacing:{ls};color:{ink};{extra_outer}">{lead}{it}</span>'

def unboxed(dark, space):
    acc = SKY if dark else STEEL
    return f'color:{acc};margin-left:{space};letter-spacing:0'

OPTIONS = [
 # (box key or None, wordmark style, mark or None, unboxed spacing, label override)
 ('tab', 'bold', None, None), ('square', 'bold', None, None), ('pill', 'bold', None, None), ('soft', 'bold', None, None),
 ('gap', 'bold', None, None), ('full', 'bold', None, None), ('small', 'bold', None, None),
 ('baseline', 'bold', None, None), ('navy', 'bold', None, None), ('skybox', 'bold', None, None), ('outline', 'bold', None, None),
 ('outfill', 'bold', None, None), ('slant', 'bold', None, None), ('tag', 'bold', None, None), ('notch', 'bold', None, None),
 ('key', 'bold', None, None), ('shadow', 'bold', None, None), ('dot', 'bold', None, None), ('gradient', 'bold', None, None),
 ('under', 'bold', None, None), ('tab', 'caps', None, None), ('tab', 'lower', None, None), ('tab', 'onewell', None, None),
 ('tab', 'stack', None, None), ('tab', 'semibold', None, None), ('tab', 'bold', 'pulse', None), ('tab', 'bold', 'gauge', None),
 ('slant', 'bold', 'wcheck', None), ('square', 'caps', 'bars', None),
 (None, 'bold', None, '.035em'), (None, 'bold', None, '.06em'), (None, 'bold', 'pulse', '.05em'), (None, 'onewell', None, '.05em'),
 ('bracket', 'bold', None, None), (None, 'caps', 'status', '.08em'),
]

def lockup(opt, dark, size_cls=''):
    bk, st, mk, sp = opt
    if bk == 'bracket':
        acc = SKY if dark else STEEL
        it_css = f'color:{acc};margin-left:.04em;letter-spacing:0'
        ink = '#fff' if dark else NAVY
        w = f'<span style="font-weight:800;letter-spacing:-.035em;color:{ink}">Well Run<span style="color:{acc};font-weight:400;margin-left:.05em">[</span><span style="{it_css};margin-left:0">IT</span><span style="color:{acc};font-weight:400">]</span></span>'
    elif bk:
        it_css = BOXES[bk][1](dark)
        if st == 'caps':
            w = word(st, dark, it_css, text='WELL RUN', ls='.05em')
        elif st == 'lower':
            w = word(st, dark, it_css, text='well run')
        elif st == 'semibold':
            w = word(st, dark, it_css, weight=600, ls='-.025em')
        else:
            w = word(st, dark, it_css)
        if bk == 'under':
            line = SKY if dark else STEEL
            w = f'<span style="display:inline-block;border-bottom:.07em solid {line};padding-bottom:.08em">{w}</span>'
    else:
        it_css = unboxed(dark, sp)
        w = word(st, dark, it_css, text='WELL RUN', ls='.05em') if st == 'caps' else word(st, dark, it_css)
    m = mark(mk, dark) if mk else ''
    return f'<div class="lk {size_cls}">{m}<span class="wm">{w}</span></div>'

def fav(opt, dark):
    bk, st, mk, sp = opt
    if mk:
        return f'<span class="fav{" d" if dark else ""}">{mark(mk, dark)}</span>'
    css = BOXES[bk][1](dark) if bk and BOXES[bk][1] else f'color:{SKY if dark else STEEL}'
    return f'<span class="fav{" d" if dark else ""}"><span style="font:800 13px Inter;{css};margin:0;vertical-align:0">IT</span></span>'

def label(opt):
    bk, st, mk, sp = opt
    names = {'bold': 'bold', 'caps': 'all caps', 'lower': 'lowercase', 'onewell': 'light Well, heavy Run', 'stack': 'stacked', 'semibold': 'medium weight'}
    if bk == 'bracket': return 'Brackets instead of a box', 'IT set in light brackets'
    if bk:
        t = BOXES[bk][0]
        sub = f'Wordmark {names[st]}' + (f', with the {MNAME[mk]} mark' if mk else '')
        return t, sub
    return 'No box, a hair of space', f'IT in steel blue, wordmark {names[st]}' + (f', with the {MNAME[mk]} mark' if mk else '')


# ---------- round two, part two: other fonts, subtle color shifts, and a leaning IT ----------
FONTS = [('Manrope', 'manrope-latin-800', 800), ('Sora', 'sora-latin-700', 700), ('Space Grotesk', 'space-grotesk-latin-700', 700), ('Outfit', 'outfit-latin-700', 700),
         ('Lexend', 'lexend-latin-700', 700), ('Montserrat', 'montserrat-latin-800', 800), ('IBM Plex Sans', 'ibm-plex-sans-latin-700', 700), ('Archivo', 'archivo-latin-800', 800),
         ('Bricolage Grotesque', 'bricolage-grotesque-latin-800', 800), ('Poppins', 'poppins-latin-700', 700)]
FONT_CSS = ''.join(f"@font-face{{font-family:'{n}';font-weight:{w};font-display:swap;src:url(assets/fonts/{f}-normal.woff2) format('woff2')}}" for n, f, w in FONTS)
PALETTES = {
 'navy':     ('Navy and steel blue (current)', NAVY, STEEL, '#fff', SKY),
 'graphite': ('Graphite and slate blue', '#1b2430', '#3d5f85', '#fff', '#9bb6d3'),
 'midnight': ('Midnight and deep teal blue', '#0c1b2b', '#2d6475', '#fff', '#8cc1cc'),
 'charcoal': ('Charcoal and soft steel', '#22262b', '#4a6b8f', '#fff', '#a3bcd6'),
 'ink':      ('Ink and denim', '#101828', '#36557a', '#fff', '#9db3cf'),
 'slatebox': ('Navy with a slate box', NAVY, '#4b5d73', '#fff', '#a9b8c9'),
}
def lock2(font='Inter', weight=800, pal='navy', lean=0, boxlean=0, box=True, dark=False, ls='-.035em', size=''):
    _, ink, acc, boxfg, dacc = PALETTES[pal]
    ink_c = '#fff' if dark else ink
    acc_c = dacc if dark else acc
    fg = NAVY if dark else boxfg
    lean_css = f'transform:skewX({lean}deg);' if lean else ''
    if box:
        inner = f'<span style="display:inline-block;{lean_css}">IT</span>'
        it = (f'<span style="display:inline-block;background:{acc_c};color:{fg};border-radius:.2em;padding:.04em .14em .06em;margin-left:.07em;'
              f'font-size:.86em;vertical-align:.06em;letter-spacing:0;line-height:1;{f"transform:skewX({boxlean}deg);" if boxlean else ""}">{inner}</span>')
    else:
        it = f'<span style="display:inline-block;color:{acc_c};margin-left:.06em;letter-spacing:0;{lean_css}">IT</span>'
    return f'<div class="lk {size}"><span class="wm"><span style="font-family:\'{font}\',Inter,sans-serif;font-weight:{weight};letter-spacing:{ls};color:{ink_c}">Well Run{it}</span></span></div>'

def fav2(dark, **k):
    _, ink, acc, boxfg, dacc = PALETTES[k.get('pal', 'navy')]
    bg = dacc if dark else acc
    lean = k.get('lean', 0); bl = k.get('boxlean', 0)
    inner = f'<span style="display:inline-block;{f"transform:skewX({lean}deg)" if lean else ""}">IT</span>'
    return (f'<span class="fav{" d" if dark else ""}"><span style="font:{k.get("weight", 800)} 13px \'{k.get("font", "Inter")}\',Inter;background:{bg};color:{NAVY if dark else boxfg};border-radius:3px;padding:1px 3px;'
            f'{f"transform:skewX({bl}deg);display:inline-block" if bl else ""}">{inner}</span></span>')

EXTRA = []
for name, _, w in FONTS:
    EXTRA.append((dict(font=name, weight=w), f'{name} font', 'Same box and colors'))
for key in ['graphite', 'midnight', 'charcoal', 'ink', 'slatebox']:
    EXTRA.append((dict(pal=key), PALETTES[key][0], 'Subtle color shift, same box'))
EXTRA += [
 (dict(lean=-10), 'IT leans, box stays straight', 'A slight forward lean on the letters only'),
 (dict(lean=-6), 'IT leans a little less', 'A gentler lean, letters only'),
 (dict(boxlean=-10), 'Box and IT lean together', 'The whole tab tilts forward'),
 (dict(boxlean=-6, pal='graphite'), 'Gentle tilt, graphite and slate', 'Whole tab tilted a little, with a color shift'),
 (dict(box=False, lean=-10), 'No box, leaning IT', 'IT in steel blue with a forward lean'),
 (dict(font='Manrope', weight=800, lean=-10), 'Manrope with a leaning IT', 'Letters lean inside a straight box'),
 (dict(font='Sora', weight=700, boxlean=-8), 'Sora with a tilted tab', 'Whole tab tilts forward'),
]
start = len(OPTIONS) + 1
cards2 = ''
for i, (k, t, sub) in enumerate(EXTRA, start):
    fk = {x: k[x] for x in ('font', 'weight', 'pal', 'lean', 'boxlean') if x in k}
    cards2 += f'''<article class="opt"><div class="num">{i}</div>
<div class="lite">{lock2(**k)}</div><div class="drk">{lock2(dark=True, **k)}</div>
<div class="small">{fav2(False, **fk)}{fav2(True, **fk)}{lock2(size="sm", **k)}</div>
<p class="cap"><b>{t}</b><br>{sub}</p></article>'''

cards = ''
for n, opt in enumerate(OPTIONS, 1):
    t, sub = label(opt)
    cards += f'''<article class="opt"><div class="num">{n}</div>
<div class="lite">{lockup(opt, False)}</div><div class="drk">{lockup(opt, True)}</div>
<div class="small">{fav(opt, False)}{fav(opt, True)}{lockup(opt, False, 'sm')}</div>
<p class="cap"><b>{t}</b><br>{sub}</p></article>'''

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Logo options | Well Run IT</title>
<link rel="stylesheet" href="assets/css/site.css">
<style>
{FONT_CSS}
.intro{{padding:56px 0 28px}} .intro h1{{font-size:clamp(34px,4.5vw,52px)}} .intro p{{margin-top:14px;max-width:780px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding-bottom:80px}}
@media (max-width:1000px){{.grid{{grid-template-columns:repeat(2,1fr)}}}} @media (max-width:640px){{.grid{{grid-template-columns:1fr}}}}
.opt{{position:relative;background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden}}
.num{{position:absolute;top:10px;left:12px;font:700 13px Inter;color:var(--muted)}}
.lite,.drk{{display:flex;align-items:center;justify-content:center;height:118px;padding:0 18px}}
.drk{{background:var(--dark)}}
.lk{{display:flex;align-items:center;gap:.42em;font:400 34px/1.1 Inter,system-ui,sans-serif;white-space:nowrap}}
.lk .mk{{width:1.1em;height:1.1em;flex:none}}
.lk.sm{{font-size:17px}}
.small{{display:flex;align-items:center;gap:12px;padding:14px 18px;border-top:1px solid var(--line)}}
.fav{{width:30px;height:30px;border:1px solid var(--line);border-radius:8px;display:grid;place-items:center;background:#fff;flex:none}}
.fav.d{{background:var(--dark);border-color:var(--dark)}} .fav svg{{width:20px;height:20px}}
.cap{{padding:0 18px 16px;font-size:14px;color:var(--ink2);line-height:1.45}}
</style></head><body>
<header class="top"><div class="wrap"><a class="brand" href="index.html" style="font:800 18px Inter;color:var(--ink);text-decoration:none">Well Run IT</a><nav class="nav" style="display:flex"><a href="logos-round1.html">Round one</a><a href="index.html">Back to the site</a></nav></div></header>
<main class="wrap">
<section class="intro"><h1>Logo options, round two.</h1><p class="lead">{len(OPTIONS)} options built around IT in a box, starting with the one you picked (number 1).  Every box sits a hair away from Run, with IT at full weight, so it never blurs into Run at small sizes.  Numbers 30 to 35 skip the box and use a hair of space instead, for comparison.  Each card shows the logo on light, on dark, and small, with the browser tab icon.</p></section>
<div class="grid">{cards}</div>
<section class="intro" style="padding-top:8px"><h2 style="font-size:clamp(28px,3.4vw,40px)">More fonts, subtle colors and a lean.</h2><p class="lead">Numbers {start} to {start + len(EXTRA) - 1} keep your box and try other typefaces, small color shifts and a forward-leaning IT.</p></section>
<div class="grid">{cards2}</div>
</main></body></html>
'''
(ROOT / 'logos-round2.html').write_text(page)
print('built logos.html with', len(OPTIONS), 'options')
