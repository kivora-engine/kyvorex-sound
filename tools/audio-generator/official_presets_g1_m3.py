"""Generation 1 - module 3 : sons reconstruits (son WAV + apercu navigateur)."""
import math
from synthesis import white_noise, DEFAULT_SAMPLE_RATE
SR = DEFAULT_SAMPLE_RATE

def _blep(t, dt):
    if t < dt:
        t = t / dt
        return t + t - t * t - 1.0
    if t > 1.0 - dt:
        t = (t - 1.0) / dt
        return t * t + t + t + 1.0
    return 0.0

def _wave_sample(wave_type, phase, dphase=0.0):
    t = (phase / (2.0 * math.pi)) % 1.0
    dt = min(0.49, dphase / (2.0 * math.pi))
    if wave_type == 'sine': return math.sin(phase)
    if wave_type == 'square': return (1.0 if t < 0.5 else -1.0) + _blep(t, dt) - _blep((t + 0.5) % 1.0, dt)
    if wave_type == 'triangle': return 4.0 * abs(t - 0.5) - 1.0
    if wave_type == 'sawtooth': return 2.0 * t - 1.0 - _blep(t, dt)
    return 0.0

def _env_exp(n, attack, amplitude=1.0):
    # same shape as the browser engine: exponential ramp 0.0001 -> peak, then peak -> 0.0001
    n_atk = max(1, int(attack * SR))
    if n_atk > n: n_atk = n
    r = 0.0001 / max(amplitude, 0.0002)
    out = []
    for i in range(n):
        if i < n_atk: out.append(r ** (1.0 - i / float(n_atk)))
        else:
            t = (i - n_atk) / float(max(1, n - n_atk))
            out.append(r ** t)
    return out

def _tone(wave_type, freq, dur, amplitude, attack):
    n = int(dur * SR)
    if n <= 0: return []
    env = _env_exp(n, attack, amplitude)
    return [amplitude * _wave_sample(wave_type, 2.0 * math.pi * freq * i / SR, 2.0 * math.pi * freq / SR) * env[i] for i in range(n)]

def _sweep(wave_type, f0, f1, dur, amplitude, attack):
    n = int(dur * SR)
    if n <= 0: return []
    env = _env_exp(n, attack, amplitude)
    out = []
    phase = 0.0
    for i in range(n):
        t = i / float(max(1, n - 1))
        f = f0 * ((f1 / f0) ** t)
        phase += 2.0 * math.pi * f / SR
        out.append(amplitude * _wave_sample(wave_type, phase, 2.0 * math.pi * f / SR) * env[i])
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

def _noise(dur, amplitude, attack, seed=1, ftype=None, freq=None):
    n = int(dur * SR)
    if n <= 0: return []
    env = _env_exp(n, attack, amplitude)
    raw = white_noise(dur, SR, amplitude, seed=seed)
    if ftype: raw = _filter(raw, ftype, freq)
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

def _nticks(ftype, dur, attack, seed0, ticks, total_sec):
    out = [0.0] * int(total_sec * SR)
    for i, (when, freq, amp) in enumerate(ticks):
        part = _at(_noise(dur, amp, attack, seed0 + i, ftype, freq), when, total_sec)
        for j in range(len(out)): out[j] += part[j]
    return out

def _tticks(wave_type, dur, attack, ticks, total_sec):
    out = [0.0] * int(total_sec * SR)
    for when, freq, amp in ticks:
        part = _at(_tone(wave_type, freq, dur, amp, attack), when, total_sec)
        for j in range(len(out)): out[j] += part[j]
    return out

def _finalize(samples):
    peak = max((abs(s) for s in samples), default=0.0)
    if peak == 0.0: return samples
    target = 0.85
    factor = target / peak if peak > target else 1.0
    return [s * factor for s in samples]

def env_aurora_borealis_001():
    L = [
        _at(_tone('sine', 440, 2.1, 0.202, 0.8), 0, 2.2), _at(_tone('sine', 660, 2.1, 0.1616, 1), 0.05, 2.2), _at(_tone('sine', 880, 2.1, 0.1078, 1.1), 0.1, 2.2),
        _at(_tone('sine', 443, 2.1, 0.1616, 0.8), 0, 2.2), _at(_sweep('sine', 1200, 2400, 1.5, 0.0674, 0.7), 0.3, 2.2), _at(_noise(1.8, 0.0808, 0.9, 630005, 'highpass', 7000), 0.2, 2.2),
        _at(_tone('sine', 110, 2.1, 0.1616, 0.6), 0, 2.2),
    ]
    return _finalize(_mix(*L))
def env_blizzard_001():
    L = [
        _at(_noise(2.1, 0.6, 0.7, 630100, 'bandpass', 600), 0, 2.2), _at(_noise(2, 0.3, 0.6, 630101, 'highpass', 2500), 0.1, 2.2), _at(_sweep('sine', 420, 520, 2, 0.08, 0.8), 0.1, 2.2),
        _at(_sweep('sine', 630, 780, 2, 0.05, 0.8), 0.1, 2.2), _at(_noise(1.5, 0.4, 0.6, 630104, 'lowpass', 300), 0.4, 2.2),
    ]
    return _finalize(_mix(*L))
def env_floating_islands_001():
    L = [
        _at(_tone('sine', 82, 2.1, 0.25, 0.6), 0, 2.2), _at(_tone('sine', 123, 2.1, 0.15, 0.8), 0, 2.2), _at(_noise(2.1, 0.3, 0.8, 630202, 'bandpass', 300), 0, 2.2),
        _at(_tone('triangle', 220, 2.1, 0.08, 0.8), 0, 2.2), _at(_tone('sine', 1568, 0.8, 0.08, 0.003), 0.5, 2.2), _at(_tone('sine', 1175, 0.8, 0.08, 0.003), 1.1, 2.2),
        _at(_tone('sine', 1760, 0.6, 0.06, 0.003), 1.5, 2.2),
    ]
    return _finalize(_mix(*L))
def env_river_flow_001():
    L = [
        _at(_noise(2.1, 0.9365, 0.5, 630300, 'bandpass', 1500), 0, 2.2), _at(_noise(2.1, 0.6243, 0.5, 630301, 'lowpass', 600), 0, 2.2), _at(_noise(2.1, 0.1665, 0.5, 630302, 'highpass', 5000), 0, 2.2),
        _at(_sweep('sine', 400, 900, 0.05, 0.2081, 0.003), 0.15, 2.2), _at(_sweep('sine', 400, 900, 0.05, 0.2081, 0.003), 0.4, 2.2), _at(_sweep('sine', 400, 900, 0.05, 0.2081, 0.003), 0.65, 2.2),
        _at(_sweep('sine', 400, 900, 0.05, 0.2081, 0.003), 0.9, 2.2), _at(_sweep('sine', 400, 900, 0.05, 0.2081, 0.003), 1.1, 2.2), _at(_sweep('sine', 400, 900, 0.05, 0.2081, 0.003), 1.3, 2.2),
    ]
    return _finalize(_mix(*L))
def env_sandstorm_distant_001():
    L = [
        _at(_noise(2.1, 0.8688, 0.8, 630400, 'lowpass', 400), 0, 2.2), _at(_noise(2, 0.362, 0.9, 630401, 'bandpass', 1200), 0.1, 2.2), _at(_tone('sine', 55, 2.1, 0.2896, 0.6), 0, 2.2),
        _at(_noise(0.01, 0.1448, 0.002, 630403, 'highpass', 5000), 0.2, 2.2), _at(_noise(0.01, 0.1448, 0.002, 630404, 'highpass', 5000), 0.5, 2.2), _at(_noise(0.01, 0.1448, 0.002, 630405, 'highpass', 5000), 0.65, 2.2),
        _at(_noise(0.01, 0.1448, 0.002, 630406, 'highpass', 5000), 0.9, 2.2), _at(_noise(0.01, 0.1448, 0.002, 630407, 'highpass', 5000), 1.2, 2.2), _at(_noise(0.01, 0.1448, 0.002, 630408, 'highpass', 5000), 1.4, 2.2),
    ]
    return _finalize(_mix(*L))
def env_waterfall_001():
    L = [
        _at(_noise(2.1, 0.6, 0.4, 630500, 'bandpass', 2500), 0, 2.2), _at(_noise(2.1, 0.6, 0.4, 630501, 'lowpass', 800), 0, 2.2), _at(_noise(2.1, 0.12, 0.4, 630502, 'highpass', 6000), 0, 2.2),
        _at(_tone('sine', 70, 2.1, 0.2, 0.4), 0, 2.2),
    ]
    return _finalize(_mix(*L))
def infra_highway_traffic_001():
    L = [
        _at(_noise(2.1, 0.7797, 0.6, 630600, 'lowpass', 250), 0, 2.2), _at(_tone('sawtooth', 55, 2.1, 0.2079, 0.5), 0, 2.2), _at(_noise(0.9, 1.0396, 0.4, 630602, 'lowpass', 500), 0, 2.2),
        _at(_noise(0.8, 0.6498, 0.35, 630603, 'bandpass', 1800), 0.1, 2.2), _at(_noise(0.9, 1.0396, 0.4, 630604, 'lowpass', 500), 1.1, 2.2), _at(_noise(0.8, 0.6498, 0.35, 630605, 'bandpass', 1800), 1.15, 2.2),
        _at(_sweep('sine', 200, 120, 0.8, 0.1559, 0.35), 0.15, 2.2), _at(_sweep('sine', 220, 130, 0.8, 0.1559, 0.35), 1.15, 2.2),
    ]
    return _finalize(_mix(*L))
def infra_tunnel_ambience_001():
    L = [
        _at(_tone('sine', 60, 2.1, 0.3, 0.6), 0, 2.2), _at(_tone('sine', 120, 2.1, 0.15, 0.7), 0, 2.2), _at(_noise(2.1, 0.35, 0.7, 630702, 'bandpass', 250), 0, 2.2),
        _at(_noise(0.5, 0.2, 0.15, 630703, 'lowpass', 400), 1, 2.2), _at(_sweep('sine', 1800, 1200, 0.06, 0.08, 0.003), 0.5, 2.2), _at(_sweep('sine', 1800, 1200, 0.06, 0.08, 0.003), 1.3, 2.2),
        _at(_sweep('sine', 1800, 1200, 0.06, 0.08, 0.003), 1.8, 2.2), _at(_sweep('sine', 1800, 1200, 0.06, 0.04, 0.003), 0.62, 2.2), _at(_sweep('sine', 1800, 1200, 0.06, 0.04, 0.003), 1.42, 2.2),
        _at(_sweep('sine', 1800, 1200, 0.06, 0.04, 0.003), 1.92, 2.2),
    ]
    return _finalize(_mix(*L))
def nebula_ambience_001():
    L = [
        _at(_tone('sine', 110, 2.1, 0.15, 0.8), 0, 2.2), _at(_tone('sine', 165, 2.1, 0.15, 0.8), 0, 2.2), _at(_tone('sine', 220, 2.1, 0.15, 0.9), 0, 2.2),
        _at(_sweep('sine', 300, 700, 1.8, 0.06, 0.8), 0.2, 2.2), _at(_noise(2.1, 0.15, 1, 630804, 'bandpass', 800), 0, 2.2), _at(_tone('sine', 40, 2.1, 0.2, 0.6), 0, 2.2),
        _at(_tone('sine', 2200, 0.5, 0.04, 0.05), 0.6, 2.2), _at(_tone('sine', 2200, 0.5, 0.04, 0.05), 1.4, 2.2),
    ]
    return _finalize(_mix(*L))
def black_hole_collapse_001():
    L = [
        _at(_sweep('sawtooth', 2400, 60, 1.3, 0.14, 0.02), 0, 1.6), _at(_sweep('square', 1200, 40, 1.3, 0.05, 0.02), 0, 1.6), _at(_noise(1.3, 0.2, 0.05, 630902, 'bandpass', 1500), 0, 1.6),
        _at(_sweep('sine', 1500, 40, 0.25, 0.4, 0.002), 1.3, 1.6), _at(_noise(0.05, 0.3, 0.001, 630904, 'highpass', 5000), 1.3, 1.6), _at(_sweep('sine', 80, 45, 0.09, 0.4, 0.003), 0, 1.6),
        _at(_sweep('sine', 80, 45, 0.09, 0.4, 0.003), 0.22, 1.6), _at(_sweep('sine', 80, 45, 0.09, 0.4, 0.003), 0.4, 1.6), _at(_sweep('sine', 80, 45, 0.09, 0.4, 0.003), 0.55, 1.6),
        _at(_sweep('sine', 80, 45, 0.09, 0.4, 0.003), 0.67, 1.6), _at(_sweep('sine', 80, 45, 0.09, 0.4, 0.003), 0.77, 1.6), _at(_sweep('sine', 80, 45, 0.09, 0.4, 0.003), 0.85, 1.6),
        _at(_sweep('sine', 80, 45, 0.09, 0.4, 0.003), 0.92, 1.6), _at(_sweep('sine', 80, 45, 0.09, 0.4, 0.003), 0.98, 1.6), _at(_sweep('sine', 80, 45, 0.09, 0.4, 0.003), 1.03, 1.6),
        _at(_sweep('sine', 80, 45, 0.09, 0.4, 0.003), 1.07, 1.6), _at(_sweep('sine', 80, 45, 0.09, 0.4, 0.003), 1.1, 1.6), _at(_sweep('sine', 80, 45, 0.09, 0.4, 0.003), 1.13, 1.6),
        _at(_sweep('sine', 80, 45, 0.09, 0.4, 0.003), 1.16, 1.6), _at(_sweep('sine', 80, 45, 0.09, 0.4, 0.003), 1.18, 1.6),
    ]
    return _finalize(_mix(*L))
def env_bioluminescent_forest_001():
    L = [
        _at(_tone('sine', 880, 0.8, 0.174, 0.3), 0, 1.6), _at(_tone('sine', 1100, 0.8, 0.174, 0.3), 0.3, 1.6), _at(_tone('sine', 1320, 0.8, 0.174, 0.3), 0.6, 1.6),
        _at(_tone('sine', 220, 1.5, 0.261, 0.5), 0, 1.6), _at(_noise(1.5, 0.261, 0.5, 631004, 'bandpass', 400), 0, 1.6), _at(_noise(1.2, 0.087, 0.4, 631005, 'highpass', 7000), 0.2, 1.6),
        _at(_sweep('sine', 700, 1000, 0.05, 0.1392, 0.003), 0.2, 1.6), _at(_sweep('sine', 700, 1000, 0.05, 0.1392, 0.003), 0.9, 1.6), _at(_sweep('sine', 700, 1000, 0.05, 0.1392, 0.003), 1.3, 1.6),
    ]
    return _finalize(_mix(*L))
def env_crystal_cave_hum_001():
    L = [
        _at(_tone('sine', 330, 1.5, 0.2, 0.4), 0, 1.6), _at(_tone('sine', 495, 1.5, 0.15, 0.4), 0, 1.6), _at(_tone('sine', 660, 1.5, 0.1, 0.5), 0, 1.6),
        _at(_tone('sine', 333, 1.5, 0.15, 0.4), 0, 1.6), _at(_noise(1.5, 0.06, 0.5, 631104, 'highpass', 6000), 0, 1.6), _at(_tone('sine', 82, 1.5, 0.15, 0.4), 0, 1.6),
        _at(_tone('sine', 1980, 0.6, 0.08, 0.003), 0.4, 1.6), _at(_tone('sine', 1980, 0.6, 0.08, 0.003), 1, 1.6),
    ]
    return _finalize(_mix(*L))
def env_desert_mirage_shimmer_001():
    L = [
        _at(_noise(1.5, 0.2525, 0.6, 631200, 'highpass', 5000), 0, 1.6), _at(_sweep('sine', 1500, 1700, 1.5, 0.101, 0.5), 0, 1.6), _at(_sweep('sine', 1510, 1690, 1.5, 0.101, 0.5), 0.05, 1.6),
        _at(_noise(1.5, 0.3366, 0.6, 631203, 'bandpass', 400), 0, 1.6), _at(_tone('sine', 220, 1.4, 0.1683, 0.4), 0, 1.6), _at(_tone('sine', 3000, 0.3, 0.0505, 0.05), 0.7, 1.6),
    ]
    return _finalize(_mix(*L))
def env_jungle_rain_001():
    L = [
        _at(_noise(1.5, 0.3876, 0.5, 631300, 'highpass', 3500), 0, 1.6), _at(_noise(1.5, 0.3876, 0.5, 631301, 'bandpass', 2500), 0, 1.6), _at(_noise(1.5, 0.1938, 0.5, 631302, 'lowpass', 500), 0, 1.6),
        _at(_tone('sine', 1200, 0.02, 0.1034, 0.003), 0.1, 1.6), _at(_tone('sine', 1200, 0.02, 0.1034, 0.003), 0.35, 1.6), _at(_tone('sine', 1200, 0.02, 0.1034, 0.003), 0.6, 1.6),
        _at(_tone('sine', 1200, 0.02, 0.1034, 0.003), 0.85, 1.6), _at(_tone('sine', 1200, 0.02, 0.1034, 0.003), 1.1, 1.6), _at(_tone('sine', 1200, 0.02, 0.1034, 0.003), 1.35, 1.6),
        _at(_sweep('sine', 2400, 3200, 0.08, 0.0775, 0.003), 0.3, 1.6), _at(_sweep('sine', 2400, 3200, 0.08, 0.0775, 0.003), 0.45, 1.6), _at(_sweep('sine', 2400, 3200, 0.08, 0.0775, 0.003), 1, 1.6),
        _at(_sweep('sine', 2200, 2800, 0.08, 0.0775, 0.003), 1.2, 1.6),
    ]
    return _finalize(_mix(*L))
def env_solar_flare_wind_001():
    L = [
        _at(_noise(1.5, 0.5304, 0.6, 631400, 'bandpass', 1500), 0, 1.6), _at(_sweep('sine', 150, 1500, 1.4, 0.1768, 0.5), 0, 1.6), _at(_sweep('sawtooth', 80, 160, 1.5, 0.1061, 0.5), 0, 1.6),
        _at(_noise(1.4, 0.2652, 0.6, 631403, 'highpass', 4000), 0.1, 1.6), _at(_noise(0.01, 0.2122, 0.002, 631404, 'highpass', 5000), 0.3, 1.6), _at(_noise(0.01, 0.2122, 0.002, 631405, 'highpass', 5000), 0.5, 1.6),
        _at(_noise(0.01, 0.2122, 0.002, 631406, 'highpass', 5000), 0.7, 1.6), _at(_noise(0.01, 0.2122, 0.002, 631407, 'highpass', 5000), 0.9, 1.6), _at(_noise(0.01, 0.2122, 0.002, 631408, 'highpass', 5000), 1.1, 1.6),
    ]
    return _finalize(_mix(*L))
def env_swamp_ambience_001():
    L = [
        _at(_noise(1.5, 0.6244, 0.5, 631500, 'lowpass', 300), 0, 1.6), _at(_tone('sine', 55, 1.5, 0.2676, 0.4), 0, 1.6), _at(_noise(1.5, 0.2141, 0.5, 631502, 'bandpass', 600), 0, 1.6),
        _at(_sweep('sawtooth', 120, 90, 0.12, 0.2141, 0.01), 0.5, 1.6), _at(_sweep('sawtooth', 120, 90, 0.12, 0.2141, 0.01), 1.2, 1.6), _at(_sweep('sine', 200, 400, 0.08, 0.3568, 0.003), 0.1, 1.6),
        _at(_sweep('sine', 200, 400, 0.08, 0.3568, 0.003), 0.4, 1.6), _at(_sweep('sine', 200, 400, 0.08, 0.3568, 0.003), 0.75, 1.6), _at(_sweep('sine', 200, 400, 0.08, 0.3568, 0.003), 1.1, 1.6),
    ]
    return _finalize(_mix(*L))
def env_waterfall_misty_001():
    L = [
        _at(_noise(1.5, 0.5864, 0.4, 631600, 'bandpass', 3000), 0, 1.6), _at(_noise(1.5, 0.2199, 0.4, 631601, 'highpass', 7000), 0, 1.6), _at(_noise(1.5, 0.4398, 0.4, 631602, 'lowpass', 700), 0, 1.6),
        _at(_tone('sine', 60, 1.5, 0.1466, 0.4), 0, 1.6),
    ]
    return _finalize(_mix(*L))
def epic_ancient_awakens_001():
    L = [
        _at(_tone('sine', 45, 1.5, 0.4, 0.5), 0, 1.6), _at(_tone('sawtooth', 90, 1.5, 0.15, 0.6), 0, 1.6), _at(_tone('sawtooth', 135, 1.5, 0.08, 0.7), 0, 1.6),
        _at(_sweep('sine', 100, 400, 1.2, 0.15, 0.4), 0, 1.6), _at(_sweep('sine', 60, 35, 0.3, 0.4, 0.005), 1, 1.6), _at(_tone('sine', 220, 1.3, 0.1, 0.6), 0.3, 1.6),
        _at(_tone('sine', 277, 1.3, 0.1, 0.6), 0.3, 1.6), _at(_noise(1.5, 0.15, 0.6, 631707, 'bandpass', 500), 0, 1.6),
    ]
    return _finalize(_mix(*L))
def forge_workshop_ambience_001():
    L = [
        _at(_noise(1.5, 0.6212, 0.4, 631800, 'lowpass', 500), 0, 1.6), _at(_tone('sine', 70, 1.5, 0.2485, 0.4), 0, 1.6), _at(_noise(0.5, 0.497, 0.15, 631802, 'bandpass', 700), 0.5, 1.6),
        _at(_noise(0.01, 0.497, 0.002, 631803, 'bandpass', 3000), 0.1, 1.6), _at(_noise(0.01, 0.497, 0.002, 631804, 'bandpass', 3000), 0.25, 1.6), _at(_noise(0.01, 0.497, 0.002, 631805, 'bandpass', 3000), 0.4, 1.6),
        _at(_noise(0.01, 0.497, 0.002, 631806, 'bandpass', 3000), 0.62, 1.6), _at(_noise(0.01, 0.497, 0.002, 631807, 'bandpass', 3000), 0.7, 1.6), _at(_noise(0.01, 0.497, 0.002, 631808, 'bandpass', 3000), 0.95, 1.6),
        _at(_noise(0.01, 0.497, 0.002, 631809, 'bandpass', 3000), 1.1, 1.6), _at(_noise(0.01, 0.497, 0.002, 631810, 'bandpass', 3000), 1.25, 1.6), _at(_noise(0.01, 0.497, 0.002, 631811, 'bandpass', 3000), 1.4, 1.6),
        _at(_tone('sine', 1800, 0.15, 0.2485, 0.003), 0.3, 1.6), _at(_tone('sine', 1800, 0.15, 0.2485, 0.003), 0.8, 1.6), _at(_tone('sine', 1800, 0.15, 0.2485, 0.003), 1.3, 1.6),
        _at(_noise(0.01, 0.3727, 0.002, 631815, 'bandpass', 2500), 0.3, 1.6), _at(_noise(0.01, 0.3727, 0.002, 631816, 'bandpass', 2500), 0.8, 1.6), _at(_noise(0.01, 0.3727, 0.002, 631817, 'bandpass', 2500), 1.3, 1.6),
    ]
    return _finalize(_mix(*L))
def infra_runway_jet_001():
    L = [
        _at(_noise(1.5, 0.4, 0.7, 631900, 'bandpass', 1200), 0, 1.6), _at(_noise(1.5, 0.3, 0.7, 631901, 'highpass', 3000), 0, 1.6), _at(_sweep('sine', 600, 1200, 1.4, 0.1, 0.7), 0, 1.6),
        _at(_noise(1.5, 0.45, 0.6, 631903, 'lowpass', 400), 0, 1.6), _at(_tone('sine', 90, 1.5, 0.15, 0.5), 0, 1.6),
    ]
    return _finalize(_mix(*L))
def infra_tunnel_wind_001():
    L = [
        _at(_noise(1.5, 0.9125, 0.6, 632000, 'bandpass', 500), 0, 1.6), _at(_sweep('sine', 300, 400, 1.4, 0.1825, 0.6), 0, 1.6), _at(_sweep('sine', 450, 520, 1.4, 0.146, 0.6), 0, 1.6),
        _at(_noise(1.5, 0.5475, 0.6, 632003, 'lowpass', 250), 0, 1.6), _at(_sweep('sine', 900, 1100, 1, 0.073, 0.4), 0.3, 1.6),
    ]
    return _finalize(_mix(*L))
def ruin_temple_wind_001():
    L = [
        _at(_noise(1.5, 0.7596, 0.6, 632100, 'bandpass', 700), 0, 1.6), _at(_sweep('sine', 330, 350, 1.5, 0.1519, 0.6), 0, 1.6), _at(_tone('sine', 495, 1.5, 0.095, 0.6), 0, 1.6),
        _at(_noise(1.5, 0.3798, 0.5, 632103, 'lowpass', 300), 0, 1.6), _at(_tone('sine', 110, 1.5, 0.1899, 0.5), 0, 1.6), _at(_noise(0.01, 0.1519, 0.002, 632105, 'bandpass', 2500), 0.5, 1.6),
        _at(_noise(0.01, 0.1519, 0.002, 632106, 'bandpass', 2500), 0.9, 1.6), _at(_noise(0.01, 0.1519, 0.002, 632107, 'bandpass', 2500), 1.2, 1.6),
    ]
    return _finalize(_mix(*L))
def env_meteor_shower_distant_001():
    L = [
        _at(_noise(0.6, 0.5507, 0.25, 632200, 'bandpass', 1500), 0, 1.3), _at(_noise(0.5, 0.3304, 0.2, 632201, 'highpass', 4000), 0.4, 1.3), _at(_noise(0.5, 0.4406, 0.2, 632202, 'bandpass', 2000), 0.7, 1.3),
        _at(_noise(1.2, 0.4406, 0.4, 632203, 'lowpass', 800), 0, 1.3), _at(_sweep('sine', 60, 40, 0.15, 0.3304, 0.01), 0.55, 1.3), _at(_sweep('sine', 60, 40, 0.15, 0.3304, 0.01), 1.1, 1.3),
        _at(_tone('sine', 80, 1.2, 0.2203, 0.3), 0, 1.3),
    ]
    return _finalize(_mix(*L))
def infra_bridge_lift_001():
    L = [
        _at(_sweep('sawtooth', 60, 90, 1, 0.2103, 0.1), 0, 1.3), _at(_sweep('sine', 120, 180, 1, 0.1402, 0.1), 0, 1.3), _at(_noise(1, 0.4206, 0.2, 632302, 'bandpass', 500), 0, 1.3),
        _at(_sweep('sawtooth', 90, 120, 0.6, 0.1682, 0.1), 0.55, 1.3), _at(_noise(0.55, 0.3505, 0.1, 632304, 'bandpass', 600), 0.55, 1.3), _at(_sweep('sine', 100, 70, 0.1, 0.5608, 0.002), 0, 1.3),
        _at(_sweep('sawtooth', 200, 280, 0.3, 0.1122, 0.05), 0.3, 1.3), _at(_sweep('sine', 70, 45, 0.15, 0.5608, 0.002), 1.1, 1.3), _at(_noise(0.1, 0.4206, 0.002, 632308, 'lowpass', 300), 1.1, 1.3),
        _at(_noise(0.02, 0.2103, 0.002, 632309, 'bandpass', 2000), 0.2, 1.3), _at(_noise(0.02, 0.2103, 0.002, 632310, 'bandpass', 2000), 0.4, 1.3), _at(_noise(0.02, 0.2103, 0.002, 632311, 'bandpass', 2000), 0.6, 1.3),
        _at(_noise(0.02, 0.2103, 0.002, 632312, 'bandpass', 2000), 0.8, 1.3),
    ]
    return _finalize(_mix(*L))
def meteor_shower_pass_001():
    L = [
        _at(_noise(0.5, 0.4977, 0.2, 632400, 'highpass', 3000), 0, 1.3), _at(_sweep('sine', 2000, 500, 0.5, 0.1659, 0.01), 0, 1.3), _at(_sweep('sine', 2500, 700, 0.5, 0.1659, 0.01), 0.45, 1.3),
        _at(_noise(0.5, 0.4148, 0.2, 632403, 'bandpass', 1800), 0.45, 1.3), _at(_sweep('sine', 3000, 1000, 0.4, 0.1327, 0.01), 0.85, 1.3), _at(_noise(0.4, 0.3318, 0.15, 632405, 'highpass', 4000), 0.85, 1.3),
        _at(_noise(1.2, 0.3318, 0.4, 632406, 'lowpass', 300), 0, 1.3), _at(_noise(0.01, 0.1659, 0.002, 632407, 'highpass', 6000), 0.1, 1.3), _at(_noise(0.01, 0.1659, 0.002, 632408, 'highpass', 6000), 0.55, 1.3),
        _at(_noise(0.01, 0.1659, 0.002, 632409, 'highpass', 6000), 0.95, 1.3),
    ]
    return _finalize(_mix(*L))

OFFICIAL_PRESETS_G1_M3 = {
    'env-aurora-borealis-001': env_aurora_borealis_001,
    'env-blizzard-001': env_blizzard_001,
    'env-floating-islands-001': env_floating_islands_001,
    'env-river-flow-001': env_river_flow_001,
    'env-sandstorm-distant-001': env_sandstorm_distant_001,
    'env-waterfall-001': env_waterfall_001,
    'infra-highway-traffic-001': infra_highway_traffic_001,
    'infra-tunnel-ambience-001': infra_tunnel_ambience_001,
    'nebula-ambience-001': nebula_ambience_001,
    'black-hole-collapse-001': black_hole_collapse_001,
    'env-bioluminescent-forest-001': env_bioluminescent_forest_001,
    'env-crystal-cave-hum-001': env_crystal_cave_hum_001,
    'env-desert-mirage-shimmer-001': env_desert_mirage_shimmer_001,
    'env-jungle-rain-001': env_jungle_rain_001,
    'env-solar-flare-wind-001': env_solar_flare_wind_001,
    'env-swamp-ambience-001': env_swamp_ambience_001,
    'env-waterfall-misty-001': env_waterfall_misty_001,
    'epic-ancient-awakens-001': epic_ancient_awakens_001,
    'forge-workshop-ambience-001': forge_workshop_ambience_001,
    'infra-runway-jet-001': infra_runway_jet_001,
    'infra-tunnel-wind-001': infra_tunnel_wind_001,
    'ruin-temple-wind-001': ruin_temple_wind_001,
    'env-meteor-shower-distant-001': env_meteor_shower_distant_001,
    'infra-bridge-lift-001': infra_bridge_lift_001,
    'meteor-shower-pass-001': meteor_shower_pass_001,
}
