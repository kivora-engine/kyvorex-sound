"""Mission 19 - Dimensions & Impossible Phenomena (25 sounds)."""
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


def dim_endless_staircase_001():
    p1 = _at(_sweep('sine', 200.0, 400.0, 1.6, 0.52, 0.3), 0.0, 2.85)
    p2 = _at(_sweep('sine', 400.0, 800.0, 1.6, 0.52, 0.3), 0.4, 2.85)
    p3 = _at(_sweep('sine', 800.0, 1600.0, 1.6, 0.52, 0.3), 0.8, 2.85)
    p4 = _at(_sweep('sine', 1600.0, 3200.0, 1.6, 0.52, 0.3), 1.2, 2.85)
    return _finalize(_mix(p1, p2, p3, p4))
def dim_mirror_crossing_001():
    p1 = _at(_noise(0.5, 0.25, 0.4, 191001, 'bandpass', 2000.0), 0.0, 1.15)
    p2 = _at(_tone('sine', 2400.0, 0.6, 0.1, 0.001), 0.5, 1.15)
    p3 = _at(_tone('sine', 3100.0, 0.5, 0.08, 0.001), 0.52, 1.15)
    p4 = _at(_tone('sine', 3900.0, 0.5, 0.06, 0.001), 0.55, 1.15)
    p5 = _at(_noise(0.01, 0.4, 0.0005, 191005, 'highpass', 3500.0), 0.5, 1.15)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def dim_time_skip_stutter_001():
    p1 = _tticks('sine', 0.06, 0.001, [(0.0, 800.0, 0.573), (0.12, 720.0, 0.535), (0.216, 640.0, 0.497), (0.293, 560.0, 0.458), (0.354, 480.0, 0.42), (0.403, 400.0, 0.382)], 1.25)
    p2 = _at(_sweep('sine', 1200.0, 300.0, 0.3, 0.477, 0.01), 0.9, 1.25)
    return _finalize(_mix(p1, p2))
def dim_vacuum_implosion_001():
    p1 = _at(_noise(0.4, 0.612, 0.3, 193001, 'bandpass', 3000.0), 0.0, 1.3)
    p2 = _at(_sweep('sine', 3000.0, 100.0, 0.4, 0.245, 0.1), 0.0, 1.3)
    p3 = _at(_tone('sine', 40.0, 0.8, 0.184, 0.02), 0.45, 1.3)
    return _finalize(_mix(p1, p2, p3))
def dim_synesthesia_chord_001():
    p1 = _at(_tone('sine', 262.0, 1.2, 0.392, 0.1), 0.0, 1.85)
    p2 = _at(_tone('sine', 330.0, 1.2, 0.392, 0.1), 0.15, 1.85)
    p3 = _at(_tone('sine', 392.0, 1.2, 0.392, 0.1), 0.3, 1.85)
    p4 = _at(_tone('sine', 494.0, 1.2, 0.392, 0.1), 0.45, 1.85)
    p5 = _at(_tone('sine', 587.0, 1.2, 0.392, 0.1), 0.6, 1.85)
    p6 = _at(_noise(1.4, 0.104, 0.3, 194006, 'highpass', 6000.0), 0.0, 1.85)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def dim_reality_tear_rip_001():
    p1 = _at(_noise(0.6, 0.328, 0.05, 195001, 'highpass', 1500.0), 0.0, 0.75)
    p2 = _nticks('highpass', 0.01, 0.0005, 195120, [(0.006, 4101.0, 0.169), (0.083, 2393.0, 0.127), (0.153, 2148.0, 0.179), (0.172, 2281.0, 0.233), (0.196, 4257.0, 0.145), (0.208, 4581.0, 0.176), (0.219, 3827.0, 0.161), (0.274, 2087.0, 0.229), (0.277, 2537.0, 0.099), (0.293, 2367.0, 0.17), (0.313, 3019.0, 0.241), (0.336, 4995.0, 0.093), (0.356, 4407.0, 0.102), (0.365, 5855.0, 0.23), (0.402, 4868.0, 0.132), (0.409, 3883.0, 0.134), (0.474, 5586.0, 0.195), (0.476, 3600.0, 0.166), (0.496, 5393.0, 0.151), (0.504, 3955.0, 0.179), (0.532, 3754.0, 0.208), (0.548, 4353.0, 0.179), (0.558, 3931.0, 0.084), (0.582, 5781.0, 0.145)], 0.75)
    p3 = _at(_tone('sine', 60.0, 0.7, 0.164, 0.02), 0.0, 0.75)
    return _finalize(_mix(p1, p2, p3))
def dim_pre_echo_swell_001():
    p1 = _at(_tone('sine', 440.0, 0.3, 0.037, 0.002), 0.0, 1.75)
    p2 = _at(_tone('sine', 440.0, 0.3, 0.074, 0.002), 0.3, 1.75)
    p3 = _at(_tone('sine', 440.0, 0.3, 0.147, 0.002), 0.55, 1.75)
    p4 = _at(_tone('sine', 440.0, 0.3, 0.294, 0.002), 0.75, 1.75)
    p5 = _at(_tone('sine', 440.0, 0.8, 0.368, 0.002), 0.9, 1.75)
    p6 = _at(_noise(0.05, 0.221, 0.001, 196006, 'highpass', 3000.0), 0.9, 1.75)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def dim_infinite_corridor_001():
    p1 = _at(_tone('sine', 600.0, 0.12, 0.561, 0.001), 0.0, 2.62)
    p2 = _at(_tone('sine', 582.0, 0.12, 0.393, 0.001), 0.35, 2.62)
    p3 = _at(_tone('sine', 564.5, 0.12, 0.275, 0.001), 0.7, 2.62)
    p4 = _at(_tone('sine', 547.6, 0.12, 0.192, 0.001), 1.05, 2.62)
    p5 = _at(_tone('sine', 531.2, 0.12, 0.135, 0.001), 1.4, 2.62)
    p6 = _at(_tone('sine', 515.2, 0.12, 0.094, 0.001), 1.75, 2.62)
    p7 = _at(_tone('sine', 499.8, 0.12, 0.066, 0.001), 2.1, 2.62)
    p8 = _at(_tone('sine', 484.8, 0.12, 0.046, 0.001), 2.45, 2.62)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8))
def dim_clone_split_detune_001():
    p1 = _at(_sweep('sine', 440.0, 660.0, 1.2, 0.3, 0.1), 0.0, 1.25)
    p2 = _at(_sweep('sine', 440.0, 330.0, 1.2, 0.3, 0.1), 0.0, 1.25)
    p3 = _at(_noise(0.02, 0.6, 0.0005, 198003, 'highpass', 3000.0), 0.0, 1.25)
    p4 = _at(_noise(1.2, 0.06, 0.3, 198004, 'highpass', 6000.0), 0.0, 1.25)
    return _finalize(_mix(p1, p2, p3, p4))
def dim_time_bubble_slow_001():
    p1 = _tticks('sine', 0.05, 0.002, [(0.0, 1500.0, 0.496), (0.05, 1430.0, 0.476), (0.109, 1361.0, 0.458), (0.179, 1292.0, 0.438), (0.261, 1223.0, 0.42), (0.358, 1153.0, 0.4), (0.472, 1084.0, 0.382), (0.607, 1015.0, 0.362), (0.766, 946.0, 0.344), (0.954, 876.0, 0.324), (1.176, 807.0, 0.306), (1.438, 738.0, 0.286), (1.747, 669.0, 0.268), (2.111, 600.0, 0.248)], 2.21)
    p2 = _at(_sweep('sine', 200.0, 100.0, 1.4, 0.165, 0.1), 0.0, 2.21)
    p3 = _at(_noise(1.4, 0.099, 0.5, 199003, 'bandpass', 500.0), 0.0, 2.21)
    return _finalize(_mix(p1, p2, p3))
def dim_time_rush_accelerate_001():
    p1 = _tticks('sine', 0.03, 0.001, [(0.0, 500.0, 0.113), (0.35, 700.0, 0.133), (0.63, 900.0, 0.151), (0.854, 1100.0, 0.17), (1.033, 1300.0, 0.19), (1.177, 1500.0, 0.208), (1.291, 1700.0, 0.227), (1.383, 1900.0, 0.246), (1.456, 2100.0, 0.264), (1.515, 2300.0, 0.284), (1.562, 2500.0, 0.303), (1.6, 2700.0, 0.321), (1.63, 2900.0, 0.34), (1.654, 3100.0, 0.36), (1.673, 3300.0, 0.378), (1.688, 3500.0, 0.397)], 1.79)
    p2 = _at(_sweep('sine', 200.0, 1600.0, 1.2, 0.113, 0.3), 0.0, 1.79)
    p3 = _nticks('highpass', 0.005, 0.0005, 200180, [(1.738, 4000.0, 0.454)], 1.79)
    return _finalize(_mix(p1, p2, p3))
def dim_paradox_knot_001():
    p1 = _at(_tone('sine', 330.0, 0.5, 0.422, 0.005), 0.0, 1.15)
    p2 = _at(_tone('sine', 660.0, 0.5, 0.422, 0.005), 0.12, 1.15)
    p3 = _at(_tone('sine', 392.0, 0.5, 0.422, 0.005), 0.24, 1.15)
    p4 = _at(_tone('sine', 784.0, 0.5, 0.422, 0.005), 0.36, 1.15)
    p5 = _at(_tone('sine', 494.0, 0.5, 0.422, 0.005), 0.48, 1.15)
    p6 = _at(_tone('sine', 988.0, 0.5, 0.422, 0.005), 0.6, 1.15)
    p7 = _at(_tone('sine', 880.0, 0.5, 0.282, 0.005), 0.06, 1.15)
    p8 = _at(_tone('sine', 740.0, 0.5, 0.282, 0.005), 0.18, 1.15)
    p9 = _at(_tone('sine', 660.0, 0.5, 0.282, 0.005), 0.3, 1.15)
    p10 = _at(_tone('sine', 554.0, 0.5, 0.282, 0.005), 0.42, 1.15)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10))
def dim_unseen_footsteps_001():
    p1 = _tticks('sine', 0.1, 0.002, [(0.0, 90.0, 0.578), (0.55, 85.0, 0.496), (1.15, 92.0, 0.578), (1.7, 80.0, 0.413)], 2.05)
    p2 = _nticks('lowpass', 0.04, 0.001, 202120, [(0.0, 700.0, 0.198), (0.55, 700.0, 0.165), (1.15, 700.0, 0.198), (1.7, 700.0, 0.132)], 2.05)
    p3 = _at(_tone('sine', 500.0, 2.0, 0.033, 0.8), 0.0, 2.05)
    return _finalize(_mix(p1, p2, p3))
def dim_otherworld_wind_001():
    p1 = _at(_noise(2.0, 0.677, 0.7, 203001, 'bandpass', 800.0), 0.0, 2.45)
    p2 = _at(_noise(2.0, 0.406, 0.7, 203002, 'bandpass', 1800.0), 0.4, 2.45)
    p3 = _at(_tone('sine', 233.0, 2.0, 0.163, 0.8), 0.0, 2.45)
    p4 = _at(_tone('sine', 247.0, 2.0, 0.163, 0.8), 0.0, 2.45)
    return _finalize(_mix(p1, p2, p3, p4))
def dim_impossible_geometry_001():
    p1 = _at(_tone('sine', 220.0, 0.6, 0.352, 0.02), 0.0, 1.85)
    p2 = _at(_tone('sine', 293.7, 0.6, 0.352, 0.02), 0.4, 1.85)
    p3 = _at(_tone('sine', 352.0, 0.6, 0.352, 0.02), 0.8, 1.85)
    p4 = _at(_tone('sine', 440.0, 0.6, 0.352, 0.02), 1.2, 1.85)
    p5 = _at(_tone('sine', 330.0, 0.6, 0.234, 0.02), 0.0, 1.85)
    p6 = _at(_tone('sine', 440.54999999999995, 0.6, 0.234, 0.02), 0.4, 1.85)
    p7 = _at(_tone('sine', 528.0, 0.6, 0.234, 0.02), 0.8, 1.85)
    p8 = _at(_tone('sine', 660.0, 0.6, 0.234, 0.02), 1.2, 1.85)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8))
def dim_shadow_stretch_001():
    p1 = _at(_sweep('sawtooth', 55.0, 38.0, 1.8, 0.234, 0.3), 0.0, 1.85)
    p2 = _at(_tone('sine', 40.0, 1.8, 0.389, 0.4), 0.0, 1.85)
    p3 = _at(_noise(1.8, 0.389, 0.5, 205003, 'lowpass', 200.0), 0.0, 1.85)
    p4 = _at(_sweep('triangle', 200.0, 120.0, 1.5, 0.078, 0.2), 0.2, 1.85)
    return _finalize(_mix(p1, p2, p3, p4))
def dim_memory_fade_001():
    p1 = _at(_sweep('sine', 880.0, 440.0, 0.5, 0.551, 0.05), 0.0, 1.85)
    p2 = _at(_sweep('sine', 660.0, 330.0, 0.5, 0.331, 0.05), 0.4, 1.85)
    p3 = _at(_sweep('sine', 500.0, 250.0, 0.5, 0.198, 0.05), 0.8, 1.85)
    p4 = _at(_sweep('sine', 380.0, 190.0, 0.5, 0.11, 0.05), 1.2, 1.85)
    p5 = _at(_noise(1.8, 0.11, 0.5, 206005, 'bandpass', 1000.0), 0.0, 1.85)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def dim_superposition_flicker_001():
    p1 = _tticks('sine', 0.04, 0.001, [(0.0, 600.0, 0.5), (0.05, 900.0, 0.5), (0.1, 600.0, 0.5), (0.15, 900.0, 0.5), (0.2, 600.0, 0.5), (0.25, 900.0, 0.5), (0.3, 600.0, 0.5), (0.35, 900.0, 0.5), (0.4, 600.0, 0.5), (0.45, 900.0, 0.5), (0.5, 600.0, 0.5), (0.55, 900.0, 0.5), (0.6, 600.0, 0.5), (0.65, 900.0, 0.5), (0.7, 600.0, 0.5), (0.75, 900.0, 0.5), (0.8, 600.0, 0.5), (0.85, 900.0, 0.5), (0.9, 600.0, 0.5), (0.95, 900.0, 0.5)], 1.05)
    p2 = _at(_tone('sine', 750.0, 1.0, 0.133, 0.1), 0.0, 1.05)
    return _finalize(_mix(p1, p2))
def dim_anomaly_detector_001():
    p1 = _nticks('highpass', 0.004, 0.0005, 208060, [(0.122, 4823.0, 0.32), (0.259, 4684.0, 0.473), (0.295, 4124.0, 0.498), (0.441, 4099.0, 0.271), (0.465, 4919.0, 0.519), (0.52, 4387.0, 0.483), (0.533, 4030.0, 0.508), (0.559, 4913.0, 0.498), (0.599, 4934.0, 0.433), (0.655, 4942.0, 0.274), (0.66, 3182.0, 0.433), (0.71, 3558.0, 0.264), (0.745, 4235.0, 0.274), (0.786, 4849.0, 0.281), (0.82, 4401.0, 0.405), (0.827, 4094.0, 0.397), (0.971, 4080.0, 0.392), (1.013, 3106.0, 0.354), (1.019, 4073.0, 0.384), (1.051, 3484.0, 0.266), (1.092, 3771.0, 0.286), (1.154, 4349.0, 0.309), (1.155, 3473.0, 0.409), (1.159, 4009.0, 0.35), (1.242, 3557.0, 0.431), (1.372, 3337.0, 0.286), (1.431, 3688.0, 0.459), (1.528, 3260.0, 0.509), (1.562, 4725.0, 0.467), (1.592, 4645.0, 0.387)], 1.65)
    p2 = _at(_sweep('sine', 150.0, 300.0, 1.6, 0.052, 0.5), 0.0, 1.65)
    return _finalize(_mix(p1, p2))
def dim_wrong_door_knock_001():
    p1 = _tticks('triangle', 0.06, 0.001, [(0.0, 260.0, 0.582), (0.25, 260.0, 0.582), (0.5, 260.0, 0.582)], 1.55)
    p2 = _tticks('triangle', 0.08, 0.001, [(0.9, 200.0, 0.291), (1.15, 200.0, 0.218), (1.4, 200.0, 0.145)], 1.55)
    p3 = _at(_tone('sine', 110.0, 1.5, 0.073, 0.2), 0.0, 1.55)
    return _finalize(_mix(p1, p2, p3))
def dim_cosmic_whale_song_001():
    p1 = _at(_sweep('sine', 90.0, 180.0, 1.6, 0.456, 0.4), 0.0, 2.85)
    p2 = _at(_sweep('sine', 180.0, 360.0, 1.6, 0.183, 0.4), 0.0, 2.85)
    p3 = _at(_sweep('sine', 150.0, 60.0, 1.4, 0.365, 0.3), 1.4, 2.85)
    p4 = _at(_sweep('sine', 300.0, 120.0, 1.4, 0.146, 0.3), 1.4, 2.85)
    p5 = _at(_noise(2.8, 0.091, 0.8, 210005, 'lowpass', 200.0), 0.0, 2.85)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def dim_spiral_descent_001():
    p1 = _tticks('sine', 0.08, 0.002, [(0.0, 1800.0, 0.507), (0.1, 1690.0, 0.507), (0.2, 1580.0, 0.507), (0.3, 1470.0, 0.507), (0.4, 1360.0, 0.507), (0.5, 1250.0, 0.507), (0.6, 1140.0, 0.507), (0.7, 1030.0, 0.507), (0.8, 920.0, 0.507), (0.9, 810.0, 0.507), (1.0, 700.0, 0.507), (1.1, 590.0, 0.507), (1.2, 480.0, 0.507), (1.3, 370.0, 0.507)], 1.45)
    p2 = _at(_sweep('sine', 1800.0, 200.0, 1.4, 0.203, 0.05), 0.0, 1.45)
    return _finalize(_mix(p1, p2))
def dim_hourglass_reverse_001():
    p1 = _at(_noise(1.2, 0.355, 1.0, 212001, 'highpass', 4500.0), 0.0, 1.65)
    p2 = _nticks('highpass', 0.004, 0.0005, 212120, [(0.0, 5000.0, 0.059), (0.12, 5230.0, 0.077), (0.222, 5461.0, 0.096), (0.309, 5692.0, 0.114), (0.382, 5923.0, 0.132), (0.445, 6153.0, 0.15), (0.498, 6384.0, 0.168), (0.544, 6615.0, 0.187), (0.582, 6846.0, 0.205), (0.615, 7076.0, 0.222), (0.643, 7307.0, 0.241), (0.666, 7538.0, 0.259), (0.686, 7769.0, 0.278), (0.703, 8000.0, 0.296)], 1.65)
    p3 = _at(_tone('sine', 1568.0, 0.4, 0.237, 0.002), 1.2, 1.65)
    p4 = _at(_tone('sine', 4327.679999999999, 0.2, 0.071, 0.002), 1.2, 1.65)
    return _finalize(_mix(p1, p2, p3, p4))
def dim_static_between_worlds_001():
    p1 = _at(_noise(0.3, 0.478, 0.02, 213001, 'bandpass', 2500.0), 0.0, 1.2)
    p2 = _at(_noise(0.3, 0.478, 0.02, 213002, 'bandpass', 1500.0), 0.45, 1.2)
    p3 = _at(_tone('sine', 440.0, 0.15, 0.239, 0.01), 0.3, 1.2)
    p4 = _at(_tone('sine', 520.0, 0.15, 0.239, 0.01), 0.75, 1.2)
    p5 = _at(_noise(0.25, 0.399, 0.02, 213005, 'highpass', 4000.0), 0.9, 1.2)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def dim_unraveling_threads_001():
    p1 = _tticks('sine', 0.03, 0.001, [(0.0, 800.0, 0.27), (0.2, 1090.0, 0.295), (0.37, 1381.0, 0.318), (0.514, 1672.0, 0.343), (0.637, 1963.0, 0.369), (0.742, 2254.0, 0.392), (0.83, 2545.0, 0.417), (0.906, 2836.0, 0.441), (0.97, 3127.0, 0.466), (1.025, 3418.0, 0.491), (1.071, 3709.0, 0.514), (1.11, 4000.0, 0.539)], 1.56)
    p2 = _at(_noise(1.2, 0.18, 0.4, 214002, 'highpass', 5000.0), 0.0, 1.56)
    p3 = _at(_tone('sine', 100.0, 0.4, 0.36, 0.01), 1.11, 1.56)
    return _finalize(_mix(p1, p2, p3))

OFFICIAL_PRESETS_DIMENSIONS = {
    'dim-endless-staircase-001': dim_endless_staircase_001,
    'dim-mirror-crossing-001': dim_mirror_crossing_001,
    'dim-time-skip-stutter-001': dim_time_skip_stutter_001,
    'dim-vacuum-implosion-001': dim_vacuum_implosion_001,
    'dim-synesthesia-chord-001': dim_synesthesia_chord_001,
    'dim-reality-tear-rip-001': dim_reality_tear_rip_001,
    'dim-pre-echo-swell-001': dim_pre_echo_swell_001,
    'dim-infinite-corridor-001': dim_infinite_corridor_001,
    'dim-clone-split-detune-001': dim_clone_split_detune_001,
    'dim-time-bubble-slow-001': dim_time_bubble_slow_001,
    'dim-time-rush-accelerate-001': dim_time_rush_accelerate_001,
    'dim-paradox-knot-001': dim_paradox_knot_001,
    'dim-unseen-footsteps-001': dim_unseen_footsteps_001,
    'dim-otherworld-wind-001': dim_otherworld_wind_001,
    'dim-impossible-geometry-001': dim_impossible_geometry_001,
    'dim-shadow-stretch-001': dim_shadow_stretch_001,
    'dim-memory-fade-001': dim_memory_fade_001,
    'dim-superposition-flicker-001': dim_superposition_flicker_001,
    'dim-anomaly-detector-001': dim_anomaly_detector_001,
    'dim-wrong-door-knock-001': dim_wrong_door_knock_001,
    'dim-cosmic-whale-song-001': dim_cosmic_whale_song_001,
    'dim-spiral-descent-001': dim_spiral_descent_001,
    'dim-hourglass-reverse-001': dim_hourglass_reverse_001,
    'dim-static-between-worlds-001': dim_static_between_worlds_001,
    'dim-unraveling-threads-001': dim_unraveling_threads_001,
}
