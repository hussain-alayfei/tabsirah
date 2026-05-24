import pickle
import cv2
import mediapipe as mp
import numpy as np
import os
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from constants import LABELS
from features import hand_to_features


def engineer_features(X):
    """Input (N, 42) -> output (N, 62). Adds 20 geometric features.
    Order: [42 raw] + [10 tip-tip dist] + [5 tip-wrist dist] + [5 bend angles]."""
    X = np.asarray(X, dtype=np.float32)
    N = X.shape[0]
    pts = X.reshape(N, 21, 2)
    WRIST = 0
    TIPS = [4, 8, 12, 16, 20]
    PIPS = [3, 7, 11, 15, 19]
    MCPS = [2, 6, 10, 14, 18]
    feats = []
    # 1) 10 pairwise tip-to-tip distances (i<j order)
    for i in range(5):
        for j in range(i + 1, 5):
            feats.append(np.linalg.norm(pts[:, TIPS[i]] - pts[:, TIPS[j]], axis=1))
    # 2) 5 tip-to-wrist distances
    for tip in TIPS:
        feats.append(np.linalg.norm(pts[:, tip] - pts[:, WRIST], axis=1))
    # 3) 5 bend angles at PIP (MCP->PIP->TIP)
    def bend_angle(a, b, c):
        v1, v2 = a - b, c - b
        n1 = np.linalg.norm(v1, axis=1) + 1e-8
        n2 = np.linalg.norm(v2, axis=1) + 1e-8
        cos = np.clip(np.einsum("ij,ij->i", v1, v2) / (n1 * n2), -1.0, 1.0)
        return np.arccos(cos)
    for mcp, pip, tip in zip(MCPS, PIPS, TIPS):
        feats.append(bend_angle(pts[:, mcp], pts[:, pip], pts[:, tip]))
    extras = np.stack(feats, axis=1).astype(np.float32)
    return np.concatenate([X, extras], axis=1)


class SignLanguageClassifier:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, 'models', 'model_lightgbm.p')
        task_path = os.path.join(base_dir, 'models', 'hand_landmarker.task')

        if not os.path.exists(model_path):
             raise FileNotFoundError(f"Model file not found: {model_path}")
        if not os.path.exists(task_path):
             raise FileNotFoundError(f"Task file not found: {task_path}")

        # --- Robust model loading ---
        obj = pickle.load(open(model_path, 'rb'))

        if isinstance(obj, dict) and 'model' in obj:
            model = obj['model']
            self.use_engineered = obj.get('use_engineered', False)
            self.feature_pipeline = obj.get('feature_pipeline', 'legacy')
        else:
            # Raw estimator (e.g. old model_arabic.p style)
            model = obj
            self.use_engineered = False
            self.feature_pipeline = 'legacy'

        # Normalize into a list of models
        if isinstance(model, (list, tuple)):
            self.models = list(model)
        else:
            self.models = [model]

        self.n_features_expected = self.models[0].n_features_in_

        print(f"[inference] Loaded {len(self.models)} model(s), "
              f"use_engineered={self.use_engineered}, "
              f"n_features_expected={self.n_features_expected}, "
              f"feature_pipeline={self.feature_pipeline}")

        # --- HandLandmarker (optional; fails on Render headless) ---
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
        except Exception as e:
            self.landmarks_only = True
            print(f"HandLandmarker unavailable (client-landmarks mode): {e}")
        
        self.labels_dict = LABELS

    def _features_from_points(self, x_, y_):
        data_aux = []
        min_x, min_y = min(x_), min(y_)
        for x, y in zip(x_, y_):
            data_aux.append(x - min_x)
            data_aux.append(y - min_y)
        return data_aux

    def _run_models(self, X):
        """Run ensemble on a ready feature matrix. Returns Arabic label or None."""
        if X.shape[1] != self.n_features_expected:
            print(f"[inference] feature mismatch: got {X.shape[1]}, "
                  f"model expects {self.n_features_expected}")
            return None
        proba = None
        for m in self.models:
            p = m.predict_proba(X)
            proba = p if proba is None else proba + p
        proba /= len(self.models)
        idx = int(np.argmax(proba, axis=1)[0])
        class_id = int(self.models[0].classes_[idx])
        return self.labels_dict.get(class_id)

    def _predict_label(self, data_aux):
        """data_aux: list/array of 42 raw features. Returns Arabic label str or None."""
        X = np.asarray(data_aux, dtype=np.float32).reshape(1, -1)   # (1, 42)
        if self.use_engineered:
            X = engineer_features(X)                                # (1, 62)
        return self._run_models(X)

    def classify_landmarks(self, landmarks, width=None, height=None):
        """Classify from client MediaPipe landmarks [{x,y,z}, ...] (21 points).
        
        For CHFN models, width and height of the source video frame are required.
        For legacy models, they are ignored.
        """
        if not landmarks or len(landmarks) < 21:
            return None
        try:
            if self.feature_pipeline == 'chfn_v1':
                if not width or not height:
                    print("[inference] CHFN model needs width/height from client")
                    return None
                xy = [(float(lm['x']), float(lm['y'])) for lm in landmarks]
                return self._run_models(hand_to_features(xy, width, height).reshape(1, -1))
            # Legacy path
            x_ = [float(lm['x']) for lm in landmarks]
            y_ = [float(lm['y']) for lm in landmarks]
            return self._predict_label(self._features_from_points(x_, y_))
        except Exception as e:
            print(f"[inference] predict error in classify_landmarks: {e}")
            return None

    def predict(self, frame_rgb):
        if not self.detector:
            return None, None

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        detection_result = self.detector.detect(mp_image)
        
        prediction_label = None
        
        if detection_result.hand_landmarks:
            hand = detection_result.hand_landmarks[0]
            try:
                if self.feature_pipeline == 'chfn_v1':
                    H, W = frame_rgb.shape[:2]
                    xy = [(lm.x, lm.y) for lm in hand]
                    prediction_label = self._run_models(
                        hand_to_features(xy, W, H).reshape(1, -1))
                else:
                    x_ = [lm.x for lm in hand]
                    y_ = [lm.y for lm in hand]
                    data_aux = self._features_from_points(x_, y_)
                    prediction_label = self._predict_label(data_aux)
            except Exception as e:
                print(f"[inference] predict error in predict: {e}")
                
        return prediction_label, detection_result
