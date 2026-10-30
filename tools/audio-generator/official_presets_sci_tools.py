"""Mission 6 - Scientific Instruments (25 sounds)."""
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

def sci_inst_microscope_laser_001():
    sw = _at(_sweep('sine', 2000.0, 2500.0, 0.50, 0.20, 0.010), 0.00, 0.60)
    return _finalize(_mix(sw))
def sci_inst_spectrometer_scan_001():
    sw = _at(_sweep('sawtooth', 100.0, 1500.0, 1.20, 0.25, 0.050), 0.00, 1.30)
    return _finalize(_mix(sw))
def sci_inst_calibration_ping_001():
    a = _at(_tone('sine', 1000.0, 0.05, 0.30, 0.001), 0.00, 0.10)
    return _finalize(_mix(a))
def sci_inst_centrifuge_spin_001():
    sw = _at(_sweep('square', 50.0, 200.0, 1.50, 0.20, 0.100), 0.00, 1.60)
    return _finalize(_mix(sw))
def sci_inst_dna_sequencer_001():
    parts = []
    for i in range(8): parts.append(_at(_tone('triangle', 600.0 + i*50, 0.05, 0.15, 0.001), i*0.06, 0.50))
    return _finalize(_mix(*parts))
def sci_inst_electron_beam_001():
    nz = _at(_noise(0.30, 0.40, 0.010, seed=2500), 0.00, 0.40)
    return _finalize(_mix(nz))
def sci_inst_radar_sweep_001():
    sw = _at(_sweep('sine', 800.0, 1200.0, 0.60, 0.20, 0.020), 0.00, 0.70)
    return _finalize(_mix(sw))
def sci_inst_sonar_ping_001():
    a = _at(_tone('sine', 1500.0, 0.10, 0.25, 0.001), 0.00, 0.20)
    return _finalize(_mix(a))
def sci_inst_telescope_focus_001():
    sw = _at(_sweep('sine', 400.0, 500.0, 0.40, 0.20, 0.010), 0.00, 0.50)
    return _finalize(_mix(sw))
def sci_inst_lab_door_open_001():
    sw = _at(_sweep('sawtooth', 100.0, 200.0, 0.80, 0.25, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))
def sci_inst_lab_door_close_001():
    sw = _at(_sweep('sawtooth', 200.0, 100.0, 0.80, 0.25, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))
def sci_inst_chemical_analysis_001():
    nz = _at(_noise(0.60, 0.30, 0.020, seed=2501), 0.00, 0.70)
    return _finalize(_mix(nz))
def sci_inst_vacuum_pump_001():
    sw = _at(_sweep('square', 80.0, 120.0, 1.00, 0.25, 0.050), 0.00, 1.10)
    return _finalize(_mix(sw))
def sci_inst_spectrum_analyzer_001():
    parts = []
    for i in range(5): parts.append(_at(_tone('sine', 1000.0 + i*200, 0.10, 0.15, 0.005), i*0.10, 0.50))
    return _finalize(_mix(*parts))
def sci_inst_microscope_slide_001():
    nz = _at(_noise(0.05, 0.25, 0.001, seed=2502), 0.00, 0.10)
    a = _at(_tone('sine', 800.0, 0.05, 0.20, 0.001), 0.00, 0.10)
    return _finalize(_mix(nz, a))
def sci_inst_cryo_analysis_001():
    sw = _at(_sweep('sine', 1000.0, 200.0, 0.80, 0.25, 0.020), 0.00, 0.90)
    return _finalize(_mix(sw))
def sci_inst_particle_accelerator_001():
    sw = _at(_sweep('sawtooth', 200.0, 2000.0, 1.50, 0.30, 0.100), 0.00, 1.60)
    return _finalize(_mix(sw))
def sci_inst_laser_calibration_001():
    a = _at(_tone('square', 1200.0, 0.05, 0.20, 0.001), 0.00, 0.10)
    b = _at(_tone('square', 1200.0, 0.05, 0.20, 0.001), 0.15, 0.10)
    return _finalize(_mix(a, b))
def sci_inst_radiation_detector_001():
    parts = []
    for i in range(6): parts.append(_at(_noise(0.02, 0.30, 0.001, seed=2503+i), i*0.08, 0.40))
    return _finalize(_mix(*parts))
def sci_inst_dna_helix_scan_001():
    parts = []
    for i in range(4): parts.append(_at(_tone('sine', 400.0 + i*100, 0.15, 0.20, 0.010), i*0.10, 0.50))
    return _finalize(_mix(*parts))
def sci_inst_chemical_synthesizer_001():
    sw = _at(_sweep('sawtooth', 300.0, 600.0, 0.60, 0.25, 0.050), 0.00, 0.70)
    return _finalize(_mix(sw))
def sci_inst_lab_diagnostic_001():
    a = _at(_tone('sine', 1500.0, 0.10, 0.25, 0.001), 0.00, 0.20)
    b = _at(_tone('sine', 1800.0, 0.15, 0.25, 0.001), 0.10, 0.20)
    return _finalize(_mix(a, b))
def sci_inst_microscope_zoom_001():
    sw = _at(_sweep('sine', 400.0, 800.0, 0.40, 0.20, 0.010), 0.00, 0.50)
    return _finalize(_mix(sw))
def sci_inst_experimental_pulse_001():
    parts = []
    for i in range(3): parts.append(_at(_tone('square', 200.0, 0.20, 0.30, 0.005), i*0.25, 0.60))
    return _finalize(_mix(*parts))
def sci_inst_lab_ambience_001():
    nz = _at(_noise(2.00, 0.15, 0.200, seed=2504), 0.00, 2.20)
    return _finalize(_mix(nz))

OFFICIAL_PRESETS_SCI_TOOLS = {
    'sci-inst-microscope-laser-001': sci_inst_microscope_laser_001, 'sci-inst-spectrometer-scan-001': sci_inst_spectrometer_scan_001,
    'sci-inst-calibration-ping-001': sci_inst_calibration_ping_001, 'sci-inst-centrifuge-spin-001': sci_inst_centrifuge_spin_001,
    'sci-inst-dna-sequencer-001': sci_inst_dna_sequencer_001, 'sci-inst-electron-beam-001': sci_inst_electron_beam_001,
    'sci-inst-radar-sweep-001': sci_inst_radar_sweep_001, 'sci-inst-sonar-ping-001': sci_inst_sonar_ping_001,
    'sci-inst-telescope-focus-001': sci_inst_telescope_focus_001, 'sci-inst-lab-door-open-001': sci_inst_lab_door_open_001,
    'sci-inst-lab-door-close-001': sci_inst_lab_door_close_001, 'sci-inst-chemical-analysis-001': sci_inst_chemical_analysis_001,
    'sci-inst-vacuum-pump-001': sci_inst_vacuum_pump_001, 'sci-inst-spectrum-analyzer-001': sci_inst_spectrum_analyzer_001,
    'sci-inst-microscope-slide-001': sci_inst_microscope_slide_001, 'sci-inst-cryo-analysis-001': sci_inst_cryo_analysis_001,
    'sci-inst-particle-accelerator-001': sci_inst_particle_accelerator_001, 'sci-inst-laser-calibration-001': sci_inst_laser_calibration_001,
    'sci-inst-radiation-detector-001': sci_inst_radiation_detector_001, 'sci-inst-dna-helix-scan-001': sci_inst_dna_helix_scan_001,
    'sci-inst-chemical-synthesizer-001': sci_inst_chemical_synthesizer_001, 'sci-inst-lab-diagnostic-001': sci_inst_lab_diagnostic_001,
    'sci-inst-microscope-zoom-001': sci_inst_microscope_zoom_001, 'sci-inst-experimental-pulse-001': sci_inst_experimental_pulse_001,
    'sci-inst-lab-ambience-001': sci_inst_lab_ambience_001,
}