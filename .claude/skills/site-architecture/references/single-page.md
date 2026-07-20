# Single-Page Site Pattern
Default section order: hero, services, about, testimonials (if any),
gallery (if photos), faq (if provided), cta, contact+map, footer.
Nav = anchor links to section ids; active state via IntersectionObserver;
smooth scroll with prefers-reduced-motion fallback (instant jump).
Every anchor id is a stable contract (component-api rule 6).
Mobile nav: hamburger only above 5 items, else inline condensed.
