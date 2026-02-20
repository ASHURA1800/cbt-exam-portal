"""
translation_engine.py
=====================
Translates questions into 9 Indian languages using deep-translator (free).
Languages: Hindi, Bengali, Tamil, Telugu, Gujarati, Marathi, Kannada, Odia, English

Install: pip install deep-translator
"""

import json
import time
import sqlite3
from typing import Dict, List, Optional

try:
    from deep_translator import GoogleTranslator
    TRANSLATOR_AVAILABLE = True
except ImportError:
    TRANSLATOR_AVAILABLE = False

try:
    from googletrans import Translator as GtTranslator
    GOOGLETRANS_AVAILABLE = True
except ImportError:
    GOOGLETRANS_AVAILABLE = False

from question_bank_db import _bank_conn, _bank_lock, save_translation, questions_needing_translation

LANG_CODES = {
    "hi": "Hindi",
    "bn": "Bengali",
    "ta": "Tamil",
    "te": "Telugu",
    "gu": "Gujarati",
    "mr": "Marathi",
    "kn": "Kannada",
    "or": "Odia",
}

# deep-translator uses full language names or ISO codes
DEEP_TRANS_CODES = {
    "hi": "hi",
    "bn": "bn",
    "ta": "ta",
    "te": "te",
    "gu": "gu",
    "mr": "mr",
    "kn": "kn",
    "or": "or",
}

# Simple translation cache in memory
_cache = {}


def translate_text(text: str, target_lang: str) -> str:
    """Translate text to target language."""
    if not text or text.strip() == "":
        return text
    if target_lang == "en":
        return text

    cache_key = f"{target_lang}:{text[:50]}"
    if cache_key in _cache:
        return _cache[cache_key]

    # Try deep-translator first
    if TRANSLATOR_AVAILABLE:
        try:
            translated = GoogleTranslator(source='en', target=DEEP_TRANS_CODES[target_lang]).translate(text)
            if translated:
                _cache[cache_key] = translated
                return translated
        except Exception as e:
            pass

    # Try googletrans
    if GOOGLETRANS_AVAILABLE:
        try:
            translator = GtTranslator()
            result = translator.translate(text, dest=target_lang)
            if result and result.text:
                _cache[cache_key] = result.text
                return result.text
        except Exception as e:
            pass

    # Fallback: return original English
    return text


def translate_question(qb_id: int, lang: str) -> bool:
    """Translate all fields of a single question to target language."""
    conn = _bank_conn()
    with _bank_lock:
        row = conn.execute(
            "SELECT * FROM question_bank WHERE qb_id=?", (qb_id,)
        ).fetchone()
    if not row:
        return False
    row = dict(row)

    fields_to_translate = [
        "question_en",
        "option_a_en", "option_b_en", "option_c_en", "option_d_en",
    ]

    translations = {}
    for field in fields_to_translate:
        text = row.get(field, "")
        key = field.replace("_en", "")
        translations[key] = translate_text(text, lang)
        time.sleep(0.05)  # Rate limiting

    save_translation(qb_id, lang, translations)
    return True


def batch_translate_subject(subject: str, lang: str, limit: int = 200):
    """Translate questions for a subject to a language."""
    conn = _bank_conn()
    with _bank_lock:
        rows = conn.execute(f"""
            SELECT qb_id, question_en, option_a_en, option_b_en, option_c_en, option_d_en
            FROM question_bank
            WHERE subject=? AND (question_{lang} IS NULL OR question_{lang} = '')
            LIMIT ?
        """, (subject, limit)).fetchall()

    if not rows:
        print(f"  ✅ {subject} → {LANG_CODES.get(lang, lang)}: all translated")
        return 0

    count = 0
    for row in rows:
        d = dict(row)
        translations = {}
        for field in ["question", "option_a", "option_b", "option_c", "option_d"]:
            text = d.get(f"{field}_en", "")
            translations[field] = translate_text(text, lang)
            time.sleep(0.05)
        save_translation(d["qb_id"], lang, translations)
        count += 1
        if count % 50 == 0:
            print(f"  Translated {count}/{len(rows)} for {subject} → {lang}")

    return count


def run_translation_for_all_subjects(langs=None, questions_per_subject=500):
    """Run translation pipeline for all subjects and languages."""
    if langs is None:
        langs = list(LANG_CODES.keys())

    if not (TRANSLATOR_AVAILABLE or GOOGLETRANS_AVAILABLE):
        print("⚠️  No translation library found.")
        print("   Install with: pip install deep-translator")
        print("   Questions will fall back to English when translation is unavailable.")
        return

    conn = _bank_conn()
    with _bank_lock:
        subjects = [r[0] for r in conn.execute(
            "SELECT DISTINCT subject FROM question_bank"
        ).fetchall()]

    for subject in subjects:
        for lang in langs:
            print(f"\nTranslating {subject} → {LANG_CODES.get(lang, lang)}...")
            try:
                count = batch_translate_subject(subject, lang, limit=questions_per_subject)
                print(f"  ✅ Translated {count} questions")
            except Exception as e:
                print(f"  ⚠️  Error: {e}")

    print("\n✅ Translation batch complete!")


def get_translation_stats() -> Dict:
    """Get stats on how many questions are translated per language."""
    conn = _bank_conn()
    stats = {}
    for lang in LANG_CODES.keys():
        with _bank_lock:
            translated = conn.execute(f"""
                SELECT COUNT(*) FROM question_bank
                WHERE question_{lang} IS NOT NULL AND question_{lang} != ''
            """).fetchone()[0]
            total = conn.execute("SELECT COUNT(*) FROM question_bank").fetchone()[0]
        stats[lang] = {
            "translated": translated,
            "total": total,
            "pct": round(translated / total * 100, 1) if total > 0 else 0,
        }
    return stats


def get_question_text(row: dict, lang: str) -> dict:
    """
    Get question text in specified language.
    Falls back to English if translation not available.
    """
    if lang == "en":
        return {
            "question": row.get("question_en", ""),
            "option_a": row.get("option_a_en", ""),
            "option_b": row.get("option_b_en", ""),
            "option_c": row.get("option_c_en", ""),
            "option_d": row.get("option_d_en", ""),
        }

    q_translated = row.get(f"question_{lang}", "")
    a_translated = row.get(f"option_a_{lang}", "")

    # If not translated, return English
    if not q_translated:
        return {
            "question": row.get("question_en", ""),
            "option_a": row.get("option_a_en", ""),
            "option_b": row.get("option_b_en", ""),
            "option_c": row.get("option_c_en", ""),
            "option_d": row.get("option_d_en", ""),
            "_translation_available": False,
        }

    return {
        "question": q_translated,
        "option_a": a_translated or row.get("option_a_en", ""),
        "option_b": row.get(f"option_b_{lang}", "") or row.get("option_b_en", ""),
        "option_c": row.get(f"option_c_{lang}", "") or row.get("option_c_en", ""),
        "option_d": row.get(f"option_d_{lang}", "") or row.get("option_d_en", ""),
        "_translation_available": True,
    }
