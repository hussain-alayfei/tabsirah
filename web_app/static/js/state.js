// ============================================
// STATE
// ============================================

export const state = {
    // AI & Camera
    handLandmarker: undefined,
    runningMode: "VIDEO",

    // DOM Elements (will be populated in main)
    video: null,
    overlay: null,
    ctx: null,
    predVal: null,

    // Game Props
    lastVideoTime: -1,
    lastPredictionTime: 0,
    PREDICTION_INTERVAL: 100,

    targetSentence: "",
    currentTargetIndex: 0,
    score: 0,
    startTime: 0,
    gameActive: false,
    pauseDetection: false,

    // Consecutive correct detections required before advancing
    consecutiveCorrect: 0,
    REQUIRED_CONSECUTIVE: 3,

    // Track last wrong prediction to avoid counting repetitive same-letter errors
    lastWrongPrediction: null,

    // Analytics tracking
    mistakes: [], // Array of {letter: 'ب', attempts: 3, timestamp: ...}
    letterStats: {}, // {letter: {correct: 0, wrong: 0, totalTime: 0}}
    currentLetterStartTime: 0,
    totalAttempts: 0,

    // RECITATION MODE STATE
    recitationMode: false,
    letterErrorCount: {},
    verseErrorCounts: [],
    failedVerses: [],
    verseResults: [],
    MAX_ATTEMPTS_PER_LETTER: 10,
    VERSE_FAILURE_THRESHOLD: 40,

    // Surah training state
    currentSurah: null,
    currentVerseIndex: 0,
    surahMode: false,
    verseStartTime: 0,
    verseMistakes: []
};

// Helper to reset game state
export function resetGameState() {
    state.targetSentence = "";
    state.currentTargetIndex = 0;
    state.score = 0;
    state.startTime = 0;
    state.currentLetterStartTime = 0;
    state.mistakes = [];
    state.letterStats = {};
    state.totalAttempts = 0;
    state.recitationMode = false;
    state.letterErrorCount = {};
    state.verseErrorCounts = [];
    state.failedVerses = [];
    state.verseResults = [];

    if (state.surahMode) {
        state.currentSurah = null;
        state.currentVerseIndex = 0;
        state.surahMode = false;
    }
}
