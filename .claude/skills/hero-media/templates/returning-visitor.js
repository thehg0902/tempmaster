// Returning-visitor detection: play hero motion once per visitor.
// KEY must be prefixed with the client site slug (rules/js.md).
(function () {
  const KEY = "SITE_SLUG:heroPlayed"; // <- replace SITE_SLUG
  const video = document.querySelector("[data-hero-video]");
  if (!video) return;
  let seen = false;
  try { seen = localStorage.getItem(KEY) === "1"; } catch (e) { /* private mode */ }
  if (seen || matchMedia("(prefers-reduced-motion: reduce)").matches) {
    // show final frame immediately, no playback
    video.addEventListener("loadedmetadata", () => {
      video.currentTime = Math.max(0, (video.duration || 0) - 0.05);
    }, { once: true });
    return;
  }
  video.addEventListener("ended", () => {
    try { localStorage.setItem(KEY, "1"); } catch (e) {}
  }, { once: true });
  const p = video.play();
  if (p && p.catch) p.catch(() => {});
})();
