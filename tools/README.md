# Art generators

`assets/header-*.svg` and `assets/process-*.svg` are generated, not hand-edited.
Text is converted to outlines so the art renders identically everywhere, which
matters because GitHub strips inline `<svg>` and will not load a webfont inside
an `<img>`-referenced one.

```bash
python3 -m venv .venv
.venv/bin/pip install uharfbuzz fonttools
.venv/bin/python tools/mkheader.py
.venv/bin/python tools/mkprocess.py
```

Run from the repo root. Output lands next to the scripts, so move the four SVGs
into `assets/`.

## Fonts

Not committed, because their licences do not allow redistribution. Install to
`~/Library/Fonts` first:

| Face | Used for | Source | Licence |
|---|---|---|---|
| Clash Display Semibold | Display | [fontshare.com](https://www.fontshare.com/fonts/clash-display) | Free, incl. commercial |
| Geist | Body copy | [vercel.com/font](https://vercel.com/font) | SIL OFL 1.1 |
| Geist Mono Medium | Eyebrows and labels | [vercel.com/font](https://vercel.com/font) | SIL OFL 1.1 |

`svgkit.py` looks in `./fonts` first, then `~/Library/Fonts`.

## Why these three

Haffer and Martina Plantijn are the usual picks, but the installed copies are
unverified retail builds. This is the most public surface there is, so it uses
only faces that are unambiguously free to publish.
