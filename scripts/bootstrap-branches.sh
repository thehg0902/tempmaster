#!/usr/bin/env bash
# bootstrap-branches.sh
# Create `staging` and `deploy` as SAFE site-only placeholders (an orphan
# commit holding only index.html "coming soon" + a noindex robots.txt) if
# they don't exist locally or on origin. Run at fresh-build start (/build
# bootstrap). Hosting can then be connected to either branch at any time
# with zero OS files leaked. Real content comes from the only writers:
# scripts/stage-split.sh (staging) and scripts/deploy-split.sh (deploy).
set -euo pipefail

TMP_INDEX=$(mktemp)
trap 'rm -f "$TMP_INDEX"' EXIT
GIT_INDEX_FILE="$TMP_INDEX" git read-tree --empty
HTML_BLOB=$(printf '<!doctype html>\n<meta charset="utf-8">\n<meta name="robots" content="noindex">\n<title>Site coming soon</title>\n<h1>Site coming soon</h1>\n' | git hash-object -w --stdin)
ROBOTS_BLOB=$(printf 'User-agent: *\nDisallow: /\n' | git hash-object -w --stdin)
GIT_INDEX_FILE="$TMP_INDEX" git update-index --add \
  --cacheinfo "100644,${HTML_BLOB},index.html"
GIT_INDEX_FILE="$TMP_INDEX" git update-index --add \
  --cacheinfo "100644,${ROBOTS_BLOB},robots.txt"
TREE=$(GIT_INDEX_FILE="$TMP_INDEX" git write-tree)

HAVE_REMOTE=0
git remote get-url origin >/dev/null 2>&1 && HAVE_REMOTE=1

for BR in staging deploy; do
  if git show-ref --verify --quiet "refs/heads/${BR}"; then
    echo "SKIP: ${BR} already exists locally."
    continue
  fi
  if [ "$HAVE_REMOTE" = "1" ] && git ls-remote --exit-code --heads origin "$BR" >/dev/null 2>&1; then
    echo "SKIP: ${BR} already exists on origin."
    continue
  fi
  C=$(git commit-tree "$TREE" -m "bootstrap: safe site-only placeholder for ${BR}")
  git branch "$BR" "$C"
  echo "Created ${BR} -> ${C} (placeholder: index.html + noindex robots.txt)"
  if [ "$HAVE_REMOTE" = "1" ]; then
    git push origin "refs/heads/${BR}:refs/heads/${BR}"
    echo "Pushed ${BR} to origin."
  fi
done
