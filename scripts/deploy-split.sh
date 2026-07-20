#!/usr/bin/env bash
# deploy-split.sh [commit] [--force-deploy] [--no-push]
# Push the CURRENT LOCAL website files (working-tree site/, uncommitted and
# untracked included) to the site-only `deploy` branch - the live target.
# QA gate is ADVISORY: if BUILD_STATE.md phase 6 (qa) isn't done, this warns
# and exits unless --force-deploy is passed. /deploy runs the advisory,
# shows the operator what's outstanding, and adds --force-deploy only after
# an explicit in-session go (recorded in BUILD_STATE.md notes).
# Optional [commit] arg: deploy site/ as of that commit instead of the
# working tree (rollback: pass the previous good main commit).
# --no-push: build + verify the deploy commit locally, don't touch origin.
set -euo pipefail

SRC_COMMIT=""
FORCE=0
NO_PUSH=0
for arg in "$@"; do
  case "$arg" in
    --force-deploy) FORCE=1 ;;
    --no-push)      NO_PUSH=1 ;;
    *)              SRC_COMMIT="$arg" ;;
  esac
done
OS_PATHS='^(CLAUDE\.md|\.claude/|contracts/|state/|scripts/|client/|docs/)'

# --- QA gate (ADVISORY - same grep as .claude/hooks/pre-deploy-qa-gate.sh) --
if ! grep -E '^\|\s*6\s*\|\s*qa\s*\|\s*done' state/BUILD_STATE.md >/dev/null 2>&1; then
  if [ "$FORCE" = "1" ]; then
    echo "WARN: QA phase not marked done - deploying on operator override (--force-deploy)."
  else
    echo "WARN: QA phase not marked done in state/BUILD_STATE.md." >&2
    echo "Run /qa, or deploy anyway with the operator's explicit go: rerun with --force-deploy." >&2
    exit 1
  fi
fi

# --- build the site tree ----------------------------------------------------
TMP_INDEX=$(mktemp)
trap 'rm -f "$TMP_INDEX"' EXIT
if [ -n "$SRC_COMMIT" ]; then
  if ! git rev-parse -q --verify "${SRC_COMMIT}:site" >/dev/null; then
    echo "ABORT: no site/ tree at commit ${SRC_COMMIT}." >&2
    exit 1
  fi
  TREE=$(git rev-parse "${SRC_COMMIT}:site")
  echo "Using site/ as of ${SRC_COMMIT} (rollback/redeploy mode)."
else
  if [ ! -f site/index.html ]; then
    echo "ABORT: site/index.html missing - nothing to deploy." >&2
    exit 1
  fi
  GIT_INDEX_FILE="$TMP_INDEX" git read-tree --empty
  GIT_INDEX_FILE="$TMP_INDEX" git add -A site/
  FULL=$(GIT_INDEX_FILE="$TMP_INDEX" git write-tree)
  TREE=$(git rev-parse "${FULL}:site")
  echo "Snapshotted LOCAL working-tree site/ (uncommitted + untracked included)."
fi

# --- commit (keep branch history when a tip exists) --------------------------
PARENT=$(git rev-parse -q --verify refs/remotes/origin/deploy 2>/dev/null \
      || git rev-parse -q --verify refs/heads/deploy 2>/dev/null || true)
if [ -n "$PARENT" ]; then
  COMMIT=$(git commit-tree "$TREE" -p "$PARENT" -m "deploy: local site snapshot")
else
  COMMIT=$(git commit-tree "$TREE" -m "deploy: local site snapshot")
fi
echo "Deploy commit: ${COMMIT}"

# --- cleanliness check (proof the branch is site-only) -----------------------
FILES=$(git ls-tree -r --name-only "$COMMIT")
echo "--- files at deploy tip ---"
echo "$FILES"
echo "---------------------------"
if echo "$FILES" | grep -E "$OS_PATHS" ; then
  echo "FAIL: OS files found in the snapshot - deploy would leak Agency OS files. NOT pushing." >&2
  exit 1
fi
echo "PASS: snapshot contains only site files."

git branch -f deploy "$COMMIT"

# --- push (graceful if no remote; skipped with --no-push) --------------------
if [ "$NO_PUSH" = "1" ]; then
  echo "NOTE: --no-push - deploy commit verified locally, origin untouched."
  exit 0
fi
if ! git remote get-url origin >/dev/null 2>&1; then
  echo "NOTE: no 'origin' remote configured - skipping push. Verified locally."
  exit 0
fi
git push origin "${COMMIT}:refs/heads/deploy" --force
echo "Pushed ${COMMIT} -> origin/deploy. Pull it in hPanel (public_html) to go live."
