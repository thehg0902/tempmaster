# Media Shopping List — Temp Master (Phase 4)

Written by media-generation per contracts/asset-slots.md. Drop each file
into its `folder:` under the EXACT slot filename, tick `[x]`, then run
/ingest. Slots left unticked with no file become Higgsfield candidates
(in-chat approval required before any paid generation).

CONSTRAINTS (apply to every generation prompt below):
- Photos policy is UNCONFIRMED in client.md — treat as undecided; the
  three image slots below have prompts ready but generating them (paid
  or manual AI) should wait until Photos policy is confirmed, or supply
  real photos instead (always preferred).
- People in imagery UNCONFIRMED — all prompts are NO-PEOPLE (no faces,
  no fake technicians presented as staff; media-generation rule 3).

STYLE BLOCK (reuse verbatim in every image prompt):
"Photo-realistic, clean bright daylight, cool blue sky, crisp suburban
Ontario residential setting, modern detached home exterior, natural
color grading with cool blue tones and warm neutral siding, sharp focus,
high detail, no people, no text, no watermarks, no logos."

---

## hero-loop.mp4        [x] filled
folder: Home - Hero video/
treatment: loop - 5.04s, 1916x1080, 24fps, h264, 3.0MB (client-provided)
Idle hero background loop for the full-bleed home hero stage.
PROMPT ->
(client-provided file — no generation needed; /ingest re-encodes to
budget and extracts hero-poster.webp from frame 1)

## hero-transition.mp4        [x] filled
folder: Home - Hero video/
treatment: scroll-scrub (operator changed from a real-time play-once/
reverse video to a true scroll-scrubbed frame sequence, 2026-07-20) -
source 5.04s 1916x1080 24fps h264 7.8MB (client-provided), extracted to
61 webp frames @ 1440x812, 12fps, q70, 2.9MB total -> site/assets/images/
scrub/hero-transition/ + manifest.json. The source MP4 is no longer
shipped (site/assets/video/hero-transition.mp4 removed - dead weight
once the canvas scrub replaced it).
PROMPT ->
(client-provided file — no generation needed; frame extraction only)

## logo.png        [x] filled
folder: Brand - Logo/
treatment: alpha - PNG passthrough, 1536x1024 RGBA (client-provided)
Header + footer brand mark; never flattened.
PROMPT ->
(client-provided file — no generation needed; /ingest may emit resized
copies but keeps PNG alpha)

## services-ac.jpg        [x] filled
folder: Home - AC service feature/
treatment: static - superseded by a real client job photo instead of
generating (real beats generated, media-generation rule 3)
Home page featured-service card image (AC specialty block).
RESOLVED -> gallery-wall-mount-ac.webp (client-provided, from the "Our
Work" gallery set) reused here; no generation needed.

## ac-install.jpg        [x] filled
folder: AC page - Install/
treatment: static - superseded by a real client job photo instead of
generating (real beats generated, media-generation rule 3)
AC page "Installation" split-section image.
RESOLVED -> gallery-ductless-condenser.webp (client-provided, from the
"Our Work" gallery set) reused here; no generation needed.

## ac-repair.jpg        [x] filled
folder: AC page - Repair/
treatment: static - 4:3, min 1600x1200, target <300KB after webp
AC page "Repair" split-section image. No real photo matched this scene
(none of the 6 client job photos show mid-repair/diagnosis) - generated
via Higgsfield (marketing_studio_image), operator-approved in-chat
2026-07-20, 2 credits.
PROMPT ->
An open residential central AC condenser unit with its service panel
removed, revealing the fan and coil, a digital multimeter and pressure
gauge set resting on top of the unit, suggesting an in-progress
diagnosis. Photo-realistic, clean bright daylight, cool blue sky, crisp
suburban Ontario residential setting, modern detached home exterior,
natural color grading with cool blue tones and warm neutral siding,
sharp focus, high detail, no people, no text, no watermarks, no logos.
RESULT -> site/assets/images/ac-repair.webp (1000x747, 139KB)
