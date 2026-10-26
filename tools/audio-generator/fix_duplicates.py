import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
CATALOG_DIR = os.path.join(ROOT, 'data', 'catalog')

def load(name):
    with open(os.path.join(CATALOG_DIR, name), 'r', encoding='utf-8') as f:
        return json.load(f)

def save(name, data):
    with open(os.path.join(CATALOG_DIR, name), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write('\n')

def clean_file(filename):
    data = load(filename)
    sounds = data.get('sounds', [])
    unique_sounds = []
    seen_ids = set()
    
    for s in sounds:
        sid = s.get('id')
        if sid not in seen_ids:
            unique_sounds.append(s)
            seen_ids.add(sid)
    
    data['sounds'] = unique_sounds
    save(filename, data)
    print(f"✅ {filename} nettoyé : {len(sounds)} -> {len(unique_sounds)} sons")

def main():
    print("Nettoyage des doublons...")
    clean_file('sci-fi.json')
    clean_file('gameplay.json')

if __name__ == '__main__':
    main()