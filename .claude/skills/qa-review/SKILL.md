---
name: qa-review
description: Pre-delivery quality gate - automated checks script plus manual
  review checklist covering correctness, contracts compliance, links, copy
  placeholders, and cross-page consistency. Use via /qa in Phase 6 and in
  reduced form for retainer edits. Not for performance budgets
  (performance) or WCAG depth (accessibility).
metadata: {version: 1.0.0, category: qa, tier: A}
---
# QA Review

## Purpose
Nothing ships with broken links, leftover placeholders, contract
violations, or drifted shared markup.

## Inputs
site/ (pages, shared/, assets/), state files, contracts/.

## Outputs
Pass/fail per check in BUILD_STATE.md notes; fixes applied.

## Rules
1. Run scripts/check.py FIRST; it is authoritative for its checks
   (placeholders, broken local refs, missing alt, hardcoded colors,
   header/footer drift, TODOs). Fix and re-run to clean.
2. Manual review after the script, in this order:
   a. Read every page top-to-bottom as the target visitor; flag copy that
      contradicts client.md.
   b. Verify every client fact against client.md (phone, hours, address,
      prices) character-by-character.
   c. Click-path test: every nav link, every CTA, form submits to the
      real Formspree endpoint, Calendly loads, map centers correctly.
   d. Resize pass: covered by the rendered /visual-qa audit (Phase 6
      step 2) - do not repeat it mentally; verify its PASS block exists
      in BUILD_STATE notes.
   e. Disable JS mentally: does every section still make sense
      (component-api rule 5)?
3. Any MEDIA_LOG row with status=generated but file missing from
   site/assets/, or asset in use without a log row: FAIL.
4. Criticals block phase 6. Cosmetic nits: fix if <5 min, else log to
   DECISIONS.md as accepted.

## Scripts
- scripts/check.py - run from repo root: python3 .claude/skills/qa-review/scripts/check.py

## Anti-patterns
- Marking QA done from memory of earlier state instead of re-running.

## Changelog
- 1.0.0 initial
