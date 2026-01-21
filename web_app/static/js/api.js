import { state } from "./state.js";

// Send landmarks to backend for prediction
export async function predictCharacter(videoElement, landmarks) {
    // 1. Snapshot
    const canvas = document.createElement('canvas');
    canvas.width = videoElement.videoWidth;
    canvas.height = videoElement.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/jpeg', 0.8);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                image: dataURL,
                landmarks: landmarks
            })
        });
        const data = await response.json();
        return data.prediction;
    } catch (e) {
        console.error('Prediction error:', e);
        return null;
    }
}

// Fetch all surahs
export async function fetchSurahs() {
    try {
        const response = await fetch('/get_surahs');
        return await response.json();
    } catch (e) {
        console.error('Error loading surahs:', e);
        return {};
    }
}

// Fetch specific surah
export async function fetchSurah(id) {
    try {
        const response = await fetch(`/get_surah/${id}`);
        if (!response.ok) throw new Error('Surah not available');
        return await response.json();
    } catch (e) {
        console.error('Error selecting surah:', e);
        throw e;
    }
}
