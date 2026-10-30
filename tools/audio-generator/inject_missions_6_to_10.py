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
    print("Injection des 125 nouveaux sons dans le catalogue...")
    sci_fi = load('sci-fi.json')
    gameplay = load('gameplay.json')
    environment = load('environment.json')
    
    date_str = "2026-10-30"
    license_str = "KYVOREX Free Sound License 1.0"

    # Dictionnaire de correspondance : Mission -> Catégorie cible
    categories = {
        "sci_inst": ("sci-fi", sci_fi),
        "veh": ("sci-fi", sci_fi),
        "infra": ("environment", environment),
        "cyber": ("sci-fi", sci_fi),
        "react": ("sci-fi", sci_fi)
    }

    # 125 identifiants à ajouter (générés à partir des préfixes)
    ids_to_add = [
        "sci-inst-microscope-laser-001", "sci-inst-spectrometer-scan-001", "sci-inst-calibration-ping-001", "sci-inst-centrifuge-spin-001", "sci-inst-dna-sequencer-001",
        "sci-inst-electron-beam-001", "sci-inst-radar-sweep-001", "sci-inst-sonar-ping-001", "sci-inst-telescope-focus-001", "sci-inst-lab-door-open-001",
        "sci-inst-lab-door-close-001", "sci-inst-chemical-analysis-001", "sci-inst-vacuum-pump-001", "sci-inst-spectrum-analyzer-001", "sci-inst-microscope-slide-001",
        "sci-inst-cryo-analysis-001", "sci-inst-particle-accelerator-001", "sci-inst-laser-calibration-001", "sci-inst-radiation-detector-001", "sci-inst-dna-helix-scan-001",
        "sci-inst-chemical-synthesizer-001", "sci-inst-lab-diagnostic-001", "sci-inst-microscope-zoom-001", "sci-inst-experimental-pulse-001", "sci-inst-lab-ambience-001",
        
        "veh-engine-turbo-001", "veh-gear-shift-heavy-001", "veh-gear-shift-light-001", "veh-brake-squeal-001", "veh-exhaust-burst-001",
        "veh-engine-start-futuristic-001", "veh-engine-stop-futuristic-001", "veh-drivetrain-engage-001", "veh-suspension-bounce-001", "veh-tire-screech-001",
        "veh-nitro-boost-001", "veh-racing-pass-by-001", "veh-mechanical-whine-001", "veh-hydraulic-lift-001", "veh-hydraulic-lower-001",
        "veh-wheel-spin-001", "veh-crash-metal-impact-001", "veh-fuel-pump-001", "veh-speedometer-ping-001", "veh-engine-rev-001",
        "veh-gear-grind-001", "veh-futuristic-hover-001", "veh-ignition-spark-001", "veh-cockpit-ambience-001", "veh-engine-cooling-001",

        "infra-train-horn-001", "infra-bridge-lift-001", "infra-elevator-ding-001", "infra-subway-arrival-001", "infra-traffic-light-beep-001",
        "infra-bus-door-open-001", "infra-bus-door-close-001", "infra-train-track-clatter-001", "infra-tunnel-wind-001", "infra-ferry-horn-001",
        "infra-drawbridge-motor-001", "infra-toll-booth-beep-001", "infra-parking-barrier-open-001", "infra-parking-barrier-close-001", "infra-crosswalk-signal-001",
        "infra-train-brake-squeal-001", "infra-tram-bell-001", "infra-cargo-crane-move-001", "infra-container-lock-001", "infra-gate-open-001",
        "infra-gate-close-001", "infra-highway-traffic-001", "infra-tunnel-ambience-001", "infra-runway-jet-001", "infra-airport-bell-001",

        "cyber-firewall-block-001", "cyber-access-granted-001", "cyber-access-denied-001", "cyber-password-accepted-001", "cyber-password-rejected-001",
        "cyber-data-encrypt-001", "cyber-data-decrypt-001", "cyber-mainframe-connect-001", "cyber-server-hum-001", "cyber-ddos-attack-001",
        "cyber-brute-force-001", "cyber-vpn-connect-001", "cyber-alert-intrusion-001", "cyber-trace-route-001", "cyber-system-lockdown-001",
        "cyber-secure-channel-001", "cyber-digital-sig-001", "cyber-quantum-key-001", "cyber-proxy-switch-001", "cyber-node-scan-001",
        "cyber-honeypot-trigger-001", "cyber-zero-day-patch-001", "cyber-backdoor-open-001", "cyber-network-ping-001", "cyber-system-reboot-001",

        "react-startup-hum-001", "react-stabilize-pulse-001", "react-energy-surge-001", "react-core-overload-001", "react-coolant-flow-001",
        "react-field-generate-001", "react-field-collapse-001", "react-power-transfer-001", "react-containment-beep-001", "react-warning-alarm-001",
        "react-shutdown-sequence-001", "react-plasma-ignite-001", "react-magnetic-lock-001", "react-energy-beam-001", "react-core-vent-001",
        "react-stabilizer-hum-001", "react-power-down-001", "react-emergency-purge-001", "react-quantum-flux-001", "react-energy-absorb-001",
        "react-energy-release-001", "react-coolant-leak-001", "react-reactor-ambience-001", "react-plasma-containment-001", "react-energy-siphon-001",
    ]

    # Fonction utilitaire pour générer un nom et une description simples
    def make_entry(sid, cat):
        name = sid.replace('-', ' ').title()
        tags = sid.replace('-001', '').split('-')
        return {
            "id": sid, "name": name, "category": cat, "description": f"{name} sound effect.", "tags": tags,
            "duration": "0.80s", "date": date_str,
            "mp3": f"audio/mp3/{sid}.mp3", "wav": f"audio/wav/{sid}.wav",
            "license": license_str, "status": "available",
            "previewMode": "procedural", "wavMode": "file", "mp3Mode": "file"
        }

    # Répartition dans les bons fichiers
    for sid in ids_to_add:
        if sid.startswith("sci-inst") or sid.startswith("veh") or sid.startswith("cyber") or sid.startswith("react"):
            sci_fi['sounds'].append(make_entry(sid, "Sci-Fi"))
        elif sid.startswith("infra"):
            environment['sounds'].append(make_entry(sid, "Environment"))

    save('sci-fi.json', sci_fi)
    save('environment.json', environment)
    save('gameplay.json', gameplay)
    print(f"✅ {len(ids_to_add)} nouveaux sons injectés avec succès.")

if __name__ == '__main__':
    main()