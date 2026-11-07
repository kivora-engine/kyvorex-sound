"""Remastering V1.1 - lot 1 : level harmonisation.
Gain factors applied to the final samples of the listed sounds (target: active RMS about -21.5 dBFS,
peak never above 0.6). Sounds not listed are left untouched."""

LEVEL_GAINS = {
    'bat-wings-flutter-001': 7.943, 'battery-recharge-001': 1.362, 'bird-chirp-001': 2.268,
    'board-game-token-move-001': 7.943, 'chains-rattle-001': 4.413, 'city-recycling-sorter-whir-001': 1.197,
    'coin-flip-table-001': 1.485, 'craft-brick-trowel-001': 3.235, 'craft-caulking-gun-001': 1.442,
    'craft-lock-picking-001': 3.038, 'craft-nail-puller-001': 4.899, 'craft-paint-brush-001': 5.931,
    'craft-pencil-mark-001': 5.817, 'craft-plaster-scrape-001': 3.333, 'craft-rasp-wood-001': 4.347,
    'craft-rivet-gun-001': 0.65, 'craft-soldering-gun-001': 2.317, 'craft-tape-measure-001': 1.847,
    'craft-tile-cutting-001': 2.24, 'craft-wood-sanding-001': 4.691, 'cricket-single-call-001': 1.539,
    'cryo-pod-open-001': 0.716, 'cyber-brute-force-001': 2.148, 'cyber-data-decrypt-001': 2.569,
    'cyber-data-encrypt-001': 2.569, 'cyber-ddos-attack-001': 3.357, 'cyber-digital-sig-001': 2.361,
    'cyber-firewall-block-001': 0.724, 'cyber-honeypot-trigger-001': 3.923, 'cyber-network-ping-001': 2.294,
    'cyber-node-scan-001': 3.084, 'cyber-password-accepted-001': 1.888, 'cyber-server-hum-001': 1.372,
    'cyber-trace-route-001': 1.352, 'cyber-vpn-connect-001': 1.441, 'cyber-zero-day-patch-001': 1.494,
    'data-corruption-001': 1.89, 'data-stream-flow-001': 2.148, 'dice-cup-shake-001': 1.916,
    'dice-single-roll-001': 4.333, 'digital-footprint-001': 1.884, 'digital-map-render-001': 4.519,
    'dolphin-click-train-001': 2.942, 'door-metal-open-001': 1.355, 'door-open-001': 1.331,
    'env-avalanche-001': 0.665, 'env-bamboo-creak-001': 1.463, 'env-desert-wind-001': 2.12,
    'env-earthquake-rumble-001': 0.526, 'env-frozen-lake-crack-001': 1.911, 'env-geyser-eruption-001': 0.611,
    'env-glacier-crack-001': 0.474, 'env-icicle-fall-001': 0.71, 'env-lava-bubble-001': 0.671,
    'env-quarry-blast-001': 0.555, 'env-quicksand-001': 0.81, 'env-rock-fall-001': 3.432,
    'env-sandstorm-001': 0.664, 'env-volcanic-lightning-001': 0.597, 'env-volcanic-vent-001': 0.803,
    'environment-thunder-001': 0.716, 'epic-boss-defeat-001': 0.552, 'epic-multiverse-collapse-001': 4.849,
    'epic-portal-destroy-001': 0.722, 'epic-power-surge-001': 0.681, 'epic-time-shatter-001': 0.451,
    'experience-gain-001': 2.053, 'fire-crackle-001': 1.453, 'footstep-gravel-001': 0.566,
    'footstep-gravel-loose-001': 3.518, 'footstep-sand-dunes-001': 5.62, 'footstep-shallow-water-001': 1.367,
    'footstep-single-001': 0.629, 'footstep-wet-grass-001': 1.46, 'footstep-wood-hollow-001': 0.805,
    'forest-ambience-001': 5.551, 'forge-anvil-strike-heavy-001': 0.613, 'forge-chain-pull-001': 4.385,
    'forge-coal-shovel-001': 5.554, 'forge-metal-fold-001': 3.49, 'forge-rivet-gun-001': 0.617,
    'forge-weld-seam-001': 0.811, 'fx-armor-break-001': 0.701, 'fx-dimension-rift-001': 0.681,
    'fx-illusion-break-001': 0.585, 'fx-invisibility-001': 6.864, 'fx-mind-blast-001': 0.526,
    'fx-reality-glitch-001': 0.46, 'fx-rune-activate-001': 1.515, 'fx-weapon-enchant-001': 1.852,
    'heavy-landing-dirt-001': 0.764, 'hit-impact-001': 0.668, 'horse-snort-001': 3.68,
    'ind-conveyor-heavy-001': 1.684, 'ind-forge-hammer-001': 0.523, 'ind-forklift-move-001': 1.353,
    'ind-furnace-roar-001': 4.808, 'ind-heavy-door-lock-001': 0.776, 'ind-metal-pour-001': 4.165,
    'ind-robot-arm-weld-001': 0.829, 'ind-scrap-metal-crush-001': 3.797, 'ind-steam-release-001': 0.741,
    'ind-ventilation-hum-001': 7.943, 'infra-gate-close-001': 1.639, 'infra-train-brake-squeal-001': 1.985,
    'lab-glass-stirring-001': 5.732, 'lab-microscope-focus-001': 2.616, 'lab-radiation-counter-burst-001': 1.532,
    'lab-spectrometer-scan-001': 1.461, 'ladder-metal-rattle-001': 1.451, 'lion-territorial-roar-001': 0.828,
    'magic-dispel-001': 1.421, 'magical-trap-snap-001': 0.54, 'mech-chain-rattle-001': 3.9,
    'mech-hammer-strike-001': 0.756, 'mech-pneumatic-hiss-001': 1.364, 'mech-steam-burst-001': 0.83,
    'micro-ant-colony-march-001': 1.769, 'micro-bark-beetle-gnaw-001': 1.721, 'micro-caterpillar-chew-001': 2.156,
    'micro-leafcutter-snip-001': 1.576, 'micro-spore-cloud-release-001': 1.849, 'micro-thorn-scrape-001': 1.724,
    'monkey-canopy-leap-001': 4.176, 'music-box-winding-001': 2.661, 'neural-network-connect-001': 2.572,
    'object-break-001': 0.721, 'ocean-wave-001': 1.635, 'plasma-welding-001': 0.766,
    'playing-card-deal-001': 4.278, 'poker-chip-slide-001': 7.214, 'react-coolant-flow-001': 1.688,
    'react-core-overload-001': 2.062, 'react-core-vent-001': 2.918, 'react-emergency-purge-001': 2.063,
    'react-quantum-flux-001': 2.983, 'react-reactor-ambience-001': 7.943, 'react-stabilize-pulse-001': 1.208,
    'robot-circuit-hum-001': 1.406, 'robot-claw-grab-001': 0.825, 'robot-claw-release-001': 1.481,
    'robot-lock-release-001': 6.221, 'robot-overload-001': 2.084, 'robot-scan-sweep-001': 1.352,
    'robot-sensor-ping-001': 1.54, 'rock-climb-grip-001': 3.566, 'ruin-artifact-shatter-001': 0.614,
    'ruin-lock-engage-001': 0.727, 'ruin-lock-release-001': 3.883, 'ruin-relic-activate-001': 1.314,
    'ruin-stone-grind-001': 4.008, 'ruin-trap-trigger-001': 0.579, 'runic-translation-001': 2.972,
    'sci-fi-data-transfer-001': 1.706, 'sci-inst-chemical-analysis-001': 3.399, 'sci-inst-dna-helix-scan-001': 1.395,
    'sci-inst-dna-sequencer-001': 2.517, 'sci-inst-electron-beam-001': 0.8, 'sci-inst-lab-ambience-001': 7.943,
    'sci-inst-microscope-laser-001': 1.46, 'sci-inst-microscope-zoom-001': 1.424, 'sci-inst-radar-sweep-001': 1.43,
    'sci-inst-radiation-detector-001': 1.526, 'sci-inst-spectrum-analyzer-001': 1.923, 'sci-inst-telescope-focus-001': 1.424,
    'shield-block-001': 1.412, 'signal-jammer-001': 2.737, 'slide-stone-surface-001': 4.972,
    'snare-drum-roll-short-001': 3.203, 'spaceship-cockpit-click-001': 2.148, 'spaceship-comms-static-001': 1.631,
    'spaceship-emp-burst-001': 2.922, 'spaceship-hull-breach-001': 2.133, 'spaceship-life-support-001': 1.405,
    'spaceship-navigation-ping-001': 1.541, 'spaceship-stabilizer-001': 1.442, 'spell-lightning-001': 0.634,
    'sub-airlock-close-001': 1.457, 'sub-control-panel-beep-001': 2.148, 'sub-depth-charge-001': 0.683,
    'sub-docking-clamp-001': 0.796, 'sub-hatch-close-001': 4.365, 'sub-hatch-open-001': 3.736,
    'sub-navigation-beep-001': 1.537, 'sub-radar-sweep-001': 3.048, 'summon-creature-001': 1.572,
    'sword-swing-001': 1.348, 'system-overload-001': 0.662, 'tech-cyber-terraform-001': 4.48,
    'tech-drone-squadron-001': 1.708, 'tech-matter-compiler-001': 1.818, 'tech-neural-link-001': 1.888,
    'tool-dropping-wrench-001': 1.448, 'tool-glue-apply-001': 1.442, 'tool-metal-scrape-001': 3.608,
    'tool-picking-up-nails-001': 3.048, 'tool-rope-tie-001': 6.535, 'tool-saw-wood-001': 3.372,
    'tool-solder-iron-001': 2.188, 'tool-stone-chisel-001': 0.801, 'tool-toolbox-close-001': 4.16,
    'tool-wire-strip-001': 4.27, 'tool-wood-creak-001': 5.634, 'trapdoor-trigger-001': 0.723,
    'ui-data-processing-001': 2.148, 'ui-drag-drop-002': 1.325, 'ui-dropdown-open-001': 1.609,
    'ui-file-export-001': 1.976, 'ui-file-import-001': 1.976, 'ui-hover-002': 2.362,
    'ui-panel-collapse-001': 1.522, 'ui-panel-expand-001': 1.523, 'ui-scroll-001': 3.925,
    'ui-slider-adjust-001': 2.148, 'ui-sync-complete-001': 1.442, 'ui-sync-start-001': 1.493,
    'ui-tab-switch-002': 2.365, 'unique-magic-mirror-shatter-001': 0.695, 'unique-reality-glitch-short-001': 0.71,
    'unique-stealth-footstep-001': 7.943, 'unique-wall-climb-001': 1.442, 'veh-brake-squeal-001': 1.499,
    'veh-cockpit-ambience-001': 7.943, 'veh-crash-metal-impact-001': 0.523, 'veh-engine-cooling-001': 1.362,
    'veh-exhaust-burst-001': 2.307, 'veh-fuel-pump-001': 1.352, 'veh-gear-grind-001': 3.059,
    'veh-gear-shift-heavy-001': 0.639, 'veh-speedometer-ping-001': 2.148, 'veh-wheel-spin-001': 4.612,
    'wireless-charge-001': 1.991,
}


def _scaled(fn, gain):
    def run():
        return [x * gain for x in fn()]
    return run


def apply_levels(presets):
    out = {}
    for sid, fn in presets.items():
        gain = LEVEL_GAINS.get(sid)
        out[sid] = fn if gain is None else _scaled(fn, gain)
    return out
