"""Basic waveform generators - Python standard library only."""
import math
import random

DEFAULT_SAMPLE_RATE = 44100


def _count(duration, sample_rate):
    n = int(duration * sample_rate)
    return n if n > 0 else 1


def sine(freq, duration, sample_rate=DEFAULT_SAMPLE_RATE, amplitude=0.5):
    n = _count(duration, sample_rate)
    w = 2.0 * math.pi * freq / sample_rate
    return [amplitude * math.sin(w * i) for i in range(n)]


def square(freq, duration, sample_rate=DEFAULT_SAMPLE_RATE, amplitude=0.5, duty=0.5):
    n = _count(duration, sample_rate)
    period = sample_rate / float(freq)
    out = []
    for i in range(n):
        phase = (i % period) / period
        out.append(amplitude if phase < duty else -amplitude)
    return out


def triangle(freq, duration, sample_rate=DEFAULT_SAMPLE_RATE, amplitude=0.5):
    n = _count(duration, sample_rate)
    period = sample_rate / float(freq)
    out = []
    for i in range(n):
        phase = (i % period) / period
        v = 4.0 * abs(phase - 0.5) - 1.0
        out.append(amplitude * v)
    return out


def sawtooth(freq, duration, sample_rate=DEFAULT_SAMPLE_RATE, amplitude=0.5):
    n = _count(duration, sample_rate)
    period = sample_rate / float(freq)
    out = []
    for i in range(n):
        phase = (i % period) / period
        out.append(amplitude * (2.0 * phase - 1.0))
    return out


def white_noise(duration, sample_rate=DEFAULT_SAMPLE_RATE, amplitude=0.5, seed=None):
    """White noise using a LOCAL random generator (no global state mutation)."""
    n = _count(duration, sample_rate)
    rng = random.Random(seed) if seed is not None else random.Random()
    return [rng.uniform(-amplitude, amplitude) for _ in range(n)]