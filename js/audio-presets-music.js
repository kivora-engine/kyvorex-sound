// audio-presets-music.js — 15 music presets
(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};
  if (!KY.audio) { return; }

  KY.audio.registerPreset('piano-single-note-001', { duration: 0.90, build: function(E) { E.tone({ freq: 440, dur: 0.80, type: 'sine', gain: 0.40, attack: 0.005 }); E.tone({ freq: 880, dur: 0.80, type: 'triangle', gain: 0.15, attack: 0.005 }); } });
  KY.audio.registerPreset('piano-chord-soft-001', { duration: 1.10, build: function(E) { var n = [261.63, 329.63, 392.00]; n.forEach(function(f) { E.tone({ freq: f, dur: 1.00, type: 'sine', gain: 0.30, attack: 0.010 }); }); } });
  KY.audio.registerPreset('music-box-melody-short-001', { duration: 0.60, build: function(E) { var n = [1046.50, 1318.51, 1567.98, 1046.50]; n.forEach(function(f, i) { E.tone({ freq: f, dur: 0.15, type: 'sine', gain: 0.25, when: i*0.15, attack: 0.002 }); }); } });
  KY.audio.registerPreset('music-box-winding-001', { duration: 0.70, build: function(E) { for(var i=0; i<8; i++) { E.noise({ dur: 0.02, gain: 0.20, seed: 200+i, when: i*0.08, filter: { type: 'highpass', freq: 2000 } }); } } });
  KY.audio.registerPreset('acoustic-guitar-strum-001', { duration: 0.50, build: function(E) { E.noise({ dur: 0.15, gain: 0.30, seed: 201, filter: { type: 'bandpass', freq: 1000 } }); E.tone({ freq: 196.00, dur: 0.40, type: 'sawtooth', gain: 0.20, when: 0.05, attack: 0.010 }); E.tone({ freq: 246.94, dur: 0.40, type: 'sawtooth', gain: 0.20, when: 0.08, attack: 0.010 }); E.tone({ freq: 293.66, dur: 0.40, type: 'sawtooth', gain: 0.20, when: 0.11, attack: 0.010 }); } });
  KY.audio.registerPreset('acoustic-guitar-pluck-001', { duration: 0.40, build: function(E) { E.noise({ dur: 0.05, gain: 0.20, seed: 202, filter: { type: 'highpass', freq: 1500 } }); E.tone({ freq: 440, dur: 0.30, type: 'sawtooth', gain: 0.30, attack: 0.005 }); } });
  KY.audio.registerPreset('electric-guitar-feedback-001', { duration: 0.90, build: function(E) { E.tone({ freq: 400, freqEnd: 1200, dur: 0.80, type: 'sawtooth', gain: 0.30, attack: 0.010 }); E.tone({ freq: 800, freqEnd: 2400, dur: 0.80, type: 'square', gain: 0.15, attack: 0.010 }); } });
  KY.audio.registerPreset('bass-guitar-slide-001', { duration: 0.70, build: function(E) { E.tone({ freq: 100, freqEnd: 50, dur: 0.60, type: 'sawtooth', gain: 0.40, attack: 0.005 }); } });
  KY.audio.registerPreset('snare-drum-roll-short-001', { duration: 0.35, build: function(E) { for(var i=0; i<10; i++) { E.noise({ dur: 0.05, gain: 0.30, seed: 203+i, when: i*0.03, filter: { type: 'bandpass', freq: 2000 } }); } } });
  KY.audio.registerPreset('cymbal-swell-001', { duration: 1.60, build: function(E) { E.noise({ dur: 1.50, gain: 0.35, seed: 204, filter: { type: 'highpass', freq: 4000 } }); } });
  KY.audio.registerPreset('triangle-instrument-hit-001', { duration: 1.10, build: function(E) { E.tone({ freq: 2500, dur: 1.00, type: 'sine', gain: 0.30, attack: 0.002 }); } });
  KY.audio.registerPreset('xylophone-run-001', { duration: 0.40, build: function(E) { var n = [1046.50, 987.77, 880.00, 783.99]; n.forEach(function(f, i) { E.tone({ freq: f, dur: 0.10, type: 'triangle', gain: 0.25, when: i*0.10, attack: 0.002 }); }); } });
  KY.audio.registerPreset('harp-glissando-short-001', { duration: 0.50, build: function(E) { E.tone({ freq: 400, freqEnd: 2000, dur: 0.40, type: 'triangle', gain: 0.25, attack: 0.005 }); } });
  KY.audio.registerPreset('orchestral-stinger-triumphant-001', { duration: 0.90, build: function(E) { var n = [261.63, 329.63, 392.00, 523.25]; n.forEach(function(f) { E.tone({ freq: f, dur: 0.80, type: 'sawtooth', gain: 0.20, attack: 0.010 }); }); } });
  KY.audio.registerPreset('orchestral-stinger-mysterious-001', { duration: 1.30, build: function(E) { var n = [220.00, 277.18, 311.13]; n.forEach(function(f) { E.tone({ freq: f, dur: 1.20, type: 'sawtooth', gain: 0.20, attack: 0.050 }); }); } });
})();