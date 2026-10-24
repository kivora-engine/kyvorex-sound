// audio-presets-board.js — 15 board game presets
(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};
  if (!KY.audio) { return; }

  KY.audio.registerPreset('chess-piece-place-001', { duration: 0.10, build: function(E) { E.noise({ dur: 0.05, gain: 0.30, seed: 301, filter: { type: 'lowpass', freq: 600 } }); E.tone({ freq: 150, dur: 0.08, type: 'sine', gain: 0.30, attack: 0.002 }); } });
  KY.audio.registerPreset('chess-clock-press-001', { duration: 0.05, build: function(E) { E.tone({ freq: 800, dur: 0.03, type: 'square', gain: 0.25, when: 0.00, attack: 0.001 }); E.tone({ freq: 600, dur: 0.03, type: 'square', gain: 0.25, when: 0.04, attack: 0.001 }); } });
  KY.audio.registerPreset('dice-single-roll-001', { duration: 0.40, build: function(E) { E.noise({ dur: 0.05, gain: 0.30, seed: 302, when: 0.00, filter: { type: 'bandpass', freq: 2000 } }); E.noise({ dur: 0.05, gain: 0.25, seed: 303, when: 0.15, filter: { type: 'bandpass', freq: 2000 } }); E.noise({ dur: 0.05, gain: 0.20, seed: 304, when: 0.30, filter: { type: 'bandpass', freq: 2000 } }); } });
  KY.audio.registerPreset('dice-cup-shake-001', { duration: 0.45, build: function(E) { for(var i=0; i<10; i++) { E.noise({ dur: 0.03, gain: 0.25, seed: 305+i, when: i*0.04, filter: { type: 'highpass', freq: 1500 } }); } } });
  KY.audio.registerPreset('playing-cards-shuffle-001', { duration: 1.10, build: function(E) { E.noise({ dur: 1.00, gain: 0.30, seed: 306, filter: { type: 'highpass', freq: 3000 } }); } });
  KY.audio.registerPreset('playing-card-deal-001', { duration: 0.15, build: function(E) { E.noise({ dur: 0.10, gain: 0.25, seed: 307, filter: { type: 'bandpass', freq: 2500 } }); } });
  KY.audio.registerPreset('playing-card-flip-001', { duration: 0.08, build: function(E) { E.noise({ dur: 0.05, gain: 0.30, seed: 308, filter: { type: 'highpass', freq: 4000 } }); } });
  KY.audio.registerPreset('coin-flip-table-001', { duration: 0.30, build: function(E) { E.tone({ freq: 1200, dur: 0.10, type: 'sine', gain: 0.25, when: 0.00, attack: 0.002 }); E.noise({ dur: 0.05, gain: 0.20, seed: 309, when: 0.20, filter: { type: 'bandpass', freq: 3000 } }); } });
  KY.audio.registerPreset('domino-tile-place-001', { duration: 0.08, build: function(E) { E.noise({ dur: 0.03, gain: 0.35, seed: 310, filter: { type: 'highpass', freq: 2000 } }); E.tone({ freq: 400, dur: 0.03, type: 'square', gain: 0.20, attack: 0.001 }); } });
  KY.audio.registerPreset('domino-chain-fall-001', { duration: 0.50, build: function(E) { for(var i=0; i<8; i++) { E.noise({ dur: 0.02, gain: 0.25, seed: 311+i, when: i*0.06, filter: { type: 'highpass', freq: 2000 } }); } } });
  KY.audio.registerPreset('board-game-token-move-001', { duration: 0.20, build: function(E) { E.noise({ dur: 0.15, gain: 0.15, seed: 312, filter: { type: 'bandpass', freq: 1000 } }); } });
  KY.audio.registerPreset('board-game-piece-stack-001', { duration: 0.15, build: function(E) { E.tone({ freq: 300, dur: 0.05, type: 'sine', gain: 0.25, when: 0.00, attack: 0.002 }); E.tone({ freq: 350, dur: 0.05, type: 'sine', gain: 0.25, when: 0.08, attack: 0.002 }); } });
  KY.audio.registerPreset('poker-chip-stack-001', { duration: 0.10, build: function(E) { E.noise({ dur: 0.04, gain: 0.30, seed: 313, filter: { type: 'highpass', freq: 1500 } }); E.tone({ freq: 600, dur: 0.03, type: 'square', gain: 0.20, attack: 0.001 }); } });
  KY.audio.registerPreset('poker-chip-slide-001', { duration: 0.25, build: function(E) { E.noise({ dur: 0.20, gain: 0.20, seed: 314, filter: { type: 'bandpass', freq: 800 } }); } });
  KY.audio.registerPreset('game-timer-expire-001', { duration: 0.60, build: function(E) { E.tone({ freq: 200, dur: 0.50, type: 'square', gain: 0.35, attack: 0.005 }); } });
})();