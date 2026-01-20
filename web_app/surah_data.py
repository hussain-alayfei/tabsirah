# -*- coding: utf-8 -*-
"""
بيانات السور القرآنية للتدريب
Quranic Surah data for training
"""

SURAHS = {
    'al-kawthar': {
        'id': 'al-kawthar',
        'name': 'سورة الكوثر',
        'name_english': 'Al-Kawthar',
        'number': 108,
        'verses': [
            'إنا أعطيناك الكوثر',
            'فصل لربك وانحر',
            'إن شانئك هو الأبتر'
        ],
        'unlocked': True,
        'video_url': 'https://www.youtube.com/embed/JvXeFXrOe-8',
        'description': 'سورة مكية، عدد آياتها 3'
    },
    'al-maun': {
        'id': 'al-maun',
        'name': 'سورة الماعون',
        'name_english': 'Al-Maun',
        'number': 107,
        'verses': [],  # مقفلة - سيتم إضافتها لاحقاً
        'unlocked': False,
        'video_url': None,
        'description': 'سورة مكية، عدد آياتها 7'
    },
    'quraysh': {
        'id': 'quraysh',
        'name': 'سورة قريش',
        'name_english': 'Quraysh',
        'number': 106,
        'verses': [],  # مقفلة - سيتم إضافتها لاحقاً
        'unlocked': False,
        'video_url': None,
        'description': 'سورة مكية، عدد آياتها 4'
    },
    'al-fil': {
        'id': 'al-fil',
        'name': 'سورة الفيل',
        'name_english': 'Al-Fil',
        'number': 105,
        'verses': [],  # مقفلة - سيتم إضافتها لاحقاً
        'unlocked': False,
        'video_url': None,
        'description': 'سورة مكية، عدد آياتها 5'
    }
}

def get_all_surahs():
    """
    Get all surahs with their metadata
    """
    return SURAHS

def get_surah(surah_id):
    """
    Get a specific surah by ID
    Returns None if not found
    """
    return SURAHS.get(surah_id)

def is_surah_unlocked(surah_id):
    """
    Check if a surah is unlocked
    """
    surah = get_surah(surah_id)
    return surah and surah.get('unlocked', False)
