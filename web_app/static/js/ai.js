import { FilesetResolver, HandLandmarker } from "https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0";
import { state } from "./state.js";
import { drawHandLandmarks } from "./ui.js"; // Circular dependency potential, careful
import { predictCharacter } from "./api.js";
import { checkGameLogic } from "./game.js";

// Initialize AI
export async function initAI() {
    try {
        const vision = await FilesetResolver.forVisionTasks("https://cdn.jsdelivr.net/npm/@mediapipe/tasks-vision@0.10.0/wasm");
        state.handLandmarker = await HandLandmarker.createFromOptions(vision, {
            baseOptions: {
                modelAssetPath: `https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task`,
                delegate: "GPU"
            },
            runningMode: state.runningMode,
            numHands: 2,
            minHandDetectionConfidence: 0.5,
            minHandPresenceConfidence: 0.5,
            minTrackingConfidence: 0.5
        });
        startCamera();
    } catch (e) {
        console.error("AI Init Failed:", e);
        alert("Could not load AI model. Please refresh.");
    }
}

export function startCamera() {
    // Detect if mobile device
    const isMobile = /iPhone|iPad|iPod|Android/i.test(navigator.userAgent);

    const videoConstraints = isMobile ? {
        facingMode: "user",
        width: { ideal: 720 },
        height: { ideal: 1280 },
        frameRate: { ideal: 30 }
    } : {
        width: { ideal: 1280 },
        height: { ideal: 720 },
        frameRate: { ideal: 60 }
    };

    navigator.mediaDevices.getUserMedia({
        video: videoConstraints
    }).then((stream) => {
        state.video.srcObject = stream;
        state.video.addEventListener("loadeddata", predictWebcam);
    }).catch(e => {
        console.error("Camera denied:", e);
        alert("Camera access denied. Please allow camera access.");
    });
}

export async function predictWebcam() {
    // Check coverage - optimization
    const app = document.getElementById('appView');
    if (!app || app.style.display === 'none') {
        requestAnimationFrame(predictWebcam);
        return;
    }

    // PAUSE CHECK
    if (state.pauseDetection) {
        requestAnimationFrame(predictWebcam);
        return;
    }

    // Setup Canvas Dimensions
    if (state.video.videoWidth > 0 && state.overlay.width !== state.video.videoWidth) {
        state.overlay.width = state.video.videoWidth;
        state.overlay.height = state.video.videoHeight;
        document.getElementById("cameraWrapper").style.aspectRatio = `${state.video.videoWidth}/${state.video.videoHeight}`;
    }

    if (state.handLandmarker && state.video.currentTime !== state.lastVideoTime) {
        state.lastVideoTime = state.video.currentTime;
        let startTimeMs = performance.now();
        const results = state.handLandmarker.detectForVideo(state.video, startTimeMs);

        state.ctx.save();
        state.ctx.clearRect(0, 0, state.overlay.width, state.overlay.height);

        if (results.landmarks && results.landmarks.length > 0) {
            // Draw Landmarks
            drawHandLandmarks(results.landmarks, state.overlay.width, state.overlay.height);

            // Prediction Throttling
            const now = Date.now();
            if (state.gameActive && (now - state.lastPredictionTime > state.PREDICTION_INTERVAL)) {
                state.lastPredictionTime = now;

                // Get prediction from backend
                const predictedChar = await predictCharacter(state.video, results.landmarks);

                // Update UI with prediction
                state.predVal.innerText = predictedChar || "-";

                // Check Game Logic
                checkGameLogic(predictedChar);
            }
        } else {
            // No hands detected
            state.predVal.innerText = '-';
            state.predVal.classList.remove('text-green-500', 'text-red-500');
            state.predVal.classList.add('text-blue-600');
        }
        state.ctx.restore();
    }

    requestAnimationFrame(predictWebcam);
}
