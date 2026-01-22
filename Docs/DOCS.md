# 📖 ArASL Project Documentation

## 🏗️ System Architecture
The application follows a **Modular Monolith** pattern:
*   **Backend**: Flask (Python) serving API endpoints.
*   **Frontend**: Vanilla JS with Modular Architecture (ES6 Modules).
*   **AI Engine**: LightGBM Classifier + MediaPipe Hand Tracking.

---

## 🖥️ Frontend Architecture (`web_app/static/js/`)
We moved away from monolithic scripts to specialized modules:

| Module | Purpose |
| :--- | :--- |
| **`main.js`** | Entry point. Initializes App, Router, and global event listeners. |
| **`ai.js`** | Handles Camera, MediaPipe, and Prediction polling. |
| **`game.js`** | Game Logic (Level progress, Answer checking, Scoring). |
| **`ui.js`** | DOM Manipulation (Rendering cards, overlays, animations). |
| **`state.js`** | Centralized State Store (Current Surah, Verse, Score). |
| **`api.js`** | Fetch Wrappers (`/predict`, `/get_surah`). |

---

## 🐍 Backend Architecture (`web_app/`)

### Core Files
*   **`app.py`**: Flask Server.
    *   **Config**: Suppresses TensorFlow/GLOG logs for clean output.
    *   **Endpoints**: `/predict` (POST), `/get_surahs` (GET).
*   **`inference_classifier.py`**:
    *   Loads `models/lighGBM_model.p`.
    *   Normalizes landmarks (Top-left origin).
    *   Returns Arabic Character predictions.
*   **`constants.py`**:
    *   `ARABIC_LABELS`: Mapping of Model Class IDs to Arabic Letters.

### AI Model
*   **Type**: LightGBM (Gradient Boosting Machine).
*   **Input**: 42 Hand Landmarks (x, y) from MediaPipe.
*   **Output**: 29 Classes (Arabic Alphabet).

---

## 🚀 Setup & Installation

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    # Key libs: flask, mediapipe, scikit-learn==1.6.1, lightgbm
    ```

2.  **Run Server**:
    ```bash
    cd web_app
    python app.py
    ```

3.  **Access**: `http://127.0.0.1:5000/`

---

## 🔢 API Reference

### `POST /predict`
*   **Input**: JSON `{ "landmarks": [[x, y], ...] }`
*   **Output**: JSON `{ "prediction": "أ" }`

### `GET /get_surah/<surah_name>`
*   **Output**: JSON `{ "verses": ["..."], "audio": "..." }`
