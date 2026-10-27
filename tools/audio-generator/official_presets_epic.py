"""Milestone 500 - Epic Events (15 sounds)."""
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

def epic_victory_fanfare_001():
    parts = []
    for i, f in enumerate([523.25, 659.25, 783.99, 1046.50]):
        parts.append(_at(_tone('square', f, 0.20, 0.30, 0.005), i*0.15, 0.80))
    return _finalize(_mix(*parts))
def epic_legendary_unlock_001():
    sw = _at(_sweep('sawtooth', 200.0, 2000.0, 0.60, 0.40, 0.020), 0.00, 0.70)
    return _finalize(_mix(sw))
def epic_world_reveal_001():
    sw = _at(_sweep('sine', 100.0, 800.0, 1.20, 0.30, 0.100), 0.00, 1.30)
    high = _at(_tone('sine', 2000.0, 0.80, 0.15, 0.050), 0.40, 1.30)
    return _finalize(_mix(sw, high))
def epic_power_surge_001():
    nz = _at(_noise(0.80, 0.40, 0.010, seed=1500), 0.00, 0.90)
    sw = _at(_sweep('square', 400.0, 100.0, 0.80, 0.30, 0.010), 0.00, 0.90)
    return _finalize(_mix(nz, sw))
def epic_quest_complete_massive_001():
    parts = []
    for i, f in enumerate([440.0, 554.37, 659.25, 880.0, 1108.73]):
        parts.append(_at(_tone('triangle', f, 0.25, 0.25, 0.005), i*0.10, 0.70))
    return _finalize(_mix(*parts))
def epic_transcendence_001():
    sw = _at(_sweep('sine', 300.0, 3000.0, 1.50, 0.25, 0.200), 0.00, 1.60)
    return _finalize(_mix(sw))
def epic_artifact_awaken_001():
    parts = []
    for i in range(5):
        parts.append(_at(_tone('square', 300.0 + i*100, 0.15, 0.25, 0.010), i*0.08, 0.60))
    return _finalize(_mix(*parts))
def epic_portal_destroy_001():
    sw = _at(_sweep('sawtooth', 2000.0, 50.0, 1.00, 0.50, 0.050), 0.00, 1.10)
    nz = _at(_noise(0.50, 0.30, 0.010, seed=1501), 0.50, 1.10)
    return _finalize(_mix(sw, nz))
def epic_boss_defeat_001():
    nz = _at(_noise(1.20, 0.60, 0.020, seed=1502), 0.00, 1.30)
    low = _at(_sweep('sine', 80.0, 20.0, 1.20, 0.50, 0.020), 0.00, 1.30)
    return _finalize(_mix(nz, low))
def epic_champion_crown_001():
    parts = []
    for i, f in enumerate([659.25, 783.99, 987.77, 1318.51]):
        parts.append(_at(_tone('sine', f, 0.30, 0.20, 0.010), i*0.12, 0.70))
    return _finalize(_mix(*parts))
def epic_time_shatter_001():
    nz = _at(_noise(0.40, 0.50, 0.001, seed=1503), 0.00, 0.50)
    sw = _at(_sweep('square', 1000.0, 200.0, 0.40, 0.40, 0.001), 0.00, 0.50)
    return _finalize(_mix(nz, sw))
def epic_energy_overflow_001():
    sw = _at(_sweep('sine', 100.0, 1000.0, 0.80, 0.40, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))
def epic_ancient_awakens_001():
    sw = _at(_sweep('sawtooth', 50.0, 150.0, 1.50, 0.35, 0.200), 0.00, 1.60)
    return _finalize(_mix(sw))
def epic_multiverse_collapse_001():
    nz = _at(_noise(2.00, 0.50, 0.100, seed=1504), 0.00, 2.20)
    return _finalize(_mix(nz))
def epic_final_stand_001():
    parts = []
    for i, f in enumerate([261.63, 329.63, 392.00, 523.25, 659.25, 783.99]):
        parts.append(_at(_tone('sawtooth', f, 0.40, 0.20, 0.010), i*0.10, 0.90))
    return _finalize(_mix(*parts))

OFFICIAL_PRESETS_EPIC = {
    'epic-victory-fanfare-001': epic_victory_fanfare_001, 'epic-legendary-unlock-001': epic_legendary_unlock_001,
    'epic-world-reveal-001': epic_world_reveal_001, 'epic-power-surge-001': epic_power_surge_001,
    'epic-quest-complete-massive-001': epic_quest_complete_massive_001, 'epic-transcendence-001': epic_transcendence_001,
    'epic-artifact-awaken-001': epic_artifact_awaken_001, 'epic-portal-destroy-001': epic_portal_destroy_001,
    'epic-boss-defeat-001': epic_boss_defeat_001, 'epic-champion-crown-001': epic_champion_crown_001,
    'epic-time-shatter-001': epic_time_shatter_001, 'epic-energy-overflow-001': epic_energy_overflow_001,
    'epic-ancient-awakens-001': epic_ancient_awakens_001, 'epic-multiverse-collapse-001': epic_multiverse_collapse_001,
    'epic-final-stand-001': epic_final_stand_001,
}