# Contract: Asset Slots  (v1.1.0)

The interface between media planning (media-generation), the operator's
manual generation workflow, ingestion (scripts/ingest-assets.py via
/ingest), and playback code (hero-media). One folder, one list, exact
filenames.

## The drop zone

`client/assets-intake/slots/` — the operator saves every incoming asset
here, named EXACTLY as the shopping list says. Slot media files are
gitignored (heavy originals); SHOPPING_LIST.md is tracked.

PLACEMENT FOLDERS (v1.5.0, per-project since v1.6.0): Phase 4 creates
one subfolder per placement, named `<Page> - <what goes there>` and
DERIVED FROM THIS SITE'S actual page/section map + niche — every
project's folder set looks different. A coffee shop might get
`Home - Hero coffee/`, `Home - Menu images/`; a roofer
`Home - Hero/`, `About us - Before and after/`. Each shopping-list
block carries a `folder:` line. Drop each file into its matching
folder. Folders are organizational only — /ingest matches RECURSIVELY
by exact filename, so a file at the slots/ root still works; the same
filename in two folders is reported as a conflict, never guessed.

INTAKE SWEEP (v1.6.0): client-provided files land in
client/assets-intake/ before any build. At Phase 0 they are
INVENTORIED (filenames classified by convention: logo*, hero1/hero2*,
gallery1/gallery2*, team*, menu*, before*/after*, ...). At Phase 4,
when the placement folders exist, matching intake files are MOVED into
their folders, their slots renamed-to/matched and PRE-TICKED `[x]` in
the shopping list, and their MEDIA_LOG rows recorded as
model=client, credits 0. Numbered sequences (gallery1, gallery2, ...)
map to numbered slots. Only the GAPS get prompts/generation — client
material always beats generated material (media-generation rule 3).

## Slot naming grammar

`<section>-<treatment>[-NN].<ext>`   (kebab-case, per file-structure rules)

- `hero-loop.mp4`          hero section, looping video
- `hero-intro.mp4` + `hero-loop.mp4`   intro+loop pair (both required)
- `hero-scrub.mp4`         hero section, scroll-scrub source video
- `about-loop.mp4`         any section can take a treatment
- `gallery-01.jpg`         numbered stills
- `logo.png`               reserved name; alpha rules apply

## Treatments (the vocabulary)

| treatment | source | ingest output | player template (hero-media) |
|---|---|---|---|
| loop | one mp4 | re-encoded mp4 + poster webp -> site/assets/video/ | loop-crossfade.js (rAF dip-to-black; use native loop attr only for footage designed seamless) |
| intro-loop | two mp4s (-intro, -loop) | both re-encoded + poster from intro first frame | intro-loop.js (intro once, rAF crossfade to loop) |
| scroll-scrub | one mp4 | frame sequence + manifest.json -> site/assets/images/scrub/<slot>/ | scrub-player.js (canvas) |
| static / image | jpg/png | webp (+srcset variants) -> site/assets/images/ | plain <img> |
| alpha | png with transparency | PNG passthrough, never flattened | plain <img> |

## SHOPPING_LIST.md format

Lives at `client/assets-intake/slots/SHOPPING_LIST.md`. Written by
media-generation in Phase 4. One block per slot:

    ## <exact-filename>        [ ] filled
    folder: <Page> - <Section>/
    treatment: <treatment> - <duration/aspect/other spec>
    <one line of intent/constraints>
    PROMPT ->
    <full copy-paste generation prompt, multi-line allowed>

Tick semantics (v1.5.0):
- The OPERATOR ticks `[x]` after dropping the file in its folder
  ("I supplied this"). /ingest also auto-ticks anything it processes,
  so a forgotten tick self-heals.
- A slot left `[ ]` with NO file at ingest time = a Higgsfield
  candidate: /ingest lists it and Claude asks in-chat for generation
  approval (named slots + estimated credits; media-log contract rule 1).
- Ticked but file missing = warning (tick without a file does nothing).
The list is a worksheet; state/MEDIA_LOG.md remains the ledger of record.

## MEDIA_LOG mirroring

Every shopping-list slot gets a MEDIA_LOG row at Phase 4 with
`id = slot filename`, `status = planned`. Operator-provided files:
`model = operator`, `credits = 0` — the paid-generation approval
invariant is untouched (it gates PAID generation only). /ingest sets
`file` to the final site/assets path and `status = in-use`.

## Scrub manifest.json (written by ingest, read by scrub-player.js)

    {"slot": "hero-scrub", "frames": 120, "fps": 12,
     "width": 1440, "height": 810, "pattern": "frame-%04d.webp"}

Lives next to its frames: `site/assets/images/scrub/<slot>/manifest.json`.
frame numbering starts at 0001. Frame 0001 doubles as the poster/
reduced-motion fallback.

## Rules

1. The shopping list is the single source of slot names. /ingest matches
   by exact filename; unexpected files are reported, never guessed at.
2. Filenames are law: renaming a slot after Phase 4 requires updating
   SHOPPING_LIST.md + MEDIA_LOG row + any wired template in the same
   change.
3. Ingest is idempotent: re-running processes only unfilled or changed
   slots; it never re-encodes an already-processed unchanged file.
4. Every ingest output lands per contracts/file-structure.md; nothing
   is ever served from client/assets-intake/.
5. Weight budgets (performance skill) are enforced at ingest time:
   over-budget outputs are flagged in the ingest report, not silently
   shipped.
