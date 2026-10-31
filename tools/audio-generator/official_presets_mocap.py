"""Mission 16 - Motion Capture & Animation (25 sounds)."""
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


def anim_sensor_suit_calibrate_001():
    p1 = _tticks('sine', 0.08, 0.002, [(0.0, 600.0, 0.452), (0.15, 750.0, 0.452), (0.3, 900.0, 0.452), (0.45, 1050.0, 0.452), (0.6, 1200.0, 0.452), (0.75, 1350.0, 0.452), (0.9, 1500.0, 0.452)], 1.35)
    p2 = _nticks('highpass', 0.006, 0.0005, 160120, [(0.05, 4000.0, 0.361), (0.2, 4000.0, 0.361), (0.35, 4000.0, 0.361), (0.5, 4000.0, 0.361), (0.65, 4000.0, 0.361), (0.8, 4000.0, 0.361)], 1.35)
    p3 = _at(_tone('sine', 1760.0, 0.3, 0.361, 0.005), 1.0, 1.35)
    p4 = _at(_noise(1.0, 0.09, 0.3, 160004, 'bandpass', 3000.0), 0.0, 1.35)
    return _finalize(_mix(p1, p2, p3, p4))
def anim_marker_track_lock_001():
    p1 = _at(_tone('sine', 1200.0, 0.07, 0.473, 0.002), 0.0, 0.24)
    p2 = _at(_tone('sine', 1800.0, 0.1, 0.473, 0.002), 0.09, 0.24)
    p3 = _nticks('highpass', 0.005, 0.0005, 161180, [(0.0, 4000.0, 0.405), (0.09, 4500.0, 0.405)], 0.24)
    return _finalize(_mix(p1, p2, p3))
def anim_capture_start_countdown_001():
    p1 = _tticks('sine', 0.08, 0.002, [(0.0, 800.0, 0.436), (0.4, 800.0, 0.436), (0.8, 800.0, 0.436)], 1.65)
    p2 = _at(_tone('sine', 1600.0, 0.4, 0.508, 0.005), 1.2, 1.65)
    p3 = _at(_tone('sine', 3200.0, 0.2, 0.116, 0.005), 1.2, 1.65)
    return _finalize(_mix(p1, p2, p3))
def anim_capture_stop_001():
    p1 = _at(_tone('sine', 1400.0, 0.08, 0.558, 0.002), 0.0, 0.52)
    p2 = _at(_tone('sine', 900.0, 0.08, 0.558, 0.002), 0.1, 0.52)
    p3 = _at(_sweep('sine', 500.0, 300.0, 0.25, 0.465, 0.002), 0.22, 0.52)
    return _finalize(_mix(p1, p2, p3))
def anim_keyframe_set_001():
    p1 = _at(_noise(0.01, 0.43, 0.0005, 164001, 'highpass', 3500.0), 0.0, 0.19)
    p2 = _at(_tone('sine', 2400.0, 0.05, 0.258, 0.0005), 0.0, 0.19)
    p3 = _at(_tone('sine', 1200.0, 0.12, 0.129, 0.001), 0.02, 0.19)
    return _finalize(_mix(p1, p2, p3))
def anim_keyframe_scrub_001():
    p1 = _tticks('triangle', 0.02, 0.0005, [(0.0, 800.0, 0.577), (0.03, 1142.0, 0.577), (0.06, 1444.0, 0.577), (0.09, 1667.0, 0.577), (0.12, 1785.0, 0.577), (0.15, 1783.0, 0.577), (0.18, 1663.0, 0.577), (0.21, 1437.0, 0.577), (0.24, 1134.0, 0.577), (0.27, 808.0, 0.577), (0.3, 1150.0, 0.577), (0.33, 1450.0, 0.577), (0.36, 1671.0, 0.577), (0.39, 1786.0, 0.577), (0.42, 1782.0, 0.577), (0.45, 1658.0, 0.577), (0.48, 1431.0, 0.577), (0.51, 1127.0, 0.577), (0.54, 816.0, 0.577), (0.57, 1158.0, 0.577), (0.6, 1456.0, 0.577), (0.63, 1675.0, 0.577), (0.66, 1788.0, 0.577), (0.69, 1780.0, 0.577), (0.72, 1654.0, 0.577), (0.75, 1424.0, 0.577), (0.78, 1119.0, 0.577), (0.81, 825.0, 0.577)], 0.95)
    p2 = _at(_noise(0.9, 0.115, 0.1, 165002, 'bandpass', 2000.0), 0.0, 0.95)
    return _finalize(_mix(p1, p2))
def anim_joint_ik_snap_001():
    p1 = _at(_sweep('sine', 300.0, 900.0, 0.06, 0.4, 0.001), 0.0, 0.23)
    p2 = _at(_sweep('sine', 900.0, 500.0, 0.12, 0.3, 0.001), 0.06, 0.23)
    p3 = _at(_noise(0.01, 0.4, 0.0005, 166003, 'highpass', 3500.0), 0.06, 0.23)
    p4 = _at(_sweep('sawtooth', 200.0, 260.0, 0.1, 0.08, 0.005), 0.0, 0.23)
    return _finalize(_mix(p1, p2, p3, p4))
def anim_ragdoll_collapse_001():
    p1 = _at(_sweep('sine', 90.0, 60.0, 0.15, 0.568, 0.002), 0.0, 0.7)
    p2 = _at(_sweep('sine', 90.0, 60.0, 0.15, 0.477, 0.002), 0.18, 0.7)
    p3 = _at(_sweep('sine', 90.0, 60.0, 0.15, 0.386, 0.002), 0.3, 0.7)
    p4 = _at(_sweep('sine', 90.0, 60.0, 0.15, 0.295, 0.002), 0.38, 0.7)
    p5 = _at(_sweep('sine', 90.0, 60.0, 0.15, 0.205, 0.002), 0.43, 0.7)
    p6 = _nticks('lowpass', 0.04, 0.001, 167360, [(0.0, 700.0, 0.284), (0.18, 700.0, 0.239), (0.3, 700.0, 0.193), (0.38, 700.0, 0.148), (0.43, 700.0, 0.102)], 0.7)
    p7 = _at(_noise(0.6, 0.17, 0.1, 167007, 'bandpass', 2500.0), 0.05, 0.7)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7))
def anim_rig_bind_weld_001():
    p1 = _at(_sweep('sine', 200.0, 600.0, 0.5, 0.288, 0.2), 0.0, 0.65)
    p2 = _nticks('bandpass', 0.01, 0.0005, 168120, [(0.0, 1500.0, 0.288), (0.12, 1642.0, 0.329), (0.222, 1785.0, 0.371), (0.309, 1928.0, 0.411), (0.382, 2071.0, 0.454), (0.445, 2214.0, 0.494), (0.498, 2357.0, 0.536), (0.544, 2500.0, 0.577)], 0.65)
    p3 = _at(_tone('sine', 1400.0, 0.05, 0.577, 0.001), 0.55, 0.65)
    return _finalize(_mix(p1, p2, p3))
def anim_blend_crossfade_001():
    p1 = _at(_sweep('sine', 300.0, 900.0, 1.0, 0.283, 0.2), 0.0, 1.05)
    p2 = _at(_sweep('sine', 900.0, 300.0, 1.0, 0.283, 0.2), 0.0, 1.05)
    p3 = _at(_noise(1.0, 0.085, 0.3, 169003, 'bandpass', 1500.0), 0.0, 1.05)
    return _finalize(_mix(p1, p2, p3))
def anim_loop_wrap_rewind_001():
    p1 = _at(_sweep('sine', 1600.0, 300.0, 0.25, 0.442, 0.005), 0.0, 0.44)
    p2 = _at(_sweep('sine', 300.0, 600.0, 0.12, 0.354, 0.002), 0.27, 0.44)
    p3 = _nticks('highpass', 0.006, 0.0005, 170180, [(0.27, 4000.0, 0.531)], 0.44)
    return _finalize(_mix(p1, p2, p3))
def anim_retarget_sweep_001():
    p1 = _at(_noise(0.6, 0.341, 0.15, 171001, 'bandpass', 2000.0), 0.0, 1.1)
    p2 = _tticks('sine', 0.06, 0.002, [(0.0, 500.0, 0.426), (0.12, 620.0, 0.426), (0.24, 740.0, 0.426), (0.36, 860.0, 0.426), (0.48, 980.0, 0.426), (0.6, 1100.0, 0.426)], 1.1)
    p3 = _at(_tone('sine', 1500.0, 0.3, 0.341, 0.005), 0.75, 1.1)
    return _finalize(_mix(p1, p2, p3))
def anim_pose_freeze_hold_001():
    p1 = _at(_tone('sine', 700.0, 0.3, 0.35, 0.001), 0.0, 0.65)
    p2 = _at(_noise(0.01, 0.4, 0.0005, 172002, 'highpass', 3000.0), 0.0, 0.65)
    p3 = _at(_tone('sine', 350.0, 0.5, 0.08, 0.05), 0.1, 0.65)
    return _finalize(_mix(p1, p2, p3))
def anim_pose_mirror_flip_001():
    p1 = _at(_noise(0.3, 0.523, 0.05, 173001, 'bandpass', 2500.0), 0.0, 0.45)
    p2 = _at(_sweep('sine', 500.0, 1500.0, 0.2, 0.523, 0.01), 0.0, 0.45)
    p3 = _at(_sweep('sine', 1500.0, 500.0, 0.2, 0.523, 0.01), 0.2, 0.45)
    return _finalize(_mix(p1, p2, p3))
def anim_onion_skin_ghost_001():
    p1 = _tticks('sine', 0.12, 0.002, [(0.0, 880.0, 0.4), (0.15, 880.0, 0.25), (0.3, 880.0, 0.15), (0.45, 880.0, 0.09), (0.6, 880.0, 0.05)], 0.77)
    p2 = _tticks('sine', 0.12, 0.002, [(0.0, 1320.0, 0.2), (0.15, 1320.0, 0.12), (0.3, 1320.0, 0.07), (0.45, 1320.0, 0.04)], 0.77)
    return _finalize(_mix(p1, p2))
def anim_motion_trail_whoosh_001():
    p1 = _at(_noise(0.5, 0.601, 0.15, 175001, 'bandpass', 2200.0), 0.0, 0.85)
    p2 = _at(_sweep('sine', 400.0, 2000.0, 0.5, 0.2, 0.2), 0.0, 0.85)
    p3 = _tticks('sine', 0.08, 0.001, [(0.262, 6922.0, 0.176), (0.271, 7004.0, 0.158), (0.334, 4959.0, 0.162), (0.502, 4442.0, 0.182), (0.507, 5798.0, 0.182), (0.529, 6740.0, 0.168), (0.534, 4840.0, 0.126), (0.561, 7919.0, 0.192), (0.67, 7220.0, 0.2), (0.716, 6054.0, 0.108)], 0.85)
    return _finalize(_mix(p1, p2, p3))
def anim_foot_plant_lock_001():
    p1 = _at(_sweep('sine', 100.0, 50.0, 0.1, 0.608, 0.001), 0.0, 0.15)
    p2 = _at(_noise(0.04, 0.487, 0.001, 176002, 'lowpass', 700.0), 0.0, 0.15)
    p3 = _at(_tone('sine', 1800.0, 0.04, 0.243, 0.0005), 0.03, 0.15)
    p4 = _at(_noise(0.01, 0.365, 0.0005, 176004, 'highpass', 3500.0), 0.03, 0.15)
    return _finalize(_mix(p1, p2, p3, p4))
def anim_hand_grip_servo_001():
    p1 = _tticks('sawtooth', 0.06, 0.003, [(0.0, 220.0, 0.106), (0.07, 260.0, 0.106), (0.14, 300.0, 0.106), (0.21, 340.0, 0.106), (0.28, 380.0, 0.106), (0.35, 420.0, 0.106)], 0.55)
    p2 = _at(_noise(0.4, 0.071, 0.02, 177002, 'bandpass', 1800.0), 0.0, 0.55)
    p3 = _at(_noise(0.015, 0.353, 0.0005, 177003, 'highpass', 3000.0), 0.45, 0.55)
    p4 = _at(_sweep('triangle', 500.0, 350.0, 0.05, 0.212, 0.001), 0.45, 0.55)
    return _finalize(_mix(p1, p2, p3, p4))
def anim_expression_morph_001():
    p1 = _at(_sweep('sine', 300.0, 500.0, 0.3, 0.551, 0.05), 0.0, 0.7)
    p2 = _at(_sweep('sine', 500.0, 260.0, 0.35, 0.441, 0.05), 0.3, 0.7)
    p3 = _at(_noise(0.6, 0.176, 0.2, 178003, 'bandpass', 900.0), 0.0, 0.7)
    return _finalize(_mix(p1, p2, p3))
def anim_tpose_calibrate_001():
    p1 = _at(_tone('sine', 262.0, 0.5, 0.501, 0.005), 0.0, 1.0)
    p2 = _at(_tone('sine', 330.0, 0.5, 0.501, 0.005), 0.15, 1.0)
    p3 = _at(_tone('sine', 392.0, 0.5, 0.501, 0.005), 0.3, 1.0)
    p4 = _at(_tone('sine', 523.0, 0.5, 0.501, 0.005), 0.45, 1.0)
    p5 = _at(_tone('sine', 1046.0, 0.5, 0.15, 0.01), 0.45, 1.0)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def anim_physics_bake_001():
    p1 = _tticks('sine', 0.02, 0.0005, [(0.0, 500.0, 0.167), (0.15, 666.0, 0.184), (0.277, 833.0, 0.201), (0.386, 1000.0, 0.217), (0.478, 1166.0, 0.234), (0.556, 1333.0, 0.251), (0.623, 1500.0, 0.268), (0.679, 1666.0, 0.284), (0.728, 1833.0, 0.301), (0.768, 2000.0, 0.318), (0.803, 2166.0, 0.335), (0.833, 2333.0, 0.351), (0.858, 2500.0, 0.368), (0.879, 2666.0, 0.385), (0.897, 2833.0, 0.401), (0.913, 3000.0, 0.418)], 1.46)
    p2 = _at(_tone('sine', 2093.0, 0.5, 0.279, 0.002), 0.913, 1.46)
    p3 = _at(_tone('sine', 5776.679999999999, 0.25, 0.084, 0.002), 0.913, 1.46)
    p4 = _at(_tone('sine', 3136.0, 0.4, 0.139, 0.002), 0.913, 1.46)
    return _finalize(_mix(p1, p2, p3, p4))
def anim_frame_step_tick_001():
    p1 = _nticks('bandpass', 0.01, 0.0005, 181060, [(0.0, 2500.0, 0.762), (0.18, 2800.0, 0.704), (0.36, 3100.0, 0.647), (0.54, 3400.0, 0.59), (0.72, 2500.0, 0.533), (0.9, 2800.0, 0.476)], 0.96)
    p2 = _tticks('triangle', 0.01, 0.0005, [(0.0, 1200.0, 0.381), (0.18, 1200.0, 0.381), (0.36, 1200.0, 0.381), (0.54, 1200.0, 0.381), (0.72, 1200.0, 0.381), (0.9, 1200.0, 0.381)], 0.96)
    return _finalize(_mix(p1, p2))
def anim_capture_jitter_001():
    p1 = _tticks('sawtooth', 0.04, 0.001, [(0.017, 614.0, 0.43), (0.204, 2325.0, 0.455), (0.238, 1625.0, 0.546), (0.254, 998.0, 0.404), (0.279, 2800.0, 0.421), (0.296, 1698.0, 0.293), (0.32, 906.0, 0.321), (0.349, 431.0, 0.484), (0.39, 2694.0, 0.313), (0.404, 1980.0, 0.418), (0.41, 1601.0, 0.35), (0.493, 2691.0, 0.464), (0.498, 1533.0, 0.418), (0.614, 2809.0, 0.566)], 0.75)
    p2 = _at(_noise(0.7, 0.284, 0.05, 182002, 'highpass', 5000.0), 0.0, 0.75)
    return _finalize(_mix(p1, p2))
def anim_render_complete_chime_001():
    p1 = _at(_tone('sine', 784.0, 0.6, 0.408, 0.002), 0.0, 1.05)
    p2 = _at(_tone('sine', 2163.8399999999997, 0.3, 0.122, 0.002), 0.0, 1.05)
    p3 = _at(_tone('sine', 988.0, 0.6, 0.408, 0.002), 0.15, 1.05)
    p4 = _at(_tone('sine', 2726.8799999999997, 0.3, 0.122, 0.002), 0.15, 1.05)
    p5 = _at(_tone('sine', 1319.0, 0.7, 0.408, 0.002), 0.3, 1.05)
    p6 = _at(_tone('sine', 3640.4399999999996, 0.35, 0.122, 0.002), 0.3, 1.05)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def anim_hit_react_stagger_001():
    p1 = _at(_sweep('sine', 120.0, 50.0, 0.12, 0.55, 0.002), 0.0, 0.8)
    p2 = _at(_noise(0.05, 0.4, 0.001, 184002, 'lowpass', 600.0), 0.0, 0.8)
    p3 = _at(_noise(0.25, 0.2, 0.03, 184003, 'bandpass', 1800.0), 0.02, 0.8)
    p4 = _tticks('triangle', 0.05, 0.001, [(0.3, 200.0, 0.3), (0.5, 190.0, 0.25), (0.7, 180.0, 0.2)], 0.8)
    p5 = _nticks('lowpass', 0.04, 0.001, 184300, [(0.3, 600.0, 0.2), (0.5, 600.0, 0.15), (0.7, 600.0, 0.12)], 0.8)
    return _finalize(_mix(p1, p2, p3, p4, p5))

OFFICIAL_PRESETS_MOCAP = {
    'anim-sensor-suit-calibrate-001': anim_sensor_suit_calibrate_001,
    'anim-marker-track-lock-001': anim_marker_track_lock_001,
    'anim-capture-start-countdown-001': anim_capture_start_countdown_001,
    'anim-capture-stop-001': anim_capture_stop_001,
    'anim-keyframe-set-001': anim_keyframe_set_001,
    'anim-keyframe-scrub-001': anim_keyframe_scrub_001,
    'anim-joint-ik-snap-001': anim_joint_ik_snap_001,
    'anim-ragdoll-collapse-001': anim_ragdoll_collapse_001,
    'anim-rig-bind-weld-001': anim_rig_bind_weld_001,
    'anim-blend-crossfade-001': anim_blend_crossfade_001,
    'anim-loop-wrap-rewind-001': anim_loop_wrap_rewind_001,
    'anim-retarget-sweep-001': anim_retarget_sweep_001,
    'anim-pose-freeze-hold-001': anim_pose_freeze_hold_001,
    'anim-pose-mirror-flip-001': anim_pose_mirror_flip_001,
    'anim-onion-skin-ghost-001': anim_onion_skin_ghost_001,
    'anim-motion-trail-whoosh-001': anim_motion_trail_whoosh_001,
    'anim-foot-plant-lock-001': anim_foot_plant_lock_001,
    'anim-hand-grip-servo-001': anim_hand_grip_servo_001,
    'anim-expression-morph-001': anim_expression_morph_001,
    'anim-tpose-calibrate-001': anim_tpose_calibrate_001,
    'anim-physics-bake-001': anim_physics_bake_001,
    'anim-frame-step-tick-001': anim_frame_step_tick_001,
    'anim-capture-jitter-001': anim_capture_jitter_001,
    'anim-render-complete-chime-001': anim_render_complete_chime_001,
    'anim-hit-react-stagger-001': anim_hit_react_stagger_001,
}
