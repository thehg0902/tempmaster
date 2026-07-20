#!/usr/bin/env python3
"""Generate preview/style-preview.html from site/shared/tokens.css +
the Phase 2 design rationale in state/DECISIONS.md.

The page renders the REAL tokens (links ../site/shared/tokens.css and
uses var(--...) everywhere), so it always reflects the current design.
Python only enumerates token names and computes WCAG contrast ratios
for the key text/bg pairings. Lives OUTSIDE site/ so it can never ship.
Run: python scripts/generate-style-preview.py
"""
import re, sys, pathlib

TOKENS = pathlib.Path("site/shared/tokens.css")
DECISIONS = pathlib.Path("state/DECISIONS.md")
OUT = pathlib.Path("preview/style-preview.html")

if not TOKENS.exists():
    print("no site/shared/tokens.css yet - run Phase 2 design first"); sys.exit(1)

css = TOKENS.read_text(encoding="utf-8")
tokens = dict(re.findall(r"(--[\w-]+)\s*:\s*([^;]+);", css))

def hex_rgb(v):
    v = v.strip()
    m = re.fullmatch(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", v)
    if not m: return None
    h = m.group(1)
    if len(h) == 3: h = "".join(c * 2 for c in h)
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def luminance(rgb):
    def ch(c):
        c /= 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(c) for c in rgb)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast(a, b):
    ca, cb = hex_rgb(tokens.get(a, "")), hex_rgb(tokens.get(b, ""))
    if not ca or not cb: return None
    l1, l2 = sorted((luminance(ca), luminance(cb)), reverse=True)
    return (l1 + 0.05) / (l2 + 0.05)

PAIRINGS = [  # (fg, bg, label, AA threshold)
    ("--color-text", "--color-bg", "body text / page bg", 4.5),
    ("--color-text-muted", "--color-bg", "muted text / page bg", 4.5),
    ("--color-text", "--color-surface", "text / surface (cards)", 4.5),
    ("--color-bg", "--color-primary", "button label / primary", 4.5),
]

def pairing_rows():
    rows = []
    for fg, bg, label, aa in PAIRINGS:
        r = contrast(fg, bg)
        verdict = "-" if r is None else (f"{r:.2f}:1 {'PASS' if r >= aa else 'FAIL AA'}")
        cls = "" if r is None or r >= aa else ' style="outline:3px solid red"'
        rows.append(
            f'<div class="pair"{cls} style="color:var({fg});background:var({bg})">'
            f"{label}<br><strong>The quick brown fox — $149</strong>"
            f'<span class="ratio">{verdict}</span></div>')
    return "\n".join(rows)

def swatches():
    out = []
    for name in sorted(t for t in tokens if t.startswith("--color-")):
        out.append(f'<div class="sw"><div class="chip" style="background:var({name})"></div>'
                   f"<code>{name}</code><small>{tokens[name].strip()}</small></div>")
    return "\n".join(out)

def type_scale():
    sizes = ["--text-hero", "--text-3xl", "--text-2xl", "--text-xl",
             "--text-lg", "--text-base", "--text-sm", "--text-xs"]
    out = []
    for s in sizes:
        if s not in tokens: continue
        fam = "var(--font-heading)" if s in ("--text-hero", "--text-3xl", "--text-2xl") else "var(--font-body)"
        out.append(f'<div class="ts" style="font-size:var({s});font-family:{fam}">'
                   f"Aa Quick brown fox <code>{s} = {tokens[s].strip()}</code></div>")
    return "\n".join(out)

def spacing_bars():
    out = []
    for i in range(1, 13):
        t = f"--space-{i}"
        if t in tokens:
            out.append(f'<div class="sp"><code>{t}</code>'
                       f'<div class="bar" style="width:var({t})"></div>'
                       f"<small>{tokens[t].strip()}</small></div>")
    return "\n".join(out)

def rationale():
    if not DECISIONS.exists(): return "(state/DECISIONS.md not found)"
    text = DECISIONS.read_text(encoding="utf-8")
    m = re.search(r"^#{2,3}.*design.*$", text, re.M | re.I)
    if not m: return "(no design rationale section found in DECISIONS.md)"
    start = m.start()
    nxt = re.search(r"^#{2,3} ", text[m.end():], re.M)
    block = text[start:m.end() + (nxt.start() if nxt else len(text))]
    return block.strip()

html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Style Preview (never shipped)</title>
<link rel="stylesheet" href="../site/shared/tokens.css">
<style>
body{{margin:0;background:var(--color-bg);color:var(--color-text);
  font-family:var(--font-body,sans-serif);padding:2rem}}
h2{{font-family:var(--font-heading,serif);border-bottom:1px solid var(--color-border);
  padding-bottom:.3rem;margin-top:2.5rem}}
.grid{{display:flex;flex-wrap:wrap;gap:1rem}}
.sw{{width:130px;font-size:12px}} .chip{{height:56px;border-radius:var(--radius-sm,6px);
  border:1px solid var(--color-border)}}
.pair{{padding:1rem;border-radius:var(--radius-md,10px);width:230px;position:relative}}
.pair .ratio{{display:block;margin-top:.4rem;font-size:11px;opacity:.8}}
.ts code,.sp code{{font-size:11px;opacity:.6;margin-left:.75rem;font-family:monospace}}
.sp .bar{{height:10px;background:var(--color-accent);border-radius:2px;display:inline-block}}
.sp{{display:flex;align-items:center;gap:.5rem}}
.cards{{display:flex;gap:1rem;flex-wrap:wrap}}
.card{{background:var(--color-surface);padding:var(--space-5,1.25rem);width:200px}}
.r-sm{{border-radius:var(--radius-sm)}} .r-md{{border-radius:var(--radius-md)}}
.r-lg{{border-radius:var(--radius-lg)}}
.s-sm{{box-shadow:var(--shadow-sm)}} .s-md{{box-shadow:var(--shadow-md)}}
.s-lg{{box-shadow:var(--shadow-lg)}}
.btn{{display:inline-block;padding:.7rem 1.4rem;border-radius:var(--radius-full,999px);
  font-weight:600;text-decoration:none;margin-right:1rem}}
.btn-primary{{background:var(--color-primary);color:var(--color-bg)}}
.btn-secondary{{border:2px solid var(--color-primary);color:var(--color-primary)}}
input{{background:var(--color-surface);color:var(--color-text);
  border:1px solid var(--color-border);border-radius:var(--radius-sm);
  padding:.7rem 1rem;font-family:inherit}}
.hero{{margin-top:1rem;padding:12vh 2rem;background:var(--color-surface);
  border-radius:var(--radius-lg);text-align:center}}
.hero h1{{font-family:var(--font-heading,serif);font-size:var(--text-hero,3.5rem);
  line-height:var(--leading-tight,1.1);margin:0 0 1rem}}
.hero p{{color:var(--color-text-muted);max-width:38rem;margin:0 auto 1.5rem}}
.motion{{display:inline-block;padding:.6rem 1.2rem;background:var(--color-accent);
  color:var(--color-bg);border-radius:var(--radius-md)}}
@media (prefers-reduced-motion: no-preference){{
  .motion{{transition:transform var(--duration-base,300ms) var(--ease-standard,ease)}}
  .motion:hover{{transform:translateY(-4px) scale(1.04)}}}}
pre.rationale{{background:var(--color-surface);padding:1rem;overflow:auto;
  border-radius:var(--radius-sm);font-size:13px;white-space:pre-wrap}}
</style></head><body>
<h1 style="font-family:var(--font-heading)">Style Preview</h1>
<p>Generated from <code>site/shared/tokens.css</code> — approve the vibe
before Phases 3-5 build on it. This file never ships.</p>

<h2>Design rationale (DECISIONS.md)</h2>
<pre class="rationale">{rationale()}</pre>

<h2>Mock hero</h2>
<div class="hero"><h1>Your Headline In The Display Face</h1>
<p>Subheading in the body face at muted color — does this pairing carry
the mood the client asked for?</p>
<a class="btn btn-primary" href="#">Primary Action</a>
<a class="btn btn-secondary" href="#">Secondary</a></div>

<h2>Contrast pairings (WCAG AA)</h2><div class="grid">{pairing_rows()}</div>
<h2>Palette</h2><div class="grid">{swatches()}</div>
<h2>Type scale</h2>{type_scale()}
<h2>Spacing</h2>{spacing_bars()}
<h2>Radius + elevation</h2><div class="cards">
<div class="card r-sm s-sm">radius-sm / shadow-sm</div>
<div class="card r-md s-md">radius-md / shadow-md</div>
<div class="card r-lg s-lg">radius-lg / shadow-lg</div></div>
<h2>Form + motion</h2>
<p><input placeholder="Input field"> <span class="motion">hover me (motion tokens)</span></p>
</body></html>"""

OUT.parent.mkdir(exist_ok=True)
OUT.write_text(html, encoding="utf-8")
fails = [l for f, b, _, aa in PAIRINGS
         if (r := contrast(f, b)) is not None and r < aa
         for l in [f"{f} on {b} = {r:.2f}:1 (< {aa}:1)"]]
print(f"wrote {OUT}")
for f in fails: print(f"CONTRAST FAIL  {f}")
print(f"{len(tokens)} tokens, {len(fails)} contrast failures")
sys.exit(1 if fails else 0)
