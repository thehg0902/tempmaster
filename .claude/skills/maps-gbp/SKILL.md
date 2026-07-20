---
name: maps-gbp
description: Google Maps embed + Google Business Profile alignment - map on
  the contact section, directions links, NAP consistency with GBP. Use when
  client has a physical location. Not for schema markup (seo-technical owns
  JSON-LD, using data verified here) or GBP profile optimization and review
  generation (local-seo-gbp).
metadata: {version: 1.0.1, category: integrations, tier: D}
---
# Maps & GBP

## Purpose
The map is a conversion element for walk-in niches and a trust element
everywhere; GBP alignment feeds local SEO.

## Inputs
client.md Links (Maps URL, GBP), Contact address.

## Outputs
Map embed on contact, directions links, verified NAP notes for seo-technical.

## Rules
1. Embed: standard Google Maps iframe embed (no API key path) from the
   client's own Maps listing link - lazy facade pattern: static styled
   placeholder with address + "Load map" or near-viewport injection;
   reserve height (CLS).
2. "Get directions" links point to the client's actual Maps listing URL
   (from client.md), not a search query.
3. Cross-check: address/phone/name on GBP vs client.md - mismatch is a
   QUESTIONS.md item ("which is canonical?"), never silently normalized.
   The answer becomes the site-wide NAP (seo-technical rule 2).
4. Hours shown on site must match GBP hours; missing hours ->
   QUESTIONS.md.
5. Title the iframe (accessibility) and provide the address in text
   beside the map always - the map is enhancement, not the source.

## Anti-patterns
- API-key Maps JS for a single static pin; screenshot-of-map images.

## Changelog
- 1.0.0 initial
