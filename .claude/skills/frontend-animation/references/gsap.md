# GSAP Pattern
Load gsap + ScrollTrigger from cdnjs (allowed external per client
approval - confirm licensing tier: standard GSAP files are free; Club
plugins are not) with defer, AFTER page content. Init inside
DOMContentLoaded; guard: if(!window.gsap) return; (site must work if CDN
fails). Use gsap.matchMedia() for reduced-motion + breakpoint variants.
Defaults mirror the CSS pattern (y:24, autoAlpha, stagger .08,
ease "expo.out", once:true via ScrollTrigger toggleActions). Pin/scrub
only for the single signature moment, desktop-only via matchMedia.
Kill triggers on bfcache restore (pageshow) to avoid ghost states.
