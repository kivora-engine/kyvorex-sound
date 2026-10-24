"""Quest & Rewards presets - 15 sounds."""
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

def _pad(samples, total_sec):
    n = int(total_sec * SR)
    if len(samples) < n: return samples + [0.0] * (n - len(samples))
    return samples[:n]

def _finalize(samples):
    peak = max((abs(s) for s in samples), default=0.0)
    if peak == 0.0: return samples
    target = 0.85
    factor = target / peak if peak > target else 1.0
    return [s * factor for s in samples]

def quest_accepted_002():
    a = _at(_tone('sine', 600.0, 0.10, 0.30, 0.004), 0.00, 0.35)
    b = _at(_tone('sine', 900.0, 0.12, 0.28, 0.004), 0.10, 0.35)
    return _finalize(_mix(a, b))

def quest_completed_001():
    notes = [(523.25, 0.0), (659.25, 0.1), (783.99, 0.2), (1046.5, 0.3)]
    parts = [_at(_tone('triangle', f, 0.15, 0.30, 0.005), t, 0.60) for f, t in notes]
    return _finalize(_mix(*parts))

def quest_failed_001():
    a = _at(_tone('sawtooth', 300.0, 0.20, 0.35, 0.005), 0.00, 0.50)
    b = _at(_tone('sawtooth', 200.0, 0.25, 0.35, 0.005), 0.20, 0.50)
    return _finalize(_mix(a, b))

def inventory_open_001():
    a = _at(_tone('triangle', 400.0, 0.08, 0.25, 0.002), 0.00, 0.15)
    b = _at(_tone('triangle', 800.0, 0.06, 0.25, 0.002), 0.08, 0.15)
    return _finalize(_mix(a, b))

def inventory_close_001():
    a = _at(_tone('triangle', 800.0, 0.08, 0.25, 0.002), 0.00, 0.15)
    b = _at(_tone('triangle', 400.0, 0.06, 0.25, 0.002), 0.08, 0.15)
    return _finalize(_mix(a, b))

def item_pickup_rare_001():
    notes = [(880.0, 0.0), (1108.73, 0.1), (1318.51, 0.2)]
    parts = [_at(_tone('sine', f, 0.20, 0.25, 0.005), t, 0.50) for f, t in notes]
    return _finalize(_mix(*parts))

def item_drop_wood_001():
    nz = _at(_noise(0.08, 0.30, 0.002, seed=109), 0.00, 0.15)
    t = _at(_tone('square', 150.0, 0.05, 0.20, 0.002), 0.00, 0.15)
    return _finalize(_mix(nz, t))

def key_item_unlock_001():
    a = _at(_tone('sine', 1200.0, 0.05, 0.20, 0.002), 0.00, 0.20)
    b = _at(_tone('sine', 1600.0, 0.10, 0.25, 0.003), 0.05, 0.20)
    return _finalize(_mix(a, b))

def treasure_chest_open_001():
    nz = _at(_noise(0.15, 0.25, 0.005, seed=110), 0.00, 0.30)
    t = _at(_tone('triangle', 300.0, 0.20, 0.30, 0.005), 0.10, 0.30)
    return _finalize(_mix(nz, t))

def treasure_chest_close_001():
    nz = _at(_noise(0.10, 0.25, 0.002, seed=111), 0.00, 0.20)
    t = _at(_tone('square', 200.0, 0.10, 0.30, 0.002), 0.05, 0.20)
    return _finalize(_mix(nz, t))

def secret_discovered_001():
    up = _at(_sweep('sine', 200.0, 800.0, 0.50, 0.25, 0.010), 0.00, 0.60)
    t = _at(_tone('triangle', 1200.0, 0.15, 0.20, 0.005), 0.40, 0.60)
    return _finalize(_mix(up, t))

def level_up_002():
    notes = [(440.0, 0.0), (554.37, 0.08), (659.25, 0.16), (880.0, 0.24), (1108.73, 0.32)]
    parts = [_at(_tone('square', f, 0.12, 0.25, 0.003), t, 0.60) for f, t in notes]
    return _finalize(_mix(*parts))

def experience_gain_001():
    s = _tone('sine', 1500.0, 0.10, 0.15, 0.002)
    return _finalize(_pad(s, 0.12))

def achievement_unlocked_001():
    notes = [(523.25, 0.0), (659.25, 0.1), (783.99, 0.2), (1046.5, 0.3)]
    parts = [_at(_tone('square', f, 0.15, 0.28, 0.004), t, 0.60) for f, t in notes]
    return _finalize(_mix(*parts))

def save_checkpoint_001():
    a = _at(_tone('sine', 600.0, 0.10, 0.30, 0.005), 0.00, 0.30)
    b = _at(_tone('sine', 900.0, 0.15, 0.25, 0.005), 0.10, 0.30)
    return _finalize(_mix(a, b))

OFFICIAL_PRESETS_QUESTS = {
    'quest-accepted-002': quest_accepted_002,
    'quest-completed-001': quest_completed_001,
    'quest-failed-001': quest_failed_001,
    'inventory-open-001': inventory_open_001,
    'inventory-close-001': inventory_close_001,
    'item-pickup-rare-001': item_pickup_rare_001,
    'item-drop-wood-001': item_drop_wood_001,
    'key-item-unlock-001': key_item_unlock_001,
    'treasure-chest-open-001': treasure_chest_open_001,
    'treasure-chest-close-001': treasure_chest_close_001,
    'secret-discovered-001': secret_discovered_001,
    'level-up-002': level_up_002,
    'experience-gain-001': experience_gain_001,
    'achievement-unlocked-001': achievement_unlocked_001,
    'save-checkpoint-001': save_checkpoint_001,
}