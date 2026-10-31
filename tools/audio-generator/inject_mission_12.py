"""Mission 12 - injection des 25 sons (Glaciers & Geological Phenomena) dans data/catalog/environment.json.
Lancer depuis la racine du projet : python3 tools/audio-generator/inject_mission_12.py
Le script peut etre relance sans danger : un son deja present est ignore.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG_DIR = os.path.join(ROOT, 'data', 'catalog')

DATE_STR = "2026-10-31"
LICENSE_STR = "KYVOREX Free Sound License 1.0"
CATEGORY = "Environment"
TARGET_FILE = "environment.json"

SOUNDS = [
    ('geo-glacier-moulin-gurgle-001', 'Glacier Moulin Gurgle 001', 'Meltwater swirls and gurgles down a deep shaft inside a glacier.',
     ['geo', 'glacier', 'moulin', 'meltwater', 'gurgle', 'ice', 'eau', 'fonte', 'glacier'],
     "1.55s"),
    ('geo-iceberg-roll-001', 'Iceberg Roll 001', 'A huge iceberg slowly rolls over, sloshing water and groaning under its own weight.',
     ['geo', 'iceberg', 'roll', 'ice', 'sea', 'banquise', 'glace', 'mer'],
     "2.15s"),
    ('geo-icicle-snap-001', 'Icicle Snap 001', 'A thin icicle snaps off and tinkles into brittle pieces on the ground.',
     ['geo', 'icicle', 'snap', 'ice', 'brittle', 'stalactite', 'glacon', 'casser'],
     "0.58s"),
    ('geo-ice-cave-whistle-001', 'Ice Cave Whistle 001', 'Wind funnels through an ice cavern, producing an eerie hollow whistle.',
     ['geo', 'ice', 'cave', 'wind', 'whistle', 'grotte', 'vent', 'sifflement'],
     "2.05s"),
    ('geo-snow-slab-whump-001', 'Snow Slab Whump 001', 'A weak snow layer collapses with a dull whump and a hiss of settling snow.',
     ['geo', 'snow', 'slab', 'whump', 'collapse', 'neige', 'plaque', 'effondrement'],
     "0.86s"),
    ('geo-frost-crystal-glint-001', 'Frost Crystal Glint 001', 'Delicate frost crystals form with a sparkle of tiny high glints.',
     ['geo', 'frost', 'crystal', 'glint', 'sparkle', 'givre', 'cristal', 'scintiller'],
     "1.15s"),
    ('geo-frost-heave-creak-001', 'Frost Heave Creak 001', 'Freezing ground heaves upward with dull cracks and slow, groaning creaks.',
     ['geo', 'frost', 'heave', 'creak', 'ground', 'gel', 'sol', 'grincement'],
     "1.25s"),
    ('geo-scree-pebble-trickle-001', 'Scree Pebble Trickle 001', 'Loose pebbles trickle and bounce down a scree slope, slowly dying away.',
     ['geo', 'scree', 'pebble', 'trickle', 'slope', 'eboulis', 'galet', 'pente'],
     "1.01s"),
    ('geo-boulder-settle-001', 'Boulder Settle 001', 'A boulder shifts with a grinding scrape, thuds into place and lets pebbles settle.',
     ['geo', 'boulder', 'settle', 'grind', 'rock', 'rocher', 'bloc', 'tasser'],
     "0.89s"),
    ('geo-cliff-edge-crumble-001', 'Cliff Edge Crumble 001', 'The edge of a cliff crumbles away, with debris falling and thudding far below.',
     ['geo', 'cliff', 'edge', 'crumble', 'debris', 'falaise', 'effriter', 'debris'],
     "1.37s"),
    ('geo-cave-boom-echo-001', 'Cave Boom Echo 001', 'A deep boom reverberates through a cavern as four fading echoes.',
     ['geo', 'cave', 'boom', 'echo', 'cavern', 'grotte', 'echo', 'resonance'],
     "2.25s"),
    ('geo-sinkhole-collapse-001', 'Sinkhole Collapse 001', 'The ground cracks and gives way into a sinkhole, rubble falling to a final thud.',
     ['geo', 'sinkhole', 'collapse', 'ground', 'rubble', 'doline', 'effondrement', 'gouffre'],
     "1.75s"),
    ('geo-geyser-eruption-001', 'Geyser Eruption 001', 'A geyser builds with gurgles and a steam hiss, then erupts in a roaring water column.',
     ['geo', 'geyser', 'eruption', 'steam', 'water', 'vapeur', 'eau', 'jaillir'],
     "2.55s"),
    ('geo-obsidian-flake-chip-001', 'Obsidian Flake Chip 001', 'Sharp flakes of volcanic glass chip off a core, each ringing briefly.',
     ['geo', 'obsidian', 'flake', 'chip', 'glass', 'volcan', 'eclat', 'silex'],
     "0.37s"),
    ('geo-cooling-rock-tick-001', 'Cooling Rock Tick 001', 'Hot rock contracts as it cools, giving off sparse metallic ticks.',
     ['geo', 'cooling', 'rock', 'tick', 'contract', 'refroidir', 'roche', 'craquer'],
     "1.65s"),
    ('geo-geode-split-shimmer-001', 'Geode Split Shimmer 001', 'A geode cracks open and its crystal interior shimmers with glassy overtones.',
     ['geo', 'geode', 'split', 'shimmer', 'crystal', 'geode', 'cristal', 'ouvrir'],
     "0.85s"),
    ('geo-hollow-rock-tap-001', 'Hollow Rock Tap 001', 'Three taps on a rock reveal a hollow cavity behind it.',
     ['geo', 'hollow', 'rock', 'tap', 'cavity', 'creux', 'roche', 'frapper'],
     "0.85s"),
    ('geo-singing-dune-boom-001', 'Singing Dune Boom 001', 'A sand dune slips and booms with a deep, humming resonance.',
     ['geo', 'dune', 'singing', 'boom', 'sand', 'sable', 'chant', 'resonance'],
     "1.85s"),
    ('geo-drought-clay-crack-001', 'Drought Clay Crack 001', 'Dried clay splits into a web of small, dry cracks.',
     ['geo', 'drought', 'clay', 'crack', 'dry', 'secheresse', 'argile', 'fissure'],
     "0.96s"),
    ('geo-salt-crust-crunch-001', 'Salt Crust Crunch 001', 'Brittle salt crust crunches and shatters underfoot.',
     ['geo', 'salt', 'crust', 'crunch', 'brittle', 'sel', 'croute', 'craquer'],
     "0.53s"),
    ('geo-plate-stick-slip-001', 'Plate Stick Slip 001', 'Deep rock plates strain and then slip in three sudden jerks.',
     ['geo', 'plate', 'tectonic', 'slip', 'grind', 'plaque', 'tectonique', 'glissement'],
     "2.05s"),
    ('geo-volcanic-ash-fall-001', 'Volcanic Ash Fall 001', 'Fine volcanic ash drifts down with a soft hiss and tiny grains pattering.',
     ['geo', 'volcanic', 'ash', 'fall', 'fine', 'volcan', 'cendre', 'chute'],
     "1.86s"),
    ('geo-magma-chamber-throb-001', 'Magma Chamber Throb 001', 'A magma chamber pulses with slow, deep throbs under constant rumble.',
     ['geo', 'magma', 'chamber', 'throb', 'rumble', 'volcan', 'pulsation', 'grondement'],
     "2.35s"),
    ('geo-pumice-water-bump-001', 'Pumice Water Bump 001', 'Light pumice stones bump together as they float on water.',
     ['geo', 'pumice', 'water', 'bump', 'float', 'ponce', 'eau', 'flotter'],
     "0.95s"),
    ('geo-ice-shelf-chirp-001', 'Ice Shelf Chirp 001', 'A fast descending chirp zips across an ice shelf and echoes away.',
     ['geo', 'ice', 'shelf', 'chirp', 'echo', 'glace', 'banquise', 'sifflement'],
     "1.40s"),
]

def load(name):
    with open(os.path.join(CATALOG_DIR, name), 'r', encoding='utf-8') as f:
        return json.load(f)

def save(name, data):
    with open(os.path.join(CATALOG_DIR, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

def main():
    print("Injection des 25 sons de la Mission 12 (Glaciers & Geological Phenomena)...")
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
