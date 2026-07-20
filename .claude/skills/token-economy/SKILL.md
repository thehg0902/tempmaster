---
name: token-economy
description: Reduce token/usage consumption of any session without changing
  output quality. Use when a session feels heavy, before long phases, or
  when the operator asks about usage. Not for output style/formatting
  rules (CLAUDE.md owns the always-on rules).
metadata: {version: 1.0.0, category: process, tier: A}
---
# Token Economy

## Purpose
The first real build burned usage limits too fast. This is the playbook
for keeping sessions cheap without degrading the site.

## Inputs
The current session's loaded context; state/BUILD_STATE.md (resume point).

## Outputs
Lower per-session and per-turn token consumption; measurements recorded
in this skill's changelog.

## Rules
1. Grep-before-read: locate the change surface with grep/glob, then read
   ONLY the matching region (line-range reads). Whole-file reads are for
   files under ~200 lines or files about to be rewritten.
2. Line-range reads for anything big: state files, HTML pages, and this
   repo's docs are mostly append/patch targets - read the tail or the
   matched section, not the body.
3. Fork research: for research-heavy steps (competitor scans, content
   audits, long doc digestion) spawn a subagent with an isolated context
   (context: fork) so intermediate output never enters the main window -
   only the conclusion returns.
4. Append-only state: MEDIA_LOG/QUESTIONS/DECISIONS are kept short and
   append-only - never rewrite them to "tidy up"; never re-read them
   whole when appending.
5. Validate once: run validate-client-md.py once per client.md change,
   not once per phase. Phase 0's result stands until the file changes.
6. Session shape: BUILD_STATE.md is the resume point - end the session
   at a phase boundary and start fresh rather than dragging a huge
   context into the next phase. Short sessions = every turn cheaper.
7. Scripts over prose: a check that exists as a script is run, never
   reasoned through in chat.

## Measure it
- /context shows what is actually loaded and what it costs - run it when
  a session feels heavy, and before/after applying these levers.
- /compact between phases on long runs compresses accumulated history.
- Record before/after numbers in the changelog below per client build.

## Anti-patterns
- "Let me re-read the whole file to be safe"; re-validating unchanged
  client.md; narrating file contents back into chat; preloading skills.

## Unverified
These levers follow platform mechanics (progressive disclosure, context
re-sent per turn) but exact savings were NOT measured in this repo.
Measure with /context before/after on the next client build and record
numbers here.

## Changelog
- 1.0.0 initial (v1.1.0 change order; no measured numbers yet)
