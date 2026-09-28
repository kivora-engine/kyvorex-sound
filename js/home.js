// home.js — homepage categories, initialized by app.js only
(function () {
  'use strict';

  var KY = window.KYVOREX = window.KYVOREX || {};

  var DESCRIPTIONS = {
    'Interface': 'Clicks, taps, notifications.',
    'Game': 'Actions, hits, pickups, feedback.',
    'Alerts': 'Success, error, warning.',
    'Sci-Fi': 'Energy, lasers, futuristic effects.',
    'Gameplay': 'Actions, hits, feedback.',
    'Ambient': 'Loops and atmospheres.'
  };

  var initialized = false;

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

  function render(categories) {
    var container = document.getElementById('category-grid');
    if (!container) return;
    container.innerHTML = '';

    if (!categories.length) {
      container.appendChild(el('p', {
        class: 'category-empty',
        text: 'Categories will appear here as the library grows.'
      }));
      return;
    }

    categories.forEach(function (cat) {
      var children = [
        el('span', { class: 'cat-dot' }),
        el('h3', { text: cat })
      ];
      var desc = DESCRIPTIONS[cat];
      if (desc) children.push(el('p', { text: desc }));

      container.appendChild(el('a', {
        class: 'category-card',
        href: 'sounds.html?category=' + encodeURIComponent(cat)
      }, children));
    });
  }

  function init() {
    if (initialized) return;
    initialized = true;

    var container = document.getElementById('category-grid');
    if (!container) return;

    fetch('data/sounds.json')
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (data) {
        var list = Array.isArray(data) ? data : (data && data.sounds) || [];
        var seen = {};
        list.forEach(function (s) { if (s && s.category) seen[s.category] = true; });
        render(Object.keys(seen).sort());
      })
      .catch(function () {
        render([]);
      });
  }

  KY.home = { init: init };
})();