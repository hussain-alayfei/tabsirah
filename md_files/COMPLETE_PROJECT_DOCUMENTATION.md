# 📖 Tabsirah (تطبيق تبصرة) - Complete Project Documentation

**Version:** 2.1  
**Last Updated:** January 22, 2026  
**Status:** Production Ready

---

## 📑 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Features & Capabilities](#2-features--capabilities)
3. [Technical Architecture](#3-technical-architecture)
4. [Technology Stack](#4-technology-stack)
5. [AI Model & Inference](#5-ai-model--inference-logic)
6. [Frontend Architecture](#6-frontend-architecture)
7. [Backend Architecture](#7-backend-architecture)
8. [Design System](#8-design-system)
9. [Key Implementations](#9-key-implementations)
10. [Bug Fixes & Improvements](#10-bug-fixes--improvements)
11. [Installation Guide](#11-installation-guide)
12. [Deployment Guide](#12-deployment-guide)
13. [Troubleshooting](#13-troubleshooting)
14. [Future Roadmap](#14-future-roadmap)
15. [Contributing](#15-contributing)

---

## 1. Project Overview

### 1.1 Mission
**Tabsirah** (تبصرة - "Insight") is an innovative AI-powered web application designed to help users learn and memorize the Holy Quran using **Arabic Sign Language (ArASL)**. The application combines computer vision, machine learning, and intuitive UI/UX to provide real-time feedback on sign accuracy.

### 1.2 Target Audience
- Deaf and hearing-impaired individuals learning Quranic recitation
- Sign language instructors teaching Quranic Arabic
- Students memorizing the Quran through sign language

### 1.3 Core Value Proposition
- **Real-time AI Feedback**: Instant validation of sign accuracy
- **Verse-by-Verse Training**: Structured learning path through Quranic surahs
- **Detailed Analytics**: Track progress, identify weak points, and improve
- **No Installation Required**: Runs entirely in the web browser

---

## 2. Features & Capabilities

### 2.1 Practice Reading Mode (تدرب على القراءة)

#### Purpose
Visual learning mode where users learn new signs with reference images.

#### User Flow
1. Select a Surah (e.g., Al-Kawthar)
2. Choose to watch instructional video OR start training directly
3. See reference sign images for each letter
4. Perform signs in front of camera
5. Get instant feedback (correct/incorrect)
6. Progress through verses word by word

#### Key Features
- **Reference Cards Track**: Horizontal scrolling cards showing each letter's sign image
- **Real-time Hand Tracking**: Green skeletal overlay on detected hand
- **Current Word Display**: Shows the current word with colored letters (green = completed, blue = current, gray = upcoming)
- **Score Tracking**: Real-time score display
- **Responsive Design**: Works on mobile, tablet, and desktop

### 2.2 Practice Reciting Mode (تدرب على التسميع)

#### Purpose
Testing mode for memorization assessment - users recite from memory without reference images.

#### User Flow
1. Select a Surah for recitation test
2. Signs are hidden - user must recall from memory
3. Camera detects signs and validates in real-time
4. If error occurs 10 times on same letter → Correction overlay appears
5. User can skip letter or retry
6. At end → Detailed results showing verse-by-verse accuracy

#### Key Features
- **Hidden Reference Images**: No visual aids during recitation
- **Error Counter**: Shows attempts per letter (0/10 → 10/10)
- **Verse Progress Bar**: Displays "آية X من Y" with progress percentage
- **Intelligent Error Tracking**: 
  - Only counts unique incorrect predictions (not repeated same letter)
  - Tracks errors per letter position
- **Correction Overlay**: 
  - Shows correct sign image after 10 failed attempts
  - Displays error count
  - Options: Skip or Retry
- **Verse Pass/Fail Logic**:
  - Calculates error rate based on unique letters failed
  - Verse fails if error rate > 40%
- **Final Results Screen**:
  - Verse-by-verse breakdown (passed/failed)
  - Error rate percentage per verse
  - Total correct vs. incorrect verses
  - Option to "Practice Errors" (retry only failed verses)

### 2.3 Surah Management System
- **Dynamic Surah Loading**: Surahs loaded from `surah_data.py`
- **Lock/Unlock Mechanism**: Progressive unlocking based on completion
- **Search Functionality**: Search bar in surah selection view
- **Metadata Display**: Surah number, name, verse count, description

### 2.4 Analytics & Progress Tracking
- **Verse-Level Metrics**: Error rate, letters failed, total letters
- **Weak Point Identification**: Shows which letters caused most errors
- **Practice Errors Feature**: Re-train only on failed verses

---

## 3. Technical Architecture

### 3.1 System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT SIDE                         │
├─────────────────────────────────────────────────────────────┤
│  HTML/CSS (Tailwind) + Vanilla JavaScript                   │
│  ┌─────────────────┐  ┌──────────────────┐                 │
│  │   Webcam Feed   │  │  MediaPipe.js    │                 │
│  │  (getUserMedia) │→ │  Hand Landmarker │                 │
│  └─────────────────┘  └──────────────────┘                 │
│           ↓                      ↓                           │
│    Canvas Rendering      Extract 21 Landmarks               │
│    (Hand Skeleton)            (x, y)                         │
│           ↓                      ↓                           │
│    Base64 Encode         Send via Fetch API                 │
└──────────────────────────────┬──────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│                       SERVER SIDE (Flask)                   │
├─────────────────────────────────────────────────────────────┤
│  POST /predict                                              │
│    ↓                                                         │
│  Decode Base64 → OpenCV Image                               │
│    ↓                                                         │
│  MediaPipe HandLandmarker (Python)                          │
│    ↓                                                         │
│  Extract 21 Landmarks → Normalize (relative to wrist)       │
│    ↓                                                         │
│  Random Forest Classifier (scikit-learn)                    │
│    ↓                                                         │
│  Predict Arabic Letter (0-29 → ا-ي + لا + ة)               │
│    ↓                                                         │
│  Return { prediction: 'ا', landmarks: [...] }               │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Data Flow

#### Training Flow (Practice Reading)
1. User performs sign → Webcam captures frame
2. MediaPipe (JS) detects hand → Draws skeleton
3. Frame sent to `/predict` endpoint
4. Server extracts landmarks → Classifies letter
5. Prediction sent back to client
6. JavaScript validates against target letter
7. UI updates (green flash if correct, error counter if wrong)
8. Progress to next letter if correct

#### Recitation Flow (Practice Reciting)
1. User performs sign (no reference images shown)
2. Same detection and prediction process
3. Error tracking: `letterErrorCount[currentTargetIndex]++`
4. If same wrong letter repeated → Don't count again
5. If `letterErrorCount >= 10` → Show correction overlay
6. User can skip or retry
7. On verse complete → Calculate error rate
8. If error rate > 40% → Mark verse as failed
9. Final results → Show detailed breakdown

---

## 4. Technology Stack

### 4.1 Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **HTML5** | - | Structure and semantic markup |
| **Tailwind CSS** | 3.4.x (CDN) | Utility-first styling and responsiveness |
| **JavaScript (ES6+)** | - | Application logic and DOM manipulation |
| **MediaPipe (JS)** | Latest | Client-side hand detection and landmark extraction |
| **Canvas API** | - | Drawing hand skeleton overlay |

### 4.2 Backend
| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.10+ | Programming language |
| **Flask** | Latest | Web framework and API server |
| **MediaPipe (Python)** | Latest | Server-side hand landmark extraction |
| **OpenCV** | Latest | Image processing |
| **scikit-learn** | Latest | Machine learning (Random Forest) |
| **NumPy** | <2.0 | Numerical operations |

### 4.3 AI/ML Components
| Component | Purpose |
|-----------|---------|
| **MediaPipe Hand Landmarker** | Detects 21 3D hand landmarks |
| **Random Forest Classifier** | Predicts Arabic letter from landmarks |
| **Feature Normalization** | Makes model position/scale invariant |

### 4.4 Dependencies (`requirements.txt`)
```
opencv-python
mediapipe
scikit-learn
flask
kagglehub
numpy<2
```

---

## 5. AI Model & Inference Logic

### 5.1 Model Architecture

#### Components
- **Hand Detection**: MediaPipe Hand Landmarker (Google)
- **Feature Extraction**: Custom normalization logic
- **Classification**: Random Forest Classifier (scikit-learn)

### 5.2 Feature Extraction Pipeline (`web_app/inference_classifier.py`)

The model does NOT use raw pixel data. It uses geometric relationships between hand landmarks.

#### Step 1: Hand Detection
- Input: RGB Frame
- Output: 21 Landmarks (x, y, z coordinates)

#### Step 2: Normalization (Crucial)
To make the model robust to camera distance and hand size, we use a specific normalization technique:
1.  **Anchor to Wrist**: Subtract the wrist coordinate (Landmark 0) from all points.
    *   `P_new = P - P_wrist`
2.  **Scale Invariance**: Calculate the Euclidean distance between the wrist and the Middle Finger Tip (Landmark 12).
    *   `Scale = Distance(Wrist, Middle_Tip)`
3.  **Normalize**: Divide all coordinates by this scale factor.
    *   `P_final_x = P_new_x / Scale`
    *   `P_final_y = P_new_y / Scale`

 This ensures that whether the hand is close to the camera (large) or far away (small), the numerical features represented to the model are identical.

#### Step 3: Feature Vector
- The final input to the classifier is a flattened vector of 42 values:
- `[x0, y0, ..., x20, y20]` (Normalized)

### 5.3 The Classifier
- **File**: `models/model_normalized_augmented_LGM.p`
- **Type**: Random Forest Classifier
- **Classes**: 30 Arabic Sign Language Classes (Letters + combinations)

**Why Random Forest?**
- Fast inference time (<10ms)
- Robust to noise
- Excellent performance on tabular/geometric data


---

## 6. Frontend Architecture

### 6.1 HTML Structure (`web_app/templates/index.html`)

#### Views (Single Page Application)
```html
<div id="landingView">           <!-- Home screen -->
<div id="surahSelectionView">    <!-- Surah list -->
<div id="videoChoiceView">       <!-- Video or Direct Training -->
<div id="appView">               <!-- Main training interface -->
<div id="resultsView">           <!-- Final results -->
```

#### Main Training Interface (`#appView`)
```html
<main>
  <section>                      <!-- Camera Section -->
    <video id="videoElement">    <!-- Webcam feed -->
    <canvas id="overlayCanvas">  <!-- Hand skeleton -->
    <div id="predBadge">         <!-- Predicted letter badge -->
    <div id="letterErrorCounter"> <!-- Error counter (recitation) -->
  </section>
  
  <section id="verseProgressDisplay">  <!-- Verse progress bar -->
  <section id="currentWordDisplay">    <!-- Current word (colored) -->
  <section id="cardsTrack">            <!-- Reference cards -->
</main>
```

### 6.2 JavaScript Architecture

#### Global State Variables
```javascript
// Mode flags
let surahMode = false;           // Is user in surah training?
let recitationMode = false;      // Is user in recitation mode?

// Surah data
let currentSurah = null;         // Current surah object
let currentVerseIndex = 0;       // Current verse index

// Training state
let targetSentence = "";         // Current verse text
let currentTargetIndex = 0;      // Current letter index
let score = 0;                   // User score

// Recitation tracking
let letterErrorCount = {};       // Error count per letter position
let lastIncorrectPrediction = {}; // Track last wrong prediction
let verseResults = [];           // Results per verse
let failedVerses = [];           // Verses with error rate > 40%

// Constants
const MAX_ATTEMPTS_PER_LETTER = 10;
const VERSE_FAILURE_THRESHOLD = 40; // 40% error rate
```

#### Core Functions

##### 1. Mode Selection
```javascript
selectTrainingMode()  // → Navigate to surah selection (training)
selectFreePracticeMode() // → Navigate to surah selection (recitation)
```

##### 2. Surah Management
```javascript
loadSurahs()          // Fetch surahs from /get_surahs
selectSurah(id)       // Select and load specific surah
```

##### 3. Training Flow
```javascript
startSurahTraining()  // Initialize verse-by-verse training
startVerseTraining()  // Start training for current verse
onVerseComplete()     // Calculate error rate, advance verse
```

##### 4. Prediction Loop
```javascript
sendForPrediction()   // Send frame to /predict endpoint
handleSuccess()       // On correct prediction
handleIncorrect()     // On wrong prediction
```

##### 5. Recitation-Specific
```javascript
showCorrectionOverlay(letter)  // Show correct sign after 10 errors
skipLetter()          // Mark letter as failed, advance
retryLetter()         // Hide overlay, resume detection
startPracticeErrors() // Retry only failed verses
```

##### 6. UI Updates
```javascript
updateCurrentWord()   // Update colored word display
updateVerseProgress() // Update "آية X من Y" counter
renderCards()         // Render reference sign cards
```

### 6.3 Arabic Character Normalization (Client-Side)

#### Problem
Arabic letters have multiple forms (أ, إ, آ → ا) but model only trained on base forms.

#### Solution
```javascript
function normalizeArabic(char) {
    // Normalize Alef variants
    char = char.replace(/[أإآءٱ]/g, 'ا');
    
    // Normalize Ya variants
    char = char.replace(/[ىئ]/g, 'ي');
    
    // Normalize Ta Marbuta
    char = char.replace(/ة/g, 'ه');
    
    // Remove diacritics
    char = char.replace(/[\u064B-\u065F\u0670]/g, '');
    
    return char;
}
```

### 6.4 Hand Skeleton Visualization

#### Drawing Logic (`overlayCanvas`)
```javascript
// Draw connections (bones)
for (const [start, end] of HAND_CONNECTIONS) {
    ctx.beginPath();
    ctx.moveTo(landmarks[start].x, landmarks[start].y);
    ctx.lineTo(landmarks[end].x, landmarks[end].y);
    ctx.strokeStyle = '#22C55E'; // Green
    ctx.lineWidth = 4;
    ctx.stroke();
}

// Draw landmarks (joints)
for (const point of landmarks) {
    ctx.beginPath();
    ctx.arc(point.x, point.y, 8, 0, 2 * Math.PI);
    ctx.fillStyle = '#FFFFFF';
    ctx.fill();
    ctx.strokeStyle = '#22C55E';
    ctx.lineWidth = 3;
    ctx.stroke();
}
```

---

## 7. Backend Architecture

### 7.1 Flask Application (`web_app/app.py`)

#### Initialization
```python
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False  # Support Arabic in JSON

# Load AI model on startup
classifier = SignLanguageClassifier()
```

#### API Endpoints

##### GET `/`
- **Purpose**: Serve main HTML page
- **Returns**: `templates/index.html`

##### GET `/get_surahs`
- **Purpose**: Fetch all surahs with metadata
- **Returns**: JSON object with all surahs
- **Example Response**:
```json
{
  "al-kawthar": {
    "id": "al-kawthar",
    "name": "سورة الكوثر",
    "number": 108,
    "verses": ["إنا أعطيناك الكوثر", ...],
    "unlocked": true
  }
}
```

##### GET `/get_surah/<surah_id>`
- **Purpose**: Fetch specific surah data
- **Returns**: 
  - `200`: Surah object
  - `403`: If surah is locked
  - `404`: If surah doesn't exist

##### GET `/sign_image/<char>`
- **Purpose**: Serve sign image for given character
- **Logic**:
  1. Decode URL-encoded character
  2. Normalize character (أ → ا)
  3. Look for exact match (`ا.jpg`)
  4. If not found, search for versioned files (`ا_v2.jpg`)
  5. Return last match (for versioning support)
- **Returns**: JPEG image or 404

##### POST `/predict`
- **Purpose**: Classify hand sign from image
- **Input**: JSON with base64-encoded image
- **Process**:
  1. Decode base64 → OpenCV image
  2. Convert BGR → RGB
  3. Run MediaPipe hand detection
  4. Extract and normalize landmarks
  5. Classify with Random Forest
  6. Return prediction + landmarks
- **Returns**:
```json
{
  "prediction": "ا",
  "landmarks": [[{x: 0.5, y: 0.3}, ...]]
}
```

### 7.2 Inference Classifier (`web_app/inference_classifier.py`)

#### Initialization
```python
class SignLanguageClassifier:
    def __init__(self):
        # Load Random Forest model
        # Updated to use the consistent normalized model
        model_path = os.path.join(base_dir, 'models', 'model_normalized_augmented_LGM.p')
        
        with open(model_path, 'rb') as f:
            self.model_dict = pickle.load(f)
        self.model = self.model_dict['model']
        
        # Initialize MediaPipe Hand Landmarker
        self.detector = vision.HandLandmarker.create_from_options(...)
        
        # Arabic labels mapping
        self.labels_dict = {0: 'ا', 1: 'ب', ...}
```

#### Prediction Method
```python
def predict(self, frame_rgb):
    # Detect hand landmarks
    results = self.detector.detect(mp_image)
    
    if results.hand_landmarks:
        # Extract first hand
        hand = results.hand_landmarks[0]
        
        # Extract features using Wrist-Anchor + Middle-Finger-Scale Normalization
        features = self._preprocess_landmarks(hand)
        
        # Predict
        prediction = self.model.predict([features])
        label = self.labels_dict[int(prediction[0])]
        
        return label, results
    
    return None, results
```

### 7.3 Arabic Character Normalization (Server-Side)

#### Function: `normalize_char_for_image(char)`
```python
def normalize_char_for_image(char):
    # Normalize Alef
    char = char.replace('أ', 'ا')
               .replace('إ', 'ا')
               .replace('آ', 'ا')
               .replace('ء', 'ا')
               .replace('ٱ', 'ا')
    
    # Normalize Ya
    char = char.replace('ى', 'ي')
               .replace('ئ', 'ي')
    
    # Normalize Ta Marbuta
    char = char.replace('ة', 'ه')
    
    # Remove diacritics
    char = re.sub(r'[\u064B-\u065F\u0670]', '', char)
    
    return char
```

### 7.4 Surah Data Management (`web_app/surah_data.py`)

#### Data Structure
```python
SURAHS = {
    'al-kawthar': {
        'id': 'al-kawthar',
        'name': 'سورة الكوثر',
        'name_english': 'Al-Kawthar',
        'number': 108,
        'verses': [
            'إنا أعطيناك الكوثر',
            'فصل لربك وانحر',
            'إن شانئك هو الأبتر'
        ],
        'unlocked': True,
        'video_url': 'https://...',
        'description': 'سورة مكية، عدد آياتها 3'
    }
}
```

#### Helper Functions
```python
get_all_surahs()         # Return all surahs
get_surah(surah_id)      # Get specific surah
is_surah_unlocked(id)    # Check if unlocked
```

---

## 8. Design System

### 8.1 Color Palette

#### Primary Colors
```css
/* Primary Blue - Logo, Icons, Brand Identity */
--primary-blue: #617ED2;
/* RGB(97, 126, 210) */

/* Light Cyan - "Practice Reading" Card */
--light-cyan: #3CA1D3;
/* RGB(60, 161, 211) */

/* Dark Navy - "Practice Reciting" Card */
--dark-navy: #4A6BB7;
/* RGB(74, 107, 183) */
```

#### Accent Colors
```css
/* Turquoise - Active States, Home Button */
--turquoise: #0284CA;
/* RGB(2, 132, 202) */

/* Success Green - Correct Predictions */
--success-green: #22C55E;

/* Error Red - Incorrect Predictions */
--error-red: #EF4444;
```

#### Neutral Colors
```css
/* White Background */
--white: #FFFFFF;

/* Dark Text */
--dark-text: #2C3E50;

/* Light Gray - Cards, Borders */
--light-gray: #F1F5F9;
```

### 8.2 Typography

#### Font Families
```css
/* ZAIN - Modern Arabic UI Font */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
font-family: 'Cairo', sans-serif;

/* Amiri - Traditional Quranic Text */
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');
font-family: 'Amiri', serif;
```

#### Usage
```css
/* General UI */
body, button, input {
    font-family: 'Cairo', sans-serif;
}

/* Quranic Verses */
.quran-text {
    font-family: 'Amiri', serif;
}
```

### 8.3 UI Components

#### Button Styles
```html
<!-- Primary Button -->
<button class="bg-gradient-to-br from-blue-500 to-blue-600 
               text-white font-bold py-3 px-6 rounded-2xl 
               shadow-lg hover:shadow-xl transform hover:scale-105 
               transition-all duration-300">
    Button Text
</button>

<!-- Card Style -->
<div class="bg-white rounded-3xl shadow-2xl shadow-blue-900/10 
            p-8 border border-slate-50">
    Card Content
</div>
```

#### Animation Classes
```css
@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(30px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.animate-fade-in-up {
    animation: fadeInUp 0.6s ease-out;
}
```

### 8.4 Responsive Design

#### Breakpoints (Tailwind)
```css
/* Mobile First */
/* sm: 640px */
/* md: 768px */
/* lg: 1024px */
/* xl: 1280px */
```

#### Example Usage
```html
<!-- Responsive Grid -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-5">
    <!-- Stacks on mobile, 2 columns on tablet+ -->
</div>

<!-- Responsive Padding -->
<div class="px-4 md:px-6 lg:px-8">
    <!-- Scales padding based on screen size -->
</div>
```

---

## 9. Key Implementations

### 9.1 Surah Training Mode

#### Architecture
```javascript
// State
currentSurah = {
    verses: ["إنا أعطيناك الكوثر", ...]
}
currentVerseIndex = 0
targetSentence = currentSurah.verses[0]

// Flow
startSurahTraining() {
    1. Load first verse
    2. Display reference cards
    3. Start prediction loop
}

onVerseComplete() {
    1. Show "Ahsant" (Well Done) message
    2. Increment verse index
    3. Load next verse OR show final results
}
```

### 9.2 Recitation Mode with Error Tracking

#### Error Tracking Logic
```javascript
// Track errors per letter position
letterErrorCount = {
    0: 3,  // First letter: 3 errors
    1: 0,  // Second letter: 0 errors
    2: 10  // Third letter: 10 errors (threshold reached)
}

// Prevent counting repeated same wrong predictions
lastIncorrectPrediction = {
    0: 'ب',  // Position 0: last wrong prediction was 'ب'
    2: 'ن'   // Position 2: last wrong prediction was 'ن'
}

// On incorrect prediction
if (predicted !== target) {
    // Only count if prediction is different from last error
    if (lastIncorrectPrediction[index] !== predicted) {
        letterErrorCount[index]++;
        lastIncorrectPrediction[index] = predicted;
    }
    
    // Check threshold
    if (letterErrorCount[index] >= 10) {
        showCorrectionOverlay(target);
    }
}
```

#### Verse Error Rate Calculation
```javascript
onVerseComplete() {
    // Count unique letters with errors
    let lettersWithErrors = 0;
    for (let idx in letterErrorCount) {
        if (letterErrorCount[idx] > 0) {
            lettersWithErrors++;
        }
    }
    
    // Calculate error rate
    const totalLetters = targetSentence.replace(/\s/g, '').length;
    const errorRate = (lettersWithErrors / totalLetters) * 100;
    
    // Determine pass/fail
    const passed = errorRate <= 40;
    
    // Store result
    verseResults.push({
        verse: targetSentence,
        errorRate,
        lettersWithErrors,
        totalLetters,
        passed
    });
    
    // Add to failed verses if > 40%
    if (!passed) {
        failedVerses.push(...);
    }
}
```

### 9.3 Correction Overlay

#### Trigger Condition
- User makes 10 incorrect attempts on the same letter

#### Overlay Content
```html
<div id="correctionOverlay">
    <h2>الإشارة الصحيحة</h2>
    
    <!-- Correct Sign Image -->
    <img id="correctSignImage" src="/sign_image/ا">
    
    <!-- Letter Display -->
    <div id="correctLetterDisplay">ا</div>
    
    <!-- Error Count Message -->
    <p>حاولت 10 من 10 مرات</p>
    
    <!-- Actions -->
    <button onclick="retryLetter()">إعادة المحاولة</button>
    <button onclick="skipLetter()">تخطي</button>
</div>
```

#### Actions
- **Retry**: Hide overlay, resume detection, reset error counter
- **Skip**: Mark letter as failed, advance to next letter

### 9.4 Practice Errors Feature

#### Purpose
Allow user to re-train only on verses where they failed (error rate > 40%).

#### Implementation
```javascript
startPracticeErrors() {
    // Filter failed verses
    const failedVerseTexts = failedVerses.map(v => v.verse);
    
    // Reset state
    letterErrorCount = {};
    verseResults = [];
    failedVerses = [];
    currentVerseIndex = 0;
    
    // Replace surah verses with only failed ones
    currentSurah.verses = failedVerseTexts;
    
    // Restart training
    startSurahTraining();
}
```

### 9.5 Real-Time Hand Skeleton Visualization

#### MediaPipe Hand Connections
```javascript
const HAND_CONNECTIONS = [
    [0, 1], [1, 2], [2, 3], [3, 4],        // Thumb
    [0, 5], [5, 6], [6, 7], [7, 8],        // Index
    [0, 9], [9, 10], [10, 11], [11, 12],   // Middle
    [0, 13], [13, 14], [14, 15], [15, 16], // Ring
    [0, 17], [17, 18], [18, 19], [19, 20], // Pinky
    [5, 9], [9, 13], [13, 17]              // Palm
];
```

#### Drawing on Canvas
```javascript
drawHandSkeleton(landmarks, canvasElement) {
    const ctx = canvasElement.getContext('2d');
    
    // Convert normalized coordinates to canvas pixels
    const width = canvasElement.width;
    const height = canvasElement.height;
    
    const points = landmarks.map(lm => ({
        x: lm.x * width,
        y: lm.y * height
    }));
    
    // Draw bones (lines)
    ctx.strokeStyle = '#22C55E'; // Green
    ctx.lineWidth = 4;
    ctx.lineCap = 'round';
    
    for (const [start, end] of HAND_CONNECTIONS) {
        ctx.beginPath();
        ctx.moveTo(points[start].x, points[start].y);
        ctx.lineTo(points[end].x, points[end].y);
        ctx.stroke();
    }
    
    // Draw joints (circles)
    for (const point of points) {
        // Outer circle (white)
        ctx.beginPath();
        ctx.arc(point.x, point.y, 8, 0, 2 * Math.PI);
        ctx.fillStyle = '#FFFFFF';
        ctx.fill();
        
        // Border (green)
        ctx.strokeStyle = '#22C55E';
        ctx.lineWidth = 3;
        ctx.stroke();
    }
}
```

---

## 10. Bug Fixes & Improvements

This section documents all fixes and improvements made during development.

### 10.1 Arabic Character Normalization

#### Problem
- Model trained on base forms (ا, ي, ه)
- User input contains variants (أ, إ, آ, ء, ى, ئ, ة)
- Predictions failed due to mismatch

#### Solution
Implemented normalization on both client and server:

**Client-Side (`index.html`)**:
```javascript
function normalizeArabic(char) {
    char = char.replace(/[أإآءٱ]/g, 'ا');
    char = char.replace(/[ىئ]/g, 'ي');
    char = char.replace(/ة/g, 'ه');
    return char;
}
```

**Server-Side (`app.py`)**:
```python
def normalize_char_for_image(char):
    char = char.replace('أ', 'ا').replace('إ', 'ا')...
    char = char.replace('ى', 'ي').replace('ئ', 'ي')
    char = char.replace('ة', 'ه')
    return char
```

#### Impact
- ✅ All Alef variants now map to single sign
- ✅ Sign images load correctly
- ✅ Predictions match correctly

### 10.2 Unicode Encoding Errors

#### Problem
```
UnicodeEncodeError: 'charmap' codec can't encode character '\u0625'
```
Flask console on Windows couldn't display Arabic characters in `print()` statements.

#### Solution
- Removed all `print()` statements containing Arabic characters from `app.py`
- Added descriptive English messages for debugging

#### Impact
- ✅ No more console errors
- ✅ Cleaner logs

### 10.3 Camera Feed and Model Issues

#### Problem
- Camera feed was unclear/distorted
- Model returning `None` for valid signs
- Sign images not loading (404 errors)

#### Root Causes
1. Sign images missing for character variants (إ, أ, etc.)
2. MediaPipe detection confidence too high
3. Image normalization not applied

#### Solutions
1. Implemented character normalization in `get_sign_image()`
2. Lowered detection confidence:
   ```python
   min_hand_detection_confidence=0.3  # Was 0.5
   ```
3. Added fallback image search with glob patterns

#### Impact
- ✅ All sign images load correctly
- ✅ Detection more sensitive (catches more signs)
- ✅ Fewer false negatives

### 10.4 Responsive Design Issues

#### Problem
- Home page not responsive on mobile/tablet
- Bottom navigation bar disappearing on mobile
- Components too large, camera too small

#### Solutions

**1. Made Home Page Responsive**:
```html
<!-- Before -->
<div class="grid grid-cols-2 gap-5">

<!-- After -->
<div class="grid grid-cols-1 md:grid-cols-2 gap-5">
```

**2. Fixed Bottom Navigation**:
```html
<!-- Before -->
<nav class="absolute bottom-0">

<!-- After -->
<nav class="fixed bottom-0">
```

**3. Increased Camera Size**:
```html
<!-- Before -->
<section class="max-w-md aspect-[3/4]">

<!-- After -->
<section class="max-w-xl aspect-[9/16]">
```

**4. Reduced Component Sizes**:
```html
<!-- Prediction Badge -->
<!-- Before: p-6, min-w-[110px] -->
<!-- After: p-3, min-w-[80px] -->

<!-- Error Counter -->
<!-- Before: px-4 py-3 -->
<!-- After: px-3 py-2 -->
```

#### Impact
- ✅ Works on all screen sizes
- ✅ Navigation always visible
- ✅ Camera feed larger and more usable
- ✅ Cleaner UI with better proportions

### 10.5 Surah Selection Redesign

#### Problem
- Grid layout cluttered
- No search functionality
- Hard to find specific surah

#### Solution
```html
<!-- Added Search Bar -->
<input type="text" id="surahSearch" 
       placeholder="ابحث عن سورة..." 
       oninput="filterSurahs()">

<!-- Changed to Vertical List -->
<div class="flex flex-col gap-3">
    <!-- Surah cards -->
</div>
```

#### Impact
- ✅ Easier to browse surahs
- ✅ Quick search functionality
- ✅ Better UX on mobile

### 10.6 Video Choice Screen Redesign

#### Problem
- Old design didn't match brand style
- Text said "تسميع" (recitation) instead of "تدريب" (training)
- Buttons too large

#### Solution
```html
<!-- YouTube-Style Card (Red) -->
<button class="relative h-20 rounded-2xl overflow-hidden 
               bg-gradient-to-br from-red-500 to-red-600">
    <!-- YouTube icon + "مشاهدة الشرح" -->
</button>

<!-- Practice-Style Card (Green/Teal) -->
<button class="relative h-20 rounded-2xl overflow-hidden 
               bg-gradient-to-br from-emerald-500 to-teal-600">
    <!-- Brain icon + "بدء التدريب" -->
</button>
```

#### Impact
- ✅ Modern, clean design
- ✅ Correct terminology
- ✅ Better visual hierarchy

### 10.7 Typography Improvements

#### Problem
- Inconsistent fonts
- Quranic text not using appropriate font
- Prediction badge using system font

#### Solution
```css
/* Import Fonts */
@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&display=swap');

/* Apply to Elements */
body { font-family: 'Cairo', sans-serif; }
.quran-text { font-family: 'Amiri', serif; }
```

**Applied to**:
- Prediction badge (`#predVal`)
- Current word display (`#currentWordText`)
- Score display
- All verse text

#### Impact
- ✅ Beautiful Quranic typography
- ✅ Consistent UI font
- ✅ Better readability

### 10.8 Border Styling Fix

#### Problem
- Active letter card's top border disappearing
- Hard to see which letter is active

#### Solution
```css
/* Before */
.active-card {
    border: 2px solid #3B82F6;
    transform: scale(1.1);
}

/* After */
.active-card {
    border: 3px solid #3B82F6;
    box-shadow: 0 4px 20px rgba(59, 130, 246, 0.4);
    transform: scale(1.15) translateY(-4px);
}
```

#### Impact
- ✅ Clear visual indicator
- ✅ Better depth perception
- ✅ Smoother animations

### 10.9 Smooth Animations

#### Problem
- Abrupt transitions
- No visual feedback on correct predictions
- Jarring screen changes

#### Solutions

**1. Green Flash on Correct Prediction**:
```javascript
handleSuccess() {
    // Show green flash
    document.getElementById('successFlash').classList.remove('hidden');
    setTimeout(() => {
        document.getElementById('successFlash').classList.add('hidden');
    }, 300);
}
```

**2. Bouncing Checkmark**:
```html
<div id="successFlash" class="absolute inset-0 bg-green-500/20 hidden">
    <div class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
        <div class="text-6xl animate-bounce">✓</div>
    </div>
</div>
```

**3. Fade-In Animations**:
```css
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(30px); }
    to { opacity: 1; transform: translateY(0); }
}
```

#### Impact
- ✅ Satisfying feedback
- ✅ Smooth transitions
- ✅ Professional feel

### 10.10 Error Tracking Refinement

#### Problem
- Repeated predictions of same wrong letter counted as multiple errors
- Example: Predicting "ف ف ف ف" for "ا" counted as 4 errors
- Unfair penalty

#### Solution
```javascript
// Track last incorrect prediction per letter position
let lastIncorrectPrediction = {};

// In sendForPrediction()
if (predicted !== target) {
    // Only count if different from last error
    if (lastIncorrectPrediction[currentTargetIndex] !== predicted) {
        letterErrorCount[currentTargetIndex]++;
        lastIncorrectPrediction[currentTargetIndex] = predicted;
    }
}
```

#### Impact
- ✅ Fair error counting
- ✅ Doesn't penalize stuck predictions
- ✅ More accurate assessment

### 10.11 Verse Error Rate Calculation

#### Problem
- Initial implementation counted total incorrect attempts
- Led to error rates > 100% (e.g., 300%)
- Example: 10 letters, 30 wrong attempts = 300% error rate ❌

#### Correct Implementation
```javascript
// Count unique letters with errors
let lettersWithErrors = 0;
for (let idx in letterErrorCount) {
    if (letterErrorCount[idx] > 0) {
        lettersWithErrors++;  // Count once per letter
    }
}

// Calculate percentage
const errorRate = (lettersWithErrors / totalLetters) * 100;
```

**Example**:
- Verse: "إنا" (3 letters)
- Errors: Position 0: 5 attempts, Position 2: 3 attempts
- Letters with errors: 2
- Error rate: (2 / 3) * 100 = 66.7% ✅

#### Impact
- ✅ Accurate error rates (0-100%)
- ✅ Fair verse pass/fail determination
- ✅ Meaningful analytics

### 10.12 Branding Update

#### Problem
- Generic branding
- No consistent color scheme

#### Solution
**Updated Colors**:
```css
Primary Blue: #617ED2 (Logo, Icons)
Light Cyan: #3CA1D3 (Reading Card)
Dark Navy: #4A6BB7 (Recitation Card)
Turquoise: #0284CA (Active States)
```

**Updated Text**:
- App Title: "تطبيق تبصرة"
- Subtitle: "للحفظ المتقن للقرآن الكريم"

#### Impact
- ✅ Professional brand identity
- ✅ Consistent visual language
- ✅ Memorable app name

### 10.13 Localization (Arabic UI)

#### Changes
```javascript
// Before
"Detected" → "الإشارة"
"Errors" → "أخطاء"
"Verse 1 of 3" → "آية 1 من 3"
"Skip" → "تخطي"
"Retry" → "إعادة المحاولة"
```

#### Impact
- ✅ Fully Arabic interface
- ✅ Better accessibility for target audience
- ✅ Cultural appropriateness

---

## 11. Installation Guide

### 11.1 Prerequisites

#### System Requirements
- **OS**: Windows 10/11, macOS, or Linux
- **Python**: 3.10 or higher
- **RAM**: Minimum 4GB (8GB recommended)
- **Webcam**: Required for sign detection

#### Software Requirements
- Git (for cloning repository)
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge)

### 11.2 Installation Steps

#### Step 1: Clone Repository
```bash
git clone https://github.com/your-username/tabsirah.git
cd tabsirah
```

#### Step 2: Create Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

**Expected Output**:
```
Collecting opencv-python...
Collecting mediapipe...
Collecting scikit-learn...
Collecting flask...
Successfully installed...
```

#### Step 4: Verify Model Files
```bash
# Check if models exist
ls models/
# Should see:
# - hand_landmarker.task (MediaPipe model)
# - model_arabic.p (Random Forest model)
```

If models are missing, run training scripts:
```bash
python src/3_process_data.py
python src/4_train_model.py
```

#### Step 5: Run Application
```bash
cd web_app
python app.py
```

**Expected Output**:
```
Model loaded successfully.
 * Running on http://127.0.0.1:5000
 * Restarting with stat
 * Debugger is active!
```

#### Step 6: Access Application
Open browser and navigate to:
```
http://127.0.0.1:5000
```

### 11.3 Troubleshooting Installation

#### Issue: `ModuleNotFoundError: No module named 'mediapipe'`
**Solution**: Reinstall dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Issue: `FileNotFoundError: models/model_arabic.p`
**Solution**: Train the model
```bash
python src/3_process_data.py
python src/4_train_model.py
```

#### Issue: Webcam not detected
**Solution**: 
1. Check browser permissions (allow camera access)
2. Try different browser
3. Test webcam in other applications

#### Issue: Slow predictions
**Solution**:
1. Close other applications
2. Use faster hardware
3. Reduce MediaPipe detection confidence (edit `inference_classifier.py`)

---

## 12. Deployment Guide

### 12.1 Production Checklist

Before deploying to production:

- [ ] Set `app.debug = False` in `app.py`
- [ ] Use production WSGI server (Gunicorn, uWSGI)
- [ ] Enable HTTPS
- [ ] Set up proper error logging
- [ ] Configure CORS if needed
- [ ] Optimize static assets
- [ ] Set up monitoring

### 12.2 Deployment Options

#### Option 1: Deploy to Heroku

**Steps**:
1. Create `Procfile`:
```
web: gunicorn web_app.app:app
```

2. Create `runtime.txt`:
```
python-3.10.12
```

3. Update `requirements.txt`:
```
gunicorn
opencv-python-headless
mediapipe
scikit-learn
flask
numpy<2
```

4. Deploy:
```bash
heroku create tabsirah-app
git push heroku main
heroku open
```

#### Option 2: Deploy to AWS EC2

**Steps**:
1. Launch EC2 instance (Ubuntu 22.04)
2. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip python3-venv nginx
```

3. Clone and setup:
```bash
git clone https://github.com/your-username/tabsirah.git
cd tabsirah
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

4. Create systemd service (`/etc/systemd/system/tabsirah.service`):
```ini
[Unit]
Description=Tabsirah Flask App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/tabsirah/web_app
Environment="PATH=/home/ubuntu/tabsirah/venv/bin"
ExecStart=/home/ubuntu/tabsirah/venv/bin/gunicorn -w 4 -b 0.0.0.0:5000 app:app

[Install]
WantedBy=multi-user.target
```

5. Start service:
```bash
sudo systemctl start tabsirah
sudo systemctl enable tabsirah
```

6. Configure Nginx:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### Option 3: Deploy to DigitalOcean App Platform

**Steps**:
1. Push code to GitHub
2. Create new App in DigitalOcean
3. Connect GitHub repository
4. Configure build settings:
   - Build Command: `pip install -r requirements.txt`
   - Run Command: `gunicorn --chdir web_app app:app`
5. Deploy

### 12.3 Environment Variables

For production, use environment variables:

```python
# app.py
import os

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
app.config['DEBUG'] = os.environ.get('DEBUG', 'False') == 'True'
```

Set in production:
```bash
export SECRET_KEY="your-secret-key"
export DEBUG="False"
```

### 12.4 Performance Optimization

#### 1. Use Gunicorn with Workers
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
# -w 4 = 4 worker processes
```

#### 2. Enable Gzip Compression
```python
from flask_compress import Compress
Compress(app)
```

#### 3. Cache Static Assets
```python
@app.route('/static/<path:filename>')
def static_files(filename):
    response = send_from_directory('static', filename)
    response.cache_control.max_age = 31536000  # 1 year
    return response
```

#### 4. Use CDN for MediaPipe
Already using CDN in `index.html`:
```html
<script src="https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@latest"></script>
```

---

## 13. Troubleshooting

### 13.1 Common Issues

#### Issue: Camera Not Working

**Symptoms**:
- Black screen instead of webcam feed
- "Permission denied" error

**Solutions**:
1. **Check Browser Permissions**:
   - Chrome: Settings → Privacy → Site Settings → Camera
   - Allow access for `localhost:5000`

2. **Use HTTPS**:
   - `getUserMedia` requires HTTPS (except localhost)
   - Deploy with SSL certificate

3. **Try Different Browser**:
   - Chrome has best WebRTC support
   - Avoid older browsers

#### Issue: Model Not Predicting

**Symptoms**:
- Prediction always returns `null`
- No hand landmarks detected

**Solutions**:
1. **Check Lighting**:
   - Ensure good lighting
   - Avoid backlighting

2. **Adjust Detection Confidence**:
```python
# inference_classifier.py
min_hand_detection_confidence=0.2  # Lower threshold
```

3. **Check Hand Visibility**:
   - Ensure entire hand is in frame
   - Keep hand at reasonable distance

#### Issue: Slow Performance

**Symptoms**:
- Laggy camera feed
- Delayed predictions

**Solutions**:
1. **Reduce Prediction Frequency**:
```javascript
// index.html
setInterval(sendForPrediction, 500);  // Was 300ms
```

2. **Close Other Applications**:
   - Free up CPU/RAM

3. **Use Better Hardware**:
   - Webcam with higher FPS
   - Faster processor

#### Issue: Arabic Text Not Displaying

**Symptoms**:
- Square boxes instead of Arabic letters
- Garbled text

**Solutions**:
1. **Check Font Loading**:
```html
<!-- Ensure fonts are loaded -->
<link href="https://fonts.googleapis.com/css2?family=Cairo&display=swap" rel="stylesheet">
```

2. **Set Charset**:
```html
<meta charset="UTF-8">
```

3. **Server Config**:
```python
app.config['JSON_AS_ASCII'] = False
```

#### Issue: 404 on Sign Images

**Symptoms**:
- Missing images for certain letters
- Console errors: `Failed to load resource: 404`

**Solutions**:
1. **Check Image Files**:
```bash
ls web_app/static/signs/
# Should have all 30 letters
```

2. **Verify Normalization**:
```python
# app.py - normalize_char_for_image()
# Ensure all variants are handled
```

3. **Add Missing Images**:
- Add `ا.jpg`, `ي.jpg`, etc. to `static/signs/`

### 13.2 Debugging Tips

#### Enable Verbose Logging
```python
# app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

#### Check Browser Console
- F12 → Console tab
- Look for JavaScript errors

#### Test Prediction Endpoint
```bash
# Test with curl
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"image": "base64-encoded-image"}'
```

#### Verify Model Loading
```python
# In Python shell
from inference_classifier import SignLanguageClassifier
classifier = SignLanguageClassifier()
print("Model loaded successfully")
```

---

## 14. Future Roadmap

### 14.1 Short-Term (1-3 months)

#### 1. Expand Content
- Add 10 more surahs (short surahs from Juz' Amma)
- Progressive unlocking system

#### 2. User Accounts
- Sign up / Login
- Save progress across sessions
- Personal statistics dashboard

#### 3. Offline Mode
- Service Worker for PWA
- Cache models and assets
- Work without internet

#### 4. Accessibility Improvements
- Screen reader support
- Keyboard navigation
- High contrast mode

### 14.2 Mid-Term (3-6 months)

#### 1. Mobile Native Apps
- Convert to React Native / Flutter
- iOS and Android releases
- Better camera integration

#### 2. Advanced Analytics
- Weekly/Monthly progress reports
- Comparison with other learners
- Personalized recommendations

#### 3. Gamification
- Badge system
- Daily streaks
- Leaderboards
- Challenges

#### 4. Social Features
- Share achievements
- Friend challenges
- Study groups

### 14.3 Long-Term (6-12 months)

#### 1. AI Improvements
- Fine-tune model for specific users
- Multi-hand detection (two-handed signs)
- Temporal modeling (sign sequences)
- Real-time feedback on hand position

#### 2. Expanded Curriculum
- Full Quran coverage (30 Juz')
- Different Quranic recitation styles
- Tajweed rules in sign language

#### 3. Teacher Dashboard
- Create classes
- Assign homework
- Monitor student progress
- Generate reports

#### 4. Video Recording
- Record practice sessions
- Review your own signs
- Get feedback from instructors

### 14.4 Research & Innovation

#### 1. Transformer Models
- Replace Random Forest with deep learning
- Use LSTM/GRU for temporal sequences
- Transfer learning from larger datasets

#### 2. 3D Hand Pose Estimation
- Use depth information
- More accurate z-axis tracking
- Better disambiguation of similar signs

#### 3. Multi-Modal Learning
- Combine hand signs with facial expressions
- Lip reading integration
- Context-aware predictions

---

## 15. Contributing

### 15.1 How to Contribute

We welcome contributions! Here's how:

#### 1. Report Bugs
- Open an issue on GitHub
- Include steps to reproduce
- Add screenshots if applicable

#### 2. Suggest Features
- Open a feature request
- Explain use case
- Provide mockups if possible

#### 3. Submit Code
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests (if applicable)
5. Submit a pull request

### 15.2 Development Guidelines

#### Code Style
```python
# Python: Follow PEP 8
# - Use 4 spaces for indentation
# - Maximum line length: 100 characters
# - Use descriptive variable names

# JavaScript: Follow Airbnb Style Guide
# - Use 2 spaces for indentation
# - Use camelCase for variables
# - Use semicolons
```

#### Commit Messages
```
feat: Add new surah Al-Ikhlas
fix: Correct normalization for hamza
docs: Update installation guide
style: Format code with black
refactor: Simplify error tracking logic
test: Add unit tests for normalization
```

#### Testing
```bash
# Run tests before submitting PR
python -m pytest tests/
```

### 15.3 Project Structure for Contributors

```
tabsirah/
├── md_files/             # Project documentation
├── models/               # Trained AI models
│   ├── hand_landmarker.task   # MediaPipe model
│   └── model_normalized_augmented_LGM.p # Main classifier
├── web_app/              # Main Flask application
│   ├── app.py            # Flask server
│   ├── inference_classifier.py  # AI inference
│   ├── surah_data.py     # Quranic content
│   ├── static/           # Sign images & assets
│   └── templates/        # HTML templates
├── requirements.txt      # Python dependencies
└── README.md            # Project entry pointProject overview
```

---

## 16. License & Credits

### 16.1 License
This project is licensed under the MIT License.

### 16.2 Credits

#### Datasets
- Arabic Sign Language Dataset: Kaggle (public domain)

#### Libraries & Frameworks
- MediaPipe by Google
- Scikit-Learn
- Flask
- Tailwind CSS

#### Fonts
- Cairo by Mohamed Gaber
- Amiri by Khaled Hosny

#### Icons
- Heroicons
- Custom SVG icons

### 16.3 Acknowledgments
- All contributors and testers
- Arabic Sign Language community
- Islamic education community

---

## 17. Contact & Support

### 17.1 Get Help
- **Documentation**: This file
- **Issues**: GitHub Issues
- **Email**: support@tabsirah.com (placeholder)

### 17.2 Community
- **Discord**: [Join our Discord](#) (placeholder)
- **Twitter**: [@tabsirah](#) (placeholder)

### 17.3 Donate
Support the project:
- **PayPal**: [Donate](#) (placeholder)
- **Patreon**: [Become a Patron](#) (placeholder)

---

## Appendix A: API Reference

### Endpoint: `GET /`
- **Description**: Serve main application page
- **Returns**: HTML page
- **Example**: `http://localhost:5000/`

### Endpoint: `GET /get_surahs`
- **Description**: Get all surahs
- **Returns**: JSON object
- **Example Response**:
```json
{
  "al-kawthar": {
    "id": "al-kawthar",
    "name": "سورة الكوثر",
    "verses": ["إنا أعطيناك الكوثر", ...],
    "unlocked": true
  }
}
```

### Endpoint: `GET /get_surah/<surah_id>`
- **Description**: Get specific surah
- **Parameters**: 
  - `surah_id` (path): Surah identifier (e.g., "al-kawthar")
- **Returns**: Surah object
- **Status Codes**:
  - `200`: Success
  - `403`: Surah locked
  - `404`: Surah not found

### Endpoint: `GET /sign_image/<char>`
- **Description**: Get sign image for character
- **Parameters**:
  - `char` (path): Arabic character (URL-encoded)
- **Returns**: JPEG image
- **Example**: `http://localhost:5000/sign_image/ا`

### Endpoint: `POST /predict`
- **Description**: Predict sign from image
- **Headers**: `Content-Type: application/json`
- **Body**:
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQ..."
}
```
- **Returns**:
```json
{
  "prediction": "ا",
  "landmarks": [[{"x": 0.5, "y": 0.3}, ...]]
}
```

---

## Appendix B: Database Schema (Future)

For user accounts and progress tracking:

```sql
-- Users Table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    email VARCHAR(100) UNIQUE,
    created_at TIMESTAMP
);

-- Progress Table
CREATE TABLE progress (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    surah_id VARCHAR(50),
    verse_index INTEGER,
    error_rate FLOAT,
    completed BOOLEAN,
    timestamp TIMESTAMP
);

-- Achievements Table
CREATE TABLE achievements (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    achievement_type VARCHAR(50),
    earned_at TIMESTAMP
);
```

---

## Appendix C: Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Space` | Start/Stop Detection |
| `R` | Restart Current Verse |
| `N` | Next Verse (if completed) |
| `Esc` | Back to Home |
| `S` | Toggle Surah Selection |

*(To be implemented)*

---

## Changelog

### Version 2.0 (January 2026)
- ✨ Added Recitation Mode with error tracking
- ✨ Implemented correction overlay
- ✨ Added "Practice Errors" feature
- 🎨 Complete UI redesign with brand colors
- 🐛 Fixed Arabic character normalization
- 🐛 Fixed camera and model issues
- 🐛 Fixed responsive design issues
- 📱 Improved mobile experience
- 🌍 Full Arabic localization

### Version 1.0 (December 2025)
- 🎉 Initial release
- ✨ Basic sign language detection
- ✨ Surah training mode
- ✨ Reference card system

---

**Document Version**: 2.0  
**Last Updated**: January 20, 2026  
**Maintained By**: Tabsirah Development Team

---

*May this project bring benefit to learners of the Holy Quran. Ameen.*
