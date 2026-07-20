---
name: seo-technical
description: Technical + local SEO - titles, meta descriptions, Open Graph,
  schema.org LocalBusiness JSON-LD, sitemap.xml, robots.txt, GBP/NAP
  consistency. Use in Phase 5 finishing pass. Not copy tone (copywriting),
  GBP embeds (maps-gbp), or GBP optimization/reviews/SEO-vs-ads strategy
  (local-seo-gbp).
metadata: {version: 1.1.1, category: seo, tier: B}
---
# SEO Technical

## Purpose
Local businesses win on local pack + a technically clean site; this skill
covers the on-site half.

## Inputs
client.md (Business, Contact, Links, Services), final pages in site/.

## Outputs
Per-page head metadata, JSON-LD, sitemap.xml, robots.txt.

## Rules
1. Title pattern: {Primary service/what} in {City} | {Business Name} -
   <= 60 chars, unique per page. Meta description <= 155 chars, contains
   the page's conversion offer. Overrides "Target search terms" (when
   filled) are the phrase source for titles; "Domain" preempts the
   domain question; "Service area" and "Price range" feed areaServed
   and priceRange in the JSON-LD.
2. NAP (name/address/phone) rendered in HTML footer/contact must match
   client.md and GBP EXACTLY, character for character
   (references/local-seo.md). NAP source: Overrides or [confirmed] Auto
   facts ONLY. Never publish an [unconfirmed] NAP fact — it stays
   [PLACEHOLDER: value?] until confirmed.
3. JSON-LD: LocalBusiness (or subtype - Dentist, Restaurant, HVACBusiness
   etc.) per references/structured-data.md; one block, on every page,
   facts only from client.md.
4. OG/Twitter: og:title, og:description, og:image (1200x630 derived from
   hero poster), og:url per page.
5. sitemap.xml lists every page as a clean folder URL with the final
   domain — `https://domain/` for home, `https://domain/about/` for
   subpages, never `/about/index.html` (ask if domain unknown ->
   QUESTIONS.md); robots.txt allows all + sitemap line.
6. Canonical tag per page uses the same folder-URL form; no duplicate
   titles/descriptions (qa should catch, but own it here).

## References
- references/local-seo.md, references/structured-data.md

## Anti-patterns
- Keyword-stuffed titles; schema claiming ratings/reviews not on the page;
  guessing the domain.

## Changelog
- 1.1.0 NAP from confirmed Auto/Overrides only; never publish
  unconfirmed NAP
- 1.0.0 initial
