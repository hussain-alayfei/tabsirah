import os
import warnings

# Suppress annoying warnings BEFORE importing other libraries
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
os.environ['GLOG_minloglevel'] = '2'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' # Suppress TensorFlow INFO/WARNING
warnings.filterwarnings("ignore", category=UserWarning, module='google.protobuf')
warnings.filterwarnings("ignore", message=".*'force_all_finite' was renamed to 'ensure_all_finite'.*")

from flask import Flask, render_template, request, jsonify, send_file, abort
from inference_classifier import SignLanguageClassifier
from surah_data import get_all_surahs, get_surah, is_surah_unlocked
import cv2
import numpy as np
import base64
import glob
from urllib.parse import unquote
import re

app = Flask(__name__)
# Ensure Arabic characters are not escaped in JSON
app.config['JSON_AS_ASCII'] = False

# ==========================
# Initialize classifier
# ==========================
try:
    classifier = SignLanguageClassifier()
    print("Model loaded successfully.")
except Exception as e:
    print(f"Error loading model: {e}")
    classifier = None


# ==========================
# Routes
# ==========================
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_surahs')
def get_surahs_route():
    """Return all surahs with metadata."""
    try:
        surahs = get_all_surahs()
        return jsonify(surahs)
    except Exception as e:
        print(f"Error fetching surahs: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/get_surah/<surah_id>')
def get_surah_route(surah_id):
    """
    Get a specific surah by ID.
    403 if locked, 404 if not found.
    """
    try:
        surah = get_surah(surah_id)

        if not surah:
            return jsonify({'error': 'Surah not found'}), 404

        if not is_surah_unlocked(surah_id):
            return jsonify({'error': 'Surah is locked'}), 403

        return jsonify(surah)
    except Exception as e:
        print(f"Error fetching surah {surah_id}: {e}")
        return jsonify({'error': str(e)}), 500


# ==========================
# Helper: normalize char name
# ==========================
def normalize_char_for_image(char: str) -> str:
    """Normalize Arabic character for image lookup."""
    if not char:
        return char

    # تطبيع الألف: أ، إ، آ، ء، ٱ → ا
    char = (
        char.replace('أ', 'ا')
            .replace('إ', 'ا')
            .replace('آ', 'ا')
            .replace('ء', 'ا')
            .replace('ٱ', 'ا')
    )

    # تطبيع الياء: ى، ئ → ي
    char = char.replace('ى', 'ي').replace('ئ', 'ي')

    # تطبيع التاء المربوطة: ة → ه
    char = char.replace('ة', 'ه')

    # إزالة التشكيل
    char = re.sub(r'[\u064B-\u065F\u0670]', '', char)

    return char


@app.route('/sign_image/<path:char>')
def get_sign_image(char):
    """
    Dynamic Image Selector for static/signs/.
    Returns last matching JPG for a given normalized character.
    """
    try:
        static_folder = os.path.join(app.static_folder, 'signs')

        # decode URL-encoded char and normalize
        char = unquote(char)
        normalized_char = normalize_char_for_image(char)

        # Priority 1: exact match
        exact_path = os.path.join(static_folder, f"{normalized_char}.jpg")
        if os.path.exists(exact_path):
            return send_file(exact_path, mimetype='image/jpeg')

        # Priority 2: any file starting with normalized_char
        pattern = os.path.join(static_folder, f"{normalized_char}*.jpg")
        matches = glob.glob(pattern)

        if not matches:
            return abort(404)

        matches.sort()
        last_image = matches[-1]
        return send_file(last_image, mimetype='image/jpeg')

    except Exception:
        return abort(404)


# ==========================
# Prediction endpoint
# ==========================
@app.route('/predict', methods=['POST'])
def predict():
    if not classifier:
        return jsonify({'error': 'Model not loaded', 'prediction': None, 'landmarks': []}), 200

    try:
        if not request.is_json:
            return jsonify({'error': 'No JSON data', 'prediction': None, 'landmarks': []}), 200

        json_data = request.get_json(silent=True)
        if not json_data or 'image' not in json_data:
            return jsonify({'error': 'No image data', 'prediction': None, 'landmarks': []}), 200

        data = json_data['image']

        # Data URL "data:image/jpeg;base64,..." -> keep only base64
        if ',' in data:
            _, encoded = data.split(',', 1)
        else:
            encoded = data

        try:
            binary = base64.b64decode(encoded)
        except Exception:
            return jsonify({'error': 'Invalid base64', 'prediction': None, 'landmarks': []}), 200

        image_array = np.frombuffer(binary, dtype=np.uint8)
        frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

        if frame is None:
            return jsonify({'error': 'Failed to decode image', 'prediction': None, 'landmarks': []}), 200

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # classify
        label, detection_result = classifier.predict(frame_rgb)

        # serialize landmarks for debugging / overlay
        landmarks_data = []
        if detection_result and detection_result.hand_landmarks:
            for hand_landmarks in detection_result.hand_landmarks:
                hand_points = [{'x': lm.x, 'y': lm.y} for lm in hand_landmarks]
                landmarks_data.append(hand_points)

        return jsonify({
            'prediction': label if label is not None else None,
            'landmarks': landmarks_data
        })

    except Exception as e:
        return jsonify({'error': str(e), 'prediction': None, 'landmarks': []}), 200


if __name__ == '__main__':
    print("\n✅ Server is ready! Access it at: http://127.0.0.1:5000/")
    app.run(debug=True)
