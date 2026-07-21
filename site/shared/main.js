// main.js — shared behavior: JS flag, header state, mobile nav, reveals.
// Page-specific behavior (hero video machine, loader) lives in the page's script.js.
(function () {
  document.documentElement.classList.add('js');

  // header shadow / solid state on scroll
  var header = document.getElementById('site-header');
  if (header) {
    var onScroll = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 8);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // mobile nav — transform/opacity overlay, never display-swap
  var burger = document.querySelector('.hamburger');
  var mnav = document.getElementById('mobile-nav');
  if (burger && mnav) {
    var closeNav = function () {
      mnav.classList.remove('is-open');
      burger.setAttribute('aria-expanded', 'false');
    };
    burger.addEventListener('click', function () {
      if (mnav.classList.contains('is-open')) { closeNav(); }
      else { mnav.classList.add('is-open'); burger.setAttribute('aria-expanded', 'true'); }
    });
    mnav.querySelectorAll('[data-nav-close]').forEach(function (el) {
      el.addEventListener('click', closeNav);
    });
    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeNav();
    });
  }

  // scroll-entrance reveals
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-visible'); io.unobserve(e.target); }
      });
    }, { threshold: 0.15 });
    document.querySelectorAll('.reveal').forEach(function (el) { io.observe(el); });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) { el.classList.add('is-visible'); });
  }
})();
