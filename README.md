# 📖 Tabsirah (تطبيق تبصرة)

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-blue)
![Python](https://img.shields.io/badge/python-3.10+-green)
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
- **MediaPipe Hand Tracking**: 21 landmark detection with 95%+ accuracy
- **Random Forest Classifier**: Fast, accurate sign classification
- **Real-time Processing**: <50ms prediction latency
- **30 Arabic Letters**: Complete Arabic alphabet + special combinations

### 🎨 Modern UI/UX
- **Responsive Design**: Works on mobile, tablet, and desktop
- **Beautiful Typography**: Amiri font for Quranic text, Cairo for UI
- **Smooth Animations**: Delightful user experience
- **RTL Support**: Native right-to-left Arabic layout
- **Brand Colors**: Professional color palette (Primary Blue, Light Cyan, Dark Navy)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Webcam
- Modern web browser

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/tabsirah.git
cd tabsirah

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
cd web_app
python app.py
```

### Access the App
Open your browser and navigate to:
```
http://127.0.0.1:5000
```

---

## 📚 Documentation

For complete technical documentation, see:

**[📖 COMPLETE_PROJECT_DOCUMENTATION.md](COMPLETE_PROJECT_DOCUMENTATION.md)**

This comprehensive guide covers:
- 🏗️ **Architecture**: System design and data flow
- 💻 **Technology Stack**: All frameworks and libraries
- 🧠 **AI Model**: Training pipeline and data processing
- 🎨 **Design System**: Colors, typography, components
- 🔧 **Implementation**: Key features with code examples
- 🐛 **Bug Fixes**: All improvements and corrections
- 🚀 **Deployment**: Production deployment guides
- 🔍 **Troubleshooting**: Common issues and solutions

---

## 🎥 Demo

### Home Screen
Beautiful landing page with two learning modes:
- 📖 Practice Reading (Visual Learning)
- 📝 Practice Reciting (Memorization Test)

### Training Interface
- Camera feed with hand skeleton overlay
- Reference sign cards (in Reading mode)
- Real-time prediction badge
- Progress tracking

### Recitation Mode
- Error counter per letter
- Verse progress bar
- Correction overlay after 10 attempts
- Detailed final results with analytics

---

## 🛠️ Technology Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Flask (Python) |
| **Frontend** | HTML5, Tailwind CSS, JavaScript |
| **AI/ML** | MediaPipe, Scikit-Learn, OpenCV |
| **Hand Detection** | MediaPipe Hand Landmarker |
| **Classification** | Random Forest (200 estimators) |
| **Fonts** | Cairo (UI), Amiri (Quranic Text) |

---

## 📊 Project Structure

```
tabsirah/
├── dataset/              # Training images (~6,000 images, 30 classes)
├── data_processed/       # Processed features (pickle files)
├── models/               # Trained AI models
│   ├── hand_landmarker.task   # MediaPipe model
│   └── model_arabic.p         # Random Forest classifier
├── src/                  # Data processing & training scripts
│   ├── 3_process_data.py
│   └── 4_train_model.py
├── web_app/              # Main Flask application
│   ├── app.py            # Flask server
│   ├── inference_classifier.py  # AI inference
│   ├── surah_data.py     # Quranic content
│   ├── static/           # Sign images & assets
│   └── templates/        # HTML templates
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

---

## 🎯 Roadmap

### Short-Term
- [ ] Add 10 more surahs
- [ ] User accounts & progress saving
- [ ] Offline PWA mode
- [ ] Accessibility improvements

### Mid-Term
- [ ] Mobile native apps (iOS/Android)
- [ ] Advanced analytics dashboard
- [ ] Gamification (badges, streaks)
- [ ] Social features

### Long-Term
- [ ] Deep learning models (LSTM/Transformer)
- [ ] Full Quran coverage (30 Juz')
- [ ] Teacher dashboard
- [ ] Video recording & review

---

## 🤝 Contributing

We welcome contributions! Here's how:

1. **Report Bugs**: Open an issue with reproduction steps
2. **Suggest Features**: Share your ideas in feature requests
3. **Submit Code**: 
   - Fork the repo
   - Create a feature branch
   - Make your changes
   - Submit a pull request

See [CONTRIBUTING.md](md_files/CONTRIBUTING.md) for detailed guidelines.

---

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Credits

### Datasets
- Arabic Sign Language Dataset (Kaggle)

### Libraries
- MediaPipe by Google
- Scikit-Learn
- Flask
- Tailwind CSS

### Fonts
- Cairo by Mohamed Gaber
- Amiri by Khaled Hosny

---

## 📞 Contact & Support

- **Documentation**: [Complete Docs](COMPLETE_PROJECT_DOCUMENTATION.md)
- **Issues**: [GitHub Issues](https://github.com/your-username/tabsirah/issues)
- **Email**: support@tabsirah.com

---

## 🌟 Star History

If you find this project useful, please consider giving it a star ⭐

---

<div align="center">

**Made with ❤️ for the Arabic Sign Language Community**

*May this project bring benefit to learners of the Holy Quran. Ameen.*

</div>
