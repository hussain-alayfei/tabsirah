# -*- coding: utf-8 -*-
"""
بيانات السور القرآنية للتدريب
Quranic Surah data for training
"""
import json
import os
import glob

# Path to JSON files
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'surahs')

# Cache for loaded surahs
_SURAHS_CACHE = {}

def _load_surahs():
    """Load all JSON files from data/surahs directory"""
    global _SURAHS_CACHE
    if _SURAHS_CACHE:
        return _SURAHS_CACHE

    if not os.path.exists(DATA_DIR):
        print(f"Warning: Data directory not found: {DATA_DIR}")
        return {}

    json_files = glob.glob(os.path.join(DATA_DIR, '*.json'))
    surahs = {}
    
    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                surahs[data['id']] = data
        except Exception as e:
            print(f"Error loading {file_path}: {e}")
            
    _SURAHS_CACHE = surahs
    return surahs

def get_all_surahs():
    """
    Get all surahs with their metadata
    """
    return _load_surahs()

def get_surah(surah_id):
    """
    Get a specific surah by ID
    Returns None if not found
    """
    surahs = _load_surahs()
    return surahs.get(surah_id)

def is_surah_unlocked(surah_id):
    """
    Check if a surah is unlocked
    """
    surah = get_surah(surah_id)
    return surah and surah.get('unlocked', False)
