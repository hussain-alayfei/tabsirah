# Changelog

All notable changes to the Tabsirah project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-05-22

### Added
- **GitHub Actions CI**: Pytest runs automatically on every push to `dev` and PR to `main`
- **Test suite**: 17 tests covering model loading, prediction pipeline, and feature engineering
- **`web_app/constants.py`**: Single source of truth for LABELS dict (30 classes) and HAND_CONNECTIONS
- **`requirements-dev.txt`**: Dev-only dependencies (pytest, kagglehub)
- **`convert_model.py`**: Utility to shrink ensemble (5→3 models) without retraining

### Changed
- **Model upgrade**: LightGBM 3-model ensemble (62 features, ~97.7% accuracy) replaces single model
- **Inference pipeline**: `engineer_features()` adds 20 geometric features (tip distances, wrist distances, bend angles)
- **Ensemble prediction**: Averaged `predict_proba` across 3 models instead of single `predict()`
- **Codebase cleanup**: Removed 8 dead/duplicate files, consolidated 5 scattered docs into `docs/`
- **Encoding fix**: Converted 6 UTF-16LE Python files to UTF-8
- **Git workflow**: `dev` branch for integration, `main` for production (replaces old `develop`/`master`)

### Removed
- `copy_signs.py`, `verify_images.py` (dead utility scripts)
- `models/model_arabic.p` (18 MB legacy Random Forest — superseded by LightGBM)
- `web_app/gunicorn.conf.py` (unused; Procfile handles this)
- `src/1_download_data.py`, `src/2_verify_mapping.py`, `src/5_update_app.py`, `src/sync_images.py` (dead scripts)
- 5 redundant markdown files (COMPLETE_PROJECT_DOCUMENTATION.md, PRODUCTION_READY.md, etc.)
- Stale remote branches: `develop`, `master`

### Fixed
- **Silent null predictions**: Model loaded as list but code called `.predict()` on it — now iterates ensemble
- **Feature mismatch**: 42-feature extraction hitting 62-feature model — now engineers features when `use_engineered=True`
- **Error logging**: Feature mismatches and prediction errors now log explicitly instead of failing silently

## [2.0.1] - 2026-05-19

### Fixed
- **Render production predictions**: Added `lightgbm` to `requirements.txt`
- **Render runtime**: Switched service from Node to Python 3 with correct Gunicorn start command
- **Headless Linux**: Server MediaPipe no longer blocks startup; classify from **browser-sent landmarks** when `libGLESv2` unavailable
- **Auto-deploy**: Re-enabled on Render `main` branch

### Added
- **AGENTS.md**: Maintainer/agent guide (Git status, Render checklist, common failures)
- **Aptfile**: Optional Mesa GL libraries for server MediaPipe
- Client sends `landmarks` array with each `/predict` request

### Changed
- Production model documented as `model_lightgbm.p` (replaces Random Forest in inference)

## [2.0.0] - 2026-01-20

### Added
- **Practice Reciting Mode (التسميع)**: Complete memorization testing feature
  - Hidden reference images for memory-based learning
  - Intelligent error tracking (max 10 attempts per letter)
  - Correction overlay with skip/retry options
  - Verse-by-verse analytics dashboard
  - "Practice Errors" feature to retry only failed verses
  
- **Hand Skeleton Visualization**: Real-time green skeletal overlay with 21 landmarks
- **Advanced Analytics**: Detailed error rates, pass/fail determination, and progress tracking
- **Responsive Design**: Mobile-first approach with tablet and desktop optimization
- **Production Deployment**: Deployed to Render with Gunicorn

### Changed
- **UI/UX Redesign**: 
  - Enlarged camera feed (max-w-xl, aspect-[9/16])
  - Updated brand colors (Primary Blue #617ED2, Light Cyan #3CA1D3)
  - Improved typography (Cairo for UI, Amiri for Quranic text)
  - Better responsive navigation bar
  
- **Model Optimization**: Lowered detection confidence to 0.3 for better real-time performance

### Fixed
- **Arabic Character Normalization**: Fixed variants (أ, إ, آ → ا) for 100% compatibility
- **Camera & Model Issues**: Resolved unclear feed and `None` prediction errors
- **Unicode Encoding**: Fixed Windows console crashes with Arabic characters
- **Error Rate Calculation**: Corrected analytics logic for accurate metrics
- **404 Errors**: Fixed image path resolution with dynamic selector
- **Responsive Issues**: Fixed disappearing navigation and component sizing

### Security
- Added proper error handling for production
- Implemented CORS configuration
- Disabled debug mode for production

## [1.0.0] - 2025-12-01

### Added
- Initial release with basic sign language detection
- MediaPipe hand tracking with Random Forest classifier
- Practice Reading mode with reference images
- Surah management system (Al-Fatiha initially)
- Real-time prediction API
- Basic Flask web application
- Model training pipeline

---

## Version History Summary

- **v2.1.0** (Current): Codebase cleanup, LightGBM ensemble, CI pipeline, test suite
- **v2.0.0**: Production-ready with advanced features and full deployment
- **v1.0.0**: Initial MVP with basic sign language detection
