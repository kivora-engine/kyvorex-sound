"""Mission 11 - injection des 25 sons Microfaune et vie vegetale dans data/catalog/environment.json.
Lancer depuis la racine du projet : python3 tools/audio-generator/inject_mission_11.py
Le script peut etre relance sans danger : un son deja present est ignore.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG_DIR = os.path.join(ROOT, 'data', 'catalog')

DATE_STR = "2026-10-31"
LICENSE_STR = "KYVOREX Free Sound License 1.0"
CATEGORY = "Environment"

SOUNDS = [
        ('micro-seed-pod-burst-001', 'Seed Pod Burst 001', 'Dry seed pod snaps open and flings its seeds, which patter on the ground.',
         ['micro', 'seed', 'pod', 'burst', 'plant', 'nature', 'graine', 'gousse', 'plante'],
         "0.49s"),
        ('micro-flower-bud-open-001', 'Flower Bud Open 001', 'Soft petals unfurl as a flower bud slowly opens.',
         ['micro', 'flower', 'bud', 'open', 'petal', 'plant', 'fleur', 'bourgeon', 'petale'],
         "0.85s"),
        ('micro-dew-roll-drop-001', 'Dew Roll Drop 001', 'A dewdrop slides down a leaf blade and drops off with a small plop.',
         ['micro', 'dew', 'drop', 'leaf', 'water', 'rosee', 'goutte', 'feuille'],
         "0.36s"),
        ('micro-ant-colony-march-001', 'Ant Colony March 001', 'Hundreds of tiny feet tick in a steady column as an ant colony marches past.',
         ['micro', 'ant', 'colony', 'march', 'insect', 'fourmi', 'colonne', 'insecte'],
         "1.25s"),
        ('micro-beetle-wing-unfold-001', 'Beetle Wing Unfold 001', 'A beetle pops its wing cases open, then its folded wings whir into flight.',
         ['micro', 'beetle', 'wing', 'unfold', 'insect', 'scarabee', 'aile', 'insecte'],
         "0.62s"),
        ('micro-cocoon-crack-001', 'Cocoon Crack 001', 'A papery cocoon splits from the inside with small crackles and a soft thump.',
         ['micro', 'cocoon', 'crack', 'larva', 'insect', 'cocon', 'craquement', 'larve'],
         "0.45s"),
        ('micro-spider-silk-pluck-001', 'Spider Silk Pluck 001', 'A taut strand of spider silk is plucked and rings with a thin, high shimmer.',
         ['micro', 'spider', 'silk', 'pluck', 'web', 'araignee', 'soie', 'toile'],
         "0.95s"),
        ('micro-caterpillar-chew-001', 'Caterpillar Chew 001', 'A caterpillar munches a leaf in five slow, juicy bites.',
         ['micro', 'caterpillar', 'chew', 'leaf', 'eat', 'chenille', 'mastiquer', 'feuille'],
         "0.98s"),
        ('micro-leafcutter-snip-001', 'Leafcutter Snip 001', 'A leafcutter ant slices a leaf edge with crisp, tiny snips.',
         ['micro', 'leafcutter', 'snip', 'ant', 'leaf', 'fourmi', 'coupe', 'feuille'],
         "0.92s"),
        ('micro-firefly-pulse-001', 'Firefly Pulse 001', 'A firefly glows twice, each pulse a soft rising shimmer.',
         ['micro', 'firefly', 'pulse', 'glow', 'light', 'luciole', 'lueur', 'insecte'],
         "1.20s"),
        ('micro-pollen-puff-001', 'Pollen Puff 001', 'A flower releases a soft puff of pollen dust.',
         ['micro', 'pollen', 'puff', 'dust', 'flower', 'fleur', 'poussiere', 'bouffee'],
         "0.41s"),
        ('micro-root-groan-001', 'Root Groan 001', 'A thick root slowly strains and creaks as it pushes through the soil.',
         ['micro', 'root', 'groan', 'creak', 'soil', 'racine', 'grincement', 'sol'],
         "1.55s"),
        ('micro-vine-whip-snap-001', 'Vine Whip Snap 001', 'A springy vine lashes through the air and snaps taut.',
         ['micro', 'vine', 'whip', 'snap', 'plant', 'liane', 'fouet', 'claquement'],
         "0.22s"),
        ('micro-mushroom-cap-pop-001', 'Mushroom Cap Pop 001', 'A soft, hollow pop as a mushroom cap bursts through the ground cover.',
         ['micro', 'mushroom', 'cap', 'pop', 'fungus', 'champignon', 'chapeau', 'eclosion'],
         "0.18s"),
        ('micro-spore-cloud-release-001', 'Spore Cloud Release 001', 'A fungus exhales a drifting cloud of spores, a hiss of fine granular grains.',
         ['micro', 'spore', 'cloud', 'release', 'fungus', 'spores', 'nuage', 'champignon'],
         "1.10s"),
        ('micro-snail-slime-glide-001', 'Snail Slime Glide 001', 'A snail glides over a surface with a wet, slow squelching trail.',
         ['micro', 'snail', 'slime', 'glide', 'wet', 'escargot', 'bave', 'glisser'],
         "1.45s"),
        ('micro-grasshopper-leap-001', 'Grasshopper Leap 001', 'A grasshopper kicks off a stem, flutters a wing and lands in the grass.',
         ['micro', 'grasshopper', 'leap', 'jump', 'insect', 'sauterelle', 'saut', 'insecte'],
         "0.31s"),
        ('micro-dragonfly-dart-001', 'Dragonfly Dart 001', 'A dragonfly darts forward and brakes into a hover.',
         ['micro', 'dragonfly', 'dart', 'insect', 'fly', 'libellule', 'vol', 'insecte'],
         "0.42s"),
        ('micro-acorn-bounce-001', 'Acorn Bounce 001', 'An acorn falls and bounces several times on bark, each bounce shorter than the last.',
         ['micro', 'acorn', 'bounce', 'drop', 'wood', 'gland', 'rebond', 'chene'],
         "0.57s"),
        ('micro-thorn-scrape-001', 'Thorn Scrape 001', 'A thorn drags across a rough surface in stuttering scratches.',
         ['micro', 'thorn', 'scrape', 'scratch', 'plant', 'epine', 'gratter', 'ronce'],
         "0.58s"),
        ('micro-bark-beetle-gnaw-001', 'Bark Beetle Gnaw 001', 'A bark beetle bores into wood with a fast, fine rasping gnaw.',
         ['micro', 'bark', 'beetle', 'gnaw', 'wood', 'scolyte', 'ronger', 'ecorce'],
         "1.02s"),
        ('micro-nectar-sip-001', 'Nectar Sip 001', 'A tiny insect sips nectar with a quick wet slurp and two small smacks.',
         ['micro', 'nectar', 'sip', 'insect', 'flower', 'siroter', 'fleur'],
         "0.42s"),
        ('micro-seedling-sprout-001', 'Seedling Sprout 001', 'Soil cracks and a seedling pushes up, growing with a soft rising tone.',
         ['micro', 'seedling', 'sprout', 'grow', 'soil', 'plantule', 'pousse', 'croissance'],
         "0.90s"),
        ('micro-glow-fungus-hum-001', 'Glow Fungus Hum 001', 'A bioluminescent fungus hums with a slow, beating, eerie glow.',
         ['micro', 'glow', 'fungus', 'hum', 'bioluminescent', 'champignon', 'lueur', 'bourdonnement'],
         "1.65s"),
        ('micro-flytrap-snap-001', 'Flytrap Snap 001', 'A carnivorous plant lures with a soft hum, then snaps shut with a squish.',
         ['micro', 'flytrap', 'snap', 'carnivorous', 'plant', 'dionee', 'carnivore', 'plante'],
         "0.70s"),
]

def load(name):
    with open(os.path.join(CATALOG_DIR, name), 'r', encoding='utf-8') as f:
        return json.load(f)

def save(name, data):
    with open(os.path.join(CATALOG_DIR, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

def main():
    print("Injection des 25 sons de la Mission 11 (Microfaune et vie vegetale)...")
    environment = load('environment.json')
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
        environment['sounds'].append({
            "id": sid, "name": name, "category": CATEGORY, "description": desc, "tags": tags,
            "duration": dur, "date": DATE_STR,
            "mp3": "audio/mp3/" + sid + ".mp3", "wav": "audio/wav/" + sid + ".wav",
            "license": LICENSE_STR, "status": "available",
            "previewMode": "procedural", "wavMode": "file", "mp3Mode": "file"
        })
        added += 1
    save('environment.json', environment)
    print("OK : " + str(added) + " sons ajoutes a environment.json")

if __name__ == '__main__':
    main()
