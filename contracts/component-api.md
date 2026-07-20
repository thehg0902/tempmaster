# Contract: Component API  (v1.1.0)

Every page is composed of sections. Every section follows this shape:

<section class="section section--{name}" id="{anchor}">
  <div class="container"> ... </div>
</section>

Rules:
1. Class naming: BEM-lite. Block `.card`, element `.card__title`,
   modifier `.card--featured`. No utility soup, no inline styles.
2. Standard section names: hero, services, about, testimonials, gallery,
   faq, cta, contact, footer. Custom sections allowed with the same shape.
3. Every section is self-contained: removing its HTML block and its CSS
   block must not break other sections.
4. Interactive components expose behavior via data attributes
   (e.g. data-accordion, data-carousel), initialized from
   site/shared/main.js (components used on 2+ pages) or the page's own
   script.js (page-specific behavior).
5. All sections must render acceptably with JS disabled (progressive
   enhancement); animation is additive, never load-bearing.
6. Anchors (id=) are stable and used by nav links; changing an anchor
   requires updating nav in the same commit.
