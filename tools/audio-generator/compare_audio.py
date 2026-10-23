"""Audio comparison tool - pure Python, no external dependencies."""
import wave
import struct
import math
import os
import argparse
import hashlib
import glob

def read_wav(path):
    try:
        with wave.open(path, 'rb') as wf:
            if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getframerate() != 44100:
                print(f"Warning: {path} is not standard mono 16-bit 44.1kHz")
            frames = wf.readframes(wf.getnframes())
            samples = struct.unpack(f'<{len(frames)//2}h', frames)
            return samples, wf.getframerate()
    except Exception as e:
        print(f"Error reading {path}: {e}")
        return None, None

def get_features(samples, rate):
    n = len(samples)
    if n == 0: return None
    duration = n / float(rate)
    peak = max(abs(s) for s in samples)
    rms = math.sqrt(sum(s**2 for s in samples) / n)
    
    # Zero-crossing rate
    zcr = 0
    for i in range(1, n):
        if (samples[i-1] >= 0 and samples[i] < 0) or (samples[i-1] < 0 and samples[i] >= 0):
            zcr += 1
    zcr = zcr / duration

    # Hash for exact duplicate
    raw_bytes = struct.pack(f'<{n}h', *samples)
    hash_val = hashlib.sha256(raw_bytes).hexdigest()

    return {
        'duration': duration,
        'peak': peak,
        'rms': rms,
        'zcr': zcr,
        'hash': hash_val
    }

def compare_features(f1, f2):
    if f1['hash'] == f2['hash']:
        return 100.0, "Exact duplicate (identical hash)"
    
    # Simple similarity score based on features
    scores = []
    # Duration similarity (max 1.0)
    d_diff = abs(f1['duration'] - f2['duration'])
    d_score = max(0, 1.0 - (d_diff / max(f1['duration'], f2['duration'])))
    scores.append(d_score)
    
    # RMS similarity
    r_diff = abs(f1['rms'] - f2['rms'])
    r_max = max(f1['rms'], f2['rms'])
    r_score = max(0, 1.0 - (r_diff / r_max)) if r_max > 0 else 1.0
    scores.append(r_score)
    
    # ZCR similarity
    z_diff = abs(f1['zcr'] - f2['zcr'])
    z_max = max(f1['zcr'], f2['zcr'])
    z_score = max(0, 1.0 - (z_diff / z_max)) if z_max > 0 else 1.0
    scores.append(z_score)

    final_score = sum(scores) / len(scores) * 100
    reasons = f"Dur:{d_score*100:.0f}% Energy:{r_score*100:.0f}% Texture:{z_score*100:.0f}%"
    return final_score, reasons

def main():
    parser = argparse.ArgumentParser(description="Compare WAV files for similarities")
    parser.add_argument("--new-only", action="store_true", help="Compare new sounds against existing catalog")
    parser.add_argument("--target", nargs='+', help="Specific files to compare")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    wav_dir = os.path.join(base_dir, 'audio', 'wav')

    if args.new_only:
        # Les 10 nouveaux sons d'Halloween
        new_ids = [
            "raven-caw-001", "ghost-apparition-001", "witch-laugh-001",
            "chains-rattle-001", "creepy-whisper-001", "zombie-groan-001",
            "halloween-bell-001", "pumpkin-smash-001", "cauldron-bubble-001",
            "bat-wings-flutter-001"
        ]
        new_files = [os.path.join(wav_dir, f"{sid}.wav") for sid in new_ids]
        existing_files = [f for f in glob.glob(os.path.join(wav_dir, "*.wav")) if os.path.basename(f) not in [n+".wav" for n in new_ids]]
    else:
        new_files = args.target if args.target else []
        existing_files = [f for f in glob.glob(os.path.join(wav_dir, "*.wav")) if f not in new_files]

    print(f"Chargement des {len(existing_files)} sons existants...")
    existing_data = []
    for f in existing_files:
        samples, rate = read_wav(f)
        if samples:
            existing_data.append((os.path.basename(f), get_features(samples, rate)))

    print(f"Analyse des {len(new_files)} nouveaux sons...\n")
    print(f"{'Nouveau Son':25} | {'Son Existant':25} | {'Score':5} | Raison")
    print("-" * 90)

    for nf in new_files:
        if not os.path.exists(nf):
            print(f"Manquant : {nf}")
            continue
        n_samples, n_rate = read_wav(nf)
        if not n_samples: continue
        n_feat = get_features(n_samples, n_rate)
        n_name = os.path.basename(nf)

        for ename, efeat in existing_data:
            score, reason = compare_features(n_feat, efeat)
            if score > 85.0: # Seuil d'alerte
                print(f"{n_name:25} | {ename:25} | {score:5.1f} | {reason}")

if __name__ == "__main__":
    main()