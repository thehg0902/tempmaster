---
name: audience-research
description: Niche audience psychology library - personas, pains, deep
  desires, objections, decision triggers, and website conversion
  implications for 11 local-business niches (roofing, electrician,
  med-spa, physio, chiro, paving, concrete, tree service, garage door,
  kitchen-bath reno, home builder). Use at Phase 1 (architecture) and
  Phase 3 (copy) when client.md's Target Audience section is empty or
  thin. Not for visual direction (design-direction), per-client facts
  (client.md), or per-client market-research diagnostics
  (winners-writing-process).
metadata: {version: 1.0.1, category: process, tier: A}
---
# Audience Research

## Purpose
Conversion structure and copy grounded in who the visitor actually is
and what they fear/want - even when the operator pastes no research.
The studies are operator-authored (Studio Sol, Ontario market) and are
the niche-level default behind client.md's Target Audience section.

## Inputs
Detected niche (Phase 0, DECISIONS.md), client.md `## Target Audience`
(may be empty), references/<niche>.md.

## Outputs
A distilled AUDIENCE BRIEF (~12 lines) in state/DECISIONS.md, written
once at Phase 1 start; Phases 1-3 consume the brief.

## Rules
1. Match the detected niche to ONE study in references/. No exact
   match: use the closest study (a deck builder reads concrete/paving;
   an HVAC install co reads electrician) and note the adaptation in
   the brief.
2. Read the study ONCE, at Phase 1 start; distill the brief into
   DECISIONS.md: primary persona (one line), top 3 pains (their
   words), the deep desire, biggest motivator, decision trigger,
   objections to pre-answer, primary CTA + trust stack (study section
   9). Downstream phases use the BRIEF and never re-read the study
   (token economy - same pattern as vibe refs).
3. Precedence: client.md Target Audience is level 2; the study is a
   skill reference (level 7). When both exist, client-pasted facts WIN;
   the study supplies psychology depth underneath. Contradictions get
   one line in the brief, resolved toward the client's version.
4. Section 9 of every study ("Website Conversion Implications") is
   build-ready: architecture takes the CTA choice, dual-path/hero
   guidance, and trust-stack placement; copywriting takes headline
   angles and pain/desire phrasing verbatim-in-spirit.
5. The studies are Ontario-market research. Outside Ontario: keep the
   psychology (pains/desires travel), drop province-specific claims
   (WSIB, seasonality) unless the client's market matches.

## References
- references/roofing.md, electrician.md, garage-door-repair.md,
  paving.md, concrete-contractor.md, tree-service.md, home-builder.md,
  kitchen-bath-reno.md, med-spa.md, physiotherapy.md, chiropractor.md
  - identical 9-section format; section 9 is the build-notes payload.

## Anti-patterns
- Re-reading the full study at Phase 3 instead of using the brief.
- Copying study prose into site copy verbatim (it is research language,
  not customer-facing voice).
- Letting the study override client-pasted audience facts.

## Changelog
- 1.0.0 initial (v1.7.0 - operator-supplied study library, 11 niches)
