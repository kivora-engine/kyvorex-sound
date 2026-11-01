"""Remastering V1.1 - lot 1 (A) : 73 sounds rebuilt from their browser-preview definition,
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
    'acoustic-guitar-pluck-001': (0.4, [
        ('n', 0, 0.05, 0.2, 0.001, 202, 'highpass', 1500),
        ('t', 0, 0.3, 'sawtooth', 440, None, 0.3, 0.005),
    ]),
    'alien-flora-bloom-001': (0.6, [
        ('n', 0, 0.5, 0.2, 0.001, 1302, 'bandpass', 800),
        ('t', 0, 0.4, 'sine', 600, 1200, 0.2, 0.05),
    ]),
    'ancient-gear-turn-001': (0.9, [
        ('n', 0, 0.8, 0.3, 0.001, 1300, 'bandpass', 1000),
        ('t', 0, 0.8, 'sawtooth', 80, 100, 0.25, 0.05),
    ]),
    'bat-wings-flutter-001': (0.45, [
        ('n', 0, 0.03, 0.2, 0.001, 50, 'bandpass', 800),
        ('n', 0.04, 0.03, 0.2, 0.001, 51, 'bandpass', 800),
        ('n', 0.08, 0.03, 0.2, 0.001, 52, 'bandpass', 800),
        ('n', 0.12, 0.03, 0.2, 0.001, 53, 'bandpass', 800),
        ('n', 0.16, 0.03, 0.2, 0.001, 54, 'bandpass', 800),
        ('n', 0.2, 0.03, 0.2, 0.001, 55, 'bandpass', 800),
        ('n', 0.24, 0.03, 0.2, 0.001, 56, 'bandpass', 800),
        ('n', 0.28, 0.03, 0.2, 0.001, 57, 'bandpass', 800),
        ('n', 0.32, 0.03, 0.2, 0.001, 58, 'bandpass', 800),
        ('n', 0.36, 0.03, 0.2, 0.001, 59, 'bandpass', 800),
    ]),
    'bees-swarm-pass-001': (0.9, [
        ('n', 0, 0.8, 0.3, 0.001, 705, 'bandpass', 1200),
    ]),
    'boar-ground-snuffle-001': (0.5, [
        ('n', 0, 0.4, 0.3, 0.001, 709, 'lowpass', 1000),
    ]),
    'board-game-token-move-001': (0.2, [
        ('n', 0, 0.15, 0.15, 0.001, 312, 'bandpass', 1000),
    ]),
    'body-roll-gravel-001': (0.7, [
        ('n', 0, 0.6, 0.3, 0.001, 621, 'bandpass', 2500),
    ]),
    'chains-rattle-001': (0.4, [
        ('n', 0, 0.05, 0.25, 0.001, 10, 'bandpass', 2000),
        ('n', 0.06, 0.05, 0.25, 0.001, 11, 'bandpass', 2000),
        ('n', 0.12, 0.05, 0.25, 0.001, 12, 'bandpass', 2000),
        ('n', 0.18, 0.05, 0.25, 0.001, 13, 'bandpass', 2000),
        ('n', 0.24, 0.05, 0.25, 0.001, 14, 'bandpass', 2000),
        ('n', 0.3, 0.05, 0.25, 0.001, 15, 'bandpass', 2000),
    ]),
    'chess-piece-place-001': (0.1, [
        ('n', 0, 0.05, 0.3, 0.001, 301, 'lowpass', 600),
        ('t', 0, 0.08, 'sine', 150, None, 0.3, 0.002),
    ]),
    'cicada-day-chorus-001': (0.9, [
        ('n', 0, 0.8, 0.25, 0.001, 702, 'highpass', 4000),
    ]),
    'coin-flip-table-001': (0.3, [
        ('t', 0, 0.1, 'sine', 1200, None, 0.25, 0.002),
        ('n', 0.2, 0.05, 0.2, 0.001, 309, 'bandpass', 3000),
    ]),
    'craft-brick-trowel-001': (0.2, [
        ('n', 0, 0.15, 0.3, 0.001, 920, 'bandpass', 1500),
    ]),
    'craft-cement-mix-001': (0.9, [
        ('n', 0, 0.8, 0.3, 0.001, 921, 'lowpass', 1000),
    ]),
    'craft-chisel-wood-001': (0.1, [
        ('t', 0, 0.05, 'square', 500, None, 0.25, 0.001),
        ('n', 0, 0.05, 0.2, 0.001, 932, 'lowpass', 800),
    ]),
    'craft-glass-cutting-001': (0.4, [
        ('n', 0, 0.3, 0.35, 0.001, 922, 'highpass', 3000),
        ('t', 0, 0.2, 'sine', 2000, None, 0.15, 0.001),
    ]),
    'craft-hacksaw-metal-001': (0.5, [
        ('n', 0, 0.4, 0.25, 0.001, 936, 'highpass', 2500),
    ]),
    'craft-metal-filing-001': (0.5, [
        ('n', 0, 0.4, 0.25, 0.001, 924, 'highpass', 2500),
    ]),
    'craft-nail-puller-001': (0.15, [
        ('n', 0, 0.1, 0.3, 0.001, 935, 'bandpass', 1200),
    ]),
    'craft-paint-brush-001': (0.25, [
        ('n', 0, 0.2, 0.15, 0.001, 931, 'bandpass', 2500),
    ]),
    'craft-paint-roller-001': (0.5, [
        ('n', 0, 0.4, 0.2, 0.001, 930, 'lowpass', 1200),
    ]),
    'craft-pencil-mark-001': (0.08, [
        ('n', 0, 0.05, 0.15, 0.001, 928, 'bandpass', 4000),
    ]),
    'craft-plaster-scrape-001': (0.25, [
        ('n', 0, 0.2, 0.3, 0.001, 925, 'lowpass', 1500),
    ]),
    'craft-pvc-pipe-cut-001': (0.15, [
        ('n', 0, 0.1, 0.35, 0.001, 934, 'highpass', 2000),
    ]),
    'craft-rasp-wood-001': (0.4, [
        ('n', 0, 0.3, 0.25, 0.001, 933, 'bandpass', 1500),
    ]),
    'craft-rivet-gun-001': (0.1, [
        ('t', 0, 0.05, 'square', 300, None, 0.35, 0.001),
        ('n', 0, 0.05, 0.2, 0.001, 929, 'lowpass', 1000),
    ]),
    'craft-soldering-gun-001': (0.25, [
        ('n', 0, 0.2, 0.15, 0.001, 937, 'highpass', 4000),
    ]),
    'craft-tape-measure-001': (0.15, [
        ('n', 0, 0.1, 0.2, 0.001, 927, 'highpass', 3000),
    ]),
    'craft-tile-cutting-001': (0.2, [
        ('n', 0, 0.15, 0.35, 0.001, 926, 'bandpass', 3000),
    ]),
    'craft-wood-sanding-001': (0.6, [
        ('n', 0, 0.5, 0.2, 0.001, 923, 'bandpass', 2000),
    ]),
    'creepy-whisper-001': (0.8, [
        ('n', 0, 0.7, 0.35, 0.001, 777, 'highpass', 1500),
    ]),
    'crocodile-water-movement-001': (0.7, [
        ('n', 0, 0.6, 0.25, 0.001, 707, 'lowpass', 800),
    ]),
    'cryo-pod-close-001': (0.5, [
        ('n', 0, 0.4, 0.3, 0.001, 1305, 'lowpass', 800),
        ('t', 0.3, 0.2, 'sine', 80, None, 0.4, 0.005),
    ]),
    'cryo-pod-open-001': (0.7, [
        ('n', 0, 0.6, 0.35, 0.001, 1304, 'highpass', 2000),
        ('t', 0, 0.5, 'sine', 400, 100, 0.25, 0.01),
    ]),
    'cyber-ddos-attack-001': (1.1, [
        ('n', 0, 1, 0.4, 0.001, 2801, 'bandpass', 1000),
    ]),
    'cyber-firewall-block-001': (0.25, [
        ('n', 0, 0.2, 0.4, 0.001, 2800, 'bandpass', 1500),
        ('t', 0, 0.15, 'square', 200, None, 0.3, 0.001),
    ]),
    'cyber-honeypot-trigger-001': (0.5, [
        ('n', 0, 0.4, 0.3, 0.001, 2802, 'lowpass', 800),
    ]),
    'cymbal-swell-001': (1.6, [
        ('n', 0, 1.5, 0.35, 0.001, 204, 'highpass', 4000),
    ]),
    'data-corruption-001': (0.4, [
        ('n', 0, 0.3, 0.45, 0.001, 1203, 'bandpass', 2500),
    ]),
    'deep-water-dive-001': (0.7, [
        ('n', 0, 0.6, 0.4, 0.001, 617, 'lowpass', 1000),
        ('t', 0, 0.5, 'sine', 300, 50, 0.3, 0.01),
    ]),
    'dice-cup-shake-001': (0.45, [
        ('n', 0, 0.03, 0.25, 0.001, 305, 'highpass', 1500),
        ('n', 0.04, 0.03, 0.25, 0.001, 306, 'highpass', 1500),
        ('n', 0.08, 0.03, 0.25, 0.001, 307, 'highpass', 1500),
        ('n', 0.12, 0.03, 0.25, 0.001, 308, 'highpass', 1500),
        ('n', 0.16, 0.03, 0.25, 0.001, 309, 'highpass', 1500),
        ('n', 0.2, 0.03, 0.25, 0.001, 310, 'highpass', 1500),
        ('n', 0.24, 0.03, 0.25, 0.001, 311, 'highpass', 1500),
        ('n', 0.28, 0.03, 0.25, 0.001, 312, 'highpass', 1500),
        ('n', 0.32, 0.03, 0.25, 0.001, 313, 'highpass', 1500),
        ('n', 0.36, 0.03, 0.25, 0.001, 314, 'highpass', 1500),
    ]),
    'dice-single-roll-001': (0.4, [
        ('n', 0, 0.05, 0.3, 0.001, 302, 'bandpass', 2000),
        ('n', 0.15, 0.05, 0.25, 0.001, 303, 'bandpass', 2000),
        ('n', 0.3, 0.05, 0.2, 0.001, 304, 'bandpass', 2000),
    ]),
    'dimensional-fold-001': (0.7, [
        ('n', 0, 0.6, 0.4, 0.001, 1307, 'bandpass', 2000),
        ('t', 0, 0.6, 'sawtooth', 800, 200, 0.3, 0.02),
    ]),
    'dodge-roll-001': (0.25, [
        ('n', 0, 0.2, 0.25, 0.001, 42, 'lowpass', 800),
        ('t', 0, 0.2, 'sine', 150, 50, 0.35, 0.005),
    ]),
    'domino-chain-fall-001': (0.5, [
        ('n', 0, 0.02, 0.25, 0.001, 311, 'highpass', 2000),
        ('n', 0.06, 0.02, 0.25, 0.001, 312, 'highpass', 2000),
        ('n', 0.12, 0.02, 0.25, 0.001, 313, 'highpass', 2000),
        ('n', 0.18, 0.02, 0.25, 0.001, 314, 'highpass', 2000),
        ('n', 0.24, 0.02, 0.25, 0.001, 315, 'highpass', 2000),
        ('n', 0.3, 0.02, 0.25, 0.001, 316, 'highpass', 2000),
        ('n', 0.36, 0.02, 0.25, 0.001, 317, 'highpass', 2000),
        ('n', 0.42, 0.02, 0.25, 0.001, 318, 'highpass', 2000),
    ]),
    'domino-tile-place-001': (0.08, [
        ('n', 0, 0.03, 0.35, 0.001, 310, 'highpass', 2000),
        ('t', 0, 0.03, 'square', 400, None, 0.2, 0.001),
    ]),
    'door-metal-open-001': (0.6, [
        ('n', 0, 0.5, 0.2, 0.001, 42, 'bandpass', 1200),
        ('t', 0, 0.55, 'sawtooth', 150, 80, 0.25, 0.01),
    ]),
    'door-open-001': (0.48, [
        ('n', 0, 0.35, 0.28, 0.001, 33, 'bandpass', 600),
        ('t', 0.02, 0.35, 'triangle', 220, 130, 0.28, 0.005),
    ]),
    'duck-flock-takeoff-001': (0.7, [
        ('n', 0, 0.6, 0.3, 0.001, 704, 'bandpass', 1500),
    ]),
    'enemy-spawn-001': (0.5, [
        ('t', 0, 0.4, 'sawtooth', 100, 400, 0.3, 0.01),
        ('n', 0, 0.3, 0.15, 0.001, 104, 'lowpass', 600),
    ]),
    'env-avalanche-001': (1.6, [
        ('n', 0, 1.5, 0.5, 0.001, 1000, 'lowpass', 400),
        ('t', 0, 1, 'sine', 60, 30, 0.4, 0.1),
    ]),
    'env-bamboo-creak-001': (0.6, [
        ('n', 0, 0.5, 0.25, 0.001, 1010, 'bandpass', 1200),
        ('t', 0, 0.5, 'sawtooth', 100, 150, 0.2, 0.05),
    ]),
    'env-bioluminescent-forest-001': (1.6, [
        ('n', 0, 1.5, 0.15, 0.001, 1704, 'highpass', 3000),
    ]),
    'env-blizzard-001': (2.2, [
        ('n', 0, 2, 0.5, 0.001, 1023, 'lowpass', 600),
    ]),
    'env-desert-wind-001': (1.6, [
        ('n', 0, 1.5, 0.4, 0.001, 1003, 'bandpass', 800),
        ('t', 0, 1.2, 'sine', 2000, None, 0.1, 0.1),
    ]),
    'env-earthquake-rumble-001': (2.2, [
        ('n', 0, 2, 0.6, 0.001, 1002, 'lowpass', 200),
        ('t', 0, 1.8, 'sine', 40, 20, 0.5, 0.2),
    ]),
    'env-forest-fire-001': (1.6, [
        ('n', 0, 1.5, 0.5, 0.001, 1014, 'lowpass', 1500),
        ('t', 0, 1.2, 'sine', 100, 50, 0.3, 0.05),
    ]),
    'env-frozen-lake-crack-001': (0.25, [
        ('n', 0, 0.2, 0.5, 0.001, 1702, 'bandpass', 2000),
    ]),
    'env-geyser-eruption-001': (1, [
        ('n', 0, 0.8, 0.4, 0.001, 1001, 'highpass', 1000),
        ('t', 0, 0.5, 'sine', 200, 800, 0.3, 0.05),
    ]),
    'env-geyser-mini-001': (0.5, [
        ('n', 0, 0.4, 0.3, 0.001, 1700, 'highpass', 1500),
    ]),
    'env-glacier-crack-001': (0.15, [
        ('n', 0, 0.1, 0.5, 0.001, 1004, 'highpass', 2000),
        ('t', 0, 0.05, 'square', 1500, None, 0.3, 0.001),
    ]),
    'env-hail-storm-001': (0.5, [
        ('n', 0, 0.1, 0.4, 0.001, 1015, 'highpass', 3000),
        ('n', 0.15, 0.1, 0.4, 0.001, 1016, 'highpass', 3000),
        ('n', 0.3, 0.1, 0.4, 0.001, 1017, 'highpass', 3000),
    ]),
    'env-icicle-fall-001': (0.15, [
        ('n', 0, 0.1, 0.4, 0.001, 1012, 'highpass', 3000),
        ('t', 0, 0.1, 'sine', 2500, None, 0.3, 0.001),
    ]),
    'env-jungle-rain-001': (1.6, [
        ('n', 0, 1.5, 0.4, 0.001, 1024, 'highpass', 2000),
    ]),
    'env-lava-bubble-001': (0.5, [
        ('t', 0, 0.4, 'sine', 80, 150, 0.4, 0.05),
        ('n', 0, 0.3, 0.2, 0.001, 1005, 'lowpass', 500),
    ]),
    'env-meteor-shower-distant-001': (1.3, [
        ('n', 0, 1.2, 0.2, 0.001, 1701, 'lowpass', 400),
    ]),
    'env-quarry-blast-001': (0.6, [
        ('n', 0, 0.5, 0.6, 0.001, 1025, 'lowpass', 300),
        ('t', 0, 0.5, 'sine', 80, 20, 0.5, 0.01),
    ]),
    'env-quicksand-001': (1.3, [
        ('n', 0, 1.2, 0.4, 0.001, 1007, 'lowpass', 600),
        ('t', 0, 1, 'sine', 50, 20, 0.3, 0.2),
    ]),
    'env-river-flow-001': (2.2, [
        ('n', 0, 2, 0.4, 0.001, 1013, 'bandpass', 800),
    ]),
    'env-rock-fall-001': (0.6, [
        ('n', 0, 0.2, 0.4, 0.001, 1020, 'lowpass', 800),
        ('n', 0.2, 0.2, 0.4, 0.001, 1021, 'lowpass', 800),
    ]),
    'env-sandstorm-001': (1.6, [
        ('n', 0, 1.5, 0.5, 0.001, 1011, 'highpass', 1500),
        ('t', 0, 1.2, 'sawtooth', 3000, None, 0.15, 0.05),
    ]),
    'env-sandstorm-distant-001': (2.2, [
        ('n', 0, 2, 0.3, 0.001, 1705, 'lowpass', 600),
    ]),
    'env-snow-crunch-001': (0.4, [
        ('n', 0, 0.3, 0.3, 0.001, 1008, 'highpass', 2000),
    ]),
}

OFFICIAL_PRESETS_REMASTER_A = {key: _make(key) for key in _DATA}
