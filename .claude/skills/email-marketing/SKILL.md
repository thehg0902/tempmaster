---
name: email-marketing
description: Brevo newsletter/lead signup embed - styled form posting to a
  Brevo list, GDPR-appropriate consent line - or a provider-agnostic
  placeholder signup block. Use when Stack email-marketing is brevo,
  placeholder, or free text. Not for contact/quote forms (forms).
metadata: {version: 1.1.0, category: integrations, tier: D}
---
# Email Marketing

## Purpose
List growth for retainer-tier marketing without heavy embeds.

## Inputs
Brevo form action URL/ID from client setup (absent -> QUESTIONS.md:
create the form in Brevo, send the embed action URL).

## Outputs
Signup block (usually footer or a band section) wired to Brevo.

## Rules
1. Prefer Brevo's plain HTML form action over their script embed: style
   it with site tokens, single email field + submit, honeypot if their
   embed provides one.
2. Consent: one-line plain-language consent text + link to privacy page
   (legal-pages skill) - REQUIRED for CA/CASL context; unsubscribe is
   Brevo's job, mention "unsubscribe anytime".
3. Success/error handled inline (aria-live) if using fetch; otherwise
   Brevo's redirect back to a ?subscribed=1 param the page acknowledges.
4. One signup block per page maximum; never a popup/interstitial unless
   the client explicitly requests it (and push back once via QUESTIONS.md).
5. Double opt-in recommended to the client (deliverability) - their call,
   configured in Brevo, log the decision.
6. Placeholder mode (`email-marketing: placeholder` or provider
   undecided): render the signup block (email field + consent line +
   submit) with `action="#"` and `data-provider=""`, no vendor script.
   Comment block documents wiring later: point action at Brevo's form
   action URL (or any provider's) and set data-provider. Log in
   DECISIONS.md (claude-proposed).

## Anti-patterns
- Loading Brevo's full script sitewide for one footer form.

## Changelog
- 1.1.0 placeholder mode (provider-agnostic slot)
- 1.0.0 initial
