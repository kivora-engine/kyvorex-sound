"""Missions 3 - Ancient Ruins & Artifacts (25 sounds)."""
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

def ruin_stone_mechanism_001():
    nz = _at(_noise(0.20, 0.40, 0.010, seed=2200), 0.00, 0.25)
    low = _at(_sweep('sawtooth', 100.0, 80.0, 0.20, 0.30, 0.010), 0.00, 0.25)
    return _finalize(_mix(nz, low))
def ruin_ancient_door_open_001():
    sw = _at(_sweep('sawtooth', 50.0, 120.0, 1.20, 0.35, 0.050), 0.00, 1.30)
    return _finalize(_mix(sw))
def ruin_ancient_door_close_001():
    sw = _at(_sweep('sawtooth', 120.0, 50.0, 1.20, 0.35, 0.050), 0.00, 1.30)
    return _finalize(_mix(sw))
def ruin_lock_engage_001():
    a = _at(_tone('square', 300.0, 0.10, 0.30, 0.002), 0.00, 0.15)
    nz = _at(_noise(0.10, 0.20, 0.001, seed=2201), 0.00, 0.15)
    return _finalize(_mix(a, nz))
def ruin_lock_release_001():
    nz = _at(_noise(0.10, 0.30, 0.001, seed=2202), 0.00, 0.15)
    return _finalize(_mix(nz))
def ruin_relic_activate_001():
    parts = []
    for i in range(4): parts.append(_at(_tone('sine', 600.0 + i*100, 0.10, 0.20, 0.010), i*0.10, 0.50))
    return _finalize(_mix(*parts))
def ruin_statue_turn_001():
    nz = _at(_noise(0.60, 0.30, 0.020, seed=2203), 0.00, 0.70)
    return _finalize(_mix(nz))
def ruin_secret_wall_slide_001():
    sw = _at(_sweep('sine', 150.0, 100.0, 0.80, 0.30, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))
def ruin_trap_trigger_001():
    nz = _at(_noise(0.05, 0.40, 0.001, seed=2204), 0.00, 0.10)
    a = _at(_tone('square', 200.0, 0.05, 0.30, 0.001), 0.00, 0.10)
    return _finalize(_mix(nz, a))
def ruin_block_move_001():
    nz = _at(_noise(0.60, 0.35, 0.050, seed=2205), 0.00, 0.70)
    return _finalize(_mix(nz))
def ruin_rune_glow_001():
    sw = _at(_sweep('sine', 200.0, 800.0, 0.60, 0.20, 0.050), 0.00, 0.70)
    return _finalize(_mix(sw))
def ruin_artifact_pickup_001():
    parts = []
    for i in range(3): parts.append(_at(_tone('triangle', 800.0 + i*100, 0.10, 0.25, 0.005), i*0.08, 0.35))
    return _finalize(_mix(*parts))
def ruin_temple_bell_001():
    a = _at(_tone('sine', 400.0, 1.20, 0.30, 0.005), 0.00, 1.30)
    return _finalize(_mix(a))
def ruin_archaeological_scan_001():
    sw = _at(_sweep('sine', 400.0, 1600.0, 0.80, 0.20, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))
def ruin_pedestal_activate_001():
    a = _at(_tone('square', 300.0, 0.20, 0.30, 0.005), 0.00, 0.25)
    return _finalize(_mix(a))
def ruin_glyph_light_001():
    sw = _at(_sweep('sine', 800.0, 1200.0, 0.50, 0.20, 0.050), 0.00, 0.60)
    return _finalize(_mix(sw))
def ruin_pressure_plate_001():
    nz = _at(_noise(0.05, 0.35, 0.001, seed=2206), 0.00, 0.10)
    a = _at(_tone('sine', 100.0, 0.05, 0.30, 0.001), 0.00, 0.10)
    return _finalize(_mix(nz, a))
def ruin_sarcophagus_open_001():
    nz = _at(_noise(0.80, 0.40, 0.050, seed=2207), 0.00, 0.90)
    return _finalize(_mix(nz))
def ruin_artifact_beam_001():
    sw = _at(_sweep('sine', 1000.0, 2000.0, 0.80, 0.20, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))
def ruin_stone_grind_001():
    nz = _at(_noise(0.40, 0.30, 0.050, seed=2208), 0.00, 0.50)
    return _finalize(_mix(nz))
def ruin_temple_door_rumble_001():
    low = _at(_sweep('sine', 60.0, 40.0, 1.20, 0.40, 0.100), 0.00, 1.30)
    return _finalize(_mix(low))
def ruin_relic_hum_001():
    a = _at(_tone('sine', 80.0, 1.50, 0.20, 0.100), 0.00, 1.60)
    return _finalize(_mix(a))
def ruin_ancient_magic_001():
    parts = []
    for i in range(6): parts.append(_at(_tone('sine', 400.0 + i*80, 0.15, 0.15, 0.010), i*0.08, 0.60))
    return _finalize(_mix(*parts))
def ruin_artifact_shatter_001():
    nz = _at(_noise(0.20, 0.50, 0.001, seed=2209), 0.00, 0.25)
    high = _at(_tone('sine', 2000.0, 0.15, 0.20, 0.001), 0.00, 0.25)
    return _finalize(_mix(nz, high))
def ruin_temple_wind_001():
    nz = _at(_noise(1.50, 0.20, 0.100, seed=2210), 0.00, 1.60)
    return _finalize(_mix(nz))

OFFICIAL_PRESETS_RUINS = {
    'ruin-stone-mechanism-001': ruin_stone_mechanism_001, 'ruin-ancient-door-open-001': ruin_ancient_door_open_001,
    'ruin-ancient-door-close-001': ruin_ancient_door_close_001, 'ruin-lock-engage-001': ruin_lock_engage_001,
    'ruin-lock-release-001': ruin_lock_release_001, 'ruin-relic-activate-001': ruin_relic_activate_001,
    'ruin-statue-turn-001': ruin_statue_turn_001, 'ruin-secret-wall-slide-001': ruin_secret_wall_slide_001,
    'ruin-trap-trigger-001': ruin_trap_trigger_001, 'ruin-block-move-001': ruin_block_move_001,
    'ruin-rune-glow-001': ruin_rune_glow_001, 'ruin-artifact-pickup-001': ruin_artifact_pickup_001,
    'ruin-temple-bell-001': ruin_temple_bell_001, 'ruin-archaeological-scan-001': ruin_archaeological_scan_001,
    'ruin-pedestal-activate-001': ruin_pedestal_activate_001, 'ruin-glyph-light-001': ruin_glyph_light_001,
    'ruin-pressure-plate-001': ruin_pressure_plate_001, 'ruin-sarcophagus-open-001': ruin_sarcophagus_open_001,
    'ruin-artifact-beam-001': ruin_artifact_beam_001, 'ruin-stone-grind-001': ruin_stone_grind_001,
    'ruin-temple-door-rumble-001': ruin_temple_door_rumble_001, 'ruin-relic-hum-001': ruin_relic_hum_001,
    'ruin-ancient-magic-001': ruin_ancient_magic_001, 'ruin-artifact-shatter-001': ruin_artifact_shatter_001,
    'ruin-temple-wind-001': ruin_temple_wind_001,
}