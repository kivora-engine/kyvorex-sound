"""Mission 11 - Microfauna & Plant Life (25 sounds)."""
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


def micro_seed_pod_burst_001():
    p1 = _at(_noise(0.012, 0.55, 0.0005, 5001, 'highpass', 4500.0), 0.0, 0.49)
    p2 = _at(_sweep('triangle', 1800.0, 900.0, 0.03, 0.3, 0.001), 0.0, 0.49)
    p3 = _tticks('sine', 0.018, 0.001, [(0.07, 3600.0, 0.16), (0.11, 2600.0, 0.14), (0.16, 4100.0, 0.13), (0.2, 3000.0, 0.11), (0.27, 2300.0, 0.09), (0.33, 3400.0, 0.07), (0.42, 2800.0, 0.05)], 0.49)
    return _finalize(_mix(p1, p2, p3))
def micro_flower_bud_open_001():
    p1 = _at(_noise(0.8, 0.18, 0.35, 5101, 'bandpass', 2600.0), 0.0, 0.85)
    p2 = _at(_sweep('sine', 320.0, 520.0, 0.7, 0.16, 0.3), 0.0, 0.85)
    p3 = _at(_sweep('sine', 640.0, 1040.0, 0.6, 0.07, 0.3), 0.1, 0.85)
    p4 = _at(_tone('sine', 1900.0, 0.05, 0.1, 0.002), 0.55, 0.85)
    return _finalize(_mix(p1, p2, p3, p4))
def micro_dew_roll_drop_001():
    p1 = _at(_noise(0.16, 0.1, 0.06, 5201, 'bandpass', 900.0), 0.0, 0.36)
    p2 = _at(_noise(0.04, 0.12, 0.001, 5202, 'highpass', 3000.0), 0.16, 0.36)
    p3 = _at(_sweep('sine', 1700.0, 650.0, 0.09, 0.35, 0.001), 0.19, 0.36)
    p4 = _at(_noise(0.05, 0.2, 0.001, 5204, 'bandpass', 4500.0), 0.19, 0.36)
    p5 = _at(_sweep('sine', 900.0, 420.0, 0.07, 0.15, 0.001), 0.24, 0.36)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def micro_ant_colony_march_001():
    p1 = _at(_noise(1.2, 0.08, 0.3, 5301, 'bandpass', 5000.0), 0.0, 1.25)
    p2 = _nticks('highpass', 0.006, 0.0005, 5400, [(0.0, 5800.0, 0.239), (0.021, 4200.0, 0.19), (0.053, 5800.0, 0.255), (0.072, 4200.0, 0.186), (0.091, 5800.0, 0.195), (0.125, 4200.0, 0.186), (0.143, 4200.0, 0.296), (0.184, 3500.0, 0.241), (0.196, 5000.0, 0.239), (0.229, 5000.0, 0.228), (0.249, 5800.0, 0.283), (0.278, 4200.0, 0.282), (0.31, 6800.0, 0.223), (0.318, 6800.0, 0.286), (0.345, 3500.0, 0.175), (0.365, 5000.0, 0.192), (0.4, 4200.0, 0.182), (0.422, 6800.0, 0.173), (0.446, 4200.0, 0.258), (0.467, 6800.0, 0.233), (0.503, 4200.0, 0.256), (0.527, 5000.0, 0.24), (0.561, 5800.0, 0.176), (0.584, 5000.0, 0.186), (0.591, 3500.0, 0.171), (0.627, 5800.0, 0.245), (0.639, 3500.0, 0.204), (0.67, 5800.0, 0.191), (0.706, 5000.0, 0.236), (0.736, 5000.0, 0.272), (0.744, 3500.0, 0.231), (0.765, 5000.0, 0.195), (0.789, 6800.0, 0.258), (0.817, 4200.0, 0.191), (0.852, 6800.0, 0.187), (0.88, 6800.0, 0.162), (0.911, 5000.0, 0.291), (0.934, 5800.0, 0.163), (0.942, 5000.0, 0.279), (0.978, 3500.0, 0.296), (1.004, 5800.0, 0.205), (1.026, 6800.0, 0.264), (1.044, 6800.0, 0.165), (1.068, 5800.0, 0.281), (1.104, 6800.0, 0.285), (1.121, 4200.0, 0.157), (1.15, 4200.0, 0.242), (1.174, 6800.0, 0.221)], 1.25)
    return _finalize(_mix(p1, p2))
def micro_beetle_wing_unfold_001():
    p1 = _at(_noise(0.015, 0.5, 0.0005, 5401, 'highpass', 3500.0), 0.0, 0.62)
    p2 = _at(_sweep('triangle', 2200.0, 1500.0, 0.03, 0.2, 0.001), 0.0, 0.62)
    p3 = _at(_sweep('sawtooth', 160.0, 320.0, 0.45, 0.18, 0.06), 0.12, 0.62)
    p4 = _at(_noise(0.45, 0.12, 0.08, 5404, 'bandpass', 2500.0), 0.12, 0.62)
    return _finalize(_mix(p1, p2, p3, p4))
def micro_cocoon_crack_001():
    p1 = _at(_noise(0.03, 0.35, 0.0008, 5501, 'bandpass', 1500.0), 0.0, 0.45)
    p2 = _at(_sweep('sine', 140.0, 70.0, 0.12, 0.35, 0.002), 0.0, 0.45)
    p3 = _nticks('bandpass', 0.012, 0.0005, 5650, [(0.05, 3000.0, 0.15), (0.09, 3400.0, 0.14), (0.12, 2800.0, 0.15), (0.18, 3200.0, 0.12), (0.21, 3600.0, 0.12), (0.3, 3000.0, 0.1)], 0.45)
    p4 = _at(_noise(0.25, 0.08, 0.05, 5504, 'highpass', 2500.0), 0.15, 0.45)
    return _finalize(_mix(p1, p2, p3, p4))
def micro_spider_silk_pluck_001():
    p1 = _at(_sweep('sine', 1760.0, 1740.0, 0.9, 0.3, 0.001), 0.0, 0.95)
    p2 = _at(_tone('sine', 3520.0, 0.5, 0.1, 0.001), 0.0, 0.95)
    p3 = _at(_tone('sine', 5280.0, 0.3, 0.04, 0.001), 0.0, 0.95)
    p4 = _at(_noise(0.01, 0.15, 0.0005, 5604, 'highpass', 6000.0), 0.0, 0.95)
    return _finalize(_mix(p1, p2, p3, p4))
def micro_caterpillar_chew_001():
    p1 = _nticks('bandpass', 0.07, 0.002, 5750, [(0.0, 1800.0, 0.3), (0.22, 1800.0, 0.3), (0.44, 1800.0, 0.3), (0.62, 1800.0, 0.3), (0.86, 1800.0, 0.3)], 0.98)
    p2 = _nticks('highpass', 0.03, 0.001, 5800, [(0.03, 4000.0, 0.2), (0.25, 4000.0, 0.2), (0.47, 4000.0, 0.2), (0.65, 4000.0, 0.2), (0.89, 4000.0, 0.2)], 0.98)
    p3 = _tticks('sine', 0.05, 0.002, [(0.0, 230.0, 0.12), (0.22, 218.0, 0.12), (0.44, 206.0, 0.12), (0.62, 194.0, 0.12), (0.86, 182.0, 0.12)], 0.98)
    return _finalize(_mix(p1, p2, p3))
def micro_leafcutter_snip_001():
    p1 = _nticks('highpass', 0.018, 0.0005, 5850, [(0.0, 4800.0, 0.3), (0.16, 4800.0, 0.3), (0.3, 4800.0, 0.3), (0.5, 4800.0, 0.3), (0.64, 4800.0, 0.3), (0.8, 4800.0, 0.3)], 0.92)
    p2 = _nticks('bandpass', 0.06, 0.004, 5900, [(0.012, 1500.0, 0.1), (0.17200000000000001, 1500.0, 0.1), (0.312, 1500.0, 0.1), (0.512, 1500.0, 0.1), (0.652, 1500.0, 0.1), (0.812, 1500.0, 0.1)], 0.92)
    p3 = _tticks('triangle', 0.012, 0.0005, [(0.0, 3400.0, 0.1), (0.16, 3400.0, 0.1), (0.3, 3400.0, 0.1), (0.5, 3400.0, 0.1), (0.64, 3400.0, 0.1), (0.8, 3400.0, 0.1)], 0.92)
    return _finalize(_mix(p1, p2, p3))
def micro_firefly_pulse_001():
    p1 = _at(_tone('sine', 740.0, 0.5, 0.2, 0.18), 0.0, 1.2)
    p2 = _at(_tone('sine', 1110.0, 0.45, 0.07, 0.2), 0.02, 1.2)
    p3 = _at(_tone('sine', 988.0, 0.5, 0.2, 0.18), 0.65, 1.2)
    p4 = _at(_tone('sine', 1480.0, 0.45, 0.07, 0.2), 0.67, 1.2)
    return _finalize(_mix(p1, p2, p3, p4))
def micro_pollen_puff_001():
    p1 = _at(_noise(0.3, 0.3, 0.02, 6001, 'bandpass', 2200.0), 0.0, 0.41)
    p2 = _at(_sweep('sine', 95.0, 50.0, 0.12, 0.3, 0.003), 0.0, 0.41)
    p3 = _nticks('highpass', 0.01, 0.0005, 6150, [(0.1, 7000.0, 0.05), (0.15, 7500.0, 0.05), (0.2, 6800.0, 0.05), (0.24, 7200.0, 0.05), (0.3, 7000.0, 0.05), (0.35, 6500.0, 0.05)], 0.41)
    return _finalize(_mix(p1, p2, p3))
def micro_root_groan_001():
    p1 = _at(_sweep('sawtooth', 62.0, 78.0, 1.5, 0.25, 0.25), 0.0, 1.55)
    p2 = _at(_sweep('triangle', 93.0, 117.0, 1.4, 0.18, 0.3), 0.1, 1.55)
    p3 = _at(_noise(1.5, 0.4, 0.4, 6103, 'lowpass', 250.0), 0.0, 1.55)
    p4 = _nticks('bandpass', 0.02, 0.001, 6300, [(0.4, 900.0, 0.4), (0.9, 1100.0, 0.4), (1.2, 800.0, 0.4)], 1.55)
    return _finalize(_mix(p1, p2, p3, p4))
def micro_vine_whip_snap_001():
    p1 = _at(_noise(0.1, 0.25, 0.003, 6201, 'bandpass', 2800.0), 0.0, 0.22)
    p2 = _at(_sweep('sine', 3200.0, 350.0, 0.09, 0.25, 0.001), 0.0, 0.22)
    p3 = _at(_noise(0.015, 0.5, 0.0005, 6203, 'highpass', 3500.0), 0.09, 0.22)
    p4 = _at(_sweep('sine', 200.0, 100.0, 0.08, 0.2, 0.001), 0.09, 0.22)
    return _finalize(_mix(p1, p2, p3, p4))
def micro_mushroom_cap_pop_001():
    p1 = _at(_sweep('sine', 320.0, 110.0, 0.09, 0.4, 0.001), 0.0, 0.18)
    p2 = _at(_noise(0.03, 0.25, 0.001, 6302, 'lowpass', 1400.0), 0.0, 0.18)
    p3 = _at(_tone('sine', 520.0, 0.12, 0.07, 0.002), 0.01, 0.18)
    return _finalize(_mix(p1, p2, p3))
def micro_spore_cloud_release_001():
    p1 = _at(_sweep('sine', 110.0, 60.0, 0.1, 0.2, 0.003), 0.0, 1.1)
    p2 = _at(_noise(0.8, 0.2, 0.15, 6402, 'highpass', 6500.0), 0.0, 1.1)
    p3 = _nticks('bandpass', 0.02, 0.001, 6550, [(0.0, 4500.0, 0.218), (0.045, 3500.0, 0.262), (0.082, 3500.0, 0.257), (0.162, 3500.0, 0.263), (0.195, 8000.0, 0.158), (0.24, 6500.0, 0.237), (0.278, 5500.0, 0.208), (0.339, 4500.0, 0.224), (0.393, 4500.0, 0.216), (0.447, 6500.0, 0.218), (0.52, 3500.0, 0.211), (0.537, 3500.0, 0.183), (0.603, 6500.0, 0.181), (0.66, 6500.0, 0.24), (0.706, 3500.0, 0.219), (0.757, 3500.0, 0.158), (0.792, 8000.0, 0.165), (0.834, 4500.0, 0.255), (0.887, 3500.0, 0.23), (0.941, 8000.0, 0.268), (0.986, 5500.0, 0.19), (1.028, 6500.0, 0.256)], 1.1)
    return _finalize(_mix(p1, p2, p3))
def micro_snail_slime_glide_001():
    p1 = _at(_noise(0.5, 1.0, 0.15, 6501, 'bandpass', 450.0), 0.0, 1.45)
    p2 = _at(_noise(0.5, 0.9, 0.15, 6502, 'bandpass', 650.0), 0.45, 1.45)
    p3 = _at(_noise(0.5, 0.85, 0.15, 6503, 'bandpass', 850.0), 0.9, 1.45)
    p4 = _nticks('bandpass', 0.01, 0.0005, 6700, [(0.2, 2000.0, 0.25), (0.55, 2000.0, 0.25), (0.7, 2000.0, 0.25), (1.0, 2000.0, 0.25), (1.3, 2000.0, 0.25)], 1.45)
    p5 = _at(_tone('sine', 70.0, 1.4, 0.15, 0.4), 0.0, 1.45)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def micro_grasshopper_leap_001():
    p1 = _at(_noise(0.01, 0.4, 0.0005, 6601, 'highpass', 4000.0), 0.0, 0.31)
    p2 = _at(_sweep('sine', 180.0, 900.0, 0.07, 0.25, 0.002), 0.005, 0.31)
    p3 = _at(_noise(0.12, 0.15, 0.01, 6603, 'bandpass', 3500.0), 0.02, 0.31)
    p4 = _at(_sweep('sawtooth', 300.0, 420.0, 0.12, 0.07, 0.02), 0.06, 0.31)
    p5 = _at(_noise(0.03, 0.3, 0.001, 6605, 'lowpass', 400.0), 0.2, 0.31)
    p6 = _at(_sweep('sine', 110.0, 60.0, 0.06, 0.25, 0.001), 0.2, 0.31)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def micro_dragonfly_dart_001():
    p1 = _at(_sweep('triangle', 500.0, 1600.0, 0.12, 0.35, 0.01), 0.0, 0.42)
    p2 = _at(_sweep('triangle', 1600.0, 800.0, 0.25, 0.28, 0.01), 0.12, 0.42)
    p3 = _at(_noise(0.35, 0.25, 0.05, 6703, 'bandpass', 4000.0), 0.0, 0.42)
    return _finalize(_mix(p1, p2, p3))
def micro_acorn_bounce_001():
    p1 = _tticks('triangle', 0.05, 0.001, [(0.0, 520.0, 0.35), (0.16, 480.0, 0.28), (0.28, 440.0, 0.22), (0.37, 400.0, 0.16), (0.43, 380.0, 0.12), (0.47, 360.0, 0.08)], 0.57)
    p2 = _nticks('lowpass', 0.03, 0.001, 6900, [(0.0, 1500.0, 0.15), (0.16, 1500.0, 0.13), (0.28, 1500.0, 0.11), (0.37, 1500.0, 0.09), (0.43, 1500.0, 0.07), (0.47, 1500.0, 0.05)], 0.57)
    return _finalize(_mix(p1, p2))
def micro_thorn_scrape_001():
    p1 = _nticks('highpass', 0.025, 0.001, 6950, [(0.0, 2500.0, 0.3), (0.04, 2500.0, 0.28), (0.07, 2500.0, 0.3), (0.11, 2500.0, 0.25), (0.14, 2500.0, 0.24), (0.19, 2500.0, 0.22), (0.23, 2500.0, 0.2), (0.26, 2500.0, 0.18), (0.33, 2500.0, 0.15), (0.4, 2500.0, 0.12), (0.5, 2500.0, 0.1)], 0.58)
    p2 = _at(_noise(0.5, 0.1, 0.05, 6902, 'bandpass', 3000.0), 0.0, 0.58)
    return _finalize(_mix(p1, p2))
def micro_bark_beetle_gnaw_001():
    p1 = _nticks('bandpass', 0.025, 0.001, 7050, [(0.0, 1100.0, 0.7), (0.045, 1100.0, 0.5), (0.09, 1100.0, 0.7), (0.135, 1100.0, 0.5), (0.18, 1100.0, 0.7), (0.225, 1100.0, 0.5), (0.27, 1100.0, 0.7), (0.315, 1100.0, 0.5), (0.36, 1100.0, 0.7), (0.405, 1100.0, 0.5), (0.45, 1100.0, 0.7), (0.495, 1100.0, 0.5), (0.54, 1100.0, 0.7), (0.585, 1100.0, 0.5), (0.63, 1100.0, 0.7), (0.675, 1100.0, 0.5), (0.72, 1100.0, 0.7), (0.765, 1100.0, 0.5), (0.81, 1100.0, 0.7), (0.855, 1100.0, 0.5), (0.9, 1100.0, 0.7), (0.945, 1100.0, 0.5)], 1.02)
    p2 = _nticks('highpass', 0.008, 0.0005, 7100, [(0.0, 5000.0, 0.25), (0.09, 5000.0, 0.25), (0.18, 5000.0, 0.25), (0.27, 5000.0, 0.25), (0.36, 5000.0, 0.25), (0.45, 5000.0, 0.25), (0.54, 5000.0, 0.25), (0.63, 5000.0, 0.25), (0.72, 5000.0, 0.25), (0.81, 5000.0, 0.25), (0.9, 5000.0, 0.25)], 1.02)
    return _finalize(_mix(p1, p2))
def micro_nectar_sip_001():
    p1 = _at(_sweep('sine', 450.0, 1000.0, 0.12, 0.25, 0.005), 0.0, 0.42)
    p2 = _at(_sweep('sine', 1000.0, 520.0, 0.1, 0.2, 0.002), 0.14, 0.42)
    p3 = _at(_noise(0.2, 0.12, 0.01, 7103, 'bandpass', 3500.0), 0.02, 0.42)
    p4 = _nticks('bandpass', 0.01, 0.0005, 7300, [(0.3, 2500.0, 0.15), (0.36, 2500.0, 0.15)], 0.42)
    return _finalize(_mix(p1, p2, p3, p4))
def micro_seedling_sprout_001():
    p1 = _at(_noise(0.08, 0.3, 0.001, 7201, 'lowpass', 600.0), 0.0, 0.9)
    p2 = _nticks('lowpass', 0.02, 0.001, 7300, [(0.05, 500.0, 0.2), (0.1, 500.0, 0.2), (0.16, 500.0, 0.2)], 0.9)
    p3 = _at(_sweep('sine', 180.0, 540.0, 0.7, 0.3, 0.15), 0.12, 0.9)
    p4 = _at(_sweep('triangle', 360.0, 1080.0, 0.6, 0.1, 0.2), 0.15, 0.9)
    p5 = _at(_tone('sine', 1200.0, 0.05, 0.12, 0.002), 0.8, 0.9)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def micro_glow_fungus_hum_001():
    p1 = _at(_tone('sine', 110.0, 1.6, 0.16, 0.5), 0.0, 1.65)
    p2 = _at(_tone('sine', 113.5, 1.6, 0.16, 0.5), 0.0, 1.65)
    p3 = _at(_tone('sine', 220.0, 1.6, 0.05, 0.6), 0.0, 1.65)
    return _finalize(_mix(p1, p2, p3))
def micro_flytrap_snap_001():
    p1 = _at(_sweep('sine', 300.0, 420.0, 0.35, 0.1, 0.15), 0.0, 0.7)
    p2 = _at(_noise(0.3, 0.07, 0.1, 7402, 'bandpass', 1200.0), 0.0, 0.7)
    p3 = _at(_noise(0.02, 0.5, 0.0005, 7403, 'highpass', 2500.0), 0.45, 0.7)
    p4 = _at(_sweep('sine', 900.0, 200.0, 0.06, 0.3, 0.001), 0.45, 0.7)
    p5 = _at(_noise(0.15, 0.2, 0.01, 7405, 'bandpass', 600.0), 0.5, 0.7)
    p6 = _at(_sweep('sine', 120.0, 70.0, 0.12, 0.25, 0.002), 0.5, 0.7)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))

OFFICIAL_PRESETS_MICROLIFE = {
    'micro-seed-pod-burst-001': micro_seed_pod_burst_001,
    'micro-flower-bud-open-001': micro_flower_bud_open_001,
    'micro-dew-roll-drop-001': micro_dew_roll_drop_001,
    'micro-ant-colony-march-001': micro_ant_colony_march_001,
    'micro-beetle-wing-unfold-001': micro_beetle_wing_unfold_001,
    'micro-cocoon-crack-001': micro_cocoon_crack_001,
    'micro-spider-silk-pluck-001': micro_spider_silk_pluck_001,
    'micro-caterpillar-chew-001': micro_caterpillar_chew_001,
    'micro-leafcutter-snip-001': micro_leafcutter_snip_001,
    'micro-firefly-pulse-001': micro_firefly_pulse_001,
    'micro-pollen-puff-001': micro_pollen_puff_001,
    'micro-root-groan-001': micro_root_groan_001,
    'micro-vine-whip-snap-001': micro_vine_whip_snap_001,
    'micro-mushroom-cap-pop-001': micro_mushroom_cap_pop_001,
    'micro-spore-cloud-release-001': micro_spore_cloud_release_001,
    'micro-snail-slime-glide-001': micro_snail_slime_glide_001,
    'micro-grasshopper-leap-001': micro_grasshopper_leap_001,
    'micro-dragonfly-dart-001': micro_dragonfly_dart_001,
    'micro-acorn-bounce-001': micro_acorn_bounce_001,
    'micro-thorn-scrape-001': micro_thorn_scrape_001,
    'micro-bark-beetle-gnaw-001': micro_bark_beetle_gnaw_001,
    'micro-nectar-sip-001': micro_nectar_sip_001,
    'micro-seedling-sprout-001': micro_seedling_sprout_001,
    'micro-glow-fungus-hum-001': micro_glow_fungus_hum_001,
    'micro-flytrap-snap-001': micro_flytrap_snap_001,
}
