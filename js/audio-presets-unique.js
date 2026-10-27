(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};
  if (!KY.audio) { return; }
  KY.audio.registerPreset('unique-alchemy-brew-001', { duration: 0.90, build: function(E) { E.noise({ dur: 0.80, gain: 0.30, seed: 1800, filter: { type: 'lowpass', freq: 800 } }); } });
  KY.audio.registerPreset('unique-lockpick-snap-001', { duration: 0.10, build: function(E) { E.tone({ freq: 1000, dur: 0.05, type: 'square', gain: 0.30, attack: 0.001 }); } });
  KY.audio.registerPreset('unique-trap-disarm-001', { duration: 0.40, build: function(E) { E.tone({ freq: 800, freqEnd: 400, dur: 0.30, type: 'sine', gain: 0.25, attack: 0.010 }); } });
  KY.audio.registerPreset('unique-stealth-footstep-001', { duration: 0.15, build: function(E) { E.noise({ dur: 0.10, gain: 0.15, seed: 1801, filter: { type: 'lowpass', freq: 500 } }); } });
  KY.audio.registerPreset('unique-vent-crawl-001', { duration: 0.60, build: function(E) { E.noise({ dur: 0.50, gain: 0.20, seed: 1802, filter: { type: 'bandpass', freq: 600 } }); } });
  KY.audio.registerPreset('unique-wall-climb-001', { duration: 0.50, build: function(E) { E.tone({ freq: 200, freqEnd: 400, dur: 0.40, type: 'sine', gain: 0.20, attack: 0.020 }); } });
  KY.audio.registerPreset('unique-vehicle-boost-001', { duration: 0.90, build: function(E) { E.tone({ freq: 100, freqEnd: 600, dur: 0.80, type: 'sawtooth', gain: 0.35, attack: 0.050 }); } });
  KY.audio.registerPreset('unique-cyber-deck-overheat-001', { duration: 0.70, build: function(E) { E.noise({ dur: 0.60, gain: 0.40, seed: 1803, filter: { type: 'highpass', freq: 2000 } }); } });
  KY.audio.registerPreset('unique-magic-mirror-shatter-001', { duration: 0.50, build: function(E) { E.noise({ dur: 0.40, gain: 0.50, seed: 1804, filter: { type: 'highpass', freq: 4000 } }); } });
  KY.audio.registerPreset('unique-reality-glitch-short-001', { duration: 0.15, build: function(E) { E.noise({ dur: 0.10, gain: 0.40, seed: 1805, filter: { type: 'bandpass', freq: 3000 } }); E.tone({ freq: 1000, freqEnd: 200, dur: 0.10, type: 'square', gain: 0.30, attack: 0.001 }); } });
})();