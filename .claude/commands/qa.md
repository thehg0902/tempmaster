Run the pre-delivery QA gate.

1. Run `python3 .claude/skills/qa-review/scripts/check.py`. Fix every FAIL
   it reports, re-run until clean.
2. Run /visual-qa (visual-qa skill): rendered audit of every page at
   360/768/1280 against the layout checklist, design rationale, and
   vibe refs. Every page must PASS.
3. Then perform the manual review in the qa-review skill (read it now) -
   the resize pass is covered by step 2; focus on facts, copy, and
   click-paths.
4. Write results to state/BUILD_STATE.md notes. Mark phase 6 done ONLY if
   the script passes, visual QA passes, and manual review has no
   criticals. Otherwise list what blocks, mark phase 6 blocked.
