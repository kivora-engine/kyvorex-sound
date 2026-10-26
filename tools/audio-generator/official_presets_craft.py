"""Mission 6 - Crafts, Masonry & Precision (25 sounds)."""
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

def craft_brick_trowel_001():
    nz = _at(_noise(0.15, 0.30, 0.010, seed=920), 0.00, 0.20)
    return _finalize(_mix(nz))

def craft_cement_mix_001():
    nz = _at(_noise(0.80, 0.30, 0.050, seed=921), 0.00, 0.90)
    return _finalize(_mix(nz))

def craft_glass_cutting_001():
    nz = _at(_noise(0.30, 0.35, 0.001, seed=922), 0.00, 0.40)
    a = _at(_tone('sine', 2000.0, 0.20, 0.15, 0.001), 0.00, 0.40)
    return _finalize(_mix(nz, a))

def craft_wood_sanding_001():
    nz = _at(_noise(0.50, 0.20, 0.020, seed=923), 0.00, 0.60)
    return _finalize(_mix(nz))

def craft_metal_filing_001():
    nz = _at(_noise(0.40, 0.25, 0.010, seed=924), 0.00, 0.50)
    return _finalize(_mix(nz))

def craft_plaster_scrape_001():
    nz = _at(_noise(0.20, 0.30, 0.005, seed=925), 0.00, 0.25)
    return _finalize(_mix(nz))

def craft_tile_cutting_001():
    nz = _at(_noise(0.15, 0.35, 0.002, seed=926), 0.00, 0.20)
    return _finalize(_mix(nz))

def craft_wire_snips_001():
    a = _at(_tone('square', 1500.0, 0.02, 0.25, 0.001), 0.00, 0.05)
    return _finalize(_mix(a))

def craft_pipe_wrench_001():
    a = _at(_tone('triangle', 400.0, 0.10, 0.30, 0.002), 0.00, 0.15)
    return _finalize(_mix(a))

def craft_tape_measure_001():
    nz = _at(_noise(0.10, 0.20, 0.001, seed=927), 0.00, 0.15)
    return _finalize(_mix(nz))

def craft_level_bubble_001():
    a = _at(_tone('sine', 1200.0, 0.05, 0.20, 0.001), 0.00, 0.10)
    return _finalize(_mix(a))

def craft_pencil_mark_001():
    nz = _at(_noise(0.05, 0.15, 0.001, seed=928), 0.00, 0.08)
    return _finalize(_mix(nz))

def craft_rivet_gun_001():
    a = _at(_tone('square', 300.0, 0.05, 0.35, 0.001), 0.00, 0.10)
    nz = _at(_noise(0.05, 0.20, 0.001, seed=929), 0.00, 0.10)
    return _finalize(_mix(a, nz))

def craft_staple_gun_001():
    a = _at(_tone('square', 800.0, 0.02, 0.30, 0.001), 0.00, 0.05)
    return _finalize(_mix(a))

def craft_caulking_gun_001():
    sw = _at(_sweep('sine', 400.0, 200.0, 0.20, 0.20, 0.010), 0.00, 0.25)
    return _finalize(_mix(sw))

def craft_paint_roller_001():
    nz = _at(_noise(0.40, 0.20, 0.020, seed=930), 0.00, 0.50)
    return _finalize(_mix(nz))

def craft_paint_brush_001():
    nz = _at(_noise(0.20, 0.15, 0.010, seed=931), 0.00, 0.25)
    return _finalize(_mix(nz))

def craft_chisel_wood_001():
    a = _at(_tone('square', 500.0, 0.05, 0.25, 0.001), 0.00, 0.10)
    nz = _at(_noise(0.05, 0.20, 0.001, seed=932), 0.00, 0.10)
    return _finalize(_mix(a, nz))

def craft_rasp_wood_001():
    nz = _at(_noise(0.30, 0.25, 0.010, seed=933), 0.00, 0.40)
    return _finalize(_mix(nz))

def craft_pvc_pipe_cut_001():
    nz = _at(_noise(0.10, 0.35, 0.001, seed=934), 0.00, 0.15)
    return _finalize(_mix(nz))

def craft_screw_driver_electric_001():
    sw = _at(_sweep('square', 400.0, 600.0, 0.30, 0.20, 0.010), 0.00, 0.40)
    return _finalize(_mix(sw))

def craft_nail_puller_001():
    nz = _at(_noise(0.10, 0.30, 0.002, seed=935), 0.00, 0.15)
    return _finalize(_mix(nz))

def craft_hacksaw_metal_001():
    nz = _at(_noise(0.40, 0.25, 0.010, seed=936), 0.00, 0.50)
    return _finalize(_mix(nz))

def craft_soldering_gun_001():
    nz = _at(_noise(0.20, 0.15, 0.050, seed=937), 0.00, 0.25)
    return _finalize(_mix(nz))

def craft_lock_picking_001():
    parts = []
    for i in range(4): parts.append(_at(_tone('sine', 2000.0 + i*100, 0.02, 0.15, 0.001), i*0.05, 0.25))
    return _finalize(_mix(*parts))

OFFICIAL_PRESETS_CRAFT = {
    'craft-brick-trowel-001': craft_brick_trowel_001, 'craft-cement-mix-001': craft_cement_mix_001,
    'craft-glass-cutting-001': craft_glass_cutting_001, 'craft-wood-sanding-001': craft_wood_sanding_001,
    'craft-metal-filing-001': craft_metal_filing_001, 'craft-plaster-scrape-001': craft_plaster_scrape_001,
    'craft-tile-cutting-001': craft_tile_cutting_001, 'craft-wire-snips-001': craft_wire_snips_001,
    'craft-pipe-wrench-001': craft_pipe_wrench_001, 'craft-tape-measure-001': craft_tape_measure_001,
    'craft-level-bubble-001': craft_level_bubble_001, 'craft-pencil-mark-001': craft_pencil_mark_001,
    'craft-rivet-gun-001': craft_rivet_gun_001, 'craft-staple-gun-001': craft_staple_gun_001,
    'craft-caulking-gun-001': craft_caulking_gun_001, 'craft-paint-roller-001': craft_paint_roller_001,
    'craft-paint-brush-001': craft_paint_brush_001, 'craft-chisel-wood-001': craft_chisel_wood_001,
    'craft-rasp-wood-001': craft_rasp_wood_001, 'craft-pvc-pipe-cut-001': craft_pvc_pipe_cut_001,
    'craft-screw-driver-electric-001': craft_screw_driver_electric_001, 'craft-nail-puller-001': craft_nail_puller_001,
    'craft-hacksaw-metal-001': craft_hacksaw_metal_001, 'craft-soldering-gun-001': craft_soldering_gun_001,
    'craft-lock-picking-001': craft_lock_picking_001,
}