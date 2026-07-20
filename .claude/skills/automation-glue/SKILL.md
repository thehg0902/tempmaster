---
name: automation-glue
description: Wire Make/Zapier automations around site events - form lead to
  CRM/sheet/notification pipelines. Use when the client's package includes
  lead automation or client.md Special requests mention it. Not for the
  on-site form markup (forms).
metadata: {version: 1.0.0, category: integrations, tier: D, optional: true}
---
# Automation Glue

## Purpose
Turn site leads into the client's workflow (email, sheet, CRM, SMS)
without custom backend.

## Inputs
Which events exist on the site (Formspree submissions, Calendly bookings,
Brevo signups), client's desired destination.

## Outputs
A documented automation design in DECISIONS.md + setup steps for the
human (these run in Make/Zapier dashboards, not in this repo).

## Rules
1. Source triggers: Formspree -> webhook/native app; Calendly -> native
   app; Brevo -> native app. Prefer native app triggers over polling.
2. Design the scenario as: trigger -> filter (spam/test) -> destination(s)
   -> notification. Document field mapping explicitly.
3. Claude does NOT log into Make/Zapier or handle credentials: produce
   the exact click-path setup doc; the human executes; webhook URLs are
   secrets - referenced by name, never committed (CLAUDE.md invariant).
4. Always include a test-lead step in the doc and a "verify received"
   checkbox before marking the automation live in DECISIONS.md.
5. Keep scenarios single-purpose; two goals = two scenarios (debuggable,
   billable separately).

## Anti-patterns
- Webhook URLs in the repo; polling triggers when native apps exist.

## Changelog
- 1.0.0 initial
