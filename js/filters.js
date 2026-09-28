// filters.js — search, category filtering, URL param parsing
(function () {
  'use strict';

  var KY = window.KYVOREX = window.KYVOREX || {};

  function getCategories(list) {
    var seen = {};
    list.forEach(function (s) {
      if (s && s.category) seen[s.category] = true;
    });
    return Object.keys(seen).sort();
  }

  function norm(v) { return (v == null ? '' : String(v)).toLowerCase(); }

  function matchesCategory(sound, category) {
    if (!category || category === 'all') return true;
    return sound.category === category;
  }

  function matchesQuery(sound, query) {
    var q = norm(query).trim();
    if (!q) return true;
    var hay = [
      sound.name, sound.category, sound.description, sound.id
    ].map(norm).join(' ');
    return hay.indexOf(q) !== -1;
  }

  function apply(list, opts) {
    opts = opts || {};
    var category = opts.category || 'all';
    var query = opts.query || '';
    return list.filter(function (s) {
      return matchesCategory(s, category) && matchesQuery(s, query);
    });
  }

  function readCategoryFromUrl() {
    try {
      if (!window.location || !window.location.search) return null;
      var params = new URLSearchParams(window.location.search);
      var raw = params.get('category');
      if (!raw) return null;
      var decoded = decodeURIComponent(raw).trim();
      return decoded || null;
    } catch (e) {
      return null;
    }
  }

  KY.filters = {
    init: function () { /* no-op — controlled by sounds.js */ },
    getCategories: getCategories,
    apply: apply,
    readCategoryFromUrl: readCategoryFromUrl
  };
})();