"""Generation 1 - module 7 : sons reconstruits (son WAV + apercu navigateur)."""
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

def power_up_002():
    L = [
        _at(_sweep('sine', 200, 1200, 0.6, 0.3738, 0.05), 0, 1.1), _at(_sweep('square', 400, 2400, 0.6, 0.0997, 0.05), 0, 1.1), _at(_tone('triangle', 523, 0.15, 0.3115, 0.005), 0.55, 1.1),
        _at(_tone('triangle', 659, 0.15, 0.3115, 0.005), 0.65, 1.1), _at(_tone('triangle', 784, 0.15, 0.3115, 0.005), 0.75, 1.1), _at(_tone('triangle', 1047, 0.25, 0.3115, 0.005), 0.85, 1.1),
        _at(_noise(0.3, 0.1246, 0.05, 670006, 'highpass', 6000), 0.7, 1.1),
    ]
    return _finalize(_mix(*L))
def alien_communication_001():
    L = [
        _at(_sweep('sine', 600, 1200, 0.2, 0.4108, 0.01), 0, 1.7), _at(_sweep('sine', 900, 500, 0.2, 0.4108, 0.01), 0.25, 1.7), _at(_sweep('sine', 700, 1500, 0.15, 0.4108, 0.01), 0.5, 1.7),
        _at(_sweep('sine', 1400, 600, 0.25, 0.4108, 0.01), 0.7, 1.7), _at(_sweep('sawtooth', 150, 300, 0.3, 0.1643, 0.02), 1, 1.7), _at(_sweep('sine', 2000, 3000, 0.2, 0.1643, 0.01), 1, 1.7),
        _at(_sweep('sine', 800, 1600, 0.3, 0.3615, 0.01), 1.3, 1.7), _at(_sweep('sine', 1200, 400, 0.2, 0.3615, 0.01), 1.5, 1.7), _at(_tone('sine', 90, 1.6, 0.1314, 0.2), 0, 1.7),
        _at(_noise(0.02, 0.2465, 0.002, 670109, 'bandpass', 3000), 0.15, 1.7), _at(_noise(0.02, 0.2465, 0.002, 670110, 'bandpass', 3000), 0.45, 1.7), _at(_noise(0.02, 0.2465, 0.002, 670111, 'bandpass', 3000), 0.65, 1.7),
        _at(_noise(0.02, 0.2465, 0.002, 670112, 'bandpass', 3000), 1.25, 1.7),
    ]
    return _finalize(_mix(*L))
def artifact_discovery_001():
    L = [
        _at(_tone('sine', 523, 0.6, 0.25, 0.003), 0, 1.4), _at(_tone('sine', 659, 0.6, 0.25, 0.003), 0.15, 1.4), _at(_tone('sine', 784, 0.6, 0.25, 0.003), 0.3, 1.4),
        _at(_tone('sine', 1047, 0.8, 0.25, 0.003), 0.45, 1.4), _at(_tone('sine', 262, 1.2, 0.15, 0.3), 0, 1.4), _at(_noise(0.8, 0.07, 0.3, 670205, 'highpass', 6000), 0.4, 1.4),
        _at(_tone('sine', 65, 1.2, 0.2, 0.2), 0, 1.4),
    ]
    return _finalize(_mix(*L))
def boar_ground_snuffle_001():
    L = [
        _at(_noise(0.15, 1.066, 0.03, 670300, 'bandpass', 600), 0, 1.2), _at(_noise(0.15, 1.066, 0.03, 670301, 'bandpass', 600), 0.25, 1.2), _at(_noise(0.15, 1.066, 0.03, 670302, 'bandpass', 600), 0.5, 1.2),
        _at(_noise(0.15, 1.066, 0.03, 670303, 'bandpass', 600), 0.75, 1.2), _at(_noise(0.15, 0.8528, 0.03, 670304, 'lowpass', 300), 0, 1.2), _at(_noise(0.15, 0.8528, 0.03, 670305, 'lowpass', 300), 0.25, 1.2),
        _at(_noise(0.15, 0.8528, 0.03, 670306, 'lowpass', 300), 0.5, 1.2), _at(_noise(0.15, 0.8528, 0.03, 670307, 'lowpass', 300), 0.75, 1.2), _at(_sweep('sawtooth', 90, 70, 0.3, 0.4264, 0.03), 0.9, 1.2),
        _at(_noise(0.3, 0.6396, 0.03, 670309, 'bandpass', 400), 0.9, 1.2),
    ]
    return _finalize(_mix(*L))
def craft_hacksaw_metal_001():
    L = [
        _at(_noise(0.3, 0.4323, 0.08, 670400, 'highpass', 3000), 0, 1.15), _at(_noise(0.3, 0.4323, 0.08, 670401, 'highpass', 3000), 0.4, 1.15), _at(_noise(0.3, 0.4323, 0.08, 670402, 'highpass', 3000), 0.8, 1.15),
        _at(_noise(0.3, 0.3088, 0.08, 670403, 'bandpass', 1800), 0, 1.15), _at(_noise(0.3, 0.3088, 0.08, 670404, 'bandpass', 1800), 0.4, 1.15), _at(_noise(0.3, 0.3088, 0.08, 670405, 'bandpass', 1800), 0.8, 1.15),
        _at(_tone('sine', 2400, 0.3, 0.0988, 0.01), 0, 1.15), _at(_tone('sine', 2400, 0.3, 0.0988, 0.01), 0.4, 1.15), _at(_tone('sine', 2400, 0.3, 0.0988, 0.01), 0.8, 1.15),
    ]
    return _finalize(_mix(*L))
def craft_metal_filing_001():
    L = [
        _at(_noise(0.22, 0.4389, 0.06, 670500, 'highpass', 4000), 0, 1.05), _at(_noise(0.22, 0.4389, 0.06, 670501, 'highpass', 4000), 0.27, 1.05), _at(_noise(0.22, 0.4389, 0.06, 670502, 'highpass', 4000), 0.54, 1.05),
        _at(_noise(0.22, 0.4389, 0.06, 670503, 'highpass', 4000), 0.81, 1.05), _at(_noise(0.22, 0.1881, 0.06, 670504, 'bandpass', 6500), 0, 1.05), _at(_noise(0.22, 0.1881, 0.06, 670505, 'bandpass', 6500), 0.27, 1.05),
        _at(_noise(0.22, 0.1881, 0.06, 670506, 'bandpass', 6500), 0.54, 1.05), _at(_noise(0.22, 0.1881, 0.06, 670507, 'bandpass', 6500), 0.81, 1.05), _at(_tone('sine', 1800, 0.2, 0.0752, 0.01), 0, 1.05),
        _at(_tone('sine', 1800, 0.2, 0.0752, 0.01), 0.27, 1.05), _at(_tone('sine', 1800, 0.2, 0.0752, 0.01), 0.54, 1.05), _at(_tone('sine', 1800, 0.2, 0.0752, 0.01), 0.81, 1.05),
    ]
    return _finalize(_mix(*L))
def craft_paint_roller_001():
    L = [
        _at(_noise(0.5, 0.8984, 0.1, 670600, 'lowpass', 1500), 0, 1.1), _at(_noise(0.5, 0.3851, 0.1, 670601, 'bandpass', 3000), 0, 1.1), _at(_noise(0.5, 0.8984, 0.1, 670602, 'lowpass', 1500), 0.55, 1.1),
        _at(_noise(0.5, 0.3851, 0.1, 670603, 'bandpass', 3000), 0.55, 1.1), _at(_sweep('sine', 300, 200, 0.06, 0.3851, 0.003), 0.02, 1.1), _at(_sweep('sine', 300, 200, 0.06, 0.3851, 0.003), 0.57, 1.1),
        _at(_noise(0.02, 0.2567, 0.002, 670606, 'bandpass', 2000), 0.2, 1.1), _at(_noise(0.02, 0.2567, 0.002, 670607, 'bandpass', 2000), 0.3, 1.1), _at(_noise(0.02, 0.2567, 0.002, 670608, 'bandpass', 2000), 0.4, 1.1),
        _at(_noise(0.02, 0.2567, 0.002, 670609, 'bandpass', 2000), 0.75, 1.1), _at(_noise(0.02, 0.2567, 0.002, 670610, 'bandpass', 2000), 0.85, 1.1), _at(_noise(0.02, 0.2567, 0.002, 670611, 'bandpass', 2000), 0.95, 1.1),
    ]
    return _finalize(_mix(*L))
def domino_chain_fall_001():
    L = [
        _at(_noise(0.02, 0.7, 0.002, 670700, 'bandpass', 2500), 0, 1.5), _at(_noise(0.02, 0.7, 0.002, 670701, 'bandpass', 2500), 0.12, 1.5), _at(_noise(0.02, 0.7, 0.002, 670702, 'bandpass', 2500), 0.23, 1.5),
        _at(_noise(0.02, 0.7, 0.002, 670703, 'bandpass', 2500), 0.33, 1.5), _at(_noise(0.02, 0.7, 0.002, 670704, 'bandpass', 2500), 0.42, 1.5), _at(_noise(0.02, 0.7, 0.002, 670705, 'bandpass', 2500), 0.5, 1.5),
        _at(_noise(0.02, 0.7, 0.002, 670706, 'bandpass', 2500), 0.57, 1.5), _at(_noise(0.02, 0.7, 0.002, 670707, 'bandpass', 2500), 0.64, 1.5), _at(_noise(0.02, 0.7, 0.002, 670708, 'bandpass', 2500), 0.7, 1.5),
        _at(_noise(0.02, 0.7, 0.002, 670709, 'bandpass', 2500), 0.76, 1.5), _at(_noise(0.02, 0.7, 0.002, 670710, 'bandpass', 2500), 0.82, 1.5), _at(_noise(0.02, 0.7, 0.002, 670711, 'bandpass', 2500), 0.87, 1.5),
        _at(_noise(0.02, 0.7, 0.002, 670712, 'bandpass', 2500), 0.92, 1.5), _at(_noise(0.02, 0.7, 0.002, 670713, 'bandpass', 2500), 0.97, 1.5), _at(_noise(0.02, 0.7, 0.002, 670714, 'bandpass', 2500), 1.02, 1.5),
        _at(_noise(0.02, 0.7, 0.002, 670715, 'bandpass', 2500), 1.07, 1.5), _at(_noise(0.02, 0.7, 0.002, 670716, 'bandpass', 2500), 1.12, 1.5), _at(_noise(0.02, 0.7, 0.002, 670717, 'bandpass', 2500), 1.17, 1.5),
        _at(_noise(0.02, 0.7, 0.002, 670718, 'bandpass', 2500), 1.22, 1.5), _at(_noise(0.02, 0.7, 0.002, 670719, 'bandpass', 2500), 1.27, 1.5), _at(_tone('sine', 800, 0.03, 0.2, 0.002), 0, 1.5),
        _at(_tone('sine', 800, 0.03, 0.2, 0.002), 0.12, 1.5), _at(_tone('sine', 800, 0.03, 0.2, 0.002), 0.23, 1.5), _at(_tone('sine', 800, 0.03, 0.2, 0.002), 0.33, 1.5),
        _at(_tone('sine', 800, 0.03, 0.2, 0.002), 0.42, 1.5), _at(_tone('sine', 800, 0.03, 0.2, 0.002), 0.5, 1.5), _at(_tone('sine', 800, 0.03, 0.2, 0.002), 0.57, 1.5),
        _at(_tone('sine', 800, 0.03, 0.2, 0.002), 0.64, 1.5), _at(_tone('sine', 800, 0.03, 0.2, 0.002), 0.7, 1.5), _at(_tone('sine', 800, 0.03, 0.2, 0.002), 0.76, 1.5),
        _at(_tone('sine', 800, 0.03, 0.2, 0.002), 0.82, 1.5), _at(_tone('sine', 800, 0.03, 0.2, 0.002), 0.87, 1.5), _at(_tone('sine', 800, 0.03, 0.2, 0.002), 0.92, 1.5),
        _at(_tone('sine', 800, 0.03, 0.2, 0.002), 0.97, 1.5), _at(_tone('sine', 800, 0.03, 0.2, 0.002), 1.02, 1.5), _at(_tone('sine', 800, 0.03, 0.2, 0.002), 1.07, 1.5),
        _at(_tone('sine', 800, 0.03, 0.2, 0.002), 1.12, 1.5), _at(_tone('sine', 800, 0.03, 0.2, 0.002), 1.17, 1.5), _at(_tone('sine', 800, 0.03, 0.2, 0.002), 1.22, 1.5),
        _at(_tone('sine', 800, 0.03, 0.2, 0.002), 1.27, 1.5), _at(_sweep('sine', 120, 80, 0.15, 0.6, 0.002), 1.35, 1.5), _at(_noise(0.1, 0.5, 0.002, 670741, 'bandpass', 700), 1.35, 1.5),
    ]
    return _finalize(_mix(*L))
def elephant_trumpet_001():
    L = [
        _at(_sweep('sawtooth', 280, 560, 1.2, 0.3, 0.05), 0, 1.4), _at(_sweep('sawtooth', 560, 300, 0.7, 0.25, 0.02), 0.6, 1.4), _at(_sweep('square', 285, 570, 1.2, 0.08, 0.05), 0, 1.4),
        _at(_noise(1.2, 0.2, 0.1, 670803, 'bandpass', 1200), 0, 1.4), _at(_tone('sine', 1200, 1.2, 0.06, 0.1), 0, 1.4),
    ]
    return _finalize(_mix(*L))
def env_geyser_mini_001():
    L = [
        _at(_noise(0.6, 0.4, 0.3, 670900, 'lowpass', 300), 0, 1.4), _at(_tone('sine', 50, 0.6, 0.25, 0.3), 0, 1.4), _at(_noise(0.8, 0.45, 0.02, 670902, 'highpass', 2000), 0.6, 1.4),
        _at(_noise(0.8, 0.35, 0.02, 670903, 'bandpass', 800), 0.6, 1.4), _at(_sweep('sine', 90, 50, 0.3, 0.3, 0.02), 0.6, 1.4), _at(_noise(0.5, 0.12, 0.05, 670905, 'highpass', 5000), 0.9, 1.4),
        _at(_sweep('sine', 300, 700, 0.05, 0.12, 0.003), 0.1, 1.4), _at(_sweep('sine', 300, 700, 0.05, 0.12, 0.003), 0.25, 1.4), _at(_sweep('sine', 300, 700, 0.05, 0.12, 0.003), 0.4, 1.4),
        _at(_sweep('sine', 300, 700, 0.05, 0.12, 0.003), 0.5, 1.4),
    ]
    return _finalize(_mix(*L))
def environment_rain_start_001():
    L = [
        _at(_noise(1.8, 0.3672, 1, 671000, 'highpass', 3000), 0, 1.9), _at(_noise(1.8, 0.2203, 1, 671001, 'bandpass', 6000), 0, 1.9), _at(_noise(0.015, 0.3672, 0.002, 671002, 'bandpass', 4000), 0, 1.9),
        _at(_noise(0.015, 0.3672, 0.002, 671003, 'bandpass', 4000), 0.15, 1.9), _at(_noise(0.015, 0.3672, 0.002, 671004, 'bandpass', 4000), 0.3, 1.9), _at(_noise(0.015, 0.3672, 0.002, 671005, 'bandpass', 4000), 0.38, 1.9),
        _at(_noise(0.015, 0.3672, 0.002, 671006, 'bandpass', 4000), 0.5, 1.9), _at(_noise(0.015, 0.3672, 0.002, 671007, 'bandpass', 4000), 0.58, 1.9), _at(_noise(0.015, 0.3672, 0.002, 671008, 'bandpass', 4000), 0.65, 1.9),
        _at(_noise(0.015, 0.3672, 0.002, 671009, 'bandpass', 4000), 0.72, 1.9), _at(_tone('sine', 1500, 0.02, 0.1469, 0.002), 0.1, 1.9), _at(_tone('sine', 1500, 0.02, 0.1469, 0.002), 0.33, 1.9),
        _at(_tone('sine', 1500, 0.02, 0.1469, 0.002), 0.55, 1.9), _at(_tone('sine', 1500, 0.02, 0.1469, 0.002), 0.78, 1.9),
    ]
    return _finalize(_mix(*L))
def forge_file_metal_001():
    L = [
        _at(_noise(0.3, 0.4872, 0.08, 671100, 'highpass', 2500), 0, 1), _at(_noise(0.3, 0.3045, 0.08, 671101, 'bandpass', 1500), 0, 1), _at(_tone('sine', 1100, 0.3, 0.0731, 0.01), 0, 1),
        _at(_noise(0.3, 0.4872, 0.08, 671103, 'highpass', 2500), 0.35, 1), _at(_noise(0.3, 0.3045, 0.08, 671104, 'bandpass', 1500), 0.35, 1), _at(_tone('sine', 1100, 0.3, 0.0731, 0.01), 0.35, 1),
        _at(_tone('sine', 600, 0.2, 0.1218, 0.003), 0.7, 1), _at(_noise(0.02, 0.1827, 0.002, 671107, 'bandpass', 2000), 0.7, 1),
    ]
    return _finalize(_mix(*L))
def forge_glue_apply_001():
    L = [
        _at(_noise(0.5, 0.6894, 0.15, 671200, 'bandpass', 500), 0, 1.15), _at(_sweep('sine', 200, 150, 0.5, 0.2758, 0.1), 0, 1.15), _at(_sweep('sine', 400, 150, 0.08, 0.4596, 0.003), 0.55, 1.15),
        _at(_sweep('sine', 400, 150, 0.08, 0.4596, 0.003), 0.7, 1.15), _at(_noise(0.3, 0.4596, 0.05, 671204, 'lowpass', 800), 0.5, 1.15), _at(_noise(0.35, 0.3447, 0.1, 671205, 'bandpass', 1200), 0.75, 1.15),
    ]
    return _finalize(_mix(*L))
def frog_pond_croak_001():
    L = [
        _at(_sweep('sawtooth', 140, 110, 0.15, 0.4998, 0.01), 0, 1.3), _at(_sweep('square', 280, 220, 0.15, 0.1666, 0.01), 0, 1.3), _at(_sweep('sawtooth', 160, 120, 0.15, 0.4998, 0.01), 0.25, 1.3),
        _at(_sweep('sawtooth', 130, 100, 0.2, 0.4998, 0.01), 0.5, 1.3), _at(_sweep('sine', 500, 900, 0.05, 0.1666, 0.003), 1.1, 1.3), _at(_noise(1.3, 0.1666, 0.3, 671305, 'lowpass', 400), 0, 1.3),
        _at(_noise(0.15, 0.2499, 0.01, 671306, 'bandpass', 600), 0, 1.3), _at(_noise(0.15, 0.2499, 0.01, 671307, 'bandpass', 600), 0.25, 1.3), _at(_noise(0.15, 0.2499, 0.01, 671308, 'bandpass', 600), 0.5, 1.3),
        _at(_tone('sawtooth', 200, 0.04, 0.3332, 0.003), 0.8, 1.3), _at(_tone('sawtooth', 200, 0.04, 0.3332, 0.003), 0.86, 1.3), _at(_tone('sawtooth', 200, 0.04, 0.3332, 0.003), 0.92, 1.3),
        _at(_tone('sawtooth', 200, 0.04, 0.3332, 0.003), 0.98, 1.3),
    ]
    return _finalize(_mix(*L))
def hyena_cackle_001():
    L = [
        _at(_sweep('sawtooth', 700, 400, 0.1, 0.3255, 0.005), 0, 1.3), _at(_sweep('sawtooth', 670, 385, 0.1, 0.3255, 0.005), 0.128, 1.3), _at(_sweep('sawtooth', 640, 370, 0.1, 0.3255, 0.005), 0.252, 1.3),
        _at(_sweep('sawtooth', 610, 355, 0.1, 0.3255, 0.005), 0.372, 1.3), _at(_sweep('sawtooth', 580, 340, 0.1, 0.3255, 0.005), 0.488, 1.3), _at(_sweep('sawtooth', 550, 325, 0.1, 0.3255, 0.005), 0.6, 1.3),
        _at(_sweep('sawtooth', 520, 310, 0.1, 0.3255, 0.005), 0.708, 1.3), _at(_sweep('sawtooth', 490, 295, 0.1, 0.3255, 0.005), 0.812, 1.3), _at(_sweep('sawtooth', 460, 280, 0.1, 0.3255, 0.005), 0.912, 1.3),
        _at(_sweep('sawtooth', 430, 265, 0.1, 0.3255, 0.005), 1.008, 1.3), _at(_sweep('sawtooth', 400, 250, 0.1, 0.3255, 0.005), 1.1, 1.3), _at(_sweep('square', 350, 200, 0.1, 0.1302, 0.005), 0, 1.3),
        _at(_sweep('square', 335, 192, 0.1, 0.1302, 0.005), 0.128, 1.3), _at(_sweep('square', 320, 184, 0.1, 0.1302, 0.005), 0.252, 1.3), _at(_sweep('square', 305, 176, 0.1, 0.1302, 0.005), 0.372, 1.3),
        _at(_sweep('square', 290, 168, 0.1, 0.1302, 0.005), 0.488, 1.3), _at(_sweep('square', 275, 160, 0.1, 0.1302, 0.005), 0.6, 1.3), _at(_sweep('square', 260, 152, 0.1, 0.1302, 0.005), 0.708, 1.3),
        _at(_sweep('square', 245, 144, 0.1, 0.1302, 0.005), 0.812, 1.3), _at(_sweep('square', 230, 136, 0.1, 0.1302, 0.005), 0.912, 1.3), _at(_sweep('square', 215, 128, 0.1, 0.1302, 0.005), 1.008, 1.3),
        _at(_sweep('square', 200, 120, 0.1, 0.1302, 0.005), 1.1, 1.3), _at(_noise(0.08, 0.1953, 0.005, 671422, 'bandpass', 1500), 0, 1.3), _at(_noise(0.08, 0.1953, 0.005, 671423, 'bandpass', 1500), 0.128, 1.3),
        _at(_noise(0.08, 0.1953, 0.005, 671424, 'bandpass', 1500), 0.252, 1.3), _at(_noise(0.08, 0.1953, 0.005, 671425, 'bandpass', 1500), 0.372, 1.3), _at(_noise(0.08, 0.1953, 0.005, 671426, 'bandpass', 1500), 0.488, 1.3),
        _at(_noise(0.08, 0.1953, 0.005, 671427, 'bandpass', 1500), 0.6, 1.3), _at(_noise(0.08, 0.1953, 0.005, 671428, 'bandpass', 1500), 0.708, 1.3), _at(_noise(0.08, 0.1953, 0.005, 671429, 'bandpass', 1500), 0.812, 1.3),
        _at(_noise(0.08, 0.1953, 0.005, 671430, 'bandpass', 1500), 0.912, 1.3), _at(_noise(0.08, 0.1953, 0.005, 671431, 'bandpass', 1500), 1.008, 1.3), _at(_noise(0.08, 0.1953, 0.005, 671432, 'bandpass', 1500), 1.1, 1.3),
    ]
    return _finalize(_mix(*L))
def infra_airport_bell_001():
    L = [
        _at(_tone('sine', 880, 0.9, 0.3, 0.003), 0, 1.45), _at(_tone('sine', 1760, 0.5, 0.1, 0.003), 0, 1.45), _at(_tone('sine', 698, 0.9, 0.3, 0.003), 0.5, 1.45),
        _at(_tone('sine', 1396, 0.5, 0.1, 0.003), 0.5, 1.45), _at(_tone('sine', 2217, 0.5, 0.06, 0.003), 0, 1.45), _at(_tone('sine', 1760, 0.4, 0.05, 0.003), 0.5, 1.45),
    ]
    return _finalize(_mix(*L))
def infra_crosswalk_signal_001():
    L = [
        _at(_tone('sine', 1200, 0.12, 0.3, 0.003), 0, 1.25), _at(_tone('sine', 1200, 0.12, 0.3, 0.003), 0.3, 1.25), _at(_tone('sine', 1200, 0.12, 0.3, 0.003), 0.55, 1.25),
        _at(_tone('sine', 1200, 0.12, 0.3, 0.003), 0.75, 1.25), _at(_tone('sine', 1200, 0.12, 0.3, 0.003), 0.9, 1.25), _at(_tone('sine', 1200, 0.12, 0.3, 0.003), 1, 1.25),
        _at(_tone('sine', 1200, 0.12, 0.3, 0.003), 1.1, 1.25), _at(_tone('square', 1200, 0.1, 0.05, 0.003), 0, 1.25), _at(_tone('square', 1200, 0.1, 0.05, 0.003), 0.3, 1.25),
        _at(_tone('square', 1200, 0.1, 0.05, 0.003), 0.55, 1.25), _at(_tone('square', 1200, 0.1, 0.05, 0.003), 0.75, 1.25), _at(_tone('square', 1200, 0.1, 0.05, 0.003), 0.9, 1.25),
        _at(_tone('square', 1200, 0.1, 0.05, 0.003), 1, 1.25), _at(_tone('square', 1200, 0.1, 0.05, 0.003), 1.1, 1.25),
    ]
    return _finalize(_mix(*L))
def infra_parking_barrier_close_001():
    L = [
        _at(_sweep('sine', 200, 300, 0.6, 0.151, 0.05), 0, 0.9), _at(_sweep('sawtooth', 80, 100, 0.6, 0.151, 0.05), 0, 0.9), _at(_noise(0.6, 0.3775, 0.1, 671702, 'bandpass', 900), 0, 0.9),
        _at(_sweep('sine', 90, 50, 0.12, 0.604, 0.002), 0.6, 0.9), _at(_noise(0.03, 0.3775, 0.002, 671704, 'bandpass', 1500), 0.6, 0.9), _at(_sweep('sine', 120, 80, 0.08, 0.2265, 0.003), 0.75, 0.9),
        _at(_tone('sine', 1000, 0.1, 0.2265, 0.003), 0, 0.9), _at(_tone('sine', 1000, 0.1, 0.2265, 0.003), 0.25, 0.9), _at(_tone('sine', 1000, 0.1, 0.2265, 0.003), 0.5, 0.9),
    ]
    return _finalize(_mix(*L))
def infra_parking_barrier_open_001():
    L = [
        _at(_noise(0.02, 0.4086, 0.001, 671800, 'highpass', 3000), 0, 0.65), _at(_sweep('sine', 100, 70, 0.08, 0.4767, 0.002), 0, 0.65), _at(_sweep('sine', 200, 320, 0.45, 0.1634, 0.05), 0.05, 0.65),
        _at(_sweep('sawtooth', 70, 110, 0.45, 0.1362, 0.05), 0.05, 0.65), _at(_noise(0.45, 0.2724, 0.1, 671804, 'bandpass', 800), 0.05, 0.65), _at(_sweep('sine', 80, 55, 0.1, 0.4767, 0.002), 0.5, 0.65),
        _at(_tone('sine', 1400, 0.1, 0.2043, 0.003), 0.2, 0.65), _at(_tone('sine', 1400, 0.1, 0.2043, 0.003), 0.4, 0.65),
    ]
    return _finalize(_mix(*L))
def infra_train_track_clatter_001():
    L = [
        _at(_noise(1.6, 0.4183, 0.2, 671900, 'lowpass', 250), 0, 1.7), _at(_sweep('sawtooth', 45, 50, 1.6, 0.1673, 0.2), 0, 1.7), _at(_noise(0.03, 0.5856, 0.002, 671902, 'bandpass', 1200), 0, 1.7),
        _at(_noise(0.03, 0.5856, 0.002, 671903, 'bandpass', 1200), 0.22, 1.7), _at(_noise(0.03, 0.5856, 0.002, 671904, 'bandpass', 1200), 0.44, 1.7), _at(_noise(0.03, 0.5856, 0.002, 671905, 'bandpass', 1200), 0.66, 1.7),
        _at(_noise(0.03, 0.5856, 0.002, 671906, 'bandpass', 1200), 0.88, 1.7), _at(_noise(0.03, 0.5856, 0.002, 671907, 'bandpass', 1200), 1.1, 1.7), _at(_noise(0.03, 0.5856, 0.002, 671908, 'bandpass', 1200), 1.32, 1.7),
        _at(_noise(0.03, 0.5856, 0.002, 671909, 'bandpass', 1200), 1.54, 1.7), _at(_sweep('sine', 120, 80, 0.06, 0.5019, 0.002), 0, 1.7), _at(_sweep('sine', 120, 80, 0.06, 0.5019, 0.002), 0.22, 1.7),
        _at(_sweep('sine', 120, 80, 0.06, 0.5019, 0.002), 0.44, 1.7), _at(_sweep('sine', 120, 80, 0.06, 0.5019, 0.002), 0.66, 1.7), _at(_sweep('sine', 120, 80, 0.06, 0.5019, 0.002), 0.88, 1.7),
        _at(_sweep('sine', 120, 80, 0.06, 0.5019, 0.002), 1.1, 1.7), _at(_sweep('sine', 120, 80, 0.06, 0.5019, 0.002), 1.32, 1.7), _at(_sweep('sine', 120, 80, 0.06, 0.5019, 0.002), 1.54, 1.7),
        _at(_noise(0.025, 0.4183, 0.002, 671918, 'bandpass', 1500), 0.07, 1.7), _at(_noise(0.025, 0.4183, 0.002, 671919, 'bandpass', 1500), 0.29, 1.7), _at(_noise(0.025, 0.4183, 0.002, 671920, 'bandpass', 1500), 0.51, 1.7),
        _at(_noise(0.025, 0.4183, 0.002, 671921, 'bandpass', 1500), 0.73, 1.7), _at(_noise(0.025, 0.4183, 0.002, 671922, 'bandpass', 1500), 0.95, 1.7), _at(_noise(0.025, 0.4183, 0.002, 671923, 'bandpass', 1500), 1.17, 1.7),
        _at(_noise(0.025, 0.4183, 0.002, 671924, 'bandpass', 1500), 1.39, 1.7), _at(_noise(0.025, 0.4183, 0.002, 671925, 'bandpass', 1500), 1.61, 1.7),
    ]
    return _finalize(_mix(*L))
def mech_valve_hiss_001():
    L = [
        _at(_noise(0.9, 0.4, 0.02, 672000, 'highpass', 4000), 0, 1), _at(_noise(0.9, 0.15, 0.02, 672001, 'bandpass', 6000), 0, 1), _at(_sweep('sine', 100, 60, 0.06, 0.25, 0.002), 0, 1),
        _at(_noise(0.02, 0.2, 0.002, 672003, 'bandpass', 2000), 0, 1), _at(_tone('sine', 220, 0.9, 0.05, 0.05), 0, 1),
    ]
    return _finalize(_mix(*L))
def mosquito_near_ear_001():
    L = [
        _at(_sweep('sine', 500, 750, 0.7, 0.2966, 0.05), 0, 1.5), _at(_sweep('sine', 750, 480, 0.8, 0.2966, 0.02), 0.7, 1.5), _at(_sweep('sine', 1000, 1500, 0.7, 0.089, 0.05), 0, 1.5),
        _at(_sweep('sine', 1500, 960, 0.8, 0.089, 0.02), 0.7, 1.5), _at(_noise(1.5, 0.1186, 0.2, 672104, 'bandpass', 500), 0, 1.5),
    ]
    return _finalize(_mix(*L))
def owl_wing_pass_001():
    L = [
        _at(_noise(0.8, 1.4, 0.3, 672200, 'lowpass', 800), 0, 1), _at(_noise(0.8, 1.2, 0.3, 672201, 'bandpass', 400), 0, 1), _at(_tone('sine', 60, 0.1, 0.4, 0.01), 0, 1),
        _at(_noise(0.08, 1.2, 0.01, 672203, 'lowpass', 200), 0.1, 1), _at(_noise(0.08, 1.2, 0.01, 672204, 'lowpass', 200), 0.3, 1), _at(_noise(0.08, 1.2, 0.01, 672205, 'lowpass', 200), 0.5, 1),
    ]
    return _finalize(_mix(*L))
def potion_drink_001():
    L = [
        _at(_noise(0.8, 0.215, 0.1, 672300, 'bandpass', 1200), 0, 1.5), _at(_tone('sine', 880, 0.6, 0.172, 0.02), 0.9, 1.5), _at(_tone('sine', 1320, 0.5, 0.1433, 0.02), 0.95, 1.5),
        _at(_noise(0.4, 0.086, 0.1, 672303, 'highpass', 6000), 0.9, 1.5), _at(_sweep('sine', 200, 120, 0.12, 0.5015, 0.003), 0.2, 1.5), _at(_sweep('sine', 200, 120, 0.12, 0.5015, 0.003), 0.5, 1.5),
        _at(_sweep('sine', 200, 120, 0.12, 0.5015, 0.003), 0.8, 1.5), _at(_noise(0.1, 0.2866, 0.003, 672307, 'lowpass', 500), 0.2, 1.5), _at(_noise(0.1, 0.2866, 0.003, 672308, 'lowpass', 500), 0.5, 1.5),
        _at(_noise(0.1, 0.2866, 0.003, 672309, 'lowpass', 500), 0.8, 1.5), _at(_sweep('sine', 600, 1000, 0.04, 0.215, 0.003), 0.1, 1.5), _at(_sweep('sine', 600, 1000, 0.04, 0.215, 0.003), 0.35, 1.5),
        _at(_sweep('sine', 600, 1000, 0.04, 0.215, 0.003), 0.65, 1.5),
    ]
    return _finalize(_mix(*L))
def rope_swing_pass_001():
    L = [
        _at(_sweep('sawtooth', 150, 200, 0.3, 0.2267, 0.05), 0, 1.05), _at(_noise(0.3, 0.5667, 0.1, 672401, 'bandpass', 700), 0, 1.05), _at(_noise(0.8, 0.9068, 0.35, 672402, 'bandpass', 900), 0.2, 1.05),
        _at(_noise(0.8, 0.6801, 0.35, 672403, 'lowpass', 500), 0.2, 1.05), _at(_sweep('sine', 400, 250, 0.8, 0.2267, 0.3), 0.2, 1.05),
    ]
    return _finalize(_mix(*L))

OFFICIAL_PRESETS_G1_M7 = {
    'power-up-002': power_up_002,
    'alien-communication-001': alien_communication_001,
    'artifact-discovery-001': artifact_discovery_001,
    'boar-ground-snuffle-001': boar_ground_snuffle_001,
    'craft-hacksaw-metal-001': craft_hacksaw_metal_001,
    'craft-metal-filing-001': craft_metal_filing_001,
    'craft-paint-roller-001': craft_paint_roller_001,
    'domino-chain-fall-001': domino_chain_fall_001,
    'elephant-trumpet-001': elephant_trumpet_001,
    'env-geyser-mini-001': env_geyser_mini_001,
    'environment-rain-start-001': environment_rain_start_001,
    'forge-file-metal-001': forge_file_metal_001,
    'forge-glue-apply-001': forge_glue_apply_001,
    'frog-pond-croak-001': frog_pond_croak_001,
    'hyena-cackle-001': hyena_cackle_001,
    'infra-airport-bell-001': infra_airport_bell_001,
    'infra-crosswalk-signal-001': infra_crosswalk_signal_001,
    'infra-parking-barrier-close-001': infra_parking_barrier_close_001,
    'infra-parking-barrier-open-001': infra_parking_barrier_open_001,
    'infra-train-track-clatter-001': infra_train_track_clatter_001,
    'mech-valve-hiss-001': mech_valve_hiss_001,
    'mosquito-near-ear-001': mosquito_near_ear_001,
    'owl-wing-pass-001': owl_wing_pass_001,
    'potion-drink-001': potion_drink_001,
    'rope-swing-pass-001': rope_swing_pass_001,
}
