// Home page behavior: launch sequence (loader -> reveal -> header entrance)
// + the pinned hero stage. The idle loop (hero-loop.mp4) plays as a real
// video; once the visitor scrolls into the transition zone it crossfades
// into a scroll-scrubbed frame sequence (canvas + preloaded webp frames,
// per hero-media's scroll-scrub treatment) drawn directly from scroll
// progress — reverse is free (just an earlier frame index), no separate
// forward/reverse state machine needed. Reproduces the binding
// preview/layout-preview.html plus the pinned-stage + scrub refinements
// logged in state/DECISIONS.md.
(function () {
  var loader = document.getElementById('loader');
  var headerEl = document.getElementById('site-header');
  var loopVideo = document.querySelector('[data-hero-loop]');
  var canvas = document.querySelector('[data-hero-scrub]');
  var wrapper = document.getElementById('hero-stage-wrapper');
  var heroLayer = document.getElementById('hero-layer');
  var trustLayer = document.getElementById('trust-layer');
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // ---- launch sequence ----
  (function () {
    if (!loader || !headerEl) return;
    var done = false;
    function reveal() {
      if (done) return;
      done = true;
      loader.classList.add('is-done');
      document.body.classList.add('is-revealed');
      // header slides in once the background is fully revealed (loader fade = 600ms)
      setTimeout(function () { headerEl.classList.add('is-revealed'); }, reduced ? 0 : 1100);
    }
    if (reduced) { reveal(); return; }
    if (loopVideo && loopVideo.readyState >= 3) { reveal(); }
    else if (loopVideo) { loopVideo.addEventListener('canplaythrough', reveal, { once: true }); }
    setTimeout(reveal, 2500); // fallback: never hold visitors hostage
  })();

  if (loopVideo) {
    if (reduced) {
      loopVideo.removeAttribute('autoplay');
      loopVideo.pause(); // poster/frame 0 stands — a complete hero on its own
    } else {
      var p0 = loopVideo.play();
      if (p0 && p0.catch) p0.catch(function () {}); // autoplay blocked: poster stands
      // No native `loop` attribute (footage isn't confirmed seamless — a
      // hard cut is fine, a silently-frozen-on-last-frame hero is not).
      // Restart on 'ended'; harmless if paused mid-scrub since a paused
      // video never fires 'ended'.
      loopVideo.addEventListener('ended', function () {
        loopVideo.currentTime = 0;
        var pr = loopVideo.play();
        if (pr && pr.catch) pr.catch(function () {});
      });
    }
  }

  // ---- scroll-scrub loader: canvas + preloaded webp frames ----
  // Frame 0001 loads first and stands as the poster; progressive preload
  // (every 4th frame, then backfill) means scrubbing degrades to slightly
  // steppy on a slow connection, never blank (references/scroll-scrub.md).
  var scrub = (function () {
    if (!canvas || !canvas.getContext) return null;
    var ctx = canvas.getContext('2d');
    var frames = [], manifest = null, current = -1;

    fetch(canvas.getAttribute('data-manifest'))
      .then(function (r) { return r.json(); })
      .then(function (m) {
        manifest = m;
        canvas.width = m.width;
        canvas.height = m.height;
        var base = canvas.getAttribute('data-manifest').replace(/manifest\.json$/, '');
        function src(i) { return base + m.pattern.replace('%04d', String(i + 1).padStart(4, '0')); }
        function load(i, cb) {
          if (frames[i]) { if (cb) cb(); return; }
          var img = new Image();
          img.onload = function () { frames[i] = img; if (cb) cb(); };
          img.src = src(i);
        }
        load(0, function () { draw(0); });
        if (reduced) return; // reduced motion: frame 0 only, no preload, no scroll-link
        var order = [], i;
        for (i = 0; i < m.frames; i += 4) order.push(i);
        for (i = 0; i < m.frames; i++) if (i % 4) order.push(i);
        order.forEach(function (idx) { load(idx); });
      })
      .catch(function () {}); // no manifest: canvas stays empty, overlay/poster stand

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
    return {
      frameCount: function () { return manifest ? manifest.frames : 0; },
      ready: function () { return !!manifest; },
      drawFrame: function (i) { if (i !== current) draw(i); }
    };
  })();

  // ---- pinned scroll driver: hero out -> loop crossfades into scrub -> trust in ----
  // Scroll-linked (transform/opacity only, rAF-throttled — no layout thrash).
  (function () {
    if (reduced || !wrapper || !heroLayer || !trustLayer) return;

    var HERO_OUT_END = 0.35;   // hero fully faded/out by 35% through the runway
    var SCRUB_START = 0.02;    // loop crossfades to the scrub sequence as soon as
                                // scroll-down is detected — hero-transition's first
                                // frame matches hero-loop's, so the swap is invisible
                                // (operator spec; a tiny epsilon, not 0, avoids
                                // triggering on sub-pixel scroll/resize jitter at rest)
    var SCRUB_END = 0.95;      // scrub finishes exactly as trust finishes scrolling in
    var TRUST_START = 0.40;
    var TRUST_END = 0.95;
    var HERO_TRAVEL = 70;      // px the hero drifts up while fading
    var TRUST_TRAVEL = 60;     // px the trust stats travel up from below

    var ticking = false;
    var scrubActive = false; // whether the crossfade to canvas has happened

    function progress() {
      var rect = wrapper.getBoundingClientRect();
      var vh = window.innerHeight;
      var runway = wrapper.offsetHeight - vh;
      if (runway <= 0) return 1;
      return Math.min(1, Math.max(0, -rect.top / runway));
    }

    function apply() {
      ticking = false;
      var p = progress();

      var heroP = Math.min(1, p / HERO_OUT_END);
      heroLayer.style.transform = 'translateY(' + (-heroP * HERO_TRAVEL) + 'px)';
      heroLayer.style.opacity = String(1 - heroP);

      var trustP = p <= TRUST_START ? 0 : Math.min(1, (p - TRUST_START) / (TRUST_END - TRUST_START));
      trustLayer.style.transform = 'translateY(' + ((1 - trustP) * TRUST_TRAVEL) + 'px)';
      trustLayer.style.opacity = String(trustP);

      if (scrub && scrub.ready() && loopVideo) {
        var shouldBeActive = p >= SCRUB_START;
        if (shouldBeActive !== scrubActive) {
          scrubActive = shouldBeActive;
          if (scrubActive) { loopVideo.style.opacity = 0; canvas.style.opacity = 1; loopVideo.pause(); }
          else {
            canvas.style.opacity = 0; loopVideo.style.opacity = 1;
            loopVideo.currentTime = 0;
            var pp = loopVideo.play();
            if (pp && pp.catch) pp.catch(function () {});
          }
        }
        if (scrubActive) {
          var scrubP = Math.min(1, Math.max(0, (p - SCRUB_START) / (SCRUB_END - SCRUB_START)));
          var idx = Math.round(scrubP * (scrub.frameCount() - 1));
          scrub.drawFrame(idx);
        }
      }

      // header goes solid only once the visitor has scrolled fully through
      // the pinned stage — overrides main.js's generic scrollY>8 toggle
      // (both listeners run on 'scroll'; this one is registered after
      // main.js's, so it wins as the final state for the same tick).
      if (headerEl) headerEl.classList.toggle('is-scrolled', p >= 0.98);
    }

    window.addEventListener('scroll', function () {
      if (!ticking) { ticking = true; requestAnimationFrame(apply); }
    }, { passive: true });
    apply();
  })();
})();
