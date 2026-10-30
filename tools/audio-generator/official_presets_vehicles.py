"""Mission 7 - Mechanical Sports & Vehicles (25 sounds)."""
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

def veh_engine_turbo_001():
    sw = _at(_sweep('sawtooth', 100.0, 600.0, 0.80, 0.35, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))
def veh_gear_shift_heavy_001():
    nz = _at(_noise(0.10, 0.40, 0.001, seed=2600), 0.00, 0.15)
    a = _at(_tone('square', 100.0, 0.10, 0.35, 0.002), 0.00, 0.15)
    return _finalize(_mix(nz, a))
def veh_gear_shift_light_001():
    a = _at(_tone('triangle', 300.0, 0.05, 0.25, 0.001), 0.00, 0.10)
    return _finalize(_mix(a))
def veh_brake_squeal_001():
    nz = _at(_noise(0.50, 0.30, 0.050, seed=2601), 0.00, 0.60)
    high = _at(_tone('sine', 2000.0, 0.40, 0.15, 0.050), 0.00, 0.60)
    return _finalize(_mix(nz, high))
def veh_exhaust_burst_001():
    nz = _at(_noise(0.20, 0.50, 0.001, seed=2602), 0.00, 0.25)
    return _finalize(_mix(nz))
def veh_engine_start_futuristic_001():
    sw = _at(_sweep('sine', 50.0, 400.0, 1.20, 0.30, 0.100), 0.00, 1.30)
    return _finalize(_mix(sw))
def veh_engine_stop_futuristic_001():
    sw = _at(_sweep('sine', 400.0, 50.0, 1.20, 0.30, 0.100), 0.00, 1.30)
    return _finalize(_mix(sw))
def veh_drivetrain_engage_001():
    nz = _at(_noise(0.20, 0.35, 0.005, seed=2603), 0.00, 0.25)
    low = _at(_sweep('sawtooth', 80.0, 100.0, 0.20, 0.30, 0.005), 0.00, 0.25)
    return _finalize(_mix(nz, low))
def veh_suspension_bounce_001():
    sw = _at(_sweep('sine', 150.0, 80.0, 0.30, 0.35, 0.010), 0.00, 0.40)
    return _finalize(_mix(sw))
def veh_tire_screech_001():
    nz = _at(_noise(0.80, 0.35, 0.050, seed=2604), 0.00, 0.90)
    return _finalize(_mix(nz))
def veh_nitro_boost_001():
    sw = _at(_sweep('square', 200.0, 800.0, 0.60, 0.40, 0.020), 0.00, 0.70)
    return _finalize(_mix(sw))
def veh_racing_pass_by_001():
    sw = _at(_sweep('sawtooth', 400.0, 100.0, 0.80, 0.35, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))
def veh_mechanical_whine_001():
    sw = _at(_sweep('sine', 800.0, 1200.0, 0.60, 0.20, 0.020), 0.00, 0.70)
    return _finalize(_mix(sw))
def veh_hydraulic_lift_001():
    sw = _at(_sweep('sawtooth', 100.0, 200.0, 0.60, 0.30, 0.050), 0.00, 0.70)
    return _finalize(_mix(sw))
def veh_hydraulic_lower_001():
    sw = _at(_sweep('sawtooth', 200.0, 100.0, 0.60, 0.30, 0.050), 0.00, 0.70)
    return _finalize(_mix(sw))
def veh_wheel_spin_001():
    nz = _at(_noise(0.60, 0.25, 0.020, seed=2605), 0.00, 0.70)
    return _finalize(_mix(nz))
def veh_crash_metal_impact_001():
    nz = _at(_noise(0.30, 0.60, 0.001, seed=2606), 0.00, 0.40)
    low = _at(_sweep('sine', 80.0, 40.0, 0.30, 0.40, 0.005), 0.00, 0.40)
    return _finalize(_mix(nz, low))
def veh_fuel_pump_001():
    sw = _at(_sweep('sine', 200.0, 300.0, 0.60, 0.20, 0.050), 0.00, 0.70)
    return _finalize(_mix(sw))
def veh_speedometer_ping_001():
    a = _at(_tone('square', 2000.0, 0.02, 0.15, 0.001), 0.00, 0.05)
    return _finalize(_mix(a))
def veh_engine_rev_001():
    sw = _at(_sweep('sawtooth', 100.0, 200.0, 0.50, 0.35, 0.020), 0.00, 0.60)
    return _finalize(_mix(sw))
def veh_gear_grind_001():
    nz = _at(_noise(0.30, 0.40, 0.005, seed=2607), 0.00, 0.40)
    return _finalize(_mix(nz))
def veh_futuristic_hover_001():
    sw = _at(_sweep('sine', 80.0, 120.0, 1.00, 0.25, 0.100), 0.00, 1.10)
    return _finalize(_mix(sw))
def veh_ignition_spark_001():
    a = _at(_tone('square', 1500.0, 0.02, 0.30, 0.001), 0.00, 0.05)
    return _finalize(_mix(a))
def veh_cockpit_ambience_001():
    nz = _at(_noise(1.50, 0.15, 0.100, seed=2608), 0.00, 1.60)
    return _finalize(_mix(nz))
def veh_engine_cooling_001():
    sw = _at(_sweep('sine', 200.0, 150.0, 0.80, 0.20, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))

OFFICIAL_PRESETS_VEHICLES = {
    'veh-engine-turbo-001': veh_engine_turbo_001, 'veh-gear-shift-heavy-001': veh_gear_shift_heavy_001,
    'veh-gear-shift-light-001': veh_gear_shift_light_001, 'veh-brake-squeal-001': veh_brake_squeal_001,
    'veh-exhaust-burst-001': veh_exhaust_burst_001, 'veh-engine-start-futuristic-001': veh_engine_start_futuristic_001,
    'veh-engine-stop-futuristic-001': veh_engine_stop_futuristic_001, 'veh-drivetrain-engage-001': veh_drivetrain_engage_001,
    'veh-suspension-bounce-001': veh_suspension_bounce_001, 'veh-tire-screech-001': veh_tire_screech_001,
    'veh-nitro-boost-001': veh_nitro_boost_001, 'veh-racing-pass-by-001': veh_racing_pass_by_001,
    'veh-mechanical-whine-001': veh_mechanical_whine_001, 'veh-hydraulic-lift-001': veh_hydraulic_lift_001,
    'veh-hydraulic-lower-001': veh_hydraulic_lower_001, 'veh-wheel-spin-001': veh_wheel_spin_001,
    'veh-crash-metal-impact-001': veh_crash_metal_impact_001, 'veh-fuel-pump-001': veh_fuel_pump_001,
    'veh-speedometer-ping-001': veh_speedometer_ping_001, 'veh-engine-rev-001': veh_engine_rev_001,
    'veh-gear-grind-001': veh_gear_grind_001, 'veh-futuristic-hover-001': veh_futuristic_hover_001,
    'veh-ignition-spark-001': veh_ignition_spark_001, 'veh-cockpit-ambience-001': veh_cockpit_ambience_001,
    'veh-engine-cooling-001': veh_engine_cooling_001,
}