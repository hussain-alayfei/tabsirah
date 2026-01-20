
import os
import glob

# defined mapping from inference_classifier.py
labels_dict = {
    0: 'ا', 1: 'ب', 2: 'ت', 3: 'ث', 4: 'ج', 5: 'ح', 6: 'خ', 7: 'د', 8: 'ذ', 9: 'ر', 
    10: 'ز', 11: 'س', 12: 'ش', 13: 'ص', 14: 'ض', 15: 'ط', 16: 'ظ', 17: 'ع', 18: 'غ', 
    19: 'ف', 20: 'ق', 21: 'ك', 22: 'ل', 23: 'م', 24: 'ن', 25: 'ه', 26: 'و', 27: 'ي', 
    28: 'ة', 29: 'لا'
}

# Add normalizing variants that app.py might handle or that we want to ensure exist
# app.py logic: f"{char}*.jpg"

static_signs_dir = r"c:\Users\huhul\Desktop\New folder\ArASL_Project\web_app\static\signs"

print(f"Checking images in: {static_signs_dir}")

missing = []
found = []

for idx, char in labels_dict.items():
    # Construct pattern exactly like app.py
    pattern = os.path.join(static_signs_dir, f"{char}*.jpg")
    matches = glob.glob(pattern)
    
    if matches:
        found.append(f"✅ {char} (ID: {idx}) -> Found: {len(matches)} files (e.g. {os.path.basename(matches[0])})")
    else:
        missing.append(f"❌ {char} (ID: {idx}) -> NO IMAGE FOUND")

    # Also check specific Alef variants if useful
    if char == 'ا':
        for var in ['أ', 'إ', 'آ']:
            p = os.path.join(static_signs_dir, f"{var}*.jpg")
            m = glob.glob(p)
            if m:
                 found.append(f"   ℹ️ Variant {var} -> Found")
            else:
                 missing.append(f"   ⚠️ Variant {var} -> Missing")

print("\n--- RESULTS ---")
for f in found:
    print(f)

if missing:
    print("\n--- MISSING ---")
    for m in missing:
        print(m)
else:
    print("\n🎉 ALL IMAGES FOUND!")
