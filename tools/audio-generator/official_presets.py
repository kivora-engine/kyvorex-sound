"""Official catalog presets - 20 sounds.

Mirrors the JS presets in js/audio-presets.js so the generated WAV/MP3
match what the browser Preview plays.
"""
import math

from synthesis import (
    sine, square, triangle, sawtooth, white_noise, DEFAULT_SAMPLE_RATE
)

SR = DEFAULT_SAMPLE_RATE


# ---------- internal helpers ----------

def _wave_sample(wave_type, phase):
    ph = (phase / (2.0 * math.pi)) % 1.0
    if wave_type == 'sine':
        return math.sin(phase)
    if wave_type == 'square':
        return 1.0 if ph < 0.5 else -1.0
    if wave_type == 'triangle':
        return 4.0 * abs(ph - 0.5) - 1.0
    if wave_type == 'sawtooth':
        return 2.0 * ph - 1.0
    return 0.0


def _env_exp(n, attack):
    """Attack then exponential decay toward near-zero."""
    n_atk = max(1, int(attack * SR))
    if n_atk > n:
        n_atk = n
    out = []
    for i in range(n):
        if i < n_atk:
            out.append(i / float(n_atk))
        else:
            t = (i - n_atk) / float(max(1, n - n_atk))
            out.append(0.0001 ** t)
    return out


def _tone(wave_type, freq, dur, amplitude, attack):
    n = int(dur * SR)
    if n <= 0:
        return []
    env = _env_exp(n, attack)
    out = []
    for i in range(n):
        phase = 2.0 * math.pi * freq * i / SR
        s = _wave_sample(wave_type, phase)
        out.append(amplitude * s * env[i])
    return out


def _sweep(wave_type, f0, f1, dur, amplitude, attack):
    n = int(dur * SR)
    if n <= 0:
        return []
    env = _env_exp(n, attack)
    out = []
    phase = 0.0
    for i in range(n):
        t = i / float(max(1, n - 1))
        f = f0 * ((f1 / f0) ** t)
        phase += 2.0 * math.pi * f / SR
        s = _wave_sample(wave_type, phase)
        out.append(amplitude * s * env[i])
    return out


def _noise(dur, amplitude, attack, seed=1):
    n = int(dur * SR)
    if n <= 0:
        return []
    env = _env_exp(n, attack)
    raw = white_noise(dur, SR, amplitude, seed=seed)
    out = [raw[i] * env[i] for i in range(min(n, len(raw)))]
    if len(out) < n:
        out.extend([0.0] * (n - len(out)))
    return out


def _mix(*parts):
    n = max((len(p) for p in parts), default=0)
    out = [0.0] * n
    for p in parts:
        for i in range(len(p)):
            out[i] += p[i]
    return out


def _at(samples, offset_sec, total_sec):
    """Place `samples` at offset, inside a buffer of total_sec."""
    n_total = int(total_sec * SR)
    n_off = int(offset_sec * SR)
    out = [0.0] * n_total
    for i, s in enumerate(samples):
        idx = n_off + i
        if idx < n_total:
            out[idx] += s
    return out


def _pad(samples, total_sec):
    n = int(total_sec * SR)
    if len(samples) < n:
        return samples + [0.0] * (n - len(samples))
    return samples[:n]


def _finalize(samples):
    """Soft clip + normalize to a safe peak."""
    peak = max((abs(s) for s in samples), default=0.0)
    if peak == 0.0:
        return samples
    target = 0.85
    factor = target / peak if peak > target else 1.0
    return [s * factor for s in samples]


# ---------- INTERFACE ----------

def ui_click_001():
    s = _tone('square', 1500.0, 0.045, 0.32, 0.001)
    return _finalize(_pad(s, 0.08))


def ui_confirm_001():
    a = _at(_tone('sine', 660.0, 0.10, 0.32, 0.004), 0.00, 0.26)
    b = _at(_tone('sine', 880.0, 0.12, 0.32, 0.004), 0.09, 0.26)
    return _finalize(_mix(a, b))


def ui_hover_001():
    s = _tone('sine', 2200.0, 0.04, 0.22, 0.001)
    return _finalize(_pad(s, 0.06))


def ui_back_001():
    s = _sweep('triangle', 800.0, 500.0, 0.10, 0.28, 0.003)
    return _finalize(_pad(s, 0.12))


def ui_toggle_001():
    a = _at(_tone('square', 950.0, 0.04, 0.26, 0.001), 0.00, 0.12)
    b = _at(_tone('square', 650.0, 0.04, 0.26, 0.001), 0.05, 0.12)
    return _finalize(_mix(a, b))


# ---------- ALERTS ----------

def alert_error_001():
    a = _at(_tone('triangle', 520.0, 0.13, 0.34, 0.003), 0.00, 0.36)
    b = _at(_tone('triangle', 390.0, 0.15, 0.34, 0.003), 0.13, 0.36)
    return _finalize(_mix(a, b))


def alert_success_001():
    notes = [(523.25, 0.00), (659.25, 0.10), (783.99, 0.20)]
    parts = [_at(_tone('sine', f, 0.13, 0.30, 0.005), t, 0.42) for f, t in notes]
    return _finalize(_mix(*parts))


def alert_warning_001():
    a = _at(_tone('triangle', 750.0, 0.11, 0.30, 0.004), 0.00, 0.30)
    b = _at(_tone('triangle', 600.0, 0.13, 0.30, 0.004), 0.12, 0.30)
    return _finalize(_mix(a, b))


def alert_info_001():
    s = _tone('sine', 700.0, 0.20, 0.28, 0.005)
    return _finalize(_pad(s, 0.25))


# ---------- GAMEPLAY ----------

def coin_pickup_001():
    a = _at(_tone('square', 987.77, 0.09, 0.28, 0.002), 0.00, 0.36)
    b = _at(_tone('square', 1318.51, 0.24, 0.28, 0.002), 0.09, 0.36)
    return _finalize(_mix(a, b))


def jump_001():
    s = _sweep('triangle', 320.0, 1100.0, 0.20, 0.34, 0.008)
    return _finalize(_pad(s, 0.22))


def hit_impact_001():
    low = _at(_sweep('sine', 140.0, 80.0, 0.20, 0.40, 0.002), 0.00, 0.26)
    nz = _at(_noise(0.12, 0.35, 0.001, seed=11), 0.00, 0.26)
    return _finalize(_mix(low, nz))


def explosion_small_001():
    nz = _at(_noise(0.55, 0.45, 0.002, seed=7), 0.00, 0.60)
    low = _at(_sweep('sine', 180.0, 45.0, 0.50, 0.35, 0.005), 0.00, 0.60)
    return _finalize(_mix(nz, low))


def footstep_single_001():
    low = _at(_sweep('sine', 95.0, 70.0, 0.07, 0.40, 0.001), 0.00, 0.10)
    nz = _at(_noise(0.04, 0.18, 0.001, seed=101), 0.00, 0.10)
    return _finalize(_mix(low, nz))


def damage_player_001():
    sw = _at(_sweep('sawtooth', 400.0, 150.0, 0.18, 0.32, 0.002), 0.00, 0.20)
    nz = _at(_noise(0.06, 0.18, 0.001, seed=13), 0.00, 0.20)
    return _finalize(_mix(sw, nz))


def checkpoint_001():
    a = _at(_tone('sine', 550.0, 0.11, 0.30, 0.004), 0.00, 0.30)
    b = _at(_tone('sine', 750.0, 0.14, 0.30, 0.004), 0.12, 0.30)
    return _finalize(_mix(a, b))


# ---------- SCI-FI ----------

def laser_shot_001():
    s = _sweep('sawtooth', 1800.0, 240.0, 0.18, 0.30, 0.002)
    return _finalize(_pad(s, 0.22))


def power_up_001():
    notes = [(440.0, 0.00), (554.37, 0.08), (659.25, 0.16), (880.0, 0.24)]
    parts = [_at(_tone('square', f, 0.11, 0.26, 0.003), t, 0.52) for f, t in notes]
    return _finalize(_mix(*parts))


def shield_activate_001():
    s = _sweep('triangle', 250.0, 900.0, 0.35, 0.30, 0.010)
    return _finalize(_pad(s, 0.40))


def teleport_001():
    up = _at(_sweep('sine', 300.0, 1400.0, 0.15, 0.30, 0.003), 0.00, 0.30)
    down = _at(_sweep('sine', 1400.0, 350.0, 0.15, 0.30, 0.003), 0.15, 0.30)
    return _finalize(_mix(up, down))


OFFICIAL_PRESETS = {
    'ui-click-001': ui_click_001,
    'ui-confirm-001': ui_confirm_001,
    'ui-hover-001': ui_hover_001,
    'ui-back-001': ui_back_001,
    'ui-toggle-001': ui_toggle_001,
    'alert-error-001': alert_error_001,
    'alert-success-001': alert_success_001,
    'alert-warning-001': alert_warning_001,
    'alert-info-001': alert_info_001,
    'coin-pickup-001': coin_pickup_001,
    'jump-001': jump_001,
    'hit-impact-001': hit_impact_001,
    'explosion-small-001': explosion_small_001,
    'footstep-single-001': footstep_single_001,
    'damage-player-001': damage_player_001,
    'checkpoint-001': checkpoint_001,
    'laser-shot-001': laser_shot_001,
    'power-up-001': power_up_001,
    'shield-activate-001': shield_activate_001,
    'teleport-001': teleport_001,
}