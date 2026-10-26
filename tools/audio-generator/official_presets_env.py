"""Mission 7 - Extreme Environments & Natural Phenomena (25 sounds)."""
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

def env_avalanche_001():
    nz = _at(_noise(1.5, 0.5, 0.10, seed=1000), 0.00, 1.60)
    low = _at(_sweep('sine', 60.0, 30.0, 1.0, 0.4, 0.1), 0.00, 1.60)
    return _finalize(_mix(nz, low))
def env_geyser_eruption_001():
    nz = _at(_noise(0.8, 0.4, 0.01, seed=1001), 0.00, 1.00)
    sw = _at(_sweep('sine', 200.0, 800.0, 0.5, 0.3, 0.05), 0.00, 1.00)
    return _finalize(_mix(nz, sw))
def env_earthquake_rumble_001():
    nz = _at(_noise(2.0, 0.6, 0.20, seed=1002), 0.00, 2.20)
    low = _at(_sweep('sine', 40.0, 20.0, 1.8, 0.5, 0.2), 0.00, 2.20)
    return _finalize(_mix(nz, low))
def env_desert_wind_001():
    nz = _at(_noise(1.5, 0.4, 0.1, seed=1003), 0.00, 1.60)
    high = _at(_tone('sine', 2000.0, 1.2, 0.1, 0.1), 0.00, 1.60)
    return _finalize(_mix(nz, high))
def env_glacier_crack_001():
    nz = _at(_noise(0.1, 0.5, 0.001, seed=1004), 0.00, 0.15)
    high = _at(_tone('square', 1500.0, 0.05, 0.3, 0.001), 0.00, 0.15)
    return _finalize(_mix(nz, high))
def env_lava_bubble_001():
    sw = _at(_sweep('sine', 80.0, 150.0, 0.4, 0.4, 0.05), 0.00, 0.50)
    nz = _at(_noise(0.3, 0.2, 0.02, seed=1005), 0.00, 0.50)
    return _finalize(_mix(sw, nz))
def env_mud_bubble_001():
    for i in range(5):
        pass
    sw = _at(_sweep('triangle', 200.0, 300.0, 0.2, 0.3, 0.01), 0.00, 0.30)
    return _finalize(_mix(sw))
def env_waterfall_001():
    nz = _at(_noise(2.0, 0.5, 0.10, seed=1006), 0.00, 2.20)
    return _finalize(_mix(nz))
def env_quicksand_001():
    nz = _at(_noise(1.2, 0.4, 0.20, seed=1007), 0.00, 1.30)
    low = _at(_sweep('sine', 50.0, 20.0, 1.0, 0.3, 0.2), 0.00, 1.30)
    return _finalize(_mix(nz, low))
def env_snow_crunch_001():
    nz = _at(_noise(0.3, 0.3, 0.01, seed=1008), 0.00, 0.40)
    return _finalize(_mix(nz))
def env_swamp_ambience_001():
    nz = _at(_noise(1.5, 0.2, 0.1, seed=1009), 0.00, 1.60)
    return _finalize(_mix(nz))
def env_bamboo_creak_001():
    nz = _at(_noise(0.5, 0.25, 0.05, seed=1010), 0.00, 0.60)
    sw = _at(_sweep('sawtooth', 100.0, 150.0, 0.5, 0.2, 0.05), 0.00, 0.60)
    return _finalize(_mix(nz, sw))
def env_sandstorm_001():
    nz = _at(_noise(1.5, 0.5, 0.05, seed=1011), 0.00, 1.60)
    high = _at(_tone('sawtooth', 3000.0, 1.2, 0.15, 0.05), 0.00, 1.60)
    return _finalize(_mix(nz, high))
def env_icicle_fall_001():
    nz = _at(_noise(0.1, 0.4, 0.001, seed=1012), 0.00, 0.15)
    high = _at(_tone('sine', 2500.0, 0.1, 0.3, 0.001), 0.00, 0.15)
    return _finalize(_mix(nz, high))
def env_canyon_echo_001():
    a = _at(_tone('sine', 1000.0, 0.2, 0.4, 0.01), 0.00, 0.80)
    b = _at(_tone('sine', 1000.0, 0.2, 0.2, 0.01), 0.20, 0.80)
    c = _at(_tone('sine', 1000.0, 0.2, 0.1, 0.01), 0.40, 0.80)
    return _finalize(_mix(a, b, c))
def env_river_flow_001():
    nz = _at(_noise(2.0, 0.4, 0.10, seed=1013), 0.00, 2.20)
    return _finalize(_mix(nz))
def env_forest_fire_001():
    nz = _at(_noise(1.5, 0.5, 0.05, seed=1014), 0.00, 1.60)
    low = _at(_sweep('sine', 100.0, 50.0, 1.2, 0.3, 0.05), 0.00, 1.60)
    return _finalize(_mix(nz, low))
def env_hail_storm_001():
    nz1 = _at(_noise(0.1, 0.4, 0.001, seed=1015), 0.00, 0.50)
    nz2 = _at(_noise(0.1, 0.4, 0.001, seed=1016), 0.15, 0.50)
    nz3 = _at(_noise(0.1, 0.4, 0.001, seed=1017), 0.30, 0.50)
    return _finalize(_mix(nz1, nz2, nz3))
def env_tornado_001():
    nz = _at(_noise(2.0, 0.6, 0.10, seed=1018), 0.00, 2.20)
    sw = _at(_sweep('sawtooth', 150.0, 50.0, 2.0, 0.3, 0.1), 0.00, 2.20)
    return _finalize(_mix(nz, sw))
def env_tide_pool_001():
    nz = _at(_noise(1.0, 0.2, 0.05, seed=1019), 0.00, 1.10)
    return _finalize(_mix(nz))
def env_rock_fall_001():
    nz1 = _at(_noise(0.2, 0.4, 0.01, seed=1020), 0.00, 0.60)
    nz2 = _at(_noise(0.2, 0.4, 0.01, seed=1021), 0.20, 0.60)
    return _finalize(_mix(nz1, nz2))
def env_volcanic_vent_001():
    nz = _at(_noise(1.0, 0.4, 0.05, seed=1022), 0.00, 1.10)
    high = _at(_tone('sine', 1500.0, 0.8, 0.1, 0.05), 0.00, 1.10)
    return _finalize(_mix(nz, high))
def env_blizzard_001():
    nz = _at(_noise(2.0, 0.5, 0.10, seed=1023), 0.00, 2.20)
    return _finalize(_mix(nz))
def env_jungle_rain_001():
    nz = _at(_noise(1.5, 0.4, 0.05, seed=1024), 0.00, 1.60)
    return _finalize(_mix(nz))
def env_quarry_blast_001():
    nz = _at(_noise(0.5, 0.6, 0.01, seed=1025), 0.00, 0.60)
    low = _at(_sweep('sine', 80.0, 20.0, 0.5, 0.5, 0.01), 0.00, 0.60)
    return _finalize(_mix(nz, low))

OFFICIAL_PRESETS_ENV = {
    'env-avalanche-001': env_avalanche_001, 'env-geyser-eruption-001': env_geyser_eruption_001,
    'env-earthquake-rumble-001': env_earthquake_rumble_001, 'env-desert-wind-001': env_desert_wind_001,
    'env-glacier-crack-001': env_glacier_crack_001, 'env-lava-bubble-001': env_lava_bubble_001,
    'env-mud-bubble-001': env_mud_bubble_001, 'env-waterfall-001': env_waterfall_001,
    'env-quicksand-001': env_quicksand_001, 'env-snow-crunch-001': env_snow_crunch_001,
    'env-swamp-ambience-001': env_swamp_ambience_001, 'env-bamboo-creak-001': env_bamboo_creak_001,
    'env-sandstorm-001': env_sandstorm_001, 'env-icicle-fall-001': env_icicle_fall_001,
    'env-canyon-echo-001': env_canyon_echo_001, 'env-river-flow-001': env_river_flow_001,
    'env-forest-fire-001': env_forest_fire_001, 'env-hail-storm-001': env_hail_storm_001,
    'env-tornado-001': env_tornado_001, 'env-tide-pool-001': env_tide_pool_001,
    'env-rock-fall-001': env_rock_fall_001, 'env-volcanic-vent-001': env_volcanic_vent_001,
    'env-blizzard-001': env_blizzard_001, 'env-jungle-rain-001': env_jungle_rain_001,
    'env-quarry-blast-001': env_quarry_blast_001,
}