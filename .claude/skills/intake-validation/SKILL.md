---
name: intake-validation
description: Validate client/client.md against client/client.schema.md and
  turn every gap into a client question. Use at the start of every build
  (pipeline Phase 0) or whenever client.md changes. Not for validating
  code or site output (see qa-review) or parsing the Business Profile
  Paste (client-enrichment).
metadata: {version: 1.1.0, category: process, tier: A}
---
# Intake Validation

## Purpose
Convert an incomplete client brief into either a green light or a precise
confirmation/question list, so no phase ever runs on invented facts.

## Inputs
client/client.md, client/client.schema.md

## Outputs
Confirmation table in chat (Gate 1); state/QUESTIONS.md entries; phase 0
status in state/BUILD_STATE.md.

## Rules
1. Phase 0 order: if the Business Profile Paste is non-empty, enrichment
   runs first (Auto section written), THEN
   `python3 scripts/validate-client-md.py`. The validator is
   authoritative: in v2 the only BLOCKER is "no business name found
   anywhere"; everything else is SOFT. v1.1-format files validate under
   the old required-sections rules.
2. Gate 1 is a confirmation table, not a question ping-pong: ONE compact
   table in chat, one row per [unconfirmed] Auto fact —
   field | value | source. Operator replies once. Corrections → the
   Overrides section; confirmations flip the fact's tag to [confirmed].
3. Write to state/QUESTIONS.md only what the table cannot resolve:
   genuine ambiguities, conflicts found in the paste, and creative gaps.
   Phrase each for a non-technical business owner. Bad: "Provide brand
   guidelines." Good: "Do you have exact brand colors (hex codes)? If
   not, reply 'propose' and I'll design a palette."
4. BLOCKER (no name anywhere): mark phase 0 blocked and stop. SOFT gaps:
   proceed. If the operator proceeds with facts still [unconfirmed]:
   drafts may use them, but phone/address/hours/prices ship as
   [PLACEHOLDER: value?] in HTML — qa-review's script fails on
   placeholders, so nothing unverified reaches deploy.
5. Empty Creative section: SOFT note listing which creative questions
   would most improve the result for the detected niche, then proceed on
   niche-playbook defaults.
6. Sanity-check consistency: pages listed vs services described, booking
   flag vs booking link, logo path actually exists in assets-intake,
   Overrides contradicting Auto (Overrides win — note it in the table).
   Inconsistencies are table rows or questions, not silent fixes.
6a. ASSET INVENTORY (v1.6.0): list every file in client/assets-intake/
   (root and subfolders, excluding slots/ and vibe/), classify by
   filename convention (logo*, hero1/2*, gallery1/2*, team*, menu*,
   before*/after* ...), and record the inventory in the Phase 0 notes /
   Photos context. Phase 4 consumes it: matching files are assigned to
   slots and pre-ticked so only genuine gaps reach the shopping list.
7. Free-text or `placeholder` Stack values are NOT blocking questions:
   write a short recommendation into state/DECISIONS.md (what will be
   built, what it is ready to accept later), marked claude-proposed, and
   proceed. Ask in QUESTIONS.md only when intent is genuinely ambiguous.

## Anti-patterns
- Filling a missing phone/address/price from the web without logging it.
  Facts enter ONLY via Overrides (owner-typed) or the Paste→Auto flow
  with its confirmation gate — never straight into the site.
- Asking vague or compound questions; re-asking facts already sitting
  [unconfirmed] in Auto instead of putting them in the table.

## Changelog
- 1.1.0 v2 intake: enrichment-first order, Gate 1 confirmation table,
  name-only blocker, unconfirmed→placeholder ship rule
- 1.0.0 initial
