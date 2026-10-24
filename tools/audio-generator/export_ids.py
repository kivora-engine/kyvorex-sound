import json
import os

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    catalog_path = os.path.join(base_dir, 'data', 'sounds.json')
    output_path = os.path.join(base_dir, 'data', 'all-sound-ids.txt')

    if not os.path.exists(catalog_path):
        print("Erreur : data/sounds.json introuvable.")
        return

    with open(catalog_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    sounds = data.get('sounds', [])
    ids = sorted([s['id'] for s in sounds if 'id' in s])

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("--- KYVOREX SOUNDS - LISTE DES IDS EXISTANTS ---\n")
        f.write(f"Total : {len(ids)} sons\n")
        f.write("--------------------------------------------------\n")
        for sid in ids:
            f.write(sid + "\n")

    print(f"✅ Fichier généré : data/all-sound-ids.txt")
    print(f"   Il contient {len(ids)} identifiants uniques.")

if __name__ == '__main__':
    main()