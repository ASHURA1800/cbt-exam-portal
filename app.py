"""
CBT Exam Portal — v11.0
========================
✅ No NCERT chapter references in questions
✅ Detailed results with answer sheet + subject breakdown
✅ Highly shuffled questions per student
✅ Section-wise division (Physics, Chemistry, Maths, Biology, GK, …)
✅ Question pool 100+ with random selection per attempt
✅ Hardest questions placed at end of each section
✅ Merged admin panels (student data + exam info combined)
✅ JEE / NEET / CUET / CUET_GT exam-specific patterns
✅ Real exam marks: +4/−1 JEE/NEET, +5/−1 CUET
✅ Optional-question smart scoring (NEET: best 180/200, CUET: best 40/50)
✅ Offline multilingual translation via Argos Translate (8 languages)
✅ Server-authoritative timer (anti-cheat: no client-side clock)
✅ Persistent session recovery (crash-safe auto-save)
✅ Enhanced UI with gradient cards, animated palette, dark theme
✅ Batch question generation with Llama 3.2:3b (3-4× faster)
"""

import streamlit as st
import json
import time
import random
from datetime import datetime
import db
from typing import Dict, List

# Import enhanced UI styles
from enhanced_ui_styles import (
    ENHANCED_CSS,
    create_header,
    create_section_header,
    create_info_card,
    create_success_card,
    create_warning_card,
    create_error_card,
    create_status_badge,
    create_gradient_text,
    create_loading_message,
)

# ── Model persistent keep-alive (runs once at startup) ────────────────────────
# Loads llama3.2:3b into Ollama RAM with a 20-minute keep_alive.
# Background thread pings every 4 min — model never unloads between exams.
# Restarting app.py does NOT re-download the model.
from ollama_manager import warm_up_model, is_model_ready, get_status, OLLAMA_MODEL as _ACTIVE_MODEL

st.set_page_config(
    page_title="CBT Exam Portal - Professional Testing Platform",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': "CBT Exam Portal v10.3 — AI-powered exam preparation (Llama 3.2:3b)"
    }
)

# ── Warm up Llama 3.2:3b once per Streamlit server session ───────────────────
@st.cache_resource(show_spinner=False)
def _init_ollama():
    """
    Runs ONCE when Streamlit starts (not on every rerun/code-change).
    Loads llama3.2:3b into Ollama RAM + starts background keep-alive thread.
    """
    return warm_up_model()

_ollama_ready, _ollama_msg = _init_ollama()

# ── Enhanced UI Styles ────────────────────────────────────────────────────────
st.markdown(ENHANCED_CSS, unsafe_allow_html=True)


db.init_database()
db.migrate_database()  # Auto-fix any old database schemas

# ── DOB auto-formatter: inject once globally ──────────────────────────────────
def _inject_dob_formatter():
    """Inject JS once to auto-format DD/MM/YYYY inputs across all login forms."""
    st.markdown("""
    <script>
    (function() {
        function formatDOB(input) {
            var v = input.value.replace(/[^0-9]/g, '').substring(0,8);
            var out = '';
            if (v.length >= 1) out = v.substring(0,2);
            if (v.length >= 3) out += '/' + v.substring(2,4);
            if (v.length >= 5) out += '/' + v.substring(4,8);
            else if (v.length >= 3) out += '/' + v.substring(2);
            input.value = out;
        }
        function attachDOBFormatter() {
            document.querySelectorAll('input[data-testid="stTextInput"]').forEach(function(inp) {
                var lbl = inp.closest('[data-testid="stTextInputRootElement"]');
                if (lbl) {
                    var label = lbl.querySelector('label');
                    if (label && label.innerText && label.innerText.includes('DD/MM/YYYY')) {
                        if (!inp._dobFormatted) {
                            inp._dobFormatted = true;
                            inp.setAttribute('maxlength','10');
                            inp.setAttribute('inputmode','numeric');
                            inp.setAttribute('pattern','[0-9/]*');
                            inp.addEventListener('input', function(e) { formatDOB(this); });
                            inp.addEventListener('keydown', function(e) {
                                if (e.key==='Backspace' && this.value.slice(-1)==='/') {
                                    this.value = this.value.slice(0,-1);
                                    e.preventDefault();
                                }
                            });
                        }
                    }
                }
            });
        }
        var obs = new MutationObserver(attachDOBFormatter);
        obs.observe(document.body, {childList:true, subtree:true});
        setTimeout(attachDOBFormatter, 300);
        setTimeout(attachDOBFormatter, 800);
    })();
    </script>
    """, unsafe_allow_html=True)

def init_session_state():
    defaults = {
        'logged_in': False,
        'user': None,
        'exam_started': False,
        'current_exam_id': None,
        'session_id': None,
        'current_question_idx': 0,
        'selected_answers': {},
        'marked_for_review': set(),
        'visited_questions': set(),
        'exam_start_time': None,
        'time_remaining': None,
        'show_exit_confirm': False,
        'current_section': 'all',
        'active_section': 'All',
        'exam_lang': 'en',
        'clear_version': {},
        'translation_progress': {},
        # ── Security additions ──
        'login_token': None,           # DB-backed session token
        'last_refresh_time': None,     # Anti-cheat: refresh tracking
        'refresh_count': 0,            # Anti-cheat: rapid refresh counter
        'answer_change_count': {},     # Anti-cheat: rapid switching tracker
        '_autosave_ts': 0.0,           # Timestamp of last answer auto-save
        '_admin_tab': 0,               # Remember last admin tab across reruns
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# ═══════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION
# ═══════════════════════════════════════════════════════════════════════════════

def show_login_register():
    # Enhanced main header
    st.markdown(create_header(
        "CBT EXAM PORTAL",
        "🎯 JEE Main • 🩺 NEET UG • 🎓 CUET • AI-Powered • Multilingual • Real Exam Pattern"
    ), unsafe_allow_html=True)
    
    # System status indicator — use native Streamlit (no HTML passthrough issues)
    if _ollama_ready:
        st.success(f"🚀 AI System Online — {_ACTIVE_MODEL} ready to generate exams")
    elif _ollama_msg == "model_not_pulled":
        st.warning(
            f"⚠️ Model **{_ACTIVE_MODEL}** is not downloaded yet.  \n"
            f"Open a terminal and run: `ollama pull {_ACTIVE_MODEL}`"
        )
    elif _ollama_msg == "ollama_not_running":
        st.warning(
            "⚠️ Ollama is not running.  \n"
            "Open a terminal and run: `ollama serve`"
        )
    elif _ollama_msg in ("loading", "error"):
        st.info(
            f"⏳ **{_ACTIVE_MODEL}** is loading into memory (takes ~60 s on first start).  \n"
            "You can still generate exams — Ollama will respond once loading completes."
        )
    else:
        st.info("⏳ AI system is initializing — generation will work once ready.")

    # Inject DOB formatter once for all three forms on this page
    _inject_dob_formatter()

    tab1, tab2, tab3 = st.tabs(["🔐 Student Login", "📝 Student Registration", "👨‍💼 Admin Login"])
    
    with tab1:
        show_student_login()
    
    with tab2:
        show_student_registration()
    
    with tab3:
        show_admin_login()

def show_student_login():
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:16px;
                padding:28px 32px;border:1px solid #334155;margin-bottom:8px;'>
        <div style='text-align:center;margin-bottom:20px;'>
            <span style='font-size:36px;'>🎓</span>
            <h2 style='color:white;margin:8px 0 4px;font-size:1.5rem;font-weight:800;'>Student Login</h2>
            <p style='color:#64748b;font-size:13px;margin:0;'>Enter your username and date of birth to access your portal</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("student_login_form"):
        username = st.text_input("👤 Username", placeholder="Enter your username")
        dob      = st.text_input("🎂 Date of Birth (DD/MM/YYYY)", placeholder="DDMMYYYY or DD/MM/YYYY")
        st.caption("💡 Type digits only — slashes added automatically")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        submit = st.form_submit_button("🚀 Login to Portal", type="primary", use_container_width=True)

        if submit:
            if not username or not dob:
                st.error("❌ Please enter both username and date of birth")
            else:
                user = db.authenticate_user(username, dob)
                if user and user.get('_locked'):
                    from datetime import datetime as _dt
                    try:
                        lt = _dt.fromisoformat(str(user.get('locked_until','')))
                        mins = max(1, int((lt - _dt.now()).total_seconds() // 60))
                        st.error(f"🔒 Account locked. Try again in {mins} minute(s).")
                    except Exception:
                        st.error("🔒 Account temporarily locked. Try again later.")
                elif user and user['user_type'] == 'student':
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.login_token = db.issue_login_token(user['user_id'])
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Check your username and date of birth.")

def show_student_registration():
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:16px;
                padding:28px 32px;border:1px solid #334155;margin-bottom:8px;'>
        <div style='text-align:center;margin-bottom:20px;'>
            <span style='font-size:36px;'>📝</span>
            <h2 style='color:white;margin:8px 0 4px;font-size:1.5rem;font-weight:800;'>Create Account</h2>
            <p style='color:#64748b;font-size:13px;margin:0;'>Register to start practising for JEE / NEET / CUET 2026</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("student_registration_form"):
        col1, col2 = st.columns(2)

        with col1:
            username  = st.text_input("👤 Username*", placeholder="Choose a username (min 3 chars)")
            full_name = st.text_input("🙍 Full Name*", placeholder="Enter your full name")

        with col2:
            email = st.text_input("📧 Email*", placeholder="Enter your email address")
            dob   = st.text_input("🎂 Date of Birth* (DD/MM/YYYY)", placeholder="DDMMYYYY or DD/MM/YYYY")
            st.caption("💡 Type digits only — slashes added automatically")

        submit = st.form_submit_button("✅ Register", type="primary", use_container_width=True)

        if submit:
            u = username.strip()
            n = full_name.strip()
            e = email.strip().lower()
            d = dob.strip()
            if not all([u, n, e, d]):
                st.error("❌ Please fill all required fields")
            elif len(u) < 3:
                st.error("❌ Username must be at least 3 characters")
            elif len(u) > 20:
                st.error("❌ Username must be at most 20 characters")
            elif not u.replace('_', '').isalnum():
                st.error("❌ Username may only contain letters, numbers, and underscore ( _ )")
            elif len(n) < 2:
                st.error("❌ Please enter your full name (at least 2 characters)")
            elif '@' not in e or '.' not in e.split('@')[-1]:
                st.error("❌ Please enter a valid email address (e.g. name@domain.com)")
            else:
                success, msg = db.create_user(
                    u, '', n, d, 'en', 'student', e
                )
                if success:
                    st.success("✅ Registration successful! You can now login with your **username** and **date of birth**.")
                    st.rerun()
                else:
                    st.error(f"❌ {msg}")

def show_admin_login():
    st.markdown("""
    <div style='background:linear-gradient(135deg,#0f172a,#1e293b);border-radius:16px;
                padding:28px 32px;border:1px solid #334155;margin-bottom:8px;'>
        <div style='text-align:center;margin-bottom:20px;'>
            <span style='font-size:36px;'>🛡️</span>
            <h2 style='color:white;margin:8px 0 4px;font-size:1.5rem;font-weight:800;'>Admin Portal</h2>
            <p style='color:#64748b;font-size:13px;margin:0;'>Restricted access — administrators only</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("admin_login"):
        username = st.text_input("👤 Admin Username", placeholder="Enter admin username")
        dob      = st.text_input("🎂 Date of Birth (DD/MM/YYYY)", placeholder="DDMMYYYY or DD/MM/YYYY")
        st.caption("💡 Type digits only — slashes added automatically")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        submit = st.form_submit_button("🔓 Login as Administrator", type="primary", use_container_width=True)

        if submit:
            if not username or not dob:
                st.error("❌ Please enter both username and date of birth")
            else:
                user = db.authenticate_user(username, dob)
                if user and user.get('_locked'):
                    st.error("🔒 Account locked due to repeated failed attempts.")
                elif user and user['is_admin']:
                    st.session_state.logged_in = True
                    st.session_state.user = user
                    st.session_state.login_token = db.issue_login_token(user['user_id'])
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Check your username and date of birth.")

# ═══════════════════════════════════════════════════════════════════════════════
# STUDENT DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════

def show_student_dashboard():
    user = st.session_state.user

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#0f172a 0%,#1e3a5f 50%,#1e1b4b 100%);
                padding:20px 28px;border-radius:16px;margin-bottom:20px;
                border:1px solid rgba(99,102,241,0.3);
                display:flex;align-items:center;justify-content:space-between;'>
        <div>
            <p style='color:#64748b;font-size:13px;margin:0;font-weight:600;letter-spacing:1px;'>
                WELCOME BACK
            </p>
            <h2 style='color:white;margin:4px 0;font-size:1.8rem;font-weight:900;'>
                👋 {user['full_name']}
            </h2>
            <p style='color:#94a3b8;font-size:13px;margin:0;'>
                📚 CBT Exam Portal &nbsp;·&nbsp; JEE / NEET / CUET 2026
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([6,1])
    with c2:
        if st.button("🚪 Logout", use_container_width=True):
            if st.session_state.get('login_token'):
                db.revoke_login_token(st.session_state.login_token)
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.exam_started = False
            st.session_state.login_token = None
            st.rerun()

    # ── Quick stats strip ──────────────────────────────────────────────────────
    sessions = db.get_user_sessions(user['user_id'])
    completed = [s for s in sessions if s['status'] == 'completed']
    in_progress = [s for s in sessions if s['status'] != 'completed']
    best_score  = max((s.get('total_score', 0) for s in completed), default=0)
    avg_score   = (sum(s.get('total_score', 0) for s in completed) / len(completed)) if completed else 0

    sc1, sc2, sc3, sc4 = st.columns(4)
    with sc1:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid #334155;
                    border-radius:12px;padding:16px;text-align:center;'>
            <div style='font-size:28px;font-weight:900;color:#3b82f6;'>{len(completed)}</div>
            <div style='font-size:12px;color:#64748b;font-weight:600;margin-top:4px;'>✅ COMPLETED</div>
        </div>""", unsafe_allow_html=True)
    with sc2:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid #334155;
                    border-radius:12px;padding:16px;text-align:center;'>
            <div style='font-size:28px;font-weight:900;color:#f59e0b;'>{len(in_progress)}</div>
            <div style='font-size:12px;color:#64748b;font-weight:600;margin-top:4px;'>⏳ IN PROGRESS</div>
        </div>""", unsafe_allow_html=True)
    with sc3:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid #334155;
                    border-radius:12px;padding:16px;text-align:center;'>
            <div style='font-size:28px;font-weight:900;color:#10b981;'>{best_score:.0f}</div>
            <div style='font-size:12px;color:#64748b;font-weight:600;margin-top:4px;'>🏆 BEST SCORE</div>
        </div>""", unsafe_allow_html=True)
    with sc4:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#1e293b,#0f172a);border:1px solid #334155;
                    border-radius:12px;padding:16px;text-align:center;'>
            <div style='font-size:28px;font-weight:900;color:#a78bfa;'>{avg_score:.0f}</div>
            <div style='font-size:12px;color:#64748b;font-weight:600;margin-top:4px;'>📊 AVG SCORE</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📝 Available Exams", "➕ Generate New Exam", "📊 My Results"])
    
    with tab1:
        show_available_exams()
    
    with tab2:
        show_student_exam_generator()
    
    with tab3:
        show_student_results()

def show_student_exam_generator():
    """Students can generate their own exams - REAL PATTERNS"""

    exam_type = st.selectbox(
        "📚 Select Exam Type",
        ['JEE Main 2026', 'NEET (UG) 2026', 'CUET Domain', 'CUET General Test'],
        help="Choose the exam pattern you want to practise"
    )

    # ── Compact exam info cards ────────────────────────────────────────────────
    EXAM_INFO = {
        'JEE Main 2026': {
            'icon': '🧠', 'color': '#3b82f6',
            'stats': [('75 Questions', '25 per subject'),
                      ('300 Marks', '+4 / −1'),
                      ('180 min', '3 subjects')],
            'subjects': 'Physics · Chemistry · Mathematics',
            'note': 'Concept + multi-step numericals. Chemistry is the scoring subject.',
        },
        'NEET (UG) 2026': {
            'icon': '🩺', 'color': '#10b981',
            'stats': [('200 Questions', 'Best 180 count'),
                      ('720 Marks', '+4 / −1'),
                      ('180 min', '3 subjects')],
            'subjects': 'Physics · Chemistry · Biology',
            'note': 'Biology dominates (100q). NCERT line-by-line is key.',
        },
        'CUET Domain': {
            'icon': '🎓', 'color': '#f59e0b',
            'stats': [('50Q per subject', 'Best 40 count'),
                      ('200 per subject', '+5 / −1'),
                      ('60 min/subject', 'NCERT-based')],
            'subjects': 'PCM / PCB / PCMB (your choice)',
            'note': 'Speed over depth. NCERT Class 11–12 direct questions.',
        },
        'CUET General Test': {
            'icon': '📘', 'color': '#a78bfa',
            'stats': [('60 Questions', 'Best 50 count'),
                      ('250 Marks', '+5 / −1'),
                      ('60 min', '4 sections')],
            'subjects': 'GK · Current Affairs · Reasoning · Aptitude',
            'note': 'Speed + accuracy. Mental math only, no deep calculations.',
        },
    }

    info = EXAM_INFO.get(exam_type, {})
    if info:
        stat_cells = "".join(
            f"<div style='text-align:center;padding:8px 12px;background:#0f172a;"
            f"border-radius:8px;flex:1;'>"
            f"<div style='color:white;font-weight:800;font-size:15px;'>{v}</div>"
            f"<div style='color:#64748b;font-size:11px;'>{k}</div></div>"
            for v, k in info['stats']
        )
        st.markdown(f"""
        <div style='background:#1e293b;border-radius:12px;padding:18px 20px;
                    border-left:4px solid {info["color"]};margin-bottom:16px;'>
            <div style='font-size:20px;font-weight:800;color:white;margin-bottom:2px;'>
                {info["icon"]} {exam_type}
            </div>
            <div style='color:#94a3b8;font-size:13px;margin-bottom:12px;'>
                {info["subjects"]}
            </div>
            <div style='display:flex;gap:8px;margin-bottom:10px;'>{stat_cells}</div>
            <div style='color:#64748b;font-size:12px;'>💡 {info["note"]}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Forms ──────────────────────────────────────────────────────────────────
    if exam_type == 'JEE Main 2026':
        with st.form("student_jee_form"):
            exam_name     = st.text_input("Exam Name", value=f"JEE Main Practice {datetime.now().strftime('%d-%m-%Y')}")
            include_hindi = st.checkbox("Include regional languages (Hindi, Bengali, Tamil…)", value=True)
            st.caption("Generates a pool of ~35 questions per subject; 25 are randomly selected each attempt.")
            if st.form_submit_button("🚀 Generate JEE Main Exam", type="primary", use_container_width=True):
                generate_exam_for_student_improved('JEE', exam_name,
                    {'Physics': 25, 'Chemistry': 25, 'Mathematics': 25},
                    180, include_hindi, created_by=st.session_state.user['user_id'])

    elif exam_type == 'NEET (UG) 2026':
        with st.form("student_neet_form"):
            exam_name     = st.text_input("Exam Name", value=f"NEET Practice {datetime.now().strftime('%d-%m-%Y')}")
            include_hindi = st.checkbox("Include regional languages", value=True)
            st.caption("Generates 200 questions (50 Physics + 50 Chemistry + 100 Biology). Best 180 answers count for score.")
            if st.form_submit_button("🚀 Generate NEET Exam", type="primary", use_container_width=True):
                generate_exam_for_student_improved('NEET', exam_name,
                    {'Physics': 50, 'Chemistry': 50, 'Biology': 100},
                    180, include_hindi, created_by=st.session_state.user['user_id'])

    elif exam_type == 'CUET Domain':
        with st.form("student_cuet_form"):
            exam_name = st.text_input("Exam Name", value=f"CUET Practice {datetime.now().strftime('%d-%m-%Y')}")
            subject_combo = st.selectbox("Subject Combination", [
                "PCM — Physics, Chemistry, Mathematics",
                "PCB — Physics, Chemistry, Biology",
                "PCMB — Physics, Chemistry, Mathematics, Biology"
            ])
            include_hindi = st.checkbox("Include regional languages", value=True)

            if "PCM —" in subject_combo:
                subjects, duration, total_marks = {'Physics':50,'Chemistry':50,'Mathematics':50}, 180, 600
                subjects_text = "50 Physics + 50 Chemistry + 50 Mathematics"
            elif "PCB —" in subject_combo:
                subjects, duration, total_marks = {'Physics':50,'Chemistry':50,'Biology':50}, 180, 600
                subjects_text = "50 Physics + 50 Chemistry + 50 Biology"
            else:
                subjects, duration, total_marks = {'Physics':50,'Chemistry':50,'Mathematics':50,'Biology':50}, 240, 800
                subjects_text = "50 Physics + 50 Chemistry + 50 Mathematics + 50 Biology"

            st.caption(f"{subjects_text} | {total_marks} marks total | Best 40/subject counted | {duration} min")
            if st.form_submit_button("🚀 Generate CUET Domain Exam", type="primary", use_container_width=True):
                generate_exam_for_student_improved('CUET', exam_name, subjects, duration, include_hindi,
                    created_by=st.session_state.user['user_id'])

    else:  # CUET General Test
        with st.form("student_cuet_gt_form"):
            exam_name     = st.text_input("Exam Name", value=f"CUET GT Practice {datetime.now().strftime('%d-%m-%Y')}")
            include_hindi = st.checkbox("Include regional languages", value=True)
            st.caption("60 questions (15 GK + 15 Current Affairs + 15 Reasoning + 15 Aptitude). Best 50 count. 60 min.")
            if st.form_submit_button("🚀 Generate CUET GT Exam", type="primary", use_container_width=True):
                generate_exam_for_student_improved('CUET_GT', exam_name, {
                    'General Knowledge': 15, 'Current Affairs': 15,
                    'Logical Reasoning': 15, 'Quantitative Aptitude': 15
                }, 60, include_hindi, created_by=st.session_state.user['user_id'])

def generate_exam_for_student_improved(exam_type, exam_name, subjects, duration, include_hindi, created_by=None):
    """
    Generate exam with section-wise questions, difficulty ordering, and a pool
    of questions (generates more than needed; exam draws randomly each attempt).
    """
    from ai_generator import generate_section_wise_questions
    from ollama_manager import warm_up_model, is_model_ready, OLLAMA_MODEL

    # ── Pre-flight: ensure Ollama is up and model is ready ──────────────────────
    if not is_model_ready():
        with st.spinner(f"⏳ Loading {OLLAMA_MODEL} into memory — up to 2 minutes on first start…"):
            ok, msg = warm_up_model()

        if not ok:
            from ollama_manager import _is_ollama_running, _is_model_pulled
            if msg == "ollama_not_running":
                st.error("❌ **Ollama is not running.**")
                st.code("ollama serve", language="bash")
                st.info("💡 Open a terminal, run the command above, then click Generate again.")
                return
            elif msg == "model_not_pulled":
                st.error(f"❌ **Model `{OLLAMA_MODEL}` is not downloaded.**")
                st.code(f"ollama pull {OLLAMA_MODEL}", language="bash")
                st.info("💡 One-time ~2 GB download. Run it, then click Generate again.")
                return
            elif msg in ("loading", "error"):
                # "loading": warmup timed out but Ollama IS running — model still loading
                # "error":   warmup POST returned non-200 (transient — model may be loading or
                #            briefly busy). In BOTH cases: Ollama is up, model is pulled.
                # Safe to proceed — call_ollama_streaming() has its own retry logic.
                if _is_ollama_running() and _is_model_pulled():
                    st.info(
                        f"⏳ **{OLLAMA_MODEL}** is still loading into RAM (~60 s on first start).  \n"
                        "Generation is starting now — it will retry automatically until the model responds."
                    )
                    # Fall through and proceed to generation
                else:
                    # Truly unreachable — Ollama not running at all
                    st.error("❌ Cannot reach Ollama. Make sure it is running.")
                    st.code(f"ollama serve\nollama pull {OLLAMA_MODEL}", language="bash")
                    return

    if exam_type in ['JEE', 'NEET']:
        marking = {'correct': 4, 'wrong': -1}
    elif exam_type in ['CUET', 'CUET_GT']:
        marking = {'correct': 5, 'wrong': -1}
    else:
        marking = {'correct': 4, 'wrong': -1}

    total_qs    = sum(subjects.values())
    total_marks = total_qs * marking['correct']
    subject_list = list(subjects.items())
    n_subj       = len(subject_list)

    # Time estimate: ~20s per 3-question batch (streaming — continuous token flow)
    est_mins = max(1, round(sum(
        ((min(40, max(c, int(c * 1.1))) + 2) // 3) * 20 / 60
        for _, c in subject_list
    )))
    est_label = f"~{est_mins} min" if est_mins > 1 else "~1 min"

    exam_data = {
        'exam_name':       exam_name,
        'exam_type':       exam_type,
        'total_questions': total_qs,
        'duration_mins':   duration,
        'marking_scheme':  json.dumps(marking),
        'instructions_en': (
            f'{exam_type} exam (Real Pattern). '
            f'+{marking["correct"]} for correct, {marking["wrong"]} for wrong. '
            f'Total: {total_marks} marks.'
        ),
        'created_by': created_by
    }

    success, exam_id = db.create_exam(exam_data)
    if not success:
        st.error("❌ Failed to create exam record. Please try again.")
        return

    # ── Estimated time notice ──────────────────────────────────────────────────
    st.markdown(f"""
    <div style='background:#0f172a;border-radius:10px;padding:14px 20px;
                border:1px solid #334155;margin-bottom:12px;
                display:flex;align-items:center;gap:12px;'>
        <span style='font-size:28px;'>⏱️</span>
        <div>
            <div style='color:#94a3b8;font-size:13px;font-weight:600;
                        letter-spacing:0.5px;text-transform:uppercase;'>Estimated Time</div>
            <div style='color:white;font-size:18px;font-weight:800;'>{est_label}</div>
        </div>
        <div style='margin-left:auto;color:#64748b;font-size:13px;'>
            Llama 3.2:3b generates questions via streaming — progress is continuous
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Main generation with st.status ────────────────────────────────────────
    all_questions = []
    generation_ok = True
    fail_msg      = ""

    with st.status(f"🤖 Generating **{exam_type}** Exam — {total_qs} questions…", expanded=True) as status:
        progress_bar = st.progress(0.0)

        for i, (subject, count) in enumerate(subject_list):
            # Fraction at START of this subject (before generation)
            frac_start = i / n_subj
            frac_end   = (i + 1) / n_subj

            # Compute pool size BEFORE using it in the write() call
            # 1.1× pool: enough variety without massive generation time
            target_pool  = min(40, max(count, int(count * 1.1)))  # cap at 40 → max 14 batches of 3
            n_batches    = (target_pool + 2) // 3  # 3 questions per batch
            num_hardest  = max(3, target_pool // 4)  # 25% hardest questions
            num_hard     = target_pool - num_hardest

            progress_bar.progress(frac_start,
                text=f"🔬 [{i+1}/{n_subj}] Generating {subject}… (0/{target_pool} q)")
            st.write(f"**{subject}** — generating {target_pool} questions in {n_batches} batches of 3 (streaming)…")

            t0 = time.time()
            success_gen, section_questions, msg = generate_section_wise_questions(
                subject, num_hard, num_hardest, exam_type, include_hindi
            )
            elapsed = time.time() - t0

            if not success_gen:
                # 0 questions generated — Ollama not responding at all
                generation_ok = False
                fail_msg = msg
                try:
                    db.deactivate_exam(exam_id)
                except Exception:
                    pass
                status.update(label=f"❌ Could not reach Ollama — {subject}", state="error", expanded=True)
                break

            all_questions.extend(section_questions)
            got = len(section_questions)
            speed = f"{elapsed:.0f}s" if elapsed < 60 else f"{elapsed/60:.1f}min"
            q_rate = f"{got/elapsed*60:.0f}q/min" if elapsed > 1 else ""
            progress_bar.progress(frac_end,
                text=f"✅ [{i+1}/{n_subj}] {subject}: {got}q in {speed}")
            st.write(f"✅ **{subject}**: {got} questions in {speed} {q_rate}")

        if generation_ok:
            progress_bar.progress(1.0, text="💾 Saving to database…")
            st.write("💾 Saving questions to database…")
            db.insert_questions(exam_id, all_questions)
            progress_bar.progress(1.0, text=f"✅ Done — {len(all_questions)} questions saved!")
            status.update(
                label=f"✅ {exam_type} Exam ready — {len(all_questions)} questions generated!",
                state="complete",
                expanded=False
            )

    # ── Post-generation UI ────────────────────────────────────────────────────
    if not generation_ok:
        from ollama_manager import OLLAMA_MODEL as _MODEL
        st.error("❌ Could not connect to Ollama — 0 questions were generated.")
        with st.expander("🔍 Details", expanded=False):
            st.code(fail_msg)
        st.markdown(f"""
<div style='background:#0f172a;border-radius:12px;padding:16px 20px;
            border:1px solid #f59e0b;margin-top:8px;'>
  <div style='color:#f59e0b;font-weight:700;margin-bottom:8px;'>Fix in 3 steps:</div>
  <div style='color:#e2e8f0;font-size:14px;line-height:2;font-family:monospace;'>
    1. Open a terminal/command prompt<br>
    2. Run: <span style='color:#38bdf8;'>ollama serve</span><br>
    3. Run: <span style='color:#38bdf8;'>ollama pull {_MODEL}</span><br>
  </div>
  <div style='color:#64748b;font-size:12px;margin-top:8px;'>
    Then come back and click Generate again. The model loads in ~60 seconds on first start.
  </div>
</div>
""", unsafe_allow_html=True)
        return

    st.success(f"✅ Your **{exam_type}** exam **\"{exam_name}\"** is ready!")
    cols = st.columns(min(n_subj, 4))
    for i, (subj, count) in enumerate(subject_list):
        with cols[i % len(cols)]:
            pool_size = min(40, max(count, int(count * 1.1)))
            st.metric(subj, f"{count}Q", f"pool: {pool_size}Q")
    st.info(f"💡 {len(all_questions)} questions generated — {total_qs} will be randomly selected each attempt. Go to **Available Exams** to start!")
    st.rerun()

def _start_exam_session(exam):
    """Helper: create session and set all state vars to start the exam."""
    success, session_id = db.create_session(
        user_id=st.session_state.user['user_id'],
        exam_id=exam['exam_id'],
        language=st.session_state.user.get('preferred_lang', 'en')
    )
    if not success:
        st.error("❌ Could not create exam session. Please try again.")
        return
    if session_id == -2:
        st.error("❌ You have already completed this exam.")
        return
    st.session_state.current_exam_id  = exam['exam_id']
    st.session_state.session_id       = session_id
    st.session_state.exam_started     = True
    st.session_state.time_remaining   = db.get_server_time_remaining(session_id)
    sess_db = db.get_session(session_id)
    st.session_state.current_question_idx = sess_db.get('current_question_idx', 0) if sess_db else 0
    saved = db.get_responses(session_id)
    st.session_state.selected_answers = {r['question_id']: r['selected_answer']
                                         for r in saved if r.get('selected_answer')}
    st.session_state.marked_for_review = {r['question_id'] for r in saved if r.get('marked_for_review')}
    st.session_state.visited_questions = {r['question_id'] for r in saved if r.get('is_visited')}
    st.session_state.active_section   = 'All'
    st.session_state.exam_lang        = 'en'
    st.session_state.last_refresh_time = datetime.now()
    st.session_state.refresh_count    = 0
    st.rerun()

def show_available_exams():
    exams = db.get_student_exams(st.session_state.user['user_id'])

    if not exams:
        st.markdown("""
        <div style='text-align:center;padding:48px 24px;background:#1e293b;
                    border-radius:16px;border:1px dashed #334155;'>
            <div style='font-size:40px;margin-bottom:12px;'>🎓</div>
            <div style='color:white;font-size:18px;font-weight:700;margin-bottom:6px;'>No Exams Yet</div>
            <div style='color:#64748b;font-size:14px;'>
                Go to <b style='color:#3b82f6;'>Generate New Exam</b> tab to create your first practice test.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return

    EXAM_ICONS = {'JEE':'🧠','NEET':'🩺','CUET':'🎓','CUET_GT':'📘'}

    for exam in exams:
        marking        = json.loads(exam.get('marking_scheme', '{"correct": 4, "wrong": -1}'))
        question_count = db.get_question_count(exam['exam_id'])
        needed         = exam['total_questions']
        exam_type      = exam.get('exam_type', 'JEE')
        icon           = EXAM_ICONS.get(exam_type, '📝')
        is_ready       = question_count >= needed
        pool_pct       = min(100, int(question_count / max(needed, 1) * 100))

        st.markdown(f"""
        <div style='background:#1e293b;border-radius:12px;padding:18px 22px;
                    border:1px solid {"#3b82f6" if is_ready else "#334155"};
                    margin-bottom:10px;'>
            <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px;'>
                <div>
                    <span style='font-size:20px;'>{icon}</span>
                    <span style='color:white;font-weight:800;font-size:17px;margin-left:8px;'>{exam["exam_name"]}</span>
                    <span style='background:#334155;color:#94a3b8;font-size:11px;font-weight:700;
                                 padding:3px 8px;border-radius:4px;margin-left:8px;'>{exam_type}</span>
                </div>
                <span style='color:{"#10b981" if is_ready else "#f59e0b"};font-size:12px;font-weight:700;'>
                    {"✅ READY" if is_ready else f"⏳ {pool_pct}% ready"}</span>
            </div>
            <div style='display:flex;gap:20px;'>
                <span style='color:#94a3b8;font-size:13px;'>📊 <b style='color:white;'>{exam["total_questions"]}Q</b></span>
                <span style='color:#94a3b8;font-size:13px;'>⏱️ <b style='color:white;'>{exam["duration_mins"]} min</b></span>
                <span style='color:#94a3b8;font-size:13px;'>✅ <b style='color:#10b981;'>+{marking.get("correct",4)}</b>
                    &nbsp; ❌ <b style='color:#ef4444;'>{marking.get("wrong",-1)}</b></span>
                <span style='color:#94a3b8;font-size:13px;'>🗄️ Pool: <b style='color:white;'>{question_count}Q</b></span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if is_ready:
            btn_c1, btn_c2, btn_c3 = st.columns([3, 2, 1])
            with btn_c2:
                if st.button(f"🚀 START EXAM", key=f"start_{exam['exam_id']}",
                             type="primary", use_container_width=True):
                    _start_exam_session(exam)
            with btn_c3:
                if st.button("🗑️", key=f"del_{exam['exam_id']}", help="Remove exam"):
                    db.deactivate_exam(exam['exam_id']); st.rerun()
        else:
            del_c, _ = st.columns([1, 5])
            with del_c:
                if st.button("🗑️ Remove", key=f"del_{exam['exam_id']}", help="Remove"):
                    db.deactivate_exam(exam['exam_id']); st.rerun()

def show_student_results():
    """Show detailed results with correct/wrong breakdown, subject cards and answer sheet."""
    
    sessions = db.get_user_sessions(st.session_state.user['user_id'])
    
    if not sessions:
        st.markdown("""
        <div style='text-align:center;padding:40px 24px;background:#1e293b;
                    border-radius:16px;border:1px dashed #334155;'>
            <div style='font-size:40px;margin-bottom:10px;'>📋</div>
            <div style='color:white;font-size:17px;font-weight:700;margin-bottom:6px;'>No Results Yet</div>
            <div style='color:#64748b;font-size:14px;'>
                Take an exam first to see your results and answer sheet here.
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    for session in sessions:
        status_icon = "✅" if session['status'] == 'completed' else "⏳"
        
        with st.expander(f"{status_icon} {session['exam_name']} — {session['start_time'][:16]}", expanded=False):
            if session['status'] == 'completed':
                exam_id    = session['exam_id']
                session_id = session['session_id']
                
                questions = db.get_session_questions(session_id)
                responses = db.get_session_responses(session_id)
                
                correct_count = wrong_count = unattempted_count = 0
                total_marks   = 0
                section_scores: dict = {}
                response_dict = {r['question_id']: r for r in responses}
                
                for q in questions:
                    q_id = q['question_id']
                    subj = q['subject']
                    if subj not in section_scores:
                        section_scores[subj] = {'correct': 0, 'wrong': 0, 'unattempted': 0, 'score': 0.0}
                    if q_id in response_dict:
                        selected = response_dict[q_id]['selected_answer']
                        if selected:
                            if selected == q['correct_answer']:
                                correct_count += 1
                                total_marks   += q['marks_correct']
                                section_scores[subj]['correct'] += 1
                                section_scores[subj]['score']   += q['marks_correct']
                            else:
                                wrong_count += 1
                                total_marks += q['marks_wrong']
                                section_scores[subj]['wrong'] += 1
                                section_scores[subj]['score'] += q['marks_wrong']
                        else:
                            unattempted_count += 1
                            section_scores[subj]['unattempted'] += 1
                    else:
                        unattempted_count += 1
                        section_scores[subj]['unattempted'] += 1
                
                # ── Score badge ────────────────────────────────────────────────
                max_possible = sum(q['marks_correct'] for q in questions)
                pct = (total_marks / max_possible * 100) if max_possible > 0 else 0
                badge_color = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 40 else "#ef4444"

                st.markdown(f"""
                <div style='display:flex;align-items:center;gap:20px;background:#1e293b;
                            border-radius:12px;padding:16px 20px;border:1px solid {badge_color};
                            margin-bottom:16px;'>
                    <div style='font-size:36px;font-weight:900;color:{badge_color};'>{total_marks:.0f}</div>
                    <div>
                        <div style='color:#94a3b8;font-size:12px;'>out of {max_possible:.0f} marks</div>
                        <div style='color:{badge_color};font-weight:700;font-size:16px;'>{pct:.1f}%</div>
                    </div>
                </div>""", unsafe_allow_html=True)

                st.markdown("#### 📈 Performance Summary")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("🎯 Total Score", f"{total_marks:.0f}")
                with col2:
                    st.metric("✅ Correct", f"{correct_count}/{len(questions)}")
                with col3:
                    st.metric("❌ Wrong", f"{wrong_count}/{len(questions)}")
                with col4:
                    st.metric("⚪ Unattempted", f"{unattempted_count}/{len(questions)}")
                
                if (correct_count + wrong_count) > 0:
                    accuracy = (correct_count / (correct_count + wrong_count)) * 100
                    st.progress(accuracy / 100)
                    st.write(f"**Accuracy: {accuracy:.1f}%**")

                # ── Subject breakdown cards ────────────────────────────────────
                if len(section_scores) > 1:
                    st.markdown("#### 📘 Subject Breakdown")
                    scols = st.columns(min(len(section_scores), 4))
                    for i, (subj, sc) in enumerate(section_scores.items()):
                        s_acc = (sc['correct'] / (sc['correct'] + sc['wrong']) * 100
                                 if (sc['correct'] + sc['wrong']) > 0 else 0)
                        s_clr = "#10b981" if s_acc >= 70 else "#f59e0b" if s_acc >= 40 else "#ef4444"
                        with scols[i % len(scols)]:
                            st.markdown(f"""
                            <div style='background:#0f172a;border-radius:10px;padding:12px;
                                        text-align:center;border-left:4px solid {s_clr};
                                        margin-bottom:8px;'>
                                <div style='font-size:11px;color:#64748b;font-weight:700;'>{subj.upper()}</div>
                                <div style='font-size:22px;font-weight:900;color:{s_clr};'>{sc["score"]:.0f}</div>
                                <div style='font-size:11px;color:#94a3b8;'>
                                    ✅{sc["correct"]} ❌{sc["wrong"]} ⚪{sc["unattempted"]}</div>
                                <div style='font-size:12px;color:{s_clr};font-weight:700;'>{s_acc:.0f}%</div>
                            </div>""", unsafe_allow_html=True)
                
                # ── Answer Sheet ───────────────────────────────────────────────
                st.markdown("---")
                st.markdown("### 📋 Detailed Answer Sheet")
                
                for i, q in enumerate(questions, 1):
                    q_id = q['question_id']
                    
                    if q_id in response_dict and response_dict[q_id]['selected_answer']:
                        selected   = response_dict[q_id]['selected_answer']
                        is_correct = selected == q['correct_answer']
                        status_emoji = "✅" if is_correct else "❌"
                        status_color = "green" if is_correct else "red"
                    else:
                        selected     = None
                        status_emoji = "⚪"
                        status_color = "gray"
                        is_correct   = False
                    
                    with st.container():
                        topic = q.get('topic', '')
                        diff  = q.get('difficulty', '')
                        meta  = f" &nbsp;·&nbsp; <span style='color:#64748b;font-size:12px'>{topic}</span>" if topic else ""
                        diff_badge = f" &nbsp;<span style='color:#f59e0b;font-size:12px'>{diff.title()}</span>" if diff else ""
                        st.markdown(
                            f"**Question {i}** {status_emoji}{diff_badge}{meta}",
                            unsafe_allow_html=True)
                        st.write(q['question_text_en'])
                        
                        col_opts1, col_opts2 = st.columns(2)
                        with col_opts1:
                            st.write(f"A. {q['option_a_en']}")
                            st.write(f"B. {q['option_b_en']}")
                        with col_opts2:
                            st.write(f"C. {q['option_c_en']}")
                            st.write(f"D. {q['option_d_en']}")
                        
                        col_ans1, col_ans2 = st.columns(2)
                        with col_ans1:
                            st.markdown(f"**Correct Answer:** :green[{q['correct_answer']}]")
                        with col_ans2:
                            if selected:
                                color = "green" if is_correct else "red"
                                st.markdown(f"**Your Answer:** :{color}[{selected}]")
                            else:
                                st.markdown(f"**Your Answer:** :gray[Not Attempted]")
                        
                        st.markdown("---")
            else:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Status", session['status'].title())
                with col2:
                    st.metric("Started", session['start_time'][:16])
                with col3:
                    st.write("*In Progress*")

# ═══════════════════════════════════════════════════════════════════════════════
# EXAM INTERFACE WITH SECTION NAVIGATION
# ═══════════════════════════════════════════════════════════════════════════════


def _auto_save_answers() -> None:
    """Persist in-memory answers to DB every 30 s — crash-safe, silent."""
    now = time.time()
    if now - st.session_state.get('_autosave_ts', 0) < 30:
        return
    session_id = st.session_state.get('session_id')
    answers    = st.session_state.get('selected_answers', {})
    if not session_id or not answers:
        return
    try:
        for q_id, answer in answers.items():
            db.save_answer(session_id, q_id, answer)
        st.session_state['_autosave_ts'] = now
    except Exception:
        pass   # never interrupt an active exam for a save failure


def show_exam_interface():
    _auto_save_answers()   # flush answers every 30 s
    """Exam interface with:
    - CSS-styled palette: current=blue border, answered=green, skipped=red, marked=yellow, unvisited=grey
    - Offline translation via Argos Translate (100% FREE, no API key needed)
    - Correct global question numbering (no repeats)
    - Section-wise palette with attempt tracking
    """
    exam_id    = st.session_state.current_exam_id
    session_id = st.session_state.session_id
    exam = db.get_exam(exam_id)

    if not exam:
        st.error("Exam not found.")
        st.session_state.exam_started = False
        st.rerun()
        return

    limits            = db.get_exam_limits(exam_id)
    session_questions = db.get_session_questions(session_id)

    # ── Build question list for this session (first time only) ─────────────
    if not session_questions:
        all_questions = db.get_exam_questions(exam_id)
        if not all_questions:
            st.error("❌ No questions found. Please regenerate the exam.")
            if st.button("🔙 Back"):
                st.session_state.exam_started = False
                st.rerun()
            return

        exam_type = exam.get('exam_type', 'JEE')
        subject_targets = {'JEE':  {'Physics':25,'Chemistry':25,'Mathematics':25},
                           'NEET': {'Physics':50,'Chemistry':50,'Biology':100}}.get(exam_type, {})
        if exam_type == 'CUET':
            for q in all_questions: subject_targets.setdefault(q['subject'], 50)
        elif exam_type == 'CUET_GT':
            for q in all_questions: subject_targets.setdefault(q['subject'], 15)
        elif not subject_targets:
            for q in all_questions: subject_targets.setdefault(q['subject'], 999)

        SORD = ['Physics','Chemistry','Mathematics','Biology',
                'General Knowledge','Current Affairs','Logical Reasoning','Quantitative Aptitude']
        pool = {}
        for q in all_questions: pool.setdefault(q['subject'], []).append(q)
        ordered = [s for s in SORD if s in pool] + [s for s in pool if s not in SORD]

        selected = []; seq = 1
        for subj in ordered:
            qs = pool[subj]; random.shuffle(qs)
            for q in qs[:subject_targets.get(subj, len(qs))]:
                q['seq_number'] = seq; selected.append(q); seq += 1

        if not selected:
            st.error("❌ Could not select questions."); return

        db.save_session_questions(session_id, [q['question_id'] for q in selected])
        session_questions = selected

    # ── Global number map ───────────────────────────────────────────────────
    global_idx = {q['question_id']: i+1 for i, q in enumerate(session_questions)}

    SORD = ['Physics','Chemistry','Mathematics','Biology',
            'General Knowledge','Current Affairs','Logical Reasoning','Quantitative Aptitude']
    seen_subj = [s for s in SORD if any(q['subject']==s for q in session_questions)]
    for s in set(q['subject'] for q in session_questions):
        if s not in seen_subj: seen_subj.append(s)

    # ── Language + AI translation ───────────────────────────────────────────
    LANGS = {'en':'English','hi':'हिन्दी','mr':'मराठी',
             'ta':'தமிழ்','te':'తెలుగు','gu':'ગુજરાતી','bn':'বাংলা','kn':'ಕನ್ನಡ'}
    LANG_NAMES = {'en':'English','hi':'Hindi','mr':'Marathi','ta':'Tamil',
                  'te':'Telugu','gu':'Gujarati','bn':'Bengali','kn':'Kannada'}

    if 'exam_lang'            not in st.session_state: st.session_state.exam_lang            = 'en'
    if 'active_section'       not in st.session_state: st.session_state.active_section       = 'All'
    if 'ai_translations'      not in st.session_state: st.session_state.ai_translations      = {}
    if 'translation_progress' not in st.session_state: st.session_state.translation_progress = {}

    def _q_cache_id(q) -> str:
        """Return a stable, unique string key for this question (no id() reuse risk)."""
        return str(q.get('question_id') or q.get('seq_number') or hash(q.get('question_text_en','')[:60]))

    # ── Import Argos translate_text (already used in ai_generator.py) ────────
    from ai_generator import translate_text as _argos_translate

    def _auto_translate_question(q, lang_code, lang_name):
        """
        Translate one question (text + 4 options) using Argos Translate.
        - 100% offline, FREE, no API key needed
        - Formula/unit/symbol preservation handled inside translate_text()
        - Results cached in session_state to avoid re-translating
        """
        q_id   = _q_cache_id(q)
        fields = ['question_text', 'option_a', 'option_b', 'option_c', 'option_d']

        for f in fields:
            cache_key = f"{q_id}_{f}_{lang_code}"
            if cache_key in st.session_state.ai_translations:
                continue                          # already translated
            src_text = q.get(f'{f}_en', '')
            if not src_text:
                continue
            translated = _argos_translate(src_text, lang_code)
            if translated:
                st.session_state.ai_translations[cache_key] = translated

    def auto_translate_all_questions(questions_list, lang_code, lang_name):
        """
        Translate ALL questions for the selected language using Argos.
        Shows a progress bar. Skips questions already in DB or cache.
        """
        progress_key = f"translated_{lang_code}"
        if st.session_state.translation_progress.get(progress_key):
            return  # Already done for this language

        # Skip questions that already have a DB translation for this language
        untranslated = [
            q for q in questions_list
            if not q.get(f'question_text_{lang_code}', '')
            and f"{_q_cache_id(q)}_question_text_{lang_code}"
               not in st.session_state.ai_translations
        ]

        if not untranslated:
            st.session_state.translation_progress[progress_key] = True
            return

        prog_bar = st.progress(0, text=f"🌐 Translating to {lang_name}... 0/{len(untranslated)}")
        for i, q in enumerate(untranslated):
            _auto_translate_question(q, lang_code, lang_name)
            prog_bar.progress(
                (i + 1) / len(untranslated),
                text=f"🌐 Translating to {lang_name}... {i+1}/{len(untranslated)}"
            )
        prog_bar.empty()
        st.session_state.translation_progress[progress_key] = True

    def get_text(q, field):
        """
        Get display text for a question field in the current exam language.
        Priority: DB stored translation → Argos session cache → on-the-fly translate → English.
        """
        lang = st.session_state.exam_lang
        q_id = _q_cache_id(q)

        if lang == 'en':
            return q.get(f'{field}_en', '') or ''

        # 1. DB stored translation (generated at exam-creation time by Argos)
        val = q.get(f'{field}_{lang}', '')
        if val:
            return val

        # 2. Session cache (translated live when student switched language)
        val = st.session_state.ai_translations.get(f"{q_id}_{field}_{lang}", '')
        if val:
            return val

        # 3. Translate right now on the fly and cache it (for the current question)
        src = q.get(f'{field}_en', '')
        if src and lang != 'en':
            translated = _argos_translate(src, lang)
            if translated:
                st.session_state.ai_translations[f"{q_id}_{field}_{lang}"] = translated
                return translated

        # 4. Hindi fallback → English fallback
        return q.get(f'{field}_hi', '') or q.get(f'{field}_en', '') or ''

    # ── CSS for palette ─────────────────────────────────────────────────────
    st.markdown("""
    <style>
    /* ── Palette button base — bigger, bolder ── */
    .pal-current button,
    .pal-answered button,
    .pal-skipped button,
    .pal-marked button,
    .pal-ans-marked button,
    .pal-unvisited button {
        border-radius: 8px !important;
        font-weight: 800 !important;
        font-size: 15px !important;
        min-height: 44px !important;
        padding: 6px 4px !important;
        transition: transform 0.1s !important;
    }
    .pal-current button:hover,
    .pal-answered button:hover,
    .pal-skipped button:hover,
    .pal-marked button:hover,
    .pal-ans-marked button:hover,
    .pal-unvisited button:hover {
        transform: scale(1.08) !important;
        opacity: 0.92 !important;
    }
    /* Current question — bright blue + gold glow */
    .pal-current button {
        background: #2563eb !important;
        color: white !important;
        border: 3px solid #facc15 !important;
        box-shadow: 0 0 10px 2px #facc15 !important;
    }
    /* Answered — green */
    .pal-answered button {
        background: #16a34a !important;
        color: white !important;
        border: 1px solid #15803d !important;
    }
    /* Marked for review — amber */
    .pal-marked button {
        background: #d97706 !important;
        color: white !important;
        border: 1px solid #b45309 !important;
    }
    /* Answered + Marked — purple */
    .pal-ans-marked button {
        background: #7c3aed !important;
        color: white !important;
        border: 1px solid #6d28d9 !important;
    }
    /* Skipped (visited, not answered) — red */
    .pal-skipped button {
        background: #dc2626 !important;
        color: white !important;
        border: 1px solid #b91c1c !important;
    }
    /* Not visited — dark grey */
    .pal-unvisited button {
        background: #374151 !important;
        color: #d1d5db !important;
        border: 1px solid #4b5563 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ── TOP BAR ─────────────────────────────────────────────────────────────
    col_name, col_time, col_exit = st.columns([5, 2, 1])
    with col_name:
        label = {'JEE':'🧠 JEE Main','NEET':'🩺 NEET','CUET':'🎓 CUET','CUET_GT':'📘 CUET GT'
                 }.get(exam.get('exam_type',''), '📝')
        st.markdown(f"## {label} — {exam['exam_name']}")
    with col_time:
        # ── SERVER-AUTHORITATIVE TIMER ────────────────────────────────────
        # Recalculate from DB start_time every render — refresh cannot cheat
        server_remaining = db.get_server_time_remaining(session_id)
        st.session_state.time_remaining = server_remaining
        if server_remaining <= 0:
            # Log auto-submit as cheat event if very early
            submit_exam(); return
        m, s = divmod(server_remaining, 60)
        color = 'red' if m < 5 else 'orange' if m < 15 else 'green'
        st.markdown(f"### ⏱️ :{color}[{m:02d}:{s:02d}]")
        # ── ANTI-CHEAT: refresh frequency detection ───────────────────────
        now = datetime.now()
        last = st.session_state.get('last_refresh_time')
        if last and (now - last).total_seconds() < 3:
            st.session_state.refresh_count = st.session_state.get('refresh_count', 0) + 1
            if st.session_state.refresh_count > 10:
                db.log_cheat_event(session_id,
                    st.session_state.user['user_id'],
                    'rapid_refresh',
                    f"Refresh count: {st.session_state.refresh_count}")
        st.session_state.last_refresh_time = now
    with col_exit:
        if st.button("🚪 Exit", use_container_width=True):
            st.session_state.show_exit_confirm = True; st.rerun()

    if st.session_state.show_exit_confirm:
        st.warning("⚠️ Submit & exit? You cannot re-enter!")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Yes, Submit", type="primary", use_container_width=True):
                submit_exam(); st.session_state.show_exit_confirm = False; return
        with c2:
            if st.button("❌ No, Continue", use_container_width=True):
                st.session_state.show_exit_confirm = False; st.rerun()
        return

    # ── ATTEMPT TRACKER ─────────────────────────────────────────────────────
    if limits.get('has_limits'):
        st.markdown("---")
        etype = exam.get('exam_type','')
        headers = {'NEET':'📊 NEET *(Best 180/200)*','CUET':'📊 CUET *(Best 40/50 per subject)*',
                   'CUET_GT':'📊 CUET GT *(Best 50/60)*'}
        if etype in headers: st.markdown(f"#### {headers[etype]}")
        if limits.get('subject_limits'):
            cols = st.columns(len(limits['subject_limits']))
            for idx,(subj,lim) in enumerate(limits['subject_limits'].items()):
                att = sum(1 for q in session_questions if q['subject']==subj
                          and q['question_id'] in st.session_state.selected_answers)
                req = lim['attempt']
                delta = (f"⚠️ Need {req-att}" if att<req else
                         "✅ Perfect!" if att==req else f"❌ {att-req} extra")
                with cols[idx]: st.metric(f"{subj} ({lim['given']}Q)", f"{att}/{req}", delta)
        else:
            att = len(st.session_state.selected_answers)
            req = limits['total_attempt']; tot = limits['total_given']
            delta = (f"⚠️ Need {req-att}" if att<req else
                     "✅ Perfect!" if att==req else f"❌ {att-req} extra")
            st.metric(f"Attempted (Total {tot}Q)", f"{att}/{req}", delta)
        st.info("💡 Only your **best** answers count!")

    # ── LANGUAGE BAR ────────────────────────────────────────────────────────
    st.markdown("---")
    st.caption("🌐 Language / भाषा:")
    lang_cols = st.columns(len(LANGS))
    for i,(code,label) in enumerate(LANGS.items()):
        with lang_cols[i]:
            btype = "primary" if st.session_state.exam_lang==code else "secondary"
            if st.button(label, key=f"lang_{code}", type=btype, use_container_width=True):
                prev_lang = st.session_state.exam_lang
                st.session_state.exam_lang = code
                # Trigger auto-translation if switching to non-English
                if code != 'en' and code != prev_lang:
                    st.session_state.translation_progress[f"translated_{code}"] = False
                st.rerun()

    # ── AUTO-TRANSLATE all questions when non-English is selected ────────────
    if st.session_state.exam_lang != 'en':
        _lang_code = st.session_state.exam_lang
        _lang_name = LANG_NAMES.get(_lang_code, _lang_code)
        if not st.session_state.translation_progress.get(f"translated_{_lang_code}"):
            auto_translate_all_questions(session_questions, _lang_code, _lang_name)
            st.rerun()

    # ── SECTION TABS ─────────────────────────────────────────────────────────
    st.markdown("---")
    tab_labels = ["🗂️ All"] + [f"📘 {s}" for s in seen_subj]
    chosen_tab = st.radio("📚 Section", tab_labels, horizontal=True, key="section_nav")
    active_sec = "All" if chosen_tab=="🗂️ All" else chosen_tab.replace("📘 ","")

    if active_sec != st.session_state.active_section:
        st.session_state.active_section = active_sec
        st.session_state.current_question_idx = 0
        st.rerun()

    filtered_qs = session_questions if active_sec=="All" \
                  else [q for q in session_questions if q['subject']==active_sec]

    # ── QUESTION AREA (full width) ───────────────────────────────────────────
    st.markdown("---")

    cur_idx = st.session_state.current_question_idx
    if cur_idx >= len(filtered_qs): cur_idx = 0; st.session_state.current_question_idx = 0
    cq    = filtered_qs[cur_idx]
    q_id  = cq['question_id']
    gnum  = global_idx[q_id]
    lang  = st.session_state.exam_lang

    # ── Question header ────────────────────────────────────────────────────
    hcol1, hcol2 = st.columns([3, 1])
    with hcol1:
        st.markdown(
            f"### Q{gnum} of {len(session_questions)} &nbsp;"
            f"<span style='color:#aaa;font-size:0.75em'>"
            f"({cq['subject']} — Q{cur_idx+1} of {len(filtered_qs)})</span>",
            unsafe_allow_html=True)
    with hcol2:
        diff  = cq.get('difficulty', 'hard')
        mc    = cq.get('marks_correct', 4)
        mw    = cq.get('marks_wrong', -1)
        badge = {'hard': '🟠 Hard', 'hardest': '🔴 Hardest'}.get(diff, '🟡 Med')
        st.markdown(f"**{badge}** &nbsp; ✅+{mc} &nbsp; ❌{mw}", unsafe_allow_html=True)

    # ── Translation status badge (auto-translate runs above in lang bar) ──

    # ── Question text ──────────────────────────────────────────────────────
    q_text = get_text(cq, 'question_text')
    st.markdown(
        f"<div style='background:#1e293b;border-left:4px solid #3b82f6;"
        f"padding:16px 20px;border-radius:8px;font-size:17px;line-height:1.7;"
        f"color:#f1f5f9;margin:10px 0;'>{q_text}</div>",
        unsafe_allow_html=True)

    if lang != 'en':
        en_text = cq.get('question_text_en', '')
        if en_text:
            st.caption(f"📖 *(English): {en_text}*")

    st.markdown("")

    # ── Options ────────────────────────────────────────────────────────────
    cur_ans = st.session_state.selected_answers.get(q_id)
    opt_display, opt_letters = [], []
    for letter in ['A', 'B', 'C', 'D']:
        key = f'option_{letter.lower()}'
        txt = get_text(cq, key) or cq.get(f'{key}_en', letter)
        opt_display.append(f"{letter}.  {txt}")
        opt_letters.append(letter)

    try:    def_idx = opt_letters.index(cur_ans) if cur_ans in opt_letters else None
    except: def_idx = None

    chosen = st.radio("**Choose your answer:**", opt_display,
                      index=def_idx, key=f"q_{q_id}_{lang}_{st.session_state.clear_version.get(q_id,0)}")
    # Save answer — version key ensures this only fires on genuine user selection
    if chosen:
        prev = st.session_state.selected_answers.get(q_id)
        st.session_state.selected_answers[q_id] = chosen[0]
        # Instant DB save
        db.save_response(session_id, q_id, chosen[0],
                         q_id in st.session_state.marked_for_review, True)
        # Anti-cheat: rapid answer switching
        if prev and prev != chosen[0]:
            cnt = st.session_state.answer_change_count.get(q_id, 0) + 1
            st.session_state.answer_change_count[q_id] = cnt
            if cnt > 5:
                db.log_cheat_event(session_id,
                    st.session_state.user['user_id'],
                    'rapid_answer_switch',
                    f"Q#{q_id} changed {cnt} times")
        # Persist current question index for crash recovery
        db.update_session_question_idx(session_id,
            st.session_state.current_question_idx)
        st.session_state.visited_questions.add(q_id)
    # ── Navigation buttons ─────────────────────────────────────────────────
    st.markdown("")
    n1, n2, n3, n4 = st.columns(4)
    with n1:
        if st.button("⬅️ Previous", use_container_width=True, disabled=(cur_idx == 0)):
            st.session_state.current_question_idx -= 1; st.rerun()
    with n2:
        is_marked = q_id in st.session_state.marked_for_review
        if st.button("🟡 Unmark" if is_marked else "🔖 Mark Review", use_container_width=True):
            (st.session_state.marked_for_review.discard(q_id) if is_marked
             else st.session_state.marked_for_review.add(q_id))
            st.rerun()
    with n3:
        if st.button("🗑️ Clear Response", use_container_width=True):
            # Remove answer AND bump version so radio widget recreates fresh
            st.session_state.selected_answers.pop(q_id, None)
            cv = st.session_state.clear_version.get(q_id, 0)
            st.session_state.clear_version[q_id] = cv + 1
            st.rerun()
    with n4:
        if cur_idx < len(filtered_qs) - 1:
            if st.button("Next ➡️", type="primary", use_container_width=True):
                st.session_state.current_question_idx += 1; st.rerun()
        else:
            if st.button("✅ Submit", type="primary", use_container_width=True):
                submit_exam(); return

    # ═══════════════════════════════════════════════════════════════════════════
    # QUESTION PALETTE — BOTTOM, FULL WIDTH
    # ═══════════════════════════════════════════════════════════════════════════
    st.markdown("---")

    # ── Legend + Summary row (horizontal, big, easy to read) ──────────────────
    total_ans  = len(st.session_state.selected_answers)
    total_mrk  = len(st.session_state.marked_for_review)
    total_skip = len([q for q in session_questions
                      if q['question_id'] not in st.session_state.selected_answers
                      and q['question_id'] in st.session_state.visited_questions])
    total_unsn = len([q for q in session_questions
                      if q['question_id'] not in st.session_state.visited_questions])

    st.markdown(
        f"""
        <div style='display:flex;flex-wrap:wrap;gap:12px;align-items:center;
                    background:#1e293b;padding:16px 20px;border-radius:12px;
                    margin-bottom:16px;'>
            <span style='font-size:15px;font-weight:700;color:#e2e8f0;
                         margin-right:8px;'>📋 Legend &amp; Status:</span>
            <span style='background:#2563eb;color:white;padding:7px 16px;
                         border-radius:8px;font-size:14px;font-weight:700;
                         border:3px solid #facc15;'>▶ Current</span>
            <span style='background:#16a34a;color:white;padding:7px 16px;
                         border-radius:8px;font-size:14px;font-weight:700;'>
                         ✅ Answered &nbsp;<b style='font-size:18px'>{total_ans}</b></span>
            <span style='background:#dc2626;color:white;padding:7px 16px;
                         border-radius:8px;font-size:14px;font-weight:700;'>
                         ⏭ Skipped &nbsp;<b style='font-size:18px'>{total_skip}</b></span>
            <span style='background:#d97706;color:white;padding:7px 16px;
                         border-radius:8px;font-size:14px;font-weight:700;'>
                         🔖 Marked &nbsp;<b style='font-size:18px'>{total_mrk}</b></span>
            <span style='background:#7c3aed;color:white;padding:7px 16px;
                         border-radius:8px;font-size:14px;font-weight:700;'>🟣 Ans+Marked</span>
            <span style='background:#374151;color:#d1d5db;padding:7px 16px;
                         border-radius:8px;font-size:14px;font-weight:700;'>
                         ⚪ Not Seen &nbsp;<b style='font-size:18px'>{total_unsn}</b></span>
            <span style='margin-left:auto;color:#94a3b8;font-size:14px;font-weight:600;'>
                         📝 Total: <b style='color:white;font-size:18px'>
                         {len(session_questions)}</b></span>
        </div>
        """,
        unsafe_allow_html=True)

    # ── Section-wise palette (full width, 10 per row) ─────────────────────────
    SUBJ_COLORS = {
        'Physics': '#1d4ed8',       'Chemistry': '#065f46',
        'Mathematics': '#6d28d9',   'Biology': '#92400e',
        'General Knowledge': '#991b1b', 'Current Affairs': '#155e75',
        'Logical Reasoning': '#5b21b6', 'Quantitative Aptitude': '#14532d'
    }
    SUBJ_SHORT = {
        'Physics': 'PHYSICS', 'Chemistry': 'CHEMISTRY', 'Mathematics': 'MATHEMATICS',
        'Biology': 'BIOLOGY', 'General Knowledge': 'GENERAL KNOWLEDGE',
        'Current Affairs': 'CURRENT AFFAIRS', 'Logical Reasoning': 'LOGICAL REASONING',
        'Quantitative Aptitude': 'QUANTITATIVE APTITUDE'
    }

    for subj in seen_subj:
        subj_qs = [q for q in session_questions if q['subject'] == subj]
        if not subj_qs: continue

        first_g = global_idx[subj_qs[0]['question_id']]
        last_g  = global_idx[subj_qs[-1]['question_id']]
        sc      = SUBJ_COLORS.get(subj, '#374151')
        label   = SUBJ_SHORT.get(subj, subj.upper())

        # Count attempted in this section
        att_count = sum(1 for q in subj_qs
                        if q['question_id'] in st.session_state.selected_answers)

        # Limit info
        lim_info = ""
        if limits.get('subject_limits') and subj in limits.get('subject_limits', {}):
            lim = limits['subject_limits'][subj]
            lim_info = f"  |  Attempted: {att_count} / {lim['attempt']} (of {lim['given']})"
        elif limits.get('has_limits'):
            lim_info = f"  |  Attempted: {att_count} / {len(subj_qs)}"

        # Section header bar
        st.markdown(
            f"<div style='background:{sc};color:white;padding:8px 16px;"
            f"border-radius:8px;font-size:15px;font-weight:700;margin:10px 0 6px 0;"
            f"letter-spacing:0.5px;'>"
            f"📘 {label} &nbsp;&nbsp; Q{first_g} – Q{last_g}{lim_info}</div>",
            unsafe_allow_html=True)

        # Palette buttons — 10 per row, full width
        COLS = 10
        for row_start in range(0, len(subj_qs), COLS):
            row_qs   = subj_qs[row_start:row_start + COLS]
            btn_cols = st.columns(COLS)
            for j, q in enumerate(row_qs):
                qid    = q['question_id']
                gn     = global_idx[qid]
                ans    = qid in st.session_state.selected_answers
                mrk    = qid in st.session_state.marked_for_review
                vis    = qid in st.session_state.visited_questions
                is_cur = (qid == cq['question_id'])

                if is_cur:
                    css_cls = "pal-current";    prefix = "▶"
                elif ans and mrk:
                    css_cls = "pal-ans-marked"; prefix = "★"
                elif ans:
                    css_cls = "pal-answered";   prefix = ""
                elif mrk:
                    css_cls = "pal-marked";     prefix = "◆"
                elif vis:
                    css_cls = "pal-skipped";    prefix = ""
                else:
                    css_cls = "pal-unvisited";  prefix = ""

                with btn_cols[j]:
                    st.markdown(f"<div class='{css_cls}'>", unsafe_allow_html=True)
                    if st.button(
                        f"{prefix}{gn}",
                        key=f"pal_{qid}",
                        use_container_width=True,
                        help=f"Q{gn} — {subj}"
                    ):
                        st.session_state.active_section = subj
                        sec_list = [qq for qq in session_questions if qq['subject'] == subj]
                        st.session_state.current_question_idx = sec_list.index(q)
                        st.rerun()
                    st.markdown("</div>", unsafe_allow_html=True)

    # Submit at bottom
    st.markdown("")
    # ── Submit summary warning ──────────────────────────────────────────────
    unanswered = len([q for q in session_questions
                      if q['question_id'] not in st.session_state.selected_answers])
    sub_c1, sub_c2, sub_c3 = st.columns([2, 2, 2])
    with sub_c2:
        btn_label = (f"✅ SUBMIT EXAM ({unanswered} unanswered ⚠️)"
                     if unanswered > 0 else "✅ SUBMIT EXAM")
        if st.button(btn_label, type="primary", use_container_width=True):
            submit_exam(); return

    time.sleep(0.5)  # short sleep keeps timer accurate without excessive CPU
    st.rerun()

def submit_exam():
    """Production-grade submission: idempotent, immutable result, locked session."""
    exam_id    = st.session_state.current_exam_id
    session_id = st.session_state.session_id
    user_id    = st.session_state.user['user_id']

    # ── Guard: already submitted ──────────────────────────────────────────
    sess = db.get_session(session_id)
    if sess and sess.get('result_locked'):
        st.session_state.exam_started = False
        return

    questions = db.get_session_questions(session_id)
    limits    = db.get_exam_limits(exam_id)

    # ── Flush any in-memory answers not yet in DB ─────────────────────────
    for question in questions:
        q_id = question['question_id']
        selected = st.session_state.selected_answers.get(q_id)
        marked   = q_id in st.session_state.marked_for_review
        db.save_response(session_id, q_id, selected, marked, True)

    # ── Score calculation (from DB — not session_state) ───────────────────
    if limits.get('has_limits'):
        total_score = db.calculate_score_with_limits(session_id, limits)
    else:
        total_score = db.calculate_normal_score(session_id)

    # ── Per-section breakdown ─────────────────────────────────────────────
    correct = wrong = unattempted = 0
    section_scores: dict = {}
    for question in questions:
        q_id  = question['question_id']
        subj  = question['subject']
        if subj not in section_scores:
            section_scores[subj] = {'correct': 0, 'wrong': 0,
                                    'unattempted': 0, 'score': 0.0}
        sel = st.session_state.selected_answers.get(q_id)
        if sel:
            if sel == question['correct_answer']:
                correct += 1
                section_scores[subj]['correct'] += 1
                section_scores[subj]['score']   += question['marks_correct']
            else:
                wrong += 1
                section_scores[subj]['wrong'] += 1
                section_scores[subj]['score'] += question['marks_wrong']
        else:
            unattempted += 1
            section_scores[subj]['unattempted'] += 1

    # ── Write immutable result record ─────────────────────────────────────
    db.save_result(session_id, user_id, exam_id, total_score,
                   correct, wrong, unattempted, section_scores)

    # ── Lock session — idempotent, blocks re-submission ───────────────────
    db.update_session_status(session_id, 'completed', total_score)
    db.deactivate_exam(exam_id)

    # Store section scores in session_state for immediate display
    st.session_state._last_section_scores = section_scores

    st.session_state.exam_started = False
    
    st.success("✅ Exam submitted successfully!")
    st.balloons()
    
    st.markdown("---")

    # ── Score badge ────────────────────────────────────────────────────────────
    max_possible = sum(q['marks_correct'] for q in questions)
    pct = (total_score / max_possible * 100) if max_possible > 0 else 0
    badge_color  = "#10b981" if pct >= 70 else "#f59e0b" if pct >= 40 else "#ef4444"
    badge_label  = "🏆 Excellent!" if pct >= 70 else "📈 Good Effort" if pct >= 40 else "📚 Keep Practising"

    st.markdown(f"""
    <div style='background:linear-gradient(135deg,#1e293b,#0f172a);border-radius:16px;
                padding:24px 32px;text-align:center;border:2px solid {badge_color};
                margin-bottom:20px;'>
        <div style='font-size:48px;font-weight:900;color:{badge_color};line-height:1;'>
            {total_score:.0f}
        </div>
        <div style='color:#94a3b8;font-size:15px;margin-top:4px;'>
            out of {max_possible:.0f} possible marks &nbsp;·&nbsp;
            <span style='color:{badge_color};font-weight:700;'>{pct:.1f}%</span>
        </div>
        <div style='margin-top:10px;font-size:18px;font-weight:700;color:{badge_color};'>
            {badge_label}
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 📈 Performance Summary")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🎯 Total Score", f"{total_score:.0f}")
    with col2:
        st.metric("✅ Correct", f"{correct}/{len(questions)}")
    with col3:
        st.metric("❌ Wrong", f"{wrong}/{len(questions)}")
    with col4:
        st.metric("⚪ Unattempted", f"{unattempted}/{len(questions)}")
    
    if (correct + wrong) > 0:
        accuracy = (correct / (correct + wrong)) * 100
        st.progress(accuracy / 100)
        st.write(f"**Accuracy: {accuracy:.1f}%**")
    
    # ── Subject-wise breakdown ─────────────────────────────────────────────────
    if len(section_scores) > 1:
        st.markdown("---")
        st.markdown("#### 📘 Subject-wise Breakdown")
        subj_cols = st.columns(len(section_scores))
        for i, (subj, sc) in enumerate(section_scores.items()):
            total_subj = sc['correct'] + sc['wrong'] + sc['unattempted']
            subj_acc   = (sc['correct'] / (sc['correct'] + sc['wrong']) * 100
                          if (sc['correct'] + sc['wrong']) > 0 else 0)
            sc_color   = "#10b981" if subj_acc >= 70 else "#f59e0b" if subj_acc >= 40 else "#ef4444"
            with subj_cols[i]:
                st.markdown(f"""
                <div style='background:#1e293b;border-radius:10px;padding:14px;
                            text-align:center;border-left:4px solid {sc_color};'>
                    <div style='font-size:12px;color:#64748b;font-weight:700;
                                letter-spacing:0.5px;'>{subj.upper()}</div>
                    <div style='font-size:26px;font-weight:900;color:{sc_color};margin:4px 0;'>
                        {sc["score"]:.0f}
                    </div>
                    <div style='font-size:12px;color:#94a3b8;'>
                        ✅{sc["correct"]} &nbsp; ❌{sc["wrong"]} &nbsp; ⚪{sc["unattempted"]}
                    </div>
                    <div style='font-size:13px;color:{sc_color};font-weight:700;margin-top:4px;'>
                        {subj_acc:.0f}% acc
                    </div>
                </div>""", unsafe_allow_html=True)

    # Show limit info if applicable
    st.markdown("---")
    if limits.get('has_limits'):
        st.info(f"""
        💡 **Scoring Note:** 
        - Questions Given: {limits['total_given']}
        - Best Answers Counted: {limits['total_attempt']}
        - Your score is based on your best {limits['total_attempt']} answers!
        """)
    
    st.info("💡 Your full answer sheet is in the **My Results** tab on your dashboard.")
    
    col_back1, col_back2, col_back3 = st.columns([1, 2, 1])
    with col_back2:
        if st.button("🏠 Back to Dashboard", use_container_width=True, type="primary"):
            st.session_state.exam_started = False
            st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# IMPROVED ADMIN DASHBOARD
# ═══════════════════════════════════════════════════════════════════════════════

def show_admin_dashboard():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("👨‍💼 Admin Dashboard")
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.rerun()
    
    st.markdown("---")
    
    stats = db.get_database_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("👥 Students", stats['total_students'])
    with col2:
        st.metric("📝 Active Exams", stats['active_exams'])
    with col3:
        st.metric("❓ Total Questions", stats['total_questions'])
    with col4:
        st.metric("✅ Completed Sessions", stats['completed_sessions'])

    # ── AI System Status panel ─────────────────────────────────────────────────
    from ollama_manager import OLLAMA_MODEL as _ACTIVE_MODEL, clear_response_cache

    with st.expander(f"🤖 AI System Status — {_ACTIVE_MODEL} / Ollama", expanded=False):
        ai_status = get_status()

        # ── 5-card status row ─────────────────────────────────────────────────
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            ok = ai_status['ollama_running']
            st.markdown(f"""
            <div style='background:#1e293b;border-radius:10px;padding:14px;text-align:center;
                        border-left:4px solid {"#10b981" if ok else "#ef4444"};'>
                <div style='font-size:22px;'>{"🟢" if ok else "🔴"}</div>
                <div style='color:#94a3b8;font-size:11px;font-weight:700;margin-top:4px;
                             letter-spacing:0.5px;'>OLLAMA SERVER</div>
                <div style='color:{"#10b981" if ok else "#ef4444"};font-size:13px;font-weight:700;'>
                    {"Running" if ok else "Offline"}</div>
            </div>""", unsafe_allow_html=True)
        with c2:
            ok = ai_status['model_pulled']
            model_short = _ACTIVE_MODEL.upper().replace(':', ' ')
            st.markdown(f"""
            <div style='background:#1e293b;border-radius:10px;padding:14px;text-align:center;
                        border-left:4px solid {"#10b981" if ok else "#f59e0b"};'>
                <div style='font-size:22px;'>{"✅" if ok else "⚠️"}</div>
                <div style='color:#94a3b8;font-size:11px;font-weight:700;margin-top:4px;
                             letter-spacing:0.5px;'>{model_short}</div>
                <div style='color:{"#10b981" if ok else "#f59e0b"};font-size:13px;font-weight:700;'>
                    {"Downloaded" if ok else "Not Pulled"}</div>
            </div>""", unsafe_allow_html=True)
        with c3:
            ok = ai_status['model_warm']
            st.markdown(f"""
            <div style='background:#1e293b;border-radius:10px;padding:14px;text-align:center;
                        border-left:4px solid {"#10b981" if ok else "#f59e0b"};'>
                <div style='font-size:22px;'>{"🔥" if ok else "❄️"}</div>
                <div style='color:#94a3b8;font-size:11px;font-weight:700;margin-top:4px;
                             letter-spacing:0.5px;'>MODEL WARM</div>
                <div style='color:{"#10b981" if ok else "#f59e0b"};font-size:13px;font-weight:700;'>
                    {"In RAM" if ok else "Not Loaded"}</div>
            </div>""", unsafe_allow_html=True)
        with c4:
            n = ai_status['cached_responses']
            st.markdown(f"""
            <div style='background:#1e293b;border-radius:10px;padding:14px;text-align:center;
                        border-left:4px solid #3b82f6;'>
                <div style='font-size:22px;'>⚡</div>
                <div style='color:#94a3b8;font-size:11px;font-weight:700;margin-top:4px;
                             letter-spacing:0.5px;'>CACHE</div>
                <div style='color:#3b82f6;font-size:13px;font-weight:700;'>{n} prompts</div>
            </div>""", unsafe_allow_html=True)
        with c5:
            alive = ai_status.get('warmup_thread_alive', False)
            st.markdown(f"""
            <div style='background:#1e293b;border-radius:10px;padding:14px;text-align:center;
                        border-left:4px solid {"#10b981" if alive else "#64748b"};'>
                <div style='font-size:22px;'>{"💓" if alive else "⏸️"}</div>
                <div style='color:#94a3b8;font-size:11px;font-weight:700;margin-top:4px;
                             letter-spacing:0.5px;'>KEEP-ALIVE</div>
                <div style='color:{"#10b981" if alive else "#64748b"};font-size:13px;font-weight:700;'>
                    {"Active" if alive else "Inactive"}</div>
            </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if not ai_status['ollama_running']:
            st.warning("⚠️ Ollama is not running. Start it with: `ollama serve`")
        elif not ai_status['model_pulled']:
            st.warning(f"⚠️ **{_ACTIVE_MODEL}** not found. Pull it once:\n```\nollama pull {_ACTIVE_MODEL}\n```\n*(~2 GB one-time download, takes 2–5 minutes)*")
        elif not ai_status['model_warm']:
            st.info(f"💡 **{_ACTIVE_MODEL}** is ready but not yet loaded into RAM. It will warm up automatically on first exam generation.")
        else:
            st.success(f"✅ **{_ACTIVE_MODEL}** fully operational — exam generation is ready!")

        if st.button("🗑️ Clear AI Response Cache", help="Forces fresh questions on next generation"):
            cleared = clear_response_cache()
            st.success(f"✅ Cleared {cleared} cached responses. Next generation will be fully fresh.")

    st.markdown("---")
    
    # IMPROVED: Combined tabs - Student Data includes exam info
    tab1, tab2 = st.tabs(["👥 Student Data & Exams", "➕ Generate Test Exam"])
    
    with tab1:
        show_student_data_with_exams()
    
    with tab2:
        show_admin_exam_generator()

def show_student_data_with_exams():
    """IMPROVED: Unified student data view with exam information"""
    st.header("👥 Student Data & Performance")
    
    # Show all exams first
    st.subheader("📝 All Exams")
    exams = db.get_all_exams()
    
    if exams:
        for exam in exams:
            with st.expander(f"📋 {exam['exam_name']} ({exam['exam_type']})", expanded=False):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Questions:** {exam['total_questions']}")
                    st.write(f"**Duration:** {exam['duration_mins']} min")
                with col2:
                    st.write(f"**Status:** {'✅ Active' if exam['is_active'] else '❌ Inactive'}")
                    st.write(f"**Created:** {exam['created_at'][:10]}")
                with col3:
                    question_count = db.get_question_count(exam['exam_id'])
                    st.write(f"**Questions in DB:** {question_count}")
                    
                    attempts = db.get_exam_attempts(exam['exam_id'])
                    st.write(f"**Total Attempts:** {attempts}")
                
                # Show students who attempted this exam
                st.markdown("**Students who attempted this exam:**")
                sessions = db.get_exam_sessions(exam['exam_id'])
                
                if sessions:
                    for session in sessions:
                        user = db.get_user_by_id(session['user_id'])
                        if user:
                            st.write(f"- {user['full_name']} (@{user['username']}) - Score: {session.get('total_score', 0):.0f} - Status: {session['status']}")
                else:
                    st.write("*No attempts yet*")
                
                if st.button(f"🗑️ Delete Exam", key=f"del_exam_{exam['exam_id']}", type="secondary"):
                    success, msg = db.delete_exam(exam['exam_id'])
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
    else:
        st.info("No exams created yet")
    
    # Show all students
    st.markdown("---")
    st.subheader("📊 All Students")
    
    users = db.get_all_users()
    students = [u for u in users if u['user_type'] == 'student']
    
    if not students:
        st.info("No students registered yet")
        return
    
    st.write(f"**Total Students: {len(students)}**")
    
    for student in students:
        with st.expander(f"👤 {student['full_name']} (@{student['username']})", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**User ID:** {student['user_id']}")
                st.write(f"**Username:** {student['username']}")
                st.write(f"**Full Name:** {student['full_name']}")
                st.write(f"**Language:** {student['preferred_lang']}")
                st.write(f"**Registered:** {student['created_at'][:10]}")
            
            with col2:
                sessions = db.get_user_sessions(student['user_id'])
                st.write(f"**Total Exams Attempted:** {len(sessions)}")
                
                completed = [s for s in sessions if s['status'] == 'completed']
                st.write(f"**Completed:** {len(completed)}")
                
                if completed:
                    avg_score = sum(s.get('total_score', 0) for s in completed) / len(completed)
                    st.write(f"**Average Score:** {avg_score:.0f}")
                    
                    max_score = max(s.get('total_score', 0) for s in completed)
                    st.write(f"**Best Score:** {max_score:.0f}")
            
            # Show exam attempts with details
            if sessions:
                st.markdown("**Exam Attempts:**")
                for session in sessions:
                    status_icon = "✅" if session['status'] == 'completed' else "⏳"
                    
                    # Get detailed results if completed
                    if session['status'] == 'completed':
                        questions = db.get_session_questions(session['session_id'])
                        responses = db.get_session_responses(session['session_id'])
                        
                        correct_count = 0
                        wrong_count = 0
                        unattempted_count = 0
                        
                        response_dict = {r['question_id']: r for r in responses}
                        
                        for q in questions:
                            q_id = q['question_id']
                            if q_id in response_dict and response_dict[q_id]['selected_answer']:
                                if response_dict[q_id]['selected_answer'] == q['correct_answer']:
                                    correct_count += 1
                                else:
                                    wrong_count += 1
                            else:
                                unattempted_count += 1
                        
                        st.write(f"{status_icon} **{session['exam_name']}** — Score: **{session.get('total_score', 0):.0f}** | ✅ {correct_count} ❌ {wrong_count} ⚪ {unattempted_count} | {session['start_time'][:10]}")
                    else:
                        st.write(f"{status_icon} **{session['exam_name']}** | Status: {session['status']} | Started: {session['start_time'][:16]}")
            
            if st.button(f"🗑️ Delete Student", key=f"del_{student['user_id']}", type="secondary"):
                success, msg = db.delete_user(student['user_id'])
                if success:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

def show_admin_exam_generator():
    """IMPROVED: Admin can generate test exams - COMPLETE WITH PHASE 1+2"""
    st.header("➕ Generate Test Exam (Admin)")
    st.info("💡 Generate test exams with FULL implementation (Phase 1 + Phase 2 optional questions)")
    
    exam_type = st.selectbox("📚 Select Exam Type", 
                            ['JEE Main 2026', 'NEET (UG) 2026', 'CUET Domain', 'CUET General Test'], 
                            key="admin_exam_type")
    
    if exam_type == 'JEE Main 2026':
        st.info("🧠 **JEE Main 2026:** 75 questions (25 each) | +4/-1 | 300 marks | 180 min")
        
        with st.form("admin_jee_form"):
            exam_name = st.text_input("Exam Name", value=f"Admin Test JEE {datetime.now().strftime('%d-%m-%Y %H:%M')}")
            include_hindi = st.checkbox("Include Hindi", value=True, key="admin_jee_hindi")
            
            st.success("✅ Physics: 25 | Chemistry: 25 | Mathematics: 25")
            
            if st.form_submit_button("🚀 Generate Admin Test Exam", type="primary"):
                generate_exam_for_student_improved('JEE', exam_name, {
                    'Physics': 25, 'Chemistry': 25, 'Mathematics': 25
                }, 180, include_hindi, created_by=st.session_state.user['user_id'])
    
    elif exam_type == 'NEET (UG) 2026':
        st.info("🩺 **NEET (UG) 2026:** 200 questions | Best 180 counted (45+45+90) | +4/-1 | 720 marks")
        
        with st.form("admin_neet_form"):
            exam_name = st.text_input("Exam Name", value=f"Admin Test NEET {datetime.now().strftime('%d-%m-%Y %H:%M')}")
            include_hindi = st.checkbox("Include Hindi", value=True, key="admin_neet_hindi")
            
            st.success("✅ Physics: 50 | Chemistry: 50 | Biology: 100")
            st.info("✨ Optional questions: Students can attempt all, best 180 count (45+45+90)")
            
            if st.form_submit_button("🚀 Generate Admin Test Exam", type="primary"):
                generate_exam_for_student_improved('NEET', exam_name, {
                    'Physics': 50, 'Chemistry': 50, 'Biology': 100
                }, 180, include_hindi, created_by=st.session_state.user['user_id'])
    
    elif exam_type == 'CUET Domain':
        st.info("🎓 **CUET Domain:** 50/subject | Best 40 counted | +5/-1 | 200 marks/subject")
        
        with st.form("admin_cuet_domain_form"):
            exam_name = st.text_input("Exam Name", value=f"Admin Test CUET {datetime.now().strftime('%d-%m-%Y %H:%M')}")
            
            subject_combo = st.selectbox("Subject Combination", [
                "PCM (Physics, Chemistry, Mathematics)",
                "PCB (Physics, Chemistry, Biology)",
                "PCMB (Physics, Chemistry, Mathematics, Biology)"
            ], key="admin_cuet_combo")
            
            include_hindi = st.checkbox("Include Hindi", value=True, key="admin_cuet_hindi")
            
            if "PCM" in subject_combo and "PCMB" not in subject_combo:
                subjects = {'Physics': 50, 'Chemistry': 50, 'Mathematics': 50}
                duration = 180
            elif "PCB" in subject_combo and "PCMB" not in subject_combo:
                subjects = {'Physics': 50, 'Chemistry': 50, 'Biology': 50}
                duration = 180
            else:  # PCMB
                subjects = {'Physics': 50, 'Chemistry': 50, 'Mathematics': 50, 'Biology': 50}
                duration = 240
            
            st.success(f"✅ {len(subjects)} subjects × 50 questions each")
            st.info("✨ Optional questions: Students can attempt all, best 40/subject count")
            
            if st.form_submit_button("🚀 Generate Admin Test Exam", type="primary"):
                generate_exam_for_student_improved('CUET', exam_name, subjects, duration, include_hindi, created_by=st.session_state.user['user_id'])
    
    else:  # CUET General Test
        st.info("📘 **CUET GT:** 60 questions | Best 50 counted | +5/-1 | 250 marks")
        
        with st.form("admin_cuet_gt_form"):
            exam_name = st.text_input("Exam Name", value=f"Admin Test CUET GT {datetime.now().strftime('%d-%m-%Y %H:%M')}")
            include_hindi = st.checkbox("Include Hindi", value=True, key="admin_cuet_gt_hindi")
            
            st.success("✅ 15 GK + 15 CA + 15 LR + 15 QA = 60 questions")
            st.info("✨ Optional questions: Students can attempt all, best 50 count")
            
            if st.form_submit_button("🚀 Generate Admin Test Exam", type="primary"):
                generate_exam_for_student_improved('CUET_GT', exam_name, {
                    'General Knowledge': 15,
                    'Current Affairs': 15,
                    'Logical Reasoning': 15,
                    'Quantitative Aptitude': 15
                }, 60, include_hindi, created_by=st.session_state.user['user_id'])

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    if not st.session_state.logged_in:
        show_login_register()
    else:
        user = st.session_state.user
        
        if user['is_admin']:
            show_admin_dashboard()
        else:
            if st.session_state.exam_started:
                show_exam_interface()
            else:
                show_student_dashboard()

if __name__ == "__main__":
    main()
