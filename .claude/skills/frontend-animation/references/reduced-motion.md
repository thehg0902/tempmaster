# Reduced Motion
Respect prefers-reduced-motion at three layers:
1. CSS: all keyframes/transitions inside no-preference media query.
2. JS: const reduced = matchMedia("(prefers-reduced-motion: reduce)").matches;
   skip observers/GSAP init entirely when true.
3. Media: hero video does not autoplay (hero-media skill handles).
Reduced != frozen UX: keep instant state changes (show content immediately),
keep focus styles and hover color shifts (non-movement feedback).
