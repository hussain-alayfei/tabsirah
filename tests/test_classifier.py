"""Tests for SignLanguageClassifier — model loading and prediction."""
import os
import pickle
import numpy as np
import pytest
from inference_classifier import SignLanguageClassifier, engineer_features
from constants import LABELS


class TestModelLoading:
    def test_model_file_exists(self, model_path):
        """Production model file must exist."""
        assert os.path.exists(model_path), f"Model not found: {model_path}"

    def test_pickle_format(self, model_path):
        """Pickle must be a dict with 'model' key."""
        with open(model_path, 'rb') as f:
            obj = pickle.load(f)
        assert isinstance(obj, dict), "Pickle must be a dict"
        assert 'model' in obj, "Pickle must have 'model' key"

    def test_ensemble_is_list(self, model_path):
        """model value must be a list of estimators."""
        with open(model_path, 'rb') as f:
            obj = pickle.load(f)
        model = obj['model']
        assert isinstance(model, list), "model must be a list"
        assert len(model) >= 1, "Must have at least 1 model"

    def test_use_engineered_flag(self, model_path):
        """Pickle must have use_engineered flag."""
        with open(model_path, 'rb') as f:
            obj = pickle.load(f)
        assert 'use_engineered' in obj, "Missing use_engineered flag"

    def test_feature_count_matches(self, model_path):
        """All models must expect the same feature count."""
        with open(model_path, 'rb') as f:
            obj = pickle.load(f)
        models = obj['model']
        expected = models[0].n_features_in_
        for i, m in enumerate(models):
            assert m.n_features_in_ == expected, \
                f"Model {i} expects {m.n_features_in_} features, model 0 expects {expected}"


class TestPrediction:
    @pytest.fixture(autouse=True)
    def _skip_if_no_mediapipe_task(self):
        """Skip if hand_landmarker.task is missing (CI environments)."""
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        task_path = os.path.join(base, 'models', 'hand_landmarker.task')
        if not os.path.exists(task_path):
            pytest.skip("hand_landmarker.task not available")

    def test_predict_label_returns_string(self, sample_landmarks_42):
        """_predict_label should return a string from LABELS."""
        clf = SignLanguageClassifier()
        result = clf._predict_label(sample_landmarks_42)
        assert result is not None, "Prediction should not be None for valid input"
        assert result in LABELS.values(), f"'{result}' not in LABELS"

    def test_classify_landmarks_returns_string(self):
        """classify_landmarks with valid client landmarks should return a label."""
        clf = SignLanguageClassifier()
        # Simulate 21 MediaPipe landmarks
        landmarks = [{'x': np.random.rand(), 'y': np.random.rand(), 'z': 0.0}
                     for _ in range(21)]
        result = clf.classify_landmarks(landmarks)
        assert result is None or result in LABELS.values()

    def test_feature_mismatch_returns_none(self):
        """Wrong-sized input should return None when features don't match model."""
        clf = SignLanguageClassifier()
        if clf.n_features_expected == 42:
            pytest.skip("Model expects 42 features — no mismatch possible")
        # Temporarily disable engineering so 42 raw features hit a model expecting 62
        original = clf.use_engineered
        clf.use_engineered = False
        try:
            result = clf._predict_label(np.random.rand(42).tolist())
        except Exception:
            result = None  # exception on mismatch is also acceptable
        finally:
            clf.use_engineered = original  # restore
        assert result is None, "Feature mismatch should return None or raise"

    def test_classify_landmarks_rejects_too_few(self):
        """Less than 21 landmarks should return None."""
        clf = SignLanguageClassifier()
        result = clf.classify_landmarks([{'x': 0, 'y': 0, 'z': 0}] * 10)
        assert result is None

    def test_labels_count(self):
        """Classifier should have exactly 30 labels."""
        clf = SignLanguageClassifier()
        assert len(clf.labels_dict) == 30
