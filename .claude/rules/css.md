---
paths: ["**/*.css"]
---
# CSS rules (load only when editing CSS)
- var(--token) only; zero hardcoded colors/sizes/durations (contracts/design-tokens.md).
- Mobile-first: base styles are mobile; min-width media queries at 640/1024px.
- BEM-lite per contracts/component-api.md. No !important except utilities.
- Wrap all keyframe/transition motion in @media (prefers-reduced-motion: no-preference).
- Max nesting depth 2. One component per block comment header.
- Card/column grids: auto-fit can strand a lone widow card in the last
  row - if item-count mod columns = 1, use explicit repeat(N,1fr)
  breakpoints or span/center the last item instead.
