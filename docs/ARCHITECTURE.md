# Agency OS — Architecture Design Document

**Purpose:** Modular AI operating system for a solo web design agency using Claude Code as primary developer.
**Status:** Architecture design only. No skill files generated yet.
**Date:** 2026-07-02

---

## 0. Evidence Basis — Read This First

This document distinguishes three classes of claims:

| Marker | Meaning |
|---|---|
| **[VERIFIED]** | Confirmed against official Anthropic docs (code.claude.com, platform.claude.com, anthropic.com/engineering) on 2026-07-02. Source URLs in Appendix A. |
| **[DESIGN]** | My architectural recommendation. Reasoned, but not empirically tested against your repo. |
| **[UNVERIFIED]** | Plausible but I could not confirm it. Treat as hypothesis until you test it. |

The single most important finding, before anything else:

> **You are proposing to hand-build a system that Claude Code already ships natively.** Your "markdown skill modules + master router" concept is, almost exactly, Claude Code's **Agent Skills** feature. [VERIFIED] Skills are folders containing a `SKILL.md` with YAML frontmatter; at session start, only each skill's `name` + `description` (~tens of tokens per skill) load into context; the full body loads only when the task matches; bundled reference files load only when read. This is called **progressive disclosure** and it is Anthropic's official, documented pattern.
>
> Building your own router in `CLAUDE.md` prose would recreate this mechanism worse: **[VERIFIED]** `@import`s in CLAUDE.md expand inline at launch and still consume the full context — they organize text, they do not save tokens. A prose router that says "read Design.md when doing design" relies on Claude remembering to do it; the native skill system does the matching automatically from frontmatter descriptions.
>
> **Therefore the correct architecture is not "CLAUDE.md as CEO routing to department files." It is: a minimal CLAUDE.md constitution + native Skills + slash commands + hooks.** Everything below is designed on that foundation.

---

## 1. Assumption Challenges

You asked me to be critical. Four of your assumptions should change:

### 1.1 "token-minimization.md should be read first" — **rejected, replaced**

Reading a file to save tokens **costs tokens**, and it costs them in every single session, forever. Worse, per official docs **[VERIFIED]**, CLAUDE.md content is *context, not enforced configuration* — a file of token-saving tips gets ~partial adherence at best, while guaranteed to burn its own weight at 100% frequency.

Token minimization in this system is achieved **architecturally, not instructionally**:

| Mechanism | Token effect | Verified? |
|---|---|---|
| Skills' progressive disclosure (metadata-only at startup) | The big win. 40 skills ≈ a few thousand tokens of descriptions instead of hundreds of thousands of body tokens | [VERIFIED] |
| CLAUDE.md kept under ~150 lines | Docs recommend <200 lines; longer files consume context *and reduce adherence* | [VERIFIED] |
| Path-scoped rules (`.claude/rules/` with glob matching) | Rules load only when Claude touches matching files | [VERIFIED] |
| Bundled scripts executed, not read | A validation script runs via bash without its source entering context | [VERIFIED] |
| Skills reference files one level deep | Deep detail costs zero tokens until the specific file is read | [VERIFIED] |
| A 10-line "output economy" block inside CLAUDE.md | Behavioral rules: no restating file contents, no verbose summaries, edit-don't-rewrite | [DESIGN] |

What survives of your idea: a **short section in CLAUDE.md** (not a separate always-read file) with output-economy rules. Ten lines, not a document. The rest of "token minimization" is the folder structure itself.

### 1.2 "Even if there are 100+ markdown files" — **rejected**

300 flat skill files is a maintenance liability and a discovery problem (300 frontmatter descriptions ≈ 15–20k tokens at startup just for the index — **[UNVERIFIED]** exact figure, but directionally certain since each description costs tokens). The correct scaling unit is: **~35–50 skills, each with internal reference files.** Official guidance **[VERIFIED]**: keep SKILL.md under 500 lines and split overflow into bundled reference files loaded on demand, one level deep. So `frontend-animation/` is *one* skill containing `gsap.md`, `scroll-triggers.md`, `reverse-playback.md` as references — not three top-level skills.

### 1.3 "Skills never know about each other" — **partially rejected**

Pure isolation is right for *content* (no duplicated rules) but wrong for *interfaces*. Skills must share **contracts**: the design-tokens skill outputs CSS custom properties that the layout skill consumes. The fix is a shared-contracts layer (§10): skills reference contract files, never each other's bodies.

### 1.4 "Optimize for future autonomous agents, assume massive context" — **partially rejected**

Massive context does not make loading everything free or wise: docs explicitly frame the context window as a shared, scarce resource where every loaded token competes with the actual task **[VERIFIED — framing; the docs phrase this as the context window being a public good]**. Progressive disclosure remains correct at any context size because it also improves *adherence* (less noise = better instruction-following, per the <200-line guidance). The future-proof bet is: filesystem + markdown + frontmatter, which is exactly what Anthropic committed to as the cross-product skill format (Claude Code, Claude apps, API all consume the same SKILL.md format **[VERIFIED]**).

---

## 2. Verified Platform Facts the Design Rests On

| # | Fact | Consequence for design |
|---|---|---|
| F1 | CLAUDE.md loads fully at every session start; target <200 lines | CLAUDE.md = constitution only |
| F2 | `@imports` expand inline at launch; no token savings | Never use imports for skill content |
| F3 | Skills: startup loads only frontmatter name+description; body on trigger; references on read | Skills are the module system |
| F4 | Skills live in `.claude/skills/<name>/SKILL.md`; also user-level `~/.claude/skills/` and plugins | Template repo carries project skills; your global prefs live at user level |
| F5 | Skills can be invoked as `/slash-commands`; directory name = command | Pipeline phases become commands |
| F6 | Skills support `context: fork` + `agent:` to run in an isolated subagent context | Heavy research/QA runs without polluting main context |
| F7 | Skills can bundle executable scripts; scripts run without their source entering context | Validators are Python/bash scripts, not prose checklists |
| F8 | CLAUDE.md is guidance, not enforcement; hooks (e.g., PreToolUse) are enforcement | Hard rules (never commit secrets, never deploy without QA pass) become hooks |
| F9 | Path-scoped rules (`.claude/rules/`, glob-matched) load only when touching matching files | CSS conventions load only when editing CSS |
| F10 | SKILL.md recommended <500 lines; overflow → bundled reference files, one level deep | Defines the skill granularity rule (§1.2) |

Source URLs: Appendix A.

---

## 3. Complete Folder Structure

```
agency-template/                      ← the repo you clone per client
│
├── CLAUDE.md                         ← constitution (~120 lines max). §6
├── client/
│   ├── client.md                     ← THE only file you replace per client
│   ├── client.schema.md              ← required/optional field spec (drives intake validation)
│   └── assets-intake/                ← client-supplied logo, photos, docs
│
├── .claude/
│   ├── settings.json                 ← permissions, hooks wiring, autoMemory prefs
│   ├── rules/                        ← path-scoped rules (load only when touching matching files)
│   │   ├── css.md                    ← applies to **/*.css
│   │   ├── js.md                     ← applies to **/*.js
│   │   └── html.md                   ← applies to **/*.html
│   ├── hooks/                        ← enforcement scripts (F8)
│   │   ├── pre-commit-secrets.sh
│   │   └── pre-deploy-qa-gate.sh
│   ├── skills/                       ← THE module system (~35–50 skills). Full inventory §4
│   │   └── <skill-name>/
│   │       ├── SKILL.md
│   │       ├── references/           ← deep docs, loaded on demand
│   │       ├── scripts/              ← executed, never loaded
│   │       └── templates/            ← copyable boilerplate
│   └── commands/                     ← workflow verbs (pipeline phases). §14
│
├── contracts/                        ← shared interfaces between skills (§10)
│   ├── design-tokens.md              ← how tokens are named/emitted (CSS custom props)
│   ├── file-structure.md             ← canonical output tree (/assets/video/ etc.)
│   ├── component-api.md              ← how sections/components expose options
│   └── media-log.md                  ← MEDIA_LOG.md format spec
│
├── state/                            ← per-project working state (gitignored or committed per taste)
│   ├── BUILD_STATE.md                ← pipeline phase tracker (§14)
│   ├── DECISIONS.md                  ← resolved ambiguities + client answers
│   ├── QUESTIONS.md                  ← open questions for the client
│   └── MEDIA_LOG.md                  ← your existing media generation ledger
│
├── site/                             ← the standalone website deliverable (v1.1.0: home at
│                                        site/ root, one folder per page, shared/ + assets/
│                                        single-sourced — see contracts/file-structure.md)
├── scripts/                          ← repo-level utilities (registry generator, validators)
│   ├── validate-client-md.py
│   ├── generate-skill-registry.py
│   └── lint-skills.py                ← CI: frontmatter present, <500 lines, no cross-skill refs
└── docs/
    ├── ARCHITECTURE.md               ← this document, committed
    └── CHANGELOG.md                  ← template version history (§13)
```

**Why each top-level folder exists:**

- **`client/`** — the single variable. Everything else is invariant across clients. `client.schema.md` is what makes "what information is missing → what questions to ask" *deterministic* instead of vibes: a script diffs `client.md` against the schema and emits `state/QUESTIONS.md`.
- **`.claude/`** — native Claude Code surface. Skills here are auto-discovered [F4]; nothing about discovery needs to be written in CLAUDE.md.
- **`contracts/`** — solves your "isolation vs. duplication" tension (§10). Skills never import each other; they cite contracts.
- **`state/`** — solves "CLAUDE.md as state machine" (§6): state lives in files that change, not in the constitution that must stay stable.
- **`scripts/`** — determinism where prose fails [F7]. Validation is code, not instructions.

---

## 4. Skill Inventory (grouped, with granularity rationale)

Target: **~40 skills.** Each row is one directory under `.claude/skills/`. Items in parentheses are *reference files inside* that skill — not separate skills (per §1.2).

### Tier A — Core process (always relevant to a build)

| Skill | Contents / references |
|---|---|
| `intake-validation` | reads client.md vs schema; script emits QUESTIONS.md |
| `site-architecture` | page mapping, nav structure, sitemap decisions (refs: single-page.md, multi-page.md, local-business-patterns.md) |
| `design-direction` | mood→style translation, niche archetypes (refs: coffee-shop.md, hvac.md, dental.md, gym.md, restaurant.md — your niche playbooks) |
| `design-tokens` | color systems, type scale, spacing; emits per contracts/design-tokens.md (refs: color-theory.md, typography.md) |
| `copywriting` | tone, local-SEO copy, section-level copy patterns (refs: headlines.md, cta.md, about-pages.md, service-pages.md) |
| `qa-review` | pre-delivery checklist as executable script + prose review guide |

### Tier B — Build (frontend)

| Skill | Contents / references |
|---|---|
| `layout-systems` | section composition, grid, responsive breakpoints (refs: hero-patterns.md, responsive-rules.md) |
| `hero-media` | your MP4 vs JPEG-sequence system, play-once-freeze, reverse-then-freeze, localStorage returning-visitor detection (refs + working JS in templates/) |
| `frontend-animation` | scroll/entrance animation defaults (refs: gsap.md, css-only.md, reduced-motion.md) |
| `three-js` | 3D scenes — **optional, loads only if triggered** (refs: setup.md, performance-budget.md) |
| `components` | header/footer/cards/testimonials/faq boilerplate (templates/) |
| `accessibility` | WCAG targets, contrast, focus, semantics (refs: audit-checklist.md + script) |
| `performance` | image formats, lazy loading, LCP/CLS budgets, video weight limits (script: lighthouse-check) |
| `seo-technical` | meta, schema.org LocalBusiness, sitemap, GBP alignment (refs: local-seo.md, structured-data.md) |

### Tier C — Media pipeline (your Higgsfield system)

| Skill | Contents / references |
|---|---|
| `media-generation` | storyboard-approval-before-paid-generation gate; Higgsfield model selection; MEDIA_LOG.md upkeep per contract (refs: image-prompts.md, video-prompts.md, credit-budgeting.md) |
| `image-optimization` | compression, srcset, WebP/AVIF pipeline (scripts/) |

### Tier D — Integrations (your chosen low-overhead stack)

| Skill | Contents / references |
|---|---|
| `forms` | Formspree patterns, validation, spam handling |
| `booking` | Calendly iframe patterns, sizing, styling |
| `email-marketing` | Brevo signup embeds |
| `automation-glue` | Make/Zapier handoff notes |
| `analytics` | GA4/Plausible install patterns |
| `maps-gbp` | Google Maps embed, GBP consistency checks |

### Tier E — Ship & operate

| Skill | Contents / references |
|---|---|
| `deploy-hostinger` | hPanel Git integration steps, branch strategy, rollback (your documented workflow) |
| `domains-dns` | DNS records, SSL checklist |
| `maintenance-retainer` | your done-for-you monthly edit workflow: how to take a client change request → edit → verify → deploy |
| `security-basics` | headers, form hardening, no-secrets rules (paired with hook) |
| `legal-pages` | privacy policy / terms generators for CA/local-business context |

### Tier F — Agency ops (not per-build)

| Skill | Contents / references |
|---|---|
| `winners-writing-process` | mandatory market-research diagnostic before any marketing asset (WWP questions, awareness/sophistication, MR template, avatar, top player analysis) |
| `persuasion-mechanics` | psychology layer: value equation, attention, desire, curiosity, trust/belief, tribal marketing |
| `copy-frameworks` | drafting skeletons: DIC/PAS/HSO, long-form Lead/Body/Close, hooks, storytelling, refinement checklist |
| `objections-and-closes` | aikido moves, objection bank, CTA laddering, boost stack, close library |
| `funnel-playbooks` | Google Ads lead-gen, Meta intro-offer, organic DM funnels + selection matrix and pricing |
| `local-seo-gbp` | GBP optimization, review generation, local rankings, SEO-vs-ads logic |
| `cold-outreach` | WOSS frame control, cold email/DM structure, call scripts, follow-up cadence |
| `sales-calls-and-pricing` | SPIN bank, call flow, project-math pricing, recap emails, upsells, testimonials |

**[DECIDED 2026-07-09, supersedes the earlier user-level design]** The original design placed agency-scoped skills in `~/.claude/skills/` or a plugin to keep per-project startup index smaller. Operator decision at v1.8.0: Tier F lives in the template so the skills version and sync via git with everything else. Cost: 8 extra frontmatter descriptions in every clone's startup index.

**Counting:** 41 template skills = under 50. Your "SEO.md, ColorTheory.md, Typography.md, GSAP.md…" examples all exist — as reference files inside the right skill, which is exactly the granularity official best practices prescribe [F10].

---

## 5. Dependency Relationships & Load Order

There is no manual "read order." **[VERIFIED]** load mechanics are: CLAUDE.md + all skill frontmatter at startup; skill bodies on trigger; references on read; path-rules on file touch. What you control is the **logical pipeline**, expressed as commands (§14), and a **tier model** for what may depend on what:

```
Tier 0  CLAUDE.md (constitution)          ── may reference: contracts, pipeline
Tier 1  contracts/*                       ── may reference: nothing
Tier 2  client/client.md + schema         ── may reference: nothing
Tier 3  skills/*                          ── may reference: contracts, client.md, own refs/scripts
Tier 4  commands/* (pipeline verbs)       ── may reference: skills by name, state files
Tier 5  state/* (mutable)                 ── written by pipeline, read by everything
```

**Rules [DESIGN]:**
- Arrows only point *down or sideways within a tier*, never up. A skill never instructs the pipeline; a contract never mentions a skill.
- Skills never reference other skills (§10). If two skills need shared knowledge, it becomes a contract.
- Nothing is "read first" except what the platform reads first (CLAUDE.md + frontmatter index). Priority is handled by precedence (§7), not read order — read order is not a reliable control surface for an LLM anyway.

**Optional vs. required:** Tier A skills fire on every build (their descriptions match every build task). Tiers B–E fire conditionally via frontmatter descriptions + client.md flags (§11). Tier F never loads in project context if kept at user level.

---

## 6. CLAUDE.md Architecture: Router vs. State Machine vs. Decision Tree

| Option | Pros | Cons | Verdict |
|---|---|---|---|
| **Prose router** ("if doing X, read Y.md") | Simple to write | Duplicates native skill matching, worse (relies on adherence, not mechanism); grows unboundedly; every routing rule is a permanent token cost | Reject |
| **State machine in CLAUDE.md** | Explicit phases | CLAUDE.md must stay *stable*; state changes constantly. Docs/community guidance: memory files should not hold running plans — they fossilize | Reject as location; keep the concept |
| **Decision tree** | Handles branching | Same problems as router, plus combinatorial growth | Reject |
| **Constitution + externalized state + native routing** [DESIGN] | CLAUDE.md stays <150 lines forever; routing is mechanical (frontmatter); state is mutable files; phases are commands | Requires discipline writing good skill descriptions | **Adopt** |

**CLAUDE.md contents (the whole file, ~120 lines):**
1. *Identity* (5 lines): what this repo is, what a "build" means.
2. *Precedence ladder* (§7) — the conflict-resolution law (10 lines).
3. *Output economy rules* (10 lines) — the surviving core of your token-minimization idea (§1.1).
4. *Pipeline pointer* (5 lines): "A build proceeds through the phases in `state/BUILD_STATE.md`; start or resume with `/build`."
5. *Hard invariants* (15 lines): never generate paid media without storyboard approval; never deploy without QA gate; never invent client facts — ask via QUESTIONS.md. (Each also backed by a hook where mechanically enforceable [F8].)
6. *Map* (10 lines): one line each pointing at `client/`, `contracts/`, `state/` — locations only, no content.

That's it. It never grows, because everything that grows lives in skills.

**State machine lives in `state/BUILD_STATE.md`** — a phase checklist the `/build` command creates and updates. This gives you resumability (open Claude Code tomorrow, `/build` reads state, continues) without polluting the constitution.

---

## 7. Priority System (conflict resolution)

A single precedence ladder, stated once in CLAUDE.md, highest wins:

```
1. Explicit user instruction in the current session
2. client/client.md                («the client is the spec»)
3. state/DECISIONS.md              (previously resolved ambiguities)
4. Hard invariants in CLAUDE.md    (safety/business rules — these beat client.md
                                    only for the enumerated invariants, e.g. the
                                    paid-media approval gate)
5. contracts/*                     (interface law between skills)
6. skills/* bodies
7. skill reference files
8. Claude's general knowledge
```

**Tie-breaker within a level [DESIGN]:** more specific beats more general (a niche playbook in `design-direction/references/dental.md` beats the generic body). If two same-level sources genuinely conflict, the rule is: *do not silently pick — log the conflict to `state/QUESTIONS.md` and choose the reversible option.* This converts conflicts into maintenance signals instead of hidden coin-flips.

Note the deliberate inversion at levels 2 vs 4: client wishes beat your style preferences, but never beat your business invariants. Example: client says "just generate whatever images you think are good" — the storyboard-approval invariant still holds because it protects your Higgsfield credit spend.

---

## 8. Token Economics (formal replacement of token-minimization.md)

Startup cost model **[VERIFIED mechanics, [UNVERIFIED] exact numbers — measure with `/context` in your repo]**:

```
fixed per session  = CLAUDE.md (~120 lines)
                   + skill index (≈ N_skills × description length)
                   + client.md if referenced early
variable           = only the skill bodies + references the task actually triggers
```

Design levers, in order of impact:
1. **Fewer, fatter skills** (§1.2): index cost scales with skill count, not knowledge volume.
2. **One-sentence descriptions** that are *trigger-precise*: they are both your router and your largest fixed cost. Description-writing is the highest-leverage editing you'll do.
3. **Scripts over prose** [F7]: your QA checklist as `qa-review/scripts/check.py` costs ~0 tokens to run vs. hundreds to read and "follow."
4. **Path-scoped rules** [F9] for language conventions instead of putting them in CLAUDE.md.
5. **`context: fork` subagents** [F6] for research-heavy steps (competitor analysis, content audits) so their intermediate output never enters the main window.
6. **Output economy rules** in CLAUDE.md: don't restate file contents; summarize diffs, not files; prefer edits over rewrites; no ceremonial recaps.

---

## 9. Naming Conventions

**[DESIGN]**, aligned to platform constraints (directory name = skill name = slash command [F5]):

- **Skills:** `kebab-case`, `domain-noun` or `noun-qualifier`: `hero-media`, `deploy-hostinger`, `seo-technical`. No category prefixes in the name (`frontend-animation` reads as a name, not a taxonomy) — the *description* frontmatter carries category metadata if you want to auto-group in the generated registry.
- **Reference files:** `topic.md`, lowercase, no numbering (numbering rots): `gsap.md`, `reduced-motion.md`.
- **Scripts:** `verb_noun.py`: `validate_client_md.py`, `check_contrast.py`.
- **Contracts:** `noun-noun.md`: `design-tokens.md`, `media-log.md`.
- **Commands:** imperative verbs: `/build`, `/qa`, `/deploy`, `/handoff`, `/client-edit`.
- **State files:** SCREAMING_CASE to signal mutability: `BUILD_STATE.md`, `QUESTIONS.md` (matches your existing `MEDIA_LOG.md`).
- **Reserved names:** never create a skill named after a contract or command; enforce via `lint-skills.py`.

Scales to hundreds because names are flat and the registry (auto-generated, §12) is the browsable taxonomy — not the filenames.

---

## 10. Inheritance & Isolation

**Inheritance (globals → skills):** don't. Composition instead:
- Global rules live in exactly one place each: behavioral globals in CLAUDE.md (loaded every session — that *is* the propagation mechanism [F1]); interface globals in `contracts/`; mechanical globals in hooks.
- Skills are written assuming CLAUDE.md is already in context — they never restate it. A skill that says "remember to be accessible" is a lint failure; accessibility has its own skill and contract.

**Isolation (avoiding duplication):**
- **Rule of one home [DESIGN]:** every fact has exactly one file. Anything needed by ≥2 skills is promoted to a contract; anything needed by exactly 1 stays in that skill's references.
- **Enforced by `scripts/lint-skills.py`:** flags cross-skill mentions (skill body containing another skill's name), flags CLAUDE.md phrases duplicated in skill bodies, flags SKILL.md >500 lines [F10], flags missing frontmatter. Run in CI / as a `/lint-os` command.
- **Contracts, not conversations:** the design-tokens skill *emits* `:root` custom properties per `contracts/design-tokens.md`; the layout skill *consumes* variables per the same contract. Neither knows the other exists. This is your "departments don't know each other" — kept, but with a shared law book.

---

## 11. Optional Skill Loading

Two native mechanisms, layered:

1. **Frontmatter description matching [VERIFIED]:** `three-js`'s description reads "Build WebGL/3D scenes with Three.js. Use only when client.md requests 3D, WebGL, or interactive 3D elements." If the task never mentions it, the body never loads. This is your GSAP/ThreeJS conditional, natively.
2. **client.md stack flags → pipeline enforcement [DESIGN]:** `client.md` schema includes a `## Stack` section (`animation: gsap | css-only | none`, `3d: yes/no`, `booking: calendly`, …). The `/build` command's phase logic says: "consult the skills matching the Stack flags." This makes optional loading *deterministic at the pipeline level* rather than trusting semantic matching alone — belt and suspenders.

Negative control matters as much: descriptions should say when **not** to fire ("Do not use for simple CSS transitions — see frontend-animation"), because over-triggering is the token leak in this design.

---

## 12. Scalability (the 5-year picture)

Your projection: 300 md files, 50 skills, 100 templates. Corrections and mechanisms:

- **300 files is fine; 300 *skills* is not.** 50 skills × ~6 internal files = 300 files with a startup index of only 50 descriptions. The granularity rule (§1.2) is the scaling law.
- **Auto-generated registry:** `scripts/generate-skill-registry.py` scans frontmatter → emits `docs/REGISTRY.md` (name, description, version, category, last-modified). Humans browse the registry; Claude never needs it (it has the live index). Never hand-maintain an index — hand-maintained indexes are how systems rot.
- **Split by change-rate [DESIGN]:** when the template gets heavy, extract stable cross-project skills into a **plugin/marketplace** (skills-as-plugins is supported [F4/VERIFIED that skills load from plugins]) or a git submodule `agency-skills` repo. Client template then contains only project-shaped things (contracts, state, pipeline) + pinned plugin version. This is the real answer to "100 project templates": templates become thin — a `client.schema.md` variant + a niche playbook reference — not 100 forks of the skill library.
- **CI as the maintainer:** `lint-skills.py` + `validate-client-md.py` run on every commit. A system this size stays healthy only if health checks are code.
- **Auto memory [VERIFIED feature]:** Claude Code can accumulate its own notes across sessions. Let it, but treat auto memory as *scratch* — anything it learns that's worth keeping gets promoted, by you, into a skill reference during a monthly review. One-way promotion keeps the canonical system curated.

---

## 13. Versioning

- **Template repo is the versioned artifact.** Tag releases (`v3.2.0`). Every client repo records its origin tag in `docs/CHANGELOG.md` at clone time. Old client sites keep the skills they were built with — that's your backward compatibility, for free, via git. You almost never retro-upgrade a shipped site's skill set; you upgrade the *template* and the next client benefits.
- **Per-skill versioning:** semver in frontmatter metadata (`metadata: {version: 1.4.0}`) + a `CHANGELOG` section at the bottom of each SKILL.md. Breaking change = the skill's *contract output* changes (e.g., design-tokens emits a new variable naming scheme) → bump contract version too, since contracts are the compatibility surface.
- **Retainer clients (your maintenance model):** when you open an old client repo under a newer personal setup, the repo's committed `.claude/skills/` wins for project skills — the site is edited under its original rules. If you deliberately migrate it, that's a commit ("upgrade to template v4"), visible in history. **[UNVERIFIED]:** exact precedence when a user-level skill and project skill share a name — test before relying on shadowing; safest is to avoid name collisions entirely (lint rule).

---

## 14. Pipeline & Documentation Standards

### 14.1 The build pipeline (commands + state)

```
/build  →  Phase 0  intake      validate client.md vs schema → QUESTIONS.md; STOP if blockers
           Phase 1  architecture  pages, nav, sitemap → DECISIONS.md
           Phase 2  design       direction + tokens (design-direction, design-tokens)
           Phase 3  content      copywriting per page
           Phase 4  media        storyboard → YOUR APPROVAL GATE → Higgsfield generation → MEDIA_LOG.md
           Phase 5  build        layout, components, animation, integrations
           Phase 6  qa           /qa — scripts + review; gate hook for phase 7
           Phase 7  deploy       /deploy — Hostinger Git flow
           Phase 8  handoff      /handoff — client docs, credentials list, retainer onboarding
```

Each phase: reads `BUILD_STATE.md`, does work, writes results + checks the box, stops at human gates (Phase 0 questions, Phase 4 media approval, Phase 7 deploy confirm). "Build this website" with zero repetition works because the *command* encodes the process and the *state file* encodes progress — not because CLAUDE.md narrates it.

### 14.2 SKILL.md standard template

```markdown
---
name: hero-media
description: Implement hero sections with video/image sequences — MP4 vs JPEG
  sequence selection, play-once-then-freeze, returning-visitor detection.
  Use when building or editing any hero section with motion. Not for
  general page animation (see frontend-animation).
metadata: {version: 1.0.0, category: frontend, tier: B}
---

# Hero Media

## Purpose            (2–3 sentences: what problem, what output)
## Inputs             (what it reads: client.md fields, contracts)
## Outputs            (what it produces, per which contract)
## Rules              (imperative, numbered, ≤15; the actual expertise)
## Decision guide     (small table: situation → approach)
## References         (when to read which bundled file — one line each)
## Scripts            (what each does, how to invoke; run, don't read)
## Anti-patterns      (3–5 known failure modes)
## Changelog
```

Constraints (lint-enforced): frontmatter complete; description contains both a "use when" and a "not for"; body <500 lines [F10]; no other skill named in body; rules imperative ("Never autoplay with sound" not "we prefer avoiding sound") — imperative phrasing is the documented best practice for adherence **[VERIFIED — docs/community guidance on direct commands]**.

---

## 15. Future-Proofing

- **Bet on the filesystem, not the harness.** SKILL.md is Anthropic's cross-product format (Code, Claude apps, API) [VERIFIED]; markdown + YAML + scripts will outlive any specific router syntax. Your knowledge is portable even if Claude Code changes.
- **Contracts are the longest-lived layer.** Models improve; your design-token conventions and file-structure law remain the stable interface a smarter model plugs into. Invest quality there.
- **More capable models change *granularity*, not architecture:** you'll delete hand-holding from skill bodies (rules shrink), keep the same skeleton. Progressive disclosure, precedence ladder, contracts, and state files remain correct at any capability level.
- **Autonomy readiness:** the human gates (Phase 0/4/7) are the only places requiring you. As trust grows, gates become configurable per client (`client.md: autonomy: high`), flipping a gate from "stop and ask" to "log and proceed." The architecture doesn't change — one flag does.

---

## 16. Migration Plan From Your Current Master CLAUDE.md

1. **Inventory** your existing master CLAUDE.md; label every section {invariant | contract | skill-knowledge | state}.
2. **Extract contracts first** (file structure, MEDIA_LOG format, token naming) — smallest, highest-value move.
3. **Carve the 6 Tier-A skills**, then hero-media + media-generation (your most developed material — hero patterns, Higgsfield pipeline, storyboard gate map 1:1 onto skills).
4. **Shrink CLAUDE.md to the constitution** (§6). Everything cut either moved to a skill or gets deleted as redundant.
5. **Add `/build` + `BUILD_STATE.md`**, run one real client end-to-end, measure with `/context` before/after.
6. **Add lint + registry scripts.** Only then expand the skill catalog.

Do not build all 40 skills up front. Official authoring guidance **[VERIFIED]**: build skills by observing where the agent actually struggles on real tasks, incrementally. Weeks 1–2 of real use will reorder your priorities better than any upfront plan — including this one.

---

## Appendix A — Sources (verified 2026-07-02)

- Claude Code memory / CLAUDE.md mechanics: https://code.claude.com/docs/en/memory
- Claude Code skills (project/user locations, slash invocation, context: fork, watching): https://code.claude.com/docs/en/skills
- Agent Skills overview (progressive disclosure, three loading levels, cross-product): https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Skill authoring best practices (<500 lines, reference files, scripts, context-as-public-good): https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Anthropic engineering — Agent Skills design rationale: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

## Appendix B — What Is NOT Verified

- Exact token counts for any startup configuration in *your* repo (measure with `/context`).
- Skill name-collision precedence between user-level and project-level skills (test; avoid collisions regardless).
- That this specific folder layout produces better adherence than alternatives — it follows documented guidance, but I have not run it against a real build. Treat the first client project as the experiment.
- Any adherence-percentage claims floating around the community (e.g., "~70% CLAUDE.md compliance") — plausible direction, unverified numbers; that's why hard rules are hooks, not prose.
