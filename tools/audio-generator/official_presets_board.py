"""Mission 4 - Board Games (15 sounds)."""
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

def chess_piece_place_001():
    nz = _at(_noise(0.05, 0.30, 0.001, seed=301), 0.00, 0.10)
    a = _at(_tone('sine', 150.0, 0.08, 0.30, 0.002), 0.00, 0.10)
    return _finalize(_mix(nz, a))

def chess_clock_press_001():
    a = _at(_tone('square', 800.0, 0.03, 0.25, 0.001), 0.00, 0.05)
    b = _at(_tone('square', 600.0, 0.03, 0.25, 0.001), 0.04, 0.05)
    return _finalize(_mix(a, b))

def dice_single_roll_001():
    nz1 = _at(_noise(0.05, 0.30, 0.001, seed=302), 0.00, 0.40)
    nz2 = _at(_noise(0.05, 0.25, 0.001, seed=303), 0.15, 0.40)
    nz3 = _at(_noise(0.05, 0.20, 0.001, seed=304), 0.30, 0.40)
    return _finalize(_mix(nz1, nz2, nz3))

def dice_cup_shake_001():
    parts = []
    for i in range(10):
        nz = _at(_noise(0.03, 0.25, 0.001, seed=305+i), i*0.04, 0.45)
        parts.append(nz)
    return _finalize(_mix(*parts))

def playing_cards_shuffle_001():
    nz = _at(_noise(1.00, 0.30, 0.010, seed=306), 0.00, 1.10)
    return _finalize(_mix(nz))

def playing_card_deal_001():
    nz = _at(_noise(0.10, 0.25, 0.002, seed=307), 0.00, 0.15)
    return _finalize(_mix(nz))

def playing_card_flip_001():
    nz = _at(_noise(0.05, 0.30, 0.001, seed=308), 0.00, 0.08)
    return _finalize(_mix(nz))

def coin_flip_table_001():
    a = _at(_tone('sine', 1200.0, 0.10, 0.25, 0.002), 0.00, 0.30)
    nz = _at(_noise(0.05, 0.20, 0.001, seed=309), 0.20, 0.30)
    return _finalize(_mix(a, nz))

def domino_tile_place_001():
    nz = _at(_noise(0.03, 0.35, 0.001, seed=310), 0.00, 0.08)
    a = _at(_tone('square', 400.0, 0.03, 0.20, 0.001), 0.00, 0.08)
    return _finalize(_mix(nz, a))

def domino_chain_fall_001():
    parts = []
    for i in range(8):
        nz = _at(_noise(0.02, 0.25, 0.001, seed=311+i), i*0.06, 0.50)
        parts.append(nz)
    return _finalize(_mix(*parts))

def board_game_token_move_001():
    nz = _at(_noise(0.15, 0.15, 0.010, seed=312), 0.00, 0.20)
    return _finalize(_mix(nz))

def board_game_piece_stack_001():
    a = _at(_tone('sine', 300.0, 0.05, 0.25, 0.002), 0.00, 0.15)
    b = _at(_tone('sine', 350.0, 0.05, 0.25, 0.002), 0.08, 0.15)
    return _finalize(_mix(a, b))

def poker_chip_stack_001():
    nz = _at(_noise(0.04, 0.30, 0.001, seed=313), 0.00, 0.10)
    a = _at(_tone('square', 600.0, 0.03, 0.20, 0.001), 0.00, 0.10)
    return _finalize(_mix(nz, a))

def poker_chip_slide_001():
    nz = _at(_noise(0.20, 0.20, 0.005, seed=314), 0.00, 0.25)
    return _finalize(_mix(nz))

def game_timer_expire_001():
    a = _at(_tone('square', 200.0, 0.50, 0.35, 0.005), 0.00, 0.60)
    return _finalize(_mix(a))

OFFICIAL_PRESETS_BOARD = {
    'chess-piece-place-001': chess_piece_place_001,
    'chess-clock-press-001': chess_clock_press_001,
    'dice-single-roll-001': dice_single_roll_001,
    'dice-cup-shake-001': dice_cup_shake_001,
    'playing-cards-shuffle-001': playing_cards_shuffle_001,
    'playing-card-deal-001': playing_card_deal_001,
    'playing-card-flip-001': playing_card_flip_001,
    'coin-flip-table-001': coin_flip_table_001,
    'domino-tile-place-001': domino_tile_place_001,
    'domino-chain-fall-001': domino_chain_fall_001,
    'board-game-token-move-001': board_game_token_move_001,
    'board-game-piece-stack-001': board_game_piece_stack_001,
    'poker-chip-stack-001': poker_chip_stack_001,
    'poker-chip-slide-001': poker_chip_slide_001,
    'game-timer-expire-001': game_timer_expire_001,
}