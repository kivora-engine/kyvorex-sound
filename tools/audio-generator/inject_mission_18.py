"""Mission 18 - injection des 25 sons (Smart Cities) dans data/catalog/environment.json.
Lancer depuis la racine du projet : python3 tools/audio-generator/inject_mission_18.py
Le script peut etre relance sans danger : un son deja present est ignore.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG_DIR = os.path.join(ROOT, 'data', 'catalog')

DATE_STR = "2026-10-31"
LICENSE_STR = "KYVOREX Free Sound License 1.0"
CATEGORY = "Environment"
TARGET_FILE = "environment.json"

SOUNDS = [
    ('city-autonomous-pod-glide-001', 'Autonomous Pod Glide 001', 'An autonomous transit pod glides past with a smooth electric hum and a soft wind of motion.',
     ['city', 'autonomous', 'pod', 'glide', 'transit', 'autonome', 'navette', 'electrique'],
     "1.25s"),
    ('city-maglev-station-arrive-001', 'Maglev Station Arrive 001', 'A maglev train brakes into a station with a falling whine and two arrival chimes.',
     ['city', 'maglev', 'station', 'arrive', 'train', 'arrivee', 'gare', 'lévitation'],
     "2.40s"),
    ('city-drone-delivery-drop-001', 'Drone Delivery Drop 001', 'A delivery drone hovers, releases its package with a click and the parcel lands with a soft thud.',
     ['city', 'drone', 'delivery', 'drop', 'parcel', 'livraison', 'colis', 'largage'],
     "0.95s"),
    ('city-smart-streetlight-wake-001', 'Smart Streetlight Wake 001', 'A smart streetlight switches on with a relay click, a warm hum and a final tick.',
     ['city', 'smart', 'streetlight', 'wake', 'lamp', 'lampadaire', 'intelligent', 'allumer'],
     "0.80s"),
    ('city-sensor-mesh-ping-001', 'Sensor Mesh Ping 001', 'A chain of city sensors pings one after another in a rising, echoing mesh.',
     ['city', 'sensor', 'mesh', 'ping', 'network', 'capteur', 'reseau', 'maille'],
     "1.30s"),
    ('city-ev-charge-start-001', 'EV Charge Start 001', 'An electric vehicle plugs in with a click, a rising hum and two confirmation beeps.',
     ['city', 'ev', 'charge', 'start', 'plug', 'recharge', 'electrique', 'branchement'],
     "1.10s"),
    ('city-ev-charge-complete-001', 'EV Charge Complete 001', 'A charger winds down and signals a full battery with two bright chimes.',
     ['city', 'ev', 'charge', 'complete', 'full', 'recharge', 'terminee', 'batterie'],
     "1.35s"),
    ('city-traffic-ai-reroute-001', 'Traffic AI Reroute 001', 'A traffic system scans for a new route with four quick blips and a confirming tone.',
     ['city', 'traffic', 'ai', 'reroute', 'route', 'trafic', 'itineraire', 'intelligence'],
     "0.85s"),
    ('city-smart-crossing-beacon-001', 'Smart Crossing Beacon 001', 'A smart pedestrian crossing ticks faster and higher as the time runs out, then ends on a long tone.',
     ['city', 'smart', 'crossing', 'beacon', 'pedestrian', 'passage', 'pieton', 'balise'],
     "2.10s"),
    ('city-recycling-sorter-whir-001', 'Recycling Sorter Whir 001', 'A recycling sorter whirs and clacks as it pushes items into the right bins.',
     ['city', 'recycling', 'sorter', 'whir', 'conveyor', 'recyclage', 'trieur', 'tapis'],
     "1.55s"),
    ('city-smart-bin-compact-001', 'Smart Bin Compact 001', 'A smart bin compacts its waste with a motor groan, crunching and a final thud.',
     ['city', 'smart', 'bin', 'compact', 'trash', 'poubelle', 'compacter', 'dechets'],
     "1.10s"),
    ('city-air-quality-alert-001', 'Air Quality Alert 001', 'A gentle three-note descending tone warns of poor air quality.',
     ['city', 'air', 'quality', 'alert', 'pollution', 'qualite', 'alerte', 'air'],
     "0.95s"),
    ('city-hologram-billboard-flicker-001', 'Hologram Billboard Flicker 001', 'A holographic billboard flickers to life, buzzing and popping with electrical stutters.',
     ['city', 'hologram', 'billboard', 'flicker', 'ad', 'hologramme', 'panneau', 'scintiller'],
     "1.25s"),
    ('city-smart-glass-tint-001', 'Smart Glass Tint 001', 'Smart glass tints from clear to dark with a smooth electronic shift and a small click.',
     ['city', 'smart', 'glass', 'tint', 'window', 'verre', 'teinte', 'fenetre'],
     "0.96s"),
    ('city-elevator-pod-chime-001', 'Elevator Pod Chime 001', 'A smart elevator pod glides with a low hum and arrives with two bell tones.',
     ['city', 'elevator', 'pod', 'chime', 'arrive', 'ascenseur', 'nacelle', 'arrivee'],
     "1.85s"),
    ('city-parking-spot-guide-001', 'Parking Spot Guide 001', 'A parking guidance system beeps faster as you near the free spot and confirms with a long tone.',
     ['city', 'parking', 'spot', 'guide', 'assist', 'stationnement', 'place', 'guidage'],
     "1.98s"),
    ('city-pneumatic-tube-transit-001', 'Pneumatic Tube Transit 001', 'A capsule rushes through a pneumatic tube and arrives with a quick pop.',
     ['city', 'pneumatic', 'tube', 'transit', 'capsule', 'pneumatique', 'capsule', 'transport'],
     "0.98s"),
    ('city-water-grid-valve-open-001', 'Water Grid Valve Open 001', 'A smart valve in the water grid whirs open, clunks and releases a rush of water.',
     ['city', 'water', 'grid', 'valve', 'open', 'eau', 'vanne', 'reseau'],
     "1.55s"),
    ('city-ticket-gate-tap-001', 'Ticket Gate Tap 001', 'A transit gate accepts a card tap with a beep, a servo swing and a clack.',
     ['city', 'ticket', 'gate', 'tap', 'transit', 'portique', 'carte', 'validation'],
     "0.50s"),
    ('city-street-robot-sweeper-001', 'Street Robot Sweeper 001', 'A street-cleaning robot trundles along, its motor droning and brushes scratching.',
     ['city', 'street', 'robot', 'sweeper', 'clean', 'rue', 'balayeur', 'nettoyage'],
     "1.65s"),
    ('city-emergency-priority-signal-001', 'Emergency Priority Signal 001', 'An emergency vehicle sends a priority signal to the road network in two rising chirp triplets.',
     ['city', 'emergency', 'priority', 'signal', 'vehicle', 'urgence', 'priorite', 'vehicule'],
     "0.87s"),
    ('city-solar-panel-track-001', 'Solar Panel Track 001', 'A solar panel array tracks the sun with a slow stepper motor, ticking steadily.',
     ['city', 'solar', 'panel', 'track', 'stepper', 'solaire', 'panneau', 'moteur'],
     "1.35s"),
    ('city-data-hub-hum-001', 'Data Hub Hum 001', 'A city data hub hums with fan noise and the occasional blip of traffic.',
     ['city', 'data', 'hub', 'hum', 'server', 'donnees', 'serveur', 'ronronnement'],
     "1.85s"),
    ('city-crowd-density-pulse-001', 'Crowd Density Pulse 001', 'A crowd-monitoring scan sweeps upward, each pulse marking a busy zone.',
     ['city', 'crowd', 'density', 'pulse', 'scan', 'foule', 'densite', 'analyse'],
     "0.95s"),
    ('city-skybridge-conveyor-glide-001', 'Skybridge Conveyor Glide 001', 'A moving walkway on a skybridge glides along with a low hum and the soft rhythm of its belt.',
     ['city', 'skybridge', 'conveyor', 'glide', 'walkway', 'passerelle', 'tapis', 'roulant'],
     "2.05s"),
]

def load(name):
    with open(os.path.join(CATALOG_DIR, name), 'r', encoding='utf-8') as f:
        return json.load(f)

def save(name, data):
    with open(os.path.join(CATALOG_DIR, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

def main():
    print("Injection des 25 sons de la Mission 18 (Smart Cities)...")
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
