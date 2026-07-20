#!/usr/bin/env bash
# PreToolUse hook: blocks git push (deploy trigger on Hostinger Git AND
# GitHub Pages) unless BUILD_STATE.md shows phase 6 (qa) = done.
# The manual-handoff deploy path (a) involves no git push, so this hook
# does not block it - /package does its own phase-6 check.
# OS-maintenance exemption: if no build has started (phase 0 intake still
# pending), a push cannot be a site deploy - template/skill maintenance
# pushes are allowed. The moment a build is in progress, the gate applies.
# v1.2.1 note: `bash scripts/deploy-split.sh` contains no "git push" (the
# push happens inside the script), so "deploy-split" is matched explicitly.
# v1.4.0: pure-bash extraction (python3 was a broken MS Store stub on the
# operator machine -> silent allow). Paths via CLAUDE_PROJECT_DIR (hooks
# have no guaranteed cwd). FAIL-CLOSED: if extraction yields nothing, the
# raw JSON is scanned instead - a parsing failure never allows a deploy.
INPUT=$(cat)
ROOT="${CLAUDE_PROJECT_DIR:-.}"
STATE="$ROOT/state/BUILD_STATE.md"
CMD=$(printf '%s' "$INPUT" | sed -n 's/.*"command"[[:space:]]*:[[:space:]]*"\(\(\\.\|[^"\\]\)*\)".*/\1/p' | head -1)
[ -z "$CMD" ] && CMD="$INPUT"   # fail-closed fallback
case "$CMD" in
  *"git push"*|*"deploy-split"*)
    case "$CMD" in
      *--force-deploy*) exit 0 ;;  # operator-approved QA override (/deploy ran
                                   # the advisory and got an explicit go; the
                                   # flag in the command line is the audit trail)
      *deploy*|*production*) : ;;  # deploy targets: gated below
      *staging*|*main*) exit 0 ;;  # staging = pre-QA demo branch (operator's
                                   # own subdomain, noindex); main = /save
                                   # backup/sync - neither is ever live
    esac
    if [ -f "$STATE" ] \
       && ! grep -E '^\|\s*0\s*\|\s*intake\s*\|\s*pending' "$STATE" >/dev/null \
       && ! grep -E '^\|\s*6\s*\|\s*qa\s*\|\s*done' "$STATE" >/dev/null; then
      echo "BLOCKED: QA phase not marked done in state/BUILD_STATE.md. Run /qa first, or use /deploy - it runs the QA advisory and, on the operator's explicit go, retries with --force-deploy." >&2
      exit 2
    fi ;;
esac
exit 0
