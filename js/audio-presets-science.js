(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};
  if (!KY.audio) { return; }
  KY.audio.registerPreset('lab-microscope-focus-001', { duration: 0.15, build: function(E) { E.noise({ dur: 0.10, gain: 0.15, seed: 400, filter: { type: 'highpass', freq: 2000 } }); } });
  KY.audio.registerPreset('lab-centrifuge-start-001', { duration: 1.00, build: function(E) { E.tone({ freq: 100, freqEnd: 400, dur: 0.80, type: 'sawtooth', gain: 0.25, attack: 0.050 }); } });
  KY.audio.registerPreset('lab-centrifuge-stop-001', { duration: 1.20, build: function(E) { E.tone({ freq: 400, freqEnd: 50, dur: 1.00, type: 'sawtooth', gain: 0.25, attack: 0.020 }); } });
  KY.audio.registerPreset('lab-test-tube-rack-001', { duration: 0.08, build: function(E) { E.tone({ freq: 800, dur: 0.05, type: 'sine', gain: 0.25, when: 0.00, attack: 0.001 }); E.tone({ freq: 1200, dur: 0.05, type: 'sine', gain: 0.20, when: 0.04, attack: 0.001 }); } });
  KY.audio.registerPreset('lab-glass-stirring-001', { duration: 0.70, build: function(E) { E.noise({ dur: 0.60, gain: 0.20, seed: 401, filter: { type: 'bandpass', freq: 1500 } }); } });
  KY.audio.registerPreset('lab-liquid-dispense-001', { duration: 0.30, build: function(E) { E.tone({ freq: 600, freqEnd: 300, dur: 0.20, type: 'sine', gain: 0.25, attack: 0.005 }); } });
  KY.audio.registerPreset('lab-pipette-release-001', { duration: 0.10, build: function(E) { E.tone({ freq: 1500, dur: 0.05, type: 'sine', gain: 0.20, attack: 0.001 }); } });
  KY.audio.registerPreset('lab-sample-vial-seal-001', { duration: 0.10, build: function(E) { E.tone({ freq: 400, dur: 0.05, type: 'square', gain: 0.20, attack: 0.001 }); E.noise({ dur: 0.03, gain: 0.15, seed: 402, filter: { type: 'lowpass', freq: 1000 } }); } });
  KY.audio.registerPreset('lab-chemical-reaction-fizz-001', { duration: 1.00, build: function(E) { E.noise({ dur: 0.80, gain: 0.35, seed: 403, filter: { type: 'highpass', freq: 3000 } }); } });
  KY.audio.registerPreset('lab-vacuum-pump-cycle-001', { duration: 0.50, build: function(E) { E.tone({ freq: 150, dur: 0.40, type: 'square', gain: 0.25, when: 0.00, attack: 0.010 }); E.tone({ freq: 150, dur: 0.40, type: 'square', gain: 0.25, when: 0.50, attack: 0.010 }); } });
  KY.audio.registerPreset('lab-spectrometer-scan-001', { duration: 0.60, build: function(E) { E.tone({ freq: 200, freqEnd: 1500, dur: 0.50, type: 'sine', gain: 0.20, attack: 0.010 }); } });
  KY.audio.registerPreset('lab-electron-microscope-pulse-001', { duration: 0.05, build: function(E) { E.tone({ freq: 2000, dur: 0.03, type: 'square', gain: 0.20, when: 0.00, attack: 0.001 }); E.tone({ freq: 2000, dur: 0.03, type: 'square', gain: 0.20, when: 0.10, attack: 0.001 }); } });
  KY.audio.registerPreset('lab-radiation-counter-burst-001', { duration: 0.30, build: function(E) { for(var i=0; i<5; i++) { E.noise({ dur: 0.01, gain: 0.30, seed: 404+i, when: i*0.05, filter: { type: 'highpass', freq: 4000 } }); } } });
  KY.audio.registerPreset('lab-cryo-chamber-cycle-001', { duration: 0.70, build: function(E) { E.tone({ freq: 800, freqEnd: 200, dur: 0.60, type: 'sine', gain: 0.25, attack: 0.050 }); } });
  KY.audio.registerPreset('lab-experiment-complete-001', { duration: 0.40, build: function(E) { var n = [523.25, 659.25, 783.99]; n.forEach(function(f, i) { E.tone({ freq: f, dur: 0.20, type: 'sine', gain: 0.25, when: i*0.1, attack: 0.005 }); }); } });
})();