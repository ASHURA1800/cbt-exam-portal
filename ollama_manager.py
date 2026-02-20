"""
ollama_manager.py — STUB (CBT v12)
====================================
The old AI-based exam system (app.py) required Ollama.
CBT v12 no longer needs AI — all 58,000+ questions are pre-built.

Use the new app instead:
    streamlit run bank_exam_app.py

This stub prevents ImportError if someone accidentally runs app.py.
"""

OLLAMA_MODEL = "none"

def warm_up_model():
    return False, "AI not needed — use bank_exam_app.py"

def is_model_ready():
    return False

def get_status():
    return {
        "ollama_running": False,
        "model_pulled": False,
        "model_ready": False,
        "message": "CBT v12 uses pre-built question bank. Run: streamlit run bank_exam_app.py",
    }

def clear_response_cache():
    pass

def _is_ollama_running():
    return False

def _is_model_pulled():
    return False

def call_ollama_streaming(prompt, **kwargs):
    yield "⚠️ AI not needed in CBT v12. Please run `streamlit run bank_exam_app.py` instead."
