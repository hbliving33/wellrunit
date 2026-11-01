"""Builds logos.html, round four: variations of round three's 2, 18, 20 and 38, then new fonts, then new colors.
Reuses the drawing code from build/logos_round3_build.py.  Run from the repo root:  python3 build/logos_build.py"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / 'build' / 'logos_round3_build.py').read_text()
g = {'__file__': str(ROOT / 'build' / 'logos_round3_build.py')}
exec(src.split("\nOPTIONS = [")[0], g)          # FAMILIES, PAL, wordmark(), lockup(), fav() and friends
FAMILIES, PAL, lockup, fav = g['FAMILIES'], g['PAL'], g['lockup'], g['fav']
NAVY, STEEL, SKY = g['NAVY'], g['STEEL'], g['SKY']

FAMILIES.update({
 'Barlow': ('barlow', 400, 800), 'Syne': ('syne', 400, 800), 'Unbounded': ('unbounded', 400, 800), 'Rajdhani': ('rajdhani', 400, 700),
 'Oswald': ('oswald', 400, 700), 'Big Shoulders Display': ('big-shoulders-display', 400, 800), 'JetBrains Mono': ('jetbrains-mono', 400, 800),
 'IBM Plex Mono': ('ibm-plex-mono', 400, 700), 'Fraunces': ('fraunces', 400, 800), 'IBM Plex Serif': ('ibm-plex-serif', 400, 700),
})
FONT_CSS = ''
for name, (stem, lw, hw) in FAMILIES.items():
    for w in sorted({lw, hw, 600, 700, 800}):
        f = ROOT / 'assets' / 'fonts' / f'{stem}-latin-{w}-normal.woff2'
        if f.exists():
            FONT_CSS += f"@font-face{{font-family:'{name}';font-weight:{w};font-display:swap;src:url(assets/fonts/{f.name}) format('woff2')}}"

PAL.update({   # light: (Well, Run, IT)  dark: (Well, Run, IT)
 'cobalt':      ((NAVY, NAVY, '#2a5db0'), ('#fff', '#fff', '#8fb0e6')),
 'ocean':       ((NAVY, NAVY, '#1f6f8b'), ('#fff', '#fff', '#86c3d6')),
 'navysky':     ((NAVY, NAVY, '#4f86b8'), ('#fff', '#fff', '#a9c8e6')),
 'slatesteel':  (('#475569', '#1e293b', '#3b6a99'), ('#cbd5e1', '#fff', '#93b4d6')),
 'blackblue':   (('#141414', '#141414', '#2563a8'), ('#fff', '#fff', '#7fb0e8')),
 'graphteal':   (('#1b2430', '#1b2430', '#2d6475'), ('#fff', '#fff', '#8cc1cc')),
 'warmgray':    (('#3a3632', '#3a3632', '#2f5d8a'), ('#f2eee9', '#f2eee9', SKY)),
 'mutedgold':   ((NAVY, NAVY, '#9a7535'), ('#fff', '#fff', '#d6b46e')),
 'steelwell2':  (('#4f86b8', NAVY, '#4f86b8'), ('#a9c8e6', '#fff', '#a9c8e6')),
 'tealwell':    (('#2d6475', NAVY, '#2d6475'), ('#8cc1cc', '#fff', '#8cc1cc')),
 'graphslate':  (('#6b7787', '#1b2430', '#3d5f85'), ('#b7c4d3', '#fff', '#9bb6d3')),
 'graphwell':   (('#3d5f85', '#1b2430', '#3d5f85'), ('#9bb6d3', '#fff', '#9bb6d3')),
})

S2 = dict(lw=400, hw=700)           # round three number 2
SECTIONS = [
 ('Variations of 2: Inter, light Well, bold Run, steel IT', [
   (dict(S2), '2 as it was', 'Inter, bold Run'),
   (dict(S2, hw=600), 'Run a step lighter', 'Semi-bold Run, calmer overall'),
   (dict(S2, itw=800), 'IT a step heavier than Run', 'IT stands out a little more'),
   (dict(S2, gap='.06em'), 'A touch more space before IT', ''),
   (dict(S2, ls='-.015em'), 'A little more air', 'Letters slightly further apart'),
   (dict(S2, lean=-5), 'IT leans a little', 'Gentle forward lean'),
   (dict(S2, mark='pulse'), 'With the pulse mark', ''),
   (dict(S2, pal='slate'), 'Well in soft slate', 'Three tones'),
 ]),
 ('Variations of 18: Well and IT both colored, Run carries the weight', [
   (dict(pal='steelwell'), '18 as it was', 'Steel blue Well and IT, navy Run'),
   (dict(pal='steelwell', hw=700), 'Bold instead of extra bold', ''),
   (dict(pal='steelwell2'), 'Brighter steel', 'A slightly lighter blue on Well and IT'),
   (dict(pal='tealwell'), 'Deep teal Well and IT', ''),
   (dict(pal='graphwell'), 'Slate blue Well and IT, graphite Run', 'Mixes 18 and 20'),
   (dict(pal='steelwell', font='Raleway'), 'In Raleway', 'Mixes 18 and 38'),
   (dict(pal='steelwell', font='Manrope'), 'In Manrope', ''),
   (dict(pal='steelwell', lean=-5), 'IT leans a little', ''),
 ]),
 ('Variations of 20: graphite and slate blue', [
   (dict(pal='graphite'), '20 as it was', 'Graphite Well and Run, slate blue IT'),
   (dict(pal='graphite', hw=700), 'Bold instead of extra bold', 'Mixes 20 and 2'),
   (dict(pal='graphslate'), 'Well in light gray', 'Three tones in graphite'),
   (dict(pal='graphteal'), 'Graphite with a teal IT', ''),
   (dict(pal='graphite', font='Raleway'), 'In Raleway', 'Mixes 20 and 38'),
   (dict(pal='graphite', font='Sora'), 'In Sora', ''),
   (dict(pal='graphite', mark='status'), 'With the status dot', ''),
 ]),
 ('Variations of 38: Raleway', [
   (dict(font='Raleway'), '38 as it was', 'Raleway, light Well, extra bold Run'),
   (dict(font='Raleway', hw=700), 'Bold instead of extra bold', 'Mixes 38 and 2'),
   (dict(font='Raleway', ls='-.045em'), 'Tighter', 'Letters pulled closer'),
   (dict(font='Raleway', ls='.0em'), 'Looser', 'More air between letters'),
   (dict(font='Raleway', pal='slate'), 'Well in soft slate', 'Three tones'),
   (dict(font='Raleway', caps=True, ls='.04em'), 'All caps', 'WELLRUNIT'),
   (dict(font='Raleway', lean=-5), 'IT leans a little', ''),
   (dict(font='Raleway', mark='pulse'), 'With the pulse mark', ''),
 ]),
 ('New fonts, in the style of 2', [(dict(S2, font=f, hw=FAMILIES[f][2]), f, d) for f, d in [
   ('Barlow', 'Clean and slightly condensed'), ('Syne', 'Distinctive, wide bold'), ('Unbounded', 'Very wide, modern'),
   ('Rajdhani', 'Squared, technical'), ('Oswald', 'Tall and condensed'), ('Big Shoulders Display', 'Narrow, strong'),
   ('JetBrains Mono', 'Code font, IT feel'), ('IBM Plex Mono', 'Typewriter-style code font'),
   ('Fraunces', 'Soft serif, warm'), ('IBM Plex Serif', 'Serious serif, engineered')]]),
 ('New color options, in the style of 2', [(dict(S2, pal=p), t, d) for p, t, d in [
   ('base', 'Navy and steel blue', 'Current colors, for reference'), ('cobalt', 'Navy and cobalt', 'A cleaner, brighter blue'),
   ('ocean', 'Navy and ocean blue', 'Blue with a hint of green'), ('navysky', 'Navy and sky blue', 'Lighter, airier accent'),
   ('slatesteel', 'Slate and steel', 'Softer, three tones'), ('blackblue', 'Near black and true blue', 'Highest contrast'),
   ('graphteal', 'Graphite and teal', 'Calm and technical'), ('warmgray', 'Warm gray and steel', 'A touch warmer than navy'),
   ('mutedgold', 'Navy and muted gold', 'One warm option, still quiet')]]),
]

body = ''; n = 0
for title, opts in SECTIONS:
    cards = ''
    for o, t, sub in opts:
        n += 1
        cards += f'''<article class="opt"><div class="num">{n}</div>
<div class="lite">{lockup(o)}</div><div class="drk">{lockup(o, True)}</div>
<div class="small">{fav(o, False)}{fav(o, True)}{lockup(o, False, 'sm')}</div>
<p class="cap"><b>{t}</b>{('<br>' + sub) if sub else ''}</p></article>'''
    body += f'<h2 class="sec">{title}</h2><div class="grid">{cards}</div>'

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Logo options | Well Run IT</title>
<link rel="stylesheet" href="assets/css/site.css">
<style>
{FONT_CSS}
.intro{{padding:56px 0 20px}} .intro h1{{font-size:clamp(34px,4.5vw,52px)}} .intro p{{margin-top:14px;max-width:780px}}
.sec{{font-size:clamp(22px,2.4vw,28px);margin:34px 0 16px;padding-top:22px;border-top:1px solid var(--line2)}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding-bottom:24px}}
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
<header class="top"><div class="wrap"><a class="brand" href="index.html" style="font:800 18px Inter;color:var(--ink);text-decoration:none">Well Run IT</a><nav class="nav" style="display:flex"><a href="logos-round3.html">Round three</a><a href="logos-round2.html">Round two</a><a href="logos-round1.html">Round one</a><a href="index.html">Back to the site</a></nav></div></header>
<main class="wrap">
<section class="intro"><h1>Logo options, round four.</h1><p class="lead">{n} options.  First, variations of the four you picked from round three (2, 18, 20 and 38), each in its own section.  Then new typefaces, and then new color options, all in the style of 2.</p></section>
{body}
<div style="height:60px"></div>
</main></body></html>
'''
(ROOT / 'logos.html').write_text(page)
print('built logos.html, round four, with', n, 'options')
