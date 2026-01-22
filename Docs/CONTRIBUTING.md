# 🤝 Contributing Guide

## 🌳 Git Strategy
*   **`main`**: 🛡️ **Production**. Stable code only. Do NOT push here directly.
*   **`develop`**: 🚧 **Work**. All active development happens here.

### Workflow
1.  Checkout `develop`: `git checkout develop`
2.  Create a feature branch (optional): `git checkout -b feat/new-thing`
3.  Commit changes.
4.  Merge back to `develop`.

## 🏗️ Project Structure
*   **`web_app/`**: Flask application & Frontend (`static/js`, `templates`).
*   **`models/`**: AI Models (`lighGBM_model.p`).
*   **`md_files/`**: Documentation.

## 📝 Code Style
*   **Python**: PEP8.
*   **JS**: Modular ES6. Keep logic in `ai.js`, `game.js`, `ui.js`.
