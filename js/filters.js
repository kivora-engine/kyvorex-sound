// filters.js — search, category filtering, sorting, URL param parsing
(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};

  /* ---------- normalization ---------- */

  function removeAccents(s) {
    if (s.normalize) {
      return s.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
    }
    return s;
  }

  // Lowercase, no accents, hyphens/underscores -> space, collapsed spaces.
  function norm(v) {
    if (v == null) return '';
    var s = String(v);
    s = removeAccents(s);
    s = s.toLowerCase();
    s = s.replace(/[-_\u2010-\u2015]+/g, ' ');
    s = s.replace(/\s+/g, ' ').trim();
    return s;
  }

  function tokenize(q) {
    return norm(q).split(' ').filter(function (t) { return t.length > 0; });
  }

  /* ---------- categories ---------- */

  function getCategories(list) {
    var seen = {};
    list.forEach(function (s) { if (s && s.category) seen[s.category] = true; });
    return Object.keys(seen).sort();
  }

  function getCategoryCounts(list) {
    var counts = { all: list.length };
    list.forEach(function (s) {
      if (s && s.category) {
        counts[s.category] = (counts[s.category] || 0) + 1;
      }
    });
    return counts;
  }

  /* ---------- prepared haystack (cached per sound) ---------- */

  function prepare(sound) {
    if (!sound) return sound;
    if (sound.__hay) return sound;
    var tags = Array.isArray(sound.tags) ? sound.tags.join(' ') : '';
    sound.__hay = {
      id: norm(sound.id),
      name: norm(sound.name),
      category: norm(sound.category),
      description: norm(sound.description),
      tags: norm(tags)
    };
    return sound;
  }

  /* ---------- relevance scoring ---------- */

  function scoreOne(sound, tokens) {
    if (!tokens.length) return 0;
    var h = sound.__hay;
    var total = 0;

    for (var i = 0; i < tokens.length; i++) {
      var t = tokens[i];
      var s = 0;

      if (h.id === t) s = 100;
      else if (h.id.indexOf(t) === 0) s = 90;
      else if (h.id.indexOf(t) !== -1) s = 70;

      if (s < 85) {
        if (h.name === t) s = Math.max(s, 85);
        else if (h.name.indexOf(t) === 0) s = Math.max(s, 75);
        else if (h.name.indexOf(t) !== -1) s = Math.max(s, 65);
      }

      if (h.tags.indexOf(t) !== -1) s = Math.max(s, 55);
      if (h.category.indexOf(t) !== -1) s = Math.max(s, 40);
      if (h.description.indexOf(t) !== -1) s = Math.max(s, 25);

      if (s === 0) return 0;
      total += s;
    }
    return total;
  }

  function matchesCategory(sound, category) {
    if (!category || category === 'all') return true;
    return sound.category === category;
  }

  /* ---------- sorting helpers ---------- */

  function dateKey(sound) {
    var d = sound && sound.date ? Date.parse(sound.date) : 0;
    return isNaN(d) ? 0 : d;
  }
  function nameKey(sound) {
    return (sound && sound.name) ? sound.name : '';
  }

  function sortItems(items, sort, hasQuery) {
    var copy = items.slice();
    switch (sort) {
      case 'newest':
        copy.sort(function (a, b) {
          return dateKey(b.sound) - dateKey(a.sound) || a.index - b.index;
        });
        break;
      case 'oldest':
        copy.sort(function (a, b) {
          return dateKey(a.sound) - dateKey(b.sound) || a.index - b.index;
        });
        break;
      case 'name-asc':
        copy.sort(function (a, b) {
          return nameKey(a.sound).localeCompare(nameKey(b.sound)) || a.index - b.index;
        });
        break;
      case 'name-desc':
        copy.sort(function (a, b) {
          return nameKey(b.sound).localeCompare(nameKey(a.sound)) || a.index - b.index;
        });
        break;
      case 'relevance':
      default:
        if (hasQuery) {
          copy.sort(function (a, b) {
            return b.score - a.score || a.index - b.index;
          });
        }
        break;
    }
    return copy;
  }

  /* ---------- main entry ---------- */

  function apply(list, opts) {
    opts = opts || {};
    var category = opts.category || 'all';
    var query = opts.query || '';
    var sort = opts.sort || 'relevance';
    var tokens = tokenize(query);

    var matched = [];
    for (var i = 0; i < list.length; i++) {
      var s = list[i];
      if (!matchesCategory(s, category)) continue;
      prepare(s);
      if (!tokens.length) {
        matched.push({ sound: s, score: 0, index: i });
        continue;
      }
      var sc = scoreOne(s, tokens);
      if (sc > 0) matched.push({ sound: s, score: sc, index: i });
    }

    var sorted = sortItems(matched, sort, tokens.length > 0);
    return sorted.map(function (w) { return w.sound; });
  }

  /* ---------- URL param ---------- */

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
    init: function () {},
    getCategories: getCategories,
    getCategoryCounts: getCategoryCounts,
    apply: apply,
    readCategoryFromUrl: readCategoryFromUrl,
    normalize: norm
  };
})();