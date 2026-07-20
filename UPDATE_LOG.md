# Update Log — HUMAN READ ONLY

<!-- Claude: NEVER read, parse, or summarize this file (CLAUDE.md rule).
     This is the operator's private notebook. It is not a source of
     truth for builds; docs/CHANGELOG.md is the technical record. -->

Personal notes on why each update happened and what to remember.
Write freely — nothing here affects the pipeline.

---

## V1.7.1 — Layout preview at the design gate (2026-07-08)
The Phase 2 gate now shows me TWO pages before anything gets built:
the style preview (colors/type/vibe) and a new layout preview — the
actual home page skeleton with grey boxes labeled by asset slot,
real spacing, and the exact animations, transitions and mobile nav
the final build will use. What I approve is what gets built; QA
compares the finished page against it.

## V1.7.0 — The Audience Library (2026-07-08)
My 11 niche audience studies are now built in (roofing, electrician,
garage door, paving, concrete, tree service, home builder, kitchen &
bath, med spa, physio, chiro). When I don't paste custom research into
Target Audience, the build reads the matching study once at Phase 1
and distills an audience brief — persona, pains, motivator, objections,
CTA and trust stack — that drives the page structure and every line of
copy. My pasted research always wins over the library when both exist.

## V1.6.1 — Branch bootstrap (2026-07-07)
Fresh projects now set up their own branches: first /build creates
staging (push work-in-progress there for client previews — QA gate
doesn't block it) and deploy (the generated site-only branch hosting
pulls; renamed from "production" so the names finally make sense).
GitHub Pages and Hostinger now share the exact same deploy mechanism.

## V1.6.0 — The Intake Update (2026-07-07)
Drop files in assets-intake with sensible names (logo.png, hero1.mp4,
gallery1.jpg) and the build finds, sorts, and uses them — only what's
missing gets prompts. Placement folders are now custom per project
(Home - Hero coffee for a café, About us - Before and after for a
roofer). {Curly braces} work as my comments anywhere in client.md. New
Target Audience paste section steers the whole conversion design and
CTA wording. Claude stops narrating its thinking (conclusions only).
Plus the grid widow fix from build #2 (lone card stranded in the last
row) is now law in the CSS rules.

## V1.5.0 — Second Iteration Feedback (2026-07-07)
Fixes from build #2. Approving Higgsfield generation is now one chat
reply (name the slots, Claude records it in MEDIA_LOG) — no more file
editing. Every Claude reply during a build starts with the phase
position and ends with NEXT: so I always know what's needed. The slots
folder now has placement subfolders (Home - Hero, Contact - pictures…)
— drop the file in its folder, tick the list; anything I skip comes
back as a "want me to generate this?" question. New mobile-polish
skill: the phone version is the showpiece — sticky call bar, touch
feedback, sheet nav, slick-but-fast motion, audited first at 360px.

## V1.4.1 — Adaptive Optimization (2026-07-06)
Performance first, quality second — automatically. Ingest now starts
every image/video at high quality and only compresses harder if it
breaks the budget, so nothing gets crushed when there's headroom. The
budget itself now depends on the client's Hostinger plan (new "Hosting
plan:" field): Business has a CDN so it affords bigger assets; Premium
doesn't, so budgets tighten and browser-cache headers become mandatory.
QA now weighs every page's real bytes and names the heaviest files if
over. ffmpeg + Pillow installed — video and image slots now process
fully hands-off, no more PENDING.

## V1.4.0 — The Clear Sight Update (2026-07-06)
Big one: debugging is now visual, not code. Phase 2 generates a style
preview page (palette, contrast ratios, type, mock hero from the real
tokens) that I approve BEFORE anything gets built on top — vibe debug
at the cheapest moment. Phase 6 gained /visual-qa: Claude serves the
site, audits every page at 360/768/1280 against the design rationale
and my vibe refs, and fixes what looks wrong. Also: the QA-gate hook
was silently broken (Windows python issue) — now fixed, tested, and
fail-closed; Overrides got grouped headers + Audience; frameworks are
accepted when requested (vanilla stays the default); the operation
manual now explains every phase (what it does / what I do / what comes
out) and lint forces it to stay current.

## V1.3.4 — First-generation accuracy fields (2026-07-06)
17 more optional Overrides lines that make build #1 land closer: trust
facts (years, service area, certifications, prices, payment, 24/7),
conversion steering (primary action, search terms, languages),
integration IDs (domain, Formspree, GA4 — each one kills a mid-build
question), media policy (real-only vs AI, people yes/no), and visual
hard constraints (brand fonts, light/dark, visual avoids). Fill what I
know, skip the rest — empty lines are ignored.

## V1.3.3 — Overrides scaffold (2026-07-06)
The Overrides section in client.md now shows every field I can force as
ready-to-fill lines (contact, hours, pages markup, links, testimonials,
autonomy, all Stack flags with their known values in the comment).
Empty lines are ignored — fill only what I want, delete nothing.

## V1.3.2 — Vibe files travel (2026-07-06)
Changed my mind on the gitignore: vibe reference images are now
committed so I can work away from my laptop and still have them on any
clone or cloud session. Keep each under ~500KB (validator nags above
that). They still never ship — the deliverable is site/ only.

## V1.3.1 — The Vibe Update (2026-07-06)
client.md now has a ## Vibe section: I describe the feel I want in my
own words and drop reference images/screenshots into
client/assets-intake/vibe/ (gitignored — purely local so Claude can SEE
the aesthetic I'm going for). Claude views them once at Phase 2 and
bakes named elements into the design rationale. References never get
committed or shipped.

## V1.3.0 — The Shopping List Update (2026-07-05)
Asset creation is now streamlined: Phase 4 writes a shopping list into
client/assets-intake/slots/ with exact filenames and full ready-to-paste
Higgsfield prompts. I generate the media myself (keeps credit control),
save each file under its slot name in that same folder, then run
/ingest — it converts everything, extracts scroll-scrub frames, places
files into site/assets/, and logs it all without me touching anything.
Three new hero treatments with ready code: loop (crossfade hides the
cut), intro+loop handoff, and canvas scroll-scrub.
REMEMBER: install ffmpeg + cwebp once, or video slots come back PENDING.

## V1.2.1 — Clean deploy branch (2026-07-05)
Hostinger now pulls a generated `production` branch that contains ONLY
the site files — scripts/deploy-split.sh builds it from site/ and
proves no OS files leak. Never commit to production by hand; the script
is its only writer. Rollback = rerun the script with the previous good
commit.

## V1.2.0 — Paste-based intake (2026-07-05)
client.md v2: I just paste the business's GBP/Maps text into "Business
Profile Paste" and optionally answer Creative questions; Claude parses
facts into an Auto section and shows ONE confirmation table at Phase 0
(reply once — corrections go to Overrides). Only hard blocker is a
missing business name; unconfirmed facts ship as [PLACEHOLDER] and QA
blocks deploy until fixed. 2-minute setup per client.

## V1.1.0 — First test-run change order (2026-07-03)
Fixes from the first real client build. client.md never gets rejected
anymore — weird flag values become recommendations, and every
integration has a "placeholder" mode (build the UI, wire the provider
later). Pages can declare their sections in one line
(home | hero | about / menu | ...). The website now lives standalone in
site/ — zip it with /package, double-click index.html works. Logos keep
their transparency (PNG allowed, no more white boxes). Deploy is a
choice: manual handoff / GitHub Pages / Hostinger. Token-economy rules
added because the first run burned usage way too fast — one session per
phase, /compact between phases.

## V1.0.0 — Initial template (2026-07-02)
The starting point: CLAUDE.md constitution, 27 skills, 4 contracts,
pipeline commands (/build /qa /deploy /handoff /client-edit /lint-os),
enforcement hooks, and the validate/lint/registry scripts. One client =
one clone, only client/client.md changes.
