import svgkit as k

DISPLAY="ClashDisplay-Semibold.otf"; MONO="GeistMono-Medium.ttf"; SANS="Geist-VariableFont_wght.ttf"
W,H=1200,238; PAD=72; WELL=W-PAD*2

THEMES={
 "dark": dict(bg="#010522", ink="#F5F5F5", mut="#7F86AD", line="#FFFFFF", lineop=".14", accent="#0099FF", rail="#FFFFFF", railop=".12"),
 "light":dict(bg="#FBFBFA", ink="#0B0B0B", mut="#6B6A66", line="#0B0B0B", lineop=".15", accent="#1745C4", rail="#0B0B0B", railop=".13"),
}
DAYS=[("DAY 1","Kickoff","I audit your current page, we agree the conversion goal and lock the scope."),
      ("DAY 2","Copy first","Hook, offer and section-by-section copy, before a pixel moves."),
      ("DAY 3","Direction","Two visual directions and one hero concept. You pick a lane."),
      ("DAY 4","Full design","Every section, desktop and phone, designed in Figma."),
      ("DAY 5","Build and ship","Built in Framer, checked on devices, analytics wired, live.")]

def build(t):
    c=THEMES[t]
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
       f'aria-label="Five working days: kickoff, copy, direction, design, build and ship.">',
       f'<rect width="{W}" height="{H}" fill="{c["bg"]}"/>']
    p,_=k.text("BRIEF ON MONDAY. LIVE ON FRIDAY.",MONO,12.5,PAD,44,c["mut"],.085); s.append(p)
    p,_=k.text("ONE PAGE · ONE CONVERSION GOAL",MONO,12.5,W-PAD,44,c["mut"],.085,anchor="end"); s.append(p)

    rail=74
    s.append(f'<rect x="{PAD}" y="{rail}" width="{WELL}" height="1" fill="{c["rail"]}" opacity="{c["railop"]}"/>')
    colw=WELL/5
    for i,(day,title,body) in enumerate(DAYS):
        x=PAD+i*colw
        s.append(f'<rect x="{x:.1f}" y="{rail-2.5}" width="6" height="6" rx="1" fill="{c["accent"]}"/>')
        p,_=k.text(day,MONO,11,x,rail+30,c["accent"],.09); s.append(p)
        p,_=k.text(title,DISPLAY,21,x,rail+62,c["ink"],-0.01,wordspace=.04); s.append(p)
        for j,ln in enumerate(k.wrap(body,SANS,13.5,0,colw-30)):
            p,_=k.text(ln,SANS,13.5,x,rail+90+j*20,c["mut"]); s.append(p)
        if i:
            s.append(f'<rect x="{x-24:.1f}" y="{rail+8}" width="1" height="130" fill="{c["line"]}" opacity="{c["lineop"]}"/>')
    s.append("</svg>")
    return "\n".join(s)

for t in THEMES:
    open(f"process-{t}.svg","w").write(build(t))
print("ok")
