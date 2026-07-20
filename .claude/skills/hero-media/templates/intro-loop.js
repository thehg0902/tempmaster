// Intro+loop treatment: intro plays once, then an rAF crossfade hands
// off to the loop video, which loops natively (loop footage should be
// generated/edited to loop cleanly; if it can't, use the
// loop-crossfade.js pattern on the loop element instead).
// Markup (loop stacked under intro, both absolutely positioned):
//   <div data-intro-loop>
//     <video data-il-loop  muted playsinline preload="auto" loop
//            style="opacity:0"><source src="...-loop.mp4"></video>
//     <video data-il-intro muted playsinline preload="auto" autoplay
//            poster="...-intro-poster.webp"><source src="...-intro.mp4"></video>
//   </div>
(function () {
  var wrap = document.querySelector("[data-intro-loop]");
  if (!wrap) return;
  var intro = wrap.querySelector("[data-il-intro]");
  var loop = wrap.querySelector("[data-il-loop]");
  if (!intro || !loop) return;
  var FADE_MS = 400, LEAD = 0.4, rafId = null, handedOff = false;

  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    intro.removeAttribute("autoplay"); intro.pause(); loop.pause();
    return; // poster stands
  }

  function crossfade() {
    if (handedOff) return;
    handedOff = true;
    var p = loop.play();
    if (p && p.catch) p.catch(function () {});
    var start = null;
    function step(ts) {
      if (start === null) start = ts;
      var f = Math.min((ts - start) / FADE_MS, 1);
      loop.style.opacity = String(f);
      intro.style.opacity = String(1 - f);
      if (f < 1) rafId = requestAnimationFrame(step);
      else intro.pause();
    }
    if (rafId) cancelAnimationFrame(rafId);
    rafId = requestAnimationFrame(step);
  }

  intro.addEventListener("timeupdate", function () {
    var left = intro.duration - intro.currentTime;
    if (left <= LEAD && left > 0) crossfade();
  });
  intro.addEventListener("ended", crossfade); // safety if timeupdate missed
})();
