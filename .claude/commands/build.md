Run or resume the website build pipeline.

1. Read state/BUILD_STATE.md. If "Client:" is unset, this is a fresh build:
   set client name from client/client.md, set Started date, and BOOTSTRAP
   BRANCHES: run `bash scripts/bootstrap-branches.sh` - creates any
   missing `staging` and `deploy` branch as a SAFE site-only placeholder
   (orphan commit: index.html "coming soon" + noindex robots.txt) and
   pushes when a remote is configured, so hosting can be connected to
   either branch at any time with zero OS files leaked. Real content
   comes from the only writers: scripts/stage-split.sh (staging = pre-QA
   demo, via /stage or /demo) and scripts/deploy-split.sh (deploy =
   production, via /deploy).
2. Find the first phase not marked done and execute phases in order:
   - Phase 0 intake (enrich → confirm → proceed):
     a. FIRST inventory client/assets-intake/ (excluding slots/, vibe/):
        classify filenames (logo*, hero1/2*, gallery1/2*, team*, menu*,
        before*/after*...) and note the inventory — Phase 4 assigns
        these files to slots so only gaps get generated. Then, if
        client.md's Business Profile Paste section is non-empty, run
        the client-enrichment skill (writes the Auto section).
     b. Run `python3 scripts/validate-client-md.py`. Blockers (only "no
        business name found anywhere" in v2) → questions in
        state/QUESTIONS.md, mark phase 0 blocked, STOP.
     c. Gate 1 = confirmation table: present ONE compact table in chat —
        every [unconfirmed] Auto fact, one row each: field | value |
        source. The operator replies once ("all good" / corrections).
        Corrections go to Overrides; confirmations flip tags to
        [confirmed]. QUESTIONS.md remains only for genuine ambiguities
        and creative gaps.
     d. If the operator says "proceed anyway", facts still [unconfirmed]
        may drive drafting, but phone/address/hours/prices render as
        `[PLACEHOLDER: value?]` in shipped HTML — the qa-review script
        fails on placeholders, so nothing unverified can ship.
     e. Empty Creative section = SOFT: note which questions would most
        improve the result for the detected niche, then proceed with
        niche-playbook defaults. Mark phase 0 done, continue.
   - Phase 1 architecture: FIRST distill the audience brief into
     state/DECISIONS.md (audience-research skill: the matching niche
     study, read once - skipped only when client.md's Target Audience
     is already rich). Then use the site-architecture skill. Output:
     audience brief + page map + section list per page in DECISIONS.md.
   - Phase 2 design: use design-direction then design-tokens skills.
     Output: site/shared/tokens.css + a 10-line design rationale in
     DECISIONS.md. Then build the TWO gate artifacts:
     a. `python3 scripts/generate-style-preview.py` ->
        preview/style-preview.html (tokens: palette, contrast, type,
        mock hero - mechanical).
     b. AUTHOR preview/layout-preview.html - the HOME page as it will
        actually be built: real section order (Phase 1 architecture),
        real grid/spacing (layout-systems patterns), labeled grey
        placeholder boxes where every asset slot goes (slot filename
        printed in the box), placeholder headings at real type sizes,
        and the EXACT animation/transition code Phase 5 will ship
        (same css-only/gsap reference patterns, same tokens, same
        mobile nav/motion behavior per mobile-polish). Links
        ../site/shared/tokens.css. Self-check it on the preview server
        (scroll the entrances, open the mobile nav at 360) before
        presenting. STOP: operator approves both files - the approved
        layout preview is BINDING for Phase 5. Then run `python3 scripts/generate-style-preview.py`
     (fix any CONTRAST FAIL it reports first), screenshot the preview
     yourself via the local preview server and self-check it against
     the vibe references, then STOP: "Style preview at
     preview/style-preview.html — approve the vibe or correct."
     Autonomy: high skips the stop (log claude-approved in DECISIONS).
   - Phase 3 content: use the copywriting skill. Output: final copy for
     every section of every page, written directly into the HTML files
     (create page skeletons per contracts/file-structure.md if absent).
   - Phase 4 media: use the media-generation skill. Create THIS
     project's placement folders (named from the page/section map),
     sweep the Phase 0 asset inventory into them (client files
     pre-fill + pre-tick their slots, model=client), then write the
     shopping list for the GAPS: client/assets-intake/slots/
     SHOPPING_LIST.md (one block per slot: exact filename, folder,
     treatment, spec, full prompt - per contracts/asset-slots.md)
     + mirrored MEDIA_LOG rows (status=planned). STOP. Then either:
     (a) DEFAULT - the operator generates manually (Higgsfield), drops
         each file into its placement folder (slots/<Page> - <Section>/,
         exact slot filename), ticks [x] on the list, runs /ingest.
         Unfilled slots come back as Higgsfield candidates -> in-chat
         approval per (b).
     (b) Paid auto-generation ONLY with per-row approval: the operator
         types YES in MEDIA_LOG, or approves the named slots in-chat
         (present slot names + estimated credits, wait for the reply,
         transcribe `YES [in-chat <date>]`). Never generate before
         approval; blanket permission never counts.
     Optional: with operator consent, proceed to Phase 5 with poster
     placeholders while slots are filled; /ingest swaps real media in
     later with no code changes.
   - Phase 5 build: use layout-systems, components, hero-media
     (treatment templates wired per the shopping list / scrub manifests),
     frontend-animation (per Stack flags), accessibility, performance,
     honoring the Stack framework flag per the file-structure contract's
     Framework exception (vanilla default; requested frameworks accepted),
     then mobile-polish (phone experience as the showpiece - default on),
     plus integration skills matching Stack flags (forms, booking,
     email-marketing, analytics, maps-gbp). Output: complete standalone
     site in site/ per contracts/file-structure.md.
   - Phase 6 qa: run the /qa command logic. Only mark done if it passes.
   - Phase 7 deploy: after phase 6 = done, STOP and ask exactly:
     "Deploy how? (a) manual — I'll hand off files myself, (b) GitHub
     Pages from this repo, (c) Hostinger Git." Then:
     (a) run /package, write `deploy: manual — packaged <zip path>` to
         BUILD_STATE.md, mark phase 7 done. Phase 8 becomes optional:
         offer /handoff, skip on decline, mark workflow COMPLETE either way.
     (b) follow the deploy-hostinger skill's GitHub Pages section
         (references/github-pages.md). The QA-gate hook still applies to
         the push.
     (c) Hostinger flow per the deploy-hostinger skill
         (scripts/deploy-split.sh generates the site-only deploy
         branch; never commit to deploy manually).
   - Phase 8 handoff: use maintenance-retainer + write client handoff doc
     (optional after a manual deploy — see Phase 7a).
3. After each phase: update BUILD_STATE.md (status, completed date, notes).
4. Respect all hard invariants in CLAUDE.md at every phase.
