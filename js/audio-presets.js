// audio-presets.js — 25 procedural sound presets
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
      E.tone({ freq: 1500, dur: 0.045, type: 'square', gain: 0.32, attack: 0.001 });
    }
  });

  // Softer sine click, lower pitch.
  KY.audio.registerPreset('ui-click-002', {
    duration: 0.07,
    build: function (E) {
      E.tone({ freq: 1100, dur: 0.05, type: 'sine', gain: 0.28, attack: 0.002 });
    }
  });

  // Two ascending sine tones.
  KY.audio.registerPreset('ui-confirm-001', {
    duration: 0.26,
    build: function (E) {
      E.tone({ freq: 660, dur: 0.1, type: 'sine', gain: 0.32, when: 0.00, attack: 0.004 });
      E.tone({ freq: 880, dur: 0.12, type: 'sine', gain: 0.32, when: 0.09, attack: 0.004 });
    }
  });

  // Very soft high tone for hover feedback.
  KY.audio.registerPreset('ui-hover-001', {
    duration: 0.06,
    build: function (E) {
      E.tone({ freq: 2200, dur: 0.04, type: 'sine', gain: 0.22, attack: 0.001 });
    }
  });

  // Short downward triangle sweep (back / close).
  KY.audio.registerPreset('ui-back-001', {
    duration: 0.12,
    build: function (E) {
      E.tone({ freq: 800, freqEnd: 500, dur: 0.10, type: 'triangle', gain: 0.28, attack: 0.003 });
    }
  });

  // Two quick blips (toggle on/off).
  KY.audio.registerPreset('ui-toggle-001', {
    duration: 0.12,
    build: function (E) {
      E.tone({ freq: 950, dur: 0.04, type: 'square', gain: 0.26, when: 0.00, attack: 0.001 });
      E.tone({ freq: 650, dur: 0.04, type: 'square', gain: 0.26, when: 0.05, attack: 0.001 });
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

  // Three-note triangle arpeggio — bright and bouncy.
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

  // Three ascending bell tones — larger, more rewarding.
  KY.audio.registerPreset('checkpoint-002', {
    duration: 0.45,
    build: function (E) {
      var notes = [523.25, 659.25, 880.00];
      notes.forEach(function (f, i) {
        E.tone({ freq: f, dur: 0.14, type: 'triangle', gain: 0.26, when: i * 0.10, attack: 0.004 });
      });
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

  // Two-phase sweep: brief bright chirp then deeper discharge.
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

  // Continuous rising sweep + high bell finish — smooth energy build.
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
})();