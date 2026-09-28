// app.js — single entry point, calls each module's init()
(function () {
  'use strict';

  function setYear() {
    var el = document.getElementById('year');
    if (el) el.textContent = String(new Date().getFullYear());
  }

  function init() {
    setYear();

    var KY = window.KYVOREX;
    if (!KY) return;

    if (KY.home && KY.home.init) KY.home.init();
    if (KY.ui && KY.ui.init) KY.ui.init();
    if (KY.sounds && KY.sounds.init) KY.sounds.init();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();