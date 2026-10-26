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
    print("Injection des 50 nouveaux sons (Missions 7 & 8) dans le catalogue...")
    environment = load('environment.json')
    sci_fi = load('sci-fi.json') # On place les effets spéciaux dans Sci-Fi
    
    date_str = "2026-10-26"
    license_str = "KYVOREX Free Sound License 1.0"

    env_sounds = [
        ("env-avalanche-001", "Avalanche 001", "Rumbling avalanche.", ["nature", "avalanche", "snow", "neige"]),
        ("env-geyser-eruption-001", "Geyser Eruption 001", "Erupting geyser.", ["nature", "geyser", "water", "eau"]),
        ("env-earthquake-rumble-001", "Earthquake Rumble 001", "Deep earthquake rumble.", ["nature", "earthquake", "tremblement"]),
        ("env-desert-wind-001", "Desert Wind 001", "Whistling desert wind.", ["nature", "desert", "désert"]),
        ("env-glacier-crack-001", "Glacier Crack 001", "Ice cracking.", ["nature", "glacier", "ice", "glace"]),
        ("env-lava-bubble-001", "Lava Bubble 001", "Bubbling lava.", ["nature", "lava", "lave"]),
        ("env-mud-bubble-001", "Mud Bubble 001", "Bubbling mud.", ["nature", "mud", "boue"]),
        ("env-waterfall-001", "Waterfall 001", "Heavy waterfall.", ["nature", "water", "cascade"]),
        ("env-quicksand-001", "Quicksand 001", "Sinking quicksand.", ["nature", "quicksand", "sables"]),
        ("env-snow-crunch-001", "Snow Crunch 001", "Crunching snow.", ["nature", "snow", "neige"]),
        ("env-swamp-ambience-001", "Swamp Ambience 001", "Murky swamp ambience.", ["nature", "swamp", "marais"]),
        ("env-bamboo-creak-001", "Bamboo Creak 001", "Creaking bamboo.", ["nature", "bamboo", "bambou"]),
        ("env-sandstorm-001", "Sandstorm 001", "Harsh sandstorm.", ["nature", "sandstorm", "tempête"]),
        ("env-icicle-fall-001", "Icicle Fall 001", "Falling icicle.", ["nature", "ice", "glace"]),
        ("env-canyon-echo-001", "Canyon Echo 001", "Echoing canyon.", ["nature", "canyon", "écho"]),
        ("env-river-flow-001", "River Flow 001", "Flowing river.", ["nature", "river", "rivière"]),
        ("env-forest-fire-001", "Forest Fire 001", "Raging forest fire.", ["nature", "fire", "feu"]),
        ("env-hail-storm-001", "Hail Storm 001", "Hail impacts.", ["nature", "hail", "grêle"]),
        ("env-tornado-001", "Tornado 001", "Roaring tornado.", ["nature", "tornado", "tornade"]),
        ("env-tide-pool-001", "Tide Pool 001", "Tide pool water.", ["nature", "water", "eau"]),
        ("env-rock-fall-001", "Rock Fall 001", "Falling rocks.", ["nature", "rock", "roche"]),
        ("env-volcanic-vent-001", "Volcanic Vent 001", "Hissing volcanic vent.", ["nature", "volcano", "volcan"]),
        ("env-blizzard-001", "Blizzard 001", "Howling blizzard.", ["nature", "blizzard", "neige"]),
        ("env-jungle-rain-001", "Jungle Rain 001", "Heavy jungle rain.", ["nature", "rain", "pluie"]),
        ("env-quarry-blast-001", "Quarry Blast 001", "Distant quarry blast.", ["nature", "blast", "explosion"]),
    ]

    fx_sounds = [
        ("fx-time-freeze-001", "Time Freeze 001", "Time freezing effect.", ["fx", "time", "temps"]),
        ("fx-time-rewind-001", "Time Rewind 001", "Time rewinding effect.", ["fx", "time", "temps"]),
        ("fx-gravity-shift-001", "Gravity Shift 001", "Shifting gravity.", ["fx", "gravity", "gravité"]),
        ("fx-reality-glitch-001", "Reality Glitch 001", "Digital reality glitch.", ["fx", "glitch", "réalité"]),
        ("fx-cloaking-device-001", "Cloaking Device 001", "Activating cloak.", ["fx", "cloak", "invisibilité"]),
        ("fx-mind-control-001", "Mind Control 001", "Mind control wave.", ["fx", "mind", "esprit"]),
        ("fx-illusion-break-001", "Illusion Break 001", "Breaking an illusion.", ["fx", "illusion", "illusion"]),
        ("fx-size-change-001", "Size Change 001", "Changing size.", ["fx", "size", "taille"]),
        ("fx-elemental-fusion-001", "Elemental Fusion 001", "Fusing elements.", ["fx", "element", "élément"]),
        ("fx-arcane-barrier-001", "Arcane Barrier 001", "Arcane shield.", ["fx", "magic", "barrière"]),
        ("fx-mana-drain-001", "Mana Drain 001", "Draining mana.", ["fx", "mana", "mana"]),
        ("fx-rune-activate-001", "Rune Activate 001", "Activating a rune.", ["fx", "rune", "rune"]),
        ("fx-dimension-rift-001", "Dimension Rift 001", "Opening a rift.", ["fx", "dimension", "faille"]),
        ("fx-telekinesis-001", "Telekinesis 001", "Using telekinesis.", ["fx", "telekinesis", "télékinésie"]),
        ("fx-invisibility-001", "Invisibility 001", "Fading into invisibility.", ["fx", "invisible", "invisible"]),
        ("fx-possession-001", "Possession 001", "Demonic possession.", ["fx", "possession", "possession"]),
        ("fx-healing-aura-001", "Healing Aura 001", "Healing aura.", ["fx", "heal", "soin"]),
        ("fx-curse-applied-001", "Curse Applied 001", "Applying a curse.", ["fx", "curse", "malédiction"]),
        ("fx-blessing-received-001", "Blessing Received 001", "Receiving a blessing.", ["fx", "blessing", "bénédiction"]),
        ("fx-weapon-enchant-001", "Weapon Enchant 001", "Enchanting a weapon.", ["fx", "enchant", "enchantement"]),
        ("fx-armor-break-001", "Armor Break 001", "Breaking magical armor.", ["fx", "armor", "armure"]),
        ("fx-spirit-summon-001", "Spirit Summon 001", "Summoning a spirit.", ["fx", "spirit", "esprit"]),
        ("fx-vortex-creation-001", "Vortex Creation 001", "Creating a vortex.", ["fx", "vortex", "vortex"]),
        ("fx-levitation-001", "Levitation 001", "Levitating.", ["fx", "levitate", "lévitation"]),
        ("fx-mind-blast-001", "Mind Blast 001", "Psychic mind blast.", ["fx", "mind", "esprit"]),
    ]

    for sid, name, desc, tags in env_sounds:
        environment['sounds'].append({
            "id": sid, "name": name, "category": "Environment", "description": desc, "tags": tags,
            "duration": "1.50s", "date": date_str,
            "mp3": f"audio/mp3/{sid}.mp3", "wav": f"audio/wav/{sid}.wav",
            "license": license_str, "status": "available",
            "previewMode": "procedural", "wavMode": "file", "mp3Mode": "file"
        })

    for sid, name, desc, tags in fx_sounds:
        sci_fi['sounds'].append({
            "id": sid, "name": name, "category": "Sci-Fi", "description": desc, "tags": tags,
            "duration": "0.80s", "date": date_str,
            "mp3": f"audio/mp3/{sid}.mp3", "wav": f"audio/wav/{sid}.wav",
            "license": license_str, "status": "available",
            "previewMode": "procedural", "wavMode": "file", "mp3Mode": "file"
        })

    save('environment.json', environment)
    save('sci-fi.json', sci_fi)
    print("✅ 25 sons Environnement ajoutés à environment.json")
    print("✅ 25 sons Effets Spéciaux ajoutés à sci-fi.json")

if __name__ == '__main__':
    main()