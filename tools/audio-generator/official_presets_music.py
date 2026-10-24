"""Mission 3 - Music & Instruments (15 sounds)."""
import math
from synthesis import sine, square, triangle, sawtooth, white_noise, DEFAULT_SAMPLE_RATE

SR = DEFAULT_SAMPLE_RATE

def _wave_sample(wave_type, phase):
    ph = (phase / (2.0 * math.pi)) % 1.0
    if wave_type == 'sine': return math.sin(phase)
    if wave_type == 'square': return 1.0 if ph < 0.5 else -1.0
    if wave_type == 'triangle': return 4.0 * abs(ph - 0.5) - 1.0
    if wave_type == 'sawtooth': return 2.0 * ph - 1.0
    return 0.0

def _env_exp(n, attack):
    n_atk = max(1, int(attack * SR))
    if n_atk > n: n_atk = n
    out = []
    for i in range(n):
        if i < n_atk: out.append(i / float(n_atk))
        else:
            t = (i - n_atk) / float(max(1, n - n_atk))
            out.append(0.0001 ** t)
    return out

def _tone(wave_type, freq, dur, amplitude, attack):
    n = int(dur * SR)
    if n <= 0: return []
    env = _env_exp(n, attack)
    return [amplitude * _wave_sample(wave_type, 2.0 * math.pi * freq * i / SR) * env[i] for i in range(n)]

def _sweep(wave_type, f0, f1, dur, amplitude, attack):
    n = int(dur * SR)
    if n <= 0: return []
    env = _env_exp(n, attack)
    out = []
    phase = 0.0
    for i in range(n):
        t = i / float(max(1, n - 1))
        f = f0 * ((f1 / f0) ** t)
        phase += 2.0 * math.pi * f / SR
        out.append(amplitude * _wave_sample(wave_type, phase) * env[i])
    return out

def _noise(dur, amplitude, attack, seed=1):
    n = int(dur * SR)
    if n <= 0: return []
    env = _env_exp(n, attack)
    raw = white_noise(dur, SR, amplitude, seed=seed)
    out = [raw[i] * env[i] for i in range(min(n, len(raw)))]
    if len(out) < n: out.extend([0.0] * (n - len(out)))
    return out

def _mix(*parts):
    n = max((len(p) for p in parts), default=0)
    out = [0.0] * n
    for p in parts:
        for i in range(len(p)): out[i] += p[i]
    return out

def _at(samples, offset_sec, total_sec):
    n_total = int(total_sec * SR)
    n_off = int(offset_sec * SR)
    out = [0.0] * n_total
    for i, s in enumerate(samples):
        idx = n_off + i
        if idx < n_total: out[idx] += s
    return out

def _pad(samples, total_sec):
    n = int(total_sec * SR)
    if len(samples) < n: return samples + [0.0] * (n - len(samples))
    return samples[:n]

def _finalize(samples):
    peak = max((abs(s) for s in samples), default=0.0)
    if peak == 0.0: return samples
    target = 0.85
    factor = target / peak if peak > target else 1.0
    return [s * factor for s in samples]

def piano_single_note_001():
    a = _at(_tone('sine', 440.0, 0.80, 0.40, 0.005), 0.00, 0.90)
    b = _at(_tone('triangle', 880.0, 0.80, 0.15, 0.005), 0.00, 0.90)
    return _finalize(_mix(a, b))

def piano_chord_soft_001():
    a = _at(_tone('sine', 261.63, 1.00, 0.30, 0.010), 0.00, 1.10)
    b = _at(_tone('sine', 329.63, 1.00, 0.30, 0.010), 0.00, 1.10)
    c = _at(_tone('sine', 392.00, 1.00, 0.30, 0.010), 0.00, 1.10)
    return _finalize(_mix(a, b, c))

def music_box_melody_short_001():
    notes = [(1046.50, 0.0), (1318.51, 0.15), (1567.98, 0.30), (1046.50, 0.45)]
    parts = [_at(_tone('sine', f, 0.15, 0.25, 0.002), t, 0.60) for f, t in notes]
    return _finalize(_mix(*parts))

def music_box_winding_001():
    parts = []
    for i in range(8):
        nz = _at(_noise(0.02, 0.20, 0.001, seed=200+i), i*0.08, 0.70)
        parts.append(nz)
    return _finalize(_mix(*parts))

def acoustic_guitar_strum_001():
    nz = _at(_noise(0.15, 0.30, 0.005, seed=201), 0.00, 0.50)
    a = _at(_tone('sawtooth', 196.00, 0.40, 0.20, 0.010), 0.05, 0.50)
    b = _at(_tone('sawtooth', 246.94, 0.40, 0.20, 0.010), 0.08, 0.50)
    c = _at(_tone('sawtooth', 293.66, 0.40, 0.20, 0.010), 0.11, 0.50)
    return _finalize(_mix(nz, a, b, c))

def acoustic_guitar_pluck_001():
    nz = _at(_noise(0.05, 0.20, 0.002, seed=202), 0.00, 0.40)
    a = _at(_tone('sawtooth', 440.00, 0.30, 0.30, 0.005), 0.00, 0.40)
    return _finalize(_mix(nz, a))

def electric_guitar_feedback_001():
    a = _at(_sweep('sawtooth', 400.0, 1200.0, 0.80, 0.30, 0.010), 0.00, 0.90)
    b = _at(_sweep('square', 800.0, 2400.0, 0.80, 0.15, 0.010), 0.00, 0.90)
    return _finalize(_mix(a, b))

def bass_guitar_slide_001():
    a = _at(_sweep('sawtooth', 100.0, 50.0, 0.60, 0.40, 0.005), 0.00, 0.70)
    return _finalize(_mix(a))

def snare_drum_roll_short_001():
    parts = []
    for i in range(10):
        nz = _at(_noise(0.05, 0.30, 0.001, seed=203+i), i*0.03, 0.35)
        parts.append(nz)
    return _finalize(_mix(*parts))

def cymbal_swell_001():
    nz = _at(_noise(1.50, 0.35, 0.30, seed=204), 0.00, 1.60)
    return _finalize(_mix(nz))

def triangle_instrument_hit_001():
    a = _at(_tone('sine', 2500.0, 1.00, 0.30, 0.002), 0.00, 1.10)
    return _finalize(_mix(a))

def xylophone_run_001():
    notes = [(1046.50, 0.0), (987.77, 0.10), (880.00, 0.20), (783.99, 0.30)]
    parts = [_at(_tone('triangle', f, 0.10, 0.25, 0.002), t, 0.40) for f, t in notes]
    return _finalize(_mix(*parts))

def harp_glissando_short_001():
    a = _at(_sweep('triangle', 400.0, 2000.0, 0.40, 0.25, 0.005), 0.00, 0.50)
    return _finalize(_mix(a))

def orchestral_stinger_triumphant_001():
    a = _at(_tone('sawtooth', 261.63, 0.80, 0.20, 0.010), 0.00, 0.90)
    b = _at(_tone('sawtooth', 329.63, 0.80, 0.20, 0.010), 0.00, 0.90)
    c = _at(_tone('sawtooth', 392.00, 0.80, 0.20, 0.010), 0.00, 0.90)
    d = _at(_tone('sawtooth', 523.25, 0.80, 0.20, 0.010), 0.00, 0.90)
    return _finalize(_mix(a, b, c, d))

def orchestral_stinger_mysterious_001():
    a = _at(_tone('sawtooth', 220.00, 1.20, 0.20, 0.050), 0.00, 1.30)
    b = _at(_tone('sawtooth', 277.18, 1.20, 0.20, 0.050), 0.00, 1.30)
    c = _at(_tone('sawtooth', 311.13, 1.20, 0.20, 0.050), 0.00, 1.30)
    return _finalize(_mix(a, b, c))

OFFICIAL_PRESETS_MUSIC = {
    'piano-single-note-001': piano_single_note_001,
    'piano-chord-soft-001': piano_chord_soft_001,
    'music-box-melody-short-001': music_box_melody_short_001,
    'music-box-winding-001': music_box_winding_001,
    'acoustic-guitar-strum-001': acoustic_guitar_strum_001,
    'acoustic-guitar-pluck-001': acoustic_guitar_pluck_001,
    'electric-guitar-feedback-001': electric_guitar_feedback_001,
    'bass-guitar-slide-001': bass_guitar_slide_001,
    'snare-drum-roll-short-001': snare_drum_roll_short_001,
    'cymbal-swell-001': cymbal_swell_001,
    'triangle-instrument-hit-001': triangle_instrument_hit_001,
    'xylophone-run-001': xylophone_run_001,
    'harp-glissando-short-001': harp_glissando_short_001,
    'orchestral-stinger-triumphant-001': orchestral_stinger_triumphant_001,
    'orchestral-stinger-mysterious-001': orchestral_stinger_mysterious_001,
}