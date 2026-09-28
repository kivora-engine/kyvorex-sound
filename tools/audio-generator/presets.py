"""Presets - test presets + 10 official catalog sounds.

Each sound is a separate function. No external sample is used.
Everything is synthesized from waveforms defined in synthesis.py.
"""
from synthesis import (
    sine, square, triangle, sawtooth, white_noise, DEFAULT_SAMPLE_RATE
)
from envelopes import adsr, percussive, apply_envelope
from effects import (
    gain, mix, concat, fade_in, fade_out, sweep, tremolo,
    soft_clip, normalize, remove_dc
)

SR = DEFAULT_SAMPLE_RATE


def _finalize(samples, fade=0.005):
    """Common cleanup: fade edges, remove DC, soft clip, normalize."""
    s = fade_in(samples, fade, SR)
    s = fade_out(s, fade, SR)
    s = remove_dc(s)
    s = soft_clip(s, 0.95)
    s = normalize(s, 0.92)
    return s


# ---------------------------------------------------------------------------
# TEST PRESETS (Day 4 - kept for engine sanity checks)
# ---------------------------------------------------------------------------

def test_tone():
    s = sine(440.0, 0.5, SR, 0.5)
    env = adsr(0.5, SR, 0.01, 0.1, 0.6, 0.15)
    return _finalize(apply_envelope(s, env))


def test_sweep():
    s = sweep(200.0, 2000.0, 0.6, SR, 0.5)
    return _finalize(s)


def test_noise():
    s = white_noise(0.3, SR, 0.5, seed=42)
    env = percussive(0.3, SR, 0.002, 2.0)
    return _finalize(apply_envelope(s, env))


def test_ui_click():
    s = square(1800.0, 0.06, SR, 0.5, 0.25)
    env = percussive(0.06, SR, 0.001, 3.0)
    return _finalize(apply_envelope(s, env), 0.005)


TEST_PRESETS = {
    "test_tone": test_tone,
    "test_sweep": test_sweep,
    "test_noise": test_noise,
    "test_ui_click": test_ui_click,
}


# ---------------------------------------------------------------------------
# OFFICIAL PRESETS (Day 5 - catalog sounds)
# ---------------------------------------------------------------------------

def ui_click_001():
    """Very short UI click. Square + short noise transient."""
    click = square(1800.0, 0.06, SR, 0.5, 0.25)
    click = apply_envelope(click, percussive(0.06, SR, 0.001, 4.0))
    noise = white_noise(0.06, SR, 0.25, seed=101)
    noise = apply_envelope(noise, percussive(0.06, SR, 0.0005, 6.0))
    return _finalize(mix(click, noise, 0.3), 0.003)


def ui_confirm_001():
    """Two ascending sine tones. Friendly confirmation."""
    a = sine(660.0, 0.10, SR, 0.4)
    a = apply_envelope(a, adsr(0.10, SR, 0.005, 0.02, 0.7, 0.04))
    b = sine(880.0, 0.20, SR, 0.4)
    b = apply_envelope(b, adsr(0.20, SR, 0.005, 0.05, 0.6, 0.12))
    return _finalize(concat(a, b), 0.005)


def alert_error_001():
    """Two descending pulses. Reads immediately as an error."""
    a = mix(sine(520.0, 0.12, SR, 0.4),
            square(520.0, 0.12, SR, 0.15), 0.4)
    a = apply_envelope(a, adsr(0.12, SR, 0.003, 0.03, 0.7, 0.05))
    b = mix(sine(380.0, 0.20, SR, 0.4),
            square(380.0, 0.20, SR, 0.15), 0.4)
    b = apply_envelope(b, adsr(0.20, SR, 0.003, 0.05, 0.6, 0.10))
    return _finalize(concat(a, b), 0.005)


def alert_success_001():
    """Three-note ascending chime (C5, E5, G5)."""
    out = []
    for f, d in [(523.0, 0.15), (659.0, 0.15), (784.0, 0.30)]:
        n = sine(f, d, SR, 0.35)
        n = apply_envelope(n, adsr(d, SR, 0.005, 0.04, 0.6, 0.08))
        out.append(n)
    return _finalize(concat(*out), 0.005)


def coin_pickup_001():
    """Classic two-note pickup (B5 then E6)."""
    a = triangle(988.0, 0.08, SR, 0.45)
    a = apply_envelope(a, adsr(0.08, SR, 0.002, 0.02, 0.7, 0.03))
    b = triangle(1319.0, 0.30, SR, 0.45)
    b = apply_envelope(b, adsr(0.30, SR, 0.002, 0.08, 0.6, 0.20))
    return _finalize(concat(a, b), 0.005)


def jump_001():
    """Rising sine sweep - movement upwards."""
    s = sweep(220.0, 900.0, 0.35, SR, 0.5)
    s = apply_envelope(s, adsr(0.35, SR, 0.01, 0.05, 0.7, 0.15))
    return _finalize(s, 0.005)


def hit_impact_001():
    """Noise burst + low thump. Short and punchy."""
    noise = white_noise(0.20, SR, 0.6, seed=202)
    noise = apply_envelope(noise, percussive(0.20, SR, 0.001, 3.5))
    thump = sine(90.0, 0.20, SR, 0.6)
    thump = apply_envelope(thump, percussive(0.20, SR, 0.002, 2.5))
    return _finalize(mix(noise, thump, 0.55), 0.003)


def explosion_small_001():
    """Layered noise + low rumble. Compact, decaying."""
    noise = white_noise(0.90, SR, 0.7, seed=303)
    noise = apply_envelope(noise, percussive(0.90, SR, 0.002, 1.8))
    noise = tremolo(noise, 18.0, 0.25, SR)

    rumble = sine(55.0, 0.90, SR, 0.5)
    rumble = apply_envelope(rumble, percussive(0.90, SR, 0.005, 2.0))
    return _finalize(mix(noise, rumble, 0.5), 0.005)


def laser_shot_001():
    """Descending fast sweep. Sci-fi laser."""
    s = sweep(2400.0, 320.0, 0.30, SR, 0.55)
    s = tremolo(s, 40.0, 0.15, SR)
    s = apply_envelope(s, percussive(0.30, SR, 0.001, 2.8))
    return _finalize(s, 0.003)


def power_up_001():
    """Ascending arpeggio (C5, E5, G5, C6). Energy build-up."""
    out = []
    notes = [(523.0, 0.12), (659.0, 0.12), (784.0, 0.12), (1047.0, 0.35)]
    for i, (f, d) in enumerate(notes):
        n = mix(sine(f, d, SR, 0.35),
                triangle(f, d, SR, 0.15), 0.4)
        rel = 0.05 if i < len(notes) - 1 else 0.15
        n = apply_envelope(n, adsr(d, SR, 0.005, 0.03, 0.6, rel))
        out.append(n)
    return _finalize(concat(*out), 0.005)


OFFICIAL_PRESETS = {
    "ui-click-001": ui_click_001,
    "ui-confirm-001": ui_confirm_001,
    "alert-error-001": alert_error_001,
    "alert-success-001": alert_success_001,
    "coin-pickup-001": coin_pickup_001,
    "jump-001": jump_001,
    "hit-impact-001": hit_impact_001,
    "explosion-small-001": explosion_small_001,
    "laser-shot-001": laser_shot_001,
    "power-up-001": power_up_001,
}