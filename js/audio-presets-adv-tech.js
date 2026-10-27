(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};
  if (!KY.audio) { return; }
  KY.audio.registerPreset('tech-nanobot-swarm-001', { duration: 0.90, build: function(E) { E.noise({ dur: 0.80, gain: 0.30, seed: 1600, filter: { type: 'highpass', freq: 2000 } }); } });
  KY.audio.registerPreset('tech-antigravity-boot-001', { duration: 0.70, build: function(E) { E.tone({ freq: 100, freqEnd: 400, dur: 0.60, type: 'sine', gain: 0.30, attack: 0.050 }); } });
  KY.audio.registerPreset('tech-matter-compiler-001', { duration: 0.40, build: function(E) { for(var i=0; i<8; i++) { E.tone({ freq: 800+i*100, dur: 0.03, type: 'square', gain: 0.15, when: i*0.05, attack: 0.001 }); } } });
  KY.audio.registerPreset('tech-warp-core-init-001', { duration: 1.10, build: function(E) { E.tone({ freq: 100, freqEnd: 1500, dur: 1.00, type: 'sawtooth', gain: 0.35, attack: 0.100 }); } });
  KY.audio.registerPreset('tech-ai-uplink-001', { duration: 0.60, build: function(E) { E.tone({ freq: 2000, freqEnd: 800, dur: 0.50, type: 'sine', gain: 0.25, attack: 0.020 }); } });
  KY.audio.registerPreset('tech-hologram-deploy-001', { duration: 0.50, build: function(E) { E.noise({ dur: 0.40, gain: 0.30, seed: 1601, filter: { type: 'bandpass', freq: 1500 } }); E.tone({ freq: 1000, freqEnd: 500, dur: 0.40, type: 'square', gain: 0.20, attack: 0.010 }); } });
  KY.audio.registerPreset('tech-plasma-conduit-001', { duration: 0.70, build: function(E) { E.noise({ dur: 0.60, gain: 0.40, seed: 1602, filter: { type: 'highpass', freq: 2500 } }); } });
  KY.audio.registerPreset('tech-neural-link-001', { duration: 0.35, build: function(E) { for(var i=0; i<6; i++) { E.tone({ freq: 400+i*100, dur: 0.05, type: 'sine', gain: 0.20, when: i*0.05, attack: 0.001 }); } } });
  KY.audio.registerPreset('tech-energy-siphon-001', { duration: 0.90, build: function(E) { E.tone({ freq: 800, freqEnd: 100, dur: 0.80, type: 'sawtooth', gain: 0.35, attack: 0.050 }); } });
  KY.audio.registerPreset('tech-quantum-entangle-001', { duration: 0.60, build: function(E) { E.tone({ freq: 1000, dur: 0.10, type: 'sine', gain: 0.25, when: 0.00, attack: 0.002 }); E.tone({ freq: 1000, dur: 0.10, type: 'sine', gain: 0.25, when: 0.30, attack: 0.002 }); } });
  KY.audio.registerPreset('tech-phase-shift-001', { duration: 0.60, build: function(E) { E.tone({ freq: 400, freqEnd: 1200, dur: 0.50, type: 'square', gain: 0.30, attack: 0.010 }); } });
  KY.audio.registerPreset('tech-singularity-form-001', { duration: 1.60, build: function(E) { E.tone({ freq: 50, freqEnd: 800, dur: 1.50, type: 'sine', gain: 0.40, attack: 0.200 }); } });
  KY.audio.registerPreset('tech-cyber-terraform-001', { duration: 1.10, build: function(E) { E.noise({ dur: 1.00, gain: 0.30, seed: 1603, filter: { type: 'lowpass', freq: 800 } }); } });
  KY.audio.registerPreset('tech-drone-squadron-001', { duration: 0.50, build: function(E) { for(var i=0; i<4; i++) { E.tone({ freq: 300+i*20, dur: 0.15, type: 'sawtooth', gain: 0.20, when: i*0.10, attack: 0.010 }); } } });
  KY.audio.registerPreset('tech-system-reboot-prime-001', { duration: 0.60, build: function(E) { for(var i=0; i<5; i++) { E.tone({ freq: 200+i*200, dur: 0.10, type: 'sine', gain: 0.25, when: i*0.10, attack: 0.005 }); } } });
})();