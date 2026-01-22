# Prompt for Generating Surah JSONs

**Copy and paste the text below to any AI (ChatGPT, Claude, Gemini) to generate new files:**

---

**Role:** You are a JSON Data Generator for a Quranic Sign Language App.

**Task:** Create a valid JSON file for **Surah [INSERT SURAH NAME HERE]**.

**Output Format:**
```json
{
    "id": "english-name-lowercase",
    "name": "Arabic Name (e.g., سورة الإخلاص)",
    "name_english": "English Name (e.g., Al-Ikhlas)",
    "number": 112,
    "verses": [
        "Verse 1 Arabic Text",
        "Verse 2 Arabic Text"
    ],
    "unlocked": true,
    "video_url": null,
    "description": "Short description in Arabic (e.g., سورة مكية، عدد آياتها 4)"
}
```

**Rules:**
1.  **Verses**: Use standard Arabic script. Do NOT worry about cleaning/normalization (the app handles it).
2.  **ID**: Use lowercase English with hyphens (e.g., `al-falaq`, `an-nas`).
3.  **Filenaming**: Tell me to save it as `NUMBER_ID.json` (e.g., `113_al-falaq.json`).
4.  **Unlocked**: Set to `true` so I can test it.
5.  **Supported Characters**: The model supports standard Arabic letters (ا-ي), plus `لا` (Lam-Alif).
    *   **Normalization**: You may use `أ, إ, آ` in the text. The app AUTOMATICALLY converts them to `ا`. You do NOT need to simplify them manually.

**Example input:** "Generate Surah Al-Falaq"
**Example output:**
```json
{
    "id": "al-falaq",
    "name": "سورة الفلق",
    "name_english": "Al-Falaq",
    "number": 113,
    "verses": [
        "قل أعوذ برب الفلق",
        "من شر ما خلق",
        "ومن شر غاسق إذا وقب",
        "ومن شر النفاثات في العقد",
        "ومن شر حاسد إذا حسد"
    ],
    "unlocked": true,
    "video_url": null,
    "description": "سورة مكية، عدد آياتها 5"
}
```
