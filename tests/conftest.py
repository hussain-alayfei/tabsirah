"""Shared fixtures for tests."""
import sys
import os
import pytest

# Add web_app to path so imports work
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'web_app'))


@pytest.fixture
def sample_landmarks_42():
    """42 raw features: 21 (x, y) pairs, normalized."""
    import numpy as np
    rng = np.random.RandomState(42)
    return rng.rand(42).astype(np.float32).tolist()


@pytest.fixture
def model_path():
    """Path to the production model."""
    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, 'models', 'model_lightgbm.p')
