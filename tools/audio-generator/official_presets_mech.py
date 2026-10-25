"""Mission 3 - Mechanical / Industrial (25 sounds)."""
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

def mech_gear_engage_001():
    a = _at(_tone('square', 200.0, 0.05, 0.30, 0.002), 0.00, 0.15)
    b = _at(_tone('square', 250.0, 0.05, 0.30, 0.002), 0.08, 0.15)
    return _finalize(_mix(a, b))
def mech_gear_grind_001():
    nz = _at(_noise(0.40, 0.30, 0.020, seed=800), 0.00, 0.50)
    sw = _at(_sweep('sawtooth', 100.0, 150.0, 0.40, 0.25, 0.020), 0.00, 0.50)
    return _finalize(_mix(nz, sw))
def mech_piston_pump_001():
    a = _at(_tone('sine', 80.0, 0.15, 0.40, 0.005), 0.00, 0.30)
    b = _at(_tone('sine', 80.0, 0.15, 0.40, 0.005), 0.15, 0.30)
    return _finalize(_mix(a, b))
def mech_hydraulic_press_001():
    sw = _at(_sweep('sawtooth', 150.0, 50.0, 0.40, 0.35, 0.010), 0.00, 0.50)
    nz = _at(_noise(0.20, 0.20, 0.005, seed=801), 0.30, 0.50)
    return _finalize(_mix(sw, nz))
def mech_spring_snap_001():
    a = _at(_tone('triangle', 1000.0, 0.05, 0.30, 0.001), 0.00, 0.10)
    return _finalize(_mix(a))
def mech_chain_rattle_001():
    parts = []
    for i in range(6):
        nz = _at(_noise(0.03, 0.25, 0.001, seed=802+i), i*0.04, 0.30)
        parts.append(nz)
    return _finalize(_mix(*parts))
def mech_ratchet_turn_001():
    parts = []
    for i in range(4):
        a = _at(_tone('square', 800.0, 0.02, 0.25, 0.001), i*0.06, 0.25)
        parts.append(a)
    return _finalize(_mix(*parts))
def mech_motor_start_001():
    sw = _at(_sweep('sawtooth', 50.0, 300.0, 0.60, 0.30, 0.050), 0.00, 0.70)
    return _finalize(_mix(sw))
def mech_motor_stop_001():
    sw = _at(_sweep('sawtooth', 300.0, 30.0, 0.60, 0.30, 0.020), 0.00, 0.70)
    return _finalize(_mix(sw))
def mech_bolt_tighten_001():
    parts = []
    for i in range(3):
        a = _at(_tone('square', 400.0, 0.03, 0.20, 0.001), i*0.08, 0.30)
        parts.append(a)
    return _finalize(_mix(*parts))
def mech_lock_engage_001():
    nz = _at(_noise(0.05, 0.30, 0.001, seed=803), 0.00, 0.10)
    a = _at(_tone('square', 300.0, 0.04, 0.25, 0.001), 0.05, 0.10)
    return _finalize(_mix(nz, a))
def mech_lock_release_001():
    a = _at(_tone('square', 300.0, 0.04, 0.25, 0.001), 0.00, 0.10)
    nz = _at(_noise(0.05, 0.30, 0.001, seed=804), 0.05, 0.10)
    return _finalize(_mix(a, nz))
def mech_valve_hiss_001():
    nz = _at(_noise(0.40, 0.30, 0.020, seed=805), 0.00, 0.50)
    return _finalize(_mix(nz))
def mech_steam_burst_001():
    nz = _at(_noise(0.30, 0.40, 0.005, seed=806), 0.00, 0.40)
    return _finalize(_mix(nz))
def mech_turbine_spin_001():
    sw = _at(_sweep('sawtooth', 100.0, 400.0, 1.00, 0.25, 0.050), 0.00, 1.10)
    return _finalize(_mix(sw))
def mech_conveyor_move_001():
    sw = _at(_sweep('sawtooth', 80.0, 100.0, 0.80, 0.20, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))
def mech_robotic_arm_001():
    a = _at(_sweep('sine', 200.0, 400.0, 0.15, 0.25, 0.005), 0.00, 0.20)
    b = _at(_tone('square', 600.0, 0.05, 0.20, 0.001), 0.20, 0.25)
    return _finalize(_mix(a, b))
def mech_weld_spark_001():
    nz = _at(_noise(0.20, 0.30, 0.001, seed=807), 0.00, 0.25)
    return _finalize(_mix(nz))
def mech_hammer_strike_001():
    a = _at(_tone('sine', 150.0, 0.10, 0.40, 0.001), 0.00, 0.15)
    nz = _at(_noise(0.05, 0.20, 0.001, seed=808), 0.00, 0.15)
    return _finalize(_mix(a, nz))
def mech_metal_clank_001():
    a = _at(_tone('triangle', 1200.0, 0.15, 0.30, 0.001), 0.00, 0.20)
    return _finalize(_mix(a))
def mech_pneumatic_hiss_001():
    nz = _at(_noise(0.20, 0.25, 0.005, seed=809), 0.00, 0.25)
    return _finalize(_mix(nz))
def mech_clockwork_tick_001():
    a = _at(_tone('square', 1000.0, 0.01, 0.25, 0.001), 0.00, 0.05)
    b = _at(_tone('square', 1000.0, 0.01, 0.25, 0.001), 0.10, 0.05)
    return _finalize(_mix(a, b))
def mech_heavy_door_slide_001():
    nz = _at(_noise(0.60, 0.25, 0.020, seed=810), 0.00, 0.70)
    return _finalize(_mix(nz))
def mech_security_breach_001():
    a = _at(_tone('sawtooth', 800.0, 0.10, 0.30, 0.005), 0.00, 0.15)
    b = _at(_tone('sawtooth', 600.0, 0.10, 0.30, 0.005), 0.15, 0.15)
    return _finalize(_mix(a, b))
def mech_system_shutdown_001():
    sw = _at(_sweep('square', 400.0, 50.0, 0.80, 0.30, 0.010), 0.00, 0.90)
    return _finalize(_mix(sw))

OFFICIAL_PRESETS_MECH = {
    'mech-gear-engage-001': mech_gear_engage_001, 'mech-gear-grind-001': mech_gear_grind_001,
    'mech-piston-pump-001': mech_piston_pump_001, 'mech-hydraulic-press-001': mech_hydraulic_press_001,
    'mech-spring-snap-001': mech_spring_snap_001, 'mech-chain-rattle-001': mech_chain_rattle_001,
    'mech-ratchet-turn-001': mech_ratchet_turn_001, 'mech-motor-start-001': mech_motor_start_001,
    'mech-motor-stop-001': mech_motor_stop_001, 'mech-bolt-tighten-001': mech_bolt_tighten_001,
    'mech-lock-engage-001': mech_lock_engage_001, 'mech-lock-release-001': mech_lock_release_001,
    'mech-valve-hiss-001': mech_valve_hiss_001, 'mech-steam-burst-001': mech_steam_burst_001,
    'mech-turbine-spin-001': mech_turbine_spin_001, 'mech-conveyor-move-001': mech_conveyor_move_001,
    'mech-robotic-arm-001': mech_robotic_arm_001, 'mech-weld-spark-001': mech_weld_spark_001,
    'mech-hammer-strike-001': mech_hammer_strike_001, 'mech-metal-clank-001': mech_metal_clank_001,
    'mech-pneumatic-hiss-001': mech_pneumatic_hiss_001, 'mech-clockwork-tick-001': mech_clockwork_tick_001,
    'mech-heavy-door-slide-001': mech_heavy_door_slide_001, 'mech-security-breach-001': mech_security_breach_001,
    'mech-system-shutdown-001': mech_system_shutdown_001,
}