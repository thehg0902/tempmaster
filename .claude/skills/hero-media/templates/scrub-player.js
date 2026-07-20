// Scroll-scrub treatment: canvas + preloaded webp frames driven by the
// section's scroll progress (the reliable cross-browser pattern; video
// currentTime scrubbing is janky on mobile Safari - see
// references/scroll-scrub.md). Reads the manifest /ingest wrote.
// Markup:
//   <section class="section section--hero" data-scrub-section>
//     <canvas data-scrub="hero-scrub"
//             data-manifest="assets/images/scrub/hero-scrub/manifest.json">
//     </canvas> ...
//   </section>
// (subpage depth: prefix data-manifest with ../)
(function () {
  var canvas = document.querySelector("[data-scrub]");
  if (!canvas || !canvas.getContext) return;
  var section = canvas.closest("[data-scrub-section]") || canvas.parentElement;
  var ctx = canvas.getContext("2d");
  var frames = [], manifest = null, current = -1, rafId = null;

  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  fetch(canvas.getAttribute("data-manifest"))
    .then(function (r) { return r.json(); })
    .then(function (m) {
      manifest = m;
      canvas.width = m.width; canvas.height = m.height;
      var base = canvas.getAttribute("data-manifest").replace(/manifest\.json$/, "");
      function src(i) {
        return base + m.pattern.replace("%04d", String(i + 1).padStart(4, "0"));
      }
      function load(i, cb) {
        if (frames[i]) { if (cb) cb(); return; }
        var img = new Image();
        img.onload = function () { frames[i] = img; if (cb) cb(); };
        img.src = src(i);
      }
      load(0, function () { draw(0); });   // first frame = poster duty
      if (reduced) return;                  // reduced motion: frame 0 only
      // progressive preload: every 4th frame first, then backfill
      var order = [], i;
      for (i = 0; i < m.frames; i += 4) order.push(i);
      for (i = 0; i < m.frames; i++) if (i % 4) order.push(i);
      order.forEach(function (idx) { load(idx); });
      window.addEventListener("scroll", onScroll, { passive: true });
      onScroll();
    })
    .catch(function () { /* no manifest: canvas stays empty, CSS bg/poster stands */ });

  function draw(i) {
    var f = frames[i] || nearestLoaded(i);
    if (!f) return;
    ctx.drawImage(f, 0, 0, canvas.width, canvas.height);
    current = i;
  }
  function nearestLoaded(i) {
    for (var d = 1; d < frames.length; d++) {
      if (frames[i - d]) return frames[i - d];
      if (frames[i + d]) return frames[i + d];
    }
    return frames[0] || null;
  }
  function onScroll() {
    if (rafId) return;
    rafId = requestAnimationFrame(function () {
      rafId = null;
      if (!manifest) return;
      var r = section.getBoundingClientRect();
      var scrollable = r.height - window.innerHeight;
      if (scrollable <= 0) return;
      var progress = Math.min(Math.max(-r.top / scrollable, 0), 1);
      var idx = Math.round(progress * (manifest.frames - 1));
      if (idx !== current) draw(idx);
    });
  }
})();
