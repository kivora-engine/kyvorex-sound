// audio-presets-extra.js — 55 extra sound presets
(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};
  if (!KY.audio) { return; }

  // ... [GARDE TOUS TES PRESETS EXISTANTS ICI] ...

  /* HALLOWEEN */
  KY.audio.registerPreset('raven-caw-001', { duration: 0.25, build: function(E) { E.noise({ dur: 0.15, gain: 0.30, seed: 666, filter: { type: 'bandpass', freq: 1500 } }); E.tone({ freq: 800, freqEnd: 200, dur: 0.15, type: 'sawtooth', gain: 0.35, attack: 0.002 }); } });
  KY.audio.registerPreset('ghost-apparition-001', { duration: 0.80, build: function(E) { E.tone({ freq: 200, freqEnd: 800, dur: 0.40, type: 'sine', gain: 0.30, attack: 0.010 }); E.tone({ freq: 800, freqEnd: 300, dur: 0.30, type: 'sine', gain: 0.20, when: 0.40, attack: 0.050 }); E.tone({ freq: 8, dur: 0.80, type: 'sine', gain: 0.10, attack: 0.010 }); } });
  KY.audio.registerPreset('witch-laugh-001', { duration: 0.50, build: function(E) { var f = [800, 950, 700, 1100, 850]; var d = [0.06, 0.08, 0.05, 0.07, 0.06]; var offset = 0; for(var i=0; i<5; i++) { E.tone({ freq: f[i], dur: d[i], type: 'square', gain: 0.25, when: offset, attack: 0.002 }); offset += d[i] + 0.02; } } });
  KY.audio.registerPreset('chains-rattle-001', { duration: 0.40, build: function(E) { for(var i=0; i<6; i++) { E.noise({ dur: 0.05, gain: 0.25, seed: 10+i, when: i*0.06, filter: { type: 'bandpass', freq: 2000 } }); } } });
  KY.audio.registerPreset('creepy-whisper-001', { duration: 0.80, build: function(E) { E.noise({ dur: 0.70, gain: 0.35, seed: 777, filter: { type: 'highpass', freq: 1500 } }); E.tone({ freq: 1200, dur: 0.70, type: 'sine', gain: 0.05, attack: 0.010 }); } });
  KY.audio.registerPreset('zombie-groan-001', { duration: 0.70, build: function(E) { E.tone({ freq: 150, freqEnd: 80, dur: 0.60, type: 'sawtooth', gain: 0.35, attack: 0.020 }); E.noise({ dur: 0.50, gain: 0.15, seed: 13, filter: { type: 'lowpass', freq: 600 } }); } });
  KY.audio.registerPreset('halloween-bell-001', { duration: 0.50, build: function(E) { E.tone({ freq: 220, dur: 0.40, type: 'triangle', gain: 0.30, attack: 0.005 }); E.tone({ freq: 233, dur: 0.40, type: 'triangle', gain: 0.25, attack: 0.005 }); } });
  KY.audio.registerPreset('pumpkin-smash-001', { duration: 0.15, build: function(E) { E.noise({ dur: 0.10, gain: 0.40, seed: 99, filter: { type: 'lowpass', freq: 800 } }); E.tone({ freq: 200, freqEnd: 50, dur: 0.10, type: 'sine', gain: 0.30, attack: 0.002 }); } });
  KY.audio.registerPreset('cauldron-bubble-001', { duration: 0.90, build: function(E) { for(var i=0; i<8; i++) { E.tone({ freq: 300 + (i*50), freqEnd: 100, dur: 0.08, type: 'sine', gain: 0.20, when: i*0.10, attack: 0.010 }); } } });
  KY.audio.registerPreset('bat-wings-flutter-001', { duration: 0.45, build: function(E) { for(var i=0; i<10; i++) { E.noise({ dur: 0.03, gain: 0.20, seed: 50+i, when: i*0.04, filter: { type: 'bandpass', freq: 800 } }); } } });
})();