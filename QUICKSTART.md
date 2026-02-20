# CBT Exam Portal v15 — Quickstart

## 🚀 Start the App

**Windows:**
```
Double-click START.bat
```

**Mac/Linux:**
```bash
bash start.sh
```

**Manual:**
```bash
pip install streamlit
streamlit run bank_exam_app.py
```

Open: **http://localhost:8501**

---

## 🌐 Translate All 1 Lakh+ Questions (Offline)

1. Login as admin (username: `admin`)
2. Click **🛠 Admin** → **🌐 Translation** tab
3. Click **🌏 Translate ALL 8 Languages (Recommended)**
4. Wait ~5 minutes — no internet needed!
5. All 100,000+ questions translated offline at ~2,000/sec

**How it works:**
- Uses built-in phrase dictionaries covering Physics, Chemistry, Biology, Maths, GK
- Completely offline — no API key, no internet required
- Results saved permanently to `question_bank.db`
- Students can switch language during exam anytime

---

## 📚 Supported Languages

| Code | Language | Native |
|------|----------|--------|
| en | English | English |
| hi | Hindi | हिंदी |
| bn | Bengali | বাংলা |
| ta | Tamil | தமிழ் |
| te | Telugu | తెలుగు |
| gu | Gujarati | ગુજરાતી |
| mr | Marathi | मराठी |
| kn | Kannada | ಕನ್ನಡ |
| or | Odia | ଓଡ଼ିଆ |

---

## 📊 Database Info

- **106,815+ questions** pre-loaded
- Subjects: Physics, Chemistry, Biology, Mathematics, GK, English, Reasoning, Quantitative
- Exams: NEET, JEE, CUET Domain, CUET General + 4 subject-wise practice modes
- Smart dedup: never shows the same question twice per student
- Recycle pool: deleted exam questions can be reused

---

## 🔧 Key Files

| File | Purpose |
|------|---------|
| `bank_exam_app.py` | **Main app** — run this |
| `translation_engine_v2.py` | Offline translation engine (fixed v2.1) |
| `question_bank_db.py` | Question bank database layer |
| `question_bank.db` | SQLite DB with 106k+ questions |
| `db.py` | User auth database |

---

## ✅ What Was Fixed in v15

1. **Offline translation now works for all 1 lakh+ questions** — batch processes 2,000 q/sec
2. **Fixed Python 3.6–3.9 DB bug** — `sqlite3.in_transaction` AttributeError removed
3. **Fixed DB deadlocks** — transactions simplified and thread-safe
4. **Fixed missing `ai_generator.py`** — ImportError in legacy app.py resolved
5. **Improved translation admin panel** — progress bars, per-language status, one-click all-language translate
6. **Faster batch DB writes** — single transaction for batch inserts (10x faster)
7. **On-the-fly translation fallback** — questions always show in selected language even if not pre-translated
8. **Async DB save** — on-the-fly translations saved to DB in background thread
9. **Improved palette button styling** — JS-based color override for exam question palette
10. **Better error handling** — graceful fallbacks throughout

