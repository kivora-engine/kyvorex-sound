"""Mission 8 - Reality & Meta-Physical Effects (25 sounds)."""
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

def fx_time_freeze_001():
    sw = _at(_sweep('sawtooth', 2000.0, 100.0, 0.8, 0.4, 0.05), 0.00, 0.90)
    return _finalize(_mix(sw))
def fx_time_rewind_001():
    sw = _at(_sweep('sine', 100.0, 1500.0, 0.6, 0.4, 0.05), 0.00, 0.70)
    return _finalize(_mix(sw))
def fx_gravity_shift_001():
    sw = _at(_sweep('triangle', 800.0, 100.0, 0.7, 0.4, 0.05), 0.00, 0.80)
    return _finalize(_mix(sw))
def fx_reality_glitch_001():
    for i in range(5):
        pass
    nz = _at(_noise(0.05, 0.5, 0.001, seed=1100), 0.00, 0.10)
    sq = _at(_tone('square', 1000.0, 0.05, 0.4, 0.001), 0.00, 0.10)
    return _finalize(_mix(nz, sq))
def fx_cloaking_device_001():
    nz = _at(_noise(0.8, 0.3, 0.05, seed=1101), 0.00, 0.90)
    sw = _at(_sweep('sine', 800.0, 200.0, 0.7, 0.2, 0.05), 0.00, 0.90)
    return _finalize(_mix(nz, sw))
def fx_mind_control_001():
    sw = _at(_sweep('sine', 100.0, 200.0, 1.0, 0.3, 0.1), 0.00, 1.10)
    return _finalize(_mix(sw))
def fx_illusion_break_001():
    nz = _at(_noise(0.2, 0.5, 0.001, seed=1102), 0.00, 0.30)
    high = _at(_tone('sine', 3000.0, 0.15, 0.3, 0.001), 0.00, 0.30)
    return _finalize(_mix(nz, high))
def fx_size_change_001():
    sw = _at(_sweep('sawtooth', 200.0, 800.0, 0.6, 0.4, 0.05), 0.00, 0.70)
    return _finalize(_mix(sw))
def fx_elemental_fusion_001():
    a = _at(_sweep('sine', 400.0, 800.0, 0.5, 0.3, 0.05), 0.00, 0.60)
    b = _at(_sweep('sine', 800.0, 400.0, 0.5, 0.3, 0.05), 0.00, 0.60)
    return _finalize(_mix(a, b))
def fx_arcane_barrier_001():
    low = _at(_tone('sine', 80.0, 1.0, 0.4, 0.01), 0.00, 1.10)
    high = _at(_tone('sine', 2000.0, 0.8, 0.1, 0.05), 0.00, 1.10)
    return _finalize(_mix(low, high))
def fx_mana_drain_001():
    sw = _at(_sweep('sine', 1000.0, 200.0, 0.8, 0.4, 0.05), 0.00, 0.90)
    return _finalize(_mix(sw))
def fx_rune_activate_001():
    nz = _at(_noise(0.5, 0.3, 0.05, seed=1103), 0.00, 0.60)
    high = _at(_tone('sine', 2500.0, 0.2, 0.3, 0.001), 0.30, 0.60)
    return _finalize(_mix(nz, high))
def fx_dimension_rift_001():
    nz = _at(_noise(1.0, 0.5, 0.05, seed=1104), 0.00, 1.10)
    low = _at(_tone('sine', 40.0, 1.0, 0.4, 0.05), 0.00, 1.10)
    return _finalize(_mix(nz, low))
def fx_telekinesis_001():
    sw = _at(_sweep('sine', 300.0, 900.0, 0.8, 0.4, 0.05), 0.00, 0.90)
    return _finalize(_mix(sw))
def fx_invisibility_001():
    nz = _at(_noise(0.6, 0.3, 0.02, seed=1105), 0.00, 0.70)
    return _finalize(_mix(nz))
def fx_possession_001():
    sw = _at(_sweep('sawtooth', 150.0, 100.0, 1.0, 0.4, 0.05), 0.00, 1.10)
    return _finalize(_mix(sw))
def fx_healing_aura_001():
    sw = _at(_sweep('sine', 400.0, 600.0, 1.0, 0.3, 0.1), 0.00, 1.10)
    return _finalize(_mix(sw))
def fx_curse_applied_001():
    sw = _at(_sweep('sawtooth', 200.0, 150.0, 0.8, 0.4, 0.05), 0.00, 0.90)
    return _finalize(_mix(sw))
def fx_blessing_received_001():
    sw = _at(_sweep('sine', 600.0, 800.0, 1.0, 0.3, 0.1), 0.00, 1.10)
    return _finalize(_mix(sw))
def fx_weapon_enchant_001():
    nz = _at(_noise(0.3, 0.3, 0.01, seed=1106), 0.00, 0.40)
    high = _at(_tone('sine', 3000.0, 0.2, 0.2, 0.01), 0.10, 0.40)
    return _finalize(_mix(nz, high))
def fx_armor_break_001():
    nz = _at(_noise(0.2, 0.5, 0.001, seed=1107), 0.00, 0.30)
    low = _at(_sweep('sine', 100.0, 50.0, 0.2, 0.4, 0.01), 0.00, 0.30)
    return _finalize(_mix(nz, low))
def fx_spirit_summon_001():
    nz = _at(_noise(1.0, 0.4, 0.05, seed=1108), 0.00, 1.10)
    return _finalize(_mix(nz))
def fx_vortex_creation_001():
    sw = _at(_sweep('sawtooth', 100.0, 300.0, 0.8, 0.4, 0.05), 0.00, 0.90)
    return _finalize(_mix(sw))
def fx_levitation_001():
    sw = _at(_sweep('sine', 300.0, 600.0, 1.0, 0.3, 0.1), 0.00, 1.10)
    return _finalize(_mix(sw))
def fx_mind_blast_001():
    nz = _at(_noise(0.2, 0.6, 0.001, seed=1109), 0.00, 0.30)
    high = _at(_tone('square', 2000.0, 0.1, 0.4, 0.001), 0.00, 0.30)
    return _finalize(_mix(nz, high))

OFFICIAL_PRESETS_FX = {
    'fx-time-freeze-001': fx_time_freeze_001, 'fx-time-rewind-001': fx_time_rewind_001,
    'fx-gravity-shift-001': fx_gravity_shift_001, 'fx-reality-glitch-001': fx_reality_glitch_001,
    'fx-cloaking-device-001': fx_cloaking_device_001, 'fx-mind-control-001': fx_mind_control_001,
    'fx-illusion-break-001': fx_illusion_break_001, 'fx-size-change-001': fx_size_change_001,
    'fx-elemental-fusion-001': fx_elemental_fusion_001, 'fx-arcane-barrier-001': fx_arcane_barrier_001,
    'fx-mana-drain-001': fx_mana_drain_001, 'fx-rune-activate-001': fx_rune_activate_001,
    'fx-dimension-rift-001': fx_dimension_rift_001, 'fx-telekinesis-001': fx_telekinesis_001,
    'fx-invisibility-001': fx_invisibility_001, 'fx-possession-001': fx_possession_001,
    'fx-healing-aura-001': fx_healing_aura_001, 'fx-curse-applied-001': fx_curse_applied_001,
    'fx-blessing-received-001': fx_blessing_received_001, 'fx-weapon-enchant-001': fx_weapon_enchant_001,
    'fx-armor-break-001': fx_armor_break_001, 'fx-spirit-summon-001': fx_spirit_summon_001,
    'fx-vortex-creation-001': fx_vortex_creation_001, 'fx-levitation-001': fx_levitation_001,
    'fx-mind-blast-001': fx_mind_blast_001,
}