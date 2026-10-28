"""New Plan 500 - Mission 1: Robotics & Automation (25 sounds)."""
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

def robot_arm_move_001():
    sw = _at(_sweep('sawtooth', 100.0, 200.0, 0.60, 0.25, 0.050), 0.00, 0.70)
    return _finalize(_mix(sw))
def robot_servo_activate_001():
    a = _at(_tone('square', 400.0, 0.10, 0.20, 0.002), 0.00, 0.15)
    return _finalize(_mix(a))
def robot_claw_grab_001():
    nz = _at(_noise(0.05, 0.30, 0.001, seed=2000), 0.00, 0.10)
    a = _at(_tone('sine', 200.0, 0.05, 0.35, 0.001), 0.00, 0.10)
    return _finalize(_mix(nz, a))
def robot_claw_release_001():
    nz = _at(_noise(0.05, 0.25, 0.001, seed=2001), 0.00, 0.10)
    return _finalize(_mix(nz))
def robot_joint_rotate_001():
    sw = _at(_sweep('sine', 150.0, 300.0, 0.40, 0.25, 0.020), 0.00, 0.50)
    return _finalize(_mix(sw))
def robot_hydraulic_pump_001():
    sw = _at(_sweep('sawtooth', 80.0, 120.0, 0.60, 0.30, 0.050), 0.00, 0.70)
    return _finalize(_mix(sw))
def robot_weld_spark_001():
    nz = _at(_noise(0.20, 0.40, 0.001, seed=2002), 0.00, 0.25)
    return _finalize(_mix(nz))
def robot_circuit_hum_001():
    a = _at(_tone('sine', 60.0, 1.00, 0.20, 0.050), 0.00, 1.10)
    return _finalize(_mix(a))
def robot_calibration_beep_001():
    parts = []
    for i in range(3): parts.append(_at(_tone('square', 1000.0, 0.05, 0.25, 0.001), i*0.10, 0.35))
    return _finalize(_mix(*parts))
def robot_scan_sweep_001():
    sw = _at(_sweep('sine', 200.0, 2000.0, 0.60, 0.20, 0.050), 0.00, 0.70)
    return _finalize(_mix(sw))
def robot_lock_engage_001():
    a = _at(_tone('square', 150.0, 0.10, 0.30, 0.002), 0.00, 0.15)
    nz = _at(_noise(0.05, 0.20, 0.001, seed=2003), 0.00, 0.15)
    return _finalize(_mix(a, nz))
def robot_lock_release_001():
    nz = _at(_noise(0.05, 0.25, 0.001, seed=2004), 0.00, 0.10)
    return _finalize(_mix(nz))
def robot_step_heavy_001():
    a = _at(_tone('sine', 80.0, 0.15, 0.40, 0.002), 0.00, 0.20)
    return _finalize(_mix(a))
def robot_step_light_001():
    a = _at(_tone('sine', 150.0, 0.05, 0.25, 0.001), 0.00, 0.10)
    return _finalize(_mix(a))
def robot_tool_switch_001():
    a = _at(_tone('square', 600.0, 0.05, 0.20, 0.001), 0.00, 0.10)
    b = _at(_tone('square', 800.0, 0.05, 0.20, 0.001), 0.05, 0.10)
    return _finalize(_mix(a, b))
def robot_assembly_line_001():
    parts = []
    for i in range(6): parts.append(_at(_tone('square', 200.0, 0.03, 0.20, 0.001), i*0.08, 0.50))
    return _finalize(_mix(*parts))
def robot_error_buzz_001():
    a = _at(_tone('sawtooth', 100.0, 0.30, 0.40, 0.005), 0.00, 0.40)
    return _finalize(_mix(a))
def robot_shutdown_001():
    sw = _at(_sweep('sine', 400.0, 50.0, 1.00, 0.35, 0.050), 0.00, 1.10)
    return _finalize(_mix(sw))
def robot_startup_001():
    sw = _at(_sweep('sine', 50.0, 400.0, 1.00, 0.35, 0.050), 0.00, 1.10)
    return _finalize(_mix(sw))
def robot_drill_arm_001():
    sw = _at(_sweep('sawtooth', 300.0, 500.0, 0.50, 0.30, 0.010), 0.00, 0.60)
    return _finalize(_mix(sw))
def robot_magnet_grab_001():
    a = _at(_tone('sine', 100.0, 0.20, 0.30, 0.010), 0.00, 0.25)
    return _finalize(_mix(a))
def robot_magnet_release_001():
    a = _at(_tone('sine', 80.0, 0.10, 0.25, 0.005), 0.00, 0.15)
    return _finalize(_mix(a))
def robot_sensor_ping_001():
    a = _at(_tone('sine', 2000.0, 0.05, 0.20, 0.001), 0.00, 0.10)
    return _finalize(_mix(a))
def robot_battery_low_001():
    parts = []
    for i in range(2): parts.append(_at(_tone('square', 800.0, 0.10, 0.25, 0.002), i*0.20, 0.40))
    return _finalize(_mix(*parts))
def robot_overload_001():
    nz = _at(_noise(0.40, 0.50, 0.005, seed=2005), 0.00, 0.50)
    return _finalize(_mix(nz))

OFFICIAL_PRESETS_ROBOTICS = {
    'robot-arm-move-001': robot_arm_move_001, 'robot-servo-activate-001': robot_servo_activate_001,
    'robot-claw-grab-001': robot_claw_grab_001, 'robot-claw-release-001': robot_claw_release_001,
    'robot-joint-rotate-001': robot_joint_rotate_001, 'robot-hydraulic-pump-001': robot_hydraulic_pump_001,
    'robot-weld-spark-001': robot_weld_spark_001, 'robot-circuit-hum-001': robot_circuit_hum_001,
    'robot-calibration-beep-001': robot_calibration_beep_001, 'robot-scan-sweep-001': robot_scan_sweep_001,
    'robot-lock-engage-001': robot_lock_engage_001, 'robot-lock-release-001': robot_lock_release_001,
    'robot-step-heavy-001': robot_step_heavy_001, 'robot-step-light-001': robot_step_light_001,
    'robot-tool-switch-001': robot_tool_switch_001, 'robot-assembly-line-001': robot_assembly_line_001,
    'robot-error-buzz-001': robot_error_buzz_001, 'robot-shutdown-001': robot_shutdown_001,
    'robot-startup-001': robot_startup_001, 'robot-drill-arm-001': robot_drill_arm_001,
    'robot-magnet-grab-001': robot_magnet_grab_001, 'robot-magnet-release-001': robot_magnet_release_001,
    'robot-sensor-ping-001': robot_sensor_ping_001, 'robot-battery-low-001': robot_battery_low_001,
    'robot-overload-001': robot_overload_001,
}