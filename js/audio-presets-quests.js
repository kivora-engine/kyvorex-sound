// audio-presets-quests.js — 15 quest & reward sound presets
(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};
  if (!KY.audio) { return; }

  KY.audio.registerPreset('quest-accepted-002', { duration: 0.35, build: function(E) { E.tone({ freq: 600, dur: 0.10, type: 'sine', gain: 0.30, when: 0.00, attack: 0.004 }); E.tone({ freq: 900, dur: 0.12, type: 'sine', gain: 0.28, when: 0.10, attack: 0.004 }); } });
  KY.audio.registerPreset('quest-completed-001', { duration: 0.60, build: function(E) { var n = [523.25, 659.25, 783.99, 1046.50]; n.forEach(function(f, i) { E.tone({ freq: f, dur: 0.15, type: 'triangle', gain: 0.30, when: i * 0.1, attack: 0.005 }); }); } });
  KY.audio.registerPreset('quest-failed-001', { duration: 0.50, build: function(E) { E.tone({ freq: 300, dur: 0.20, type: 'sawtooth', gain: 0.35, when: 0.00, attack: 0.005 }); E.tone({ freq: 200, dur: 0.25, type: 'sawtooth', gain: 0.35, when: 0.20, attack: 0.005 }); } });
  KY.audio.registerPreset('inventory-open-001', { duration: 0.15, build: function(E) { E.tone({ freq: 400, dur: 0.08, type: 'triangle', gain: 0.25, when: 0.00, attack: 0.002 }); E.tone({ freq: 800, dur: 0.06, type: 'triangle', gain: 0.25, when: 0.08, attack: 0.002 }); } });
  KY.audio.registerPreset('inventory-close-001', { duration: 0.15, build: function(E) { E.tone({ freq: 800, dur: 0.08, type: 'triangle', gain: 0.25, when: 0.00, attack: 0.002 }); E.tone({ freq: 400, dur: 0.06, type: 'triangle', gain: 0.25, when: 0.08, attack: 0.002 }); } });
  KY.audio.registerPreset('item-pickup-rare-001', { duration: 0.50, build: function(E) { var n = [880, 1108.73, 1318.51]; n.forEach(function(f, i) { E.tone({ freq: f, dur: 0.20, type: 'sine', gain: 0.25, when: i * 0.1, attack: 0.005 }); }); } });
  KY.audio.registerPreset('item-drop-wood-001', { duration: 0.15, build: function(E) { E.noise({ dur: 0.08, gain: 0.30, seed: 109, filter: { type: 'bandpass', freq: 800 } }); E.tone({ freq: 150, dur: 0.05, type: 'square', gain: 0.20, attack: 0.002 }); } });
  KY.audio.registerPreset('key-item-unlock-001', { duration: 0.20, build: function(E) { E.tone({ freq: 1200, dur: 0.05, type: 'sine', gain: 0.20, when: 0.00, attack: 0.002 }); E.tone({ freq: 1600, dur: 0.10, type: 'sine', gain: 0.25, when: 0.05, attack: 0.003 }); } });
  KY.audio.registerPreset('treasure-chest-open-001', { duration: 0.30, build: function(E) { E.noise({ dur: 0.15, gain: 0.25, seed: 110, filter: { type: 'lowpass', freq: 1000 } }); E.tone({ freq: 300, dur: 0.20, type: 'triangle', gain: 0.30, when: 0.10, attack: 0.005 }); } });
  KY.audio.registerPreset('treasure-chest-close-001', { duration: 0.20, build: function(E) { E.noise({ dur: 0.10, gain: 0.25, seed: 111, filter: { type: 'lowpass', freq: 600 } }); E.tone({ freq: 200, dur: 0.10, type: 'square', gain: 0.30, when: 0.05, attack: 0.002 }); } });
  KY.audio.registerPreset('secret-discovered-001', { duration: 0.60, build: function(E) { E.tone({ freq: 200, freqEnd: 800, dur: 0.50, type: 'sine', gain: 0.25, attack: 0.010 }); E.tone({ freq: 1200, dur: 0.15, type: 'triangle', gain: 0.20, when: 0.40, attack: 0.005 }); } });
  KY.audio.registerPreset('level-up-002', { duration: 0.60, build: function(E) { var n = [440, 554.37, 659.25, 880, 1108.73]; n.forEach(function(f, i) { E.tone({ freq: f, dur: 0.12, type: 'square', gain: 0.25, when: i * 0.08, attack: 0.003 }); }); } });
  KY.audio.registerPreset('experience-gain-001', { duration: 0.12, build: function(E) { E.tone({ freq: 1500, dur: 0.10, type: 'sine', gain: 0.15, attack: 0.002 }); } });
  KY.audio.registerPreset('achievement-unlocked-001', { duration: 0.60, build: function(E) { var n = [523.25, 659.25, 783.99, 1046.50]; n.forEach(function(f, i) { E.tone({ freq: f, dur: 0.15, type: 'square', gain: 0.28, when: i * 0.1, attack: 0.004 }); }); } });
  KY.audio.registerPreset('save-checkpoint-001', { duration: 0.30, build: function(E) { E.tone({ freq: 600, dur: 0.10, type: 'sine', gain: 0.30, when: 0.00, attack: 0.005 }); E.tone({ freq: 900, dur: 0.15, type: 'sine', gain: 0.25, when: 0.10, attack: 0.005 }); } });
})();