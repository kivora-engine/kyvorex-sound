// news.js — Loads announcements or updates dynamically
(function () {
  'use strict';

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

  function formatDate(isoDate) {
    if (!isoDate) return '';
    try {
      var d = new Date(isoDate + 'T00:00:00');
      return new Intl.DateTimeFormat(undefined, { year: 'numeric', month: 'short', day: 'numeric' }).format(d);
    } catch (e) { return isoDate; }
  }

  function renderNews(data, type) {
    var container = document.getElementById('news-container');
    if (!container) return;
    container.innerHTML = '';

    var items = data[type] || [];
    if (items.length === 0) {
      container.appendChild(el('p', { class: 'muted', text: 'No news at the moment.' }));
      return;
    }

    items.sort(function(a, b) {
      return new Date(b.date) - new Date(a.date);
    });

    items.forEach(function (item) {
      var card = el('article', { class: 'news-card' });

      var header = el('div', { class: 'news-header' }, [
        el('span', { class: 'news-date', text: formatDate(item.date) }),
        el('h3', { class: 'news-title', text: item.title })
      ]);

      var body = el('p', { class: 'news-desc', text: item.message || item.description });

      card.appendChild(header);
      card.appendChild(body);
      container.appendChild(card);
    });
  }

  function init() {
    var container = document.getElementById('news-container');
    if (!container) return;

    var dataType = container.getAttribute('data-type');
    var jsonFile = dataType === 'updates' ? 'data/updates.json' : 'data/announcements.json';

    fetch(jsonFile)
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.json();
      })
      .then(function (data) {
        renderNews(data, dataType);
      })
      .catch(function (err) {
        console.error('[KYVOREX NEWS] Failed to load:', err);
        container.innerHTML = '<p class="muted">Unable to load news. Please try again later.</p>';
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();