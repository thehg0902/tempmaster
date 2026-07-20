---
name: frontend-animation
description: Scroll, entrance, and micro-interactions for the page - CSS-only
  by default, GSAP when the Stack flag requests it. Use in Phase 5 when the
  Stack animation flag is css-only or gsap. Not for hero video/sequence
  logic (hero-media) or 3D (three-js).
metadata: {version: 1.0.0, category: frontend, tier: B}
---
# Frontend Animation

## Purpose
Motion that supports hierarchy and mood without hurting performance or
accessibility.

## Inputs
Stack animation flag, design rationale motion level, tokens (durations/easings).

## Outputs
Animation JS in site/shared/main.js (used by 2+ pages) or the page's own
script.js; animation CSS per the same shared-vs-per-page rule.

## Rules
1. Flag = none: no scroll/entrance animation; hover/focus transitions only.
   Flag = css-only: references/css-only.md patterns (IntersectionObserver
   adds .is-visible; CSS does the rest). Flag = gsap: references/gsap.md.
2. All motion gated by prefers-reduced-motion (references/reduced-motion.md)
   - both the CSS and the JS trigger side.
3. Animate transform + opacity ONLY. Never layout properties, never
   width/height/top.
4. Entrance defaults: 16-24px translate + fade, var(--duration-slow),
   var(--ease-out-expo), stagger 60-90ms, trigger at 20% visibility, once.
5. Content must be visible without JS: the hidden initial state is applied
   by JS adding a class at init, never hardcoded in CSS (no-JS = no hiding).
6. Motion level "subtle": entrances only. "Expressive": may add parallax
   (transform-based, capped) and one signature moment - never on every section.

## References
- references/css-only.md, references/gsap.md, references/reduced-motion.md

## Anti-patterns
- Animating everything; scroll-jacking; opacity:0 in stylesheet defaults.

## Changelog
- 1.0.0 initial
