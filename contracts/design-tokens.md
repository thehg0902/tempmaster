# Contract: Design Tokens  (v1.1.0)

All visual values are CSS custom properties defined ONCE in
`site/shared/tokens.css` on `:root`. No component may hardcode a color,
font size, spacing value, radius, shadow, or duration.

## Required token set

Colors:        --color-primary, --color-primary-dark, --color-accent,
               --color-bg, --color-surface, --color-text, --color-text-muted,
               --color-border, --color-success, --color-error
Typography:    --font-heading, --font-body,
               --text-xs, --text-sm, --text-base, --text-lg, --text-xl,
               --text-2xl, --text-3xl, --text-hero  (rem-based modular scale)
               --leading-tight, --leading-normal, --leading-loose
Spacing:       --space-1 .. --space-12 (4px base scale expressed in rem)
Layout:        --container-max (default 1200px), --section-pad-y,
               --radius-sm, --radius-md, --radius-lg, --radius-full
Elevation:     --shadow-sm, --shadow-md, --shadow-lg
Motion:        --duration-fast (150ms), --duration-base (300ms),
               --duration-slow (600ms), --ease-standard, --ease-out-expo

## Rules
1. Producer: the design-tokens skill writes `site/shared/tokens.css`.
2. Consumers: every other skill uses `var(--token)` only.
3. Dark variants (if used) override on `[data-theme="dark"]`, same names.
4. Adding a token = append here first (bump minor), then to tokens.css.
5. Renaming/removing a token = breaking change (bump major). Avoid.
