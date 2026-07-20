#!/usr/bin/env bash
# Usage: optimize.sh [--logo|--keep-alpha] <input> [max-width]
# Requires cwebp (images) / ffmpeg (video). Prints commands it runs + sizes.
# Alpha assets (logos/icons): NEVER flattened - auto-detected for PNG, or
# forced with --logo / --keep-alpha. PNG passes through unconverted.
set -e
MODE=""
case "$1" in --logo|--keep-alpha) MODE="keep-alpha"; shift ;; esac
IN="$1"; W="${2:-1440}"
[ -f "$IN" ] || { echo "no such file: $IN" >&2; exit 1; }
BASE="${IN%.*}"; EXT="${IN##*.}"

# PNG alpha check: IHDR color type (byte 25, 0-based) 4 or 6 = alpha
# channel; type 3 (palette) has transparency when a tRNS chunk exists.
png_has_alpha() {
  local ct
  ct=$(od -An -j25 -N1 -tu1 "$1" | tr -d ' ')
  [ "$ct" = "4" ] || [ "$ct" = "6" ] || { [ "$ct" = "3" ] && grep -aq tRNS "$1"; }
}

case "$EXT" in
  png)
    if [ "$MODE" = "keep-alpha" ] || png_has_alpha "$IN"; then
      # Alpha asset: copy through, no lossy/flattening path, no resize.
      OUT="${BASE}-web.png"
      cp "$IN" "$OUT"
      if png_has_alpha "$OUT"; then
        echo "alpha preserved: YES ($OUT)"
      else
        echo "alpha preserved: NO - DO NOT SHIP, investigate" >&2; exit 1
      fi
      ls -l "$IN" "$OUT"
      echo "note: PNG kept per alpha rule. Optional WebP-with-alpha:"
      echo "  cwebp -exact -q 90 '$IN' -o '${BASE}.webp'  (then VISUALLY verify on the site's background colors)"
      exit 0
    fi
    ;;
esac

case "$EXT" in
  jpg|jpeg|png)
    command -v cwebp >/dev/null || { echo "cwebp missing - run locally: cwebp -q 80 -resize $W 0 '$IN' -o '${BASE}.webp'"; exit 2; }
    cwebp -q 80 -resize "$W" 0 "$IN" -o "${BASE}.webp"
    ls -l "$IN" "${BASE}.webp" ;;
  mp4|mov|webm)
    command -v ffmpeg >/dev/null || { echo "ffmpeg missing - run locally: ffmpeg -i '$IN' -an -c:v libx264 -crf 24 -movflags +faststart -vf scale=-2:1080 '${BASE}-web.mp4'"; exit 2; }
    ffmpeg -y -i "$IN" -an -c:v libx264 -crf 24 -movflags +faststart -vf "scale=-2:1080" "${BASE}-web.mp4"
    ffmpeg -y -sseof -0.1 -i "${BASE}-web.mp4" -frames:v 1 "${BASE}-poster.png"
    command -v cwebp >/dev/null && cwebp -q 80 "${BASE}-poster.png" -o "${BASE}-poster.webp" && rm "${BASE}-poster.png"
    ls -l "$IN" "${BASE}-web.mp4" ;;
  *) echo "unsupported: $EXT" >&2; exit 1 ;;
esac
