(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};
  if (!KY.audio) { return; }
  KY.audio.registerPreset('epic-victory-fanfare-001', { duration: 0.80, build: function(E) { var n = [523.25, 659.25, 783.99, 1046.50]; n.forEach(function(f, i) { E.tone({ freq: f, dur: 0.20, type: 'square', gain: 0.30, when: i*0.15, attack: 0.005 }); }); } });
  KY.audio.registerPreset('epic-legendary-unlock-001', { duration: 0.70, build: function(E) { E.tone({ freq: 200, freqEnd: 2000, dur: 0.60, type: 'sawtooth', gain: 0.40, attack: 0.020 }); } });
  KY.audio.registerPreset('epic-world-reveal-001', { duration: 1.30, build: function(E) { E.tone({ freq: 100, freqEnd: 800, dur: 1.20, type: 'sine', gain: 0.30, attack: 0.100 }); E.tone({ freq: 2000, dur: 0.80, type: 'sine', gain: 0.15, when: 0.40, attack: 0.050 }); } });
  KY.audio.registerPreset('epic-power-surge-001', { duration: 0.90, build: function(E) { E.noise({ dur: 0.80, gain: 0.40, seed: 1500, filter: { type: 'lowpass', freq: 1000 } }); E.tone({ freq: 400, freqEnd: 100, dur: 0.80, type: 'square', gain: 0.30, attack: 0.010 }); } });
  KY.audio.registerPreset('epic-quest-complete-massive-001', { duration: 0.70, build: function(E) { var n = [440.0, 554.37, 659.25, 880.0, 1108.73]; n.forEach(function(f, i) { E.tone({ freq: f, dur: 0.25, type: 'triangle', gain: 0.25, when: i*0.10, attack: 0.005 }); }); } });
  KY.audio.registerPreset('epic-transcendence-001', { duration: 1.60, build: function(E) { E.tone({ freq: 300, freqEnd: 3000, dur: 1.50, type: 'sine', gain: 0.25, attack: 0.200 }); } });
  KY.audio.registerPreset('epic-artifact-awaken-001', { duration: 0.60, build: function(E) { for(var i=0; i<5; i++) { E.tone({ freq: 300+i*100, dur: 0.15, type: 'square', gain: 0.25, when: i*0.08, attack: 0.010 }); } } });
  KY.audio.registerPreset('epic-portal-destroy-001', { duration: 1.10, build: function(E) { E.tone({ freq: 2000, freqEnd: 50, dur: 1.00, type: 'sawtooth', gain: 0.50, attack: 0.050 }); E.noise({ dur: 0.50, gain: 0.30, seed: 1501, when: 0.50, filter: { type: 'lowpass', freq: 600 } }); } });
  KY.audio.registerPreset('epic-boss-defeat-001', { duration: 1.30, build: function(E) { E.noise({ dur: 1.20, gain: 0.60, seed: 1502, filter: { type: 'lowpass', freq: 400 } }); E.tone({ freq: 80, freqEnd: 20, dur: 1.20, type: 'sine', gain: 0.50, attack: 0.020 }); } });
  KY.audio.registerPreset('epic-champion-crown-001', { duration: 0.70, build: function(E) { var n = [659.25, 783.99, 987.77, 1318.51]; n.forEach(function(f, i) { E.tone({ freq: f, dur: 0.30, type: 'sine', gain: 0.20, when: i*0.12, attack: 0.010 }); }); } });
  KY.audio.registerPreset('epic-time-shatter-001', { duration: 0.50, build: function(E) { E.noise({ dur: 0.40, gain: 0.50, seed: 1503, filter: { type: 'highpass', freq: 3000 } }); E.tone({ freq: 1000, freqEnd: 200, dur: 0.40, type: 'square', gain: 0.40, attack: 0.001 }); } });
  KY.audio.registerPreset('epic-energy-overflow-001', { duration: 0.90, build: function(E) { E.tone({ freq: 100, freqEnd: 1000, dur: 0.80, type: 'sine', gain: 0.40, attack: 0.050 }); } });
  KY.audio.registerPreset('epic-ancient-awakens-001', { duration: 1.60, build: function(E) { E.tone({ freq: 50, freqEnd: 150, dur: 1.50, type: 'sawtooth', gain: 0.35, attack: 0.200 }); } });
  KY.audio.registerPreset('epic-multiverse-collapse-001', { duration: 2.20, build: function(E) { E.noise({ dur: 2.00, gain: 0.50, seed: 1504, filter: { type: 'lowpass', freq: 300 } }); } });
  KY.audio.registerPreset('epic-final-stand-001', { duration: 0.90, build: function(E) { var n = [261.63, 329.63, 392.00, 523.25, 659.25, 783.99]; n.forEach(function(f, i) { E.tone({ freq: f, dur: 0.40, type: 'sawtooth', gain: 0.20, when: i*0.10, attack: 0.010 }); }); } });
})();