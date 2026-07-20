---
name: legal-pages
description: Generate privacy policy and terms pages appropriate to what the
  site actually collects (forms, analytics, booking, newsletter), Canadian
  local-business context. Use in Phase 5 when any data-collecting feature
  exists. Not legal advice - drafts for the client's review.
metadata: {version: 1.0.0, category: content, tier: E}
---
# Legal Pages

## Purpose
Honest, plain-language policies matching the site's real data practices.

## Inputs
Which Stack integrations are live (each = a disclosure), client contact
info, business jurisdiction from client.md address.

## Outputs
privacy.html (and terms.html if requested), footer-linked.

## Rules
1. Inventory-first: list exactly what is collected and by which processor
   (Formspree fields, Calendly booking data, Brevo email, GA4/Plausible
   analytics, embedded Maps). The policy describes THIS list - nothing
   generic, nothing the site doesn't do.
2. Include: what/why collected, processors named with links to their
   policies, retention in plain terms, contact for requests (client
   email), consent note for the newsletter (CASL context), cookie/local-
   storage note (hero localStorage flag counts - disclose it).
3. Plain language, short sections, same site styling - a policy page is
   still the client's brand.
4. ALWAYS append the caveat to the client in handoff: draft for review,
   not legal advice; recommend professional review for regulated niches
   (health data adjacent - dental intake etc. must NOT flow through the
   site forms; forms skill keeps fields minimal for this reason too).
5. Update trigger: any integration change on retainer = policy edit in
   the same request.

## Anti-patterns
- Boilerplate policies claiming practices the site doesn't have (worse
  than none); collecting health details via generic forms.

## Changelog
- 1.0.0 initial
