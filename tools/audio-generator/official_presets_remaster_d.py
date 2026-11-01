"""Remastering V1.1 - lot 1 (D) : 71 sounds rebuilt from their browser-preview definition,
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
    'ruin-stone-grind-001': (0.5, [
        ('n', 0, 0.4, 0.3, 0.001, 2208, 'lowpass', 800),
    ]),
    'ruin-stone-mechanism-001': (0.25, [
        ('n', 0, 0.2, 0.4, 0.001, 2200, 'lowpass', 600),
        ('t', 0, 0.2, 'sawtooth', 100, 80, 0.3, 0.01),
    ]),
    'ruin-temple-wind-001': (1.6, [
        ('n', 0, 1.5, 0.2, 0.001, 2210, 'lowpass', 500),
    ]),
    'ruin-trap-trigger-001': (0.1, [
        ('n', 0, 0.05, 0.4, 0.001, 2204, 'highpass', 2000),
        ('t', 0, 0.05, 'square', 200, None, 0.3, 0.001),
    ]),
    'sci-inst-chemical-analysis-001': (0.7, [
        ('n', 0, 0.6, 0.3, 0.001, 2501, 'bandpass', 1500),
    ]),
    'sci-inst-electron-beam-001': (0.4, [
        ('n', 0, 0.3, 0.4, 0.001, 2500, 'highpass', 3000),
    ]),
    'sci-inst-lab-ambience-001': (2.2, [
        ('n', 0, 2, 0.15, 0.001, 2504, 'lowpass', 500),
    ]),
    'sci-inst-microscope-slide-001': (0.1, [
        ('n', 0, 0.05, 0.25, 0.001, 2502, 'highpass', 2000),
        ('t', 0, 0.05, 'sine', 800, None, 0.2, 0.001),
    ]),
    'sci-inst-radiation-detector-001': (0.4, [
        ('n', 0, 0.02, 0.3, 0.001, 2503, 'highpass', 3000),
        ('n', 0.08, 0.02, 0.3, 0.001, 2504, 'highpass', 3000),
        ('n', 0.16, 0.02, 0.3, 0.001, 2505, 'highpass', 3000),
        ('n', 0.24, 0.02, 0.3, 0.001, 2506, 'highpass', 3000),
        ('n', 0.32, 0.02, 0.3, 0.001, 2507, 'highpass', 3000),
        ('n', 0.4, 0.02, 0.3, 0.001, 2508, 'highpass', 3000),
    ]),
    'shield-block-001': (0.2, [
        ('n', 0, 0.08, 0.3, 0.001, 103, 'bandpass', 1500),
        ('t', 0.02, 0.15, 'sine', 1200, None, 0.25, 0.002),
    ]),
    'signal-jammer-001': (0.7, [
        ('n', 0, 0.6, 0.4, 0.001, 1204, 'bandpass', 1000),
    ]),
    'slide-ice-long-001': (0.9, [
        ('n', 0, 0.8, 0.2, 0.001, 614, 'highpass', 2000),
        ('t', 0, 0.8, 'sine', 1500, 800, 0.15, 0.02),
    ]),
    'slide-stone-surface-001': (0.5, [
        ('n', 0, 0.4, 0.25, 0.001, 613, 'lowpass', 1200),
    ]),
    'snake-hiss-long-001': (0.9, [
        ('n', 0, 0.8, 0.3, 0.001, 706, 'highpass', 3000),
    ]),
    'snare-drum-roll-short-001': (0.35, [
        ('n', 0, 0.05, 0.3, 0.001, 203, 'bandpass', 2000),
        ('n', 0.03, 0.05, 0.3, 0.001, 204, 'bandpass', 2000),
        ('n', 0.06, 0.05, 0.3, 0.001, 205, 'bandpass', 2000),
        ('n', 0.09, 0.05, 0.3, 0.001, 206, 'bandpass', 2000),
        ('n', 0.12, 0.05, 0.3, 0.001, 207, 'bandpass', 2000),
        ('n', 0.15, 0.05, 0.3, 0.001, 208, 'bandpass', 2000),
        ('n', 0.18, 0.05, 0.3, 0.001, 209, 'bandpass', 2000),
        ('n', 0.21, 0.05, 0.3, 0.001, 210, 'bandpass', 2000),
        ('n', 0.24, 0.05, 0.3, 0.001, 211, 'bandpass', 2000),
        ('n', 0.27, 0.05, 0.3, 0.001, 212, 'bandpass', 2000),
    ]),
    'spaceship-comms-static-001': (0.7, [
        ('n', 0, 0.6, 0.2, 0.001, 2101, 'highpass', 2500),
    ]),
    'spaceship-docking-clamp-001': (0.15, [
        ('n', 0, 0.1, 0.4, 0.001, 2102, 'lowpass', 600),
        ('t', 0, 0.1, 'sine', 100, None, 0.35, 0.002),
    ]),
    'spaceship-emp-burst-001': (0.4, [
        ('n', 0, 0.3, 0.6, 0.001, 2105, 'lowpass', 500),
    ]),
    'spaceship-hull-breach-001': (0.6, [
        ('n', 0, 0.5, 0.6, 0.001, 2104, 'lowpass', 800),
    ]),
    'spaceship-oxygen-leak-001': (0.9, [
        ('n', 0, 0.8, 0.3, 0.001, 2103, 'highpass', 3000),
    ]),
    'spaceship-shield-hit-001': (0.25, [
        ('n', 0, 0.2, 0.5, 0.001, 2100, 'bandpass', 1000),
        ('t', 0, 0.15, 'sine', 200, None, 0.3, 0.002),
    ]),
    'spell-lightning-001': (0.3, [
        ('n', 0, 0.1, 0.5, 0.001, 107, 'highpass', 1000),
        ('t', 0, 0.2, 'sine', 100, 40, 0.4, 0.002),
    ]),
    'sub-airlock-close-001': (0.7, [
        ('n', 0, 0.6, 0.3, 0.001, 2301, 'lowpass', 800),
        ('t', 0.5, 0.2, 'sine', 80, None, 0.3, 0.005),
    ]),
    'sub-airlock-open-001': (0.7, [
        ('n', 0, 0.6, 0.3, 0.001, 2300, 'highpass', 1500),
    ]),
    'sub-ballast-blow-001': (0.9, [
        ('n', 0, 0.8, 0.4, 0.001, 2305, 'highpass', 2000),
    ]),
    'sub-cabin-pressure-leak-001': (0.9, [
        ('n', 0, 0.8, 0.3, 0.001, 2307, 'highpass', 3000),
    ]),
    'sub-depth-charge-001': (0.6, [
        ('n', 0, 0.5, 0.6, 0.001, 2306, 'lowpass', 400),
        ('t', 0, 0.5, 'sine', 80, 20, 0.4, 0.005),
    ]),
    'sub-docking-clamp-001': (0.15, [
        ('n', 0, 0.1, 0.4, 0.001, 2304, 'lowpass', 500),
        ('t', 0, 0.1, 'sine', 100, None, 0.35, 0.002),
    ]),
    'sub-external-hull-tap-001': (0.1, [
        ('n', 0, 0.05, 0.35, 0.001, 2308, 'bandpass', 2000),
        ('t', 0, 0.05, 'sine', 150, None, 0.3, 0.001),
    ]),
    'sub-hatch-close-001': (0.5, [
        ('n', 0, 0.4, 0.35, 0.001, 2303, 'lowpass', 600),
    ]),
    'sub-hatch-open-001': (0.5, [
        ('n', 0, 0.4, 0.35, 0.001, 2302, 'bandpass', 1000),
    ]),
    'summon-creature-001': (0.7, [
        ('n', 0, 0.6, 0.3, 0.001, 44, 'lowpass', 800),
        ('t', 0, 0.6, 'sawtooth', 100, 250, 0.2, 0.02),
    ]),
    'sword-swing-001': (0.2, [
        ('n', 0, 0.15, 0.35, 0.001, 11, 'bandpass', 1500),
        ('t', 0, 0.15, 'sawtooth', 400, 100, 0.2, 0.002),
    ]),
    'system-overload-001': (0.6, [
        ('n', 0, 0.5, 0.5, 0.001, 1202, 'bandpass', 1500),
        ('t', 0, 0.5, 'square', 400, 1000, 0.3, 0.01),
    ]),
    'tech-cyber-terraform-001': (1.1, [
        ('n', 0, 1, 0.3, 0.001, 1603, 'lowpass', 800),
    ]),
    'tech-hologram-deploy-001': (0.5, [
        ('n', 0, 0.4, 0.3, 0.001, 1601, 'bandpass', 1500),
        ('t', 0, 0.4, 'square', 1000, 500, 0.2, 0.01),
    ]),
    'tech-nanobot-swarm-001': (0.9, [
        ('n', 0, 0.8, 0.3, 0.001, 1600, 'highpass', 2000),
    ]),
    'tech-plasma-conduit-001': (0.7, [
        ('n', 0, 0.6, 0.4, 0.001, 1602, 'highpass', 2500),
    ]),
    'tool-dropping-wrench-001': (0.15, [
        ('n', 0, 0.1, 0.35, 0.001, 832, 'bandpass', 1000),
        ('t', 0, 0.1, 'triangle', 800, None, 0.25, 0.001),
    ]),
    'tool-metal-scrape-001': (0.25, [
        ('n', 0, 0.2, 0.3, 0.001, 825, 'bandpass', 1500),
    ]),
    'tool-pliers-snip-001': (0.1, [
        ('n', 0, 0.05, 0.3, 0.001, 822, 'highpass', 2500),
    ]),
    'tool-rope-tie-001': (0.2, [
        ('n', 0, 0.15, 0.2, 0.001, 828, 'lowpass', 1000),
    ]),
    'tool-sandpaper-rub-001': (0.6, [
        ('n', 0, 0.5, 0.2, 0.001, 823, 'bandpass', 1000),
    ]),
    'tool-saw-metal-001': (0.5, [
        ('n', 0, 0.4, 0.3, 0.001, 821, 'highpass', 3000),
    ]),
    'tool-saw-wood-001': (0.5, [
        ('n', 0, 0.4, 0.3, 0.001, 820, 'lowpass', 1500),
    ]),
    'tool-solder-iron-001': (0.4, [
        ('n', 0, 0.3, 0.15, 0.001, 830, 'highpass', 3000),
    ]),
    'tool-stone-chisel-001': (0.1, [
        ('t', 0, 0.05, 'square', 600, None, 0.25, 0.001),
        ('n', 0, 0.05, 0.2, 0.001, 827, 'highpass', 2000),
    ]),
    'tool-tape-peel-001': (0.4, [
        ('n', 0, 0.3, 0.25, 0.001, 824, 'highpass', 2000),
    ]),
    'tool-toolbox-close-001': (0.12, [
        ('n', 0, 0.08, 0.3, 0.001, 833, 'lowpass', 800),
    ]),
    'tool-welding-arc-001': (0.6, [
        ('n', 0, 0.5, 0.4, 0.001, 831, 'highpass', 4000),
    ]),
    'tool-wire-strip-001': (0.15, [
        ('n', 0, 0.1, 0.25, 0.001, 829, 'bandpass', 2000),
    ]),
    'tool-wood-creak-001': (0.4, [
        ('n', 0, 0.3, 0.25, 0.001, 826, 'lowpass', 800),
    ]),
    'trapdoor-trigger-001': (0.15, [
        ('n', 0, 0.1, 0.4, 0.001, 1308, 'lowpass', 600),
        ('t', 0, 0.1, 'sine', 100, None, 0.4, 0.002),
    ]),
    'ui-drag-drop-002': (0.1, [
        ('t', 0, 0.05, 'sine', 400, None, 0.2, 0.002),
        ('n', 0, 0.03, 0.15, 0.001, 500, 'lowpass', 800),
    ]),
    'underwater-movement-001': (0.6, [
        ('n', 0, 0.5, 0.25, 0.001, 618, 'lowpass', 600),
    ]),
    'unique-alchemy-brew-001': (0.9, [
        ('n', 0, 0.8, 0.3, 0.001, 1800, 'lowpass', 800),
    ]),
    'unique-cyber-deck-overheat-001': (0.7, [
        ('n', 0, 0.6, 0.4, 0.001, 1803, 'highpass', 2000),
    ]),
    'unique-magic-mirror-shatter-001': (0.5, [
        ('n', 0, 0.4, 0.5, 0.001, 1804, 'highpass', 4000),
    ]),
    'unique-reality-glitch-short-001': (0.15, [
        ('n', 0, 0.1, 0.4, 0.001, 1805, 'bandpass', 3000),
        ('t', 0, 0.1, 'square', 1000, 200, 0.3, 0.001),
    ]),
    'unique-stealth-footstep-001': (0.15, [
        ('n', 0, 0.1, 0.15, 0.001, 1801, 'lowpass', 500),
    ]),
    'unique-vent-crawl-001': (0.6, [
        ('n', 0, 0.5, 0.2, 0.001, 1802, 'bandpass', 600),
    ]),
    'veh-brake-squeal-001': (0.6, [
        ('n', 0, 0.5, 0.3, 0.001, 2601, 'bandpass', 2000),
        ('t', 0, 0.4, 'sine', 2000, None, 0.15, 0.05),
    ]),
    'veh-cockpit-ambience-001': (1.6, [
        ('n', 0, 1.5, 0.15, 0.001, 2608, 'lowpass', 400),
    ]),
    'veh-crash-metal-impact-001': (0.4, [
        ('n', 0, 0.3, 0.6, 0.001, 2606, 'highpass', 2000),
        ('t', 0, 0.3, 'sine', 80, 40, 0.4, 0.005),
    ]),
    'veh-drivetrain-engage-001': (0.25, [
        ('n', 0, 0.2, 0.35, 0.001, 2603, 'bandpass', 1200),
        ('t', 0, 0.2, 'sawtooth', 80, 100, 0.3, 0.005),
    ]),
    'veh-exhaust-burst-001': (0.25, [
        ('n', 0, 0.2, 0.5, 0.001, 2602, 'lowpass', 1000),
    ]),
    'veh-gear-grind-001': (0.4, [
        ('n', 0, 0.3, 0.4, 0.001, 2607, 'bandpass', 1000),
    ]),
    'veh-gear-shift-heavy-001': (0.15, [
        ('n', 0, 0.1, 0.4, 0.001, 2600, 'lowpass', 800),
        ('t', 0, 0.1, 'square', 100, None, 0.35, 0.002),
    ]),
    'veh-tire-screech-001': (0.9, [
        ('n', 0, 0.8, 0.35, 0.001, 2604, 'highpass', 3000),
    ]),
    'veh-wheel-spin-001': (0.7, [
        ('n', 0, 0.6, 0.25, 0.001, 2605, 'bandpass', 1500),
    ]),
    'zombie-groan-001': (0.7, [
        ('t', 0, 0.6, 'sawtooth', 150, 80, 0.35, 0.02),
        ('n', 0, 0.5, 0.15, 0.001, 13, 'lowpass', 600),
    ]),
}

OFFICIAL_PRESETS_REMASTER_D = {key: _make(key) for key in _DATA}
