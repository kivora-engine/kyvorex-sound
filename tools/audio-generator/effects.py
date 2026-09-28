"""Simple audio effects - standard library only."""
import math


def gain(samples, factor):
    return [s * factor for s in samples]


def mix(a, b, ratio=0.5):
    n = max(len(a), len(b))
    out = [0.0] * n
    for i in range(n):
        sa = a[i] if i < len(a) else 0.0
        sb = b[i] if i < len(b) else 0.0
        out[i] = sa * (1.0 - ratio) + sb * ratio
    return out


def concat(*parts):
    out = []
    for p in parts:
        out.extend(p)
    return out


def fade_in(samples, duration, sample_rate):
    n = min(len(samples), int(duration * sample_rate))
    out = list(samples)
    if n <= 0:
        return out
    for i in range(n):
        out[i] *= i / float(n)
    return out


def fade_out(samples, duration, sample_rate):
    n = min(len(samples), int(duration * sample_rate))
    out = list(samples)
    if n <= 0:
        return out
    start = len(out) - n
    for i in range(n):
        out[start + i] *= (n - i) / float(n)
    return out


def sweep(start_freq, end_freq, duration, sample_rate, amplitude=0.5):
    n = int(duration * sample_rate)
    if n <= 0:
        return []
    out = []
    phase = 0.0
    for i in range(n):
        t = i / float(max(1, n - 1))
        f = start_freq + (end_freq - start_freq) * t
        phase += 2.0 * math.pi * f / sample_rate
        out.append(amplitude * math.sin(phase))
    return out


def tremolo(samples, rate, depth, sample_rate):
    out = []
    for i, s in enumerate(samples):
        m = 1.0 - depth + depth * (0.5 + 0.5 * math.sin(2.0 * math.pi * rate * i / sample_rate))
        out.append(s * m)
    return out


def soft_clip(samples, threshold=0.95):
    out = []
    for s in samples:
        if s > threshold:
            out.append(threshold + (s - threshold) / (1.0 + abs(s - threshold)))
        elif s < -threshold:
            out.append(-threshold + (s + threshold) / (1.0 + abs(s + threshold)))
        else:
            out.append(s)
    return out


def remove_dc(samples):
    """Subtract the mean so the signal is centered around zero."""
    if not samples:
        return list(samples)
    mean = sum(samples) / float(len(samples))
    return [s - mean for s in samples]


def peak(samples):
    return max((abs(s) for s in samples), default=0.0)


def normalize(samples, target=0.95):
    p = peak(samples)
    if p == 0.0:
        return list(samples)
    f = target / p
    return [s * f for s in samples]