"""Remastering V1.1 - lot 1 (C) : 73 sounds rebuilt from their browser-preview definition,
so that the downloadable WAV/MP3 matches the preview (noise filters now applied)."""
import math
from synthesis import white_noise, DEFAULT_SAMPLE_RATE
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

def _tone(wave_type, freq, dur, amplitude, attack, freq_end=None):
    n = int(dur * SR)
    if n <= 0: return []
    env = _env_exp(n, attack)
    out = []
    phase = 0.0
    for i in range(n):
        if freq_end is None:
            f = freq
        else:
            f = freq * ((max(1.0, freq_end) / freq) ** (i / float(max(1, n - 1))))
        phase += 2.0 * math.pi * f / SR
        out.append(amplitude * _wave_sample(wave_type, phase) * env[i])
    return out

def _filter(samples, ftype, freq):
    w0 = 2.0 * math.pi * freq / SR
    cw = math.cos(w0)
    alpha = math.sin(w0) / 2.0
    if ftype == 'lowpass':
        b0, b1, b2 = (1.0 - cw) / 2.0, 1.0 - cw, (1.0 - cw) / 2.0
    elif ftype == 'highpass':
        b0, b1, b2 = (1.0 + cw) / 2.0, -(1.0 + cw), (1.0 + cw) / 2.0
    else:
        b0, b1, b2 = alpha, 0.0, -alpha
    a0, a1, a2 = 1.0 + alpha, -2.0 * cw, 1.0 - alpha
    b0, b1, b2, a1, a2 = b0 / a0, b1 / a0, b2 / a0, a1 / a0, a2 / a0
    x1 = x2 = y1 = y2 = 0.0
    out = []
    for x in samples:
        y = b0 * x + b1 * x1 + b2 * x2 - a1 * y1 - a2 * y2
        x2, x1 = x1, x
        y2, y1 = y1, y
        out.append(y)
    return out

def _noise(dur, amplitude, attack, seed, ftype, freq):
    n = int(dur * SR)
    if n <= 0: return []
    env = _env_exp(n, attack)
    raw = _filter(white_noise(dur, SR, amplitude, seed=seed), ftype, freq)
    out = [raw[i] * env[i] for i in range(min(n, len(raw)))]
    if len(out) < n: out.extend([0.0] * (n - len(out)))
    return out

def _at(samples, offset_sec, total_sec):
    n_total = int(total_sec * SR)
    n_off = int(offset_sec * SR)
    out = [0.0] * n_total
    for i, s in enumerate(samples):
        idx = n_off + i
        if idx < n_total: out[idx] += s
    return out

def _finalize(samples):
    peak = max((abs(s) for s in samples), default=0.0)
    if peak == 0.0: return samples
    target = 0.85
    factor = target / peak if peak > target else 1.0
    return [s * factor for s in samples]

# Layer formats:
#   ('t', when, dur, wave, freq, freq_end_or_None, gain, attack)
#   ('n', when, dur, gain, attack, seed, filter_type, filter_freq)
def _render(total, layers):
    out = [0.0] * int(total * SR)
    for L in layers:
        if L[0] == 't':
            part = _tone(L[3], L[4], L[2], L[6], L[7], L[5])
        else:
            part = _noise(L[2], L[3], L[4], L[5], L[6], L[7])
        part = _at(part, L[1], total)
        for i in range(len(out)): out[i] += part[i]
    return _finalize(out)

def _make(key):
    total, layers = _DATA[key]
    return lambda: _render(total, layers)

_DATA = {
    'infra-bus-door-close-001': (0.6, [
        ('t', 0, 0.5, 'sine', 200, 100, 0.25, 0.02),
        ('n', 0.4, 0.1, 0.2, 0.001, 2701, 'lowpass', 600),
    ]),
    'infra-container-lock-001': (0.15, [
        ('n', 0, 0.1, 0.4, 0.001, 2705, 'lowpass', 500),
        ('t', 0, 0.1, 'sine', 100, None, 0.35, 0.001),
    ]),
    'infra-gate-close-001': (0.7, [
        ('n', 0, 0.6, 0.3, 0.001, 2707, 'lowpass', 800),
        ('t', 0.5, 0.15, 'sine', 80, None, 0.3, 0.005),
    ]),
    'infra-gate-open-001': (0.7, [
        ('n', 0, 0.6, 0.3, 0.001, 2706, 'lowpass', 800),
    ]),
    'infra-highway-traffic-001': (2.2, [
        ('n', 0, 2, 0.2, 0.001, 2708, 'lowpass', 400),
    ]),
    'infra-subway-arrival-001': (0.9, [
        ('n', 0, 0.8, 0.3, 0.001, 2700, 'lowpass', 800),
    ]),
    'infra-train-brake-squeal-001': (1.3, [
        ('n', 0, 1.2, 0.3, 0.001, 2704, 'bandpass', 2500),
        ('t', 0, 0.8, 'sine', 2000, None, 0.1, 0.05),
    ]),
    'infra-train-track-clatter-001': (0.5, [
        ('n', 0, 0.05, 0.3, 0.001, 2702, 'bandpass', 2000),
        ('n', 0.08, 0.05, 0.3, 0.001, 2703, 'bandpass', 2000),
        ('n', 0.16, 0.05, 0.3, 0.001, 2704, 'bandpass', 2000),
        ('n', 0.24, 0.05, 0.3, 0.001, 2705, 'bandpass', 2000),
        ('n', 0.32, 0.05, 0.3, 0.001, 2706, 'bandpass', 2000),
        ('n', 0.4, 0.05, 0.3, 0.001, 2707, 'bandpass', 2000),
    ]),
    'infra-tunnel-ambience-001': (2.2, [
        ('n', 0, 2, 0.15, 0.001, 2709, 'lowpass', 300),
    ]),
    'infra-tunnel-wind-001': (1.6, [
        ('n', 0, 1.5, 0.2, 0.001, 2703, 'lowpass', 600),
    ]),
    'item-drop-wood-001': (0.15, [
        ('n', 0, 0.08, 0.3, 0.001, 109, 'bandpass', 800),
        ('t', 0, 0.05, 'square', 150, None, 0.2, 0.002),
    ]),
    'lab-chemical-reaction-fizz-001': (1, [
        ('n', 0, 0.8, 0.35, 0.001, 403, 'highpass', 3000),
    ]),
    'lab-glass-stirring-001': (0.7, [
        ('n', 0, 0.6, 0.2, 0.001, 401, 'bandpass', 1500),
    ]),
    'lab-microscope-focus-001': (0.15, [
        ('n', 0, 0.1, 0.15, 0.001, 400, 'highpass', 2000),
    ]),
    'lab-radiation-counter-burst-001': (0.3, [
        ('n', 0, 0.01, 0.3, 0.001, 404, 'highpass', 4000),
        ('n', 0.05, 0.01, 0.3, 0.001, 405, 'highpass', 4000),
        ('n', 0.1, 0.01, 0.3, 0.001, 406, 'highpass', 4000),
        ('n', 0.15, 0.01, 0.3, 0.001, 407, 'highpass', 4000),
        ('n', 0.2, 0.01, 0.3, 0.001, 408, 'highpass', 4000),
    ]),
    'lab-sample-vial-seal-001': (0.1, [
        ('t', 0, 0.05, 'square', 400, None, 0.2, 0.001),
        ('n', 0, 0.03, 0.15, 0.001, 402, 'lowpass', 1000),
    ]),
    'ladder-metal-rattle-001': (0.2, [
        ('n', 0, 0.15, 0.3, 0.001, 616, 'bandpass', 3000),
        ('t', 0, 0.1, 'triangle', 800, None, 0.2, 0.002),
    ]),
    'landing-knee-hard-001': (0.2, [
        ('t', 0, 0.15, 'sawtooth', 150, 50, 0.4, 0.002),
        ('n', 0, 0.1, 0.3, 0.001, 612, 'lowpass', 600),
    ]),
    'landing-roll-soft-001': (0.4, [
        ('n', 0, 0.3, 0.25, 0.001, 611, 'lowpass', 800),
        ('t', 0, 0.2, 'sine', 100, None, 0.3, 0.01),
    ]),
    'leaves-rustle-001': (0.7, [
        ('n', 0, 0.6, 0.3, 0.001, 106, 'highpass', 2000),
    ]),
    'lion-territorial-roar-001': (0.7, [
        ('t', 0, 0.6, 'sawtooth', 150, 80, 0.4, 0.02),
        ('n', 0, 0.4, 0.2, 0.001, 700, 'lowpass', 600),
    ]),
    'magic-dispel-001': (0.5, [
        ('t', 0, 0.4, 'triangle', 1000, 300, 0.25, 0.005),
        ('n', 0, 0.3, 0.15, 0.001, 12, 'lowpass', 2000),
    ]),
    'magic-fire-cast-001': (0.5, [
        ('n', 0, 0.4, 0.3, 0.001, 66, 'lowpass', 1500),
        ('t', 0, 0.4, 'sawtooth', 300, 100, 0.25, 0.005),
    ]),
    'magical-trap-snap-001': (0.1, [
        ('t', 0, 0.05, 'square', 600, None, 0.35, 0.001),
        ('n', 0, 0.1, 0.25, 0.001, 1301, 'highpass', 2000),
    ]),
    'mech-chain-rattle-001': (0.3, [
        ('n', 0, 0.03, 0.25, 0.001, 802, 'bandpass', 3000),
        ('n', 0.04, 0.03, 0.25, 0.001, 803, 'bandpass', 3000),
        ('n', 0.08, 0.03, 0.25, 0.001, 804, 'bandpass', 3000),
        ('n', 0.12, 0.03, 0.25, 0.001, 805, 'bandpass', 3000),
        ('n', 0.16, 0.03, 0.25, 0.001, 806, 'bandpass', 3000),
        ('n', 0.2, 0.03, 0.25, 0.001, 807, 'bandpass', 3000),
    ]),
    'mech-gear-grind-001': (0.5, [
        ('n', 0, 0.4, 0.3, 0.001, 800, 'lowpass', 800),
        ('t', 0, 0.4, 'sawtooth', 100, 150, 0.25, 0.02),
    ]),
    'mech-hammer-strike-001': (0.15, [
        ('t', 0, 0.1, 'sine', 150, None, 0.4, 0.001),
        ('n', 0, 0.05, 0.2, 0.001, 808, 'bandpass', 1500),
    ]),
    'mech-heavy-door-slide-001': (0.7, [
        ('n', 0, 0.6, 0.25, 0.001, 810, 'lowpass', 1000),
    ]),
    'mech-hydraulic-press-001': (0.5, [
        ('t', 0, 0.4, 'sawtooth', 150, 50, 0.35, 0.01),
        ('n', 0.3, 0.2, 0.2, 0.001, 801, 'lowpass', 600),
    ]),
    'mech-lock-release-001': (0.1, [
        ('t', 0, 0.04, 'square', 300, None, 0.25, 0.001),
        ('n', 0.05, 0.05, 0.3, 0.001, 804, 'bandpass', 2000),
    ]),
    'mech-pneumatic-hiss-001': (0.25, [
        ('n', 0, 0.2, 0.25, 0.001, 809, 'highpass', 2500),
    ]),
    'mech-steam-burst-001': (0.4, [
        ('n', 0, 0.3, 0.4, 0.001, 806, 'highpass', 3000),
    ]),
    'mech-valve-hiss-001': (0.5, [
        ('n', 0, 0.4, 0.3, 0.001, 805, 'highpass', 2000),
    ]),
    'mech-weld-spark-001': (0.25, [
        ('n', 0, 0.2, 0.3, 0.001, 807, 'highpass', 4000),
    ]),
    'melee-hit-heavy-001': (0.25, [
        ('n', 0, 0.15, 0.4, 0.001, 102, 'lowpass', 800),
        ('t', 0, 0.2, 'sawtooth', 150, 50, 0.35, 0.002),
    ]),
    'melee-hit-light-001': (0.1, [
        ('n', 0, 0.06, 0.25, 0.001, 101, 'highpass', 1000),
        ('t', 0, 0.04, 'square', 600, None, 0.2, 0.001),
    ]),
    'meteor-shower-pass-001': (1.3, [
        ('n', 0, 1.2, 0.3, 0.001, 1306, 'lowpass', 400),
    ]),
    'monkey-canopy-leap-001': (0.4, [
        ('n', 0, 0.3, 0.25, 0.001, 708, 'bandpass', 1500),
    ]),
    'music-box-winding-001': (0.7, [
        ('n', 0, 0.02, 0.2, 0.001, 200, 'highpass', 2000),
        ('n', 0.08, 0.02, 0.2, 0.001, 201, 'highpass', 2000),
        ('n', 0.16, 0.02, 0.2, 0.001, 202, 'highpass', 2000),
        ('n', 0.24, 0.02, 0.2, 0.001, 203, 'highpass', 2000),
        ('n', 0.32, 0.02, 0.2, 0.001, 204, 'highpass', 2000),
        ('n', 0.4, 0.02, 0.2, 0.001, 205, 'highpass', 2000),
        ('n', 0.48, 0.02, 0.2, 0.001, 206, 'highpass', 2000),
        ('n', 0.56, 0.02, 0.2, 0.001, 207, 'highpass', 2000),
    ]),
    'nebula-ambience-001': (2.2, [
        ('n', 0, 2, 0.2, 0.001, 1309, 'lowpass', 500),
    ]),
    'object-break-001': (0.25, [
        ('n', 0, 0.2, 0.4, 0.001, 88, 'highpass', 800),
        ('t', 0, 0.1, 'square', 200, 100, 0.2, 0.002),
    ]),
    'ocean-wave-001': (1.5, [
        ('n', 0, 1.4, 0.35, 0.001, 8, 'lowpass', 600),
        ('t', 0, 1.2, 'sine', 200, 100, 0.15, 0.1),
    ]),
    'owl-wing-pass-001': (0.5, [
        ('n', 0, 0.4, 0.15, 0.001, 703, 'lowpass', 1000),
    ]),
    'plasma-shot-001': (0.2, [
        ('t', 0, 0.15, 'sawtooth', 2000, 300, 0.3, 0.002),
        ('n', 0, 0.05, 0.2, 0.001, 108, 'bandpass', 1500),
    ]),
    'plasma-welding-001': (0.5, [
        ('n', 0, 0.4, 0.45, 0.001, 1303, 'highpass', 3000),
    ]),
    'playing-card-deal-001': (0.15, [
        ('n', 0, 0.1, 0.25, 0.001, 307, 'bandpass', 2500),
    ]),
    'playing-card-flip-001': (0.08, [
        ('n', 0, 0.05, 0.3, 0.001, 308, 'highpass', 4000),
    ]),
    'playing-cards-shuffle-001': (1.1, [
        ('n', 0, 1, 0.3, 0.001, 306, 'highpass', 3000),
    ]),
    'poker-chip-slide-001': (0.25, [
        ('n', 0, 0.2, 0.2, 0.001, 314, 'bandpass', 800),
    ]),
    'poker-chip-stack-001': (0.1, [
        ('n', 0, 0.04, 0.3, 0.001, 313, 'highpass', 1500),
        ('t', 0, 0.03, 'square', 600, None, 0.2, 0.001),
    ]),
    'pumpkin-smash-001': (0.15, [
        ('n', 0, 0.1, 0.4, 0.001, 99, 'lowpass', 800),
        ('t', 0, 0.1, 'sine', 200, 50, 0.3, 0.002),
    ]),
    'raven-caw-001': (0.25, [
        ('n', 0, 0.15, 0.3, 0.001, 666, 'bandpass', 1500),
        ('t', 0, 0.15, 'sawtooth', 800, 200, 0.35, 0.002),
    ]),
    'react-coolant-flow-001': (1.1, [
        ('n', 0, 1, 0.2, 0.001, 2901, 'highpass', 3000),
    ]),
    'react-coolant-leak-001': (0.9, [
        ('n', 0, 0.8, 0.3, 0.001, 2905, 'highpass', 2500),
    ]),
    'react-core-overload-001': (0.6, [
        ('n', 0, 0.5, 0.5, 0.001, 2900, 'bandpass', 1500),
    ]),
    'react-core-vent-001': (0.7, [
        ('n', 0, 0.6, 0.45, 0.001, 2903, 'lowpass', 800),
    ]),
    'react-emergency-purge-001': (0.5, [
        ('n', 0, 0.4, 0.6, 0.001, 2904, 'bandpass', 1000),
    ]),
    'react-plasma-ignite-001': (0.25, [
        ('n', 0, 0.2, 0.4, 0.001, 2902, 'highpass', 2000),
    ]),
    'react-reactor-ambience-001': (2.2, [
        ('n', 0, 2, 0.15, 0.001, 2906, 'lowpass', 400),
    ]),
    'robot-claw-grab-001': (0.1, [
        ('n', 0, 0.05, 0.3, 0.001, 2000, 'bandpass', 1500),
        ('t', 0, 0.05, 'sine', 200, None, 0.35, 0.001),
    ]),
    'robot-claw-release-001': (0.1, [
        ('n', 0, 0.05, 0.25, 0.001, 2001, 'highpass', 2000),
    ]),
    'robot-lock-release-001': (0.1, [
        ('n', 0, 0.05, 0.25, 0.001, 2004, 'bandpass', 1000),
    ]),
    'robot-overload-001': (0.5, [
        ('n', 0, 0.4, 0.5, 0.001, 2005, 'bandpass', 1500),
    ]),
    'robot-weld-spark-001': (0.25, [
        ('n', 0, 0.2, 0.4, 0.001, 2002, 'highpass', 3000),
    ]),
    'rock-climb-grip-001': (0.12, [
        ('n', 0, 0.08, 0.25, 0.001, 619, 'bandpass', 2000),
    ]),
    'rope-climb-strain-001': (0.6, [
        ('n', 0, 0.5, 0.2, 0.001, 615, 'bandpass', 800),
    ]),
    'ruin-artifact-shatter-001': (0.25, [
        ('n', 0, 0.2, 0.5, 0.001, 2209, 'highpass', 3000),
        ('t', 0, 0.15, 'sine', 2000, None, 0.2, 0.001),
    ]),
    'ruin-block-move-001': (0.7, [
        ('n', 0, 0.6, 0.35, 0.001, 2205, 'lowpass', 400),
    ]),
    'ruin-lock-engage-001': (0.15, [
        ('t', 0, 0.1, 'square', 300, None, 0.3, 0.002),
        ('n', 0, 0.1, 0.2, 0.001, 2201, 'lowpass', 800),
    ]),
    'ruin-lock-release-001': (0.15, [
        ('n', 0, 0.1, 0.3, 0.001, 2202, 'bandpass', 1500),
    ]),
    'ruin-pressure-plate-001': (0.1, [
        ('n', 0, 0.05, 0.35, 0.001, 2206, 'lowpass', 600),
        ('t', 0, 0.05, 'sine', 100, None, 0.3, 0.001),
    ]),
    'ruin-sarcophagus-open-001': (0.9, [
        ('n', 0, 0.8, 0.4, 0.001, 2207, 'lowpass', 300),
    ]),
    'ruin-statue-turn-001': (0.7, [
        ('n', 0, 0.6, 0.3, 0.001, 2203, 'lowpass', 500),
    ]),
}

OFFICIAL_PRESETS_REMASTER_C = {key: _make(key) for key in _DATA}
