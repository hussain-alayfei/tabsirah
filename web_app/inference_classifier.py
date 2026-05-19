import pickle
import cv2
import mediapipe as mp
import numpy as np
import os
import json
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# #region agent log
_DEBUG_LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'debug-e8a399.log')
def _dbg(location, message, data, hypothesis_id):
    try:
        with open(_DEBUG_LOG, 'a', encoding='utf-8') as f:
            f.write(json.dumps({'sessionId': 'e8a399', 'timestamp': int(time.time() * 1000), 'location': location, 'message': message, 'data': data, 'hypothesisId': hypothesis_id}) + '\n')
    except Exception:
        pass
# #endregion

class SignLanguageClassifier:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, 'models', 'model_lightgbm.p')
        task_path = os.path.join(base_dir, 'models', 'hand_landmarker.task')

        if not os.path.exists(model_path):
             raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(task_path):
             raise FileNotFoundError(f"Task file not found: {task_path}")

        self.model_dict = pickle.load(open(model_path, 'rb'))
        self.model = self.model_dict['model']
        self.detector = None
        self.landmarks_only = False

        try:
            base_options = python.BaseOptions(
                model_asset_path=task_path,
                delegate=python.BaseOptions.Delegate.CPU,
            )
            options = vision.HandLandmarkerOptions(
                base_options=base_options,
                num_hands=1,
                min_hand_detection_confidence=0.3)
            self.detector = vision.HandLandmarker.create_from_options(options)
            # #region agent log
            _dbg('inference_classifier.py:init', 'detector_ok', {}, 'H1')
            # #endregion
        except Exception as e:
            self.landmarks_only = True
            print(f"HandLandmarker unavailable (client-landmarks mode): {e}")
            # #region agent log
            _dbg('inference_classifier.py:init', 'detector_failed', {'error': str(e)}, 'H1')
            # #endregion
        
        self.labels_dict = {
            0: 'ا', 1: 'ب', 2: 'ت', 3: 'ث', 4: 'ج', 5: 'ح', 6: 'خ', 7: 'د', 8: 'ذ',
            9: 'ر', 10: 'ز', 11: 'س', 12: 'ش', 13: 'ص', 14: 'ض', 15: 'ط', 16: 'ظ',
            17: 'ع', 18: 'غ', 19: 'ف', 20: 'ق', 21: 'ك', 22: 'ل', 23: 'م', 24: 'ن',
            25: 'ه', 26: 'و', 27: 'ي', 28: 'ة', 29: 'لا',
        }

    def _features_from_points(self, x_, y_):
        data_aux = []
        min_x, min_y = min(x_), min(y_)
        for x, y in zip(x_, y_):
            data_aux.append(x - min_x)
            data_aux.append(y - min_y)
        return data_aux

    def classify_landmarks(self, landmarks):
        """Classify from client MediaPipe landmarks [{x,y,z}, ...] (21 points)."""
        if not landmarks or len(landmarks) < 21:
            # #region agent log
            _dbg('inference_classifier.py:classify_landmarks', 'too_few_points', {'n': len(landmarks) if landmarks else 0}, 'H2')
            # #endregion
            return None
        x_ = [float(lm['x']) for lm in landmarks]
        y_ = [float(lm['y']) for lm in landmarks]
        data_aux = self._features_from_points(x_, y_)
        try:
            prediction = self.model.predict([np.asarray(data_aux)])
            label_key = prediction[0]
            try:
                key_int = int(label_key)
                label = self.labels_dict.get(key_int, label_key)
            except (TypeError, ValueError):
                label = self.labels_dict.get(label_key, label_key)
            # #region agent log
            _dbg('inference_classifier.py:classify_landmarks', 'predict_ok', {'label': label, 'raw': str(label_key)}, 'H3')
            # #endregion
            return label
        except Exception as e:
            # #region agent log
            _dbg('inference_classifier.py:classify_landmarks', 'predict_failed', {'error': str(e)}, 'H3')
            # #endregion
            return None

    def predict(self, frame_rgb):
        if not self.detector:
            # #region agent log
            _dbg('inference_classifier.py:predict', 'no_detector', {}, 'H2')
            # #endregion
            return None, None

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        detection_result = self.detector.detect(mp_image)
        
        prediction_label = None
        
        if detection_result.hand_landmarks:
            hand_landmarks = detection_result.hand_landmarks[0]
            x_ = [landmark.x for landmark in hand_landmarks]
            y_ = [landmark.y for landmark in hand_landmarks]
            data_aux = self._features_from_points(x_, y_)

            try:
                prediction = self.model.predict([np.asarray(data_aux)])
                label_key = prediction[0]
                try:
                    key_int = int(label_key)
                    prediction_label = self.labels_dict.get(key_int, label_key)
                except (TypeError, ValueError):
                    prediction_label = self.labels_dict.get(label_key, label_key)
                # #region agent log
                _dbg('inference_classifier.py:predict', 'server_predict_ok', {'label': prediction_label}, 'H3')
                # #endregion
            except Exception as e:
                # #region agent log
                _dbg('inference_classifier.py:predict', 'server_predict_failed', {'error': str(e)}, 'H3')
                # #endregion
                pass
        else:
            # #region agent log
            _dbg('inference_classifier.py:predict', 'no_hand_in_frame', {}, 'H2')
            # #endregion
                
        return prediction_label, detection_result
