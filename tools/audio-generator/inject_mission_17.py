"""Mission 17 - injection des 25 sons (Fantasy Ecosystems) dans data/catalog/magic-fantasy.json.
Lancer depuis la racine du projet : python3 tools/audio-generator/inject_mission_17.py
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
    ('eco-fairy-wing-glimmer-001', 'Fairy Wing Glimmer 001', 'Tiny fairy wings flutter rapidly, shedding bright glimmering chimes.',
     ['eco', 'fairy', 'wing', 'glimmer', 'flutter', 'fee', 'aile', 'scintillement'],
     "0.91s"),
    ('eco-spore-sprite-pop-001', 'Spore Sprite Pop 001', 'Tiny sprites hatch from spores in a rising cascade of bubbly pops.',
     ['eco', 'spore', 'sprite', 'pop', 'hatch', 'sporange', 'lutin', 'eclore'],
     "0.55s"),
    ('eco-luminous-moth-swarm-001', 'Luminous Moth Swarm 001', 'A swarm of luminous moths drifts by in a soft cloud of chimes and fluttering.',
     ['eco', 'luminous', 'moth', 'swarm', 'glow', 'papillon', 'lumineux', 'essaim'],
     "1.51s"),
    ('eco-crystal-tree-chime-001', 'Crystal Tree Chime 001', 'A breeze moves through the leaves of a crystal tree, ringing out glassy pentatonic chimes.',
     ['eco', 'crystal', 'tree', 'chime', 'wind', 'arbre', 'cristal', 'carillon'],
     "2.20s"),
    ('eco-living-vine-wake-001', 'Living Vine Wake 001', 'A mass of living vines wakes up, stretching with creaks and a long leafy rustle.',
     ['eco', 'living', 'vine', 'wake', 'plant', 'liane', 'vivante', 'reveil'],
     "1.05s"),
    ('eco-dragon-hatchling-chirp-001', 'Dragon Hatchling Chirp 001', 'A baby dragon chirps and squeaks in two rising-and-falling calls.',
     ['eco', 'dragon', 'hatchling', 'chirp', 'baby', 'dragonneau', 'cri', 'bebe'],
     "0.67s"),
    ('eco-unicorn-hoof-sparkle-001', 'Unicorn Hoof Sparkle 001', 'A unicorn trots on enchanted ground, each hoofbeat leaving a bright sparkle.',
     ['eco', 'unicorn', 'hoof', 'sparkle', 'trot', 'licorne', 'sabot', 'etincelle'],
     "1.03s"),
    ('eco-treant-groan-step-001', 'Treant Groan Step 001', 'A giant tree creature groans as it lifts a root-foot, then lands with a heavy thud and falling leaves.',
     ['eco', 'treant', 'groan', 'step', 'giant', 'arbre', 'geant', 'pas'],
     "1.40s"),
    ('eco-pixie-dust-trail-001', 'Pixie Dust Trail 001', 'Pixie dust sprinkles down in a long descending trail of tiny sparkles.',
     ['eco', 'pixie', 'dust', 'trail', 'sparkle', 'poussiere', 'lutin', 'traine'],
     "1.06s"),
    ('eco-moon-bloom-chime-001', 'Moon Bloom Chime 001', 'A night flower blooms in the moonlight with four rising bell tones.',
     ['eco', 'moon', 'bloom', 'chime', 'night', 'lune', 'fleur', 'carillon'],
     "1.39s"),
    ('eco-enchanted-stream-babble-001', 'Enchanted Stream Babble 001', 'A magical brook babbles and bubbles, with faint chimes ringing from the water.',
     ['eco', 'enchanted', 'stream', 'babble', 'water', 'ruisseau', 'enchante', 'eau'],
     "1.45s"),
    ('eco-griffin-screech-001', 'Griffin Screech 001', 'A griffin lets out a sweeping, raspy screech.',
     ['eco', 'griffin', 'screech', 'cry', 'creature', 'griffon', 'cri', 'creature'],
     "0.56s"),
    ('eco-forest-spirit-whisper-001', 'Forest Spirit Whisper 001', 'A forest spirit whispers in airy, shifting vowel-like breaths.',
     ['eco', 'forest', 'spirit', 'whisper', 'breath', 'foret', 'esprit', 'murmure'],
     "1.35s"),
    ('eco-wisp-lantern-flicker-001', 'Wisp Lantern Flicker 001', 'A will-o-the-wisp flickers softly, its glow wavering between close notes.',
     ['eco', 'wisp', 'lantern', 'flicker', 'glow', 'feu-follet', 'lanterne', 'vaciller'],
     "1.20s"),
    ('eco-giant-beanstalk-grow-001', 'Giant Beanstalk Grow 001', 'A giant beanstalk shoots upward with groaning stretches and ends in a burst of leaves.',
     ['eco', 'giant', 'beanstalk', 'grow', 'plant', 'haricot', 'geant', 'pousser'],
     "1.85s"),
    ('eco-floating-island-drift-001', 'Floating Island Drift 001', 'A floating island drifts through the sky with a deep hum and slow wind sweeps.',
     ['eco', 'floating', 'island', 'drift', 'sky', 'ile', 'flottante', 'derive'],
     "2.35s"),
    ('eco-fire-salamander-crackle-001', 'Fire Salamander Crackle 001', 'A fire salamander hisses and crackles as sparks pop off its hide.',
     ['eco', 'fire', 'salamander', 'crackle', 'creature', 'salamandre', 'feu', 'crepiter'],
     "1.24s"),
    ('eco-mermaid-pearl-song-001', 'Mermaid Pearl Song 001', 'A mermaid sings a short pearly melody of five bell-like notes.',
     ['eco', 'mermaid', 'pearl', 'song', 'sea', 'sirene', 'perle', 'chant'],
     "1.95s"),
    ('eco-root-door-creak-open-001', 'Root Door Creak Open 001', 'Someone knocks twice on a door in a tree trunk, which creaks slowly open.',
     ['eco', 'root', 'door', 'creak', 'open', 'racine', 'porte', 'grincement'],
     "1.55s"),
    ('eco-phoenix-egg-warm-pulse-001', 'Phoenix Egg Warm Pulse 001', 'A phoenix egg glows with three warm pulses and a faint crackle of fire.',
     ['eco', 'phoenix', 'egg', 'warm', 'pulse', 'oeuf', 'chaleur', 'pulsation'],
     "2.05s"),
    ('eco-fairy-ring-activate-001', 'Fairy Ring Activate 001', 'A ring of mushrooms ignites with a rising arpeggio, a swell and a final shimmer.',
     ['eco', 'fairy', 'ring', 'activate', 'mushroom', 'cercle', 'fee', 'activer'],
     "1.15s"),
    ('eco-glow-worm-cavern-001', 'Glow Worm Cavern 001', 'A cavern ceiling of glow worms twinkles above slow, echoing drips.',
     ['eco', 'glow', 'worm', 'cavern', 'drip', 'ver', 'luisant', 'grotte'],
     "2.20s"),
    ('eco-wyvern-wing-flap-001', 'Wyvern Wing Flap 001', 'A wyvern beats its leathery wings three times with heavy whooshes and membrane cracks.',
     ['eco', 'wyvern', 'wing', 'flap', 'leather', 'aile', 'cuir', 'battement'],
     "1.28s"),
    ('eco-enchanted-wind-whistle-001', 'Enchanted Wind Whistle 001', 'An enchanted wind blows through the trees, carrying three faint whistled notes.',
     ['eco', 'enchanted', 'wind', 'whistle', 'melody', 'vent', 'sifflement', 'enchante'],
     "2.05s"),
    ('eco-forest-awakening-dawn-001', 'Forest Awakening Dawn 001', 'A forest greets the dawn with a swelling chord and four bright bird-like chirps.',
     ['eco', 'forest', 'awakening', 'dawn', 'ambience', 'foret', 'aube', 'reveil'],
     "2.45s"),
]

def load(name):
    with open(os.path.join(CATALOG_DIR, name), 'r', encoding='utf-8') as f:
        return json.load(f)

def save(name, data):
    with open(os.path.join(CATALOG_DIR, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

def main():
    print("Injection des 25 sons de la Mission 17 (Fantasy Ecosystems)...")
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
