import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG_DIR = os.path.join(ROOT, 'data', 'catalog')

def load(name):
    with open(os.path.join(CATALOG_DIR, name), 'r', encoding='utf-8') as f:
        return json.load(f)

def save(name, data):
    with open(os.path.join(CATALOG_DIR, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

def main():
    print("Injection des nouveaux sons dans le catalogue...")
    gameplay = load('gameplay.json')
    environment = load('environment.json')
    
    date_str = "2026-10-25"
    license_str = "KYVOREX Free Sound License 1.0"

    # Terrain (Gameplay)
    terrain_sounds = [
        ("footstep-mud-deep-001", "Footstep Mud Deep 001", "Pas lourds dans une boue profonde.", ["mud", "footstep", "terrain", "boue"]),
        ("footstep-wet-grass-001", "Footstep Wet Grass 001", "Pas dans une herbe mouillée.", ["grass", "footstep", "terrain", "herbe"]),
        ("footstep-gravel-loose-001", "Footstep Gravel Loose 001", "Pas sur du gravier meuble.", ["gravel", "footstep", "terrain", "gravier"]),
        ("footstep-wood-hollow-001", "Footstep Wood Hollow 001", "Pas sur un plancher en bois creux.", ["wood", "footstep", "terrain", "bois"]),
        ("footstep-marble-hall-001", "Footstep Marble Hall 001", "Pas résonnants dans un hall en marbre.", ["marble", "footstep", "terrain", "marbre"]),
        ("footstep-metal-grate-001", "Footstep Metal Grate 001", "Pas sur une grille métallique.", ["metal", "footstep", "terrain", "métal"]),
        ("footstep-snow-crust-001", "Footstep Snow Crust 001", "Pas écrasant une croûte de neige.", ["snow", "footstep", "terrain", "neige"]),
        ("footstep-shallow-water-001", "Footstep Shallow Water 001", "Pas dans de l'eau peu profonde.", ["water", "footstep", "terrain", "eau"]),
        ("footstep-dry-leaves-pile-001", "Footstep Dry Leaves Pile 001", "Pas dans un tas de feuilles sèches.", ["leaves", "footstep", "terrain", "feuilles"]),
        ("footstep-sand-dunes-001", "Footstep Sand Dunes 001", "Pas sur du sable meuble de dunes.", ["sand", "footstep", "terrain", "sable"]),
        ("landing-roll-soft-001", "Landing Roll Soft 001", "Atterrissage suivi d'un roulement doux.", ["landing", "roll", "terrain", "atterrissage"]),
        ("landing-knee-hard-001", "Landing Knee Hard 001", "Atterrissage brutal sur les genoux.", ["landing", "knee", "terrain", "genoux"]),
        ("slide-stone-surface-001", "Slide Stone Surface 001", "Glissade sur une surface en pierre.", ["slide", "stone", "terrain", "pierre"]),
        ("slide-ice-long-001", "Slide Ice Long 001", "Longue glissade sur de la glace.", ["slide", "ice", "terrain", "glace"]),
        ("rope-climb-strain-001", "Rope Climb Strain 001", "Corde sollicitée pendant une ascension.", ["rope", "climb", "terrain", "corde"]),
        ("ladder-wood-climb-001", "Ladder Wood Climb 001", "Montée sur une échelle en bois.", ["ladder", "wood", "terrain", "échelle"]),
        ("ladder-metal-rattle-001", "Ladder Metal Rattle 001", "Échelle métallique qui tremble.", ["ladder", "metal", "terrain", "échelle"]),
        ("rope-swing-pass-001", "Rope Swing Pass 001", "Passage d'une corde en mouvement.", ["rope", "swing", "terrain", "corde"]),
        ("zipline-start-001", "Zipline Start 001", "Départ d'une tyrolienne.", ["zipline", "start", "terrain", "tyrolienne"]),
        ("zipline-stop-001", "Zipline Stop 001", "Arrêt d'une tyrolienne.", ["zipline", "stop", "terrain", "tyrolienne"]),
        ("deep-water-dive-001", "Deep Water Dive 001", "Plongeon dans une eau profonde.", ["dive", "water", "terrain", "plongeon"]),
        ("underwater-movement-001", "Underwater Movement 001", "Mouvement sous l'eau.", ["underwater", "move", "terrain", "sous-marin"]),
        ("rock-climb-grip-001", "Rock Climb Grip 001", "Prise sur une paroi rocheuse.", ["rock", "climb", "terrain", "roche"]),
        ("heavy-landing-dirt-001", "Heavy Landing Dirt 001", "Atterrissage lourd sur de la terre.", ["landing", "heavy", "terrain", "terre"]),
        ("body-roll-gravel-001", "Body Roll Gravel 001", "Roulement sur du gravier.", ["roll", "gravel", "terrain", "gravier"]),
    ]

    for sid, name, desc, tags in terrain_sounds:
        gameplay['sounds'].append({
            "id": sid, "name": name, "category": "Gameplay", "description": desc, "tags": tags,
            "duration": "0.20s", "date": date_str,
            "mp3": f"audio/mp3/{sid}.mp3", "wav": f"audio/wav/{sid}.wav",
            "license": license_str, "status": "available",
            "previewMode": "procedural", "wavMode": "file", "mp3Mode": "file"
        })

    # Animals (Environment)
    animal_sounds = [
        ("wolf-pack-howling-001", "Wolf Pack Howling 001", "Hurlements coordonnés.", ["wolf", "howl", "animal", "loup"]),
        ("lion-territorial-roar-001", "Lion Territorial Roar 001", "Rugissement territorial.", ["lion", "roar", "animal", "lion"]),
        ("elephant-trumpet-001", "Elephant Trumpet 001", "Barrissement d'éléphant.", ["elephant", "trumpet", "animal", "éléphant"]),
        ("horse-snort-001", "Horse Snort 001", "Reniflement de cheval.", ["horse", "snort", "animal", "cheval"]),
        ("horse-hoof-stone-001", "Horse Hoof Stone 001", "Sabots sur pierre.", ["horse", "hoof", "animal", "sabots"]),
        ("camel-call-001", "Camel Call 001", "Vocalisation de chameau.", ["camel", "call", "animal", "chameau"]),
        ("hyena-cackle-001", "Hyena Cackle 001", "Rires de hyène.", ["hyena", "cackle", "animal", "hyène"]),
        ("frog-pond-croak-001", "Frog Pond Croak 001", "Coassements de grenouilles.", ["frog", "croak", "animal", "grenouille"]),
        ("cicada-day-chorus-001", "Cicada Day Chorus 001", "Chœur de cigales.", ["cicada", "chorus", "animal", "cigale"]),
        ("owl-wing-pass-001", "Owl Wing Pass 001", "Ailes de chouette.", ["owl", "wing", "animal", "chouette"]),
        ("eagle-screech-001", "Eagle Screech 001", "Cri d'aigle.", ["eagle", "screech", "animal", "aigle"]),
        ("peacock-display-call-001", "Peacock Display Call 001", "Appel de paon.", ["peacock", "call", "animal", "paon"]),
        ("duck-flock-takeoff-001", "Duck Flock Takeoff 001", "Envol de canards.", ["duck", "takeoff", "animal", "canard"]),
        ("goose-warning-call-001", "Goose Warning Call 001", "Cri d'oie.", ["goose", "warning", "animal", "oie"]),
        ("dolphin-click-train-001", "Dolphin Click Train 001", "Clics de dauphin.", ["dolphin", "click", "animal", "dauphin"]),
        ("whale-song-low-001", "Whale Song Low 001", "Chant de baleine.", ["whale", "song", "animal", "baleine"]),
        ("seal-colony-call-001", "Seal Colony Call 001", "Vocalisations de phoques.", ["seal", "call", "animal", "phoque"]),
        ("cricket-single-call-001", "Cricket Single Call 001", "Appel de grillon.", ["cricket", "call", "animal", "grillon"]),
        ("bees-swarm-pass-001", "Bees Swarm Pass 001", "Essaim d'abeilles.", ["bees", "swarm", "animal", "abeilles"]),
        ("mosquito-near-ear-001", "Mosquito Near Ear 001", "Bourdonnement de moustique.", ["mosquito", "buzz", "animal", "moustique"]),
        ("snake-hiss-long-001", "Snake Hiss Long 001", "Sifflement de serpent.", ["snake", "hiss", "animal", "serpent"]),
        ("crocodile-water-movement-001", "Crocodile Water Movement 001", "Déplacement de crocodile.", ["crocodile", "water", "animal", "crocodile"]),
        ("monkey-canopy-leap-001", "Monkey Canopy Leap 001", "Saut de singe.", ["monkey", "leap", "animal", "singe"]),
        ("boar-ground-snuffle-001", "Boar Ground Snuffle 001", "Reniflements de sanglier.", ["boar", "snuffle", "animal", "sanglier"]),
        ("deer-alarm-bark-001", "Deer Alarm Bark 001", "Cri d'alarme de cerf.", ["deer", "bark", "animal", "cerf"]),
    ]

    for sid, name, desc, tags in animal_sounds:
        environment['sounds'].append({
            "id": sid, "name": name, "category": "Environment", "description": desc, "tags": tags,
            "duration": "0.50s", "date": date_str,
            "mp3": f"audio/mp3/{sid}.mp3", "wav": f"audio/wav/{sid}.wav",
            "license": license_str, "status": "available",
            "previewMode": "procedural", "wavMode": "file", "mp3Mode": "file"
        })

    save('gameplay.json', gameplay)
    save('environment.json', environment)
    print("✅ 25 sons Terrain ajoutés à gameplay.json")
    print("✅ 25 sons Animaux ajoutés à environment.json")

if __name__ == '__main__':
    main()