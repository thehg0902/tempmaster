---
name: site-architecture
description: Decide page map, navigation, and per-page section composition
  for a local small-business website. Use in pipeline Phase 1, or when
  adding/removing pages. Not for visual design (design-direction) or
  copy (copywriting).
metadata: {version: 1.2.0, category: process, tier: A}
---
# Site Architecture

## Purpose
Turn client.md Pages + Services + Audience into a concrete sitemap and a
section list per page that every later phase builds against.

## Inputs
client/client.md (Pages from Overrides if given; Services/Links from
Overrides or confirmed Auto; legacy v1.1 sections for old repos),
contracts/component-api.md

## Outputs
Sitemap + per-page section lists appended to state/DECISIONS.md.

## Rules
1. Pages source: Overrides when the owner specified pages (markup or
   list); otherwise propose the page map from the niche playbook —
   defaults below apply. Default for local businesses: fewer pages,
   stronger pages. If client listed only "Home", propose a single-page
   site with anchor nav
   (references/single-page.md). 5+ services with distinct search intent
   justify separate service pages (SEO), otherwise one Services page.
1a. If client.md Pages uses the markup syntax (pages separated by `/`,
   sections by `|` — see client.schema.md), that markup IS the
   authoritative page/section map. Never silently add or drop a
   user-specified page or section. The markup maps 1:1 to the
   file-structure contract layout: FIRST page group = site/ root
   (index.html), every other page group = its own folder
   (site/<page>/index.html).
1b. Compare the given sections against the niche playbook's
   `Must-have sections:` line (design-direction references). PROPOSE
   missing important ones as additions in state/QUESTIONS.md ("your niche
   usually needs X — add it? recommended yes"). If client.md Autonomy is
   `high`, default to including them, marked claude-proposed in
   DECISIONS.md, instead of asking.
2. Every page gets: purpose (one line), primary conversion action
   (call / book / form), ordered section list using standard names from
   contracts/component-api.md. Overrides "Primary action" (when filled)
   IS the site-wide default conversion action - never override it
   silently; when it is empty, DERIVE the conversion action from the
   `## Target Audience` section, and when that is empty too, from the
   Phase 1 AUDIENCE BRIEF in DECISIONS.md (distilled from the niche
   study library). Tailor section ORDER to the audience's decision
   path - objections they hold get answered before the CTA that asks
   for commitment; the brief's trust stack sits above the fold. "Target search terms" inform the
   service-page split (rule 1); "Languages" beyond one is a scope
   decision to log in DECISIONS.md before Phase 2.
3. Conversion action appears within the first viewport of every page and
   again at the bottom (cta section).
4. Nav: max 6 items; phone number always visible in header on mobile
   for call-first niches (HVAC, dental, restaurants).
5. Contact page exists whenever a physical address exists; embed map per
   maps-gbp skill flag.
6. Log the architecture in DECISIONS.md before proceeding - later phases
   treat it as level-3 precedence.

## Decision guide
| Situation | Approach |
|---|---|
| 1-3 services, walk-in business | Single page + anchors |
| Services with distinct search terms | /services/<service>.html each |
| Client insists on many thin pages | Push back once in QUESTIONS.md with SEO reasoning, then obey |

## References
- references/single-page.md - anchor-nav pattern, section order defaults
- references/multi-page.md - shared header/footer strategy, URL naming

## Anti-patterns
- Blog scaffolding for clients with no content plan.
- Deep nav hierarchies for a 6-page site.

## Changelog
- 1.2.0 v2 intake sources: Pages from Overrides, else niche-playbook
  proposal (unchanged v1.1 behavior, new source location)
- 1.1.0 pages+sections markup is authoritative; niche must-have proposals
- 1.0.0 initial
