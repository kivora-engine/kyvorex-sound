"""Remastering V1.1 - lot 1 (B) : 73 sounds rebuilt from their browser-preview definition,
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
    'env-solar-flare-wind-001': (1.6, [
        ('n', 0, 1.5, 0.35, 0.001, 1707, 'bandpass', 1000),
    ]),
    'env-swamp-ambience-001': (1.6, [
        ('n', 0, 1.5, 0.2, 0.001, 1009, 'lowpass', 500),
    ]),
    'env-tide-pool-001': (1.1, [
        ('n', 0, 1, 0.2, 0.001, 1019, 'bandpass', 1000),
    ]),
    'env-tornado-001': (2.2, [
        ('n', 0, 2, 0.6, 0.001, 1018, 'lowpass', 800),
        ('t', 0, 2, 'sawtooth', 150, 50, 0.3, 0.1),
    ]),
    'env-volcanic-lightning-001': (0.4, [
        ('n', 0, 0.3, 0.6, 0.001, 1703, 'highpass', 1000),
    ]),
    'env-volcanic-vent-001': (1.1, [
        ('n', 0, 1, 0.4, 0.001, 1022, 'highpass', 1500),
        ('t', 0, 0.8, 'sine', 1500, None, 0.1, 0.05),
    ]),
    'env-waterfall-001': (2.2, [
        ('n', 0, 2, 0.5, 0.001, 1006, 'lowpass', 1000),
    ]),
    'env-waterfall-misty-001': (1.6, [
        ('n', 0, 1.5, 0.4, 0.001, 1706, 'lowpass', 1200),
    ]),
    'environment-rain-start-001': (0.5, [
        ('n', 0, 0.05, 0.1, 0.001, 100, 'highpass', 3000),
        ('n', 0.04, 0.05, 0.1, 0.001, 101, 'highpass', 3000),
        ('n', 0.08, 0.05, 0.1, 0.001, 102, 'highpass', 3000),
        ('n', 0.12, 0.05, 0.1, 0.001, 103, 'highpass', 3000),
        ('n', 0.16, 0.05, 0.1, 0.001, 104, 'highpass', 3000),
        ('n', 0.2, 0.05, 0.1, 0.001, 105, 'highpass', 3000),
        ('n', 0.24, 0.05, 0.1, 0.001, 106, 'highpass', 3000),
        ('n', 0.28, 0.05, 0.1, 0.001, 107, 'highpass', 3000),
        ('n', 0.32, 0.05, 0.1, 0.001, 108, 'highpass', 3000),
        ('n', 0.36, 0.05, 0.1, 0.001, 109, 'highpass', 3000),
        ('n', 0.4, 0.05, 0.1, 0.001, 110, 'highpass', 3000),
        ('n', 0.44, 0.05, 0.1, 0.001, 111, 'highpass', 3000),
    ]),
    'environment-thunder-001': (1.2, [
        ('n', 0, 1, 0.5, 0.001, 77, 'lowpass', 200),
        ('t', 0, 1, 'sine', 60, 30, 0.4, 0.01),
    ]),
    'environment-wind-gust-001': (0.8, [
        ('n', 0, 0.7, 0.35, 0.001, 12, 'lowpass', 800),
    ]),
    'epic-boss-defeat-001': (1.3, [
        ('n', 0, 1.2, 0.6, 0.001, 1502, 'lowpass', 400),
        ('t', 0, 1.2, 'sine', 80, 20, 0.5, 0.02),
    ]),
    'epic-multiverse-collapse-001': (2.2, [
        ('n', 0, 2, 0.5, 0.001, 1504, 'lowpass', 300),
    ]),
    'epic-portal-destroy-001': (1.1, [
        ('t', 0, 1, 'sawtooth', 2000, 50, 0.5, 0.05),
        ('n', 0.5, 0.5, 0.3, 0.001, 1501, 'lowpass', 600),
    ]),
    'epic-power-surge-001': (0.9, [
        ('n', 0, 0.8, 0.4, 0.001, 1500, 'lowpass', 1000),
        ('t', 0, 0.8, 'square', 400, 100, 0.3, 0.01),
    ]),
    'epic-time-shatter-001': (0.5, [
        ('n', 0, 0.4, 0.5, 0.001, 1503, 'highpass', 3000),
        ('t', 0, 0.4, 'square', 1000, 200, 0.4, 0.001),
    ]),
    'explosion-small-001': (0.6, [
        ('n', 0, 0.55, 0.45, 0.001, 7, 'lowpass', 900),
        ('t', 0, 0.5, 'sine', 180, 45, 0.35, 0.005),
    ]),
    'explosion-small-002': (0.7, [
        ('n', 0, 0.6, 0.4, 0.001, 15, 'lowpass', 600),
        ('t', 0, 0.6, 'sawtooth', 120, 40, 0.3, 0.005),
    ]),
    'fire-crackle-001': (0.8, [
        ('n', 0, 0.7, 0.25, 0.001, 3, 'highpass', 2000),
        ('n', 0.2, 0.05, 0.3, 0.001, 19, 'bandpass', 3000),
        ('n', 0.5, 0.05, 0.3, 0.001, 23, 'bandpass', 2500),
    ]),
    'firewall-deflect-001': (0.15, [
        ('n', 0, 0.1, 0.3, 0.001, 1200, 'highpass', 2000),
        ('t', 0, 0.05, 'sawtooth', 400, None, 0.2, 0.001),
    ]),
    'footstep-dry-leaves-pile-001': (0.25, [
        ('n', 0, 0.2, 0.35, 0.001, 609, 'highpass', 2500),
    ]),
    'footstep-gravel-001': (0.15, [
        ('n', 0, 0.1, 0.4, 0.001, 66, 'highpass', 2000),
        ('t', 0, 0.05, 'sine', 120, None, 0.3, 0.001),
    ]),
    'footstep-gravel-loose-001': (0.15, [
        ('n', 0, 0.05, 0.3, 0.001, 602, 'bandpass', 3000),
        ('n', 0.06, 0.05, 0.25, 0.001, 603, 'bandpass', 3000),
    ]),
    'footstep-marble-hall-001': (0.15, [
        ('t', 0, 0.1, 'sine', 800, None, 0.25, 0.002),
        ('n', 0, 0.05, 0.1, 0.001, 605, 'highpass', 4000),
    ]),
    'footstep-metal-grate-001': (0.12, [
        ('n', 0, 0.08, 0.35, 0.001, 606, 'bandpass', 2500),
        ('t', 0, 0.06, 'sawtooth', 400, None, 0.2, 0.002),
    ]),
    'footstep-mud-deep-001': (0.2, [
        ('n', 0, 0.15, 0.3, 0.001, 600, 'lowpass', 400),
        ('t', 0, 0.1, 'sine', 100, 50, 0.35, 0.005),
    ]),
    'footstep-sand-dunes-001': (0.3, [
        ('n', 0, 0.25, 0.2, 0.001, 610, 'lowpass', 1500),
    ]),
    'footstep-shallow-water-001': (0.2, [
        ('n', 0, 0.15, 0.3, 0.001, 608, 'bandpass', 1200),
        ('t', 0, 0.1, 'sine', 600, 300, 0.2, 0.005),
    ]),
    'footstep-single-001': (0.1, [
        ('t', 0, 0.07, 'sine', 95, 70, 0.4, 0.001),
        ('n', 0, 0.04, 0.18, 0.001, 101, 'lowpass', 1200),
    ]),
    'footstep-snow-crust-001': (0.15, [
        ('n', 0, 0.1, 0.3, 0.001, 607, 'highpass', 3000),
    ]),
    'footstep-wet-grass-001': (0.15, [
        ('n', 0, 0.12, 0.25, 0.001, 601, 'highpass', 2000),
    ]),
    'footstep-wood-hollow-001': (0.1, [
        ('t', 0, 0.08, 'square', 200, None, 0.3, 0.002),
        ('n', 0, 0.05, 0.15, 0.001, 604, 'lowpass', 800),
    ]),
    'forest-ambience-001': (1.5, [
        ('n', 0, 1.4, 0.2, 0.001, 5, 'lowpass', 1000),
        ('t', 0.2, 0.1, 'sine', 3000, None, 0.05, 0.01),
        ('t', 0.8, 0.1, 'sine', 3200, None, 0.05, 0.01),
    ]),
    'forge-anvil-strike-heavy-001': (0.25, [
        ('t', 0, 0.2, 'sine', 80, None, 0.5, 0.002),
        ('n', 0, 0.1, 0.3, 0.001, 2400, 'lowpass', 1000),
    ]),
    'forge-bellows-blow-001': (0.9, [
        ('n', 0, 0.8, 0.3, 0.001, 2401, 'lowpass', 800),
    ]),
    'forge-chain-pull-001': (0.4, [
        ('n', 0, 0.05, 0.25, 0.001, 2403, 'bandpass', 2000),
        ('n', 0.08, 0.05, 0.25, 0.001, 2404, 'bandpass', 2000),
        ('n', 0.16, 0.05, 0.25, 0.001, 2405, 'bandpass', 2000),
        ('n', 0.24, 0.05, 0.25, 0.001, 2406, 'bandpass', 2000),
    ]),
    'forge-coal-shovel-001': (0.4, [
        ('n', 0, 0.3, 0.25, 0.001, 2406, 'lowpass', 600),
    ]),
    'forge-cooling-crackle-001': (0.7, [
        ('n', 0, 0.6, 0.2, 0.001, 2408, 'bandpass', 1200),
    ]),
    'forge-crucible-pour-001': (0.9, [
        ('n', 0, 0.8, 0.35, 0.001, 2404, 'lowpass', 1000),
    ]),
    'forge-cut-tongs-001': (0.15, [
        ('n', 0, 0.1, 0.3, 0.001, 2410, 'highpass', 2500),
        ('t', 0, 0.05, 'triangle', 1000, None, 0.2, 0.001),
    ]),
    'forge-file-metal-001': (0.5, [
        ('n', 0, 0.4, 0.2, 0.001, 2409, 'bandpass', 2000),
    ]),
    'forge-metal-fold-001': (0.4, [
        ('n', 0, 0.3, 0.3, 0.001, 2405, 'bandpass', 1500),
    ]),
    'forge-polish-leather-001': (0.7, [
        ('n', 0, 0.6, 0.15, 0.001, 2411, 'bandpass', 800),
    ]),
    'forge-quenching-sizzle-001': (0.7, [
        ('n', 0, 0.6, 0.4, 0.001, 2402, 'highpass', 3000),
    ]),
    'forge-rivet-gun-001': (0.1, [
        ('t', 0, 0.05, 'square', 300, None, 0.35, 0.001),
        ('n', 0, 0.05, 0.2, 0.001, 2412, 'lowpass', 600),
    ]),
    'forge-sparks-burst-001': (0.25, [
        ('n', 0, 0.2, 0.35, 0.001, 2407, 'highpass', 4000),
    ]),
    'forge-weld-seam-001': (0.4, [
        ('n', 0, 0.3, 0.4, 0.001, 2413, 'highpass', 3000),
    ]),
    'forge-workshop-ambience-001': (1.6, [
        ('n', 0, 1.5, 0.15, 0.001, 2414, 'lowpass', 500),
    ]),
    'fx-armor-break-001': (0.3, [
        ('n', 0, 0.2, 0.5, 0.001, 1107, 'bandpass', 1500),
        ('t', 0, 0.2, 'sine', 100, 50, 0.4, 0.01),
    ]),
    'fx-cloaking-device-001': (0.9, [
        ('n', 0, 0.8, 0.3, 0.001, 1101, 'lowpass', 800),
        ('t', 0, 0.7, 'sine', 800, 200, 0.2, 0.05),
    ]),
    'fx-dimension-rift-001': (1.1, [
        ('n', 0, 1, 0.5, 0.001, 1104, 'lowpass', 600),
        ('t', 0, 1, 'sine', 40, None, 0.4, 0.05),
    ]),
    'fx-illusion-break-001': (0.3, [
        ('n', 0, 0.2, 0.5, 0.001, 1102, 'highpass', 4000),
        ('t', 0, 0.15, 'sine', 3000, None, 0.3, 0.001),
    ]),
    'fx-invisibility-001': (0.7, [
        ('n', 0, 0.6, 0.3, 0.001, 1105, 'lowpass', 400),
    ]),
    'fx-mind-blast-001': (0.3, [
        ('n', 0, 0.2, 0.6, 0.001, 1109, 'highpass', 3000),
        ('t', 0, 0.1, 'square', 2000, None, 0.4, 0.001),
    ]),
    'fx-reality-glitch-001': (0.1, [
        ('n', 0, 0.05, 0.5, 0.001, 1100, 'highpass', 3000),
        ('t', 0, 0.05, 'square', 1000, None, 0.4, 0.001),
    ]),
    'fx-rune-activate-001': (0.6, [
        ('n', 0, 0.5, 0.3, 0.001, 1103, 'bandpass', 1000),
        ('t', 0.3, 0.2, 'sine', 2500, None, 0.3, 0.001),
    ]),
    'fx-spirit-summon-001': (1.1, [
        ('n', 0, 1, 0.4, 0.001, 1108, 'highpass', 2000),
    ]),
    'fx-weapon-enchant-001': (0.4, [
        ('n', 0, 0.3, 0.3, 0.001, 1106, 'bandpass', 2000),
        ('t', 0.1, 0.2, 'sine', 3000, None, 0.2, 0.01),
    ]),
    'heavy-landing-dirt-001': (0.25, [
        ('t', 0, 0.2, 'sine', 120, 40, 0.4, 0.005),
        ('n', 0, 0.15, 0.3, 0.001, 620, 'lowpass', 800),
    ]),
    'hit-impact-001': (0.26, [
        ('t', 0, 0.2, 'sine', 140, 80, 0.4, 0.002),
        ('n', 0, 0.12, 0.35, 0.001, 1, 'lowpass', 1800),
    ]),
    'hit-impact-002': (0.3, [
        ('t', 0, 0.25, 'sawtooth', 100, 50, 0.4, 0.002),
        ('n', 0, 0.15, 0.3, 0.001, 21, 'lowpass', 1000),
    ]),
    'hologram-glitch-001': (0.25, [
        ('n', 0, 0.2, 0.4, 0.001, 1201, 'bandpass', 3000),
        ('t', 0, 0.2, 'sawtooth', 2000, 500, 0.25, 0.001),
    ]),
    'horse-snort-001': (0.4, [
        ('n', 0, 0.3, 0.35, 0.001, 701, 'bandpass', 1000),
    ]),
    'ind-belt-snap-001': (0.1, [
        ('n', 0, 0.05, 0.4, 0.001, 906, 'bandpass', 1200),
        ('t', 0, 0.05, 'sawtooth', 150, None, 0.3, 0.001),
    ]),
    'ind-coolant-spray-001': (0.5, [
        ('n', 0, 0.4, 0.3, 0.001, 903, 'highpass', 2500),
    ]),
    'ind-forge-hammer-001': (0.3, [
        ('t', 0, 0.2, 'sine', 80, None, 0.5, 0.002),
        ('n', 0, 0.1, 0.3, 0.001, 902, 'bandpass', 1500),
    ]),
    'ind-furnace-roar-001': (1.1, [
        ('n', 0, 1, 0.4, 0.001, 904, 'lowpass', 400),
    ]),
    'ind-heavy-door-lock-001': (0.2, [
        ('n', 0, 0.1, 0.35, 0.001, 909, 'lowpass', 800),
        ('t', 0, 0.15, 'sine', 100, None, 0.4, 0.002),
    ]),
    'ind-metal-pour-001': (0.9, [
        ('n', 0, 0.8, 0.35, 0.001, 905, 'lowpass', 800),
    ]),
    'ind-robot-arm-weld-001': (0.4, [
        ('n', 0, 0.3, 0.4, 0.001, 900, 'highpass', 4000),
    ]),
    'ind-scrap-metal-crush-001': (0.6, [
        ('n', 0, 0.5, 0.45, 0.001, 908, 'lowpass', 600),
    ]),
    'ind-steam-release-001': (0.7, [
        ('n', 0, 0.6, 0.45, 0.001, 901, 'highpass', 3000),
    ]),
    'ind-ventilation-hum-001': (1.1, [
        ('n', 0, 1, 0.15, 0.001, 907, 'lowpass', 500),
    ]),
}

OFFICIAL_PRESETS_REMASTER_B = {key: _make(key) for key in _DATA}
