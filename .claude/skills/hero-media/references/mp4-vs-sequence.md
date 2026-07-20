# MP4 vs JPEG Sequence
| Need | Use |
|---|---|
| Autoplay ambiance, play-once | MP4 h.264 |
| Scroll-scrubbed motion | JPEG/WebP sequence on canvas |
| Alpha/transparency over page bg | Sequence (or WebM+alpha w/ mp4 fallback) |
| Lowest effort, best compression | MP4 |
MP4 encoding: h.264 high profile, CRF 23-26, AAC stripped (an audio track
wastes bytes on a muted video), faststart flag, 1080p max (720p often
indistinguishable in a hero), 24fps. Poster: extract final frame ->
.webp q80 - the final frame, because freeze/returning states land there.
Sequence: cap ~60-90 frames, .webp q75, preload progressively, draw to
canvas sized by devicePixelRatio capped at 2.
