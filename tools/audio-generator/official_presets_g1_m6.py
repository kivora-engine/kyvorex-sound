"""Generation 1 - module 6 : sons reconstruits (son WAV + apercu navigateur)."""
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

def mech_motor_start_001():
    L = []
    L.append(_at(_sweep('sawtooth', 35, 95, 1, 0.4095, 0.15), 0, 1.2))
    L.append(_at(_sweep('square', 70, 190, 1, 0.1365, 0.15), 0, 1.2))
    L.append(_at(_noise(1, 0.3412, 0.3, 660002, 'lowpass', 400), 0, 1.2))
    L.append(_at(_sweep('sine', 300, 900, 0.9, 0.1092, 0.2), 0.2, 1.2))
    L.append(_at(_sweep('sine', 90, 45, 0.08, 0.546, 0.002), 0, 1.2))
    L.append(_at(_noise(0.03, 0.2047, 0.001, 660005, 'bandpass', 1800), 0, 1.2))
    return _finalize(_mix(*L))
def mech_motor_stop_001():
    L = []
    L.append(_at(_sweep('sawtooth', 95, 30, 0.7, 0.3789, 0.01), 0, 0.85))
    L.append(_at(_sweep('square', 190, 60, 0.7, 0.1263, 0.01), 0, 0.85))
    L.append(_at(_noise(0.6, 0.2526, 0.02, 660102, 'lowpass', 350), 0, 0.85))
    L.append(_at(_sweep('sine', 900, 200, 0.45, 0.0884, 0.01), 0, 0.85))
    L.append(_at(_sweep('sine', 60, 40, 0.1, 0.442, 0.002), 0.5, 0.85))
    L.append(_at(_noise(0.08, 0.2526, 0.002, 660105, 'lowpass', 300), 0.5, 0.85))
    return _finalize(_mix(*L))
def ruin_block_move_001():
    L = []
    L.append(_at(_noise(0.8, 0.5, 0.15, 660200, 'bandpass', 220), 0, 1))
    L.append(_at(_noise(0.85, 0.5, 0.15, 660201, 'lowpass', 120), 0, 1))
    L.append(_at(_sweep('sine', 55, 45, 0.85, 0.3, 0.1), 0, 1))
    L.append(_at(_noise(0.05, 0.1, 0.003, 660203, 'bandpass', 1800), 0.15, 1))
    L.append(_at(_noise(0.05, 0.1, 0.003, 660204, 'bandpass', 1800), 0.35, 1))
    L.append(_at(_noise(0.05, 0.1, 0.003, 660205, 'bandpass', 1800), 0.55, 1))
    L.append(_at(_sweep('sine', 70, 40, 0.15, 0.4, 0.002), 0.72, 1))
    L.append(_at(_noise(0.1, 0.3, 0.002, 660207, 'lowpass', 300), 0.72, 1))
    return _finalize(_mix(*L))
def ruin_rune_glow_001():
    L = []
    L.append(_at(_tone('sine', 392, 1.4, 0.22, 0.4), 0, 1.5))
    L.append(_at(_tone('sine', 588, 1.4, 0.15, 0.5), 0, 1.5))
    L.append(_at(_tone('sine', 784, 1.3, 0.1, 0.6), 0.1, 1.5))
    L.append(_at(_tone('sine', 396, 1.4, 0.2, 0.4), 0, 1.5))
    L.append(_at(_tone('triangle', 196, 1.4, 0.12, 0.3), 0, 1.5))
    L.append(_at(_sweep('sine', 1500, 3000, 0.8, 0.05, 0.2), 0.3, 1.5))
    return _finalize(_mix(*L))
def ruin_statue_turn_001():
    L = []
    L.append(_at(_noise(1, 0.8333, 0.2, 660400, 'bandpass', 180), 0, 1.25))
    L.append(_at(_noise(1.05, 0.7575, 0.2, 660401, 'lowpass', 100), 0, 1.25))
    L.append(_at(_sweep('sawtooth', 48, 58, 1, 0.1818, 0.2), 0, 1.25))
    L.append(_at(_noise(0.03, 0.1818, 0.002, 660403, 'bandpass', 2500), 0.15, 1.25))
    L.append(_at(_noise(0.03, 0.1818, 0.002, 660404, 'bandpass', 2500), 0.35, 1.25))
    L.append(_at(_noise(0.03, 0.1818, 0.002, 660405, 'bandpass', 2500), 0.6, 1.25))
    L.append(_at(_noise(0.03, 0.1818, 0.002, 660406, 'bandpass', 2500), 0.85, 1.25))
    L.append(_at(_sweep('sine', 60, 35, 0.18, 0.606, 0.002), 1, 1.25))
    L.append(_at(_noise(0.12, 0.4545, 0.002, 660408, 'lowpass', 250), 1, 1.25))
    return _finalize(_mix(*L))
def sub_airlock_open_001():
    L = []
    L.append(_at(_noise(0.05, 0.3636, 0.001, 660500, 'bandpass', 1200), 0, 1.1))
    L.append(_at(_sweep('sine', 110, 70, 0.2, 0.4242, 0.002), 0, 1.1))
    L.append(_at(_tone('sine', 440, 0.5, 0.1212, 0.003), 0.02, 1.1))
    L.append(_at(_tone('triangle', 880, 0.4, 0.0606, 0.003), 0.02, 1.1))
    L.append(_at(_noise(0.7, 0.2666, 0.05, 660504, 'highpass', 3500), 0.25, 1.1))
    L.append(_at(_sweep('sawtooth', 70, 110, 0.6, 0.1454, 0.1), 0.25, 1.1))
    L.append(_at(_sweep('sine', 60, 90, 0.6, 0.1454, 0.1), 0.25, 1.1))
    L.append(_at(_sweep('sine', 80, 50, 0.15, 0.4242, 0.002), 0.8, 1.1))
    return _finalize(_mix(*L))
def sub_sonar_sweep_001():
    L = []
    L.append(_at(_tone('sine', 1400, 1.2, 0.35, 0.003), 0, 1.8))
    L.append(_at(_tone('sine', 1400, 0.8, 0.15, 0.003), 0.45, 1.8))
    L.append(_at(_tone('sine', 1400, 0.8, 0.07, 0.003), 0.9, 1.8))
    L.append(_at(_sweep('sine', 900, 1500, 0.1, 0.15, 0.005), 0, 1.8))
    L.append(_at(_tone('sine', 90, 1.7, 0.12, 0.2), 0, 1.8))
    L.append(_at(_noise(1.7, 0.1, 0.3, 660605, 'bandpass', 600), 0, 1.8))
    return _finalize(_mix(*L))
def sub_underwater_scan_001():
    L = []
    L.append(_at(_sweep('sine', 600, 1800, 0.6, 0.3266, 0.05), 0, 1.6))
    L.append(_at(_sweep('sine', 600, 1800, 0.6, 0.1633, 0.05), 0.55, 1.6))
    L.append(_at(_noise(1.5, 0.245, 0.3, 660702, 'lowpass', 500), 0, 1.6))
    L.append(_at(_tone('sine', 80, 1.5, 0.245, 0.2), 0, 1.6))
    L.append(_at(_tone('sine', 2200, 0.04, 0.196, 0.002), 1.1, 1.6))
    L.append(_at(_tone('sine', 2200, 0.04, 0.196, 0.002), 1.2, 1.6))
    L.append(_at(_tone('sine', 2200, 0.04, 0.196, 0.002), 1.3, 1.6))
    L.append(_at(_sweep('sine', 400, 800, 0.05, 0.1633, 0.003), 0.2, 1.6))
    L.append(_at(_sweep('sine', 400, 800, 0.05, 0.1633, 0.003), 0.8, 1.6))
    L.append(_at(_sweep('sine', 400, 800, 0.05, 0.1633, 0.003), 1.4, 1.6))
    return _finalize(_mix(*L))
def camel_call_001():
    L = []
    L.append(_at(_sweep('sawtooth', 150, 110, 1, 0.25, 0.08), 0, 1.1))
    L.append(_at(_sweep('sawtooth', 300, 220, 1, 0.1, 0.08), 0, 1.1))
    L.append(_at(_noise(1, 0.2, 0.1, 660802, 'bandpass', 900), 0, 1.1))
    L.append(_at(_sweep('sawtooth', 153, 112, 1, 0.2, 0.08), 0, 1.1))
    L.append(_at(_sweep('square', 75, 60, 1, 0.1, 0.05), 0, 1.1))
    L.append(_at(_sweep('sawtooth', 110, 80, 0.3, 0.15, 0.02), 0.78, 1.1))
    return _finalize(_mix(*L))
def epic_artifact_awaken_001():
    L = []
    L.append(_at(_tone('sine', 55, 2, 0.35, 0.6), 0, 2.2))
    L.append(_at(_tone('sawtooth', 110, 2, 0.1, 0.8), 0, 2.2))
    L.append(_at(_sweep('sine', 200, 1200, 1.5, 0.2, 0.3), 0, 2.2))
    L.append(_at(_tone('sine', 262, 1.5, 0.12, 0.7), 0.5, 2.2))
    L.append(_at(_tone('sine', 330, 1.5, 0.12, 0.7), 0.5, 2.2))
    L.append(_at(_tone('sine', 392, 1.5, 0.12, 0.7), 0.5, 2.2))
    L.append(_at(_noise(1.2, 0.1, 0.6, 660906, 'highpass', 5000), 0.6, 2.2))
    L.append(_at(_sweep('sine', 70, 40, 0.4, 0.4, 0.002), 1.4, 2.2))
    L.append(_at(_tone('sine', 1568, 0.7, 0.12, 0.003), 1.4, 2.2))
    return _finalize(_mix(*L))
def explosion_small_001():
    L = []
    L.append(_at(_sweep('sine', 120, 35, 0.6, 0.5, 0.002), 0, 1))
    L.append(_at(_noise(0.6, 0.6, 0.003, 661001, 'lowpass', 900), 0, 1))
    L.append(_at(_noise(0.05, 0.3, 0.001, 661002, 'highpass', 2500), 0, 1))
    L.append(_at(_tone('sine', 45, 0.9, 0.25, 0.02), 0, 1))
    L.append(_at(_noise(0.02, 0.12, 0.002, 661004, 'bandpass', 2500), 0.15, 1))
    L.append(_at(_noise(0.02, 0.12, 0.002, 661005, 'bandpass', 2500), 0.28, 1))
    L.append(_at(_noise(0.02, 0.12, 0.002, 661006, 'bandpass', 2500), 0.4, 1))
    L.append(_at(_noise(0.02, 0.12, 0.002, 661007, 'bandpass', 2500), 0.55, 1))
    return _finalize(_mix(*L))
def game_tie_break_start_001():
    L = []
    L.append(_at(_sweep('sine', 100, 60, 0.12, 0.45, 0.002), 0, 1.4))
    L.append(_at(_sweep('sine', 100, 60, 0.12, 0.45, 0.002), 0.15, 1.4))
    L.append(_at(_sweep('sine', 100, 60, 0.12, 0.45, 0.002), 0.3, 1.4))
    L.append(_at(_sweep('sine', 100, 60, 0.12, 0.45, 0.002), 0.45, 1.4))
    L.append(_at(_sweep('sine', 100, 60, 0.12, 0.45, 0.002), 0.6, 1.4))
    L.append(_at(_noise(0.02, 0.15, 0.001, 661105, 'highpass', 4000), 0, 1.4))
    L.append(_at(_noise(0.02, 0.15, 0.001, 661106, 'highpass', 4000), 0.15, 1.4))
    L.append(_at(_noise(0.02, 0.15, 0.001, 661107, 'highpass', 4000), 0.3, 1.4))
    L.append(_at(_noise(0.02, 0.15, 0.001, 661108, 'highpass', 4000), 0.45, 1.4))
    L.append(_at(_noise(0.02, 0.15, 0.001, 661109, 'highpass', 4000), 0.6, 1.4))
    L.append(_at(_sweep('sawtooth', 300, 600, 0.5, 0.1, 0.05), 0.6, 1.4))
    L.append(_at(_tone('triangle', 330, 0.6, 0.2, 0.01), 0.8, 1.4))
    L.append(_at(_tone('triangle', 440, 0.6, 0.2, 0.01), 0.8, 1.4))
    L.append(_at(_tone('sine', 1760, 0.2, 0.12, 0.002), 1.1, 1.4))
    return _finalize(_mix(*L))
def game_timer_expire_001():
    L = []
    L.append(_at(_tone('square', 880, 0.15, 0.2, 0.005), 0, 1.1))
    L.append(_at(_tone('square', 660, 0.15, 0.2, 0.005), 0.18, 1.1))
    L.append(_at(_tone('square', 440, 0.25, 0.2, 0.005), 0.36, 1.1))
    L.append(_at(_tone('sawtooth', 110, 0.5, 0.25, 0.01), 0.55, 1.1))
    L.append(_at(_noise(0.5, 0.08, 0.02, 661204, 'bandpass', 1500), 0.55, 1.1))
    L.append(_at(_sweep('sine', 80, 45, 0.15, 0.35, 0.002), 0.55, 1.1))
    return _finalize(_mix(*L))
def laser_grid_activate_001():
    L = []
    L.append(_at(_sweep('sine', 200, 2000, 0.5, 0.356, 0.05), 0, 1.2))
    L.append(_at(_sweep('sawtooth', 100, 1000, 0.5, 0.1139, 0.05), 0, 1.2))
    L.append(_at(_tone('square', 120, 0.65, 0.1424, 0.05), 0.45, 1.2))
    L.append(_at(_tone('sine', 240, 0.65, 0.1709, 0.05), 0.45, 1.2))
    L.append(_at(_noise(0.06, 0.1139, 0.002, 661304, 'highpass', 6000), 0.5, 1.2))
    L.append(_at(_sweep('sawtooth', 3000, 800, 0.06, 0.1709, 0.002), 0.5, 1.2))
    L.append(_at(_sweep('sawtooth', 3000, 800, 0.06, 0.1709, 0.002), 0.58, 1.2))
    L.append(_at(_sweep('sawtooth', 3000, 800, 0.06, 0.1709, 0.002), 0.66, 1.2))
    L.append(_at(_sweep('sawtooth', 3000, 800, 0.06, 0.1709, 0.002), 0.74, 1.2))
    return _finalize(_mix(*L))
def rope_climb_strain_001():
    L = []
    L.append(_at(_sweep('sawtooth', 180, 240, 0.18, 0.3708, 0.02), 0, 1))
    L.append(_at(_sweep('sawtooth', 200, 150, 0.15, 0.3708, 0.02), 0.3, 1))
    L.append(_at(_sweep('sawtooth', 160, 230, 0.2, 0.3708, 0.02), 0.55, 1))
    L.append(_at(_noise(0.25, 0.8652, 0.05, 661403, 'bandpass', 800), 0, 1))
    L.append(_at(_noise(0.25, 0.8652, 0.05, 661404, 'bandpass', 800), 0.3, 1))
    L.append(_at(_noise(0.25, 0.8652, 0.05, 661405, 'bandpass', 800), 0.55, 1))
    L.append(_at(_tone('triangle', 90, 0.9, 0.2472, 0.05), 0, 1))
    L.append(_at(_noise(0.04, 0.3708, 0.003, 661407, 'bandpass', 400), 0.15, 1))
    L.append(_at(_noise(0.04, 0.3708, 0.003, 661408, 'bandpass', 400), 0.45, 1))
    L.append(_at(_noise(0.04, 0.3708, 0.003, 661409, 'bandpass', 400), 0.8, 1))
    return _finalize(_mix(*L))
def ruin_ancient_magic_001():
    L = []
    L.append(_at(_tone('sine', 220, 1.6, 0.25, 0.5), 0, 1.8))
    L.append(_at(_tone('sine', 330, 1.6, 0.18, 0.6), 0, 1.8))
    L.append(_at(_tone('sine', 440, 1.6, 0.14, 0.6), 0, 1.8))
    L.append(_at(_sweep('sine', 300, 1800, 1, 0.1, 0.3), 0.3, 1.8))
    L.append(_at(_tone('sine', 1320, 0.9, 0.1, 0.003), 0.9, 1.8))
    L.append(_at(_noise(1.4, 0.12, 0.5, 661505, 'bandpass', 2500), 0, 1.8))
    L.append(_at(_tone('sine', 55, 1.7, 0.2, 0.4), 0, 1.8))
    return _finalize(_mix(*L))
def ruin_glyph_light_001():
    L = []
    L.append(_at(_tone('sine', 880, 0.25, 0.3098, 0.003), 0, 1.2))
    L.append(_at(_tone('sine', 1108, 0.25, 0.3098, 0.003), 0.1, 1.2))
    L.append(_at(_tone('sine', 1318, 0.25, 0.3098, 0.003), 0.2, 1.2))
    L.append(_at(_tone('sine', 1760, 0.4, 0.3098, 0.003), 0.3, 1.2))
    L.append(_at(_tone('sine', 440, 1, 0.1859, 0.3), 0, 1.2))
    L.append(_at(_noise(0.6, 0.0743, 0.3, 661605, 'highpass', 6000), 0, 1.2))
    L.append(_at(_tone('sine', 2637, 0.15, 0.1239, 0.003), 0.6, 1.2))
    L.append(_at(_tone('sine', 2637, 0.15, 0.1239, 0.003), 0.75, 1.2))
    return _finalize(_mix(*L))
def sub_dive_alarm_001():
    L = []
    L.append(_at(_sweep('square', 520, 470, 0.42, 0.271, 0.01), 0, 1.6))
    L.append(_at(_sweep('square', 520, 470, 0.42, 0.271, 0.01), 0.5, 1.6))
    L.append(_at(_sweep('square', 520, 470, 0.42, 0.271, 0.01), 1, 1.6))
    L.append(_at(_tone('sawtooth', 260, 0.4, 0.1232, 0.01), 0, 1.6))
    L.append(_at(_tone('sawtooth', 260, 0.4, 0.1232, 0.01), 0.5, 1.6))
    L.append(_at(_tone('sawtooth', 260, 0.4, 0.1232, 0.01), 1, 1.6))
    L.append(_at(_sweep('sawtooth', 70, 55, 1.4, 0.0986, 0.1), 0, 1.6))
    L.append(_at(_noise(1.5, 0.1478, 0.2, 661707, 'lowpass', 400), 0, 1.6))
    L.append(_at(_tone('sine', 100, 1.5, 0.1232, 0.1), 0, 1.6))
    return _finalize(_mix(*L))
def sub_oxygen_warning_001():
    L = []
    L.append(_at(_tone('sine', 1000, 0.15, 0.4113, 0.005), 0, 1.5))
    L.append(_at(_tone('sine', 1000, 0.15, 0.4113, 0.005), 0.3, 1.5))
    L.append(_at(_tone('sine', 1000, 0.15, 0.4113, 0.005), 0.6, 1.5))
    L.append(_at(_sweep('sine', 800, 300, 0.5, 0.2742, 0.01), 0.85, 1.5))
    L.append(_at(_noise(0.5, 0.1645, 0.05, 661804, 'highpass', 4000), 0.85, 1.5))
    L.append(_at(_noise(0.4, 0.2056, 0.05, 661805, 'highpass', 5000), 0.1, 1.5))
    return _finalize(_mix(*L))
def tool_drill_metal_001():
    L = []
    L.append(_at(_sweep('sawtooth', 180, 260, 0.7, 0.25, 0.05), 0, 0.85))
    L.append(_at(_sweep('square', 360, 520, 0.7, 0.1, 0.05), 0, 0.85))
    L.append(_at(_sweep('sine', 3200, 3600, 0.65, 0.15, 0.1), 0, 0.85))
    L.append(_at(_noise(0.7, 0.3125, 0.1, 661903, 'highpass', 4500), 0, 0.85))
    L.append(_at(_noise(0.7, 0.3125, 0.1, 661904, 'bandpass', 2500), 0, 0.85))
    L.append(_at(_sweep('sawtooth', 260, 120, 0.25, 0.1875, 0.01), 0.6, 0.85))
    return _finalize(_mix(*L))
def tool_drill_wood_001():
    L = []
    L.append(_at(_sweep('sawtooth', 140, 180, 0.7, 0.3287, 0.05), 0, 0.85))
    L.append(_at(_sweep('square', 280, 360, 0.7, 0.1052, 0.05), 0, 0.85))
    L.append(_at(_noise(0.7, 0.4602, 0.1, 662002, 'lowpass', 1800), 0, 0.85))
    L.append(_at(_noise(0.7, 0.263, 0.1, 662003, 'bandpass', 900), 0, 0.85))
    L.append(_at(_tone('sine', 70, 0.7, 0.1972, 0.05), 0, 0.85))
    L.append(_at(_sweep('sawtooth', 180, 90, 0.25, 0.1972, 0.01), 0.6, 0.85))
    return _finalize(_mix(*L))
def tool_sandpaper_rub_001():
    L = []
    L.append(_at(_noise(0.35, 0.4, 0.1, 662100, 'highpass', 2500), 0, 1.15))
    L.append(_at(_noise(0.35, 0.15, 0.1, 662101, 'bandpass', 5000), 0, 1.15))
    L.append(_at(_noise(0.35, 0.4, 0.1, 662102, 'highpass', 2500), 0.4, 1.15))
    L.append(_at(_noise(0.35, 0.15, 0.1, 662103, 'bandpass', 5000), 0.4, 1.15))
    L.append(_at(_noise(0.3, 0.4, 0.1, 662104, 'highpass', 2500), 0.8, 1.15))
    L.append(_at(_noise(0.3, 0.15, 0.1, 662105, 'bandpass', 5000), 0.8, 1.15))
    return _finalize(_mix(*L))
def underwater_movement_001():
    L = []
    L.append(_at(_noise(0.6, 0.6849, 0.2, 662200, 'lowpass', 600), 0, 1.4))
    L.append(_at(_noise(0.6, 0.5871, 0.2, 662201, 'lowpass', 400), 0.6, 1.4))
    L.append(_at(_tone('sine', 70, 1.3, 0.2348, 0.2), 0, 1.4))
    L.append(_at(_sweep('sine', 900, 1500, 0.03, 0.1957, 0.002), 0.3, 1.4))
    L.append(_at(_sweep('sine', 300, 600, 0.08, 0.4893, 0.005), 0.1, 1.4))
    L.append(_at(_sweep('sine', 250, 500, 0.08, 0.4893, 0.005), 0.5, 1.4))
    L.append(_at(_sweep('sine', 350, 700, 0.08, 0.4893, 0.005), 0.9, 1.4))
    return _finalize(_mix(*L))
def unique_vent_crawl_001():
    L = []
    L.append(_at(_sweep('sine', 160, 110, 0.1, 0.662, 0.002), 0, 1.8))
    L.append(_at(_sweep('sine', 160, 110, 0.1, 0.662, 0.002), 0.5, 1.8))
    L.append(_at(_sweep('sine', 160, 110, 0.1, 0.662, 0.002), 0.95, 1.8))
    L.append(_at(_sweep('sine', 160, 110, 0.1, 0.662, 0.002), 1.4, 1.8))
    L.append(_at(_noise(0.12, 0.4138, 0.003, 662304, 'bandpass', 700), 0, 1.8))
    L.append(_at(_noise(0.12, 0.4138, 0.003, 662305, 'bandpass', 700), 0.5, 1.8))
    L.append(_at(_noise(0.12, 0.4138, 0.003, 662306, 'bandpass', 700), 0.95, 1.8))
    L.append(_at(_noise(0.12, 0.4138, 0.003, 662307, 'bandpass', 700), 1.4, 1.8))
    L.append(_at(_tone('sine', 480, 0.3, 0.1324, 0.003), 0, 1.8))
    L.append(_at(_tone('sine', 480, 0.3, 0.1324, 0.003), 0.5, 1.8))
    L.append(_at(_tone('sine', 480, 0.3, 0.1324, 0.003), 0.95, 1.8))
    L.append(_at(_tone('sine', 480, 0.3, 0.1324, 0.003), 1.4, 1.8))
    L.append(_at(_noise(0.3, 0.331, 0.05, 662312, 'bandpass', 1500), 0.15, 1.8))
    L.append(_at(_noise(0.3, 0.331, 0.05, 662313, 'bandpass', 1500), 0.65, 1.8))
    L.append(_at(_noise(0.3, 0.331, 0.05, 662314, 'bandpass', 1500), 1.1, 1.8))
    L.append(_at(_noise(1.7, 0.2482, 0.3, 662315, 'lowpass', 500), 0, 1.8))
    return _finalize(_mix(*L))
def chest_open_001():
    L = []
    L.append(_at(_sweep('sawtooth', 140, 260, 0.5, 0.1481, 0.1), 0, 1.25))
    L.append(_at(_noise(0.45, 0.3085, 0.1, 662401, 'bandpass', 1000), 0, 1.25))
    L.append(_at(_noise(0.015, 0.3702, 0.001, 662402, 'highpass', 4000), 0, 1.25))
    L.append(_at(_tone('sine', 1800, 0.04, 0.1851, 0.001), 0, 1.25))
    L.append(_at(_sweep('sine', 100, 50, 0.15, 0.4319, 0.002), 0.42, 1.25))
    L.append(_at(_tone('sine', 784, 0.6, 0.2468, 0.003), 0.52, 1.25))
    L.append(_at(_tone('sine', 988, 0.6, 0.2468, 0.003), 0.62, 1.25))
    L.append(_at(_tone('sine', 1318, 0.5, 0.2468, 0.003), 0.72, 1.25))
    L.append(_at(_tone('sine', 1568, 0.4, 0.1851, 0.003), 0.77, 1.25))
    L.append(_at(_noise(0.4, 0.074, 0.2, 662409, 'highpass', 7000), 0.57, 1.25))
    return _finalize(_mix(*L))

OFFICIAL_PRESETS_G1_M6 = {
    'mech-motor-start-001': mech_motor_start_001,
    'mech-motor-stop-001': mech_motor_stop_001,
    'ruin-block-move-001': ruin_block_move_001,
    'ruin-rune-glow-001': ruin_rune_glow_001,
    'ruin-statue-turn-001': ruin_statue_turn_001,
    'sub-airlock-open-001': sub_airlock_open_001,
    'sub-sonar-sweep-001': sub_sonar_sweep_001,
    'sub-underwater-scan-001': sub_underwater_scan_001,
    'camel-call-001': camel_call_001,
    'epic-artifact-awaken-001': epic_artifact_awaken_001,
    'explosion-small-001': explosion_small_001,
    'game-tie-break-start-001': game_tie_break_start_001,
    'game-timer-expire-001': game_timer_expire_001,
    'laser-grid-activate-001': laser_grid_activate_001,
    'rope-climb-strain-001': rope_climb_strain_001,
    'ruin-ancient-magic-001': ruin_ancient_magic_001,
    'ruin-glyph-light-001': ruin_glyph_light_001,
    'sub-dive-alarm-001': sub_dive_alarm_001,
    'sub-oxygen-warning-001': sub_oxygen_warning_001,
    'tool-drill-metal-001': tool_drill_metal_001,
    'tool-drill-wood-001': tool_drill_wood_001,
    'tool-sandpaper-rub-001': tool_sandpaper_rub_001,
    'underwater-movement-001': underwater_movement_001,
    'unique-vent-crawl-001': unique_vent_crawl_001,
    'chest-open-001': chest_open_001,
}
