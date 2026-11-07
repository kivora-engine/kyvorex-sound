"""V1.1 generation 1 - met a jour la duree affichee des 125 sons reconstruits (data/catalog/*.json).
Lancer depuis la racine du projet : python3 tools/audio-generator/update_durations_gen1.py
Le script peut etre relance sans danger. Il ne change que le champ "duration" de ces 125 sons.
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG_DIR = os.path.join(ROOT, 'data', 'catalog')

DURATIONS = {
    'alien-communication-001': "1.70s",
    'artifact-discovery-001': "1.40s",
    'aura-reveal-001': "0.90s",
    'bees-swarm-pass-001': "0.90s",
    'black-hole-collapse-001': "1.60s",
    'boar-ground-snuffle-001': "1.20s",
    'body-roll-gravel-001': "0.70s",
    'camel-call-001': "1.10s",
    'chest-open-001': "1.25s",
    'cicada-day-chorus-001': "0.90s",
    'craft-cement-mix-001': "0.90s",
    'craft-hacksaw-metal-001': "1.15s",
    'craft-metal-filing-001': "1.05s",
    'craft-paint-roller-001': "1.10s",
    'creepy-whisper-001': "0.80s",
    'crocodile-water-movement-001': "0.70s",
    'domino-chain-fall-001': "1.50s",
    'duck-flock-takeoff-001': "0.70s",
    'elephant-trumpet-001': "1.40s",
    'elevator-mechanism-001': "0.70s",
    'env-aurora-borealis-001': "2.20s",
    'env-bioluminescent-forest-001': "1.60s",
    'env-blizzard-001': "2.20s",
    'env-crystal-cave-hum-001': "1.60s",
    'env-desert-mirage-shimmer-001': "1.60s",
    'env-floating-islands-001': "2.20s",
    'env-geyser-mini-001': "1.40s",
    'env-gravity-well-pulse-001': "0.90s",
    'env-jungle-rain-001': "1.60s",
    'env-magnetic-anomaly-001': "1.10s",
    'env-meteor-shower-distant-001': "1.30s",
    'env-river-flow-001': "2.20s",
    'env-sandstorm-distant-001': "2.20s",
    'env-solar-flare-wind-001': "1.60s",
    'env-swamp-ambience-001': "1.60s",
    'env-tide-pool-001': "1.10s",
    'env-waterfall-001': "2.20s",
    'env-waterfall-misty-001': "1.60s",
    'environment-rain-start-001': "1.90s",
    'environment-wind-gust-001': "0.80s",
    'epic-ancient-awakens-001': "1.60s",
    'epic-artifact-awaken-001': "2.20s",
    'explosion-small-001': "1.00s",
    'forge-anvil-ring-001': "0.70s",
    'forge-bellows-blow-001': "0.90s",
    'forge-cooling-crackle-001': "0.70s",
    'forge-crucible-pour-001': "0.90s",
    'forge-file-metal-001': "1.00s",
    'forge-glue-apply-001': "1.15s",
    'forge-metal-bend-001': "0.70s",
    'forge-polish-leather-001': "0.70s",
    'forge-quenching-sizzle-001': "0.70s",
    'forge-workshop-ambience-001': "1.60s",
    'frog-pond-croak-001': "1.30s",
    'futuristic-surgery-001': "0.70s",
    'game-tie-break-start-001': "1.40s",
    'game-timer-expire-001': "1.10s",
    'hyena-cackle-001': "1.30s",
    'infra-airport-bell-001': "1.45s",
    'infra-bridge-lift-001': "1.30s",
    'infra-cargo-crane-move-001': "1.10s",
    'infra-crosswalk-signal-001': "1.25s",
    'infra-drawbridge-motor-001': "1.10s",
    'infra-ferry-horn-001': "1.10s",
    'infra-gate-open-001': "0.70s",
    'infra-highway-traffic-001': "2.20s",
    'infra-parking-barrier-close-001': "0.90s",
    'infra-parking-barrier-open-001': "0.65s",
    'infra-runway-jet-001': "1.60s",
    'infra-subway-arrival-001': "0.90s",
    'infra-train-track-clatter-001': "1.70s",
    'infra-tunnel-ambience-001': "2.20s",
    'infra-tunnel-wind-001': "1.60s",
    'ion-thruster-ignite-001': "0.90s",
    'laser-grid-activate-001': "1.20s",
    'leaves-rustle-001': "0.70s",
    'mech-conveyor-move-001': "0.90s",
    'mech-heavy-door-slide-001': "0.70s",
    'mech-motor-start-001': "1.20s",
    'mech-motor-stop-001': "0.85s",
    'mech-system-shutdown-001': "0.90s",
    'mech-valve-hiss-001': "1.00s",
    'meteor-shower-pass-001': "1.30s",
    'mosquito-near-ear-001': "1.50s",
    'nebula-ambience-001': "2.20s",
    'night-insects-001': "0.80s",
    'owl-wing-pass-001': "1.00s",
    'playing-cards-shuffle-001': "1.10s",
    'potion-drink-001': "1.50s",
    'power-up-002': "1.10s",
    'rope-climb-strain-001': "1.00s",
    'rope-swing-pass-001': "1.05s",
    'ruin-ancient-door-close-001': "1.30s",
    'ruin-ancient-door-open-001': "1.30s",
    'ruin-ancient-magic-001': "1.80s",
    'ruin-archaeological-scan-001': "0.90s",
    'ruin-artifact-beam-001': "0.90s",
    'ruin-block-move-001': "1.00s",
    'ruin-glyph-light-001': "1.20s",
    'ruin-rune-glow-001': "1.50s",
    'ruin-sarcophagus-open-001': "0.90s",
    'ruin-secret-wall-slide-001': "0.90s",
    'ruin-statue-turn-001': "1.25s",
    'ruin-temple-bell-001': "1.30s",
    'ruin-temple-door-rumble-001': "1.30s",
    'ruin-temple-wind-001': "1.60s",
    'snake-hiss-long-001': "0.90s",
    'space-station-alarm-001': "0.80s",
    'sub-airlock-open-001': "1.10s",
    'sub-ballast-blow-001': "0.90s",
    'sub-dive-alarm-001': "1.60s",
    'sub-engine-reverse-001': "0.90s",
    'sub-oxygen-warning-001': "1.50s",
    'sub-propeller-start-001': "1.10s",
    'sub-propeller-stop-001': "1.10s",
    'sub-sonar-sweep-001': "1.80s",
    'sub-underwater-scan-001': "1.60s",
    'tool-drill-metal-001': "0.85s",
    'tool-drill-wood-001': "0.85s",
    'tool-sandpaper-rub-001': "1.15s",
    'underwater-movement-001': "1.40s",
    'unique-alchemy-brew-001': "0.90s",
    'unique-vent-crawl-001': "1.80s",
    'whale-song-low-001': "1.20s",
    'zero-gravity-float-001': "1.30s",
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
