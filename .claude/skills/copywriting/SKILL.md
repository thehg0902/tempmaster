---
name: copywriting
description: Write all website copy for a local small business - headlines,
  section copy, CTAs, about pages - in the client's voice, conversion-first,
  locally grounded. Use in pipeline Phase 3 and for copy edits. Not for
  meta tags/schema (seo-technical) or marketing assets like ads, emails,
  and scripts (copy-frameworks, persuasion-mechanics).
metadata: {version: 1.2.1, category: content, tier: A}
---
# Copywriting

## Purpose
Copy that sounds like the specific business, addresses its specific
audience, and moves them to the page's one conversion action.

## Inputs
client.md (Creative answers, Overrides, confirmed Auto facts; legacy v1.1
sections for old repos), architecture in DECISIONS.md, niche playbook via
design-direction rationale.

## Outputs
Final copy written directly into the page HTML (never lorem ipsum).

## Rules
1. Every page has exactly one conversion action (from architecture);
   every section's copy points toward it. When client.md has a
   `## Target Audience` section, every CTA is written FOR that
   audience - their words for what they want, their objections
   pre-answered in the adjacent copy ("book a meeting" vs "order now"
   vs "call for same-day service" are different audiences, not
   interchangeable buttons).
2. NEVER invent facts: prices, years in business, certifications, "family
   owned", guarantees, review counts. Missing proof points ->
   [PLACEHOLDER: ...] + a question in state/QUESTIONS.md.
2b. Check the Overrides accuracy fields FIRST for proof points: Years in
   business / founded, Service area, Certifications / licenses, Price
   range, Payment methods, Emergency / after-hours. A filled field is a
   confirmed owner-typed fact - use it directly; these are the cheapest
   trust lines on the site.
2c. Write to the AUDIENCE BRIEF (DECISIONS.md, distilled at Phase 1):
   headlines from its motivator + the study's headline angles, pains
   named in the audience's own words, every CTA phrased as the action
   THIS audience takes, their objections pre-answered near the CTA.
   Research prose itself never ships verbatim - it is source, not voice.
2a. Voice sources in order: the Creative answers are PRIMARY;
   review-mined differentiator language (Auto suggestions) is secondary.
   Auto facts are usable in copy only when [confirmed] — an
   [unconfirmed] phone/address/hours/price renders as
   [PLACEHOLDER: value?] per rule 2.
3. Voice from Mood adjectives (Creative; Overrides may set them too):
   write 2 candidate hero headlines in different registers, pick one,
   note the register in DECISIONS.md and keep it consistent site-wide.
4. Local grounding: mention city/neighbourhood naturally in hero-adjacent
   copy and service copy (also serves local SEO) - never keyword-stuff.
5. Benefit before feature; reading level ~grade 7; sentences short;
   scannability over cleverness for trades, more voice allowed for
   food/lifestyle niches.
6. Testimonials: verbatim only, from client.md Overrides or from Auto
   "Testimonial candidates" the operator has APPROVED (never
   [needs-approval] ones); trimmed with [...] allowed, never rewritten
   or fabricated.

## References
- references/headlines.md - hero formulas by niche intent
- references/cta.md - CTA copy by conversion type

## Anti-patterns
- "Welcome to our website" openings; "we are passionate about" filler.
- Superlatives without proof ("best in Markham").

## Changelog
- 1.3.0 audience-brief-driven headlines/CTAs/objection copy (v1.7.0)
- 1.2.0 Overrides accuracy fields as primary proof-point source (v1.3.4)
- 1.1.0 v2 intake sources: Creative primary, confirmed-Auto-only facts,
  approved testimonial candidates
- 1.0.0 initial
