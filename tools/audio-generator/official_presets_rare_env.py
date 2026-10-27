"""Milestone 500 - Rare Environments (15 sounds)."""
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

def env_aurora_borealis_001():
    sw = _at(_sweep('sine', 200.0, 800.0, 2.00, 0.20, 0.200), 0.00, 2.20)
    return _finalize(_mix(sw))
def env_geyser_mini_001():
    nz = _at(_noise(0.40, 0.30, 0.010, seed=1700), 0.00, 0.50)
    return _finalize(_mix(nz))
def env_crystal_cave_hum_001():
    a = _at(_tone('sine', 120.0, 1.50, 0.25, 0.100), 0.00, 1.60)
    return _finalize(_mix(a))
def env_floating_islands_001():
    a = _at(_tone('sine', 80.0, 2.00, 0.20, 0.200), 0.00, 2.20)
    return _finalize(_mix(a))
def env_meteor_shower_distant_001():
    nz = _at(_noise(1.20, 0.20, 0.100, seed=1701), 0.00, 1.30)
    return _finalize(_mix(nz))
def env_swamp_gas_bubble_001():
    sw = _at(_sweep('sine', 100.0, 50.0, 0.30, 0.30, 0.020), 0.00, 0.40)
    return _finalize(_mix(sw))
def env_desert_mirage_shimmer_001():
    a = _at(_tone('sine', 3000.0, 1.50, 0.10, 0.200), 0.00, 1.60)
    return _finalize(_mix(a))
def env_frozen_lake_crack_001():
    nz = _at(_noise(0.20, 0.50, 0.001, seed=1702), 0.00, 0.25)
    return _finalize(_mix(nz))
def env_volcanic_lightning_001():
    nz = _at(_noise(0.30, 0.60, 0.010, seed=1703), 0.00, 0.40)
    return _finalize(_mix(nz))
def env_bioluminescent_forest_001():
    nz = _at(_noise(1.50, 0.15, 0.100, seed=1704), 0.00, 1.60)
    return _finalize(_mix(nz))
def env_sandstorm_distant_001():
    nz = _at(_noise(2.00, 0.30, 0.100, seed=1705), 0.00, 2.20)
    return _finalize(_mix(nz))
def env_waterfall_misty_001():
    nz = _at(_noise(1.50, 0.40, 0.050, seed=1706), 0.00, 1.60)
    return _finalize(_mix(nz))
def env_magnetic_anomaly_001():
    sw = _at(_sweep('square', 200.0, 400.0, 1.00, 0.20, 0.100), 0.00, 1.10)
    return _finalize(_mix(sw))
def env_gravity_well_pulse_001():
    sw = _at(_sweep('sine', 100.0, 40.0, 0.80, 0.40, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))
def env_solar_flare_wind_001():
    nz = _at(_noise(1.50, 0.35, 0.100, seed=1707), 0.00, 1.60)
    return _finalize(_mix(nz))

OFFICIAL_PRESETS_RARE_ENV = {
    'env-aurora-borealis-001': env_aurora_borealis_001, 'env-geyser-mini-001': env_geyser_mini_001,
    'env-crystal-cave-hum-001': env_crystal_cave_hum_001, 'env-floating-islands-001': env_floating_islands_001,
    'env-meteor-shower-distant-001': env_meteor_shower_distant_001, 'env-swamp-gas-bubble-001': env_swamp_gas_bubble_001,
    'env-desert-mirage-shimmer-001': env_desert_mirage_shimmer_001, 'env-frozen-lake-crack-001': env_frozen_lake_crack_001,
    'env-volcanic-lightning-001': env_volcanic_lightning_001, 'env-bioluminescent-forest-001': env_bioluminescent_forest_001,
    'env-sandstorm-distant-001': env_sandstorm_distant_001, 'env-waterfall-misty-001': env_waterfall_misty_001,
    'env-magnetic-anomaly-001': env_magnetic_anomaly_001, 'env-gravity-well-pulse-001': env_gravity_well_pulse_001,
    'env-solar-flare-wind-001': env_solar_flare_wind_001,
}