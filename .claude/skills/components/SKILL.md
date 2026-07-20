---
name: components
description: Build the standard section components - header/nav, footer,
  service cards, testimonials, gallery, FAQ accordion, CTA band, contact
  block - per the component API contract. Use in Phase 5 for section
  markup/CSS/JS. Not for page composition (layout-systems) or hero media.
metadata: {version: 1.0.0, category: frontend, tier: B}
---
# Components

## Purpose
Consistent, self-contained sections that obey contracts/component-api.md,
adapted per client rather than reinvented per client.

## Inputs
Architecture section lists, tokens.css, copy from Phase 3, component-api
contract, templates/.

## Outputs
Section markup in page HTML + components.css blocks + data-attribute JS
in main.js.

## Rules
1. Start from templates/sections.html, restyle via tokens + the design
   direction's distinctive element - never ship the template look raw.
2. Header: sticky optional per direction; phone visible on mobile for
   call-first niches; current-page/active-anchor state.
3. FAQ: native <details>/<summary> styled - free accessibility, no JS
   required; enhance animation only.
4. Testimonials: static grid up to 3; carousel only for 4+ AND client
   approval (carousels underperform) - if carousel: buttons, no autoplay,
   keyboard operable.
5. Gallery: CSS grid, lazy-loaded, lightbox only if photos justify it
   (dialog element pattern in templates/).
6. Every interactive behavior initialized from main.js via data attribute
   (component-api rule 4), each init defensive (rules/js.md).

## Scripts / Templates
- templates/sections.html - canonical markup for every standard section

## Anti-patterns
- Autoplaying carousels; div-soup accordions; component CSS that reaches
  outside its block.

## Changelog
- 1.0.0 initial
