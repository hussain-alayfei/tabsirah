import { state } from "./state.js";

function getPerformanceRating(accuracy) {
    if (accuracy >= 95) {
        return `
            <div class="text-center">
                <div class="text-6xl mb-4">🏆</div>
                <div class="text-3xl font-black text-yellow-500 mb-2 font-arabic">ممتاز جداً!</div>
                <p class="text-slate-600 font-arabic">أداء رائع! واصل التميز</p>
            </div>
        `;
    } else if (accuracy >= 80) {
        return `
            <div class="text-center">
                <div class="text-6xl mb-4">⭐</div>
                <div class="text-3xl font-black text-blue-600 mb-2 font-arabic">جيد جداً</div>
                <p class="text-slate-600 font-arabic">أداء مميز! يمكنك تحسينه أكثر</p>
            </div>
        `;
    } else if (accuracy >= 60) {
        return `
            <div class="text-center">
                <div class="text-6xl mb-4">👍</div>
                <div class="text-3xl font-black text-center text-slate-700 mb-2 font-arabic">جيد</div>
                <p class="text-slate-600 font-arabic">أداء جيد، واصل التدريب</p>
            </div>
        `;
    } else {
        return `
            <div class="text-center">
                <div class="text-6xl mb-4">💪</div>
                <div class="text-3xl font-black text-slate-700 mb-2 font-arabic">استمر في المحاولة</div>
                <p class="text-slate-600 font-arabic">كثرة التدريب توصل للإتقان</p>
            </div>
        `;
    }
}

export function generateAnalytics() {
    const content = document.getElementById('analyticsContent');
    if (!content) return;

    const duration = ((Date.now() - state.startTime) / 1000).toFixed(1);

    let totalLetters;
    let displaySentence;
    if (state.surahMode && state.currentSurah) {
        totalLetters = state.currentSurah.verses.join('').replace(/\s/g, '').length;
        displaySentence = state.currentSurah.verses.join(' • ');
    } else {
        totalLetters = state.targetSentence.replace(/\s/g, '').length;
        displaySentence = state.targetSentence;
    }

    const totalMistakes = state.mistakes.length;
    const accuracy = totalLetters > 0 ? ((totalLetters / (totalLetters + totalMistakes)) * 100).toFixed(1) : 0;

    // Find most difficult letter
    let mostDifficult = null;
    let maxErrors = 0;
    for (let letter in state.letterStats) {
        if (state.letterStats[letter].wrong > maxErrors) {
            maxErrors = state.letterStats[letter].wrong;
            mostDifficult = letter;
        }
    }

    // Average time
    let totalTime = 0;
    let letterCount = 0;
    for (let letter in state.letterStats) {
        if (state.letterStats[letter].correct > 0) {
            totalTime += state.letterStats[letter].totalTime;
            letterCount += state.letterStats[letter].correct;
        }
    }
    const avgTimePerLetter = letterCount > 0 ? (totalTime / letterCount / 1000).toFixed(1) : 0;

    let html = '';

    // Header
    if (state.surahMode && state.currentSurah) {
        const passedVerses = state.recitationMode ? state.verseResults.filter(v => v.passed).length : state.currentSurah.verses.length;
        const totalVerses = state.currentSurah.verses.length;
        const modeLabel = state.recitationMode ? 'تقرير التسميع' : 'تقرير التدريب';
        const headerColor = state.recitationMode ? 'from-indigo-500 to-purple-600' : 'from-cyan-500 to-blue-600';

        html += `
            <div class="bg-gradient-to-br ${headerColor} rounded-3xl p-8 shadow-xl text-center mb-6">
                <div class="text-5xl mb-4">${state.recitationMode ? '📝' : '📖'}</div>
                <h2 class="text-3xl font-black text-white mb-2 font-arabic">${state.currentSurah.name}</h2>
                <p class="text-cyan-100 font-arabic">${modeLabel}</p>
                <div class="mt-6 bg-white/20 backdrop-blur rounded-2xl p-4">
                    <div class="text-white text-lg font-bold font-arabic">
                        ${state.recitationMode ? `${passedVerses} من ${totalVerses} آيات صحيحة` : `أكملت ${totalVerses} ${totalVerses === 1 ? 'آية' : 'آيات'}`}
                    </div>
                </div>
            </div>
        `;

        if (state.recitationMode && state.verseResults.length > 0) {
            html += `
                <div class="bg-white rounded-3xl p-8 shadow-xl">
                    <h2 class="text-2xl font-black text-slate-900 mb-6 font-arabic">📋 تفصيل الآيات</h2>
                    <div class="space-y-3">
            `;
            state.verseResults.forEach((result) => {
                const statusIcon = result.passed ? '✅' : '❌';
                const statusText = result.passed ? 'نجحت' : 'تحتاج مراجعة';
                const bgColor = result.passed ? 'bg-green-50 border-green-200' : 'bg-red-50 border-red-200';
                const textColor = result.passed ? 'text-green-700' : 'text-red-700';

                html += `
                    <div class="flex items-start justify-between ${bgColor} rounded-xl p-4 border">
                        <div class="flex-1 text-right">
                            <div class="quran-text text-lg text-slate-800 mb-2">${result.verse}</div>
                            <div class="text-xs text-slate-500">
                                أخطأت في ${result.lettersWithErrors} حرف من ${result.totalLetters} حرف
                                (${result.errorRate.toFixed(0)}%)
                            </div>
                        </div>
                        <div class="${textColor} font-bold text-sm whitespace-nowrap mr-4">
                            ${statusIcon} ${statusText}
                        </div>
                    </div>
                `;
            });
            html += `</div></div>`;
        }
    }

    // Overall Stats
    html += `
        <div class="bg-white rounded-3xl p-8 shadow-xl">
            <h2 class="text-2xl font-black text-slate-900 mb-6 font-arabic">📈 الإحصائيات العامة</h2>
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-6 text-center">
                    <div class="text-4xl font-black text-blue-600">${totalLetters}</div>
                    <div class="text-sm text-blue-800 mt-2 font-arabic font-bold">حرف مكتمل</div>
                </div>
                <div class="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl p-6 text-center">
                    <div class="text-4xl font-black text-green-600">${accuracy}%</div>
                    <div class="text-sm text-green-800 mt-2 font-arabic font-bold">نسبة الدقة</div>
                </div>
                <div class="bg-gradient-to-br from-red-50 to-red-100 rounded-2xl p-6 text-center">
                    <div class="text-4xl font-black text-red-600">${totalMistakes}</div>
                    <div class="text-sm text-red-800 mt-2 font-arabic font-bold">عدد الأخطاء</div>
                </div>
                <div class="bg-gradient-to-br from-purple-50 to-purple-100 rounded-2xl p-6 text-center">
                    <div class="text-4xl font-black text-purple-600">${duration}s</div>
                    <div class="text-sm text-purple-800 mt-2 font-arabic font-bold">الوقت الكلي</div>
                </div>
            </div>
        </div>
        
        <div class="bg-gradient-to-br from-emerald-500 to-cyan-600 rounded-3xl p-8 shadow-xl text-center">
             <div class="text-white text-sm font-semibold mb-4 font-arabic">${state.surahMode ? 'آيات السورة' : 'الجملة التي تدربت عليها'}</div>
             <div dir="rtl" class="text-5xl font-bold text-white leading-relaxed quran-text">
                 ${displaySentence}
             </div>
        </div>

        <div class="bg-white rounded-3xl p-8 shadow-xl">
             <h2 class="text-2xl font-black text-slate-900 mb-6 font-arabic">⭐ تقييم الأداء</h2>
             <div class="flex items-center justify-center gap-6">
                 ${getPerformanceRating(accuracy)}
             </div>
        </div>
    `;

    // Most Difficult Letter
    if (mostDifficult) {
        html += `
            <div class="bg-white rounded-3xl p-8 shadow-xl">
                <h2 class="text-2xl font-black text-slate-900 mb-6 font-arabic">🎯 الحرف الأكثر صعوبة</h2>
                <div class="bg-gradient-to-br from-orange-50 to-red-50 rounded-2xl p-8 text-center border-2 border-orange-200">
                    <div class="text-7xl font-black text-orange-600 mb-4 quran-text">${mostDifficult}</div>
                    <div class="text-lg text-orange-800 font-arabic font-bold">
                        ${maxErrors} ${maxErrors === 1 ? 'خطأ' : 'أخطاء'}
                    </div>
                    <p class="text-sm text-orange-700 mt-3 font-arabic">ركز على هذا الحرف في التدريبات القادمة</p>
                </div>
            </div>
        `;
    }

    // Letter Breakdown
    html += `
        <div class="bg-white rounded-3xl p-8 shadow-xl">
            <h2 class="text-2xl font-black text-slate-900 mb-6 font-arabic">📝 تفصيل الحروف</h2>
            <div class="space-y-3">
    `;

    for (let letter in state.letterStats) {
        const stats = state.letterStats[letter];
        const letterAccuracy = stats.correct > 0 ?
            ((stats.correct / (stats.correct + stats.wrong)) * 100).toFixed(0) : 0;
        const avgTime = stats.correct > 0 ? (stats.totalTime / stats.correct / 1000).toFixed(1) : 0;

        html += `
            <div class="bg-slate-50 rounded-xl p-4 flex items-center justify-between">
                <div class="flex-1 flex items-center gap-4">
                    <div class="text-3xl font-black text-slate-700 quran-text">${letter}</div>
                    <div>
                        <div class="text-sm font-arabic text-slate-600">
                            <span class="text-green-600 font-bold">${stats.correct} صحيح</span>
                            ${stats.wrong > 0 ? `<span class="text-red-600 font-bold"> • ${stats.wrong} خطأ</span>` : ''}
                        </div>
                        <div class="text-xs text-slate-500 font-arabic mt-1">متوسط الوقت: ${avgTime}ث</div>
                    </div>
                </div>
                <div class="flex items-center gap-2">
                    <div class="text-2xl font-black ${letterAccuracy >= 80 ? 'text-green-600' : letterAccuracy >= 50 ? 'text-orange-600' : 'text-red-600'}">
                        ${letterAccuracy}%
                    </div>
                </div>
            </div>
        `;
    }
    html += `</div></div>`;

    // Speed Analysis
    html += `
        <div class="bg-white rounded-3xl p-8 shadow-xl">
            <h2 class="text-2xl font-black text-slate-900 mb-6 font-arabic">⚡ تحليل السرعة</h2>
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-blue-50 rounded-2xl p-6 text-center">
                    <div class="text-3xl font-black text-blue-600">${avgTimePerLetter}s</div>
                    <div class="text-sm text-blue-800 mt-2 font-arabic font-bold">متوسط الوقت لكل حرف</div>
                </div>
                <div class="bg-green-50 rounded-2xl p-6 text-center">
                    <div class="text-3xl font-black text-green-600">${(totalLetters / (duration || 1) * 60).toFixed(1)}</div>
                    <div class="text-sm text-green-800 mt-2 font-arabic font-bold">حرف في الدقيقة</div>
                </div>
                <div class="bg-purple-50 rounded-2xl p-6 text-center">
                    <div class="text-3xl font-black text-purple-600">${state.score}</div>
                    <div class="text-sm text-purple-800 mt-2 font-arabic font-bold">النقاط المكتسبة</div>
                </div>
            </div>
        </div>
    `;

    content.innerHTML = html;
}
