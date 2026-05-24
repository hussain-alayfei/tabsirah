"""
features.py — single source of truth for the Tabsirah feature pipeline.

This module is imported by BOTH:
  - the Kaggle training notebook (re-extraction + training), and
  - web_app/inference_classifier.py (serving)
so the two can never drift.

Canonical Hand-Frame Normalization (CHFN) makes the feature vector invariant to:
  - position in frame   (translation)
  - zoom / camera distance (scale)
  - left vs right hand  (reflection / handedness)
  - phone vs desktop screen (aspect ratio)

Rotation is intentionally NOT normalized away (some letters carry orientation);
handle small tilt with light augmentation at training time instead.
"""
import numpy as np

# ---- MediaPipe landmark indices (single source of truth) -------------------
N_LANDMARKS = 21
WRIST       = 0
INDEX_MCP   = 5
PINKY_MCP   = 17
MIDDLE_MCP  = 9
TIPS = [4, 8, 12, 16, 20]   # thumb, index, middle, ring, pinky tips
PIPS = [3, 7, 11, 15, 19]   # second joints
MCPS = [2, 6, 10, 14, 18]   # knuckles

N_RAW      = 42   # 21 landmarks * 2 coords
N_ENGINEER = 20   # 10 tip-tip + 5 tip-wrist + 5 angles
N_FEATURES = 62   # N_RAW + N_ENGINEER

_EPS = 1e-8


def normalize_hand(landmarks_xy, width, height):
    """MediaPipe-normalized (x,y) landmarks -> canonical hand frame, shape (21, 2).

    Parameters
    ----------
    landmarks_xy : iterable of 21 (x, y) pairs, each in [0, 1] (MediaPipe output)
    width, height : the pixel dimensions of the source image / video frame

    Returns
    -------
    np.ndarray of shape (21, 2): canonical coordinates.
    """
    pts = np.asarray(landmarks_xy, dtype=np.float64).reshape(N_LANDMARKS, 2).copy()

    # 1) ASPECT CORRECTION — undo MediaPipe's per-axis normalization so the
    #    hand has true geometry regardless of frame aspect ratio.
    pts[:, 0] *= float(width)
    pts[:, 1] *= float(height)

    # 2) HANDEDNESS CANONICALIZATION — mirror to a single chirality using a
    #    geometric test (independent of MediaPipe's Left/Right label and of any
    #    camera/selfie mirroring, so training and inference always agree).
    v1 = pts[INDEX_MCP] - pts[WRIST]
    v2 = pts[PINKY_MCP] - pts[WRIST]
    cross = v1[0] * v2[1] - v1[1] * v2[0]
    if cross < 0.0:
        pts[:, 0] = -pts[:, 0]

    # 3) TRANSLATION — move the wrist to the origin.
    pts = pts - pts[WRIST]

    # 4) SCALE — divide by a rigid reference length (wrist -> middle knuckle)
    #    so the hand is unit-size regardless of zoom / camera distance.
    ref = np.linalg.norm(pts[MIDDLE_MCP])
    pts = pts / (ref if ref > _EPS else _EPS)

    return pts


def _engineered(pts):
    """20 geometric features from canonical (21, 2) coords."""
    feats = []
    # 10 pairwise fingertip-to-fingertip distances
    for i in range(5):
        for j in range(i + 1, 5):
            feats.append(np.linalg.norm(pts[TIPS[i]] - pts[TIPS[j]]))
    # 5 fingertip-to-wrist distances
    for tip in TIPS:
        feats.append(np.linalg.norm(pts[tip] - pts[WRIST]))
    # 5 finger bend angles (MCP -> PIP -> TIP)
    def angle(a, b, c):
        u, v = a - b, c - b
        nu = np.linalg.norm(u) + _EPS
        nv = np.linalg.norm(v) + _EPS
        return np.arccos(np.clip(np.dot(u, v) / (nu * nv), -1.0, 1.0))
    for mcp, pip, tip in zip(MCPS, PIPS, TIPS):
        feats.append(angle(pts[mcp], pts[pip], pts[tip]))
    return np.asarray(feats, dtype=np.float64)


def feats_from_canonical(canon_42):
    """Engineer the 62-dim vector from already-canonical (CHFN) 42 coords.

    Used by training-time augmentation, which perturbs canonical coords and
    needs to re-derive features without re-running normalize_hand().
    """
    pts = np.asarray(canon_42, dtype=np.float64).reshape(N_LANDMARKS, 2)
    return np.concatenate([pts.flatten(), _engineered(pts)]).astype(np.float32)


def hand_to_features(landmarks_xy, width, height):
    """Full pipeline: raw MediaPipe landmarks -> 62-dim feature vector (float32).

    THE one function both training and inference must call.
    """
    return feats_from_canonical(normalize_hand(landmarks_xy, width, height).flatten())
