// donate.js — Handle the "Donate" button and modal info
(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};

  function init() {
    // 1. Ajout du bouton dans le footer
    var footerNav = document.querySelector('.footer-nav');
    if (footerNav) {
      var btn = document.createElement('button');
      btn.className = 'btn btn-ghost';
      btn.id = 'open-donate-btn';
      // Styles inline minimaux pour s'intégrer au footer
      btn.style.padding = '4px 10px';
      btn.style.fontSize = '0.8rem';
      btn.style.minHeight = 'auto';
      btn.style.marginRight = '10px';
      btn.textContent = 'Donate'; // <-- En anglais
      btn.addEventListener('click', openModal);
      
      // On l'insère au début de la navigation du footer
      footerNav.insertBefore(btn, footerNav.firstChild);
    }

    // 2. Création de la fenêtre modale (cachée par défaut)
    var modalHTML = 
      '<div id="donate-modal" class="modal-overlay hidden">' +
        '<div class="modal-content">' +
          '<h2>Thank you for your support!</h2>' +
          '<p>We appreciate your willingness to support KYVOREX SOUNDS.</p>' +
          '<p>The donation feature is not yet available. In the meantime, feel free to enjoy our sound library and developer resources.</p>' +
          '<p>Thank you for being part of the KYVOREX SOUNDS adventure!</p>' +
          '<div class="modal-actions">' +
            '<button id="close-donate-btn" class="btn btn-primary">Continue exploring</button>' +
          '</div>' +
        '</div>' +
      '</div>';
      
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // 3. Événements pour fermer la modale
    document.getElementById('close-donate-btn').addEventListener('click', closeModal);
    
    // Fermer en cliquant en dehors de la boîte
    document.getElementById('donate-modal').addEventListener('click', function(e) {
      if (e.target === this) closeModal();
    });
  }

  function openModal() {
    document.getElementById('donate-modal').classList.remove('hidden');
  }

  function closeModal() {
    document.getElementById('donate-modal').classList.add('hidden');
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();