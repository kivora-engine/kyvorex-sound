"""Mission 16 - injection des 25 sons (Motion Capture & Animation) dans data/catalog/gameplay.json.
Lancer depuis la racine du projet : python3 tools/audio-generator/inject_mission_16.py
Le script peut etre relance sans danger : un son deja present est ignore.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG_DIR = os.path.join(ROOT, 'data', 'catalog')

DATE_STR = "2026-10-31"
LICENSE_STR = "KYVOREX Free Sound License 1.0"
CATEGORY = "Gameplay"
TARGET_FILE = "gameplay.json"

SOUNDS = [
    ('anim-sensor-suit-calibrate-001', 'Sensor Suit Calibrate 001', 'A motion capture suit calibrates with rising scan beeps and a final confirmation tone.',
     ['anim', 'sensor', 'suit', 'calibrate', 'mocap', 'capture', 'combinaison', 'etalonner'],
     "1.35s"),
    ('anim-marker-track-lock-001', 'Marker Track Lock 001', 'An optical tracker locks onto a marker with a quick two-tone blip.',
     ['anim', 'marker', 'track', 'lock', 'optical', 'marqueur', 'suivi', 'verrou'],
     "0.24s"),
    ('anim-capture-start-countdown-001', 'Capture Start Countdown 001', 'Three countdown ticks lead into a bright recording-start tone.',
     ['anim', 'capture', 'start', 'countdown', 'record', 'enregistrer', 'decompte', 'debut'],
     "1.65s"),
    ('anim-capture-stop-001', 'Capture Stop 001', 'Recording stops with two falling beeps and a short fading tone.',
     ['anim', 'capture', 'stop', 'record', 'end', 'arreter', 'fin', 'enregistrement'],
     "0.52s"),
    ('anim-keyframe-set-001', 'Keyframe Set 001', 'A keyframe is set on the timeline with a sharp click and a soft confirming tick.',
     ['anim', 'keyframe', 'set', 'timeline', 'click', 'image-cle', 'chronologie', 'cle'],
     "0.19s"),
    ('anim-keyframe-scrub-001', 'Keyframe Scrub 001', 'Dragging through a timeline produces a fast run of ticks that rise and fall in pitch.',
     ['anim', 'keyframe', 'scrub', 'timeline', 'drag', 'defilement', 'chronologie', 'glisser'],
     "0.95s"),
    ('anim-joint-ik-snap-001', 'Joint IK Snap 001', 'An inverse-kinematics joint snaps into place with a springy twang and a small servo whirr.',
     ['anim', 'joint', 'ik', 'snap', 'spring', 'articulation', 'ressort', 'claquement'],
     "0.23s"),
    ('anim-ragdoll-collapse-001', 'Ragdoll Collapse 001', 'A character goes limp, hitting the ground in a series of softer and softer thumps with cloth rustle.',
     ['anim', 'ragdoll', 'collapse', 'limp', 'fall', 'pantin', 'chute', 'inerte'],
     "0.70s"),
    ('anim-rig-bind-weld-001', 'Rig Bind Weld 001', 'A skeleton rig binds to a mesh with a rising tone, quickening ticks and a final click.',
     ['anim', 'rig', 'bind', 'skeleton', 'skin', 'squelette', 'lier', 'maillage'],
     "0.65s"),
    ('anim-blend-crossfade-001', 'Blend Crossfade 001', 'Two animation layers blend into each other as one tone falls while another rises.',
     ['anim', 'blend', 'crossfade', 'transition', 'mix', 'fondu', 'melange', 'transition'],
     "1.05s"),
    ('anim-loop-wrap-rewind-001', 'Loop Wrap Rewind 001', 'An animation loop wraps around with a quick rewinding swoop and a restart tick.',
     ['anim', 'loop', 'wrap', 'rewind', 'restart', 'boucle', 'rembobiner', 'redemarrer'],
     "0.44s"),
    ('anim-retarget-sweep-001', 'Retarget Sweep 001', 'A motion is retargeted to a new skeleton with a scanning sweep, stepped notes and a confirmation tone.',
     ['anim', 'retarget', 'sweep', 'skeleton', 'motion', 'retargeting', 'balayage', 'squelette'],
     "1.10s"),
    ('anim-pose-freeze-hold-001', 'Pose Freeze Hold 001', 'A pose is frozen with an abrupt tone cut and a faint hum that holds underneath.',
     ['anim', 'pose', 'freeze', 'hold', 'still', 'figer', 'pose', 'maintenir'],
     "0.65s"),
    ('anim-pose-mirror-flip-001', 'Pose Mirror Flip 001', 'A pose is mirrored with a whoosh and a symmetrical up-and-down chirp pair.',
     ['anim', 'pose', 'mirror', 'flip', 'symmetry', 'miroir', 'inverser', 'symetrie'],
     "0.45s"),
    ('anim-onion-skin-ghost-001', 'Onion Skin Ghost 001', 'A frame echoes into fading ghost copies, like onion-skin frames trailing behind a motion.',
     ['anim', 'onion', 'skin', 'ghost', 'echo', 'fantome', 'echo', 'images'],
     "0.77s"),
    ('anim-motion-trail-whoosh-001', 'Motion Trail Whoosh 001', 'A motion trail streaks past with a filtered whoosh, a rising tone and a trail of sparkles.',
     ['anim', 'motion', 'trail', 'whoosh', 'streak', 'trainee', 'mouvement', 'souffle'],
     "0.85s"),
    ('anim-foot-plant-lock-001', 'Foot Plant Lock 001', 'A foot plants on the ground and locks with a thud and a precise high click.',
     ['anim', 'foot', 'plant', 'lock', 'step', 'pied', 'verrouiller', 'pas'],
     "0.15s"),
    ('anim-hand-grip-servo-001', 'Hand Grip Servo 001', 'A robotic hand closes in six servo steps and clacks shut on an object.',
     ['anim', 'hand', 'grip', 'servo', 'close', 'main', 'servomoteur', 'saisir'],
     "0.55s"),
    ('anim-expression-morph-001', 'Expression Morph 001', 'A face morphs between expressions with a smooth rising and falling squish.',
     ['anim', 'expression', 'morph', 'face', 'blend', 'visage', 'morphose', 'expression'],
     "0.70s"),
    ('anim-tpose-calibrate-001', 'T-Pose Calibrate 001', 'A character holds a T-pose while four rising notes confirm the calibration.',
     ['anim', 'tpose', 'calibrate', 'pose', 'character', 'etalonnage', 'personnage', 'pose'],
     "1.00s"),
    ('anim-physics-bake-001', 'Physics Bake 001', 'A physics simulation bakes with quickening ticks and finishes with a bright chime.',
     ['anim', 'physics', 'bake', 'simulation', 'done', 'physique', 'simulation', 'terminer'],
     "1.46s"),
    ('anim-frame-step-tick-001', 'Frame Step Tick 001', 'Stepping through animation frames, six crisp ticks with slightly changing pitch.',
     ['anim', 'frame', 'step', 'tick', 'timeline', 'image', 'pas', 'tic'],
     "0.96s"),
    ('anim-capture-jitter-001', 'Capture Jitter 001', 'Noisy capture data jitters with sudden random pitch jumps.',
     ['anim', 'capture', 'jitter', 'noise', 'glitch', 'bruit', 'tremblement', 'donnees'],
     "0.75s"),
    ('anim-render-complete-chime-001', 'Render Complete Chime 001', 'A finished render is announced by three rising chime notes.',
     ['anim', 'render', 'complete', 'chime', 'done', 'rendu', 'termine', 'notification'],
     "1.05s"),
    ('anim-hit-react-stagger-001', 'Hit React Stagger 001', 'A character takes a hit and staggers backward in three heavy steps.',
     ['anim', 'hit', 'react', 'stagger', 'impact', 'coup', 'reaction', 'chanceler'],
     "0.80s"),
]

def load(name):
    with open(os.path.join(CATALOG_DIR, name), 'r', encoding='utf-8') as f:
        return json.load(f)

def save(name, data):
    with open(os.path.join(CATALOG_DIR, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

def main():
    print("Injection des 25 sons de la Mission 16 (Motion Capture & Animation)...")
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
