---
name: accessibility
description: Meet WCAG 2.1 AA across the site - semantics, contrast, focus,
  keyboard operability, motion safety. Use in Phase 5 while building and as
  an audit before QA. Not the generic QA gate (qa-review).
metadata: {version: 1.0.0, category: frontend, tier: B}
---
# Accessibility

## Purpose
AA compliance as a build property, not a retrofit.

## Inputs
site/, shared/tokens.css (contrast pairs), rules/html.md baseline.

## Outputs
Compliant markup/CSS; audit notes in BUILD_STATE.md.

## Rules
1. Semantics first: landmarks, heading order, lists as lists, buttons for
   actions / links for navigation - never divs with click handlers.
2. Contrast: every token pairing used must hit 4.5:1 body / 3:1 large+UI.
   The design-tokens skill verified the palette; verify the USAGE here
   (text over images needs a scrim).
3. Keyboard: everything operable; visible :focus-visible style (token-based,
   never outline:none without replacement); logical tab order; skip link
   to #main on multi-section pages.
4. Forms: label every input (visible label, not placeholder-as-label);
   errors announced via aria-live region; required marked in text.
5. Motion: delegated to frontend-animation reduced-motion reference - but
   audit that it actually happened.
6. Images: alt discipline per rules/html.md; decorative -> alt="".
7. Run through references/audit-checklist.md before handing to /qa.

## References
- references/audit-checklist.md

## Anti-patterns
- aria-* as a fix for wrong elements; contrast checked only on the palette
  page, not over photos.

## Changelog
- 1.0.0 initial
