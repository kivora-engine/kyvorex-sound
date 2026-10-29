"""Missions 5 - Forge & Specialized Crafting (25 sounds)."""
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

def forge_anvil_strike_heavy_001():
    a = _at(_tone('sine', 80.0, 0.20, 0.50, 0.002), 0.00, 0.25)
    nz = _at(_noise(0.10, 0.30, 0.001, seed=2400), 0.00, 0.25)
    return _finalize(_mix(a, nz))
def forge_anvil_strike_light_001():
    a = _at(_tone('sine', 150.0, 0.10, 0.35, 0.001), 0.00, 0.15)
    return _finalize(_mix(a))
def forge_bellows_blow_001():
    nz = _at(_noise(0.80, 0.30, 0.050, seed=2401), 0.00, 0.90)
    return _finalize(_mix(nz))
def forge_tongs_clank_001():
    a = _at(_tone('triangle', 1200.0, 0.10, 0.25, 0.001), 0.00, 0.15)
    return _finalize(_mix(a))
def forge_quenching_sizzle_001():
    nz = _at(_noise(0.60, 0.40, 0.010, seed=2402), 0.00, 0.70)
    return _finalize(_mix(nz))
def forge_grindstone_spin_001():
    sw = _at(_sweep('sawtooth', 100.0, 200.0, 0.60, 0.25, 0.050), 0.00, 0.70)
    return _finalize(_mix(sw))
def forge_hammer_strike_soft_001():
    a = _at(_tone('sine', 200.0, 0.10, 0.30, 0.002), 0.00, 0.15)
    return _finalize(_mix(a))
def forge_chain_pull_001():
    parts = []
    for i in range(4): parts.append(_at(_noise(0.05, 0.25, 0.001, seed=2403+i), i*0.08, 0.40))
    return _finalize(_mix(*parts))
def forge_crucible_pour_001():
    nz = _at(_noise(0.80, 0.35, 0.020, seed=2404), 0.00, 0.90)
    return _finalize(_mix(nz))
def forge_metal_fold_001():
    nz = _at(_noise(0.30, 0.30, 0.010, seed=2405), 0.00, 0.40)
    return _finalize(_mix(nz))
def forge_anvil_ring_001():
    a = _at(_tone('sine', 800.0, 0.60, 0.25, 0.002), 0.00, 0.70)
    return _finalize(_mix(a))
def forge_coal_shovel_001():
    nz = _at(_noise(0.30, 0.25, 0.010, seed=2406), 0.00, 0.40)
    return _finalize(_mix(nz))
def forge_sparks_burst_001():
    nz = _at(_noise(0.20, 0.35, 0.001, seed=2407), 0.00, 0.25)
    return _finalize(_mix(nz))
def forge_cooling_crackle_001():
    nz = _at(_noise(0.60, 0.20, 0.050, seed=2408), 0.00, 0.70)
    return _finalize(_mix(nz))
def forge_metal_press_001():
    sw = _at(_sweep('sawtooth', 100.0, 50.0, 0.50, 0.40, 0.010), 0.00, 0.60)
    return _finalize(_mix(sw))
def forge_mold_stamp_001():
    a = _at(_tone('square', 200.0, 0.05, 0.35, 0.001), 0.00, 0.10)
    return _finalize(_mix(a))
def forge_file_metal_001():
    nz = _at(_noise(0.40, 0.20, 0.020, seed=2409), 0.00, 0.50)
    return _finalize(_mix(nz))
def forge_cut_tongs_001():
    nz = _at(_noise(0.10, 0.30, 0.001, seed=2410), 0.00, 0.15)
    a = _at(_tone('triangle', 1000.0, 0.05, 0.20, 0.001), 0.00, 0.15)
    return _finalize(_mix(nz, a))
def forge_metal_bend_001():
    sw = _at(_sweep('sine', 150.0, 100.0, 0.60, 0.25, 0.020), 0.00, 0.70)
    return _finalize(_mix(sw))
def forge_polish_leather_001():
    nz = _at(_noise(0.60, 0.15, 0.050, seed=2411), 0.00, 0.70)
    return _finalize(_mix(nz))
def forge_glue_apply_001():
    sw = _at(_sweep('sine', 400.0, 200.0, 0.40, 0.20, 0.010), 0.00, 0.50)
    return _finalize(_mix(sw))
def forge_clamp_tighten_001():
    parts = []
    for i in range(3): parts.append(_at(_tone('square', 500.0, 0.03, 0.20, 0.001), i*0.08, 0.30))
    return _finalize(_mix(*parts))
def forge_rivet_gun_001():
    a = _at(_tone('square', 300.0, 0.05, 0.35, 0.001), 0.00, 0.10)
    nz = _at(_noise(0.05, 0.20, 0.001, seed=2412), 0.00, 0.10)
    return _finalize(_mix(a, nz))
def forge_weld_seam_001():
    nz = _at(_noise(0.30, 0.40, 0.010, seed=2413), 0.00, 0.40)
    return _finalize(_mix(nz))
def forge_workshop_ambience_001():
    nz = _at(_noise(1.50, 0.15, 0.100, seed=2414), 0.00, 1.60)
    return _finalize(_mix(nz))

OFFICIAL_PRESETS_FORGE = {
    'forge-anvil-strike-heavy-001': forge_anvil_strike_heavy_001, 'forge-anvil-strike-light-001': forge_anvil_strike_light_001,
    'forge-bellows-blow-001': forge_bellows_blow_001, 'forge-tongs-clank-001': forge_tongs_clank_001,
    'forge-quenching-sizzle-001': forge_quenching_sizzle_001, 'forge-grindstone-spin-001': forge_grindstone_spin_001,
    'forge-hammer-strike-soft-001': forge_hammer_strike_soft_001, 'forge-chain-pull-001': forge_chain_pull_001,
    'forge-crucible-pour-001': forge_crucible_pour_001, 'forge-metal-fold-001': forge_metal_fold_001,
    'forge-anvil-ring-001': forge_anvil_ring_001, 'forge-coal-shovel-001': forge_coal_shovel_001,
    'forge-sparks-burst-001': forge_sparks_burst_001, 'forge-cooling-crackle-001': forge_cooling_crackle_001,
    'forge-metal-press-001': forge_metal_press_001, 'forge-mold-stamp-001': forge_mold_stamp_001,
    'forge-file-metal-001': forge_file_metal_001, 'forge-cut-tongs-001': forge_cut_tongs_001,
    'forge-metal-bend-001': forge_metal_bend_001, 'forge-polish-leather-001': forge_polish_leather_001,
    'forge-glue-apply-001': forge_glue_apply_001, 'forge-clamp-tighten-001': forge_clamp_tighten_001,
    'forge-rivet-gun-001': forge_rivet_gun_001, 'forge-weld-seam-001': forge_weld_seam_001,
    'forge-workshop-ambience-001': forge_workshop_ambience_001,
}