// home.js — renders homepage categories and count from data/sounds.json
(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};

  var DESCRIPTIONS = {
    'Interface': 'Commands, menus, sliders and interactions.',
    'Alerts': 'Confirmations, errors, warnings and success.',
    'Gameplay': 'Movements, objects, actions and game feedback.',
    'Sci-Fi': 'Energy, electronic systems and futuristic effects.',
    'Magic / Fantasy': 'Spells, magic heals, elements and portals.',
    'Environment': 'Wind, thunder, rain and ambient details.'
  };

  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        var v = attrs[k];
        if (v == null) return;
        if (k === 'class') node.className = v;
        else if (k === 'text') node.textContent = v;
        else node.setAttribute(k, v);
      });
    }
    if (children) {
      (Array.isArray(children) ? children : [children]).forEach(function (c) {
        if (c == null) return;
        if (typeof c === 'string') node.appendChild(document.createTextNode(c));
        else node.appendChild(c);
      });
    }
    return node;
  }

  function renderCategories(counts, total) {
    var container = document.getElementById('category-grid');
    if (!container) return;
    container.innerHTML = '';

    var countEl = document.getElementById('home-sound-count');
    if (countEl) countEl.textContent = total + ' sounds available now.';

    if (Object.keys(counts).length === 0) {
      container.appendChild(el('p', { class: 'category-empty', text: 'Categories will appear here as the library grows.' }));
      return;
    }

    Object.keys(counts).sort().forEach(function (cat) {
      var desc = DESCRIPTIONS[cat];
      var children = [
        el('span', { class: 'cat-dot' }),
        el('h3', { text: cat })
      ];
      if (desc) children.push(el('p', { text: desc }));
      children.push(el('span', { class: 'cat-count', text: counts[cat] + ' sounds' }));

      var card = el('a', {
        class: 'category-card',
        href: 'sounds.html?category=' + encodeURIComponent(cat)
      }, children);

      container.appendChild(card);
    });
  }

  function init() {
    var container = document.getElementById('category-grid');
    if (!container) return;

    fetch('data/sounds.json')
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (data) {
        var list = Array.isArray(data) ? data : (data && data.sounds) || [];
        var counts = {};
        list.forEach(function (s) { if (s && s.category) counts[s.category] = (counts[s.category] || 0) + 1; });
        renderCategories(counts, list.length);
      })
      .catch(function () {
        var countEl = document.getElementById('home-sound-count');
        if (countEl) countEl.textContent = 'Unable to load sound count.';
        renderCategories({}, 0);
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

  KY.home = { init: init };
})();