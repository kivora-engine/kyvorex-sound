"""Mission 8 - Infrastructures & Transports (25 sounds)."""
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

def infra_train_horn_001():
    a = _at(_tone('sawtooth', 200.0, 0.60, 0.30, 0.050), 0.00, 0.70)
    b = _at(_tone('sawtooth', 250.0, 0.60, 0.20, 0.050), 0.00, 0.70)
    return _finalize(_mix(a, b))
def infra_bridge_lift_001():
    sw = _at(_sweep('sine', 100.0, 200.0, 1.20, 0.30, 0.050), 0.00, 1.30)
    return _finalize(_mix(sw))
def infra_elevator_ding_001():
    a = _at(_tone('sine', 1200.0, 0.10, 0.30, 0.001), 0.00, 0.15)
    b = _at(_tone('sine', 1500.0, 0.15, 0.30, 0.001), 0.10, 0.15)
    return _finalize(_mix(a, b))
def infra_subway_arrival_001():
    nz = _at(_noise(0.80, 0.30, 0.050, seed=2700), 0.00, 0.90)
    return _finalize(_mix(nz))
def infra_traffic_light_beep_001():
    parts = []
    for i in range(3): parts.append(_at(_tone('square', 1000.0, 0.05, 0.25, 0.001), i*0.15, 0.35))
    return _finalize(_mix(*parts))
def infra_bus_door_open_001():
    sw = _at(_sweep('sine', 100.0, 200.0, 0.50, 0.25, 0.020), 0.00, 0.60)
    return _finalize(_mix(sw))
def infra_bus_door_close_001():
    sw = _at(_sweep('sine', 200.0, 100.0, 0.50, 0.25, 0.020), 0.00, 0.60)
    nz = _at(_noise(0.10, 0.20, 0.001, seed=2701), 0.40, 0.60)
    return _finalize(_mix(sw, nz))
def infra_train_track_clatter_001():
    parts = []
    for i in range(6): parts.append(_at(_noise(0.05, 0.30, 0.001, seed=2702+i), i*0.08, 0.50))
    return _finalize(_mix(*parts))
def infra_tunnel_wind_001():
    nz = _at(_noise(1.50, 0.20, 0.100, seed=2703), 0.00, 1.60)
    return _finalize(_mix(nz))
def infra_ferry_horn_001():
    a = _at(_tone('sawtooth', 150.0, 1.00, 0.40, 0.050), 0.00, 1.10)
    return _finalize(_mix(a))
def infra_drawbridge_motor_001():
    sw = _at(_sweep('sawtooth', 80.0, 120.0, 1.00, 0.25, 0.050), 0.00, 1.10)
    return _finalize(_mix(sw))
def infra_toll_booth_beep_001():
    a = _at(_tone('square', 800.0, 0.10, 0.25, 0.001), 0.00, 0.15)
    return _finalize(_mix(a))
def infra_parking_barrier_open_001():
    sw = _at(_sweep('sine', 300.0, 400.0, 0.40, 0.20, 0.010), 0.00, 0.50)
    return _finalize(_mix(sw))
def infra_parking_barrier_close_001():
    sw = _at(_sweep('sine', 400.0, 300.0, 0.40, 0.20, 0.010), 0.00, 0.50)
    return _finalize(_mix(sw))
def infra_crosswalk_signal_001():
    parts = []
    for i in range(4): parts.append(_at(_tone('square', 1200.0, 0.05, 0.20, 0.001), i*0.15, 0.50))
    return _finalize(_mix(*parts))
def infra_train_brake_squeal_001():
    nz = _at(_noise(1.20, 0.30, 0.050, seed=2704), 0.00, 1.30)
    high = _at(_tone('sine', 2000.0, 0.80, 0.10, 0.050), 0.00, 1.30)
    return _finalize(_mix(nz, high))
def infra_tram_bell_001():
    a = _at(_tone('triangle', 1000.0, 0.20, 0.25, 0.002), 0.00, 0.30)
    return _finalize(_mix(a))
def infra_cargo_crane_move_001():
    sw = _at(_sweep('sawtooth', 100.0, 150.0, 1.00, 0.25, 0.100), 0.00, 1.10)
    return _finalize(_mix(sw))
def infra_container_lock_001():
    nz = _at(_noise(0.10, 0.40, 0.001, seed=2705), 0.00, 0.15)
    a = _at(_tone('sine', 100.0, 0.10, 0.35, 0.001), 0.00, 0.15)
    return _finalize(_mix(nz, a))
def infra_gate_open_001():
    nz = _at(_noise(0.60, 0.30, 0.020, seed=2706), 0.00, 0.70)
    return _finalize(_mix(nz))
def infra_gate_close_001():
    nz = _at(_noise(0.60, 0.30, 0.020, seed=2707), 0.00, 0.70)
    a = _at(_tone('sine', 80.0, 0.15, 0.30, 0.005), 0.50, 0.70)
    return _finalize(_mix(nz, a))
def infra_highway_traffic_001():
    nz = _at(_noise(2.00, 0.20, 0.100, seed=2708), 0.00, 2.20)
    return _finalize(_mix(nz))
def infra_tunnel_ambience_001():
    nz = _at(_noise(2.00, 0.15, 0.200, seed=2709), 0.00, 2.20)
    return _finalize(_mix(nz))
def infra_runway_jet_001():
    sw = _at(_sweep('sawtooth', 100.0, 400.0, 1.50, 0.35, 0.100), 0.00, 1.60)
    return _finalize(_mix(sw))
def infra_airport_bell_001():
    parts = []
    for i in range(3): parts.append(_at(_tone('sine', 1500.0, 0.10, 0.20, 0.001), i*0.15, 0.50))
    return _finalize(_mix(*parts))

OFFICIAL_PRESETS_INFRA = {
    'infra-train-horn-001': infra_train_horn_001, 'infra-bridge-lift-001': infra_bridge_lift_001,
    'infra-elevator-ding-001': infra_elevator_ding_001, 'infra-subway-arrival-001': infra_subway_arrival_001,
    'infra-traffic-light-beep-001': infra_traffic_light_beep_001, 'infra-bus-door-open-001': infra_bus_door_open_001,
    'infra-bus-door-close-001': infra_bus_door_close_001, 'infra-train-track-clatter-001': infra_train_track_clatter_001,
    'infra-tunnel-wind-001': infra_tunnel_wind_001, 'infra-ferry-horn-001': infra_ferry_horn_001,
    'infra-drawbridge-motor-001': infra_drawbridge_motor_001, 'infra-toll-booth-beep-001': infra_toll_booth_beep_001,
    'infra-parking-barrier-open-001': infra_parking_barrier_open_001, 'infra-parking-barrier-close-001': infra_parking_barrier_close_001,
    'infra-crosswalk-signal-001': infra_crosswalk_signal_001, 'infra-train-brake-squeal-001': infra_train_brake_squeal_001,
    'infra-tram-bell-001': infra_tram_bell_001, 'infra-cargo-crane-move-001': infra_cargo_crane_move_001,
    'infra-container-lock-001': infra_container_lock_001, 'infra-gate-open-001': infra_gate_open_001,
    'infra-gate-close-001': infra_gate_close_001, 'infra-highway-traffic-001': infra_highway_traffic_001,
    'infra-tunnel-ambience-001': infra_tunnel_ambience_001, 'infra-runway-jet-001': infra_runway_jet_001,
    'infra-airport-bell-001': infra_airport_bell_001,
}