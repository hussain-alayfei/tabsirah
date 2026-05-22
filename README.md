# 📖 Tabsirah (تطبيق تبصرة)

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.11-green)
![License](https://img.shields.io/badge/license-MIT-orange)

**Learn and Memorize the Quran with Arabic Sign Language**

An AI-powered web application that provides real-time feedback on Arabic sign language for Quranic recitation.

[Features](#-features) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Demo](#-demo)

</div>

---

## ✨ Features

### 🎯 Two Learning Modes

#### 📖 Practice Reading (تدرب على القراءة)
- **Visual Learning**: Reference images for each sign
- **Real-time Feedback**: Instant validation of hand signs
- **Verse-by-Verse Training**: Structured learning through Quranic surahs
- **Hand Skeleton Overlay**: Visual guide showing detected hand landmarks

#### 📝 Practice Reciting (تدرب على التسميع)
- **Memorization Testing**: No reference images - recite from memory
- **Intelligent Error Tracking**: Track mistakes per letter (max 10 attempts)
- **Correction Overlay**: Shows correct sign after repeated errors
- **Detailed Analytics**: Verse-by-verse accuracy breakdown
- **Practice Errors**: Re-train only on failed verses

### 🤖 AI-Powered Detection
- **MediaPipe Hand Tracking**: 21 landmark detection with GPU acceleration
- **LightGBM Ensemble**: 3-model ensemble with engineered geometric features (~97.6% accuracy)
- **EMA Smoothing**: Exponential moving average on landmarks for steady predictions
- **30 Arabic Letters**: Complete Arabic alphabet + special combinations

### 🎨 Modern UI/UX
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Beautiful Typography**: Cairo for UI, Noto Naskh Arabic for Quranic text
- **Smooth Animations**: Delightful user experience
- **RTL Support**: Native right-to-left Arabic layout

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Webcam
- Modern web browser

### Installation

```bash
git clone https://github.com/hussain-alayfei/tabsirah.git
cd tabsirah

python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt

cd web_app
python app.py
```

Open http://127.0.0.1:5000

---

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [AGENTS.md](AGENTS.md) | AI agent / maintainer guide — production pitfalls, deploy checklist |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design, prediction pipeline, API reference |
| [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) | Render deploy config, troubleshooting |
| [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) | Dev setup, git workflow, code guidelines |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Flask (Python) |
| **Frontend** | HTML5, Tailwind CSS, JavaScript |
| **AI/ML** | MediaPipe, LightGBM, Scikit-Learn, OpenCV |
| **Hand Detection** | MediaPipe Hand Landmarker (browser WASM) |
| **Classification** | LightGBM ensemble (`model_lightgbm.p`) |
| **Fonts** | Cairo (UI), Noto Naskh Arabic (Quranic Text) |

---

## 📊 Project Structure

```
tabsirah/
├── models/               # Trained AI models
│   ├── hand_landmarker.task   # MediaPipe model
│   └── model_lightgbm.p      # Production classifier (LightGBM ensemble)
├── src/                  # Training scripts (not deployed)
│   ├── 3_process_data.py
│   └── 4_train_model.py
├── web_app/              # Flask application
│   ├── app.py            # Flask server & routes
│   ├── inference_classifier.py  # LightGBM inference + feature engineering
│   ├── constants.py      # Label mapping (single source of truth)
│   ├── surah_data.py     # Quranic content
│   ├── static/signs/     # Sign reference images
│   └── templates/        # HTML templates
├── tests/                # Test suite
├── docs/                 # Technical documentation
├── requirements.txt      # Production dependencies
└── Procfile              # Render start command
```

---

## 🎥 Demo

**Live app**: https://tabsirah.onrender.com

### Training Interface
- Camera feed with smoothed hand skeleton overlay
- Reference sign cards (in Reading mode)
- Real-time prediction badge
- Progress tracking

### Recitation Mode
- Error counter per letter
- Verse progress bar
- Correction overlay after 10 attempts
- Detailed final results with analytics

---

## 🤝 Contributing

See [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md) for development setup, git workflow, and code guidelines.

---

## 📝 License

MIT License — see [LICENSE](LICENSE) for details.

---

## 🙏 Credits

- **Datasets**: Arabic Sign Language Dataset (Kaggle)
- **Libraries**: MediaPipe (Google), Scikit-Learn, Flask, LightGBM, Tailwind CSS
- **Fonts**: Cairo by Mohamed Gaber, Noto Naskh Arabic by Google

---

<div align="center">

**Made with ❤️ for the Arabic Sign Language Community**

*May this project bring benefit to learners of the Holy Quran. Ameen.*

</div>
