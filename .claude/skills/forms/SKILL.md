---
name: forms
description: Implement contact/quote forms via Formspree - markup, validation,
  spam protection, success/error UX - or a provider-agnostic placeholder
  form. Use when Stack forms is formspree, placeholder, or free text in
  Phase 5. Not for booking (booking) or newsletter signup (email-marketing).
metadata: {version: 1.1.0, category: integrations, tier: D}
---
# Forms

## Purpose
Reliable lead capture with zero backend on static hosting.

## Inputs
Stack forms flag, Formspree endpoint - Overrides "Formspree ID" and
"Form notify email" first; if absent, QUESTIONS.md: create form in
Formspree dashboard, provide the ID.

## Outputs
Form markup in the contact section + submit handling in main.js.

## Rules
1. Short forms convert: default fields name, phone OR email (niche
   playbook decides which is primary), message. Every extra field needs a
   reason in DECISIONS.md.
2. Markup: real <form action="https://formspree.io/f/{id}" method="POST">;
   works with JS disabled (Formspree hosted redirect). JS enhancement:
   fetch submit with Accept: application/json, inline success/error
   states in an aria-live region - never navigate away on success.
3. Spam: Formspree _gotcha honeypot field (visually hidden, not
   display:none-detectable pattern per their docs - verify current docs at
   integration time) + server-side filtering is theirs.
4. Validation: native required + type=email/tel + accessible error text;
   no JS validation library.
5. Notify-to address confirmed with client (QUESTIONS.md if unknown);
   test a real submission during QA click-path and note the received email.
6. NEVER commit any Formspree secrets; the public form ID is fine in
   markup.
7. Placeholder mode (`forms: placeholder` or provider undecided): build
   the complete form markup with `action="#"` and `data-provider=""` on
   the <form>, native validation intact, and a mailto: fallback link so
   leads are never lost pre-wiring. Comment block documents wiring later:
   set action to the Formspree endpoint (or any POST endpoint) and
   data-provider to its name — no markup changes needed. Log the slot in
   DECISIONS.md (claude-proposed).

## Anti-patterns
- CAPTCHAs on a 3-field local-lead form; success alert() popups.

## Changelog
- 1.1.0 placeholder mode (provider-agnostic slot)
- 1.0.0 initial
