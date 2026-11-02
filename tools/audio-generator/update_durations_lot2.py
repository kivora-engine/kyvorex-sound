"""V1.1 lot 2 - met a jour la duree affichee des 31 sons reconstruits (data/catalog/*.json).
Lancer depuis la racine du projet : python3 tools/audio-generator/update_durations_lot2.py
Le script peut etre relance sans danger. Il ne change que le champ "duration" de ces 31 sons.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG_DIR = os.path.join(ROOT, 'data', 'catalog')

DURATIONS = {
    'craft-level-bubble-001': "0.51s",
    'craft-staple-gun-001': "0.23s",
    'craft-wire-snips-001': "0.20s",
    'cyber-backdoor-open-001': "0.99s",
    'cyber-mainframe-connect-001': "1.07s",
    'cyber-secure-channel-001': "0.67s",
    'cyber-system-reboot-001': "1.40s",
    'deer-alarm-bark-001': "0.45s",
    'forge-grindstone-spin-001': "1.05s",
    'game-final-result-reveal-001': "2.10s",
    'gravity-well-generate-001': "1.60s",
    'lab-pipette-release-001': "0.29s",
    'mech-turbine-spin-001': "1.65s",
    'react-containment-beep-001': "0.77s",
    'react-field-generate-001': "1.25s",
    'react-plasma-containment-001': "1.05s",
    'react-stabilizer-hum-001': "1.55s",
    'robot-arm-move-001': "0.86s",
    'ruin-relic-hum-001': "1.60s",
    'smart-device-activate-001': "0.65s",
    'spaceship-cryo-freeze-001': "1.30s",
    'spaceship-cryo-thaw-001': "1.35s",
    'spaceship-door-close-001': "0.80s",
    'spaceship-door-open-001': "0.94s",
    'spaceship-radar-sweep-001': "0.95s",
    'sub-engine-hum-001': "1.55s",
    'sub-torpedo-tube-open-001': "0.95s",
    'tech-energy-siphon-001': "1.15s",
    'unique-vehicle-boost-001': "1.05s",
    'veh-ignition-spark-001': "1.05s",
    'veh-mechanical-whine-001': "0.85s",
}


def main():
    changed = 0
    found = set()
    for fname in sorted(os.listdir(CATALOG_DIR)):
        if not fname.endswith('.json'):
            continue
        path = os.path.join(CATALOG_DIR, fname)
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        touched = False
        for s in data.get('sounds', []):
            sid = s.get('id')
            if sid in DURATIONS:
                found.add(sid)
                if s.get('duration') != DURATIONS[sid]:
                    s['duration'] = DURATIONS[sid]
                    changed += 1
                    touched = True
        if touched:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write('\n')
    print("OK : " + str(changed) + " durees mises a jour (" + str(len(found)) + "/" + str(len(DURATIONS)) + " sons trouves)")


if __name__ == '__main__':
    main()
