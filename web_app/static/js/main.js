import { state, resetGameState } from "./state.js";
import { initAI, startCamera, predictWebcam } from "./ai.js";
import { fetchSurahs, fetchSurah } from "./api.js";
import {
    startGameLogic,
    endGame,
    handleSuccess,
    onVerseComplete,
    checkGameLogic
} from "./game.js";
import {
    renderCards,
    updateCardStyles,
    updateCurrentWord,
    showSuccessFlash,
    showCorrectionOverlay,
    showSurahFinalResults,
    updateVerseProgress,
    markWordComplete
} from "./ui.js";
import { generateAnalytics } from "./analytics.js";

// ============================================
// MAIN INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', () => {
    // Initialize DOM references in state
    state.video = document.getElementById("videoElement");
    state.overlay = document.getElementById("overlayCanvas");
    state.ctx = state.overlay.getContext("2d");
    state.predVal = document.getElementById("predVal");

    // Initialize global event listeners/exposures
    attachGlobalFunctions();
});

function attachGlobalFunctions() {
    // Expose functions to window because inline HTML onclicks need them

    // Navigation
    window.openApp = function () {
        const landing = document.getElementById('landingView');
        const app = document.getElementById('appView');

        landing.style.display = 'none';
        app.style.display = 'flex';
        app.classList.remove('hidden');

        if (!state.video.srcObject) {
            initAI();
        }
    };

    window.closeApp = function () {
        const landing = document.getElementById('landingView');
        const app = document.getElementById('appView');

        app.style.display = 'none';
        landing.style.display = 'flex';

        resetGameState();
        state.gameActive = false;
        state.pauseDetection = false;
    };

    window.selectTrainingMode = function () {
        state.recitationMode = false;
        state.surahMode = true;

        document.getElementById('landingView').style.display = 'none';
        document.getElementById('surahSelectionView').style.display = 'flex';
        document.getElementById('surahSelectionView').classList.remove('hidden');
        document.querySelector('#surahSelectionView h1').innerText = 'اختر السورة للتدريب';

        loadSurahsToGrid();
    };

    window.selectFreePracticeMode = function () {
        state.recitationMode = true;
        state.surahMode = true;

        resetGameState();
        state.recitationMode = true; // Ensure it stays true after reset
        state.surahMode = true;

        document.getElementById('landingView').style.display = 'none';
        document.getElementById('surahSelectionView').style.display = 'flex';
        document.getElementById('surahSelectionView').classList.remove('hidden');
        document.querySelector('#surahSelectionView h1').innerText = 'اختر السورة للتسميع';

        loadSurahsToGrid();
    };

    window.backToLanding = function () {
        document.getElementById('surahSelectionView').style.display = 'none';
        document.getElementById('landingView').style.display = 'flex';
    };

    window.backToSurahSelection = function () {
        document.getElementById('videoChoiceView').style.display = 'none';
        document.getElementById('surahSelectionView').style.display = 'flex';
    };

    // Game Control
    window.startGame = () => {
        const input = document.getElementById('gameInput').value.trim();
        if (!input) return;

        startGameLogic(input);

        // Reset analytics specific
        state.mistakes = [];
        state.letterStats = {};
        state.totalAttempts = 0;

        renderCards();
        document.getElementById('gameInput').value = "";
    };

    window.restartGame = () => {
        state.gameActive = false;
        state.pauseDetection = false;

        resetGameState();

        // UI Reset
        document.getElementById('scoreValue').innerText = '0';
        state.predVal.innerText = '-';
        state.predVal.classList.remove('text-green-500', 'text-red-500');
        state.predVal.classList.add('text-blue-600');
        document.getElementById('gameInput').value = '';
        document.getElementById('cardsTrack').innerHTML = '';
        document.getElementById('cardsTrack').classList.remove('hidden');
        document.getElementById('letterErrorCounter').classList.add('hidden');
        document.getElementById('verseProgressDisplay').classList.add('hidden');
        document.getElementById('scoreDisplay').classList.remove('hidden');
        state.lastWrongPrediction = null;
        document.getElementById('currentWordDisplay').classList.add('hidden');
    };

    // Overlays
    window.closeSummary = () => {
        document.getElementById('summaryOverlay').classList.add('hidden');
    };

    window.showAnalytics = () => {
        document.getElementById('summaryOverlay').classList.add('hidden');
        document.getElementById('loadingOverlay').classList.remove('hidden');

        setTimeout(() => {
            document.getElementById('loadingOverlay').classList.add('hidden');
            generateAnalytics();
            document.getElementById('analyticsOverlay').classList.remove('hidden');
        }, 2000);
    };

    window.closeAnalytics = () => {
        document.getElementById('analyticsOverlay').classList.add('hidden');
    };

    // Surah Specifics
    window.showVideoPlayer = function () {
        document.getElementById('videoChoiceView').style.display = 'none';
        document.getElementById('videoPlayerView').style.display = 'flex';
        document.getElementById('videoPlayerView').classList.remove('hidden');
        document.getElementById('videoPlayerTitle').innerText = state.currentSurah.name + ' - الشرح التعليمي';

        const iframe = document.getElementById('youtubePlayer');
        iframe.src = state.currentSurah.video_url || '';
    };

    window.backToVideoChoice = function () {
        document.getElementById('videoPlayerView').style.display = 'none';
        document.getElementById('videoChoiceView').style.display = 'flex';
    };

    window.startDirectTraining = function () {
        document.getElementById('videoChoiceView').style.display = 'none';
        startSurahTraining();
    };

    window.startTrainingAfterVideo = function () {
        document.getElementById('videoPlayerView').style.display = 'none';
        startSurahTraining();
    };

    // Correction Overlay Actions
    window.skipLetter = function () {
        document.getElementById('correctionOverlay').classList.add('hidden');

        // Visual skip
        const card = document.getElementById(`c-${state.currentTargetIndex}`);
        if (card) {
            card.classList.add('border-orange-500', 'bg-orange-50');
            const letterDisplay = document.getElementById(`letter-${state.currentTargetIndex}`);
            if (letterDisplay) {
                letterDisplay.className = 'text-2xl font-black text-orange-500 mt-1 quran-text';
            }
        }

        state.currentTargetIndex++;
        while (state.currentTargetIndex < state.targetSentence.length && state.targetSentence[state.currentTargetIndex] === ' ') {
            state.currentTargetIndex++;
        }

        if (state.currentTargetIndex >= state.targetSentence.length) {
            onVerseComplete();
        } else {
            state.gameActive = true;
            state.pauseDetection = false;
            updateCardStyles();
            updateCurrentWord();
            state.currentLetterStartTime = Date.now();

            const next = document.getElementById(`c-${state.currentTargetIndex}`);
            if (next) {
                next.scrollIntoView({ behavior: 'smooth', inline: 'center' });
            }
        }
    };

    window.retryLetter = function () {
        document.getElementById('correctionOverlay').classList.add('hidden');
        state.letterErrorCount[state.currentTargetIndex] = 0;
        state.gameActive = true;
        state.pauseDetection = false;
    };

    // Results Actions
    window.backToSurahSelectionFromResults = function () {
        document.getElementById('summaryOverlay').classList.add('hidden');
        document.getElementById('analyticsOverlay').classList.add('hidden');
        document.getElementById('appView').style.display = 'none';
        document.getElementById('surahSelectionView').style.display = 'flex';
        document.getElementById('surahSelectionView').classList.remove('hidden');

        window.restartGame();

        document.getElementById('backToSurahSelectionBtn').classList.add('hidden');
        document.getElementById('practiceErrorsBtn').classList.add('hidden');
    };

    window.startPracticeErrors = function () {
        if (state.failedVerses.length === 0) {
            alert('لا توجد آيات تحتاج مراجعة!');
            return;
        }

        document.getElementById('summaryOverlay').classList.add('hidden');

        const originalVerses = state.currentSurah.verses.slice();
        state.currentSurah.verses = state.failedVerses.map(fv => fv.verse);

        state.currentVerseIndex = 0;
        state.letterErrorCount = {};
        state.verseResults = [];
        state.failedVerses = [];
        state.mistakes = [];
        state.letterStats = {};

        startVerseTraining();

        state.currentSurah._originalVerses = originalVerses;
        state.currentSurah._isPracticeErrors = true;
    };

    // We also need to expose startVerseTraining for recursion in game.js via window if we didn't export it
    // But since game.js needs it too, we define it here and attach
    window.startVerseTrainingGlobal = startVerseTraining;
}

// Helper to load surahs into the grid
async function loadSurahsToGrid() {
    const surahs = await fetchSurahs();
    const grid = document.getElementById('surahGrid');
    grid.innerHTML = '';

    for (const [id, surah] of Object.entries(surahs)) {
        const card = createSurahCard(id, surah);
        grid.appendChild(card);
    }
}

// UI Factory for Surah Card
function createSurahCard(id, surah) {
    const div = document.createElement('div');
    const isLocked = !surah.unlocked;
    const versesCount = surah.verses ? surah.verses.length : 0;

    div.className = `group flex items-center justify-between p-5 transition-all hover:bg-slate-50 ${isLocked ? 'cursor-not-allowed opacity-75' : 'cursor-pointer'}`;

    div.innerHTML = `
        <div class="flex items-center gap-4">
            <div class="relative w-12 h-12 flex items-center justify-center flex-shrink-0">
                <svg viewBox="0 0 24 24" class="absolute w-full h-full ${isLocked ? 'text-slate-300' : 'text-blue-500'} drop-shadow-sm" fill="currentColor">
                    <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /> 
                </svg>
                <span class="relative text-white font-bold text-sm pt-1 font-sans">${surah.number || '0'}</span>
            </div>
            
            <div class="text-right">
                <h3 class="text-lg font-bold text-slate-800 font-arabic group-hover:text-blue-600 transition-colors">${surah.name}</h3>
                <div class="flex items-center gap-2 text-xs text-slate-400 font-arabic mt-0.5">
                    <span>${versesCount} آيات</span>
                    <span>•</span>
                    <span>صفحة 1</span>
                </div>
            </div>
        </div>

        <div>
            ${isLocked
            ? `<span class="bg-slate-100 text-slate-400 text-[10px] font-bold px-3 py-1.5 rounded-full border border-slate-200">قريباً</span>`
            : `<svg class="w-5 h-5 text-slate-300 group-hover:text-blue-500 transition-colors transform group-hover:-translate-x-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
                    </svg>`
        }
        </div>
    `;

    if (!isLocked) {
        div.onclick = () => selectSurah(id);
    }

    return div;
}

// Selecting a surah
async function selectSurah(surahId) {
    try {
        const surah = await fetchSurah(surahId);

        state.currentSurah = surah;
        state.currentVerseIndex = 0;
        state.surahMode = true;

        document.getElementById('surahSelectionView').style.display = 'none';

        if (state.recitationMode) {
            state.letterErrorCount = {};
            state.verseErrorCounts = [];
            state.verseResults = [];
            startSurahTraining();
        } else {
            document.getElementById('videoChoiceView').style.display = 'flex';
            document.getElementById('videoChoiceView').classList.remove('hidden');
            document.getElementById('videoChoiceTitle').innerText = state.currentSurah.name;
        }
    } catch (e) {
        alert('حدث خطأ في تحميل السورة');
    }
}

// Logic to start Verse Training (orchestrator)
function startSurahTraining() {
    document.getElementById('appView').style.display = 'flex';
    document.getElementById('appView').classList.remove('hidden');
    document.getElementById('freePracticeInput').classList.add('hidden');

    if (!state.video.srcObject) {
        initAI();
    }

    startVerseTraining();
}

function startVerseTraining() {
    if (!state.currentSurah || state.currentVerseIndex >= state.currentSurah.verses.length) {
        return;
    }

    const verse = state.currentSurah.verses[state.currentVerseIndex];
    state.targetSentence = verse;
    state.currentTargetIndex = 0;
    state.score = 0;
    state.verseStartTime = Date.now();
    state.verseMistakes = [];
    state.consecutiveCorrect = 0;
    state.letterErrorCount = {};

    document.getElementById('scoreValue').innerText = '0';

    const cardsTrack = document.getElementById('cardsTrack');
    const letterErrorCounter = document.getElementById('letterErrorCounter');
    const verseProgressDisplay = document.getElementById('verseProgressDisplay');
    const scoreDisplay = document.getElementById('scoreDisplay');

    if (state.recitationMode) {
        cardsTrack.classList.add('hidden');
        letterErrorCounter.classList.remove('hidden');
        document.getElementById('letterErrorCount').innerText = '0/10';
        verseProgressDisplay.classList.remove('hidden');
        scoreDisplay.classList.add('hidden');
        updateVerseProgress();
    } else {
        cardsTrack.classList.remove('hidden');
        letterErrorCounter.classList.add('hidden');
        verseProgressDisplay.classList.add('hidden');
        scoreDisplay.classList.remove('hidden');
    }

    state.lastWrongPrediction = null;

    renderCards();

    state.gameActive = true;
    state.startTime = Date.now();
    state.currentLetterStartTime = Date.now();
    state.pauseDetection = false;
}
