"""Milestone 500 - Advanced Tech (15 sounds)."""
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

def tech_nanobot_swarm_001():
    nz = _at(_noise(0.80, 0.30, 0.050, seed=1600), 0.00, 0.90)
    return _finalize(_mix(nz))
def tech_antigravity_boot_001():
    sw = _at(_sweep('sine', 100.0, 400.0, 0.60, 0.30, 0.050), 0.00, 0.70)
    return _finalize(_mix(sw))
def tech_matter_compiler_001():
    parts = []
    for i in range(8):
        parts.append(_at(_tone('square', 800.0 + i*100, 0.03, 0.15, 0.001), i*0.05, 0.40))
    return _finalize(_mix(*parts))
def tech_warp_core_init_001():
    sw = _at(_sweep('sawtooth', 100.0, 1500.0, 1.00, 0.35, 0.100), 0.00, 1.10)
    return _finalize(_mix(sw))
def tech_ai_uplink_001():
    sw = _at(_sweep('sine', 2000.0, 800.0, 0.50, 0.25, 0.020), 0.00, 0.60)
    return _finalize(_mix(sw))
def tech_hologram_deploy_001():
    nz = _at(_noise(0.40, 0.30, 0.010, seed=1601), 0.00, 0.50)
    sw = _at(_sweep('square', 1000.0, 500.0, 0.40, 0.20, 0.010), 0.00, 0.50)
    return _finalize(_mix(nz, sw))
def tech_plasma_conduit_001():
    nz = _at(_noise(0.60, 0.40, 0.050, seed=1602), 0.00, 0.70)
    return _finalize(_mix(nz))
def tech_neural_link_001():
    parts = []
    for i in range(6):
        parts.append(_at(_tone('sine', 400.0 + i*100, 0.05, 0.20, 0.001), i*0.05, 0.35))
    return _finalize(_mix(*parts))
def tech_energy_siphon_001():
    sw = _at(_sweep('sawtooth', 800.0, 100.0, 0.80, 0.35, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))
def tech_quantum_entangle_001():
    a = _at(_tone('sine', 1000.0, 0.10, 0.25, 0.002), 0.00, 0.60)
    b = _at(_tone('sine', 1000.0, 0.10, 0.25, 0.002), 0.30, 0.60)
    return _finalize(_mix(a, b))
def tech_phase_shift_001():
    sw = _at(_sweep('square', 400.0, 1200.0, 0.50, 0.30, 0.010), 0.00, 0.60)
    return _finalize(_mix(sw))
def tech_singularity_form_001():
    sw = _at(_sweep('sine', 50.0, 800.0, 1.50, 0.40, 0.200), 0.00, 1.60)
    return _finalize(_mix(sw))
def tech_cyber_terraform_001():
    nz = _at(_noise(1.00, 0.30, 0.100, seed=1603), 0.00, 1.10)
    return _finalize(_mix(nz))
def tech_drone_squadron_001():
    parts = []
    for i in range(4):
        parts.append(_at(_tone('sawtooth', 300.0 + i*20, 0.15, 0.20, 0.010), i*0.10, 0.50))
    return _finalize(_mix(*parts))
def tech_system_reboot_prime_001():
    parts = []
    for i in range(5):
        parts.append(_at(_tone('sine', 200.0 + i*200, 0.10, 0.25, 0.005), i*0.10, 0.60))
    return _finalize(_mix(*parts))

OFFICIAL_PRESETS_ADV_TECH = {
    'tech-nanobot-swarm-001': tech_nanobot_swarm_001, 'tech-antigravity-boot-001': tech_antigravity_boot_001,
    'tech-matter-compiler-001': tech_matter_compiler_001, 'tech-warp-core-init-001': tech_warp_core_init_001,
    'tech-ai-uplink-001': tech_ai_uplink_001, 'tech-hologram-deploy-001': tech_hologram_deploy_001,
    'tech-plasma-conduit-001': tech_plasma_conduit_001, 'tech-neural-link-001': tech_neural_link_001,
    'tech-energy-siphon-001': tech_energy_siphon_001, 'tech-quantum-entangle-001': tech_quantum_entangle_001,
    'tech-phase-shift-001': tech_phase_shift_001, 'tech-singularity-form-001': tech_singularity_form_001,
    'tech-cyber-terraform-001': tech_cyber_terraform_001, 'tech-drone-squadron-001': tech_drone_squadron_001,
    'tech-system-reboot-prime-001': tech_system_reboot_prime_001,
}