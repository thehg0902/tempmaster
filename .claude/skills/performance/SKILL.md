---
name: performance
description: Enforce speed budgets - Core Web Vitals targets, asset weight
  limits, loading strategy for images/video/fonts/scripts. Use in Phase 5
  while wiring assets and as a pre-QA audit. Not image file generation
  (image-optimization does conversion; this skill sets the budgets).
metadata: {version: 1.0.0, category: frontend, tier: B}
---
# Performance

## Purpose
Local-business sites must load instantly on mid mobile - speed is a
conversion feature and a retainer selling point.

## Inputs
site/, site/assets/, hero-media weight rules.

## Outputs
Budget-compliant loading setup; numbers recorded in BUILD_STATE.md notes.

## Rules
0. PRIORITY LAW: (1) load + interaction targets are hard floors;
   (2) media quality is maximized WITHIN them. Optimization is
   adaptive - never degrade quality that budget headroom allows, never
   keep quality that breaks a budget. /ingest implements this as a
   quality ladder; check.py audits real per-page weight.
1. Budgets are PROFILE-AWARE (client.md Overrides "Hosting plan:";
   unknown = no-cdn, the fail-safe tighter set):
   - cdn profile (hostinger-business/cloud - includes Hostinger CDN,
     ~223ms global TTFB): page <= 1.5MB excl. video; hero video 2.5MB
     target / 4MB cap; scrub sequence <= 10MB.
   - no-cdn profile (hostinger-premium or unknown - no CDN, ~495ms
     TTFB pre-spends ~0.5s of the LCP budget): page <= 1.0MB; hero
     video 2MB target / 3MB cap; scrub <= 8MB; long-lived
     Cache-Control headers in .htaccess are REQUIRED (repeat-visit
     speed is the no-CDN compensator - block lives in security-basics).
   Both profiles: LCP < 2.5s on simulated 4G; CLS < 0.1 (width/height
   everywhere); JS total < 60KB before GSAP/three (deferred,
   non-blocking); scrub loads progressively AFTER first paint - frame
   0001 is the LCP candidate, the rest never block.
2. Images: .webp with sized variants via srcset for anything > 400px
   display width; loading=lazy below the fold; hero poster preloaded,
   never lazy. Exception: alpha assets (logos/icons) - PNG permitted,
   exempt from the WebP mandate (never flatten transparency).
3. Fonts: <= 3 woff2 files, font-display swap, preload the above-the-fold
   heading face only.
4. Scripts: defer everything; no script in <head> without defer; third-party
   (Calendly, analytics) loaded per their skill's lazy pattern.
5. CSS per file-structure contract: tokens.css + base.css (shared) +
   one small per-page style.css — per-page CSS is small by definition
   (page-specific rules only); no @import chains.
6. Verify: the page-weight audit is SCRIPTED - qa-review's check.py
   sums each page's referenced asset bytes against the profile caps and
   names the heaviest offenders; record its output. If the user has
   Lighthouse/PageSpeed available, ask them to run it and paste scores;
   treat unverified LCP/CLS as open QA items, not passes.

## References
- references/loading-strategy.md

## Anti-patterns
- Claiming a Core Web Vitals pass without a measurement to point to.

## Changelog
- 1.0.0 initial
