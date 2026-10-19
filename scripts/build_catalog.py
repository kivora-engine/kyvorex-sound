import json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_DIR = os.path.join(ROOT, 'data', 'catalog')
OUTPUT = os.path.join(ROOT, 'data', 'sounds.json')
SCHEMA_VERSION = 5

SOURCES = [
    ('interface.json', 'Interface'),
    ('alerts.json', 'Alerts'),
    ('gameplay.json', 'Gameplay'),
    ('sci-fi.json', 'Sci-Fi'),
    ('magic-fantasy.json', 'Magic / Fantasy'),
    ('environment.json', 'Environment'),
]

REQUIRED_FIELDS = ['id', 'name', 'category', 'description', 'duration', 'date', 'mp3', 'wav', 'license', 'status']

def fail(msg):
    print('CATALOG BUILD FAILED: ' + msg, file=sys.stderr)
    sys.exit(1)

def read_source(filename, expected_category):
    path = os.path.join(CATALOG_DIR, filename)
    if not os.path.isfile(path): fail('missing ' + filename)
    try:
        with open(path, 'r', encoding='utf-8') as f: data = json.load(f)
    except Exception as e: fail(filename + ' is not valid JSON: ' + str(e))

    if not isinstance(data, dict): fail(filename + ': top-level must be an object')
    if data.get('category') != expected_category:
        fail(filename + ': expected category "' + expected_category + '", found "' + str(data.get('category')) + '"')
    if not isinstance(data.get('sounds'), list): fail(filename + ': "sounds" must be an array')
    return data['sounds']

def check_sound(sound, filename, expected_category):
    if not isinstance(sound, dict): fail(filename + ': a sound entry is not an object')
    sid = sound.get('id')
    if not sid or not isinstance(sid, str): fail(filename + ': sound without valid id')
    if sound.get('category') != expected_category:
        fail(filename + ': sound "' + sid + '" has category "' + str(sound.get('category')) + '" but file is for "' + expected_category + '"')
    for field in REQUIRED_FIELDS:
        if sound.get(field) is None: fail(filename + ': sound "' + sid + '" missing field "' + field + '"')

def compact_string_arrays(text):
    pattern = re.compile(r'\[\s*((?:"[^"]*",?\s*)+)\]')
    def repl(m):
        items = re.findall(r'"[^"]*"', m.group(1))
        return '[' + ', '.join(items) + ']'
    return pattern.sub(repl, text)

def build():
    print('Building catalog from source files...')
    all_sounds = []
    seen = set()

    for filename, category in SOURCES:
        sounds = read_source(filename, category)
        for s in sounds:
            check_sound(s, filename, category)
            sid = s['id']
            if sid in seen: fail('duplicate id: ' + sid)
            seen.add(sid)
            all_sounds.append(s)
        print('  ' + filename + ': ' + str(len(sounds)) + ' sounds')

    max_date = ''
    for s in all_sounds:
        d = s.get('date') or ''
        if d > max_date: max_date = d

    output = {'version': SCHEMA_VERSION, 'updated': max_date, 'sounds': all_sounds}
    raw = json.dumps(output, indent=2, ensure_ascii=False)
    raw = compact_string_arrays(raw)

    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    with open(OUTPUT, 'w', encoding='utf-8') as f:
        f.write(raw)
        if not raw.endswith('\n'): f.write('\n')

    print('Catalog written: ' + str(len(all_sounds)) + ' sounds -> ' + os.path.relpath(OUTPUT, ROOT))

if __name__ == '__main__':
    build()