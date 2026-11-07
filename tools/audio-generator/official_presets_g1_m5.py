"""Generation 1 - module 5 : sons reconstruits (son WAV + apercu navigateur)."""
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

def ruin_archaeological_scan_001():
    L = [
        _at(_sweep('sine', 800, 2400, 0.4, 0.3564, 0.02), 0, 0.9), _at(_sweep('sine', 800, 2400, 0.4, 0.1782, 0.02), 0.4, 0.9), _at(_tone('sine', 120, 0.85, 0.2138, 0.1), 0, 0.9),
        _at(_noise(0.85, 0.2138, 0.2, 650003, 'bandpass', 2500), 0, 0.9), _at(_tone('sine', 1800, 0.05, 0.2673, 0.003), 0.15, 0.9), _at(_tone('sine', 1800, 0.05, 0.2673, 0.003), 0.3, 0.9),
        _at(_tone('sine', 1800, 0.05, 0.2673, 0.003), 0.55, 0.9), _at(_tone('sine', 1800, 0.05, 0.2673, 0.003), 0.7, 0.9), _at(_tone('sine', 1800, 0.05, 0.2673, 0.003), 0.8, 0.9),
    ]
    return _finalize(_mix(*L))
def ruin_artifact_beam_001():
    L = [
        _at(_sweep('sine', 200, 1000, 0.4, 0.3255, 0.05), 0, 0.9), _at(_sweep('sawtooth', 100, 500, 0.4, 0.1042, 0.05), 0, 0.9), _at(_tone('sine', 600, 0.5, 0.2344, 0.05), 0.35, 0.9),
        _at(_tone('sine', 604, 0.5, 0.2344, 0.05), 0.35, 0.9), _at(_tone('sine', 1200, 0.5, 0.1042, 0.05), 0.35, 0.9), _at(_noise(0.8, 0.1302, 0.1, 650105, 'highpass', 5000), 0, 0.9),
        _at(_tone('sine', 80, 0.85, 0.1953, 0.1), 0, 0.9),
    ]
    return _finalize(_mix(*L))
def ruin_sarcophagus_open_001():
    L = [
        _at(_noise(0.6, 0.634, 0.1, 650200, 'bandpass', 250), 0, 0.9), _at(_noise(0.65, 0.634, 0.1, 650201, 'lowpass', 120), 0, 0.9), _at(_sweep('sawtooth', 50, 65, 0.6, 0.1014, 0.1), 0, 0.9),
        _at(_noise(0.3, 0.1522, 0.1, 650203, 'highpass', 3500), 0.1, 0.9), _at(_noise(0.35, 0.5072, 0.05, 650204, 'bandpass', 250), 0.35, 0.9), _at(_sweep('sine', 55, 38, 0.3, 0.5072, 0.002), 0.47, 0.9),
        _at(_noise(0.3, 0.4438, 0.002, 650206, 'lowpass', 250), 0.47, 0.9), _at(_noise(0.03, 0.1268, 0.002, 650207, 'bandpass', 2200), 0.15, 0.9), _at(_noise(0.03, 0.1268, 0.002, 650208, 'bandpass', 2200), 0.35, 0.9),
        _at(_noise(0.03, 0.1268, 0.002, 650209, 'bandpass', 2200), 0.55, 0.9),
    ]
    return _finalize(_mix(*L))
def ruin_secret_wall_slide_001():
    L = [
        _at(_noise(0.8, 0.7755, 0.15, 650300, 'bandpass', 200), 0, 0.9), _at(_noise(0.85, 0.705, 0.15, 650301, 'lowpass', 100), 0, 0.9), _at(_sweep('sawtooth', 48, 60, 0.8, 0.141, 0.15), 0, 0.9),
        _at(_sweep('sine', 55, 40, 0.2, 0.564, 0.002), 0.6, 0.9), _at(_noise(0.15, 0.423, 0.002, 650304, 'lowpass', 300), 0.6, 0.9), _at(_noise(0.03, 0.141, 0.002, 650305, 'bandpass', 2000), 0.1, 0.9),
        _at(_noise(0.03, 0.141, 0.002, 650306, 'bandpass', 2000), 0.25, 0.9), _at(_noise(0.03, 0.141, 0.002, 650307, 'bandpass', 2000), 0.4, 0.9), _at(_noise(0.03, 0.141, 0.002, 650308, 'bandpass', 2000), 0.55, 0.9),
        _at(_noise(0.03, 0.141, 0.002, 650309, 'bandpass', 2000), 0.7, 0.9),
    ]
    return _finalize(_mix(*L))
def snake_hiss_long_001():
    L = [
        _at(_noise(0.85, 0.4, 0.15, 650400, 'highpass', 4000), 0, 0.9), _at(_noise(0.85, 0.3, 0.15, 650401, 'bandpass', 6000), 0, 0.9), _at(_noise(0.85, 0.15, 0.15, 650402, 'bandpass', 3000), 0, 0.9),
        _at(_sweep('sine', 4500, 5200, 0.8, 0.04, 0.15), 0, 0.9), _at(_noise(0.03, 0.12, 0.002, 650404, 'highpass', 5000), 0.1, 0.9), _at(_noise(0.03, 0.12, 0.002, 650405, 'highpass', 5000), 0.3, 0.9),
        _at(_noise(0.03, 0.12, 0.002, 650406, 'highpass', 5000), 0.5, 0.9), _at(_noise(0.03, 0.12, 0.002, 650407, 'highpass', 5000), 0.7, 0.9),
    ]
    return _finalize(_mix(*L))
def sub_ballast_blow_001():
    L = [
        _at(_noise(0.8, 0.45, 0.03, 650500, 'highpass', 1500), 0, 0.9), _at(_noise(0.8, 0.35, 0.03, 650501, 'bandpass', 800), 0, 0.9), _at(_sweep('sine', 90, 60, 0.12, 0.35, 0.002), 0, 0.9),
        _at(_tone('sine', 200, 0.8, 0.06, 0.05), 0, 0.9), _at(_noise(0.6, 0.25, 0.05, 650504, 'lowpass', 400), 0, 0.9), _at(_noise(0.04, 0.2, 0.002, 650505, 'bandpass', 2500), 0, 0.9),
        _at(_noise(0.04, 0.2, 0.002, 650506, 'bandpass', 2500), 0.25, 0.9), _at(_noise(0.04, 0.2, 0.002, 650507, 'bandpass', 2500), 0.5, 0.9),
    ]
    return _finalize(_mix(*L))
def sub_engine_reverse_001():
    L = [
        _at(_sweep('sawtooth', 100, 45, 0.5, 0.4785, 0.02), 0, 0.9), _at(_sweep('square', 200, 90, 0.5, 0.1531, 0.02), 0, 0.9), _at(_sweep('sawtooth', 45, 110, 0.5, 0.4785, 0.2), 0.4, 0.9),
        _at(_sweep('square', 90, 220, 0.5, 0.1531, 0.2), 0.4, 0.9), _at(_noise(0.85, 0.5742, 0.2, 650604, 'lowpass', 400), 0, 0.9), _at(_noise(0.85, 0.2871, 0.3, 650605, 'bandpass', 700), 0, 0.9),
        _at(_noise(0.04, 0.3828, 0.002, 650606, 'lowpass', 300), 0.1, 0.9), _at(_noise(0.04, 0.3828, 0.002, 650607, 'lowpass', 300), 0.25, 0.9), _at(_noise(0.04, 0.3828, 0.002, 650608, 'lowpass', 300), 0.4, 0.9),
        _at(_noise(0.04, 0.3828, 0.002, 650609, 'lowpass', 300), 0.55, 0.9), _at(_noise(0.04, 0.3828, 0.002, 650610, 'lowpass', 300), 0.7, 0.9),
    ]
    return _finalize(_mix(*L))
def unique_alchemy_brew_001():
    L = [
        _at(_noise(0.85, 0.365, 0.2, 650700, 'bandpass', 1200), 0, 0.9), _at(_noise(0.85, 0.2737, 0.2, 650701, 'lowpass', 500), 0, 0.9), _at(_sweep('sine', 220, 330, 0.8, 0.146, 0.2), 0, 0.9),
        _at(_sweep('sine', 330, 440, 0.7, 0.1095, 0.25), 0.1, 0.9), _at(_tone('sine', 1760, 0.35, 0.1095, 0.003), 0.55, 0.9), _at(_sweep('sine', 400, 900, 0.05, 0.4562, 0.003), 0.08, 0.9),
        _at(_sweep('sine', 400, 900, 0.05, 0.4562, 0.003), 0.2, 0.9), _at(_sweep('sine', 400, 900, 0.05, 0.4562, 0.003), 0.33, 0.9), _at(_sweep('sine', 400, 900, 0.05, 0.4562, 0.003), 0.46, 0.9),
        _at(_sweep('sine', 400, 900, 0.05, 0.4562, 0.003), 0.6, 0.9), _at(_sweep('sine', 400, 900, 0.05, 0.4562, 0.003), 0.72, 0.9), _at(_sweep('sine', 700, 1300, 0.04, 0.3285, 0.003), 0.14, 0.9),
        _at(_sweep('sine', 700, 1300, 0.04, 0.3285, 0.003), 0.27, 0.9), _at(_sweep('sine', 700, 1300, 0.04, 0.3285, 0.003), 0.4, 0.9), _at(_sweep('sine', 700, 1300, 0.04, 0.3285, 0.003), 0.53, 0.9),
        _at(_sweep('sine', 700, 1300, 0.04, 0.3285, 0.003), 0.66, 0.9), _at(_sweep('sine', 700, 1300, 0.04, 0.3285, 0.003), 0.8, 0.9),
    ]
    return _finalize(_mix(*L))
def creepy_whisper_001():
    L = [
        _at(_noise(0.7, 0.4809, 0.2, 650800, 'bandpass', 3500), 0, 0.8), _at(_noise(0.7, 0.3206, 0.2, 650801, 'highpass', 5000), 0, 0.8), _at(_noise(0.3, 0.4007, 0.1, 650802, 'bandpass', 2500), 0.45, 0.8),
        _at(_noise(0.3, 0.3206, 0.1, 650803, 'highpass', 4500), 0.45, 0.8), _at(_sweep('sine', 180, 160, 0.75, 0.0801, 0.15), 0, 0.8), _at(_sweep('sine', 3500, 2800, 0.5, 0.0481, 0.1), 0.1, 0.8),
    ]
    return _finalize(_mix(*L))
def environment_wind_gust_001():
    L = [
        _at(_noise(0.75, 0.7887, 0.3, 650900, 'bandpass', 800), 0, 0.8), _at(_noise(0.75, 0.5736, 0.3, 650901, 'lowpass', 400), 0, 0.8), _at(_noise(0.7, 0.2868, 0.3, 650902, 'highpass', 2500), 0, 0.8),
        _at(_sweep('sine', 350, 480, 0.7, 0.086, 0.3), 0, 0.8), _at(_tone('sine', 60, 0.7, 0.1434, 0.2), 0, 0.8),
    ]
    return _finalize(_mix(*L))
def night_insects_001():
    L = [
        _at(_tone('sine', 4200, 0.7, 0.1558, 0.05), 0, 0.8), _at(_tone('sine', 4650, 0.7, 0.1558, 0.05), 0, 0.8), _at(_tone('sine', 5100, 0.7, 0.1113, 0.05), 0, 0.8),
        _at(_noise(0.75, 0.3337, 0.1, 651003, 'bandpass', 4500), 0, 0.8), _at(_noise(0.03, 0.5563, 0.002, 651004, 'bandpass', 4300), 0, 0.8), _at(_noise(0.03, 0.5563, 0.002, 651005, 'bandpass', 4300), 0.06, 0.8),
        _at(_noise(0.03, 0.5563, 0.002, 651006, 'bandpass', 4300), 0.12, 0.8), _at(_noise(0.03, 0.5563, 0.002, 651007, 'bandpass', 4300), 0.18, 0.8), _at(_noise(0.03, 0.5563, 0.002, 651008, 'bandpass', 4300), 0.24, 0.8),
        _at(_noise(0.03, 0.5563, 0.002, 651009, 'bandpass', 4300), 0.3, 0.8), _at(_noise(0.03, 0.5563, 0.002, 651010, 'bandpass', 4300), 0.36, 0.8), _at(_noise(0.03, 0.5563, 0.002, 651011, 'bandpass', 4300), 0.42, 0.8),
        _at(_noise(0.03, 0.5563, 0.002, 651012, 'bandpass', 4300), 0.48, 0.8), _at(_noise(0.03, 0.5563, 0.002, 651013, 'bandpass', 4300), 0.54, 0.8), _at(_noise(0.03, 0.5563, 0.002, 651014, 'bandpass', 4300), 0.6, 0.8),
        _at(_noise(0.03, 0.5563, 0.002, 651015, 'bandpass', 4300), 0.66, 0.8), _at(_noise(0.03, 0.445, 0.002, 651016, 'bandpass', 5200), 0.02, 0.8), _at(_noise(0.03, 0.445, 0.002, 651017, 'bandpass', 5200), 0.11, 0.8),
        _at(_noise(0.03, 0.445, 0.002, 651018, 'bandpass', 5200), 0.2, 0.8), _at(_noise(0.03, 0.445, 0.002, 651019, 'bandpass', 5200), 0.29, 0.8), _at(_noise(0.03, 0.445, 0.002, 651020, 'bandpass', 5200), 0.38, 0.8),
        _at(_noise(0.03, 0.445, 0.002, 651021, 'bandpass', 5200), 0.47, 0.8), _at(_noise(0.03, 0.445, 0.002, 651022, 'bandpass', 5200), 0.56, 0.8), _at(_noise(0.03, 0.445, 0.002, 651023, 'bandpass', 5200), 0.65, 0.8),
    ]
    return _finalize(_mix(*L))
def space_station_alarm_001():
    L = [
        _at(_tone('square', 880, 0.18, 0.2884, 0.005), 0, 0.8), _at(_tone('square', 880, 0.18, 0.2884, 0.005), 0.4, 0.8), _at(_tone('square', 660, 0.18, 0.2884, 0.005), 0.2, 0.8),
        _at(_tone('square', 660, 0.18, 0.2884, 0.005), 0.6, 0.8), _at(_tone('sawtooth', 440, 0.18, 0.1049, 0.005), 0, 0.8), _at(_tone('sawtooth', 440, 0.18, 0.1049, 0.005), 0.4, 0.8),
        _at(_tone('sawtooth', 330, 0.18, 0.1049, 0.005), 0.2, 0.8), _at(_tone('sawtooth', 330, 0.18, 0.1049, 0.005), 0.6, 0.8), _at(_sweep('sawtooth', 70, 60, 0.75, 0.1311, 0.1), 0, 0.8),
        _at(_noise(0.75, 0.1311, 0.1, 651109, 'lowpass', 400), 0, 0.8), _at(_tone('sine', 110, 0.75, 0.1049, 0.1), 0, 0.8),
    ]
    return _finalize(_mix(*L))
def body_roll_gravel_001():
    L = [
        _at(_noise(0.65, 0.4496, 0.05, 651200, 'bandpass', 2500), 0, 0.7), _at(_noise(0.65, 0.3372, 0.05, 651201, 'highpass', 3500), 0, 0.7), _at(_noise(0.5, 0.3372, 0.05, 651202, 'lowpass', 500), 0, 0.7),
        _at(_sweep('sine', 80, 55, 0.12, 0.3372, 0.003), 0.05, 0.7), _at(_noise(0.015, 0.3372, 0.002, 651204, 'bandpass', 3000), 0.02, 0.7), _at(_noise(0.015, 0.3372, 0.002, 651205, 'bandpass', 3000), 0.065, 0.7),
        _at(_noise(0.015, 0.3372, 0.002, 651206, 'bandpass', 3000), 0.11, 0.7), _at(_noise(0.015, 0.3372, 0.002, 651207, 'bandpass', 3000), 0.155, 0.7), _at(_noise(0.015, 0.3372, 0.002, 651208, 'bandpass', 3000), 0.2, 0.7),
        _at(_noise(0.015, 0.3372, 0.002, 651209, 'bandpass', 3000), 0.245, 0.7), _at(_noise(0.015, 0.3372, 0.002, 651210, 'bandpass', 3000), 0.29, 0.7), _at(_noise(0.015, 0.3372, 0.002, 651211, 'bandpass', 3000), 0.335, 0.7),
        _at(_noise(0.015, 0.3372, 0.002, 651212, 'bandpass', 3000), 0.38, 0.7), _at(_noise(0.015, 0.3372, 0.002, 651213, 'bandpass', 3000), 0.425, 0.7), _at(_noise(0.015, 0.3372, 0.002, 651214, 'bandpass', 3000), 0.47, 0.7),
        _at(_noise(0.015, 0.3372, 0.002, 651215, 'bandpass', 3000), 0.515, 0.7), _at(_noise(0.015, 0.3372, 0.002, 651216, 'bandpass', 3000), 0.56, 0.7), _at(_noise(0.015, 0.3372, 0.002, 651217, 'bandpass', 3000), 0.605, 0.7),
        _at(_sweep('sine', 110, 70, 0.04, 0.1349, 0.003), 0.15, 0.7), _at(_sweep('sine', 110, 70, 0.04, 0.1349, 0.003), 0.35, 0.7), _at(_sweep('sine', 110, 70, 0.04, 0.1349, 0.003), 0.55, 0.7),
    ]
    return _finalize(_mix(*L))
def crocodile_water_movement_001():
    L = [
        _at(_noise(0.65, 0.5916, 0.15, 651300, 'lowpass', 600), 0, 0.7), _at(_noise(0.65, 0.4437, 0.15, 651301, 'bandpass', 1200), 0, 0.7), _at(_sweep('sine', 70, 50, 0.65, 0.2219, 0.1), 0, 0.7),
        _at(_sweep('sine', 300, 700, 0.06, 0.3698, 0.003), 0.05, 0.7), _at(_sweep('sine', 300, 700, 0.06, 0.3698, 0.003), 0.2, 0.7), _at(_sweep('sine', 300, 700, 0.06, 0.3698, 0.003), 0.38, 0.7),
        _at(_sweep('sine', 300, 700, 0.06, 0.3698, 0.003), 0.5, 0.7), _at(_noise(0.02, 0.2219, 0.002, 651307, 'highpass', 4500), 0.1, 0.7), _at(_noise(0.02, 0.2219, 0.002, 651308, 'highpass', 4500), 0.3, 0.7),
        _at(_noise(0.02, 0.2219, 0.002, 651309, 'highpass', 4500), 0.45, 0.7), _at(_noise(0.02, 0.2219, 0.002, 651310, 'highpass', 4500), 0.58, 0.7),
    ]
    return _finalize(_mix(*L))
def duck_flock_takeoff_001():
    L = [
        _at(_sweep('sawtooth', 600, 450, 0.08, 0.313, 0.005), 0, 0.7), _at(_sweep('sawtooth', 600, 450, 0.08, 0.313, 0.005), 0.06, 0.7), _at(_sweep('sawtooth', 600, 450, 0.08, 0.313, 0.005), 0.13, 0.7),
        _at(_sweep('sawtooth', 600, 450, 0.08, 0.313, 0.005), 0.2, 0.7), _at(_sweep('sawtooth', 600, 450, 0.08, 0.313, 0.005), 0.28, 0.7), _at(_sweep('sawtooth', 600, 450, 0.08, 0.313, 0.005), 0.35, 0.7),
        _at(_sweep('sawtooth', 600, 450, 0.08, 0.313, 0.005), 0.45, 0.7), _at(_sweep('square', 300, 220, 0.08, 0.0939, 0.005), 0.02, 0.7), _at(_sweep('square', 300, 220, 0.08, 0.0939, 0.005), 0.1, 0.7),
        _at(_sweep('square', 300, 220, 0.08, 0.0939, 0.005), 0.22, 0.7), _at(_sweep('square', 300, 220, 0.08, 0.0939, 0.005), 0.38, 0.7), _at(_noise(0.65, 0.4695, 0.1, 651411, 'bandpass', 1500), 0, 0.7),
        _at(_noise(0.6, 0.3912, 0.1, 651412, 'lowpass', 500), 0, 0.7), _at(_noise(0.6, 0.313, 0.1, 651413, 'highpass', 3000), 0, 0.7), _at(_noise(0.03, 0.313, 0.002, 651414, 'bandpass', 2000), 0.1, 0.7),
        _at(_noise(0.03, 0.313, 0.002, 651415, 'bandpass', 2000), 0.2, 0.7), _at(_noise(0.03, 0.313, 0.002, 651416, 'bandpass', 2000), 0.3, 0.7), _at(_noise(0.03, 0.313, 0.002, 651417, 'bandpass', 2000), 0.4, 0.7),
        _at(_noise(0.03, 0.313, 0.002, 651418, 'bandpass', 2000), 0.5, 0.7), _at(_noise(0.03, 0.313, 0.002, 651419, 'bandpass', 2000), 0.6, 0.7),
    ]
    return _finalize(_mix(*L))
def elevator_mechanism_001():
    L = [
        _at(_sweep('sawtooth', 80, 130, 0.5, 0.2304, 0.05), 0, 0.7), _at(_sweep('square', 160, 260, 0.5, 0.0768, 0.05), 0, 0.7), _at(_noise(0.5, 0.384, 0.1, 651502, 'bandpass', 700), 0, 0.7),
        _at(_noise(0.6, 0.384, 0.1, 651503, 'lowpass', 250), 0, 0.7), _at(_tone('sine', 1500, 0.08, 0.2304, 0.003), 0.4, 0.7), _at(_sweep('sine', 80, 50, 0.15, 0.5376, 0.002), 0.46, 0.7),
        _at(_noise(0.02, 0.384, 0.001, 651506, 'bandpass', 1500), 0.46, 0.7), _at(_noise(0.02, 0.1843, 0.002, 651507, 'bandpass', 2000), 0.1, 0.7), _at(_noise(0.02, 0.1843, 0.002, 651508, 'bandpass', 2000), 0.25, 0.7),
        _at(_noise(0.02, 0.1843, 0.002, 651509, 'bandpass', 2000), 0.4, 0.7),
    ]
    return _finalize(_mix(*L))
def forge_anvil_ring_001():
    L = [
        _at(_tone('sine', 1100, 0.65, 0.3, 0.001), 0, 0.7), _at(_tone('sine', 2400, 0.5, 0.2, 0.001), 0, 0.7), _at(_tone('sine', 3500, 0.35, 0.1, 0.001), 0, 0.7),
        _at(_tone('sine', 1650, 0.5, 0.12, 0.001), 0, 0.7), _at(_noise(0.03, 0.5, 0.0005, 651604, 'bandpass', 3500), 0, 0.7), _at(_sweep('sine', 150, 90, 0.08, 0.3, 0.001), 0, 0.7),
        _at(_tone('sine', 560, 0.6, 0.1, 0.001), 0, 0.7),
    ]
    return _finalize(_mix(*L))
def forge_cooling_crackle_001():
    L = [
        _at(_noise(0.65, 0.3165, 0.05, 651700, 'highpass', 4000), 0, 0.7), _at(_noise(0.65, 0.2532, 0.05, 651701, 'bandpass', 2500), 0, 0.7), _at(_tone('sine', 120, 0.65, 0.1266, 0.1), 0, 0.7),
        _at(_noise(0.012, 0.844, 0.002, 651703, 'bandpass', 3500), 0.02, 0.7), _at(_noise(0.012, 0.844, 0.002, 651704, 'bandpass', 3500), 0.07, 0.7), _at(_noise(0.012, 0.844, 0.002, 651705, 'bandpass', 3500), 0.12, 0.7),
        _at(_noise(0.012, 0.844, 0.002, 651706, 'bandpass', 3500), 0.19, 0.7), _at(_noise(0.012, 0.844, 0.002, 651707, 'bandpass', 3500), 0.24, 0.7), _at(_noise(0.012, 0.844, 0.002, 651708, 'bandpass', 3500), 0.33, 0.7),
        _at(_noise(0.012, 0.844, 0.002, 651709, 'bandpass', 3500), 0.4, 0.7), _at(_noise(0.012, 0.844, 0.002, 651710, 'bandpass', 3500), 0.47, 0.7), _at(_noise(0.012, 0.844, 0.002, 651711, 'bandpass', 3500), 0.58, 0.7),
        _at(_sweep('sine', 2000, 3000, 0.015, 0.3165, 0.003), 0.05, 0.7), _at(_sweep('sine', 2000, 3000, 0.015, 0.3165, 0.003), 0.17, 0.7), _at(_sweep('sine', 2000, 3000, 0.015, 0.3165, 0.003), 0.3, 0.7),
        _at(_sweep('sine', 2000, 3000, 0.015, 0.3165, 0.003), 0.44, 0.7), _at(_sweep('sine', 2000, 3000, 0.015, 0.3165, 0.003), 0.55, 0.7),
    ]
    return _finalize(_mix(*L))
def forge_metal_bend_001():
    L = [
        _at(_sweep('sawtooth', 180, 130, 0.5, 0.2464, 0.05), 0, 0.7), _at(_sweep('sawtooth', 183, 133, 0.5, 0.2054, 0.05), 0, 0.7), _at(_sweep('square', 360, 260, 0.5, 0.0684, 0.05), 0, 0.7),
        _at(_noise(0.5, 0.3422, 0.1, 651803, 'bandpass', 1500), 0, 0.7), _at(_sweep('sine', 90, 60, 0.1, 0.5476, 0.002), 0.45, 0.7), _at(_noise(0.025, 0.4107, 0.001, 651805, 'bandpass', 2500), 0.45, 0.7),
        _at(_sweep('sine', 1200, 900, 0.2, 0.1369, 0.003), 0.48, 0.7), _at(_noise(0.02, 0.1643, 0.002, 651807, 'bandpass', 2200), 0.15, 0.7), _at(_noise(0.02, 0.1643, 0.002, 651808, 'bandpass', 2200), 0.3, 0.7),
    ]
    return _finalize(_mix(*L))
def forge_polish_leather_001():
    L = [
        _at(_noise(0.3, 0.8008, 0.1, 651900, 'lowpass', 1500), 0, 0.7), _at(_noise(0.3, 0.4576, 0.1, 651901, 'bandpass', 3000), 0, 0.7), _at(_noise(0.3, 0.8008, 0.1, 651902, 'lowpass', 1500), 0.25, 0.7),
        _at(_noise(0.3, 0.4576, 0.1, 651903, 'bandpass', 3000), 0.25, 0.7), _at(_sweep('sine', 250, 200, 0.3, 0.1373, 0.1), 0, 0.7), _at(_sweep('sine', 250, 200, 0.3, 0.1373, 0.1), 0.25, 0.7),
        _at(_noise(0.015, 0.2288, 0.002, 651906, 'bandpass', 4000), 0.1, 0.7), _at(_noise(0.015, 0.2288, 0.002, 651907, 'bandpass', 4000), 0.2, 0.7), _at(_noise(0.015, 0.2288, 0.002, 651908, 'bandpass', 4000), 0.35, 0.7),
        _at(_noise(0.015, 0.2288, 0.002, 651909, 'bandpass', 4000), 0.45, 0.7),
    ]
    return _finalize(_mix(*L))
def forge_quenching_sizzle_001():
    L = [
        _at(_noise(0.65, 0.5, 0.02, 652000, 'highpass', 3500), 0, 0.7), _at(_noise(0.65, 0.3, 0.02, 652001, 'bandpass', 6000), 0, 0.7), _at(_noise(0.4, 0.3, 0.02, 652002, 'lowpass', 800), 0, 0.7),
        _at(_sweep('sine', 120, 70, 0.08, 0.3, 0.002), 0, 0.7), _at(_sweep('sine', 300, 800, 0.3, 0.05, 0.02), 0, 0.7), _at(_noise(0.012, 0.2, 0.002, 652005, 'highpass', 5500), 0.1, 0.7),
        _at(_noise(0.012, 0.2, 0.002, 652006, 'highpass', 5500), 0.18, 0.7), _at(_noise(0.012, 0.2, 0.002, 652007, 'highpass', 5500), 0.28, 0.7), _at(_noise(0.012, 0.2, 0.002, 652008, 'highpass', 5500), 0.36, 0.7),
        _at(_noise(0.012, 0.2, 0.002, 652009, 'highpass', 5500), 0.45, 0.7), _at(_noise(0.012, 0.2, 0.002, 652010, 'highpass', 5500), 0.55, 0.7),
    ]
    return _finalize(_mix(*L))
def futuristic_surgery_001():
    L = [
        _at(_sweep('sine', 4000, 4600, 0.35, 0.2364, 0.03), 0, 0.7), _at(_sweep('sawtooth', 300, 500, 0.35, 0.1182, 0.03), 0, 0.7), _at(_noise(0.35, 0.394, 0.05, 652102, 'bandpass', 3000), 0, 0.7),
        _at(_tone('sine', 2000, 0.1, 0.3546, 0.003), 0.26, 0.7), _at(_tone('sine', 2500, 0.1, 0.3546, 0.003), 0.4, 0.7), _at(_tone('sine', 1500, 0.1, 0.2955, 0.003), 0.5, 0.7),
        _at(_sweep('sine', 1000, 600, 0.3, 0.1576, 0.02), 0.28, 0.7), _at(_noise(0.08, 0.2364, 0.003, 652107, 'highpass', 6000), 0.28, 0.7),
    ]
    return _finalize(_mix(*L))
def infra_gate_open_001():
    L = [
        _at(_sweep('sawtooth', 90, 130, 0.5, 0.2009, 0.05), 0, 0.7), _at(_noise(0.5, 0.4017, 0.1, 652201, 'bandpass', 600), 0, 0.7), _at(_noise(0.55, 0.3347, 0.1, 652202, 'lowpass', 250), 0, 0.7),
        _at(_sweep('sine', 100, 70, 0.08, 0.5356, 0.002), 0, 0.7), _at(_noise(0.02, 0.3347, 0.001, 652204, 'bandpass', 1500), 0, 0.7), _at(_sweep('sine', 1000, 1300, 0.45, 0.0669, 0.1), 0, 0.7),
        _at(_sweep('sine', 70, 45, 0.15, 0.4017, 0.002), 0.4, 0.7), _at(_noise(0.02, 0.1339, 0.002, 652207, 'bandpass', 2000), 0.1, 0.7), _at(_noise(0.02, 0.1339, 0.002, 652208, 'bandpass', 2000), 0.2, 0.7),
        _at(_noise(0.02, 0.1339, 0.002, 652209, 'bandpass', 2000), 0.3, 0.7),
    ]
    return _finalize(_mix(*L))
def leaves_rustle_001():
    L = [
        _at(_noise(0.65, 0.3785, 0.1, 652300, 'highpass', 3000), 0, 0.7), _at(_noise(0.65, 0.3028, 0.1, 652301, 'bandpass', 4500), 0, 0.7), _at(_noise(0.65, 0.1817, 0.1, 652302, 'bandpass', 2000), 0, 0.7),
        _at(_noise(0.015, 0.3785, 0.002, 652303, 'highpass', 5000), 0.01, 0.7), _at(_noise(0.015, 0.3785, 0.002, 652304, 'highpass', 5000), 0.05, 0.7), _at(_noise(0.015, 0.3785, 0.002, 652305, 'highpass', 5000), 0.09, 0.7),
        _at(_noise(0.015, 0.3785, 0.002, 652306, 'highpass', 5000), 0.13, 0.7), _at(_noise(0.015, 0.3785, 0.002, 652307, 'highpass', 5000), 0.17, 0.7), _at(_noise(0.015, 0.3785, 0.002, 652308, 'highpass', 5000), 0.21, 0.7),
        _at(_noise(0.015, 0.3785, 0.002, 652309, 'highpass', 5000), 0.25, 0.7), _at(_noise(0.015, 0.3785, 0.002, 652310, 'highpass', 5000), 0.29, 0.7), _at(_noise(0.015, 0.3785, 0.002, 652311, 'highpass', 5000), 0.33, 0.7),
        _at(_noise(0.015, 0.3785, 0.002, 652312, 'highpass', 5000), 0.37, 0.7), _at(_noise(0.015, 0.3785, 0.002, 652313, 'highpass', 5000), 0.41, 0.7), _at(_noise(0.015, 0.3785, 0.002, 652314, 'highpass', 5000), 0.45, 0.7),
        _at(_noise(0.015, 0.3785, 0.002, 652315, 'highpass', 5000), 0.49, 0.7), _at(_noise(0.015, 0.3785, 0.002, 652316, 'highpass', 5000), 0.53, 0.7), _at(_noise(0.015, 0.3785, 0.002, 652317, 'highpass', 5000), 0.57, 0.7),
        _at(_noise(0.015, 0.3785, 0.002, 652318, 'highpass', 5000), 0.61, 0.7), _at(_noise(0.02, 0.2271, 0.002, 652319, 'bandpass', 3000), 0.03, 0.7), _at(_noise(0.02, 0.2271, 0.002, 652320, 'bandpass', 3000), 0.085, 0.7),
        _at(_noise(0.02, 0.2271, 0.002, 652321, 'bandpass', 3000), 0.14, 0.7), _at(_noise(0.02, 0.2271, 0.002, 652322, 'bandpass', 3000), 0.195, 0.7), _at(_noise(0.02, 0.2271, 0.002, 652323, 'bandpass', 3000), 0.25, 0.7),
        _at(_noise(0.02, 0.2271, 0.002, 652324, 'bandpass', 3000), 0.305, 0.7), _at(_noise(0.02, 0.2271, 0.002, 652325, 'bandpass', 3000), 0.36, 0.7), _at(_noise(0.02, 0.2271, 0.002, 652326, 'bandpass', 3000), 0.415, 0.7),
        _at(_noise(0.02, 0.2271, 0.002, 652327, 'bandpass', 3000), 0.47, 0.7), _at(_noise(0.02, 0.2271, 0.002, 652328, 'bandpass', 3000), 0.525, 0.7), _at(_noise(0.02, 0.2271, 0.002, 652329, 'bandpass', 3000), 0.58, 0.7),
    ]
    return _finalize(_mix(*L))
def mech_heavy_door_slide_001():
    L = [
        _at(_noise(0.55, 0.6102, 0.08, 652400, 'bandpass', 250), 0, 0.7), _at(_noise(0.55, 0.5424, 0.08, 652401, 'lowpass', 120), 0, 0.7), _at(_sweep('sawtooth', 55, 75, 0.55, 0.1356, 0.08), 0, 0.7),
        _at(_noise(0.5, 0.1356, 0.1, 652403, 'bandpass', 1200), 0, 0.7), _at(_sweep('sine', 65, 40, 0.2, 0.5424, 0.002), 0.38, 0.7), _at(_noise(0.2, 0.4068, 0.002, 652405, 'lowpass', 300), 0.38, 0.7),
        _at(_noise(0.03, 0.2034, 0.001, 652406, 'highpass', 3000), 0.38, 0.7), _at(_noise(0.03, 0.1356, 0.002, 652407, 'bandpass', 2000), 0.1, 0.7), _at(_noise(0.03, 0.1356, 0.002, 652408, 'bandpass', 2000), 0.22, 0.7),
        _at(_noise(0.03, 0.1356, 0.002, 652409, 'bandpass', 2000), 0.34, 0.7),
    ]
    return _finalize(_mix(*L))

OFFICIAL_PRESETS_G1_M5 = {
    'ruin-archaeological-scan-001': ruin_archaeological_scan_001,
    'ruin-artifact-beam-001': ruin_artifact_beam_001,
    'ruin-sarcophagus-open-001': ruin_sarcophagus_open_001,
    'ruin-secret-wall-slide-001': ruin_secret_wall_slide_001,
    'snake-hiss-long-001': snake_hiss_long_001,
    'sub-ballast-blow-001': sub_ballast_blow_001,
    'sub-engine-reverse-001': sub_engine_reverse_001,
    'unique-alchemy-brew-001': unique_alchemy_brew_001,
    'creepy-whisper-001': creepy_whisper_001,
    'environment-wind-gust-001': environment_wind_gust_001,
    'night-insects-001': night_insects_001,
    'space-station-alarm-001': space_station_alarm_001,
    'body-roll-gravel-001': body_roll_gravel_001,
    'crocodile-water-movement-001': crocodile_water_movement_001,
    'duck-flock-takeoff-001': duck_flock_takeoff_001,
    'elevator-mechanism-001': elevator_mechanism_001,
    'forge-anvil-ring-001': forge_anvil_ring_001,
    'forge-cooling-crackle-001': forge_cooling_crackle_001,
    'forge-metal-bend-001': forge_metal_bend_001,
    'forge-polish-leather-001': forge_polish_leather_001,
    'forge-quenching-sizzle-001': forge_quenching_sizzle_001,
    'futuristic-surgery-001': futuristic_surgery_001,
    'infra-gate-open-001': infra_gate_open_001,
    'leaves-rustle-001': leaves_rustle_001,
    'mech-heavy-door-slide-001': mech_heavy_door_slide_001,
}
