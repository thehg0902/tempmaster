---
name: hero-media
description: Implement hero/section motion media - looping video
  (crossfade), intro+loop handoff, scroll-scrub frame sequences,
  play-once-then-freeze, reverse-then-freeze, returning-visitor
  detection. Use when building or editing any section with
  video/sequence media. Not for general page animation
  (frontend-animation) or generating the media itself (media-generation).
metadata: {version: 1.1.0, category: frontend, tier: B}
---
# Hero Media

## Purpose
Cinematic hero motion that is fast, robust, and plays exactly once per
visitor - the agency's signature hero system.

## Inputs
client.md Stack hero-media flag, ingested assets in site/assets/ (with
MEDIA_LOG rows; scrub manifests per contracts/asset-slots.md),
tokens.css, contracts/file-structure.md.

## Outputs
Hero section markup + hero JS in the hero page's script.js + poster
assets wired in (assets central in site/assets/).

## Rules
1. Format decision per references/mp4-vs-sequence.md. Default: MP4
   (h.264, muted, playsinline) with .webp poster. Sequence only when
   scroll-scrubbing or transparency is required.
2. Behavior default: play once on first visit, freeze on final frame;
   returning visitors (localStorage flag, site-slug prefixed) see the
   final frame immediately - templates/returning-visitor.js.
3. Play-once: templates/play-once-freeze.js (pause on 'ended', never
   loop). Reverse effects: templates/reverse-freeze.js (rAF-driven
   currentTime stepping - native reverse playback is not reliable).
4. Poster is mandatory and is the LCP candidate: preload it, size it,
   never lazy-load hero media.
5. Reduced motion: prefers-reduced-motion users get the poster only -
   wire in JS, not just CSS.
6. Autoplay requires muted + playsinline; never audio. If autoplay is
   blocked, the poster stands - design so the frozen frame is a complete
   hero on its own.
7. Weight budget: hero video <= 2.5MB target, <= 4MB hard cap, <= 8s;
   over budget -> re-encode or cut before shipping (performance skill
   verifies).
8. Treatment selection follows the Stack flag / shopping-list treatment
   (contracts/asset-slots.md):
   - loop: templates/loop-crossfade.js - rAF dip-to-black hides the cut;
     use the native loop attribute ONLY for footage designed seamless.
   - intro-loop: templates/intro-loop.js - intro plays once, rAF
     crossfade hands off to the natively-looping loop video; poster =
     intro's first frame.
   - scroll-scrub: templates/scrub-player.js reads the /ingest manifest;
     canvas-based, never video.currentTime (references/scroll-scrub.md);
     scrub section is taller than the viewport with a sticky inner
     stage; frame 0001 doubles as poster.
   All three keep rules 4-6: poster mandatory, reduced-motion gets the
   poster, muted+playsinline, frozen frame is a complete hero.

## References
- references/mp4-vs-sequence.md - decision table + encoding settings
- references/scroll-scrub.md - canvas vs currentTime, budget math,
  section sizing, progressive loading

## Scripts / Templates
- templates/hero-video.html - canonical markup
- templates/play-once-freeze.js, reverse-freeze.js, returning-visitor.js
- templates/loop-crossfade.js, intro-loop.js, scrub-player.js
  (v1.3.0 slot treatments)
  (copy into the hero page's script.js and adapt; keep the defensive
  guards; asset paths: `assets/...` from site/ root, `../assets/...`
  from a page folder)

## Anti-patterns
- Looping hero video (distracting, battery); YouTube embeds as heroes;
  lazy-loading the poster; localStorage keys without site prefix.

## Changelog
- 1.1.0 slot treatments: loop-crossfade, intro-loop, scroll-scrub
- 1.0.0 initial (encodes patterns from prior client work)
