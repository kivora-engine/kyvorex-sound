// player.js — procedural preview via KY.audio engine
(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};

  var current = null;
  var playing = false;
  var bar, titleEl, stateEl, toggleBtn, stopBtn;

  function log() {
    if (!window.console || !console.log) return;
    var a = Array.prototype.slice.call(arguments);
    a.unshift('[KYVOREX PLAYER]');
    console.log.apply(console, a);
  }
  function logErr() {
    if (!window.console || !console.error) return;
    var a = Array.prototype.slice.call(arguments);
    a.unshift('[KYVOREX PLAYER]');
    console.error.apply(console, a);
  }

  function setState(text) { if (stateEl) stateEl.textContent = text; }
  function updateToggle() { if (toggleBtn) toggleBtn.textContent = playing ? '❚❚' : '▶'; }

  function showBar(sound) {
    if (!bar) return;
    bar.classList.remove('hidden');
    if (titleEl) titleEl.textContent = sound ? (sound.name || sound.id) : '—';
  }

  function hasPreset(id) {
    return !!(KY.audio && KY.audio.getPreset && KY.audio.getPreset(id));
  }

  function play(sound) {
    if (!sound) return;
    if (!KY.audio) {
      logErr('audio engine not loaded');
      setState('Preview unavailable');
      return;
    }
    showBar(sound);
    current = sound;

    if (!hasPreset(sound.id)) {
      logErr('no preset registered for:', sound.id);
      setState('Preview unavailable');
      return;
    }

    setState('Loading');
    log('Playing preset:', sound.id);
    KY.audio.playPreset(sound.id)
      .then(function (info) {
        log('Started:', info.id, 'duration=' + info.duration.toFixed(3) + 's');
      })
      .catch(function (err) {
        var name = err && err.name ? err.name : 'Error';
        var msg = err && err.message ? err.message : String(err);
        logErr('playPreset failed:', name, '-', msg);
        setState('Unable to start audio playback.');
      });
  }

  function toggle(sound) {
    if (sound && (!current || current.id !== sound.id)) {
      play(sound);
      return;
    }
    if (playing) {
      KY.audio.stop();
    } else if (current) {
      play(current);
    }
  }

  function stop() {
    if (KY.audio) KY.audio.stop();
  }

  function init() {
    bar = document.getElementById('player-bar');
    titleEl = document.getElementById('player-title');
    stateEl = document.getElementById('player-state');
    toggleBtn = document.getElementById('player-toggle');
    stopBtn = document.getElementById('player-stop');

    if (toggleBtn) {
      toggleBtn.addEventListener('click', function () {
        if (!current) return;
        toggle(current);
      });
    }
    if (stopBtn) stopBtn.addEventListener('click', stop);

    if (KY.audio && KY.audio.on) {
      KY.audio.on('start', function (data) {
        playing = true;
        setState('Playing');
        updateToggle();
        if (data && data.id && titleEl && (!current || current.id !== data.id)) {
          // Shouldn't happen — play() sets current first.
        }
      });
      KY.audio.on('stop', function () {
        playing = false;
        setState('Stopped');
        updateToggle();
      });
      KY.audio.on('error', function (data) {
        playing = false;
        setState('Preview unavailable');
        updateToggle();
        logErr('engine error', data);
      });
    }
  }

  KY.player = { init: init, play: play, toggle: toggle, stop: stop };
})();