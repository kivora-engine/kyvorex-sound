"""Mission 10 - Rare & Specialized Events (25 sounds)."""
import math
from synthesis import sine, square, triangle, sawtooth, white_noise, DEFAULT_SAMPLE_RATE

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

def _noise(dur, amplitude, attack, seed=1):
    n = int(dur * SR)
    if n <= 0: return []
    env = _env_exp(n, attack)
    raw = white_noise(dur, SR, amplitude, seed=seed)
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

def _finalize(samples):
    peak = max((abs(s) for s in samples), default=0.0)
    if peak == 0.0: return samples
    target = 0.85
    factor = target / peak if peak > target else 1.0
    return [s * factor for s in samples]

def ancient_gear_turn_001():
    nz = _at(_noise(0.80, 0.30, 0.050, seed=1300), 0.00, 0.90)
    sw = _at(_sweep('sawtooth', 80.0, 100.0, 0.80, 0.25, 0.050), 0.00, 0.90)
    return _finalize(_mix(nz, sw))

def magical_trap_snap_001():
    a = _at(_tone('square', 600.0, 0.05, 0.35, 0.001), 0.00, 0.10)
    nz = _at(_noise(0.10, 0.25, 0.001, seed=1301), 0.00, 0.10)
    return _finalize(_mix(a, nz))

def zero_gravity_float_001():
    sw = _at(_sweep('sine', 400.0, 200.0, 1.20, 0.25, 0.200), 0.00, 1.30)
    return _finalize(_mix(sw))

def time_loop_echo_001():
    a = _at(_tone('sine', 800.0, 0.10, 0.30, 0.002), 0.00, 0.60)
    b = _at(_tone('sine', 800.0, 0.10, 0.20, 0.002), 0.20, 0.60)
    c = _at(_tone('sine', 800.0, 0.10, 0.10, 0.002), 0.40, 0.60)
    return _finalize(_mix(a, b, c))

def artifact_discovery_001():
    parts = []
    for i in range(3): parts.append(_at(_tone('triangle', 523.25 + i*100, 0.15, 0.25, 0.005), i*0.12, 0.50))
    return _finalize(_mix(*parts))

def alien_flora_bloom_001():
    nz = _at(_noise(0.50, 0.20, 0.050, seed=1302), 0.00, 0.60)
    sw = _at(_sweep('sine', 600.0, 1200.0, 0.40, 0.20, 0.050), 0.00, 0.60)
    return _finalize(_mix(nz, sw))

def futuristic_surgery_001():
    sw = _at(_sweep('sawtooth', 1000.0, 1500.0, 0.60, 0.20, 0.010), 0.00, 0.70)
    return _finalize(_mix(sw))

def plasma_welding_001():
    nz = _at(_noise(0.40, 0.45, 0.010, seed=1303), 0.00, 0.50)
    return _finalize(_mix(nz))

def ion_thruster_ignite_001():
    sw = _at(_sweep('sine', 100.0, 400.0, 0.80, 0.40, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))

def cryo_pod_open_001():
    nz = _at(_noise(0.60, 0.35, 0.010, seed=1304), 0.00, 0.70)
    sw = _at(_sweep('sine', 400.0, 100.0, 0.50, 0.25, 0.010), 0.00, 0.70)
    return _finalize(_mix(nz, sw))

def cryo_pod_close_001():
    nz = _at(_noise(0.40, 0.30, 0.010, seed=1305), 0.00, 0.50)
    a = _at(_tone('sine', 80.0, 0.20, 0.40, 0.005), 0.30, 0.50)
    return _finalize(_mix(nz, a))

def sonic_screwdriver_001():
    sw = _at(_sweep('square', 1500.0, 2000.0, 0.40, 0.20, 0.010), 0.00, 0.50)
    return _finalize(_mix(sw))

def gravity_well_generate_001():
    sw = _at(_sweep('sine', 400.0, 50.0, 1.00, 0.40, 0.050), 0.00, 1.10)
    return _finalize(_mix(sw))

def space_station_alarm_001():
    parts = []
    for i in range(4): parts.append(_at(_tone('square', 800.0, 0.15, 0.25, 0.002), i*0.20, 0.80))
    return _finalize(_mix(*parts))

def meteor_shower_pass_001():
    nz = _at(_noise(1.20, 0.30, 0.100, seed=1306), 0.00, 1.30)
    return _finalize(_mix(nz))

def aura_reveal_001():
    sw = _at(_sweep('sine', 600.0, 1200.0, 0.80, 0.20, 0.100), 0.00, 0.90)
    return _finalize(_mix(sw))

def runic_translation_001():
    parts = []
    for i in range(5): parts.append(_at(_tone('triangle', 800.0 + i*50, 0.05, 0.15, 0.001), i*0.05, 0.30))
    return _finalize(_mix(*parts))

def dimensional_fold_001():
    nz = _at(_noise(0.60, 0.40, 0.020, seed=1307), 0.00, 0.70)
    sw = _at(_sweep('sawtooth', 800.0, 200.0, 0.60, 0.30, 0.020), 0.00, 0.70)
    return _finalize(_mix(nz, sw))

def elevator_mechanism_001():
    a = _at(_tone('sawtooth', 100.0, 0.60, 0.25, 0.020), 0.00, 0.70)
    return _finalize(_mix(a))

def trapdoor_trigger_001():
    nz = _at(_noise(0.10, 0.40, 0.001, seed=1308), 0.00, 0.15)
    a = _at(_tone('sine', 100.0, 0.10, 0.40, 0.002), 0.00, 0.15)
    return _finalize(_mix(nz, a))

def laser_grid_activate_001():
    sw = _at(_sweep('square', 400.0, 800.0, 0.50, 0.30, 0.010), 0.00, 0.60)
    return _finalize(_mix(sw))

def biometric_lock_001():
    a = _at(_tone('sine', 1000.0, 0.10, 0.30, 0.002), 0.00, 0.15)
    b = _at(_tone('sine', 1200.0, 0.15, 0.30, 0.002), 0.10, 0.15)
    return _finalize(_mix(a, b))

def black_hole_collapse_001():
    sw = _at(_sweep('sine', 200.0, 20.0, 1.50, 0.50, 0.100), 0.00, 1.60)
    return _finalize(_mix(sw))

def nebula_ambience_001():
    nz = _at(_noise(2.00, 0.20, 0.200, seed=1309), 0.00, 2.20)
    return _finalize(_mix(nz))

def alien_communication_001():
    parts = []
    for i in range(6): parts.append(_at(_tone('sine', 400.0 + i*150, 0.10, 0.20, 0.010), i*0.08, 0.50))
    return _finalize(_mix(*parts))

OFFICIAL_PRESETS_RARE = {
    'ancient-gear-turn-001': ancient_gear_turn_001, 'magical-trap-snap-001': magical_trap_snap_001,
    'zero-gravity-float-001': zero_gravity_float_001, 'time-loop-echo-001': time_loop_echo_001,
    'artifact-discovery-001': artifact_discovery_001, 'alien-flora-bloom-001': alien_flora_bloom_001,
    'futuristic-surgery-001': futuristic_surgery_001, 'plasma-welding-001': plasma_welding_001,
    'ion-thruster-ignite-001': ion_thruster_ignite_001, 'cryo-pod-open-001': cryo_pod_open_001,
    'cryo-pod-close-001': cryo_pod_close_001, 'sonic-screwdriver-001': sonic_screwdriver_001,
    'gravity-well-generate-001': gravity_well_generate_001, 'space-station-alarm-001': space_station_alarm_001,
    'meteor-shower-pass-001': meteor_shower_pass_001, 'aura-reveal-001': aura_reveal_001,
    'runic-translation-001': runic_translation_001, 'dimensional-fold-001': dimensional_fold_001,
    'elevator-mechanism-001': elevator_mechanism_001, 'trapdoor-trigger-001': trapdoor_trigger_001,
    'laser-grid-activate-001': laser_grid_activate_001, 'biometric-lock-001': biometric_lock_001,
    'black-hole-collapse-001': black_hole_collapse_001, 'nebula-ambience-001': nebula_ambience_001,
    'alien-communication-001': alien_communication_001,
}