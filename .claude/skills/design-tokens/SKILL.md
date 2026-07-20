---
name: design-tokens
description: Produce site/shared/tokens.css - the complete design token set
  (colors, type scale, spacing, motion) implementing the approved design
  direction per contracts/design-tokens.md. Use in Phase 2 after
  design-direction. Not for component CSS (layout-systems, components).
metadata: {version: 1.0.0, category: design, tier: A}
---
# Design Tokens

## Purpose
One file, one source of truth for every visual value on the site.

## Inputs
Design rationale in state/DECISIONS.md, client.md Brand colors,
contracts/design-tokens.md (the required token list - obey exactly).

## Outputs
site/shared/tokens.css defining every token in the contract, nothing
else. Then `python3 scripts/generate-style-preview.py` renders the
tokens as preview/style-preview.html (palette, contrast pairings, type
scale, mock hero) for the Phase 2 approval gate — fix any CONTRAST
FAIL it prints before presenting.

## Rules
1. Emit the full required token set from the contract even if some tokens
   are initially unused - consumers rely on their existence.
2. Colors: build a palette around client brand colors; verify every
   text/bg pairing you intend to use hits WCAG AA (4.5:1 body, 3:1 large).
   Use references/color-theory.md for palette construction.
3. Type: pick pairing per references/typography.md; self-host .woff2 in
   site/assets/fonts (file-structure contract); modular scale ratio per
   direction (calm 1.2, expressive 1.333).
4. Spacing/radius/shadow/motion values per the contract defaults unless
   the direction justifies deviation - note deviations in tokens.css
   comments.
5. tokens.css contains ONLY :root (and optional [data-theme=dark])
   custom properties + the @font-face rules. No selectors, no components.

## References
- references/color-theory.md - palette construction, contrast method
- references/typography.md - pairings by direction, scale, loading

## Anti-patterns
- Hardcoding any visual value outside tokens.css anywhere in the project.
- Google Fonts <link> tags (privacy + performance): self-host instead.

## Changelog
- 1.0.0 initial
