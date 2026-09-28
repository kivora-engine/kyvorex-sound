// sounds.js — data loading + orchestration of filters/rendering
(function () {
  'use strict';

  var KY = window.KYVOREX = window.KYVOREX || {};
  var DATA_URL = 'data/sounds.json';

  var state = { all: [], filtered: [], category: 'all', query: '' };

  function loadData() {
    return fetch(DATA_URL).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    });
  }

  function normalize(data) {
    if (!data) return [];
    if (Array.isArray(data)) return data;
    if (Array.isArray(data.sounds)) return data.sounds;
    return [];
  }

  function render() {
    var grid = document.getElementById('sounds-grid');
    if (!grid) return;

    KY.ui.clear(grid);
    state.filtered = KY.filters.apply(state.all, {
      category: state.category,
      query: state.query
    });

    if (!state.filtered.length) {
      KY.ui.setStatus('No sounds match your search.');
      return;
    }
    KY.ui.setStatus(state.filtered.length + ' sound' + (state.filtered.length > 1 ? 's' : ''));
    state.filtered.forEach(function (s) {
      grid.appendChild(KY.ui.renderSoundCard(s));
    });
  }

  function refreshChips() {
    var cats = KY.filters.getCategories(state.all);
    KY.ui.renderChips(cats, state.category, function (cat) {
      state.category = cat;
      refreshChips();
      render();
    });
  }

  function findById(id) {
    for (var i = 0; i < state.all.length; i++) {
      if (state.all[i].id === id) return state.all[i];
    }
    return null;
  }

  function bindGridEvents() {
    var grid = document.getElementById('sounds-grid');
    if (!grid) return;
    grid.addEventListener('click', function (e) {
      var trigger = e.target.closest('[data-action]');
      if (!trigger) return;
      var action = trigger.getAttribute('data-action');
      var id = trigger.getAttribute('data-id');
      var sound = findById(id);
      if (!sound) return;

      if (action === 'play') {
        e.preventDefault();
        KY.player.toggle(sound);
      } else if (action === 'download-mp3' || action === 'download-wav') {
        KY.downloads.handle(action, sound, e);
      }
    });
  }

  function bindSearch() {
    var search = document.getElementById('search-input');
    if (!search) return;
    search.addEventListener('input', function (e) {
      state.query = e.target.value || '';
      render();
    });
  }

  function init() {
    if (!document.getElementById('sounds-grid')) return;

    // Read ?category= before data loads.
    var urlCat = KY.filters.readCategoryFromUrl();
    if (urlCat) state.category = urlCat;

    KY.player.init();
    KY.downloads.init();
    KY.filters.init();
    KY.ui.init();

    bindGridEvents();
    bindSearch();

    KY.ui.setStatus('Loading sounds...');

    loadData()
      .then(function (data) {
        state.all = normalize(data);

        // Validate initial category against actual data.
        var cats = KY.filters.getCategories(state.all);
        if (state.category !== 'all' && cats.indexOf(state.category) === -1) {
          state.category = 'all';
        }

        refreshChips();
        render();
      })
      .catch(function (err) {
        console.error('[KYVOREX] failed to load sounds.json:', err);
        KY.ui.setStatus(
          'Could not load sound data. Please open the project through a local web server or hosted website.'
        );
      });
  }

  KY.sounds = {
    init: init,
    getAll: function () { return state.all; },
    getFiltered: function () { return state.filtered; },
    findById: findById
  };
})();