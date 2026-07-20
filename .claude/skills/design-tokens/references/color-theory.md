# Palette Construction
From one brand color: derive primary-dark (same hue, -25 to -35 L in HSL),
accent (analogous for calm directions, complementary for energetic),
neutrals tinted 2-4% toward primary hue (never pure gray #808080 family),
bg near-white or near-black per direction, surface one step from bg.
Contrast check method: compute ratios for (text/bg), (text-muted/bg),
(text on primary buttons), (accent on bg). Body >= 4.5:1, large text and
UI borders >= 3:1. If a client brand color fails as text, use it only for
large elements/fills and derive a darker text-safe variant - log this in
DECISIONS.md so the client understands why.
60-30-10 distribution: neutrals dominate; primary structures; accent is
scarce (CTAs, highlights). Accent overuse is the #1 amateur tell.
