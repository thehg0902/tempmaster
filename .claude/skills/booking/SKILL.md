---
name: booking
description: Embed Calendly booking - inline widget or popup button - styled
  to the site and lazy-loaded, or a provider-agnostic placeholder slot.
  Use when Stack booking is calendly, placeholder, or free text deferring
  the provider. Not for contact forms (forms).
metadata: {version: 1.1.0, category: integrations, tier: D}
---
# Booking

## Purpose
Frictionless booking without owning a scheduling backend.

## Inputs
Calendly link from client.md Links (absent -> QUESTIONS.md), design tokens.

## Outputs
Booking section/CTA wiring with lazy-loaded Calendly embed.

## Rules
1. Default: inline embed on the contact/booking section for
   consideration niches (dental, gym); popup-button pattern when booking
   is secondary to calling.
2. Lazy facade: render a styled placeholder (btn/skeleton at the embed's
   reserved height ~700px to prevent CLS); inject Calendly's script +
   widget on near-viewport or click - never in initial page load
   (performance skill).
3. Pass utm/source params on the Calendly URL so the client can attribute
   bookings to the site.
4. Style: Calendly embed colors via its URL params matched to tokens
   (primary/text/bg hex) - keep the widget from clashing.
5. No-JS fallback: plain link to the Calendly page, always present under
   the embed.
6. QA click-path: open the real widget, step to the date screen (don't
   book), verify colors and mobile fit at 360px.
7. Placeholder mode (`booking: placeholder` or free text deferring the
   provider, e.g. "front-end only, choose software later"): build the
   booking section UI in full — heading, copy, CTA slot — plus a reserved
   embed container with a stable id and empty provider hook:
   `<div id="booking-embed" data-provider="" style-reserved height>`.
   NO external script. Add an HTML comment block documenting how to wire
   Calendly OR any other provider later (set data-provider, inject the
   vendor embed/script inside #booking-embed; keep the no-JS fallback
   link slot). Log what was built + what it accepts later in DECISIONS.md
   (claude-proposed).

## Anti-patterns
- Autoloading Calendly JS on every page; iframe with no reserved height.

## Changelog
- 1.1.0 placeholder mode (provider-agnostic slot)
- 1.0.0 initial
