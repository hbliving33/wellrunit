# Builds the WellRunIT wordmark as pure SVG paths (Inter 400/800 shaped with HarfBuzz, plus the custom stride R).
import io, re, sys, json, uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
sys.path.insert(0, '/home/claude/wellrunit/build')
F = '/home/claude/wellrunit/assets/fonts/'
src = open('/home/claude/wellrunit/build/build.py').read()
STRIDE_W = int(re.search(r'^STRIDE_W = (\d+)', src, re.M).group(1))
STRIDE_R = re.search(r"^STRIDE_R = '''(.*?)'''", src, re.M | re.S).group(1)

def load(w):
    data = open(F + f'inter-latin-{w}-normal.woff2', 'rb').read()
    tt = TTFont(io.BytesIO(data)); buf = io.BytesIO(); tt.flavor = None; tt.save(buf)
    raw = buf.getvalue(); face = hb.Face(raw); font = hb.Font(face)
    return tt, font, tt['head'].unitsPerEm
FONTS = {w: load(w) for w in (400, 800)}

def run(text, w, size, x, ls_em):
    """Shape text; return (svg path d, new x).  CSS letter-spacing is added after every character."""
    tt, font, upem = FONTS[w]
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, {'kern': True, 'liga': True})
    gs = tt.getGlyphSet(); s = size / upem; d = ''
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        name = tt.getGlyphName(info.codepoint)
        pen = SVGPathPen(gs)
        gs[name].draw(TransformPen(pen, (s, 0, 0, -s, x + pos.x_offset * s, -pos.y_offset * s)))
        d += pen.getCommands()
        x += pos.x_advance * s + ls_em * size
    return d, x

def wordmark(well, run_c, it, marks, size=100):
    """Returns (svg inner, width, top, bottom) with baseline at y=0, matching the site's CSS."""
    ls = -0.03
    d1, x = run('Well', 400, size, 0, ls)
    capk = 0.727 * size / 100          # stride R is drawn on a 100-unit cap height
    rx = x
    r = STRIDE_R.replace('class="rm"', f'fill="{marks}"').replace('currentColor', run_c)
    rsvg = f'<g transform="translate({rx:.2f} {-0.727*size:.2f}) scale({capk:.5f})">{r}</g>'
    x += STRIDE_W * capk + ls * size  # the svg box is one "character" with letter-spacing after it
    d2, x = run('un', 800, size, x, ls)
    x += 0.03 * size                    # margin-left on IT
    d3, x = run('IT', 800, size, x, 0)
    inner = f'<path fill="{well}" d="{d1}"/>{rsvg}<path fill="{run_c}" d="{d2}"/><path fill="{it}" d="{d3}"/>'
    return inner, x

def icon(run_c, marks):
    r = STRIDE_R.replace('class="rm"', f'fill="{marks}"').replace('currentColor', run_c)
    return r, STRIDE_W

if __name__ == '__main__':
    inner, w = wordmark('#2f5580', '#1b2430', '#2f5580', '#2f5580')
    print('width', round(w, 1))
