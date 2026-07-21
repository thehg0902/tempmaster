# Build State

Client: Temp Master
Template version: v1.7.1
Started: 2026-07-20

| phase | name         | status  | gate                      | completed |
|-------|--------------|---------|---------------------------|-----------|
| 0     | intake       | done    | HUMAN: confirm table      | 2026-07-20 |
| 1     | architecture | done    | -                         | 2026-07-20 |
| 2     | design       | done    | HUMAN: approve style prev | 2026-07-20 |
| 3     | content      | done    | -                         | 2026-07-20 |
| 4     | media        | in-progress | HUMAN: fill slots/approve | -     |
| 5     | build        | done    | -                         | 2026-07-20 |
| 6     | qa           | blocked | scripts must pass         | -         |
| 7     | deploy       | pending | HUMAN: confirm deploy     | -         |
| 8     | handoff      | pending | -                         | -         |

status: pending | in-progress | blocked | done
Notes:
- /stage (2026-07-20, re-push): staging was stale - last pushed at 17:36 (5c084db),
  BEFORE the scroll-scrub rewrite, work gallery, and final photo approvals all
  happened. Operator couldn't see the scroll-scrub because they were looking at that
  stale staging build, not local files. Re-ran stage-split.sh -> fa04aa7; verified via
  git show that origin/staging now contains hero-scrub/SCRUB_START in script.js and
  the gallery section in index.html. Lesson: re-stage after every batch of changes
  the operator might want to preview, not just once per session.
- Phase 6 (2026-07-20, 7th round — all media resolved, check.py CLEAN): operator said
  "approve all" in direct response to the 3 named pending photo slots. Before
  generating, checked the 6 just-added real job photos for matches first (real beats
  generated, media-generation rule 3): 2 of 3 slots resolved by REUSING real client
  photos instead (services-ac.jpg -> gallery-wall-mount-ac.webp, ac-install.jpg ->
  gallery-ductless-condenser.webp; added aspect-ratio+object-fit:cover to both image
  contexts so a portrait source photo crops consistently). Only ac-repair.jpg (open
  condenser mid-diagnosis) had no real match - generated via Higgsfield
  marketing_studio_image (cost preflighted: 2 credits), reviewed the result before
  accepting. check.py: 0 FAIL / 6 WARN (all 6 warnings are the same pre-existing
  cosmetic header/footer "drift" false-positive - expected, per-page nav-active-state
  and header-CTA differences are intentional). Verified via fetch() that all 7 new/
  changed image URLs return 200 on both the home and AC pages, console clean on both
  - the Browser pane's screenshot pipeline remained down this whole round (consistent
  timeouts even after a fresh preview-server restart), so this is DOM/network-level
  verification, not a rendered visual pass. RECOMMEND: run a proper /visual-qa pass
  once the Browser pane's screenshot capability recovers, before treating Phase 6 as
  fully closed - marking QA gate close to done but not flipping status to "done" in
  this table until that visual pass happens, per the qa skill's own criteria (script
  pass + visual pass + manual review, not script pass alone).
- Phase 6 (2026-07-20, 6th round — scrub timing, work gallery, final placeholders):
  SCRUB_START moved 0.30->0.02 and SCRUB_END 0.75->0.95 (operator: crossfade should
  happen "as soon as scroll-down is detected" since hero-transition's first frame
  matches hero-loop's; scrub now finishes exactly as trust finishes appearing).
  Verification note: the Browser pane's screenshot pipeline was down for this round
  (persistent 30s timeouts, on a fresh tab and after restarting the preview server) -
  visual confirmation was NOT obtained. Verified what was possible without it:
  manifest fetches correctly, frame 1 vs frame 61 draw distinctly different pixel
  content on a manually-constructed canvas (proves the image assets + drawImage
  pipeline are sound), and the constant change is a straight numeric substitution in
  the exact code path already proven correct end-to-end in the PRIOR round (with the
  old 0.30/0.75 values) via real scroll + frame-index instrumentation. Confidence is
  high but this one is code-review-level, not live-browser-level, for the timing
  change specifically - flagging honestly rather than claiming a screenshot check that
  didn't happen.
  Also: 6 real job-site photos (client-provided, pre-existing in site/assets/images/
  as 1-6.webp, not yet inventoried) built into a new "Our Work" gallery section on
  Home between Services and Testimonials - resized/recompressed/renamed descriptively,
  logged in MEDIA_LOG.md as model=client.
  Also: operator answered the remaining 6 QUESTIONS.md items (disposal, diagnostic
  fee, rebates, brands, TSSA number, response-time) - all 7 [PLACEHOLDER] markers
  site-wide are now resolved (grep-verified zero remaining). check.py: 3 fail / 6
  warn - every remaining fail is one of the 3 unfilled photo slots, nothing else.
- Phase 6 (2026-07-20, 5th round — scroll-scrub hero transition): operator changed the
  hero transition from a real-time play-once/reverse video to a true scroll-scrub
  (canvas + 61 webp frames extracted from hero-transition.mp4, 12fps/1440x812/q70,
  2.9MB). Reverse-on-scroll-up is now structurally free (earlier frame index, no
  timing/threshold logic) - resolves the earlier reverse-feel concern at its root.
  Fixed one regression caught during verification: the loop video's 'ended' restart
  handler got dropped when the old state machine was removed, so the idle loop would
  play once and freeze - restored. Also discovered and worked around a test-harness
  artifact worth remembering: requestAnimationFrame (and therefore all scroll-driven
  visual updates) pauses when the browser tab isn't the fronted/visible one in this
  tool - always tabs_select before trusting a scroll-linked JS check. Verified via
  instrumented frame-index logging (removed after) + pixel-content diffing that
  different scroll positions draw genuinely different frames, both directions.
  check.py: 6 fail / 6 warn (one warning dropped - the old video-weight-near-cap
  warning no longer applies now that the transition ships as images, not a video).
- /demo (2026-07-20): current local site/ (uncommitted + untracked included) snapshotted
  and force-pushed to origin/staging at f642dc0, noindex robots.txt forced. Site-only
  content verified (no OS files leaked). Still pre-QA - operator connects hosting in
  hPanel manually; do not point the production domain at staging.
- Phase 6 (2026-07-20, 4th round — answered questions processed): operator answered 6
  QUESTIONS.md items directly. Promoted to client.md Overrides/Auto (rating 5.0/34
  reviews confirmed, genuine 24/7 dispatch confirmed, 3 testimonials approved, all 3
  differentiation policies confirmed true, Temp Master confirmed owner-operated -
  woven into the About section intro per the Target Audience research's top
  positioning recommendation). Replaced 7 [PLACEHOLDER] instances across index.html
  with real copy (trust rating, 2 About policy items, Testimonials section 3 cards,
  2 FAQ answers) + added aggregateRating to the JSON-LD. Domain stays deferred
  (temporary subdomain TBD). The 6 smaller items that were only informal inline
  placeholders (disposal fee, diagnostic fee, rebate handling, brands carried, TSSA
  licence, response-time commitment) are now formally tracked as QUESTIONS.md rows -
  still correctly gating check.py at 6 fail (composition changed: fewer real content
  gaps, same count because 3 media slots + these newly-tracked items remain). No
  regressions; verified live (rating/About/testimonials/FAQ copy correct on screen,
  hero/trust layers still transitioning correctly, DOM-verified after a Browser pane
  screenshot-renderer glitch gave a false stale-frame reading - confirmed via
  computed styles, not visual only).
- Phase 6 (2026-07-20, 3rd refinement round): root-caused the reverse-scroll bug via
  REAL mouse-wheel scroll testing (computer.scroll, not just programmatic scrollTop) -
  the trigger threshold was only 18% from the top of the pinned range, so almost the
  entire scroll-up gesture showed a frozen video before snapping to reverse in the
  final sliver. Moved to hysteresis thresholds (forward 0.38 / reverse 0.34) right at
  the hero/trust boundary - reverse now has ~62% of the scroll-up range to visibly
  play, confirmed via real wheel-scroll at p=0.63 (still frozen, correct - above
  threshold) and p=0.25 (fully reversed, correct - below threshold). Also added a
  continuously auto-rotating (CSS-only, reduced-motion-safe) horizontal marquee of the
  3 real confirmed review quotes inside the trust layer, styled as translucent chips
  (not white cards). One QA fail introduced and fixed same pass: marquee's edge-fade
  mask used literal #000 - swapped to var(--color-text) (masks only need opacity, hue
  is irrelevant) to stay token-driven. check.py back to 6/7 baseline, no regressions.
- Phase 6 (2026-07-20, 2nd refinement round): trust layer re-centered on the video
  (was bottom-anchored, left empty-looking video above it) - now overlays like the
  hero does, with a darkened-middle overlay gradient + text-shadow so it stays legible
  wherever it sits. Transition video now plays at 2x (native playbackRate for forward,
  real elapsed-time-based rAF stepping for the fallback/reverse path - replaced a
  fixed-fps assumption that was silently running at a display-dependent speed).
  Verified via instrumented sampling: reverse is genuine frame-by-frame playback of the
  actual footage at an accurate, consistent 2x, not a jump. check.py unchanged at 6/7,
  no regressions.
- Phase 6 (2026-07-20, retainer-style refinement mid-gate): pinned hero stage per operator
  spec - video locked via `position:sticky` in a 200svh wrapper; hero copy and trust
  stats are separate absolutely-positioned layers driven by a single rAF-throttled
  scroll listener (transform/opacity only). Verified live end-to-end at desktop + 375px:
  hero fades/translates out 0-40% progress, video forward-triggers at 18% and freezes,
  trust stats translate up from below 45-100%, header goes solid only once fully
  scrolled through; full reverse trip confirmed (trust hides, video reverses, loop
  resumes, header goes transparent again). No console errors, no regressions in
  check.py (still 6/7, all pre-existing operator-gated items). Reduced-motion path
  verified by code review only (harness has no OS-level emulation) - CSS falls back to
  static stacked layout, JS state-machine returns before wiring the scroll driver.
- Phase 6 QA (2026-07-20): check.py = 6 FAIL / 7 WARN. ALL 6 fails are operator-gated,
  not code defects: 3x [PLACEHOLDER] copy (rating/count, testimonials approval, policy
  claims, response time, brands, disposal, diagnostic fee, rebate handling - see
  QUESTIONS.md) + 3x broken img refs = the 3 unfilled media slots (services-ac,
  ac-install, ac-repair). WARNs: header/footer cross-page drift is by-design (relative
  paths + per-page CTAs differ; checker uses exact match); video weight 2.6MB/80% of
  cap mitigated by deferring hero-transition.mp4 (preload=metadata, fetched after
  reveal - initial payload is the 975KB loop only). Visual pass done live in-browser:
  all 4 pages at 360+desktop, console clean, launch sequence + full hero video cycle
  verified (loop -> fwd freeze -> reverse -> loop), no horizontal scroll at 360.
  Phase 6 flips to done automatically once the operator answers QUESTIONS.md and
  fills/approves the 3 media slots + /ingest.
- Phase 5 (2026-07-20): complete standalone site in site/ per file-structure contract.
  4 pages + shared base.css/main.js + per-page css/js; hero videos ingested (transition
  re-encoded 7.8MB->1.7MB, posters extracted, logo alpha-preserved + resized 400px);
  loader/header-entrance/borderless-stage implemented per the operator-approved plan;
  JSON-LD LocalBusiness, maps embeds, .htaccess security+cache headers. Deferred pending
  operator input: sitemap/canonicals/OG (need Domain), legal pages + forms provider
  (Stack flags unset - form is an unwired placeholder), analytics (flag unset).
- Phase 4: shopping list written (3 client slots pre-filled: hero-loop, hero-transition,
  logo; 3 image gaps with prompts ready but held on unconfirmed Photos policy). STOPPED
  at the human gate: operator fills slots + /ingest, or approves named-slot generation.
  hero-transition.mp4 is 7.8MB (cap 4MB) - ingest re-encode mandatory.
- Phase 3: copy final in all 4 pages; placeholders gate on QUESTIONS.md items
  (rating/count, testimonial approval, policy claims, response time, brands,
  disposal, diagnostic fee, rebate handling). QA fails on placeholders by design.
- Phase 0: Gate 1 confirmed "all good" 2026-07-20. 3 open questions carried forward in
  state/QUESTIONS.md (Google rating/review count exact figures, true meaning of "Open 24
  hours", owner-operated status) - none blocking, but affect trust-bar and hero copy
  precision. Testimonial candidates (3 reviews) still [needs-approval], to be confirmed
  at Phase 3 before use.
