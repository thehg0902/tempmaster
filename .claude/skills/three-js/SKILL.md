---
name: three-js
description: Add a Three.js WebGL scene to a page. Use ONLY when client.md
  Stack has 3d:yes or the client explicitly requests 3D/WebGL. Do not use
  for parallax, video, or 2D canvas effects (frontend-animation,
  hero-media).
metadata: {version: 1.0.0, category: frontend, tier: B, optional: true}
---
# Three.js

## Purpose
One contained, performant 3D moment - not a 3D website.

## Inputs
Stack 3d flag, design direction, performance budget.

## Outputs
A self-contained scene module in the page's script.js (or
site/shared/main.js if used on 2+ pages) + its canvas mount.

## Rules
1. Scope: ONE scene per site, in one section, lazy-initialized when the
   canvas nears the viewport (IntersectionObserver), disposed when far.
2. Budget (references/performance-budget.md): renderer pixelRatio capped
   at min(devicePixelRatio,2); target 60fps on mid-range mobile; pause
   rAF when tab hidden or canvas offscreen.
3. Progressive enhancement: static poster image behind the canvas; WebGL
   unavailable or reduced-motion -> poster stands, no errors.
4. Load three via CDN with defer; guard init; version-pin the URL.
5. Assets: compressed GLB (draco if tooling available), textures <=1024px,
   total 3D payload <= 3MB.
6. Interaction limited to pointer-move parallax / slow idle rotation
   unless the client asked for more - log scope in DECISIONS.md.

## References
- references/setup.md, references/performance-budget.md

## Anti-patterns
- 3D as page background behind text; controls that hijack scroll.

## Changelog
- 1.0.0 initial
