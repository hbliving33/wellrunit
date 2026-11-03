# Makes every file in assets/brand/kit/ from the approved logo.  Needs: pip install uharfbuzz fonttools brotli Pillow playwright, and the site served on localhost:8765.
import sys, os, io, json; sys.path.insert(0, '/home/claude/wellrunit/build')
from brand_vec import wordmark, icon, STRIDE_W
from playwright.sync_api import sync_playwright
from PIL import Image
OUT = '/home/claude/wellrunit/assets/brand/kit/'; os.makedirs(OUT, exist_ok=True)
for f in os.listdir(OUT): os.remove(OUT + f)
S, G, SKY, W = '#2f5580', '#1b2430', '#9bb6d3', '#ffffff'

b = None; pg = None
def bbox(inner):
    pg.set_content(f'<svg xmlns="http://www.w3.org/2000/svg" width="2000" height="400" viewBox="-50 -200 2000 400"><g id="g">{inner}</g></svg>')
    return pg.evaluate("(()=>{const r=document.getElementById('g').getBBox();return [r.x,r.y,r.width,r.height]})()")

def svgdoc(inner, box, pad):
    x, y, w, h = box; x -= pad; y -= pad; w += 2 * pad; h += 2 * pad
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x:.2f} {y:.2f} {w:.2f} {h:.2f}" width="{w:.0f}" height="{h:.0f}">{inner}</svg>', w, h

def png(svg, w, h, width_px, path):
    scale = width_px / w; H = round(h * scale)
    pg.set_viewport_size({'width': width_px, 'height': H})
    pg.set_content(f'<html><body style="margin:0;background:transparent">{svg.replace("<svg ", f"<svg style=\"display:block;width:{width_px}px;height:{H}px\" ", 1)}</body></html>')
    pg.screenshot(path=path, omit_background=True)
    return Image.open(path).convert('RGBA')

def jpg(img, bg, path, quality=92):
    base = Image.new('RGBA', img.size, bg); base.alpha_composite(img); base.convert('RGB').save(path, quality=quality)

files = []
def add(name, label, group):
    files.append({'file': name, 'label': label, 'group': group, 'bytes': os.path.getsize(OUT + name)})

with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page()
    # ---- wordmarks ----
    LOGOS = [
      ('logo-color',   'Full color, for light backgrounds', (S, G, S, S), [('white', '#ffffff')]),
      ('logo-reverse', 'Reverse, for dark backgrounds',     (SKY, W, SKY, SKY), [('graphite', G)]),
      ('logo-white',   'White only',                        (W, W, W, W), [('slate', S), ('graphite', G)]),
      ('logo-graphite','One color, graphite',               (G, G, G, G), [('white', '#ffffff')]),
    ]
    for stem, label, (well, runc, it, marks), bgs in LOGOS:
        inner, _ = wordmark(well, runc, it, marks)
        box = bbox(inner); svg, w, h = svgdoc(inner, box, pad=18)
        open(OUT + stem + '.svg', 'w').write(svg); add(stem + '.svg', 'SVG (vector)', stem)
        img = png(svg, w, h, 2400, OUT + stem + '.png'); add(stem + '.png', 'PNG, transparent, 2400 wide', stem)
        for bgname, bg in bgs:
            # jpg with roomier padding on the colored background
            canvas = Image.new('RGBA', (img.width + 400, img.height + 300), (0, 0, 0, 0)); canvas.alpha_composite(img, (200, 150))
            jpg(canvas, bg, OUT + f'{stem}-on-{bgname}.jpg'); add(f'{stem}-on-{bgname}.jpg', f'JPG on {bgname}', stem)
    # ---- icon (the stride R) ----
    ICONS = [('icon-color', 'Icon, full color', (G, S)), ('icon-white', 'Icon, white only', (W, W)), ('icon-reverse', 'Icon, for dark backgrounds', (W, SKY))]
    for stem, label, (runc, marks) in ICONS:
        inner, _ = icon(runc, marks); box = bbox(inner); svg, w, h = svgdoc(inner, box, pad=6)
        open(OUT + stem + '.svg', 'w').write(svg); add(stem + '.svg', 'SVG (vector)', stem)
        png(svg, w, h, 1024, OUT + stem + '.png'); add(stem + '.png', 'PNG, transparent, 1024 wide', stem)
    # square app icon: white R, sky marks, on slate, centered
    def square(size, bg, runc, marks, radius, rfrac, path):
        inner, _ = icon(runc, marks); x, y, w, h = bbox(inner)
        k = size * rfrac / h; tx = size / 2 - (x + w / 2) * k; ty = size / 2 - (y + h / 2) * k
        rect = f'<rect width="{size}" height="{size}" rx="{radius}" fill="{bg}"/>' if bg else ''
        svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}">{rect}<g transform="translate({tx:.2f} {ty:.2f}) scale({k:.4f})">{inner}</g></svg>'
        if path.endswith('.svg'): open(path, 'w').write(svg); return None
        return png(svg, size, size, size, path)
    square(1024, S, W, SKY, 220, .56, OUT + 'app-icon.svg'); add('app-icon.svg', 'SVG (vector)', 'app-icon')
    big = square(1024, S, W, SKY, 220, .56, OUT + 'app-icon.png'); add('app-icon.png', 'PNG, 1024 square', 'app-icon')
    big.save(OUT + 'app-icon.ico', sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]); add('app-icon.ico', 'ICO, Windows icon (16 to 256)', 'app-icon')
    fav = square(256, None, G, S, 0, .86, OUT + '_fav.png')
    fav.save(OUT + 'favicon.ico', sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]); os.remove(OUT + '_fav.png'); add('favicon.ico', 'ICO, transparent (16 to 256)', 'app-icon')
    # ---- support mailbox photo: 648 square, Microsoft 365's largest photo size; it shows as a circle ----
    ph = square(648, S, W, SKY, 0, .50, OUT + 'support-mailbox-photo.png')
    ph.convert('RGB').save(OUT + 'support-mailbox-photo.jpg', quality=95)
    add('support-mailbox-photo.jpg', 'JPG, 648 square (Microsoft 365)', 'support-photo'); add('support-mailbox-photo.png', 'PNG, 648 square', 'support-photo')
    # ---- Zoom backgrounds, 1920 x 1080 ----
    for stem, bgcss, logo_cols, tag in [
        ('zoom-dark', 'linear-gradient(135deg,#1b2430 0%,#22344a 55%,#2f5580 100%)', (SKY, W, SKY, SKY), '#d5dfea'),
        ('zoom-light', 'linear-gradient(135deg,#f4f6f9 0%,#e3e8ef 100%)', (S, G, S, S), '#3c4a5c')]:
        inner, _ = wordmark(*logo_cols); box = bbox(inner); svg, w, h = svgdoc(inner, box, pad=0)
        pg.set_viewport_size({'width': 1920, 'height': 1080})
        pg.set_content(f'''<html><head><style>@font-face{{font-family:Inter;font-weight:600;src:url(http://localhost:8765/assets/fonts/inter-latin-600-normal.woff2)}}
body{{margin:0;width:1920px;height:1080px;background:{bgcss};position:relative;overflow:hidden;font-family:Inter}}
.logo{{position:absolute;left:90px;top:80px;width:420px}} .logo svg{{width:420px;height:auto;display:block}}
.tag{{position:absolute;left:90px;bottom:84px;font:600 30px Inter;color:{tag};letter-spacing:-.01em}}
.url{{position:absolute;right:90px;bottom:84px;font:600 26px Inter;color:{tag};opacity:.8}}</style></head>
<body><div class="logo">{svg}</div><div class="tag">Your IT, well run.</div><div class="url">wellrunit.com</div></body></html>''')
        pg.wait_for_timeout(500); pg.screenshot(path=OUT + stem + '.png')
        Image.open(OUT + stem + '.png').convert('RGB').save(OUT + stem + '.jpg', quality=92)
        add(stem + '.jpg', 'JPG, 1920 x 1080', stem); add(stem + '.png', 'PNG, 1920 x 1080', stem)
    b.close()
json.dump(files, open(OUT + '../kit.json', 'w'), indent=1)
print(len(files), 'files'); [print(f"  {f['file']:34} {f['bytes']//1024:>5} KB") for f in files]
