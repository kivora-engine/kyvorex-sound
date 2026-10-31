"""Mission 13 - Fortifications & Siege Machines (25 sounds)."""
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

def _tone(wave_type, freq, dur, amplitude, attack):
    n = int(dur * SR)
    if n <= 0: return []
    env = _env_exp(n, attack)
    return [amplitude * _wave_sample(wave_type, 2.0 * math.pi * freq * i / SR) * env[i] for i in range(n)]

def _sweep(wave_type, f0, f1, dur, amplitude, attack):
    n = int(dur * SR)
    if n <= 0: return []
    env = _env_exp(n, attack)
    out = []
    phase = 0.0
    for i in range(n):
        t = i / float(max(1, n - 1))
        f = f0 * ((f1 / f0) ** t)
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

def _noise(dur, amplitude, attack, seed=1, ftype=None, freq=None):
    n = int(dur * SR)
    if n <= 0: return []
    env = _env_exp(n, attack)
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


def fort_drawbridge_lower_001():
    p1 = _nticks('bandpass', 0.02, 0.001, 130060, [(0.0, 2300.0, 0.12), (0.1, 2331.0, 0.123), (0.193, 2362.0, 0.127), (0.279, 2393.0, 0.13), (0.36, 2424.0, 0.134), (0.435, 2455.0, 0.137), (0.504, 2486.0, 0.141), (0.569, 2517.0, 0.144), (0.629, 2548.0, 0.148), (0.685, 2579.0, 0.151), (0.737, 2610.0, 0.154), (0.786, 2641.0, 0.158), (0.831, 2672.0, 0.161), (0.872, 2703.0, 0.165), (0.911, 2734.0, 0.168), (0.948, 2765.0, 0.172), (0.981, 2796.0, 0.175), (1.013, 2827.0, 0.179), (1.042, 2858.0, 0.182), (1.069, 2889.0, 0.186), (1.094, 2920.0, 0.189), (1.117, 2951.0, 0.192), (1.139, 2982.0, 0.196), (1.159, 3013.0, 0.199), (1.178, 3044.0, 0.203), (1.196, 3075.0, 0.206), (1.212, 3106.0, 0.21), (1.227, 3137.0, 0.213), (1.241, 3168.0, 0.217), (1.254, 3200.0, 0.22)], 2.15)
    p2 = _at(_sweep('sawtooth', 90.0, 120.0, 1.6, 0.08, 0.3), 0.0, 2.15)
    p3 = _at(_sweep('sine', 70.0, 35.0, 0.3, 0.5, 0.002), 1.7, 2.15)
    p4 = _at(_noise(0.12, 0.5, 0.002, 130004, 'lowpass', 500.0), 1.7, 2.15)
    p5 = _at(_sweep('sine', 90.0, 50.0, 0.15, 0.2, 0.002), 1.95, 2.15)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def fort_drawbridge_raise_creak_001():
    p1 = _at(_sweep('sawtooth', 70.0, 95.0, 2.2, 0.082, 0.3), 0.0, 2.45)
    p2 = _at(_sweep('triangle', 140.0, 190.0, 2.0, 0.069, 0.3), 0.1, 2.45)
    p3 = _at(_noise(2.2, 0.103, 0.4, 131003, 'bandpass', 500.0), 0.0, 2.45)
    p4 = _nticks('bandpass', 0.015, 0.001, 131240, [(0.2, 3000.0, 0.137), (0.5, 3000.0, 0.137), (0.8, 3000.0, 0.137), (1.1, 3000.0, 0.137), (1.4, 3000.0, 0.137), (1.7, 3000.0, 0.137), (2.0, 3000.0, 0.137)], 2.45)
    p5 = _at(_noise(0.03, 0.275, 0.001, 131005, 'highpass', 2500.0), 2.3, 2.45)
    p6 = _at(_sweep('sine', 150.0, 80.0, 0.1, 0.24, 0.002), 2.3, 2.45)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def fort_portcullis_drop_001():
    p1 = _at(_noise(0.6, 0.224, 0.02, 132001, 'bandpass', 2500.0), 0.0, 1.37)
    p2 = _nticks('highpass', 0.02, 0.001, 132120, [(0.0, 3500.0, 0.112), (0.08, 3590.0, 0.122), (0.15, 3681.0, 0.132), (0.212, 3772.0, 0.142), (0.267, 3863.0, 0.153), (0.315, 3954.0, 0.163), (0.357, 4045.0, 0.173), (0.394, 4136.0, 0.183), (0.427, 4227.0, 0.193), (0.456, 4318.0, 0.204), (0.481, 4409.0, 0.213), (0.503, 4500.0, 0.224)], 1.37)
    p3 = _at(_sweep('sine', 60.0, 30.0, 0.35, 0.41, 0.002), 0.62, 1.37)
    p4 = _at(_noise(0.15, 0.373, 0.001, 132004, 'lowpass', 700.0), 0.62, 1.37)
    p5 = _at(_tone('sine', 420.0, 0.7, 0.075, 0.002), 0.62, 1.37)
    p6 = _at(_tone('sine', 1160.0, 0.5, 0.052, 0.002), 0.62, 1.37)
    p7 = _at(_tone('sine', 2300.0, 0.3, 0.03, 0.002), 0.62, 1.37)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7))
def fort_portcullis_ratchet_raise_001():
    p1 = _nticks('bandpass', 0.01, 0.0005, 133060, [(0.0, 1800.0, 1.0), (0.12, 2400.0, 1.0), (0.24, 1800.0, 1.0), (0.36, 2400.0, 1.0), (0.48, 1800.0, 1.0), (0.6, 2400.0, 1.0), (0.72, 1800.0, 1.0), (0.84, 2400.0, 1.0), (0.96, 1800.0, 1.0), (1.08, 2400.0, 1.0), (1.2, 1800.0, 1.0), (1.3199999999999998, 2400.0, 1.0), (1.44, 1800.0, 1.0), (1.56, 2400.0, 1.0), (1.68, 1800.0, 1.0)], 1.85)
    p2 = _at(_sweep('triangle', 110.0, 130.0, 1.8, 0.305, 0.4), 0.0, 1.85)
    p3 = _at(_noise(1.8, 0.305, 0.5, 133003, 'lowpass', 400.0), 0.0, 1.85)
    return _finalize(_mix(p1, p2, p3))
def fort_gate_bar_drop_001():
    p1 = _at(_sweep('sine', 110.0, 60.0, 0.15, 0.5, 0.001), 0.0, 0.47)
    p2 = _at(_noise(0.05, 0.4, 0.001, 134002, 'bandpass', 600.0), 0.0, 0.47)
    p3 = _at(_sweep('sine', 90.0, 55.0, 0.12, 0.3, 0.001), 0.22, 0.47)
    p4 = _tticks('triangle', 0.02, 0.0005, [(0.3, 700.0, 0.15), (0.4, 600.0, 0.1)], 0.47)
    p5 = _at(_noise(0.4, 0.1, 0.02, 134005, 'lowpass', 300.0), 0.0, 0.47)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def fort_murder_hole_pour_001():
    p1 = _at(_noise(1.2, 0.508, 0.1, 135001, 'bandpass', 1800.0), 0.0, 1.65)
    p2 = _at(_noise(1.4, 0.363, 0.2, 135002, 'highpass', 5500.0), 0.2, 1.65)
    p3 = _at(_sweep('sine', 200.0, 100.0, 0.08, 0.436, 0.002), 0.1, 1.65)
    p4 = _tticks('sine', 0.03, 0.002, [(0.326, 754.0, 0.269), (0.448, 776.0, 0.242), (0.652, 573.0, 0.176), (0.704, 476.0, 0.193), (0.781, 761.0, 0.25), (0.85, 305.0, 0.227), (0.974, 426.0, 0.193), (1.109, 622.0, 0.205), (1.115, 689.0, 0.215), (1.16, 744.0, 0.195), (1.407, 318.0, 0.177), (1.467, 360.0, 0.269)], 1.65)
    p5 = _at(_noise(0.6, 0.145, 0.2, 135005, 'highpass', 7000.0), 1.0, 1.65)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def fort_longbow_twang_whoosh_001():
    p1 = _at(_sweep('sine', 180.0, 170.0, 0.5, 0.321, 0.001), 0.0, 0.61)
    p2 = _at(_sweep('sine', 360.0, 340.0, 0.4, 0.143, 0.001), 0.0, 0.61)
    p3 = _at(_sweep('sine', 540.0, 510.0, 0.3, 0.071, 0.001), 0.0, 0.61)
    p4 = _at(_noise(0.01, 0.285, 0.0005, 136004, 'highpass', 3000.0), 0.0, 0.61)
    p5 = _at(_noise(0.45, 0.178, 0.1, 136005, 'bandpass', 3000.0), 0.03, 0.61)
    p6 = _at(_sweep('sine', 250.0, 120.0, 0.06, 0.214, 0.001), 0.5, 0.61)
    p7 = _at(_noise(0.03, 0.214, 0.001, 136007, 'bandpass', 900.0), 0.5, 0.61)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7))
def fort_crossbow_winch_latch_001():
    p1 = _nticks('bandpass', 0.01, 0.0005, 137060, [(0.0, 2000.0, 0.248), (0.07, 2040.0, 0.248), (0.14, 2080.0, 0.248), (0.21000000000000002, 2120.0, 0.248), (0.28, 2160.0, 0.248), (0.35000000000000003, 2200.0, 0.248), (0.42000000000000004, 2240.0, 0.248), (0.49000000000000005, 2280.0, 0.248), (0.56, 2320.0, 0.248), (0.6300000000000001, 2360.0, 0.248), (0.7000000000000001, 2400.0, 0.248), (0.77, 2440.0, 0.248), (0.8400000000000001, 2480.0, 0.248), (0.9100000000000001, 2520.0, 0.248)], 1.18)
    p2 = _at(_sweep('triangle', 200.0, 420.0, 1.0, 0.083, 0.1), 0.0, 1.18)
    p3 = _at(_noise(0.012, 0.413, 0.0005, 137003, 'highpass', 3500.0), 1.1, 1.18)
    p4 = _at(_sweep('sine', 1400.0, 800.0, 0.03, 0.248, 0.001), 1.1, 1.18)
    return _finalize(_mix(p1, p2, p3, p4))
def fort_ballista_release_001():
    p1 = _at(_noise(0.03, 0.5, 0.0005, 138001, 'lowpass', 900.0), 0.0, 0.55)
    p2 = _at(_sweep('sine', 90.0, 50.0, 0.2, 0.55, 0.001), 0.0, 0.55)
    p3 = _at(_sweep('sawtooth', 140.0, 100.0, 0.5, 0.2, 0.001), 0.0, 0.55)
    p4 = _at(_sweep('sine', 280.0, 250.0, 0.5, 0.15, 0.001), 0.0, 0.55)
    p5 = _at(_noise(0.35, 0.25, 0.03, 138005, 'bandpass', 2000.0), 0.05, 0.55)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def fort_catapult_arm_swing_001():
    p1 = _at(_sweep('sawtooth', 80.0, 200.0, 0.8, 0.1, 0.3), 0.0, 1.35)
    p2 = _at(_sweep('triangle', 160.0, 360.0, 0.7, 0.08, 0.3), 0.0, 1.35)
    p3 = _at(_noise(0.5, 0.35, 0.1, 139003, 'bandpass', 1800.0), 0.8, 1.35)
    p4 = _at(_sweep('sine', 70.0, 35.0, 0.25, 0.55, 0.002), 0.95, 1.35)
    p5 = _at(_noise(0.1, 0.4, 0.001, 139005, 'lowpass', 500.0), 0.95, 1.35)
    p6 = _tticks('triangle', 0.03, 0.0005, [(1.05, 500.0, 0.2), (1.12, 430.0, 0.15), (1.22, 380.0, 0.1)], 1.35)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def fort_trebuchet_weight_drop_001():
    p1 = _at(_noise(0.12, 0.35, 0.002, 140001, 'highpass', 2500.0), 0.0, 1.75)
    p2 = _at(_sweep('sine', 75.0, 45.0, 1.2, 0.263, 0.1), 0.0, 1.75)
    p3 = _at(_sweep('sine', 50.0, 28.0, 0.4, 0.526, 0.002), 0.45, 1.75)
    p4 = _at(_noise(0.2, 0.438, 0.002, 140004, 'lowpass', 200.0), 0.45, 1.75)
    p5 = _at(_sweep('sawtooth', 100.0, 70.0, 1.2, 0.088, 0.2), 0.5, 1.75)
    p6 = _nticks('bandpass', 0.02, 0.001, 140360, [(0.621, 647.0, 0.148), (0.851, 923.0, 0.088), (0.922, 657.0, 0.117), (0.932, 731.0, 0.128), (1.149, 963.0, 0.103), (1.356, 785.0, 0.138)], 1.75)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def fort_stone_incoming_whistle_001():
    p1 = _at(_sweep('sine', 1800.0, 500.0, 1.3, 0.2, 0.4), 0.0, 1.91)
    p2 = _at(_noise(1.3, 0.2, 0.5, 141002, 'bandpass', 2500.0), 0.0, 1.91)
    p3 = _at(_sweep('sine', 70.0, 35.0, 0.3, 0.55, 0.002), 1.4, 1.91)
    p4 = _at(_noise(0.3, 0.5, 0.002, 141004, 'lowpass', 600.0), 1.4, 1.91)
    p5 = _nticks('lowpass', 0.03, 0.001, 141300, [(1.549, 1488.0, 0.248), (1.583, 1410.0, 0.199), (1.622, 841.0, 0.152), (1.689, 1106.0, 0.138), (1.752, 1383.0, 0.226), (1.807, 536.0, 0.174), (1.82, 521.0, 0.221), (1.83, 753.0, 0.213)], 1.91)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def fort_battering_ram_hit_001():
    p1 = _at(_sweep('sine', 65.0, 30.0, 0.5, 0.506, 0.002), 0.0, 0.85)
    p2 = _at(_noise(0.15, 0.422, 0.001, 142002, 'lowpass', 500.0), 0.0, 0.85)
    p3 = _at(_noise(0.08, 0.338, 0.001, 142003, 'bandpass', 2500.0), 0.02, 0.85)
    p4 = _at(_sweep('triangle', 200.0, 120.0, 0.7, 0.101, 0.02), 0.1, 0.85)
    p5 = _at(_noise(0.7, 0.127, 0.1, 142005, 'bandpass', 900.0), 0.1, 0.85)
    p6 = _nticks('bandpass', 0.02, 0.001, 142360, [(0.133, 2944.0, 0.168), (0.139, 2864.0, 0.181), (0.219, 2097.0, 0.145), (0.231, 1681.0, 0.149), (0.264, 2544.0, 0.126), (0.34, 2135.0, 0.127), (0.347, 1862.0, 0.209), (0.605, 3226.0, 0.106)], 0.85)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def fort_siege_ladder_clack_001():
    p1 = _tticks('triangle', 0.04, 0.001, [(0.0, 900.0, 0.503), (0.07, 700.0, 0.378), (0.5, 800.0, 0.378), (0.58, 650.0, 0.252)], 0.95)
    p2 = _at(_noise(0.03, 0.503, 0.001, 143002, 'bandpass', 1500.0), 0.0, 0.95)
    p3 = _at(_noise(0.35, 0.252, 0.05, 143003, 'bandpass', 1100.0), 0.1, 0.95)
    p4 = _at(_sweep('triangle', 300.0, 250.0, 0.3, 0.076, 0.02), 0.6, 0.95)
    return _finalize(_mix(p1, p2, p3, p4))
def fort_siege_tower_roll_001():
    p1 = _at(_noise(2.8, 0.608, 0.4, 144001, 'lowpass', 250.0), 0.0, 2.85)
    p2 = _at(_sweep('sawtooth', 55.0, 62.0, 2.8, 0.174, 0.5), 0.0, 2.85)
    p3 = _at(_sweep('triangle', 700.0, 760.0, 2.5, 0.069, 0.6), 0.2, 2.85)
    p4 = _at(_sweep('sine', 65.0, 40.0, 0.12, 0.434, 0.002), 0.0, 2.85)
    p5 = _at(_sweep('sine', 65.0, 40.0, 0.12, 0.434, 0.002), 0.5, 2.85)
    p6 = _at(_sweep('sine', 65.0, 40.0, 0.12, 0.434, 0.002), 1.0, 2.85)
    p7 = _at(_sweep('sine', 65.0, 40.0, 0.12, 0.434, 0.002), 1.5, 2.85)
    p8 = _at(_sweep('sine', 65.0, 40.0, 0.12, 0.434, 0.002), 2.0, 2.85)
    p9 = _at(_sweep('sine', 65.0, 40.0, 0.12, 0.434, 0.002), 2.5, 2.85)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8, p9))
def fort_grapple_hook_catch_001():
    p1 = _at(_noise(0.4, 0.15, 0.05, 145001, 'bandpass', 2000.0), 0.0, 1.3)
    p2 = _at(_sweep('sine', 2400.0, 2200.0, 0.2, 0.25, 0.001), 0.42, 1.3)
    p3 = _at(_tone('sine', 3300.0, 0.15, 0.15, 0.001), 0.42, 1.3)
    p4 = _at(_noise(0.01, 0.4, 0.0005, 145004, 'highpass', 4000.0), 0.42, 1.3)
    p5 = _at(_noise(0.3, 0.1, 0.05, 145005, 'bandpass', 1500.0), 0.5, 1.3)
    p6 = _at(_sweep('triangle', 180.0, 200.0, 0.4, 0.1, 0.1), 0.85, 1.3)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def fort_war_horn_call_001():
    p1 = _at(_tone('sawtooth', 116.0, 0.9, 0.417, 0.12), 0.0, 1.95)
    p2 = _at(_tone('sawtooth', 117.5, 0.9, 0.298, 0.12), 0.0, 1.95)
    p3 = _at(_tone('square', 232.0, 0.9, 0.119, 0.15), 0.0, 1.95)
    p4 = _at(_noise(0.15, 0.223, 0.03, 146004, 'bandpass', 900.0), 0.0, 1.95)
    p5 = _at(_tone('sawtooth', 155.0, 1.0, 0.417, 0.1), 0.9, 1.95)
    p6 = _at(_tone('sawtooth', 156.5, 1.0, 0.298, 0.1), 0.9, 1.95)
    p7 = _at(_tone('square', 310.0, 1.0, 0.119, 0.12), 0.9, 1.95)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7))
def fort_alarm_bell_frantic_001():
    p1 = _tticks('sine', 0.5, 0.001, [(0.0, 620.0, 0.317), (0.22, 620.0, 0.317), (0.44, 620.0, 0.317), (0.66, 620.0, 0.317), (0.88, 620.0, 0.317), (1.1, 620.0, 0.317), (1.32, 620.0, 0.317), (1.54, 620.0, 0.317)], 2.09)
    p2 = _tticks('sine', 0.35, 0.001, [(0.0, 1730.0, 0.152), (0.22, 1730.0, 0.152), (0.44, 1730.0, 0.152), (0.66, 1730.0, 0.152), (0.88, 1730.0, 0.152), (1.1, 1730.0, 0.152), (1.32, 1730.0, 0.152), (1.54, 1730.0, 0.152)], 2.09)
    p3 = _tticks('sine', 0.25, 0.001, [(0.0, 3350.0, 0.076), (0.22, 3350.0, 0.076), (0.44, 3350.0, 0.076), (0.66, 3350.0, 0.076), (0.88, 3350.0, 0.076), (1.1, 3350.0, 0.076), (1.32, 3350.0, 0.076), (1.54, 3350.0, 0.076)], 2.09)
    p4 = _nticks('highpass', 0.01, 0.0005, 147240, [(0.0, 3500.0, 0.254), (0.22, 3500.0, 0.254), (0.44, 3500.0, 0.254), (0.66, 3500.0, 0.254), (0.88, 3500.0, 0.254), (1.1, 3500.0, 0.254), (1.32, 3500.0, 0.254), (1.54, 3500.0, 0.254)], 2.09)
    return _finalize(_mix(p1, p2, p3, p4))
def fort_stake_barricade_set_001():
    p1 = _tticks('triangle', 0.05, 0.001, [(0.0, 600.0, 0.522), (0.25, 520.0, 0.522), (0.5, 680.0, 0.522), (0.8, 560.0, 0.457)], 1.25)
    p2 = _nticks('lowpass', 0.03, 0.001, 148120, [(0.0, 1000.0, 0.392), (0.25, 1000.0, 0.392), (0.5, 1000.0, 0.392), (0.8, 1000.0, 0.392)], 1.25)
    p3 = _at(_sweep('triangle', 260.0, 230.0, 0.3, 0.078, 0.05), 0.9, 1.25)
    return _finalize(_mix(p1, p2, p3))
def fort_shield_wall_lock_001():
    p1 = _nticks('bandpass', 0.04, 0.001, 149060, [(0.0, 900.0, 0.898), (0.03, 1100.0, 0.898), (0.05, 800.0, 0.898), (0.09, 1000.0, 0.808), (0.12, 700.0, 0.808), (0.16, 950.0, 0.718)], 0.93)
    p2 = _tticks('triangle', 0.08, 0.001, [(0.0, 200.0, 0.539), (0.05, 230.0, 0.539), (0.1, 180.0, 0.539), (0.15, 210.0, 0.539)], 0.93)
    p3 = _at(_tone('sine', 700.0, 0.5, 0.144, 0.001), 0.02, 0.93)
    p4 = _nticks('highpass', 0.02, 0.001, 149240, [(0.274, 4218.0, 0.171), (0.38, 3927.0, 0.171), (0.468, 4016.0, 0.21), (0.564, 4027.0, 0.242), (0.81, 3541.0, 0.253), (0.863, 3977.0, 0.214)], 0.93)
    return _finalize(_mix(p1, p2, p3, p4))
def fort_cell_bars_clang_001():
    p1 = _at(_noise(0.02, 0.303, 0.0005, 150001, 'highpass', 3000.0), 0.0, 0.95)
    p2 = _at(_tone('sine', 320.0, 0.9, 0.182, 0.001), 0.0, 0.95)
    p3 = _at(_tone('sine', 883.0, 0.7, 0.121, 0.001), 0.0, 0.95)
    p4 = _at(_tone('sine', 1730.0, 0.5, 0.073, 0.001), 0.0, 0.95)
    p5 = _at(_tone('sine', 2850.0, 0.35, 0.049, 0.001), 0.0, 0.95)
    p6 = _at(_tone('sine', 323.0, 0.9, 0.091, 0.001), 0.0, 0.95)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def fort_moat_heavy_splash_001():
    p1 = _at(_sweep('sine', 150.0, 45.0, 0.3, 0.5, 0.002), 0.0, 1.29)
    p2 = _at(_noise(0.25, 0.45, 0.002, 151002, 'bandpass', 900.0), 0.0, 1.29)
    p3 = _at(_noise(1.0, 0.3, 0.01, 151003, 'highpass', 2500.0), 0.03, 1.29)
    p4 = _tticks('sine', 0.04, 0.002, [(0.437, 491.0, 0.182), (0.593, 859.0, 0.106), (0.653, 866.0, 0.103), (0.785, 952.0, 0.194), (0.796, 525.0, 0.127), (0.854, 778.0, 0.136), (0.956, 720.0, 0.119), (1.057, 437.0, 0.119), (1.182, 507.0, 0.164), (1.197, 742.0, 0.155)], 1.29)
    p5 = _at(_noise(1.1, 0.2, 0.2, 151005, 'lowpass', 300.0), 0.1, 1.29)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def fort_chain_snap_whip_001():
    p1 = _at(_sweep('sawtooth', 150.0, 320.0, 0.35, 0.065, 0.2), 0.0, 0.88)
    p2 = _at(_noise(0.012, 0.446, 0.0005, 152002, 'highpass', 3500.0), 0.36, 0.88)
    p3 = _at(_sweep('sine', 3000.0, 300.0, 0.1, 0.243, 0.001), 0.36, 0.88)
    p4 = _nticks('bandpass', 0.02, 0.001, 152240, [(0.416, 2011.0, 0.107), (0.422, 2879.0, 0.172), (0.485, 3220.0, 0.124), (0.522, 3135.0, 0.114), (0.578, 2286.0, 0.183), (0.6, 2634.0, 0.143), (0.656, 3249.0, 0.115), (0.699, 2336.0, 0.2), (0.793, 2319.0, 0.114), (0.811, 3487.0, 0.142)], 0.88)
    p5 = _at(_sweep('sine', 80.0, 50.0, 0.1, 0.243, 0.002), 0.6, 0.88)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def fort_armored_patrol_march_001():
    p1 = _at(_sweep('sine', 110.0, 70.0, 0.08, 0.419, 0.002), 0.0, 1.33)
    p2 = _at(_sweep('sine', 110.0, 70.0, 0.08, 0.419, 0.002), 0.38, 1.33)
    p3 = _at(_sweep('sine', 110.0, 70.0, 0.08, 0.419, 0.002), 0.76, 1.33)
    p4 = _at(_sweep('sine', 110.0, 70.0, 0.08, 0.419, 0.002), 1.14, 1.33)
    p5 = _nticks('bandpass', 0.03, 0.001, 153300, [(0.0, 1100.0, 0.359), (0.38, 1100.0, 0.359), (0.76, 1100.0, 0.359), (1.14, 1100.0, 0.359)], 1.33)
    p6 = _tticks('sine', 0.04, 0.001, [(0.02, 3000.0, 0.144), (0.05, 3800.0, 0.12), (0.1, 2700.0, 0.096), (0.4, 3000.0, 0.144), (0.43, 3800.0, 0.12), (0.48, 2700.0, 0.096), (0.78, 3000.0, 0.144), (0.81, 3800.0, 0.12), (0.86, 2700.0, 0.096), (1.16, 3000.0, 0.144), (1.19, 3800.0, 0.12), (1.24, 2700.0, 0.096)], 1.33)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def fort_banner_unfurl_flap_001():
    p1 = _at(_noise(0.4, 0.536, 0.1, 154001, 'bandpass', 900.0), 0.0, 1.53)
    p2 = _nticks('lowpass', 0.06, 0.003, 154120, [(0.35, 700.0, 0.938), (0.5, 700.0, 0.884), (0.62, 700.0, 0.804), (0.75, 700.0, 0.75), (0.85, 700.0, 0.67), (0.97, 700.0, 0.589), (1.06, 700.0, 0.536), (1.16, 700.0, 0.482), (1.28, 700.0, 0.429), (1.42, 700.0, 0.402)], 1.53)
    p3 = _nticks('highpass', 0.02, 0.001, 154180, [(0.35, 2500.0, 0.402), (0.62, 2500.0, 0.402), (0.85, 2500.0, 0.402), (1.06, 2500.0, 0.402), (1.28, 2500.0, 0.402)], 1.53)
    p4 = _at(_sweep('triangle', 300.0, 330.0, 0.4, 0.134, 0.1), 0.0, 1.53)
    return _finalize(_mix(p1, p2, p3, p4))

OFFICIAL_PRESETS_FORTRESS = {
    'fort-drawbridge-lower-001': fort_drawbridge_lower_001,
    'fort-drawbridge-raise-creak-001': fort_drawbridge_raise_creak_001,
    'fort-portcullis-drop-001': fort_portcullis_drop_001,
    'fort-portcullis-ratchet-raise-001': fort_portcullis_ratchet_raise_001,
    'fort-gate-bar-drop-001': fort_gate_bar_drop_001,
    'fort-murder-hole-pour-001': fort_murder_hole_pour_001,
    'fort-longbow-twang-whoosh-001': fort_longbow_twang_whoosh_001,
    'fort-crossbow-winch-latch-001': fort_crossbow_winch_latch_001,
    'fort-ballista-release-001': fort_ballista_release_001,
    'fort-catapult-arm-swing-001': fort_catapult_arm_swing_001,
    'fort-trebuchet-weight-drop-001': fort_trebuchet_weight_drop_001,
    'fort-stone-incoming-whistle-001': fort_stone_incoming_whistle_001,
    'fort-battering-ram-hit-001': fort_battering_ram_hit_001,
    'fort-siege-ladder-clack-001': fort_siege_ladder_clack_001,
    'fort-siege-tower-roll-001': fort_siege_tower_roll_001,
    'fort-grapple-hook-catch-001': fort_grapple_hook_catch_001,
    'fort-war-horn-call-001': fort_war_horn_call_001,
    'fort-alarm-bell-frantic-001': fort_alarm_bell_frantic_001,
    'fort-stake-barricade-set-001': fort_stake_barricade_set_001,
    'fort-shield-wall-lock-001': fort_shield_wall_lock_001,
    'fort-cell-bars-clang-001': fort_cell_bars_clang_001,
    'fort-moat-heavy-splash-001': fort_moat_heavy_splash_001,
    'fort-chain-snap-whip-001': fort_chain_snap_whip_001,
    'fort-armored-patrol-march-001': fort_armored_patrol_march_001,
    'fort-banner-unfurl-flap-001': fort_banner_unfurl_flap_001,
}
