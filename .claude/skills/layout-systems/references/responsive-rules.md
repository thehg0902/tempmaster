# Responsive Rules
Breakpoints: base (mobile), 640px, 1024px only - resist adding more.
Fluid type via clamp() (tokens); fluid space allowed on section padding.
Nav: <=5 links inline-condensed on mobile if they fit; else hamburger
(no-JS fallback: nav visible, toggle hidden). Tables become stacked cards
under 640px. Images: width/height attrs always (CLS), object-fit: cover
for media boxes. Touch targets 44px min. Test tap-to-call visibility at
360px before anything else.
