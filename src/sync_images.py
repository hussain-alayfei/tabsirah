import pandas as pd
import os
import shutil

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATASET_DIR = os.path.join(BASE_DIR, 'dataset', 'Lettres_sign_ar', 'Lettres_sign_ar')
STATIC_DIR = os.path.join(BASE_DIR, 'web_app', 'static', 'signs')
MAPPING_FILE = os.path.join(BASE_DIR, 'dataset', 'class_mapping.csv')

def sync_images():
    print("Starting synchronization...")
    
    # Check if paths exist
    if not os.path.exists(MAPPING_FILE):
        print(f"Error: Mapping file not found at {MAPPING_FILE}")
        return
    
    if not os.path.exists(DATASET_DIR):
        print(f"Error: Dataset directory not found at {DATASET_DIR}")
        return

    # Load mapping
    df = pd.read_csv(MAPPING_FILE)
    
    success_count = 0
    
    for index, row in df.iterrows():
        class_id = str(row['Class_ID'])
        arabic_char = row['Arabic_Letter']
        
        # Path to class folder
        class_folder = os.path.join(DATASET_DIR, class_id)
        
        if not os.path.exists(class_folder):
            print(f"Warning: Folder for class {class_id} ({arabic_char}) missing.")
            continue
            
        # Get all jpg files
        files = [f for f in os.listdir(class_folder) if f.endswith('.jpg')]
        
        if not files:
            print(f"Warning: No images found for class {class_id} ({arabic_char}).")
            continue
            
        # Find max index
        # Filenames are like '0.jpg', '199.jpg'
        try:
            # Sort by integer value of filename
            files.sort(key=lambda x: int(os.path.splitext(x)[0]))
            last_image_name = files[-1]
            
            src_path = os.path.join(class_folder, last_image_name)
            
            # Destination path: static/signs/{Char}.jpg
            # Note: overwrites existing. If you want versioning, change dest name.
            # But user request implied "replacing" for the main view. 
            # However, since we added "Dynamic Image Selection" (last file), 
            # we should name it such that it is the "last" in static too?
            # User said "copy it to the static folder and remove the olds static image".
            # So simple overwrite is what they asked for logic-wise for the target.
            
            dst_path = os.path.join(STATIC_DIR, f"{arabic_char}.jpg")
            
            shutil.copy2(src_path, dst_path)
            # print(f"Synced {arabic_char}: {last_image_name} -> {dst_path}")
            success_count += 1
            
        except ValueError:
            print(f"Error parsing filenames in {class_folder}")
            
    print(f"Successfully synchronized {success_count} images.")

if __name__ == "__main__":
    sync_images()
