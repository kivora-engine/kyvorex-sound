"""Mission 15 - injection des 25 sons (Percussion & Musical Textures) dans data/catalog/interface.json.
Lancer depuis la racine du projet : python3 tools/audio-generator/inject_mission_15.py
Le script peut etre relance sans danger : un son deja present est ignore.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG_DIR = os.path.join(ROOT, 'data', 'catalog')

DATE_STR = "2026-10-31"
LICENSE_STR = "KYVOREX Free Sound License 1.0"
CATEGORY = "Interface"
TARGET_FILE = "interface.json"

SOUNDS = [
    ('perc-sub-kick-808-001', 'Sub Kick 808 001', 'A deep synthetic sub kick with a long falling tone and a tiny click.',
     ['perc', 'kick', 'sub', '808', 'drum', 'percussion', 'grosse-caisse', 'basse'],
     "0.85s"),
    ('perc-rimshot-crack-001', 'Rimshot Crack 001', 'A sharp rimshot crack with a bright click and a short wooden body.',
     ['perc', 'rimshot', 'crack', 'snare', 'drum', 'percussion', 'caisse-claire', 'sec'],
     "0.15s"),
    ('perc-hihat-pair-001', 'Hihat Pair 001', 'A closed hi-hat tick followed by a longer open hi-hat.',
     ['perc', 'hihat', 'pair', 'open', 'closed', 'percussion', 'charleston', 'cymbale'],
     "0.80s"),
    ('perc-clap-stack-001', 'Clap Stack 001', 'A layered clap built from four tightly spaced noise bursts and a short tail.',
     ['perc', 'clap', 'stack', 'hand', 'percussion', 'clap', 'mains', 'frappe'],
     "0.34s"),
    ('perc-tom-fill-descend-001', 'Tom Fill Descend 001', 'A short fill of four toms stepping down in pitch.',
     ['perc', 'tom', 'fill', 'descend', 'drum', 'percussion', 'tom', 'roulement'],
     "0.77s"),
    ('perc-woodblock-duo-001', 'Woodblock Duo 001', 'Two woodblock hits, a high one followed by a lower one.',
     ['perc', 'woodblock', 'duo', 'wood', 'percussion', 'bloc', 'bois', 'tock'],
     "0.32s"),
    ('perc-cowbell-clank-001', 'Cowbell Clank 001', 'A clanking cowbell hit built from two detuned square tones.',
     ['perc', 'cowbell', 'clank', 'metal', 'percussion', 'cloche', 'vache', 'metal'],
     "0.45s"),
    ('perc-conga-slap-001', 'Conga Slap 001', 'A conga slap with a sharp attack, followed by a quieter open tone.',
     ['perc', 'conga', 'slap', 'hand', 'percussion', 'conga', 'main', 'frappe'],
     "0.66s"),
    ('perc-shaker-pattern-001', 'Shaker Pattern 001', 'A shaker plays an accented eight-beat pattern.',
     ['perc', 'shaker', 'pattern', 'rhythm', 'percussion', 'maracas', 'rythme', 'secouer'],
     "1.16s"),
    ('perc-tambourine-shake-001', 'Tambourine Shake 001', 'A tambourine shake with a head hit, a spray of jingles and metallic rings.',
     ['perc', 'tambourine', 'shake', 'jingle', 'percussion', 'tambourin', 'secouer', 'grelot'],
     "0.87s"),
    ('perc-gong-partials-001', 'Gong Partials 001', 'A large gong struck once, its inharmonic partials blooming and fading over three seconds.',
     ['perc', 'gong', 'partials', 'metal', 'resonance', 'gong', 'metal', 'resonance'],
     "2.05s"),
    ('perc-metal-pipe-ring-001', 'Metal Pipe Ring 001', 'A metal pipe is struck and rings with bright inharmonic overtones.',
     ['perc', 'metal', 'pipe', 'ring', 'strike', 'tuyau', 'metal', 'frappe'],
     "1.05s"),
    ('perc-singing-bowl-001', 'Singing Bowl 001', 'A singing bowl rings softly with slowly beating tones.',
     ['perc', 'singing', 'bowl', 'beat', 'ring', 'bol', 'chantant', 'resonance'],
     "1.95s"),
    ('perc-kalimba-tine-001', 'Kalimba Tine 001', 'A kalimba tine plucked with a soft click, a bell-like tone and a short upper partial.',
     ['perc', 'kalimba', 'tine', 'pluck', 'thumb', 'kalimba', 'lamelle', 'pincer'],
     "0.95s"),
    ('perc-taiko-deep-hit-001', 'Taiko Deep Hit 001', 'A deep taiko-style drum hit with a heavy skin thump and long body.',
     ['perc', 'taiko', 'deep', 'hit', 'drum', 'taiko', 'tambour', 'grave'],
     "1.25s"),
    ('perc-electro-tom-zap-001', 'Electro Tom Zap 001', 'An electronic tom with a fast falling sine and a snappy click.',
     ['perc', 'electro', 'tom', 'zap', 'synth', 'electro', 'synthetique', 'tom'],
     "0.45s"),
    ('perc-chip-snare-001', 'Chip Snare 001', 'An 8-bit style snare with a square tone drop and stepped noise bursts.',
     ['perc', 'chip', 'snare', '8bit', 'retro', 'puce', 'caisse-claire', 'retro'],
     "0.13s"),
    ('perc-reverse-swell-riser-001', 'Reverse Swell Riser 001', 'A reverse-style swell that rises for over a second and cuts off at its peak.',
     ['perc', 'reverse', 'swell', 'riser', 'transition', 'montee', 'transition', 'inverse'],
     "1.46s"),
    ('perc-metronome-tick-tock-001', 'Metronome Tick Tock 001', 'A metronome tick and a lower tock.',
     ['perc', 'metronome', 'tick', 'tock', 'click', 'metronome', 'tic', 'tac'],
     "0.58s"),
    ('perc-march-snare-pattern-001', 'March Snare Pattern 001', 'A marching snare pattern of nine accented strokes.',
     ['perc', 'march', 'snare', 'pattern', 'rhythm', 'marche', 'caisse-claire', 'rythme'],
     "1.31s"),
    ('perc-heartbeat-drum-001', 'Heartbeat Drum 001', 'A drum heartbeat of lub-dub pairs, the second pair softer.',
     ['perc', 'heartbeat', 'drum', 'pulse', 'thump', 'battement', 'coeur', 'pouls'],
     "1.10s"),
    ('perc-bass-pulse-sixteenths-001', 'Bass Pulse Sixteenths 001', 'A synthetic bass motif of eight short pulses with changing pitch and accents.',
     ['perc', 'bass', 'pulse', 'motif', 'synth', 'basse', 'impulsion', 'rythme'],
     "1.22s"),
    ('perc-glitch-stutter-hit-001', 'Glitch Stutter Hit 001', 'A single hit stutters with shrinking gaps for a glitchy transition.',
     ['perc', 'glitch', 'stutter', 'hit', 'transition', 'glitch', 'begaiement', 'transition'],
     "0.69s"),
    ('perc-transition-boom-drop-001', 'Transition Boom Drop 001', 'A short riser leads to a huge boom with a long, dark tail.',
     ['perc', 'transition', 'boom', 'drop', 'impact', 'transition', 'impact', 'grave'],
     "1.75s"),
    ('perc-tin-shimmer-wash-001', 'Tin Shimmer Wash 001', 'A wash of bright, inharmonic tin-like partials that shimmer and fade.',
     ['perc', 'tin', 'shimmer', 'wash', 'texture', 'etain', 'brillant', 'texture'],
     "1.95s"),
]

def load(name):
    with open(os.path.join(CATALOG_DIR, name), 'r', encoding='utf-8') as f:
        return json.load(f)

def save(name, data):
    with open(os.path.join(CATALOG_DIR, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

def main():
    print("Injection des 25 sons de la Mission 15 (Percussion & Musical Textures)...")
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
