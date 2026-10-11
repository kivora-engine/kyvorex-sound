// sounds.js — data loading + orchestration of filters/rendering
(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};
  var DATA_URL = 'data/sounds.json';

  var state = {
    all: [],
    filtered: [],
    category: 'all',
    query: '',
    sort: 'relevance'
  };

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

  function hasActiveFilters() {
    return state.query.trim() !== '' || state.category !== 'all';
  }

  function countLabel(n) {
    return n + ' sound' + (n > 1 ? 's' : '');
  }

  function renderEmptyState() {
    var grid = document.getElementById('sounds-grid');
    if (!grid) return;

    var wrap = KY.ui.el('div', { class: 'sounds-empty' }, [
      KY.ui.el('p', { class: 'sounds-empty-msg', text: 'No sounds match your search.' }),
      KY.ui.el('p', { class: 'sounds-empty-hint', text: 'Try different keywords or reset the filters.' }),
      KY.ui.el('button', {
        class: 'btn btn-ghost',
        type: 'button',
        id: 'reset-filters',
        text: 'Reset filters'
      })
    ]);
    grid.appendChild(wrap);

    var btn = document.getElementById('reset-filters');
    if (btn) btn.addEventListener('click', resetFilters);
  }

  function resetFilters() {
    state.query = '';
    state.category = 'all';
    state.sort = 'relevance';
    var search = document.getElementById('search-input');
    if (search) search.value = '';
    var sortSel = document.getElementById('sort-select');
    if (sortSel) sortSel.value = 'relevance';
    refreshChips();
    render();
  }

  function render() {
    var grid = document.getElementById('sounds-grid');
    if (!grid) return;

    KY.ui.clear(grid);
    state.filtered = KY.filters.apply(state.all, {
      category: state.category,
      query: state.query,
      sort: state.sort
    });

    if (!state.filtered.length) {
      KY.ui.setStatus('No sounds match your search.');
      renderEmptyState();
      return;
    }

    var label = hasActiveFilters()
      ? countLabel(state.filtered.length) + ' found'
      : countLabel(state.filtered.length);
    KY.ui.setStatus(label);

    state.filtered.forEach(function (s) {
      grid.appendChild(KY.ui.renderSoundCard(s));
    });
  }

  function refreshChips() {
    var cats = KY.filters.getCategories(state.all);
    var counts = KY.filters.getCategoryCounts(state.all);
    KY.ui.renderChips(cats, state.category, counts, function (cat) {
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

  function bindSort() {
    var sel = document.getElementById('sort-select');
    if (!sel) return;
    sel.addEventListener('change', function (e) {
      state.sort = e.target.value || 'relevance';
      render();
    });
  }

  function init() {
    if (!document.getElementById('sounds-grid')) return;

    var urlCat = KY.filters.readCategoryFromUrl();
    if (urlCat) state.category = urlCat;

    KY.player.init();
    KY.downloads.init();
    KY.filters.init();
    KY.ui.init();

    bindGridEvents();
    bindSearch();
    bindSort();

    KY.ui.setStatus('Loading sounds...');

    loadData()
      .then(function (data) {
        state.all = normalize(data);

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