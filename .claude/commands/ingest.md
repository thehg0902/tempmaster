Ingest operator-provided assets from the slot folder.

1. Run `python3 scripts/ingest-assets.py`. It matches files in
   client/assets-intake/slots/ against SHOPPING_LIST.md, processes each
   per its treatment (contracts/asset-slots.md), places outputs under
   site/assets/, ticks the list, and updates state/MEDIA_LOG.md.
2. Read the report:
   - PENDING = a tool (ffmpeg/cwebp) is missing; give the user the
     printed commands, mark those assets pending-optimization.
   - UNFILLED = no file and not ticked: these are Higgsfield
     candidates. Present them in-chat with estimated credits and wait
     for explicit per-slot approval (media-log contract rule 1) before
     any paid generation; record YES [in-chat <date>] in MEDIA_LOG.
   - UNKNOWN = files that match no slot; ask the user, never guess.
   - FLAG = over-budget output, filename conflicts across placement
     folders, or ticks without files; resolve before shipping.
3. If all slots are DONE, report Phase 4 media complete in
   state/BUILD_STATE.md and continue the pipeline (Phase 5 wires
   players per hero-media treatment templates).
4. Re-run any time; already-ticked slots are skipped (use --force to
   re-process).
