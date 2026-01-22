import { state } from "./state.js";
import { areCharsEquivalent } from "./utils.js";
import {
    updateCardStyles,
    updateCurrentWord,
    markWordComplete,
    showCorrectionOverlay,
    showSuccessFlash,
    showSurahFinalResults
} from "./ui.js";

// Check prediction against target
export function checkGameLogic(prediction) {
    if (!state.gameActive || !state.targetSentence) return;

    // Skip spaces
    if (state.targetSentence[state.currentTargetIndex] === ' ') {
        state.currentTargetIndex++;
        if (state.currentTargetIndex >= state.targetSentence.length) {
            onVerseComplete();
            return;
        }
    }

    const targetChar = state.targetSentence[state.currentTargetIndex];
    const isCorrect = areCharsEquivalent(prediction, targetChar);

    if (isCorrect) {
        // --- CORRECT ---
        state.consecutiveCorrect++;

        // Show green feedback
        state.predVal.classList.remove('text-blue-600', 'text-red-500');
        state.predVal.classList.add('text-green-500');

        state.lastWrongPrediction = null;

        // Advance after REQUIRED_CONSECUTIVE correct detections
        if (state.consecutiveCorrect >= state.REQUIRED_CONSECUTIVE) {
            state.consecutiveCorrect = 0;
            handleSuccess();
        }
    } else {
        // --- INCORRECT ---
        state.consecutiveCorrect = 0;
        state.predVal.classList.remove('text-green-500', 'text-blue-600');
        state.predVal.classList.add('text-red-500');

        // Avoid counting same wrong prediction multiple times
        if (prediction === state.lastWrongPrediction) {
            return;
        }
        state.lastWrongPrediction = prediction;

        // Track mistake
        state.totalAttempts++;
        const currentLetter = targetChar;
        if (!state.letterStats[currentLetter]) {
            state.letterStats[currentLetter] = { correct: 0, wrong: 0, totalTime: 0 };
        }
        state.letterStats[currentLetter].wrong++;

        state.mistakes.push({
            letter: currentLetter,
            predicted: prediction,
            timestamp: Date.now() - state.startTime
        });

        // RECITATION MODE specifics
        if (state.recitationMode) {
            if (!state.letterErrorCount[state.currentTargetIndex]) {
                state.letterErrorCount[state.currentTargetIndex] = 0;
            }
            state.letterErrorCount[state.currentTargetIndex]++;

            // Update error counter UI
            const errorCounter = document.getElementById('letterErrorCount');
            if (errorCounter) errorCounter.innerText = `${state.letterErrorCount[state.currentTargetIndex]}/${state.MAX_ATTEMPTS_PER_LETTER}`;

            if (state.letterErrorCount[state.currentTargetIndex] >= state.MAX_ATTEMPTS_PER_LETTER) {
                showCorrectionOverlay(currentLetter);
            }
        }
    }
}

export function handleSuccess() {
    if (state.pauseDetection) return;
    state.pauseDetection = true;

    state.totalAttempts++;
    const currentLetter = state.targetSentence[state.currentTargetIndex];
    if (!state.letterStats[currentLetter]) {
        state.letterStats[currentLetter] = { correct: 0, wrong: 0, totalTime: 0 };
    }
    state.letterStats[currentLetter].correct++;

    if (state.currentLetterStartTime > 0) {
        const letterTime = Date.now() - state.currentLetterStartTime;
        state.letterStats[currentLetter].totalTime += letterTime;
    }

    // UI Updates
    state.score += 10;
    document.getElementById('scoreValue').innerText = state.score;

    state.predVal.classList.remove('text-blue-600', 'text-red-500');
    state.predVal.classList.add('text-green-500', 'scale-110');

    if (state.recitationMode) {
        showSuccessFlash();
    }

    // Highlight Card
    const card = document.getElementById(`c-${state.currentTargetIndex}`);
    if (card) {
        const letterDisplay = document.getElementById(`letter-${state.currentTargetIndex}`);
        if (letterDisplay) {
            letterDisplay.className = 'text-2xl font-black text-green-500 mt-1 quran-text';
            letterDisplay.style.fontFamily = "'Amiri', 'Arabic Typesetting', 'Traditional Arabic', serif";
        }
        card.classList.add('border-green-500', 'bg-green-50', 'ring-2', 'ring-green-200');
    }

    updateCurrentWord();

    // Advance Logic
    setTimeout(() => {
        state.predVal.classList.remove('scale-110');

        if (card) {
            card.classList.remove('ring-2', 'ring-green-200', 'scale-105');
            card.className = 'flex-shrink-0 w-28 h-40 bg-green-50 rounded-xl border border-green-400 flex flex-col items-center justify-between py-2 px-2 transition-all duration-500 transform scale-90 opacity-40';
        }

        state.currentTargetIndex++;

        // Reset error counter for new letter
        if (state.recitationMode) {
            const currentErrors = state.letterErrorCount[state.currentTargetIndex] || 0;
            const el = document.getElementById('letterErrorCount');
            if (el) el.innerText = `${currentErrors}/10`;
        }

        // Check for SPACE
        if (state.currentTargetIndex < state.targetSentence.length && state.targetSentence[state.currentTargetIndex] === ' ') {
            markWordComplete(state.currentTargetIndex - 1);
            updateCurrentWord();
            state.currentTargetIndex++; // Skip space
            if (state.recitationMode) {
                const currentErrors = state.letterErrorCount[state.currentTargetIndex] || 0;
                const el = document.getElementById('letterErrorCount');
                if (el) el.innerText = `${currentErrors}/10`;
            }
        }

        // Check for End of Sentence/Verse
        if (state.currentTargetIndex >= state.targetSentence.length) {
            markWordComplete(state.currentTargetIndex - 1);

            if (state.surahMode && state.currentSurah) {
                setTimeout(onVerseComplete, 1000);
            } else {
                // For custom definition of endGame, we assume it's exposed or we import it if it was a module
                // But logic is effectively finishing the session
                setTimeout(endGame, 1000);
            }
        } else {
            const next = document.getElementById(`c-${state.currentTargetIndex}`);
            if (next) {
                next.scrollIntoView({ behavior: 'smooth', inline: 'center' });
                updateCardStyles();
                state.currentLetterStartTime = Date.now();
            }
        }

        state.pauseDetection = false;
    }, 800);
}

// Logic for Verse Completion
export function onVerseComplete() {
    state.gameActive = false;

    if (state.recitationMode) {
        const verseLetterCount = state.targetSentence.replace(/\s/g, '').length;
        let lettersWithErrors = 0;
        let totalAttemptErrors = 0;

        for (let idx in state.letterErrorCount) {
            if (state.letterErrorCount[idx] > 0) {
                lettersWithErrors++;
                totalAttemptErrors += state.letterErrorCount[idx];
            }
        }

        const verseErrorRate = verseLetterCount > 0 ? (lettersWithErrors / verseLetterCount) * 100 : 0;

        state.verseResults.push({
            verse: state.targetSentence,
            verseIndex: state.currentVerseIndex,
            errorRate: verseErrorRate,
            lettersWithErrors: lettersWithErrors,
            totalAttemptErrors: totalAttemptErrors,
            totalLetters: verseLetterCount,
            passed: verseErrorRate <= state.VERSE_FAILURE_THRESHOLD
        });

        if (verseErrorRate > state.VERSE_FAILURE_THRESHOLD) {
            state.failedVerses.push({
                verse: state.targetSentence,
                verseIndex: state.currentVerseIndex,
                errorRate: verseErrorRate
            });
        }
    }

    document.getElementById('congratsOverlay').classList.remove('hidden');

    setTimeout(() => {
        document.getElementById('congratsOverlay').classList.add('hidden');
        state.currentVerseIndex++;

        if (state.currentVerseIndex < state.currentSurah.verses.length) {
            // We need to trigger next verse training. 
            // Since this is circular setup, UI should expose a function or we dispatch event
            // But for now, we will assume we can set state and UI refreshes or we need to export startVerseTraining logic separately
            // Let's rely on an exported function reference that we can call
            if (window.startVerseTrainingGlobal) window.startVerseTrainingGlobal();
        } else {
            showSurahFinalResults();
        }
    }, 800);
}

export function endGame() {
    state.gameActive = false;
    const dur = ((Date.now() - state.startTime) / 1000).toFixed(1);
    document.getElementById('sumScore').innerText = state.score;
    document.getElementById('sumTime').innerText = dur + "s";
    document.getElementById('completedSentence').innerText = state.targetSentence;
    document.getElementById('summaryOverlay').classList.remove('hidden');
}

export function startGameLogic(inputSentence) {
    if (!inputSentence) return;
    state.targetSentence = inputSentence;
    state.score = 0;
    document.getElementById('scoreValue').innerText = 0;
    state.currentTargetIndex = 0;
    state.gameActive = true;
    state.startTime = Date.now();
    state.currentLetterStartTime = Date.now();

    state.mistakes = [];
    state.letterStats = {};
    state.totalAttempts = 0;
}
