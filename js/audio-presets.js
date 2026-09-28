// audio-presets.js — 10 procedural sound presets
(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};
  if (!KY.audio) {
    console.error('[KYVOREX PRESETS] audio-engine.js must load first');
    return;
  }

  /* -----------------------------------------------------------
     INTERFACE
     ----------------------------------------------------------- */

  // Short square click.
  KY.audio.registerPreset('ui-click-001', {
    duration: 0.08,
    build: function (E) {
      E.tone({ freq: 1500, dur: 0.045, type: 'square', gain: 0.32, attack: 0.001, release: 0.035 });
    }
  });

  // Two ascending sine tones.
  KY.audio.registerPreset('ui-confirm-001', {
    duration: 0.26,
    build: function (E) {
      E.tone({ freq: 660, dur: 0.1, type: 'sine', gain: 0.32, when: 0.00, attack: 0.004, release: 0.08 });
      E.tone({ freq: 880, dur: 0.12, type: 'sine', gain: 0.32, when: 0.09, attack: 0.004, release: 0.1 });
    }
  });

  /* -----------------------------------------------------------
     ALERTS
     ----------------------------------------------------------- */

  // Two descending tones, harsher (triangle + slight square).
  KY.audio.registerPreset('alert-error-001', {
    duration: 0.36,
    build: function (E) {
      E.tone({ freq: 520, dur: 0.13, type: 'triangle', gain: 0.34, when: 0.00, attack: 0.003, release: 0.11 });
      E.tone({ freq: 390, dur: 0.15, type: 'triangle', gain: 0.34, when: 0.13, attack: 0.003, release: 0.13 });
    }
  });

  // Ascending arpeggio C-E-G.
  KY.audio.registerPreset('alert-success-001', {
    duration: 0.42,
    build: function (E) {
      var notes = [523.25, 659.25, 783.99];
      notes.forEach(function (f, i) {
        E.tone({ freq: f, dur: 0.13, type: 'sine', gain: 0.3, when: i * 0.1, attack: 0.005, release: 0.11 });
      });
    }
  });

  /* -----------------------------------------------------------
     GAME
     ----------------------------------------------------------- */

  // Two short notes with a bright high tail (arcade coin).
  KY.audio.registerPreset('coin-pickup-001', {
    duration: 0.36,
    build: function (E) {
      E.tone({ freq: 987.77, dur: 0.09, type: 'square', gain: 0.28, when: 0.00, attack: 0.002, release: 0.07 });
      E.tone({ freq: 1318.51, dur: 0.24, type: 'square', gain: 0.28, when: 0.09, attack: 0.002, release: 0.22 });
    }
  });

  // Fast rising sweep (jump).
  KY.audio.registerPreset('jump-001', {
    duration: 0.22,
    build: function (E) {
      E.tone({ freq: 320, freqEnd: 1100, dur: 0.2, type: 'triangle', gain: 0.34, attack: 0.008, release: 0.02 });
    }
  });

  // Low tone + noise burst (impact).
  KY.audio.registerPreset('hit-impact-001', {
    duration: 0.26,
    build: function (E) {
      E.tone({ freq: 140, freqEnd: 80, dur: 0.2, type: 'sine', gain: 0.4, attack: 0.002, release: 0.18 });
      E.noise({ dur: 0.12, gain: 0.35, when: 0, filter: { type: 'lowpass', freq: 1800 } });
    }
  });

  // Filtered noise + downward low sweep (small explosion).
  KY.audio.registerPreset('explosion-small-001', {
    duration: 0.6,
    build: function (E) {
      E.noise({ dur: 0.55, gain: 0.45, seed: 7, filter: { type: 'lowpass', freq: 900 } });
      E.tone({ freq: 180, freqEnd: 45, dur: 0.5, type: 'sine', gain: 0.35, attack: 0.005, release: 0.4 });
    }
  });

  /* -----------------------------------------------------------
     SCI-FI
     ----------------------------------------------------------- */

  // Fast downward sweep (laser shot).
  KY.audio.registerPreset('laser-shot-001', {
    duration: 0.22,
    build: function (E) {
      E.tone({ freq: 1800, freqEnd: 240, dur: 0.18, type: 'sawtooth', gain: 0.3, attack: 0.002, release: 0.04 });
    }
  });

  // Four ascending notes (power up).
  KY.audio.registerPreset('power-up-001', {
    duration: 0.52,
    build: function (E) {
      var notes = [440, 554.37, 659.25, 880];
      notes.forEach(function (f, i) {
        E.tone({ freq: f, dur: 0.11, type: 'square', gain: 0.26, when: i * 0.08, attack: 0.003, release: 0.09 });
      });
    }
  });
})();