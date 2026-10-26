"""Mission 5 - Heavy Industry & Production (25 sounds)."""
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

def ind_factory_siren_001():
    sw = _at(_sweep('sawtooth', 400.0, 600.0, 0.80, 0.30, 0.050), 0.00, 1.00)
    return _finalize(_mix(sw))
def ind_assembly_line_001():
    parts = []
    for i in range(8): parts.append(_at(_tone('square', 100.0, 0.05, 0.25, 0.001), i*0.12, 1.00))
    return _finalize(_mix(*parts))
def ind_robot_arm_weld_001():
    nz = _at(_noise(0.30, 0.40, 0.010, seed=900), 0.00, 0.40)
    return _finalize(_mix(nz))
def ind_conveyor_heavy_001():
    sw = _at(_sweep('sawtooth', 50.0, 80.0, 1.00, 0.20, 0.050), 0.00, 1.10)
    return _finalize(_mix(sw))
def ind_steam_release_001():
    nz = _at(_noise(0.60, 0.45, 0.010, seed=901), 0.00, 0.70)
    return _finalize(_mix(nz))
def ind_forge_hammer_001():
    a = _at(_tone('sine', 80.0, 0.20, 0.50, 0.002), 0.00, 0.30)
    nz = _at(_noise(0.10, 0.30, 0.001, seed=902), 0.00, 0.30)
    return _finalize(_mix(a, nz))
def ind_laser_cutter_001():
    sw = _at(_sweep('square', 2000.0, 1000.0, 0.40, 0.25, 0.005), 0.00, 0.50)
    return _finalize(_mix(sw))
def ind_molding_press_001():
    sw = _at(_sweep('sine', 100.0, 40.0, 0.30, 0.40, 0.005), 0.00, 0.40)
    return _finalize(_mix(sw))
def ind_coolant_spray_001():
    nz = _at(_noise(0.40, 0.30, 0.020, seed=903), 0.00, 0.50)
    return _finalize(_mix(nz))
def ind_turbine_startup_001():
    sw = _at(_sweep('sawtooth', 50.0, 300.0, 1.20, 0.25, 0.100), 0.00, 1.30)
    return _finalize(_mix(sw))
def ind_magnetic_crane_001():
    a = _at(_tone('square', 200.0, 0.10, 0.30, 0.010), 0.00, 0.15)
    return _finalize(_mix(a))
def ind_furnace_roar_001():
    nz = _at(_noise(1.00, 0.40, 0.050, seed=904), 0.00, 1.10)
    return _finalize(_mix(nz))
def ind_packing_machine_001():
    a = _at(_tone('square', 150.0, 0.05, 0.20, 0.001), 0.00, 0.20)
    b = _at(_tone('square', 150.0, 0.05, 0.20, 0.001), 0.15, 0.20)
    return _finalize(_mix(a, b))
def ind_shutdown_sequence_001():
    sw = _at(_sweep('sawtooth', 300.0, 50.0, 1.00, 0.30, 0.020), 0.00, 1.10)
    return _finalize(_mix(sw))
def ind_emergency_stop_001():
    a = _at(_tone('square', 1000.0, 0.10, 0.35, 0.002), 0.00, 0.20)
    b = _at(_tone('square', 800.0, 0.10, 0.35, 0.002), 0.20, 0.20)
    return _finalize(_mix(a, b))
def ind_metal_pour_001():
    nz = _at(_noise(0.80, 0.35, 0.020, seed=905), 0.00, 0.90)
    return _finalize(_mix(nz))
def ind_belt_snap_001():
    nz = _at(_noise(0.05, 0.40, 0.001, seed=906), 0.00, 0.10)
    a = _at(_tone('sawtooth', 150.0, 0.05, 0.30, 0.001), 0.00, 0.10)
    return _finalize(_mix(nz, a))
def ind_ventilation_hum_001():
    nz = _at(_noise(1.00, 0.15, 0.100, seed=907), 0.00, 1.10)
    return _finalize(_mix(nz))
def ind_drill_press_heavy_001():
    sw = _at(_sweep('square', 200.0, 100.0, 0.50, 0.30, 0.010), 0.00, 0.60)
    return _finalize(_mix(sw))
def ind_forklift_move_001():
    sw = _at(_sweep('sine', 80.0, 120.0, 0.60, 0.20, 0.050), 0.00, 0.70)
    return _finalize(_mix(sw))
def ind_safety_alarm_001():
    a = _at(_tone('square', 800.0, 0.15, 0.30, 0.002), 0.00, 0.20)
    return _finalize(_mix(a))
def ind_scrap_metal_crush_001():
    nz = _at(_noise(0.50, 0.45, 0.005, seed=908), 0.00, 0.60)
    return _finalize(_mix(nz))
def ind_electric_motor_hum_001():
    a = _at(_tone('sawtooth', 60.0, 1.00, 0.25, 0.010), 0.00, 1.10)
    return _finalize(_mix(a))
def ind_production_bell_001():
    a = _at(_tone('triangle', 1000.0, 0.30, 0.30, 0.005), 0.00, 0.40)
    return _finalize(_mix(a))
def ind_heavy_door_lock_001():
    nz = _at(_noise(0.10, 0.35, 0.001, seed=909), 0.00, 0.15)
    a = _at(_tone('sine', 100.0, 0.15, 0.40, 0.002), 0.00, 0.20)
    return _finalize(_mix(nz, a))

OFFICIAL_PRESETS_IND = {
    'ind-factory-siren-001': ind_factory_siren_001, 'ind-assembly-line-001': ind_assembly_line_001,
    'ind-robot-arm-weld-001': ind_robot_arm_weld_001, 'ind-conveyor-heavy-001': ind_conveyor_heavy_001,
    'ind-steam-release-001': ind_steam_release_001, 'ind-forge-hammer-001': ind_forge_hammer_001,
    'ind-laser-cutter-001': ind_laser_cutter_001, 'ind-molding-press-001': ind_molding_press_001,
    'ind-coolant-spray-001': ind_coolant_spray_001, 'ind-turbine-startup-001': ind_turbine_startup_001,
    'ind-magnetic-crane-001': ind_magnetic_crane_001, 'ind-furnace-roar-001': ind_furnace_roar_001,
    'ind-packing-machine-001': ind_packing_machine_001, 'ind-shutdown-sequence-001': ind_shutdown_sequence_001,
    'ind-emergency-stop-001': ind_emergency_stop_001, 'ind-metal-pour-001': ind_metal_pour_001,
    'ind-belt-snap-001': ind_belt_snap_001, 'ind-ventilation-hum-001': ind_ventilation_hum_001,
    'ind-drill-press-heavy-001': ind_drill_press_heavy_001, 'ind-forklift-move-001': ind_forklift_move_001,
    'ind-safety-alarm-001': ind_safety_alarm_001, 'ind-scrap-metal-crush-001': ind_scrap_metal_crush_001,
    'ind-electric-motor-hum-001': ind_electric_motor_hum_001, 'ind-production-bell-001': ind_production_bell_001,
    'ind-heavy-door-lock-001': ind_heavy_door_lock_001,
}