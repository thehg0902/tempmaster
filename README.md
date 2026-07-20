# Agency OS(V1.10.0) — Website Build Template

Per-client workflow (2-minute setup):
1. Clone this repo → rename to the client → point origin at the client's
   own repo. First `/build` (or `/demo`) creates the branch set as safe
   site-only placeholders. Four control verbs move your local site files:
   `/stage` → staging branch (demo subdomain), `/save` → main (GitHub
   backup), `/deploy` → deploy branch (live, after a QA advisory + your
   go), `/demo` → one-shot branch setup + first stage push.
2. In `client/client.md`: paste the business's Google Business Profile /
   Maps text into **Business Profile Paste** and answer what you can under
   **Creative** (everything optional; hard facts you want to force go
   under **Overrides** — see `client/client.schema.md`). Drop client
   assets in `client/assets-intake/`.
3. Open Claude Code in the repo root. Say `/build`.
4. Answer the gates: the Phase 0 confirmation table (parsed facts —
   reply once), media (fill slots or approve paid generation), deploy
   choice (manual /package, GitHub Pages, or Hostinger Git). Genuine
   ambiguities land in `state/QUESTIONS.md`.
5. Media: Phase 4 writes a shopping list at
   `client/assets-intake/slots/SHOPPING_LIST.md` (slot filenames +
   ready-to-paste prompts). Generate, save files under those exact names
   in the same folder, run `/ingest`.

The deliverable is the standalone `site/` folder (openable by
double-clicking site/index.html; zip it with `/package`):

```
site/
  index.html  style.css  script.js   <- home page
  shared/     tokens.css  base.css  main.js
  assets/     images/  video/  fonts/
  <page>/     index.html  style.css  script.js   (one folder per page)
```

Operator guide: `OPERATION_MANUAL.md` (repo root).

Architecture: `docs/ARCHITECTURE.md`. Skill index: `docs/REGISTRY.md`
(regenerate with `python3 scripts/generate-skill-registry.py`).

Maintenance: run `python3 scripts/lint-skills.py` before committing skill
changes.

VERIFY BEFORE RELYING ON (see docs/ARCHITECTURE.md Appendix B):
- Path-scoped rule frontmatter format in `.claude/rules/` against current
  Claude Code docs (https://code.claude.com/docs/en/memory).
Hook wiring: verified against hooks docs + unit-tested 2026-07-06
(v1.4.0) — pure-bash extraction, CLAUDE_PROJECT_DIR paths, fail-closed
deploy gate. Hooks load at session start; after editing them, restart
the session before relying on enforcement.
