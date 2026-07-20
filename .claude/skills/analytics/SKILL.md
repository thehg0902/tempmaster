---
name: analytics
description: Install GA4 or Plausible per the Stack flag - consent-aware,
  performance-safe, with conversion events for calls/forms/bookings - or a
  tool-agnostic placeholder event layer. Use in Phase 5 finishing, incl.
  analytics placeholder/free text. Not for SEO metadata (seo-technical).
metadata: {version: 1.1.0, category: integrations, tier: D}
---
# Analytics

## Purpose
Prove ROI to the client: track the conversions the site was built for.

## Inputs
Stack analytics flag + measurement ID / domain - Overrides "GA4 ID /
Plausible domain" first; absent -> QUESTIONS.md.

## Outputs
Tag installed on all pages + conversion events wired.

## Rules
1. Plausible: single script, defer, data-domain set - simplest and
   consent-light. GA4: gtag snippet loaded AFTER window load or first
   interaction (performance skill), never blocking.
2. Conversion events on: tel: link clicks, form success, booking widget
   open, mailto clicks - via small delegated listener in main.js emitting
   to whichever tool is installed (single wrapper fn track(name)).
3. Consent: for GA4 in CA context, load only after a lightweight consent
   notice acceptance if the client requests compliance posture; log the
   client's choice in DECISIONS.md (Claude states options, does not give
   legal advice - point to legal-pages note).
4. Verify install: after deploy, confirm live hits (realtime view) as a
   post-deploy check item - not before.
5. Never install both tools; never add heatmap/session-recording scripts
   unless explicitly requested.
6. Placeholder mode (`analytics: placeholder` or tool undecided): install
   NO tag. Keep the track(name) wrapper in main.js wired to all
   conversion events, emitting console.debug only. Comment block
   documents dropping GA4/Plausible (or any tool) into the wrapper later
   — events flow with zero markup changes. Log in DECISIONS.md
   (claude-proposed).

## Anti-patterns
- Blocking analytics in <head>; counting page_view as "conversion".

## Changelog
- 1.1.0 placeholder mode (tool-agnostic event layer)
- 1.0.0 initial
