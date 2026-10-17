// audio-presets.js — 35 procedural sound presets
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

  KY.audio.registerPreset('ui-click-001', {
    duration: 0.08,
    build: function (E) {
      E.tone({ freq: 1500, dur: 0.045, type: 'square', gain: 0.32, attack: 0.001 });
    }
  });

  KY.audio.registerPreset('ui-click-002', {
    duration: 0.07,
    build: function (E) {
      E.tone({ freq: 1100, dur: 0.05, type: 'sine', gain: 0.28, attack: 0.002 });
    }
  });

  KY.audio.registerPreset('ui-confirm-001', {
    duration: 0.26,
    build: function (E) {
      E.tone({ freq: 660, dur: 0.1, type: 'sine', gain: 0.32, when: 0.00, attack: 0.004 });
      E.tone({ freq: 880, dur: 0.12, type: 'sine', gain: 0.32, when: 0.09, attack: 0.004 });
    }
  });

  KY.audio.registerPreset('ui-hover-001', {
    duration: 0.06,
    build: function (E) {
      E.tone({ freq: 2200, dur: 0.04, type: 'sine', gain: 0.22, attack: 0.001 });
    }
  });

  KY.audio.registerPreset('ui-back-001', {
    duration: 0.12,
    build: function (E) {
      E.tone({ freq: 800, freqEnd: 500, dur: 0.10, type: 'triangle', gain: 0.28, attack: 0.003 });
    }
  });

  KY.audio.registerPreset('ui-toggle-001', {
    duration: 0.12,
    build: function (E) {
      E.tone({ freq: 950, dur: 0.04, type: 'square', gain: 0.26, when: 0.00, attack: 0.001 });
      E.tone({ freq: 650, dur: 0.04, type: 'square', gain: 0.26, when: 0.05, attack: 0.001 });
    }
  });

  // Two-note bell notification (D5 then A5, bell character).
  KY.audio.registerPreset('ui-notification-001', {
    duration: 0.22,
    build: function (E) {
      E.tone({ freq: 587.33, dur: 0.10, type: 'sine', gain: 0.30, when: 0.00, attack: 0.003 });
      E.tone({ freq: 880.00, dur: 0.13, type: 'sine', gain: 0.28, when: 0.10, attack: 0.003 });
    }
  });

  // Short rising whoosh for opening a menu.
  KY.audio.registerPreset('ui-open-001', {
    duration: 0.14,
    build: function (E) {
      E.tone({ freq: 420, freqEnd: 900, dur: 0.11, type: 'sine', gain: 0.26, attack: 0.004 });
    }
  });

  /* -----------------------------------------------------------
     ALERTS
     ----------------------------------------------------------- */

  KY.audio.registerPreset('alert-error-001', {
    duration: 0.36,
    build: function (E) {
      E.tone({ freq: 520, dur: 0.13, type: 'triangle', gain: 0.34, when: 0.00, attack: 0.003 });
      E.tone({ freq: 390, dur: 0.15, type: 'triangle', gain: 0.34, when: 0.13, attack: 0.003 });
    }
  });

  KY.audio.registerPreset('alert-success-001', {
    duration: 0.42,
    build: function (E) {
      var notes = [523.25, 659.25, 783.99];
      notes.forEach(function (f, i) {
        E.tone({ freq: f, dur: 0.13, type: 'sine', gain: 0.30, when: i * 0.1, attack: 0.005 });
      });
    }
  });

  KY.audio.registerPreset('alert-warning-001', {
    duration: 0.30,
    build: function (E) {
      E.tone({ freq: 750, dur: 0.11, type: 'triangle', gain: 0.30, when: 0.00, attack: 0.004 });
      E.tone({ freq: 600, dur: 0.13, type: 'triangle', gain: 0.30, when: 0.12, attack: 0.004 });
    }
  });

  KY.audio.registerPreset('alert-info-001', {
    duration: 0.25,
    build: function (E) {
      E.tone({ freq: 700, dur: 0.20, type: 'sine', gain: 0.28, attack: 0.005 });
    }
  });

  // Three quick ascending square notes (achievement).
  KY.audio.registerPreset('alert-achievement-001', {
    duration: 0.40,
    build: function (E) {
      var notes = [523.25, 659.25, 880.00];
      notes.forEach(function (f, i) {
        E.tone({ freq: f, dur: 0.09, type: 'square', gain: 0.24, when: i * 0.09, attack: 0.003 });
      });
    }
  });

  // Four ascending notes with a held final note (mission complete).
  KY.audio.registerPreset('alert-mission-complete-001', {
    duration: 0.60,
    build: function (E) {
      var steps = [
        { f: 523.25, t: 0.00, d: 0.10 },
        { f: 659.25, t: 0.10, d: 0.10 },
        { f: 783.99, t: 0.20, d: 0.10 },
        { f: 1046.50, t: 0.30, d: 0.28 }
      ];
      steps.forEach(function (s) {
        E.tone({ freq: s.f, dur: s.d, type: 'triangle', gain: 0.26, when: s.t, attack: 0.004 });
      });
    }
  });

  /* -----------------------------------------------------------
     GAMEPLAY
     ----------------------------------------------------------- */

  KY.audio.registerPreset('coin-pickup-001', {
    duration: 0.36,
    build: function (E) {
      E.tone({ freq: 987.77, dur: 0.09, type: 'square', gain: 0.28, when: 0.00, attack: 0.002 });
      E.tone({ freq: 1318.51, dur: 0.24, type: 'square', gain: 0.28, when: 0.09, attack: 0.002 });
    }
  });

  KY.audio.registerPreset('coin-pickup-002', {
    duration: 0.40,
    build: function (E) {
      var notes = [1046.50, 1318.51, 1567.98];
      notes.forEach(function (f, i) {
        E.tone({ freq: f, dur: 0.12, type: 'triangle', gain: 0.26, when: i * 0.08, attack: 0.002 });
      });
    }
  });

  KY.audio.registerPreset('jump-001', {
    duration: 0.22,
    build: function (E) {
      E.tone({ freq: 320, freqEnd: 1100, dur: 0.20, type: 'triangle', gain: 0.34, attack: 0.008 });
    }
  });

  KY.audio.registerPreset('hit-impact-001', {
    duration: 0.26,
    build: function (E) {
      E.tone({ freq: 140, freqEnd: 80, dur: 0.20, type: 'sine', gain: 0.40, attack: 0.002 });
      E.noise({ dur: 0.12, gain: 0.35, when: 0, filter: { type: 'lowpass', freq: 1800 } });
    }
  });

  KY.audio.registerPreset('explosion-small-001', {
    duration: 0.6,
    build: function (E) {
      E.noise({ dur: 0.55, gain: 0.45, seed: 7, filter: { type: 'lowpass', freq: 900 } });
      E.tone({ freq: 180, freqEnd: 45, dur: 0.50, type: 'sine', gain: 0.35, attack: 0.005 });
    }
  });

  KY.audio.registerPreset('footstep-single-001', {
    duration: 0.10,
    build: function (E) {
      E.tone({ freq: 95, freqEnd: 70, dur: 0.07, type: 'sine', gain: 0.40, attack: 0.001 });
      E.noise({ dur: 0.04, gain: 0.18, seed: 101, filter: { type: 'lowpass', freq: 1200 } });
    }
  });

  KY.audio.registerPreset('damage-player-001', {
    duration: 0.20,
    build: function (E) {
      E.tone({ freq: 400, freqEnd: 150, dur: 0.18, type: 'sawtooth', gain: 0.32, attack: 0.002 });
      E.noise({ dur: 0.06, gain: 0.18, seed: 13, filter: { type: 'lowpass', freq: 2000 } });
    }
  });

  KY.audio.registerPreset('checkpoint-001', {
    duration: 0.30,
    build: function (E) {
      E.tone({ freq: 550, dur: 0.11, type: 'sine', gain: 0.30, when: 0.00, attack: 0.004 });
      E.tone({ freq: 750, dur: 0.14, type: 'sine', gain: 0.30, when: 0.12, attack: 0.004 });
    }
  });

  KY.audio.registerPreset('checkpoint-002', {
    duration: 0.45,
    build: function (E) {
      var notes = [523.25, 659.25, 880.00];
      notes.forEach(function (f, i) {
        E.tone({ freq: f, dur: 0.14, type: 'triangle', gain: 0.26, when: i * 0.10, attack: 0.004 });
      });
    }
  });

  // Mechanical clatter then a bright reveal chime (chest open).
  KY.audio.registerPreset('chest-open-001', {
    duration: 0.55,
    build: function (E) {
      E.noise({ dur: 0.10, gain: 0.22, when: 0.00, seed: 71, filter: { type: 'bandpass', freq: 1800 } });
      E.noise({ dur: 0.08, gain: 0.20, when: 0.10, seed: 73, filter: { type: 'bandpass', freq: 2400 } });
      E.tone({ freq: 659.25, dur: 0.18, type: 'triangle', gain: 0.26, when: 0.22, attack: 0.004 });
      E.tone({ freq: 987.77, dur: 0.25, type: 'sine', gain: 0.24, when: 0.34, attack: 0.005 });
    }
  });

  // Wooden door: low filtered noise (creak) + descending low tone.
  KY.audio.registerPreset('door-open-001', {
    duration: 0.48,
    build: function (E) {
      E.noise({ dur: 0.35, gain: 0.28, when: 0.00, seed: 33, filter: { type: 'bandpass', freq: 600 } });
      E.tone({ freq: 220, freqEnd: 130, dur: 0.35, type: 'triangle', gain: 0.28, when: 0.02, attack: 0.005 });
    }
  });

  // Short natural landing thump (distinct from jump).
  KY.audio.registerPreset('landing-001', {
    duration: 0.14,
    build: function (E) {
      E.tone({ freq: 110, freqEnd: 80, dur: 0.10, type: 'sine', gain: 0.42, attack: 0.002 });
      E.noise({ dur: 0.04, gain: 0.15, when: 0.00, seed: 91, filter: { type: 'lowpass', freq: 900 } });
    }
  });

  // Magic cast: rising shimmer then a crystalline release tone.
  KY.audio.registerPreset('magic-cast-001', {
    duration: 0.65,
    build: function (E) {
      E.tone({ freq: 500, freqEnd: 1300, dur: 0.30, type: 'triangle', gain: 0.26, when: 0.00, attack: 0.010 });
      E.tone({ freq: 1760, dur: 0.28, type: 'sine', gain: 0.24, when: 0.32, attack: 0.006 });
      E.tone({ freq: 2637, dur: 0.18, type: 'sine', gain: 0.16, when: 0.36, attack: 0.006 });
    }
  });

  /* -----------------------------------------------------------
     SCI-FI
     ----------------------------------------------------------- */

  KY.audio.registerPreset('laser-shot-001', {
    duration: 0.22,
    build: function (E) {
      E.tone({ freq: 1800, freqEnd: 240, dur: 0.18, type: 'sawtooth', gain: 0.30, attack: 0.002 });
    }
  });

  KY.audio.registerPreset('laser-shot-002', {
    duration: 0.24,
    build: function (E) {
      E.tone({ freq: 2200, freqEnd: 1200, dur: 0.06, type: 'square', gain: 0.24, when: 0.00, attack: 0.002 });
      E.tone({ freq: 1200, freqEnd: 300, dur: 0.16, type: 'sawtooth', gain: 0.30, when: 0.05, attack: 0.002 });
    }
  });

  KY.audio.registerPreset('power-up-001', {
    duration: 0.52,
    build: function (E) {
      var notes = [440, 554.37, 659.25, 880];
      notes.forEach(function (f, i) {
        E.tone({ freq: f, dur: 0.11, type: 'square', gain: 0.26, when: i * 0.08, attack: 0.003 });
      });
    }
  });

  KY.audio.registerPreset('power-up-002', {
    duration: 0.55,
    build: function (E) {
      E.tone({ freq: 300, freqEnd: 1100, dur: 0.35, type: 'sine', gain: 0.28, attack: 0.008 });
      E.tone({ freq: 1320, dur: 0.20, type: 'triangle', gain: 0.24, when: 0.30, attack: 0.005 });
    }
  });

  KY.audio.registerPreset('shield-activate-001', {
    duration: 0.40,
    build: function (E) {
      E.tone({ freq: 250, freqEnd: 900, dur: 0.35, type: 'triangle', gain: 0.30, attack: 0.010 });
    }
  });

  KY.audio.registerPreset('teleport-001', {
    duration: 0.30,
    build: function (E) {
      E.tone({ freq: 300, freqEnd: 1400, dur: 0.15, type: 'sine', gain: 0.30, when: 0.00, attack: 0.003 });
      E.tone({ freq: 1400, freqEnd: 350, dur: 0.15, type: 'sine', gain: 0.30, when: 0.15, attack: 0.003 });
    }
  });

  // Progressive rising energy charge with tremolo-like modulation.
  KY.audio.registerPreset('energy-charge-001', {
    duration: 0.75,
    build: function (E) {
      E.tone({ freq: 180, freqEnd: 900, dur: 0.55, type: 'sawtooth', gain: 0.20, attack: 0.020 });
      E.tone({ freq: 90, freqEnd: 450, dur: 0.55, type: 'sine', gain: 0.22, attack: 0.020 });
      E.tone({ freq: 1320, dur: 0.16, type: 'triangle', gain: 0.22, when: 0.58, attack: 0.004 });
    }
  });

  // Scanner sweep: soft descending scan + two precise blips.
  KY.audio.registerPreset('scanner-001', {
    duration: 0.60,
    build: function (E) {
      E.tone({ freq: 1400, freqEnd: 500, dur: 0.30, type: 'sine', gain: 0.20, attack: 0.010 });
      E.tone({ freq: 900, dur: 0.06, type: 'sine', gain: 0.24, when: 0.32, attack: 0.002 });
      E.tone({ freq: 900, dur: 0.06, type: 'sine', gain: 0.24, when: 0.46, attack: 0.002 });
    }
  });
})();