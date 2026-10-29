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
    print("Injection des 75 nouveaux sons (Missions 3, 4, 5) dans le catalogue...")
    gameplay = load('gameplay.json')
    environment = load('environment.json')
    sci_fi = load('sci-fi.json')
    
    date_str = "2026-10-29" # Date de demain
    license_str = "KYVOREX Free Sound License 1.0"

    ruins_sounds = [
        ("ruin-stone-mechanism-001", "Ruin Stone Mechanism 001", "Ancient stone mechanism.", ["ruin", "stone", "ancient", "ruine"]),
        ("ruin-ancient-door-open-001", "Ruin Ancient Door Open 001", "Ancient door opening.", ["ruin", "door", "ancient", "porte"]),
        ("ruin-ancient-door-close-001", "Ruin Ancient Door Close 001", "Ancient door closing.", ["ruin", "door", "ancient", "porte"]),
        ("ruin-lock-engage-001", "Ruin Lock Engage 001", "Ancient lock engaging.", ["ruin", "lock", "ancient", "verrou"]),
        ("ruin-lock-release-001", "Ruin Lock Release 001", "Ancient lock releasing.", ["ruin", "lock", "ancient", "verrou"]),
        ("ruin-relic-activate-001", "Ruin Relic Activate 001", "Relic activation.", ["ruin", "relic", "ancient", "relique"]),
        ("ruin-statue-turn-001", "Ruin Statue Turn 001", "Statue turning.", ["ruin", "statue", "ancient", "statue"]),
        ("ruin-secret-wall-slide-001", "Ruin Secret Wall Slide 001", "Secret wall sliding.", ["ruin", "secret", "ancient", "secret"]),
        ("ruin-trap-trigger-001", "Ruin Trap Trigger 001", "Ancient trap triggering.", ["ruin", "trap", "ancient", "piège"]),
        ("ruin-block-move-001", "Ruin Block Move 001", "Stone block moving.", ["ruin", "block", "ancient", "bloc"]),
        ("ruin-rune-glow-001", "Ruin Rune Glow 001", "Rune glowing.", ["ruin", "rune", "ancient", "rune"]),
        ("ruin-artifact-pickup-001", "Ruin Artifact Pickup 001", "Artifact pickup.", ["ruin", "artifact", "ancient", "artefact"]),
        ("ruin-temple-bell-001", "Ruin Temple Bell 001", "Temple bell.", ["ruin", "temple", "ancient", "cloche"]),
        ("ruin-archaeological-scan-001", "Ruin Archaeological Scan 001", "Archaeological scan.", ["ruin", "scan", "ancient", "scan"]),
        ("ruin-pedestal-activate-001", "Ruin Pedestal Activate 001", "Pedestal activation.", ["ruin", "pedestal", "ancient", "piédestal"]),
        ("ruin-glyph-light-001", "Ruin Glyph Light 001", "Glyph lighting up.", ["ruin", "glyph", "ancient", "glyphe"]),
        ("ruin-pressure-plate-001", "Ruin Pressure Plate 001", "Pressure plate triggered.", ["ruin", "pressure", "ancient", "plaque"]),
        ("ruin-sarcophagus-open-001", "Ruin Sarcophagus Open 001", "Sarcophagus opening.", ["ruin", "sarcophagus", "ancient", "sarcophage"]),
        ("ruin-artifact-beam-001", "Ruin Artifact Beam 001", "Artifact energy beam.", ["ruin", "artifact", "ancient", "artefact"]),
        ("ruin-stone-grind-001", "Ruin Stone Grind 001", "Stone grinding.", ["ruin", "stone", "ancient", "pierre"]),
        ("ruin-temple-door-rumble-001", "Ruin Temple Door Rumble 001", "Temple door rumbling.", ["ruin", "temple", "ancient", "temple"]),
        ("ruin-relic-hum-001", "Ruin Relic Hum 001", "Relic humming.", ["ruin", "relic", "ancient", "relique"]),
        ("ruin-ancient-magic-001", "Ruin Ancient Magic 001", "Ancient magic sound.", ["ruin", "magic", "ancient", "magie"]),
        ("ruin-artifact-shatter-001", "Ruin Artifact Shatter 001", "Artifact shattering.", ["ruin", "artifact", "ancient", "artefact"]),
        ("ruin-temple-wind-001", "Ruin Temple Wind 001", "Wind in temple ruins.", ["ruin", "temple", "ancient", "vent"]),
    ]

    underwater_sounds = [
        ("sub-sonar-ping-001", "Sub Sonar Ping 001", "Submarine sonar ping.", ["submarine", "sonar", "underwater", "sonar"]),
        ("sub-engine-hum-001", "Sub Engine Hum 001", "Submarine engine hum.", ["submarine", "engine", "underwater", "moteur"]),
        ("sub-airlock-open-001", "Sub Airlock Open 001", "Airlock opening.", ["submarine", "airlock", "underwater", "sas"]),
        ("sub-airlock-close-001", "Sub Airlock Close 001", "Airlock closing.", ["submarine", "airlock", "underwater", "sas"]),
        ("sub-pressure-warning-001", "Sub Pressure Warning 001", "Pressure warning.", ["submarine", "warning", "underwater", "alerte"]),
        ("sub-torpedo-fire-001", "Sub Torpedo Fire 001", "Torpedo firing.", ["submarine", "torpedo", "underwater", "torpille"]),
        ("sub-dive-alarm-001", "Sub Dive Alarm 001", "Dive alarm.", ["submarine", "alarm", "underwater", "alarme"]),
        ("sub-navigation-beep-001", "Sub Navigation Beep 001", "Navigation beep.", ["submarine", "navigation", "underwater", "navigation"]),
        ("sub-oxygen-warning-001", "Sub Oxygen Warning 001", "Oxygen warning.", ["submarine", "oxygen", "underwater", "oxygène"]),
        ("sub-hatch-open-001", "Sub Hatch Open 001", "Hatch opening.", ["submarine", "hatch", "underwater", "trappe"]),
        ("sub-hatch-close-001", "Sub Hatch Close 001", "Hatch closing.", ["submarine", "hatch", "underwater", "trappe"]),
        ("sub-propeller-start-001", "Sub Propeller Start 001", "Propeller starting.", ["submarine", "propeller", "underwater", "hélice"]),
        ("sub-propeller-stop-001", "Sub Propeller Stop 001", "Propeller stopping.", ["submarine", "propeller", "underwater", "hélice"]),
        ("sub-docking-clamp-001", "Sub Docking Clamp 001", "Docking clamp.", ["submarine", "docking", "underwater", "amarrage"]),
        ("sub-torpedo-tube-open-001", "Sub Torpedo Tube Open 001", "Torpedo tube opening.", ["submarine", "torpedo", "underwater", "torpille"]),
        ("sub-radar-sweep-001", "Sub Radar Sweep 001", "Radar sweeping.", ["submarine", "radar", "underwater", "radar"]),
        ("sub-crash-dive-alarm-001", "Sub Crash Dive Alarm 001", "Crash dive alarm.", ["submarine", "alarm", "underwater", "alarme"]),
        ("sub-ballast-blow-001", "Sub Ballast Blow 001", "Ballast blowing.", ["submarine", "ballast", "underwater", "ballast"]),
        ("sub-depth-charge-001", "Sub Depth Charge 001", "Depth charge explosion.", ["submarine", "depth", "underwater", "charge"]),
        ("sub-sonar-sweep-001", "Sub Sonar Sweep 001", "Sonar sweeping.", ["submarine", "sonar", "underwater", "sonar"]),
        ("sub-cabin-pressure-leak-001", "Sub Cabin Pressure Leak 001", "Cabin pressure leak.", ["submarine", "leak", "underwater", "fuite"]),
        ("sub-control-panel-beep-001", "Sub Control Panel Beep 001", "Control panel beep.", ["submarine", "beep", "underwater", "bip"]),
        ("sub-engine-reverse-001", "Sub Engine Reverse 001", "Engine reversing.", ["submarine", "engine", "underwater", "moteur"]),
        ("sub-underwater-scan-001", "Sub Underwater Scan 001", "Underwater scan.", ["submarine", "scan", "underwater", "scan"]),
        ("sub-external-hull-tap-001", "Sub External Hull Tap 001", "Hull tap.", ["submarine", "hull", "underwater", "coque"]),
    ]

    forge_sounds = [
        ("forge-anvil-strike-heavy-001", "Forge Anvil Strike Heavy 001", "Heavy anvil strike.", ["forge", "anvil", "metal", "enclume"]),
        ("forge-anvil-strike-light-001", "Forge Anvil Strike Light 001", "Light anvil strike.", ["forge", "anvil", "metal", "enclume"]),
        ("forge-bellows-blow-001", "Forge Bellows Blow 001", "Bellows blowing.", ["forge", "bellows", "fire", "soufflet"]),
        ("forge-tongs-clank-001", "Forge Tongs Clank 001", "Tongs clanking.", ["forge", "tongs", "metal", "pinces"]),
        ("forge-quenching-sizzle-001", "Forge Quenching Sizzle 001", "Quenching sizzle.", ["forge", "quenching", "water", "trempe"]),
        ("forge-grindstone-spin-001", "Forge Grindstone Spin 001", "Grindstone spinning.", ["forge", "grindstone", "metal", "meule"]),
        ("forge-hammer-strike-soft-001", "Forge Hammer Strike Soft 001", "Soft hammer strike.", ["forge", "hammer", "metal", "marteau"]),
        ("forge-chain-pull-001", "Forge Chain Pull 001", "Chain pulling.", ["forge", "chain", "metal", "chaîne"]),
        ("forge-crucible-pour-001", "Forge Crucible Pour 001", "Crucible pouring.", ["forge", "crucible", "metal", "creuset"]),
        ("forge-metal-fold-001", "Forge Metal Fold 001", "Metal folding.", ["forge", "metal", "fold", "métal"]),
        ("forge-anvil-ring-001", "Forge Anvil Ring 001", "Anvil ringing.", ["forge", "anvil", "metal", "enclume"]),
        ("forge-coal-shovel-001", "Forge Coal Shovel 001", "Coal shoveling.", ["forge", "coal", "fire", "charbon"]),
        ("forge-sparks-burst-001", "Forge Sparks Burst 001", "Sparks bursting.", ["forge", "sparks", "fire", "étincelles"]),
        ("forge-cooling-crackle-001", "Forge Cooling Crackle 001", "Cooling crackle.", ["forge", "cooling", "metal", "refroidissement"]),
        ("forge-metal-press-001", "Forge Metal Press 001", "Metal pressing.", ["forge", "metal", "press", "presse"]),
        ("forge-mold-stamp-001", "Forge Mold Stamp 001", "Mold stamping.", ["forge", "mold", "metal", "moule"]),
        ("forge-file-metal-001", "Forge File Metal 001", "Filing metal.", ["forge", "file", "metal", "lime"]),
        ("forge-cut-tongs-001", "Forge Cut Tongs 001", "Cutting with tongs.", ["forge", "cut", "metal", "coupe"]),
        ("forge-metal-bend-001", "Forge Metal Bend 001", "Bending metal.", ["forge", "metal", "bend", "cintrage"]),
        ("forge-polish-leather-001", "Forge Polish Leather 001", "Polishing leather.", ["forge", "leather", "polish", "cuir"]),
        ("forge-glue-apply-001", "Forge Glue Apply 001", "Applying glue.", ["forge", "glue", "craft", "colle"]),
        ("forge-clamp-tighten-001", "Forge Clamp Tighten 001", "Tightening a clamp.", ["forge", "clamp", "metal", "serre-joint"]),
        ("forge-rivet-gun-001", "Forge Rivet Gun 001", "Rivet gun firing.", ["forge", "rivet", "metal", "rivet"]),
        ("forge-weld-seam-001", "Forge Weld Seam 001", "Welding a seam.", ["forge", "weld", "metal", "soudure"]),
        ("forge-workshop-ambience-001", "Forge Workshop Ambience 001", "Workshop ambience.", ["forge", "ambience", "craft", "atelier"]),
    ]

    for sid, name, desc, tags in ruins_sounds:
        gameplay['sounds'].append({
            "id": sid, "name": name, "category": "Gameplay", "description": desc, "tags": tags,
            "duration": "0.80s", "date": date_str,
            "mp3": f"audio/mp3/{sid}.mp3", "wav": f"audio/wav/{sid}.wav",
            "license": license_str, "status": "available",
            "previewMode": "procedural", "wavMode": "file", "mp3Mode": "file"
        })

    for sid, name, desc, tags in underwater_sounds:
        environment['sounds'].append({
            "id": sid, "name": name, "category": "Environment", "description": desc, "tags": tags,
            "duration": "0.80s", "date": date_str,
            "mp3": f"audio/mp3/{sid}.mp3", "wav": f"audio/wav/{sid}.wav",
            "license": license_str, "status": "available",
            "previewMode": "procedural", "wavMode": "file", "mp3Mode": "file"
        })

    for sid, name, desc, tags in forge_sounds:
        gameplay['sounds'].append({
            "id": sid, "name": name, "category": "Gameplay", "description": desc, "tags": tags,
            "duration": "0.50s", "date": date_str,
            "mp3": f"audio/mp3/{sid}.mp3", "wav": f"audio/wav/{sid}.wav",
            "license": license_str, "status": "available",
            "previewMode": "procedural", "wavMode": "file", "mp3Mode": "file"
        })

    save('gameplay.json', gameplay)
    save('environment.json', environment)
    save('sci-fi.json', sci_fi)
    print("✅ 75 nouveaux sons injectés avec succès.")

if __name__ == '__main__':
    main()