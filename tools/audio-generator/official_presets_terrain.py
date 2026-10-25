"""Mission 1 - Movement / Terrain (25 sounds)."""
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

def footstep_mud_deep_001():
    nz = _at(_noise(0.15, 0.30, 0.005, seed=600), 0.00, 0.20)
    low = _at(_sweep('sine', 100.0, 50.0, 0.10, 0.35, 0.005), 0.00, 0.20)
    return _finalize(_mix(nz, low))

def footstep_wet_grass_001():
    nz = _at(_noise(0.12, 0.25, 0.010, seed=601), 0.00, 0.15)
    return _finalize(_mix(nz))

def footstep_gravel_loose_001():
    nz1 = _at(_noise(0.05, 0.30, 0.001, seed=602), 0.00, 0.15)
    nz2 = _at(_noise(0.05, 0.25, 0.001, seed=603), 0.06, 0.15)
    return _finalize(_mix(nz1, nz2))

def footstep_wood_hollow_001():
    tone = _at(_tone('square', 200.0, 0.08, 0.30, 0.002), 0.00, 0.10)
    nz = _at(_noise(0.05, 0.15, 0.001, seed=604), 0.00, 0.10)
    return _finalize(_mix(tone, nz))

def footstep_marble_hall_001():
    tone = _at(_tone('sine', 800.0, 0.10, 0.25, 0.002), 0.00, 0.15)
    nz = _at(_noise(0.05, 0.10, 0.001, seed=605), 0.00, 0.15)
    return _finalize(_mix(tone, nz))

def footstep_metal_grate_001():
    nz = _at(_noise(0.08, 0.35, 0.001, seed=606), 0.00, 0.12)
    tone = _at(_tone('sawtooth', 400.0, 0.06, 0.20, 0.002), 0.00, 0.12)
    return _finalize(_mix(nz, tone))

def footstep_snow_crust_001():
    nz = _at(_noise(0.10, 0.30, 0.002, seed=607), 0.00, 0.15)
    return _finalize(_mix(nz))

def footstep_shallow_water_001():
    nz = _at(_noise(0.15, 0.30, 0.005, seed=608), 0.00, 0.20)
    sw = _at(_sweep('sine', 600.0, 300.0, 0.10, 0.20, 0.005), 0.00, 0.20)
    return _finalize(_mix(nz, sw))

def footstep_dry_leaves_pile_001():
    nz = _at(_noise(0.20, 0.35, 0.005, seed=609), 0.00, 0.25)
    return _finalize(_mix(nz))

def footstep_sand_dunes_001():
    nz = _at(_noise(0.25, 0.20, 0.020, seed=610), 0.00, 0.30)
    return _finalize(_mix(nz))

def landing_roll_soft_001():
    nz = _at(_noise(0.30, 0.25, 0.050, seed=611), 0.00, 0.40)
    tone = _at(_tone('sine', 100.0, 0.20, 0.30, 0.010), 0.00, 0.40)
    return _finalize(_mix(nz, tone))

def landing_knee_hard_001():
    low = _at(_sweep('sawtooth', 150.0, 50.0, 0.15, 0.40, 0.002), 0.00, 0.20)
    nz = _at(_noise(0.10, 0.30, 0.001, seed=612), 0.00, 0.20)
    return _finalize(_mix(low, nz))

def slide_stone_surface_001():
    nz = _at(_noise(0.40, 0.25, 0.010, seed=613), 0.00, 0.50)
    return _finalize(_mix(nz))

def slide_ice_long_001():
    nz = _at(_noise(0.80, 0.20, 0.020, seed=614), 0.00, 0.90)
    sw = _at(_sweep('sine', 1500.0, 800.0, 0.80, 0.15, 0.020), 0.00, 0.90)
    return _finalize(_mix(nz, sw))

def rope_climb_strain_001():
    nz = _at(_noise(0.50, 0.20, 0.050, seed=615), 0.00, 0.60)
    return _finalize(_mix(nz))

def ladder_wood_climb_001():
    t1 = _at(_tone('square', 300.0, 0.05, 0.25, 0.002), 0.00, 0.30)
    t2 = _at(_tone('square', 300.0, 0.05, 0.25, 0.002), 0.15, 0.30)
    return _finalize(_mix(t1, t2))

def ladder_metal_rattle_001():
    nz = _at(_noise(0.15, 0.30, 0.002, seed=616), 0.00, 0.20)
    tone = _at(_tone('triangle', 800.0, 0.10, 0.20, 0.002), 0.00, 0.20)
    return _finalize(_mix(nz, tone))

def rope_swing_pass_001():
    sw = _at(_sweep('sine', 200.0, 500.0, 0.40, 0.25, 0.010), 0.00, 0.50)
    return _finalize(_mix(sw))

def zipline_start_001():
    sw = _at(_sweep('sawtooth', 400.0, 800.0, 0.30, 0.25, 0.005), 0.00, 0.40)
    return _finalize(_mix(sw))

def zipline_stop_001():
    sw = _at(_sweep('sawtooth', 800.0, 200.0, 0.40, 0.25, 0.005), 0.00, 0.50)
    return _finalize(_mix(sw))

def deep_water_dive_001():
    nz = _at(_noise(0.60, 0.40, 0.010, seed=617), 0.00, 0.70)
    low = _at(_sweep('sine', 300.0, 50.0, 0.50, 0.30, 0.010), 0.00, 0.70)
    return _finalize(_mix(nz, low))

def underwater_movement_001():
    nz = _at(_noise(0.50, 0.25, 0.050, seed=618), 0.00, 0.60)
    return _finalize(_mix(nz))

def rock_climb_grip_001():
    nz = _at(_noise(0.08, 0.25, 0.002, seed=619), 0.00, 0.12)
    return _finalize(_mix(nz))

def heavy_landing_dirt_001():
    low = _at(_sweep('sine', 120.0, 40.0, 0.20, 0.40, 0.005), 0.00, 0.25)
    nz = _at(_noise(0.15, 0.30, 0.005, seed=620), 0.00, 0.25)
    return _finalize(_mix(low, nz))

def body_roll_gravel_001():
    nz = _at(_noise(0.60, 0.30, 0.020, seed=621), 0.00, 0.70)
    return _finalize(_mix(nz))

OFFICIAL_PRESETS_TERRAIN = {
    'footstep-mud-deep-001': footstep_mud_deep_001,
    'footstep-wet-grass-001': footstep_wet_grass_001,
    'footstep-gravel-loose-001': footstep_gravel_loose_001,
    'footstep-wood-hollow-001': footstep_wood_hollow_001,
    'footstep-marble-hall-001': footstep_marble_hall_001,
    'footstep-metal-grate-001': footstep_metal_grate_001,
    'footstep-snow-crust-001': footstep_snow_crust_001,
    'footstep-shallow-water-001': footstep_shallow_water_001,
    'footstep-dry-leaves-pile-001': footstep_dry_leaves_pile_001,
    'footstep-sand-dunes-001': footstep_sand_dunes_001,
    'landing-roll-soft-001': landing_roll_soft_001,
    'landing-knee-hard-001': landing_knee_hard_001,
    'slide-stone-surface-001': slide_stone_surface_001,
    'slide-ice-long-001': slide_ice_long_001,
    'rope-climb-strain-001': rope_climb_strain_001,
    'ladder-wood-climb-001': ladder_wood_climb_001,
    'ladder-metal-rattle-001': ladder_metal_rattle_001,
    'rope-swing-pass-001': rope_swing_pass_001,
    'zipline-start-001': zipline_start_001,
    'zipline-stop-001': zipline_stop_001,
    'deep-water-dive-001': deep_water_dive_001,
    'underwater-movement-001': underwater_movement_001,
    'rock-climb-grip-001': rock_climb_grip_001,
    'heavy-landing-dirt-001': heavy_landing_dirt_001,
    'body-roll-gravel-001': body_roll_gravel_001,
}