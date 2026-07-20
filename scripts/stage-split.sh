#!/usr/bin/env bash
# stage-split.sh [commit] [--no-push]
# Push the CURRENT LOCAL website files (working-tree site/, uncommitted and
# untracked included) to the site-only `staging` DEMO branch. NO QA gate -
# staging is the pre-QA preview by design (/stage, /demo). robots.txt is
# forced to noindex so search engines never index a demo that may still
# contain [PLACEHOLDER] text.
# The operator deploys it MANUALLY in hPanel: branch `staging` -> the demo
# subdomain's public folder. Never connect the client's production domain.
# Optional [commit] arg: stage site/ as of that commit instead of the
# working tree. --no-push: verify locally without touching origin.
set -euo pipefail

SRC_COMMIT=""
NO_PUSH=0
for arg in "$@"; do
  case "$arg" in
    --no-push) NO_PUSH=1 ;;
    *)         SRC_COMMIT="$arg" ;;
  esac
done
OS_PATHS='^(CLAUDE\.md|\.claude/|contracts/|state/|scripts/|client/|docs/)'

# --- build the site tree ----------------------------------------------------
TMP_INDEX=$(mktemp)
trap 'rm -f "$TMP_INDEX"' EXIT
if [ -n "$SRC_COMMIT" ]; then
  if ! git rev-parse -q --verify "${SRC_COMMIT}:site" >/dev/null; then
    echo "ABORT: no site/ tree at commit ${SRC_COMMIT}." >&2
    exit 1
  fi
  TREE=$(git rev-parse "${SRC_COMMIT}:site")
  echo "Using site/ as of ${SRC_COMMIT}."
else
  if [ ! -f site/index.html ]; then
    echo "ABORT: site/index.html missing - nothing to stage." >&2
    exit 1
  fi
  GIT_INDEX_FILE="$TMP_INDEX" git read-tree --empty
  GIT_INDEX_FILE="$TMP_INDEX" git add -A site/
  FULL=$(GIT_INDEX_FILE="$TMP_INDEX" git write-tree)
  TREE=$(git rev-parse "${FULL}:site")
  echo "Snapshotted LOCAL working-tree site/ (uncommitted + untracked included)."
fi

# --- force noindex robots.txt on the demo branch only ------------------------
ROBOTS_BLOB=$(printf 'User-agent: *\nDisallow: /\n' | git hash-object -w --stdin)
GIT_INDEX_FILE="$TMP_INDEX" git read-tree "$TREE"
GIT_INDEX_FILE="$TMP_INDEX" git update-index --add \
  --cacheinfo "100644,${ROBOTS_BLOB},robots.txt"
TREE=$(GIT_INDEX_FILE="$TMP_INDEX" git write-tree)

# --- commit (keep branch history when a tip exists) --------------------------
PARENT=$(git rev-parse -q --verify refs/remotes/origin/staging 2>/dev/null \
      || git rev-parse -q --verify refs/heads/staging 2>/dev/null || true)
if [ -n "$PARENT" ]; then
  COMMIT=$(git commit-tree "$TREE" -p "$PARENT" -m "stage: local site snapshot (noindex)")
else
  COMMIT=$(git commit-tree "$TREE" -m "stage: local site snapshot (noindex)")
fi
echo "Staging commit (noindex): ${COMMIT}"

# --- cleanliness check (proof the branch is site-only) -----------------------
FILES=$(git ls-tree -r --name-only "$COMMIT")
echo "--- files at staging tip ---"
echo "$FILES"
echo "----------------------------"
if echo "$FILES" | grep -E "$OS_PATHS" ; then
  echo "FAIL: OS files found in the snapshot - demo would leak Agency OS files. NOT pushing." >&2
  exit 1
fi
echo "PASS: snapshot contains only site files (+ noindex robots.txt)."

git branch -f staging "$COMMIT"

# --- push (graceful if no remote; skipped with --no-push) --------------------
if [ "$NO_PUSH" = "1" ]; then
  echo "NOTE: --no-push - staging commit verified locally, origin untouched."
  exit 0
fi
if ! git remote get-url origin >/dev/null 2>&1; then
  echo "NOTE: no 'origin' remote configured - skipping push. Verified locally."
  exit 0
fi
git push origin "${COMMIT}:refs/heads/staging" --force
echo "Pushed ${COMMIT} -> origin/staging. Pull it in hPanel (demo subdomain) to view."
