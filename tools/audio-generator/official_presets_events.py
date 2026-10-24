"""Mission 5 - Game Events (15 sounds)."""
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

def _pad(samples, total_sec):
    n = int(total_sec * SR)
    if len(samples) < n: return samples + [0.0] * (n - len(samples))
    return samples[:n]

def _finalize(samples):
    peak = max((abs(s) for s in samples), default=0.0)
    if peak == 0.0: return samples
    target = 0.85
    factor = target / peak if peak > target else 1.0
    return [s * factor for s in samples]

def game_round_start_001():
    a = _at(_tone('sine', 440.0, 0.10, 0.30, 0.005), 0.00, 0.25)
    b = _at(_tone('sine', 880.0, 0.15, 0.30, 0.005), 0.10, 0.25)
    return _finalize(_mix(a, b))

def game_round_end_001():
    a = _at(_tone('sine', 880.0, 0.10, 0.30, 0.005), 0.00, 0.25)
    b = _at(_tone('sine', 440.0, 0.15, 0.30, 0.005), 0.10, 0.25)
    return _finalize(_mix(a, b))

def game_draw_result_001():
    a = _at(_tone('triangle', 600.0, 0.15, 0.30, 0.005), 0.00, 0.30)
    b = _at(_tone('triangle', 600.0, 0.15, 0.30, 0.005), 0.20, 0.30)
    return _finalize(_mix(a, b))

def game_tie_break_start_001():
    a = _at(_sweep('sawtooth', 200.0, 800.0, 0.50, 0.30, 0.010), 0.00, 0.60)
    return _finalize(_mix(a))

def game_combo_achieved_001():
    notes = [(600, 0.0), (800, 0.08), (1000, 0.16)]
    parts = [_at(_tone('square', f, 0.10, 0.25, 0.003), t, 0.30) for f, t in notes]
    return _finalize(_mix(*parts))

def game_combo_break_001():
    a = _at(_sweep('square', 600.0, 150.0, 0.30, 0.30, 0.005), 0.00, 0.40)
    return _finalize(_mix(a))

def game_streak_milestone_001():
    notes = [(440, 0.0), (554, 0.1), (659, 0.2), (880, 0.3)]
    parts = [_at(_tone('sine', f, 0.15, 0.25, 0.005), t, 0.50) for f, t in notes]
    return _finalize(_mix(*parts))

def game_bonus_activated_001():
    a = _at(_sweep('sine', 800.0, 1200.0, 0.20, 0.30, 0.005), 0.00, 0.30)
    return _finalize(_mix(a))

def game_bonus_expired_001():
    a = _at(_sweep('sine', 1200.0, 400.0, 0.30, 0.30, 0.005), 0.00, 0.40)
    return _finalize(_mix(a))

def game_multiplier_increase_001():
    a = _at(_tone('sine', 1500.0, 0.05, 0.25, 0.002), 0.00, 0.10)
    return _finalize(_mix(a))

def game_multiplier_reset_001():
    a = _at(_tone('sine', 300.0, 0.15, 0.30, 0.005), 0.00, 0.20)
    return _finalize(_mix(a))

def game_target_locked_001():
    a = _at(_tone('square', 1000.0, 0.08, 0.25, 0.002), 0.00, 0.12)
    return _finalize(_mix(a))

def game_target_lost_001():
    a = _at(_sweep('sine', 1000.0, 600.0, 0.20, 0.30, 0.005), 0.00, 0.25)
    return _finalize(_mix(a))

def game_wave_cleared_001():
    a = _at(_tone('triangle', 523.25, 0.15, 0.30, 0.005), 0.00, 0.40)
    b = _at(_tone('triangle', 783.99, 0.25, 0.30, 0.005), 0.15, 0.40)
    return _finalize(_mix(a, b))

def game_final_result_reveal_001():
    a = _at(_sweep('sawtooth', 100.0, 400.0, 0.80, 0.30, 0.050), 0.00, 1.00)
    return _finalize(_mix(a))

OFFICIAL_PRESETS_EVENTS = {
    'game-round-start-001': game_round_start_001,
    'game-round-end-001': game_round_end_001,
    'game-draw-result-001': game_draw_result_001,
    'game-tie-break-start-001': game_tie_break_start_001,
    'game-combo-achieved-001': game_combo_achieved_001,
    'game-combo-break-001': game_combo_break_001,
    'game-streak-milestone-001': game_streak_milestone_001,
    'game-bonus-activated-001': game_bonus_activated_001,
    'game-bonus-expired-001': game_bonus_expired_001,
    'game-multiplier-increase-001': game_multiplier_increase_001,
    'game-multiplier-reset-001': game_multiplier_reset_001,
    'game-target-locked-001': game_target_locked_001,
    'game-target-lost-001': game_target_lost_001,
    'game-wave-cleared-001': game_wave_cleared_001,
    'game-final-result-reveal-001': game_final_result_reveal_001,
}