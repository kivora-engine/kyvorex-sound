// audio-engine.js — procedural sound engine (Web Audio API)
(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};

  var ctx = null;
  var masterGain = null;
  var presets = {};
  var activeNodes = [];
  var activeId = null;
  var activeEndAt = 0;
  var activeTimer = null;
  var listeners = { start: [], stop: [], error: [] };

  /* ---------- context ---------- */
  function getContext() {
    if (ctx) return ctx;
    var AC = window.AudioContext || window.webkitAudioContext;
    if (!AC) throw new Error('Web Audio API not supported');
    ctx = new AC();
    masterGain = ctx.createGain();
    masterGain.gain.value = 1.0;
    masterGain.connect(ctx.destination);
    return ctx;
  }

  function resumeContext() {
    var c = getContext();
    if (c.state === 'suspended') {
      return c.resume().catch(function (e) {
        console.error('[KYVOREX AUDIO] resume failed:', e);
        throw e;
      });
    }
    return Promise.resolve();
  }

  /* ---------- presets registry ---------- */
  function registerPreset(id, def) {
    if (!def || typeof def.build !== 'function') {
      console.error('[KYVOREX AUDIO] invalid preset:', id);
      return;
    }
    presets[id] = {
      duration: typeof def.duration === 'number' ? def.duration : 0.5,
      build: def.build
    };
  }

  function getPreset(id) { return presets[id] || null; }
  function listPresets() { return Object.keys(presets); }

  /* ---------- low-level building blocks ---------- */
  function tone(c, dest, o) {
    var when = o.when || 0;
    var dur = o.dur || 0.1;
    var osc = c.createOscillator();
    osc.type = o.type || 'sine';
    var f0 = o.freq || 440;
    osc.frequency.setValueAtTime(f0, when);
    if (o.freqEnd != null) {
      osc.frequency.exponentialRampToValueAtTime(Math.max(1, o.freqEnd), when + dur);
    }
    var g = c.createGain();
    var peak = o.gain != null ? o.gain : 0.4;
    var atk = o.attack != null ? o.attack : 0.005;
    g.gain.setValueAtTime(0.0001, when);
    g.gain.exponentialRampToValueAtTime(peak, when + atk);
    g.gain.exponentialRampToValueAtTime(0.0001, when + dur);
    osc.connect(g);
    g.connect(dest);
    osc.start(when);
    osc.stop(when + dur + 0.02);
    trackNode(osc);
    return osc;
  }

  function noise(c, dest, o) {
    var when = o.when || 0;
    var dur = o.dur || 0.2;
    var sr = c.sampleRate;
    var len = Math.max(1, Math.floor(dur * sr));
    var buf = c.createBuffer(1, len, sr);
    var data = buf.getChannelData(0);
    var seed = (o.seed || 1) >>> 0;
    for (var i = 0; i < len; i++) {
      seed = (seed * 1664525 + 1013904223) >>> 0;
      data[i] = (seed / 4294967295) * 2 - 1;
    }
    var src = c.createBufferSource();
    src.buffer = buf;
    var g = c.createGain();
    var peak = o.gain != null ? o.gain : 0.35;
    var atk = o.attack != null ? o.attack : 0.001;
    g.gain.setValueAtTime(0.0001, when);
    g.gain.exponentialRampToValueAtTime(peak, when + atk);
    g.gain.exponentialRampToValueAtTime(0.0001, when + dur);
    var head = src;
    if (o.filter) {
      var f = c.createBiquadFilter();
      f.type = o.filter.type || 'lowpass';
      f.frequency.value = o.filter.freq || 1500;
      src.connect(f);
      head = f;
    }
    head.connect(g);
    g.connect(dest);
    src.start(when);
    src.stop(when + dur + 0.02);
    trackNode(src);
    return src;
  }

  var tracking = false;
  function trackNode(n) { if (tracking) activeNodes.push(n); }

  function makeBuilder(c, dest, base) {
    return {
      tone: function (o) {
        o = o || {};
        o.when = (o.when || 0) + base;
        return tone(c, dest, o);
      },
      noise: function (o) {
        o = o || {};
        o.when = (o.when || 0) + base;
        return noise(c, dest, o);
      }
    };
  }

  /* ---------- events ---------- */
  function on(evt, cb) { if (listeners[evt]) listeners[evt].push(cb); }
  function emit(evt, data) {
    (listeners[evt] || []).forEach(function (cb) {
      try { cb(data); } catch (e) { console.error('[KYVOREX AUDIO] listener error:', e); }
    });
  }

  /* ---------- playback ---------- */
  function clearActive() {
    activeNodes.forEach(function (n) {
      try { n.stop(0); } catch (e) {}
    });
    activeNodes = [];
    activeId = null;
    activeEndAt = 0;
    if (activeTimer) { clearTimeout(activeTimer); activeTimer = null; }
  }

  function playPreset(id) {
    var p = presets[id];
    if (!p) {
      console.error('[KYVOREX AUDIO] preset not found:', id);
      emit('error', { id: id, message: 'Preset not found' });
      return Promise.reject(new Error('Preset not found: ' + id));
    }
    return resumeContext().then(function () {
      var wasPlaying = activeId;
      clearActive();
      if (wasPlaying) emit('stop', { id: wasPlaying, ended: false });

      var c = getContext();
      var when = c.currentTime + 0.03;
      tracking = true;
      try {
        p.build(makeBuilder(c, masterGain, when));
      } catch (e) {
        console.error('[KYVOREX AUDIO] build failed:', id, e);
        tracking = false;
        clearActive();
        emit('error', { id: id, message: 'Build failed' });
        return Promise.reject(e);
      }
      tracking = false;

      activeId = id;
      activeEndAt = when + p.duration;
      emit('start', { id: id, duration: p.duration });

      var ms = Math.max(80, (activeEndAt - c.currentTime) * 1000 + 60);
      activeTimer = setTimeout(function () {
        if (activeId === id) {
          var ended = activeId;
          clearActive();
          emit('stop', { id: ended, ended: true });
        }
      }, ms);
      return { id: id, duration: p.duration };
    });
  }

  function stop() {
    if (!activeId) return;
    var id = activeId;
    clearActive();
    emit('stop', { id: id, ended: false });
  }

  /* ---------- public API ---------- */
  KY.audio = {
    getContext: getContext,
    resumeContext: resumeContext,
    registerPreset: registerPreset,
    getPreset: getPreset,
    listPresets: listPresets,
    playPreset: playPreset,
    stop: stop,
    on: on,
    isPlaying: function () { return !!activeId; },
    currentId: function () { return activeId; },
    tone: tone,
    noise: noise,
    makeBuilder: makeBuilder
  };
})();