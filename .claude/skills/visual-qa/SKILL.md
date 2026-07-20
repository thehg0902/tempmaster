---
name: visual-qa
description: Render the built site in a local browser preview and debug it
  VISUALLY - layout at 360/768/1280, spacing rhythm, design-rationale and
  vibe conformance, console errors, reduced-motion. Use via /visual-qa in
  Phase 6 (after the check script passes) and after any retainer edit that
  touches layout. Not for code-level checks (qa-review script) or WCAG
  depth (accessibility).
metadata: {version: 1.0.0, category: qa, tier: A}
---
# Visual QA

## Purpose
Catch what only eyes catch: broken layout, wrong rhythm, lost vibe.
Debugging shifts from code-debug to visual/layout/vibe-debug.

## Inputs
Built site/, the Phase 2 design rationale in state/DECISIONS.md, vibe
references in client/assets-intake/vibe/, .claude/launch.json ("site"
server config).

## Outputs
Fixes applied; a VISUAL QA block (per-page PASS/issues) in
state/BUILD_STATE.md notes.

## Rules
1. Serve site/ with the preview server (launch config "site"). Never
   file:// - relative folder URLs must behave as deployed.
2. Per page, per breakpoint - 360 FIRST (the phone is the primary
   product; audit the mobile-polish checklist there: thumb-zone CTA,
   :active feedback, nav sheet, safe areas, svh), then 768, 1280. At each:
   screenshot; if screenshots time out on the machine, fall back to
   preview_snapshot (structure/text) + preview_inspect (computed
   styles, boxes) - the audit still happens, tool choice is secondary.
3. Layout checklist at every breakpoint: no horizontal overflow; nav
   fits (mobile: phone number visible for call-first niches); hero
   shows poster/first frame before motion; section spacing rhythm
   consistent (--section-pad-y); text measure readable (~45-75ch);
   tap targets >= 44px at 360; images not distorted; footer intact.
4. Rationale conformance: put the Phase 2 design rationale beside the
   1280 view once per page - direction name, type pairing, color
   intent, the ONE distinctive element: is each visibly present? A
   generic-looking page with correct code is a FAIL here. The home
   page additionally gets compared against the APPROVED
   preview/layout-preview.html: same section order, spacing rhythm,
   and animation behavior - unexplained deviations are findings.
5. Vibe conformance: compare the rendered home page against the vibe
   references ONCE (they were distilled at Phase 2 - this is the final
   echo check, not a re-analysis).
6. Behavior spot-checks via preview_eval: no console errors on load;
   prefers-reduced-motion shows posters/no animation; JS disabled
   still renders complete sections (progressive enhancement); WASTE
   check - flag any img whose naturalWidth > 2x its displayed width
   (bytes shipped for pixels never rendered) and any below-fold img
   without loading="lazy" (only detectable rendered).
7. Fix -> re-verify loop: apply targeted edits, re-check ONLY the
   changed page at the breakpoint that failed (token economy). Never
   re-audit the whole site for a one-page fix.
8. Record per-page verdicts in BUILD_STATE notes: page | 360/768/1280 |
   issues found -> fixed | PASS. Phase 6 needs every page PASS.

## Anti-patterns
- Screenshotting every page after every tiny edit; "looks fine to me"
  without walking the checklist; treating rationale conformance as
  optional polish - it is the vibe contract.

## Changelog
- 1.0.0 initial (v1.4.0 Clear Sight)
