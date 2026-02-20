"""
ai_generator.py — STUB (CBT v15)
==================================
The old AI-based exam generation (app.py) required Ollama + Llama 3.2.
CBT v15 uses a pre-built question bank (100k+ questions) instead.

Use bank_exam_app.py for all exam functionality.

This stub:
- Prevents ImportError from legacy app.py
- Provides translate_text using the new translation_engine_v2
"""

from translation_engine_v2 import translate_text, phrase_translate


def generate_section_wise_questions(*args, **kwargs):
    """Stub — not needed in v15. Use bank_exam_app.py."""
    return []


def generate_questions_batch(*args, **kwargs):
    """Stub — not needed in v15."""
    return []


__all__ = ["generate_section_wise_questions", "generate_questions_batch", "translate_text"]
