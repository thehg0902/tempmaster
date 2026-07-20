---
name: security-basics
description: Static-site security hygiene - headers via .htaccess, form abuse
  surface, dependency/CDN integrity, secrets discipline. Use in Phase 5
  finishing and when adding any third-party script. Not legal/privacy text
  (legal-pages).
metadata: {version: 1.0.0, category: security, tier: E}
---
# Security Basics

## Purpose
A static site has a small attack surface - keep it small.

## Inputs
site/, third-party embeds in use, Hostinger Apache hosting (.htaccess).

## Outputs
.htaccess with headers; integrity attributes; a pass recorded in
BUILD_STATE.md.

## Rules
1. .htaccess (Apache on Hostinger - verify support on the plan at first
   deploy): https redirect; headers: X-Content-Type-Options nosniff,
   Referrer-Policy strict-origin-when-cross-origin, X-Frame-Options
   SAMEORIGIN (or frame-ancestors CSP), Permissions-Policy trimming
   camera/mic/geolocation. Plus long-lived caching for static assets
   (REQUIRED on no-cdn hosting profiles, good everywhere):
   mod_expires/Cache-Control: images/video/fonts 1 year immutable,
   css/js 1 week, html no-cache - asset filenames change when content
   changes (new builds), so long caches are safe.
2. CSP: for sites with embeds, start with a report-only header listing
   self + the exact third-party hosts in use (cdnjs, Calendly, Formspree,
   analytics, Maps); enforce only after the QA click-path passes under it.
3. CDN scripts: version-pinned URLs + integrity/crossorigin attributes
   where the CDN provides hashes (cdnjs does).
4. Forms: honeypot per forms skill; mailto: obfuscation not required
   (Formspree is the channel); never expose the client's personal email
   in markup if a form exists - QUESTIONS.md which address is public.
5. Secrets discipline: the pre-commit hook is the net; the rule is
   nothing secret exists to catch - IDs that are public by design
   (Formspree form ID, GA measurement ID, Calendly URL) are fine.

## Anti-patterns
- Copy-pasted mega .htaccess from the internet; enforcing CSP untested.

## Changelog
- 1.0.0 initial
