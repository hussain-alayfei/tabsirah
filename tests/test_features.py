"""Tests for engineer_features — locks the 42→62 contract."""
import numpy as np
from inference_classifier import engineer_features


class TestEngineerFeatures:
    def test_output_shape(self):
        """42 raw features must produce 62 engineered features."""
        X = np.random.rand(1, 42).astype(np.float32)
        result = engineer_features(X)
        assert result.shape == (1, 62), f"Expected (1, 62), got {result.shape}"

    def test_batch_shape(self):
        """Batch of 5 samples should work."""
        X = np.random.rand(5, 42).astype(np.float32)
        result = engineer_features(X)
        assert result.shape == (5, 62)

    def test_raw_features_preserved(self):
        """First 42 columns must be the original input (passthrough)."""
        X = np.random.rand(1, 42).astype(np.float32)
        result = engineer_features(X)
        np.testing.assert_array_almost_equal(result[0, :42], X[0], decimal=5)

    def test_deterministic(self):
        """Same input must produce same output."""
        X = np.ones((1, 42), dtype=np.float32) * 0.5
        r1 = engineer_features(X.copy())
        r2 = engineer_features(X.copy())
        np.testing.assert_array_equal(r1, r2)

    def test_engineered_features_count(self):
        """20 extra features = 10 tip-tip + 5 tip-wrist + 5 bend angles."""
        X = np.random.rand(1, 42).astype(np.float32)
        result = engineer_features(X)
        extra_count = result.shape[1] - 42
        assert extra_count == 20, f"Expected 20 engineered features, got {extra_count}"

    def test_distances_non_negative(self):
        """All distance features (columns 42-56) should be non-negative."""
        X = np.random.rand(1, 42).astype(np.float32)
        result = engineer_features(X)
        # First 15 engineered features are distances (10 tip-tip + 5 tip-wrist)
        distances = result[0, 42:57]
        assert np.all(distances >= 0), "Distances must be non-negative"

    def test_angles_in_valid_range(self):
        """Bend angles (columns 57-61) should be in [0, pi]."""
        X = np.random.rand(1, 42).astype(np.float32)
        result = engineer_features(X)
        angles = result[0, 57:62]
        assert np.all(angles >= 0) and np.all(angles <= np.pi + 1e-6), \
            f"Angles must be in [0, pi], got {angles}"
