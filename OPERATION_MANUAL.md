# Agency OS — Operation Manual

Last updated: v1.10.0
(The lint script fails if this stamp lags the CHANGELOG — every update
must review this manual, especially the §3 phase rundown.)

Operator-facing guide. (Created at v1.1.0 — earlier versions had no
manual; §-references in change orders resolve here.)

## §1 What this is
One repo clone = one client website build, driven by Claude Code.
The OS (CLAUDE.md, .claude/, contracts/, state/, scripts/) never ships;
the deliverable is the standalone `site/` folder.

## §2 Per-client workflow (2-minute setup)
Clone → in `client/client.md`: paste the business's GBP/Maps text into
**Business Profile Paste**, paste audience research into **Target
Audience** (drives conversion structure + CTA wording), use {curly
braces} anywhere for notes-to-self, and answer whatever you can under
**Creative**
(everything optional; type corrections/specifics under **Overrides**;
describe the intended feel under **Vibe** and drop reference
images/screenshots into `client/assets-intake/vibe/` — committed, so
they travel to remote machines; compress to ~500KB each; viewed once at
Phase 2, never shipped) → drop assets in `client/assets-intake/` →
open Claude Code → `/build` → answer gates.

## §3 Pipeline phases — full rundown

| # | phase | gate |
|---|-------|------|
| 0 | intake | HUMAN: confirm table |
| 1 | architecture | - |
| 2 | design | HUMAN: approve style preview |
| 3 | content | - |
| 4 | media | HUMAN: fill slots (or approve paid gen) |
| 5 | build | - |
| 6 | qa | script + visual QA must pass |
| 7 | deploy | HUMAN: choose + confirm |
| 8 | handoff | - |

**Phase 0 — intake.**
Does: inventories your dropped files in client/assets-intake/ (name
them by convention: logo.png, hero1.mp4, gallery1.jpg... and they get
used automatically); client-enrichment parses your Business Profile
Paste into tagged Auto facts; the validator checks structure; you get
ONE confirmation table in chat.
You: reply once — "all good" or corrections (corrections land in
Overrides). Only hard blocker: no business name found anywhere.
Input: client/client.md (Creative, Vibe, Overrides, Paste).
Outcome: confirmed facts in client.md Auto; questions (if any) in
state/QUESTIONS.md; phase 0 done in BUILD_STATE.

**Phase 1 — architecture.**
Does: distills an audience brief from the niche study library (11
niches; skipped when your Target Audience paste is already rich), then
turns Pages markup (or proposes a page map) + niche must-haves + the
brief's conversion guidance into a sitemap and per-page section lists.
You: nothing, unless it proposes adding a niche must-have section —
answer in QUESTIONS.md (auto-included at Autonomy: high).
Input: client.md Pages/Primary action/Languages, niche playbook.
Outcome: page map + section lists in state/DECISIONS.md.

**Phase 2 — design (gate).**
Does: design-direction translates mood + Vibe refs + niche into a named
direction; design-tokens writes site/shared/tokens.css; then TWO
preview artifacts: preview/style-preview.html (palette with live WCAG
contrast ratios, type scale, spacing, mock hero — scripted) and
preview/layout-preview.html (the home page as it will be built: real
section order, real grid and spacing, grey placeholder boxes labeled
with the asset slot that fills each one, and the EXACT animations,
transitions, and mobile-nav behavior Phase 5 will ship). Claude
self-checks both on the preview server against your vibe refs first.
You: open both files — judge the VIBE on one and the LAYOUT + MOTION
on the other; approve or say what's off. The approved layout preview
is binding for the build. 5 minutes here saves 5 phases of rework.
Input: Vibe section + images, Mood, Brand fields, niche playbook.
Outcome: tokens.css + 10-line design rationale in DECISIONS.md +
approved style preview; phase 2 done.

**Phase 3 — content.**
Does: copywriting writes final copy into page HTML skeletons, using
Creative answers as the voice and Overrides accuracy fields as proof
points; unconfirmed facts render as [PLACEHOLDER].
You: nothing (answer any new QUESTIONS.md entries when convenient).
Input: confirmed facts, Creative, architecture, design rationale.
Outcome: every section of every page has real copy in site/.

**Phase 4 — media (gate).**
Does: media-generation writes the shopping list — exact slot filenames,
treatments, specs, full copy-paste Higgsfield prompts.
You: generate at your pace, drop each file into its placement folder
(slots/<Page> - <Section>/) under the exact slot name, tick [x] on the
list, run /ingest. Slots you skip come back as Higgsfield candidates —
approve them with one chat reply naming the slots. Optionally let the
build proceed with poster placeholders.
Input: design rationale imagery style, section list, hero-media flag.
Outcome: processed assets in site/assets/ at the highest quality the
performance budget allows (adaptive ladder, tuned to the Hosting plan
field; + scrub manifests), MEDIA_LOG
rows in-use, list ticked.

**Phase 5 — build.**
Does: layout-systems + components + hero-media treatments +
frontend-animation + mobile-polish (phone experience as the showpiece,
default-on) + integrations (per Stack flags, incl. placeholder slots
and the framework flag) assemble the complete standalone site/.
You: nothing.
Input: tokens, copy-filled skeletons, ingested assets, contracts.
Outcome: finished site/ per file-structure contract.

**Phase 6 — qa (gate: must pass).**
Does: three layers — check.py (placeholders, refs, viewport, stylesheet
order, img sizing, token bypass, drift), /visual-qa (rendered audit of
every page at 360/768/1280 against the layout checklist + design
rationale + vibe refs, with fixes), then the manual fact/click-path
review.
You: nothing until it reports; spot-check anything it flags as accepted.
Input: built site/, DECISIONS.md rationale, vibe refs.
Outcome: per-page PASS block + results in BUILD_STATE notes; phase 6
done only when all three layers pass.

**Phase 7 — deploy (gate).**
Does/You: answers "Deploy how? (a) manual, (b) GitHub Pages,
(c) Hostinger" — see the deployment rundown below.
Outcome: live site (b/c) or deliverables zip (a) + record in BUILD_STATE.

**Phase 8 — handoff.**
Does: writes docs/HANDOFF.md (live URL, what was built, retainer scope,
how to request changes, credentials checklist — names only).
You: send it to the client. Optional after a manual deploy.
Outcome: handoff doc; workflow COMPLETE.

Phase 7 asks exactly: **"Deploy how? (a) manual — I'll hand off files
myself, (b) GitHub Pages from this repo, (c) Hostinger Git."**
- (a) manual: /package zips site/ contents to deliverables/; BUILD_STATE
  records `deploy: manual — packaged <zip path>`; phase 7 done; Phase 8
  offered, skippable — the workflow is COMPLETE either way.
- (b) GitHub Pages: deploy-hostinger references/github-pages.md
  (deploy-branch approach recommended); QA-gate hook applies to the push.
- (c) Hostinger Git: `bash scripts/deploy-split.sh` regenerates the
  site-only `deploy` branch and force-pushes it; the Hostinger
  webhook pulls it into public_html. Rollback: rerun the script with the
  previous good main commit as its argument.

Deployment rundown — the four control verbs (placeholder branches
auto-created at fresh-build start by scripts/bootstrap-branches.sh —
safe site-only stubs, so hosting can be connected at any time). Both
split scripts snapshot the CURRENT LOCAL site/ files (uncommitted +
untracked included) to the branch root:
```
main     = everything (OS + site/), the working branch
staging  = generated demo: local site/ snapshot at branch root +
           forced noindex robots.txt; NO gate (pre-QA by design);
           connect ONLY to the operator's demo subdomain
deploy   = generated live target: local site/ snapshot at branch
           root, zero OS files (proven on every run); QA advisory +
           the operator's explicit go
hosting  = manual hPanel Git pulls (staging -> demo subdomain,
           deploy -> public_html)

edit ──/stage──> stage-split.sh ──> staging ──hPanel pull──> demo subdomain
edit ──/save───> commit all + push ──> origin/main (backup/sync)
edit ──/deploy─(QA advisory + your go)──> deploy-split.sh ──> deploy ──hPanel pull──> live
/demo = bootstrap both branches + first /stage
```
Never commit manually to staging or deploy — their split scripts are
the only writers. On the FIRST Hostinger pull, check File Manager: the
target folder must contain only site files (leftovers from earlier
manual uploads — zips, .claude/, package.json, README, serve.ps1 —
have burned an operator before).

## §4 Commands
/build /qa /demo /stage /save /deploy /package /ingest /handoff
/client-edit /lint-os —
each is a file in .claude/commands/. /visual-qa is the visual-qa skill
invoked directly (skills are natively slash-invocable).

## §4.1 The asset-slot workflow
Phase 4 writes `client/assets-intake/slots/SHOPPING_LIST.md` — one block
per asset: exact filename, its placement folder, treatment, spec, and a
full copy-paste Higgsfield prompt — and creates the placement folders
(`Home - Hero/`, `Contact - onscreen pictures/`, ...). You generate at
your own pace, drop each file INTO ITS FOLDER under the exact slot
name, tick `[x]` on the list, run `/ingest`. The script converts
(adaptive quality ladder), extracts scrub frames + manifests, places
everything under site/assets/, updates MEDIA_LOG, and reports. Slots
you left unfilled come back as Higgsfield candidates: Claude asks you
in-chat (named slots + estimated credits) and generates ONLY what you
explicitly approve — approval is one chat reply now, no file editing.
Slot media files are gitignored (only the list is tracked).

## §5 Key files
client/client.md — v2 paste-based brief: Creative (hand-written) /
Overrides (owner-typed facts, beat everything) / Business Profile Paste
(raw GBP dump) / Auto (machine-written parsed facts; never hand-edit).
state/BUILD_STATE.md (resume point), DECISIONS.md (resolved ambiguities +
claude-proposed recommendations), QUESTIONS.md (open client questions),
MEDIA_LOG.md (paid-media ledger + approval gate).

## §6 Human gates
- Gate 1b (Phase 2): the design previews. preview/style-preview.html
  (palette, contrast, type, mock hero from the real tokens) +
  preview/layout-preview.html (real home-page layout with labeled
  asset placeholders and the exact animations/transitions the build
  will ship) — approve vibe AND layout/motion BEFORE copy, media, and
  build stack on top. The layout preview is binding for Phase 5.
  Skipped at Autonomy: high.
- Gate 1 (Phase 0): the confirmation table. Claude parses your paste into
  [unconfirmed] facts and shows ONE table in chat (field | value |
  source); reply once — "all good" or corrections. Corrections land in
  Overrides; confirmed facts flip to [confirmed]. Proceeding with
  unconfirmed facts is allowed, but phone/address/hours/prices then ship
  as [PLACEHOLDER] and QA blocks deploy until resolved. QUESTIONS.md is
  only for genuine ambiguities and creative gaps. The only hard blocker:
  no business name found anywhere.
- Gate 2 (Phase 4): fill the shopping-list slots yourself (default,
  credits 0), or approve paid generation for the slots you skipped —
  one in-chat reply naming the slots (Claude records
  `YES [in-chat <date>]` in MEDIA_LOG), or type YES in the file
  yourself. Blanket "generate whatever" never counts — never
  delegable, protects paid credits.
- Gate 3 (Phase 7): the three-way deploy choice above. Choosing (a)
  manual ends the workflow at phase 7 done + package path recorded;
  (b)/(c) proceed to push-based deploy under the QA-gate hook.

## §7 The deliverable
`site/` per contracts/file-structure.md: home at site/ root, one folder
per additional page, shared/ + assets/ single-sourced. Double-clicking
site/index.html must work; /package ships exactly this.

## §8 Retainer edits
/client-edit <request> — minimal surgical edits under
maintenance-retainer rules; reduced QA; deploy per the client's mode.

## §9 Maintaining the OS
/lint-os after skill edits; scripts/generate-skill-registry.py refreshes
docs/REGISTRY.md; template versions in docs/CHANGELOG.md. Every version
bump updates: the README title "Agency OS(Vx.y.z) — ...", AND this
manual's "Last updated: vX.Y.Z" stamp (reviewing the §3 phase rundown
for accuracy). lint-skills.py enforces BOTH against the latest
CHANGELOG entry — an update that skips the manual fails lint.

## §10 Troubleshooting
Pipeline stuck → read state/BUILD_STATE.md notes. Validation refusing →
it shouldn't: only a missing business name blocks (interpretation
principle); unrecognized values are soft. Push blocked → phase 6 not
done, run /qa. Site looks wrong → this is a visual bug, not a code
bug: run /visual-qa (layout debug) or reopen
preview/style-preview.html (vibe debug) rather than reading code.

## §11 Usage economy (operator side)
Context re-sent every turn is the biggest hidden cost multiplier. Do:
- **One session per phase** (or per 2-3 phases) instead of a marathon:
  BUILD_STATE.md makes resume free; short sessions avoid paying for a
  huge accumulated context on every single message.
- **/compact at phase boundaries** if staying in one session.
- **Model choice:** Sonnet for phases 3/5/6 (content, build, qa); Opus
  only for phases 1/2 and hard debugging.
- **/context** to audit what's actually loaded when a session feels heavy.
- **Keep client.md tight** — it is read early and often; every stray
  paragraph is a recurring tax.
- The in-session levers live in the token-economy skill; behavioral
  always-on rules live in CLAUDE.md "Token economy".
