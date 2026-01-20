import os
import csv

def verify_mapping():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATASET_ROOT = os.path.join(BASE_DIR, 'dataset')
    DATA_DIR = os.path.join(DATASET_ROOT, 'Lettres_sign_ar', 'Lettres_sign_ar')
    MAPPING_FILE = os.path.join(DATASET_ROOT, 'class_mapping.csv')
    
    print(f"🕵️ Verifying mapping in: {DATA_DIR}")
    
    # 1. Check Directory Structure
    if not os.path.exists(DATA_DIR):
        print("❌ Data directory not found!")
        return

    # List subdirectories (Classes)
    subdirs = [d for d in os.listdir(DATA_DIR) if os.path.isdir(os.path.join(DATA_DIR, d))]
    subdirs.sort(key=lambda x: int(x) if x.isdigit() else 999)
    print(f"Found {len(subdirs)} class folders: {subdirs[:5]}...{subdirs[-5:]}")

    # 2. Read Mapping File
    if not os.path.exists(MAPPING_FILE):
        print(f"❌ Mapping file not found: {MAPPING_FILE}")
        return

    print("\n📜 Reading class_mapping.csv:")
    mapping = {}
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Adjust column names based on actual file content (heuristic)
            cid = row.get('Class_ID') or row.get('id') or list(row.values())[0]
            letter = row.get('Arabic_Letter') or row.get('letter') or list(row.values())[1]
            
            print(f"  ID: {cid} -> {letter}")
            mapping[int(cid)] = letter.strip()

    # 3. Generate Python Dict Code
    print("\n✅ Ground Truth Mapping (Copy this to inference_classifier.py):")
    print("labels_dict = {")
    sorted_keys = sorted(mapping.keys())
    for k in sorted_keys:
        print(f"    {k}: '{mapping[k]}',")
    print("}")

if __name__ == "__main__":
    verify_mapping()
