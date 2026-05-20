/**
 * Stripe geo-detection: show CHF payment links for CH/LI visitors, EUR for all others.
 * Safe to include in HTML — payment links are public buy.stripe.com URLs, no secret exposed.
 * agents-ia.pro
 */
(function () {
  'use strict';

  var EUR_LINKS = {
    bronze:            'https://buy.stripe.com/14AbJ0670fbq1OsdJYco00N',
    silver:            'https://buy.stripe.com/fZu7sKfHAbZe0Ko21gco00O',
    gold:              'https://buy.stripe.com/28E5kCangbZe3WAbBQco00P',
    submit_fasttrack:  'https://buy.stripe.com/dRm4gy1QKaVa8cQgWaco00Q',
    rapport_assurance: 'https://buy.stripe.com/9B6bJ0eDw2oEakY8pEco00R',
    rapport_voice:     'https://buy.stripe.com/00w7sKbrk2oEfFi6hwco00S',
    rapport_rgpd:      'https://buy.stripe.com/3cIfZg2UOd3i2SwdJYco00T',
    rapport_bundle:    'https://buy.stripe.com/5kQ8wO52W1kAeBe8pEco00U'
  };

  // CHF links — generated 2026-05-20 via Stripe API for CH/LI visitors
  var CHF_LINKS = {
    bronze:            'https://buy.stripe.com/bJe5kC8f89R6dxafS6co011',
    silver:            'https://buy.stripe.com/fZufZg3YS5AQbp2fS6co012',
    gold:              'https://buy.stripe.com/6oU14mfHA1kAfFi8pEco013',
    submit_fasttrack:  'https://buy.stripe.com/bJebJ09jc7IYdxa35kco014',
    rapport_assurance: 'https://buy.stripe.com/cNidR80MG6EUdxa9tIco015',
    rapport_voice:     'https://buy.stripe.com/14AdR8anggfuct68pEco016',
    rapport_rgpd:      'https://buy.stripe.com/8x28wOdzs8N2ct60Xcco017',
    rapport_bundle:    'https://buy.stripe.com/8x2fZg52WbZefFi0Xcco018'
  };

  var CHF_COUNTRIES = ['CH', 'LI'];

  function isCHF(links) {
    return links === CHF_LINKS;
  }

  function updatePaymentLinks(links) {
    var chf = isCHF(links);

    // 1. Update all [data-stripe-product] anchor hrefs
    var els = document.querySelectorAll('[data-stripe-product]');
    for (var i = 0; i < els.length; i++) {
      var el = els[i];
      var product = el.getAttribute('data-stripe-product');
      if (links[product]) {
        el.href = links[product];
      }
      // Update currency badge if present
      var badge = el.querySelector('.currency-badge');
      if (badge) {
        badge.textContent = chf ? 'CHF' : 'EUR';
      }
    }

    // 2. Show/hide price elements by currency
    var eurEls = document.querySelectorAll('.price-eur');
    for (var j = 0; j < eurEls.length; j++) {
      eurEls[j].style.display = chf ? 'none' : '';
    }
    var chfEls = document.querySelectorAll('.price-chf');
    for (var k = 0; k < chfEls.length; k++) {
      chfEls[k].style.display = chf ? '' : 'none';
    }

    // 3. Fire GA4 event for geo routing (non-blocking)
    if (typeof gtag === 'function') {
      gtag('event', 'stripe_geo_routed', {
        currency: chf ? 'CHF' : 'EUR',
        country: window._stripeGeoCountry || 'unknown'
      });
    }
  }

  function init() {
    // Default: show EUR links immediately (no layout shift for most visitors)
    updatePaymentLinks(EUR_LINKS);

    // Async geo detection
    fetch('https://ipapi.co/json/')
      .then(function (r) { return r.json(); })
      .then(function (data) {
        var cc = data && data.country_code ? data.country_code.toUpperCase() : '';
        window._stripeGeoCountry = cc;
        var links = (CHF_COUNTRIES.indexOf(cc) !== -1) ? CHF_LINKS : EUR_LINKS;
        updatePaymentLinks(links);
      })
      .catch(function () {
        // Fallback: keep EUR (already applied above)
      });
  }

  // Run after DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
