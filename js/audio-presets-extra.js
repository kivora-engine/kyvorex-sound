// audio-presets-extra.js — 30 new sound presets
(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};
  if (!KY.audio) {
    console.error('[KYVOREX PRESETS] audio-engine.js must load first');
    return;
  }

  /* INTERFACE */
  KY.audio.registerPreset('ui-menu-close-001', { duration: 0.12, build: function(E) { E.tone({ freq: 800, freqEnd: 400, dur: 0.10, type: 'triangle', gain: 0.28, attack: 0.003 }); } });
  KY.audio.registerPreset('ui-modal-open-001', { duration: 0.15, build: function(E) { E.tone({ freq: 600, dur: 0.08, type: 'sine', gain: 0.30, attack: 0.002 }); E.tone({ freq: 1200, dur: 0.06, type: 'sine', gain: 0.15, when: 0.05, attack: 0.002 }); } });
  KY.audio.registerPreset('ui-slider-change-001', { duration: 0.04, build: function(E) { E.tone({ freq: 1800, dur: 0.02, type: 'square', gain: 0.20, attack: 0.001 }); } });
  KY.audio.registerPreset('ui-tab-switch-001', { duration: 0.08, build: function(E) { E.tone({ freq: 950, freqEnd: 1100, dur: 0.06, type: 'triangle', gain: 0.22, attack: 0.002 }); } });
  KY.audio.registerPreset('ui-confirm-002', { duration: 0.20, build: function(E) { E.tone({ freq: 500, dur: 0.08, type: 'square', gain: 0.25, when: 0.00, attack: 0.002 }); E.tone({ freq: 750, dur: 0.10, type: 'square', gain: 0.25, when: 0.08, attack: 0.002 }); } });
  KY.audio.registerPreset('ui-back-002', { duration: 0.10, build: function(E) { E.tone({ freq: 600, freqEnd: 300, dur: 0.08, type: 'square', gain: 0.25, attack: 0.002 }); } });
  KY.audio.registerPreset('ui-hover-002', { duration: 0.05, build: function(E) { E.tone({ freq: 1800, dur: 0.03, type: 'triangle', gain: 0.20, attack: 0.001 }); } });
  KY.audio.registerPreset('ui-toggle-002', { duration: 0.10, build: function(E) { E.tone({ freq: 1200, dur: 0.03, type: 'sine', gain: 0.28, when: 0.00, attack: 0.001 }); E.tone({ freq: 800, dur: 0.03, type: 'sine', gain: 0.28, when: 0.05, attack: 0.001 }); } });

  /* ALERTS */
  KY.audio.registerPreset('alert-error-002', { duration: 0.40, build: function(E) { E.tone({ freq: 400, dur: 0.15, type: 'sawtooth', gain: 0.30, when: 0.00, attack: 0.004 }); E.tone({ freq: 300, dur: 0.15, type: 'sawtooth', gain: 0.30, when: 0.15, attack: 0.004 }); } });
  KY.audio.registerPreset('alert-success-002', { duration: 0.50, build: function(E) { var n = [523.25, 659.25, 783.99, 1046.50]; n.forEach(function(f, i) { E.tone({ freq: f, dur: 0.12, type: 'triangle', gain: 0.28, when: i * 0.1, attack: 0.004 }); }); } });

  /* GAMEPLAY */
  KY.audio.registerPreset('item-drop-001', { duration: 0.18, build: function(E) { E.tone({ freq: 600, freqEnd: 200, dur: 0.15, type: 'sine', gain: 0.35, attack: 0.002 }); } });
  KY.audio.registerPreset('door-metal-open-001', { duration: 0.60, build: function(E) { E.noise({ dur: 0.5, gain: 0.20, seed: 42, filter: { type: 'bandpass', freq: 1200 } }); E.tone({ freq: 150, freqEnd: 80, dur: 0.55, type: 'sawtooth', gain: 0.25, attack: 0.010 }); } });
  KY.audio.registerPreset('object-break-001', { duration: 0.25, build: function(E) { E.noise({ dur: 0.2, gain: 0.40, seed: 88, filter: { type: 'highpass', freq: 800 } }); E.tone({ freq: 200, freqEnd: 100, dur: 0.1, type: 'square', gain: 0.20, attack: 0.002 }); } });
  KY.audio.registerPreset('lever-pull-001', { duration: 0.30, build: function(E) { E.noise({ dur: 0.1, gain: 0.25, seed: 55, filter: { type: 'lowpass', freq: 600 } }); E.tone({ freq: 250, freqEnd: 150, dur: 0.15, type: 'triangle', gain: 0.30, when: 0.10, attack: 0.002 }); } });
  KY.audio.registerPreset('jump-002', { duration: 0.25, build: function(E) { E.tone({ freq: 200, freqEnd: 800, dur: 0.20, type: 'square', gain: 0.25, attack: 0.005 }); } });
  KY.audio.registerPreset('hit-impact-002', { duration: 0.30, build: function(E) { E.tone({ freq: 100, freqEnd: 50, dur: 0.25, type: 'sawtooth', gain: 0.40, attack: 0.002 }); E.noise({ dur: 0.15, gain: 0.30, seed: 21, filter: { type: 'lowpass', freq: 1000 } }); } });
  KY.audio.registerPreset('explosion-small-002', { duration: 0.70, build: function(E) { E.noise({ dur: 0.6, gain: 0.40, seed: 15, filter: { type: 'lowpass', freq: 600 } }); E.tone({ freq: 120, freqEnd: 40, dur: 0.6, type: 'sawtooth', gain: 0.30, attack: 0.005 }); } });
  KY.audio.registerPreset('damage-player-002', { duration: 0.25, build: function(E) { E.tone({ freq: 300, freqEnd: 100, dur: 0.20, type: 'square', gain: 0.30, attack: 0.003 }); E.noise({ dur: 0.08, gain: 0.15, seed: 33, filter: { type: 'lowpass', freq: 1500 } }); } });

  /* SCI-FI */
  KY.audio.registerPreset('sci-fi-system-boot-001', { duration: 0.80, build: function(E) { E.tone({ freq: 100, freqEnd: 600, dur: 0.50, type: 'sawtooth', gain: 0.20, attack: 0.010 }); E.tone({ freq: 1200, dur: 0.20, type: 'sine', gain: 0.25, when: 0.55, attack: 0.005 }); } });
  KY.audio.registerPreset('robot-servo-move-001', { duration: 0.20, build: function(E) { E.tone({ freq: 800, freqEnd: 1200, dur: 0.10, type: 'square', gain: 0.20, attack: 0.002 }); E.tone({ freq: 1000, freqEnd: 800, dur: 0.10, type: 'square', gain: 0.20, when: 0.10, attack: 0.002 }); } });
  KY.audio.registerPreset('sci-fi-data-transfer-001', { duration: 0.40, build: function(E) { for(var i=0; i<6; i++) { E.tone({ freq: 1500 + (i*100), dur: 0.04, type: 'sine', gain: 0.20, when: i*0.05, attack: 0.001 }); } } });
  KY.audio.registerPreset('sci-fi-force-field-hit-001', { duration: 0.35, build: function(E) { E.tone({ freq: 400, freqEnd: 150, dur: 0.30, type: 'sawtooth', gain: 0.35, attack: 0.002 }); E.noise({ dur: 0.1, gain: 0.20, seed: 99, filter: { type: 'bandpass', freq: 2000 } }); } });

  /* MAGIC / FANTASY */
  KY.audio.registerPreset('magic-fire-cast-001', { duration: 0.50, build: function(E) { E.noise({ dur: 0.4, gain: 0.30, seed: 66, filter: { type: 'lowpass', freq: 1500 } }); E.tone({ freq: 300, freqEnd: 100, dur: 0.4, type: 'sawtooth', gain: 0.25, attack: 0.005 }); } });
  KY.audio.registerPreset('magic-ice-cast-001', { duration: 0.45, build: function(E) { E.tone({ freq: 1500, dur: 0.20, type: 'sine', gain: 0.25, attack: 0.002 }); E.tone({ freq: 2000, dur: 0.15, type: 'sine', gain: 0.20, when: 0.10, attack: 0.002 }); } });
  KY.audio.registerPreset('magic-heal-001', { duration: 0.60, build: function(E) { var n = [440, 554.37, 659.25, 880]; n.forEach(function(f, i) { E.tone({ freq: f, dur: 0.20, type: 'sine', gain: 0.22, when: i*0.12, attack: 0.010 }); }); } });
  KY.audio.registerPreset('magic-portal-open-001', { duration: 0.70, build: function(E) { E.tone({ freq: 150, freqEnd: 600, dur: 0.50, type: 'triangle', gain: 0.30, attack: 0.020 }); E.tone({ freq: 1000, dur: 0.20, type: 'sine', gain: 0.20, when: 0.50, attack: 0.005 }); } });

  /* ENVIRONMENT */
  KY.audio.registerPreset('environment-wind-gust-001', { duration: 0.80, build: function(E) { E.noise({ dur: 0.7, gain: 0.35, seed: 12, filter: { type: 'lowpass', freq: 800 } }); } });
  KY.audio.registerPreset('environment-thunder-001', { duration: 1.20, build: function(E) { E.noise({ dur: 1.0, gain: 0.50, seed: 77, filter: { type: 'lowpass', freq: 200 } }); E.tone({ freq: 60, freqEnd: 30, dur: 1.0, type: 'sine', gain: 0.40, attack: 0.010 }); } });
  KY.audio.registerPreset('environment-rain-start-001', { duration: 0.50, build: function(E) { for(var i=0; i<12; i++) { E.noise({ dur: 0.05, gain: 0.10, seed: 100+i, when: i*0.04, filter: { type: 'highpass', freq: 3000 } }); } } });
  KY.audio.registerPreset('environment-cave-drip-001', { duration: 0.60, build: function(E) { E.tone({ freq: 1200, freqEnd: 800, dur: 0.10, type: 'sine', gain: 0.30, when: 0.00, attack: 0.002 }); E.tone({ freq: 1200, freqEnd: 800, dur: 0.10, type: 'sine', gain: 0.15, when: 0.15, attack: 0.002 }); E.tone({ freq: 1200, freqEnd: 800, dur: 0.10, type: 'sine', gain: 0.07, when: 0.30, attack: 0.002 }); } });
})();