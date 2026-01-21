import { state } from "./state.js";

// ============================================
// UI RENDERING
// ============================================

export function renderCards() {
    const track = document.getElementById('cardsTrack');
    track.innerHTML = "";

    const words = state.targetSentence.split(' ');
    let charIndex = 0;

    words.forEach((word, wordIdx) => {
        for (let i = 0; i < word.length; i++) {
            const char = word[i];
            const c = document.createElement('div');

            c.className = `flex-shrink-0 w-28 h-40 bg-white rounded-xl border-2 flex flex-col items-center justify-between py-2 px-2 transition-all duration-500 ease-[cubic-bezier(0.34,1.56,0.64,1)] transform ${charIndex === 0 ? 'border-blue-500 scale-105 opacity-100 shadow-lg' : 'border-slate-100 scale-95 opacity-50'}`;
            c.id = 'c-' + charIndex;
            c.setAttribute('data-word', word);
            c.setAttribute('data-word-index', i);

            const img = document.createElement('img');
            img.src = `/sign_image/${encodeURIComponent(char)}`;
            img.className = 'w-24 h-24 object-contain mix-blend-multiply flex-shrink-0';
            img.onerror = function () { this.style.opacity = '0.3'; };
            c.appendChild(img);

            const s = document.createElement('span');
            s.innerText = char;
            s.className = 'text-2xl font-black text-blue-600 mt-1 quran-text';
            s.id = `letter-${charIndex}`;
            c.appendChild(s);

            track.appendChild(c);
            charIndex++;
        }

        if (wordIdx < words.length - 1) {
            const spacer = document.createElement('div');
            spacer.className = 'flex-shrink-0 w-4 h-40 bg-transparent flex items-center justify-center';
            spacer.id = 'c-' + charIndex;
            spacer.innerHTML = '<span class="text-slate-300 text-lg opacity-30">•</span>';
            track.appendChild(spacer);
            charIndex++;
        }
    });

    track.scrollLeft = track.scrollWidth;
    updateCurrentWord();
}

export function updateCurrentWord() {
    const card = document.getElementById(`c-${state.currentTargetIndex}`);
    if (!card) return;

    const word = card.getAttribute('data-word');
    if (!word) {
        document.getElementById('currentWordDisplay').classList.add('hidden');
        return;
    }

    document.getElementById('currentWordDisplay').classList.remove('hidden');
    const wordIndex = parseInt(card.getAttribute('data-word-index') || '0');

    // Canvas rendering for connected Arabic text
    const canvas = document.getElementById('arabicWordCanvas');
    const ctx = canvas.getContext('2d');

    const dpr = window.devicePixelRatio || 1;
    const fontSize = 42;
    const fontFamily = "'Noto Naskh Arabic', 'Geeza Pro', 'SF Arabic', -apple-system, sans-serif";

    ctx.font = `bold ${fontSize}px ${fontFamily}`;
    const textMetrics = ctx.measureText(word);
    const textWidth = textMetrics.width;

    const padding = 20;
    canvas.width = (textWidth + padding * 2) * dpr;
    canvas.height = 70 * dpr;
    canvas.style.width = (textWidth + padding * 2) + 'px';
    canvas.style.height = '70px';
    ctx.scale(dpr, dpr);

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    ctx.font = `bold ${fontSize}px ${fontFamily}`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.direction = 'rtl';

    const centerX = (textWidth + padding * 2) / 2;
    const centerY = 35;

    const letterWidths = [];
    for (let i = 0; i < word.length; i++) {
        letterWidths.push(ctx.measureText(word[i]).width);
    }

    const totalMeasuredWidth = letterWidths.reduce((a, b) => a + b, 0);
    const scale = textWidth / totalMeasuredWidth;

    const rightEdge = centerX + textWidth / 2;

    const letterBoundaries = [rightEdge];
    let pos = rightEdge;
    for (let i = 0; i < word.length; i++) {
        pos -= letterWidths[i] * scale;
        letterBoundaries.push(pos);
    }

    const sections = [
        { start: 0, end: wordIndex, color: '#22c55e' },
        { start: wordIndex, end: wordIndex + 1, color: '#3b82f6' },
        { start: wordIndex + 1, end: word.length, color: '#cbd5e1' }
    ];

    for (const section of sections) {
        if (section.start >= section.end || section.start >= word.length) continue;

        ctx.save();
        const clipRight = letterBoundaries[section.start];
        const clipLeft = letterBoundaries[Math.min(section.end, word.length)];

        ctx.beginPath();
        ctx.rect(clipLeft, 0, clipRight - clipLeft, canvas.height / dpr);
        ctx.clip();

        ctx.fillStyle = section.color;
        ctx.fillText(word, centerX, centerY);
        ctx.restore();
    }
}

export function updateCardStyles() {
    updateCurrentWord();

    for (let i = 0; i < state.targetSentence.length; i++) {
        const c = document.getElementById(`c-${i}`);
        if (!c) continue;
        if (state.targetSentence[i] === ' ') continue;

        if (i === state.currentTargetIndex) {
            c.className = `flex-shrink-0 w-28 h-40 bg-white rounded-xl border-2 flex flex-col items-center justify-between py-2 px-2 transition-all duration-500 ease-[cubic-bezier(0.34,1.56,0.64,1)] transform border-blue-500 scale-105 opacity-100 shadow-lg ring-2 ring-blue-500/10`;
        } else if (i > state.currentTargetIndex) {
            c.className = `flex-shrink-0 w-28 h-40 bg-white rounded-xl border flex flex-col items-center justify-between py-2 px-2 transition-all duration-500 transform border-slate-200 scale-95 opacity-50`;
        }
    }
}

export function markWordComplete(endIdx) {
    for (let i = endIdx; i >= 0; i--) {
        if (i < 0) break;
        if (state.targetSentence[i] === ' ') break;

        const c = document.getElementById(`c-${i}`);
        if (c) {
            c.className = `flex-shrink-0 w-28 h-40 bg-green-50 rounded-xl border border-green-300 flex flex-col items-center justify-between py-2 px-2 transition-all duration-500 transform scale-85 opacity-40 shadow-inner`;
            const letterDisplay = document.getElementById(`letter-${i}`);
            if (letterDisplay) {
                letterDisplay.className = 'text-2xl font-black text-green-600 mt-1 quran-text';
                letterDisplay.style.fontFamily = "'Amiri', 'Arabic Typesetting', 'Traditional Arabic', serif";
            }
            const img = c.querySelector('img');
            if (img) {
                img.className = 'w-24 h-24 object-contain mix-blend-multiply flex-shrink-0 opacity-50';
            }
        }
    }
}

export function updateVerseProgress() {
    if (!state.recitationMode || !state.currentSurah) return;
    const totalVerses = state.currentSurah.verses.length;
    const currentVerse = state.currentVerseIndex + 1;
    const progressPercent = (state.currentVerseIndex / totalVerses) * 100;
    const elText = document.getElementById('verseProgressText');
    const elBar = document.getElementById('verseProgressBar');
    if (elText) elText.innerText = `آية ${currentVerse} من ${totalVerses}`;
    if (elBar) elBar.style.width = `${progressPercent}%`;
}

export function showSuccessFlash() {
    const flash = document.getElementById('successFlash');
    if (!flash) return;
    flash.classList.remove('hidden');
    setTimeout(() => {
        flash.classList.add('hidden');
    }, 400);
}

export function showCorrectionOverlay(letter) {
    state.pauseDetection = true;
    state.gameActive = false;

    const img = document.getElementById('correctSignImage');
    img.src = `/sign_image/${encodeURIComponent(letter)}`;
    img.onerror = function () { this.style.opacity = '0.3'; };

    document.getElementById('correctLetterDisplay').innerText = letter;

    const currentErrors = state.letterErrorCount[state.currentTargetIndex] || 0;
    document.getElementById('errorCountBadge').innerText = `حاولت ${currentErrors} من ${state.MAX_ATTEMPTS_PER_LETTER} مرات`;
    document.getElementById('correctionOverlay').classList.remove('hidden');
}

export function showSurahFinalResults() {
    const totalTime = ((Date.now() - state.startTime) / 1000).toFixed(1);
    const totalMistakes = state.mistakes.length;

    // Fallback safe checks
    const versesStr = (state.currentSurah && state.currentSurah.verses) ? state.currentSurah.verses.join('') : "";
    const totalLetters = versesStr.replace(/\s/g, '').length;
    const accuracy = totalLetters > 0 ? ((totalLetters - totalMistakes) / totalLetters * 100).toFixed(0) : 0;

    if (state.recitationMode && state.verseResults.length > 0) {
        const passedVerses = state.verseResults.filter(v => v.passed).length;
        const totalVerses = state.verseResults.length;

        document.getElementById('sumScore').innerText = `${passedVerses}/${totalVerses}`;
        document.getElementById('sumTime').innerText = totalTime + 's';

        let verseBreakdownHtml = '<div class="text-right space-y-2">';
        state.verseResults.forEach((result) => {
            const statusIcon = result.passed ? '✅' : '❌';
            const statusColor = result.passed ? 'text-green-600' : 'text-red-600';
            const bgColor = result.passed ? 'bg-green-50' : 'bg-red-50';
            const errorInfo = result.lettersWithErrors > 0
                ? `(${result.lettersWithErrors}/${result.totalLetters} حرف)`
                : '(بدون أخطاء)';
            verseBreakdownHtml += `
                <div class="flex items-center justify-between ${bgColor} rounded-xl p-3">
                    <span class="${statusColor} font-bold">${statusIcon} ${result.passed ? 'نجحت' : 'تحتاج مراجعة'} <span class="text-xs font-normal">${errorInfo}</span></span>
                    <span class="text-slate-600 font-arabic text-sm quran-text truncate max-w-[200px]">${result.verse.substring(0, 30)}${result.verse.length > 30 ? '...' : ''}</span>
                </div>
            `;
        });
        verseBreakdownHtml += '</div>';
        document.getElementById('completedSentence').innerHTML = verseBreakdownHtml;

        const practiceErrorsBtn = document.getElementById('practiceErrorsBtn');
        if (practiceErrorsBtn) {
            if (state.failedVerses.length > 0) {
                practiceErrorsBtn.classList.remove('hidden');
                practiceErrorsBtn.querySelector('span').innerText = `تدرب على الأخطاء (${state.failedVerses.length} آية)`;
            } else {
                practiceErrorsBtn.classList.add('hidden');
            }
        }
    } else {
        const totalV = (state.currentSurah && state.currentSurah.verses) ? state.currentSurah.verses.length : 0;
        document.getElementById('sumScore').innerText = `${totalV}/${totalV}`;
        document.getElementById('sumTime').innerText = totalTime + 's';
        document.getElementById('completedSentence').innerText = (state.currentSurah && state.currentSurah.verses) ? state.currentSurah.verses.join(' • ') : "";
    }

    document.getElementById('backToSurahSelectionBtn').classList.remove('hidden');
    document.getElementById('summaryOverlay').classList.remove('hidden');
}

// MediaPipe visualizer
const HAND_CONNECTIONS = [
    [0, 1], [1, 2], [2, 3], [3, 4],
    [0, 5], [5, 6], [6, 7], [7, 8],
    [0, 9], [9, 10], [10, 11], [11, 12],
    [0, 13], [13, 14], [14, 15], [15, 16],
    [0, 17], [17, 18], [18, 19], [19, 20],
    [5, 9], [9, 13], [13, 17]
];

export function drawHandLandmarks(landmarks, canvasWidth, canvasHeight) {
    if (!landmarks || landmarks.length === 0) return;
    const ctx = state.ctx;

    for (const handLandmarks of landmarks) {
        ctx.lineCap = 'round';
        ctx.lineJoin = 'round';

        // Bone Shadows
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.3)';
        ctx.lineWidth = 8;
        for (const [start, end] of HAND_CONNECTIONS) {
            const startPoint = handLandmarks[start];
            const endPoint = handLandmarks[end];
            if (startPoint && endPoint) {
                ctx.beginPath();
                ctx.moveTo(startPoint.x * canvasWidth + 2, startPoint.y * canvasHeight + 2);
                ctx.lineTo(endPoint.x * canvasWidth + 2, endPoint.y * canvasHeight + 2);
                ctx.stroke();
            }
        }

        // White Skeleton
        ctx.strokeStyle = '#FFFFFF';
        ctx.lineWidth = 5;
        for (const [start, end] of HAND_CONNECTIONS) {
            const startPoint = handLandmarks[start];
            const endPoint = handLandmarks[end];
            if (startPoint && endPoint) {
                ctx.beginPath();
                ctx.moveTo(startPoint.x * canvasWidth, startPoint.y * canvasHeight);
                ctx.lineTo(endPoint.x * canvasWidth, endPoint.y * canvasHeight);
                ctx.stroke();
            }
        }

        // Green Glow
        ctx.strokeStyle = '#22C55E';
        ctx.lineWidth = 2;
        for (const [start, end] of HAND_CONNECTIONS) {
            const startPoint = handLandmarks[start];
            const endPoint = handLandmarks[end];
            if (startPoint && endPoint) {
                ctx.beginPath();
                ctx.moveTo(startPoint.x * canvasWidth, startPoint.y * canvasHeight);
                ctx.lineTo(endPoint.x * canvasWidth, endPoint.y * canvasHeight);
                ctx.stroke();
            }
        }

        // Joints
        for (let i = 0; i < handLandmarks.length; i++) {
            const point = handLandmarks[i];
            const x = point.x * canvasWidth;
            const y = point.y * canvasHeight;
            let radius = 6;
            if (i === 0) radius = 10;
            else if ([4, 8, 12, 16, 20].includes(i)) radius = 5;

            ctx.beginPath();
            ctx.arc(x + 2, y + 2, radius, 0, 2 * Math.PI);
            ctx.fillStyle = 'rgba(0, 0, 0, 0.4)';
            ctx.fill();

            ctx.beginPath();
            ctx.arc(x, y, radius, 0, 2 * Math.PI);
            ctx.fillStyle = '#FFFFFF';
            ctx.fill();

            ctx.beginPath();
            ctx.arc(x, y, radius * 0.5, 0, 2 * Math.PI);
            ctx.fillStyle = '#22C55E';
            ctx.fill();
        }
    }
}
