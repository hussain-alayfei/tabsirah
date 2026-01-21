# Changelog

All notable changes to the Tabsirah project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- **Comprehensive Documentation**: Complete technical documentation with 17 sections

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

- **v2.0.0** (Current): Production-ready with advanced features and full deployment
- **v1.0.0**: Initial MVP with basic sign language detection

---

For detailed technical changes, see [COMPLETE_PROJECT_DOCUMENTATION.md](COMPLETE_PROJECT_DOCUMENTATION.md)
