import pickle
import cv2
import mediapipe as mp
import numpy as np
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

class SignLanguageClassifier:
    def __init__(self):
        # Paths relative to web_app/ folder
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # ArASL_Project root
        model_path = os.path.join(base_dir, 'models', 'model_arabic.p')
        task_path = os.path.join(base_dir, 'models', 'hand_landmarker.task')

        if not os.path.exists(model_path):
             raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(task_path):
             raise FileNotFoundError(f"Task file not found: {task_path}")

        self.model_dict = pickle.load(open(model_path, 'rb'))
        self.model = self.model_dict['model']
        
        base_options = python.BaseOptions(model_asset_path=task_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            num_hands=1,
            min_hand_detection_confidence=0.3)
        self.detector = vision.HandLandmarker.create_from_options(options)
        
        # ARABIC LABELS MAP
        self.labels_dict = {
            0: 'ا', 
            1: 'ب', 
            2: 'ت', 
            3: 'ث', 
            4: 'ج', 
            5: 'ح', 
            6: 'خ', 
            7: 'د', 
            8: 'ذ', 
            9: 'ر', 
            10: 'ز', 
            11: 'س', 
            12: 'ش', 
            13: 'ص', 
            14: 'ض', 
            15: 'ط', 
            16: 'ظ', 
            17: 'ع', 
            18: 'غ', 
            19: 'ف', 
            20: 'ق', 
            21: 'ك', 
            22: 'ل', 
            23: 'م', 
            24: 'ن', 
            25: 'ه', 
            26: 'و', 
            27: 'ي', 
            28: 'ة', 
            29: 'لا', 
        }

    def predict(self, frame_rgb):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        detection_result = self.detector.detect(mp_image)
        
        prediction_label = None
        
        if detection_result.hand_landmarks:
            # Take first hand
            hand_landmarks = detection_result.hand_landmarks[0]
            
            data_aux = []
            x_ = []
            y_ = []

            for landmark in hand_landmarks:
                x_.append(landmark.x)
                y_.append(landmark.y)

            for landmark in hand_landmarks:
                data_aux.append(landmark.x - min(x_))
                data_aux.append(landmark.y - min(y_))

            try:
                prediction = self.model.predict([np.asarray(data_aux)])
                # Prediction is the Folder Name (e.g., '16')
                label_key = prediction[0]
                
                # Force int conversion for lookup
                try:
                    key_int = int(label_key)
                    prediction_label = self.labels_dict.get(key_int, label_key)
                except:
                    prediction_label = self.labels_dict.get(label_key, label_key)
                    
            except Exception as e:
                pass
                
        return prediction_label, detection_result
