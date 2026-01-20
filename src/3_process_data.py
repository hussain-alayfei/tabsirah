import os
import pickle
import mediapipe as mp
import cv2
import numpy as np
import concurrent.futures
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# Global init for workers
detector = None

def init_worker(model_path):
    global detector
    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1,
        min_hand_detection_confidence=0.5)
    detector = vision.HandLandmarker.create_from_options(options)

def process_image(args):
    img_path, class_label = args
    global detector
    
    try:
        img = cv2.imread(img_path)
        if img is None: return None

        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        
        results = detector.detect(mp_image)
        
        if results.hand_landmarks:
            hand_landmarks = results.hand_landmarks[0]
            data_aux = []
            x_ = []
            y_ = []

            for landmark in hand_landmarks:
                x_.append(landmark.x)
                y_.append(landmark.y)

            for landmark in hand_landmarks:
                data_aux.append(landmark.x - min(x_))
                data_aux.append(landmark.y - min(y_))

            return (data_aux, class_label)
    except Exception as e:
        # print(f"Error processing {img_path}: {e}")
        pass
    return None

def process_data():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, 'dataset', 'Lettres_sign_ar', 'Lettres_sign_ar')
    MODEL_PATH = os.path.join(BASE_DIR, 'models', 'hand_landmarker.task')
    OUTPUT_DIR = os.path.join(BASE_DIR, 'data_processed')
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    print(f"🚀 Starting PARALLEL Data Processing from: {DATA_DIR}")
    
    # Collect all tasks
    tasks = []
    classes = os.listdir(DATA_DIR)
    for dir_ in classes:
        class_path = os.path.join(DATA_DIR, dir_)
        if not os.path.isdir(class_path): continue
        
        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            tasks.append((img_path, dir_))
            
    print(f"   Total Images to Process: {len(tasks)}")
    print(f"   Using {os.cpu_count()} CPU cores...")

    data = []
    labels = []
    
    # Run in parallel
    # Note: MediaPipe Hands is not purely thread safe, best to use ProcessPool
    # However, passing 'detector' is hard.
    # Better strategy: Init detector inside worker.
    
    chunk_size = max(1, len(tasks) // (os.cpu_count() * 4))
    
    with concurrent.futures.ProcessPoolExecutor(initializer=init_worker, initargs=(MODEL_PATH,)) as executor:
        results = list(executor.map(process_image, tasks, chunksize=chunk_size))
        
    # Collect results
    valid_count = 0
    for res in results:
        if res:
            d, l = res
            data.append(d)
            labels.append(l)
            valid_count += 1

    # Save
    print(f"\n✅ Processing Complete!")
    print(f"   Valid Samples Kept: {valid_count} ({(valid_count/len(tasks))*100:.1f}%)")
    
    with open(os.path.join(OUTPUT_DIR, 'data_arabic.pickle'), 'wb') as f:
        pickle.dump({'data': data, 'labels': labels}, f)
    print("   Saved to data_processed/data_arabic.pickle")

if __name__ == "__main__":
    # Fix for Windows multiprocessing
    import multiprocessing
    multiprocessing.freeze_support()
    process_data()
