// Loop treatment: seamless-FEEL loop for footage that doesn't loop
// cleanly. The hard cut hides inside an rAF-driven dip-to-black:
// fade out just before the end, reset, fade back in. Native `loop`
// attribute stays OFF. (For footage designed as a perfect loop, skip
// this file and just use the loop attribute.)
// Markup: <video data-loop-crossfade muted playsinline preload="auto"
//                poster="..."><source src="..."></video>
(function () {
  var video = document.querySelector("[data-loop-crossfade]");
  if (!video) return;
  var FADE_MS = 500, FADE_OUT_LEAD = 0.55, rafId = null, fadingOut = false;

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    video.removeAttribute("autoplay");
    video.pause();
    return; // poster stands - a complete hero on its own (skill rule 5/6)
  }

  function fadeTo(target, duration) {
    if (rafId) cancelAnimationFrame(rafId);
    var from = parseFloat(video.style.opacity || "0"), start = null;
    function step(ts) {
      if (start === null) start = ts;
      var p = Math.min((ts - start) / duration, 1);
      video.style.opacity = String(from + (target - from) * p);
      if (p < 1) rafId = requestAnimationFrame(step);
    }
    rafId = requestAnimationFrame(step);
  }

  video.style.opacity = "0";
  video.addEventListener("loadeddata", function () {
    var p = video.play();
    if (p && p.catch) p.catch(function () { /* autoplay blocked: poster stands */ });
    fadeTo(1, FADE_MS);
  });
  video.addEventListener("timeupdate", function () {
    var left = video.duration - video.currentTime;
    if (!fadingOut && left <= FADE_OUT_LEAD && left > 0) {
      fadingOut = true;
      fadeTo(0, FADE_MS);
    }
  });
  video.addEventListener("ended", function () {
    video.style.opacity = "0";
    setTimeout(function () {
      video.currentTime = 0;
      video.play();
      fadingOut = false;
      fadeTo(1, FADE_MS);
    }, 100);
  });
})();
