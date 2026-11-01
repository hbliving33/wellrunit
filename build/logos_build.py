"""Builds logos.html: Well Run IT logo options (marks plus wordmarks with IT set tight against Run).
Run from the repo root:  python3 build/logos_build.py"""
import pathlib, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
E = html.escape
NAVY, STEEL, SKY = '#0f1c2d', '#2f5d8a', '#8fb3d9'

# ---------- marks: 24 x 24, drawn in `c` (main) and `a` (accent) ----------
def S(body, c, a, sw=2):
    return body.replace('{c}', c).replace('{a}', a).replace('{sw}', str(sw))
MARKS = {
 'gauge': ('Gauge in the green', '<path d="M3.5 16a8.5 8.5 0 0117 0" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/><path d="M12 16l5-5.2" stroke="{a}" stroke-width="2.4" stroke-linecap="round"/><circle cx="12" cy="16" r="2" fill="{c}"/>'),
 'pulse': ('Steady pulse', '<path d="M2 12.5h5l2-4.5 3.5 9 2.5-6 1.5 1.5H22" fill="none" stroke="{c}" stroke-width="2.3" stroke-linecap="round" stroke-linejoin="round"/><circle cx="22" cy="12.5" r="1.6" fill="{a}"/>'),
 'bars': ('Rising bars', '<rect x="3" y="14" width="4" height="7" rx="1.2" fill="{c}"/><rect x="10" y="9.5" width="4" height="11.5" rx="1.2" fill="{c}"/><rect x="17" y="4" width="4" height="17" rx="1.2" fill="{a}"/>'),
 'rack': ('Server rack, all green', '<rect x="3" y="3" width="18" height="5" rx="1.5" fill="none" stroke="{c}" stroke-width="2"/><rect x="3" y="9.5" width="18" height="5" rx="1.5" fill="none" stroke="{c}" stroke-width="2"/><rect x="3" y="16" width="18" height="5" rx="1.5" fill="none" stroke="{c}" stroke-width="2"/><circle cx="17.5" cy="5.5" r="1.2" fill="{a}"/><circle cx="17.5" cy="12" r="1.2" fill="{a}"/><circle cx="17.5" cy="18.5" r="1.2" fill="{a}"/>'),
 'track': ('Running track', '<rect x="2.5" y="5" width="19" height="14" rx="7" fill="none" stroke="{c}" stroke-width="2"/><rect x="6.5" y="8.5" width="11" height="7" rx="3.5" fill="none" stroke="{a}" stroke-width="2"/>'),
 'chevrons': ('Forward motion', '<path d="M4 6l6 6-6 6" fill="none" stroke="{c}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 6l6 6-6 6" fill="none" stroke="{a}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'),
 'toggle': ('Switched on', '<rect x="2" y="6.5" width="20" height="11" rx="5.5" fill="{c}"/><circle cx="16.5" cy="12" r="3.6" fill="#fff"/><circle cx="16.5" cy="12" r="1.5" fill="{a}"/>'),
 'wcheck': ('W made of checks', '<path d="M2.5 9l4 8 4.5-8 4.5 8 6-12" fill="none" stroke="{c}" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/><circle cx="21.5" cy="5" r="1.6" fill="{a}"/>'),
 'loop': ('Always running', '<path d="M19 12a7 7 0 11-2.1-5" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/><path d="M17.5 2.8v4.6h-4.6" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="12" r="2.4" fill="{a}"/>'),
 'shield': ('Shield, quietly', '<path d="M12 2.5l7.5 2.8v5.6c0 4.6-3.2 8.4-7.5 10.3-4.3-1.9-7.5-5.7-7.5-10.3V5.3z" fill="{c}"/><path d="M8.5 12l2.4 2.4 4.6-5" fill="none" stroke="{a}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'),
 'compass': ('True north', '<circle cx="12" cy="12" r="9" fill="none" stroke="{c}" stroke-width="2"/><path d="M12 5l2.6 7H9.4z" fill="{a}"/><path d="M12 19l-2.6-7h5.2z" fill="{c}"/>'),
 'nodes': ('Connected network', '<circle cx="12" cy="5" r="2.4" fill="{a}"/><circle cx="5" cy="17" r="2.4" fill="{c}"/><circle cx="19" cy="17" r="2.4" fill="{c}"/><path d="M12 7.4L6.2 15M12 7.4l5.8 7.6M7.4 17h9.2" stroke="{c}" stroke-width="1.8"/>'),
 'horizon': ('Calm horizon', '<path d="M2.5 16h19" stroke="{c}" stroke-width="2.4" stroke-linecap="round"/><path d="M6 16a6 6 0 0112 0" fill="{a}"/><path d="M6 20h12" stroke="{c}" stroke-width="2" stroke-linecap="round" opacity=".5"/>'),
 'clock': ('Right on time', '<circle cx="12" cy="12" r="9" fill="none" stroke="{c}" stroke-width="2.2"/><path d="M12 7v5l3.5 2" fill="none" stroke="{a}" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>'),
 'status': ('Status: operational', '<circle cx="12" cy="12" r="9.5" fill="none" stroke="{c}" stroke-width="2"/><circle cx="12" cy="12" r="5" fill="{a}"/>'),
 'layers': ('The full stack', '<path d="M12 3l9 4.5-9 4.5-9-4.5z" fill="{a}"/><path d="M3 12l9 4.5 9-4.5" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/><path d="M3 16.5l9 4.5 9-4.5" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>'),
 'road': ('The road ahead', '<path d="M8 21L11 3M16 21L13 3" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/><path d="M12 19v-2.5M12 13.5v-2M12 8.5V7" stroke="{a}" stroke-width="1.8" stroke-linecap="round"/>'),
 'gear': ('Well-oiled gear', '<path d="M12 2.8l1.6 2.3 2.7-.8.6 2.8 2.7.9-.6 2.7 2 1.9-2 1.9.6 2.7-2.7.9-.6 2.8-2.7-.8L12 21.2l-1.6-2.3-2.7.8-.6-2.8-2.7-.9.6-2.7-2-1.9 2-1.9-.6-2.7 2.7-.9.6-2.8 2.7.8z" fill="{c}"/><path d="M8.8 12.2l2.2 2.2 4.2-4.6" fill="none" stroke="{a}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>'),
 'signal': ('Strong signal', '<path d="M3 9.5a13 13 0 0118 0M6 13a8.5 8.5 0 0112 0M9 16.5a4 4 0 016 0" fill="none" stroke="{c}" stroke-width="2.2" stroke-linecap="round"/><circle cx="12" cy="20" r="1.8" fill="{a}"/>'),
 'brackets': ('Handled', '<path d="M8 4H5v16h3M16 4h3v16h-3" fill="none" stroke="{c}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/><circle cx="12" cy="12" r="2.6" fill="{a}"/>'),
 'level': ('Level and balanced', '<rect x="2" y="7.5" width="20" height="9" rx="4.5" fill="none" stroke="{c}" stroke-width="2"/><rect x="9" y="10" width="6" height="4" rx="2" fill="{a}"/><path d="M7.5 9v6M16.5 9v6" stroke="{c}" stroke-width="1.4"/>'),
 'keystone': ('Keystone', '<path d="M7 4h10l-2 16H9z" fill="{c}"/><path d="M2.5 9.5L7 7.5M21.5 9.5L17 7.5" stroke="{a}" stroke-width="2" stroke-linecap="round"/>'),
 'wr': ('WR monogram', '<rect x="1.5" y="1.5" width="21" height="21" rx="6" fill="{c}"/><path d="M5 8l1.7 8 2.3-6 2.3 6L13 8" fill="none" stroke="#fff" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/><path d="M15 16V8h2.4a2.2 2.2 0 010 4.4H15M17.2 12.4l2.3 3.6" fill="none" stroke="{a}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>'),
 'stride': ('In stride', '<circle cx="12" cy="12" r="10" fill="{c}"/><path d="M7 15.5c2.5 0 3.5-7 6-7s3 3.5 5 3.5" fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round"/><circle cx="18" cy="12" r="1.7" fill="{a}"/>'),
}

# ---------- wordmarks: IT always set tight to Run ----------
F = "Inter,system-ui,sans-serif"
def wm(style, ink, acc, light=False):
    it = lambda extra='': f'<span style="color:{acc};{extra}">IT</span>'
    sp = 'letter-spacing:-.035em'
    if style == 'bold':      return f'<span style="font-weight:800;{sp}">Well Run{it()}</span>'
    if style == 'lightit':   return f'<span style="font-weight:800;{sp}">Well Run{it("font-weight:400")}</span>'
    if style == 'lower':     return f'<span style="font-weight:800;{sp}">well run{it()}</span>'
    if style == 'caps':      return f'<span style="font-weight:800;letter-spacing:.06em">WELL RUN{it()}</span>'
    if style == 'capslight': return f'<span style="font-weight:600;letter-spacing:.14em">WELL RUN{it("font-weight:800")}</span>'
    if style == 'onewell':   return f'<span style="{sp}"><span style="font-weight:400">Well</span><span style="font-weight:800">Run</span>{it("font-weight:800")}</span>'
    if style == 'pill':      return f'<span style="font-weight:800;{sp}">Well Run<span style="background:{acc};color:{"#0f1c2d" if light else "#fff"};border-radius:.28em;padding:.02em .16em .04em;margin-left:.04em;font-size:.86em;vertical-align:.06em;letter-spacing:0">IT</span></span>'
    if style == 'italic':    return f'<span style="font-weight:800;{sp}">Well Run{it("font-style:italic;letter-spacing:-.02em")}</span>'
    if style == 'stack':     return f'<span style="display:inline-flex;flex-direction:column;line-height:.92;font-weight:800;{sp}"><span style="font-weight:500;font-size:.62em;letter-spacing:.02em">Well</span><span>Run{it()}</span></span>'
    if style == 'underline': return f'<span style="font-weight:800;{sp}">Well Run<span style="color:{acc};border-bottom:.12em solid {acc};padding-bottom:.02em">IT</span></span>'
    if style == 'dot':       return f'<span style="font-weight:800;{sp}">Well Run{it()}<span style="color:{acc}">.</span></span>'
    if style == 'semibold':  return f'<span style="font-weight:600;letter-spacing:-.025em">Well Run{it("font-weight:800")}</span>'
    raise ValueError(style)

WSTYLES = {'bold': 'Bold, IT in steel blue', 'lightit': 'Bold with a lighter IT', 'lower': 'Lowercase with capital IT', 'caps': 'All caps', 'capslight': 'Spaced caps, heavy IT',
           'onewell': 'Light Well, heavy RunIT', 'pill': 'IT in a solid tab', 'italic': 'IT in italic', 'stack': 'Stacked', 'underline': 'IT underlined', 'dot': 'With a full stop', 'semibold': 'Medium weight, heavy IT'}

OPTIONS = [
 ('gauge', 'bold'), ('gauge', 'lightit'), ('pulse', 'bold'), ('pulse', 'onewell'), ('bars', 'bold'), ('bars', 'caps'),
 ('rack', 'lightit'), ('rack', 'semibold'), ('track', 'bold'), ('track', 'stack'), ('chevrons', 'italic'), ('chevrons', 'bold'),
 ('toggle', 'bold'), ('toggle', 'lower'), ('wcheck', 'bold'), ('wcheck', 'onewell'), ('loop', 'bold'), ('loop', 'capslight'),
 ('shield', 'lightit'), ('compass', 'bold'), ('nodes', 'semibold'), ('horizon', 'bold'), ('horizon', 'stack'), ('clock', 'bold'),
 ('status', 'dot'), ('status', 'pill'), ('layers', 'bold'), ('layers', 'caps'), ('road', 'italic'), ('gear', 'lightit'),
 ('signal', 'bold'), ('brackets', 'pill'), ('level', 'bold'), ('keystone', 'capslight'), ('wr', 'bold'), ('wr', 'underline'),
 ('stride', 'bold'), ('stride', 'lower'), ('gauge', 'pill'), ('pulse', 'dot'),
]

def lockup(mk, st, dark=False):
    ink, acc = ('#fff', SKY) if dark else (NAVY, STEEL)
    mc = '#fff' if dark else NAVY
    svg = f'<svg viewBox="0 0 24 24" class="mk" aria-hidden="true">{S(MARKS[mk][1], mc, acc)}</svg>'
    return f'<div class="lk" style="color:{ink}">{svg}<span class="wm">{wm(st, ink, acc, dark)}</span></div>'

cards = ''
for n, (mk, st) in enumerate(OPTIONS, 1):
    cards += f'''<article class="opt" id="o{n}"><div class="num">{n}</div>
<div class="lite">{lockup(mk, st)}</div><div class="drk">{lockup(mk, st, True)}</div>
<div class="small"><span class="fav"><svg viewBox="0 0 24 24">{S(MARKS[mk][1], NAVY, STEEL)}</svg></span><span class="fav d"><svg viewBox="0 0 24 24">{S(MARKS[mk][1], '#fff', SKY)}</svg></span>{lockup(mk, st).replace('class="lk"', 'class="lk sm"')}</div>
<p class="cap"><b>{MARKS[mk][0]}</b><br>{WSTYLES[st]}</p></article>'''

page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Logo options | Well Run IT</title>
<link rel="stylesheet" href="assets/css/site.css">
<style>
.intro{{padding:56px 0 28px}} .intro h1{{font-size:clamp(34px,4.5vw,52px)}} .intro p{{margin-top:14px;max-width:760px}}
.grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px;padding-bottom:80px}}
@media (max-width:1000px){{.grid{{grid-template-columns:repeat(2,1fr)}}}} @media (max-width:640px){{.grid{{grid-template-columns:1fr}}}}
.opt{{position:relative;background:#fff;border:1px solid var(--line);border-radius:18px;overflow:hidden}}
.num{{position:absolute;top:10px;left:12px;font:700 13px Inter;color:var(--muted)}}
.lite,.drk{{display:flex;align-items:center;justify-content:center;height:118px;padding:0 18px}}
.drk{{background:var(--dark)}}
.lk{{display:flex;align-items:center;gap:.42em;font:400 34px/1 {F};white-space:nowrap}}
.lk .mk{{width:1.15em;height:1.15em;flex:none}}
.lk.sm{{font-size:17px}}
.small{{display:flex;align-items:center;gap:12px;padding:14px 18px;border-top:1px solid var(--line)}}
.fav{{width:30px;height:30px;border:1px solid var(--line);border-radius:8px;display:grid;place-items:center;background:#fff}}
.fav.d{{background:var(--dark);border-color:var(--dark)}} .fav svg{{width:20px;height:20px}}
.cap{{padding:0 18px 16px;font-size:14px;color:var(--ink2);line-height:1.45}}
</style></head><body>
<header class="top"><div class="wrap"><a class="brand" href="index.html" style="font:800 18px Inter;color:var(--ink);text-decoration:none">Well Run IT</a><nav class="nav" style="display:flex"><a href="index.html">Back to the site</a></nav></div></header>
<main class="wrap">
<section class="intro" style="padding-bottom:28px"><h1>Logo options.</h1><p class="lead">{len(OPTIONS)} options.  In every one, IT sits tight against Run in its own color, so it reads as Well Run IT and as one word, RunIT.  Each card shows the logo on light, on dark, and small, with the mark alone as a browser tab icon.  Pick a few numbers you like and I'll refine them.</p></section>
<div class="grid">{cards}</div>
</main></body></html>
'''
(ROOT / 'logos.html').write_text(page)
print('built logos.html with', len(OPTIONS), 'options')
