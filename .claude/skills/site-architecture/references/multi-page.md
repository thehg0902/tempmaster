# Multi-Page Site Pattern
Shared header/footer: identical markup per page (no JS includes -
static hosting, no build step). Keep a canonical copy in index.html;
when editing header/footer, propagate to all pages in the same commit
(qa-review script checks for drift).
URLs: /about.html, /services.html or /services/<kebab-service>.html,
/contact.html. Service pages: hero (specific), problem/solution copy,
proof, faq, cta. Breadcrumbs only when 2+ levels deep.
