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
    sci_fi = load('sci-fi.json')
    gameplay = load('gameplay.json')
    
    date_str = "2026-10-26"
    license_str = "KYVOREX Free Sound License 1.0"

    ind_sounds = [
        ("ind-factory-siren-001", "Factory Siren 001", "Factory siren alarm.", ["industry", "siren", "machine", "sirène"]),
        ("ind-assembly-line-001", "Assembly Line 001", "Assembly line mechanism.", ["industry", "assembly", "machine", "chaîne"]),
        ("ind-robot-arm-weld-001", "Robot Arm Weld 001", "Robot arm welding.", ["industry", "robot", "machine", "soudure"]),
        ("ind-conveyor-heavy-001", "Conveyor Heavy 001", "Heavy conveyor belt.", ["industry", "conveyor", "machine", "convoyeur"]),
        ("ind-steam-release-001", "Steam Release 001", "Steam release valve.", ["industry", "steam", "machine", "vapeur"]),
        ("ind-forge-hammer-001", "Forge Hammer 001", "Heavy forge hammer.", ["industry", "forge", "machine", "marteau"]),
        ("ind-laser-cutter-001", "Laser Cutter 001", "Industrial laser cutter.", ["industry", "laser", "machine", "laser"]),
        ("ind-molding-press-001", "Molding Press 001", "Molding press machine.", ["industry", "press", "machine", "presse"]),
        ("ind-coolant-spray-001", "Coolant Spray 001", "Coolant spray.", ["industry", "coolant", "machine", "liquide"]),
        ("ind-turbine-startup-001", "Turbine Startup 001", "Turbine starting up.", ["industry", "turbine", "machine", "turbine"]),
        ("ind-magnetic-crane-001", "Magnetic Crane 001", "Magnetic crane lifting.", ["industry", "crane", "machine", "grue"]),
        ("ind-furnace-roar-001", "Furnace Roar 001", "Roaring furnace.", ["industry", "furnace", "machine", "fournaise"]),
        ("ind-packing-machine-001", "Packing Machine 001", "Packing machine.", ["industry", "packing", "machine", "emballage"]),
        ("ind-shutdown-sequence-001", "Shutdown Sequence 001", "Machine shutdown sequence.", ["industry", "shutdown", "machine", "arrêt"]),
        ("ind-emergency-stop-001", "Emergency Stop 001", "Emergency stop alarm.", ["industry", "emergency", "machine", "urgence"]),
        ("ind-metal-pour-001", "Metal Pour 001", "Pouring molten metal.", ["industry", "metal", "machine", "métal"]),
        ("ind-belt-snap-001", "Belt Snap 001", "Conveyor belt snapping.", ["industry", "belt", "machine", "courroie"]),
        ("ind-ventilation-hum-001", "Ventilation Hum 001", "Ventilation system hum.", ["industry", "ventilation", "machine", "ventilation"]),
        ("ind-drill-press-heavy-001", "Drill Press Heavy 001", "Heavy drill press.", ["industry", "drill", "machine", "perceuse"]),
        ("ind-forklift-move-001", "Forklift Move 001", "Forklift moving.", ["industry", "forklift", "machine", "chariot"]),
        ("ind-safety-alarm-001", "Safety Alarm 001", "Safety alarm.", ["industry", "alarm", "machine", "alarme"]),
        ("ind-scrap-metal-crush-001", "Scrap Metal Crush 001", "Crushing scrap metal.", ["industry", "crush", "machine", "broyage"]),
        ("ind-electric-motor-hum-001", "Electric Motor Hum 001", "Electric motor humming.", ["industry", "motor", "machine", "moteur"]),
        ("ind-production-bell-001", "Production Bell 001", "Production completion bell.", ["industry", "bell", "machine", "cloche"]),
        ("ind-heavy-door-lock-001", "Heavy Door Lock 001", "Heavy door locking.", ["industry", "door", "machine", "verrou"]),
    ]

    craft_sounds = [
        ("craft-brick-trowel-001", "Brick Trowel 001", "Spreading mortar.", ["craft", "trowel", "masonry", "truelle"]),
        ("craft-cement-mix-001", "Cement Mix 001", "Mixing cement.", ["craft", "cement", "masonry", "ciment"]),
        ("craft-glass-cutting-001", "Glass Cutting 001", "Cutting glass.", ["craft", "glass", "precision", "verre"]),
        ("craft-wood-sanding-001", "Wood Sanding 001", "Sanding wood.", ["craft", "sanding", "wood", "ponçage"]),
        ("craft-metal-filing-001", "Metal Filing 001", "Filing metal.", ["craft", "filing", "metal", "limage"]),
        ("craft-plaster-scrape-001", "Plaster Scrape 001", "Scraping plaster.", ["craft", "plaster", "masonry", "plâtre"]),
        ("craft-tile-cutting-001", "Tile Cutting 001", "Cutting a tile.", ["craft", "tile", "masonry", "carrelage"]),
        ("craft-wire-snips-001", "Wire Snips 001", "Cutting wire.", ["craft", "wire", "precision", "fil"]),
        ("craft-pipe-wrench-001", "Pipe Wrench 001", "Tightening a pipe.", ["craft", "pipe", "plumbing", "tuyau"]),
        ("craft-tape-measure-001", "Tape Measure 001", "Measuring with tape.", ["craft", "measure", "precision", "mètre"]),
        ("craft-level-bubble-001", "Level Bubble 001", "Checking level.", ["craft", "level", "precision", "niveau"]),
        ("craft-pencil-mark-001", "Pencil Mark 001", "Marking with pencil.", ["craft", "mark", "precision", "crayon"]),
        ("craft-rivet-gun-001", "Rivet Gun 001", "Using a rivet gun.", ["craft", "rivet", "assembly", "rivet"]),
        ("craft-staple-gun-001", "Staple Gun 001", "Using a staple gun.", ["craft", "staple", "assembly", "agrafeuse"]),
        ("craft-caulking-gun-001", "Caulking Gun 001", "Applying caulk.", ["craft", "caulk", "sealant", "mastic"]),
        ("craft-paint-roller-001", "Paint Roller 001", "Rolling paint.", ["craft", "paint", "finishing", "peinture"]),
        ("craft-paint-brush-001", "Paint Brush 001", "Brushing paint.", ["craft", "paint", "finishing", "pinceau"]),
        ("craft-chisel-wood-001", "Chisel Wood 001", "Chiseling wood.", ["craft", "chisel", "wood", "ciseau"]),
        ("craft-rasp-wood-001", "Rasp Wood 001", "Rasping wood.", ["craft", "rasp", "wood", "râpe"]),
        ("craft-pvc-pipe-cut-001", "PVC Pipe Cut 001", "Cutting PVC pipe.", ["craft", "pvc", "plumbing", "pvc"]),
        ("craft-screw-driver-electric-001", "Electric Screwdriver 001", "Electric screwdriver.", ["craft", "screwdriver", "power tool", "visseuse"]),
        ("craft-nail-puller-001", "Nail Puller 001", "Pulling a nail.", ["craft", "nail", "repair", "arrache-clou"]),
        ("craft-hacksaw-metal-001", "Hacksaw Metal 001", "Cutting metal with hacksaw.", ["craft", "hacksaw", "metal", "scie"]),
        ("craft-soldering-gun-001", "Soldering Gun 001", "Soldering with a gun.", ["craft", "solder", "electronics", "soudure"]),
        ("craft-lock-picking-001", "Lock Picking 001", "Picking a lock.", ["craft", "lock", "precision", "crochetage"]),
    ]

    for sid, name, desc, tags in ind_sounds:
        sci_fi['sounds'].append({
            "id": sid, "name": name, "category": "Sci-Fi", "description": desc, "tags": tags,
            "duration": "0.50s", "date": date_str,
            "mp3": f"audio/mp3/{sid}.mp3", "wav": f"audio/wav/{sid}.wav",
            "license": license_str, "status": "available",
            "previewMode": "procedural", "wavMode": "file", "mp3Mode": "file"
        })

    for sid, name, desc, tags in craft_sounds:
        gameplay['sounds'].append({
            "id": sid, "name": name, "category": "Gameplay", "description": desc, "tags": tags,
            "duration": "0.30s", "date": date_str,
            "mp3": f"audio/mp3/{sid}.mp3", "wav": f"audio/wav/{sid}.wav",
            "license": license_str, "status": "available",
            "previewMode": "procedural", "wavMode": "file", "mp3Mode": "file"
        })

    save('sci-fi.json', sci_fi)
    save('gameplay.json', gameplay)
    print("✅ 25 sons Industrie ajoutés à sci-fi.json")
    print("✅ 25 sons Artisanat ajoutés à gameplay.json")

if __name__ == '__main__':
    main()