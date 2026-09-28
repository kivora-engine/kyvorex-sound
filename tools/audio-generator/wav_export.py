"""WAV export - uses only the standard 'wave' and 'struct' modules."""
import os
import struct
import wave


def clamp(samples, lo=-1.0, hi=1.0):
    return [max(lo, min(hi, s)) for s in samples]


def to_pcm16(samples):
    """Convert float samples in [-1, 1] to 16-bit little-endian PCM bytes."""
    buf = bytearray()
    for s in samples:
        v = int(max(-1.0, min(1.0, s)) * 32767)
        buf.extend(struct.pack('<h', v))
    return bytes(buf)


def write_wav(path, samples, sample_rate):
    """Write a mono 16-bit PCM WAV file. Creates parent folders if needed."""
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    data = to_pcm16(clamp(samples))
    with wave.open(path, 'wb') as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(data)
    return path


def duration_of(samples, sample_rate):
    return len(samples) / float(sample_rate)