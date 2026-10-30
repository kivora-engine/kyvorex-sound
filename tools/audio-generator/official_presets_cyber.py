"""Mission 9 - Cybersecurity & Digital Systems (25 sounds)."""
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

def cyber_firewall_block_001():
    nz = _at(_noise(0.20, 0.40, 0.001, seed=2800), 0.00, 0.25)
    a = _at(_tone('square', 200.0, 0.15, 0.30, 0.001), 0.00, 0.25)
    return _finalize(_mix(nz, a))
def cyber_access_granted_001():
    a = _at(_tone('sine', 1000.0, 0.05, 0.25, 0.001), 0.00, 0.15)
    b = _at(_tone('sine', 1500.0, 0.10, 0.25, 0.001), 0.08, 0.15)
    return _finalize(_mix(a, b))
def cyber_access_denied_001():
    a = _at(_tone('square', 400.0, 0.10, 0.30, 0.002), 0.00, 0.20)
    return _finalize(_mix(a))
def cyber_password_accepted_001():
    a = _at(_tone('triangle', 1200.0, 0.05, 0.20, 0.001), 0.00, 0.10)
    return _finalize(_mix(a))
def cyber_password_rejected_001():
    a = _at(_tone('sawtooth', 300.0, 0.15, 0.25, 0.002), 0.00, 0.20)
    return _finalize(_mix(a))
def cyber_data_encrypt_001():
    parts = []
    for i in range(5): parts.append(_at(_tone('sine', 600.0 + i*100, 0.03, 0.15, 0.001), i*0.05, 0.30))
    return _finalize(_mix(*parts))
def cyber_data_decrypt_001():
    parts = []
    for i in range(5): parts.append(_at(_tone('sine', 1000.0 - i*100, 0.03, 0.15, 0.001), i*0.05, 0.30))
    return _finalize(_mix(*parts))
def cyber_mainframe_connect_001():
    sw = _at(_sweep('sine', 100.0, 400.0, 0.60, 0.25, 0.050), 0.00, 0.70)
    return _finalize(_mix(sw))
def cyber_server_hum_001():
    a = _at(_tone('sine', 60.0, 1.50, 0.20, 0.100), 0.00, 1.60)
    return _finalize(_mix(a))
def cyber_ddos_attack_001():
    nz = _at(_noise(1.00, 0.40, 0.020, seed=2801), 0.00, 1.10)
    return _finalize(_mix(nz))
def cyber_brute_force_001():
    parts = []
    for i in range(8): parts.append(_at(_tone('square', 800.0, 0.02, 0.15, 0.001), i*0.04, 0.35))
    return _finalize(_mix(*parts))
def cyber_vpn_connect_001():
    sw = _at(_sweep('sine', 200.0, 800.0, 0.40, 0.20, 0.020), 0.00, 0.50)
    return _finalize(_mix(sw))
def cyber_alert_intrusion_001():
    parts = []
    for i in range(2): parts.append(_at(_tone('square', 1200.0, 0.10, 0.30, 0.002), i*0.20, 0.40))
    return _finalize(_mix(*parts))
def cyber_trace_route_001():
    sw = _at(_sweep('sine', 800.0, 400.0, 0.60, 0.20, 0.050), 0.00, 0.70)
    return _finalize(_mix(sw))
def cyber_system_lockdown_001():
    sw = _at(_sweep('sawtooth', 400.0, 50.0, 1.00, 0.35, 0.050), 0.00, 1.10)
    return _finalize(_mix(sw))
def cyber_secure_channel_001():
    a = _at(_tone('sine', 1500.0, 0.05, 0.20, 0.001), 0.00, 0.10)
    b = _at(_tone('sine', 1800.0, 0.05, 0.20, 0.001), 0.10, 0.10)
    return _finalize(_mix(a, b))
def cyber_digital_sig_001():
    parts = []
    for i in range(4): parts.append(_at(_tone('triangle', 1000.0 + i*100, 0.03, 0.20, 0.001), i*0.05, 0.25))
    return _finalize(_mix(*parts))
def cyber_quantum_key_001():
    sw = _at(_sweep('sine', 2000.0, 500.0, 0.80, 0.20, 0.050), 0.00, 0.90)
    return _finalize(_mix(sw))
def cyber_proxy_switch_001():
    a = _at(_tone('square', 600.0, 0.05, 0.25, 0.001), 0.00, 0.10)
    return _finalize(_mix(a))
def cyber_node_scan_001():
    parts = []
    for i in range(6): parts.append(_at(_tone('sine', 400.0 + i*50, 0.02, 0.15, 0.001), i*0.08, 0.50))
    return _finalize(_mix(*parts))
def cyber_honeypot_trigger_001():
    nz = _at(_noise(0.40, 0.30, 0.005, seed=2802), 0.00, 0.50)
    return _finalize(_mix(nz))
def cyber_zero_day_patch_001():
    sw = _at(_sweep('sine', 300.0, 600.0, 0.30, 0.20, 0.010), 0.00, 0.40)
    return _finalize(_mix(sw))
def cyber_backdoor_open_001():
    sw = _at(_sweep('sawtooth', 100.0, 200.0, 0.50, 0.25, 0.020), 0.00, 0.60)
    return _finalize(_mix(sw))
def cyber_network_ping_001():
    a = _at(_tone('sine', 1000.0, 0.02, 0.20, 0.001), 0.00, 0.05)
    return _finalize(_mix(a))
def cyber_system_reboot_001():
    sw = _at(_sweep('square', 200.0, 800.0, 0.60, 0.30, 0.020), 0.00, 0.70)
    return _finalize(_mix(sw))

OFFICIAL_PRESETS_CYBER = {
    'cyber-firewall-block-001': cyber_firewall_block_001, 'cyber-access-granted-001': cyber_access_granted_001,
    'cyber-access-denied-001': cyber_access_denied_001, 'cyber-password-accepted-001': cyber_password_accepted_001,
    'cyber-password-rejected-001': cyber_password_rejected_001, 'cyber-data-encrypt-001': cyber_data_encrypt_001,
    'cyber-data-decrypt-001': cyber_data_decrypt_001, 'cyber-mainframe-connect-001': cyber_mainframe_connect_001,
    'cyber-server-hum-001': cyber_server_hum_001, 'cyber-ddos-attack-001': cyber_ddos_attack_001,
    'cyber-brute-force-001': cyber_brute_force_001, 'cyber-vpn-connect-001': cyber_vpn_connect_001,
    'cyber-alert-intrusion-001': cyber_alert_intrusion_001, 'cyber-trace-route-001': cyber_trace_route_001,
    'cyber-system-lockdown-001': cyber_system_lockdown_001, 'cyber-secure-channel-001': cyber_secure_channel_001,
    'cyber-digital-sig-001': cyber_digital_sig_001, 'cyber-quantum-key-001': cyber_quantum_key_001,
    'cyber-proxy-switch-001': cyber_proxy_switch_001, 'cyber-node-scan-001': cyber_node_scan_001,
    'cyber-honeypot-trigger-001': cyber_honeypot_trigger_001, 'cyber-zero-day-patch-001': cyber_zero_day_patch_001,
    'cyber-backdoor-open-001': cyber_backdoor_open_001, 'cyber-network-ping-001': cyber_network_ping_001,
    'cyber-system-reboot-001': cyber_system_reboot_001,
}