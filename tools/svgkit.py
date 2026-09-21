import os, functools
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform

SYS = os.path.expanduser("~/Library/Fonts")
LOCAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")

def _find(name):
    for d in (LOCAL, SYS):
        p = os.path.join(d, name)
        if os.path.exists(p):
            return p
    raise FileNotFoundError(name)

@functools.lru_cache(maxsize=None)
def _hb(path):
    with open(path, "rb") as fh:
        data = fh.read()
    face = hb.Face(data)
    return hb.Font(face), face.upem

@functools.lru_cache(maxsize=None)
def _tt(path):
    f = TTFont(path, fontNumber=0)
    os2 = f['OS/2']
    cap = getattr(os2, 'sCapHeight', None) or int(f['head'].unitsPerEm * 0.72)
    return f, f.getGlyphSet(), f['head'].unitsPerEm, cap

def metrics(font_file, size):
    p = _find(font_file)
    _, _, upm, cap = _tt(p)
    return {"cap": cap / upm * size, "upm": upm}

def tp(text, font_file, size, tracking=0.0, x=0.0, y=0.0, feats=None, wordspace=0.0):
    """Typeset -> (path_d, width). Baseline at y."""
    p = _find(font_file)
    hbf, upem = _hb(p)
    tt, gs, _, _ = _tt(p)
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hbf, buf, feats or {"kern": True, "liga": True, "calt": True})
    scale = size / upem
    order = tt.getGlyphOrder()
    out = []; cx = 0.0
    codes = [ord(ch) for ch in text]
    for idx, (info, pos) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        gname = order[info.codepoint]
        is_space = info.cluster < len(codes) and codes[info.cluster] == 32
        sp = SVGPathPen(gs, ntos=lambda v: f"{v:.1f}")
        gs[gname].draw(TransformPen(sp, Transform(
            scale, 0, 0, -scale,
            x + cx + pos.x_offset * scale,
            y - pos.y_offset * scale)))
        c = sp.getCommands()
        if c: out.append(c)
        cx += pos.x_advance * scale + tracking * size + (wordspace * size if is_space else 0.0)
    return " ".join(out), cx

def width(text, font_file, size, tracking=0.0, wordspace=0.0):
    return tp(text, font_file, size, tracking, wordspace=wordspace)[1]

def text(t, font_file, size, x, y, fill, tracking=0.0, anchor="start", opacity=None, wordspace=0.0):
    d, w = tp(t, font_file, size, tracking, wordspace=wordspace)
    if anchor == "middle": dx = -w / 2
    elif anchor == "end":  dx = -w
    else: dx = 0
    op = f' opacity="{opacity}"' if opacity is not None else ""
    if dx:
        d, w = tp(t, font_file, size, tracking, x=dx, wordspace=wordspace)
        return f'<g transform="translate({x:.1f},{y:.1f})"><path d="{d}" fill="{fill}"{op}/></g>', w
    return f'<path d="{d}" fill="{fill}"{op} transform="translate({x:.1f},{y:.1f})"/>', w

def wrap(t, font_file, size, tracking, maxw, wordspace=0.0):
    words, lines, cur = t.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if width(trial, font_file, size, tracking, wordspace) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines
