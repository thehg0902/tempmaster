---
name: mobile-polish
description: Make the phone experience the showpiece - mobile-first
  layout decisions, thumb ergonomics, touch feedback, and slick
  transitions so the site feels BETTER on phone than desktop
  (default-on unless client.md says otherwise). Use in Phase 5 after
  layout/components and before /qa, and for retainer polish passes.
  Not for scroll/entrance choreography (frontend-animation) or WCAG
  depth (accessibility).
metadata: {version: 1.0.0, category: frontend, tier: B}
---
# Mobile Polish

## Purpose
Most local-business visitors arrive on a phone. The phone version is
the primary product, not the shrunk-down afterthought - it should feel
slicker than desktop.

## Inputs
Built pages in site/, tokens (durations/easings), Stack animation flag,
niche playbook conversion priorities.

## Outputs
Mobile-specific CSS/JS refinements in shared/ or per-page files;
audited via the /visual-qa 360 pass.

## Rules
1. Mobile is the primary canvas: layout decisions resolve in favor of
   360-430px first; desktop is the adaptation. When a section can only
   be great on one, pick the phone.
2. Thumb ergonomics: the page's primary action reachable in the thumb
   zone - call-first niches get a sticky bottom action bar (call +
   directions); tap targets >= 44px with >= 8px gaps; inputs
   font-size >= 16px (prevents iOS focus zoom); no hover-dependent
   information anywhere.
3. Touch feedback: every tappable element gets an :active state
   (transform scale ~.97 or brightness shift) at var(--duration-fast);
   -webkit-tap-highlight-color transparent, replaced by the custom
   feedback. Feedback is instant - never delayed behind a transition.
4. Slick transitions, DEFAULT ON (skip only when the operator/client
   says so, or Stack animation: none): mobile nav opens as a smooth
   transform+opacity overlay or bottom sheet (never a display-swap
   jump); sticky header condenses on scroll; entrance motion on mobile
   uses SHORTER distances and durations than desktop (12-16px, faster
   ease) - small screens read subtlety as polish. All motion stays
   behind prefers-reduced-motion.
5. Viewport correctness: 100svh (not 100vh) for full-height sections;
   env(safe-area-inset-*) padding on fixed bars; no horizontal
   overflow at 360 ever.
6. Weight on the small screen: phones load the smaller srcset variants;
   hero video plays on mobile only when the hosting profile budget
   affords it - otherwise the poster IS the mobile hero.
7. Verify where it counts: the /visual-qa 360 pass audits this
   checklist FIRST, before tablet and desktop.

## Anti-patterns
- Desktop nav miniaturized instead of redesigned; hover-only
  affordances; 100vh sections that jump when browser chrome hides;
  sticky bars covering content with no safe-area padding; motion so
  long the page feels laggy on mid-range phones.

## Changelog
- 1.0.0 initial (v1.5.0 - phone experience as the showpiece)
