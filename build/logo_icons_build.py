"""Builds logo-icons.html, round two of the icon next to the WellRunIT wordmark.
Keeps number 3 (check inside a ring) from round one, plus the ideas picked by voice on Nov 1 2026:
more check-in-a-circle versions (nothing breaking out of the ring), the check mark that becomes a forward arrow,
number 13 (server stack) in different color mixes, a stepped server rack, a cube with one slow turn, and new marks built from the name.
All transparent, no box behind them, only the logo's own colors.
Earlier round: logo-icons-round1.html.  Run from the repo root:  python3 build/logo_icons_build.py"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
G, S, SKY, W = '#1b2430', '#2f5580', '#b9cde3', '#fff'
M = '#7f9cbd'   # lighter slate, the "Well" blue lightened, used only as a third tone

def st(c, w=3.4): return f'fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'

# Each icon gets three colors: a = accent (Well and IT), c = core (Run), m = soft third tone.
# Light (header): a=slate blue, c=graphite, m=light slate.  Dark (footer): a=light slate, c=white, m=mid slate.
def rack(top, mid, bot, a, c, m):
    col = {'a': a, 'c': c, 'm': m}
    return ''.join(f'<rect x="6" y="{y}" width="28" height="8" rx="2" fill="{col[k]}"/>' for y, k in ((5, top), (16, mid), (27, bot)))

def rack_lights(top, mid, bot, a, c, m):
    col = {'a': a, 'c': c, 'm': m}
    out = ''
    for y, k in ((5, top), (16, mid), (27, bot)):
        out += f'<rect x="6" y="{y}" width="28" height="8" rx="2" fill="{col[k]}"/><circle cx="11" cy="{y+4}" r="1.6" fill="{W if col[k] != W else G}"/>'
    return out

ICONS = [
 # ---- check inside a ring ----
 ('Check inside a ring (number 3 from round one)', 'check',
  lambda a,c,m: f'<circle cx="20" cy="20" r="16" {st(c,3.4)}/><path d="M12.5 20.5l5 5L28 15" {st(a,4.4)}/>'),
 ('Number 3, refined: thinner ring, heavier check', 'check',
  lambda a,c,m: f'<circle cx="20" cy="20" r="16.5" {st(c,2.4)}/><path d="M12 20.8l5.6 5.6L28.6 14.6" {st(a,5)}/>'),
 ('Number 3, two-tone ring', 'check',
  lambda a,c,m: f'<path d="M20 3.5a16.5 16.5 0 010 33" {st(a,3.4)}/><path d="M20 36.5a16.5 16.5 0 010-33" {st(c,3.4)}/><path d="M12.5 20.5l5 5L28 15" {st(a,4.4)}/>'),
 ('Check inside a solid circle (check cut out)', 'check',
  lambda a,c,m: f'<mask id="k{{id}}"><rect width="40" height="40" fill="#fff"/><path d="M12 20.8l5.6 5.6L28.6 14.6" {st("#000",5)}/></mask><circle cx="20" cy="20" r="17" fill="{a}" mask="url(#k{{id}})"/>'),
 ('Check inside a double ring', 'check',
  lambda a,c,m: f'<circle cx="20" cy="20" r="17" {st(m,2)}/><circle cx="20" cy="20" r="12.5" {st(c,2.6)}/><path d="M14.5 20.5l4 4 7.5-8" {st(a,3.8)}/>'),
 ('Check inside a ring, ring draws itself once on load', 'check anim-draw',
  lambda a,c,m: f'<circle class="draw" cx="20" cy="20" r="16" {st(c,3.2)} pathLength="100" transform="rotate(-90 20 20)"/><path class="draw late" d="M12.5 20.5l5 5L28 15" {st(a,4.4)} pathLength="100"/>'),

 # ---- check that becomes a forward arrow ----
 ('Check mark whose tail becomes a forward arrow', 'arrow',
  lambda a,c,m: f'<path d="M4 21l9 9L33 10" {st(a,5)}/><path d="M22 9.5h11.5V21" {st(a,5)}/>'),
 ('Check-to-arrow, two-tone', 'arrow',
  lambda a,c,m: f'<path d="M4 21l9 9" {st(c,5)}/><path d="M13 30L33 10" {st(a,5)}/><path d="M22 9.5h11.5V21" {st(a,5)}/>'),
 ('Check-to-arrow inside a ring', 'arrow',
  lambda a,c,m: f'<circle cx="20" cy="20" r="16.5" {st(c,2.4)}/><path d="M11 21l5.5 5.5L27 16" {st(a,4)}/><path d="M20.5 15.5h7v7" {st(a,4)}/>'),
 ('Check-to-arrow with speed lines', 'arrow',
  lambda a,c,m: f'<path d="M3 15h7M1 21h6" {st(m,3)}/><path d="M11 22l7 7L35 12" {st(a,5)}/><path d="M25 11.5h10.5V22" {st(a,5)}/>'),

 # ---- number 13, server stack, color mixes ----
 ('Number 13 server stack, as it was (two graphite, one slate blue)', 'rack', lambda a,c,m: rack('c','c','a',a,c,m)),
 ('Server stack, slate blue on top', 'rack', lambda a,c,m: rack('a','c','c',a,c,m)),
 ('Server stack, three tones dark to light', 'rack', lambda a,c,m: rack('c','a','m',a,c,m)),
 ('Server stack, three tones light to dark', 'rack', lambda a,c,m: rack('m','a','c',a,c,m)),
 ('Server stack, graphite in the middle', 'rack', lambda a,c,m: rack('a','c','a',a,c,m)),
 ('Server stack with status lights', 'rack', lambda a,c,m: rack_lights('c','a','m',a,c,m)),

 # ---- stepped server rack ----
 ('Stepped server rack: three units rising like stairs', 'steps',
  lambda a,c,m: f'<rect x="4" y="27" width="16" height="8" rx="2" fill="{m}"/><rect x="10" y="16" width="20" height="8" rx="2" fill="{a}"/><rect x="16" y="5" width="20" height="8" rx="2" fill="{c}"/>'),
 ('Stepped rack, rising left to right', 'steps',
  lambda a,c,m: f'<rect x="4" y="27" width="32" height="8" rx="2" fill="{c}"/><rect x="12" y="16" width="24" height="8" rx="2" fill="{a}"/><rect x="20" y="5" width="16" height="8" rx="2" fill="{m}"/>'),
 ('Stepped rack with arrow climbing the steps', 'steps',
  lambda a,c,m: f'<rect x="4" y="28" width="32" height="7" rx="2" fill="{c}"/><rect x="13" y="19" width="23" height="7" rx="2" fill="{c}"/><rect x="22" y="10" width="14" height="7" rx="2" fill="{c}"/><path d="M4 22l9-8 6 4L31 5M24 5h7v7" {st(a,3)}/>'),

 # ---- cube ----
 ('Cube, makes one slow turn on load (point at it to turn again)', 'cube', None),
 ('Cube, still', 'cube',
  lambda a,c,m: f'<path d="M20 3l15 8.5-15 8.5-15-8.5z" fill="{m}"/><path d="M5 11.5L20 20v17L5 28.5z" fill="{c}"/><path d="M35 11.5L20 20v17l15-8.5z" fill="{a}"/>'),

 # ---- new ideas built from the name ----
 ('"W" made of two check marks', 'new',
  lambda a,c,m: f'<path d="M2 13l7 15L18 9" {st(c,4.4)}/><path d="M17 13l7 15L37 6" {st(a,4.4)}/>'),
 ('Running stride: three forward-leaning bars', 'new',
  lambda a,c,m: f'<path d="M9 34L17 6" {st(m,5)}/><path d="M18 34L26 6" {st(a,5)}/><path d="M27 34L35 6" {st(c,5)}/>'),
 ('Uptime ring: almost full, with a check', 'new',
  lambda a,c,m: f'<circle cx="20" cy="20" r="16" {st(m,3.4)}/><path d="M20 4a16 16 0 11-13.9 8" {st(a,3.4)}/><path d="M14 20.5l4 4 8-8.5" {st(c,3.8)}/>'),
 ('Horizon with a rising sun ("up and running")', 'new',
  lambda a,c,m: f'<path d="M9 27a11 11 0 0122 0" {st(a,4)}/><path d="M3 32h34" {st(c,4)}/><path d="M20 6v5M8.5 11l3.5 3.5M31.5 11L28 14.5" {st(m,3.2)}/>'),
 ('Open loop that keeps running', 'new',
  lambda a,c,m: f'<path d="M28 9.5A14 14 0 1032 25" {st(c,4)}/><path d="M33 9v9h-9" {st(a,4)}/><circle cx="20" cy="20" r="4" fill="{a}"/>'),
 ('Path forward: a road narrowing to a point', 'new',
  lambda a,c,m: f'<path d="M6 36L17 6M34 36L23 6" {st(c,3.6)}/><path d="M20 33v-5M20 22v-4M20 13v-3" {st(a,3.2)}/>'),
 ('Level: three bars all at full, one step up', 'new',
  lambda a,c,m: f'<path d="M5 30h8M16 22h8M27 14h8" {st(a,5)}/><path d="M13 30v-8h3M24 22v-8h3" {st(c,2.6)}/>'),
 ('Forward chevrons, stacked heavy to light', 'new',
  lambda a,c,m: f'<path d="M6 8l12 12L6 32" {st(m,4.6)}/><path d="M15 8l12 12-12 12" {st(a,4.6)}/><path d="M24 8l12 12-12 12" {st(c,4.6)}/>'),
]

def cube_html(a, c, m, size):
    return (f'<span class="cube3d" style="--s:{size}px"><span class="cb"><i style="background:{a}"></i><i style="background:{c}"></i>'
            f'<i style="background:{m}"></i><i style="background:{a}"></i><i style="background:{m}"></i><i style="background:{c}"></i></span></span>')

def mark(fn, a, c, m, size, uid):
    if fn is None:
        return cube_html(a, c, m, size)
    return f'<svg viewBox="0 0 40 40" width="{size}" height="{size}" aria-hidden="true">{fn(a, c, m).replace("{id}", uid)}</svg>'

def wordmark(dark):
    w, r, i = ((SKY, W, SKY) if dark else (S, G, S))
    return f'<span class="wm" style="color:{w}">Well<b style="color:{r}">Run</b><i style="color:{i}">IT</i></span>'

GROUPS = {'check': 'Check inside a circle', 'arrow': 'Check mark that becomes a forward arrow', 'rack': 'Server stack (number 13) in different colors',
          'steps': 'Stepped server rack', 'cube': 'Cube', 'new': 'New ideas, built from the name'}
body, last = '', None
for n, (name, kind, fn) in enumerate(ICONS, 1):
    g = kind.split()[0]
    if g != last:
        body += ('</div>' if last else '') + f'<h2>{GROUPS[g]}</h2><div class="grid">'
        last = g
    lt = mark(fn, S, G, M, 40, f'l{n}'); dk = mark(fn, SKY, W, M, 40, f'd{n}')
    sm1 = mark(fn, S, G, M, 16, f's{n}'); sm2 = mark(fn, S, G, M, 30, f't{n}')
    body += f'''<div class="opt {kind}"><div class="num">{n}</div><div class="name">{name}</div>
<div class="row light">{lt}{wordmark(False)}</div><div class="row dark">{dk}{wordmark(True)}</div>
<div class="small">{sm1}{sm2}<span>Tab and phone size</span></div></div>'''
body += '</div>'

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Logo icon options | Well Run IT</title>
<style>
@font-face{{font-family:Inter;font-weight:400;src:url(assets/fonts/inter-latin-400-normal.woff2) format("woff2")}}
@font-face{{font-family:Inter;font-weight:800;src:url(assets/fonts/inter-latin-800-normal.woff2) format("woff2")}}
body{{margin:0;background:#eef0f3;color:{G};font:400 16px/1.5 Inter,system-ui,sans-serif}}
.wrap{{max-width:1240px;margin:0 auto;padding:40px 20px 80px}}
h1{{font-size:34px;letter-spacing:-.02em;margin:0 0 8px}}
h2{{font-size:20px;margin:40px 0 14px}}
p.lead{{margin:0;color:#3c4a5c;max-width:820px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:16px}}
.opt{{background:#fff;border:1px solid #c9d0da;border-top:4px solid {S};border-radius:16px;padding:18px;position:relative}}
.num{{position:absolute;top:14px;right:16px;font-weight:800;font-size:22px;color:{S}}}
.name{{font-size:14px;color:#3c4a5c;margin-bottom:12px;padding-right:44px;min-height:42px}}
.row{{display:flex;align-items:center;gap:10px;padding:14px 16px;border-radius:10px}}
.row svg,.row .cube3d{{flex:none}}
.row.light{{background:#eef0f3}} .row.dark{{background:{G};margin-top:8px}}
.wm{{font:400 27px/1 Inter;letter-spacing:-.03em;white-space:nowrap}}
.wm b{{font-weight:800}} .wm i{{font-style:normal;font-weight:800;margin-left:.03em;letter-spacing:0}}
.small{{display:flex;align-items:center;gap:10px;margin-top:12px;font-size:13px;color:#6b7787}}
/* ring draws itself once */
.anim-draw .draw{{stroke-dasharray:100;stroke-dashoffset:100;animation:draw 1.1s ease-out .3s forwards}}
.anim-draw .draw.late{{animation-delay:1.2s;animation-duration:.5s}}
@keyframes draw{{to{{stroke-dashoffset:0}}}}
/* 3D cube: one slow turn on load, again on hover */
.cube3d{{display:inline-block;width:var(--s);height:var(--s);perspective:calc(var(--s) * 5)}}
.cb{{position:relative;display:block;width:100%;height:100%;transform-style:preserve-3d;transform:rotateX(-24deg) rotateY(-40deg) scale(.68);animation:spin 3s cubic-bezier(.45,0,.2,1) .4s 1}}
.cb i{{position:absolute;inset:0;border-radius:calc(var(--s) * .08)}}
.cb i:nth-child(1){{transform:translateZ(calc(var(--s) / 2))}}
.cb i:nth-child(2){{transform:rotateY(90deg) translateZ(calc(var(--s) / 2))}}
.cb i:nth-child(3){{transform:rotateX(90deg) translateZ(calc(var(--s) / 2))}}
.cb i:nth-child(4){{transform:rotateY(180deg) translateZ(calc(var(--s) / 2))}}
.cb i:nth-child(5){{transform:rotateX(-90deg) translateZ(calc(var(--s) / 2))}}
.cb i:nth-child(6){{transform:rotateY(-90deg) translateZ(calc(var(--s) / 2))}}
.opt:hover .cb{{animation:spin 3s cubic-bezier(.45,0,.2,1) 1}}
@keyframes spin{{from{{transform:rotateX(-24deg) rotateY(-400deg) scale(.68)}}to{{transform:rotateX(-24deg) rotateY(-40deg) scale(.68)}}}}
@media (prefers-reduced-motion:reduce){{.cb,.opt:hover .cb{{animation:none}}.anim-draw .draw{{animation:none;stroke-dashoffset:0}}}}
</style></head><body><div class="wrap">
<h1>Logo icon options, round two</h1>
<p class="lead">{len(ICONS)} options, all transparent, using only the logo's colors.  Number 3 from round one is kept and refined, along with the check-to-arrow, the server stack in new colors, a stepped rack, a turning cube and a set of new marks.  Reload the page to see the ring draw (number 6) and the cube turn (number 20) again.  Tell me the number you like.</p>
{body}
<p style="margin-top:40px;font-size:14px;color:#6b7787">Round one is still at <a href="logo-icons-round1.html">logo-icons-round1.html</a>.</p>
</div></body></html>'''
(ROOT / 'logo-icons.html').write_text(html)
print(f'built logo-icons.html with {len(ICONS)} options')
