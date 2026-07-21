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
  var stage = document.getElementById('hero-stage');
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
      // header slides in once the (slow, grand) loader fade has finished — the
      // hero text float-up plays during the gap so the reveal feels staged.
      setTimeout(function () { headerEl.classList.add('is-revealed'); }, reduced ? 0 : 1500);
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
  // The manifest is read INLINE from the canvas's data-* attributes, NOT via
  // fetch(): fetch() of a local file is blocked under the file:// protocol, so a
  // fetch-based load would silently fail on a double-clicked site/index.html and
  // leave "just the video" — breaking the file-structure contract's "openable
  // standalone, no server" guarantee. The frame images themselves load fine over
  // file:// (plain <img> src). manifest.json still lives on disk as the ingest
  // record; these attributes mirror it. Frame 0001 loads first and stands as the
  // poster; progressive preload (every 4th, then backfill) keeps scrubbing from
  // ever going blank on a slow connection (references/scroll-scrub.md).
  var scrub = (function () {
    if (!canvas || !canvas.getContext) return null;
    var ctx = canvas.getContext('2d');
    var frames = [], current = -1;

    var frameCount = parseInt(canvas.getAttribute('data-frames'), 10) || 0;
    var width = parseInt(canvas.getAttribute('data-width'), 10) || 0;
    var height = parseInt(canvas.getAttribute('data-height'), 10) || 0;
    var pattern = canvas.getAttribute('data-pattern') || 'frame-%04d.webp';
    var base = canvas.getAttribute('data-frame-base') || '';
    if (!frameCount || !width || !height) return null; // no manifest: poster/video stands

    canvas.width = width;
    canvas.height = height;

    function src(i) { return base + pattern.replace('%04d', String(i + 1).padStart(4, '0')); }
    function load(i, cb) {
      if (frames[i]) { if (cb) cb(); return; }
      var img = new Image();
      img.onload = function () { frames[i] = img; if (cb) cb(); };
      img.src = src(i);
    }
    load(0, function () { draw(0); }); // frame 0 = poster duty
    if (!reduced) {                    // reduced motion: frame 0 only, no scroll-link
      var order = [], i;
      for (i = 0; i < frameCount; i += 4) order.push(i);
      for (i = 0; i < frameCount; i++) if (i % 4) order.push(i);
      order.forEach(function (idx) { load(idx); });
    }

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
      frameCount: function () { return frameCount; },
      ready: function () { return frameCount > 0; },
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
    // Mobile-only focal tracking: the AC unit pans right->left across the scrub,
    // so object-position-X is interpolated to keep it centered on a portrait
    // crop. Published as --hero-focus-x; CSS applies it only under the mobile
    // media query (desktop keeps its AC-right / text-left composition). Tune by
    // eye — higher FOCUS_START = AC further right at the top of the scroll.
    var FOCUS_START = 78, FOCUS_END = 31; // object-position % at scrubP 0 and 1
    // Overlay scrim multiplier: lighter over the dark hero scene, ramping to
    // full (1) over the bright indoor trust scene so the review text stays
    // legible. base gradient is .80/.68/.80; SCRIM_HERO*base is the hero look.
    var SCRIM_HERO = 0.70;

    var scrubActive = false; // whether the crossfade to canvas has happened
    var lastY = -1;

    if (stage) {
      stage.style.setProperty('--hero-focus-x', FOCUS_START + '%'); // pre-scroll paint
      stage.style.setProperty('--scrim-opacity', String(SCRIM_HERO));
    }

    function progress() {
      var rect = wrapper.getBoundingClientRect();
      var vh = window.innerHeight;
      var runway = wrapper.offsetHeight - vh;
      if (runway <= 0) return 1;
      return Math.min(1, Math.max(0, -rect.top / runway));
    }

    function apply() {
      var p = progress();

      var heroP = Math.min(1, p / HERO_OUT_END);
      heroLayer.style.transform = 'translateY(' + (-heroP * HERO_TRAVEL) + 'px)';
      heroLayer.style.opacity = String(1 - heroP);

      var trustP = p <= TRUST_START ? 0 : Math.min(1, (p - TRUST_START) / (TRUST_END - TRUST_START));
      trustLayer.style.transform = 'translateY(' + ((1 - trustP) * TRUST_TRAVEL) + 'px)';
      trustLayer.style.opacity = String(trustP);

      // scrubP is valid whether or not the scrub is active yet: at rest it clamps
      // to 0 (loop showing -> FOCUS_START, matching the loop/first frame). Drives
      // both the mobile focal point (always) and the drawn frame (when active).
      var scrubP = Math.min(1, Math.max(0, (p - SCRUB_START) / (SCRUB_END - SCRUB_START)));
      if (stage) {
        stage.style.setProperty('--hero-focus-x',
          (FOCUS_START + (FOCUS_END - FOCUS_START) * scrubP).toFixed(1) + '%');
        // scrim darkens with the scrub: SCRIM_HERO (light) -> 1 (full) as the
        // bright trust scene comes in, keeping the review text legible.
        stage.style.setProperty('--scrim-opacity',
          (SCRIM_HERO + (1 - SCRIM_HERO) * scrubP).toFixed(3));
      }

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
          scrub.drawFrame(Math.round(scrubP * (scrub.frameCount() - 1)));
        }
      }

      // header goes solid only once the visitor has scrolled fully through
      // the pinned stage — overrides main.js's generic scrollY>8 toggle
      // (both listeners run on 'scroll'; this one is registered after
      // main.js's, so it wins as the final state for the same tick).
      if (headerEl) headerEl.classList.toggle('is-scrolled', p >= 0.98);
    }

    // Drive apply() straight off the scroll event, guarded by a scrollY-change
    // check. The work is cheap (one rect read, then transform/opacity writes +
    // a guarded canvas draw) and the browser already rate-limits scroll events
    // to ~once per frame. Deliberately NOT gated behind requestAnimationFrame:
    // rAF is throttled/suspended whenever the page renders hidden (embedded
    // preview panes, background tabs), which would silently freeze the scrub on
    // the loop's first frame and leave "just a video playing". Reading the rect
    // before any write keeps this thrash-free within each call.
    window.addEventListener('scroll', function () {
      var y = window.scrollY || window.pageYOffset || 0;
      if (y === lastY) return;
      lastY = y;
      apply();
    }, { passive: true });
    apply();
  })();
})();
