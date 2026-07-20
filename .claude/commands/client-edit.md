Handle a retainer client change request: $ARGUMENTS

1. Read the maintenance-retainer skill and follow its workflow.
2. Locate the change surface (grep before reading whole files).
3. Make the minimal edit; obey contracts; never regenerate whole pages
   for small edits.
4. Verify locally per the skill's checklist, commit with message
   "client-edit: <summary>", then follow /deploy rules (QA gate applies
   in reduced form per the skill).
5. Log the edit in state/DECISIONS.md (date | client-edit | summary).
