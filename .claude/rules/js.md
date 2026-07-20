---
paths: ["**/*.js"]
---
# JS rules (load only when editing JS)
- Vanilla ES6+ by default; a framework ONLY when client.md requests one
  (Stack framework flag / Special requests) — then follow the
  file-structure contract's Framework exception (pinned CDN + SRI, or
  app/ source building into site/).
- Every script defensive: query elements, bail silently if absent
  (if (!el) return;) so pages without the component don't error.
- Event listeners passive where possible; IntersectionObserver over scroll handlers.
- No global namespace pollution: IIFE or module pattern per file.
- localStorage keys prefixed with site slug (e.g. "acme:heroPlayed").
