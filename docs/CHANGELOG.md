# Template Changelog
## v1.10.0 - 2026-07-12 "The Control Update"
Four-verb manual control surface over where local site files go:
- /stage (new): stage-split.sh (renamed from demo-split.sh) snapshots
  the CURRENT LOCAL site/ working tree (uncommitted + untracked
  included) -> site-only staging branch + forced noindex robots.txt.
  No gates; view on the demo subdomain via manual hPanel pull.
- /save (new): commit ALL local changes + push origin/main. No gates;
  hook now exempts main pushes (previously wrongly blocked mid-build).
- /deploy (reworked): QA gate is now an ADVISORY, not a hard block -
  /deploy always runs check.py + reads BUILD_STATE/QUESTIONS/leftover
  placeholders, presents the outstanding list, and STOPs for the
  operator's explicit go. deploy-split.sh snapshots local site/ ->
  deploy branch; refuses without --force-deploy when QA isn't done
  (override recorded in BUILD_STATE notes). CLAUDE.md invariant
  reworded accordingly (operator-directed).
- /demo (reworked): bootstrap-branches.sh (both branches exist as safe
  placeholders) + first /stage push. Deploy branch content is written
  only by /deploy.
- Both splits now capture the working tree (clean-tree requirement
  dropped) and keep branch history via parent commits; `stage`/`save`
  reserved in lint-skills.py; deploy-hostinger 1.5.0.
## v1.9.0 - 2026-07-11 "The Demo Update"
Pre-QA client demos via a hosted staging branch, deployed MANUALLY by
the operator in hPanel (no webhooks or auto-deploy added):
- scripts/demo-split.sh: regenerates `staging` as a generated site-only
  branch (same subtree split + zero-OS-files check as deploy-split.sh,
  NO QA gate - demos are pre-QA by design) and forces a noindex
  robots.txt onto the demo branch so search engines never index a site
  that may still carry [PLACEHOLDER] text. --no-push flag for dry runs;
  optional commit arg like deploy-split.
- /demo command: repeatable any time site/index.html exists; pushes
  staging, operator then deploys manually in hPanel (branch `staging`
  -> demo subdomain's public folder; one-time connect documented in
  deploy-hostinger 1.4.0). Never the client's production domain.
- scripts/bootstrap-branches.sh: fresh-build bootstrap now creates
  missing staging/deploy branches as SAFE site-only placeholders
  (orphan commit: "coming soon" index.html + noindex robots.txt)
  instead of full-repo copies of HEAD - connecting hosting early can
  no longer leak OS files (client.md, state/) into a webroot.
- QA gate untouched: deploy-split.sh, /deploy, and the pre-deploy hook
  are unchanged (hook's staging exemption now documented as the demo
  path); `demo` added to the reserved command names in lint-skills.py.
## v1.8.0 - 2026-07-09 "The Copywriting Update"
Eight agency-ops skills (tier F) distilled from the operator's TRW/HU
copywriting archives, installed in the template by operator decision
(overriding ARCHITECTURE §4's user-level suggestion; they sync via git
with everything else):
- winners-writing-process: mandatory market-research diagnostic before
  any marketing asset (WWP questions, awareness/sophistication, MR
  template, avatar, top player analysis)
- persuasion-mechanics: psychology layer (value equation, attention,
  desire, curiosity, trust/belief, tribal marketing)
- copy-frameworks: drafting skeletons (DIC/PAS/HSO, long-form
  Lead/Body/Close, hooks, storytelling, refinement checklist)
- objections-and-closes: aikido moves, objection bank, CTA laddering,
  boost stack, close library
- funnel-playbooks: Google Ads lead-gen, Meta intro-offer, organic DM
  funnels + selection matrix and pricing
- local-seo-gbp: GBP optimization, review generation, local rankings,
  SEO-vs-ads logic
- cold-outreach: WOSS frame control, email/DM structure, call scripts,
  follow-up cadence
- sales-calls-and-pricing: SPIN bank, call flow, project-math pricing,
  recap emails, upsells, testimonials
Routing boundaries added both directions: copywriting 1.2.1,
audience-research 1.0.1, seo-technical 1.1.1, maps-gbp 1.0.1 point at
the new skills; build pipeline unchanged (agency-side skills, not
build phases). Deliberately excluded from the source archive: INDEX.md
(REGISTRY.md is the index) and the completed niche MRs (overlap with
the audience-research library; distillable later as a
niche-insights-vault if wanted).
## v1.7.1 - 2026-07-08
Phase 2 gate gains a LAYOUT preview beside the style preview:
preview/layout-preview.html - the home page as it will actually be
built (real section order from Phase 1, real grid/spacing via
layout-systems patterns, grey placeholder boxes labeled with the slot
that fills each, placeholder headings at real type sizes) with the
EXACT animation/transition/mobile-nav code Phase 5 will ship (same
css-only/gsap patterns, same tokens, mobile-polish behaviors). Claude
self-checks it on the preview server before presenting. The approved
layout preview is BINDING: layout-systems 1.2.0 reproduces it in
Phase 5 (deviations logged), and /visual-qa compares the built home
page against it.
## v1.7.0 - 2026-07-08 "The Audience Library"
Operator-supplied niche audience studies integrated (11 niches:
roofing, electrician, garage-door repair, paving, concrete, tree
service, home builder, kitchen-bath reno, med spa, physiotherapy,
chiropractor - identical 9-section format ending in Website Conversion
Implications; Ontario market):
- New audience-research skill (tier A): matches the detected niche to
  ONE study, reads it once at Phase 1, distills a ~12-line AUDIENCE
  BRIEF into DECISIONS.md (persona, top pains, deep desire, motivator,
  decision trigger, objections, CTA + trust stack). Downstream phases
  use the brief only (distill-once pattern).
- Precedence: client.md Target Audience outranks the library; studies
  fill the gap when the operator pastes nothing.
- Consumers wired: site-architecture (conversion action + section
  order + trust stack), copywriting 1.3.0 (headline angles, pains in
  the audience's words, objection-answering near CTAs),
  design-direction (emotional register steers no-playbook adaptation),
  build.md Phase 1 (brief distilled before the page map).
## v1.6.1 - 2026-07-07
Branch bootstrap: a fresh /build (Client unset) auto-creates `staging`
(preview branch - QA-gate EXEMPT for client previews, never connected
to hosting) and `deploy`, pushing both when origin is configured. The
generated site-only branch is RENAMED production -> deploy everywhere
(deploy-split.sh, deploy-hostinger, /deploy, build.md, manual diagram);
GitHub Pages now reuses the same generated deploy branch (one deploy
mechanism for both hosts). Hook: pushes naming staging are exempt
unless deploy/production is also named.
## v1.6.0 - 2026-07-07 "The Intake Update"
Six operator changes from build #2 continued:
1. Intake asset sweep: Phase 0 inventories client/assets-intake/
   (logo*, hero1/2*, gallery1/2*, team*, before*/after* naming);
   Phase 4 moves matching files into placement folders, pre-ticks
   their slots (model=client, credits 0) - only gaps get prompts.
2. {Curly-brace} operator comments valid anywhere in client.md -
   stripped globally before parsing (validator, ingest, check.py).
3. Placement folders are PER-PROJECT: named from this site's actual
   page/section map + niche (Home - Hero coffee / About us - Before
   and after), not a fixed set; created empty for drag-and-drop.
4. New `## Target Audience` paste section: site-architecture derives
   the conversion action + section order from it (when Primary action
   is unset); copywriting tailors every CTA to what this audience is
   looking for.
5. Token economy: never narrate reasoning into chat - conclusions only.
6. Grid widow rule: css.md + layout-systems rule 3 - auto-fit strands
   a lone last card when count mod columns = 1; use explicit columns
   or span/center the last item.
## v1.5.0 - 2026-07-07 "Second Iteration Feedback"
Four operator-requested changes from real build #2:
1. In-chat Higgsfield approval: the operator can approve NAMED slots in
   chat; Claude transcribes `YES [in-chat <date>]` to MEDIA_LOG. Hard
   invariant reworded (CLAUDE.md, media-log contract rule 1,
   media-generation rule 1) - blanket permission still never counts.
2. Terminal protocol (CLAUDE.md, always-on): every reply starts
   `[Phase N - name | status]` and ends with `NEXT (you/me): ...` -
   the operator always knows where the build is and what's required.
3. Placement folders + tick semantics (asset-slots v1.1.0): Phase 4
   creates slots/<Page> - <Section>/ folders; list blocks carry a
   folder: line; operator drops the file in its folder and ticks [x].
   /ingest matches recursively by filename (root still works,
   duplicates = conflict), warns on tick-without-file, and lists
   UNFILLED slots as Higgsfield candidates for in-chat approval.
4. New mobile-polish skill (tier B, default-on): phone experience as
   the showpiece - thumb-zone CTAs/sticky action bar, 44px targets,
   16px inputs, :active touch feedback, sheet-style mobile nav, svh +
   safe-area correctness, shorter/faster mobile motion; wired into
   build.md Phase 5 and audited FIRST in the /visual-qa 360 pass.
## v1.4.1 - 2026-07-06 "Adaptive Optimization"
Quality-first within the performance budget, tuned to the hosting plan:
- Priority law (performance rule 0): load/interaction targets are hard
  floors; media quality is maximized WITHIN them.
- Hosting budget profiles via new Overrides "Hosting plan:" field:
  cdn (hostinger-business/cloud: page 1.5MB, hero 2.5/4MB, scrub 10MB)
  vs no-cdn (premium/unknown, fail-safe: 1.0MB, 2/3MB, 8MB + REQUIRED
  Cache-Control headers - block added to security-basics; CDN/cache
  post-deploy checks added to deploy-hostinger).
- /ingest quality ladders: images q90->q82->q75, video CRF 20->23->26,
  scrub 12fps/q80->q70->10fps - each steps down ONLY while over its
  profile budget; report shows kept level + headroom. Pillow fallback
  for images (no cwebp needed); video/scrub/posters need only ffmpeg
  (direct WebP encode).
- check.py page-weight audit: sums each page's real referenced asset
  bytes vs profile caps; FAIL over cap with heaviest-3 named, WARN >80%.
- visual-qa: rendered waste checks (img naturalWidth > 2x displayed,
  below-fold images missing lazy).
- Machine: ffmpeg + Pillow installed - full ingest now runs hands-off.
## v1.4.0 - 2026-07-06 "The Clear Sight Update"
Full-system consistency audit + visual-first debugging:
- Consistency fixes: stale animations.js/hero.js refs (css-only,
  loading-strategy), component-api rule 4 -> shared/main.js (v1.1.0),
  enrichment skips Overrides-answered facts, schema/scaffold sync.
- HOOKS FIXED: python3-based extraction silently failed on Windows ->
  pure-bash extraction, CLAUDE_PROJECT_DIR paths, timeouts, FAIL-CLOSED
  deploy gate; 8 unit tests pass (block/allow/exemption/fail-closed).
- Overrides regrouped under ### sub-headers (Identity/Facts/Conversion/
  Integrations/Media policy/Visual/Stack/Meta) + Audience field added;
  Photos vs Photos-policy disambiguated.
- NEW Phase 2 gate: scripts/generate-style-preview.py renders
  preview/style-preview.html from real tokens (palette, live WCAG
  contrast ratios, type scale, spacing, mock hero) - approve the vibe
  before phases 3-5. Never ships (outside site/, gitignored).
- NEW visual-qa skill (/visual-qa): rendered audit per page at
  360/768/1280 against layout checklist + design rationale + vibe refs;
  wired into /qa as mandatory layer 2; .claude/launch.json preview
  servers added.
- check.py: viewport meta, stylesheet order, img width/height (CLS),
  per-page CSS size + token-bypass warnings.
- Framework acceptance: Stack `framework:` flag (vanilla default,
  react-cdn/tailwind-cdn known, any request honored - never rejected);
  file-structure v2.1.0 Framework exception (CDN+SRI or app/ -> site/).
- OPERATION_MANUAL: full per-phase rundown (does/you/input/outcome) +
  "Last updated" stamp now lint-enforced like the README title.
## v1.3.4 - 2026-07-06 "First-generation accuracy fields"
17 new optional Overrides fields, each with a named consumer:
- Trust facts (copywriting + JSON-LD): Years in business / founded,
  Service area, Certifications / licenses, Price range, Payment
  methods, Emergency / after-hours.
- Conversion steering (site-architecture + seo-technical): Primary
  action (call|book|form|visit|order), Target search terms, Languages.
- Integration IDs (each preempts a QUESTIONS.md stop): Domain,
  Formspree ID, Form notify email, GA4 ID / Plausible domain.
- Media policy (media-generation hard constraints): Photos policy
  (real-only|ai-allowed|mix), People in imagery (yes|no).
- Visual hard constraints (design-direction/tokens): Brand fonts,
  Color mode (light|dark|either), Avoid (visual).
Consumption rules added to copywriting (1.2.0), seo-technical,
site-architecture, media-generation, design-direction, forms,
analytics. Empty values ignored as before.
## v1.3.3 - 2026-07-06
Overrides scaffold: client.md's Overrides section now lists every
available field (contact/hours/services, Pages markup, Links,
Testimonials, Photos, Competitors, Style references, Special requests,
Autonomy, all 7 Stack flags) as ready-to-fill bullet lines with known
values documented in the comment block. Empty values are ignored
everywhere - validator treats an empty flag as unset (no noise), and
the flags-present check now requires a non-empty value.
## v1.3.2 - 2026-07-06
Vibe references are now COMMITTED (gitignore rule removed): operator
works from multiple machines/cloud sessions, so vibe context must
travel with the repo. Deliverable safety unchanged - deploy-split and
/package prove nothing outside site/ ships. Validator adds a SOFT
size nudge for vibe images over 500KB. Docs/schema/client.md wording
updated.
## v1.3.1 - 2026-07-06 "The Vibe Update"
Website vibe as first-class intake:
- client.md gains an optional `## Vibe` section (v2 and v1.1 formats):
  free-text feel description + reference images listed as
  `- vibe/<file>: what to take from it`.
- New drop zone client/assets-intake/vibe/ - GITIGNORED: local-only
  context so Claude understands the aesthetic; never committed, never
  shipped, never copied into site/.
- design-direction 1.2.0: views each vibe image ONCE at Phase 2,
  distills named elements into the DECISIONS.md rationale (the artifact;
  images never re-read - token economy). Vibe outranks playbook
  aesthetics (client.md precedence); playbook conversion must-haves and
  the inspiration-not-duplication rule still apply.
- Validator: SOFT notes for referenced-but-missing vibe images and
  unlisted images on disk; VIBE summary line.
## v1.3.0 - 2026-07-05 "The Shopping List Update"
Streamlined asset creation:
- New contract contracts/asset-slots.md: slot naming grammar, treatment
  vocabulary (loop, intro-loop, scroll-scrub, image, alpha),
  SHOPPING_LIST.md format, MEDIA_LOG mirroring, scrub manifest schema.
- Phase 4 now writes client/assets-intake/slots/SHOPPING_LIST.md - exact
  slot filenames + full copy-paste Higgsfield prompts; operator manual
  generation is the default path (credits 0); paid auto-generation stays
  behind the unchanged approval invariant.
- New /ingest command + scripts/ingest-assets.py: matches slots/ against
  the list, re-encodes video + posters, extracts scroll-scrub frame
  sequences + manifest.json, WebP-converts images (alpha passthrough),
  places outputs per file-structure, ticks the list, updates MEDIA_LOG,
  reports missing/unknown/over-budget. Idempotent.
- hero-media 1.1.0: three new templates - loop-crossfade.js (rAF
  dip-to-black loop), intro-loop.js (intro->loop handoff),
  scrub-player.js (canvas scroll-scrub with progressive frame loading) +
  references/scroll-scrub.md.
- performance: scrub sequence budget (<=10MB, progressive after first
  paint). hero-media flag values extended (loop | intro-loop |
  scroll-scrub). Slot media gitignored; SHOPPING_LIST.md tracked.
- Phase 5 may optionally build with poster placeholders while slots fill.
## v1.2.1 - 2026-07-05
Clean deploy branch: Hostinger auto-deploy now pulls a generated
`production` branch containing ONLY site/ contents at its root.
- New scripts/deploy-split.sh: preconditions (clean tree, site/index.html,
  qa done), `git subtree split --prefix site`, cleanliness check that
  FAILS if any OS path (CLAUDE.md, .claude/, contracts/, state/, scripts/,
  client/, docs/) appears in the split, force-push to production; optional
  commit arg for rollback; graceful no-remote mode.
- deploy-hostinger skill: hPanel points at `production`/public_html (branch
  root IS the site); deploy = run the script; anti-pattern amended to
  "never commit manually to production"; rollback via commit arg;
  first-pull File Manager cleanup checklist item.
- /deploy command routes the Hostinger path through the script.
- pre-deploy-qa-gate hook: matches "deploy-split" too (a `bash
  scripts/deploy-split.sh` command line contains no "git push"); script
  re-checks QA itself.
- OPERATION_MANUAL: Phase 7(c) + deployment rundown diagram
  (main = everything, production = generated site-only, hosting = mirror).
## v1.2.0 - 2026-07-05
Client intake overhaul (paste-based), six changes:
1. client.md v2: Creative / Overrides / Business Profile Paste / Auto;
   every field optional; only blocker = no business name anywhere;
   in-file precedence Overrides > Auto[confirmed] > Auto[unconfirmed]
   (noted in CLAUDE.md ladder level 2).
2. New client-enrichment skill: parses the paste into tagged Auto facts
   ([paste][unconfirmed]), literal-extraction-only, testimonial
   candidates [needs-approval], up to 3 Creative suggestions as HTML
   comments, idempotent regeneration, niche detection → DECISIONS.md.
3. Phase 0 = enrich → validate → ONE confirmation table (Gate 1);
   corrections → Overrides, confirmations → [confirmed]; unconfirmed
   phone/address/hours/prices ship as [PLACEHOLDER] (qa blocks deploy).
4. Validator rewrite: v2 section model, name-only blocker, SOFT notes
   (empty Creative/Paste, missing flags, unparsed paste), v1.1 files
   still validate under old rules, facts summary line.
5. Downstream skills updated: copywriting (Creative primary voice,
   confirmed-facts-only, approved testimonials), design-direction
   (detected niche + Creative mood), site-architecture (Overrides pages
   else playbook), seo-technical (never publish unconfirmed NAP),
   intake-validation (confirmation-table flow).
6. Docs: OPERATION_MANUAL §2/§3/§5/§6 (2-minute setup, Gate 1 table),
   README quick-start, this changelog.
Also: pre-deploy-qa-gate hook gains an OS-maintenance exemption — push
is allowed while no build has started (phase 0 pending); the QA gate
applies unchanged the moment a build is in progress.
## v1.1.0 - 2026-07-03
Change order from the first real test run, six changes:
1. Flags recommend-never-refuse: interpretation principle in CLAUDE.md;
   Stack flags free-text with `placeholder` universal value; unrecognized
   values downgraded BLOCKER->SOFT; placeholder modes in booking, forms,
   email-marketing, analytics; intake writes recommendations to DECISIONS.
2. Pages markup syntax (`page | section / page2 | ...`) documented in
   schema, parsed by validator (malformed = SOFT + corrected reading);
   site-architecture treats it as authoritative, proposes niche must-have
   sections (machine-readable line added to all 5 playbooks).
3. Standalone deliverable: src/+assets/ replaced by site/ (home at root,
   one folder per page, shared/ + assets/ single-sourced); contracts,
   skills, QA script, commands updated; new /package command zipping
   site/ contents to deliverables/ (gitignored).
4. Alpha assets never flattened: PNG explicitly permitted (perf exemption);
   optimize.sh auto-detects alpha and passes PNG through with a printed
   alpha-preservation check.
5. Deploy is a three-way choice at Phase 7 (manual /package, GitHub Pages
   via new reference, Hostinger); manual path ends the workflow at phase 7;
   Phase 8 optional after manual.
6. Token economy: CLAUDE.md section replaced/strengthened; new
   token-economy skill (unverified-savings note included); operator
   practices in OPERATION_MANUAL §11. docs/OPERATION_MANUAL.md created
   (did not previously exist).
## v1.0.0 - 2026-07-02
Initial Agency OS template: constitution CLAUDE.md, 27 skills (tiers A-E),
4 contracts, pipeline commands (/build /qa /deploy /client-edit /handoff
/lint-os), path-scoped rules, 2 enforcement hooks, validation/lint/registry
scripts. Per-client usage: replace client/client.md, run /build.
