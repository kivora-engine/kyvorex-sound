// wav-renderer.js — internal offline render + PCM WAV encoder.
//
// NOTE: this module is NOT used for public downloads. Public WAV/MP3
// downloads use real static files served from audio/wav/ and audio/mp3/
// via native <a href download> anchors.
//
// This module exists only for internal/offline rendering utilities.
// It intentionally does NOT expose any function that triggers a
// browser download.
(function () {
  'use strict';
  var KY = window.KYVOREX = window.KYVOREX || {};

  /* ---------- WAV PCM 16-bit encoder ---------- */
  function encodeWav(audioBuffer) {
    var numCh = audioBuffer.numberOfChannels;
    var sr = audioBuffer.sampleRate;
    var len = audioBuffer.length;
    var bytesPerSample = 2;
    var blockAlign = numCh * bytesPerSample;
    var dataSize = len * blockAlign;
    var arrBuf = new ArrayBuffer(44 + dataSize);
    var view = new DataView(arrBuf);

    function writeStr(offset, str) {
      for (var i = 0; i < str.length; i++) {
        view.setUint8(offset + i, str.charCodeAt(i));
      }
    }

    writeStr(0, 'RIFF');
    view.setUint32(4, 36 + dataSize, true);
    writeStr(8, 'WAVE');
    writeStr(12, 'fmt ');
    view.setUint32(16, 16, true);
    view.setUint16(20, 1, true);
    view.setUint16(22, numCh, true);
    view.setUint32(24, sr, true);
    view.setUint32(28, sr * blockAlign, true);
    view.setUint16(32, blockAlign, true);
    view.setUint16(34, 16, true);
    writeStr(36, 'data');
    view.setUint32(40, dataSize, true);

    var channels = [];
    for (var ch = 0; ch < numCh; ch++) {
      channels.push(audioBuffer.getChannelData(ch));
    }

    var offset = 44;
    for (var i = 0; i < len; i++) {
      for (var c = 0; c < numCh; c++) {
        var s = channels[c][i];
        if (s > 1) s = 1;
        else if (s < -1) s = -1;
        view.setInt16(offset, s < 0 ? s * 0x8000 : s * 0x7fff, true);
        offset += 2;
      }
    }
    return new Blob([arrBuf], { type: 'audio/wav' });
  }

  /* ---------- offline rendering (internal utility only) ---------- */
  function renderPreset(id) {
    var preset = KY.audio.getPreset(id);
    if (!preset) {
      console.error('[KYVOREX WAV] preset not found:', id);
      return Promise.reject(new Error('Preset not found: ' + id));
    }

    var OAC = window.OfflineAudioContext || window.webkitOfflineAudioContext;
    if (!OAC) {
      return Promise.reject(new Error('OfflineAudioContext not supported'));
    }

    var sr = 44100;
    var length = Math.ceil((preset.duration + 0.1) * sr);
    var oac = new OAC(1, length, sr);

    try {
      var builder = KY.audio.makeBuilder(oac, oac.destination, 0);
      preset.build(builder);
    } catch (e) {
      console.error('[KYVOREX WAV] build failed:', id, e);
      return Promise.reject(e);
    }

    return oac.startRendering();
  }

  KY.wav = {
    encodeWav: encodeWav,
    renderPreset: renderPreset
    // NOTE: no download() function. Public downloads are static files.
  };
})();