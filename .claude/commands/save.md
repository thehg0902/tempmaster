Save all local work to the project repo's main branch.

1. `git add -A` and commit with a one-line message that describes what
   actually changed (site edits, state updates, client.md changes - all
   of it; the repo stays consistent, nothing is left dangling locally).
   If nothing changed, say so and stop.
2. `git push origin main`.
3. Report the commit hash and a one-line summary.

No gates. This is the operator's backup/sync verb - it does NOT touch
the staging or deploy branches (/stage and /deploy own those).
