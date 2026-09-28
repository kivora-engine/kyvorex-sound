// downloads.js — static file downloads for the public library.
//
// WAV and MP3 files in the catalog are real static files served from
// audio/wav/ and audio/mp3/. The card UI renders them as native <a>
// anchors with a `download` attribute, so the browser handles the
// download itself. No Blob, no HEAD check, no URL.createObjectURL.
//
// This module is intentionally minimal. It exists so the module
// surface stays stable for future needs (analytics, counters, etc.)
// without breaking the rest of the architecture.
(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};

  function handle() {
    // Nothing to do — the anchor's native behavior performs the
    // download. We intentionally do NOT call preventDefault().
  }

  KY.downloads = {
    init: function () {},
    handle: handle
  };
})();