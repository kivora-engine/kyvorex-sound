(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};
  if (!KY.audio) { return; }
  KY.audio.registerPreset('env-aurora-borealis-001', { duration: 2.20, build: function(E) { E.tone({ freq: 200, freqEnd: 800, dur: 2.00, type: 'sine', gain: 0.20, attack: 0.200 }); } });
  KY.audio.registerPreset('env-geyser-mini-001', { duration: 0.50, build: function(E) { E.noise({ dur: 0.40, gain: 0.30, seed: 1700, filter: { type: 'highpass', freq: 1500 } }); } });
  KY.audio.registerPreset('env-crystal-cave-hum-001', { duration: 1.60, build: function(E) { E.tone({ freq: 120, dur: 1.50, type: 'sine', gain: 0.25, attack: 0.100 }); } });
  KY.audio.registerPreset('env-floating-islands-001', { duration: 2.20, build: function(E) { E.tone({ freq: 80, dur: 2.00, type: 'sine', gain: 0.20, attack: 0.200 }); } });
  KY.audio.registerPreset('env-meteor-shower-distant-001', { duration: 1.30, build: function(E) { E.noise({ dur: 1.20, gain: 0.20, seed: 1701, filter: { type: 'lowpass', freq: 400 } }); } });
  KY.audio.registerPreset('env-swamp-gas-bubble-001', { duration: 0.40, build: function(E) { E.tone({ freq: 100, freqEnd: 50, dur: 0.30, type: 'sine', gain: 0.30, attack: 0.020 }); } });
  KY.audio.registerPreset('env-desert-mirage-shimmer-001', { duration: 1.60, build: function(E) { E.tone({ freq: 3000, dur: 1.50, type: 'sine', gain: 0.10, attack: 0.200 }); } });
  KY.audio.registerPreset('env-frozen-lake-crack-001', { duration: 0.25, build: function(E) { E.noise({ dur: 0.20, gain: 0.50, seed: 1702, filter: { type: 'bandpass', freq: 2000 } }); } });
  KY.audio.registerPreset('env-volcanic-lightning-001', { duration: 0.40, build: function(E) { E.noise({ dur: 0.30, gain: 0.60, seed: 1703, filter: { type: 'highpass', freq: 1000 } }); } });
  KY.audio.registerPreset('env-bioluminescent-forest-001', { duration: 1.60, build: function(E) { E.noise({ dur: 1.50, gain: 0.15, seed: 1704, filter: { type: 'highpass', freq: 3000 } }); } });
  KY.audio.registerPreset('env-sandstorm-distant-001', { duration: 2.20, build: function(E) { E.noise({ dur: 2.00, gain: 0.30, seed: 1705, filter: { type: 'lowpass', freq: 600 } }); } });
  KY.audio.registerPreset('env-waterfall-misty-001', { duration: 1.60, build: function(E) { E.noise({ dur: 1.50, gain: 0.40, seed: 1706, filter: { type: 'lowpass', freq: 1200 } }); } });
  KY.audio.registerPreset('env-magnetic-anomaly-001', { duration: 1.10, build: function(E) { E.tone({ freq: 200, freqEnd: 400, dur: 1.00, type: 'square', gain: 0.20, attack: 0.100 }); } });
  KY.audio.registerPreset('env-gravity-well-pulse-001', { duration: 0.90, build: function(E) { E.tone({ freq: 100, freqEnd: 40, dur: 0.80, type: 'sine', gain: 0.40, attack: 0.050 }); } });
  KY.audio.registerPreset('env-solar-flare-wind-001', { duration: 1.60, build: function(E) { E.noise({ dur: 1.50, gain: 0.35, seed: 1707, filter: { type: 'bandpass', freq: 1000 } }); } });
})();