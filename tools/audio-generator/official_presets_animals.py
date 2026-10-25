"""Mission 2 - Animals (25 sounds)."""
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

def wolf_pack_howling_001():
    p1 = _at(_sweep('sine', 400.0, 600.0, 0.80, 0.25, 0.050), 0.00, 1.00)
    p2 = _at(_sweep('sine', 450.0, 650.0, 0.80, 0.20, 0.050), 0.10, 1.00)
    return _finalize(_mix(p1, p2))

def lion_territorial_roar_001():
    sw = _at(_sweep('sawtooth', 150.0, 80.0, 0.60, 0.40, 0.020), 0.00, 0.70)
    nz = _at(_noise(0.40, 0.20, 0.010, seed=700), 0.00, 0.70)
    return _finalize(_mix(sw, nz))

def elephant_trumpet_001():
    sw = _at(_sweep('square', 400.0, 600.0, 0.40, 0.30, 0.020), 0.00, 0.50)
    return _finalize(_mix(sw))

def horse_snort_001():
    nz = _at(_noise(0.30, 0.35, 0.005, seed=701), 0.00, 0.40)
    return _finalize(_mix(nz))

def horse_hoof_stone_001():
    t1 = _at(_tone('square', 300.0, 0.05, 0.30, 0.001), 0.00, 0.30)
    t2 = _at(_tone('square', 300.0, 0.05, 0.30, 0.001), 0.15, 0.30)
    return _finalize(_mix(t1, t2))

def camel_call_001():
    sw = _at(_sweep('sine', 200.0, 150.0, 0.50, 0.30, 0.050), 0.00, 0.60)
    return _finalize(_mix(sw))

def hyena_cackle_001():
    parts = []
    for i in range(5):
        a = _at(_tone('square', 600.0, 0.05, 0.20, 0.001), i*0.08, 0.50)
        parts.append(a)
    return _finalize(_mix(*parts))

def frog_pond_croak_001():
    parts = []
    for i in range(3):
        a = _at(_tone('sine', 200.0, 0.10, 0.30, 0.005), i*0.15, 0.50)
        parts.append(a)
    return _finalize(_mix(*parts))

def cicada_day_chorus_001():
    nz = _at(_noise(0.80, 0.25, 0.100, seed=702), 0.00, 0.90)
    return _finalize(_mix(nz))

def owl_wing_pass_001():
    nz = _at(_noise(0.40, 0.15, 0.050, seed=703), 0.00, 0.50)
    return _finalize(_mix(nz))

def eagle_screech_001():
    sw = _at(_sweep('sine', 2000.0, 1500.0, 0.30, 0.25, 0.005), 0.00, 0.40)
    return _finalize(_mix(sw))

def peacock_display_call_001():
    a = _at(_tone('sine', 800.0, 0.20, 0.25, 0.010), 0.00, 0.25)
    return _finalize(_mix(a))

def duck_flock_takeoff_001():
    nz = _at(_noise(0.60, 0.30, 0.050, seed=704), 0.00, 0.70)
    return _finalize(_mix(nz))

def goose_warning_call_001():
    a = _at(_tone('square', 400.0, 0.15, 0.30, 0.005), 0.00, 0.20)
    return _finalize(_mix(a))

def dolphin_click_train_001():
    parts = []
    for i in range(6):
        a = _at(_tone('sine', 3000.0, 0.01, 0.20, 0.001), i*0.04, 0.30)
        parts.append(a)
    return _finalize(_mix(*parts))

def whale_song_low_001():
    sw = _at(_sweep('sine', 100.0, 150.0, 1.00, 0.35, 0.100), 0.00, 1.20)
    return _finalize(_mix(sw))

def seal_colony_call_001():
    a = _at(_tone('sawtooth', 300.0, 0.15, 0.25, 0.010), 0.00, 0.20)
    return _finalize(_mix(a))

def cricket_single_call_001():
    a = _at(_tone('sine', 4000.0, 0.05, 0.20, 0.001), 0.00, 0.10)
    return _finalize(_mix(a))

def bees_swarm_pass_001():
    nz = _at(_noise(0.80, 0.30, 0.050, seed=705), 0.00, 0.90)
    return _finalize(_mix(nz))

def mosquito_near_ear_001():
    a = _at(_tone('sine', 6000.0, 0.40, 0.15, 0.010), 0.00, 0.50)
    return _finalize(_mix(a))

def snake_hiss_long_001():
    nz = _at(_noise(0.80, 0.30, 0.050, seed=706), 0.00, 0.90)
    return _finalize(_mix(nz))

def crocodile_water_movement_001():
    nz = _at(_noise(0.60, 0.25, 0.050, seed=707), 0.00, 0.70)
    return _finalize(_mix(nz))

def monkey_canopy_leap_001():
    nz = _at(_noise(0.30, 0.25, 0.020, seed=708), 0.00, 0.40)
    return _finalize(_mix(nz))

def boar_ground_snuffle_001():
    nz = _at(_noise(0.40, 0.30, 0.020, seed=709), 0.00, 0.50)
    return _finalize(_mix(nz))

def deer_alarm_bark_001():
    a = _at(_tone('square', 400.0, 0.10, 0.30, 0.002), 0.00, 0.15)
    return _finalize(_mix(a))

OFFICIAL_PRESETS_ANIMALS = {
    'wolf-pack-howling-001': wolf_pack_howling_001,
    'lion-territorial-roar-001': lion_territorial_roar_001,
    'elephant-trumpet-001': elephant_trumpet_001,
    'horse-snort-001': horse_snort_001,
    'horse-hoof-stone-001': horse_hoof_stone_001,
    'camel-call-001': camel_call_001,
    'hyena-cackle-001': hyena_cackle_001,
    'frog-pond-croak-001': frog_pond_croak_001,
    'cicada-day-chorus-001': cicada_day_chorus_001,
    'owl-wing-pass-001': owl_wing_pass_001,
    'eagle-screech-001': eagle_screech_001,
    'peacock-display-call-001': peacock_display_call_001,
    'duck-flock-takeoff-001': duck_flock_takeoff_001,
    'goose-warning-call-001': goose_warning_call_001,
    'dolphin-click-train-001': dolphin_click_train_001,
    'whale-song-low-001': whale_song_low_001,
    'seal-colony-call-001': seal_colony_call_001,
    'cricket-single-call-001': cricket_single_call_001,
    'bees-swarm-pass-001': bees_swarm_pass_001,
    'mosquito-near-ear-001': mosquito_near_ear_001,
    'snake-hiss-long-001': snake_hiss_long_001,
    'crocodile-water-movement-001': crocodile_water_movement_001,
    'monkey-canopy-leap-001': monkey_canopy_leap_001,
    'boar-ground-snuffle-001': boar_ground_snuffle_001,
    'deer-alarm-bark-001': deer_alarm_bark_001,
}