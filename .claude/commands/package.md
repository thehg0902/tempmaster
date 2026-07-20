Package the standalone site for manual delivery.

1. Verify phase 6 (qa) = done in state/BUILD_STATE.md. If not, STOP and
   say /qa must pass first.
2. Zip the CONTENTS of site/ (archive root = index.html, so unzip =
   ready-to-upload; exclude .gitkeep files) to
   `deliverables/<client-name>-<YYYY-MM-DD>.zip`, creating deliverables/
   if absent (it is gitignored). Client name from state/BUILD_STATE.md,
   kebab-cased.
3. Print the zip path and the file count inside the archive.
