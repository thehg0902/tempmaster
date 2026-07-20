// Play hero video once, freeze on final frame. Defensive per rules/js.md.
(function () {
  const video = document.querySelector("[data-hero-video]");
  if (!video) return;
  const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (reduced) { video.removeAttribute("autoplay"); return; } // poster stands
  video.addEventListener("ended", () => {
    video.pause();
    // hold last frame; some browsers flash-reset without this nudge:
    if (video.duration) video.currentTime = Math.max(0, video.duration - 0.05);
  }, { once: true });
  const p = video.play();
  if (p && p.catch) p.catch(() => { /* autoplay blocked: poster stands */ });
})();
