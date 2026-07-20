---
name: deploy-hostinger
description: Deploy the static site - Hostinger Git, GitHub Pages, or
  packaged manual handoff - branch strategy, deploy steps, rollback,
  post-deploy checks. Use via the four control verbs (/demo /stage
  /save /deploy) and for retainer redeploys. Not for DNS (domains-dns).
metadata: {version: 1.5.0, category: deploy, tier: E}
---
# Deploy (Hostinger Git / GitHub Pages / manual)

## Purpose
Push-to-deploy: the repo's deploy branch is the live site.

## Inputs
Local site/ files, Hostinger repo connection (one-time setup below),
the QA advisory result + the operator's explicit go (CLAUDE.md
invariant; QA is advisory, the go is mandatory).

## Outputs
Live site; deploy record (URL, date, commit) in BUILD_STATE.md.

## Rules
1. One-time setup (human does in hPanel, Claude provides this checklist):
   Websites -> manage -> Advanced -> Git -> connect the client repo,
   branch `deploy`, target directory public_html. The ROOT of the
   deploy branch IS the site - no subdirectory. Enable the
   auto-deploy webhook if offered (unchanged). VERIFY current hPanel
   labels against Hostinger docs at setup time - panels change.
   First-deploy checklist item: after Hostinger's first pull, open File
   Manager and verify public_html contains ONLY site files (with the
   placeholder bootstrap this should always pass; leftovers from older
   manual uploads - zips, .claude/, package.json, README, serve.ps1 -
   have burned an operator before, so verify, and delete if found).
   Demo subdomain (optional, one-time, operator's own domain): hPanel ->
   create the subdomain -> its site -> Advanced -> Git -> connect the
   SAME client repo, branch `staging`, target = the subdomain's public
   folder. Deploys are triggered MANUALLY (hPanel Deploy button) unless
   the operator chooses to enable the webhook.
2. The four control verbs (branch placeholders created at fresh-build
   start by scripts/bootstrap-branches.sh - safe site-only stubs).
   Both split scripts snapshot the CURRENT LOCAL site/ working tree
   (uncommitted + untracked included) to the branch root and prove the
   result contains zero OS files. Generated branches are written ONLY
   by their script - never commit to them manually.
   - /stage -> `bash scripts/stage-split.sh` -> `staging`: pre-QA demo,
     no gate, forced noindex robots.txt; hosted only on the OPERATOR's
     demo subdomain, never the client's production domain.
   - /save -> commit all local changes, push `main`: backup/sync verb,
     no gate, touches no hosting branch.
   - /deploy -> QA ADVISORY first (check.py FAILs, BUILD_STATE phases,
     QUESTIONS.md, leftover [PLACEHOLDER]s), present outstanding items,
     STOP for the operator's explicit go; then
     `bash scripts/deploy-split.sh` -> `deploy` (production). If QA
     isn't marked done the script refuses without `--force-deploy` -
     added only on the operator's go, and the override + outstanding
     list is recorded in BUILD_STATE.md notes. The pre-deploy hook
     enforces the same rule on raw pushes.
   - /demo -> bootstrap-branches.sh + stage-split.sh: one-shot setup
     (both branches exist, hosting connectable) + first staging push.
3. The OS files (CLAUDE.md, .claude/, contracts/, state/, scripts/,
   client/, docs/) must never reach the live webroot - the split's
   cleanliness check is the proof, printed on every deploy.
4. Post-deploy checks (do all, record results): live URL 200s per page;
   assets load (no mixed-content, correct paths); form test submission;
   Calendly opens; https padlock; sitemap.xml reachable; analytics
   realtime hit. Hosting-plan extras: Business plan -> enable the CDN
   toggle in hPanel and verify it serves (response headers); Premium
   plan -> verify the .htaccess Cache-Control headers respond
   (security-basics block; required by the no-cdn performance profile).
5. Rollback: `bash scripts/deploy-split.sh <previous-good-main-commit>` -
   the optional commit arg splits site/ as of that commit and pushes it
   to deploy. Practice path documented > clever path.

## Deploy modes (chosen at the Phase 7 gate, per build)
- Hostinger Git: rules 1-5 above.
- GitHub Pages: references/github-pages.md (serving options for the
  site/ subdir, custom domain, HTTPS). The QA-gate hook applies to the
  push exactly as for Hostinger.
- Manual handoff: run /package; deliver the zip yourself. Record
  `deploy: manual — packaged <zip path>` in BUILD_STATE.md; post-deploy
  checks are the operator's responsibility on whatever host they use.

## References
- references/github-pages.md - GitHub Pages setup + site/-subdir options

## Anti-patterns
- Deploying from an uncommitted working tree; committing manually to
  the deploy or staging branch - both are generated output, and their
  split scripts' force-push is the only writer; connecting the CLIENT's
  production domain to staging (the demo lives on the operator's own
  subdomain only); editing files directly in hPanel file manager
  (breaks Git state).

## Changelog
- 1.5.0 control verbs: /demo /stage /save /deploy; splits snapshot the
  LOCAL working tree (uncommitted included); QA gate is now an ADVISORY
  + explicit operator go (--force-deploy override, recorded);
  demo-split.sh renamed stage-split.sh (v1.10.0)
- 1.4.0 demo branch: staging repurposed to a generated site-only demo
  branch (demo-split.sh: same split + leak check, no QA gate, forced
  noindex robots.txt) for MANUAL hPanel deploys to the operator's demo
  subdomain; bootstrap-branches.sh creates both branches as safe
  site-only placeholders (v1.9.0)
- 1.3.0 branch bootstrap: staging (preview, gate-exempt) + deploy
  created at fresh-build start; production renamed to deploy (v1.6.1)
- 1.2.0 clean deploy branch: generated by scripts/deploy-split.sh
  (site/ contents only), rollback via commit arg, first-pull cleanup check
- 1.1.0 three deploy modes: Hostinger Git, GitHub Pages, manual handoff
- 1.0.0 initial (encodes the hPanel Git workflow)
