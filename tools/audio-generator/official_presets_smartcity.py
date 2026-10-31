"""Mission 18 - Smart Cities (25 sounds)."""
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


def city_autonomous_pod_glide_001():
    p1 = _at(_sweep('sine', 150.0, 260.0, 1.2, 0.347, 0.3), 0.0, 1.25)
    p2 = _at(_sweep('sine', 300.0, 520.0, 1.2, 0.174, 0.3), 0.0, 1.25)
    p3 = _at(_noise(1.2, 0.434, 0.4, 180003, 'bandpass', 800.0), 0.0, 1.25)
    p4 = _at(_noise(0.6, 0.579, 0.3, 180004, 'bandpass', 2000.0), 0.3, 1.25)
    return _finalize(_mix(p1, p2, p3, p4))
def city_maglev_station_arrive_001():
    p1 = _at(_sweep('sine', 1500.0, 200.0, 1.8, 0.333, 0.1), 0.0, 2.4)
    p2 = _at(_noise(1.8, 0.444, 0.2, 181002, 'bandpass', 1200.0), 0.0, 2.4)
    p3 = _at(_tone('sine', 80.0, 1.8, 0.222, 0.2), 0.0, 2.4)
    p4 = _tticks('sine', 0.4, 0.002, [(1.8, 880.0, 0.444), (1.95, 660.0, 0.444)], 2.4)
    return _finalize(_mix(p1, p2, p3, p4))
def city_drone_delivery_drop_001():
    p1 = _at(_sweep('sawtooth', 160.0, 150.0, 0.9, 0.09, 0.05), 0.0, 0.95)
    p2 = _at(_sweep('sawtooth', 162.0, 152.0, 0.9, 0.067, 0.05), 0.0, 0.95)
    p3 = _at(_noise(0.9, 0.112, 0.1, 182003, 'bandpass', 2500.0), 0.0, 0.95)
    p4 = _at(_noise(0.01, 0.449, 0.0005, 182004, 'highpass', 3000.0), 0.6, 0.95)
    p5 = _at(_sweep('sine', 1500.0, 900.0, 0.03, 0.225, 0.001), 0.6, 0.95)
    p6 = _at(_sweep('sine', 90.0, 50.0, 0.1, 0.393, 0.002), 0.8, 0.95)
    p7 = _at(_noise(0.05, 0.225, 0.001, 182007, 'lowpass', 500.0), 0.8, 0.95)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7))
def city_smart_streetlight_wake_001():
    p1 = _at(_noise(0.008, 0.5, 0.0005, 183001, 'highpass', 3000.0), 0.0, 0.8)
    p2 = _at(_tone('sine', 100.0, 0.7, 0.12, 0.1), 0.05, 0.8)
    p3 = _at(_tone('sine', 200.0, 0.7, 0.08, 0.1), 0.05, 0.8)
    p4 = _at(_sweep('sine', 400.0, 800.0, 0.6, 0.08, 0.3), 0.05, 0.8)
    p5 = _at(_tone('sine', 2000.0, 0.05, 0.1, 0.001), 0.7, 0.8)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def city_sensor_mesh_ping_001():
    p1 = _tticks('sine', 0.25, 0.002, [(0.0, 800.0, 0.555), (0.14, 980.0, 0.51), (0.28, 1160.0, 0.47), (0.42, 1340.0, 0.433), (0.56, 1520.0, 0.397), (0.7, 1700.0, 0.366), (0.84, 1880.0, 0.337), (0.98, 2060.0, 0.308)], 1.3)
    p2 = _tticks('sine', 0.2, 0.002, [(0.07, 800.0, 0.222), (0.21, 980.0, 0.204), (0.35, 1160.0, 0.189), (0.49, 1340.0, 0.173), (0.63, 1520.0, 0.16), (0.77, 1700.0, 0.146), (0.91, 1880.0, 0.135), (1.05, 2060.0, 0.124)], 1.3)
    return _finalize(_mix(p1, p2))
def city_ev_charge_start_001():
    p1 = _at(_noise(0.012, 0.46, 0.0005, 185001, 'highpass', 3000.0), 0.0, 1.1)
    p2 = _at(_sweep('sine', 100.0, 300.0, 0.7, 0.138, 0.2), 0.02, 1.1)
    p3 = _tticks('sine', 0.1, 0.002, [(0.8, 1200.0, 0.276), (0.95, 1500.0, 0.276)], 1.1)
    return _finalize(_mix(p1, p2, p3))
def city_ev_charge_complete_001():
    p1 = _at(_sweep('sine', 300.0, 100.0, 0.5, 0.259, 0.05), 0.0, 1.35)
    p2 = _at(_tone('sine', 1319.0, 0.5, 0.431, 0.002), 0.5, 1.35)
    p3 = _at(_tone('sine', 3640.4399999999996, 0.25, 0.129, 0.002), 0.5, 1.35)
    p4 = _at(_tone('sine', 1047.0, 0.6, 0.431, 0.002), 0.7, 1.35)
    p5 = _at(_tone('sine', 2889.72, 0.3, 0.129, 0.002), 0.7, 1.35)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def city_traffic_ai_reroute_001():
    p1 = _tticks('triangle', 0.05, 0.002, [(0.0, 1400.0, 0.56), (0.1, 1000.0, 0.56), (0.2, 1700.0, 0.56), (0.3, 1200.0, 0.56)], 0.85)
    p2 = _at(_tone('sine', 1800.0, 0.3, 0.373, 0.005), 0.5, 0.85)
    return _finalize(_mix(p1, p2))
def city_smart_crossing_beacon_001():
    p1 = _tticks('sine', 0.04, 0.002, [(0.0, 1000.0, 0.402), (0.3, 1100.0, 0.423), (0.555, 1200.0, 0.442), (0.772, 1300.0, 0.461), (0.956, 1400.0, 0.482), (1.113, 1500.0, 0.501), (1.246, 1600.0, 0.522), (1.359, 1700.0, 0.542), (1.455, 1800.0, 0.563)], 2.1)
    p2 = _at(_tone('sine', 2000.0, 0.4, 0.321, 0.002), 1.655, 2.1)
    return _finalize(_mix(p1, p2))
def city_recycling_sorter_whir_001():
    p1 = _at(_sweep('sawtooth', 180.0, 260.0, 0.4, 0.181, 0.05), 0.0, 1.55)
    p2 = _at(_sweep('sawtooth', 180.0, 260.0, 0.4, 0.181, 0.05), 0.5, 1.55)
    p3 = _at(_sweep('sawtooth', 180.0, 260.0, 0.4, 0.181, 0.05), 1.0, 1.55)
    p4 = _nticks('bandpass', 0.015, 0.0005, 189240, [(0.4, 1500.0, 1.0), (0.9, 1200.0, 1.0), (1.4, 1800.0, 1.0)], 1.55)
    p5 = _at(_noise(1.5, 0.241, 0.3, 189005, 'bandpass', 1500.0), 0.0, 1.55)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def city_smart_bin_compact_001():
    p1 = _at(_sweep('sawtooth', 55.0, 48.0, 0.8, 0.141, 0.1), 0.0, 1.1)
    p2 = _at(_noise(0.8, 0.235, 0.1, 190002, 'lowpass', 400.0), 0.0, 1.1)
    p3 = _nticks('bandpass', 0.03, 0.001, 190180, [(0.201, 2477.0, 0.262), (0.276, 2310.0, 0.305), (0.293, 1571.0, 0.286), (0.33, 1971.0, 0.238), (0.421, 2364.0, 0.198), (0.425, 1778.0, 0.322), (0.509, 2025.0, 0.257), (0.566, 1877.0, 0.191), (0.586, 2168.0, 0.192), (0.729, 1742.0, 0.232)], 1.1)
    p4 = _at(_sweep('sine', 70.0, 40.0, 0.2, 0.588, 0.002), 0.85, 1.1)
    return _finalize(_mix(p1, p2, p3, p4))
def city_air_quality_alert_001():
    p1 = _at(_tone('sine', 880.0, 0.4, 0.541, 0.005), 0.0, 0.95)
    p2 = _at(_tone('sine', 740.0, 0.4, 0.541, 0.005), 0.25, 0.95)
    p3 = _at(_tone('sine', 587.0, 0.4, 0.541, 0.005), 0.5, 0.95)
    p4 = _at(_noise(0.9, 0.086, 0.2, 191004, 'bandpass', 1500.0), 0.0, 0.95)
    return _finalize(_mix(p1, p2, p3, p4))
def city_hologram_billboard_flicker_001():
    p1 = _at(_tone('sine', 120.0, 1.2, 0.171, 0.05), 0.0, 1.25)
    p2 = _nticks('highpass', 0.01, 0.0005, 192120, [(0.177, 5255.0, 0.312), (0.22, 5311.0, 0.302), (0.226, 3040.0, 0.427), (0.325, 4798.0, 0.216), (0.332, 3436.0, 0.458), (0.349, 3620.0, 0.46), (0.403, 4055.0, 0.221), (0.506, 4694.0, 0.252), (0.689, 5902.0, 0.364), (0.724, 2931.0, 0.273), (0.753, 4103.0, 0.309), (0.806, 2576.0, 0.417), (0.857, 4859.0, 0.286), (0.907, 4877.0, 0.489)], 1.25)
    p3 = _tticks('sine', 0.04, 0.001, [(0.21, 916.0, 0.228), (0.546, 1430.0, 0.295), (0.668, 609.0, 0.267), (0.847, 826.0, 0.228), (0.909, 1179.0, 0.242), (0.953, 1300.0, 0.254)], 1.25)
    return _finalize(_mix(p1, p2, p3))
def city_smart_glass_tint_001():
    p1 = _at(_sweep('sine', 400.0, 250.0, 0.8, 0.167, 0.2), 0.0, 0.96)
    p2 = _at(_noise(0.8, 0.25, 0.3, 193002, 'bandpass', 1800.0), 0.0, 0.96)
    p3 = _at(_noise(0.01, 0.626, 0.0005, 193003, 'highpass', 3000.0), 0.85, 0.96)
    p4 = _at(_tone('sine', 1500.0, 0.06, 0.25, 0.002), 0.85, 0.96)
    return _finalize(_mix(p1, p2, p3, p4))
def city_elevator_pod_chime_001():
    p1 = _at(_tone('sine', 90.0, 0.9, 0.142, 0.2), 0.0, 1.85)
    p2 = _at(_sweep('sine', 90.0, 180.0, 0.9, 0.071, 0.2), 0.0, 1.85)
    p3 = _at(_noise(0.9, 0.114, 0.3, 194003, 'lowpass', 300.0), 0.0, 1.85)
    p4 = _at(_tone('sine', 1047.0, 0.5, 0.426, 0.002), 1.0, 1.85)
    p5 = _at(_tone('sine', 2889.72, 0.25, 0.128, 0.002), 1.0, 1.85)
    p6 = _at(_tone('sine', 1319.0, 0.6, 0.426, 0.002), 1.2, 1.85)
    p7 = _at(_tone('sine', 3640.4399999999996, 0.3, 0.128, 0.002), 1.2, 1.85)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7))
def city_parking_spot_guide_001():
    p1 = _tticks('sine', 0.05, 0.002, [(0.0, 700.0, 0.372), (0.4, 816.0, 0.404), (0.72, 933.0, 0.433), (0.976, 1050.0, 0.465), (1.181, 1166.0, 0.497), (1.345, 1283.0, 0.526), (1.476, 1400.0, 0.558)], 1.98)
    p2 = _at(_tone('sine', 1800.0, 0.3, 0.372, 0.005), 1.626, 1.98)
    return _finalize(_mix(p1, p2))
def city_pneumatic_tube_transit_001():
    p1 = _at(_noise(0.8, 0.425, 0.3, 196001, 'bandpass', 1000.0), 0.0, 0.98)
    p2 = _at(_noise(0.8, 0.243, 0.3, 196002, 'lowpass', 400.0), 0.0, 0.98)
    p3 = _at(_sweep('sine', 200.0, 150.0, 0.8, 0.073, 0.3), 0.0, 0.98)
    p4 = _at(_sweep('sine', 300.0, 120.0, 0.08, 0.485, 0.001), 0.85, 0.98)
    p5 = _at(_noise(0.05, 0.364, 0.001, 196005, 'lowpass', 900.0), 0.85, 0.98)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def city_water_grid_valve_open_001():
    p1 = _at(_sweep('sawtooth', 90.0, 110.0, 0.5, 0.142, 0.05), 0.0, 1.55)
    p2 = _at(_sweep('sine', 100.0, 50.0, 0.1, 0.569, 0.002), 0.5, 1.55)
    p3 = _at(_noise(1.0, 0.427, 0.3, 197003, 'bandpass', 1500.0), 0.5, 1.55)
    p4 = _at(_noise(1.0, 0.285, 0.3, 197004, 'highpass', 4000.0), 0.5, 1.55)
    return _finalize(_mix(p1, p2, p3, p4))
def city_ticket_gate_tap_001():
    p1 = _at(_tone('sine', 1500.0, 0.12, 0.443, 0.002), 0.0, 0.5)
    p2 = _at(_sweep('sawtooth', 200.0, 300.0, 0.25, 0.076, 0.02), 0.15, 0.5)
    p3 = _at(_noise(0.015, 0.506, 0.0005, 198003, 'highpass', 3000.0), 0.4, 0.5)
    p4 = _at(_sweep('triangle', 400.0, 300.0, 0.05, 0.316, 0.001), 0.4, 0.5)
    return _finalize(_mix(p1, p2, p3, p4))
def city_street_robot_sweeper_001():
    p1 = _at(_tone('sawtooth', 80.0, 1.6, 0.131, 0.2), 0.0, 1.65)
    p2 = _at(_noise(1.6, 0.546, 0.3, 199002, 'bandpass', 2500.0), 0.0, 1.65)
    p3 = _tticks('triangle', 0.02, 0.001, [(0.017, 240.0, 0.19), (0.027, 196.0, 0.225), (0.056, 256.0, 0.234), (0.118, 233.0, 0.183), (0.143, 190.0, 0.212), (0.181, 177.0, 0.238), (0.314, 298.0, 0.262), (0.329, 286.0, 0.231), (0.33, 201.0, 0.205), (0.403, 240.0, 0.196), (0.415, 282.0, 0.249), (0.495, 155.0, 0.218), (0.508, 153.0, 0.244), (0.686, 188.0, 0.24), (0.695, 179.0, 0.199), (0.808, 276.0, 0.21), (0.945, 182.0, 0.179), (1.039, 211.0, 0.181), (1.278, 258.0, 0.231), (1.334, 252.0, 0.242)], 1.65)
    p4 = _nticks('highpass', 0.006, 0.0005, 199240, [(0.136, 6521.0, 0.159), (0.16, 6991.0, 0.168), (0.262, 5845.0, 0.192), (0.272, 4455.0, 0.194), (0.315, 6939.0, 0.22), (0.322, 4393.0, 0.234), (0.386, 5970.0, 0.118), (0.406, 5999.0, 0.113), (0.448, 6368.0, 0.253), (0.477, 4536.0, 0.151), (0.488, 5620.0, 0.164), (0.509, 5371.0, 0.138), (0.574, 4160.0, 0.138), (0.696, 4461.0, 0.207), (0.724, 5469.0, 0.192), (0.733, 4087.0, 0.142), (0.762, 5092.0, 0.192), (0.764, 5396.0, 0.223), (0.771, 4465.0, 0.159), (0.781, 6144.0, 0.116), (0.784, 4022.0, 0.124), (0.79, 5758.0, 0.216), (0.838, 6440.0, 0.148), (0.914, 6270.0, 0.133), (1.188, 4573.0, 0.234), (1.295, 5268.0, 0.175), (1.307, 6499.0, 0.135), (1.311, 4673.0, 0.258), (1.421, 4638.0, 0.133), (1.483, 6975.0, 0.175)], 1.65)
    return _finalize(_mix(p1, p2, p3, p4))
def city_emergency_priority_signal_001():
    p1 = _tticks('sine', 0.08, 0.002, [(0.0, 1000.0, 0.556), (0.12, 1400.0, 0.556), (0.24, 1800.0, 0.556), (0.5, 1000.0, 0.556), (0.62, 1400.0, 0.556), (0.74, 1800.0, 0.556)], 0.87)
    return _finalize(_mix(p1))
def city_solar_panel_track_001():
    p1 = _nticks('bandpass', 0.01, 0.0005, 201060, [(0.0, 1200.0, 1.0), (0.12, 1500.0, 1.0), (0.24, 1200.0, 1.0), (0.36, 1500.0, 1.0), (0.48, 1200.0, 1.0), (0.6, 1500.0, 1.0), (0.72, 1200.0, 1.0), (0.84, 1500.0, 1.0), (0.96, 1200.0, 1.0), (1.08, 1500.0, 1.0)], 1.35)
    p2 = _at(_sweep('sine', 90.0, 100.0, 1.3, 0.278, 0.1), 0.0, 1.35)
    return _finalize(_mix(p1, p2))
def city_data_hub_hum_001():
    p1 = _at(_tone('sine', 60.0, 1.8, 0.384, 0.4), 0.0, 1.85)
    p2 = _at(_tone('sine', 120.0, 1.8, 0.192, 0.4), 0.0, 1.85)
    p3 = _at(_noise(1.8, 0.192, 0.4, 202003, 'bandpass', 600.0), 0.0, 1.85)
    p4 = _tticks('sine', 0.03, 0.001, [(0.735, 1928.0, 0.365), (0.761, 2834.0, 0.215), (1.01, 1910.0, 0.328), (1.044, 2671.0, 0.223), (1.158, 2040.0, 0.315), (1.384, 2065.0, 0.374), (1.522, 3176.0, 0.198), (1.553, 3159.0, 0.317)], 1.85)
    return _finalize(_mix(p1, p2, p3, p4))
def city_crowd_density_pulse_001():
    p1 = _at(_sweep('sine', 300.0, 1200.0, 0.8, 0.282, 0.2), 0.0, 0.95)
    p2 = _tticks('sine', 0.1, 0.002, [(0.2, 500.0, 0.563), (0.5, 700.0, 0.563), (0.8, 900.0, 0.563)], 0.95)
    return _finalize(_mix(p1, p2))
def city_skybridge_conveyor_glide_001():
    p1 = _at(_tone('sine', 70.0, 2.0, 0.32, 0.4), 0.0, 2.05)
    p2 = _at(_noise(2.0, 0.533, 0.4, 204002, 'bandpass', 500.0), 0.0, 2.05)
    p3 = _nticks('lowpass', 0.02, 0.001, 204180, [(0.0, 600.0, 0.32), (0.1, 600.0, 0.32), (0.2, 600.0, 0.32), (0.3, 600.0, 0.32), (0.4, 600.0, 0.32), (0.5, 600.0, 0.32), (0.6, 600.0, 0.32), (0.7, 600.0, 0.32), (0.8, 600.0, 0.32), (0.9, 600.0, 0.32), (1.0, 600.0, 0.32), (1.1, 600.0, 0.32), (1.2, 600.0, 0.32), (1.3, 600.0, 0.32), (1.4, 600.0, 0.32), (1.5, 600.0, 0.32), (1.6, 600.0, 0.32), (1.7, 600.0, 0.32), (1.8, 600.0, 0.32), (1.9, 600.0, 0.32)], 2.05)
    p4 = _at(_sweep('sawtooth', 120.0, 125.0, 2.0, 0.133, 0.4), 0.0, 2.05)
    return _finalize(_mix(p1, p2, p3, p4))

OFFICIAL_PRESETS_SMARTCITY = {
    'city-autonomous-pod-glide-001': city_autonomous_pod_glide_001,
    'city-maglev-station-arrive-001': city_maglev_station_arrive_001,
    'city-drone-delivery-drop-001': city_drone_delivery_drop_001,
    'city-smart-streetlight-wake-001': city_smart_streetlight_wake_001,
    'city-sensor-mesh-ping-001': city_sensor_mesh_ping_001,
    'city-ev-charge-start-001': city_ev_charge_start_001,
    'city-ev-charge-complete-001': city_ev_charge_complete_001,
    'city-traffic-ai-reroute-001': city_traffic_ai_reroute_001,
    'city-smart-crossing-beacon-001': city_smart_crossing_beacon_001,
    'city-recycling-sorter-whir-001': city_recycling_sorter_whir_001,
    'city-smart-bin-compact-001': city_smart_bin_compact_001,
    'city-air-quality-alert-001': city_air_quality_alert_001,
    'city-hologram-billboard-flicker-001': city_hologram_billboard_flicker_001,
    'city-smart-glass-tint-001': city_smart_glass_tint_001,
    'city-elevator-pod-chime-001': city_elevator_pod_chime_001,
    'city-parking-spot-guide-001': city_parking_spot_guide_001,
    'city-pneumatic-tube-transit-001': city_pneumatic_tube_transit_001,
    'city-water-grid-valve-open-001': city_water_grid_valve_open_001,
    'city-ticket-gate-tap-001': city_ticket_gate_tap_001,
    'city-street-robot-sweeper-001': city_street_robot_sweeper_001,
    'city-emergency-priority-signal-001': city_emergency_priority_signal_001,
    'city-solar-panel-track-001': city_solar_panel_track_001,
    'city-data-hub-hum-001': city_data_hub_hum_001,
    'city-crowd-density-pulse-001': city_crowd_density_pulse_001,
    'city-skybridge-conveyor-glide-001': city_skybridge_conveyor_glide_001,
}
