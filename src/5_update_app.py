import os
import shutil
import csv
import re

def update_app():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATASET_ROOT = os.path.join(BASE_DIR, 'dataset')
    DATA_DIR = os.path.join(DATASET_ROOT, 'Lettres_sign_ar', 'Lettres_sign_ar')
    MAPPING_FILE = os.path.join(DATASET_ROOT, 'class_mapping.csv')
    APP_DIR = os.path.join(BASE_DIR, 'web_app')
    SIGNS_DIR = os.path.join(APP_DIR, 'static', 'signs')
    INFERENCE_FILE = os.path.join(APP_DIR, 'inference_classifier.py')

    print("🚀 Updating App Configuration...")

    # 1. Read Mapping
    mapping = {}
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cid = row.get('Class_ID') or row.get('id') or list(row.values())[0]
            letter = row.get('Arabic_Letter') or row.get('letter') or list(row.values())[1]
            mapping[int(cid)] = letter.strip()
    
    print(f"   Loaded {len(mapping)} classes from CSV.")

    # 2. Update reference images (static/signs)
    if os.path.exists(SIGNS_DIR):
        print(f"   Cleaning {SIGNS_DIR}...")
        shutil.rmtree(SIGNS_DIR)
    os.makedirs(SIGNS_DIR)

    print("   Populating reference images...")
    for cid, letter in mapping.items():
        src_folder = os.path.join(DATA_DIR, str(cid))
        if os.path.exists(src_folder):
            images = [f for f in os.listdir(src_folder) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            if images:
                # Copy first image
                src_img = os.path.join(src_folder, images[0])
                dst_img = os.path.join(SIGNS_DIR, f"{letter}.jpg")
                shutil.copy(src_img, dst_img)
                # print(f"    Copied {letter}.jpg")
    
    # 2b. Generate Variants (Fuzzy Match Support)
    # Copy plain 'ا' to 'أ', 'إ', 'آ' if they don't exist, or vice versa
    # The new dataset has simple labels. If 'ا' exists, creating variants helpful for UI display/logic is good.
    # Actually, the logic in index.html handles the matching. We just need the images for display.
    # If the dataset provides 'ا', we have 'ا.jpg'.
    # If game asks for 'أ', index.html handles logic, but image load might fail?
    # No, index.html fuzzy matching is for LOGIC.
    # If the user Types "أحمد", the game expects 'أ'. We need 'أ.jpg'.
    # If dataset has 'ا', we should copy 'ا.jpg' to 'أ.jpg' so it shows up.
    
    variants = {
        'ا': ['أ', 'إ', 'آ'],
        'ه': ['ة'],
        'ي': ['ى']
    }
    
    for base, others in variants.items():
        base_path = os.path.join(SIGNS_DIR, f"{base}.jpg")
        if os.path.exists(base_path):
            for var in others:
                var_path = os.path.join(SIGNS_DIR, f"{var}.jpg")
                if not os.path.exists(var_path):
                    shutil.copy(base_path, var_path)
                    print(f"    Created variant {var}.jpg from {base}")

    # 3. Update inference_classifier.py
    print(f"   Updating {INFERENCE_FILE}...")
    
    with open(INFERENCE_FILE, 'r', encoding='utf-8') as f:
        content = f.read()

    # Generate new dict string
    new_dict_str = "self.labels_dict = {\n"
    for k in sorted(mapping.keys()):
        new_dict_str += f"            {k}: '{mapping[k]}', \n"
    new_dict_str += "        }"

    # Regex replace
    # Matches: self.labels_dict = { ... } (multiline)
    pattern = re.compile(r"self\.labels_dict\s*=\s*\{[^}]*\}", re.DOTALL)
    
    if pattern.search(content):
        new_content = pattern.sub(new_dict_str, content)
        
        # Also update model name if needed
        new_content = new_content.replace("model_arabic.p", "model_arabic.p")
        
        with open(INFERENCE_FILE, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("   ✅ File updated successfully.")
    else:
        print("   ❌ Could not find labels_dict in file.")

if __name__ == "__main__":
    update_app()
