"""Amplitude envelopes - ADSR and short percussive shapes."""

def apply_envelope(samples, env):
    """Multiply samples by an envelope list (same length expected)."""
    n = min(len(samples), len(env))
    return [samples[i] * env[i] for i in range(n)]


def adsr(duration, sample_rate, attack=0.01, decay=0.05, sustain=0.7, release=0.1):
    """Classic ADSR envelope."""
    n = int(duration * sample_rate)
    if n <= 0:
        return []
    a = int(attack * sample_rate)
    d = int(decay * sample_rate)
    r = int(release * sample_rate)
    s = max(0, n - a - d - r)

    env = []
    for i in range(a):
        env.append(i / float(a))
    for i in range(d):
        t = i / float(d)
        env.append(1.0 - (1.0 - sustain) * t)
    for _ in range(s):
        env.append(sustain)
    for i in range(r):
        t = i / float(r)
        env.append(sustain * (1.0 - t))

    if len(env) < n:
        env.extend([0.0] * (n - len(env)))
    return env[:n]


def percussive(duration, sample_rate, attack=0.002, power=2.0):
    """Short percussive envelope: fast attack, exponential decay."""
    n = int(duration * sample_rate)
    if n <= 0:
        return []
    a = max(1, int(attack * sample_rate))
    env = []
    for i in range(n):
        if i < a:
            env.append(i / float(a))
        else:
            t = (i - a) / float(max(1, n - a))
            env.append(pow(max(0.0, 1.0 - t), power))
    return env