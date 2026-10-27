"""Milestone 500 - Unique Interactions (10 sounds)."""
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

def unique_alchemy_brew_001():
    nz = _at(_noise(0.80, 0.30, 0.050, seed=1800), 0.00, 0.90)
    return _finalize(_mix(nz))
def unique_lockpick_snap_001():
    a = _at(_tone('square', 1000.0, 0.05, 0.30, 0.001), 0.00, 0.10)
    return _finalize(_mix(a))
def unique_trap_disarm_001():
    sw = _at(_sweep('sine', 800.0, 400.0, 0.30, 0.25, 0.010), 0.00, 0.40)
    return _finalize(_mix(sw))
def unique_stealth_footstep_001():
    nz = _at(_noise(0.10, 0.15, 0.005, seed=1801), 0.00, 0.15)
    return _finalize(_mix(nz))
def unique_vent_crawl_001():
    nz = _at(_noise(0.50, 0.20, 0.050, seed=1802), 0.00, 0.60)
    return _finalize(_mix(nz))
def unique_wall_climb_001():
    sw = _at(_sweep('sine', 200.0, 400.0, 0.40, 0.20, 0.020), 0.00, 0.50)
    return _finalize(_mix(sw))
def unique_vehicle_boost_001():
    sw = _at(_sweep('sawtooth', 100.0, 600.0, 0.80, 0.35, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))
def unique_cyber_deck_overheat_001():
    nz = _at(_noise(0.60, 0.40, 0.020, seed=1803), 0.00, 0.70)
    return _finalize(_mix(nz))
def unique_magic_mirror_shatter_001():
    nz = _at(_noise(0.40, 0.50, 0.001, seed=1804), 0.00, 0.50)
    return _finalize(_mix(nz))
def unique_reality_glitch_short_001():
    nz = _at(_noise(0.10, 0.40, 0.001, seed=1805), 0.00, 0.15)
    sw = _at(_sweep('square', 1000.0, 200.0, 0.10, 0.30, 0.001), 0.00, 0.15)
    return _finalize(_mix(nz, sw))

OFFICIAL_PRESETS_UNIQUE = {
    'unique-alchemy-brew-001': unique_alchemy_brew_001, 'unique-lockpick-snap-001': unique_lockpick_snap_001,
    'unique-trap-disarm-001': unique_trap_disarm_001, 'unique-stealth-footstep-001': unique_stealth_footstep_001,
    'unique-vent-crawl-001': unique_vent_crawl_001, 'unique-wall-climb-001': unique_wall_climb_001,
    'unique-vehicle-boost-001': unique_vehicle_boost_001, 'unique-cyber-deck-overheat-001': unique_cyber_deck_overheat_001,
    'unique-magic-mirror-shatter-001': unique_magic_mirror_shatter_001, 'unique-reality-glitch-short-001': unique_reality_glitch_short_001,
}