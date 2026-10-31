"""Mission 12 - Glaciers & Geological Phenomena (25 sounds)."""
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


def geo_glacier_moulin_gurgle_001():
    p1 = _at(_noise(1.5, 0.519, 0.3, 120001, 'bandpass', 500.0), 0.0, 1.55)
    p2 = _at(_noise(1.4, 0.371, 0.3, 120002, 'bandpass', 900.0), 0.1, 1.55)
    p3 = _at(_tone('sine', 80.0, 1.5, 0.296, 0.4), 0.0, 1.55)
    p4 = _at(_sweep('sine', 350.0, 700.0, 0.08, 0.371, 0.003), 0.15, 1.55)
    p5 = _at(_sweep('sine', 390.0, 760.0, 0.08, 0.371, 0.003), 0.45, 1.55)
    p6 = _at(_sweep('sine', 430.0, 820.0, 0.08, 0.371, 0.003), 0.7, 1.55)
    p7 = _at(_sweep('sine', 470.0, 880.0, 0.08, 0.371, 0.003), 0.98, 1.55)
    p8 = _at(_sweep('sine', 510.0, 940.0, 0.08, 0.371, 0.003), 1.2, 1.55)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8))
def geo_iceberg_roll_001():
    p1 = _at(_sweep('sine', 55.0, 40.0, 1.8, 0.526, 0.3), 0.0, 2.15)
    p2 = _at(_noise(2.0, 0.526, 0.5, 121002, 'lowpass', 200.0), 0.0, 2.15)
    p3 = _at(_noise(1.8, 0.329, 0.6, 121003, 'bandpass', 700.0), 0.3, 2.15)
    p4 = _at(_sweep('triangle', 420.0, 300.0, 0.35, 0.158, 0.05), 0.5, 2.15)
    p5 = _at(_sweep('triangle', 560.0, 380.0, 0.3, 0.132, 0.05), 1.1, 2.15)
    p6 = _at(_sweep('sine', 70.0, 35.0, 0.3, 0.46, 0.003), 1.7, 2.15)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def geo_icicle_snap_001():
    p1 = _at(_noise(0.008, 0.431, 0.0005, 122001, 'highpass', 5000.0), 0.0, 0.58)
    p2 = _at(_sweep('triangle', 3000.0, 2000.0, 0.02, 0.215, 0.0005), 0.0, 0.58)
    p3 = _tticks('sine', 0.12, 0.0005, [(0.12, 4200.0, 0.172), (0.17, 5200.0, 0.155), (0.21, 3600.0, 0.138), (0.27, 4800.0, 0.121), (0.34, 6000.0, 0.086), (0.41, 3900.0, 0.069)], 0.58)
    return _finalize(_mix(p1, p2, p3))
def geo_ice_cave_whistle_001():
    p1 = _at(_noise(2.0, 0.509, 0.6, 123001, 'bandpass', 1200.0), 0.0, 2.05)
    p2 = _at(_sweep('sine', 620.0, 780.0, 1.8, 0.245, 0.5), 0.0, 2.05)
    p3 = _at(_sweep('sine', 930.0, 1170.0, 1.8, 0.122, 0.6), 0.1, 2.05)
    p4 = _at(_tone('sine', 311.0, 2.0, 0.163, 0.7), 0.0, 2.05)
    return _finalize(_mix(p1, p2, p3, p4))
def geo_snow_slab_whump_001():
    p1 = _at(_sweep('sine', 90.0, 35.0, 0.35, 0.5, 0.002), 0.0, 0.86)
    p2 = _at(_noise(0.25, 0.4, 0.003, 124002, 'lowpass', 250.0), 0.0, 0.86)
    p3 = _at(_noise(0.7, 0.2, 0.05, 124003, 'bandpass', 3500.0), 0.08, 0.86)
    p4 = _nticks('highpass', 0.01, 0.0005, 124240, [(0.272, 7191.0, 0.071), (0.283, 7253.0, 0.063), (0.356, 5719.0, 0.065), (0.552, 5332.0, 0.073), (0.558, 6348.0, 0.073), (0.583, 7055.0, 0.067), (0.59, 5630.0, 0.05), (0.621, 7939.0, 0.077), (0.748, 7415.0, 0.08), (0.802, 6540.0, 0.043)], 0.86)
    return _finalize(_mix(p1, p2, p3, p4))
def geo_frost_crystal_glint_001():
    p1 = _tticks('sine', 0.09, 0.0005, [(0.027, 6875.0, 0.361), (0.128, 5709.0, 0.452), (0.321, 4663.0, 0.309), (0.374, 7668.0, 0.328), (0.4, 5830.0, 0.197), (0.439, 4510.0, 0.226), (0.464, 3719.0, 0.392), (0.503, 7490.0, 0.219), (0.548, 6300.0, 0.323), (0.557, 5669.0, 0.254), (0.613, 7486.0, 0.369), (0.635, 5555.0, 0.323), (0.644, 7682.0, 0.471), (0.774, 5955.0, 0.35), (0.782, 6513.0, 0.278), (0.964, 7099.0, 0.333)], 1.15)
    p2 = _at(_noise(1.1, 0.119, 0.3, 125002, 'highpass', 7000.0), 0.0, 1.15)
    return _finalize(_mix(p1, p2))
def geo_frost_heave_creak_001():
    p1 = _at(_sweep('sawtooth', 55.0, 75.0, 1.2, 0.15, 0.2), 0.0, 1.25)
    p2 = _at(_noise(1.2, 0.251, 0.3, 126002, 'lowpass', 200.0), 0.0, 1.25)
    p3 = _nticks('bandpass', 0.03, 0.001, 126180, [(0.0, 700.0, 0.376), (0.25, 900.0, 0.313), (0.62, 650.0, 0.376), (0.85, 800.0, 0.313), (1.1, 1000.0, 0.313)], 1.25)
    p4 = _nticks('highpass', 0.008, 0.0005, 126240, [(0.25, 2500.0, 0.564), (0.62, 2500.0, 0.564)], 1.25)
    return _finalize(_mix(p1, p2, p3, p4))
def geo_scree_pebble_trickle_001():
    p1 = _tticks('triangle', 0.015, 0.0005, [(0.002, 1666.0, 0.201), (0.015, 1326.0, 0.379), (0.089, 1054.0, 0.481), (0.094, 1558.0, 0.359), (0.111, 922.0, 0.175), (0.126, 1829.0, 0.557), (0.222, 1032.0, 0.499), (0.24, 1296.0, 0.429), (0.245, 2102.0, 0.566), (0.266, 1969.0, 0.435), (0.272, 1147.0, 0.303), (0.276, 1832.0, 0.49), (0.299, 2419.0, 0.376), (0.303, 2052.0, 0.23), (0.311, 1256.0, 0.414), (0.35, 2433.0, 0.534), (0.395, 1707.0, 0.21), (0.468, 1969.0, 0.557), (0.512, 2153.0, 0.548), (0.647, 1389.0, 0.344), (0.681, 2192.0, 0.388), (0.709, 1214.0, 0.181), (0.717, 1069.0, 0.537), (0.734, 982.0, 0.318), (0.802, 1465.0, 0.49), (0.839, 941.0, 0.382), (0.855, 1424.0, 0.3), (0.863, 1421.0, 0.225), (0.938, 2418.0, 0.408), (0.942, 2187.0, 0.239)], 1.01)
    p2 = _nticks('lowpass', 0.02, 0.0005, 127120, [(0.004, 956.0, 0.292), (0.008, 1163.0, 0.172), (0.053, 1058.0, 0.306), (0.141, 1055.0, 0.341), (0.191, 948.0, 0.318), (0.222, 1016.0, 0.233), (0.239, 1024.0, 0.163), (0.308, 991.0, 0.216), (0.335, 979.0, 0.248), (0.397, 1134.0, 0.23), (0.497, 1040.0, 0.213), (0.603, 1044.0, 0.169), (0.729, 1138.0, 0.309), (0.863, 1144.0, 0.318)], 1.01)
    return _finalize(_mix(p1, p2))
def geo_boulder_settle_001():
    p1 = _at(_noise(0.5, 0.3, 0.05, 128001, 'lowpass', 500.0), 0.0, 0.89)
    p2 = _at(_noise(0.3, 0.3, 0.02, 128002, 'bandpass', 900.0), 0.05, 0.89)
    p3 = _at(_sweep('sine', 80.0, 40.0, 0.25, 0.5, 0.002), 0.5, 0.89)
    p4 = _at(_noise(0.08, 0.4, 0.001, 128004, 'lowpass', 500.0), 0.5, 0.89)
    p5 = _tticks('triangle', 0.02, 0.0005, [(0.62, 1300.0, 0.15), (0.7, 1000.0, 0.12), (0.82, 900.0, 0.1)], 0.89)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def geo_cliff_edge_crumble_001():
    p1 = _at(_noise(0.9, 0.488, 0.05, 129001, 'bandpass', 1000.0), 0.0, 1.37)
    p2 = _nticks('bandpass', 0.03, 0.001, 129120, [(0.241, 642.0, 0.409), (0.308, 1222.0, 0.368), (0.417, 778.0, 0.291), (0.467, 848.0, 0.364), (0.585, 631.0, 0.283), (0.606, 1741.0, 0.257), (0.615, 1389.0, 0.421), (0.681, 1439.0, 0.261), (0.703, 1319.0, 0.35), (0.805, 859.0, 0.442), (0.865, 878.0, 0.297), (0.891, 839.0, 0.227), (0.958, 1035.0, 0.46), (0.965, 1509.0, 0.325)], 1.37)
    p3 = _at(_sweep('sine', 110.0, 50.0, 0.12, 0.558, 0.002), 0.5, 1.37)
    p4 = _at(_sweep('sine', 110.0, 50.0, 0.12, 0.418, 0.002), 0.85, 1.37)
    p5 = _at(_sweep('sine', 110.0, 50.0, 0.12, 0.279, 0.002), 1.2, 1.37)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def geo_cave_boom_echo_001():
    p1 = _at(_sweep('sine', 70.0, 35.0, 0.4, 0.554, 0.003), 0.0, 2.25)
    p2 = _at(_noise(0.15, 0.443, 0.001, 130002, 'lowpass', 300.0), 0.0, 2.25)
    p3 = _at(_sweep('sine', 70.0, 35.0, 0.4, 0.332, 0.003), 0.45, 2.25)
    p4 = _at(_sweep('sine', 70.0, 35.0, 0.4, 0.221, 0.003), 0.85, 2.25)
    p5 = _at(_sweep('sine', 70.0, 35.0, 0.4, 0.133, 0.003), 1.3, 2.25)
    p6 = _at(_sweep('sine', 70.0, 35.0, 0.4, 0.077, 0.003), 1.8, 2.25)
    p7 = _at(_noise(0.15, 0.266, 0.001, 130007, 'lowpass', 300.0), 0.45, 2.25)
    p8 = _at(_noise(0.15, 0.177, 0.001, 130008, 'lowpass', 300.0), 0.85, 2.25)
    p9 = _at(_noise(0.15, 0.106, 0.001, 130009, 'lowpass', 300.0), 1.3, 2.25)
    p10 = _at(_noise(0.15, 0.062, 0.001, 130010, 'lowpass', 300.0), 1.8, 2.25)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10))
def geo_sinkhole_collapse_001():
    p1 = _at(_noise(0.04, 0.5, 0.0005, 131001, 'highpass', 2500.0), 0.0, 1.75)
    p2 = _at(_noise(1.4, 0.45, 0.08, 131002, 'lowpass', 350.0), 0.05, 1.75)
    p3 = _at(_sweep('sine', 120.0, 30.0, 1.2, 0.4, 0.02), 0.1, 1.75)
    p4 = _nticks('lowpass', 0.03, 0.001, 131240, [(0.515, 758.0, 0.231), (0.523, 947.0, 0.177), (0.596, 450.0, 0.203), (0.623, 985.0, 0.278), (0.85, 780.0, 0.275), (1.076, 776.0, 0.286), (1.107, 572.0, 0.29), (1.186, 549.0, 0.252), (1.28, 605.0, 0.124), (1.436, 786.0, 0.172)], 1.75)
    p5 = _at(_sweep('sine', 60.0, 30.0, 0.3, 0.45, 0.002), 1.4, 1.75)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def geo_geyser_eruption_001():
    p1 = _at(_noise(0.9, 0.11, 0.7, 132001, 'bandpass', 2500.0), 0.0, 2.55)
    p2 = _at(_tone('sine', 90.0, 0.9, 0.074, 0.8), 0.0, 2.55)
    p3 = _at(_noise(1.2, 0.368, 0.01, 132003, 'highpass', 3000.0), 0.9, 2.55)
    p4 = _at(_noise(1.2, 0.221, 0.02, 132004, 'bandpass', 800.0), 0.9, 2.55)
    p5 = _tticks('sine', 0.04, 0.002, [(0.198, 289.0, 0.125), (0.355, 291.0, 0.096), (0.374, 373.0, 0.127), (0.534, 479.0, 0.09), (0.549, 452.0, 0.109), (0.677, 384.0, 0.102), (0.714, 397.0, 0.102), (0.74, 293.0, 0.12), (0.822, 481.0, 0.144), (0.867, 489.0, 0.112)], 2.55)
    p6 = _at(_noise(0.5, 0.11, 0.05, 132006, 'bandpass', 4000.0), 2.0, 2.55)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def geo_obsidian_flake_chip_001():
    p1 = _tticks('sine', 0.06, 0.0005, [(0.0, 3200.0, 0.245), (0.14, 2600.0, 0.204), (0.26, 3800.0, 0.163)], 0.37)
    p2 = _nticks('highpass', 0.006, 0.0005, 133120, [(0.0, 5000.0, 0.326), (0.14, 5000.0, 0.285), (0.26, 5000.0, 0.245)], 0.37)
    p3 = _at(_tone('sine', 5200.0, 0.25, 0.049, 0.0005), 0.0, 0.37)
    return _finalize(_mix(p1, p2, p3))
def geo_cooling_rock_tick_001():
    p1 = _tticks('triangle', 0.012, 0.0005, [(0.115, 3145.0, 0.433), (0.419, 2171.0, 0.467), (0.615, 2856.0, 0.377), (0.63, 2721.0, 0.29), (0.651, 3169.0, 0.421), (0.712, 3158.0, 0.48), (0.956, 3006.0, 0.551), (1.057, 3068.0, 0.4), (1.111, 3166.0, 0.559), (1.184, 2125.0, 0.522), (1.416, 2281.0, 0.343), (1.537, 2302.0, 0.469)], 1.65)
    p2 = _at(_noise(1.6, 0.153, 0.4, 134002, 'bandpass', 200.0), 0.0, 1.65)
    return _finalize(_mix(p1, p2))
def geo_geode_split_shimmer_001():
    p1 = _at(_noise(0.02, 0.335, 0.0005, 135001, 'highpass', 2500.0), 0.0, 0.85)
    p2 = _at(_sweep('sine', 200.0, 100.0, 0.08, 0.234, 0.001), 0.0, 0.85)
    p3 = _at(_tone('sine', 2400.0, 0.6, 0.08, 0.002), 0.05, 0.85)
    p4 = _at(_tone('sine', 3100.0, 0.6, 0.08, 0.002), 0.09, 0.85)
    p5 = _at(_tone('sine', 3900.0, 0.6, 0.08, 0.002), 0.13, 0.85)
    p6 = _at(_tone('sine', 5200.0, 0.6, 0.08, 0.002), 0.2, 0.85)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def geo_hollow_rock_tap_001():
    p1 = _tticks('triangle', 0.08, 0.001, [(0.0, 260.0, 0.636), (0.22, 260.0, 0.557), (0.44, 220.0, 0.636)], 0.85)
    p2 = _nticks('lowpass', 0.02, 0.0005, 136120, [(0.0, 900.0, 0.318), (0.22, 900.0, 0.286), (0.44, 900.0, 0.318)], 0.85)
    p3 = _at(_tone('sine', 130.0, 0.8, 0.159, 0.01), 0.0, 0.85)
    return _finalize(_mix(p1, p2, p3))
def geo_singing_dune_boom_001():
    p1 = _at(_tone('sine', 78.0, 1.8, 0.3, 0.6), 0.0, 1.85)
    p2 = _at(_tone('sine', 81.0, 1.8, 0.3, 0.6), 0.0, 1.85)
    p3 = _at(_tone('sine', 156.0, 1.8, 0.1, 0.7), 0.0, 1.85)
    p4 = _at(_noise(1.7, 0.15, 0.6, 137004, 'bandpass', 400.0), 0.0, 1.85)
    return _finalize(_mix(p1, p2, p3, p4))
def geo_drought_clay_crack_001():
    p1 = _nticks('highpass', 0.01, 0.0005, 138060, [(0.0, 3500.0, 0.441), (0.1, 4200.0, 0.331), (0.17, 3000.0, 0.331), (0.31, 4500.0, 0.386), (0.4, 3800.0, 0.276), (0.62, 3200.0, 0.331), (0.75, 4600.0, 0.276), (0.9, 3600.0, 0.221)], 0.96)
    p2 = _tticks('sine', 0.03, 0.0005, [(0.0, 400.0, 0.221), (0.17, 380.0, 0.165), (0.4, 420.0, 0.165), (0.62, 390.0, 0.165)], 0.96)
    p3 = _at(_noise(0.9, 0.088, 0.2, 138003, 'bandpass', 1800.0), 0.0, 0.96)
    return _finalize(_mix(p1, p2, p3))
def geo_salt_crust_crunch_001():
    p1 = _nticks('bandpass', 0.025, 0.001, 139060, [(0.0, 2200.0, 0.63), (0.04, 2800.0, 0.54), (0.07, 1900.0, 0.54), (0.13, 2500.0, 0.63), (0.16, 3100.0, 0.45), (0.22, 2000.0, 0.54), (0.3, 2600.0, 0.36), (0.34, 2300.0, 0.36)], 0.53)
    p2 = _nticks('highpass', 0.008, 0.0005, 139120, [(0.077, 5336.0, 0.247), (0.094, 7924.0, 0.205), (0.237, 7958.0, 0.36), (0.274, 5073.0, 0.22), (0.29, 8394.0, 0.285), (0.314, 7290.0, 0.353), (0.32, 6522.0, 0.353), (0.351, 7066.0, 0.295), (0.394, 5632.0, 0.272), (0.398, 5342.0, 0.312), (0.407, 6334.0, 0.227), (0.418, 5166.0, 0.286), (0.447, 8148.0, 0.209), (0.475, 6171.0, 0.277)], 0.53)
    p3 = _at(_tone('sine', 120.0, 0.1, 0.36, 0.002), 0.0, 0.53)
    return _finalize(_mix(p1, p2, p3))
def geo_plate_stick_slip_001():
    p1 = _at(_sweep('sawtooth', 40.0, 48.0, 0.4, 0.239, 0.1), 0.0, 2.05)
    p2 = _at(_noise(2.0, 0.319, 0.5, 140002, 'lowpass', 150.0), 0.0, 2.05)
    p3 = _at(_sweep('triangle', 65.0, 90.0, 1.8, 0.159, 0.4), 0.0, 2.05)
    p4 = _at(_noise(0.15, 0.638, 0.005, 140004, 'lowpass', 250.0), 0.45, 2.05)
    p5 = _at(_noise(0.15, 0.638, 0.005, 140005, 'lowpass', 250.0), 1.0, 2.05)
    p6 = _at(_noise(0.15, 0.638, 0.005, 140006, 'lowpass', 250.0), 1.65, 2.05)
    p7 = _at(_sweep('sine', 100.0, 45.0, 0.2, 0.558, 0.003), 0.45, 2.05)
    p8 = _at(_sweep('sine', 100.0, 45.0, 0.2, 0.558, 0.003), 1.0, 2.05)
    p9 = _at(_sweep('sine', 100.0, 45.0, 0.2, 0.558, 0.003), 1.65, 2.05)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8, p9))
def geo_volcanic_ash_fall_001():
    p1 = _at(_noise(1.8, 0.314, 0.5, 141001, 'highpass', 5000.0), 0.0, 1.86)
    p2 = _nticks('bandpass', 0.015, 0.001, 141120, [(0.004, 4330.0, 0.088), (0.017, 5455.0, 0.116), (0.278, 5121.0, 0.135), (0.295, 3643.0, 0.127), (0.308, 4442.0, 0.105), (0.323, 5228.0, 0.088), (0.34, 4056.0, 0.143), (0.389, 4550.0, 0.115), (0.643, 4255.0, 0.085), (0.662, 4837.0, 0.085), (0.674, 3984.0, 0.104), (0.761, 4759.0, 0.096), (0.864, 3475.0, 0.118), (0.927, 3495.0, 0.149), (0.929, 4671.0, 0.146), (0.97, 3709.0, 0.093), (1.091, 4919.0, 0.096), (1.158, 4567.0, 0.105), (1.345, 4861.0, 0.11), (1.462, 4909.0, 0.108), (1.588, 2963.0, 0.137), (1.597, 4470.0, 0.088), (1.624, 3302.0, 0.144), (1.751, 3460.0, 0.144), (1.762, 3833.0, 0.089), (1.794, 4380.0, 0.097)], 1.86)
    p3 = _at(_tone('sine', 55.0, 1.8, 0.157, 0.7), 0.0, 1.86)
    return _finalize(_mix(p1, p2, p3))
def geo_magma_chamber_throb_001():
    p1 = _at(_sweep('sine', 48.0, 38.0, 0.5, 0.593, 0.01), 0.0, 2.35)
    p2 = _at(_sweep('sine', 48.0, 38.0, 0.5, 0.593, 0.01), 0.6, 2.35)
    p3 = _at(_sweep('sine', 48.0, 38.0, 0.5, 0.593, 0.01), 1.2, 2.35)
    p4 = _at(_sweep('sine', 48.0, 38.0, 0.5, 0.593, 0.01), 1.8, 2.35)
    p5 = _at(_noise(0.5, 0.264, 0.02, 142005, 'lowpass', 160.0), 0.0, 2.35)
    p6 = _at(_noise(0.5, 0.264, 0.02, 142006, 'lowpass', 160.0), 0.6, 2.35)
    p7 = _at(_noise(0.5, 0.264, 0.02, 142007, 'lowpass', 160.0), 1.2, 2.35)
    p8 = _at(_noise(0.5, 0.264, 0.02, 142008, 'lowpass', 160.0), 1.8, 2.35)
    p9 = _at(_noise(2.3, 0.198, 0.5, 142009, 'lowpass', 120.0), 0.0, 2.35)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8, p9))
def geo_pumice_water_bump_001():
    p1 = _at(_sweep('sine', 420.0, 231.00000000000003, 0.07, 0.488, 0.001), 0.0, 0.95)
    p2 = _at(_sweep('sine', 380.0, 209.00000000000003, 0.07, 0.488, 0.001), 0.19, 0.95)
    p3 = _at(_sweep('sine', 460.0, 253.00000000000003, 0.07, 0.488, 0.001), 0.4, 0.95)
    p4 = _at(_sweep('sine', 400.0, 220.00000000000003, 0.07, 0.488, 0.001), 0.62, 0.95)
    p5 = _at(_sweep('sine', 360.0, 198.00000000000003, 0.07, 0.488, 0.001), 0.8, 0.95)
    p6 = _nticks('bandpass', 0.04, 0.001, 143360, [(0.0, 2000.0, 0.244), (0.19, 2000.0, 0.244), (0.4, 2000.0, 0.244), (0.62, 2000.0, 0.244), (0.8, 2000.0, 0.244)], 0.95)
    p7 = _at(_noise(0.9, 0.13, 0.3, 143007, 'bandpass', 700.0), 0.0, 0.95)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7))
def geo_ice_shelf_chirp_001():
    p1 = _at(_noise(0.02, 0.242, 0.0005, 144001, 'highpass', 3000.0), 0.0, 1.4)
    p2 = _at(_sweep('sine', 3000.0, 300.0, 0.35, 0.282, 0.001), 0.0, 1.4)
    p3 = _at(_sweep('sine', 4500.0, 450.0, 0.35, 0.121, 0.001), 0.0, 1.4)
    p4 = _at(_sweep('sine', 3000.0, 300.0, 0.35, 0.161, 0.001), 0.5, 1.4)
    p5 = _at(_sweep('sine', 3000.0, 300.0, 0.35, 0.081, 0.001), 1.0, 1.4)
    return _finalize(_mix(p1, p2, p3, p4, p5))

OFFICIAL_PRESETS_GEOSCAPE = {
    'geo-glacier-moulin-gurgle-001': geo_glacier_moulin_gurgle_001,
    'geo-iceberg-roll-001': geo_iceberg_roll_001,
    'geo-icicle-snap-001': geo_icicle_snap_001,
    'geo-ice-cave-whistle-001': geo_ice_cave_whistle_001,
    'geo-snow-slab-whump-001': geo_snow_slab_whump_001,
    'geo-frost-crystal-glint-001': geo_frost_crystal_glint_001,
    'geo-frost-heave-creak-001': geo_frost_heave_creak_001,
    'geo-scree-pebble-trickle-001': geo_scree_pebble_trickle_001,
    'geo-boulder-settle-001': geo_boulder_settle_001,
    'geo-cliff-edge-crumble-001': geo_cliff_edge_crumble_001,
    'geo-cave-boom-echo-001': geo_cave_boom_echo_001,
    'geo-sinkhole-collapse-001': geo_sinkhole_collapse_001,
    'geo-geyser-eruption-001': geo_geyser_eruption_001,
    'geo-obsidian-flake-chip-001': geo_obsidian_flake_chip_001,
    'geo-cooling-rock-tick-001': geo_cooling_rock_tick_001,
    'geo-geode-split-shimmer-001': geo_geode_split_shimmer_001,
    'geo-hollow-rock-tap-001': geo_hollow_rock_tap_001,
    'geo-singing-dune-boom-001': geo_singing_dune_boom_001,
    'geo-drought-clay-crack-001': geo_drought_clay_crack_001,
    'geo-salt-crust-crunch-001': geo_salt_crust_crunch_001,
    'geo-plate-stick-slip-001': geo_plate_stick_slip_001,
    'geo-volcanic-ash-fall-001': geo_volcanic_ash_fall_001,
    'geo-magma-chamber-throb-001': geo_magma_chamber_throb_001,
    'geo-pumice-water-bump-001': geo_pumice_water_bump_001,
    'geo-ice-shelf-chirp-001': geo_ice_shelf_chirp_001,
}
