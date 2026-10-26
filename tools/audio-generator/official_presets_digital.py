"""Mission 9 - Digital & Electronic Systems (25 sounds)."""
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

def _finalize(samples):
    peak = max((abs(s) for s in samples), default=0.0)
    if peak == 0.0: return samples
    target = 0.85
    factor = target / peak if peak > target else 1.0
    return [s * factor for s in samples]

def data_stream_flow_001():
    parts = []
    for i in range(10): parts.append(_at(_tone('square', 1000.0 + i*50, 0.02, 0.15, 0.001), i*0.03, 0.35))
    return _finalize(_mix(*parts))
def server_sync_ping_001():
    a = _at(_tone('sine', 1200.0, 0.05, 0.25, 0.001), 0.00, 0.15)
    b = _at(_tone('sine', 1200.0, 0.05, 0.25, 0.001), 0.10, 0.15)
    return _finalize(_mix(a, b))
def firewall_deflect_001():
    nz = _at(_noise(0.10, 0.30, 0.001, seed=1200), 0.00, 0.15)
    a = _at(_tone('sawtooth', 400.0, 0.05, 0.20, 0.001), 0.00, 0.15)
    return _finalize(_mix(nz, a))
def encryption_unlock_001():
    parts = []
    for i in range(4): parts.append(_at(_tone('square', 800.0 + i*100, 0.04, 0.20, 0.001), i*0.06, 0.30))
    return _finalize(_mix(*parts))
def hologram_glitch_001():
    nz = _at(_noise(0.20, 0.40, 0.001, seed=1201), 0.00, 0.25)
    sw = _at(_sweep('sawtooth', 2000.0, 500.0, 0.20, 0.25, 0.001), 0.00, 0.25)
    return _finalize(_mix(nz, sw))
def quantum_computer_hum_001():
    a = _at(_tone('sine', 60.0, 1.00, 0.30, 0.050), 0.00, 1.10)
    b = _at(_tone('sine', 120.0, 1.00, 0.15, 0.050), 0.00, 1.10)
    return _finalize(_mix(a, b))
def system_overload_001():
    nz = _at(_noise(0.50, 0.50, 0.001, seed=1202), 0.00, 0.60)
    sw = _at(_sweep('square', 400.0, 1000.0, 0.50, 0.30, 0.010), 0.00, 0.60)
    return _finalize(_mix(nz, sw))
def neural_network_connect_001():
    parts = []
    for i in range(6): parts.append(_at(_tone('sine', 600.0 + i*200, 0.03, 0.15, 0.001), i*0.05, 0.30))
    return _finalize(_mix(*parts))
def digital_footprint_001():
    a = _at(_tone('triangle', 1500.0, 0.10, 0.20, 0.002), 0.00, 0.15)
    return _finalize(_mix(a))
def cyber_deck_boot_001():
    sw = _at(_sweep('sawtooth', 100.0, 400.0, 0.60, 0.30, 0.020), 0.00, 0.70)
    return _finalize(_mix(sw))
def data_corruption_001():
    nz = _at(_noise(0.30, 0.45, 0.001, seed=1203), 0.00, 0.40)
    return _finalize(_mix(nz))
def satellite_uplink_001():
    sw = _at(_sweep('sine', 200.0, 800.0, 0.80, 0.25, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))
def biometric_scan_pass_001():
    a = _at(_tone('sine', 1000.0, 0.10, 0.30, 0.002), 0.00, 0.15)
    b = _at(_tone('sine', 1500.0, 0.15, 0.30, 0.002), 0.10, 0.15)
    return _finalize(_mix(a, b))
def biometric_scan_fail_001():
    a = _at(_tone('sawtooth', 400.0, 0.20, 0.35, 0.002), 0.00, 0.25)
    return _finalize(_mix(a))
def drone_connect_001():
    a = _at(_tone('square', 300.0, 0.05, 0.20, 0.001), 0.00, 0.10)
    b = _at(_tone('square', 500.0, 0.05, 0.20, 0.001), 0.08, 0.10)
    return _finalize(_mix(a, b))
def smart_device_activate_001():
    a = _at(_tone('sine', 1200.0, 0.05, 0.25, 0.001), 0.00, 0.10)
    return _finalize(_mix(a))
def signal_jammer_001():
    nz = _at(_noise(0.60, 0.40, 0.050, seed=1204), 0.00, 0.70)
    return _finalize(_mix(nz))
def battery_recharge_001():
    sw = _at(_sweep('sine', 200.0, 600.0, 0.80, 0.20, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))
def power_grid_surge_001():
    sw = _at(_sweep('sawtooth', 100.0, 800.0, 0.40, 0.40, 0.010), 0.00, 0.50)
    return _finalize(_mix(sw))
def wireless_charge_001():
    a = _at(_tone('sine', 800.0, 0.30, 0.15, 0.010), 0.00, 0.40)
    return _finalize(_mix(a))
def cyber_attack_alert_001():
    parts = []
    for i in range(3): parts.append(_at(_tone('square', 1000.0, 0.05, 0.30, 0.001), i*0.10, 0.30))
    return _finalize(_mix(*parts))
def mainframe_access_001():
    sw = _at(_sweep('sawtooth', 400.0, 200.0, 0.30, 0.30, 0.005), 0.00, 0.40)
    return _finalize(_mix(sw))
def virtual_reality_enter_001():
    sw = _at(_sweep('sine', 400.0, 1200.0, 0.60, 0.25, 0.020), 0.00, 0.70)
    return _finalize(_mix(sw))
def virtual_reality_exit_001():
    sw = _at(_sweep('sine', 1200.0, 400.0, 0.60, 0.25, 0.020), 0.00, 0.70)
    return _finalize(_mix(sw))
def digital_map_render_001():
    parts = []
    for i in range(5): parts.append(_at(_tone('sine', 800.0, 0.02, 0.10, 0.001), i*0.05, 0.25))
    return _finalize(_mix(*parts))

OFFICIAL_PRESETS_DIGITAL = {
    'data-stream-flow-001': data_stream_flow_001, 'server-sync-ping-001': server_sync_ping_001,
    'firewall-deflect-001': firewall_deflect_001, 'encryption-unlock-001': encryption_unlock_001,
    'hologram-glitch-001': hologram_glitch_001, 'quantum-computer-hum-001': quantum_computer_hum_001,
    'system-overload-001': system_overload_001, 'neural-network-connect-001': neural_network_connect_001,
    'digital-footprint-001': digital_footprint_001, 'cyber-deck-boot-001': cyber_deck_boot_001,
    'data-corruption-001': data_corruption_001, 'satellite-uplink-001': satellite_uplink_001,
    'biometric-scan-pass-001': biometric_scan_pass_001, 'biometric-scan-fail-001': biometric_scan_fail_001,
    'drone-connect-001': drone_connect_001, 'smart-device-activate-001': smart_device_activate_001,
    'signal-jammer-001': signal_jammer_001, 'battery-recharge-001': battery_recharge_001,
    'power-grid-surge-001': power_grid_surge_001, 'wireless-charge-001': wireless_charge_001,
    'cyber-attack-alert-001': cyber_attack_alert_001, 'mainframe-access-001': mainframe_access_001,
    'virtual-reality-enter-001': virtual_reality_enter_001, 'virtual-reality-exit-001': virtual_reality_exit_001,
    'digital-map-render-001': digital_map_render_001,
}