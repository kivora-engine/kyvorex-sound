// audio-presets-events.js — 15 event presets
(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};
  if (!KY.audio) { return; }

  KY.audio.registerPreset('game-round-start-001', { duration: 0.25, build: function(E) { E.tone({ freq: 440, dur: 0.10, type: 'sine', gain: 0.30, when: 0.00, attack: 0.005 }); E.tone({ freq: 880, dur: 0.15, type: 'sine', gain: 0.30, when: 0.10, attack: 0.005 }); } });
  KY.audio.registerPreset('game-round-end-001', { duration: 0.25, build: function(E) { E.tone({ freq: 880, dur: 0.10, type: 'sine', gain: 0.30, when: 0.00, attack: 0.005 }); E.tone({ freq: 440, dur: 0.15, type: 'sine', gain: 0.30, when: 0.10, attack: 0.005 }); } });
  KY.audio.registerPreset('game-draw-result-001', { duration: 0.30, build: function(E) { E.tone({ freq: 600, dur: 0.15, type: 'triangle', gain: 0.30, when: 0.00, attack: 0.005 }); E.tone({ freq: 600, dur: 0.15, type: 'triangle', gain: 0.30, when: 0.20, attack: 0.005 }); } });
  KY.audio.registerPreset('game-tie-break-start-001', { duration: 0.60, build: function(E) { E.tone({ freq: 200, freqEnd: 800, dur: 0.50, type: 'sawtooth', gain: 0.30, attack: 0.010 }); } });
  KY.audio.registerPreset('game-combo-achieved-001', { duration: 0.30, build: function(E) { var n = [600, 800, 1000]; n.forEach(function(f, i) { E.tone({ freq: f, dur: 0.10, type: 'square', gain: 0.25, when: i*0.08, attack: 0.003 }); }); } });
  KY.audio.registerPreset('game-combo-break-001', { duration: 0.40, build: function(E) { E.tone({ freq: 600, freqEnd: 150, dur: 0.30, type: 'square', gain: 0.30, attack: 0.005 }); } });
  KY.audio.registerPreset('game-streak-milestone-001', { duration: 0.50, build: function(E) { var n = [440, 554, 659, 880]; n.forEach(function(f, i) { E.tone({ freq: f, dur: 0.15, type: 'sine', gain: 0.25, when: i*0.10, attack: 0.005 }); }); } });
  KY.audio.registerPreset('game-bonus-activated-001', { duration: 0.30, build: function(E) { E.tone({ freq: 800, freqEnd: 1200, dur: 0.20, type: 'sine', gain: 0.30, attack: 0.005 }); } });
  KY.audio.registerPreset('game-bonus-expired-001', { duration: 0.40, build: function(E) { E.tone({ freq: 1200, freqEnd: 400, dur: 0.30, type: 'sine', gain: 0.30, attack: 0.005 }); } });
  KY.audio.registerPreset('game-multiplier-increase-001', { duration: 0.10, build: function(E) { E.tone({ freq: 1500, dur: 0.05, type: 'sine', gain: 0.25, attack: 0.002 }); } });
  KY.audio.registerPreset('game-multiplier-reset-001', { duration: 0.20, build: function(E) { E.tone({ freq: 300, dur: 0.15, type: 'sine', gain: 0.30, attack: 0.005 }); } });
  KY.audio.registerPreset('game-target-locked-001', { duration: 0.12, build: function(E) { E.tone({ freq: 1000, dur: 0.08, type: 'square', gain: 0.25, attack: 0.002 }); } });
  KY.audio.registerPreset('game-target-lost-001', { duration: 0.25, build: function(E) { E.tone({ freq: 1000, freqEnd: 600, dur: 0.20, type: 'sine', gain: 0.30, attack: 0.005 }); } });
  KY.audio.registerPreset('game-wave-cleared-001', { duration: 0.40, build: function(E) { E.tone({ freq: 523.25, dur: 0.15, type: 'triangle', gain: 0.30, when: 0.00, attack: 0.005 }); E.tone({ freq: 783.99, dur: 0.25, type: 'triangle', gain: 0.30, when: 0.15, attack: 0.005 }); } });
  KY.audio.registerPreset('game-final-result-reveal-001', { duration: 1.00, build: function(E) { E.tone({ freq: 100, freqEnd: 400, dur: 0.80, type: 'sawtooth', gain: 0.30, attack: 0.050 }); } });
})();