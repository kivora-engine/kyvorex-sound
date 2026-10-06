// ui.js — DOM building and card/chip rendering
(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};

  /* ---------- DOM helper ---------- */
  function el(tag, attrs, children) {
    var node = document.createElement(tag);
    if (attrs) {
      Object.keys(attrs).forEach(function (k) {
        var v = attrs[k];
        if (v == null) return;
        if (k === 'class') node.className = v;
        else if (k === 'text') node.textContent = v;
        else if (k === 'disabled' && v) node.disabled = true;
        else node.setAttribute(k, v);
      });
    }
    if (children != null) {
      (Array.isArray(children) ? children : [children]).forEach(function (c) {
        if (c == null) return;
        if (typeof c === 'string') node.appendChild(document.createTextNode(c));
        else node.appendChild(c);
      });
    }
    return node;
  }

  /* ---------- date formatting (locale-aware via Intl) ---------- */
  function formatDate(isoDate) {
    if (!isoDate || typeof isoDate !== 'string') return '';
    try {
      // Force local-time interpretation of the YYYY-MM-DD value
      // so the displayed day doesn't shift across timezones.
      var d = new Date(isoDate + 'T00:00:00');
      if (isNaN(d.getTime())) return isoDate;
      return new Intl.DateTimeFormat(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      }).format(d);
    } catch (e) {
      return isoDate;
    }
  }

  /* ---------- status badge ---------- */
  function statusBadge(sound) {
    if (sound.status === 'available') {
      return el('span', { class: 'sound-status available', text: 'Available' });
    }
    return el('span', { class: 'sound-status coming', text: 'Coming soon' });
  }

  function disabledBtn(label) {
    return el('button', {
      class: 'btn btn-disabled',
      type: 'button',
      disabled: true,
      text: label
    });
  }

  /* ---------- card ---------- */
  function renderSoundCard(sound) {
    var available = sound.status === 'available';
    var card = el('article', { class: 'sound-card', 'data-id': sound.id });

    var head = el('div', { class: 'sound-card-head' }, [
      el('div', null, [
        el('span', { class: 'sound-cat', text: sound.category || 'Uncategorized' }),
        el('h3', { text: sound.name || sound.id })
      ])
    ]);

    var desc = el('p', { class: 'sound-desc', text: sound.description || '' });

    var metaChildren = [
      el('span', { text: '⏱ ' + (sound.duration || '—') }),
      statusBadge(sound)
    ];
    if (sound.date) {
      metaChildren.push(el('span', {
        class: 'sound-date',
        text: 'Added ' + formatDate(sound.date)
      }));
    }
    var meta = el('div', { class: 'sound-meta' }, metaChildren);

    // Preview — always available (procedural engine).
    var previewBtn = el('button', {
      class: 'btn btn-ghost',
      type: 'button',
      'data-action': 'play',
      'data-id': sound.id,
      text: '▶ Preview'
    });

    // WAV — native <a download> when the file exists.
    var wavBtn;
    if (available && sound.wav) {
      wavBtn = el('a', {
        class: 'btn btn-secondary',
        href: sound.wav,
        download: sound.id + '.wav',
        rel: 'noopener',
        text: 'WAV'
      });
    } else {
      wavBtn = disabledBtn('WAV — soon');
    }

    // MP3 — native <a download> when the file exists.
    var mp3Btn;
    if (available && sound.mp3) {
      mp3Btn = el('a', {
        class: 'btn btn-primary',
        href: sound.mp3,
        download: sound.id + '.mp3',
        rel: 'noopener',
        text: 'MP3'
      });
    } else {
      mp3Btn = disabledBtn('MP3 — soon');
    }

    var actions = el('div', { class: 'sound-card-actions' }, [previewBtn, wavBtn, mp3Btn]);

    card.appendChild(head);
    card.appendChild(desc);
    card.appendChild(meta);
    card.appendChild(actions);
    return card;
  }

  /* ---------- chips ---------- */
  function renderChips(categories, activeCategory, onClick) {
    var container = document.getElementById('category-filters');
    if (!container) return;
    container.innerHTML = '';

    function chip(label, value) {
      return el('button', {
        class: 'chip' + (activeCategory === value ? ' active' : ''),
        type: 'button',
        'data-cat': value,
        text: label
      });
    }

    container.appendChild(chip('All', 'all'));
    categories.forEach(function (cat) { container.appendChild(chip(cat, cat)); });

    container.onclick = function (e) {
      var c = e.target.closest('.chip');
      if (!c) return;
      onClick(c.getAttribute('data-cat'));
    };
  }

  /* ---------- status line ---------- */
  var baseStatus = '';
  var flashTimer = null;
  function statusNode() { return document.getElementById('sounds-status'); }

  function setStatus(msg) {
    var node = statusNode();
    if (!node) return;
    baseStatus = msg || '';
    if (flashTimer) { clearTimeout(flashTimer); flashTimer = null; }
    node.textContent = baseStatus;
  }

  function flashStatus(msg, ms) {
    var node = statusNode();
    if (!node) return;
    if (flashTimer) clearTimeout(flashTimer);
    node.textContent = msg;
    flashTimer = setTimeout(function () {
      node.textContent = baseStatus;
      flashTimer = null;
    }, ms || 2500);
  }

  function clear(node) { if (node) node.innerHTML = ''; }

  KY.ui = {
    el: el,
    renderSoundCard: renderSoundCard,
    renderChips: renderChips,
    clear: clear,
    setStatus: setStatus,
    flashStatus: flashStatus,
    init: function () {}
  };
})();