import svgkit as k

DISPLAY = "ClashDisplay-Semibold.otf"
MONO    = "GeistMono-Medium.ttf"

W, H = 1200, 420
PAD   = 72
WELL  = W - PAD * 2
TRACK, WS = -0.015, 0.05

THEMES = {
  "dark":  dict(bg="#010522", ink="#F5F5F5", mut="#7F86AD", line="#FFFFFF", lineop=".14",
                plate="#1E1EFC", plateink="#FFFFFF"),
  "light": dict(bg="#FBFBFA", ink="#0B0B0B", mut="#6B6A66", line="#0B0B0B", lineop=".15",
                plate="#1E1EFC", plateink="#FFFFFF"),
}

STATS = [
    ("$60,603", "ONE CLIENT, 11 INVOICES"),
    ("45",      "FRAMER TEMPLATES"),
    ("11",      "LANGUAGES, ONE CMS"),
    ("5 days",  "BRIEF TO LIVE URL"),
]

def build(t):
    c = THEMES[t]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
         f'role="img" aria-label="Hardik Dewra, landing pages. Your next landing page, live in five working days.">',
         f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>']

    def rule(y):
        s.append(f'<rect x="{PAD}" y="{y}" width="{WELL}" height="1" fill="{c["line"]}" opacity="{c["lineop"]}"/>')

    p, _ = k.text("HARDIK DEWRA — LANDING PAGES, FIGMA TO FRAMER", MONO, 12.5, PAD, 46, c["mut"], .085)
    s.append(p)
    p, _ = k.text("NEW DELHI · IST", MONO, 12.5, W - PAD, 46, c["mut"], .085, anchor="end")
    s.append(p)
    rule(72)

    size = 76
    p, _ = k.text("Your next landing page,", DISPLAY, size, PAD, 180, c["ink"], TRACK, wordspace=WS)
    s.append(p)

    lead, wlead = k.text("live in", DISPLAY, size, PAD, 262, c["ink"], TRACK, wordspace=WS)
    s.append(lead)

    phrase = "five working days"
    wph = k.width(phrase, DISPLAY, size, TRACK, WS)
    cap = k.metrics(DISPLAY, size)["cap"]
    px, py = 15, 11
    bx = PAD + wlead + 20
    by = 262 - cap - py
    s.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{wph+px*2:.1f}" height="{cap+py*2:.1f}" rx="4" fill="{c["plate"]}"/>')
    p, _ = k.text(phrase, DISPLAY, size, bx + px, 262, c["plateink"], TRACK, wordspace=WS)
    s.append(p)

    rule(316)
    colw = WELL / len(STATS)
    for i, (val, lab) in enumerate(STATS):
        x = PAD + i * colw
        p, _ = k.text(val, DISPLAY, 34, x, 364, c["ink"], -0.01, wordspace=.04); s.append(p)
        p, _ = k.text(lab, MONO, 10.5, x, 390, c["mut"], .075); s.append(p)
        if i:
            s.append(f'<rect x="{x-26:.1f}" y="338" width="1" height="58" fill="{c["line"]}" opacity="{c["lineop"]}"/>')

    s.append("</svg>")
    return "\n".join(s)

for t in THEMES:
    open(f"header-{t}.svg", "w").write(build(t))
print("ok")
