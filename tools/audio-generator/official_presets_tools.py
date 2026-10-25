"""Mission 4 - Tools & Hardware Interactions (25 sounds)."""
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

def tool_screwdriver_turn_001():
    a = _at(_tone('square', 800.0, 0.05, 0.20, 0.002), 0.00, 0.10)
    return _finalize(_mix(a))

def tool_wrench_clank_001():
    a = _at(_tone('triangle', 1000.0, 0.10, 0.30, 0.001), 0.00, 0.15)
    return _finalize(_mix(a))

def tool_saw_wood_001():
    nz = _at(_noise(0.40, 0.30, 0.010, seed=820), 0.00, 0.50)
    return _finalize(_mix(nz))

def tool_saw_metal_001():
    nz = _at(_noise(0.40, 0.30, 0.010, seed=821), 0.00, 0.50)
    return _finalize(_mix(nz))

def tool_drill_wood_001():
    sw = _at(_sweep('square', 200.0, 300.0, 0.50, 0.25, 0.010), 0.00, 0.60)
    return _finalize(_mix(sw))

def tool_drill_metal_001():
    sw = _at(_sweep('sawtooth', 400.0, 500.0, 0.50, 0.25, 0.010), 0.00, 0.60)
    return _finalize(_mix(sw))

def tool_hammer_nail_001():
    a = _at(_tone('sine', 200.0, 0.05, 0.35, 0.001), 0.00, 0.10)
    return _finalize(_mix(a))

def tool_wrench_ratchet_001():
    parts = []
    for i in range(4):
        a = _at(_tone('square', 600.0, 0.02, 0.20, 0.001), i*0.05, 0.20)
        parts.append(a)
    return _finalize(_mix(*parts))

def tool_pliers_snip_001():
    nz = _at(_noise(0.05, 0.30, 0.001, seed=822), 0.00, 0.10)
    return _finalize(_mix(nz))

def tool_sandpaper_rub_001():
    nz = _at(_noise(0.50, 0.20, 0.020, seed=823), 0.00, 0.60)
    return _finalize(_mix(nz))

def tool_tape_peel_001():
    nz = _at(_noise(0.30, 0.25, 0.010, seed=824), 0.00, 0.40)
    return _finalize(_mix(nz))

def tool_glue_apply_001():
    sw = _at(_sweep('sine', 300.0, 200.0, 0.20, 0.20, 0.010), 0.00, 0.25)
    return _finalize(_mix(sw))

def tool_glass_clink_001():
    a = _at(_tone('sine', 2500.0, 0.15, 0.25, 0.001), 0.00, 0.20)
    return _finalize(_mix(a))

def tool_metal_scrape_001():
    nz = _at(_noise(0.20, 0.30, 0.002, seed=825), 0.00, 0.25)
    return _finalize(_mix(nz))

def tool_wood_creak_001():
    nz = _at(_noise(0.30, 0.25, 0.050, seed=826), 0.00, 0.40)
    return _finalize(_mix(nz))

def tool_stone_chisel_001():
    a = _at(_tone('square', 600.0, 0.05, 0.25, 0.001), 0.00, 0.10)
    nz = _at(_noise(0.05, 0.20, 0.001, seed=827), 0.00, 0.10)
    return _finalize(_mix(a, nz))

def tool_rope_tie_001():
    nz = _at(_noise(0.15, 0.20, 0.010, seed=828), 0.00, 0.20)
    return _finalize(_mix(nz))

def tool_wire_strip_001():
    nz = _at(_noise(0.10, 0.25, 0.002, seed=829), 0.00, 0.15)
    return _finalize(_mix(nz))

def tool_solder_iron_001():
    nz = _at(_noise(0.30, 0.15, 0.050, seed=830), 0.00, 0.40)
    return _finalize(_mix(nz))

def tool_welding_arc_001():
    nz = _at(_noise(0.50, 0.40, 0.010, seed=831), 0.00, 0.60)
    return _finalize(_mix(nz))

def tool_dropping_wrench_001():
    nz = _at(_noise(0.10, 0.35, 0.001, seed=832), 0.00, 0.15)
    a = _at(_tone('triangle', 800.0, 0.10, 0.25, 0.001), 0.00, 0.15)
    return _finalize(_mix(nz, a))

def tool_picking_up_nails_001():
    parts = []
    for i in range(3):
        a = _at(_tone('sine', 1500.0, 0.02, 0.15, 0.001), i*0.05, 0.20)
        parts.append(a)
    return _finalize(_mix(*parts))

def tool_toolbox_open_001():
    a = _at(_tone('square', 300.0, 0.05, 0.25, 0.002), 0.00, 0.10)
    return _finalize(_mix(a))

def tool_toolbox_close_001():
    nz = _at(_noise(0.08, 0.30, 0.001, seed=833), 0.00, 0.12)
    return _finalize(_mix(nz))

def tool_multi_tool_switch_001():
    a = _at(_tone('square', 1200.0, 0.02, 0.20, 0.001), 0.00, 0.05)
    b = _at(_tone('square', 800.0, 0.02, 0.20, 0.001), 0.05, 0.05)
    return _finalize(_mix(a, b))

OFFICIAL_PRESETS_TOOLS = {
    'tool-screwdriver-turn-001': tool_screwdriver_turn_001, 'tool-wrench-clank-001': tool_wrench_clank_001,
    'tool-saw-wood-001': tool_saw_wood_001, 'tool-saw-metal-001': tool_saw_metal_001,
    'tool-drill-wood-001': tool_drill_wood_001, 'tool-drill-metal-001': tool_drill_metal_001,
    'tool-hammer-nail-001': tool_hammer_nail_001, 'tool-wrench-ratchet-001': tool_wrench_ratchet_001,
    'tool-pliers-snip-001': tool_pliers_snip_001, 'tool-sandpaper-rub-001': tool_sandpaper_rub_001,
    'tool-tape-peel-001': tool_tape_peel_001, 'tool-glue-apply-001': tool_glue_apply_001,
    'tool-glass-clink-001': tool_glass_clink_001, 'tool-metal-scrape-001': tool_metal_scrape_001,
    'tool-wood-creak-001': tool_wood_creak_001, 'tool-stone-chisel-001': tool_stone_chisel_001,
    'tool-rope-tie-001': tool_rope_tie_001, 'tool-wire-strip-001': tool_wire_strip_001,
    'tool-solder-iron-001': tool_solder_iron_001, 'tool-welding-arc-001': tool_welding_arc_001,
    'tool-dropping-wrench-001': tool_dropping_wrench_001, 'tool-picking-up-nails-001': tool_picking_up_nails_001,
    'tool-toolbox-open-001': tool_toolbox_open_001, 'tool-toolbox-close-001': tool_toolbox_close_001,
    'tool-multi-tool-switch-001': tool_multi_tool_switch_001,
}