"""Mission 10 - Reactors & Energy Phenomena (25 sounds)."""
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

def react_startup_hum_001():
    sw = _at(_sweep('sine', 50.0, 100.0, 1.50, 0.30, 0.100), 0.00, 1.60)
    return _finalize(_mix(sw))
def react_stabilize_pulse_001():
    parts = []
    for i in range(4): parts.append(_at(_tone('sine', 80.0, 0.15, 0.25, 0.005), i*0.20, 0.80))
    return _finalize(_mix(*parts))
def react_energy_surge_001():
    sw = _at(_sweep('sawtooth', 100.0, 800.0, 0.60, 0.40, 0.020), 0.00, 0.70)
    return _finalize(_mix(sw))
def react_core_overload_001():
    nz = _at(_noise(0.50, 0.50, 0.001, seed=2900), 0.00, 0.60)
    return _finalize(_mix(nz))
def react_coolant_flow_001():
    nz = _at(_noise(1.00, 0.20, 0.050, seed=2901), 0.00, 1.10)
    return _finalize(_mix(nz))
def react_field_generate_001():
    sw = _at(_sweep('sine', 200.0, 600.0, 0.80, 0.25, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))
def react_field_collapse_001():
    sw = _at(_sweep('sine', 600.0, 200.0, 0.80, 0.25, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))
def react_power_transfer_001():
    parts = []
    for i in range(3): parts.append(_at(_tone('square', 400.0 + i*100, 0.10, 0.20, 0.005), i*0.10, 0.40))
    return _finalize(_mix(*parts))
def react_containment_beep_001():
    a = _at(_tone('sine', 1500.0, 0.05, 0.20, 0.001), 0.00, 0.10)
    return _finalize(_mix(a))
def react_warning_alarm_001():
    parts = []
    for i in range(2): parts.append(_at(_tone('square', 1000.0, 0.10, 0.30, 0.002), i*0.20, 0.40))
    return _finalize(_mix(*parts))
def react_shutdown_sequence_001():
    sw = _at(_sweep('sawtooth', 300.0, 50.0, 1.20, 0.35, 0.050), 0.00, 1.30)
    return _finalize(_mix(sw))
def react_plasma_ignite_001():
    nz = _at(_noise(0.20, 0.40, 0.001, seed=2902), 0.00, 0.25)
    return _finalize(_mix(nz))
def react_magnetic_lock_001():
    a = _at(_tone('sine', 100.0, 0.10, 0.40, 0.002), 0.00, 0.15)
    return _finalize(_mix(a))
def react_energy_beam_001():
    sw = _at(_sweep('square', 1000.0, 2000.0, 0.50, 0.25, 0.010), 0.00, 0.60)
    return _finalize(_mix(sw))
def react_core_vent_001():
    nz = _at(_noise(0.60, 0.45, 0.010, seed=2903), 0.00, 0.70)
    return _finalize(_mix(nz))
def react_stabilizer_hum_001():
    a = _at(_tone('sine', 60.0, 1.50, 0.20, 0.100), 0.00, 1.60)
    return _finalize(_mix(a))
def react_power_down_001():
    sw = _at(_sweep('sine', 400.0, 50.0, 1.50, 0.35, 0.050), 0.00, 1.60)
    return _finalize(_mix(sw))
def react_emergency_purge_001():
    nz = _at(_noise(0.40, 0.60, 0.001, seed=2904), 0.00, 0.50)
    return _finalize(_mix(nz))
def react_quantum_flux_001():
    parts = []
    for i in range(5): parts.append(_at(_tone('triangle', 600.0 + i*50, 0.05, 0.15, 0.001), i*0.05, 0.30))
    return _finalize(_mix(*parts))
def react_energy_absorb_001():
    sw = _at(_sweep('sine', 800.0, 100.0, 0.80, 0.30, 0.020), 0.00, 0.90)
    return _finalize(_mix(sw))
def react_energy_release_001():
    sw = _at(_sweep('sine', 100.0, 800.0, 0.80, 0.30, 0.020), 0.00, 0.90)
    return _finalize(_mix(sw))
def react_coolant_leak_001():
    nz = _at(_noise(0.80, 0.30, 0.100, seed=2905), 0.00, 0.90)
    return _finalize(_mix(nz))
def react_reactor_ambience_001():
    nz = _at(_noise(2.00, 0.15, 0.200, seed=2906), 0.00, 2.20)
    return _finalize(_mix(nz))
def react_plasma_containment_001():
    a = _at(_tone('sine', 120.0, 1.00, 0.30, 0.050), 0.00, 1.10)
    return _finalize(_mix(a))
def react_energy_siphon_001():
    sw = _at(_sweep('sawtooth', 800.0, 100.0, 0.80, 0.35, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))

OFFICIAL_PRESETS_REACTORS = {
    'react-startup-hum-001': react_startup_hum_001, 'react-stabilize-pulse-001': react_stabilize_pulse_001,
    'react-energy-surge-001': react_energy_surge_001, 'react-core-overload-001': react_core_overload_001,
    'react-coolant-flow-001': react_coolant_flow_001, 'react-field-generate-001': react_field_generate_001,
    'react-field-collapse-001': react_field_collapse_001, 'react-power-transfer-001': react_power_transfer_001,
    'react-containment-beep-001': react_containment_beep_001, 'react-warning-alarm-001': react_warning_alarm_001,
    'react-shutdown-sequence-001': react_shutdown_sequence_001, 'react-plasma-ignite-001': react_plasma_ignite_001,
    'react-magnetic-lock-001': react_magnetic_lock_001, 'react-energy-beam-001': react_energy_beam_001,
    'react-core-vent-001': react_core_vent_001, 'react-stabilizer-hum-001': react_stabilizer_hum_001,
    'react-power-down-001': react_power_down_001, 'react-emergency-purge-001': react_emergency_purge_001,
    'react-quantum-flux-001': react_quantum_flux_001, 'react-energy-absorb-001': react_energy_absorb_001,
    'react-energy-release-001': react_energy_release_001, 'react-coolant-leak-001': react_coolant_leak_001,
    'react-reactor-ambience-001': react_reactor_ambience_001, 'react-plasma-containment-001': react_plasma_containment_001,
    'react-energy-siphon-001': react_energy_siphon_001,
}