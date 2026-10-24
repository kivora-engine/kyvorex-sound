"""Mission 6 - Science & Lab (15 sounds)."""
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

def lab_microscope_focus_001():
    nz = _at(_noise(0.10, 0.15, 0.005, seed=400), 0.00, 0.15)
    return _finalize(_mix(nz))
def lab_centrifuge_start_001():
    a = _at(_sweep('sawtooth', 100.0, 400.0, 0.80, 0.25, 0.050), 0.00, 1.00)
    return _finalize(_mix(a))
def lab_centrifuge_stop_001():
    a = _at(_sweep('sawtooth', 400.0, 50.0, 1.00, 0.25, 0.020), 0.00, 1.20)
    return _finalize(_mix(a))
def lab_test_tube_rack_001():
    a = _at(_tone('sine', 800.0, 0.05, 0.25, 0.001), 0.00, 0.08)
    b = _at(_tone('sine', 1200.0, 0.05, 0.20, 0.001), 0.04, 0.08)
    return _finalize(_mix(a, b))
def lab_glass_stirring_001():
    nz = _at(_noise(0.60, 0.20, 0.010, seed=401), 0.00, 0.70)
    return _finalize(_mix(nz))
def lab_liquid_dispense_001():
    a = _at(_sweep('sine', 600.0, 300.0, 0.20, 0.25, 0.005), 0.00, 0.30)
    return _finalize(_mix(a))
def lab_pipette_release_001():
    a = _at(_tone('sine', 1500.0, 0.05, 0.20, 0.001), 0.00, 0.10)
    return _finalize(_mix(a))
def lab_sample_vial_seal_001():
    a = _at(_tone('square', 400.0, 0.05, 0.20, 0.001), 0.00, 0.10)
    nz = _at(_noise(0.03, 0.15, 0.001, seed=402), 0.00, 0.10)
    return _finalize(_mix(a, nz))
def lab_chemical_reaction_fizz_001():
    nz = _at(_noise(0.80, 0.35, 0.020, seed=403), 0.00, 1.00)
    return _finalize(_mix(nz))
def lab_vacuum_pump_cycle_001():
    a = _at(_tone('square', 150.0, 0.40, 0.25, 0.010), 0.00, 0.50)
    b = _at(_tone('square', 150.0, 0.40, 0.25, 0.010), 0.50, 0.50)
    return _finalize(_mix(a, b))
def lab_spectrometer_scan_001():
    a = _at(_sweep('sine', 200.0, 1500.0, 0.50, 0.20, 0.010), 0.00, 0.60)
    return _finalize(_mix(a))
def lab_electron_microscope_pulse_001():
    a = _at(_tone('square', 2000.0, 0.03, 0.20, 0.001), 0.00, 0.05)
    b = _at(_tone('square', 2000.0, 0.03, 0.20, 0.001), 0.10, 0.05)
    return _finalize(_mix(a, b))
def lab_radiation_counter_burst_001():
    parts = []
    for i in range(5):
        nz = _at(_noise(0.01, 0.30, 0.001, seed=404+i), i*0.05, 0.30)
        parts.append(nz)
    return _finalize(_mix(*parts))
def lab_cryo_chamber_cycle_001():
    a = _at(_sweep('sine', 800.0, 200.0, 0.60, 0.25, 0.050), 0.00, 0.70)
    return _finalize(_mix(a))
def lab_experiment_complete_001():
    notes = [(523.25, 0.0), (659.25, 0.1), (783.99, 0.2)]
    parts = [_at(_tone('sine', f, 0.20, 0.25, 0.005), t, 0.40) for f, t in notes]
    return _finalize(_mix(*parts))

OFFICIAL_PRESETS_SCIENCE = {
    'lab-microscope-focus-001': lab_microscope_focus_001,
    'lab-centrifuge-start-001': lab_centrifuge_start_001,
    'lab-centrifuge-stop-001': lab_centrifuge_stop_001,
    'lab-test-tube-rack-001': lab_test_tube_rack_001,
    'lab-glass-stirring-001': lab_glass_stirring_001,
    'lab-liquid-dispense-001': lab_liquid_dispense_001,
    'lab-pipette-release-001': lab_pipette_release_001,
    'lab-sample-vial-seal-001': lab_sample_vial_seal_001,
    'lab-chemical-reaction-fizz-001': lab_chemical_reaction_fizz_001,
    'lab-vacuum-pump-cycle-001': lab_vacuum_pump_cycle_001,
    'lab-spectrometer-scan-001': lab_spectrometer_scan_001,
    'lab-electron-microscope-pulse-001': lab_electron_microscope_pulse_001,
    'lab-radiation-counter-burst-001': lab_radiation_counter_burst_001,
    'lab-cryo-chamber-cycle-001': lab_cryo_chamber_cycle_001,
    'lab-experiment-complete-001': lab_experiment_complete_001,
}