---
name: layout-systems
description: Compose page layouts - section rhythm, grid, container, and
  responsive behavior - implementing the architecture and design direction.
  Use in Phase 5 when building page structure. Not for individual component
  markup (components) or hero media logic (hero-media).
metadata: {version: 1.0.0, category: frontend, tier: B}
---
# Layout Systems

## Purpose
Pages that feel designed, not stacked: deliberate rhythm, alignment, and
responsive behavior per contracts/component-api.md and file-structure.

## Inputs
Architecture + design rationale in DECISIONS.md, tokens.css, contracts.

## Outputs
Page HTML skeletons + base.css layout layer.

## Rules
1. One .container (max-width var(--container-max), inline padding
   var(--space-4)) per section; full-bleed backgrounds on the section.
2. Section vertical rhythm via var(--section-pad-y); vary background
   (bg/surface alternation or one accent-tinted band) to create rhythm -
   never vary padding randomly.
3. Grids: CSS grid with repeat(auto-fit, minmax(min(100%, Xrem), 1fr))
   for card sets - EXCEPT when the item count strands a widow (count
   mod columns = 1 at any breakpoint): then use explicit repeat(N,1fr)
   per breakpoint, or span/center the last card deliberately
   (rules/css.md). Check the actual card count before choosing.
4. Mobile-first (rules/css.md); test composition at 360/768/1280 widths
   mentally before writing; no horizontal scroll ever.
5. Asymmetry/overlap only if the design direction's distinctive element
   calls for it - and contained so it degrades safely.
6. references/hero-patterns.md governs above-the-fold composition;
   references/responsive-rules.md governs breakpoint behavior details.
7. The Phase 2 layout preview (preview/layout-preview.html) is BINDING:
   it was authored with this skill's patterns and approved by the
   operator - Phase 5 reproduces its section order, grid, spacing
   rhythm, and animation timing exactly; any deviation the build
   requires gets one line in DECISIONS.md before it ships.

## References
- references/hero-patterns.md
- references/responsive-rules.md

## Anti-patterns
- Same centered-text-over-image hero for every client.
- min-height: 100vh on mobile (browser chrome jump) - use svh or budget.

## Changelog
- 1.2.0 binding Phase 2 layout preview (v1.7.1)
- 1.1.0 grid widow exception on rule 3 (v1.6.0 - found in build #2)
- 1.0.0 initial
