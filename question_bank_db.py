"""
question_bank_db.py — Central Question Bank Layer
===================================================
Manages 40,000+ pre-written questions across 8 subjects.
Completely separate from AI generation — pure static bank.

Tables:
  question_bank       — master pool of all questions
  student_q_history   — tracks which questions each student has seen
  bank_exams          — exams created from the bank
  bank_exam_questions — which questions belong to each bank exam
"""

import sqlite3
import threading
import json
import random
from typing import List, Dict, Optional, Tuple
from datetime import datetime

BANK_DB_PATH = "question_bank.db"
_bank_lock = threading.Lock()
_bank_local = threading.local()

# ── Auto-setup DB on first run ────────────────────────────────────────────────
def _setup_db_if_needed():
    """
    Tries 2 methods to get question_bank.db:
    1. Reassemble from .part_* files (if present)
    2. Download from GitHub Releases URL (set DB_DOWNLOAD_URL env var)
    """
    import os, glob

    if os.path.exists(BANK_DB_PATH) and os.path.getsize(BANK_DB_PATH) > 1_000_000:
        return  # Already exists

    # Method 1: Reassemble from split parts
    parts = sorted(glob.glob(BANK_DB_PATH + ".part_*"))
    if parts:
        print(f"🔧 Reassembling question_bank.db from {len(parts)} parts...", flush=True)
        with open(BANK_DB_PATH, "wb") as out:
            for part in parts:
                with open(part, "rb") as f:
                    out.write(f.read())
        size_mb = os.path.getsize(BANK_DB_PATH) / 1_048_576
        print(f"✅ question_bank.db assembled ({size_mb:.1f} MB)", flush=True)
        return

    # Method 2: Download from GitHub Releases
    url = os.environ.get("DB_DOWNLOAD_URL", "")
    if url:
        import urllib.request
        print(f"📥 Downloading question_bank.db...", flush=True)
        try:
            urllib.request.urlretrieve(url, BANK_DB_PATH)
            size_mb = os.path.getsize(BANK_DB_PATH) / 1_048_576
            print(f"✅ Downloaded ({size_mb:.1f} MB)", flush=True)
        except Exception as e:
            print(f"❌ Download failed: {e}", flush=True)

_setup_db_if_needed()

SUPPORTED_LANGUAGES = ["en", "hi", "mr", "ta", "te", "gu", "bn", "kn", "or"]

SUBJECT_EXAM_MAP = {
    # NEET
    "Physics":    ["NEET", "CUET_DOMAIN"],
    "Chemistry":  ["NEET", "CUET_DOMAIN"],
    "Biology":    ["NEET"],
    "Mathematics":["CUET_DOMAIN"],
    # CUET General
    "CUET_GK":          ["CUET_GT"],
    "CUET_English":     ["CUET_GT"],
    "CUET_Reasoning":   ["CUET_GT"],
    "CUET_Quantitative":["CUET_GT"],
}

DIFFICULTY_LEVELS = ["medium", "hard", "very_hard"]


def _bank_conn():
    if not getattr(_bank_local, "conn", None):
        _bank_local.conn = _make_conn(BANK_DB_PATH)
    return _bank_local.conn


def _make_conn(path: str):
    conn = sqlite3.connect(path, check_same_thread=False, timeout=30)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-32000")
    return conn


def _create_recycle_tables(conn):
    """Create tables for exam recycle system."""
    conn.execute("""
    CREATE TABLE IF NOT EXISTS exam_recycle_pool (
        recycle_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        original_session_id INTEGER,
        subject TEXT NOT NULL,
        qb_id INTEGER NOT NULL,
        recycled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        source TEXT DEFAULT 'deleted_exam',
        is_available INTEGER DEFAULT 1,
        UNIQUE(user_id, qb_id, subject)
    )""")
    # Track which recycled questions have been reused
    conn.execute("""
    CREATE TABLE IF NOT EXISTS recycle_usage_log (
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        recycle_id INTEGER,
        user_id TEXT NOT NULL,
        new_session_id INTEGER,
        reused_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY(recycle_id) REFERENCES exam_recycle_pool(recycle_id)
    )""")

def init_bank():
    """Create all question bank tables."""
    conn = _bank_conn()
    with _bank_lock:
        conn.execute("BEGIN")
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS question_bank (
                    qb_id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject         TEXT NOT NULL,
                    exam_type       TEXT NOT NULL,
                    topic           TEXT,
                    subtopic        TEXT,
                    difficulty      TEXT NOT NULL DEFAULT 'medium',
                    question_en     TEXT NOT NULL,
                    option_a_en     TEXT NOT NULL,
                    option_b_en     TEXT NOT NULL,
                    option_c_en     TEXT NOT NULL,
                    option_d_en     TEXT NOT NULL,
                    correct_answer  TEXT NOT NULL,
                    marks_correct   REAL DEFAULT 4.0,
                    marks_wrong     REAL DEFAULT -1.0,
                    explanation_en  TEXT,
                    -- Translated columns (filled lazily)
                    question_hi TEXT, option_a_hi TEXT, option_b_hi TEXT,
                    option_c_hi TEXT, option_d_hi TEXT, explanation_hi TEXT,
                    question_mr TEXT, option_a_mr TEXT, option_b_mr TEXT,
                    option_c_mr TEXT, option_d_mr TEXT, explanation_mr TEXT,
                    question_ta TEXT, option_a_ta TEXT, option_b_ta TEXT,
                    option_c_ta TEXT, option_d_ta TEXT, explanation_ta TEXT,
                    question_te TEXT, option_a_te TEXT, option_b_te TEXT,
                    option_c_te TEXT, option_d_te TEXT, explanation_te TEXT,
                    question_gu TEXT, option_a_gu TEXT, option_b_gu TEXT,
                    option_c_gu TEXT, option_d_gu TEXT, explanation_gu TEXT,
                    question_bn TEXT, option_a_bn TEXT, option_b_bn TEXT,
                    option_c_bn TEXT, option_d_bn TEXT, explanation_bn TEXT,
                    question_kn TEXT, option_a_kn TEXT, option_b_kn TEXT,
                    option_c_kn TEXT, option_d_kn TEXT, explanation_kn TEXT,
                    question_or TEXT, option_a_or TEXT, option_b_or TEXT,
                    option_c_or TEXT, option_d_or TEXT, explanation_or TEXT,
                    translated_langs TEXT DEFAULT '[]',
                    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS student_q_history (
                    history_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id     INTEGER NOT NULL,
                    qb_id       INTEGER NOT NULL,
                    subject     TEXT NOT NULL,
                    seen_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, qb_id)
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS bank_exams (
                    bank_exam_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                    exam_name     TEXT NOT NULL,
                    exam_type     TEXT NOT NULL,
                    subjects      TEXT NOT NULL,
                    q_per_subject INTEGER NOT NULL DEFAULT 45,
                    duration_mins INTEGER NOT NULL DEFAULT 180,
                    difficulty_mix TEXT,
                    created_by    INTEGER,
                    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS bank_exam_sessions (
                    session_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                    bank_exam_id  INTEGER NOT NULL,
                    user_id       INTEGER NOT NULL,
                    language      TEXT DEFAULT 'en',
                    status        TEXT DEFAULT 'in_progress',
                    start_time    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    end_time      TIMESTAMP,
                    total_score   REAL DEFAULT 0,
                    correct_count INTEGER DEFAULT 0,
                    wrong_count   INTEGER DEFAULT 0,
                    unattempted   INTEGER DEFAULT 0,
                    FOREIGN KEY (bank_exam_id) REFERENCES bank_exams(bank_exam_id)
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS bank_session_questions (
                    session_id INTEGER NOT NULL,
                    qb_id      INTEGER NOT NULL,
                    seq_num    INTEGER NOT NULL,
                    PRIMARY KEY (session_id, qb_id)
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS bank_responses (
                    response_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id      INTEGER NOT NULL,
                    qb_id           INTEGER NOT NULL,
                    selected_answer TEXT,
                    marked_review   BOOLEAN DEFAULT 0,
                    is_visited      BOOLEAN DEFAULT 0,
                    answered_at     TIMESTAMP
                )""")

            # Backward-compat view: user_seen_questions → student_q_history
            conn.execute("""
                CREATE VIEW IF NOT EXISTS user_seen_questions AS
                SELECT history_id, user_id, qb_id AS question_id, subject, seen_at
                FROM student_q_history
            """)

            # Indexes
            for sql in [
                "CREATE INDEX IF NOT EXISTS idx_qb_subject    ON question_bank(subject)",
                "CREATE INDEX IF NOT EXISTS idx_qb_exam_type  ON question_bank(exam_type)",
                "CREATE INDEX IF NOT EXISTS idx_qb_difficulty ON question_bank(difficulty)",
                "CREATE INDEX IF NOT EXISTS idx_qb_topic      ON question_bank(topic)",
                "CREATE INDEX IF NOT EXISTS idx_sqh_user      ON student_q_history(user_id, subject)",
                "CREATE INDEX IF NOT EXISTS idx_bsq_session   ON bank_session_questions(session_id)",
                # Prevent duplicate question text per subject
                "CREATE UNIQUE INDEX IF NOT EXISTS idx_qb_unique_question ON question_bank(subject, LOWER(TRIM(question_en)))",
            ]:
                conn.execute(sql)

            conn.commit()
            print("✅ Question bank DB initialized")
        except Exception as e:
            conn.rollback()
            raise e

    # Initialize recycling tables
    try:
        with _bank_lock:
            _create_recycle_tables(conn)
            conn.execute("COMMIT")
    except Exception:
        try:
            conn.execute("ROLLBACK")
        except Exception:
            pass

    # Migrate: add explanation columns for each language if missing
    _migrate_add_explanation_columns(conn)


def _migrate_add_explanation_columns(conn):
    """Add explanation_{lang} columns if they don't exist yet (migration for old DBs)."""
    langs = ["hi", "mr", "ta", "te", "gu", "bn", "kn", "or"]
    try:
        existing = {row[1] for row in conn.execute("PRAGMA table_info(question_bank)").fetchall()}
        with _bank_lock:
            for lang in langs:
                col = f"explanation_{lang}"
                if col not in existing:
                    try:
                        conn.execute(f"ALTER TABLE question_bank ADD COLUMN {col} TEXT")
                        conn.commit()
                    except Exception:
                        pass
    except Exception:
        pass


# ─── BANK STATISTICS ─────────────────────────────────────────────────────────

def get_bank_stats() -> Dict:
    conn = _bank_conn()
    with _bank_lock:
        total = conn.execute("SELECT COUNT(*) FROM question_bank").fetchone()[0]
        by_subject = conn.execute("""
            SELECT subject, difficulty, COUNT(*) as cnt
            FROM question_bank GROUP BY subject, difficulty
        """).fetchall()
    stats = {"total": total, "by_subject": {}}
    for row in by_subject:
        s = row["subject"]
        if s not in stats["by_subject"]:
            stats["by_subject"][s] = {}
        stats["by_subject"][s][row["difficulty"]] = row["cnt"]
    return stats


def get_subject_count(subject: str) -> int:
    conn = _bank_conn()
    with _bank_lock:
        return conn.execute(
            "SELECT COUNT(*) FROM question_bank WHERE subject=?", (subject,)
        ).fetchone()[0]


# ─── QUESTION INSERTION ───────────────────────────────────────────────────────

def bulk_insert_questions(questions: List[Dict]) -> int:
    """Insert a batch of questions. Returns count inserted."""
    conn = _bank_conn()
    inserted = 0
    with _bank_lock:
        conn.execute("BEGIN")
        try:
            for q in questions:
                conn.execute("""
                    INSERT OR IGNORE INTO question_bank
                        (subject, exam_type, topic, subtopic, difficulty,
                         question_en, option_a_en, option_b_en, option_c_en, option_d_en,
                         correct_answer, marks_correct, marks_wrong, explanation_en)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    q["subject"], q["exam_type"], q.get("topic", ""),
                    q.get("subtopic", ""), q.get("difficulty", "medium"),
                    q["question_en"],
                    q["option_a_en"], q["option_b_en"],
                    q["option_c_en"], q["option_d_en"],
                    q["correct_answer"],
                    q.get("marks_correct", 4.0),
                    q.get("marks_wrong", -1.0),
                    q.get("explanation_en", ""),
                ))
                inserted += 1
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Bulk insert error: {e}")
    return inserted


# ─── EXAM CREATION FROM BANK ──────────────────────────────────────────────────

def get_questions_for_exam(
    subject: str,
    count: int,
    user_id: int,
    difficulty_mix: Dict = None,
    exclude_ids: List[int] = None,
) -> List[Dict]:
    """
    Pull `count` UNIQUE questions for `subject` that this user hasn't seen.
    Guarantees: no duplicate qb_ids, no duplicate question texts within result.
    difficulty_mix = {"medium": 0.3, "hard": 0.4, "very_hard": 0.3}
    """
    conn = _bank_conn()
    exclude_ids = list(exclude_ids or [])

    # Get already-seen question IDs for this user+subject
    with _bank_lock:
        seen = [r[0] for r in conn.execute(
            "SELECT qb_id FROM student_q_history WHERE user_id=? AND subject=?",
            (user_id, subject)
        ).fetchall()]

    all_excluded = set(seen + exclude_ids)

    if difficulty_mix is None:
        difficulty_mix = {"medium": 0.30, "hard": 0.40, "very_hard": 0.30}

    result = []
    seen_texts = set()   # guard against any remaining duplicate question texts
    seen_result_ids = set()

    def _try_add(d: Dict) -> bool:
        qid = d["qb_id"]
        txt = (d.get("question_en") or "").strip().lower()
        if qid in all_excluded or qid in seen_result_ids:
            return False
        if txt and txt in seen_texts:
            return False
        result.append(d)
        seen_result_ids.add(qid)
        if txt:
            seen_texts.add(txt)
        return True

    for diff, ratio in difficulty_mix.items():
        needed = max(1, round(count * ratio))
        with _bank_lock:
            rows = conn.execute("""
                SELECT * FROM question_bank
                WHERE subject=? AND difficulty=?
                ORDER BY RANDOM()
                LIMIT ?
            """, (subject, diff, needed * 4)).fetchall()

        candidates = [dict(r) for r in rows]
        random.shuffle(candidates)
        for d in candidates:
            if len([q for q in result if q.get("difficulty") == diff]) >= needed:
                break
            _try_add(d)

    # Fill up if still short — pull from all difficulties
    if len(result) < count:
        with _bank_lock:
            extras = conn.execute("""
                SELECT * FROM question_bank
                WHERE subject=?
                ORDER BY RANDOM()
                LIMIT ?
            """, (subject, (count - len(result)) * 5)).fetchall()
        extras_list = [dict(r) for r in extras]
        random.shuffle(extras_list)
        for d in extras_list:
            if len(result) >= count:
                break
            _try_add(d)

    random.shuffle(result)
    return result[:count]


def mark_questions_seen(user_id: int, qb_ids: List[int], subject: str):
    """Record that user has seen these questions."""
    conn = _bank_conn()
    with _bank_lock:
        conn.execute("BEGIN")
        try:
            for qid in qb_ids:
                conn.execute(
                    "INSERT OR IGNORE INTO student_q_history (user_id, qb_id, subject) VALUES (?,?,?)",
                    (user_id, qid, subject)
                )
            conn.commit()
        except Exception as e:
            conn.rollback()


def get_user_seen_count(user_id: int, subject: str) -> int:
    conn = _bank_conn()
    with _bank_lock:
        return conn.execute(
            "SELECT COUNT(*) FROM student_q_history WHERE user_id=? AND subject=?",
            (user_id, subject)
        ).fetchone()[0]


# ─── TRANSLATION ──────────────────────────────────────────────────────────────

def save_translation(qb_id: int, lang: str, translations: Dict):
    """Save translated fields for a question."""
    conn = _bank_conn()
    fields = {
        f"question_{lang}": translations.get("question", ""),
        f"option_a_{lang}": translations.get("option_a", ""),
        f"option_b_{lang}": translations.get("option_b", ""),
        f"option_c_{lang}": translations.get("option_c", ""),
        f"option_d_{lang}": translations.get("option_d", ""),
    }
    set_clause = ", ".join(f"{k}=?" for k in fields)
    vals = list(fields.values())

    with _bank_lock:
        try:
            in_transaction = conn.in_transaction
            if not in_transaction:
                conn.execute("BEGIN")
            # Update translated_langs list
            row = conn.execute(
                "SELECT translated_langs FROM question_bank WHERE qb_id=?", (qb_id,)
            ).fetchone()
            langs = json.loads(row["translated_langs"] or "[]") if row else []
            if lang not in langs:
                langs.append(lang)

            conn.execute(
                f"UPDATE question_bank SET {set_clause}, translated_langs=? WHERE qb_id=?",
                vals + [json.dumps(langs), qb_id]
            )
            if not in_transaction:
                conn.commit()
        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass


def get_question_in_lang(qb_id: int, lang: str) -> Optional[Dict]:
    conn = _bank_conn()
    with _bank_lock:
        row = conn.execute(
            "SELECT * FROM question_bank WHERE qb_id=?", (qb_id,)
        ).fetchone()
    if not row:
        return None
    d = dict(row)
    if lang == "en":
        return d
    # Return translated if available, else English
    return {
        "qb_id": d["qb_id"],
        "subject": d["subject"],
        "difficulty": d["difficulty"],
        "question": d.get(f"question_{lang}") or d["question_en"],
        "option_a": d.get(f"option_a_{lang}") or d["option_a_en"],
        "option_b": d.get(f"option_b_{lang}") or d["option_b_en"],
        "option_c": d.get(f"option_c_{lang}") or d["option_c_en"],
        "option_d": d.get(f"option_d_{lang}") or d["option_d_en"],
        "correct_answer": d["correct_answer"],
        "marks_correct": d["marks_correct"],
        "marks_wrong": d["marks_wrong"],
        "explanation": d.get(f"explanation_{lang}") or d.get("explanation_en", ""),
        "topic": d.get("topic", ""),
    }


def questions_needing_translation(lang: str, limit: int = 100, subject: str = None) -> List[Dict]:
    """Return questions that haven't been translated to `lang` yet."""
    conn = _bank_conn()
    with _bank_lock:
        if subject:
            rows = conn.execute(f"""
                SELECT qb_id, question_en, option_a_en, option_b_en, option_c_en, option_d_en,
                       subject, topic
                FROM question_bank
                WHERE (question_{lang} IS NULL OR question_{lang} = '')
                  AND subject = ?
                LIMIT ?
            """, (subject, limit)).fetchall()
        else:
            rows = conn.execute(f"""
                SELECT qb_id, question_en, option_a_en, option_b_en, option_c_en, option_d_en,
                       subject, topic
                FROM question_bank
                WHERE question_{lang} IS NULL OR question_{lang} = ''
                LIMIT ?
            """, (limit,)).fetchall()
    return [dict(r) for r in rows]


def count_untranslated(lang: str) -> int:
    """Count questions not yet translated to lang."""
    conn = _bank_conn()
    with _bank_lock:
        return conn.execute(f"""
            SELECT COUNT(*) FROM question_bank
            WHERE question_{lang} IS NULL OR question_{lang} = ''
        """).fetchone()[0]


def count_translated(lang: str) -> int:
    """Count questions translated to lang."""
    conn = _bank_conn()
    with _bank_lock:
        return conn.execute(f"""
            SELECT COUNT(*) FROM question_bank
            WHERE question_{lang} IS NOT NULL AND question_{lang} != ''
        """).fetchone()[0]


def bulk_save_translations(translations_batch: list):
    """
    Save many translations at once for performance.
    translations_batch: list of (qb_id, lang, question, opt_a, opt_b, opt_c, opt_d)
    """
    conn = _bank_conn()
    if not translations_batch:
        return 0
    # Group by language
    by_lang = {}
    for item in translations_batch:
        qb_id, lang, q, a, b, c, d = item
        by_lang.setdefault(lang, []).append((qb_id, q, a, b, c, d))

    count = 0
    with _bank_lock:
        conn.execute("BEGIN")
        try:
            for lang, items in by_lang.items():
                for qb_id, q, a, b, c, d in items:
                    conn.execute(f"""
                        UPDATE question_bank SET
                            question_{lang}=?, option_a_{lang}=?, option_b_{lang}=?,
                            option_c_{lang}=?, option_d_{lang}=?
                        WHERE qb_id=?
                    """, (q, a, b, c, d, qb_id))
                    count += 1
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"bulk_save_translations error: {e}")
    return count


# ─── RECYCLING SYSTEM ─────────────────────────────────────────────────────────

def init_recycling_tables():
    """Create exam recycling tables."""
    conn = _bank_conn()
    with _bank_lock:
        conn.execute("BEGIN")
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS recycled_exam_pool (
                    recycle_id    INTEGER PRIMARY KEY AUTOINCREMENT,
                    qb_id         INTEGER NOT NULL,
                    subject       TEXT NOT NULL,
                    original_exam_id INTEGER,
                    recycled_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    times_recycled INTEGER DEFAULT 0,
                    UNIQUE(qb_id)
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS deleted_exams_log (
                    log_id        INTEGER PRIMARY KEY AUTOINCREMENT,
                    exam_name     TEXT,
                    exam_type     TEXT,
                    question_count INTEGER,
                    recycled_count INTEGER DEFAULT 0,
                    deleted_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS student_recycle_history (
                    history_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id     INTEGER NOT NULL,
                    qb_id       INTEGER NOT NULL,
                    recycled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(user_id, qb_id)
                )""")

            for sql in [
                "CREATE INDEX IF NOT EXISTS idx_recycle_subject ON recycled_exam_pool(subject)",
                "CREATE INDEX IF NOT EXISTS idx_recycle_qbid ON recycled_exam_pool(qb_id)",
                "CREATE INDEX IF NOT EXISTS idx_srh_user ON student_recycle_history(user_id)",
            ]:
                conn.execute(sql)
            conn.commit()
        except Exception as e:
            conn.rollback()


def recycle_exam_questions(qb_ids: List[int], subject: str,
                            exam_name: str = "", exam_type: str = "") -> int:
    """
    Move exam's questions into the recycled pool when exam is deleted.
    Returns count of questions added to recycle pool.
    """
    conn = _bank_conn()
    added = 0
    with _bank_lock:
        conn.execute("BEGIN")
        try:
            for qb_id in qb_ids:
                conn.execute("""
                    INSERT OR IGNORE INTO recycled_exam_pool (qb_id, subject)
                    VALUES (?,?)
                """, (qb_id, subject))
                added += 1

            # Log the deletion
            conn.execute("""
                INSERT INTO deleted_exams_log
                    (exam_name, exam_type, question_count, recycled_count)
                VALUES (?,?,?,?)
            """, (exam_name, exam_type, len(qb_ids), added))
            conn.commit()
        except Exception as e:
            conn.rollback()
    return added


def get_recycled_questions(subject: str, count: int,
                           user_id: int) -> List[Dict]:
    """
    Get questions from recycle pool that this user hasn't already done
    (from the recycled pool specifically).
    """
    conn = _bank_conn()
    # Get qb_ids already given to this user from recycle pool
    with _bank_lock:
        seen_recycled = set(r[0] for r in conn.execute("""
            SELECT qb_id FROM student_recycle_history WHERE user_id=?
        """, (user_id,)).fetchall())

        rows = conn.execute("""
            SELECT qb.*, rp.recycle_id
            FROM question_bank qb
            JOIN recycled_exam_pool rp ON qb.qb_id = rp.qb_id
            WHERE rp.subject = ?
            ORDER BY RANDOM()
            LIMIT ?
        """, (subject, count * 3)).fetchall()

    candidates = [dict(r) for r in rows if r["qb_id"] not in seen_recycled]
    random.shuffle(candidates)
    return candidates[:count]


def mark_recycled_seen(user_id: int, qb_ids: List[int]):
    """Record that student received these recycled questions."""
    conn = _bank_conn()
    with _bank_lock:
        conn.execute("BEGIN")
        try:
            for qb_id in qb_ids:
                conn.execute("""
                    INSERT OR IGNORE INTO student_recycle_history (user_id, qb_id)
                    VALUES (?,?)
                """, (user_id, qb_id))
                # Update times_recycled counter
                conn.execute("""
                    UPDATE recycled_exam_pool SET times_recycled = times_recycled + 1
                    WHERE qb_id = ?
                """, (qb_id,))
            conn.commit()
        except Exception as e:
            conn.rollback()


def get_recycle_pool_stats() -> Dict:
    """Stats on the recycle pool."""
    conn = _bank_conn()
    with _bank_lock:
        total = conn.execute(
            "SELECT COUNT(*) FROM recycled_exam_pool"
        ).fetchone()[0]
        by_subject = conn.execute("""
            SELECT subject, COUNT(*), AVG(times_recycled)
            FROM recycled_exam_pool GROUP BY subject
        """).fetchall()
        deleted_exams = conn.execute(
            "SELECT COUNT(*) FROM deleted_exams_log"
        ).fetchone()[0]
    return {
        "total_recycled": total,
        "deleted_exams": deleted_exams,
        "by_subject": {r[0]: {"count": r[1], "avg_reuses": round(r[2] or 0, 1)}
                       for r in by_subject},
    }


def add_to_recycle_pool(user_id: int, qb_id: int, subject: str,
                         source: str = "deleted_exam") -> bool:
    """
    Add a question to this user's personal recycle pool.
    Called when a student deletes an exam.
    Returns True if added, False if already in pool.
    """
    conn = _bank_conn()
    with _bank_lock:
        conn.execute("BEGIN")
        try:
            conn.execute("""
                INSERT OR IGNORE INTO exam_recycle_pool
                    (user_id, qb_id, subject, source, is_available)
                VALUES (?,?,?,?,1)
            """, (str(user_id), qb_id, subject, source))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            return False


def get_recycle_stats(user_id: int) -> Dict:
    """Get recycling statistics for a user."""
    conn = _bank_conn()
    with _bank_lock:
        available = conn.execute("""
            SELECT COUNT(*) FROM exam_recycle_pool
            WHERE user_id=? AND is_available=1
        """, (str(user_id),)).fetchone()[0]
        used = conn.execute("""
            SELECT COUNT(*) FROM exam_recycle_pool
            WHERE user_id=? AND is_available=0
        """, (str(user_id),)).fetchone()[0]
        by_subject_rows = conn.execute("""
            SELECT subject, COUNT(*) FROM exam_recycle_pool
            WHERE user_id=? AND is_available=1 GROUP BY subject
        """, (str(user_id),)).fetchall()
    return {
        "available": available,
        "used": used,
        "by_subject": {r[0]: r[1] for r in by_subject_rows},
    }


def get_questions_smart(subject: str, count: int, user_id: int,
                        difficulty_mix: Dict = None,
                        use_recycled: bool = True) -> List[Dict]:
    """
    Smart question fetcher: tries fresh pool first, fills gaps from recycle pool.
    This ensures no question is ever truly wasted.
    """
    qs = get_questions_for_exam(subject, count, user_id, difficulty_mix)

    if len(qs) < count and use_recycled:
        needed = count - len(qs)
        # Get from personal recycle pool (exam_recycle_pool table)
        conn = _bank_conn()
        already_fetched = {q["qb_id"] for q in qs}
        with _bank_lock:
            rows = conn.execute("""
                SELECT qb.* FROM question_bank qb
                JOIN exam_recycle_pool rp ON qb.qb_id = rp.qb_id
                WHERE rp.user_id=? AND rp.subject=? AND rp.is_available=1
                  AND qb.qb_id NOT IN ({})
                ORDER BY RANDOM()
                LIMIT ?
            """.format(",".join("?" * len(already_fetched)) if already_fetched else "0"),
            [str(user_id), subject] + list(already_fetched) + [needed]
            ).fetchall()
        recycled = [dict(r) for r in rows]
        for rq in recycled:
            rq["_from_recycle"] = True
        qs.extend(recycled)
        random.shuffle(qs)

    return qs[:count]
