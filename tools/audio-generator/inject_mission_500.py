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
    print("Injection des 55 nouveaux sons (Milestone 500) dans le catalogue...")
    gameplay = load('gameplay.json')
    alerts = load('alerts.json')
    sci_fi = load('sci-fi.json')
    environment = load('environment.json')
    
    date_str = "2026-10-27"
    license_str = "KYVOREX Free Sound License 1.0"

    epic = [
        ("epic-victory-fanfare-001", "Epic Victory Fanfare 001", "Grand victory fanfare.", "Alerts"),
        ("epic-legendary-unlock-001", "Epic Legendary Unlock 001", "Legendary unlock sound.", "Alerts"),
        ("epic-world-reveal-001", "Epic World Reveal 001", "Massive world reveal.", "Environment"),
        ("epic-power-surge-001", "Epic Power Surge 001", "Huge power surge.", "Gameplay"),
        ("epic-quest-complete-massive-001", "Epic Quest Complete Massive 001", "Massive quest completion.", "Alerts"),
        ("epic-transcendence-001", "Epic Transcendence 001", "Ascending to a higher plane.", "Sci-Fi"),
        ("epic-artifact-awaken-001", "Epic Artifact Awaken 001", "Artifact awakening.", "Gameplay"),
        ("epic-portal-destroy-001", "Epic Portal Destroy 001", "Destroying a portal.", "Sci-Fi"),
        ("epic-boss-defeat-001", "Epic Boss Defeat 001", "Defeating a major boss.", "Gameplay"),
        ("epic-champion-crown-001", "Epic Champion Crown 001", "Becoming the champion.", "Alerts"),
        ("epic-time-shatter-001", "Epic Time Shatter 001", "Shattering the time stream.", "Sci-Fi"),
        ("epic-energy-overflow-001", "Epic Energy Overflow 001", "Massive energy overflow.", "Sci-Fi"),
        ("epic-ancient-awakens-001", "Epic Ancient Awakens 001", "An ancient being awakens.", "Gameplay"),
        ("epic-multiverse-collapse-001", "Epic Multiverse Collapse 001", "The multiverse collapsing.", "Sci-Fi"),
        ("epic-final-stand-001", "Epic Final Stand 001", "The final battle begins.", "Gameplay"),
    ]

    adv_tech = [
        ("tech-nanobot-swarm-001", "Tech Nanobot Swarm 001", "Nanobot swarm.", "Sci-Fi"),
        ("tech-antigravity-boot-001", "Tech Antigravity Boot 001", "Antigravity booting.", "Sci-Fi"),
        ("tech-matter-compiler-001", "Tech Matter Compiler 001", "Matter compiling.", "Sci-Fi"),
        ("tech-warp-core-init-001", "Tech Warp Core Init 001", "Warp core initialization.", "Sci-Fi"),
        ("tech-ai-uplink-001", "Tech AI Uplink 001", "AI uplink connection.", "Sci-Fi"),
        ("tech-hologram-deploy-001", "Tech Hologram Deploy 001", "Hologram deployment.", "Sci-Fi"),
        ("tech-plasma-conduit-001", "Tech Plasma Conduit 001", "Plasma conduit humming.", "Sci-Fi"),
        ("tech-neural-link-001", "Tech Neural Link 001", "Neural link established.", "Sci-Fi"),
        ("tech-energy-siphon-001", "Tech Energy Siphon 001", "Energy siphon.", "Sci-Fi"),
        ("tech-quantum-entangle-001", "Tech Quantum Entangle 001", "Quantum entanglement.", "Sci-Fi"),
        ("tech-phase-shift-001", "Tech Phase Shift 001", "Phase shifting.", "Sci-Fi"),
        ("tech-singularity-form-001", "Tech Singularity Form 001", "Singularity formation.", "Sci-Fi"),
        ("tech-cyber-terraform-001", "Tech Cyber Terraform 001", "Cyber terraforming.", "Sci-Fi"),
        ("tech-drone-squadron-001", "Tech Drone Squadron 001", "Drone squadron flying.", "Sci-Fi"),
        ("tech-system-reboot-prime-001", "Tech System Reboot Prime 001", "Prime system reboot.", "Sci-Fi"),
    ]

    rare_env = [
        ("env-aurora-borealis-001", "Env Aurora Borealis 001", "Aurora borealis hum.", "Environment"),
        ("env-geyser-mini-001", "Env Geyser Mini 001", "Mini geyser eruption.", "Environment"),
        ("env-crystal-cave-hum-001", "Env Crystal Cave Hum 001", "Crystal cave resonance.", "Environment"),
        ("env-floating-islands-001", "Env Floating Islands 001", "Floating islands ambience.", "Environment"),
        ("env-meteor-shower-distant-001", "Env Meteor Shower Distant 001", "Distant meteor shower.", "Environment"),
        ("env-swamp-gas-bubble-001", "Env Swamp Gas Bubble 001", "Swamp gas bubbles.", "Environment"),
        ("env-desert-mirage-shimmer-001", "Env Desert Mirage Shimmer 001", "Desert mirage shimmer.", "Environment"),
        ("env-frozen-lake-crack-001", "Env Frozen Lake Crack 001", "Frozen lake cracking.", "Environment"),
        ("env-volcanic-lightning-001", "Env Volcanic Lightning 001", "Volcanic lightning.", "Environment"),
        ("env-bioluminescent-forest-001", "Env Bioluminescent Forest 001", "Bioluminescent forest.", "Environment"),
        ("env-sandstorm-distant-001", "Env Sandstorm Distant 001", "Distant sandstorm.", "Environment"),
        ("env-waterfall-misty-001", "Env Waterfall Misty 001", "Misty waterfall.", "Environment"),
        ("env-magnetic-anomaly-001", "Env Magnetic Anomaly 001", "Magnetic anomaly.", "Environment"),
        ("env-gravity-well-pulse-001", "Env Gravity Well Pulse 001", "Gravity well pulsing.", "Environment"),
        ("env-solar-flare-wind-001", "Env Solar Flare Wind 001", "Solar flare wind.", "Environment"),
    ]

    unique = [
        ("unique-alchemy-brew-001", "Unique Alchemy Brew 001", "Alchemy brewing.", "Gameplay"),
        ("unique-lockpick-snap-001", "Unique Lockpick Snap 001", "Lockpick snapping.", "Gameplay"),
        ("unique-trap-disarm-001", "Unique Trap Disarm 001", "Disarming a trap.", "Gameplay"),
        ("unique-stealth-footstep-001", "Unique Stealth Footstep 001", "Stealthy footstep.", "Gameplay"),
        ("unique-vent-crawl-001", "Unique Vent Crawl 001", "Crawling through a vent.", "Gameplay"),
        ("unique-wall-climb-001", "Unique Wall Climb 001", "Climbing a wall.", "Gameplay"),
        ("unique-vehicle-boost-001", "Unique Vehicle Boost 001", "Vehicle boost.", "Gameplay"),
        ("unique-cyber-deck-overheat-001", "Unique Cyber Deck Overheat 001", "Cyber deck overheating.", "Sci-Fi"),
        ("unique-magic-mirror-shatter-001", "Unique Magic Mirror Shatter 001", "Shattering a magic mirror.", "Gameplay"),
        ("unique-reality-glitch-short-001", "Unique Reality Glitch Short 001", "Short reality glitch.", "Sci-Fi"),
    ]

    def add_sound(target_list, sid, name, desc, cat):
        tags = sid.replace('-001', '').split('-')
        target_list['sounds'].append({
            "id": sid, "name": name, "category": cat, "description": desc, "tags": tags,
            "duration": "0.80s", "date": date_str,
            "mp3": f"audio/mp3/{sid}.mp3", "wav": f"audio/wav/{sid}.wav",
            "license": license_str, "status": "available",
            "previewMode": "procedural", "wavMode": "file", "mp3Mode": "file"
        })

    for s in epic: add_sound(gameplay if s[3]=="Gameplay" else (alerts if s[3]=="Alerts" else (sci_fi if s[3]=="Sci-Fi" else environment)), s[0], s[1], s[2], s[3])
    for s in adv_tech: add_sound(sci_fi, s[0], s[1], s[2], s[3])
    for s in rare_env: add_sound(environment, s[0], s[1], s[2], s[3])
    for s in unique: add_sound(gameplay if s[3]=="Gameplay" else sci_fi, s[0], s[1], s[2], s[3])

    save('gameplay.json', gameplay)
    save('alerts.json', alerts)
    save('sci-fi.json', sci_fi)
    save('environment.json', environment)
    print("✅ 55 nouveaux sons injectés avec succès.")

if __name__ == '__main__':
    main()