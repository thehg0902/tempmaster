#!/usr/bin/env bash
# PreToolUse hook: blocks git commits that stage likely secrets.
# Receives hook JSON on stdin; exit 2 = block (stderr shown to Claude).
# v1.4.0: pure-bash extraction (no python3/jq - external interpreters
# proved unreliable on the operator's Windows machine). Repo path via
# CLAUDE_PROJECT_DIR (hooks have no guaranteed cwd).
INPUT=$(cat)
ROOT="${CLAUDE_PROJECT_DIR:-.}"
CMD=$(printf '%s' "$INPUT" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\(\(\\.\|[^"\\]\)*\)".*/\1/p' | head -1)
[ -z "$CMD" ] && CMD="$INPUT"   # fail-closed fallback
case "$CMD" in
  *"git commit"*|*"git add"*)
    if git -C "$ROOT" diff --cached 2>/dev/null | grep -Eiq '(api[_-]?key|secret|password|token)["'"'"' ]*[:=]["'"'"' ]*[A-Za-z0-9_\-]{12,}'; then
      echo "BLOCKED: staged changes appear to contain a secret. Remove it, use env vars." >&2
      exit 2
    fi ;;
esac
exit 0
