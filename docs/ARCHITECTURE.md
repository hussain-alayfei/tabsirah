# Architecture

Technical reference for the Tabsirah codebase. Updated to reflect the current LightGBM ensemble pipeline.

---

## System Overview

```
Browser                              Server (Flask)
────────                             ──────────────
Webcam
  → MediaPipe WASM HandLandmarker    ← runs in browser (green skeleton)
    (21 landmarks, GPU delegate)
  → Smoothed landmarks (EMA)
  → JPEG frame + 21 landmarks       → POST /predict
                                       → classify_landmarks(landmarks)
                                         → _features_from_points() → 42 raw
                                         → engineer_features()     → 62 total
                                         → LightGBM ensemble (3 models)
                                         → averaged predict_proba → Arabic letter
                                       ← JSON { prediction, landmarks }
```

**Key invariant:** On Render (headless Linux), server-side MediaPipe fails with `libGLESv2.so.2`. The app **must** classify using **client-sent landmarks** only. Server MediaPipe is optional — used only when available (local dev).

---

## Project Structure

```
tabsirah/
├── AGENTS.md                  # Machine-readable agent/maintainer guide
├── CHANGELOG.md               # Version history
├── LICENSE                    # MIT
├── Procfile                   # Render start command
├── README.md                  # Entry point for humans
├── requirements.txt           # Production Python deps
├── requirements-dev.txt       # Dev/training deps (pytest, kagglehub)
├── convert_model.py           # Shrink ensemble (5→3→1 models)
├── .github/
│   └── workflows/test.yml     # CI: pytest on push to dev / PR to main
├── docs/
│   ├── ARCHITECTURE.md        # ← you are here
│   ├── DEPLOYMENT.md          # Render deploy + production notes
│   ├── CONTRIBUTING.md        # Dev workflow + git conventions
│   └── GIT_WORKFLOW.md        # Branch strategy (dev → main)
├── models/
│   ├── hand_landmarker.task   # MediaPipe hand model (~7.4 MB)
│   └── model_lightgbm.p      # Production classifier (~63 MB)
├── dataset/
│   └── class_mapping.csv      # 30-class label mapping
├── src/                       # Training scripts (not deployed)
│   ├── 3_process_data.py      # Feature extraction from images
│   └── 4_train_model.py       # Random Forest training (legacy)
├── web_app/                   # Flask application (deployed)
│   ├── app.py                 # Routes: /, /predict, /get_surahs, etc.
│   ├── inference_classifier.py # LightGBM ensemble + engineer_features()
│   ├── constants.py           # LABELS dict — single source of truth
│   ├── surah_data.py          # Surah content (Al-Kawthar unlocked)
│   ├── static/signs/          # Sign reference images (30 files)
│   └── templates/index.html   # Full SPA frontend
└── tests/
    ├── conftest.py            # Shared fixtures
    ├── test_features.py       # engineer_features contract tests
    └── test_classifier.py     # Model loading + prediction tests
```

---

## Prediction Pipeline

### 1. Feature Extraction (`_features_from_points`)

Takes 21 (x, y) landmark pairs, normalizes by subtracting min values:

```python
# Input: x_[21], y_[21]  →  Output: data_aux[42]
min_x, min_y = min(x_), min(y_)
for x, y in zip(x_, y_):
    data_aux.append(x - min_x)
    data_aux.append(y - min_y)
```

### 2. Engineered Features (`engineer_features`)

Transforms 42 raw features → 62 features. **Order is a contract with the trained model — do not reorder.**

```
[42 raw coords] + [10 tip-tip distances] + [5 tip-wrist distances] + [5 PIP bend angles]
```

| Feature group | Count | Description |
|---|---|---|
| Raw landmarks | 42 | Normalized (x,y) for 21 points |
| Tip-tip distances | 10 | Pairwise Euclidean between 5 fingertips (i<j) |
| Tip-wrist distances | 5 | Euclidean from each fingertip to wrist |
| Bend angles | 5 | Angle at PIP joint (MCP→PIP→TIP) via arccos |

### 3. Ensemble Prediction (`_predict_label`)

```python
# Average predict_proba across all models in the ensemble
proba = sum(m.predict_proba(X) for m in self.models) / len(self.models)
idx = np.argmax(proba)
class_id = int(self.models[0].classes_[idx])
return LABELS.get(class_id)  # from constants.py
```

### Model Format

The pickle at `models/model_lightgbm.p` contains:

```python
{
    'model': [lgbm_1, lgbm_2, lgbm_3],  # list of LGBMClassifier
    'use_engineered': True,               # flag to apply engineer_features
    'best_params': {...},                  # Optuna hyperparameters
    'test_accuracy': 0.9774,              # evaluated accuracy
}
```

The loader auto-detects format: dict-with-list (new) vs dict-with-single-model (old) vs raw estimator.

---

## Label Mapping

Canonical source: `web_app/constants.py` → `LABELS` dict.

```
0:ا  1:ب  2:ت  3:ث  4:ج  5:ح  6:خ  7:د  8:ذ  9:ر
10:ز 11:س 12:ش 13:ص 14:ض 15:ط 16:ظ 17:ع 18:غ 19:ف
20:ق 21:ك 22:ل 23:م 24:ن 25:ه 26:و 27:ي 28:ة 29:لا
```

30 classes total. All other code imports from `constants.py` — never duplicate this mapping.

---

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Serves `index.html` SPA |
| GET | `/get_surahs` | Returns all surahs with metadata |
| GET | `/get_surah/<id>` | Returns surah content (403 if locked) |
| GET | `/sign_image/<char>` | Serves sign reference image for a letter |
| POST | `/predict` | Accepts `{image, landmarks?}`, returns `{prediction, landmarks}` |

### POST `/predict` Details

- Input: `{ "image": "data:image/jpeg;base64,...", "landmarks": [{x,y,z}, ...] }`
- If `landmarks` has ≥21 points → uses `classify_landmarks()` (fast, no server MediaPipe needed)
- Else if server MediaPipe available → uses `predict(frame_rgb)` (fallback)
- Output: `{ "prediction": "ب", "landmarks": [[{x,y}, ...]] }`

---

## Frontend Architecture

Single-page app in `web_app/templates/index.html` with these views:

| View | ID | Purpose |
|------|-----|---------|
| Landing | `landingView` | Mode selection (Reading / Reciting) |
| Surah Selection | `surahSelectionView` | Pick a surah |
| Video Choice | `videoChoiceView` | Watch tutorial or start training |
| Video Player | `videoPlayerView` | YouTube tutorial embed |
| Training | `appView` | Camera + prediction + cards |
| Summary | `summaryOverlay` | Session results |
| Analytics | `analyticsOverlay` | Detailed performance breakdown |

### Landmark Smoothing

EMA filter (α=0.5) applied to raw MediaPipe landmarks before drawing and prediction:

```javascript
smoothed[i].x = SMOOTHING * smoothed[i].x + (1 - SMOOTHING) * raw[i].x;
```

Resets to `null` when hand disappears to prevent snapping from stale positions.

---

## Training Pipeline (for retraining)

1. **Data**: `dataset/Lettres_sign_ar/` — ~6,000 images across 30 classes
2. **Process**: `src/3_process_data.py` — MediaPipe landmark extraction → `data_arabic.pickle`
3. **Train**: `src/4_train_model.py` — trains classifier, saves to `models/`
4. **Convert**: `convert_model.py` — shrinks ensemble (e.g. 5→3 models) for deployment

> **Note:** `src/4_train_model.py` still trains a Random Forest. The current production model was trained in a Kaggle notebook using LightGBM with Optuna hyperparameter tuning. To retrain with LightGBM, use the Kaggle notebook workflow.

---

## CI/CD Pipeline

GitHub Actions (`.github/workflows/test.yml`) runs the full test suite on:

| Trigger | When |
|---------|------|
| Push to `dev` | Every commit on the integration branch |
| PR to `main` | Before anything reaches production |

The pipeline:
1. Checks out the repo (including the 63 MB model file)
2. Sets up Python 3.11 (matching Render)
3. Installs `requirements.txt` + `requirements-dev.txt`
4. Runs `pytest tests/ -v`

If any test fails, the push/PR is marked as failed. This catches:
- Feature contract breaks (42 vs 62 features)
- Model format changes (pickle structure)
- Label mapping drift
- Prediction pipeline regressions
