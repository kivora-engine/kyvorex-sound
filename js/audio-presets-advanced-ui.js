(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};
  if (!KY.audio) { return; }
  KY.audio.registerPreset('ui-tab-switch-002', { duration: 0.08, build: function(E) { E.tone({ freq: 600, dur: 0.03, type: 'triangle', gain: 0.20, when: 0.00, attack: 0.001 }); E.tone({ freq: 800, dur: 0.03, type: 'triangle', gain: 0.20, when: 0.04, attack: 0.001 }); } });
  KY.audio.registerPreset('ui-panel-expand-001', { duration: 0.25, build: function(E) { E.tone({ freq: 300, freqEnd: 600, dur: 0.20, type: 'sine', gain: 0.20, attack: 0.005 }); } });
  KY.audio.registerPreset('ui-panel-collapse-001', { duration: 0.25, build: function(E) { E.tone({ freq: 600, freqEnd: 300, dur: 0.20, type: 'sine', gain: 0.20, attack: 0.005 }); } });
  KY.audio.registerPreset('ui-toggle-on-001', { duration: 0.08, build: function(E) { E.tone({ freq: 1000, dur: 0.05, type: 'sine', gain: 0.25, attack: 0.001 }); } });
  KY.audio.registerPreset('ui-toggle-off-001', { duration: 0.08, build: function(E) { E.tone({ freq: 600, dur: 0.05, type: 'sine', gain: 0.25, attack: 0.001 }); } });
  KY.audio.registerPreset('ui-slider-adjust-001', { duration: 0.04, build: function(E) { E.tone({ freq: 2000, dur: 0.02, type: 'square', gain: 0.15, attack: 0.001 }); } });
  KY.audio.registerPreset('ui-drag-drop-002', { duration: 0.10, build: function(E) { E.tone({ freq: 400, dur: 0.05, type: 'sine', gain: 0.20, attack: 0.002 }); E.noise({ dur: 0.03, gain: 0.15, seed: 500, filter: { type: 'lowpass', freq: 800 } }); } });
  KY.audio.registerPreset('ui-file-import-001', { duration: 0.15, build: function(E) { E.tone({ freq: 800, dur: 0.08, type: 'triangle', gain: 0.20, when: 0.00, attack: 0.002 }); E.tone({ freq: 1200, dur: 0.10, type: 'triangle', gain: 0.20, when: 0.08, attack: 0.002 }); } });
  KY.audio.registerPreset('ui-file-export-001', { duration: 0.15, build: function(E) { E.tone({ freq: 1200, dur: 0.08, type: 'triangle', gain: 0.20, when: 0.00, attack: 0.002 }); E.tone({ freq: 800, dur: 0.10, type: 'triangle', gain: 0.20, when: 0.08, attack: 0.002 }); } });
  KY.audio.registerPreset('ui-sync-start-001', { duration: 0.40, build: function(E) { E.tone({ freq: 400, freqEnd: 800, dur: 0.30, type: 'sine', gain: 0.20, attack: 0.010 }); } });
  KY.audio.registerPreset('ui-sync-complete-001', { duration: 0.30, build: function(E) { var n = [523.25, 659.25, 880.00]; n.forEach(function(f, i) { E.tone({ freq: f, dur: 0.10, type: 'sine', gain: 0.20, when: i*0.1, attack: 0.005 }); }); } });
  KY.audio.registerPreset('ui-connection-established-001', { duration: 0.10, build: function(E) { E.tone({ freq: 880, dur: 0.05, type: 'sine', gain: 0.25, when: 0.00, attack: 0.002 }); E.tone({ freq: 1320, dur: 0.08, type: 'sine', gain: 0.25, when: 0.05, attack: 0.002 }); } });
  KY.audio.registerPreset('ui-connection-lost-001', { duration: 0.20, build: function(E) { E.tone({ freq: 400, dur: 0.15, type: 'sawtooth', gain: 0.25, attack: 0.005 }); } });
  KY.audio.registerPreset('ui-data-processing-001', { duration: 0.35, build: function(E) { for(var i=0; i<4; i++) { E.tone({ freq: 1500, dur: 0.02, type: 'square', gain: 0.15, when: i*0.08, attack: 0.001 }); } } });
  KY.audio.registerPreset('ui-permission-granted-001', { duration: 0.20, build: function(E) { E.tone({ freq: 1046.50, dur: 0.10, type: 'sine', gain: 0.25, when: 0.00, attack: 0.002 }); E.tone({ freq: 1318.51, dur: 0.15, type: 'sine', gain: 0.25, when: 0.10, attack: 0.002 }); } });
})();