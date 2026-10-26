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
    print("Injection des 50 nouveaux sons (Missions 9 & 10) dans le catalogue...")
    sci_fi = load('sci-fi.json')
    gameplay = load('gameplay.json')
    environment = load('environment.json')
    
    date_str = "2026-10-26"
    license_str = "KYVOREX Free Sound License 1.0"

    digital_sounds = [
        ("data-stream-flow-001", "Data Stream Flow 001", "Flowing data streams.", ["digital", "data", "stream", "données"]),
        ("server-sync-ping-001", "Server Sync Ping 001", "Server synchronization ping.", ["digital", "server", "sync", "serveur"]),
        ("firewall-deflect-001", "Firewall Deflect 001", "Firewall deflecting attack.", ["digital", "firewall", "security", "pare-feu"]),
        ("encryption-unlock-001", "Encryption Unlock 001", "Unlocking encryption.", ["digital", "encryption", "chiffrement"]),
        ("hologram-glitch-001", "Hologram Glitch 001", "Hologram glitching.", ["digital", "hologram", "hologramme"]),
        ("quantum-computer-hum-001", "Quantum Computer Hum 001", "Quantum computer humming.", ["digital", "quantum", "quantique"]),
        ("system-overload-001", "System Overload 001", "System overloading.", ["digital", "system", "système"]),
        ("neural-network-connect-001", "Neural Network Connect 001", "Neural network connecting.", ["digital", "neural", "réseau"]),
        ("digital-footprint-001", "Digital Footprint 001", "Digital footprint trace.", ["digital", "footprint", "trace"]),
        ("cyber-deck-boot-001", "Cyber Deck Boot 001", "Cyber deck booting.", ["digital", "cyber", "boot"]),
        ("data-corruption-001", "Data Corruption 001", "Corrupted data.", ["digital", "corruption", "corruption"]),
        ("satellite-uplink-001", "Satellite Uplink 001", "Satellite uplink.", ["digital", "satellite", "satellite"]),
        ("biometric-scan-pass-001", "Biometric Scan Pass 001", "Biometric scan success.", ["digital", "biometric", "biométrie"]),
        ("biometric-scan-fail-001", "Biometric Scan Fail 001", "Biometric scan failed.", ["digital", "biometric", "biométrie"]),
        ("drone-connect-001", "Drone Connect 001", "Connecting to a drone.", ["digital", "drone", "drone"]),
        ("smart-device-activate-001", "Smart Device Activate 001", "Smart device activating.", ["digital", "smart", "intelligent"]),
        ("signal-jammer-001", "Signal Jammer 001", "Signal jammer active.", ["digital", "jammer", "brouilleur"]),
        ("battery-recharge-001", "Battery Recharge 001", "Battery recharging.", ["digital", "battery", "batterie"]),
        ("power-grid-surge-001", "Power Grid Surge 001", "Power grid surge.", ["digital", "power", "énergie"]),
        ("wireless-charge-001", "Wireless Charge 001", "Wireless charging.", ["digital", "wireless", "sans-fil"]),
        ("cyber-attack-alert-001", "Cyber Attack Alert 001", "Cyber attack warning.", ["digital", "attack", "attaque"]),
        ("mainframe-access-001", "Mainframe Access 001", "Accessing the mainframe.", ["digital", "mainframe", "serveur"]),
        ("virtual-reality-enter-001", "Virtual Reality Enter 001", "Entering VR.", ["digital", "vr", "réalité"]),
        ("virtual-reality-exit-001", "Virtual Reality Exit 001", "Exiting VR.", ["digital", "vr", "réalité"]),
        ("digital-map-render-001", "Digital Map Render 001", "Rendering a digital map.", ["digital", "map", "carte"]),
    ]

    rare_sounds = [
        ("ancient-gear-turn-001", "Ancient Gear Turn 001", "Ancient gears turning.", ["rare", "ancient", "ancien"]),
        ("magical-trap-snap-001", "Magical Trap Snap 001", "A magical trap snapping.", ["rare", "trap", "piège"]),
        ("zero-gravity-float-001", "Zero Gravity Float 001", "Floating in zero gravity.", ["rare", "gravity", "gravité"]),
        ("time-loop-echo-001", "Time Loop Echo 001", "Echoing time loop.", ["rare", "time", "temps"]),
        ("artifact-discovery-001", "Artifact Discovery 001", "Discovering an artifact.", ["rare", "artifact", "artefact"]),
        ("alien-flora-bloom-001", "Alien Flora Bloom 001", "Alien flora blooming.", ["rare", "alien", "extraterrestre"]),
        ("futuristic-surgery-001", "Futuristic Surgery 001", "High-tech surgery.", ["rare", "surgery", "chirurgie"]),
        ("plasma-welding-001", "Plasma Welding 001", "Welding with plasma.", ["rare", "plasma", "plasma"]),
        ("ion-thruster-ignite-001", "Ion Thruster Ignite 001", "Igniting ion thrusters.", ["rare", "ion", "propulsion"]),
        ("cryo-pod-open-001", "Cryo Pod Open 001", "Opening a cryo pod.", ["rare", "cryo", "cryogénie"]),
        ("cryo-pod-close-001", "Cryo Pod Close 001", "Closing a cryo pod.", ["rare", "cryo", "cryogénie"]),
        ("sonic-screwdriver-001", "Sonic Screwdriver 001", "Sonic screwdriver hum.", ["rare", "sonic", "sonique"]),
        ("gravity-well-generate-001", "Gravity Well Generate 001", "Generating a gravity well.", ["rare", "gravity", "gravité"]),
        ("space-station-alarm-001", "Space Station Alarm 001", "Space station alarm.", ["rare", "space", "espace"]),
        ("meteor-shower-pass-001", "Meteor Shower Pass 001", "Meteor shower passing.", ["rare", "meteor", "météore"]),
        ("aura-reveal-001", "Aura Reveal 001", "Revealing an aura.", ["rare", "aura", "aura"]),
        ("runic-translation-001", "Runic Translation 001", "Translating runes.", ["rare", "rune", "rune"]),
        ("dimensional-fold-001", "Dimensional Fold 001", "Folding dimensions.", ["rare", "dimension", "dimension"]),
        ("elevator-mechanism-001", "Elevator Mechanism 001", "Elevator mechanism.", ["rare", "elevator", "ascenseur"]),
        ("trapdoor-trigger-001", "Trapdoor Trigger 001", "Triggering a trapdoor.", ["rare", "trapdoor", "trappe"]),
        ("laser-grid-activate-001", "Laser Grid Activate 001", "Activating a laser grid.", ["rare", "laser", "laser"]),
        ("biometric-lock-001", "Biometric Lock 001", "Biometric lock engaging.", ["rare", "lock", "verrou"]),
        ("black-hole-collapse-001", "Black Hole Collapse 001", "A black hole collapsing.", ["rare", "black hole", "trou noir"]),
        ("nebula-ambience-001", "Nebula Ambience 001", "Nebula space ambience.", ["rare", "nebula", "nébuleuse"]),
        ("alien-communication-001", "Alien Communication 001", "Alien communication signal.", ["rare", "alien", "extraterrestre"]),
    ]

    for sid, name, desc, tags in digital_sounds:
        sci_fi['sounds'].append({
            "id": sid, "name": name, "category": "Sci-Fi", "description": desc, "tags": tags,
            "duration": "0.40s", "date": date_str,
            "mp3": f"audio/mp3/{sid}.mp3", "wav": f"audio/wav/{sid}.wav",
            "license": license_str, "status": "available",
            "previewMode": "procedural", "wavMode": "file", "mp3Mode": "file"
        })

    for sid, name, desc, tags in rare_sounds:
        # On dispatche les sons rares dans les catégories les plus logiques
        cat = "Gameplay"
        if "nebula" in sid or "meteor" in sid or "black-hole" in sid: cat = "Environment"
        elif "ancient" in sid or "cryo" in sid: cat = "Gameplay"
        
        target_file = gameplay
        if cat == "Environment": target_file = environment
            
        target_file['sounds'].append({
            "id": sid, "name": name, "category": cat, "description": desc, "tags": tags,
            "duration": "0.80s", "date": date_str,
            "mp3": f"audio/mp3/{sid}.mp3", "wav": f"audio/wav/{sid}.wav",
            "license": license_str, "status": "available",
            "previewMode": "procedural", "wavMode": "file", "mp3Mode": "file"
        })

    save('sci-fi.json', sci_fi)
    save('gameplay.json', gameplay)
    save('environment.json', environment)
    print("✅ 25 sons Digital ajoutés à sci-fi.json")
    print("✅ 25 sons Rare/Specialized ajoutés à gameplay.json et environment.json")

if __name__ == '__main__':
    main()