---
name: design-direction
description: Translate client mood adjectives + niche into a concrete visual
  direction (style, imagery, layout personality) before any tokens or code.
  Use in pipeline Phase 2 before design-tokens. Not for producing CSS
  (design-tokens does that).
metadata: {version: 1.2.0, category: design, tier: A}
---
# Design Direction

## Purpose
Prevent generic template-looking output by committing to a specific,
client-appropriate visual direction and writing it down before building.

## Inputs
client/client.md (Mood from Creative; the Vibe section; niche from
Overrides if specified, else Auto's detected category; Brand/Style
references from Overrides; legacy v1.1 sections for old repos), vibe
reference images in client/assets-intake/vibe/, niche playbook in
references/.

## Outputs
A 10-line design rationale in state/DECISIONS.md: direction name, type
pairing intent, color intent, imagery style, layout personality, motion
level.

## Rules
1. Read the matching niche playbook in references/ first; it encodes what
   converts for that business type. Niche source: Overrides when the
   owner specified one, else the detected category logged in
   DECISIONS.md at Phase 0. No playbook for the niche: use the closest
   one and note the adaptation in DECISIONS.md - the audience brief's
   emotional register (fear-relief vs aspiration vs trust) also steers
   that adaptation.
2. Mood adjectives (the Creative section's Mood line) are the brief. "Warm, premium, trustworthy" and
   "bold, energetic, young" must produce visibly different sites. Name
   the direction (e.g. "quiet luxury", "craft workshop", "clinical calm").
3. Client brand colors (if given) are constraints, not the whole palette -
   design-tokens expands them into the full token set. Same for the
   Overrides hard constraints: "Brand fonts" (use them, don't propose),
   "Color mode" (light | dark | either - decides the base scheme), and
   "Avoid (visual)" (negative constraints outrank any playbook or Vibe
   suggestion).
4. Decide imagery style here (photo-real warm / editorial / illustrative)
   so media-generation prompts stay consistent.
5. Pick ONE distinctive element per site (typography scale, unusual hero
   treatment, signature section shape). One, not five.
6. Motion level (none / subtle / expressive) must match both mood and the
   Stack animation flag; conflict goes to QUESTIONS.md.
7. Vibe references (client.md ## Vibe + images in
   client/assets-intake/vibe/): view each image ONCE, here at Phase 2,
   and distill what to take from each into the rationale as NAMED
   elements ("glassy pill nav", "serif-italic display over dark video" -
   never "looks nice"). The rationale is the artifact: never re-read the
   images in later phases (token economy). Vibe is part of client.md
   (precedence level 2): it outranks playbook aesthetics; playbook
   conversion must-haves still apply. Inspiration, never duplication -
   no wholesale copying of a reference's layout.

## References
- references/coffee-shop.md, restaurant.md, gym.md, hvac.md, dental.md

## Anti-patterns
- Defaulting to the same palette/typeface across clients.
- Trend-chasing that fights the niche playbook (brutalism for a dentist).

## Changelog
- 1.2.0 vibe references: view once, distill to named elements (v1.3.1)
- 1.1.0 v2 intake sources: Mood from Creative, niche from detected
  category when Overrides silent
- 1.0.0 initial
