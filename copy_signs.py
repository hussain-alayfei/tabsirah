import os
import shutil
import csv
from pathlib import Path

# Define paths
csv_path = r"C:\Users\huhul\Desktop\ArASL_Project\dataset\class_mapping.csv"
dataset_path = r"C:\Users\huhul\Desktop\ArASL_Project\dataset\Lettres_sign_ar"
output_path = r"C:\Users\huhul\Desktop\ArASL_Project\web_app\static\signs"

# Create output directory if it doesn't exist
os.makedirs(output_path, exist_ok=True)

# Read the CSV mapping
class_to_letter = {}
with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        class_id = row['Class_ID']
        arabic_letter = row['Arabic_Letter']
        class_to_letter[class_id] = arabic_letter

print(f"Found {len(class_to_letter)} classes in CSV")
print("=" * 50)

# Process each class
for class_id, arabic_letter in class_to_letter.items():
    # Path to the class folder in dataset
    class_folder = os.path.join(dataset_path, class_id)
    
    if not os.path.exists(class_folder):
        print(f"⚠️  Class {class_id} ({arabic_letter}): Folder not found - {class_folder}")
        continue
    
    # Get all jpg files in the folder
    jpg_files = [f for f in os.listdir(class_folder) if f.lower().endswith('.jpg')]
    
    if not jpg_files:
        print(f"⚠️  Class {class_id} ({arabic_letter}): No JPG files found")
        continue
    
    # Sort files numerically (assuming names like 0.jpg, 1.jpg, ..., 500.jpg)
    # Extract the number from filename for proper sorting
    jpg_files_sorted = sorted(jpg_files, key=lambda x: int(os.path.splitext(x)[0]))
    
    # Get the last image
    last_image = jpg_files_sorted[-1]
    source_path = os.path.join(class_folder, last_image)
    
    # Create destination filename with Arabic letter
    dest_filename = f"{arabic_letter}.jpg"
    dest_path = os.path.join(output_path, dest_filename)
    
    # Copy the file (won't delete anything, just copies)
    shutil.copy2(source_path, dest_path)
    
    print(f"✓ Class {class_id} ({arabic_letter}): Copied {last_image} -> {dest_filename}")

print("=" * 50)
print(f"✓ Done! All images copied to: {output_path}")