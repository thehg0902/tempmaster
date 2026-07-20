---
name: client-enrichment
description: Parse the raw Business Profile Paste in client/client.md into
  structured business facts and write them into the Auto section. Use at
  Phase 0 whenever the Paste section is non-empty or changes. Not for
  validating structure (intake-validation) or inventing missing facts
  (never).
metadata: {version: 1.1.0, category: process, tier: A}
---
# Client Enrichment

## Purpose
Turn an unstructured GBP/Maps/old-site paste into tagged, provenance-
tracked business facts so the operator types almost nothing by hand.
Paste only — no API keys, no scraping.

## Inputs
client/client.md (`## Business Profile Paste` section).

## Outputs
Regenerated `## Auto (generated — do not hand-edit)` section in
client/client.md; suggestion comments under `## Creative`; entries in
state/QUESTIONS.md (conflicts) and state/DECISIONS.md (detected niche).

## Rules
1. Extract into the Auto section, one fact per line, each tagged with
   provenance and status: `- phone: 905-xxx-xxxx  [paste][unconfirmed]`.
   Fields to look for: name, category/niche, phone, email, address,
   hours, services, website, socials, review quotes, years/history
   claims, service area. SKIP any fact a filled Overrides field already
   answers (Name, Phone, Years in business, Service area, ...) —
   Overrides outrank Auto (schema precedence), so parsing a weaker
   duplicate only creates confirmation noise.
2. Extract ONLY what is literally present in the paste. No inference of
   facts — a review saying "fixed my AC fast" is NOT evidence of a
   "24/7 emergency" service. Unclear or conflicting items become one
   line each in state/QUESTIONS.md, never a guess.
3. Review quotes go under a `Testimonial candidates` subsection of Auto,
   verbatim with reviewer first name, each marked [needs-approval]. They
   enter the site only if the operator approves — Google reviews on a
   site should be client-confirmed.
4. Mine the paste + reviews for differentiator language and write up to
   3 one-line SUGGESTIONS under the Creative section as HTML comments
   (`<!-- suggested: known for same-day service -->`). Suggestions only —
   never auto-fill the operator's answers.
5. Idempotent: on every run, regenerate the WHOLE Auto section in place;
   never append a duplicate. Auto is machine-owned; hand edits belong in
   Overrides (which always outrank Auto).
6. Detect the niche from the GBP category line; it feeds niche-playbook
   selection in Phase 2. Log the detected niche in state/DECISIONS.md
   (claude-proposed).

## Anti-patterns
- Promoting a parsed fact straight into copy/HTML while [unconfirmed] —
  the confirmation table (Gate 1) or [PLACEHOLDER] rendering must apply.
- Editing the Overrides or Creative answers themselves.
- "Improving" review wording, merging reviews, or inventing attribution.

## Changelog
- 1.1.0 skip facts already answered by filled Overrides fields (v1.4.0)
- 1.0.0 initial (v1.2.0 change order)
