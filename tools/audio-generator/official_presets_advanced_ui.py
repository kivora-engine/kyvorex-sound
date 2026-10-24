"""Mission 7 - Advanced UI (15 sounds)."""
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

def ui_tab_switch_002():
    a = _at(_tone('triangle', 600.0, 0.03, 0.20, 0.001), 0.00, 0.08)
    b = _at(_tone('triangle', 800.0, 0.03, 0.20, 0.001), 0.04, 0.08)
    return _finalize(_mix(a, b))
def ui_panel_expand_001():
    a = _at(_sweep('sine', 300.0, 600.0, 0.20, 0.20, 0.005), 0.00, 0.25)
    return _finalize(_mix(a))
def ui_panel_collapse_001():
    a = _at(_sweep('sine', 600.0, 300.0, 0.20, 0.20, 0.005), 0.00, 0.25)
    return _finalize(_mix(a))
def ui_toggle_on_001():
    a = _at(_tone('sine', 1000.0, 0.05, 0.25, 0.001), 0.00, 0.08)
    return _finalize(_mix(a))
def ui_toggle_off_001():
    a = _at(_tone('sine', 600.0, 0.05, 0.25, 0.001), 0.00, 0.08)
    return _finalize(_mix(a))
def ui_slider_adjust_001():
    a = _at(_tone('square', 2000.0, 0.02, 0.15, 0.001), 0.00, 0.04)
    return _finalize(_mix(a))
def ui_drag_drop_002():
    a = _at(_tone('sine', 400.0, 0.05, 0.20, 0.002), 0.00, 0.10)
    nz = _at(_noise(0.03, 0.15, 0.001, seed=500), 0.00, 0.10)
    return _finalize(_mix(a, nz))
def ui_file_import_001():
    a = _at(_tone('triangle', 800.0, 0.08, 0.20, 0.002), 0.00, 0.15)
    b = _at(_tone('triangle', 1200.0, 0.10, 0.20, 0.002), 0.08, 0.15)
    return _finalize(_mix(a, b))
def ui_file_export_001():
    a = _at(_tone('triangle', 1200.0, 0.08, 0.20, 0.002), 0.00, 0.15)
    b = _at(_tone('triangle', 800.0, 0.10, 0.20, 0.002), 0.08, 0.15)
    return _finalize(_mix(a, b))
def ui_sync_start_001():
    a = _at(_sweep('sine', 400.0, 800.0, 0.30, 0.20, 0.010), 0.00, 0.40)
    return _finalize(_mix(a))
def ui_sync_complete_001():
    notes = [(523.25, 0.0), (659.25, 0.1), (880.00, 0.2)]
    parts = [_at(_tone('sine', f, 0.10, 0.20, 0.005), t, 0.30) for f, t in notes]
    return _finalize(_mix(*parts))
def ui_connection_established_001():
    a = _at(_tone('sine', 880.0, 0.05, 0.25, 0.002), 0.00, 0.10)
    b = _at(_tone('sine', 1320.0, 0.08, 0.25, 0.002), 0.05, 0.10)
    return _finalize(_mix(a, b))
def ui_connection_lost_001():
    a = _at(_tone('sawtooth', 400.0, 0.15, 0.25, 0.005), 0.00, 0.20)
    return _finalize(_mix(a))
def ui_data_processing_001():
    parts = []
    for i in range(4):
        a = _at(_tone('square', 1500.0, 0.02, 0.15, 0.001), i*0.08, 0.35)
        parts.append(a)
    return _finalize(_mix(*parts))
def ui_permission_granted_001():
    a = _at(_tone('sine', 1046.50, 0.10, 0.25, 0.002), 0.00, 0.20)
    b = _at(_tone('sine', 1318.51, 0.15, 0.25, 0.002), 0.10, 0.20)
    return _finalize(_mix(a, b))

OFFICIAL_PRESETS_ADV_UI = {
    'ui-tab-switch-002': ui_tab_switch_002,
    'ui-panel-expand-001': ui_panel_expand_001,
    'ui-panel-collapse-001': ui_panel_collapse_001,
    'ui-toggle-on-001': ui_toggle_on_001,
    'ui-toggle-off-001': ui_toggle_off_001,
    'ui-slider-adjust-001': ui_slider_adjust_001,
    'ui-drag-drop-002': ui_drag_drop_002,
    'ui-file-import-001': ui_file_import_001,
    'ui-file-export-001': ui_file_export_001,
    'ui-sync-start-001': ui_sync_start_001,
    'ui-sync-complete-001': ui_sync_complete_001,
    'ui-connection-established-001': ui_connection_established_001,
    'ui-connection-lost-001': ui_connection_lost_001,
    'ui-data-processing-001': ui_data_processing_001,
    'ui-permission-granted-001': ui_permission_granted_001,
}