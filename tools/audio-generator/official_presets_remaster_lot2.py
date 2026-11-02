"""Remastering V1.1 - lot 2 : 31 sounds rebuilt with their own identity (sound + browser preview)."""
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


def react_field_generate_001():
    p1 = _at(_sweep('sine', 150.0, 900.0, 0.7, 0.328, 0.05), 0.0, 1.25)
    p2 = _at(_sweep('sawtooth', 300.0, 1800.0, 0.7, 0.075, 0.05), 0.0, 1.25)
    p3 = _at(_noise(0.7, 0.094, 0.2, 210003, 'bandpass', 1500.0), 0.0, 1.25)
    p4 = _at(_tone('sine', 220.0, 0.6, 0.281, 0.05), 0.6, 1.25)
    p5 = _at(_tone('sine', 226.0, 0.6, 0.234, 0.05), 0.6, 1.25)
    p6 = _at(_tone('triangle', 440.0, 0.5, 0.094, 0.05), 0.65, 1.25)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def craft_level_bubble_001():
    p1 = _at(_sweep('sine', 450.0, 900.0, 0.09, 0.4, 0.004), 0.0, 0.51)
    p2 = _at(_sweep('sine', 520.0, 1000.0, 0.07, 0.3, 0.004), 0.14, 0.51)
    p3 = _at(_noise(0.3, 0.06, 0.08, 211003, 'bandpass', 700.0), 0.02, 0.51)
    p4 = _at(_sweep('sine', 700.0, 1100.0, 0.05, 0.22, 0.003), 0.3, 0.51)
    p5 = _nticks('highpass', 0.004, 0.0005, 211300, [(0.46, 5000.0, 0.12)], 0.51)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def smart_device_activate_001():
    p1 = _at(_tone('triangle', 660.0, 0.14, 0.431, 0.01), 0.0, 0.65)
    p2 = _at(_tone('triangle', 880.0, 0.14, 0.431, 0.01), 0.11, 0.65)
    p3 = _at(_tone('triangle', 1320.0, 0.14, 0.431, 0.01), 0.22, 0.65)
    p4 = _at(_tone('sine', 2640.0, 0.3, 0.172, 0.003), 0.3, 0.65)
    p5 = _nticks('highpass', 0.004, 0.0005, 212300, [(0.0, 5000.0, 0.172), (0.3, 6000.0, 0.201)], 0.65)
    p6 = _at(_tone('sine', 330.0, 0.45, 0.172, 0.02), 0.0, 0.65)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def craft_staple_gun_001():
    p1 = _at(_sweep('sine', 160.0, 60.0, 0.07, 0.472, 0.002), 0.0, 0.23)
    p2 = _nticks('bandpass', 0.018, 0.0005, 213120, [(0.0, 2600.0, 0.515), (0.012, 3400.0, 0.301)], 0.23)
    p3 = _at(_tone('sine', 3300.0, 0.1, 0.155, 0.001), 0.005, 0.23)
    p4 = _at(_tone('sine', 4700.0, 0.06, 0.086, 0.001), 0.005, 0.23)
    p5 = _at(_noise(0.07, 0.103, 0.01, 213005, 'highpass', 4000.0), 0.11, 0.23)
    p6 = _at(_sweep('square', 900.0, 500.0, 0.02, 0.129, 0.001), 0.14, 0.23)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def craft_wire_snips_001():
    p1 = _at(_noise(0.07, 0.088, 0.03, 214001, 'bandpass', 900.0), 0.0, 0.2)
    p2 = _at(_noise(0.02, 0.438, 0.001, 214002, 'highpass', 5000.0), 0.08, 0.2)
    p3 = _at(_tone('sine', 2200.0, 0.07, 0.219, 0.001), 0.08, 0.2)
    p4 = _at(_tone('sine', 3300.0, 0.05, 0.158, 0.001), 0.08, 0.2)
    p5 = _at(_sweep('sine', 1100.0, 700.0, 0.05, 0.175, 0.002), 0.1, 0.2)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def veh_ignition_spark_001():
    p1 = _at(_sweep('sawtooth', 40.0, 55.0, 0.5, 0.266, 0.02), 0.0, 1.05)
    p2 = _tticks('square', 0.03, 0.001, [(0.0, 90.0, 0.213), (0.09, 95.0, 0.213), (0.17, 100.0, 0.234), (0.24, 105.0, 0.234), (0.3, 112.0, 0.255), (0.36, 120.0, 0.266), (0.41, 128.0, 0.266)], 1.05)
    p3 = _nticks('highpass', 0.012, 0.0005, 215180, [(0.1, 4500.0, 0.372), (0.21, 5200.0, 0.319), (0.32, 4800.0, 0.425), (0.44, 5600.0, 0.372), (0.47, 6000.0, 0.266)], 1.05)
    p4 = _at(_sweep('sawtooth', 55.0, 90.0, 0.5, 0.425, 0.03), 0.5, 1.05)
    p5 = _at(_noise(0.5, 0.128, 0.05, 215005, 'lowpass', 500.0), 0.5, 1.05)
    p6 = _nticks('highpass', 0.02, 0.001, 215360, [(0.5, 3000.0, 0.531)], 1.05)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def react_stabilizer_hum_001():
    p1 = _at(_tone('sine', 55.0, 1.5, 0.179, 0.04), 0.0, 1.55)
    p2 = _at(_tone('sine', 56.4, 1.5, 0.163, 0.04), 0.0, 1.55)
    p3 = _at(_tone('triangle', 110.0, 1.4, 0.051, 0.04), 0.0, 1.55)
    p4 = _at(_tone('sine', 165.0, 1.3, 0.026, 0.04), 0.1, 1.55)
    p5 = _at(_noise(1.4, 0.026, 0.04, 216005, 'lowpass', 300.0), 0.0, 1.55)
    p6 = _tticks('sine', 0.05, 0.005, [(0.4, 880.0, 0.02), (0.9, 990.0, 0.02), (1.35, 880.0, 0.02)], 1.55)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def sub_engine_hum_001():
    p1 = _at(_tone('sawtooth', 45.0, 1.5, 0.128, 0.04), 0.0, 1.55)
    p2 = _at(_tone('sine', 90.0, 1.5, 0.321, 0.04), 0.0, 1.55)
    p3 = _at(_tone('sine', 135.0, 1.3, 0.086, 0.04), 0.0, 1.55)
    p4 = _at(_noise(1.5, 0.086, 0.04, 217004, 'lowpass', 220.0), 0.0, 1.55)
    p5 = _nticks('lowpass', 0.09, 0.01, 217300, [(0.15, 160.0, 0.235), (0.37, 160.0, 0.235), (0.59, 160.0, 0.235), (0.81, 160.0, 0.235), (1.03, 160.0, 0.235), (1.25, 160.0, 0.235)], 1.55)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def forge_grindstone_spin_001():
    p1 = _at(_sweep('sawtooth', 70.0, 150.0, 0.35, 0.251, 0.05), 0.0, 1.05)
    p2 = _at(_tone('sawtooth', 150.0, 0.65, 0.209, 0.05), 0.35, 1.05)
    p3 = _at(_noise(0.95, 0.627, 0.15, 218003, 'bandpass', 1800.0), 0.0, 1.05)
    p4 = _at(_noise(0.95, 0.209, 0.2, 218004, 'highpass', 5000.0), 0.0, 1.05)
    p5 = _nticks('highpass', 0.012, 0.001, 218300, [(0.25, 3500.0, 0.46), (0.34, 3700.0, 0.46), (0.43, 3900.0, 0.46), (0.52, 4100.0, 0.46), (0.61, 3500.0, 0.46), (0.7, 3700.0, 0.46), (0.79, 3900.0, 0.46)], 1.05)
    p6 = _at(_sweep('sine', 2800.0, 2200.0, 0.5, 0.105, 0.1), 0.4, 1.05)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def robot_arm_move_001():
    p1 = _at(_sweep('square', 250.0, 400.0, 0.22, 0.277, 0.03), 0.05, 0.86)
    p2 = _at(_sweep('square', 400.0, 330.0, 0.18, 0.277, 0.02), 0.32, 0.86)
    p3 = _at(_sweep('square', 330.0, 520.0, 0.2, 0.277, 0.02), 0.52, 0.86)
    p4 = _at(_noise(0.65, 0.231, 0.1, 219004, 'bandpass', 2400.0), 0.05, 0.86)
    p5 = _nticks('lowpass', 0.02, 0.001, 219300, [(0.0, 900.0, 1.0), (0.74, 700.0, 1.0)], 0.86)
    p6 = _at(_tone('sine', 1400.0, 0.05, 0.277, 0.002), 0.76, 0.86)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def game_final_result_reveal_001():
    p1 = _nticks('highpass', 0.04, 0.002, 220060, [(0.02, 2500.0, 0.12), (0.099, 2500.0, 0.14), (0.159, 2500.0, 0.16), (0.204, 2500.0, 0.18), (0.236, 2500.0, 0.2), (0.257, 2500.0, 0.22), (0.271, 2500.0, 0.24), (0.277, 2500.0, 0.26), (0.279, 2500.0, 0.28), (0.276, 2500.0, 0.3)], 2.1)
    p2 = _tticks('triangle', 0.06, 0.003, [(0.0, 200.0, 0.15), (0.136, 240.0, 0.15), (0.265, 280.0, 0.15), (0.387, 320.0, 0.15), (0.505, 360.0, 0.15), (0.618, 400.0, 0.15), (0.728, 440.0, 0.15), (0.834, 480.0, 0.15), (0.938, 520.0, 0.15)], 2.1)
    p3 = _at(_tone('sawtooth', 262.0, 0.9, 0.16, 0.02), 1.0, 2.1)
    p4 = _at(_tone('sawtooth', 330.0, 0.9, 0.14, 0.02), 1.0, 2.1)
    p5 = _at(_tone('sawtooth', 392.0, 0.9, 0.14, 0.02), 1.0, 2.1)
    p6 = _at(_tone('sawtooth', 523.0, 0.9, 0.12, 0.02), 1.0, 2.1)
    p7 = _at(_noise(0.6, 0.2, 0.002, 220007, 'highpass', 6000.0), 1.0, 2.1)
    p8 = _at(_tone('sine', 2093.0, 0.7, 0.1, 0.002), 1.15, 2.1)
    p9 = _at(_tone('sine', 2637.0, 0.7, 0.1, 0.002), 1.25, 2.1)
    p10 = _at(_tone('sine', 3136.0, 0.7, 0.1, 0.002), 1.35, 2.1)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10))
def mech_turbine_spin_001():
    p1 = _at(_sweep('sawtooth', 120.0, 800.0, 1.1, 0.287, 0.04), 0.0, 1.65)
    p2 = _at(_tone('sawtooth', 800.0, 0.5, 0.16, 0.02), 1.1, 1.65)
    p3 = _at(_sweep('sine', 600.0, 2400.0, 1.1, 0.112, 0.04), 0.0, 1.65)
    p4 = _at(_tone('sine', 2400.0, 0.5, 0.08, 0.02), 1.1, 1.65)
    p5 = _at(_noise(1.5, 0.191, 0.04, 221005, 'highpass', 2500.0), 0.0, 1.65)
    p6 = _at(_noise(1.5, 0.16, 0.04, 221006, 'bandpass', 500.0), 0.0, 1.65)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def gravity_well_generate_001():
    p1 = _at(_sweep('sine', 400.0, 35.0, 1.2, 0.304, 0.05), 0.0, 1.6)
    p2 = _at(_sweep('sawtooth', 200.0, 30.0, 1.2, 0.087, 0.1), 0.0, 1.6)
    p3 = _at(_noise(1.2, 0.174, 0.5, 222003, 'lowpass', 300.0), 0.0, 1.6)
    p4 = _at(_sweep('sine', 200.0, 2000.0, 0.9, 0.043, 0.3), 0.0, 1.6)
    p5 = _at(_tone('sine', 40.0, 0.35, 0.347, 0.01), 1.2, 1.6)
    p6 = _at(_noise(0.3, 0.104, 0.01, 222006, 'lowpass', 150.0), 1.2, 1.6)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def lab_pipette_release_001():
    p1 = _at(_sweep('sine', 1800.0, 800.0, 0.05, 0.475, 0.002), 0.0, 0.29)
    p2 = _at(_sweep('sine', 1100.0, 650.0, 0.06, 0.299, 0.002), 0.11, 0.29)
    p3 = _nticks('highpass', 0.004, 0.0005, 223180, [(0.0, 5000.0, 0.272), (0.11, 4500.0, 0.163)], 0.29)
    p4 = _at(_sweep('sine', 900.0, 1500.0, 0.04, 0.163, 0.002), 0.2, 0.29)
    return _finalize(_mix(p1, p2, p3, p4))
def cyber_secure_channel_001():
    p1 = _at(_tone('square', 880.0, 0.07, 0.221, 0.003), 0.0, 0.67)
    p2 = _at(_tone('square', 1320.0, 0.07, 0.221, 0.003), 0.1, 0.67)
    p3 = _at(_tone('square', 1760.0, 0.09, 0.221, 0.003), 0.2, 0.67)
    p4 = _nticks('highpass', 0.006, 0.0005, 224240, [(0.34, 5000.0, 0.553)], 0.67)
    p5 = _at(_tone('sine', 2093.0, 0.28, 0.347, 0.003), 0.34, 0.67)
    p6 = _at(_tone('sine', 440.0, 0.3, 0.158, 0.01), 0.0, 0.67)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def react_containment_beep_001():
    p1 = _at(_tone('square', 1000.0, 0.12, 0.228, 0.003), 0.0, 0.77)
    p2 = _at(_tone('square', 800.0, 0.12, 0.228, 0.003), 0.18, 0.77)
    p3 = _at(_tone('square', 1000.0, 0.12, 0.228, 0.003), 0.36, 0.77)
    p4 = _at(_tone('square', 800.0, 0.18, 0.228, 0.003), 0.54, 0.77)
    p5 = _at(_tone('sine', 120.0, 0.7, 0.228, 0.02), 0.0, 0.77)
    p6 = _at(_noise(0.2, 0.057, 0.03, 225006, 'bandpass', 3000.0), 0.0, 0.77)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def deer_alarm_bark_001():
    p1 = _at(_sweep('sawtooth', 340.0, 180.0, 0.13, 0.224, 0.004), 0.0, 0.45)
    p2 = _at(_sweep('sine', 650.0, 330.0, 0.13, 0.224, 0.004), 0.0, 0.45)
    p3 = _at(_sweep('sine', 1250.0, 700.0, 0.1, 0.104, 0.004), 0.0, 0.45)
    p4 = _at(_noise(0.14, 0.134, 0.01, 226004, 'bandpass', 800.0), 0.0, 0.45)
    p5 = _at(_sweep('sawtooth', 360.0, 190.0, 0.15, 0.224, 0.004), 0.23, 0.45)
    p6 = _at(_sweep('sine', 690.0, 350.0, 0.15, 0.224, 0.004), 0.23, 0.45)
    p7 = _at(_sweep('sine', 1300.0, 720.0, 0.12, 0.104, 0.004), 0.23, 0.45)
    p8 = _at(_noise(0.17, 0.134, 0.01, 226008, 'bandpass', 850.0), 0.23, 0.45)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8))
def ruin_relic_hum_001():
    p1 = _at(_tone('sine', 80.0, 1.5, 0.169, 0.04), 0.0, 1.6)
    p2 = _at(_tone('sine', 80.7, 1.5, 0.158, 0.04), 0.0, 1.6)
    p3 = _at(_tone('sine', 200.0, 1.3, 0.045, 0.04), 0.1, 1.6)
    p4 = _at(_tone('triangle', 320.0, 1.2, 0.028, 0.04), 0.2, 1.6)
    p5 = _at(_noise(1.4, 0.034, 0.04, 227005, 'bandpass', 400.0), 0.0, 1.6)
    p6 = _tticks('sine', 0.5, 0.003, [(0.55, 880.0, 0.034), (1.05, 1320.0, 0.028)], 1.6)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def veh_mechanical_whine_001():
    p1 = _at(_sweep('sawtooth', 700.0, 1500.0, 0.4, 0.37, 0.05), 0.0, 0.85)
    p2 = _at(_sweep('sawtooth', 1500.0, 900.0, 0.4, 0.37, 0.02), 0.4, 0.85)
    p3 = _at(_sweep('sine', 2800.0, 3600.0, 0.4, 0.158, 0.05), 0.0, 0.85)
    p4 = _at(_sweep('sine', 3600.0, 2200.0, 0.4, 0.158, 0.02), 0.4, 0.85)
    p5 = _at(_noise(0.8, 0.317, 0.2, 228005, 'bandpass', 2500.0), 0.0, 0.85)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def spaceship_door_close_001():
    p1 = _at(_noise(0.35, 0.254, 0.02, 229001, 'highpass', 3000.0), 0.0, 0.8)
    p2 = _at(_sweep('sawtooth', 220.0, 100.0, 0.55, 0.085, 0.05), 0.0, 0.8)
    p3 = _at(_noise(0.5, 0.068, 0.05, 229003, 'bandpass', 700.0), 0.0, 0.8)
    p4 = _at(_sweep('sine', 95.0, 45.0, 0.2, 0.466, 0.003), 0.55, 0.8)
    p5 = _at(_noise(0.06, 0.339, 0.001, 229005, 'lowpass', 400.0), 0.55, 0.8)
    p6 = _at(_sweep('square', 1500.0, 800.0, 0.03, 0.152, 0.001), 0.62, 0.8)
    p7 = _nticks('highpass', 0.01, 0.001, 229420, [(0.7, 4500.0, 0.169)], 0.8)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7))
def spaceship_door_open_001():
    p1 = _at(_sweep('square', 1100.0, 1500.0, 0.025, 0.246, 0.001), 0.0, 0.94)
    p2 = _nticks('highpass', 0.01, 0.001, 230120, [(0.0, 4500.0, 0.341)], 0.94)
    p3 = _at(_noise(0.3, 0.409, 0.02, 230003, 'highpass', 3000.0), 0.08, 0.94)
    p4 = _at(_sweep('sawtooth', 100.0, 230.0, 0.6, 0.136, 0.1), 0.12, 0.94)
    p5 = _at(_noise(0.6, 0.109, 0.1, 230005, 'bandpass', 800.0), 0.12, 0.94)
    p6 = _at(_sweep('sine', 80.0, 50.0, 0.15, 0.409, 0.005), 0.74, 0.94)
    p7 = _at(_noise(0.12, 0.273, 0.003, 230007, 'lowpass', 500.0), 0.74, 0.94)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7))
def react_plasma_containment_001():
    p1 = _at(_tone('sine', 120.0, 1.0, 0.3, 0.05), 0.0, 1.05)
    p2 = _at(_tone('sine', 125.0, 1.0, 0.26, 0.05), 0.0, 1.05)
    p3 = _at(_sweep('sine', 300.0, 650.0, 1.0, 0.06, 0.2), 0.0, 1.05)
    p4 = _nticks('bandpass', 0.015, 0.001, 231240, [(0.04, 1500.0, 0.18), (0.115, 2497.0, 0.27), (0.19, 3494.0, 0.24), (0.265, 4491.0, 0.21), (0.34, 1988.0, 0.18), (0.415, 2985.0, 0.27), (0.49, 3982.0, 0.24), (0.565, 4979.0, 0.21), (0.64, 2476.0, 0.18), (0.715, 3473.0, 0.27), (0.79, 4470.0, 0.24), (0.865, 1967.0, 0.21), (0.94, 2964.0, 0.18)], 1.05)
    p5 = _at(_noise(1.0, 0.06, 0.2, 231005, 'bandpass', 1200.0), 0.0, 1.05)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def spaceship_radar_sweep_001():
    p1 = _at(_sweep('sine', 500.0, 2000.0, 0.5, 0.226, 0.04), 0.0, 0.95)
    p2 = _at(_noise(0.5, 0.075, 0.04, 232002, 'bandpass', 2500.0), 0.0, 0.95)
    p3 = _at(_tone('sine', 2600.0, 0.1, 0.503, 0.002), 0.52, 0.95)
    p4 = _at(_tone('sine', 2600.0, 0.1, 0.277, 0.002), 0.66, 0.95)
    p5 = _at(_tone('sine', 2600.0, 0.1, 0.126, 0.002), 0.8, 0.95)
    p6 = _at(_tone('sine', 1300.0, 0.3, 0.075, 0.01), 0.52, 0.95)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def sub_torpedo_tube_open_001():
    p1 = _at(_sweep('square', 220.0, 110.0, 0.08, 0.255, 0.001), 0.0, 0.95)
    p2 = _at(_tone('sine', 540.0, 0.35, 0.153, 0.001), 0.0, 0.95)
    p3 = _at(_tone('sine', 810.0, 0.2, 0.068, 0.001), 0.0, 0.95)
    p4 = _at(_noise(0.5, 0.17, 0.1, 233004, 'lowpass', 1500.0), 0.15, 0.95)
    p5 = _at(_sweep('sine', 60.0, 40.0, 0.3, 0.382, 0.02), 0.3, 0.95)
    p6 = _nticks('bandpass', 0.07, 0.01, 233360, [(0.5, 600.0, 0.153), (0.62, 500.0, 0.127), (0.74, 700.0, 0.102), (0.83, 450.0, 0.085)], 0.95)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def cyber_mainframe_connect_001():
    p1 = _tticks('square', 0.015, 0.001, [(0.0, 1200.0, 0.284), (0.03, 1877.0, 0.284), (0.06, 2554.0, 0.284), (0.09, 1431.0, 0.284), (0.12, 2108.0, 0.284), (0.15, 2785.0, 0.284), (0.18, 1662.0, 0.284), (0.21, 2339.0, 0.284), (0.24, 1216.0, 0.284), (0.27, 1893.0, 0.284), (0.3, 2570.0, 0.284), (0.33, 1447.0, 0.284), (0.36, 2124.0, 0.284), (0.39, 2801.0, 0.284)], 1.07)
    p2 = _at(_sweep('sine', 200.0, 400.0, 0.3, 0.228, 0.03), 0.0, 1.07)
    p3 = _at(_tone('triangle', 523.0, 0.12, 0.417, 0.005), 0.45, 1.07)
    p4 = _at(_tone('triangle', 659.0, 0.12, 0.417, 0.005), 0.54, 1.07)
    p5 = _at(_tone('triangle', 784.0, 0.12, 0.417, 0.005), 0.63, 1.07)
    p6 = _at(_tone('sine', 1047.0, 0.3, 0.379, 0.003), 0.72, 1.07)
    p7 = _at(_noise(0.35, 0.095, 0.1, 234007, 'bandpass', 3000.0), 0.0, 1.07)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7))
def tech_energy_siphon_001():
    p1 = _at(_sweep('sawtooth', 900.0, 120.0, 0.8, 0.152, 0.03), 0.0, 1.15)
    p2 = _at(_sweep('sine', 1500.0, 300.0, 0.8, 0.152, 0.03), 0.0, 1.15)
    p3 = _at(_noise(0.8, 0.195, 0.02, 235003, 'bandpass', 1500.0), 0.0, 1.15)
    p4 = _tticks('sine', 0.04, 0.002, [(0.08, 2400.0, 0.13), (0.21, 2180.0, 0.13), (0.36, 1960.0, 0.13), (0.53, 1740.0, 0.13), (0.72, 1520.0, 0.13), (0.93, 1300.0, 0.13)], 1.15)
    p5 = _at(_tone('sine', 70.0, 0.25, 0.487, 0.01), 0.85, 1.15)
    p6 = _at(_noise(0.1, 0.217, 0.003, 235006, 'lowpass', 300.0), 0.85, 1.15)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def spaceship_cryo_freeze_001():
    p1 = _tticks('sine', 0.12, 0.002, [(0.0, 3200.0, 0.193), (0.05, 3250.0, 0.189), (0.1, 3300.0, 0.184), (0.15, 2930.0, 0.179), (0.2, 2980.0, 0.174), (0.25, 3030.0, 0.169), (0.3, 2660.0, 0.164), (0.35, 2710.0, 0.16), (0.4, 2760.0, 0.155), (0.45, 2390.0, 0.15), (0.5, 2440.0, 0.145), (0.55, 2490.0, 0.14), (0.6, 2120.0, 0.135), (0.65, 2170.0, 0.131), (0.7, 2220.0, 0.126), (0.75, 1850.0, 0.121), (0.8, 1900.0, 0.116), (0.85, 1950.0, 0.111)], 1.3)
    p2 = _at(_noise(1.0, 0.145, 0.05, 236002, 'highpass', 6000.0), 0.0, 1.3)
    p3 = _at(_sweep('sine', 220.0, 80.0, 0.7, 0.302, 0.05), 0.3, 1.3)
    p4 = _nticks('highpass', 0.01, 0.0005, 236240, [(0.95, 6000.0, 0.544), (1.03, 5200.0, 0.363)], 1.3)
    p5 = _at(_sweep('sine', 1500.0, 1200.0, 0.3, 0.097, 0.01), 0.95, 1.3)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def unique_vehicle_boost_001():
    p1 = _at(_sweep('sine', 70.0, 35.0, 0.12, 0.651, 0.002), 0.0, 1.05)
    p2 = _at(_sweep('sawtooth', 120.0, 900.0, 0.7, 0.213, 0.05), 0.05, 1.05)
    p3 = _at(_sweep('square', 60.0, 450.0, 0.7, 0.071, 0.05), 0.05, 1.05)
    p4 = _at(_noise(0.7, 0.26, 0.4, 237004, 'bandpass', 900.0), 0.05, 1.05)
    p5 = _at(_noise(0.5, 0.237, 0.3, 237005, 'highpass', 2500.0), 0.4, 1.05)
    p6 = _at(_sweep('sawtooth', 900.0, 500.0, 0.25, 0.118, 0.005), 0.75, 1.05)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def spaceship_cryo_thaw_001():
    p1 = _at(_sweep('sine', 150.0, 400.0, 1.2, 0.277, 0.04), 0.0, 1.35)
    p2 = _at(_sweep('triangle', 300.0, 500.0, 1.2, 0.083, 0.04), 0.1, 1.35)
    p3 = _at(_noise(1.2, 0.069, 0.04, 238003, 'bandpass', 600.0), 0.0, 1.35)
    p4 = _nticks('highpass', 0.01, 0.0005, 238240, [(0.1, 5000.0, 0.485), (0.35, 6000.0, 0.415), (0.55, 5500.0, 0.554), (0.9, 4800.0, 0.415), (1.1, 6200.0, 0.346)], 1.35)
    p5 = _tticks('sine', 0.08, 0.002, [(0.2, 2400.0, 0.249), (0.45, 2000.0, 0.249), (0.6, 1800.0, 0.222), (0.85, 1500.0, 0.222), (1.0, 1300.0, 0.222), (1.2, 1200.0, 0.194)], 1.35)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def cyber_backdoor_open_001():
    p1 = _nticks('bandpass', 0.012, 0.0005, 239060, [(0.0, 2500.0, 0.822), (0.15, 3000.0, 0.822), (0.28, 2800.0, 0.914)], 0.99)
    p2 = _at(_tone('sawtooth', 60.0, 0.7, 0.146, 0.1), 0.0, 0.99)
    p3 = _at(_sweep('sine', 440.0, 330.0, 0.3, 0.274, 0.02), 0.3, 0.99)
    p4 = _at(_tone('sine', 880.0, 0.1, 0.457, 0.003), 0.62, 0.99)
    p5 = _at(_tone('sine', 1320.0, 0.2, 0.457, 0.003), 0.74, 0.99)
    p6 = _nticks('highpass', 0.006, 0.0005, 239360, [(0.62, 5000.0, 0.457)], 0.99)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def cyber_system_reboot_001():
    p1 = _at(_sweep('sine', 600.0, 90.0, 0.35, 0.373, 0.005), 0.0, 1.4)
    p2 = _at(_noise(0.3, 0.149, 0.02, 240002, 'lowpass', 400.0), 0.05, 1.4)
    p3 = _at(_noise(0.45, 0.062, 0.2, 240003, 'highpass', 4000.0), 0.55, 1.4)
    p4 = _at(_tone('square', 400.0, 0.1, 0.274, 0.003), 0.55, 1.4)
    p5 = _at(_tone('square', 600.0, 0.1, 0.274, 0.003), 0.67, 1.4)
    p6 = _at(_tone('square', 800.0, 0.1, 0.274, 0.003), 0.79, 1.4)
    p7 = _at(_tone('square', 1200.0, 0.1, 0.274, 0.003), 0.91, 1.4)
    p8 = _at(_tone('sine', 1800.0, 0.3, 0.187, 0.003), 1.05, 1.4)
    p9 = _at(_sweep('sine', 120.0, 200.0, 0.35, 0.224, 0.02), 0.55, 1.4)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8, p9))

OFFICIAL_PRESETS_REMASTER_LOT2 = {
    'react-field-generate-001': react_field_generate_001,
    'craft-level-bubble-001': craft_level_bubble_001,
    'smart-device-activate-001': smart_device_activate_001,
    'craft-staple-gun-001': craft_staple_gun_001,
    'craft-wire-snips-001': craft_wire_snips_001,
    'veh-ignition-spark-001': veh_ignition_spark_001,
    'react-stabilizer-hum-001': react_stabilizer_hum_001,
    'sub-engine-hum-001': sub_engine_hum_001,
    'forge-grindstone-spin-001': forge_grindstone_spin_001,
    'robot-arm-move-001': robot_arm_move_001,
    'game-final-result-reveal-001': game_final_result_reveal_001,
    'mech-turbine-spin-001': mech_turbine_spin_001,
    'gravity-well-generate-001': gravity_well_generate_001,
    'lab-pipette-release-001': lab_pipette_release_001,
    'cyber-secure-channel-001': cyber_secure_channel_001,
    'react-containment-beep-001': react_containment_beep_001,
    'deer-alarm-bark-001': deer_alarm_bark_001,
    'ruin-relic-hum-001': ruin_relic_hum_001,
    'veh-mechanical-whine-001': veh_mechanical_whine_001,
    'spaceship-door-close-001': spaceship_door_close_001,
    'spaceship-door-open-001': spaceship_door_open_001,
    'react-plasma-containment-001': react_plasma_containment_001,
    'spaceship-radar-sweep-001': spaceship_radar_sweep_001,
    'sub-torpedo-tube-open-001': sub_torpedo_tube_open_001,
    'cyber-mainframe-connect-001': cyber_mainframe_connect_001,
    'tech-energy-siphon-001': tech_energy_siphon_001,
    'spaceship-cryo-freeze-001': spaceship_cryo_freeze_001,
    'unique-vehicle-boost-001': unique_vehicle_boost_001,
    'spaceship-cryo-thaw-001': spaceship_cryo_thaw_001,
    'cyber-backdoor-open-001': cyber_backdoor_open_001,
    'cyber-system-reboot-001': cyber_system_reboot_001,
}
