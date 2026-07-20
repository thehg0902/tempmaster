# Scroll-Scrub Implementation Guide

## Canvas frames vs video.currentTime — always canvas
| | canvas + webp frames | video currentTime scrubbing |
|---|---|---|
| iOS Safari | smooth | janky (keyframe seeking) |
| control | exact frame per scroll position | seek latency varies |
| tooling | needs extraction (/ingest does it) | needs all-intra re-encode (-g 1), huge files |
Verdict: canvas. /ingest extracts frames + writes manifest.json
automatically (contracts/asset-slots.md).

## Budget math (performance-critical)
frames = duration_s x fps. Defaults: 12fps, 1440px wide, webp q70.
- 8s source -> ~96 frames x 40-80KB ~= 4-8MB. Cap: 10MB per sequence
  (ingest flags overages). Longer footage: cut the source, don't raise fps.
- 12fps is enough: scroll interpolates position, not time; the eye reads
  scrub motion as continuous well below 24fps.

## Section sizing
The scrub section must be TALLER than the viewport - progress maps to
(-rect.top / (height - viewportHeight)). Typical: height: 300vh with a
position: sticky inner viewport holding the canvas. No scroll-jacking:
native scroll drives everything (frontend-animation anti-pattern rule
applies).

## Loading strategy
Frame 0001 loads first and draws immediately (it IS the poster /
reduced-motion fallback). Then every 4th frame, then backfill; the
player draws the nearest loaded frame until the exact one arrives -
scrubbing degrades to slightly steppy, never blank.

## Reduced motion / no-JS
prefers-reduced-motion: frame 0001 only, no scroll listener. No JS: the
canvas is empty - always set the section's CSS background (or an <img>
fallback inside <noscript>) so the section stands without the effect.
