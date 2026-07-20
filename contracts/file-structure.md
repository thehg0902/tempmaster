# Contract: File Structure  (v2.1.0)

The website is a STANDALONE deliverable: everything the browser needs
lives under `site/`. Client delivery = zip the CONTENTS of site/ (see
/package). The OS (CLAUDE.md, .claude/, contracts/, state/, scripts/,
client/, docs/) stays at repo root and contains ZERO files the website
needs.

Canonical tree — one folder per page; HOME lives at site/ root:

site/
  index.html        style.css        script.js      <- home page only
  shared/
    tokens.css      (design tokens ONLY - see design-tokens contract)
    base.css        (reset, element defaults, utilities)
    main.js         (init, nav, shared interactions)
  assets/
    images/         (optimized web images: .webp preferred; PNG allowed
                     for alpha assets like logos/icons)
    video/          (hero/section video: .mp4 h.264; poster .webp)
    fonts/          (self-hosted .woff2 only)
  about/
    index.html      style.css        script.js      <- about page only
  <each additional page>/
    index.html      style.css        script.js

Shared-vs-per-page rule: per-page style.css/script.js contain ONLY that
page's specific styles/behavior. Anything used by 2+ pages goes to
shared/. The tokens single-source contract is preserved: a brand color
change is ONE edit in shared/tokens.css, never N edits.

Stylesheet link order (every page, exactly):
  1. tokens.css   2. base.css   3. the page's own style.css

Relative-path table:
| from            | shared css/js        | assets               | nav links                     |
|-----------------|----------------------|----------------------|-------------------------------|
| site/ (home)    | shared/tokens.css    | assets/images/x.webp | about/  menu/                 |
| site/<page>/    | ../shared/tokens.css | ../assets/images/x.webp | ../ (home), ../menu/ (sibling) |

Rules:
1. Kebab-case file and folder names. No spaces, no uppercase.
2. No build step, no framework, no bundler: plain HTML/CSS/JS. site/
   must be openable standalone - double-clicking site/index.html works
   with no server. Deploy target = the CONTENTS of the site/ folder.
3. Page URLs are clean folder URLs (`/about/`), served by index.html.
4. Every image referenced from HTML lives in site/assets/images
   (no hotlinks). All media is central in site/assets/ - never
   duplicated per page.
5. Every generated media asset must have a row in state/MEDIA_LOG.md
   (see media-log contract) before it enters site/assets/.
6. Third-party embeds (Calendly, maps, Formspree endpoints) are the only
   allowed external references besides analytics.
7. Page folders are created per client build (from the Phase 1 page map);
   the template ships only site/ root files, shared/, and assets/.

## Framework exception (v1.4.0 — vanilla preferred, requests honored)

Default is vanilla HTML/CSS/JS (rules above). When client.md requests a
framework (Stack `framework:` flag or Special requests), ACCEPT it —
never reject (interpretation principle); log the approach in
DECISIONS.md (claude-proposed). Invariants that survive any framework:
- The deliverable is STILL the standalone site/ folder; QA (/qa,
  /visual-qa), /package, and deploy-split operate on site/ unchanged.
- CDN-based frameworks (react-cdn, tailwind-cdn, ...): scripts load in
  site/ pages with version-PINNED URLs + SRI integrity hashes
  (security-basics rule 3). No build step needed.
- Build-step frameworks (Vite/React/Svelte, ...): source lives in
  `app/` at repo root (gitignore node_modules); the BUILD OUTPUT is
  written into site/ — site/ remains openable/deployable standalone.
- Design tokens stay the single source of truth: framework theme
  configs (e.g. tailwind.config colors) MAP the values from
  shared/tokens.css, never fork them. A brand color change is still
  one edit.
