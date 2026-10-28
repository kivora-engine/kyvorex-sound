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
    print("Injection des 50 nouveaux sons (Robotique & Vaisseaux) dans le catalogue...")
    sci_fi = load('sci-fi.json')
    
    date_str = "2026-10-27"
    license_str = "KYVOREX Free Sound License 1.0"

    robot_sounds = [
        ("robot-arm-move-001", "Robot Arm Move 001", "Robotic arm moving.", ["robot", "arm", "robotics", "bras"]),
        ("robot-servo-activate-001", "Robot Servo Activate 001", "Servo motor activation.", ["robot", "servo", "robotics", "servo"]),
        ("robot-claw-grab-001", "Robot Claw Grab 001", "Robotic claw grabbing.", ["robot", "claw", "robotics", "pince"]),
        ("robot-claw-release-001", "Robot Claw Release 001", "Robotic claw releasing.", ["robot", "claw", "robotics", "pince"]),
        ("robot-joint-rotate-001", "Robot Joint Rotate 001", "Robotic joint rotating.", ["robot", "joint", "robotics", "articulation"]),
        ("robot-hydraulic-pump-001", "Robot Hydraulic Pump 001", "Hydraulic pump for robots.", ["robot", "hydraulic", "robotics", "pompe"]),
        ("robot-weld-spark-001", "Robot Weld Spark 001", "Robotic welding spark.", ["robot", "weld", "robotics", "soudure"]),
        ("robot-circuit-hum-001", "Robot Circuit Hum 001", "Robotic circuit humming.", ["robot", "circuit", "robotics", "circuit"]),
        ("robot-calibration-beep-001", "Robot Calibration Beep 001", "Robot calibration beep.", ["robot", "calibration", "robotics", "calibration"]),
        ("robot-scan-sweep-001", "Robot Scan Sweep 001", "Robotic scanning sweep.", ["robot", "scan", "robotics", "scan"]),
        ("robot-lock-engage-001", "Robot Lock Engage 001", "Robotic lock engaging.", ["robot", "lock", "robotics", "verrou"]),
        ("robot-lock-release-001", "Robot Lock Release 001", "Robotic lock releasing.", ["robot", "lock", "robotics", "verrou"]),
        ("robot-step-heavy-001", "Robot Step Heavy 001", "Heavy robotic step.", ["robot", "step", "robotics", "pas"]),
        ("robot-step-light-001", "Robot Step Light 001", "Light robotic step.", ["robot", "step", "robotics", "pas"]),
        ("robot-tool-switch-001", "Robot Tool Switch 001", "Switching robotic tools.", ["robot", "tool", "robotics", "outil"]),
        ("robot-assembly-line-001", "Robot Assembly Line 001", "Robotic assembly line.", ["robot", "assembly", "robotics", "assemblage"]),
        ("robot-error-buzz-001", "Robot Error Buzz 001", "Robotic error buzz.", ["robot", "error", "robotics", "erreur"]),
        ("robot-shutdown-001", "Robot Shutdown 001", "Robot shutting down.", ["robot", "shutdown", "robotics", "arrêt"]),
        ("robot-startup-001", "Robot Startup 001", "Robot starting up.", ["robot", "startup", "robotics", "démarrage"]),
        ("robot-drill-arm-001", "Robot Drill Arm 001", "Robotic drill arm.", ["robot", "drill", "robotics", "perceuse"]),
        ("robot-magnet-grab-001", "Robot Magnet Grab 001", "Robotic magnet grabbing.", ["robot", "magnet", "robotics", "aimant"]),
        ("robot-magnet-release-001", "Robot Magnet Release 001", "Robotic magnet releasing.", ["robot", "magnet", "robotics", "aimant"]),
        ("robot-sensor-ping-001", "Robot Sensor Ping 001", "Robotic sensor ping.", ["robot", "sensor", "robotics", "capteur"]),
        ("robot-battery-low-001", "Robot Battery Low 001", "Robot battery low warning.", ["robot", "battery", "robotics", "batterie"]),
        ("robot-overload-001", "Robot Overload 001", "Robot overloading.", ["robot", "overload", "robotics", "surcharge"]),
    ]

    ship_sounds = [
        ("spaceship-door-open-001", "Spaceship Door Open 001", "Spaceship door opening.", ["spaceship", "door", "space", "porte"]),
        ("spaceship-door-close-001", "Spaceship Door Close 001", "Spaceship door closing.", ["spaceship", "door", "space", "porte"]),
        ("spaceship-engine-hum-001", "Spaceship Engine Hum 001", "Spaceship engine humming.", ["spaceship", "engine", "space", "moteur"]),
        ("spaceship-warp-jump-001", "Spaceship Warp Jump 001", "Spaceship warp jumping.", ["spaceship", "warp", "space", "warp"]),
        ("spaceship-shield-hit-001", "Spaceship Shield Hit 001", "Spaceship shield impact.", ["spaceship", "shield", "space", "bouclier"]),
        ("spaceship-weapon-fire-001", "Spaceship Weapon Fire 001", "Spaceship weapon firing.", ["spaceship", "weapon", "space", "arme"]),
        ("spaceship-alert-system-001", "Spaceship Alert System 001", "Spaceship alert system.", ["spaceship", "alert", "space", "alerte"]),
        ("spaceship-navigation-ping-001", "Spaceship Navigation Ping 001", "Spaceship navigation ping.", ["spaceship", "navigation", "space", "navigation"]),
        ("spaceship-comms-static-001", "Spaceship Comms Static 001", "Spaceship comms static.", ["spaceship", "comms", "space", "communication"]),
        ("spaceship-docking-clamp-001", "Spaceship Docking Clamp 001", "Spaceship docking clamp.", ["spaceship", "docking", "space", "amarrage"]),
        ("spaceship-thruster-boost-001", "Spaceship Thruster Boost 001", "Spaceship thruster boost.", ["spaceship", "thruster", "space", "propulsion"]),
        ("spaceship-stabilizer-001", "Spaceship Stabilizer 001", "Spaceship stabilizer.", ["spaceship", "stabilizer", "space", "stabilisateur"]),
        ("spaceship-life-support-001", "Spaceship Life Support 001", "Spaceship life support.", ["spaceship", "life", "space", "support"]),
        ("spaceship-oxygen-leak-001", "Spaceship Oxygen Leak 001", "Spaceship oxygen leak.", ["spaceship", "oxygen", "space", "oxygène"]),
        ("spaceship-hull-breach-001", "Spaceship Hull Breach 001", "Spaceship hull breach.", ["spaceship", "hull", "space", "coque"]),
        ("spaceship-scan-sweep-001", "Spaceship Scan Sweep 001", "Spaceship scanning.", ["spaceship", "scan", "space", "scan"]),
        ("spaceship-target-lock-001", "Spaceship Target Lock 001", "Spaceship target lock.", ["spaceship", "target", "space", "cible"]),
        ("spaceship-emp-burst-001", "Spaceship EMP Burst 001", "Spaceship EMP burst.", ["spaceship", "emp", "space", "emp"]),
        ("spaceship-tractor-beam-001", "Spaceship Tractor Beam 001", "Spaceship tractor beam.", ["spaceship", "tractor", "space", "rayon"]),
        ("spaceship-cockpit-click-001", "Spaceship Cockpit Click 001", "Spaceship cockpit click.", ["spaceship", "cockpit", "space", "cockpit"]),
        ("spaceship-radar-sweep-001", "Spaceship Radar Sweep 001", "Spaceship radar sweep.", ["spaceship", "radar", "space", "radar"]),
        ("spaceship-gravity-off-001", "Spaceship Gravity Off 001", "Spaceship gravity off.", ["spaceship", "gravity", "space", "gravité"]),
        ("spaceship-gravity-on-001", "Spaceship Gravity On 001", "Spaceship gravity on.", ["spaceship", "gravity", "space", "gravité"]),
        ("spaceship-cryo-freeze-001", "Spaceship Cryo Freeze 001", "Spaceship cryo freezing.", ["spaceship", "cryo", "space", "cryo"]),
        ("spaceship-cryo-thaw-001", "Spaceship Cryo Thaw 001", "Spaceship cryo thawing.", ["spaceship", "cryo", "space", "cryo"]),
    ]

    for sid, name, desc, tags in robot_sounds + ship_sounds:
        sci_fi['sounds'].append({
            "id": sid, "name": name, "category": "Sci-Fi", "description": desc, "tags": tags,
            "duration": "0.50s", "date": date_str,
            "mp3": f"audio/mp3/{sid}.mp3", "wav": f"audio/wav/{sid}.wav",
            "license": license_str, "status": "available",
            "previewMode": "procedural", "wavMode": "file", "mp3Mode": "file"
        })

    save('sci-fi.json', sci_fi)
    print("✅ 50 nouveaux sons (Robotique + Vaisseaux) ajoutés à sci-fi.json")

if __name__ == '__main__':
    main()