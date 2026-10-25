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
    print("Injection des 50 nouveaux sons dans le catalogue...")
    gameplay = load('gameplay.json')
    
    date_str = "2026-10-25"
    license_str = "KYVOREX Free Sound License 1.0"

    mech_sounds = [
        ("mech-gear-engage-001", "Mech Gear Engage 001", "Gear engagement.", ["mech", "gear", "industrial", "engrenage"]),
        ("mech-gear-grind-001", "Mech Gear Grind 001", "Grinding gears.", ["mech", "grind", "industrial", "grincement"]),
        ("mech-piston-pump-001", "Mech Piston Pump 001", "Piston pumping.", ["mech", "piston", "industrial", "pompe"]),
        ("mech-hydraulic-press-001", "Mech Hydraulic Press 001", "Hydraulic press.", ["mech", "hydraulic", "industrial", "presse"]),
        ("mech-spring-snap-001", "Mech Spring Snap 001", "Spring snapping.", ["mech", "spring", "industrial", "ressort"]),
        ("mech-chain-rattle-001", "Mech Chain Rattle 001", "Rattling chains.", ["mech", "chain", "industrial", "chaîne"]),
        ("mech-ratchet-turn-001", "Mech Ratchet Turn 001", "Ratchet mechanism.", ["mech", "ratchet", "industrial", "cliquet"]),
        ("mech-motor-start-001", "Mech Motor Start 001", "Motor starting.", ["mech", "motor", "industrial", "moteur"]),
        ("mech-motor-stop-001", "Mech Motor Stop 001", "Motor stopping.", ["mech", "motor", "industrial", "moteur"]),
        ("mech-bolt-tighten-001", "Mech Bolt Tighten 001", "Tightening a bolt.", ["mech", "bolt", "industrial", "boulon"]),
        ("mech-lock-engage-001", "Mech Lock Engage 001", "Lock engaging.", ["mech", "lock", "industrial", "verrou"]),
        ("mech-lock-release-001", "Mech Lock Release 001", "Lock releasing.", ["mech", "lock", "industrial", "verrou"]),
        ("mech-valve-hiss-001", "Mech Valve Hiss 001", "Valve hissing.", ["mech", "valve", "industrial", "soupape"]),
        ("mech-steam-burst-001", "Mech Steam Burst 001", "Steam burst.", ["mech", "steam", "industrial", "vapeur"]),
        ("mech-turbine-spin-001", "Mech Turbine Spin 001", "Turbine spinning.", ["mech", "turbine", "industrial", "turbine"]),
        ("mech-conveyor-move-001", "Mech Conveyor Move 001", "Conveyor moving.", ["mech", "conveyor", "industrial", "convoyeur"]),
        ("mech-robotic-arm-001", "Mech Robotic Arm 001", "Robotic arm moving.", ["mech", "robot", "industrial", "bras"]),
        ("mech-weld-spark-001", "Mech Weld Spark 001", "Welding sparks.", ["mech", "weld", "industrial", "soudure"]),
        ("mech-hammer-strike-001", "Mech Hammer Strike 001", "Hammer strike.", ["mech", "hammer", "industrial", "marteau"]),
        ("mech-metal-clank-001", "Mech Metal Clank 001", "Metal clank.", ["mech", "metal", "industrial", "métal"]),
        ("mech-pneumatic-hiss-001", "Mech Pneumatic Hiss 001", "Pneumatic hiss.", ["mech", "pneumatic", "industrial", "pneumatique"]),
        ("mech-clockwork-tick-001", "Mech Clockwork Tick 001", "Clockwork ticking.", ["mech", "clockwork", "industrial", "horlogerie"]),
        ("mech-heavy-door-slide-001", "Mech Heavy Door Slide 001", "Heavy door sliding.", ["mech", "door", "industrial", "porte"]),
        ("mech-security-breach-001", "Mech Security Breach 001", "Security breach alert.", ["mech", "security", "industrial", "sécurité"]),
        ("mech-system-shutdown-001", "Mech System Shutdown 001", "System shutting down.", ["mech", "system", "industrial", "arrêt"]),
    ]

    tool_sounds = [
        ("tool-screwdriver-turn-001", "Tool Screwdriver Turn 001", "Screwdriver turning.", ["tool", "screwdriver", "hardware", "tournevis"]),
        ("tool-wrench-clank-001", "Tool Wrench Clank 001", "Wrench clank.", ["tool", "wrench", "hardware", "clé"]),
        ("tool-saw-wood-001", "Tool Saw Wood 001", "Sawing wood.", ["tool", "saw", "hardware", "scie"]),
        ("tool-saw-metal-001", "Tool Saw Metal 001", "Sawing metal.", ["tool", "saw", "hardware", "scie"]),
        ("tool-drill-wood-001", "Tool Drill Wood 001", "Drilling wood.", ["tool", "drill", "hardware", "perceuse"]),
        ("tool-drill-metal-001", "Tool Drill Metal 001", "Drilling metal.", ["tool", "drill", "hardware", "perceuse"]),
        ("tool-hammer-nail-001", "Tool Hammer Nail 001", "Hammering a nail.", ["tool", "hammer", "hardware", "marteau"]),
        ("tool-wrench-ratchet-001", "Tool Wrench Ratchet 001", "Ratchet wrench.", ["tool", "ratchet", "hardware", "cliquet"]),
        ("tool-pliers-snip-001", "Tool Pliers Snip 001", "Pliers snipping.", ["tool", "pliers", "hardware", "pince"]),
        ("tool-sandpaper-rub-001", "Tool Sandpaper Rub 001", "Rubbing sandpaper.", ["tool", "sandpaper", "hardware", "papier de verre"]),
        ("tool-tape-peel-001", "Tool Tape Peel 001", "Peeling tape.", ["tool", "tape", "hardware", "ruban"]),
        ("tool-glue-apply-001", "Tool Glue Apply 001", "Applying glue.", ["tool", "glue", "hardware", "colle"]),
        ("tool-glass-clink-001", "Tool Glass Clink 001", "Glass clinking.", ["tool", "glass", "hardware", "verre"]),
        ("tool-metal-scrape-001", "Tool Metal Scrape 001", "Metal scraping.", ["tool", "metal", "hardware", "métal"]),
        ("tool-wood-creak-001", "Tool Wood Creak 001", "Wood creaking.", ["tool", "wood", "hardware", "bois"]),
        ("tool-stone-chisel-001", "Tool Stone Chisel 001", "Chiseling stone.", ["tool", "stone", "hardware", "pierre"]),
        ("tool-rope-tie-001", "Tool Rope Tie 001", "Tying a rope.", ["tool", "rope", "hardware", "corde"]),
        ("tool-wire-strip-001", "Tool Wire Strip 001", "Stripping wire.", ["tool", "wire", "hardware", "fil"]),
        ("tool-solder-iron-001", "Tool Solder Iron 001", "Soldering iron.", ["tool", "solder", "hardware", "fer à souder"]),
        ("tool-welding-arc-001", "Tool Welding Arc 001", "Welding arc.", ["tool", "weld", "hardware", "soudure"]),
        ("tool-dropping-wrench-001", "Tool Dropping Wrench 001", "Dropping a wrench.", ["tool", "drop", "hardware", "chute"]),
        ("tool-picking-up-nails-001", "Tool Picking Up Nails 001", "Picking up nails.", ["tool", "nails", "hardware", "clous"]),
        ("tool-toolbox-open-001", "Tool Toolbox Open 001", "Opening a toolbox.", ["tool", "box", "hardware", "boîte"]),
        ("tool-toolbox-close-001", "Tool Toolbox Close 001", "Closing a toolbox.", ["tool", "box", "hardware", "boîte"]),
        ("tool-multi-tool-switch-001", "Tool Multi Tool Switch 001", "Switching a multi-tool.", ["tool", "switch", "hardware", "outil"]),
    ]

    for sid, name, desc, tags in mech_sounds + tool_sounds:
        gameplay['sounds'].append({
            "id": sid, "name": name, "category": "Gameplay", "description": desc, "tags": tags,
            "duration": "0.30s", "date": date_str,
            "mp3": f"audio/mp3/{sid}.mp3", "wav": f"audio/wav/{sid}.wav",
            "license": license_str, "status": "available",
            "previewMode": "procedural", "wavMode": "file", "mp3Mode": "file"
        })

    save('gameplay.json', gameplay)
    print("✅ 50 nouveaux sons (Mécanique + Outils) ajoutés à gameplay.json")

if __name__ == '__main__':
    main()