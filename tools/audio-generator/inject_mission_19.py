"""Mission 19 - injection des 25 sons (Dimensions & Impossible Phenomena) dans data/catalog/magic-fantasy.json.
Lancer depuis la racine du projet : python3 tools/audio-generator/inject_mission_19.py
Le script peut etre relance sans danger : un son deja present est ignore.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG_DIR = os.path.join(ROOT, 'data', 'catalog')

DATE_STR = "2026-10-31"
LICENSE_STR = "KYVOREX Free Sound License 1.0"
CATEGORY = "Magic / Fantasy"
TARGET_FILE = "magic-fantasy.json"

SOUNDS = [
    ('dim-endless-staircase-001', 'Endless Staircase 001', 'Layered glides give the illusion of a tone that rises forever.',
     ['dim', 'endless', 'staircase', 'illusion', 'rising', 'escalier', 'infini', 'illusion'],
     "2.85s"),
    ('dim-mirror-crossing-001', 'Mirror Crossing 001', 'Passing through a mirror into another world, a reversed whoosh ends in a glassy shimmer.',
     ['dim', 'mirror', 'crossing', 'portal', 'glass', 'miroir', 'traversee', 'monde'],
     "1.15s"),
    ('dim-time-skip-stutter-001', 'Time Skip Stutter 001', 'Time stutters, repeating a slice in falling pitch before skipping ahead with a sweep.',
     ['dim', 'time', 'skip', 'stutter', 'jump', 'temps', 'saut', 'begaiement'],
     "1.25s"),
    ('dim-vacuum-implosion-001', 'Vacuum Implosion 001', 'Air rushes inward into a sudden vacuum, followed by a deep void tone.',
     ['dim', 'vacuum', 'implosion', 'void', 'suction', 'vide', 'implosion', 'aspiration'],
     "1.30s"),
    ('dim-synesthesia-chord-001', 'Synesthesia Chord 001', 'A five-note chord builds up note by note, as if sounds were taking on colors.',
     ['dim', 'synesthesia', 'chord', 'color', 'sense', 'synesthesie', 'accord', 'couleur'],
     "1.85s"),
    ('dim-reality-tear-rip-001', 'Reality Tear Rip 001', 'The fabric of reality rips open with a tearing noise, crackles and a deep rumble.',
     ['dim', 'reality', 'tear', 'rip', 'rift', 'realite', 'dechirure', 'faille'],
     "0.75s"),
    ('dim-pre-echo-swell-001', 'Pre-Echo Swell 001', 'Echoes arrive before the sound itself, growing louder until the real hit lands.',
     ['dim', 'pre', 'echo', 'swell', 'reverse', 'pre-echo', 'inverse', 'montee'],
     "1.75s"),
    ('dim-infinite-corridor-001', 'Infinite Corridor 001', 'A single hit repeats down an endless corridor as a long train of falling echoes.',
     ['dim', 'infinite', 'corridor', 'echo', 'hallway', 'infini', 'couloir', 'echo'],
     "2.62s"),
    ('dim-clone-split-detune-001', 'Clone Split Detune 001', 'One tone splits into two clones that drift apart, one rising and one falling.',
     ['dim', 'clone', 'split', 'detune', 'double', 'clone', 'division', 'desaccord'],
     "1.25s"),
    ('dim-time-bubble-slow-001', 'Time Bubble Slow 001', 'Inside a time bubble, the ticks stretch out slower and slower beneath a deep hum.',
     ['dim', 'time', 'bubble', 'slow', 'stretch', 'temps', 'bulle', 'ralenti'],
     "2.21s"),
    ('dim-time-rush-accelerate-001', 'Time Rush Accelerate 001', 'Time speeds up: ticks get faster and higher under a rising sweep, ending in a click.',
     ['dim', 'time', 'rush', 'accelerate', 'fast', 'temps', 'acceleration', 'rapide'],
     "1.79s"),
    ('dim-paradox-knot-001', 'Paradox Knot 001', 'A rising arpeggio and a falling one weave together into an impossible knot of notes.',
     ['dim', 'paradox', 'knot', 'weave', 'loop', 'paradoxe', 'noeud', 'entrelacer'],
     "1.15s"),
    ('dim-unseen-footsteps-001', 'Unseen Footsteps 001', 'Soft footsteps pass by with nobody there, beneath a faint eerie tone.',
     ['dim', 'unseen', 'footsteps', 'ghost', 'eerie', 'invisible', 'pas', 'fantome'],
     "2.05s"),
    ('dim-otherworld-wind-001', 'Otherworld Wind 001', 'An otherworldly wind howls softly with two slightly detuned drones beating beneath it.',
     ['dim', 'otherworld', 'wind', 'drone', 'eerie', 'autre-monde', 'vent', 'bourdon'],
     "2.45s"),
    ('dim-impossible-geometry-001', 'Impossible Geometry 001', 'Four chords step through shapes that should not exist, each a fifth above the last tone.',
     ['dim', 'impossible', 'geometry', 'shape', 'chord', 'geometrie', 'impossible', 'forme'],
     "1.85s"),
    ('dim-shadow-stretch-001', 'Shadow Stretch 001', 'A shadow stretches unnaturally with a sliding low drone and a faint creak.',
     ['dim', 'shadow', 'stretch', 'dark', 'drone', 'ombre', 'etirer', 'sombre'],
     "1.85s"),
    ('dim-memory-fade-001', 'Memory Fade 001', 'A memory fades away in four falling glides, each fainter than the last.',
     ['dim', 'memory', 'fade', 'forget', 'glide', 'memoire', 'oubli', 'estomper'],
     "1.85s"),
    ('dim-superposition-flicker-001', 'Superposition Flicker 001', 'Two tones flicker in a quantum superposition, switching rapidly over a steady hum.',
     ['dim', 'superposition', 'flicker', 'quantum', 'state', 'superposition', 'quantique', 'etat'],
     "1.05s"),
    ('dim-anomaly-detector-001', 'Anomaly Detector 001', 'A detector clicks faster and faster as it nears a spatial anomaly.',
     ['dim', 'anomaly', 'detector', 'geiger', 'scan', 'anomalie', 'detecteur', 'compteur'],
     "1.65s"),
    ('dim-wrong-door-knock-001', 'Wrong Door Knock 001', 'Three knocks sound on a door, and then lower knocks answer from somewhere impossible.',
     ['dim', 'wrong', 'door', 'knock', 'echo', 'mauvaise', 'porte', 'frapper'],
     "1.55s"),
    ('dim-cosmic-whale-song-001', 'Cosmic Whale Song 001', 'A vast cosmic creature sings slow, deep gliding calls that rise and then fall.',
     ['dim', 'cosmic', 'whale', 'song', 'creature', 'cosmique', 'baleine', 'chant'],
     "2.85s"),
    ('dim-spiral-descent-001', 'Spiral Descent 001', 'A spiral descent: fourteen stepped tones fall while a long glide plunges beneath them.',
     ['dim', 'spiral', 'descent', 'fall', 'vertigo', 'spirale', 'descente', 'vertige'],
     "1.45s"),
    ('dim-hourglass-reverse-001', 'Hourglass Reverse 001', 'Sand flows upward in a reversed hourglass, swelling and ending in a chime.',
     ['dim', 'hourglass', 'reverse', 'sand', 'time', 'sablier', 'inverse', 'sable'],
     "1.65s"),
    ('dim-static-between-worlds-001', 'Static Between Worlds 001', 'A radio hops between worlds: bursts of static, fragments of tones and then silence.',
     ['dim', 'static', 'between', 'worlds', 'radio', 'parasites', 'entre', 'mondes'],
     "1.20s"),
    ('dim-unraveling-threads-001', 'Unraveling Threads 001', 'Threads of reality unravel with quickening, rising ticks and a final low note.',
     ['dim', 'unraveling', 'threads', 'unravel', 'rising', 'fils', 'defaire', 'realite'],
     "1.56s"),
]

def load(name):
    with open(os.path.join(CATALOG_DIR, name), 'r', encoding='utf-8') as f:
        return json.load(f)

def save(name, data):
    with open(os.path.join(CATALOG_DIR, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

def main():
    print("Injection des 25 sons de la Mission 19 (Dimensions & Impossible Phenomena)...")
    target = load(TARGET_FILE)
    existing = set()
    for fname in os.listdir(CATALOG_DIR):
        if fname.endswith('.json'):
            for s in load(fname).get('sounds', []):
                existing.add(s['id'])
    added = 0
    for sid, name, desc, tags, dur in SOUNDS:
        if sid in existing:
            print("  deja present, ignore : " + sid)
            continue
        target['sounds'].append({
            "id": sid, "name": name, "category": CATEGORY, "description": desc, "tags": tags,
            "duration": dur, "date": DATE_STR,
            "mp3": "audio/mp3/" + sid + ".mp3", "wav": "audio/wav/" + sid + ".wav",
            "license": LICENSE_STR, "status": "available",
            "previewMode": "procedural", "wavMode": "file", "mp3Mode": "file"
        })
        added += 1
    save(TARGET_FILE, target)
    print("OK : " + str(added) + " sons ajoutes a " + TARGET_FILE)

if __name__ == '__main__':
    main()
