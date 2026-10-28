"""New Plan 500 - Mission 2: Spacecraft & Space Systems (25 sounds)."""
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

def spaceship_door_open_001():
    sw = _at(_sweep('sawtooth', 100.0, 200.0, 0.80, 0.30, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))

def spaceship_door_close_001():
    sw = _at(_sweep('sawtooth', 200.0, 100.0, 0.80, 0.30, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))

def spaceship_engine_hum_001():
    a = _at(_tone('sine', 80.0, 1.50, 0.25, 0.100), 0.00, 1.60)
    return _finalize(_mix(a))

def spaceship_warp_jump_001():
    sw = _at(_sweep('sine', 100.0, 2000.0, 1.20, 0.40, 0.100), 0.00, 1.30)
    return _finalize(_mix(sw))

def spaceship_shield_hit_001():
    nz = _at(_noise(0.20, 0.50, 0.001, seed=2100), 0.00, 0.25)
    a = _at(_tone('sine', 200.0, 0.15, 0.30, 0.002), 0.00, 0.25)
    return _finalize(_mix(nz, a))

def spaceship_weapon_fire_001():
    sw = _at(_sweep('square', 2000.0, 500.0, 0.30, 0.35, 0.002), 0.00, 0.40)
    return _finalize(_mix(sw))

def spaceship_alert_system_001():
    parts = []
    for i in range(3): parts.append(_at(_tone('square', 1200.0, 0.10, 0.25, 0.002), i*0.15, 0.50))
    return _finalize(_mix(*parts))

def spaceship_navigation_ping_001():
    a = _at(_tone('sine', 1500.0, 0.05, 0.20, 0.001), 0.00, 0.10)
    return _finalize(_mix(a))

def spaceship_comms_static_001():
    nz = _at(_noise(0.60, 0.20, 0.050, seed=2101), 0.00, 0.70)
    return _finalize(_mix(nz))

def spaceship_docking_clamp_001():
    nz = _at(_noise(0.10, 0.40, 0.001, seed=2102), 0.00, 0.15)
    a = _at(_tone('sine', 100.0, 0.10, 0.35, 0.002), 0.00, 0.15)
    return _finalize(_mix(nz, a))

def spaceship_thruster_boost_001():
    sw = _at(_sweep('sawtooth', 100.0, 400.0, 0.60, 0.35, 0.050), 0.00, 0.70)
    return _finalize(_mix(sw))

def spaceship_stabilizer_001():
    sw = _at(_sweep('sine', 300.0, 200.0, 0.40, 0.20, 0.020), 0.00, 0.50)
    return _finalize(_mix(sw))

def spaceship_life_support_001():
    a = _at(_tone('sine', 120.0, 1.00, 0.20, 0.050), 0.00, 1.10)
    return _finalize(_mix(a))

def spaceship_oxygen_leak_001():
    nz = _at(_noise(0.80, 0.30, 0.050, seed=2103), 0.00, 0.90)
    return _finalize(_mix(nz))

def spaceship_hull_breach_001():
    nz = _at(_noise(0.50, 0.60, 0.001, seed=2104), 0.00, 0.60)
    return _finalize(_mix(nz))

def spaceship_scan_sweep_001():
    sw = _at(_sweep('sine', 200.0, 2000.0, 0.80, 0.20, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))

def spaceship_target_lock_001():
    parts = []
    for i in range(2): parts.append(_at(_tone('square', 1000.0, 0.05, 0.25, 0.001), i*0.08, 0.20))
    return _finalize(_mix(*parts))

def spaceship_emp_burst_001():
    nz = _at(_noise(0.30, 0.60, 0.001, seed=2105), 0.00, 0.40)
    return _finalize(_mix(nz))

def spaceship_tractor_beam_001():
    sw = _at(_sweep('sine', 400.0, 100.0, 0.60, 0.25, 0.020), 0.00, 0.70)
    return _finalize(_mix(sw))

def spaceship_cockpit_click_001():
    a = _at(_tone('square', 800.0, 0.02, 0.15, 0.001), 0.00, 0.05)
    return _finalize(_mix(a))

def spaceship_radar_sweep_001():
    parts = []
    for i in range(4): parts.append(_at(_tone('sine', 1500.0, 0.02, 0.15, 0.001), i*0.15, 0.60))
    return _finalize(_mix(*parts))

def spaceship_gravity_off_001():
    sw = _at(_sweep('sine', 200.0, 50.0, 0.50, 0.25, 0.020), 0.00, 0.60)
    return _finalize(_mix(sw))

def spaceship_gravity_on_001():
    sw = _at(_sweep('sine', 50.0, 200.0, 0.50, 0.25, 0.020), 0.00, 0.60)
    return _finalize(_mix(sw))

def spaceship_cryo_freeze_001():
    sw = _at(_sweep('sawtooth', 800.0, 100.0, 0.80, 0.30, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))

def spaceship_cryo_thaw_001():
    sw = _at(_sweep('sawtooth', 100.0, 800.0, 0.80, 0.30, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))

OFFICIAL_PRESETS_SPACESHIP = {
    'spaceship-door-open-001': spaceship_door_open_001, 'spaceship-door-close-001': spaceship_door_close_001,
    'spaceship-engine-hum-001': spaceship_engine_hum_001, 'spaceship-warp-jump-001': spaceship_warp_jump_001,
    'spaceship-shield-hit-001': spaceship_shield_hit_001, 'spaceship-weapon-fire-001': spaceship_weapon_fire_001,
    'spaceship-alert-system-001': spaceship_alert_system_001, 'spaceship-navigation-ping-001': spaceship_navigation_ping_001,
    'spaceship-comms-static-001': spaceship_comms_static_001, 'spaceship-docking-clamp-001': spaceship_docking_clamp_001,
    'spaceship-thruster-boost-001': spaceship_thruster_boost_001, 'spaceship-stabilizer-001': spaceship_stabilizer_001,
    'spaceship-life-support-001': spaceship_life_support_001, 'spaceship-oxygen-leak-001': spaceship_oxygen_leak_001,
    'spaceship-hull-breach-001': spaceship_hull_breach_001, 'spaceship-scan-sweep-001': spaceship_scan_sweep_001,
    'spaceship-target-lock-001': spaceship_target_lock_001, 'spaceship-emp-burst-001': spaceship_emp_burst_001,
    'spaceship-tractor-beam-001': spaceship_tractor_beam_001, 'spaceship-cockpit-click-001': spaceship_cockpit_click_001,
    'spaceship-radar-sweep-001': spaceship_radar_sweep_001, 'spaceship-gravity-off-001': spaceship_gravity_off_001,
    'spaceship-gravity-on-001': spaceship_gravity_on_001, 'spaceship-cryo-freeze-001': spaceship_cryo_freeze_001,
    'spaceship-cryo-thaw-001': spaceship_cryo_thaw_001,
}