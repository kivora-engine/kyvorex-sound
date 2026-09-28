"""Update data/sounds.json `status` field based on which files exist.

Rules:
- WAV present AND MP3 present  -> status = "available"
- otherwise                    -> status = "coming-soon"

Only the `status` field is modified.
"""
import json
import os


def _load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def sync(json_path, wav_dir, mp3_dir):
    """Returns (changed, summary) where summary is a list of dicts."""
    data = _load(json_path)
    sounds = data.get('sounds') or []
    summary = []
    changed = 0

    for s in sounds:
        sid = s.get('id')
        if not sid:
            continue
        wav_exists = os.path.isfile(os.path.join(wav_dir, sid + '.wav'))
        mp3_exists = os.path.isfile(os.path.join(mp3_dir, sid + '.mp3'))
        new_status = 'available' if (wav_exists and mp3_exists) else 'coming-soon'
        old_status = s.get('status')
        if old_status != new_status:
            s['status'] = new_status
            changed += 1
        summary.append({
            'id': sid,
            'wav': wav_exists,
            'mp3': mp3_exists,
            'old': old_status,
            'new': new_status,
        })

    if changed:
        _save(json_path, data)
    return changed, summary