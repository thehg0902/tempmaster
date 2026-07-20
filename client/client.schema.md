# client.md Schema  (v2 — paste-based; Vibe added in template v1.3.1)

Validated by scripts/validate-client-md.py. Two formats are accepted:

OPERATOR COMMENTS (v1.6.0): anything inside curly braces `{like this}`
anywhere in client.md is an operator comment — stripped before ANY
parsing (validator, enrichment, skills) and never treated as content.
Use freely for notes-to-self next to any field; multi-line allowed.

- **v2 (this schema):** sections Creative / Overrides / Business Profile
  Paste / Auto. ALL sections optional.
- **v1.1 (legacy):** if the old `## Business` / `## Contact` headers are
  found, the validator applies the v1.1 rules unchanged (old client repos
  keep working). The v1.1 field reference is preserved at the bottom of
  this file because Overrides reuses it.

## v2 sections (in this order)

### `## Creative` (optional — the only hand-written part)
Free answers to: what makes the business better than competitors; the
story / why they started; ideal customer; offer / guarantee / promo;
Mood (3-6 adjectives); never say / avoid. Empty lines are skipped.
Fully empty Creative = SOFT note (validator lists which questions would
most improve the result for the detected niche), then proceed on
niche-playbook defaults.

### `## Vibe` (optional — the website's intended feel)
Free text describing the feel (sites admired, energy, era, textures) +
reference images dropped into `client/assets-intake/vibe/`. The folder
is COMMITTED (v1.3.2) so vibe context travels with the repo to remote
machines and cloud sessions — compress each image to ~500KB (validator
nudges above that). Context only: never shipped, never copied into
site/ (deploy-split and /package prove the deliverable is site/-only).
List each as `- vibe/<file>: what to take from it`. design-direction
reads the images ONCE at Phase 2 and distills them into the
DECISIONS.md rationale. Missing referenced files and unlisted images in
the folder are SOFT notes. Also accepted as an optional section in
v1.1-format files.

### `## Target Audience` (optional — paste zone for audience research)
Paste anything about WHO the site must convince and WHAT they are
looking for: demographics, pain points, search intent, objections,
what makes them pick one business over another. Free text, any length.
Consumers: site-architecture derives the primary conversion action and
section order from it (book / order / call — whatever this audience
actually does), and copywriting tailors every CTA and objection-
handling line to it. The one-line Overrides `Audience:` field remains
for quick use; this section is the deep version and wins when both
exist (more specific beats more general).

### `## Overrides` (optional — owner-typed facts, beats everything)
Anything from the v1.1 field reference below, any subset, same syntaxes:
Name, Phone, Email, Address, Hours, Services, Pages (incl. the
`page | section / page2 | ...` markup), Brand colors, Logo path, Stack
flags (free text; universal `placeholder` value), Links, Testimonials,
Photos, Audience, Competitors, Style references, Autonomy, Special
requests. Links may equivalently be split into sub-lines (Google Maps /
Google Business Profile / Socials / Existing website / Booking link),
which is how the template scaffolds them.
The template scaffolds all of these as ready-to-fill bullet lines,
grouped under ### sub-headers (Identity & contact / Content facts /
Conversion & SEO / Integrations / Media policy / Visual constraints /
Stack flags / Meta — v1.4.0). ### headers are cosmetic only: the
validator splits sections on ## and ignores colon-less lines. A line
with an EMPTY value is ignored everywhere (validator, enrichment,
skills); no need to delete unused lines. "Photos (what exists /
what's needed)" is the asset inventory; "Photos policy" under Media
policy is the AI-generation constraint — different fields.

Accuracy fields (v1.3.4) — each has a named consumer; all optional,
free text, empty = ignored:
- Years in business / founded, Service area, Certifications / licenses,
  Price range / starting price, Payment methods, Emergency / after-hours
  → copywriting (trust facts, never inventable) + seo-technical
  (areaServed, priceRange in JSON-LD) + niche must-haves (24/7 badge
  only if Emergency says so).
- Primary action (call | book | form | visit | order), Target search
  terms, Languages (en | en+fr | ...) → site-architecture (per-page
  conversion action, service-page split, language scope) +
  seo-technical (title tags).
- Domain, Formspree ID, Form notify email, GA4 ID / Plausible domain
  → seo-technical (sitemap/canonicals), forms, analytics; each filled
  field preempts a QUESTIONS.md stop.
- Hosting plan (hostinger-business | hostinger-premium | free text)
  → selects the performance BUDGET PROFILE (v1.4.1): business/cloud =
  cdn profile (page 1.5MB, hero video 4MB cap); premium/other/EMPTY =
  no-cdn profile, fail-safe tighter (page 1.0MB, 3MB cap, required
  cache headers). Consumed by /ingest's quality ladder, check.py's
  page-weight audit, performance + deploy-hostinger skills.
- Photos policy (real-only | ai-allowed | mix), People in imagery
  (yes | no) → media-generation (what may be generated at all).
- Brand fonts, Color mode (light | dark | either), Avoid (visual)
  → design-direction + design-tokens (hard constraints; Vibe stays
  the soft feel channel).

### `## Business Profile Paste` (optional — raw dump zone, LAST input)
Paste anything: GBP about panel, Google Maps listing text, hours block,
services list, reviews, the business's old website text, socials.
Unstructured is fine. No API keys, no scraping — paste only. The
client-enrichment skill extracts facts from here into Auto at Phase 0.

### `## Auto (generated — do not hand-edit)` (machine-owned)
Written by client-enrichment. One fact per line with provenance + status
tags: `- phone: 905-xxx-xxxx  [paste][unconfirmed]`. Statuses:
`[unconfirmed]` → `[confirmed]` after the operator confirms at Gate 1.
Review quotes live in a `Testimonial candidates` subsection, marked
`[needs-approval]`. Hand edits belong in Overrides, never here;
enrichment regenerates the whole section on each run.

## Blocking rule (the ONLY Phase 0 BLOCKER)
No business name found anywhere — no Name in Overrides, no plausible name
in Paste, and Auto empty. Everything else missing = SOFT.

## Precedence within client.md
Overrides (owner-typed)
  > Auto [confirmed] (parsed from paste, operator-confirmed)
  > Auto [unconfirmed] (parsed, not yet confirmed).
Unconfirmed facts may drive design and copy DRAFTS, but ship as
`[PLACEHOLDER: value?]` in HTML until confirmed — the qa-review script
fails on placeholders, so nothing unverified can ship. This ladder is
also noted in CLAUDE.md (precedence level 2 sub-note).

---

## v1.1 field reference (used by Overrides; full rules for legacy files)

- `## Business`        - name, niche, one-line description
- `## Contact`         - phone, email, address (or "no physical address")
- `## Services`        - bullet list, at least one
- `## Pages`           - two accepted formats:
    (a) Markup (preferred): one line; pages separated by `/`; within a
        group the FIRST token is the page, following `|` tokens are its
        sections. Example:
          Pages: home | hero | about | services | contact / menu | menu-list | gallery
        = 2 pages: home (sections hero, about, services, contact) and
        menu (sections menu-list, gallery).
    (b) Plain list (legacy): comma or bullet list of page names, each
        treated as a separate page; sections decided in Phase 1.
    Malformed markup is interpreted, never rejected (interpretation
    principle) - the validator prints its corrected reading as a SOFT note.
- `## Brand`           - colors (hex or "none - propose"), logo path in
                          client/assets-intake/ or "none - text logo"
- `## Audience`        - who the site must convince
- `## Mood`            - 3-6 adjectives
- `## Stack`           - flags, one per line, exact keys. Values are FREE
                          TEXT. The lists below are KNOWN values with
                          defined behavior — recommended, not an enum.
                          ANY other text is intent to interpret: Claude
                          recommends an approach and logs it in
                          state/DECISIONS.md (claude-proposed). Every flag
                          also accepts the universal value `placeholder`
                          = build the front-end section/slot with no
                          third-party integration, wire-ready for any
                          provider later.
    animation: gsap | css-only | none | placeholder
    3d: yes | no | placeholder
    booking: calendly | none | placeholder
    forms: formspree | none | placeholder
    email-marketing: brevo | none | placeholder
    analytics: ga4 | plausible | none | placeholder
    hero-media: video | loop | intro-loop | scroll-scrub | image-sequence
                | static | propose | placeholder
                (loop/intro-loop/scroll-scrub are asset-slot treatments -
                 see contracts/asset-slots.md; media arrives via the
                 Phase 4 shopping list + /ingest)
    framework: vanilla | react-cdn | tailwind-cdn | any other = interpret
               (vanilla is the default and preference; a requested
                framework is ACCEPTED per the file-structure contract's
                Framework exception - never rejected)
  A missing flag key is a soft gap defaulting to `propose`.
- `## Links`           - Google Maps URL, Google Business Profile, socials,
                          existing website, booking link
- `## Testimonials`    - verbatim quotes with attribution
- `## Photos`          - what exists in assets-intake, what must be generated
- `## Competitors`     - names/URLs
- `## Style references`- sites the client likes/dislikes
- `## Special requests`- anything unique
- `## Autonomy`        - low | normal | high (default normal). high relaxes
                          non-safety gates; media approval gate ALWAYS holds.

Legacy blocking (v1.1 files only): the eight sections Business through
Stack are REQUIRED; missing or TODO blocks Phase 0. In v2 nothing is
required except a findable business name.
