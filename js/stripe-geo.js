/**
 * Private quote routing for former paid CTAs.
 * Public pricing and public Stripe payment links are intentionally disabled.
 */
(function () {
  'use strict';

  function initPrivateQuotes() {
    var els = document.querySelectorAll('[data-stripe-product]');
    for (var i = 0; i < els.length; i++) {
      els[i].href = '/#contact';
      els[i].setAttribute('rel', 'nofollow');
      els[i].addEventListener('click', function () {
        if (typeof gtag === 'function') {
          gtag('event', 'private_quote_request', {
            product: this.getAttribute('data-stripe-product') || 'unknown'
          });
        }
      });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initPrivateQuotes);
  } else {
    initPrivateQuotes();
  }
})();
