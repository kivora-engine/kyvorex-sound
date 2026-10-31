"""Mission 15 - Percussion & Musical Textures (25 sounds)."""
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


def perc_sub_kick_808_001():
    p1 = _at(_sweep('sine', 140.0, 38.0, 0.8, 0.569, 0.002), 0.0, 0.85)
    p2 = _at(_noise(0.01, 0.214, 0.0005, 150002, 'lowpass', 2000.0), 0.0, 0.85)
    return _finalize(_mix(p1, p2))
def perc_rimshot_crack_001():
    p1 = _at(_noise(0.012, 0.308, 0.0005, 151001, 'highpass', 3000.0), 0.0, 0.15)
    p2 = _at(_sweep('sine', 1750.0, 1650.0, 0.06, 0.247, 0.0005), 0.0, 0.15)
    p3 = _at(_sweep('triangle', 520.0, 480.0, 0.1, 0.185, 0.0005), 0.0, 0.15)
    p4 = _at(_noise(0.06, 0.123, 0.001, 151004, 'bandpass', 1800.0), 0.0, 0.15)
    return _finalize(_mix(p1, p2, p3, p4))
def perc_hihat_pair_001():
    p1 = _at(_noise(0.04, 0.4, 0.0005, 152001, 'highpass', 8000.0), 0.0, 0.8)
    p2 = _at(_noise(0.02, 0.3, 0.0005, 152002, 'bandpass', 10000.0), 0.0, 0.8)
    p3 = _at(_noise(0.45, 0.4, 0.001, 152003, 'highpass', 7000.0), 0.3, 0.8)
    p4 = _at(_noise(0.45, 0.25, 0.001, 152004, 'bandpass', 9500.0), 0.3, 0.8)
    return _finalize(_mix(p1, p2, p3, p4))
def perc_clap_stack_001():
    p1 = _nticks('bandpass', 0.02, 0.0005, 153060, [(0.0, 1500.0, 1.0), (0.012, 1700.0, 1.0), (0.025, 1400.0, 1.0), (0.04, 1600.0, 1.0)], 0.34)
    p2 = _at(_noise(0.25, 0.934, 0.002, 153002, 'bandpass', 1300.0), 0.04, 0.34)
    return _finalize(_mix(p1, p2))
def perc_tom_fill_descend_001():
    p1 = _at(_sweep('sine', 364.0, 260.0, 0.3, 0.5, 0.001), 0.0, 0.77)
    p2 = _at(_sweep('sine', 294.0, 210.0, 0.3, 0.5, 0.001), 0.14, 0.77)
    p3 = _at(_sweep('sine', 237.99999999999997, 170.0, 0.3, 0.5, 0.001), 0.28, 0.77)
    p4 = _at(_sweep('sine', 182.0, 130.0, 0.3, 0.5, 0.001), 0.42, 0.77)
    p5 = _nticks('lowpass', 0.01, 0.0005, 154300, [(0.0, 1500.0, 0.3), (0.14, 1500.0, 0.3), (0.28, 1500.0, 0.3), (0.42, 1500.0, 0.3)], 0.77)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def perc_woodblock_duo_001():
    p1 = _at(_sweep('triangle', 1200.0, 1150.0, 0.06, 0.5, 0.0005), 0.0, 0.32)
    p2 = _at(_tone('sine', 2400.0, 0.03, 0.2, 0.0005), 0.0, 0.32)
    p3 = _at(_sweep('triangle', 860.0, 820.0, 0.07, 0.5, 0.0005), 0.2, 0.32)
    p4 = _at(_tone('sine', 1720.0, 0.03, 0.2, 0.0005), 0.2, 0.32)
    return _finalize(_mix(p1, p2, p3, p4))
def perc_cowbell_clank_001():
    p1 = _at(_tone('square', 540.0, 0.4, 0.225, 0.001), 0.0, 0.45)
    p2 = _at(_tone('square', 810.0, 0.4, 0.225, 0.001), 0.0, 0.45)
    p3 = _at(_noise(0.01, 0.27, 0.0005, 156003, 'highpass', 3000.0), 0.0, 0.45)
    return _finalize(_mix(p1, p2, p3))
def perc_conga_slap_001():
    p1 = _at(_sweep('sine', 380.0, 250.0, 0.12, 0.5, 0.001), 0.0, 0.66)
    p2 = _at(_noise(0.015, 0.4, 0.0005, 157002, 'bandpass', 2500.0), 0.0, 0.66)
    p3 = _at(_sweep('sine', 220.0, 170.0, 0.4, 0.35, 0.001), 0.01, 0.66)
    p4 = _at(_sweep('sine', 300.0, 200.0, 0.1, 0.3, 0.001), 0.3, 0.66)
    p5 = _at(_sweep('sine', 190.0, 150.0, 0.3, 0.2, 0.001), 0.31, 0.66)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def perc_shaker_pattern_001():
    p1 = _nticks('highpass', 0.06, 0.015, 158060, [(0.0, 6500.0, 0.432), (0.15, 6500.0, 0.216), (0.3, 6500.0, 0.302), (0.45, 6500.0, 0.216), (0.6, 6500.0, 0.432), (0.75, 6500.0, 0.216), (0.9, 6500.0, 0.302), (1.05, 6500.0, 0.216)], 1.16)
    return _finalize(_mix(p1))
def perc_tambourine_shake_001():
    p1 = _nticks('highpass', 0.04, 0.001, 159060, [(0.034, 6307.0, 0.444), (0.05, 7719.0, 0.35), (0.162, 8690.0, 0.353), (0.202, 8552.0, 0.374), (0.255, 9047.0, 0.409), (0.394, 7233.0, 0.443), (0.432, 5709.0, 0.367), (0.461, 7389.0, 0.428), (0.492, 7392.0, 0.257), (0.501, 9161.0, 0.426), (0.521, 9329.0, 0.29), (0.546, 6471.0, 0.281), (0.548, 6330.0, 0.455), (0.552, 7340.0, 0.386), (0.671, 5985.0, 0.399), (0.674, 7610.0, 0.31), (0.699, 7075.0, 0.412), (0.783, 8070.0, 0.415)], 0.87)
    p2 = _tticks('sine', 0.08, 0.001, [(0.072, 6645.0, 0.118), (0.241, 7790.0, 0.134), (0.246, 8872.0, 0.096), (0.294, 6951.0, 0.131), (0.301, 8194.0, 0.137), (0.338, 8559.0, 0.102), (0.345, 6266.0, 0.092), (0.346, 6803.0, 0.082), (0.349, 6527.0, 0.131), (0.561, 6676.0, 0.099)], 0.87)
    p3 = _at(_sweep('sine', 300.0, 200.0, 0.08, 0.458, 0.001), 0.0, 0.87)
    return _finalize(_mix(p1, p2, p3))
def perc_gong_partials_001():
    p1 = _at(_tone('sine', 130.0, 2.0, 0.185, 0.01), 0.0, 2.05)
    p2 = _at(_tone('sine', 191.1, 1.72, 0.123, 0.01), 0.0, 2.05)
    p3 = _at(_tone('sine', 271.7, 1.44, 0.099, 0.01), 0.0, 2.05)
    p4 = _at(_tone('sine', 332.8, 1.16, 0.074, 0.01), 0.0, 2.05)
    p5 = _at(_tone('sine', 408.2, 0.8799999999999999, 0.055, 0.01), 0.0, 2.05)
    p6 = _at(_tone('sine', 131.0, 2.0, 0.092, 0.01), 0.0, 2.05)
    p7 = _at(_noise(1.5, 0.062, 0.05, 160007, 'bandpass', 900.0), 0.0, 2.05)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7))
def perc_metal_pipe_ring_001():
    p1 = _at(_tone('sine', 410.0, 1.0, 0.258, 0.001), 0.0, 1.05)
    p2 = _at(_tone('sine', 1131.6, 0.65, 0.172, 0.001), 0.0, 1.05)
    p3 = _at(_tone('sine', 2214.0, 0.4, 0.103, 0.001), 0.0, 1.05)
    p4 = _at(_tone('sine', 3661.2999999999997, 0.25, 0.06, 0.001), 0.0, 1.05)
    p5 = _at(_noise(0.01, 0.344, 0.0005, 161005, 'highpass', 3000.0), 0.0, 1.05)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def perc_singing_bowl_001():
    p1 = _at(_tone('sine', 440.0, 1.9, 0.192, 0.01), 0.0, 1.95)
    p2 = _at(_tone('sine', 443.0, 1.9, 0.192, 0.01), 0.0, 1.95)
    p3 = _at(_tone('sine', 1190.0, 1.6, 0.077, 0.01), 0.0, 1.95)
    p4 = _at(_tone('sine', 1197.0, 1.6, 0.077, 0.01), 0.0, 1.95)
    p5 = _at(_tone('sine', 2230.0, 1.2, 0.031, 0.01), 0.0, 1.95)
    p6 = _at(_noise(0.02, 0.154, 0.0005, 162006, 'bandpass', 1500.0), 0.0, 1.95)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6))
def perc_kalimba_tine_001():
    p1 = _at(_tone('sine', 523.0, 0.9, 0.35, 0.001), 0.0, 0.95)
    p2 = _at(_tone('sine', 3280.0, 0.15, 0.1, 0.0005), 0.0, 0.95)
    p3 = _at(_tone('sine', 1046.0, 0.4, 0.1, 0.001), 0.0, 0.95)
    p4 = _at(_noise(0.008, 0.25, 0.0005, 163004, 'bandpass', 3500.0), 0.0, 0.95)
    p5 = _at(_tone('sine', 130.0, 0.05, 0.15, 0.001), 0.0, 0.95)
    return _finalize(_mix(p1, p2, p3, p4, p5))
def perc_taiko_deep_hit_001():
    p1 = _at(_sweep('sine', 160.0, 48.0, 1.2, 0.483, 0.002), 0.0, 1.25)
    p2 = _at(_noise(0.1, 0.345, 0.001, 164002, 'lowpass', 500.0), 0.0, 1.25)
    p3 = _at(_noise(0.5, 0.138, 0.005, 164003, 'bandpass', 300.0), 0.0, 1.25)
    p4 = _at(_tone('sine', 95.0, 0.9, 0.138, 0.002), 0.0, 1.25)
    return _finalize(_mix(p1, p2, p3, p4))
def perc_electro_tom_zap_001():
    p1 = _at(_sweep('sine', 600.0, 80.0, 0.4, 0.442, 0.001), 0.0, 0.45)
    p2 = _at(_sweep('square', 300.0, 60.0, 0.15, 0.133, 0.001), 0.0, 0.45)
    p3 = _at(_noise(0.01, 0.265, 0.0005, 165003, 'highpass', 3000.0), 0.0, 0.45)
    return _finalize(_mix(p1, p2, p3))
def perc_chip_snare_001():
    p1 = _at(_sweep('square', 880.0, 200.0, 0.08, 0.223, 0.0005), 0.0, 0.13)
    p2 = _nticks('highpass', 0.015, 0.0005, 166120, [(0.0, 2500.0, 0.297), (0.01, 2800.0, 0.26), (0.02, 3100.0, 0.223), (0.03, 3400.0, 0.186), (0.04, 3700.0, 0.149), (0.05, 4000.0, 0.111)], 0.13)
    return _finalize(_mix(p1, p2))
def perc_reverse_swell_riser_001():
    p1 = _at(_noise(1.4, 0.675, 1.2, 167001, 'bandpass', 3000.0), 0.0, 1.46)
    p2 = _at(_sweep('sine', 200.0, 1600.0, 1.3, 0.162, 1.0), 0.0, 1.46)
    p3 = _at(_noise(0.015, 0.675, 0.0005, 167003, 'highpass', 3000.0), 1.4, 1.46)
    return _finalize(_mix(p1, p2, p3))
def perc_metronome_tick_tock_001():
    p1 = _at(_sweep('triangle', 1500.0, 1400.0, 0.025, 0.5, 0.0005), 0.0, 0.58)
    p2 = _at(_sweep('triangle', 1000.0, 950.0, 0.03, 0.4, 0.0005), 0.5, 0.58)
    p3 = _nticks('bandpass', 0.008, 0.0005, 168180, [(0.0, 2500.0, 0.3), (0.5, 2000.0, 0.25)], 0.58)
    return _finalize(_mix(p1, p2, p3))
def perc_march_snare_pattern_001():
    p1 = _nticks('bandpass', 0.06, 0.001, 169060, [(0.0, 1900.0, 0.663), (0.15, 1900.0, 0.332), (0.3, 1900.0, 0.398), (0.45, 1900.0, 0.663), (0.6, 1900.0, 0.332), (0.75, 1900.0, 0.398), (0.9, 1900.0, 0.663), (1.05, 1900.0, 0.398), (1.2, 1900.0, 0.729)], 1.31)
    p2 = _tticks('sine', 0.05, 0.001, [(0.0, 200.0, 0.332), (0.15, 200.0, 0.166), (0.3, 200.0, 0.199), (0.45, 200.0, 0.332), (0.6, 200.0, 0.166), (0.75, 200.0, 0.199), (0.9, 200.0, 0.332), (1.05, 200.0, 0.199), (1.2, 200.0, 0.365)], 1.31)
    return _finalize(_mix(p1, p2))
def perc_heartbeat_drum_001():
    p1 = _at(_sweep('sine', 110.0, 50.0, 0.18, 0.6, 0.002), 0.0, 1.1)
    p2 = _at(_sweep('sine', 95.0, 45.0, 0.15, 0.45, 0.002), 0.3, 1.1)
    p3 = _at(_sweep('sine', 110.0, 50.0, 0.18, 0.35, 0.002), 0.6, 1.1)
    p4 = _at(_sweep('sine', 95.0, 45.0, 0.15, 0.25, 0.002), 0.9, 1.1)
    return _finalize(_mix(p1, p2, p3, p4))
def perc_bass_pulse_sixteenths_001():
    p1 = _at(_tone('sine', 55.0, 0.12, 0.613, 0.003), 0.0, 1.22)
    p2 = _at(_tone('sine', 55.0, 0.12, 0.459, 0.003), 0.15, 1.22)
    p3 = _at(_tone('sine', 73.0, 0.12, 0.459, 0.003), 0.3, 1.22)
    p4 = _at(_tone('sine', 55.0, 0.12, 0.459, 0.003), 0.45, 1.22)
    p5 = _at(_tone('sine', 82.0, 0.12, 0.613, 0.003), 0.6, 1.22)
    p6 = _at(_tone('sine', 55.0, 0.12, 0.459, 0.003), 0.75, 1.22)
    p7 = _at(_tone('sine', 73.0, 0.12, 0.459, 0.003), 0.9, 1.22)
    p8 = _at(_tone('sine', 98.0, 0.12, 0.459, 0.003), 1.05, 1.22)
    p9 = _at(_tone('sawtooth', 55.0, 0.1, 0.123, 0.003), 0.0, 1.22)
    p10 = _at(_tone('sawtooth', 55.0, 0.1, 0.123, 0.003), 0.15, 1.22)
    p11 = _at(_tone('sawtooth', 73.0, 0.1, 0.123, 0.003), 0.3, 1.22)
    p12 = _at(_tone('sawtooth', 55.0, 0.1, 0.123, 0.003), 0.45, 1.22)
    p13 = _at(_tone('sawtooth', 82.0, 0.1, 0.123, 0.003), 0.6, 1.22)
    p14 = _at(_tone('sawtooth', 55.0, 0.1, 0.123, 0.003), 0.75, 1.22)
    p15 = _at(_tone('sawtooth', 73.0, 0.1, 0.123, 0.003), 0.9, 1.22)
    p16 = _at(_tone('sawtooth', 98.0, 0.1, 0.123, 0.003), 1.05, 1.22)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11, p12, p13, p14, p15, p16))
def perc_glitch_stutter_hit_001():
    p1 = _tticks('triangle', 0.05, 0.0005, [(0.0, 500.0, 0.4), (0.2, 500.0, 0.4), (0.34, 500.0, 0.4), (0.438, 500.0, 0.4), (0.507, 500.0, 0.4), (0.555, 500.0, 0.4), (0.588, 500.0, 0.4)], 0.69)
    p2 = _nticks('highpass', 0.01, 0.0005, 172120, [(0.0, 4000.0, 0.3), (0.2, 4000.0, 0.3), (0.34, 4000.0, 0.3), (0.438, 4000.0, 0.3), (0.507, 4000.0, 0.3), (0.555, 4000.0, 0.3), (0.588, 4000.0, 0.3)], 0.69)
    return _finalize(_mix(p1, p2))
def perc_transition_boom_drop_001():
    p1 = _at(_noise(0.3, 0.093, 0.25, 173001, 'highpass', 5000.0), 0.0, 1.75)
    p2 = _at(_sweep('sine', 90.0, 28.0, 1.1, 0.497, 0.003), 0.3, 1.75)
    p3 = _at(_noise(0.4, 0.311, 0.002, 173003, 'lowpass', 400.0), 0.3, 1.75)
    p4 = _at(_noise(1.4, 0.186, 0.01, 173004, 'bandpass', 500.0), 0.3, 1.75)
    return _finalize(_mix(p1, p2, p3, p4))
def perc_tin_shimmer_wash_001():
    p1 = _at(_tone('sine', 2310.0, 1.8, 0.133, 0.01), 0.0, 1.95)
    p2 = _at(_tone('sine', 2890.0, 1.8, 0.133, 0.01), 0.02, 1.95)
    p3 = _at(_tone('sine', 3470.0, 1.8, 0.133, 0.01), 0.04, 1.95)
    p4 = _at(_tone('sine', 4120.0, 1.8, 0.133, 0.01), 0.06, 1.95)
    p5 = _at(_tone('sine', 5330.0, 1.8, 0.133, 0.01), 0.08, 1.95)
    p6 = _at(_tone('sine', 6710.0, 1.8, 0.133, 0.01), 0.1, 1.95)
    p7 = _tticks('sine', 0.1, 0.001, [(0.16, 8443.0, 0.109), (0.165, 7723.0, 0.101), (0.228, 4598.0, 0.123), (0.484, 4595.0, 0.071), (0.506, 8328.0, 0.086), (0.571, 5628.0, 0.114), (0.669, 5587.0, 0.085), (1.165, 7070.0, 0.09), (1.189, 7397.0, 0.143), (1.233, 6828.0, 0.09), (1.267, 6405.0, 0.104), (1.278, 6588.0, 0.126), (1.34, 7708.0, 0.129), (1.446, 4644.0, 0.133)], 1.95)
    p8 = _at(_noise(1.8, 0.083, 0.1, 174008, 'highpass', 8000.0), 0.0, 1.95)
    return _finalize(_mix(p1, p2, p3, p4, p5, p6, p7, p8))

OFFICIAL_PRESETS_PERCUSSION = {
    'perc-sub-kick-808-001': perc_sub_kick_808_001,
    'perc-rimshot-crack-001': perc_rimshot_crack_001,
    'perc-hihat-pair-001': perc_hihat_pair_001,
    'perc-clap-stack-001': perc_clap_stack_001,
    'perc-tom-fill-descend-001': perc_tom_fill_descend_001,
    'perc-woodblock-duo-001': perc_woodblock_duo_001,
    'perc-cowbell-clank-001': perc_cowbell_clank_001,
    'perc-conga-slap-001': perc_conga_slap_001,
    'perc-shaker-pattern-001': perc_shaker_pattern_001,
    'perc-tambourine-shake-001': perc_tambourine_shake_001,
    'perc-gong-partials-001': perc_gong_partials_001,
    'perc-metal-pipe-ring-001': perc_metal_pipe_ring_001,
    'perc-singing-bowl-001': perc_singing_bowl_001,
    'perc-kalimba-tine-001': perc_kalimba_tine_001,
    'perc-taiko-deep-hit-001': perc_taiko_deep_hit_001,
    'perc-electro-tom-zap-001': perc_electro_tom_zap_001,
    'perc-chip-snare-001': perc_chip_snare_001,
    'perc-reverse-swell-riser-001': perc_reverse_swell_riser_001,
    'perc-metronome-tick-tock-001': perc_metronome_tick_tock_001,
    'perc-march-snare-pattern-001': perc_march_snare_pattern_001,
    'perc-heartbeat-drum-001': perc_heartbeat_drum_001,
    'perc-bass-pulse-sixteenths-001': perc_bass_pulse_sixteenths_001,
    'perc-glitch-stutter-hit-001': perc_glitch_stutter_hit_001,
    'perc-transition-boom-drop-001': perc_transition_boom_drop_001,
    'perc-tin-shimmer-wash-001': perc_tin_shimmer_wash_001,
}
