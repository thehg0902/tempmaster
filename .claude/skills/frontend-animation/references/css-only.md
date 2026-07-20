# CSS-Only Animation Pattern
JS (site/shared/main.js when used on 2+ pages, else the page's own
script.js): on init add .anim-ready to <body>; observe
[data-animate] with IntersectionObserver {threshold:.2}; add .is-visible,
unobserve. Stagger via inline --stagger-i set from element index.
CSS: .anim-ready [data-animate]{opacity:0;transform:translateY(20px);
transition:opacity var(--duration-slow) var(--ease-out-expo),
transform var(--duration-slow) var(--ease-out-expo);
transition-delay:calc(var(--stagger-i,0)*75ms)}
.anim-ready [data-animate].is-visible{opacity:1;transform:none}
No .anim-ready (JS off) = fully visible content. Wrap the whole block in
@media (prefers-reduced-motion: no-preference).
