---
name: maintenance-retainer
description: The done-for-you monthly retainer workflow - intake a client
  change request, execute the minimal edit, verify, deploy, log, and the
  handoff document format. Use via /client-edit and /handoff. Not for new
  full builds (/build).
metadata: {version: 1.0.0, category: business, tier: E}
---
# Maintenance Retainer

## Purpose
Fast, safe, logged edits on shipped sites - the recurring-revenue engine.
Edits are surgical: shipped sites are edited under their original rules.

## Inputs
Change request text ($ARGUMENTS via /client-edit), the shipped repo state.

## Outputs
Minimal diff, deployed; log line in DECISIONS.md; (for /handoff)
docs/HANDOFF.md.

## Rules
1. Classify the request: content edit (text/hours/price/photo swap) |
   component tweak | new section | new feature. Content edits proceed;
   new sections/features get a scope+effort note back to the owner FIRST
   (retainer boundary protection).
2. Locate by grep, read only the touched region, edit minimally. Never
   reflow/reformat surrounding code (diff noise = review burden).
3. Facts still obey the invariant: a price/hours change request from the
   client IS the source - quote it verbatim in the DECISIONS.md log line.
4. Reduced QA for content edits: run qa-review script + click-test the
   touched page at 360px. Component/section changes: full /qa.
5. Deploy per deploy-hostinger; confirm live; reply-ready summary for the
   client: what changed, where to look, one line.
6. Photo swaps route through image-optimization; new media through the
   media-generation gate as always.

## Handoff (docs/HANDOFF.md format)
Live URL; what was built (page list, one line each); hosting & domain
summary (names, not credentials); what the retainer covers + how to
request changes (email format: page + what + desired text); response-time
expectation; credentials CHECKLIST by name only - actual secrets are
never in the repo (invariant).

## Anti-patterns
- Rebuilding a page to change a sentence; scope creep executed silently.

## Changelog
- 1.0.0 initial (encodes the retainer-over-dashboard decision)
