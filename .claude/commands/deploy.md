Push the current local website files to the `deploy` branch (live target).

1. QA ADVISORY (always run, never skip):
   a. If site/ exists, run `python3 .claude/skills/qa-review/scripts/check.py`
      and note every FAIL.
   b. Read state/BUILD_STATE.md: is phase 6 (qa) done? Any phases blocked?
   c. Read state/QUESTIONS.md for unresolved client questions;
      grep site/ for [PLACEHOLDER (leftover placeholders).
2. Present the operator a short outstanding list (or "QA clean") and STOP
   for an explicit go/no-go. Never proceed without the go.
3. On go: run `bash scripts/deploy-split.sh` - snapshots the CURRENT LOCAL
   site/ files (uncommitted included), verifies zero OS files, and
   force-pushes the site-only result to `deploy`. If QA is not marked
   done, the script requires `--force-deploy` - add it ONLY with the
   operator's explicit go, and record in state/BUILD_STATE.md notes:
   deploy date + commit + "QA override" + the outstanding list.
   If QA was clean, record the deploy normally (URL, date, commit).
4. Report: deploy branch updated - the operator pulls it in hPanel
   (public_html) to go live. Rollback: `bash scripts/deploy-split.sh
   <previous-good-main-commit>` after the same advisory.
