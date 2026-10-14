"""Update the `status` field in the catalog source files.

Reads each data/catalog/*.json, checks for WAV + MP3 presence in the
corresponding audio directories, and updates the `status` field in
each source file. Then rebuilds data/sounds.json from the sources.

data/sounds.json itself is never edited directly — it is a generated
file.
"""
import json
import os
import subprocess
import sys


def _load(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def _save(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')


def sync(catalog_dir, wav_dir, mp3_dir):
    """Update status in each source file.

    Returns (changed_total, summary).
    """
    summary = []
    changed_total = 0

    if not os.path.isdir(catalog_dir):
        print('  catalog dir not found: ' + catalog_dir)
        return 0, []

    for name in sorted(os.listdir(catalog_dir)):
        if not name.endswith('.json'):
            continue
        path = os.path.join(catalog_dir, name)
        try:
            data = _load(path)
        except Exception as e:
            print('  skip ' + name + ': ' + str(e))
            continue

        sounds = data.get('sounds') or []
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
            _save(path, data)
            changed_total += changed

    return changed_total, summary


def rebuild_catalog(project_root):
    """Call scripts/build_catalog.py to regenerate data/sounds.json."""
    script = os.path.join(project_root, 'scripts', 'build_catalog.py')
    if not os.path.isfile(script):
        print('  WARNING: ' + script + ' not found, sounds.json not regenerated')
        return False
    result = subprocess.run([sys.executable, script])
    return result.returncode == 0