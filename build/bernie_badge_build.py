"""Builds bernie-badge.html: numbered options for Bernie's chat header — a badge next to his name and a name font.
Run from the repo root:  python3 build/bernie_badge_build.py"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
G, S, SKY, M, INK2 = '#1b2430', '#2f5580', '#b9cde3', '#7f9cbd', '#3c4a5c'
WINK = 'Not a fan of chatbots?  Neither are we.  No endless loops, no "I didn\'t quite get that."  Bernie just fills out the form for you.'

FONTS = {   # display name: (file stem, weight)
 'Inter': ('inter', 800), 'Sora': ('sora', 800), 'Outfit': ('outfit', 800), 'Lexend': ('lexend', 800), 'Manrope': ('manrope', 800),
 'Space Grotesk': ('space-grotesk', 700), 'Unbounded': ('unbounded', 800), 'Syne': ('syne', 800), 'Bricolage Grotesque': ('bricolage-grotesque', 800),
 'Exo 2': ('exo-2', 800), 'Rajdhani': ('rajdhani', 700), 'Fraunces': ('fraunces', 800), 'Montserrat': ('montserrat', 800), 'Poppins': ('poppins', 800),
}
css_fonts = ''
for name, (stem, w) in FONTS.items():
    f = ROOT / 'assets' / 'fonts' / f'{stem}-latin-{w}-normal.woff2'
    if f.exists():
        css_fonts += f"@font-face{{font-family:'{name}';font-weight:{w};font-display:swap;src:url(assets/fonts/{f.name}) format('woff2')}}"

# Badges: 44px.  "lean" tips the B forward like the R in the logo; "marks" adds the logo's two motion marks.
def badge(shape='sq', bg=S, fg='#fff', font='Inter', lean=0, marks=False, ring=False, grad=False, dot=False):
    w = FONTS[font][1]
    radius = {'sq': '12px', 'circle': '50%', 'squircle': '16px', 'tag': '12px 12px 12px 4px'}[shape]
    back = f'linear-gradient(145deg,{S},{G})' if grad else bg
    ring_css = f'box-shadow:0 0 0 3px #fff,0 0 0 5px {S};' if ring else ''
    mk = (f'<span class="mk" style="background:{SKY}"></span><span class="mk m2" style="background:{SKY}"></span>' if marks else '')
    d = f'<span class="dot"></span>' if dot else ''
    return (f'<span class="badge" style="border-radius:{radius};background:{back};{ring_css}">{mk}'
            f'<span style="font-family:\'{font}\';font-weight:{w};color:{fg};transform:skewX({-lean}deg);display:inline-block;{"margin-left:9px" if marks else ""}">B</span>{d}</span>')

def name(font, size=20, color=G, spacing='-.01em', upper=False):
    w = FONTS[font][1]
    t = 'BERNIE' if upper else 'Bernie'
    ls = '.08em' if upper else spacing
    return f'<b class="nm" style="font-family:\'{font}\';font-weight:{w};font-size:{size}px;color:{color};letter-spacing:{ls}">{t}</b>'

OPTS = [
 ('Slate square, white B (Inter), name in Inter', badge(), name('Inter')),
 ('Slate square, B tipped forward like the logo R', badge(lean=10), name('Inter')),
 ('B tipped forward with the logo\'s two motion marks', badge(lean=10, marks=True), name('Inter')),
 ('Graphite square, slate motion marks, tipped B', badge(bg=G, lean=10, marks=True), name('Inter')),
 ('Slate-to-graphite gradient square, tipped B', badge(grad=True, lean=10), name('Inter')),
 ('Circle, white B, green "online" dot', badge(shape='circle', dot=True), name('Inter')),
 ('Squircle, Sora font for the B and the name', badge(shape='squircle', font='Sora'), name('Sora', 21)),
 ('Square, Outfit font', badge(font='Outfit'), name('Outfit', 21)),
 ('Square, Lexend font', badge(font='Lexend'), name('Lexend', 20)),
 ('Square, Space Grotesk font (techy)', badge(font='Space Grotesk'), name('Space Grotesk', 21)),
 ('Square, Unbounded font (wide, bold)', badge(font='Unbounded'), name('Unbounded', 18)),
 ('Square, Syne font (designer feel)', badge(font='Syne'), name('Syne', 21)),
 ('Square, Bricolage Grotesque (warm, friendly)', badge(font='Bricolage Grotesque'), name('Bricolage Grotesque', 22)),
 ('Square, Exo 2 tipped (sporty, motion)', badge(font='Exo 2', lean=8, marks=True), name('Exo 2', 21)),
 ('Square, Rajdhani, name in capitals (control-room feel)', badge(font='Rajdhani', bg=G), name('Rajdhani', 21, upper=True)),
 ('Speech-tag shape, Manrope', badge(shape='tag', font='Manrope'), name('Manrope', 21)),
 ('Ringed circle, Poppins', badge(shape='circle', font='Poppins', ring=True), name('Poppins', 21)),
 ('Square, Fraunces serif (classic, warm)', badge(font='Fraunces'), name('Fraunces', 23)),
]

cards = ''
for n, (label, b, nm) in enumerate(OPTS, 1):
    cards += f'''<div class="opt"><div class="num">{n}</div><div class="label">{label}</div>
<div class="panel"><div class="bhead">{b}<div class="txt">{nm}<span class="wink">{WINK}</span></div><span class="close">Close</span></div>
<div class="msg">Hi, I'm Bernie.  What would you like to do?</div></div></div>'''

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Bernie header options | Well Run IT</title>
<style>{css_fonts}
@font-face{{font-family:Inter;font-weight:400;src:url(assets/fonts/inter-latin-400-normal.woff2) format("woff2")}}
body{{margin:0;background:#eef0f3;color:{G};font:400 16px/1.5 Inter,system-ui,sans-serif}}
.wrap{{max-width:1260px;margin:0 auto;padding:40px 20px 80px}}
h1{{font:800 34px Inter;letter-spacing:-.02em;margin:0 0 8px}} p.lead{{margin:0 0 28px;color:{INK2};max-width:820px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(380px,1fr));gap:16px}}
.opt{{background:#fff;border:1px solid #c9d0da;border-top:4px solid {S};border-radius:16px;padding:18px;position:relative}}
.num{{position:absolute;top:14px;right:16px;font:800 22px Inter;color:{S}}}
.label{{font-size:14px;color:{INK2};margin-bottom:12px;padding-right:44px;min-height:42px}}
.panel{{border:1px solid #c9d0da;border-top:4px solid {S};border-radius:14px;box-shadow:0 10px 28px rgba(15,28,45,.14);overflow:hidden}}
.bhead{{display:flex;gap:12px;align-items:flex-start;padding:16px 16px 10px}}
.badge{{position:relative;flex:none;width:44px;height:44px;display:grid;place-items:center;font-size:24px;line-height:1;overflow:visible}}
.badge .mk{{position:absolute;left:6px;height:3px;border-radius:2px;width:8px;top:17px}} .badge .m2{{top:24px;width:5px;left:8px}}
.badge .dot{{position:absolute;right:-1px;bottom:-1px;width:12px;height:12px;border-radius:50%;background:#2fa36b;border:2px solid #fff}}
.txt{{flex:1;min-width:0}} .nm{{display:block;line-height:1.15}}
.wink{{display:block;font-size:13px;color:#6b7787;line-height:1.4;margin-top:3px}}
.close{{flex:none;font:600 12px Inter;color:{INK2};border:1px solid #a9b4c3;border-radius:8px;padding:5px 9px}}
.msg{{margin:6px 16px 16px;max-width:80%;background:#eef1f5;border-radius:12px;border-bottom-left-radius:4px;padding:10px 13px;font-size:14.5px}}
</style></head><body><div class="wrap">
<h1>Bernie header options</h1>
<p class="lead">A badge next to Bernie's name and a cooler font for the name.  Each shows the top of his chat window.  Mix and match if you like the badge from one and the font from another.  Tell me the number.</p>
<div class="grid">{cards}</div></div></body></html>'''
(ROOT / 'bernie-badge.html').write_text(html)
print(f'built bernie-badge.html with {len(OPTS)} options')
