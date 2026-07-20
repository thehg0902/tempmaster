# Loading Strategy Order (per page)
1. Inline nothing except the theme-critical scrim/bg color if needed.
2. <head>: meta, title, preload hero poster + heading font, stylesheets
   (shared/tokens.css, shared/base.css, the page's own style.css - in
   that order, per contracts/file-structure.md).
3. defer shared/main.js and the page's own script.js; CDN libs last, defer.
4. Below-fold images lazy; iframes (Calendly, maps) lazy via facade
   pattern - static placeholder + click/near-viewport load (their skills
   implement it).
5. Analytics loaded after window load or on first interaction.
Weight audit: SCRIPTED - qa-review's check.py sums each page's
referenced asset bytes against the hosting-profile caps and names the
heaviest offenders. Record its output in BUILD_STATE.md notes.
