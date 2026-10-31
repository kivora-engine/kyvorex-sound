"""Mission 13 - injection des 25 sons (Fortifications & Siege Machines) dans data/catalog/gameplay.json.
Lancer depuis la racine du projet : python3 tools/audio-generator/inject_mission_13.py
Le script peut etre relance sans danger : un son deja present est ignore.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG_DIR = os.path.join(ROOT, 'data', 'catalog')

DATE_STR = "2026-10-31"
LICENSE_STR = "KYVOREX Free Sound License 1.0"
CATEGORY = "Gameplay"
TARGET_FILE = "gameplay.json"

SOUNDS = [
    ('fort-drawbridge-lower-001', 'Drawbridge Lower 001', 'Chain links pay out as a drawbridge lowers and lands on the far bank with a heavy thud.',
     ['fort', 'drawbridge', 'lower', 'chain', 'castle', 'pont-levis', 'chaine', 'chateau'],
     "2.15s"),
    ('fort-drawbridge-raise-creak-001', 'Drawbridge Raise Creak 001', 'Heavy timber groans and chains strain as a drawbridge is hauled up and latches shut.',
     ['fort', 'drawbridge', 'raise', 'creak', 'timber', 'pont-levis', 'bois', 'grincement'],
     "2.45s"),
    ('fort-portcullis-drop-001', 'Portcullis Drop 001', 'An iron portcullis rattles down its grooves and slams into the ground, ringing.',
     ['fort', 'portcullis', 'drop', 'iron', 'gate', 'herse', 'fer', 'porte'],
     "1.37s"),
    ('fort-portcullis-ratchet-raise-001', 'Portcullis Ratchet Raise 001', 'A winch ratchets the portcullis upward with steady pawl clicks and a low groan.',
     ['fort', 'portcullis', 'ratchet', 'winch', 'raise', 'herse', 'cliquet', 'treuil'],
     "1.85s"),
    ('fort-gate-bar-drop-001', 'Gate Bar Drop 001', 'A heavy wooden bar drops into its brackets and settles with a deep thunk.',
     ['fort', 'gate', 'bar', 'drop', 'wood', 'porte', 'barre', 'bois'],
     "0.47s"),
    ('fort-murder-hole-pour-001', 'Murder Hole Pour 001', 'Scalding liquid is poured from the battlements, splashing and sizzling below.',
     ['fort', 'murder', 'hole', 'pour', 'oil', 'creneau', 'huile', 'verser'],
     "1.65s"),
    ('fort-longbow-twang-whoosh-001', 'Longbow Twang Whoosh 001', 'A bowstring twangs, an arrow whooshes away and thuds into its target.',
     ['fort', 'longbow', 'twang', 'arrow', 'whoosh', 'arc', 'fleche', 'corde'],
     "0.61s"),
    ('fort-crossbow-winch-latch-001', 'Crossbow Winch Latch 001', 'A crossbow is cocked with a ratcheting winch and the string catches on the latch.',
     ['fort', 'crossbow', 'winch', 'latch', 'cock', 'arbalete', 'treuil', 'armer'],
     "1.18s"),
    ('fort-ballista-release-001', 'Ballista Release 001', 'A giant ballista releases with a frame slam, a heavy twang and a rushing bolt.',
     ['fort', 'ballista', 'release', 'bolt', 'siege', 'baliste', 'trait', 'siege'],
     "0.55s"),
    ('fort-catapult-arm-swing-001', 'Catapult Arm Swing 001', 'A catapult arm creaks under tension, whips through the air and slams into its stop.',
     ['fort', 'catapult', 'arm', 'swing', 'siege', 'catapulte', 'bras', 'siege'],
     "1.35s"),
    ('fort-trebuchet-weight-drop-001', 'Trebuchet Weight Drop 001', 'A trebuchet counterweight plunges, the rope whips and the frame groans after the impact.',
     ['fort', 'trebuchet', 'counterweight', 'drop', 'siege', 'trebuchet', 'contrepoids', 'chute'],
     "1.75s"),
    ('fort-stone-incoming-whistle-001', 'Stone Incoming Whistle 001', 'A siege stone whistles through the sky and smashes into the ground with flying debris.',
     ['fort', 'stone', 'incoming', 'whistle', 'siege', 'pierre', 'sifflement', 'impact'],
     "1.91s"),
    ('fort-battering-ram-hit-001', 'Battering Ram Hit 001', 'A battering ram booms against a gate, splintering the wood with a long creak.',
     ['fort', 'battering', 'ram', 'hit', 'gate', 'belier', 'porte', 'impact'],
     "0.85s"),
    ('fort-siege-ladder-clack-001', 'Siege Ladder Clack 001', 'A siege ladder clacks against a wall, scrapes into place and wobbles.',
     ['fort', 'siege', 'ladder', 'clack', 'wall', 'echelle', 'mur', 'assaut'],
     "0.95s"),
    ('fort-siege-tower-roll-001', 'Siege Tower Roll 001', 'A towering wooden siege engine rolls slowly forward with rumbling wheels and squealing axles.',
     ['fort', 'siege', 'tower', 'roll', 'wheels', 'tour', 'roues', 'beffroi'],
     "2.85s"),
    ('fort-grapple-hook-catch-001', 'Grapple Hook Catch 001', 'A grappling hook is thrown, clinks onto the battlement and catches as the rope draws tight.',
     ['fort', 'grapple', 'hook', 'catch', 'rope', 'grappin', 'crochet', 'rempart'],
     "1.30s"),
    ('fort-war-horn-call-001', 'War Horn Call 001', 'A watchtower war horn sounds two long notes, the second higher than the first.',
     ['fort', 'war', 'horn', 'call', 'tower', 'cor', 'guerre', 'tour'],
     "1.95s"),
    ('fort-alarm-bell-frantic-001', 'Alarm Bell Frantic 001', 'A tower bell is struck in rapid, frantic alarm.',
     ['fort', 'alarm', 'bell', 'frantic', 'tower', 'cloche', 'alarme', 'tour'],
     "2.09s"),
    ('fort-stake-barricade-set-001', 'Stake Barricade Set 001', 'Sharpened wooden stakes are set into the ground one after another to form a barricade.',
     ['fort', 'stake', 'barricade', 'set', 'wood', 'pieu', 'barricade', 'bois'],
     "1.25s"),
    ('fort-shield-wall-lock-001', 'Shield Wall Lock 001', 'A line of shields slams together into a tight defensive wall.',
     ['fort', 'shield', 'wall', 'lock', 'defense', 'bouclier', 'mur', 'defense'],
     "0.93s"),
    ('fort-cell-bars-clang-001', 'Cell Bars Clang 001', 'An iron cell door clangs shut, its bars ringing with a long metallic decay.',
     ['fort', 'cell', 'bars', 'clang', 'dungeon', 'cachot', 'barreaux', 'fer'],
     "0.95s"),
    ('fort-moat-heavy-splash-001', 'Moat Heavy Splash 001', 'A large stone drops into the moat with a deep splash and rolling waves.',
     ['fort', 'moat', 'heavy', 'splash', 'water', 'douve', 'eau', 'plouf'],
     "1.29s"),
    ('fort-chain-snap-whip-001', 'Chain Snap Whip 001', 'A siege chain strains and snaps, whipping through the air and rattling to the ground.',
     ['fort', 'chain', 'snap', 'whip', 'break', 'chaine', 'rompre', 'claquement'],
     "0.88s"),
    ('fort-armored-patrol-march-001', 'Armored Patrol March 001', 'An armored guard marches along a rampart, each step clinking with plate and mail.',
     ['fort', 'armored', 'patrol', 'march', 'guard', 'armure', 'garde', 'patrouille'],
     "1.33s"),
    ('fort-banner-unfurl-flap-001', 'Banner Unfurl Flap 001', 'A large banner unfurls and flaps in the wind above the walls.',
     ['fort', 'banner', 'unfurl', 'flap', 'wind', 'banniere', 'drapeau', 'vent'],
     "1.53s"),
]

def load(name):
    with open(os.path.join(CATALOG_DIR, name), 'r', encoding='utf-8') as f:
        return json.load(f)

def save(name, data):
    with open(os.path.join(CATALOG_DIR, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

def main():
    print("Injection des 25 sons de la Mission 13 (Fortifications & Siege Machines)...")
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
