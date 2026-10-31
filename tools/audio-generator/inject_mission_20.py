"""Mission 20 - injection des 25 sons (Prototypes & Novel Inventions) dans data/catalog/sci-fi.json.
Lancer depuis la racine du projet : python3 tools/audio-generator/inject_mission_20.py
Le script peut etre relance sans danger : un son deja present est ignore.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG_DIR = os.path.join(ROOT, 'data', 'catalog')

DATE_STR = "2026-10-31"
LICENSE_STR = "KYVOREX Free Sound License 1.0"
CATEGORY = "Sci-Fi"
TARGET_FILE = "sci-fi.json"

SOUNDS = [
    ('proto-steam-brass-engine-wake-001', 'Steam Brass Engine Wake 001', 'A brass steam engine hisses awake and its pistons begin to thump, faster and faster.',
     ['proto', 'steam', 'brass', 'engine', 'piston', 'vapeur', 'laiton', 'moteur'],
     "1.49s"),
    ('proto-tesla-coil-arc-001', 'Tesla Coil Arc 001', 'A tesla coil sizzles with a dense buzz of electric arcs.',
     ['proto', 'tesla', 'coil', 'arc', 'electric', 'bobine', 'electrique', 'arc'],
     "0.65s"),
    ('proto-pneumatic-exosuit-step-001', 'Pneumatic Exosuit Step 001', 'A pneumatic exosuit takes two steps, each with an air hiss, a heavy clunk and a servo whirr.',
     ['proto', 'pneumatic', 'exosuit', 'step', 'mech', 'pneumatique', 'exosquelette', 'pas'],
     "0.85s"),
    ('proto-gyroscope-spinup-001', 'Gyroscope Spinup 001', 'A gyroscope spins up with a rising whine and two slightly detuned tones beating together.',
     ['proto', 'gyroscope', 'spinup', 'whine', 'spin', 'gyroscope', 'rotation', 'accelerer'],
     "1.85s"),
    ('proto-cold-fusion-flutter-001', 'Cold Fusion Flutter 001', 'An unstable cold-fusion cell flutters with bubbling pops over a trembling hum.',
     ['proto', 'cold', 'fusion', 'flutter', 'cell', 'fusion', 'froide', 'cellule'],
     "1.45s"),
    ('proto-magnet-levitation-wobble-001', 'Magnet Levitation Wobble 001', 'A magnetic levitation platform wobbles in the air with a humming tone that sways.',
     ['proto', 'magnet', 'levitation', 'wobble', 'hover', 'aimant', 'levitation', 'oscillation'],
     "1.55s"),
    ('proto-sonic-cleaner-001', 'Sonic Cleaner 001', 'An ultrasonic cleaner pulses four times with a piercing tone and bubbling noise.',
     ['proto', 'sonic', 'cleaner', 'ultrasonic', 'bubbles', 'sonique', 'nettoyeur', 'ultrason'],
     "0.76s"),
    ('proto-3d-printer-layer-scan-001', 'Printer Layer Scan 001', 'A 3D printer head sweeps across a layer and back, stepper motors ticking.',
     ['proto', '3d', 'printer', 'layer', 'stepper', 'imprimante', 'couche', 'moteur'],
     "1.10s"),
    ('proto-rain-maker-engine-001', 'Rain Maker Engine 001', 'A weather engine hums and fires a thunder pop that opens into rainfall.',
     ['proto', 'rain', 'maker', 'weather', 'engine', 'pluie', 'meteo', 'machine'],
     "1.85s"),
    ('proto-mind-reader-helmet-scan-001', 'Mind Reader Helmet Scan 001', 'A mind-reading helmet scans upward with rising sweeps and brainwave-like ticks, then locks on.',
     ['proto', 'mind', 'reader', 'helmet', 'scan', 'casque', 'cerveau', 'balayage'],
     "1.35s"),
    ('proto-gravity-lens-focus-001', 'Gravity Lens Focus 001', 'A gravity lens focuses with one tone falling and another rising until they meet in a click.',
     ['proto', 'gravity', 'lens', 'focus', 'converge', 'gravite', 'lentille', 'focaliser'],
     "1.65s"),
    ('proto-nano-swarm-assemble-001', 'Nano Swarm Assemble 001', 'Thousands of nanobots assemble into a form: a cloud of ticks that gathers into a rising tone.',
     ['proto', 'nano', 'swarm', 'assemble', 'robots', 'nanorobots', 'essaim', 'assembler'],
     "1.65s"),
    ('proto-bio-organ-pulse-001', 'Bio Organ Pulse 001', 'A lab-grown organ pulses in three wet lub-dub beats.',
     ['proto', 'bio', 'organ', 'pulse', 'heartbeat', 'organe', 'battement', 'laboratoire'],
     "1.78s"),
    ('proto-solar-sail-unfurl-001', 'Solar Sail Unfurl 001', 'A solar sail unfurls with crinkling film and a shimmering rising sweep.',
     ['proto', 'solar', 'sail', 'unfurl', 'space', 'voile', 'solaire', 'deployer'],
     "1.45s"),
    ('proto-wind-tunnel-spool-001', 'Wind Tunnel Spool 001', 'A wind tunnel spools up from a low rumble to a roaring gale, with the test rig rattling.',
     ['proto', 'wind', 'tunnel', 'spool', 'fan', 'soufflerie', 'ventilateur', 'test'],
     "1.85s"),
    ('proto-plasma-loom-weave-001', 'Plasma Loom Weave 001', 'A plasma loom weaves energy threads, its shuttle zipping back and forth over a hum.',
     ['proto', 'plasma', 'loom', 'weave', 'shuttle', 'metier', 'tisser', 'plasma'],
     "1.35s"),
    ('proto-sound-cannon-charge-fire-001', 'Sound Cannon Charge Fire 001', 'A sonic cannon charges with a rising tone and then fires a deep shockwave boom.',
     ['proto', 'sound', 'cannon', 'charge', 'shockwave', 'canon', 'sonore', 'onde'],
     "1.55s"),
    ('proto-clockwork-computer-calc-001', 'Clockwork Computer Calc 001', 'A clockwork computer clatters through a calculation and rings a bell when it has an answer.',
     ['proto', 'clockwork', 'computer', 'calculate', 'relay', 'horloge', 'calcul', 'ordinateur'],
     "1.75s"),
    ('proto-dream-recorder-wow-001', 'Dream Recorder Wow 001', 'A dream recorder plays back with a wobbling, tape-like pitch drift and a soft hiss.',
     ['proto', 'dream', 'recorder', 'tape', 'wobble', 'reve', 'enregistreur', 'bande'],
     "1.05s"),
    ('proto-robotic-bird-flap-001', 'Robotic Bird Flap 001', 'A mechanical bird beats its wings three times with servo whirs, whooshes and ticks.',
     ['proto', 'robotic', 'bird', 'flap', 'servo', 'oiseau', 'robot', 'ailes'],
     "0.75s"),
    ('proto-liquid-metal-flow-001', 'Liquid Metal Flow 001', 'Liquid metal pours and pools, rippling with glassy metallic overtones.',
     ['proto', 'liquid', 'metal', 'flow', 'pour', 'metal', 'liquide', 'couler'],
     "1.45s"),
    ('proto-holo-sculptor-ripple-001', 'Holo Sculptor Ripple 001', 'A holographic sculptor shapes a form with ascending ripple chirps and an airy shimmer.',
     ['proto', 'holo', 'sculptor', 'ripple', 'hologram', 'hologramme', 'sculpteur', 'onde'],
     "0.85s"),
    ('proto-cryo-engine-start-001', 'Cryo Engine Start 001', 'A cryogenic engine sputters to life with slowing-then-quickening coughs and a frosty crackle.',
     ['proto', 'cryo', 'engine', 'start', 'frost', 'cryo', 'moteur', 'demarrage'],
     "1.75s"),
    ('proto-gravity-hammer-charge-001', 'Gravity Hammer Charge 001', 'A gravity hammer pulses with quickening, strengthening beats and then slams down.',
     ['proto', 'gravity', 'hammer', 'charge', 'slam', 'marteau', 'gravite', 'charger'],
     "1.98s"),
    ('proto-failure-fizzle-001', 'Prototype Failure Fizzle 001', 'A prototype fails: sparks sputter, a whine falls away, and it dies with a pop and a hiss of smoke.',
     ['proto', 'failure', 'fizzle', 'spark', 'fail', 'echec', 'defaillance', 'etincelles'],
     "1.90s"),
]

def load(name):
    with open(os.path.join(CATALOG_DIR, name), 'r', encoding='utf-8') as f:
        return json.load(f)

def save(name, data):
    with open(os.path.join(CATALOG_DIR, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

def main():
    print("Injection des 25 sons de la Mission 20 (Prototypes & Novel Inventions)...")
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
