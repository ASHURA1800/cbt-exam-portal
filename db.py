"""
db.py — Dual-Database Production Layer
========================================

TWO SEPARATE DATABASES:
  ┌─────────────────────────────────────────────────────────────────┐
  │  AUTH DB  →  ~/.cbt_auth/users.db  (PERSISTENT — outside proj) │
  │  Tables: users, login_sessions, login_attempts                  │
  │  Never overwritten by code updates. Survives reinstalls.        │
  ├─────────────────────────────────────────────────────────────────┤
  │  EXAM DB  →  ./cbt_exam.db  (project directory)                 │
  │  Tables: exams, questions, sessions, responses, results, etc.   │
  │  Can be replaced/reset without touching user accounts.          │
  └─────────────────────────────────────────────────────────────────┘

All public function signatures are IDENTICAL to before — app.py needs
zero changes. The split is entirely internal.
"""

import sqlite3
import hashlib
import json
import os
import secrets
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional

# ── Try bcrypt, fall back gracefully ─────────────────────────────────────────
try:
    import bcrypt
    _BCRYPT_OK = True
except ImportError:
    _BCRYPT_OK = False

# ══════════════════════════════════════════════════════════════════════════════
# DATABASE PATHS
# ══════════════════════════════════════════════════════════════════════════════

# EXAM DB — in project directory (replaceable during updates)
DATABASE_PATH = 'cbt_exam.db'

# AUTH DB — persistent, outside project directory, survives all code updates
_AUTH_DIR  = os.path.join(os.path.expanduser("~"), ".cbt_auth")
AUTH_DB_PATH = os.path.join(_AUTH_DIR, "users.db")

def _ensure_auth_dir():
    """Create the persistent auth directory if it doesn't exist."""
    os.makedirs(_AUTH_DIR, exist_ok=True)

# ══════════════════════════════════════════════════════════════════════════════
# SEPARATE LOCKS — auth and exam never block each other
# ══════════════════════════════════════════════════════════════════════════════
_auth_lock = threading.Lock()
_exam_lock = threading.Lock()

# Legacy alias kept for any code that imported db_lock directly
db_lock = _exam_lock

# ══════════════════════════════════════════════════════════════════════════════
# CONNECTION POOLS — one per thread, one per database
# ══════════════════════════════════════════════════════════════════════════════
_auth_local = threading.local()
_exam_local = threading.local()

def _make_conn(path: str):
    """Create a tuned SQLite connection."""
    conn = sqlite3.connect(path, check_same_thread=False, timeout=20, isolation_level="")
    conn.row_factory = sqlite3.Row
    conn.isolation_level = None      # autocommit for PRAGMAs
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA foreign_keys=ON")
    conn.execute("PRAGMA cache_size=-16000")
    conn.isolation_level = ""        # deferred — Python manages BEGIN/COMMIT
    return conn

def _auth_conn():
    """Return thread-local connection to the persistent AUTH database."""
    if not getattr(_auth_local, 'conn', None):
        _ensure_auth_dir()
        _auth_local.conn = _make_conn(AUTH_DB_PATH)
    return _auth_local.conn

def _exam_conn():
    """Return thread-local connection to the EXAM database."""
    if not getattr(_exam_local, 'conn', None):
        _exam_local.conn = _make_conn(DATABASE_PATH)
    return _exam_local.conn

# Legacy alias — exam functions that still call get_connection()
def get_connection():
    return _exam_conn()

# ══════════════════════════════════════════════════════════════════════════════
# PASSWORD HASHING
# ══════════════════════════════════════════════════════════════════════════════

def hash_password(password: str) -> str:
    if _BCRYPT_OK:
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()
    salt = secrets.token_hex(16)
    h = hashlib.sha256((salt + password).encode()).hexdigest()
    return f"sha256${salt}${h}"

def verify_password(password: str, stored_hash: str) -> bool:
    try:
        if stored_hash.startswith("sha256$"):
            _, salt, h = stored_hash.split("$")
            return hashlib.sha256((salt + password).encode()).hexdigest() == h
        if stored_hash.startswith("$2"):
            if _BCRYPT_OK:
                return bcrypt.checkpw(password.encode(), stored_hash.encode())
        # Legacy: plain sha256 (old data)
        return hashlib.sha256(password.encode()).hexdigest() == stored_hash
    except Exception:
        return False

def _normalize_dob(dob: str) -> str:
    """
    Normalize any DOB input to 8-digit string DDMMYYYY for storage & comparison.
    Accepts: 25072006  /  25/07/2006  /  25-07-2006  /  2006-07-25 (ISO)
    Always returns exactly 8 digits, e.g. '25072006', or '' if unparseable.
    """
    if not dob:
        return ''
    # Strip all non-digit characters
    digits = ''.join(c for c in dob.strip() if c.isdigit())
    if len(digits) == 8:
        return digits          # already DDMMYYYY
    # Handle ISO format YYYYMMDD → reorder to DDMMYYYY
    if len(digits) == 8:
        return digits
    return ''

# ══════════════════════════════════════════════════════════════════════════════
# AUTH DB INITIALISATION  (users, login_sessions, login_attempts)
# ══════════════════════════════════════════════════════════════════════════════

def _init_auth_db():
    """Create auth tables in the persistent auth database."""
    _ensure_auth_dir()
    conn = _auth_conn()
    with _auth_lock:
        conn.execute("BEGIN")
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    username        TEXT    UNIQUE NOT NULL,
                    email           TEXT,
                    password_hash   TEXT    NOT NULL DEFAULT 'DOB_AUTH',
                    date_of_birth   TEXT,
                    full_name       TEXT,
                    preferred_lang  TEXT    DEFAULT 'en',
                    user_type       TEXT    DEFAULT 'student',
                    is_admin        BOOLEAN DEFAULT 0,
                    is_deleted      BOOLEAN DEFAULT 0,
                    failed_attempts INTEGER DEFAULT 0,
                    locked_until    TIMESTAMP,
                    last_login_ip   TEXT,
                    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS login_sessions (
                    token      TEXT    PRIMARY KEY,
                    user_id    INTEGER NOT NULL,
                    ip_address TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    is_active  BOOLEAN DEFAULT 1,
                    FOREIGN KEY (user_id) REFERENCES users(user_id)
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS login_attempts (
                    attempt_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                    username     TEXT,
                    ip_address   TEXT,
                    success      BOOLEAN,
                    attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")

            # Indexes on auth DB
            conn.execute("CREATE INDEX IF NOT EXISTS idx_auth_username  ON users(username)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_auth_tok_user  ON login_sessions(user_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_auth_attempts  ON login_attempts(username)")

            # Default admin (only if no admin exists yet)
            # Login: username=admin, Date of Birth=25/06/2007
            count = conn.execute(
                "SELECT COUNT(*) FROM users WHERE user_type='admin'"
            ).fetchone()[0]
            if count == 0:
                conn.execute("""
                    INSERT INTO users
                        (username, password_hash, date_of_birth,
                         full_name, user_type, is_admin)
                    VALUES ('admin', 'DOB_AUTH', '25062007',
                            'System Administrator', 'admin', 1)
                """)
            else:
                # Migrate existing admin to DOB-based auth
                conn.execute("""
                    UPDATE users
                    SET password_hash='DOB_AUTH', date_of_birth='25062007'
                    WHERE username='admin' AND user_type='admin'
                      AND (date_of_birth IS NULL OR date_of_birth='')
                """)

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e

def _migrate_auth_db():
    """Add any missing columns to the persistent auth DB."""
    conn = _auth_conn()
    with _auth_lock:
        conn.execute("BEGIN")
        try:
            cols = [r[1] for r in conn.execute("PRAGMA table_info(users)").fetchall()]
            for col, defn in [
                ("is_deleted",      "BOOLEAN DEFAULT 0"),
                ("failed_attempts", "INTEGER DEFAULT 0"),
                ("locked_until",    "TIMESTAMP"),
                ("last_login_ip",   "TEXT"),
                ("email",           "TEXT"),
            ]:
                if col not in cols:
                    conn.execute(f"ALTER TABLE users ADD COLUMN {col} {defn}")

            # Ensure login tables exist
            conn.execute("""CREATE TABLE IF NOT EXISTS login_sessions (
                token TEXT PRIMARY KEY, user_id INTEGER NOT NULL,
                ip_address TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL, is_active BOOLEAN DEFAULT 1)""")
            conn.execute("""CREATE TABLE IF NOT EXISTS login_attempts (
                attempt_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT,
                ip_address TEXT, success BOOLEAN,
                attempted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")

            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Auth migration warning: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# EXAM DB INITIALISATION  (everything except users/auth)
# ══════════════════════════════════════════════════════════════════════════════

def _init_exam_db():
    """Create all exam-related tables in cbt_exam.db."""
    conn = _exam_conn()
    with _exam_lock:
        conn.execute("BEGIN")
        try:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS exams (
                    exam_id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    exam_name         TEXT    NOT NULL,
                    exam_name_hi      TEXT,
                    exam_type         TEXT    DEFAULT 'JEE',
                    total_questions   INTEGER NOT NULL,
                    duration_mins     INTEGER NOT NULL,
                    max_duration_mins INTEGER,
                    marking_scheme    TEXT,
                    instructions_en   TEXT,
                    instructions_hi   TEXT,
                    is_active         BOOLEAN DEFAULT 1,
                    is_deleted        BOOLEAN DEFAULT 0,
                    created_by        INTEGER,
                    created_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    question_id      INTEGER PRIMARY KEY AUTOINCREMENT,
                    exam_id          INTEGER NOT NULL,
                    subject          TEXT    NOT NULL,
                    subject_hi       TEXT,
                    question_text_en TEXT    NOT NULL,
                    question_text_hi TEXT,
                    option_a_en TEXT NOT NULL, option_a_hi TEXT,
                    option_b_en TEXT NOT NULL, option_b_hi TEXT,
                    option_c_en TEXT NOT NULL, option_c_hi TEXT,
                    option_d_en TEXT NOT NULL, option_d_hi TEXT,
                    question_text_mr TEXT, question_text_ta TEXT,
                    question_text_te TEXT, question_text_gu TEXT,
                    question_text_bn TEXT, question_text_kn TEXT,
                    option_a_mr TEXT, option_a_ta TEXT, option_a_te TEXT,
                    option_a_gu TEXT, option_a_bn TEXT, option_a_kn TEXT,
                    option_b_mr TEXT, option_b_ta TEXT, option_b_te TEXT,
                    option_b_gu TEXT, option_b_bn TEXT, option_b_kn TEXT,
                    option_c_mr TEXT, option_c_ta TEXT, option_c_te TEXT,
                    option_c_gu TEXT, option_c_bn TEXT, option_c_kn TEXT,
                    option_d_mr TEXT, option_d_ta TEXT, option_d_te TEXT,
                    option_d_gu TEXT, option_d_bn TEXT, option_d_kn TEXT,
                    correct_answer   TEXT    NOT NULL,
                    marks_correct    REAL    DEFAULT 4.0,
                    marks_wrong      REAL    DEFAULT -1.0,
                    difficulty       TEXT    DEFAULT 'medium',
                    question_type    TEXT    DEFAULT 'mcq',
                    seq_number       INTEGER NOT NULL,
                    is_deleted       BOOLEAN DEFAULT 0,
                    FOREIGN KEY (exam_id) REFERENCES exams(exam_id)
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS exam_sessions (
                    session_id           INTEGER PRIMARY KEY AUTOINCREMENT,
                    attempt_id           TEXT    UNIQUE,
                    user_id              INTEGER NOT NULL,
                    exam_id              INTEGER NOT NULL,
                    start_time           TIMESTAMP NOT NULL,
                    end_time             TIMESTAMP,
                    actual_end_time      TIMESTAMP,
                    selected_language    TEXT    DEFAULT 'en',
                    status               TEXT    DEFAULT 'in_progress',
                    total_score          REAL    DEFAULT 0,
                    result_locked        BOOLEAN DEFAULT 0,
                    current_question_idx INTEGER DEFAULT 0,
                    submission_ip        TEXT,
                    FOREIGN KEY (exam_id) REFERENCES exams(exam_id)
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS session_questions (
                    session_id  INTEGER NOT NULL,
                    question_id INTEGER NOT NULL,
                    seq_number  INTEGER NOT NULL,
                    PRIMARY KEY (session_id, question_id),
                    FOREIGN KEY (session_id)  REFERENCES exam_sessions(session_id),
                    FOREIGN KEY (question_id) REFERENCES questions(question_id)
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS responses (
                    response_id       INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id        INTEGER NOT NULL,
                    question_id       INTEGER NOT NULL,
                    selected_answer   TEXT,
                    marked_for_review BOOLEAN DEFAULT 0,
                    is_visited        BOOLEAN DEFAULT 0,
                    time_spent        INTEGER DEFAULT 0,
                    answer_changed    INTEGER DEFAULT 0,
                    answered_at       TIMESTAMP,
                    FOREIGN KEY (session_id)  REFERENCES exam_sessions(session_id),
                    FOREIGN KEY (question_id) REFERENCES questions(question_id)
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS answer_history (
                    history_id  INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id  INTEGER NOT NULL,
                    question_id INTEGER NOT NULL,
                    old_answer  TEXT,
                    new_answer  TEXT,
                    changed_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS results (
                    result_id         INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id        INTEGER UNIQUE NOT NULL,
                    user_id           INTEGER NOT NULL,
                    exam_id           INTEGER NOT NULL,
                    total_score       REAL    NOT NULL,
                    correct_count     INTEGER NOT NULL,
                    wrong_count       INTEGER NOT NULL,
                    unattempted_count INTEGER NOT NULL,
                    section_scores    TEXT,
                    submitted_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_locked         BOOLEAN DEFAULT 1,
                    FOREIGN KEY (session_id) REFERENCES exam_sessions(session_id)
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS anti_cheat_log (
                    log_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER,
                    user_id    INTEGER,
                    event_type TEXT,
                    detail     TEXT,
                    ip_address TEXT,
                    logged_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS admin_audit_log (
                    audit_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                    admin_id     INTEGER NOT NULL,
                    action       TEXT    NOT NULL,
                    target_type  TEXT,
                    target_id    INTEGER,
                    detail       TEXT,
                    ip_address   TEXT,
                    performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS exam_analytics (
                    analytics_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id       INTEGER NOT NULL,
                    analytics_data   TEXT,
                    percentile       REAL    DEFAULT 0,
                    rank_position    INTEGER DEFAULT 0,
                    tab_switches     INTEGER DEFAULT 0,
                    fullscreen_exits INTEGER DEFAULT 0,
                    created_at       TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (session_id) REFERENCES exam_sessions(session_id)
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS leaderboard (
                    leaderboard_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id        INTEGER NOT NULL,
                    exam_id        INTEGER NOT NULL,
                    score          REAL    NOT NULL,
                    rank_position  INTEGER,
                    percentile     REAL,
                    attempt_date   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (exam_id) REFERENCES exams(exam_id)
                )""")

            conn.execute("""
                CREATE TABLE IF NOT EXISTS question_topics (
                    question_id      INTEGER NOT NULL,
                    topic            TEXT,
                    subtopic         TEXT,
                    difficulty_level TEXT,
                    FOREIGN KEY (question_id) REFERENCES questions(question_id)
                )""")

            # Indexes on exam DB
            for sql in [
                "CREATE INDEX IF NOT EXISTS idx_sessions_user    ON exam_sessions(user_id)",
                "CREATE INDEX IF NOT EXISTS idx_sessions_exam    ON exam_sessions(exam_id)",
                "CREATE INDEX IF NOT EXISTS idx_sessions_status  ON exam_sessions(status)",
                "CREATE INDEX IF NOT EXISTS idx_responses_session ON responses(session_id)",
                "CREATE INDEX IF NOT EXISTS idx_responses_qid    ON responses(session_id, question_id)",
                "CREATE INDEX IF NOT EXISTS idx_sq_session       ON session_questions(session_id)",
                "CREATE INDEX IF NOT EXISTS idx_questions_exam   ON questions(exam_id)",
                "CREATE INDEX IF NOT EXISTS idx_results_session  ON results(session_id)",
                "CREATE INDEX IF NOT EXISTS idx_cheat_session    ON anti_cheat_log(session_id)",
            ]:
                conn.execute(sql)

            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e

def _migrate_exam_db():
    """Add missing columns to exam DB."""
    conn = _exam_conn()
    with _exam_lock:
        conn.execute("BEGIN")
        try:
            def _cols(tbl):
                return [r[1] for r in conn.execute(f"PRAGMA table_info({tbl})").fetchall()]

            sc = _cols("exam_sessions")
            for col, defn in [
                ("attempt_id",           "TEXT"),
                ("result_locked",        "BOOLEAN DEFAULT 0"),
                ("current_question_idx", "INTEGER DEFAULT 0"),
                ("submission_ip",        "TEXT"),
                ("end_time",             "TIMESTAMP"),
                ("actual_end_time",      "TIMESTAMP"),
            ]:
                if col not in sc:
                    conn.execute(f"ALTER TABLE exam_sessions ADD COLUMN {col} {defn}")

            ec = _cols("exams")
            for col, defn in [("is_deleted","BOOLEAN DEFAULT 0"),("created_by","INTEGER")]:
                if col not in ec:
                    conn.execute(f"ALTER TABLE exams ADD COLUMN {col} {defn}")

            qc = _cols("questions")
            if "is_deleted" not in qc:
                conn.execute("ALTER TABLE questions ADD COLUMN is_deleted BOOLEAN DEFAULT 0")
            for lang in ['mr','ta','te','gu','bn','kn']:
                for fld in ['question_text','option_a','option_b','option_c','option_d']:
                    cn = f"{fld}_{lang}"
                    if cn not in qc:
                        conn.execute(f"ALTER TABLE questions ADD COLUMN {cn} TEXT")

            rc = _cols("responses")
            for col, defn in [("is_visited","BOOLEAN DEFAULT 0"),("answer_changed","INTEGER DEFAULT 0")]:
                if col not in rc:
                    conn.execute(f"ALTER TABLE responses ADD COLUMN {col} {defn}")

            # Ensure newer tables exist in older DBs
            conn.execute("""CREATE TABLE IF NOT EXISTS answer_history (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER NOT NULL, question_id INTEGER NOT NULL,
                old_answer TEXT, new_answer TEXT,
                changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
            conn.execute("""CREATE TABLE IF NOT EXISTS results (
                result_id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id INTEGER UNIQUE NOT NULL,
                user_id INTEGER NOT NULL, exam_id INTEGER NOT NULL,
                total_score REAL NOT NULL, correct_count INTEGER NOT NULL,
                wrong_count INTEGER NOT NULL, unattempted_count INTEGER NOT NULL,
                section_scores TEXT, submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                is_locked BOOLEAN DEFAULT 1)""")
            conn.execute("""CREATE TABLE IF NOT EXISTS anti_cheat_log (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT, session_id INTEGER,
                user_id INTEGER, event_type TEXT, detail TEXT,
                ip_address TEXT, logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
            conn.execute("""CREATE TABLE IF NOT EXISTS admin_audit_log (
                audit_id INTEGER PRIMARY KEY AUTOINCREMENT, admin_id INTEGER NOT NULL,
                action TEXT NOT NULL, target_type TEXT, target_id INTEGER,
                detail TEXT, ip_address TEXT,
                performed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)""")
            conn.commit()
        except Exception as e:
            conn.rollback()
            print(f"Exam migration warning: {e}")

# ══════════════════════════════════════════════════════════════════════════════
# MIGRATE EXISTING USERS FROM OLD SINGLE DB  (one-time, safe to re-run)
# ══════════════════════════════════════════════════════════════════════════════

def _migrate_users_from_old_db():
    """
    If the old cbt_exam.db has a users table, copy all users to the new
    persistent auth DB, then mark old DB users as migrated (does not delete them).
    Safe to re-run — uses INSERT OR IGNORE so no duplicates.
    """
    old_path = DATABASE_PATH
    if not os.path.exists(old_path):
        return
    try:
        old = sqlite3.connect(old_path)
        old.row_factory = sqlite3.Row
        # Check if users table exists in old DB
        tbl = old.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='users'"
        ).fetchone()
        if not tbl:
            old.close()
            return
        users = old.execute("SELECT * FROM users").fetchall()
        if not users:
            old.close()
            return

        auth = _auth_conn()
        migrated = 0
        with _auth_lock:
            auth.execute("BEGIN")
            for u in users:
                try:
                    auth.execute("""
                        INSERT OR IGNORE INTO users
                            (username, password_hash, date_of_birth, full_name,
                             preferred_lang, user_type, is_admin, is_deleted,
                             failed_attempts, locked_until, last_login_ip, created_at)
                        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
                    """, (
                        u['username'], u['password_hash'],
                        u['date_of_birth'] if 'date_of_birth' in u.keys() else None,
                        u['full_name'],
                        u['preferred_lang'] if 'preferred_lang' in u.keys() else 'en',
                        u['user_type'] if 'user_type' in u.keys() else 'student',
                        u['is_admin'] if 'is_admin' in u.keys() else 0,
                        u['is_deleted'] if 'is_deleted' in u.keys() else 0,
                        u['failed_attempts'] if 'failed_attempts' in u.keys() else 0,
                        u['locked_until'] if 'locked_until' in u.keys() else None,
                        u['last_login_ip'] if 'last_login_ip' in u.keys() else None,
                        u['created_at'] if 'created_at' in u.keys() else None,
                    ))
                    migrated += 1
                except Exception:
                    pass
            auth.commit()
        old.close()
        if migrated:
            print(f"✅ Migrated {migrated} user(s) from old DB to persistent auth DB")
    except Exception as e:
        print(f"User migration (non-fatal): {e}")

# ══════════════════════════════════════════════════════════════════════════════
# PUBLIC INIT FUNCTIONS  (called from app.py — same names as before)
# ══════════════════════════════════════════════════════════════════════════════

def init_database():
    """Initialise both databases. Called once at app startup."""
    _init_auth_db()
    _init_exam_db()
    _migrate_users_from_old_db()

def migrate_database():
    """Apply schema migrations to both databases. Safe to re-run."""
    _migrate_auth_db()
    _migrate_exam_db()
    print("✅ Migration complete")

# ══════════════════════════════════════════════════════════════════════════════
# USER / AUTH FUNCTIONS  — all use _auth_conn() / _auth_lock
# ══════════════════════════════════════════════════════════════════════════════

def create_user(username: str, password: str, full_name: str, dob: str = None,
                lang: str = 'en', user_type: str = 'student',
                email: str = '') -> Tuple[bool, str]:
    """
    Create user. For DOB-based auth, pass dob in DD/MM/YYYY format.
    password param kept for backward-compat but ignored — DOB is the credential.
    """
    username = username.strip().lower()
    if not username or len(username) < 3:
        return False, "Username must be at least 3 characters"
    # Validate & normalize DOB — accept DDMMYYYY or DD/MM/YYYY or DD-MM-YYYY
    if dob:
        norm = _normalize_dob(dob)
        if len(norm) != 8:
            return False, "Date of birth must be 8 digits: DDMMYYYY or DD/MM/YYYY"
        # Validate it's a real date (DDMMYYYY)
        try:
            datetime(int(norm[4:8]), int(norm[2:4]), int(norm[0:2]))
        except Exception:
            return False, "Invalid date — please check day, month and year"
        dob = norm   # store normalized (digits only)
    with _auth_lock:
        conn = _auth_conn()
        try:
            conn.execute("BEGIN")
            conn.execute("""
                INSERT INTO users
                    (username, email, password_hash, date_of_birth, full_name,
                     preferred_lang, user_type, is_admin)
                VALUES (?,?,?,?,?,?,?,?)
            """, (username, email.strip().lower() if email else '',
                  'DOB_AUTH', dob if dob else '',
                  full_name, lang, user_type,
                  1 if user_type == 'admin' else 0))
            conn.commit()
            return True, "User created successfully"
        except sqlite3.IntegrityError:
            conn.rollback()
            return False, "Username already exists"
        except Exception as e:
            conn.rollback()
            return False, str(e)

_MAX_FAIL = 5
_LOCK_MIN  = 15

def authenticate_user(username: str, password: str,
                      ip_address: str = "unknown") -> Optional[Dict]:
    """
    DOB-based authentication.
    'password' param = the date_of_birth entered by user (DD/MM/YYYY).
    Kept as 'password' for full backward-compat with all existing app.py call sites.
    """
    return _authenticate_dob(username.strip(), password.strip(), ip_address)

def _authenticate_dob(username: str, dob_entered: str,
                      ip_address: str = "unknown") -> Optional[Dict]:
    """Auth with DOB as credential + lockout protection."""
    username = username.strip().lower()
    with _auth_lock:
        conn = _auth_conn()
        try:
            row = conn.execute(
                "SELECT * FROM users WHERE username=? AND is_deleted=0",
                (username,)
            ).fetchone()

            # Log attempt
            conn.execute("BEGIN")
            conn.execute("""
                INSERT INTO login_attempts (username, ip_address, success)
                VALUES (?,?,0)
            """, (username, ip_address))

            if not row:
                conn.commit()
                return None

            user = dict(row)

            # Check lockout
            if user.get('locked_until'):
                try:
                    lt = datetime.fromisoformat(str(user['locked_until']))
                    if datetime.now() < lt:
                        conn.commit()
                        return {"_locked": True, "locked_until": str(lt)}
                except Exception:
                    pass

            # Normalize both sides to pure digits DDMMYYYY before comparing
            # This makes 25/07/2006, 25072006, 25-07-2006 all equivalent
            stored_dob = _normalize_dob(user.get('date_of_birth') or '')
            entered    = _normalize_dob(dob_entered)
            if not entered or stored_dob != entered:
                fails = (user.get('failed_attempts') or 0) + 1
                if fails >= _MAX_FAIL:
                    locked_until = (datetime.now() + timedelta(minutes=_LOCK_MIN)).isoformat()
                    conn.execute(
                        "UPDATE users SET failed_attempts=?, locked_until=? WHERE user_id=?",
                        (fails, locked_until, user['user_id'])
                    )
                else:
                    conn.execute(
                        "UPDATE users SET failed_attempts=? WHERE user_id=?",
                        (fails, user['user_id'])
                    )
                conn.commit()
                return None

            # Success — reset fail counter
            conn.execute("""
                UPDATE users SET failed_attempts=0, locked_until=NULL, last_login_ip=?
                WHERE user_id=?
            """, (ip_address, user['user_id']))
            conn.execute("""
                UPDATE login_attempts SET success=1
                WHERE attempt_id=(SELECT MAX(attempt_id) FROM login_attempts WHERE username=?)
            """, (username,))
            conn.commit()
            return {k: user[k] for k in
                    ['user_id','username','full_name','preferred_lang','user_type','is_admin']}
        except Exception as e:
            try: conn.rollback()
            except Exception: pass
            print(f"Auth error: {e}")
            return None

def issue_login_token(user_id: int, ip: str = "unknown") -> str:
    """Issue session token, invalidate previous tokens for this user."""
    token   = secrets.token_urlsafe(32)
    expires = (datetime.now() + timedelta(hours=12)).isoformat()
    with _auth_lock:
        conn = _auth_conn()
        conn.execute("BEGIN")
        conn.execute("UPDATE login_sessions SET is_active=0 WHERE user_id=?", (user_id,))
        conn.execute("""
            INSERT INTO login_sessions (token, user_id, ip_address, expires_at)
            VALUES (?,?,?,?)
        """, (token, user_id, ip, expires))
        conn.commit()
    return token

def validate_login_token(token: str) -> Optional[int]:
    """Return user_id if token is valid and not expired, else None."""
    with _auth_lock:
        conn = _auth_conn()
        row = conn.execute(
            "SELECT user_id, expires_at FROM login_sessions WHERE token=? AND is_active=1",
            (token,)
        ).fetchone()
    if not row:
        return None
    try:
        if datetime.now() > datetime.fromisoformat(str(row['expires_at'])):
            return None
    except Exception:
        return None
    return row['user_id']

def revoke_login_token(token: str):
    with _auth_lock:
        conn = _auth_conn()
        conn.execute("BEGIN")
        conn.execute("UPDATE login_sessions SET is_active=0 WHERE token=?", (token,))
        conn.commit()

def get_all_users() -> List[Dict]:
    with _auth_lock:
        conn = _auth_conn()
        rows = conn.execute("""
            SELECT user_id, username, full_name, user_type,
                   preferred_lang, is_admin, created_at
            FROM users WHERE is_deleted=0 ORDER BY created_at DESC
        """).fetchall()
    return [dict(r) for r in rows]

def delete_user(user_id: int) -> Tuple[bool, str]:
    """Soft-delete user (non-admin only)."""
    with _auth_lock:
        conn = _auth_conn()
        conn.execute("BEGIN")
        try:
            conn.execute(
                "UPDATE users SET is_deleted=1 WHERE user_id=? AND is_admin=0",
                (user_id,)
            )
            conn.commit()
            return True, "User deleted"
        except Exception as e:
            conn.rollback()
            return False, str(e)

def get_user_by_id(user_id: int) -> Optional[Dict]:
    with _auth_lock:
        conn = _auth_conn()
        row = conn.execute(
            "SELECT * FROM users WHERE user_id=? AND is_deleted=0",
            (user_id,)
        ).fetchone()
    return dict(row) if row else None

# ══════════════════════════════════════════════════════════════════════════════
# EXAM FUNCTIONS  — all use _exam_conn() / _exam_lock
# ══════════════════════════════════════════════════════════════════════════════

def create_exam(exam_data: Dict) -> Tuple[bool, int]:
    with _exam_lock:
        conn = _exam_conn()
        conn.execute("BEGIN")
        try:
            cur = conn.execute("""
                INSERT INTO exams
                    (exam_name, exam_name_hi, exam_type, total_questions,
                     duration_mins, max_duration_mins, marking_scheme,
                     instructions_en, instructions_hi, created_by)
                VALUES (?,?,?,?,?,?,?,?,?,?)
            """, (exam_data['exam_name'], exam_data.get('exam_name_hi'),
                  exam_data.get('exam_type','JEE'), exam_data['total_questions'],
                  exam_data['duration_mins'],
                  exam_data.get('max_duration_mins', exam_data['duration_mins']+5),
                  exam_data.get('marking_scheme'), exam_data.get('instructions_en'),
                  exam_data.get('instructions_hi'), exam_data.get('created_by')))
            exam_id = cur.lastrowid
            conn.commit()
            return True, exam_id
        except Exception as e:
            conn.rollback()
            return False, 0

def get_active_exams() -> List[Dict]:
    with _exam_lock:
        conn = _exam_conn()
        rows = conn.execute(
            "SELECT * FROM exams WHERE is_active=1 AND is_deleted=0 ORDER BY created_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]

def get_student_exams(user_id: int) -> List[Dict]:
    with _exam_lock:
        conn = _exam_conn()
        rows = conn.execute("""
            SELECT * FROM exams
            WHERE is_active=1 AND is_deleted=0
              AND (created_by=?
                   OR (created_by IS NULL AND exam_name NOT LIKE 'Admin Test%'))
            ORDER BY created_at DESC
        """, (user_id,)).fetchall()
    return [dict(r) for r in rows]

def get_all_exams() -> List[Dict]:
    with _exam_lock:
        conn = _exam_conn()
        rows = conn.execute(
            "SELECT * FROM exams WHERE is_deleted=0 ORDER BY created_at DESC"
        ).fetchall()
    return [dict(r) for r in rows]

def get_exam(exam_id: int) -> Optional[Dict]:
    with _exam_lock:
        conn = _exam_conn()
        row = conn.execute(
            "SELECT * FROM exams WHERE exam_id=? AND is_deleted=0", (exam_id,)
        ).fetchone()
    return dict(row) if row else None

def delete_exam(exam_id: int, admin_id: int = 0) -> Tuple[bool, str]:
    """Soft-delete. Blocks if live sessions exist."""
    with _exam_lock:
        conn = _exam_conn()
        conn.execute("BEGIN")
        try:
            live = conn.execute("""
                SELECT COUNT(*) FROM exam_sessions
                WHERE exam_id=? AND status='in_progress'
            """, (exam_id,)).fetchone()[0]
            if live > 0:
                conn.rollback()
                return False, f"Cannot delete: {live} student(s) currently taking this exam"
            conn.execute(
                "UPDATE exams SET is_deleted=1, is_active=0 WHERE exam_id=?", (exam_id,)
            )
            _exam_audit(conn, admin_id, "delete_exam", "exam", exam_id, "soft-deleted")
            conn.commit()
            return True, "Exam deleted"
        except Exception as e:
            conn.rollback()
            return False, str(e)

def deactivate_exam(exam_id: int) -> bool:
    with _exam_lock:
        conn = _exam_conn()
        conn.execute("BEGIN")
        try:
            conn.execute("UPDATE exams SET is_active=0 WHERE exam_id=?", (exam_id,))
            conn.commit()
            return True
        except Exception:
            conn.rollback()
            return False

def insert_questions(exam_id: int, questions: List[Dict]) -> Tuple[bool, str]:
    with _exam_lock:
        conn = _exam_conn()
        conn.execute("BEGIN")
        try:
            for q in questions:
                conn.execute("""
                    INSERT INTO questions (
                        exam_id, subject, subject_hi,
                        question_text_en, question_text_hi,
                        option_a_en, option_a_hi, option_b_en, option_b_hi,
                        option_c_en, option_c_hi, option_d_en, option_d_hi,
                        question_text_mr, question_text_ta, question_text_te,
                        question_text_gu, question_text_bn, question_text_kn,
                        option_a_mr, option_a_ta, option_a_te, option_a_gu,
                        option_a_bn, option_a_kn,
                        option_b_mr, option_b_ta, option_b_te, option_b_gu,
                        option_b_bn, option_b_kn,
                        option_c_mr, option_c_ta, option_c_te, option_c_gu,
                        option_c_bn, option_c_kn,
                        option_d_mr, option_d_ta, option_d_te, option_d_gu,
                        option_d_bn, option_d_kn,
                        correct_answer, marks_correct, marks_wrong,
                        difficulty, question_type, seq_number
                    ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                              ?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """, (
                    exam_id, q['subject'], q.get('subject_hi',''),
                    q['question_text_en'], q.get('question_text_hi',''),
                    q['option_a_en'], q.get('option_a_hi',''),
                    q['option_b_en'], q.get('option_b_hi',''),
                    q['option_c_en'], q.get('option_c_hi',''),
                    q['option_d_en'], q.get('option_d_hi',''),
                    q.get('question_text_mr',''), q.get('question_text_ta',''),
                    q.get('question_text_te',''), q.get('question_text_gu',''),
                    q.get('question_text_bn',''), q.get('question_text_kn',''),
                    q.get('option_a_mr',''), q.get('option_a_ta',''),
                    q.get('option_a_te',''), q.get('option_a_gu',''),
                    q.get('option_a_bn',''), q.get('option_a_kn',''),
                    q.get('option_b_mr',''), q.get('option_b_ta',''),
                    q.get('option_b_te',''), q.get('option_b_gu',''),
                    q.get('option_b_bn',''), q.get('option_b_kn',''),
                    q.get('option_c_mr',''), q.get('option_c_ta',''),
                    q.get('option_c_te',''), q.get('option_c_gu',''),
                    q.get('option_c_bn',''), q.get('option_c_kn',''),
                    q.get('option_d_mr',''), q.get('option_d_ta',''),
                    q.get('option_d_te',''), q.get('option_d_gu',''),
                    q.get('option_d_bn',''), q.get('option_d_kn',''),
                    q['correct_answer'],
                    q.get('marks_correct', 4.0), q.get('marks_wrong', -1.0),
                    q.get('difficulty','medium'), q.get('question_type','mcq'),
                    q['seq_number']
                ))
            conn.commit()
            return True, f"Inserted {len(questions)} questions"
        except Exception as e:
            conn.rollback()
            return False, str(e)

def get_exam_questions(exam_id: int) -> List[Dict]:
    with _exam_lock:
        conn = _exam_conn()
        rows = conn.execute("""
            SELECT * FROM questions
            WHERE exam_id=? AND is_deleted=0
            ORDER BY seq_number
        """, (exam_id,)).fetchall()
    return [dict(r) for r in rows]

def get_question_count(exam_id: int) -> int:
    with _exam_lock:
        conn = _exam_conn()
        return conn.execute(
            "SELECT COUNT(*) FROM questions WHERE exam_id=? AND is_deleted=0",
            (exam_id,)
        ).fetchone()[0]

def create_session(user_id: int, exam_id: int, language: str = 'en') -> Tuple[bool, int]:
    with _exam_lock:
        conn = _exam_conn()
        conn.execute("BEGIN")
        try:
            done = conn.execute("""
                SELECT session_id FROM exam_sessions
                WHERE user_id=? AND exam_id=? AND status='completed' LIMIT 1
            """, (user_id, exam_id)).fetchone()
            if done:
                conn.rollback()
                return False, -2

            prog = conn.execute("""
                SELECT session_id FROM exam_sessions
                WHERE user_id=? AND exam_id=? AND status='in_progress' LIMIT 1
            """, (user_id, exam_id)).fetchone()
            if prog:
                conn.rollback()
                return True, prog['session_id']

            cur = conn.execute("""
                INSERT INTO exam_sessions
                    (attempt_id, user_id, exam_id, start_time, selected_language)
                VALUES (?,?,?,?,?)
            """, (secrets.token_hex(16), user_id, exam_id,
                  datetime.now().isoformat(), language))
            sid = cur.lastrowid
            conn.commit()
            return True, sid
        except Exception as e:
            conn.rollback()
            print(f"create_session: {e}")
            return False, -1

def get_session(session_id: int) -> Optional[Dict]:
    with _exam_lock:
        conn = _exam_conn()
        row = conn.execute(
            "SELECT * FROM exam_sessions WHERE session_id=?", (session_id,)
        ).fetchone()
    return dict(row) if row else None

def get_server_time_remaining(session_id: int) -> int:
    with _exam_lock:
        conn = _exam_conn()
        row = conn.execute("""
            SELECT es.start_time, e.duration_mins
            FROM exam_sessions es
            JOIN exams e ON es.exam_id = e.exam_id
            WHERE es.session_id=?
        """, (session_id,)).fetchone()
    if not row:
        return 0
    try:
        start   = datetime.fromisoformat(str(row['start_time']))
        elapsed = (datetime.now() - start).total_seconds()
        return max(0, int(row['duration_mins'] * 60 - elapsed))
    except Exception:
        return 0

def update_session_question_idx(session_id: int, idx: int):
    with _exam_lock:
        conn = _exam_conn()
        conn.execute("BEGIN")
        conn.execute(
            "UPDATE exam_sessions SET current_question_idx=? WHERE session_id=?",
            (idx, session_id)
        )
        conn.commit()

def update_session_status(session_id: int, status: str,
                          score: float = 0) -> Tuple[bool, str]:
    with _exam_lock:
        conn = _exam_conn()
        conn.execute("BEGIN")
        try:
            row = conn.execute(
                "SELECT result_locked FROM exam_sessions WHERE session_id=?",
                (session_id,)
            ).fetchone()
            if row and row['result_locked']:
                conn.rollback()
                return True, "Already submitted"
            conn.execute("""
                UPDATE exam_sessions
                SET status=?, actual_end_time=?, total_score=?, result_locked=1
                WHERE session_id=?
            """, (status, datetime.now().isoformat(), score, session_id))
            conn.commit()
            return True, "Session updated"
        except Exception as e:
            conn.rollback()
            return False, str(e)

def check_incomplete_session(user_id: int) -> Optional[Dict]:
    with _exam_lock:
        conn = _exam_conn()
        row = conn.execute("""
            SELECT es.*, e.duration_mins
            FROM exam_sessions es
            JOIN exams e ON es.exam_id = e.exam_id
            WHERE es.user_id=? AND es.status='in_progress'
            ORDER BY es.start_time DESC LIMIT 1
        """, (user_id,)).fetchone()
    return dict(row) if row else None

def get_user_sessions(user_id: int) -> List[Dict]:
    with _exam_lock:
        conn = _exam_conn()
        rows = conn.execute("""
            SELECT s.*, e.exam_name, e.exam_type
            FROM exam_sessions s
            JOIN exams e ON s.exam_id = e.exam_id
            WHERE s.user_id=? ORDER BY s.start_time DESC
        """, (user_id,)).fetchall()
    return [dict(r) for r in rows]

def get_session_questions(session_id: int) -> List[Dict]:
    with _exam_lock:
        conn = _exam_conn()
        rows = conn.execute("""
            SELECT q.*, sq.seq_number
            FROM questions q
            JOIN session_questions sq ON q.question_id = sq.question_id
            WHERE sq.session_id=? AND q.is_deleted=0
            ORDER BY sq.seq_number
        """, (session_id,)).fetchall()
    return [dict(r) for r in rows]

def get_session_responses(session_id: int) -> List[Dict]:
    with _exam_lock:
        conn = _exam_conn()
        rows = conn.execute(
            "SELECT * FROM responses WHERE session_id=?", (session_id,)
        ).fetchall()
    return [dict(r) for r in rows]

def save_session_questions(session_id: int, question_ids: List[int]) -> bool:
    with _exam_lock:
        conn = _exam_conn()
        conn.execute("BEGIN")
        try:
            for seq, qid in enumerate(question_ids, 1):
                conn.execute("""
                    INSERT OR IGNORE INTO session_questions
                        (session_id, question_id, seq_number)
                    VALUES (?,?,?)
                """, (session_id, qid, seq))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"save_session_questions: {e}")
            return False

def save_response(session_id: int, question_id: int,
                  selected_answer: Optional[str],
                  marked_for_review: bool = False,
                  is_visited: bool = True) -> Tuple[bool, str]:
    with _exam_lock:
        conn = _exam_conn()
        conn.execute("BEGIN")
        try:
            locked = conn.execute(
                "SELECT result_locked FROM exam_sessions WHERE session_id=?",
                (session_id,)
            ).fetchone()
            if locked and locked['result_locked']:
                conn.rollback()
                return False, "Exam already submitted"

            existing = conn.execute("""
                SELECT response_id, selected_answer, answer_changed
                FROM responses WHERE session_id=? AND question_id=?
            """, (session_id, question_id)).fetchone()

            now = datetime.now().isoformat()
            if existing:
                old_ans = existing['selected_answer']
                changed = (existing['answer_changed'] or 0)
                if old_ans != selected_answer:
                    changed += 1
                    conn.execute("""
                        INSERT INTO answer_history
                            (session_id, question_id, old_answer, new_answer)
                        VALUES (?,?,?,?)
                    """, (session_id, question_id, old_ans, selected_answer))
                conn.execute("""
                    UPDATE responses
                    SET selected_answer=?, marked_for_review=?,
                        is_visited=1, answer_changed=?, answered_at=?
                    WHERE response_id=?
                """, (selected_answer, marked_for_review, changed, now,
                      existing['response_id']))
            else:
                conn.execute("""
                    INSERT INTO responses
                        (session_id, question_id, selected_answer,
                         marked_for_review, is_visited, answered_at)
                    VALUES (?,?,?,?,1,?)
                """, (session_id, question_id, selected_answer,
                      marked_for_review, now))
            conn.commit()
            return True, "Saved"
        except Exception as e:
            conn.rollback()
            return False, str(e)

def get_responses(session_id: int) -> List[Dict]:
    with _exam_lock:
        conn = _exam_conn()
        rows = conn.execute(
            "SELECT * FROM responses WHERE session_id=?", (session_id,)
        ).fetchall()
    return [dict(r) for r in rows]

def save_result(session_id: int, user_id: int, exam_id: int,
                total_score: float, correct: int, wrong: int,
                unattempted: int, section_scores: Dict) -> bool:
    with _exam_lock:
        conn = _exam_conn()
        conn.execute("BEGIN")
        try:
            conn.execute("""
                INSERT OR IGNORE INTO results
                    (session_id, user_id, exam_id, total_score,
                     correct_count, wrong_count, unattempted_count, section_scores)
                VALUES (?,?,?,?,?,?,?,?)
            """, (session_id, user_id, exam_id, total_score,
                  correct, wrong, unattempted, json.dumps(section_scores)))
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"save_result: {e}")
            return False

def get_result(session_id: int) -> Optional[Dict]:
    with _exam_lock:
        conn = _exam_conn()
        row = conn.execute(
            "SELECT * FROM results WHERE session_id=?", (session_id,)
        ).fetchone()
    return dict(row) if row else None

def calculate_score_with_limits(session_id: int, limits: Dict) -> float:
    if not limits.get('has_limits'):
        return calculate_normal_score(session_id)
    with _exam_lock:
        conn = _exam_conn()
        rows = conn.execute("""
            SELECT q.subject, q.marks_correct, q.marks_wrong,
                   q.correct_answer, r.selected_answer
            FROM questions q
            JOIN session_questions sq ON q.question_id = sq.question_id
            LEFT JOIN responses r ON q.question_id=r.question_id AND r.session_id=?
            WHERE sq.session_id=?
        """, (session_id, session_id)).fetchall()
    total = 0.0
    if limits.get('subject_limits'):
        by_subj: Dict[str, list] = {}
        for r in rows:
            if r['selected_answer']:
                sc = r['marks_correct'] if r['selected_answer'] == r['correct_answer'] \
                     else r['marks_wrong']
                by_subj.setdefault(r['subject'], []).append(sc)
        for subj, li in limits['subject_limits'].items():
            total += sum(sorted(by_subj.get(subj,[]), reverse=True)[:li['attempt']])
    else:
        all_sc = [r['marks_correct'] if r['selected_answer']==r['correct_answer']
                  else r['marks_wrong']
                  for r in rows if r['selected_answer']]
        total = sum(sorted(all_sc, reverse=True)[:limits['total_attempt']])
    return total

def calculate_normal_score(session_id: int) -> float:
    with _exam_lock:
        conn = _exam_conn()
        rows = conn.execute("""
            SELECT q.marks_correct, q.marks_wrong,
                   q.correct_answer, r.selected_answer
            FROM questions q
            JOIN session_questions sq ON q.question_id = sq.question_id
            LEFT JOIN responses r ON q.question_id=r.question_id AND r.session_id=?
            WHERE sq.session_id=?
        """, (session_id, session_id)).fetchall()
    total = 0.0
    for r in rows:
        if r['selected_answer']:
            total += r['marks_correct'] if r['selected_answer'] == r['correct_answer'] \
                     else r['marks_wrong']
    return total

def get_exam_limits(exam_id: int) -> Dict:
    with _exam_lock:
        conn = _exam_conn()
        row = conn.execute(
            "SELECT exam_type FROM exams WHERE exam_id=?", (exam_id,)
        ).fetchone()
    if not row:
        return {}
    t = row['exam_type']
    if t == 'NEET':
        return {'has_limits': True, 'total_given': 200, 'total_attempt': 180,
                'subject_limits': {'Physics':{'given':50,'attempt':45},
                                   'Chemistry':{'given':50,'attempt':45},
                                   'Biology':{'given':100,'attempt':90}}}
    if t == 'CUET':
        with _exam_lock:
            conn = _exam_conn()
            subjects = [r['subject'] for r in conn.execute(
                "SELECT DISTINCT subject FROM questions WHERE exam_id=?", (exam_id,)
            ).fetchall()]
        return {'has_limits': True, 'total_given': len(subjects)*50,
                'total_attempt': len(subjects)*40,
                'subject_limits': {s:{'given':50,'attempt':40} for s in subjects}}
    if t == 'CUET_GT':
        return {'has_limits': True, 'total_given': 60,
                'total_attempt': 50, 'subject_limits': {}}
    return {'has_limits': False}

def log_cheat_event(session_id: int, user_id: int,
                    event_type: str, detail: str = "", ip: str = "unknown"):
    try:
        with _exam_lock:
            conn = _exam_conn()
            conn.execute("BEGIN")
            conn.execute("""
                INSERT INTO anti_cheat_log
                    (session_id, user_id, event_type, detail, ip_address)
                VALUES (?,?,?,?,?)
            """, (session_id, user_id, event_type, detail, ip))
            conn.commit()
    except Exception:
        pass

def get_cheat_events(session_id: int) -> List[Dict]:
    with _exam_lock:
        conn = _exam_conn()
        rows = conn.execute(
            "SELECT * FROM anti_cheat_log WHERE session_id=? ORDER BY logged_at",
            (session_id,)
        ).fetchall()
    return [dict(r) for r in rows]

def _exam_audit(conn, admin_id: int, action: str, target_type: str = "",
                target_id: int = 0, detail: str = "", ip: str = ""):
    try:
        conn.execute("""
            INSERT INTO admin_audit_log
                (admin_id, action, target_type, target_id, detail, ip_address)
            VALUES (?,?,?,?,?,?)
        """, (admin_id, action, target_type, target_id, detail, ip))
    except Exception:
        pass

# Legacy alias
_audit = _exam_audit

def log_admin_action(admin_id: int, action: str, target_type: str = "",
                     target_id: int = 0, detail: str = ""):
    try:
        with _exam_lock:
            conn = _exam_conn()
            conn.execute("BEGIN")
            _exam_audit(conn, admin_id, action, target_type, target_id, detail)
            conn.commit()
    except Exception:
        pass

def get_admin_audit_log(limit: int = 200) -> List[Dict]:
    with _exam_lock:
        conn = _exam_conn()
        rows = conn.execute("""
            SELECT * FROM admin_audit_log
            ORDER BY performed_at DESC LIMIT ?
        """, (limit,)).fetchall()
    return [dict(r) for r in rows]

def save_exam_analytics(session_id: int, analytics_json: str,
                        percentile: float = 0, rank: int = 0,
                        tab_switches: int = 0, fullscreen_exits: int = 0) -> Tuple[bool, str]:
    with _exam_lock:
        conn = _exam_conn()
        conn.execute("BEGIN")
        try:
            conn.execute("""
                INSERT INTO exam_analytics
                    (session_id, analytics_data, percentile,
                     rank_position, tab_switches, fullscreen_exits)
                VALUES (?,?,?,?,?,?)
            """, (session_id, analytics_json, percentile, rank,
                  tab_switches, fullscreen_exits))
            conn.commit()
            return True, "Analytics saved"
        except Exception as e:
            conn.rollback()
            return False, str(e)

def get_exam_analytics(session_id: int) -> Optional[Dict]:
    with _exam_lock:
        conn = _exam_conn()
        row = conn.execute(
            "SELECT * FROM exam_analytics WHERE session_id=?", (session_id,)
        ).fetchone()
    return dict(row) if row else None

def update_leaderboard(user_id: int, exam_id: int, score: float) -> Tuple[bool, Dict]:
    with _exam_lock:
        conn = _exam_conn()
        conn.execute("BEGIN")
        try:
            scores = [r[0] for r in conn.execute(
                "SELECT score FROM leaderboard WHERE exam_id=? ORDER BY score DESC",
                (exam_id,)
            ).fetchall()]
            scores.append(score); scores.sort(reverse=True)
            rank = scores.index(score) + 1
            pct  = ((len(scores) - rank) / len(scores)) * 100
            conn.execute("""
                INSERT INTO leaderboard
                    (user_id, exam_id, score, rank_position, percentile)
                VALUES (?,?,?,?,?)
            """, (user_id, exam_id, score, rank, pct))
            conn.commit()
            return True, {'rank': rank, 'percentile': pct, 'total_students': len(scores)}
        except Exception as e:
            conn.rollback()
            return False, {'error': str(e)}

def get_leaderboard(exam_id: int, limit: int = 100) -> List[Dict]:
    with _exam_lock:
        conn = _exam_conn()
        rows = conn.execute("""
            SELECT l.*, u.full_name, u.username
            FROM leaderboard l
            JOIN users u ON l.user_id = u.user_id
            WHERE l.exam_id=? ORDER BY l.score DESC LIMIT ?
        """, (exam_id, limit)).fetchall()
    return [dict(r) for r in rows]

def get_exam_attempts(exam_id: int) -> int:
    with _exam_lock:
        conn = _exam_conn()
        return conn.execute(
            "SELECT COUNT(*) FROM exam_sessions WHERE exam_id=?", (exam_id,)
        ).fetchone()[0]

def get_database_stats() -> Dict:
    auth = _auth_conn()
    exam = _exam_conn()
    stats = {}
    with _auth_lock:
        stats['total_students'] = auth.execute(
            "SELECT COUNT(*) FROM users WHERE user_type='student' AND is_deleted=0"
        ).fetchone()[0]
        stats['total_admins'] = auth.execute(
            "SELECT COUNT(*) FROM users WHERE user_type='admin'"
        ).fetchone()[0]
    with _exam_lock:
        for key, sql in [
            ('active_exams',      "SELECT COUNT(*) FROM exams WHERE is_active=1 AND is_deleted=0"),
            ('total_questions',   "SELECT COUNT(*) FROM questions WHERE is_deleted=0"),
            ('total_sessions',    "SELECT COUNT(*) FROM exam_sessions"),
            ('completed_sessions',"SELECT COUNT(*) FROM exam_sessions WHERE status='completed'"),
        ]:
            stats[key] = exam.execute(sql).fetchone()[0]
    return stats

def get_exam_sessions(exam_id: int) -> List[Dict]:
    with _exam_lock:
        conn = _exam_conn()
        rows = conn.execute("""
            SELECT es.*, e.exam_name
            FROM exam_sessions es
            JOIN exams e ON es.exam_id = e.exam_id
            WHERE es.exam_id=? ORDER BY es.start_time DESC
        """, (exam_id,)).fetchall()
    return [dict(r) for r in rows]


def save_answer(session_id: str, question_id, answer: str) -> bool:
    """
    Upsert a single answer during an active exam session.
    Called by _auto_save_answers() every 30 s — must be idempotent and fast.
    Returns True on success, False on any error (caller ignores failures).
    """
    try:
        conn = get_connection()
        conn.execute("""
            INSERT INTO exam_responses (session_id, question_id, selected_answer, updated_at)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(session_id, question_id) DO UPDATE SET
                selected_answer = excluded.selected_answer,
                updated_at      = CURRENT_TIMESTAMP
        """, (session_id, question_id, answer))
        conn.commit()
        return True
    except Exception:
        return False
