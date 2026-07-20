// Reverse-then-freeze: play a clip backwards via rAF currentTime stepping
// (negative playbackRate is unreliable cross-browser), freeze at frame 0.
(function () {
  const video = document.querySelector("[data-hero-video]");
  if (!video) return;
  if (matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  function reversePlay(fps = 30) {
    video.pause();
    const step = 1 / fps;
    let t = video.duration || 0;
    function tick() {
      t -= step;
      if (t <= 0) { video.currentTime = 0; return; } // frozen at start
      video.currentTime = t;
      requestAnimationFrame(tick);
    }
    if (t > 0) requestAnimationFrame(tick);
  }
  video.addEventListener("loadedmetadata", () => {
    video.currentTime = video.duration; // start at end
    reversePlay();
  }, { once: true });
})();
