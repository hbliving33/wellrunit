"""Builds logos.html: the Well Run IT brand kit, every approved logo file ready to download.
Files come from assets/brand/kit/ (made from the approved logo: the R in "Run" in stride, logo-refine number 2).
The earlier option rounds stay at logos-round1.html to logos-round3.html, logo-icons*.html, logo-r.html, logo-combo.html, logo-custom.html and logo-refine.html.
Run from the repo root:  python3 build/brand_kit_build.py"""
import json, pathlib, html as H
ROOT = pathlib.Path(__file__).resolve().parent.parent
KIT = 'assets/brand/kit/'
FILES = {f['file']: f for f in json.loads((ROOT / 'assets' / 'brand' / 'kit.json').read_text())}
G, S, SKY = '#1b2430', '#2f5580', '#9bb6d3'

def size(n):
    return f'{n / 1024 / 1024:.1f} MB' if n > 1024 * 1024 else f'{max(1, round(n / 1024))} KB'

def btns(names):
    out = ''
    for n in names:
        f = FILES[n]; ext = n.rsplit('.', 1)[1].upper()
        out += f'<a class="dl" href="{KIT}{n}" download><b>{ext}</b><span>{H.escape(f["label"])}</span><i>{size(f["bytes"])}</i></a>'
    return f'<div class="dls">{out}</div>'

def card(title, note, preview_img, bg, names, wide=False, checker=False):
    pv = f'<div class="pv{" checker" if checker else ""}" style="background:{bg}"><img src="{KIT}{preview_img}" alt="{H.escape(title)}"></div>'
    return f'<article class="card{" wide" if wide else ""}">{pv}<div class="body"><h3>{title}</h3><p>{note}</p>{btns(names)}</div></article>'

logos = ''.join([
    card('Full color', 'For white and light backgrounds.  The main logo.', 'logo-color.png', '#ffffff', ['logo-color.svg', 'logo-color.png', 'logo-color-on-white.jpg']),
    card('Reverse', 'For dark backgrounds, like the website footer.', 'logo-reverse.png', G, ['logo-reverse.svg', 'logo-reverse.png', 'logo-reverse-on-graphite.jpg']),
    card('White only', 'For photos and colored backgrounds.', 'logo-white.png', S, ['logo-white.svg', 'logo-white.png', 'logo-white-on-slate.jpg', 'logo-white-on-graphite.jpg']),
    card('One color', 'Graphite only, for print, stamps and forms.', 'logo-graphite.png', '#ffffff', ['logo-graphite.svg', 'logo-graphite.png', 'logo-graphite-on-white.jpg']),
])
icons = ''.join([
    card('Icon, full color', 'The R in stride, on its own.  Transparent.', 'icon-color.png', '#ffffff', ['icon-color.svg', 'icon-color.png'], checker=True),
    card('Icon, white', 'For dark or colored backgrounds.  Transparent.', 'icon-white.png', S, ['icon-white.svg', 'icon-white.png']),
    card('Icon, reverse', 'White R with light slate marks, for dark backgrounds.', 'icon-reverse.png', G, ['icon-reverse.svg', 'icon-reverse.png']),
    card('App icon', 'Rounded slate square.  The ICO files are for Windows shortcuts and browser tabs.', 'app-icon.png', '#e3e8ef', ['app-icon.svg', 'app-icon.png', 'app-icon.ico', 'favicon.ico']),
])
photo = card('Support mailbox photo', '648 by 648, the largest photo size Microsoft 365 uses.  Outlook and Teams show it as a circle, so the R is centered with room around it.', 'support-mailbox-photo.png', '#e3e8ef', ['support-mailbox-photo.jpg', 'support-mailbox-photo.png'])
zoom = ''.join([
    card('Zoom background, dark', '1920 by 1080 (16:9).  Logo top left, so it stays clear of you.', 'zoom-dark.jpg', G, ['zoom-dark.jpg', 'zoom-dark.png'], wide=True),
    card('Zoom background, light', '1920 by 1080 (16:9).', 'zoom-light.jpg', '#e3e8ef', ['zoom-light.jpg', 'zoom-light.png'], wide=True),
])
swatches = ''.join(f'<div class="sw"><span style="background:{c}"></span><b>{n}</b><code>{c}</code><small>{u}</small></div>' for n, c, u in [
    ('Slate blue', S, 'Well, IT, motion marks, buttons'), ('Graphite', G, 'Run, text, dark backgrounds'), ('Light slate', SKY, 'Logo on dark backgrounds'), ('Mist', '#eef0f3', 'Page background')])

page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Brand kit | Well Run IT</title>
<link rel="icon" href="assets/brand/favicon.svg" type="image/svg+xml">
<style>
@font-face{{font-family:Inter;font-weight:400;src:url(assets/fonts/inter-latin-400-normal.woff2) format("woff2")}}
@font-face{{font-family:Inter;font-weight:700;src:url(assets/fonts/inter-latin-700-normal.woff2) format("woff2")}}
@font-face{{font-family:Inter;font-weight:800;src:url(assets/fonts/inter-latin-800-normal.woff2) format("woff2")}}
*{{box-sizing:border-box}}
body{{margin:0;background:#eef0f3;color:{G};font:400 16px/1.5 Inter,system-ui,sans-serif}}
.top{{background:{G};padding:22px 0}} .top img{{height:34px;display:block}}
.wrap{{max-width:1240px;margin:0 auto;padding:0 20px}}
h1{{font:800 clamp(32px,4vw,44px)/1.1 Inter;letter-spacing:-.03em;margin:44px 0 10px}}
.lead{{color:#3c4a5c;max-width:780px;margin:0}}
h2{{font:800 24px Inter;letter-spacing:-.02em;margin:48px 0 16px;padding-bottom:10px;border-bottom:2px solid {G}}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:18px}}
.card{{background:#fff;border:1px solid #c9d0da;border-radius:16px;overflow:hidden}}
.g2{{grid-template-columns:1fr 1fr}}
@media (max-width:820px){{.g2{{grid-template-columns:1fr}}}}
.pv{{height:200px;display:grid;place-items:center;padding:28px;border-bottom:1px solid #e3e8ef}}
.card.wide .pv{{height:auto;padding:0}} .card.wide .pv img{{width:100%;height:auto;max-height:none}}
.pv img{{max-width:100%;max-height:140px;display:block}}
.pv.checker{{background-color:#fff!important;background-image:linear-gradient(45deg,#e9edf2 25%,transparent 25%),linear-gradient(-45deg,#e9edf2 25%,transparent 25%),linear-gradient(45deg,transparent 75%,#e9edf2 75%),linear-gradient(-45deg,transparent 75%,#e9edf2 75%);background-size:20px 20px;background-position:0 0,0 10px,10px -10px,-10px 0}}
.body{{padding:18px 20px 20px}} .body h3{{margin:0;font:700 18px Inter}} .body p{{margin:6px 0 14px;color:#3c4a5c;font-size:14.5px}}
.dls{{display:flex;flex-direction:column;gap:6px}}
.dl{{display:grid;grid-template-columns:52px 1fr auto;align-items:center;gap:10px;padding:9px 12px;border:1px solid #c9d0da;border-radius:10px;text-decoration:none;color:{G};font-size:14px}}
.dl:hover{{border-color:{S};background:#f3f6fa}}
.dl b{{font:800 12px Inter;letter-spacing:.06em;color:#fff;background:{S};border-radius:6px;padding:4px 0;text-align:center}}
.dl i{{font-style:normal;color:#6b7787;font-size:13px}}
.sws{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}}
.sw{{background:#fff;border:1px solid #c9d0da;border-radius:14px;padding:14px;display:grid;grid-template-columns:56px 1fr;column-gap:14px;align-items:center}}
.sw span{{grid-row:span 3;width:56px;height:56px;border-radius:12px;border:1px solid #c9d0da}}
.sw code{{font:600 14px ui-monospace,Consolas,monospace;color:{S}}} .sw small{{color:#6b7787}}
.foot{{margin:56px 0 40px;color:#6b7787;font-size:14px}} .foot a{{color:{S}}}
</style></head><body>
<div class="top"><div class="wrap"><a href="index.html"><img src="{KIT}logo-reverse.svg" alt="Well Run IT"></a></div></div>
<div class="wrap">
<h1>Brand kit</h1>
<p class="lead">Every approved Well Run IT logo, ready to download.  SVG is the original and scales to any size.  PNG has a transparent background.  JPG has the background shown.  Font: Inter.</p>
<h2>Logo</h2><div class="grid">{logos}</div>
<h2>Icon</h2><div class="grid">{icons}</div>
<h2>Microsoft 365</h2><div class="grid">{photo}</div>
<h2>Zoom backgrounds</h2><div class="grid g2">{zoom}</div>
<h2>Colors</h2><div class="sws">{swatches}</div>
<p class="foot">Earlier logo options: <a href="logo-refine.html">final round</a>, <a href="logo-custom.html">custom letters</a>, <a href="logo-icons.html">icons</a>, <a href="logos-round3.html">wordmark rounds</a>.</p>
</div></body></html>'''
(ROOT / 'logos.html').write_text(page)
print('built logos.html with', len(FILES), 'downloads')
