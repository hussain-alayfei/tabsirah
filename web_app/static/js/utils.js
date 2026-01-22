// ============================================
// UTILS
// ============================================

export function normalizeArabicChar(char) {
    if (!char) return '';

    // تطبيع الألف: أ، إ، آ، ء → ا
    char = char.replace(/[أإآءٱ]/g, 'ا');

    // تطبيع الياء: ى، ئ → ي
    char = char.replace(/[ىئ]/g, 'ي');

    // تطبيع التاء المربوطة: ة → ه
    char = char.replace(/[ة]/g, 'ه');

    // إزالة التشكيل (الحركات)
    char = char.replace(/[\u064B-\u065F\u0670]/g, '');

    return char;
}

export function areCharsEquivalent(pred, target) {
    if (!pred || !target) return false;

    // تطبيع كلا الحرفين للمقارنة
    const normalizedPred = normalizeArabicChar(pred);
    const normalizedTarget = normalizeArabicChar(target);

    return normalizedPred === normalizedTarget;
}
