# Typography
Pairings by direction (all with solid free/OFL options - verify current
license before shipping):
- Quiet luxury / premium: high-contrast serif display + neutral sans body
- Craft / warm: humanist serif or slab + humanist sans
- Clinical calm: geometric or humanist sans for both, weight contrast only
- Bold energy: condensed grotesque display + plain grotesque body
Rules: max 2 families; weights limited to 2-3 per family (file size);
--text-hero uses clamp() for fluid scale, e.g.
clamp(2.25rem, 5vw + 1rem, 4.5rem). Body 16px min mobile.
Loading: @font-face with font-display: swap; preload only the heading
woff2 used above the fold.
