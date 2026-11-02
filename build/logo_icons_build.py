"""Builds logo-icons.html: 40 numbered transparent icon options to sit next to the WellRunIT wordmark.
Run from the repo root:  python3 build/logo_icons_build.py"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
G, S, SKY, W = '#1b2430', '#2f5580', '#b9cde3', '#fff'

def st(c, w=3.4):            return f'fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'

# Transparent icons, no box or circle behind them, using only the wordmark's own colors.
# a = the accent color (Well and IT), c = the core color (Run).  Light: slate blue + graphite.  Dark: light slate + white.
ICONS = [
 ('Check mark', lambda a,c: f'<path d="M5 21l10 10L35 9" {st(a,6.5)}/>'),
 ('Check mark, two-tone', lambda a,c: f'<path d="M5 21l10 10" {st(c,6.5)}/><path d="M15 31L35 9" {st(a,6.5)}/>'),
 ('Check inside a ring', lambda a,c: f'<circle cx="20" cy="20" r="16" {st(c,3.4)}/><path d="M12.5 20.5l5 5L28 15" {st(a,4.4)}/>'),
 ('Shield outline with check', lambda a,c: f'<path d="M20 4l13 5v9c0 9-6 14.5-13 18-7-3.5-13-9-13-18V9z" {st(c,3.2)}/><path d="M13.5 20l4.5 4.5L27 15.5" {st(a,4)}/>'),
 ('Solid shield', lambda a,c: f'<path d="M20 4l13 5v9c0 9-6 14.5-13 18-7-3.5-13-9-13-18V9z" fill="{a}"/><path d="M20 4v32c-7-3.5-13-9-13-18V9z" fill="{c}"/>'),
 ('Gauge, needle up', lambda a,c: f'<path d="M5 29a15 15 0 1130 0" {st(c,4)}/><path d="M20 29l8.5-10" {st(a,4)}/><circle cx="20" cy="29" r="3.6" fill="{a}"/>'),
 ('Heartbeat line', lambda a,c: f'<path d="M2 21h8l3.5-8 6 15 4.5-10 2.5 3h11.5" {st(a,3.8)}/>'),
 ('Heartbeat, two-tone', lambda a,c: f'<path d="M2 21h8l3.5-8" {st(c,3.8)}/><path d="M13.5 13l6 15 4.5-10 2.5 3h11.5" {st(a,3.8)}/>'),
 ('Double forward arrows', lambda a,c: f'<path d="M7 9l11 11L7 31" {st(c,5)}/><path d="M20 9l11 11-11 11" {st(a,5)}/>'),
 ('Play / run triangle', lambda a,c: f'<path d="M10 6l24 14-24 14z" fill="{a}" stroke="{a}" stroke-width="3" stroke-linejoin="round"/>'),
 ('Rising bars', lambda a,c: f'<rect x="4" y="24" width="8" height="12" rx="2" fill="{c}"/><rect x="16" y="15" width="8" height="21" rx="2" fill="{a}"/><rect x="28" y="5" width="8" height="31" rx="2" fill="{a}"/>'),
 ('Rising bars with arrow', lambda a,c: f'<rect x="5" y="25" width="7" height="11" rx="1.6" fill="{c}"/><rect x="16.5" y="19" width="7" height="17" rx="1.6" fill="{c}"/><rect x="28" y="13" width="7" height="23" rx="1.6" fill="{c}"/><path d="M4 18L15 9l6 5L35 4M28 4h7v7" {st(a,3.2)}/>'),
 ('Server stack', lambda a,c: f'<rect x="6" y="5" width="28" height="8" rx="2" fill="{c}"/><rect x="6" y="16" width="28" height="8" rx="2" fill="{c}"/><rect x="6" y="27" width="28" height="8" rx="2" fill="{a}"/>'),
 ('Server stack with check', lambda a,c: f'<rect x="3" y="6" width="22" height="7" rx="1.8" fill="{c}"/><rect x="3" y="16" width="22" height="7" rx="1.8" fill="{c}"/><rect x="3" y="26" width="14" height="7" rx="1.8" fill="{c}"/><path d="M21 29l4.5 4.5L37 22" {st(a,4.4)}/>'),
 ('Cloud with check', lambda a,c: f'<path d="M11 31a7 7 0 01-.8-14A9.5 9.5 0 0128.5 15a8 8 0 011 16z" {st(c,3.2)}/><path d="M14.5 23l4 4 7.5-7.5" {st(a,3.8)}/>'),
 ('Gear', lambda a,c: f'<circle cx="20" cy="20" r="10" {st(c,5)}/>' + ''.join(f'<rect x="17.5" y="2.5" width="5" height="7" rx="1.2" fill="{c}" transform="rotate({x} 20 20)"/>' for x in range(0,360,45)) + f'<circle cx="20" cy="20" r="4" fill="{a}"/>'),
 ('Gear with check', lambda a,c: f'<circle cx="20" cy="20" r="10.5" {st(c,4)}/>' + ''.join(f'<rect x="17.8" y="3" width="4.4" height="6" rx="1.1" fill="{c}" transform="rotate({x} 20 20)"/>' for x in range(0,360,45)) + f'<path d="M15 20.5l3.5 3.5 7-7.5" {st(a,3.6)}/>'),
 ('Wrench', lambda a,c: f'<path d="M30 6a9 9 0 00-11.5 11.5L6.5 29.5a3.2 3.2 0 004.5 4.5l12-12A9 9 0 0034.5 10.5l-5 5-4.2-.6-.6-4.2z" fill="{a}"/>'),
 ('Key', lambda a,c: f'<circle cx="12" cy="20" r="8" {st(c,4)}/><path d="M20 20h16M30 20v6M35 20v5" {st(a,4)}/>'),
 ('Padlock', lambda a,c: f'<path d="M12 18v-5a8 8 0 0116 0v5" {st(c,4)}/><rect x="7" y="18" width="26" height="18" rx="3.5" fill="{a}"/>'),
 ('Network nodes', lambda a,c: f'<path d="M20 8L7 31M20 8l13 23M7 31h26" {st(c,2.8)}/><circle cx="20" cy="8" r="5" fill="{a}"/><circle cx="7" cy="31" r="5" fill="{c}"/><circle cx="33" cy="31" r="5" fill="{c}"/>'),
 ('Hub and spokes', lambda a,c: f'<path d="M20 20L6 8M20 20L34 8M20 20v15" {st(c,2.8)}/><circle cx="6" cy="8" r="4" fill="{c}"/><circle cx="34" cy="8" r="4" fill="{c}"/><circle cx="20" cy="35" r="4" fill="{c}"/><circle cx="20" cy="20" r="6" fill="{a}"/>'),
 ('Wi-Fi signal', lambda a,c: f'<path d="M3 15a24 24 0 0134 0M9 21a15.5 15.5 0 0122 0" {st(c,4)}/><path d="M15 27a7 7 0 0110 0" {st(a,4)}/><circle cx="20" cy="33" r="3" fill="{a}"/>'),
 ('Globe', lambda a,c: f'<circle cx="20" cy="20" r="16" {st(c,3)}/><path d="M4 20h32M20 4c6 5 6 27 0 32M20 4c-6 5-6 27 0 32" {st(a,2.8)}/>'),
 ('Compass', lambda a,c: f'<circle cx="20" cy="20" r="16" {st(c,3)}/><path d="M20 6l5 14h-10z" fill="{a}"/><path d="M20 34l-5-14h10z" fill="{c}"/>'),
 ('Lighthouse', lambda a,c: f'<path d="M16 12h8l3 24H13z" fill="{c}"/><rect x="15" y="6" width="10" height="6" rx="1.4" fill="{a}"/><path d="M27 7l9-3M27 10.5h9" {st(a,2.6)}/>'),
 ('Mountain peak', lambda a,c: f'<path d="M2 34l13-20 7 10 5-6 11 16z" fill="{c}"/><path d="M15 14l4 6-4-2-4 2z" fill="{a}"/>'),
 ('Sunrise', lambda a,c: f'<path d="M8 27a12 12 0 0124 0" {st(a,4)}/><path d="M4 32h32" {st(c,4)}/><path d="M20 5v5M7 11l3.5 3.5M33 11l-3.5 3.5" {st(a,3.4)}/>'),
 ('Ocean wave', lambda a,c: f'<path d="M2 20c5 0 6-6 11-6s6 6 11 6 6-6 11-6" {st(a,4)}/><path d="M2 29c5 0 6-5 11-5s6 5 11 5 6-5 11-5" {st(c,4)}/>'),
 ('Lightning bolt', lambda a,c: f'<path d="M23 3L8 23h10l-3 14 17-21H21z" fill="{a}"/>'),
 ('Rocket', lambda a,c: f'<path d="M20 3c6 5 8.5 12 6 21H14c-2.5-9 0-16 6-21z" fill="{c}"/><circle cx="20" cy="14" r="3" fill="{a}"/><path d="M14 19l-6 8 6-1.5M26 19l6 8-6-1.5M17 27l3 9 3-9z" fill="{a}"/>'),
 ('Target / bullseye', lambda a,c: f'<circle cx="20" cy="20" r="16" {st(c,3.4)}/><circle cx="20" cy="20" r="9" {st(c,3.4)}/><circle cx="20" cy="20" r="3.6" fill="{a}"/>'),
 ('Hexagon with check', lambda a,c: f'<path d="M20 3l15 8.5v17L20 37 5 28.5v-17z" {st(c,3.2)}/><path d="M13 20.5l5 5L27.5 15" {st(a,4)}/>'),
 ('Cube', lambda a,c: f'<path d="M20 3l15 8.5-15 8.5-15-8.5z" fill="{a}"/><path d="M5 11.5L20 20v17L5 28.5z" fill="{c}"/><path d="M35 11.5L20 20v17l15-8.5z" fill="{a}" opacity=".55"/>'),
 ('Puzzle piece', lambda a,c: f'<path d="M6 10h8a4 4 0 118 0h8v8a4 4 0 110 8v8H6v-8.5a4 4 0 100-7.5z" fill="{a}"/>'),
 ('Monogram W', lambda a,c: f'<path d="M3 8l7 24 10-19 10 19 7-24" {st(a,5)}/>'),
 ('Monogram W, two-tone', lambda a,c: f'<path d="M3 8l7 24 10-19" {st(c,5)}/><path d="M20 13l10 19 7-24" {st(a,5)}/>'),
 ('Infinity loop (always on)', lambda a,c: f'<path d="M20 20c-3.5-5-6.5-7.5-10-7.5a7.5 7.5 0 000 15c3.5 0 6.5-2.5 10-7.5" {st(c,4)}/><path d="M20 20c3.5-5 6.5-7.5 10-7.5a7.5 7.5 0 010 15c-3.5 0-6.5-2.5-10-7.5" {st(a,4)}/>'),
 ('Circular arrows (kept running)', lambda a,c: f'<path d="M33 15a14 14 0 00-24.5-2" {st(a,4)}/><path d="M7 25a14 14 0 0024.5 2" {st(c,4)}/><path d="M7 5v8h8" {st(a,4)}/><path d="M33 35v-8h-8" {st(c,4)}/>'),
 ('Lightbulb', lambda a,c: f'<path d="M20 3a11 11 0 00-6 20.3V28h12v-4.7A11 11 0 0020 3z" fill="{a}"/><path d="M15 32h10M16.5 36.5h7" {st(c,3)}/>'),
]

def wordmark(dark):
    w, r, i = ((SKY, W, SKY) if dark else (S, G, S))
    return f'<span class="wm" style="color:{w}">Well<b style="color:{r}">Run</b><i style="color:{i}">IT</i></span>'

cards = ''
for n, (name, svg) in enumerate(ICONS, 1):
    lt, dk = svg(S, G), svg(SKY, W)
    cards += f'''<div class="opt"><div class="num">{n}</div><div class="name">{name}</div>
<div class="row light"><svg viewBox="0 0 40 40" aria-hidden="true">{lt}</svg>{wordmark(False)}</div><div class="row dark"><svg viewBox="0 0 40 40" aria-hidden="true">{dk}</svg>{wordmark(True)}</div>
<div class="small"><svg viewBox="0 0 40 40">{lt}</svg><svg viewBox="0 0 40 40">{lt}</svg><span>Tab and phone size</span></div></div>'''

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Logo icon options | Well Run IT</title>
<style>
@font-face{{font-family:Inter;font-weight:400;src:url(assets/fonts/inter-latin-400-normal.woff2) format("woff2")}}
@font-face{{font-family:Inter;font-weight:800;src:url(assets/fonts/inter-latin-800-normal.woff2) format("woff2")}}
body{{margin:0;background:#eef0f3;color:{G};font:400 16px/1.5 Inter,system-ui,sans-serif}}
.wrap{{max-width:1240px;margin:0 auto;padding:40px 20px}}
h1{{font-size:34px;letter-spacing:-.02em;margin:0 0 8px}}
p.lead{{margin:0 0 32px;color:#3c4a5c}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:16px}}
.opt{{background:#fff;border:1px solid #c9d0da;border-top:4px solid {S};border-radius:16px;padding:18px;position:relative}}
.num{{position:absolute;top:14px;right:16px;font-weight:800;font-size:22px;color:{S}}}
.name{{font-size:14px;color:#3c4a5c;margin-bottom:12px;padding-right:40px}}
.row{{display:flex;align-items:center;gap:10px;padding:14px 16px;border-radius:10px}}
.row svg{{width:40px;height:44px;flex:none}}
.row.light{{background:#eef0f3}} .row.dark{{background:{G};margin-top:8px}}
.wm{{font:400 27px/1 Inter;letter-spacing:-.03em;white-space:nowrap}}
.wm b{{font-weight:800}} .wm i{{font-style:normal;font-weight:800;margin-left:.03em;letter-spacing:0}}
.small{{display:flex;align-items:center;gap:10px;margin-top:12px;font-size:13px;color:#6b7787}}
.small svg:first-child{{width:16px;height:16px}} .small svg:nth-child(2){{width:30px;height:30px}}
</style></head><body><div class="wrap">
<h1>Logo icon options</h1>
<p class="lead">{len(ICONS)} transparent icons to sit next to the WellRunIT wordmark, no box behind them, using only the logo's own colors.  Each is shown in the header (light), the footer (dark), and at browser-tab and phone-icon size.  Tell me the number you like.</p>
<div class="grid">{cards}</div></div></body></html>'''
(ROOT / 'logo-icons.html').write_text(html)
print(f'built logo-icons.html with {len(ICONS)} options')
