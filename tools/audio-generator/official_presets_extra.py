"""Extra catalog presets - 45 sounds."""
import math
from synthesis import sine, square, triangle, sawtooth, white_noise, DEFAULT_SAMPLE_RATE

SR = DEFAULT_SAMPLE_RATE

def _wave_sample(wave_type, phase):
    ph = (phase / (2.0 * math.pi)) % 1.0
    if wave_type == 'sine': return math.sin(phase)
    if wave_type == 'square': return 1.0 if ph < 0.5 else -1.0
    if wave_type == 'triangle': return 4.0 * abs(ph - 0.5) - 1.0
    if wave_type == 'sawtooth': return 2.0 * ph - 1.0
    return 0.0

def _env_exp(n, attack):
    n_atk = max(1, int(attack * SR))
    if n_atk > n: n_atk = n
    out = []
    for i in range(n):
        if i < n_atk: out.append(i / float(n_atk))
        else:
            t = (i - n_atk) / float(max(1, n - n_atk))
            out.append(0.0001 ** t)
    return out

def _tone(wave_type, freq, dur, amplitude, attack):
    n = int(dur * SR)
    if n <= 0: return []
    env = _env_exp(n, attack)
    return [amplitude * _wave_sample(wave_type, 2.0 * math.pi * freq * i / SR) * env[i] for i in range(n)]

def _sweep(wave_type, f0, f1, dur, amplitude, attack):
    n = int(dur * SR)
    if n <= 0: return []
    env = _env_exp(n, attack)
    out = []
    phase = 0.0
    for i in range(n):
        t = i / float(max(1, n - 1))
        f = f0 * ((f1 / f0) ** t)
        phase += 2.0 * math.pi * f / SR
        out.append(amplitude * _wave_sample(wave_type, phase) * env[i])
    return out

def _noise(dur, amplitude, attack, seed=1):
    n = int(dur * SR)
    if n <= 0: return []
    env = _env_exp(n, attack)
    raw = white_noise(dur, SR, amplitude, seed=seed)
    out = [raw[i] * env[i] for i in range(min(n, len(raw)))]
    if len(out) < n: out.extend([0.0] * (n - len(out)))
    return out

def _mix(*parts):
    n = max((len(p) for p in parts), default=0)
    out = [0.0] * n
    for p in parts:
        for i in range(len(p)): out[i] += p[i]
    return out

def _at(samples, offset_sec, total_sec):
    n_total = int(total_sec * SR)
    n_off = int(offset_sec * SR)
    out = [0.0] * n_total
    for i, s in enumerate(samples):
        idx = n_off + i
        if idx < n_total: out[idx] += s
    return out

def _pad(samples, total_sec):
    n = int(total_sec * SR)
    if len(samples) < n: return samples + [0.0] * (n - len(samples))
    return samples[:n]

def _finalize(samples):
    peak = max((abs(s) for s in samples), default=0.0)
    if peak == 0.0: return samples
    target = 0.85
    factor = target / peak if peak > target else 1.0
    return [s * factor for s in samples]

# INTERFACE
def ui_menu_close_001():
    s = _sweep('triangle', 800.0, 400.0, 0.10, 0.28, 0.003); return _finalize(_pad(s, 0.12))
def ui_modal_open_001():
    a = _at(_tone('sine', 600.0, 0.08, 0.30, 0.002), 0.00, 0.15); b = _at(_tone('sine', 1200.0, 0.06, 0.15, 0.002), 0.05, 0.15); return _finalize(_mix(a, b))
def ui_slider_change_001():
    s = _tone('square', 1800.0, 0.02, 0.20, 0.001); return _finalize(_pad(s, 0.04))
def ui_tab_switch_001():
    s = _sweep('triangle', 950.0, 1100.0, 0.06, 0.22, 0.002); return _finalize(_pad(s, 0.08))
def ui_confirm_002():
    a = _at(_tone('square', 500.0, 0.08, 0.25, 0.002), 0.00, 0.20); b = _at(_tone('square', 750.0, 0.10, 0.25, 0.002), 0.08, 0.20); return _finalize(_mix(a, b))
def ui_back_002():
    s = _sweep('square', 600.0, 300.0, 0.08, 0.25, 0.002); return _finalize(_pad(s, 0.10))
def ui_hover_002():
    s = _tone('triangle', 1800.0, 0.03, 0.20, 0.001); return _finalize(_pad(s, 0.05))
def ui_toggle_002():
    a = _at(_tone('sine', 1200.0, 0.03, 0.28, 0.001), 0.00, 0.10); b = _at(_tone('sine', 800.0, 0.03, 0.28, 0.001), 0.05, 0.10); return _finalize(_mix(a, b))
def ui_drag_drop_001():
    s = _sweep('sine', 800.0, 400.0, 0.08, 0.25, 0.002); return _finalize(_pad(s, 0.10))
def ui_unlock_001():
    a = _at(_tone('square', 600.0, 0.06, 0.22, 0.002), 0.00, 0.20); b = _at(_tone('square', 900.0, 0.08, 0.22, 0.002), 0.08, 0.20); return _finalize(_mix(a, b))

# ALERTS
def alert_error_002():
    a = _at(_tone('sawtooth', 400.0, 0.15, 0.30, 0.004), 0.00, 0.40); b = _at(_tone('sawtooth', 300.0, 0.15, 0.30, 0.004), 0.15, 0.40); return _finalize(_mix(a, b))
def alert_success_002():
    notes = [(523.25, 0.0), (659.25, 0.1), (783.99, 0.2), (1046.5, 0.3)]; parts = [_at(_tone('triangle', f, 0.12, 0.28, 0.004), t, 0.50) for f, t in notes]; return _finalize(_mix(*parts))
def level_up_001():
    notes = [(523.25, 0.0), (659.25, 0.10), (783.99, 0.20), (1046.50, 0.30)]; parts = [_at(_tone('square', f, 0.15, 0.25, 0.005), t, 0.60) for f, t in notes]; return _finalize(_mix(*parts))
def quest_accepted_001():
    a = _at(_tone('triangle', 440.0, 0.10, 0.30, 0.004), 0.00, 0.40); b = _at(_tone('sine', 880.0, 0.15, 0.25, 0.005), 0.10, 0.40); return _finalize(_mix(a, b))

# GAMEPLAY
def item_drop_001():
    s = _sweep('sine', 600.0, 200.0, 0.15, 0.35, 0.002); return _finalize(_pad(s, 0.18))
def door_metal_open_001():
    nz = _at(_noise(0.50, 0.20, 0.010, seed=42), 0.00, 0.60); sw = _at(_sweep('sawtooth', 150.0, 80.0, 0.55, 0.25, 0.010), 0.00, 0.60); return _finalize(_mix(nz, sw))
def object_break_001():
    nz = _at(_noise(0.20, 0.40, 0.001, seed=88), 0.00, 0.25); sw = _at(_sweep('square', 200.0, 100.0, 0.10, 0.20, 0.002), 0.00, 0.25); return _finalize(_mix(nz, sw))
def lever_pull_001():
    nz = _at(_noise(0.10, 0.25, 0.002, seed=55), 0.00, 0.30); sw = _at(_sweep('triangle', 250.0, 150.0, 0.15, 0.30, 0.002), 0.10, 0.30); return _finalize(_mix(nz, sw))
def jump_002():
    s = _sweep('square', 200.0, 800.0, 0.20, 0.25, 0.005); return _finalize(_pad(s, 0.25))
def hit_impact_002():
    low = _at(_sweep('sawtooth', 100.0, 50.0, 0.25, 0.40, 0.002), 0.00, 0.30); nz = _at(_noise(0.15, 0.30, 0.001, seed=21), 0.00, 0.30); return _finalize(_mix(low, nz))
def explosion_small_002():
    nz = _at(_noise(0.60, 0.40, 0.002, seed=15), 0.00, 0.70); low = _at(_sweep('sawtooth', 120.0, 40.0, 0.60, 0.30, 0.005), 0.00, 0.70); return _finalize(_mix(nz, low))
def damage_player_002():
    sw = _at(_sweep('square', 300.0, 100.0, 0.20, 0.30, 0.003), 0.00, 0.25); nz = _at(_noise(0.08, 0.15, 0.001, seed=33), 0.00, 0.25); return _finalize(_mix(sw, nz))
def sword_swing_001():
    nz = _at(_noise(0.15, 0.35, 0.002, seed=11), 0.00, 0.20); sw = _at(_sweep('sawtooth', 400.0, 100.0, 0.15, 0.20, 0.002), 0.00, 0.20); return _finalize(_mix(nz, sw))
def footstep_gravel_001():
    nz = _at(_noise(0.10, 0.40, 0.001, seed=66), 0.00, 0.15); t = _at(_tone('sine', 120.0, 0.05, 0.30, 0.001), 0.00, 0.15); return _finalize(_mix(nz, t))
def weapon_reload_001():
    a = _at(_tone('square', 1500.0, 0.03, 0.20, 0.001), 0.00, 0.30); b = _at(_tone('square', 1200.0, 0.04, 0.20, 0.001), 0.10, 0.30); c = _at(_tone('square', 1800.0, 0.03, 0.20, 0.001), 0.22, 0.30); return _finalize(_mix(a, b, c))
def dodge_roll_001():
    nz = _at(_noise(0.20, 0.25, 0.002, seed=42), 0.00, 0.25); t = _at(_sweep('sine', 150.0, 50.0, 0.20, 0.35, 0.005), 0.00, 0.25); return _finalize(_mix(nz, t))

# SCI-FI
def sci_fi_system_boot_001():
    up = _at(_sweep('sawtooth', 100.0, 600.0, 0.50, 0.20, 0.010), 0.00, 0.80); t = _at(_tone('sine', 1200.0, 0.20, 0.25, 0.005), 0.55, 0.80); return _finalize(_mix(up, t))
def robot_servo_move_001():
    a = _at(_sweep('square', 800.0, 1200.0, 0.10, 0.20, 0.002), 0.00, 0.20); b = _at(_sweep('square', 1000.0, 800.0, 0.10, 0.20, 0.002), 0.10, 0.20); return _finalize(_mix(a, b))
def sci_fi_data_transfer_001():
    parts = []
    for i in range(6): parts.append(_at(_tone('sine', 1500.0 + (i*100), 0.04, 0.20, 0.001), i*0.05, 0.40))
    return _finalize(_mix(*parts))
def sci_fi_force_field_hit_001():
    sw = _at(_sweep('sawtooth', 400.0, 150.0, 0.30, 0.35, 0.002), 0.00, 0.35); nz = _at(_noise(0.10, 0.20, 0.002, seed=99), 0.00, 0.35); return _finalize(_mix(sw, nz))

# MAGIC / FANTASY
def magic_fire_cast_001():
    nz = _at(_noise(0.40, 0.30, 0.005, seed=66), 0.00, 0.50); sw = _at(_sweep('sawtooth', 300.0, 100.0, 0.40, 0.25, 0.005), 0.00, 0.50); return _finalize(_mix(nz, sw))
def magic_ice_cast_001():
    a = _at(_tone('sine', 1500.0, 0.20, 0.25, 0.002), 0.00, 0.45); b = _at(_tone('sine', 2000.0, 0.15, 0.20, 0.002), 0.10, 0.45); return _finalize(_mix(a, b))
def magic_heal_001():
    notes = [(440.0, 0.00), (554.37, 0.12), (659.25, 0.24), (880.0, 0.36)]; parts = [_at(_tone('sine', f, 0.20, 0.22, 0.010), t, 0.60) for f, t in notes]; return _finalize(_mix(*parts))
def magic_portal_open_001():
    up = _at(_sweep('triangle', 150.0, 600.0, 0.50, 0.30, 0.020), 0.00, 0.70); t = _at(_tone('sine', 1000.0, 0.20, 0.20, 0.005), 0.50, 0.70); return _finalize(_mix(up, t))
def magic_enchantment_001():
    notes = [(659.25, 0.00), (783.99, 0.15), (987.77, 0.30)]; parts = [_at(_tone('sine', f, 0.15, 0.25, 0.010), t, 0.60) for f, t in notes]; return _finalize(_mix(*parts))
def magic_dispel_001():
    sw = _at(_sweep('triangle', 1000.0, 300.0, 0.40, 0.25, 0.005), 0.00, 0.50); nz = _at(_noise(0.30, 0.15, 0.002, seed=12), 0.00, 0.50); return _finalize(_mix(sw, nz))
def summon_creature_001():
    nz = _at(_noise(0.60, 0.30, 0.020, seed=44), 0.00, 0.70); sw = _at(_sweep('sawtooth', 100.0, 250.0, 0.60, 0.20, 0.020), 0.00, 0.70); return _finalize(_mix(nz, sw))

# ENVIRONMENT
def environment_wind_gust_001():
    nz = _at(_noise(0.70, 0.35, 0.010, seed=12), 0.00, 0.80); return _finalize(nz)
def environment_thunder_001():
    nz = _at(_noise(1.00, 0.50, 0.010, seed=77), 0.00, 1.20); low = _at(_sweep('sine', 60.0, 30.0, 1.00, 0.40, 0.010), 0.00, 1.20); return _finalize(_mix(nz, low))
def environment_rain_start_001():
    parts = []
    for i in range(12): parts.append(_at(_noise(0.05, 0.10, 0.001, seed=100+i), i*0.04, 0.50))
    return _finalize(_mix(*parts))
def environment_cave_drip_001():
    a = _at(_sweep('sine', 1200.0, 800.0, 0.10, 0.30, 0.002), 0.00, 0.60); b = _at(_sweep('sine', 1200.0, 800.0, 0.10, 0.15, 0.002), 0.15, 0.60); c = _at(_sweep('sine', 1200.0, 800.0, 0.10, 0.07, 0.002), 0.30, 0.60); return _finalize(_mix(a, b, c))
def forest_ambience_001():
    nz = _at(_noise(1.40, 0.20, 0.010, seed=5), 0.00, 1.50); t1 = _at(_tone('sine', 3000.0, 0.10, 0.05, 0.010), 0.20, 1.50); t2 = _at(_tone('sine', 3200.0, 0.10, 0.05, 0.010), 0.80, 1.50); return _finalize(_mix(nz, t1, t2))
def ocean_wave_001():
    nz = _at(_noise(1.40, 0.35, 0.100, seed=8), 0.00, 1.50); low = _at(_sweep('sine', 200.0, 100.0, 1.20, 0.15, 0.100), 0.00, 1.50); return _finalize(_mix(nz, low))
def bird_chirp_001():
    a = _at(_sweep('sine', 3000.0, 4000.0, 0.08, 0.15, 0.002), 0.00, 0.30); b = _at(_sweep('sine', 3200.0, 4200.0, 0.08, 0.15, 0.002), 0.15, 0.30); return _finalize(_mix(a, b))
def fire_crackle_001():
    nz = _at(_noise(0.70, 0.25, 0.010, seed=3), 0.00, 0.80); c1 = _at(_noise(0.05, 0.30, 0.001, seed=19), 0.20, 0.80); c2 = _at(_noise(0.05, 0.30, 0.001, seed=23), 0.50, 0.80); return _finalize(_mix(nz, c1, c2))

OFFICIAL_PRESETS_EXTRA = {
    'ui-menu-close-001': ui_menu_close_001, 'ui-modal-open-001': ui_modal_open_001, 'ui-slider-change-001': ui_slider_change_001, 'ui-tab-switch-001': ui_tab_switch_001,
    'ui-confirm-002': ui_confirm_002, 'ui-back-002': ui_back_002, 'ui-hover-002': ui_hover_002, 'ui-toggle-002': ui_toggle_002,
    'ui-drag-drop-001': ui_drag_drop_001, 'ui-unlock-001': ui_unlock_001,
    'alert-error-002': alert_error_002, 'alert-success-002': alert_success_002,
    'level-up-001': level_up_001, 'quest-accepted-001': quest_accepted_001,
    'item-drop-001': item_drop_001, 'door-metal-open-001': door_metal_open_001, 'object-break-001': object_break_001, 'lever-pull-001': lever_pull_001,
    'jump-002': jump_002, 'hit-impact-002': hit_impact_002, 'explosion-small-002': explosion_small_002, 'damage-player-002': damage_player_002,
    'sword-swing-001': sword_swing_001, 'footstep-gravel-001': footstep_gravel_001, 'weapon-reload-001': weapon_reload_001, 'dodge-roll-001': dodge_roll_001,
    'sci-fi-system-boot-001': sci_fi_system_boot_001, 'robot-servo-move-001': robot_servo_move_001, 'sci-fi-data-transfer-001': sci_fi_data_transfer_001, 'sci-fi-force-field-hit-001': sci_fi_force_field_hit_001,
    'magic-fire-cast-001': magic_fire_cast_001, 'magic-ice-cast-001': magic_ice_cast_001, 'magic-heal-001': magic_heal_001, 'magic-portal-open-001': magic_portal_open_001,
    'magic-enchantment-001': magic_enchantment_001, 'magic-dispel-001': magic_dispel_001, 'summon-creature-001': summon_creature_001,
    'environment-wind-gust-001': environment_wind_gust_001, 'environment-thunder-001': environment_thunder_001, 'environment-rain-start-001': environment_rain_start_001, 'environment-cave-drip-001': environment_cave_drip_001,
    'forest-ambience-001': forest_ambience_001, 'ocean-wave-001': ocean_wave_001, 'bird-chirp-001': bird_chirp_001, 'fire-crackle-001': fire_crackle_001,
}