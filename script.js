// Home page behavior: launch sequence (loader -> reveal -> header entrance)
// + the pinned hero stage (video locked in place; hero scrolls up and out,
// the transition video plays, then trust stats scroll up from below) +
// the hero video state machine (loop -> forward transition freeze ->
// reverse -> loop). Reproduces the binding preview/layout-preview.html
// plus the pinned-stage refinement logged in state/DECISIONS.md.
(function () {
  var loader = document.getElementById('loader');
  var headerEl = document.getElementById('site-header');
  var loopVideo = document.querySelector('[data-hero-loop]');
  var transVideo = document.querySelector('[data-hero-transition]');
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
      // critical path is done — fetch the transition video in the background
      // (it ships with preload="metadata" so it never competes with the loop/LCP)
      if (transVideo) { transVideo.preload = 'auto'; transVideo.load(); }
    }
    if (reduced) { reveal(); return; }
    if (loopVideo && loopVideo.readyState >= 3) { reveal(); }
    else if (loopVideo) { loopVideo.addEventListener('canplaythrough', reveal, { once: true }); }
    setTimeout(reveal, 2500); // fallback: never hold visitors hostage
  })();

  // ---- hero video state machine (loop / forward-freeze / reverse-freeze) ----
  var TRANS_SPEED = 2; // transition video plays at 2x (operator request)

  var machine = (function () {
    if (!loopVideo || !transVideo) return null;
    var state = 'loop'; // loop | transitioning-fwd | transitioned | transitioning-rev

    function crossfade(hide, show) { hide.style.opacity = 0; show.style.opacity = 1; }

    function startLoop() {
      loopVideo.style.opacity = 1;
      loopVideo.currentTime = 0;
      var p = loopVideo.play();
      if (p && p.catch) p.catch(function () { /* autoplay blocked: poster stands */ });
    }
    loopVideo.addEventListener('ended', function () {
      if (state !== 'loop') return;
      startLoop();
    });

    // rAF frame-stepper: drives the transition in either direction without
    // needing play() permission (seeks are always allowed). dir: +1 | -1.
    // Uses REAL elapsed time between frames (not a fixed-fps assumption) so
    // playback speed is accurate and consistent across displays/refresh
    // rates — this is genuine reverse PLAYBACK of the clip, frame by frame,
    // never a hard cut back to the loop.
    function rafStep(dir, fromTime) {
      var expect = dir > 0 ? 'transitioning-fwd' : 'transitioning-rev';
      var t = (typeof fromTime === 'number') ? fromTime : (dir > 0 ? 0 : (transVideo.duration || 0));
      var last = null;
      function tick(now) {
        if (state !== expect) return; // superseded by a new trigger
        if (last === null) { last = now; requestAnimationFrame(tick); return; }
        var dt = (now - last) / 1000; // seconds of real time since last frame
        last = now;
        t += dir * dt * TRANS_SPEED;
        if (dir > 0 && t >= (transVideo.duration || 0)) { finishForward(); return; }
        if (dir < 0 && t <= 0) { finishReverse(); return; }
        transVideo.currentTime = t;
        requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
    }

    function finishForward() {
      transVideo.pause();
      transVideo.currentTime = Math.max(0, (transVideo.duration || 0.05) - 0.05);
      state = 'transitioned';
    }

    function finishReverse() {
      transVideo.currentTime = 0;
      crossfade(transVideo, loopVideo);
      startLoop();
      state = 'loop';
    }

    function playForward(fromTime) {
      state = 'transitioning-fwd';
      loopVideo.pause();
      crossfade(loopVideo, transVideo);
      transVideo.currentTime = fromTime || 0;
      transVideo.playbackRate = TRANS_SPEED;
      var p = transVideo.play();
      // play() rejected (no activation / power saving): step frames instead
      if (p && p.catch) p.catch(function () { rafStep(1, fromTime || 0); });
    }
    transVideo.addEventListener('ended', function () {
      if (state !== 'transitioning-fwd') return;
      finishForward();
    });

    // Reverse has no native browser primitive (negative playbackRate is
    // unreliable cross-browser per hero-media/reverse-freeze.js) — always
    // frame-steps backward through the actual footage via rafStep.
    function playReverse(fromTime) {
      state = 'transitioning-rev';
      transVideo.pause();
      rafStep(-1, fromTime);
    }

    if (reduced) {
      loopVideo.removeAttribute('autoplay');
      loopVideo.pause();
      return null; // poster/frame 0 stands — a complete hero on its own, no pin/scroll-link
    }

    startLoop();
    return {
      getState: function () { return state; },
      playForward: playForward,
      playReverse: playReverse,
      currentTransTime: function () { return transVideo.currentTime; }
    };
  })();

  // ---- pinned scroll driver: hero out -> video plays -> trust in ----
  // Scroll-linked (transform/opacity only, rAF-throttled — no layout thrash).
  // The video itself is NOT scrubbed frame-by-frame; it plays on its own
  // real-time timeline via the state machine, triggered by a progress
  // threshold, matching hero-media's play-once-freeze / reverse-freeze
  // treatments rather than the scroll-scrub treatment.
  (function () {
    if (reduced || !machine || !wrapper || !heroLayer || !trustLayer) return;

    var HERO_OUT_END = 0.35;      // hero fully faded/out by 35% through the runway
    var FORWARD_TRIGGER = 0.38;   // crossing this (going down) plays the transition
    var REVERSE_TRIGGER = 0.34;   // crossing this (going up) reverses it — a few
                                   // points below FORWARD_TRIGGER as a dead-zone so
                                   // the boundary doesn't jitter between states.
                                   // Both sit right after hero-out: reverse gets the
                                   // full 0.34-1.0 span of the scroll-up gesture to
                                   // actually play, instead of being compressed into
                                   // a sliver near the top (the bug the operator caught
                                   // via real mouse-wheel scrolling — see DECISIONS.md).
    var TRUST_START = 0.40;
    var TRUST_END = 0.95;
    var HERO_TRAVEL = 70;      // px the hero drifts up while fading
    var TRUST_TRAVEL = 60;     // px the trust stats travel up from below

    var ticking = false;

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

      var state = machine.getState();
      if (p >= FORWARD_TRIGGER) {
        if (state === 'loop') machine.playForward(0);
        else if (state === 'transitioning-rev') machine.playForward(machine.currentTransTime());
      } else if (p < REVERSE_TRIGGER) {
        if (state === 'transitioned') machine.playReverse();
        else if (state === 'transitioning-fwd') machine.playReverse(machine.currentTransTime());
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
