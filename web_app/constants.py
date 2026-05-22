"""Single source of truth for label mappings and hand landmark connections."""

# Arabic Sign Language letter labels (index → Arabic character)
# This is the ONLY place this mapping should be defined.
# All other modules should import from here.
LABELS = {
    0: 'ا', 1: 'ب', 2: 'ت', 3: 'ث', 4: 'ج', 5: 'ح', 6: 'خ', 7: 'د', 8: 'ذ',
    9: 'ر', 10: 'ز', 11: 'س', 12: 'ش', 13: 'ص', 14: 'ض', 15: 'ط', 16: 'ظ',
    17: 'ع', 18: 'غ', 19: 'ف', 20: 'ق', 21: 'ك', 22: 'ل', 23: 'م', 24: 'ن',
    25: 'ه', 26: 'و', 27: 'ي', 28: 'ة', 29: 'لا',
}

# MediaPipe hand landmark connections for skeleton drawing
# Each tuple is (start_index, end_index) following the 21-point hand model
HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),       # Thumb
    (0, 5), (5, 6), (6, 7), (7, 8),       # Index finger
    (5, 9), (9, 10), (10, 11), (11, 12),   # Middle finger
    (9, 13), (13, 14), (14, 15), (15, 16), # Ring finger
    (13, 17), (17, 18), (18, 19), (19, 20),# Pinky
    (0, 17),                                # Palm base
]
