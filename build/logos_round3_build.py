"""Builds logos.html, round three: variations on option 33 of round two (light Well, heavy Run, IT in steel blue, one word).
Run from the repo root:  python3 build/logos_build.py   (earlier rounds: logos-round1.html, logos-round2.html)"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
NAVY, STEEL, SKY = '#0f1c2d', '#2f5d8a', '#8fb3d9'

FAMILIES = {   # name: (file stem, light weight, heavy weight)
 'Inter': ('inter', 400, 800), 'Manrope': ('manrope', 400, 800), 'Sora': ('sora', 400, 800), 'Outfit': ('outfit', 400, 800),
 'Lexend': ('lexend', 400, 800), 'Montserrat': ('montserrat', 400, 800), 'Poppins': ('poppins', 400, 800), 'IBM Plex Sans': ('ibm-plex-sans', 400, 700),
 'Archivo': ('archivo', 400, 800), 'Space Grotesk': ('space-grotesk', 400, 700), 'Bricolage Grotesque': ('bricolage-grotesque', 400, 800),
 'Exo 2': ('exo-2', 400, 800), 'Raleway': ('raleway', 400, 800), 'Josefin Sans': ('josefin-sans', 400, 700),
}
FONT_CSS = ''
for name, (stem, lw, hw) in FAMILIES.items():
    for w in sorted({lw, hw, 700}):
        f = ROOT / 'assets' / 'fonts' / f'{stem}-latin-{w}-normal.woff2'
        if f.exists():
            FONT_CSS += f"@font-face{{font-family:'{name}';font-weight:{w};font-display:swap;src:url(assets/fonts/{f.name}) format('woff2')}}"

PAL = {   # light: (Well, Run, IT), dark: (Well, Run, IT)
 'base':     ((NAVY, NAVY, STEEL), ('#fff', '#fff', SKY)),
 'slate':    (('#5b6b7f', NAVY, STEEL), ('#b7c4d3', '#fff', SKY)),
 'steelwell':((STEEL, NAVY, STEEL), (SKY, '#fff', SKY)),
 'graphite': (('#1b2430', '#1b2430', '#3d5f85'), ('#fff', '#fff', '#9bb6d3')),
 'teal':     ((NAVY, NAVY, '#2d6475'), ('#fff', '#fff', '#8cc1cc')),
 'ink':      (('#101828', '#101828', '#36557a'), ('#fff', '#fff', '#9db3cf')),
 'twotone':  ((STEEL, NAVY, NAVY), (SKY, '#fff', '#fff')),
}
MARKS = {
 'pulse': '<path d="M2 12.5h5l2-4.5 3.5 9 2.5-6 1.5 1.5H22" fill="none" stroke="{a}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>',
 'status': '<circle cx="12" cy="12" r="9.5" fill="none" stroke="{c}" stroke-width="2"/><circle cx="12" cy="12" r="5" fill="{a}"/>',
 'gauge': '<path d="M3.5 16a8.5 8.5 0 0117 0" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/><path d="M12 16l5-5.2" stroke="{a}" stroke-width="2.4" stroke-linecap="round"/><circle cx="12" cy="16" r="2" fill="{c}"/>',
 'chev': '<path d="M5 6l6 6-6 6" fill="none" stroke="{c}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M13 6l6 6-6 6" fill="none" stroke="{a}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
}

def wordmark(o, dark=False):
    fam = o.get('font', 'Inter'); stem, lw, hw = FAMILIES[fam]
    lw = o.get('lw', lw); hw = o.get('hw', hw)
    cw, cr, ci = PAL[o.get('pal', 'base')][1 if dark else 0]
    ls = o.get('ls', '-.03em'); gap = o.get('gap', '.03em')
    well, run, it = o.get('text', ('Well', 'Run', 'IT'))
    it_style = f"color:{ci};font-weight:{o.get('itw', hw)};margin-left:{gap};letter-spacing:0;display:inline-block;"
    if o.get('lean'): it_style += f"transform:skewX({o['lean']}deg);"
    if o.get('under'): it_style += f"border-bottom:.09em solid {ci};padding-bottom:.01em;"
    if o.get('dot'): it += f'<span style="color:{ci}">.</span>'
    tail = ''
    if o.get('bar'):   # thin rule after the wordmark
        tail = f'<span style="display:inline-block;width:.5em;height:.12em;background:{ci};margin-left:.1em;vertical-align:.32em;border-radius:.06em"></span>'
    caps = 'text-transform:uppercase;' if o.get('caps') else ''
    well_gap = f"margin-right:{o['wellgap']};" if o.get('wellgap') else ''
    return (f'<span style="font-family:\'{fam}\',Inter,sans-serif;letter-spacing:{ls};white-space:nowrap;{caps}">'
            f'<span style="font-weight:{lw};color:{cw};{well_gap}">{well}</span><span style="font-weight:{hw};color:{cr}">{run}</span>'
            f'<span style="{it_style}">{it}</span>{tail}</span>')

def mark(o, dark):
    m = o.get('mark')
    if not m: return ''
    c, a = ('#fff', SKY) if dark else (NAVY, STEEL)
    return f'<svg viewBox="0 0 24 24" class="mk" aria-hidden="true">{MARKS[m].replace("{c}", c).replace("{a}", a)}</svg>'

def lockup(o, dark=False, cls=''):
    if o.get('stack'):
        fam = o.get('font', 'Inter'); stem, lw, hw = FAMILIES[fam]
        cw, cr, ci = PAL[o.get('pal', 'base')][1 if dark else 0]
        w = (f'<span style="display:inline-flex;flex-direction:column;line-height:.9;font-family:\'{fam}\',Inter;letter-spacing:-.03em">'
             f'<span style="font-weight:{lw};color:{cw};font-size:.62em">Well</span><span><span style="font-weight:{hw};color:{cr}">Run</span>'
             f'<span style="font-weight:{hw};color:{ci};margin-left:.03em">IT</span></span></span>')
    else:
        w = wordmark(o, dark)
    return f'<div class="lk {cls}">{mark(o, dark)}<span class="wm">{w}</span></div>'

def fav(o, dark):
    fam = o.get('font', 'Inter'); stem, lw, hw = FAMILIES[fam]
    cw, cr, ci = PAL[o.get('pal', 'base')][1 if dark else 0]
    if o.get('mark'):
        return f'<span class="fav{" d" if dark else ""}">{mark(o, dark)}</span>'
    return (f'<span class="fav{" d" if dark else ""}"><span style="font:{hw} 12px \'{fam}\',Inter;letter-spacing:-.02em">'
            f'<span style="color:{cr}">R</span><span style="color:{ci}">IT</span></span></span>')

OPTIONS = [
 (dict(), 'Your pick, number 33', 'Inter, light Well, heavy Run, IT in steel blue'),
 (dict(lw=400, hw=700), 'Slightly lighter Run', 'Inter, bold instead of extra bold'),
 (dict(gap='0'), 'IT tight to Run', 'No extra space before IT'),
 (dict(gap='.06em'), 'A touch more space before IT', 'Inter'),
 (dict(ls='-.045em'), 'Tighter overall', 'Letters pulled a little closer'),
 (dict(ls='-.01em'), 'Looser overall', 'More air between letters'),
 (dict(itw=700), 'IT a bit lighter than Run', 'Run extra bold, IT bold'),
 (dict(lean=-8), 'IT leans forward', 'A slight forward lean on IT only'),
 (dict(lean=-5), 'IT leans a little', 'A gentle lean on IT only'),
 (dict(under=True), 'IT underlined', 'A short rule under IT'),
 (dict(dot=True), 'With a full stop', 'WellRunIT.'),
 (dict(bar=True), 'With a short dash after', 'A small steel bar finishes the word'),
 (dict(caps=True, ls='.03em'), 'All caps', 'WELLRUNIT, IT in steel blue'),
 (dict(text=('well', 'run', 'IT')), 'Lowercase, capital IT', 'wellrunIT'),
 (dict(text=('well', 'Run', 'IT')), 'Lowercase well', 'wellRunIT'),
 (dict(stack=True), 'Stacked', 'Well above RunIT'),
 (dict(pal='slate'), 'Well in soft slate', 'Three tones: slate, navy, steel blue'),
 (dict(pal='steelwell'), 'Well and IT both steel blue', 'Run carries the weight'),
 (dict(pal='twotone'), 'Steel Well, navy RunIT', 'Color on Well instead of IT'),
 (dict(pal='graphite'), 'Graphite and slate blue', 'Subtle color shift'),
 (dict(pal='teal'), 'Navy with deep teal IT', 'Subtle color shift'),
 (dict(pal='ink'), 'Ink and denim', 'Subtle color shift'),
 (dict(mark='pulse'), 'With a pulse', 'Steel blue pulse line before the word'),
 (dict(mark='status'), 'With a status dot', 'Operational dot before the word'),
 (dict(mark='gauge'), 'With a gauge', 'Needle in the green'),
 (dict(mark='chev'), 'With forward chevrons', 'Motion before the word'),
 (dict(font='Manrope'), 'Manrope', 'Same idea, rounder letters'),
 (dict(font='Sora'), 'Sora', 'Wide and modern'),
 (dict(font='Outfit'), 'Outfit', 'Geometric and friendly'),
 (dict(font='Lexend'), 'Lexend', 'Very readable, slightly wide'),
 (dict(font='Montserrat'), 'Montserrat', 'Classic geometric'),
 (dict(font='Poppins'), 'Poppins', 'Round geometric'),
 (dict(font='IBM Plex Sans'), 'IBM Plex Sans', 'Technical, engineered feel'),
 (dict(font='Archivo'), 'Archivo', 'Compact and sturdy'),
 (dict(font='Space Grotesk'), 'Space Grotesk', 'Tech character'),
 (dict(font='Bricolage Grotesque'), 'Bricolage Grotesque', 'A bit of personality'),
 (dict(font='Exo 2'), 'Exo 2', 'Technical, slightly angular'),
 (dict(font='Raleway'), 'Raleway', 'Elegant, thin and bold contrast'),
 (dict(font='Josefin Sans'), 'Josefin Sans', 'Vintage geometric'),
 (dict(font='Manrope', lean=-6), 'Manrope with a leaning IT', 'Gentle forward lean'),
 (dict(font='Sora', pal='slate'), 'Sora in three tones', 'Slate Well, navy Run, steel IT'),
 (dict(font='Outfit', mark='pulse'), 'Outfit with a pulse', 'Friendly letters with the pulse mark'),
]

cards = ''
for n, (o, t, sub) in enumerate(OPTIONS, 1):
    cards += f'''<article class="opt"><div class="num">{n}</div>
<div class="lite">{lockup(o)}</div><div class="drk">{lockup(o, True)}</div>
<div class="small">{fav(o, False)}{fav(o, True)}{lockup(o, False, 'sm')}</div>
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
.lk{{display:flex;align-items:center;gap:.4em;font-size:36px;line-height:1.1}}
.lk .mk{{width:1.05em;height:1.05em;flex:none}}
.lk.sm{{font-size:18px}}
.small{{display:flex;align-items:center;gap:12px;padding:14px 18px;border-top:1px solid var(--line)}}
.fav{{width:30px;height:30px;border:1px solid var(--line);border-radius:8px;display:grid;place-items:center;background:#fff;flex:none}}
.fav.d{{background:var(--dark);border-color:var(--dark)}} .fav svg{{width:20px;height:20px}}
.cap{{padding:0 18px 16px;font-size:14px;color:var(--ink2);line-height:1.45}}
</style></head><body>
<header class="top"><div class="wrap"><a class="brand" href="index.html" style="font:800 18px Inter;color:var(--ink);text-decoration:none">Well Run IT</a><nav class="nav" style="display:flex"><a href="logos.html">Round four</a><a href="logos-round2.html">Round two</a><a href="logos-round1.html">Round one</a><a href="index.html">Back to the site</a></nav></div></header>
<main class="wrap">
<section class="intro"><h1>Logo options, round three.</h1><p class="lead">{len(OPTIONS)} variations on the one you liked: a light Well, a heavy Run and IT in steel blue, written as one word.  Number 1 is your pick as it was.  The rest try spacing, a lean, small accents, subtle colors, a mark, and 14 different typefaces.  The tab icon on each card uses R and IT.</p></section>
<div class="grid">{cards}</div>
</main></body></html>
'''
(ROOT / 'logos-round3.html').write_text(page)
print('built logos.html, round three, with', len(OPTIONS), 'options')
