import kagglehub
import shutil
import os

def download_data():
    print("⬇️ Downloading ArSL dataset (6k images)...")
    try:
        # Download latest version
        path = kagglehub.dataset_download("birafaneimane/arabic-sign-language-alphabet-arsl-dataset")
        print("✅ Download complete at cache:", path)

        # Move to project dataset folder
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        TARGET_DIR = os.path.join(BASE_DIR, 'dataset')
        
        # Ensure target is clean
        if os.path.exists(TARGET_DIR):
            print(f"🧹 Cleaning existing {TARGET_DIR}...")
            shutil.rmtree(TARGET_DIR)
            
        print(f"📂 Moving data to {TARGET_DIR}...")
        shutil.copytree(path, TARGET_DIR)
        print("✅ Data setup complete. Ready for verification.")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    download_data()
