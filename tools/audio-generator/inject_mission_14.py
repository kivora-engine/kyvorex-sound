"""Mission 14 - injection des 25 sons (Alchemy & Transformations) dans data/catalog/magic-fantasy.json.
Lancer depuis la racine du projet : python3 tools/audio-generator/inject_mission_14.py
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
    ('alch-liquid-to-vapor-001', 'Liquid To Vapor 001', 'A bubbling liquid turns into vapor with a rising hiss and a soft puff.',
     ['alch', 'liquid', 'vapor', 'transform', 'bubble', 'alchimie', 'liquide', 'vapeur'],
     "1.75s"),
    ('alch-metal-to-gold-001', 'Metal To Gold 001', 'Dull metal rings, shifts upward in a sweep and resolves into a warm, bright golden chord.',
     ['alch', 'metal', 'gold', 'transmute', 'chord', 'alchimie', 'metal', 'or'],
     "1.75s"),
    ('alch-stone-to-liquid-001', 'Stone To Liquid 001', 'Solid stone grinds, softens and melts into a sloshing liquid.',
     ['alch', 'stone', 'liquid', 'melt', 'transform', 'alchimie', 'pierre', 'fondre'],
     "1.75s"),
    ('alch-crystallize-snap-001', 'Crystallize Snap 001', 'A solution crystallizes in accelerating ticks that end in a bright ringing chime.',
     ['alch', 'crystallize', 'snap', 'crystal', 'chime', 'alchimie', 'cristalliser', 'cristal'],
     "1.36s"),
    ('alch-cork-pop-fizz-001', 'Cork Pop Fizz 001', 'A cork pops out of a flask, followed by a sparkling fizz that fades.',
     ['alch', 'cork', 'pop', 'fizz', 'flask', 'alchimie', 'bouchon', 'petillant'],
     "1.23s"),
    ('alch-vial-shake-slosh-001', 'Vial Shake Slosh 001', 'A vial is shaken, the liquid sloshing against the glass with fine fizzing.',
     ['alch', 'vial', 'shake', 'slosh', 'glass', 'alchimie', 'fiole', 'agiter'],
     "1.45s"),
    ('alch-reagent-mix-hiss-001', 'Reagent Mix Hiss 001', 'Two reagents react with a rising hiss, growing bubbles and a final pop.',
     ['alch', 'reagent', 'mix', 'hiss', 'reaction', 'alchimie', 'reactif', 'melange'],
     "1.75s"),
    ('alch-boil-over-surge-001', 'Boil Over Surge 001', 'A bubbling brew boils over in a frothing surge and spills across the surface.',
     ['alch', 'boil', 'over', 'surge', 'froth', 'alchimie', 'bouillir', 'mousse'],
     "2.25s"),
    ('alch-powder-flash-burst-001', 'Powder Flash Burst 001', 'An alchemical powder ignites in a quick flash with crackles and sparkles.',
     ['alch', 'powder', 'flash', 'burst', 'spark', 'alchimie', 'poudre', 'eclair'],
     "0.77s"),
    ('alch-philosopher-stone-pulse-001', 'Philosopher Stone Pulse 001', 'A legendary stone hums with a swelling, slowly beating chord and distant bell tones.',
     ['alch', 'philosopher', 'stone', 'pulse', 'legendary', 'alchimie', 'pierre', 'philosophale'],
     "2.95s"),
    ('alch-living-ink-writhe-001', 'Living Ink Writhe 001', 'Viscous ink writhes and slithers across a page with wet gloops.',
     ['alch', 'living', 'ink', 'writhe', 'wet', 'alchimie', 'encre', 'vivante'],
     "1.60s"),
    ('alch-matter-condense-001', 'Matter Condense 001', 'Floating matter pulls inward in accelerating ticks and condenses into a dense thud.',
     ['alch', 'matter', 'condense', 'compress', 'implode', 'alchimie', 'matiere', 'condenser'],
     "0.95s"),
    ('alch-matter-disperse-001', 'Matter Disperse 001', 'Dense matter bursts apart into a spray of granules.',
     ['alch', 'matter', 'disperse', 'burst', 'spray', 'alchimie', 'matiere', 'disperser'],
     "1.16s"),
    ('alch-glass-to-ice-freeze-001', 'Glass To Ice Freeze 001', 'Glass freezes into ice with a rising glassy sweep, accelerating crackles and crystalline tones.',
     ['alch', 'glass', 'ice', 'freeze', 'crystal', 'alchimie', 'verre', 'glace'],
     "1.75s"),
    ('alch-ash-to-flame-ignite-001', 'Ash To Flame Ignite 001', 'Smoldering ash crackles, then ignites into a roaring flame.',
     ['alch', 'ash', 'flame', 'ignite', 'fire', 'alchimie', 'cendre', 'flamme'],
     "1.40s"),
    ('alch-petrify-harden-001', 'Petrify Harden 001', 'Soft matter stiffens step by step into stone with a final crack and thud.',
     ['alch', 'petrify', 'harden', 'stone', 'transform', 'alchimie', 'petrifier', 'durcir'],
     "2.17s"),
    ('alch-distillation-drip-rise-001', 'Distillation Drip Rise 001', 'Drops fall into a flask faster and faster, their pitch rising as it fills.',
     ['alch', 'distillation', 'drip', 'rise', 'flask', 'alchimie', 'goutte', 'fiole'],
     "2.21s"),
    ('alch-flask-shatter-vapor-001', 'Flask Shatter Vapor 001', 'A glass flask shatters, releasing a swelling cloud of vapor.',
     ['alch', 'flask', 'shatter', 'vapor', 'glass', 'alchimie', 'fiole', 'briser'],
     "1.30s"),
    ('alch-essence-extract-pull-001', 'Essence Extract Pull 001', 'An essence is drawn out with a rising suction, sealed in a vial with a click and a soft chime.',
     ['alch', 'essence', 'extract', 'pull', 'vial', 'alchimie', 'essence', 'extraire'],
     "1.90s"),
    ('alch-mortar-grind-pestle-001', 'Mortar Grind Pestle 001', 'A pestle grinds herbs in a mortar with circular, gritty passes and soft knocks.',
     ['alch', 'mortar', 'grind', 'pestle', 'herbs', 'alchimie', 'mortier', 'broyer'],
     "1.60s"),
    ('alch-glowing-liquid-pulse-001', 'Glowing Liquid Pulse 001', 'A luminous liquid pulses three times with a soft glowing tone.',
     ['alch', 'glowing', 'liquid', 'pulse', 'glow', 'alchimie', 'liquide', 'lueur'],
     "2.05s"),
    ('alch-clay-animate-001', 'Clay Animate 001', 'Lumps of clay gather, squelch and grow in a rising tone as they come to life.',
     ['alch', 'clay', 'animate', 'golem', 'life', 'alchimie', 'argile', 'animer'],
     "1.95s"),
    ('alch-energies-merge-001', 'Energies Merge 001', 'Two energies glide toward one another, beat as they meet and lock into one flash.',
     ['alch', 'energies', 'merge', 'fusion', 'beat', 'alchimie', 'energies', 'fusionner'],
     "2.25s"),
    ('alch-unstable-ticking-pop-001', 'Unstable Ticking Pop 001', 'An unstable mixture ticks faster and faster before bursting with a pop and fizz.',
     ['alch', 'unstable', 'ticking', 'pop', 'warning', 'alchimie', 'instable', 'eclater'],
     "2.21s"),
    ('alch-antidote-clear-001', 'Antidote Clear 001', 'A murky tone clears away and resolves into a pure, sparkling bell chord.',
     ['alch', 'antidote', 'clear', 'cleanse', 'chord', 'alchimie', 'antidote', 'purifier'],
     "2.00s"),
]

def load(name):
    with open(os.path.join(CATALOG_DIR, name), 'r', encoding='utf-8') as f:
        return json.load(f)

def save(name, data):
    with open(os.path.join(CATALOG_DIR, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

def main():
    print("Injection des 25 sons de la Mission 14 (Alchemy & Transformations)...")
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
