"""Generation 1 - module 4 : sons reconstruits (son WAV + apercu navigateur)."""
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

def ruin_ancient_door_close_001():
    L = [
        _at(_noise(1, 0.5, 0.1, 640000, 'bandpass', 200), 0, 1.3), _at(_noise(1.1, 0.5, 0.1, 640001, 'lowpass', 110), 0, 1.3), _at(_sweep('sine', 60, 45, 1, 0.25, 0.1), 0, 1.3),
        _at(_noise(0.5, 0.45, 0.1, 640003, 'bandpass', 200), 0.55, 1.3), _at(_noise(0.45, 0.45, 0.1, 640004, 'lowpass', 110), 0.55, 1.3), _at(_sweep('sine', 65, 30, 0.5, 0.5, 0.002), 0.78, 1.3),
        _at(_noise(0.3, 0.5, 0.002, 640006, 'lowpass', 250), 0.78, 1.3), _at(_noise(0.04, 0.15, 0.002, 640007, 'highpass', 3000), 0.78, 1.3), _at(_noise(0.04, 0.1, 0.002, 640008, 'bandpass', 1800), 0.2, 1.3),
        _at(_noise(0.04, 0.1, 0.002, 640009, 'bandpass', 1800), 0.45, 1.3), _at(_noise(0.04, 0.1, 0.002, 640010, 'bandpass', 1800), 0.7, 1.3),
    ]
    return _finalize(_mix(*L))
def ruin_ancient_door_open_001():
    L = [
        _at(_noise(1.2, 0.6605, 0.2, 640100, 'bandpass', 180), 0, 1.3), _at(_noise(1.25, 0.6605, 0.2, 640101, 'lowpass', 100), 0, 1.3), _at(_sweep('sawtooth', 45, 60, 1.2, 0.1321, 0.2), 0, 1.3),
        _at(_noise(0.6, 0.5945, 0.15, 640103, 'bandpass', 180), 0.4, 1.3), _at(_noise(0.55, 0.5945, 0.15, 640104, 'lowpass', 100), 0.4, 1.3), _at(_sweep('sine', 55, 40, 0.3, 0.5284, 0.002), 0, 1.3),
        _at(_sweep('sine', 50, 35, 0.45, 0.3963, 0.003), 0.8, 1.3), _at(_noise(0.3, 0.3963, 0.003, 640107, 'lowpass', 250), 0.8, 1.3), _at(_noise(0.15, 0.4623, 0.002, 640108, 'lowpass', 250), 0, 1.3),
        _at(_noise(0.04, 0.1321, 0.002, 640109, 'bandpass', 2200), 0.25, 1.3), _at(_noise(0.04, 0.1321, 0.002, 640110, 'bandpass', 2200), 0.5, 1.3), _at(_noise(0.04, 0.1321, 0.002, 640111, 'bandpass', 2200), 0.75, 1.3),
        _at(_noise(0.04, 0.1321, 0.002, 640112, 'bandpass', 2200), 0.95, 1.3),
    ]
    return _finalize(_mix(*L))
def ruin_temple_bell_001():
    L = [
        _at(_tone('sine', 392, 1.25, 0.3, 0.002), 0, 1.3), _at(_tone('sine', 784, 1, 0.15, 0.002), 0, 1.3), _at(_tone('sine', 1176, 0.8, 0.1, 0.002), 0, 1.3),
        _at(_tone('sine', 1030, 0.7, 0.07, 0.002), 0, 1.3), _at(_tone('sine', 395, 1.25, 0.2, 0.002), 0, 1.3), _at(_noise(0.04, 0.2, 0.001, 640205, 'bandpass', 2500), 0, 1.3),
        _at(_tone('sine', 196, 1.1, 0.12, 0.003), 0, 1.3),
    ]
    return _finalize(_mix(*L))
def ruin_temple_door_rumble_001():
    L = [
        _at(_noise(1.2, 0.7, 0.2, 640300, 'lowpass', 150), 0, 1.3), _at(_sweep('sine', 40, 55, 1.2, 0.35, 0.2), 0, 1.3), _at(_sweep('sawtooth', 38, 50, 1.2, 0.1, 0.2), 0, 1.3),
        _at(_noise(1.2, 0.35, 0.2, 640303, 'bandpass', 250), 0, 1.3), _at(_noise(0.1, 0.3, 0.002, 640304, 'lowpass', 300), 0.3, 1.3), _at(_noise(0.1, 0.3, 0.002, 640305, 'lowpass', 300), 0.6, 1.3),
        _at(_noise(0.1, 0.3, 0.002, 640306, 'lowpass', 300), 0.9, 1.3),
    ]
    return _finalize(_mix(*L))
def zero_gravity_float_001():
    L = [
        _at(_sweep('sine', 220, 260, 1.2, 0.193, 0.5), 0, 1.3), _at(_sweep('sine', 330, 390, 1.2, 0.1287, 0.5), 0, 1.3), _at(_noise(1.2, 0.193, 0.5, 640402, 'bandpass', 500), 0, 1.3),
        _at(_tone('sine', 55, 1.25, 0.193, 0.4), 0, 1.3), _at(_sweep('sine', 880, 1000, 0.8, 0.0644, 0.3), 0.2, 1.3), _at(_tone('sine', 1760, 0.4, 0.0644, 0.003), 0.6, 1.3),
    ]
    return _finalize(_mix(*L))
def whale_song_low_001():
    L = [
        _at(_sweep('sine', 80, 160, 0.6, 0.35, 0.15), 0, 1.2), _at(_sweep('sine', 160, 320, 0.6, 0.1, 0.15), 0, 1.2), _at(_sweep('sine', 150, 70, 0.55, 0.35, 0.1), 0.6, 1.2),
        _at(_sweep('sine', 300, 140, 0.55, 0.1, 0.1), 0.6, 1.2), _at(_noise(1.1, 0.15, 0.3, 640504, 'lowpass', 300), 0, 1.2), _at(_tone('sine', 45, 1.1, 0.1, 0.3), 0, 1.2),
    ]
    return _finalize(_mix(*L))
def env_magnetic_anomaly_001():
    L = [
        _at(_tone('sine', 60, 1, 0.3, 0.2), 0, 1.1), _at(_tone('sine', 63, 1, 0.3, 0.2), 0, 1.1), _at(_sweep('sine', 120, 180, 1, 0.1, 0.2), 0, 1.1),
        _at(_sweep('sine', 400, 800, 1, 0.05, 0.3), 0, 1.1), _at(_noise(1, 0.1, 0.3, 640604, 'bandpass', 1000), 0, 1.1), _at(_sweep('sawtooth', 30, 60, 1, 0.1, 0.2), 0, 1.1),
        _at(_sweep('sine', 1500, 400, 0.06, 0.1, 0.003), 0.3, 1.1), _at(_sweep('sine', 1500, 400, 0.06, 0.1, 0.003), 0.6, 1.1), _at(_sweep('sine', 1500, 400, 0.06, 0.1, 0.003), 0.85, 1.1),
    ]
    return _finalize(_mix(*L))
def env_tide_pool_001():
    L = [
        _at(_noise(1, 0.523, 0.3, 640700, 'bandpass', 1500), 0, 1.1), _at(_noise(1, 0.4184, 0.3, 640701, 'lowpass', 500), 0, 1.1), _at(_sweep('sine', 500, 1000, 0.05, 0.523, 0.003), 0.1, 1.1),
        _at(_sweep('sine', 500, 1000, 0.05, 0.523, 0.003), 0.3, 1.1), _at(_sweep('sine', 500, 1000, 0.05, 0.523, 0.003), 0.55, 1.1), _at(_sweep('sine', 500, 1000, 0.05, 0.523, 0.003), 0.75, 1.1),
        _at(_sweep('sine', 500, 1000, 0.05, 0.523, 0.003), 0.95, 1.1), _at(_sweep('sine', 800, 1500, 0.04, 0.3138, 0.003), 0.2, 1.1), _at(_sweep('sine', 800, 1500, 0.04, 0.3138, 0.003), 0.45, 1.1),
        _at(_sweep('sine', 800, 1500, 0.04, 0.3138, 0.003), 0.85, 1.1), _at(_noise(0.015, 0.251, 0.002, 640710, 'highpass', 5000), 0.15, 1.1), _at(_noise(0.015, 0.251, 0.002, 640711, 'highpass', 5000), 0.5, 1.1),
        _at(_noise(0.015, 0.251, 0.002, 640712, 'highpass', 5000), 0.7, 1.1),
    ]
    return _finalize(_mix(*L))
def infra_cargo_crane_move_001():
    L = [
        _at(_sweep('sawtooth', 100, 150, 0.9, 0.1704, 0.1), 0, 1.1), _at(_sweep('square', 200, 300, 0.9, 0.071, 0.1), 0, 1.1), _at(_noise(0.9, 0.426, 0.15, 640802, 'bandpass', 700), 0, 1.1),
        _at(_noise(1, 0.355, 0.2, 640803, 'lowpass', 250), 0, 1.1), _at(_sweep('sine', 55, 70, 1, 0.1704, 0.2), 0, 1.1), _at(_sweep('sawtooth', 130, 170, 0.45, 0.1704, 0.1), 0.5, 1.1),
        _at(_noise(0.45, 0.426, 0.1, 640806, 'bandpass', 700), 0.5, 1.1), _at(_sweep('sine', 80, 50, 0.3, 0.568, 0.002), 0.78, 1.1), _at(_noise(0.02, 0.426, 0.001, 640808, 'bandpass', 1500), 0.78, 1.1),
        _at(_noise(0.02, 0.213, 0.002, 640809, 'bandpass', 2000), 0.1, 1.1), _at(_noise(0.02, 0.213, 0.002, 640810, 'bandpass', 2000), 0.35, 1.1), _at(_noise(0.02, 0.213, 0.002, 640811, 'bandpass', 2000), 0.6, 1.1),
    ]
    return _finalize(_mix(*L))
def infra_drawbridge_motor_001():
    L = [
        _at(_sweep('sawtooth', 50, 80, 1, 0.2712, 0.15), 0, 1.1), _at(_sweep('square', 100, 160, 1, 0.1085, 0.15), 0, 1.1), _at(_noise(1, 0.4068, 0.2, 640902, 'lowpass', 400), 0, 1.1),
        _at(_sweep('sine', 300, 600, 0.9, 0.0678, 0.2), 0, 1.1), _at(_sweep('sawtooth', 70, 100, 0.45, 0.2712, 0.1), 0.5, 1.1), _at(_noise(0.45, 0.4068, 0.1, 640905, 'lowpass', 400), 0.5, 1.1),
        _at(_sweep('sine', 70, 45, 0.3, 0.5424, 0.002), 0.78, 1.1), _at(_noise(0.03, 0.2712, 0.002, 640907, 'bandpass', 1200), 0.78, 1.1), _at(_noise(0.02, 0.1356, 0.002, 640908, 'bandpass', 2000), 0.15, 1.1),
        _at(_noise(0.02, 0.1356, 0.002, 640909, 'bandpass', 2000), 0.4, 1.1), _at(_noise(0.02, 0.1356, 0.002, 640910, 'bandpass', 2000), 0.65, 1.1),
    ]
    return _finalize(_mix(*L))
def infra_ferry_horn_001():
    L = [
        _at(_tone('sawtooth', 110, 1, 0.3, 0.05), 0, 1.1), _at(_tone('sawtooth', 165, 1, 0.2, 0.05), 0, 1.1), _at(_tone('sawtooth', 220, 1, 0.1, 0.05), 0, 1.1),
        _at(_tone('square', 55, 1, 0.1, 0.05), 0, 1.1), _at(_noise(1, 0.1, 0.1, 641004, 'bandpass', 400), 0, 1.1), _at(_tone('sawtooth', 111, 1, 0.2, 0.05), 0, 1.1),
    ]
    return _finalize(_mix(*L))
def playing_cards_shuffle_001():
    L = [
        _at(_noise(0.02, 0.5499, 0.002, 641100, 'highpass', 3000), 0, 1.1), _at(_noise(0.02, 0.5499, 0.002, 641101, 'highpass', 3000), 0.04, 1.1), _at(_noise(0.02, 0.5499, 0.002, 641102, 'highpass', 3000), 0.08, 1.1),
        _at(_noise(0.02, 0.5499, 0.002, 641103, 'highpass', 3000), 0.12, 1.1), _at(_noise(0.02, 0.5499, 0.002, 641104, 'highpass', 3000), 0.16, 1.1), _at(_noise(0.02, 0.5499, 0.002, 641105, 'highpass', 3000), 0.2, 1.1),
        _at(_noise(0.02, 0.5499, 0.002, 641106, 'highpass', 3000), 0.24, 1.1), _at(_noise(0.02, 0.5499, 0.002, 641107, 'highpass', 3000), 0.28, 1.1), _at(_noise(0.02, 0.5499, 0.002, 641108, 'highpass', 3000), 0.32, 1.1),
        _at(_noise(0.02, 0.5499, 0.002, 641109, 'highpass', 3000), 0.36, 1.1), _at(_noise(0.02, 0.5499, 0.002, 641110, 'highpass', 3000), 0.4, 1.1), _at(_noise(0.02, 0.5499, 0.002, 641111, 'highpass', 3000), 0.44, 1.1),
        _at(_noise(0.02, 0.5499, 0.002, 641112, 'highpass', 3000), 0.48, 1.1), _at(_noise(0.02, 0.5499, 0.002, 641113, 'highpass', 3000), 0.52, 1.1), _at(_noise(0.02, 0.5499, 0.002, 641114, 'highpass', 3000), 0.56, 1.1),
        _at(_noise(0.02, 0.5499, 0.002, 641115, 'highpass', 3000), 0.6, 1.1), _at(_noise(0.02, 0.5499, 0.002, 641116, 'highpass', 3000), 0.64, 1.1), _at(_noise(0.02, 0.5499, 0.002, 641117, 'highpass', 3000), 0.68, 1.1),
        _at(_noise(0.02, 0.5499, 0.002, 641118, 'highpass', 3000), 0.72, 1.1), _at(_noise(0.02, 0.5499, 0.002, 641119, 'highpass', 3000), 0.76, 1.1), _at(_noise(0.02, 0.5499, 0.002, 641120, 'highpass', 3000), 0.8, 1.1),
        _at(_noise(0.02, 0.5499, 0.002, 641121, 'highpass', 3000), 0.84, 1.1), _at(_noise(0.02, 0.5499, 0.002, 641122, 'highpass', 3000), 0.88, 1.1), _at(_noise(0.02, 0.5499, 0.002, 641123, 'highpass', 3000), 0.92, 1.1),
        _at(_noise(0.015, 0.3666, 0.002, 641124, 'bandpass', 5000), 0.02, 1.1), _at(_noise(0.015, 0.3666, 0.002, 641125, 'bandpass', 5000), 0.06, 1.1), _at(_noise(0.015, 0.3666, 0.002, 641126, 'bandpass', 5000), 0.1, 1.1),
        _at(_noise(0.015, 0.3666, 0.002, 641127, 'bandpass', 5000), 0.14, 1.1), _at(_noise(0.015, 0.3666, 0.002, 641128, 'bandpass', 5000), 0.18, 1.1), _at(_noise(0.015, 0.3666, 0.002, 641129, 'bandpass', 5000), 0.22, 1.1),
        _at(_noise(0.015, 0.3666, 0.002, 641130, 'bandpass', 5000), 0.26, 1.1), _at(_noise(0.015, 0.3666, 0.002, 641131, 'bandpass', 5000), 0.3, 1.1), _at(_noise(0.015, 0.3666, 0.002, 641132, 'bandpass', 5000), 0.34, 1.1),
        _at(_noise(0.015, 0.3666, 0.002, 641133, 'bandpass', 5000), 0.38, 1.1), _at(_noise(0.015, 0.3666, 0.002, 641134, 'bandpass', 5000), 0.42, 1.1), _at(_noise(0.015, 0.3666, 0.002, 641135, 'bandpass', 5000), 0.46, 1.1),
        _at(_noise(0.015, 0.3666, 0.002, 641136, 'bandpass', 5000), 0.5, 1.1), _at(_noise(0.015, 0.3666, 0.002, 641137, 'bandpass', 5000), 0.54, 1.1), _at(_noise(0.015, 0.3666, 0.002, 641138, 'bandpass', 5000), 0.58, 1.1),
        _at(_noise(0.015, 0.3666, 0.002, 641139, 'bandpass', 5000), 0.62, 1.1), _at(_noise(0.015, 0.3666, 0.002, 641140, 'bandpass', 5000), 0.66, 1.1), _at(_noise(0.015, 0.3666, 0.002, 641141, 'bandpass', 5000), 0.7, 1.1),
        _at(_noise(0.015, 0.3666, 0.002, 641142, 'bandpass', 5000), 0.74, 1.1), _at(_noise(0.015, 0.3666, 0.002, 641143, 'bandpass', 5000), 0.78, 1.1), _at(_noise(0.015, 0.3666, 0.002, 641144, 'bandpass', 5000), 0.82, 1.1),
        _at(_noise(0.015, 0.3666, 0.002, 641145, 'bandpass', 5000), 0.86, 1.1), _at(_noise(0.015, 0.3666, 0.002, 641146, 'bandpass', 5000), 0.9, 1.1), _at(_noise(0.015, 0.3666, 0.002, 641147, 'bandpass', 5000), 0.94, 1.1),
        _at(_noise(0.1, 0.1833, 0.002, 641148, 'bandpass', 2500), 0.95, 1.1), _at(_sweep('sine', 150, 100, 0.06, 0.5499, 0.002), 0.98, 1.1),
    ]
    return _finalize(_mix(*L))
def sub_propeller_start_001():
    L = [
        _at(_sweep('sawtooth', 30, 80, 1, 0.4225, 0.3), 0, 1.1), _at(_sweep('square', 60, 160, 1, 0.1352, 0.3), 0, 1.1), _at(_noise(1, 0.507, 0.3, 641202, 'lowpass', 400), 0, 1.1),
        _at(_sweep('sine', 400, 900, 0.9, 0.0845, 0.3), 0, 1.1), _at(_noise(1, 0.338, 0.4, 641204, 'bandpass', 600), 0, 1.1), _at(_noise(0.3, 0.507, 0.1, 641205, 'lowpass', 400), 0.7, 1.1),
        _at(_noise(0.04, 0.4225, 0.002, 641206, 'lowpass', 300), 0.1, 1.1), _at(_noise(0.04, 0.4225, 0.002, 641207, 'lowpass', 300), 0.3, 1.1), _at(_noise(0.04, 0.4225, 0.002, 641208, 'lowpass', 300), 0.5, 1.1),
        _at(_noise(0.04, 0.4225, 0.002, 641209, 'lowpass', 300), 0.65, 1.1), _at(_noise(0.04, 0.4225, 0.002, 641210, 'lowpass', 300), 0.78, 1.1), _at(_noise(0.04, 0.4225, 0.002, 641211, 'lowpass', 300), 0.9, 1.1),
    ]
    return _finalize(_mix(*L))
def sub_propeller_stop_001():
    L = [
        _at(_sweep('sawtooth', 80, 25, 1, 0.3977, 0.02), 0, 1.1), _at(_sweep('square', 160, 50, 1, 0.1273, 0.02), 0, 1.1), _at(_noise(1, 0.3977, 0.03, 641302, 'lowpass', 350), 0, 1.1),
        _at(_sweep('sine', 900, 300, 0.7, 0.0636, 0.02), 0, 1.1), _at(_noise(0.9, 0.2386, 0.05, 641304, 'bandpass', 500), 0, 1.1), _at(_noise(0.05, 0.3977, 0.002, 641305, 'lowpass', 300), 0.1, 1.1),
        _at(_noise(0.05, 0.3977, 0.002, 641306, 'lowpass', 300), 0.25, 1.1), _at(_noise(0.05, 0.3977, 0.002, 641307, 'lowpass', 300), 0.45, 1.1), _at(_noise(0.05, 0.3977, 0.002, 641308, 'lowpass', 300), 0.7, 1.1),
    ]
    return _finalize(_mix(*L))
def aura_reveal_001():
    L = [
        _at(_sweep('sine', 300, 1500, 0.5, 0.15, 0.05), 0, 0.9), _at(_tone('sine', 523, 0.6, 0.2, 0.01), 0.3, 0.9), _at(_tone('sine', 659, 0.55, 0.2, 0.01), 0.35, 0.9),
        _at(_tone('sine', 784, 0.5, 0.2, 0.01), 0.4, 0.9), _at(_tone('sine', 1568, 0.45, 0.1, 0.003), 0.45, 0.9), _at(_noise(0.5, 0.1, 0.1, 641405, 'highpass', 6000), 0.3, 0.9),
        _at(_tone('sine', 130, 0.8, 0.15, 0.1), 0, 0.9),
    ]
    return _finalize(_mix(*L))
def bees_swarm_pass_001():
    L = [
        _at(_sweep('sawtooth', 180, 220, 0.85, 0.1804, 0.3), 0, 0.9), _at(_sweep('sawtooth', 183, 223, 0.85, 0.1804, 0.3), 0, 0.9), _at(_sweep('sawtooth', 240, 190, 0.85, 0.0962, 0.3), 0, 0.9),
        _at(_noise(0.85, 0.3609, 0.3, 641503, 'bandpass', 900), 0, 0.9), _at(_sweep('square', 90, 110, 0.85, 0.0962, 0.3), 0, 0.9), _at(_noise(0.85, 0.1804, 0.3, 641505, 'bandpass', 1500), 0, 0.9),
    ]
    return _finalize(_mix(*L))
def cicada_day_chorus_001():
    L = [
        _at(_noise(0.85, 0.3, 0.1, 641600, 'highpass', 4000), 0, 0.9), _at(_noise(0.85, 0.3, 0.1, 641601, 'bandpass', 5500), 0, 0.9), _at(_tone('sine', 4500, 0.85, 0.08, 0.1), 0, 0.9),
        _at(_tone('sine', 4800, 0.85, 0.06, 0.1), 0, 0.9), _at(_tone('sine', 5200, 0.85, 0.05, 0.1), 0, 0.9), _at(_noise(0.03, 0.25, 0.002, 641605, 'bandpass', 5000), 0, 0.9),
        _at(_noise(0.03, 0.25, 0.002, 641606, 'bandpass', 5000), 0.07, 0.9), _at(_noise(0.03, 0.25, 0.002, 641607, 'bandpass', 5000), 0.14, 0.9), _at(_noise(0.03, 0.25, 0.002, 641608, 'bandpass', 5000), 0.21, 0.9),
        _at(_noise(0.03, 0.25, 0.002, 641609, 'bandpass', 5000), 0.28, 0.9), _at(_noise(0.03, 0.25, 0.002, 641610, 'bandpass', 5000), 0.35, 0.9), _at(_noise(0.03, 0.25, 0.002, 641611, 'bandpass', 5000), 0.42, 0.9),
        _at(_noise(0.03, 0.25, 0.002, 641612, 'bandpass', 5000), 0.49, 0.9), _at(_noise(0.03, 0.25, 0.002, 641613, 'bandpass', 5000), 0.56, 0.9), _at(_noise(0.03, 0.25, 0.002, 641614, 'bandpass', 5000), 0.63, 0.9),
        _at(_noise(0.03, 0.25, 0.002, 641615, 'bandpass', 5000), 0.7, 0.9), _at(_noise(0.03, 0.25, 0.002, 641616, 'bandpass', 5000), 0.77, 0.9),
    ]
    return _finalize(_mix(*L))
def craft_cement_mix_001():
    L = [
        _at(_noise(0.85, 0.836, 0.1, 641700, 'lowpass', 500), 0, 0.9), _at(_noise(0.85, 0.6688, 0.1, 641701, 'bandpass', 250), 0, 0.9), _at(_sweep('sawtooth', 70, 90, 0.85, 0.2508, 0.1), 0, 0.9),
        _at(_tone('sine', 55, 0.85, 0.2006, 0.1), 0, 0.9), _at(_noise(0.04, 0.3344, 0.002, 641704, 'bandpass', 1200), 0.1, 0.9), _at(_noise(0.04, 0.3344, 0.002, 641705, 'bandpass', 1200), 0.22, 0.9),
        _at(_noise(0.04, 0.3344, 0.002, 641706, 'bandpass', 1200), 0.38, 0.9), _at(_noise(0.04, 0.3344, 0.002, 641707, 'bandpass', 1200), 0.5, 0.9), _at(_noise(0.04, 0.3344, 0.002, 641708, 'bandpass', 1200), 0.62, 0.9),
        _at(_noise(0.04, 0.3344, 0.002, 641709, 'bandpass', 1200), 0.75, 0.9), _at(_noise(0.04, 0.5016, 0.002, 641710, 'lowpass', 400), 0.15, 0.9), _at(_noise(0.04, 0.5016, 0.002, 641711, 'lowpass', 400), 0.3, 0.9),
        _at(_noise(0.04, 0.5016, 0.002, 641712, 'lowpass', 400), 0.45, 0.9), _at(_noise(0.04, 0.5016, 0.002, 641713, 'lowpass', 400), 0.58, 0.9), _at(_noise(0.04, 0.5016, 0.002, 641714, 'lowpass', 400), 0.7, 0.9),
    ]
    return _finalize(_mix(*L))
def env_gravity_well_pulse_001():
    L = [
        _at(_sweep('sine', 60, 35, 0.4, 0.4, 0.01), 0, 0.9), _at(_sweep('sine', 120, 70, 0.4, 0.1, 0.01), 0, 0.9), _at(_sweep('sine', 60, 35, 0.4, 0.35, 0.01), 0.45, 0.9),
        _at(_sweep('sine', 400, 100, 0.3, 0.1, 0.01), 0, 0.9), _at(_noise(0.85, 0.2, 0.15, 641804, 'lowpass', 300), 0, 0.9), _at(_sweep('sine', 900, 200, 0.35, 0.05, 0.01), 0.45, 0.9),
    ]
    return _finalize(_mix(*L))
def forge_bellows_blow_001():
    L = [
        _at(_noise(0.4, 0.4, 0.15, 641900, 'highpass', 1500), 0, 0.9), _at(_noise(0.4, 0.3, 0.15, 641901, 'bandpass', 1000), 0, 0.9), _at(_noise(0.4, 0.4, 0.15, 641902, 'highpass', 1500), 0.35, 0.9),
        _at(_noise(0.4, 0.3, 0.15, 641903, 'bandpass', 1000), 0.35, 0.9), _at(_sweep('sine', 150, 100, 0.4, 0.12, 0.1), 0, 0.9), _at(_sweep('sine', 150, 100, 0.4, 0.12, 0.1), 0.35, 0.9),
        _at(_sweep('sine', 90, 60, 0.08, 0.3, 0.003), 0, 0.9), _at(_sweep('sine', 90, 60, 0.08, 0.3, 0.003), 0.35, 0.9),
    ]
    return _finalize(_mix(*L))
def forge_crucible_pour_001():
    L = [
        _at(_noise(0.8, 0.5477, 0.1, 642000, 'bandpass', 1800), 0, 0.9), _at(_noise(0.8, 0.4695, 0.1, 642001, 'lowpass', 600), 0, 0.9), _at(_noise(0.8, 0.1878, 0.1, 642002, 'highpass', 5000), 0, 0.9),
        _at(_sweep('sine', 300, 500, 0.5, 0.1565, 0.1), 0, 0.9), _at(_tone('sine', 100, 0.8, 0.1878, 0.1), 0, 0.9), _at(_sweep('sine', 600, 1100, 0.04, 0.1878, 0.003), 0.15, 0.9),
        _at(_sweep('sine', 600, 1100, 0.04, 0.1878, 0.003), 0.35, 0.9), _at(_sweep('sine', 600, 1100, 0.04, 0.1878, 0.003), 0.55, 0.9), _at(_sweep('sine', 600, 1100, 0.04, 0.1878, 0.003), 0.7, 0.9),
        _at(_noise(0.01, 0.1878, 0.002, 642009, 'highpass', 6000), 0.25, 0.9), _at(_noise(0.01, 0.1878, 0.002, 642010, 'highpass', 6000), 0.45, 0.9), _at(_noise(0.01, 0.1878, 0.002, 642011, 'highpass', 6000), 0.62, 0.9),
        _at(_noise(0.01, 0.1878, 0.002, 642012, 'highpass', 6000), 0.78, 0.9),
    ]
    return _finalize(_mix(*L))
def infra_subway_arrival_001():
    L = [
        _at(_noise(0.85, 0.5145, 0.3, 642100, 'lowpass', 300), 0, 0.9), _at(_noise(0.85, 0.441, 0.3, 642101, 'bandpass', 1500), 0, 0.9), _at(_sweep('sawtooth', 60, 40, 0.85, 0.1764, 0.3), 0, 0.9),
        _at(_sweep('sine', 800, 300, 0.8, 0.147, 0.4), 0, 0.9), _at(_noise(0.5, 0.3675, 0.2, 642104, 'highpass', 4000), 0.3, 0.9), _at(_sweep('sine', 120, 70, 0.1, 0.441, 0.003), 0.75, 0.9),
        _at(_noise(0.02, 0.1764, 0.002, 642106, 'bandpass', 2000), 0.1, 0.9), _at(_noise(0.02, 0.1764, 0.002, 642107, 'bandpass', 2000), 0.25, 0.9), _at(_noise(0.02, 0.1764, 0.002, 642108, 'bandpass', 2000), 0.4, 0.9),
        _at(_noise(0.02, 0.1764, 0.002, 642109, 'bandpass', 2000), 0.55, 0.9), _at(_noise(0.02, 0.1764, 0.002, 642110, 'bandpass', 2000), 0.7, 0.9),
    ]
    return _finalize(_mix(*L))
def ion_thruster_ignite_001():
    L = [
        _at(_sweep('sine', 100, 600, 0.4, 0.3, 0.02), 0, 0.9), _at(_sweep('sawtooth', 200, 1200, 0.4, 0.08, 0.02), 0, 0.9), _at(_noise(0.8, 0.3, 0.05, 642202, 'highpass', 3000), 0, 0.9),
        _at(_noise(0.8, 0.2, 0.05, 642203, 'bandpass', 2000), 0, 0.9), _at(_tone('sine', 400, 0.5, 0.12, 0.05), 0.35, 0.9), _at(_tone('sine', 404, 0.5, 0.12, 0.05), 0.35, 0.9),
        _at(_tone('square', 100, 0.5, 0.05, 0.05), 0.35, 0.9), _at(_noise(0.01, 0.2, 0.002, 642207, 'highpass', 6000), 0, 0.9),
    ]
    return _finalize(_mix(*L))
def mech_conveyor_move_001():
    L = [
        _at(_noise(0.85, 0.4836, 0.1, 642300, 'lowpass', 400), 0, 0.9), _at(_sweep('sawtooth', 70, 80, 0.85, 0.1934, 0.1), 0, 0.9), _at(_tone('sine', 150, 0.85, 0.129, 0.1), 0, 0.9),
        _at(_noise(0.03, 0.5642, 0.002, 642303, 'bandpass', 1500), 0, 0.9), _at(_noise(0.03, 0.5642, 0.002, 642304, 'bandpass', 1500), 0.1, 0.9), _at(_noise(0.03, 0.5642, 0.002, 642305, 'bandpass', 1500), 0.2, 0.9),
        _at(_noise(0.03, 0.5642, 0.002, 642306, 'bandpass', 1500), 0.3, 0.9), _at(_noise(0.03, 0.5642, 0.002, 642307, 'bandpass', 1500), 0.4, 0.9), _at(_noise(0.03, 0.5642, 0.002, 642308, 'bandpass', 1500), 0.5, 0.9),
        _at(_noise(0.03, 0.5642, 0.002, 642309, 'bandpass', 1500), 0.6, 0.9), _at(_noise(0.03, 0.5642, 0.002, 642310, 'bandpass', 1500), 0.7, 0.9), _at(_noise(0.03, 0.5642, 0.002, 642311, 'bandpass', 1500), 0.8, 0.9),
        _at(_sweep('sine', 120, 80, 0.05, 0.4836, 0.003), 0.02, 0.9), _at(_sweep('sine', 120, 80, 0.05, 0.4836, 0.003), 0.12, 0.9), _at(_sweep('sine', 120, 80, 0.05, 0.4836, 0.003), 0.22, 0.9),
        _at(_sweep('sine', 120, 80, 0.05, 0.4836, 0.003), 0.32, 0.9), _at(_sweep('sine', 120, 80, 0.05, 0.4836, 0.003), 0.42, 0.9), _at(_sweep('sine', 120, 80, 0.05, 0.4836, 0.003), 0.52, 0.9),
        _at(_sweep('sine', 120, 80, 0.05, 0.4836, 0.003), 0.62, 0.9), _at(_sweep('sine', 120, 80, 0.05, 0.4836, 0.003), 0.72, 0.9), _at(_sweep('sine', 120, 80, 0.05, 0.4836, 0.003), 0.82, 0.9),
    ]
    return _finalize(_mix(*L))
def mech_system_shutdown_001():
    L = [
        _at(_sweep('sawtooth', 150, 30, 0.8, 0.3247, 0.01), 0, 0.9), _at(_sweep('square', 300, 60, 0.8, 0.1039, 0.01), 0, 0.9), _at(_sweep('sine', 1200, 200, 0.6, 0.1299, 0.01), 0, 0.9),
        _at(_noise(0.7, 0.3247, 0.01, 642403, 'lowpass', 400), 0, 0.9), _at(_tone('sine', 440, 0.1, 0.2598, 0.003), 0, 0.9), _at(_tone('sine', 330, 0.1, 0.2598, 0.003), 0.12, 0.9),
        _at(_tone('sine', 220, 0.15, 0.2598, 0.003), 0.24, 0.9), _at(_noise(0.08, 0.3897, 0.002, 642407, 'lowpass', 250), 0.5, 0.9),
    ]
    return _finalize(_mix(*L))

OFFICIAL_PRESETS_G1_M4 = {
    'ruin-ancient-door-close-001': ruin_ancient_door_close_001,
    'ruin-ancient-door-open-001': ruin_ancient_door_open_001,
    'ruin-temple-bell-001': ruin_temple_bell_001,
    'ruin-temple-door-rumble-001': ruin_temple_door_rumble_001,
    'zero-gravity-float-001': zero_gravity_float_001,
    'whale-song-low-001': whale_song_low_001,
    'env-magnetic-anomaly-001': env_magnetic_anomaly_001,
    'env-tide-pool-001': env_tide_pool_001,
    'infra-cargo-crane-move-001': infra_cargo_crane_move_001,
    'infra-drawbridge-motor-001': infra_drawbridge_motor_001,
    'infra-ferry-horn-001': infra_ferry_horn_001,
    'playing-cards-shuffle-001': playing_cards_shuffle_001,
    'sub-propeller-start-001': sub_propeller_start_001,
    'sub-propeller-stop-001': sub_propeller_stop_001,
    'aura-reveal-001': aura_reveal_001,
    'bees-swarm-pass-001': bees_swarm_pass_001,
    'cicada-day-chorus-001': cicada_day_chorus_001,
    'craft-cement-mix-001': craft_cement_mix_001,
    'env-gravity-well-pulse-001': env_gravity_well_pulse_001,
    'forge-bellows-blow-001': forge_bellows_blow_001,
    'forge-crucible-pour-001': forge_crucible_pour_001,
    'infra-subway-arrival-001': infra_subway_arrival_001,
    'ion-thruster-ignite-001': ion_thruster_ignite_001,
    'mech-conveyor-move-001': mech_conveyor_move_001,
    'mech-system-shutdown-001': mech_system_shutdown_001,
}
