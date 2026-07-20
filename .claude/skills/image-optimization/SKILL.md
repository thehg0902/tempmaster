---
name: image-optimization
description: Convert and compress media for the web - WebP conversion, srcset
  size variants, video re-encode to budget, poster extraction. Use whenever
  files move into assets/ (client photos or generated media). Not for
  choosing what to generate (media-generation).
metadata: {version: 1.1.0, category: media, tier: C}
---
# Image Optimization

## Purpose
Nothing enters site/assets/ raw. Every file web-ready, budget-compliant,
named per contract.

## Inputs
Files from client/assets-intake/ or fresh generations; performance budgets.

## Outputs
Optimized files in site/assets/images|video per file-structure contract.

## Rules
1. Quality-first ladder (priority law: performance floors first, then
   maximum quality within them). Free transforms ALWAYS run: resize to
   the 1440px display cap, WebP conversion, EXIF strip. The LOSSY level
   adapts: q90 -> q82 -> q75, stepping down ONLY while over budget.
   Budgets per hosting profile (performance skill rule 1): image
   300KB/200KB, poster 200KB/150KB (cdn/no-cdn). /ingest implements
   this automatically and reports the kept level + headroom. Keep a jpg
   fallback only if a target embed requires it (og:image: jpg/png
   1200x630).
1a. Alpha assets (logos, icons, any image with transparency): NEVER
   flatten. The white-background failure mode is flattening or a
   conversion path that drops alpha - WebP itself supports alpha. Keep
   the original PNG as an always-valid option; WebP-with-alpha is
   allowed ONLY if converted with alpha preserved AND visually verified
   on the site's actual background colors. When in doubt, ship the PNG.
   Budget note: logos are small; PNG weight is acceptable here.
2. srcset variants for images displayed > 400px wide: 480/960/1440 widths;
   name {base}-{w}.webp.
3. Video -> hero-media encoding settings (references there are canonical);
   extract final frame as {name}-poster.webp.
4. Tooling: /ingest is the canonical adaptive path (cwebp -> Pillow ->
   pending; video/scrub/posters need only ffmpeg). scripts/optimize.sh
   is the fixed-settings manual fallback for one-off files. If tools
   are missing, DO NOT fake it - the scripts print the exact commands
   to run locally; mark the asset pending-optimization in MEDIA_LOG.
5. Record final byte sizes in MEDIA_LOG prompt-summary or notes - budgets
   are verified numbers, not vibes.

## Scripts
- scripts/optimize.sh <file> - converts per rules; prints before/after
  bytes. PNGs with alpha are auto-detected and passed through unflattened
  (also forceable with `--logo` / `--keep-alpha`); the script prints an
  alpha-preservation check result.

## Anti-patterns
- Committing multi-MB originals to the repo; resizing with CSS instead of
  files.

## Changelog
- 1.1.0 alpha assets never flattened; PNG explicitly permitted
- 1.0.0 initial
