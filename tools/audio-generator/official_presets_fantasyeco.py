"""Mission 17 - Fantasy Ecosystems (25 sounds)."""
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


def eco_fairy_wing_glimmer_001():
    p1 = _nticks('highpass', 0.015, 0.001, 170060, [(0.0, 6000.0, 0.037), (0.025, 6000.0, 0.064), (0.05, 6000.0, 0.09), (0.075, 6000.0, 0.118), (0.1, 6000.0, 0.142), (0.125, 6000.0, 0.167), (0.15, 6000.0, 0.189), (0.175, 6000.0, 0.212), (0.2, 6000.0, 0.232), (0.225, 6000.0, 0.25), (0.25, 6000.0, 0.267), (0.275, 6000.0, 0.28), (0.3, 6000.0, 0.293), (0.325, 6000.0, 0.302), (0.35, 6000.0, 0.307), (0.375, 6000.0, 0.311), (0.4, 6000.0, 0.313), (0.425, 6000.0, 0.311), (0.45, 6000.0, 0.307), (0.475, 6000.0, 0.302), (0.5, 6000.0, 0.293), (0.525, 6000.0, 0.28), (0.55, 6000.0, 0.267), (0.575, 6000.0, 0.25), (0.6, 6000.0, 0.232), (0.625, 6000.0, 0.212), (0.65, 6000.0, 0.189), (0.675, 6000.0, 0.167), (0.7, 6000.0, 0.142), (0.725, 6000.0, 0.118), (0.75, 6000.0, 0.09), (0.775, 6000.0, 0.064)], 0.91)
    p2 = _tticks('sine', 0.15, 0.001, [(0.246, 4732.0, 0.237), (0.383, 4076.0, 0.189), (0.402, 5622.0, 0.294), (0.437, 4832.0, 0.28), (0.448, 4958.0, 0.353), (0.536, 4040.0, 0.274), (0.64, 5045.0, 0.337), (0.708, 6231.0, 0.287)], 0.91)
    return _finalize(_mix(p1, p2))
def eco_spore_sprite_pop_001():
    p1 = _tticks('sine', 0.05, 0.001, [(0.0, 400.0, 0.524), (0.065, 590.0, 0.524), (0.13, 780.0, 0.524), (0.195, 970.0, 0.524), (0.26, 1160.0, 0.524), (0.325, 1350.0, 0.524), (0.39, 1540.0, 0.524)], 0.55)
    p2 = _nticks('bandpass', 0.01, 0.0005, 171120, [(0.0, 2500.0, 0.262), (0.065, 2500.0, 0.262), (0.13, 2500.0, 0.262), (0.195, 2500.0, 0.262), (0.26, 2500.0, 0.262), (0.325, 2500.0, 0.262), (0.39, 2500.0, 0.262)], 0.55)
    p3 = _at(_noise(0.5, 0.087, 0.1, 171003, 'highpass', 6000.0), 0.0, 0.55)
    return _finalize(_mix(p1, p2, p3))
def eco_luminous_moth_swarm_001():
    p1 = _tticks('sine', 0.3, 0.005, [(0.118, 2458.0, 0.181), (0.38, 2032.0, 0.256), (0.544, 1693.0, 0.297), (0.618, 2322.0, 0.246), (0.827, 1528.0, 0.171), (0.942, 2661.0, 0.331), (0.998, 1666.0, 0.307), (1.011, 1995.0, 0.276), (1.089, 3003.0, 0.334), (1.1, 2836.0, 0.28), (1.158, 1809.0, 0.225), (1.161, 2666.0, 0.3)], 1.51)
    p2 = _nticks('lowpass', 0.04, 0.003, 172120, [(0.017, 621.0, 0.259), (0.101, 610.0, 0.184), (0.162, 670.0, 0.242), (0.236, 605.0, 0.205), (0.268, 665.0, 0.177), (0.367, 665.0, 0.153), (0.494, 789.0, 0.215), (0.59, 760.0, 0.157), (0.606, 703.0, 0.194), (0.624, 667.0, 0.218), (0.706, 735.0, 0.147), (0.802, 679.0, 0.164), (0.865, 784.0, 0.143), (0.94, 708.0, 0.252), (0.97, 690.0, 0.239), (1.051, 637.0, 0.232), (1.098, 775.0, 0.153), (1.122, 705.0, 0.242), (1.14, 703.0, 0.266), (1.15, 632.0, 0.252)], 1.51)
    p3 = _at(_noise(1.2, 0.171, 0.4, 172003, 'highpass', 6000.0), 0.0, 1.51)
    return _finalize(_mix(p1, p2, p3))
def eco_crystal_tree_chime_001():
    p1 = _at(_tone('sine', 1319.0, 0.8, 0.464, 0.001), 0.0, 2.2)
    p2 = _at(_tone('sine', 1760.0, 0.8, 0.372, 0.001), 0.25, 2.2)
    p3 = _at(_tone('sine', 1175.0, 0.8, 0.372, 0.001), 0.5, 2.2)
    p4 = _at(_tone('sine', 1568.0, 0.8, 0.372, 0.001), 0.8, 2.2)
    p5 = _at(_tone('sine', 1047.0, 0.8, 0.334, 0.001), 1.1, 2.2)
    p6 = _at(_tone('sine', 1319.0, 0.8, 0.279, 0.001), 1.35, 2.2)
    p7 = _at(_tone('sine', 3640.4399999999996, 0.3, 0.093, 0.001), 0.0, 2.2)
    p8 = _at(_tone('sine', 3242.9999999999995, 0.3, 0.074, 0.001), 0.5, 2.2)
    p9 = _at(_tone('sine', 2889.72, 0.3, 0.067, 0.001), 1.1, 2.2)
    p10 = _at(_noise(1.8, 0.111, 0.5, 173010, 'bandpass', 2000.0), 0.0, 2.2)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10))
def eco_living_vine_wake_001():
    p1 = _at(_sweep('sawtooth', 60.0, 90.0, 1.0, 0.328, 0.2), 0.0, 1.05)
    p2 = _at(_noise(0.9, 0.657, 0.3, 174002, 'bandpass', 2500.0), 0.1, 1.05)
    p3 = _at(_sweep('triangle', 150.0, 230.0, 0.8, 0.263, 0.2), 0.1, 1.05)
    p4 = _nticks('bandpass', 0.03, 0.001, 174240, [(0.2, 800.0, 0.821), (0.55, 1000.0, 0.821), (0.85, 700.0, 0.821)], 1.05)
    return _finalize(_mix(p1, p2, p3, p4))
def eco_dragon_hatchling_chirp_001():
    p1 = _at(_sweep('triangle', 900.0, 1800.0, 0.08, 0.539, 0.003), 0.0, 0.67)
    p2 = _at(_sweep('triangle', 1700.0, 900.0, 0.1, 0.539, 0.003), 0.1, 0.67)
    p3 = _at(_sweep('triangle', 1000.0, 2000.0, 0.08, 0.539, 0.003), 0.4, 0.67)
    p4 = _at(_sweep('triangle', 2000.0, 1100.0, 0.12, 0.539, 0.003), 0.5, 0.67)
    p5 = _at(_noise(0.04, 0.18, 0.002, 175005, 'bandpass', 3000.0), 0.0, 0.67)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def eco_unicorn_hoof_sparkle_001():
    p1 = _tticks('triangle', 0.05, 0.001, [(0.0, 380.0, 0.525), (0.22, 340.0, 0.525), (0.44, 380.0, 0.525), (0.66, 340.0, 0.525)], 1.03)
    p2 = _nticks('lowpass', 0.04, 0.001, 176120, [(0.0, 900.0, 0.262), (0.22, 900.0, 0.262), (0.44, 900.0, 0.262), (0.66, 900.0, 0.262)], 1.03)
    p3 = _tticks('sine', 0.3, 0.001, [(0.02, 3500.0, 0.131), (0.24, 4200.0, 0.131), (0.46, 3800.0, 0.131), (0.68, 4600.0, 0.131)], 1.03)
    return _finalize(_mix(p1, p2, p3))
def eco_treant_groan_step_001():
    p1 = _at(_sweep('sawtooth', 50.0, 70.0, 1.0, 0.15, 0.2), 0.0, 1.4)
    p2 = _at(_sweep('triangle', 110.0, 85.0, 0.9, 0.12, 0.2), 0.1, 1.4)
    p3 = _at(_sweep('sine', 60.0, 35.0, 0.3, 0.5, 0.002), 0.6, 1.4)
    p4 = _at(_noise(0.3, 0.4, 0.002, 177004, 'lowpass', 250.0), 0.6, 1.4)
    p5 = _at(_noise(0.7, 0.15, 0.1, 177005, 'bandpass', 2500.0), 0.65, 1.4)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def eco_pixie_dust_trail_001():
    p1 = _tticks('sine', 0.1, 0.001, [(0.0, 7000.0, 0.474), (0.07, 6650.0, 0.474), (0.14, 6300.0, 0.474), (0.21, 5950.0, 0.474), (0.28, 5600.0, 0.474), (0.35, 5250.0, 0.474), (0.42, 4900.0, 0.474), (0.49, 4550.0, 0.474), (0.56, 4200.0, 0.474), (0.63, 3850.0, 0.474), (0.7, 3500.0, 0.474), (0.77, 3150.0, 0.474), (0.84, 2800.0, 0.474), (0.91, 2450.0, 0.474)], 1.06)
    p2 = _at(_noise(1.0, 0.158, 0.2, 178002, 'highpass', 7500.0), 0.0, 1.06)
    return _finalize(_mix(p1, p2))
def eco_moon_bloom_chime_001():
    p1 = _at(_tone('sine', 523.0, 0.8, 0.489, 0.002), 0.0, 1.39)
    p2 = _at(_tone('sine', 659.0, 0.8, 0.489, 0.002), 0.18, 1.39)
    p3 = _at(_tone('sine', 784.0, 0.8, 0.489, 0.002), 0.36, 1.39)
    p4 = _at(_tone('sine', 1047.0, 0.8, 0.489, 0.002), 0.54, 1.39)
    p5 = _at(_noise(0.6, 0.196, 0.3, 179005, 'bandpass', 2500.0), 0.0, 1.39)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def eco_enchanted_stream_babble_001():
    p1 = _at(_noise(1.4, 0.516, 0.3, 180001, 'bandpass', 1200.0), 0.0, 1.45)
    p2 = _at(_noise(1.4, 0.412, 0.3, 180002, 'bandpass', 2400.0), 0.0, 1.45)
    p3 = _tticks('sine', 0.05, 0.002, [(0.102, 1079.0, 0.303), (0.156, 1168.0, 0.237), (0.301, 525.0, 0.28), (0.342, 857.0, 0.276), (0.396, 487.0, 0.313), (0.424, 844.0, 0.283), (0.447, 571.0, 0.225), (0.507, 614.0, 0.28), (0.53, 481.0, 0.219), (0.538, 1163.0, 0.2), (0.54, 947.0, 0.322), (0.553, 977.0, 0.204), (0.608, 904.0, 0.27), (0.627, 621.0, 0.338), (0.647, 632.0, 0.229), (0.839, 608.0, 0.177), (1.014, 729.0, 0.351), (1.018, 1021.0, 0.25), (1.036, 412.0, 0.186), (1.036, 418.0, 0.19), (1.061, 948.0, 0.285), (1.102, 1148.0, 0.237), (1.142, 1023.0, 0.291), (1.24, 923.0, 0.293)], 1.45)
    p4 = _tticks('sine', 0.5, 0.002, [(0.3, 2093.0, 0.165), (0.9, 2637.0, 0.165)], 1.45)
    return _finalize(_mix(p1, p2, p3, p4))
def eco_griffin_screech_001():
    p1 = _at(_sweep('sawtooth', 1800.0, 900.0, 0.5, 0.28, 0.02), 0.0, 0.56)
    p2 = _at(_sweep('sawtooth', 1900.0, 1000.0, 0.5, 0.21, 0.02), 0.01, 0.56)
    p3 = _at(_noise(0.5, 0.42, 0.02, 181003, 'bandpass', 2500.0), 0.0, 0.56)
    p4 = _at(_sweep('sine', 3500.0, 1800.0, 0.4, 0.112, 0.02), 0.0, 0.56)
    return _finalize(_mix(p1, p2, p3, p4))
def eco_forest_spirit_whisper_001():
    p1 = _at(_noise(0.5, 0.684, 0.2, 182001, 'bandpass', 900.0), 0.0, 1.35)
    p2 = _at(_noise(0.5, 0.684, 0.2, 182002, 'bandpass', 1500.0), 0.4, 1.35)
    p3 = _at(_noise(0.5, 0.684, 0.2, 182003, 'bandpass', 700.0), 0.8, 1.35)
    p4 = _at(_noise(1.3, 0.205, 0.5, 182004, 'highpass', 5000.0), 0.0, 1.35)
    p5 = _at(_tone('sine', 220.0, 1.3, 0.137, 0.5), 0.0, 1.35)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def eco_wisp_lantern_flicker_001():
    p1 = _tticks('sine', 0.15, 0.02, [(0.0, 660.0, 0.443), (0.12, 740.0, 0.333), (0.3, 620.0, 0.443), (0.4, 700.0, 0.333), (0.65, 660.0, 0.399), (0.8, 780.0, 0.266), (1.0, 640.0, 0.333)], 1.2)
    p2 = _tticks('sine', 0.15, 0.02, [(0.0, 1320.0, 0.177), (0.3, 1240.0, 0.177), (0.65, 1320.0, 0.155), (1.0, 1280.0, 0.133)], 1.2)
    p3 = _at(_noise(1.0, 0.067, 0.3, 183003, 'highpass', 7000.0), 0.0, 1.2)
    return _finalize(_mix(p1, p2, p3))
def eco_giant_beanstalk_grow_001():
    p1 = _at(_sweep('sawtooth', 50.0, 200.0, 1.4, 0.165, 0.3), 0.0, 1.85)
    p2 = _at(_sweep('triangle', 100.0, 400.0, 1.2, 0.132, 0.3), 0.0, 1.85)
    p3 = _nticks('bandpass', 0.03, 0.001, 184180, [(0.0, 600.0, 0.33), (0.25, 714.0, 0.353), (0.463, 828.0, 0.378), (0.643, 942.0, 0.401), (0.797, 1057.0, 0.424), (0.927, 1171.0, 0.447), (1.038, 1285.0, 0.472), (1.132, 1400.0, 0.495)], 1.85)
    p4 = _at(_noise(1.4, 0.33, 0.3, 184004, 'bandpass', 2500.0), 0.2, 1.85)
    p5 = _at(_noise(0.4, 0.412, 0.02, 184005, 'highpass', 3000.0), 1.4, 1.85)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def eco_floating_island_drift_001():
    p1 = _at(_tone('sine', 70.0, 2.0, 0.322, 0.7), 0.0, 2.35)
    p2 = _at(_tone('sine', 105.0, 2.0, 0.161, 0.7), 0.0, 2.35)
    p3 = _at(_noise(2.0, 0.322, 0.8, 185003, 'bandpass', 500.0), 0.0, 2.35)
    p4 = _at(_noise(2.0, 0.161, 0.9, 185004, 'bandpass', 1500.0), 0.3, 2.35)
    p5 = _at(_sweep('sine', 300.0, 420.0, 1.5, 0.048, 0.6), 0.2, 2.35)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def eco_fire_salamander_crackle_001():
    p1 = _nticks('highpass', 0.01, 0.0005, 186060, [(0.028, 4594.0, 0.518), (0.147, 5710.0, 0.366), (0.259, 5804.0, 0.469), (0.347, 3562.0, 0.442), (0.379, 3591.0, 0.307), (0.428, 4770.0, 0.449), (0.467, 6278.0, 0.28), (0.524, 5890.0, 0.369), (0.555, 4920.0, 0.338), (0.818, 5104.0, 0.333), (0.824, 3626.0, 0.42), (0.834, 6307.0, 0.527), (0.882, 6418.0, 0.382), (0.921, 4274.0, 0.313), (0.96, 3116.0, 0.349), (1.034, 5394.0, 0.346), (1.054, 4573.0, 0.531), (1.108, 5968.0, 0.502), (1.11, 5764.0, 0.451), (1.136, 7806.0, 0.413), (1.15, 4326.0, 0.446), (1.175, 6772.0, 0.36)], 1.24)
    p2 = _at(_noise(1.0, 0.364, 0.1, 186002, 'bandpass', 900.0), 0.0, 1.24)
    p3 = _at(_noise(0.8, 0.218, 0.1, 186003, 'highpass', 5000.0), 0.1, 1.24)
    p4 = _at(_sweep('triangle', 220.0, 260.0, 0.4, 0.109, 0.05), 0.1, 1.24)
    return _finalize(_mix(p1, p2, p3, p4))
def eco_mermaid_pearl_song_001():
    p1 = _at(_tone('sine', 659.0, 0.6, 0.458, 0.01), 0.0, 1.95)
    p2 = _at(_tone('sine', 784.0, 0.6, 0.458, 0.01), 0.3, 1.95)
    p3 = _at(_tone('sine', 880.0, 0.6, 0.458, 0.01), 0.6, 1.95)
    p4 = _at(_tone('sine', 784.0, 0.6, 0.458, 0.01), 1.0, 1.95)
    p5 = _at(_tone('sine', 988.0, 0.6, 0.458, 0.01), 1.3, 1.95)
    p6 = _at(_tone('sine', 1318.0, 0.4, 0.114, 0.01), 0.0, 1.95)
    p7 = _at(_tone('sine', 1568.0, 0.4, 0.114, 0.01), 0.3, 1.95)
    p8 = _at(_tone('sine', 1760.0, 0.4, 0.114, 0.01), 0.6, 1.95)
    p9 = _at(_tone('sine', 1568.0, 0.4, 0.114, 0.01), 1.0, 1.95)
    p10 = _at(_tone('sine', 1976.0, 0.4, 0.114, 0.01), 1.3, 1.95)
    p11 = _at(_noise(1.8, 0.092, 0.4, 187011, 'highpass', 6000.0), 0.0, 1.95)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11))
def eco_root_door_creak_open_001():
    p1 = _tticks('triangle', 0.06, 0.001, [(0.0, 300.0, 0.618), (0.2, 300.0, 0.618)], 1.55)
    p2 = _at(_sweep('sawtooth', 90.0, 140.0, 1.0, 0.154, 0.1), 0.5, 1.55)
    p3 = _at(_sweep('triangle', 180.0, 300.0, 0.9, 0.124, 0.1), 0.5, 1.55)
    p4 = _nticks('bandpass', 0.02, 0.001, 188240, [(0.7, 900.0, 0.309), (1.0, 1100.0, 0.309), (1.3, 800.0, 0.309)], 1.55)
    return _finalize(_mix(p1, p2, p3, p4))
def eco_phoenix_egg_warm_pulse_001():
    p1 = _at(_tone('sine', 110.0, 0.6, 0.42, 0.1), 0.0, 2.05)
    p2 = _at(_tone('sine', 110.0, 0.6, 0.42, 0.1), 0.7, 2.05)
    p3 = _at(_tone('sine', 110.0, 0.6, 0.42, 0.1), 1.4, 2.05)
    p4 = _at(_tone('sine', 165.0, 0.5, 0.202, 0.1), 0.0, 2.05)
    p5 = _at(_tone('sine', 165.0, 0.5, 0.202, 0.1), 0.7, 2.05)
    p6 = _at(_tone('sine', 165.0, 0.5, 0.202, 0.1), 1.4, 2.05)
    p7 = _nticks('highpass', 0.01, 0.0005, 189420, [(0.021, 7904.0, 0.197), (0.718, 4930.0, 0.182), (0.847, 5374.0, 0.108), (1.184, 5436.0, 0.16), (1.222, 6195.0, 0.14), (1.552, 7154.0, 0.153), (1.631, 4751.0, 0.158), (1.669, 4615.0, 0.19), (1.746, 7801.0, 0.18), (1.761, 7340.0, 0.167)], 2.05)
    p8 = _at(_noise(1.8, 0.168, 0.5, 189008, 'lowpass', 500.0), 0.0, 2.05)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8))
def eco_fairy_ring_activate_001():
    p1 = _at(_tone('sine', 523.0, 0.5, 0.247, 0.005), 0.0, 1.15)
    p2 = _at(_tone('sine', 659.0, 0.5, 0.247, 0.005), 0.08, 1.15)
    p3 = _at(_tone('sine', 784.0, 0.5, 0.247, 0.005), 0.16, 1.15)
    p4 = _at(_tone('sine', 1047.0, 0.5, 0.247, 0.005), 0.24, 1.15)
    p5 = _at(_tone('sine', 1319.0, 0.5, 0.247, 0.005), 0.32, 1.15)
    p6 = _at(_tone('sine', 1568.0, 0.5, 0.247, 0.005), 0.4, 1.15)
    p7 = _at(_noise(0.8, 0.247, 0.3, 190007, 'highpass', 4000.0), 0.1, 1.15)
    p8 = _tticks('sine', 0.1, 0.001, [(0.542, 4073.0, 0.101), (0.569, 7394.0, 0.13), (0.686, 6290.0, 0.162), (0.82, 5522.0, 0.162), (0.866, 6066.0, 0.135), (0.87, 4632.0, 0.124), (0.898, 4342.0, 0.143), (0.999, 5334.0, 0.104)], 1.15)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8))
def eco_glow_worm_cavern_001():
    p1 = _at(_sweep('sine', 1800.0, 1260.0, 0.15, 0.552, 0.001), 0.0, 2.2)
    p2 = _at(_sweep('sine', 1500.0, 1050.0, 0.15, 0.552, 0.001), 0.7, 2.2)
    p3 = _at(_sweep('sine', 1650.0, 1155.0, 0.15, 0.552, 0.001), 1.3, 2.2)
    p4 = _tticks('sine', 0.4, 0.002, [(0.075, 2971.0, 0.16), (0.292, 2523.0, 0.147), (0.527, 3700.0, 0.131), (0.643, 4530.0, 0.175), (0.974, 4947.0, 0.184), (1.067, 2927.0, 0.14), (1.417, 2949.0, 0.142), (1.751, 2909.0, 0.173)], 2.2)
    p5 = _at(_noise(1.8, 0.11, 0.5, 191005, 'lowpass', 400.0), 0.0, 2.2)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def eco_wyvern_wing_flap_001():
    p1 = _at(_noise(0.3, 0.667, 0.05, 192001, 'lowpass', 500.0), 0.0, 1.28)
    p2 = _at(_noise(0.3, 0.667, 0.05, 192002, 'lowpass', 500.0), 0.45, 1.28)
    p3 = _at(_noise(0.3, 0.667, 0.05, 192003, 'lowpass', 500.0), 0.9, 1.28)
    p4 = _at(_noise(0.3, 0.37, 0.05, 192004, 'bandpass', 1500.0), 0.03, 1.28)
    p5 = _at(_noise(0.3, 0.37, 0.05, 192005, 'bandpass', 1500.0), 0.48, 1.28)
    p6 = _at(_noise(0.3, 0.37, 0.05, 192006, 'bandpass', 1500.0), 0.93, 1.28)
    p7 = _at(_sweep('sine', 70.0, 45.0, 0.2, 0.445, 0.01), 0.0, 1.28)
    p8 = _at(_sweep('sine', 70.0, 45.0, 0.2, 0.445, 0.01), 0.45, 1.28)
    p9 = _at(_sweep('sine', 70.0, 45.0, 0.2, 0.445, 0.01), 0.9, 1.28)
    p10 = _at(_noise(0.02, 0.445, 0.0005, 192010, 'highpass', 3000.0), 0.0, 1.28)
    p11 = _at(_noise(0.02, 0.445, 0.0005, 192011, 'highpass', 3000.0), 0.45, 1.28)
    p12 = _at(_noise(0.02, 0.445, 0.0005, 192012, 'highpass', 3000.0), 0.9, 1.28)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12))
def eco_enchanted_wind_whistle_001():
    p1 = _at(_noise(2.0, 1.0, 0.7, 193001, 'bandpass', 1100.0), 0.0, 2.05)
    p2 = _at(_tone('sine', 880.0, 0.6, 0.303, 0.2), 0.3, 2.05)
    p3 = _at(_tone('sine', 1047.0, 0.6, 0.303, 0.2), 0.8, 2.05)
    p4 = _at(_tone('sine', 784.0, 0.6, 0.303, 0.2), 1.3, 2.05)
    return _finalize(_mix(p1, p2, p3, p4))
def eco_forest_awakening_dawn_001():
    p1 = _at(_tone('sine', 196.0, 2.4, 0.147, 1.0), 0.0, 2.45)
    p2 = _at(_tone('sine', 247.0, 2.4, 0.147, 1.0), 0.0, 2.45)
    p3 = _at(_tone('sine', 294.0, 2.4, 0.147, 1.0), 0.0, 2.45)
    p4 = _at(_tone('sine', 392.0, 2.4, 0.147, 1.0), 0.0, 2.45)
    p5 = _at(_sweep('sine', 2400.0, 3200.0, 0.06, 0.22, 0.003), 0.9, 2.45)
    p6 = _at(_sweep('sine', 2800.0, 3600.0, 0.06, 0.22, 0.003), 1.15, 2.45)
    p7 = _at(_sweep('sine', 2200.0, 3000.0, 0.07, 0.22, 0.003), 1.6, 2.45)
    p8 = _at(_sweep('sine', 3000.0, 3800.0, 0.06, 0.22, 0.003), 1.8, 2.45)
    p9 = _at(_noise(2.4, 0.073, 0.8, 194009, 'bandpass', 3000.0), 0.0, 2.45)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8, p9))

OFFICIAL_PRESETS_FANTASYECO = {
    'eco-fairy-wing-glimmer-001': eco_fairy_wing_glimmer_001,
    'eco-spore-sprite-pop-001': eco_spore_sprite_pop_001,
    'eco-luminous-moth-swarm-001': eco_luminous_moth_swarm_001,
    'eco-crystal-tree-chime-001': eco_crystal_tree_chime_001,
    'eco-living-vine-wake-001': eco_living_vine_wake_001,
    'eco-dragon-hatchling-chirp-001': eco_dragon_hatchling_chirp_001,
    'eco-unicorn-hoof-sparkle-001': eco_unicorn_hoof_sparkle_001,
    'eco-treant-groan-step-001': eco_treant_groan_step_001,
    'eco-pixie-dust-trail-001': eco_pixie_dust_trail_001,
    'eco-moon-bloom-chime-001': eco_moon_bloom_chime_001,
    'eco-enchanted-stream-babble-001': eco_enchanted_stream_babble_001,
    'eco-griffin-screech-001': eco_griffin_screech_001,
    'eco-forest-spirit-whisper-001': eco_forest_spirit_whisper_001,
    'eco-wisp-lantern-flicker-001': eco_wisp_lantern_flicker_001,
    'eco-giant-beanstalk-grow-001': eco_giant_beanstalk_grow_001,
    'eco-floating-island-drift-001': eco_floating_island_drift_001,
    'eco-fire-salamander-crackle-001': eco_fire_salamander_crackle_001,
    'eco-mermaid-pearl-song-001': eco_mermaid_pearl_song_001,
    'eco-root-door-creak-open-001': eco_root_door_creak_open_001,
    'eco-phoenix-egg-warm-pulse-001': eco_phoenix_egg_warm_pulse_001,
    'eco-fairy-ring-activate-001': eco_fairy_ring_activate_001,
    'eco-glow-worm-cavern-001': eco_glow_worm_cavern_001,
    'eco-wyvern-wing-flap-001': eco_wyvern_wing_flap_001,
    'eco-enchanted-wind-whistle-001': eco_enchanted_wind_whistle_001,
    'eco-forest-awakening-dawn-001': eco_forest_awakening_dawn_001,
}
