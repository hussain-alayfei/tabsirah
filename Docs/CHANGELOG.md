# 📜 Changelog

## [v2.0.0] - 2026-01-22
### 🚀 Major Architecture Overhaul
*   **Frontend**: Refactored monolithic code into modular components (`ai.js`, `game.js`, `ui.js`, `state.js`).
*   **Backend**: Switched AI model to **LightGBM** (`lighGBM_model.p`) for better accuracy.
*   **Cleanup**: Removed legacy `master` branch. Consolidated to `main` (Prod) and `develop` (Dev).
*   **Performance**: Suppressed verbose MediaPipe/TensorFlow C++ logs.
*   **Docs**: Renamed documentation to `DOCS.md` for simplicity.

## [v1.0.0] - Legacy
*   Initial Random Forest implementation.
*   Basic Flask app.
