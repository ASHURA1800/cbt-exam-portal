"""
bank_exam_app.py  v3 — MAJOR UPDATE
=====================================================
✅ FIX: No more flickering — JS-powered timer (no page reruns for clock)
✅ FIX: Language selector visible INSIDE exam for users
✅ FIX: Beautiful question palette with subject sections + color legend
✅ FIX: Exam on separate page (dashboard → preview → exam)
✅ NEW: All 9 languages available for users during exam
"""

import streamlit as st
import streamlit.components.v1 as components
import json, time, random, threading
from datetime import datetime
from typing import Dict, List, Optional

from question_bank_db import (
    init_bank, get_bank_stats, get_subject_count,
    get_questions_for_exam, mark_questions_seen, get_user_seen_count,
    add_to_recycle_pool, get_recycled_questions, get_recycle_stats,
    get_questions_smart, _bank_conn, _bank_lock,
)
from translation_engine_v2 import (
    translate_all_questions, get_question_in_lang,
    get_all_translation_stats, get_untranslated_count, get_translated_count,
    translate_batch, SUPPORTED_LANGS,
)

try:
    import db as auth_db
    AUTH_AVAILABLE = True
    auth_db.init_database()
    try: auth_db.migrate_database()
    except: pass
except: AUTH_AVAILABLE = False

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════

EXAM_CONFIGS = {
    "NEET": {
        "label":"NEET","full_label":"National Eligibility cum Entrance Test",
        "subjects":["Physics","Chemistry","Biology"],
        "q_per_subject":{"Physics":45,"Chemistry":45,"Biology":90},
        "total_q":180,"duration_mins":180,"marks_correct":4,"marks_wrong":-1,"icon":"🔬",
        "color":"#EF4444","desc":"Medical entrance — Physics, Chemistry & Biology",
    },
    "JEE": {
        "label":"JEE","full_label":"Joint Entrance Examination",
        "subjects":["Physics","Chemistry","Mathematics"],
        "q_per_subject":{"Physics":30,"Chemistry":30,"Mathematics":30},
        "total_q":90,"duration_mins":180,"marks_correct":4,"marks_wrong":-1,"icon":"⚙️",
        "color":"#3B82F6","desc":"Engineering entrance — Physics, Chemistry & Maths",
    },
    "CUET_DOMAIN": {
        "label":"CUET Domain","full_label":"CUET Domain Subjects",
        "subjects":["Physics","Chemistry","Mathematics"],
        "q_per_subject":{"Physics":40,"Chemistry":40,"Mathematics":40},
        "total_q":120,"duration_mins":120,"marks_correct":5,"marks_wrong":-1,"icon":"📐",
        "color":"#8B5CF6","desc":"University entrance — Domain subjects",
    },
    "CUET_GT": {
        "label":"CUET General","full_label":"CUET General Test",
        "subjects":["CUET_GK","CUET_English","CUET_Reasoning","CUET_Quantitative"],
        "q_per_subject":{"CUET_GK":15,"CUET_English":15,"CUET_Reasoning":10,"CUET_Quantitative":10},
        "total_q":50,"duration_mins":60,"marks_correct":5,"marks_wrong":-1,"icon":"📝",
        "color":"#10B981","desc":"General test — GK, English, Reasoning & Aptitude",
    },
    "PHYSICS_PRACTICE": {
        "label":"Physics Practice","full_label":"Physics Only Practice",
        "subjects":["Physics"],"q_per_subject":{"Physics":30},
        "total_q":30,"duration_mins":45,"marks_correct":4,"marks_wrong":-1,"icon":"⚡",
        "color":"#F59E0B","desc":"Physics focused practice test",
    },
    "CHEM_PRACTICE": {
        "label":"Chem Practice","full_label":"Chemistry Only Practice",
        "subjects":["Chemistry"],"q_per_subject":{"Chemistry":30},
        "total_q":30,"duration_mins":45,"marks_correct":4,"marks_wrong":-1,"icon":"⚗️",
        "color":"#06B6D4","desc":"Chemistry focused practice test",
    },
    "MATH_PRACTICE": {
        "label":"Maths Practice","full_label":"Mathematics Only Practice",
        "subjects":["Mathematics"],"q_per_subject":{"Mathematics":30},
        "total_q":30,"duration_mins":45,"marks_correct":4,"marks_wrong":-1,"icon":"📊",
        "color":"#EC4899","desc":"Mathematics focused practice test",
    },
    "BIO_PRACTICE": {
        "label":"Bio Practice","full_label":"Biology Only Practice",
        "subjects":["Biology"],"q_per_subject":{"Biology":30},
        "total_q":30,"duration_mins":45,"marks_correct":4,"marks_wrong":-1,"icon":"🧬",
        "color":"#84CC16","desc":"Biology focused practice test",
    },
}

LANG_OPTIONS = {
    "en":"🇬🇧 English","hi":"🇮🇳 हिंदी","bn":"🇧🇩 বাংলা","ta":"🇮🇳 தமிழ்",
    "te":"🇮🇳 తెలుగు","gu":"🇮🇳 ગુજરાતી","mr":"🇮🇳 मराठी","kn":"🇮🇳 ಕನ್ನಡ","or":"🇮🇳 ଓଡ଼ିଆ",
}
LANG_FULL = {
    "en":"English","hi":"हिंदी (Hindi)","bn":"বাংলা (Bengali)","ta":"தமிழ் (Tamil)",
    "te":"తెలుగు (Telugu)","gu":"ગુજરાતી (Gujarati)","mr":"मराठी (Marathi)",
    "kn":"ಕನ್ನಡ (Kannada)","or":"ଓଡ଼ିଆ (Odia)",
}
SUBJECT_LABELS = {
    "Physics":"Physics","Chemistry":"Chemistry","Biology":"Biology",
    "Mathematics":"Mathematics","CUET_GK":"General Knowledge",
    "CUET_English":"English","CUET_Reasoning":"Logical Reasoning",
    "CUET_Quantitative":"Quantitative Aptitude",
}
SUBJECT_COLORS = {
    "Physics":"#3B82F6","Chemistry":"#10B981","Biology":"#84CC16",
    "Mathematics":"#8B5CF6","CUET_GK":"#F59E0B","CUET_English":"#EF4444",
    "CUET_Reasoning":"#06B6D4","CUET_Quantitative":"#EC4899",
}
ALL_SUBJECTS = list(SUBJECT_LABELS.keys())

# ══════════════════════════════════════════════════════════════════════════════
# PAGE CONFIG & GLOBAL CSS
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="CBT Exam Portal", page_icon="🎓",
    layout="wide", initial_sidebar_state="collapsed"
)

GLOBAL_CSS = """
<style>
[data-testid="stAppViewContainer"]{background:#0F1117}
[data-testid="stSidebar"]{background:#161B22;border-right:1px solid #30363D}
body,p,span,div,label{color:#E6EDF3 !important}
.stButton button{border-radius:10px !important;font-weight:600 !important;transition:all .2s !important}
.stButton button:hover{transform:translateY(-1px) !important}
.stRadio label{color:#E6EDF3 !important}
.stSelectbox label,.stNumberInput label,.stTextInput label{color:#8B949E !important;font-size:.85rem !important}
[data-testid="stSelectbox"] > div > div{background:#21262D;border:1px solid #30363D;color:#E6EDF3;border-radius:8px}
[data-testid="stTextInput"] input{background:#21262D;border:1px solid #30363D;color:#E6EDF3;border-radius:8px}

.hero{background:linear-gradient(135deg,#0D1117,#161B22,#1C2128);border:1px solid #30363D;color:#E6EDF3;padding:2.5rem 2rem;border-radius:20px;text-align:center;margin-bottom:1.5rem;box-shadow:0 8px 32px rgba(0,0,0,.4)}
.hero h1{font-size:2.2rem;font-weight:900;margin:0 0 .5rem;background:linear-gradient(90deg,#58A6FF,#A78BFA,#F78166);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.hero p{color:#8B949E !important;margin:0;font-size:1rem}
.pill{display:inline-block;background:#21262D;border:1px solid #30363D;padding:.2rem .75rem;border-radius:99px;font-size:.8rem;margin:.4rem .2rem;color:#58A6FF !important}

.stat-card{background:#161B22;border:1px solid #30363D;border-radius:14px;padding:1.25rem;text-align:center;margin-bottom:.5rem}
.stat-num{font-size:1.9rem;font-weight:900}
.stat-label{font-size:.72rem;color:#8B949E !important;text-transform:uppercase;letter-spacing:.06em;margin-top:.2rem}

.exam-card{background:#161B22;border:2px solid #30363D;border-radius:16px;padding:1.4rem 1.5rem;margin-bottom:.75rem;transition:all .2s;cursor:pointer;position:relative;overflow:hidden}
.exam-card:hover{border-color:#58A6FF;box-shadow:0 4px 24px rgba(88,166,255,.15);transform:translateY(-2px)}
.exam-card h3{font-size:1.1rem;font-weight:700;margin:0 0 .4rem;color:#E6EDF3 !important}
.exam-card .meta{color:#8B949E !important;font-size:.82rem;margin:.2rem 0}

.qcard{background:#161B22;border:1px solid #30363D;border-radius:16px;padding:2rem;margin-bottom:1rem;box-shadow:0 4px 16px rgba(0,0,0,.3)}
.qnum{font-size:.82rem;color:#8B949E !important;font-weight:700;letter-spacing:.06em;text-transform:uppercase;margin-bottom:.85rem}
.qtext{font-size:1.3rem;color:#E6EDF3 !important;line-height:1.95;font-weight:500}

.result-hero{background:linear-gradient(135deg,#0D1117,#161B22);border:1px solid #30363D;color:#E6EDF3;border-radius:20px;padding:3rem 2rem;text-align:center;margin-bottom:1.5rem}
.score-big{font-size:4rem;font-weight:900;line-height:1.1}

.pbar-wrap{background:#21262D;border-radius:99px;height:7px;margin:.3rem 0}
.pbar-fill{border-radius:99px;height:7px;transition:width .6s cubic-bezier(.4,0,.2,1)}

.recycle-box{background:#1C1209;border:1px solid #7C4A00;border-radius:8px;padding:.6rem 1rem;font-size:.82rem;color:#F59E0B !important;margin-bottom:.5rem}
.warn-box{background:#1B0E0E;border:1px solid #7C1A1A;border-radius:8px;padding:.5rem 1rem;font-size:.82rem;color:#FCA5A5 !important;margin-bottom:.5rem}

.pal-legend{display:flex;flex-wrap:wrap;gap:.35rem;margin:.3rem 0 .8rem}
.pal-dot{display:flex;align-items:center;gap:.25rem;font-size:.68rem;color:#8B949E !important}
.pal-sq{width:12px;height:12px;border-radius:3px;flex-shrink:0}

[data-testid="stRadio"] > div{gap:.5rem !important}
[data-testid="stRadio"] label{background:#21262D;border:1px solid #30363D;border-radius:10px;padding:.85rem 1.2rem;width:100%;transition:all .15s;color:#E6EDF3 !important;font-size:1.05rem !important;line-height:1.6}
[data-testid="stRadio"] label:hover{border-color:#58A6FF;background:#1C2128}
[data-testid="stRadio"] label p{font-size:1.05rem !important}
[data-testid="stRadio"] div[data-testid="stMarkdownContainer"] p{font-size:1.05rem !important;line-height:1.6}
</style>
"""
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

def ss(k, d=None): return st.session_state.get(k, d)
def ss_set(k, v): st.session_state[k] = v

@st.cache_resource
def _init():
    init_bank(); return True
_init()

# ══════════════════════════════════════════════════════════════════════════════
# LOGIN
# ══════════════════════════════════════════════════════════════════════════════

def show_login():
    st.markdown("""<div class="hero">
        <h1>🎓 CBT Exam Portal</h1>
        <p>India's smartest exam practice platform</p>
        <div style="margin-top:.75rem">
        <span class="pill">📚 58,000+ Questions</span>
        <span class="pill">🔬 8 Subjects</span>
        <span class="pill">🌐 9 Languages</span>
        <span class="pill">♻️ Smart Recycle</span>
        <span class="pill">⚡ No Repeats Ever</span>
        </div>
    </div>""", unsafe_allow_html=True)
    _, col, _ = st.columns([1.5, 2, 1.5])
    with col:
        t_login, t_reg = st.tabs(["🔑 Login", "📝 Register"])
        with t_login:
            un = st.text_input("Username", placeholder="Enter your username")
            dob = st.text_input("Date of Birth", placeholder="DD/MM/YYYY")
            if st.button("Login →", type="primary", use_container_width=True):
                if AUTH_AVAILABLE:
                    u = auth_db.authenticate_user(un, dob)
                    if u: ss_set("user", u); ss_set("user_id", u.get("user_id", 1)); st.rerun()
                    else: st.error("❌ Invalid credentials")
                else:
                    if un.strip():
                        demo = {"user_id": abs(hash(un)) % 99999 + 1, "full_name": un.title(),
                                "username": un, "is_admin": 1 if un.lower() == "admin" else 0,
                                "preferred_lang": "en"}
                        ss_set("user", demo); ss_set("user_id", demo["user_id"]); st.rerun()
                    else: st.error("Enter a username")
        with t_reg:
            if AUTH_AVAILABLE:
                fn = st.text_input("Full Name", key="rfn")
                nu = st.text_input("Username", key="rnu")
                nd = st.text_input("DOB (DD/MM/YYYY)", key="rnd")
                if st.button("Register →", type="primary", use_container_width=True):
                    ok, msg = auth_db.create_user(nu, "", fn, nd)
                    st.success("✅ Registered!") if ok else st.error(msg)
            else:
                st.info("Demo mode — login with any username")

# ══════════════════════════════════════════════════════════════════════════════
# DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════

def show_dashboard():
    user = ss("user", {}); name = user.get("full_name", "Student"); uid = ss("user_id", 1)
    stats = get_bank_stats(); total_q = stats.get("total", 0)
    all_seen = sum(get_user_seen_count(uid, s) for s in ALL_SUBJECTS)
    recycle_stats = get_recycle_stats(uid); recycle_avail = recycle_stats.get("available", 0)
    fresh = max(0, total_q - all_seen)

    c1, c2, c3, c4 = st.columns([5, 1.2, 1.2, 1.2])
    with c1: st.markdown(f"<h2 style='margin:0;font-size:1.4rem;color:#E6EDF3'>Welcome, <span style='color:#58A6FF'>{name}</span> 👋</h2>", unsafe_allow_html=True)
    with c2:
        if user.get("is_admin") and st.button("🛠 Admin", use_container_width=True):
            ss_set("view", "admin"); st.rerun()
    with c3:
        st.selectbox("🌐", list(LANG_OPTIONS.keys()), format_func=lambda x: LANG_OPTIONS[x],
                     key="selected_lang", label_visibility="collapsed")
    with c4:
        if st.button("🚪 Logout", use_container_width=True): st.session_state.clear(); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    for col, num, label, color in [
        (c1, f"{total_q:,}", "Total Questions", "#58A6FF"),
        (c2, f"{all_seen:,}", "You've Attempted", "#A78BFA"),
        (c3, f"{fresh:,}", "Fresh Available", "#34D399"),
        (c4, f"{recycle_avail:,}", "♻️ Recyclable", "#FBBF24"),
    ]:
        with col: st.markdown(f'<div class="stat-card"><div class="stat-num" style="color:{color}">{num}</div><div class="stat-label">{label}</div></div>', unsafe_allow_html=True)

    st.markdown("<br><h3 style='color:#E6EDF3;margin-bottom:1rem'>📋 Choose Your Exam</h3>", unsafe_allow_html=True)

    items = list(EXAM_CONFIGS.items())
    for row in range(0, len(items), 3):
        cols = st.columns(3)
        for col, (ek, cfg) in zip(cols, items[row:row+3]):
            subj_str = " · ".join(SUBJECT_LABELS.get(s, s) for s in cfg["subjects"])
            color = cfg.get("color", "#58A6FF")
            with col:
                st.markdown(f"""<div class="exam-card" style="border-left:4px solid {color};padding-left:1.2rem">
                    <h3>{cfg['icon']} {cfg['label']}</h3>
                    <div class="meta">📚 {subj_str}</div>
                    <div class="meta">❓ {cfg['total_q']} Q &nbsp;·&nbsp; ⏱ {cfg['duration_mins']} min</div>
                    <div class="meta">✅ +{cfg['marks_correct']} &nbsp;·&nbsp; ❌ {cfg['marks_wrong']}</div>
                    <div class="meta" style="color:#8B949E;font-style:italic;margin-top:.2rem">{cfg.get('desc','')}</div>
                </div>""", unsafe_allow_html=True)
                if st.button(f"Start {cfg['label']} →", key=f"btn_{ek}", use_container_width=True, type="primary"):
                    ss_set("preview_exam_type", ek)
                    ss_set("preview_lang", ss("selected_lang", "en"))
                    ss_set("view", "preview"); st.rerun()

    with st.sidebar:
        st.markdown(f"### 👤 {name}\n*Your progress:*\n---")
        for subj in ALL_SUBJECTS:
            seen = get_user_seen_count(uid, subj); total_s = get_subject_count(subj)
            pct = min(100, int(seen / total_s * 100)) if total_s > 0 else 0
            sc = SUBJECT_COLORS.get(subj, "#58A6FF")
            st.markdown(f"<div style='display:flex;justify-content:space-between;margin-bottom:.1rem'><span style='font-size:.78rem;color:#8B949E'>{SUBJECT_LABELS.get(subj,subj)}</span><span style='font-size:.78rem;color:{sc};font-weight:700'>{pct}%</span></div>", unsafe_allow_html=True)
            st.markdown(f'<div class="pbar-wrap"><div class="pbar-fill" style="width:{pct}%;background:{sc}"></div></div><div style="font-size:.68rem;color:#8B949E;margin-bottom:.4rem">{seen:,}/{total_s:,}</div>', unsafe_allow_html=True)
        st.markdown("---")
        st.markdown(f"♻️ **{recycle_avail}** in recycle pool")
        if st.button("♻️ Recycle My Questions", use_container_width=True, help="Add your seen questions back to pool"):
            ss_set("view","recycle"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# EXAM PREVIEW (Page before starting)
# ══════════════════════════════════════════════════════════════════════════════

def show_exam_preview():
    ek = ss("preview_exam_type", "NEET"); cfg = EXAM_CONFIGS.get(ek, {}); uid = ss("user_id", 1)
    color = cfg.get("color", "#58A6FF")

    c_back, _ = st.columns([1, 8])
    with c_back:
        if st.button("← Back", use_container_width=True): ss_set("view", "dashboard"); st.rerun()

    st.markdown(f"""<div style='background:#161B22;border:2px solid {color}40;border-left:5px solid {color};
    border-radius:16px;padding:2rem;margin-bottom:1.5rem'>
        <h2 style='color:#E6EDF3;margin:0 0 .3rem'>{cfg.get('icon','')} {cfg.get('full_label','')}</h2>
        <p style='color:#8B949E;margin:0'>{cfg.get('desc','')}</p></div>""", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 📋 Exam Details")
        for key, val in [("Total Questions", cfg.get("total_q",0)),
                         ("Duration", f"{cfg.get('duration_mins',0)} minutes"),
                         ("Correct", f"+{cfg.get('marks_correct',4)} marks"),
                         ("Wrong", f"{cfg.get('marks_wrong',-1)} marks")]:
            st.markdown(f"<div style='display:flex;justify-content:space-between;padding:.55rem 0;border-bottom:1px solid #21262D'><span style='color:#8B949E'>{key}</span><span style='color:#E6EDF3;font-weight:700'>{val}</span></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("### 📚 Subject Breakdown")
        for subj in cfg.get("subjects", []):
            n = cfg["q_per_subject"].get(subj, 0)
            sc = SUBJECT_COLORS.get(subj, "#58A6FF")
            seen = get_user_seen_count(uid, subj); total_s = get_subject_count(subj)
            fresh = max(0, total_s - seen)
            st.markdown(f"""<div style='background:#21262D;border-left:3px solid {sc};border-radius:8px;padding:.7rem 1rem;margin-bottom:.4rem'>
                <div style='display:flex;justify-content:space-between'><span style='color:#E6EDF3;font-weight:600'>{SUBJECT_LABELS.get(subj,subj)}</span><span style='color:{sc};font-weight:700'>{n} Q</span></div>
                <div style='color:#8B949E;font-size:.75rem;margin-top:.2rem'>{fresh:,} fresh available (seen {seen:,})</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>### 🌐 Select Language")
    prev_lang = ss("preview_lang", "en")
    lang_items = list(LANG_OPTIONS.items())
    rows = [lang_items[i:i+5] for i in range(0, len(lang_items), 5)]
    for row in rows:
        rcols = st.columns(len(row))
        for col, (lc, label) in zip(rcols, row):
            is_sel = (lc == prev_lang)
            with col:
                if st.button(label, key=f"ls_{lc}", type="primary" if is_sel else "secondary", use_container_width=True):
                    ss_set("preview_lang", lc); st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📜 Exam Instructions"):
        st.markdown("""
1. **JS Timer** — runs client-side (no screen flicker!)
2. **Save & Next** — saves answer, goes to next question
3. **Mark Review** — flags question with 🟨 for review later
4. **Palette Colors:** 🟦 Current · 🟩 Answered · 🟨 Review · 🔷 Visited · ⬜ Unseen
5. **Change language** anytime during exam using the dropdown in the top bar
6. **Delete Exam** — recycles questions back to your pool
7. **Submit** when done or wait for timer
        """)

    c_start, c_cancel = st.columns(2)
    with c_start:
        lang_final = ss("preview_lang", "en")
        if st.button(f"🚀 Begin Exam in {LANG_FULL.get(lang_final,'English')}", type="primary", use_container_width=True):
            start_exam(ek, lang_final)
    with c_cancel:
        if st.button("← Cancel", use_container_width=True): ss_set("view", "dashboard"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# EXAM START
# ══════════════════════════════════════════════════════════════════════════════

def start_exam(exam_type: str, language: str):
    cfg = EXAM_CONFIGS[exam_type]; uid = ss("user_id", 1)
    with st.spinner("🎲 Preparing your unique question set..."):
        all_questions = []; subjects_recycled = []
        global_seen_ids = set()   # prevent any cross-subject duplicate qb_ids
        global_seen_texts = set() # prevent any cross-subject duplicate question texts

        for subject in cfg["subjects"]:
            n_q = cfg["q_per_subject"][subject]
            qs = get_questions_smart(
                subject, n_q, uid,
                {"medium": 0.30, "hard": 0.45, "very_hard": 0.25},
                True,
            )
            # Strict dedup: filter out any qb_id or question_en already used
            unique_qs = []
            for q in qs:
                qid = q.get("qb_id")
                txt = (q.get("question_en") or "").strip().lower()
                if qid in global_seen_ids:
                    continue
                if txt and txt in global_seen_texts:
                    continue
                unique_qs.append(q)
                global_seen_ids.add(qid)
                if txt:
                    global_seen_texts.add(txt)

            rec = sum(1 for q in unique_qs if q.get("_from_recycle"))
            if rec: subjects_recycled.append(f"{SUBJECT_LABELS.get(subject,subject)}: {rec} recycled")
            for q in unique_qs: q["_subject"] = subject
            all_questions.extend(unique_qs)

        # Final shuffle for extra randomness
        random.shuffle(all_questions)

    if len(all_questions) < 5:
        st.error("❌ Not enough questions. Run: `python seed_to_40000.py`"); return

    subj_index = {}
    for i, q in enumerate(all_questions):
        s = q.get("_subject", ""); subj_index.setdefault(s, []).append(i)

    ss_set("exam_active", True); ss_set("exam_type", exam_type); ss_set("exam_cfg", cfg)
    ss_set("exam_lang", language); ss_set("exam_questions", all_questions)
    ss_set("exam_subj_index", subj_index); ss_set("exam_responses", {})
    ss_set("exam_review", set()); ss_set("exam_visited", set())
    ss_set("exam_current_idx", 0); ss_set("exam_start_time", time.time())
    ss_set("exam_duration_secs", cfg["duration_mins"] * 60)
    ss_set("exam_submitted", False); ss_set("exam_deleted", False)
    ss_set("confirm_delete", False); ss_set("view", "exam")
    if subjects_recycled: ss_set("exam_recycled_note", subjects_recycled)
    st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# EXAM UI
# ══════════════════════════════════════════════════════════════════════════════

def show_exam():
    if ss("exam_submitted"): show_results(); return
    if ss("exam_deleted"): show_exam_deleted(); return

    questions = ss("exam_questions", []); responses = ss("exam_responses", {})
    review = ss("exam_review", set()); visited = ss("exam_visited", set())
    subj_index = ss("exam_subj_index", {}); idx = max(0, min(ss("exam_current_idx", 0), len(questions)-1))
    lang = ss("exam_lang", "en"); cfg = ss("exam_cfg", {}); uid = ss("user_id", 1)
    total = len(questions); q_data = questions[idx]; qb_id = q_data["qb_id"]
    visited.add(idx); ss_set("exam_visited", visited)

    elapsed_secs = int(time.time() - ss("exam_start_time", time.time()))
    remaining_secs = max(0, ss("exam_duration_secs", 10800) - elapsed_secs)
    if remaining_secs <= 0: submit_exam(); return
    h, rem = divmod(remaining_secs, 3600); m, s = divmod(rem, 60)
    init_time_str = f"{h:02d}:{m:02d}:{s:02d}"

    # ══ SIDEBAR — Beautiful Palette ══
    with st.sidebar:
        answered_idxs = {i for i, q in enumerate(questions) if q["qb_id"] in responses}
        st.markdown(f"<div style='text-align:center;padding:.4rem 0 .6rem'><div style='font-size:.65rem;color:#8B949E;text-transform:uppercase;letter-spacing:.07em;margin-bottom:.2rem'>Question Palette</div><div style='font-size:1.1rem;font-weight:700;color:#E6EDF3'>{idx+1} <span style='color:#8B949E;font-weight:400'>/ {total}</span></div></div>", unsafe_allow_html=True)
        st.markdown("""<div class="pal-legend">
            <div class="pal-dot"><div class="pal-sq" style="background:#3B82F6"></div><span>Current</span></div>
            <div class="pal-dot"><div class="pal-sq" style="background:#22C55E"></div><span>Done</span></div>
            <div class="pal-dot"><div class="pal-sq" style="background:#EAB308"></div><span>Review</span></div>
            <div class="pal-dot"><div class="pal-sq" style="background:#64748B"></div><span>Visited</span></div>
            <div class="pal-dot"><div class="pal-sq" style="background:#21262D;border:1px solid #30363D"></div><span>Unseen</span></div>
        </div>""", unsafe_allow_html=True)
        st.markdown("---")

        for subj, subj_idxs in subj_index.items():
            sc = SUBJECT_COLORS.get(subj, "#58A6FF"); label = SUBJECT_LABELS.get(subj, subj)
            done_in_subj = sum(1 for i in subj_idxs if questions[i]["qb_id"] in responses)
            st.markdown(f"<div style='background:{sc}22;border-left:3px solid {sc};border-radius:6px;padding:.3rem .6rem;margin-bottom:.4rem;display:flex;justify-content:space-between;align-items:center'><span style='font-size:.7rem;font-weight:700;color:{sc}'>{label}</span><span style='font-size:.68rem;color:#8B949E'>{done_in_subj}/{len(subj_idxs)}</span></div>", unsafe_allow_html=True)

            COLS = 6
            for row_start in range(0, len(subj_idxs), COLS):
                row_qs = subj_idxs[row_start:row_start+COLS]
                ccols = st.columns(COLS)
                for col_i, qi in enumerate(row_qs):
                    with ccols[col_i]:
                        qid_i = questions[qi]["qb_id"]
                        is_current = (qi == idx)
                        is_answered = qid_i in responses; is_review = qi in review; is_visited = qi in visited
                        if is_current: bg, fc = "#3B82F6","white"
                        elif is_answered and is_review: bg, fc = "#D97706","white"
                        elif is_answered: bg, fc = "#22C55E","white"
                        elif is_review: bg, fc = "#EAB308","#0F1117"
                        elif is_visited: bg, fc = "#64748B","white"
                        else: bg, fc = "#21262D","#8B949E"
                        if st.button(str(qi+1), key=f"pal_{qi}", help=f"Q{qi+1}",
                                     use_container_width=True):
                            ss_set("exam_current_idx", qi); st.rerun()
                        # Color via inline JS (works with Streamlit's dynamic DOM)
                        st.markdown(f"""<script>
                        (function(){{var btns=document.querySelectorAll('button');
                        btns.forEach(function(b){{if(b.innerText.trim()=='{qi+1}' && b.closest('[data-testid="stSidebar"]')){{
                        b.style.background='{bg}';b.style.color='{fc}';b.style.borderColor='{bg}';}}}})}})();
                        </script>""", unsafe_allow_html=True)
            st.markdown("")

        st.markdown("---")
        answered_n = len(answered_idxs)
        st.markdown(f"""<div style='font-size:.78rem'>
            <div style='display:flex;justify-content:space-between;padding:.2rem 0'><span style='color:#22C55E'>✅ Answered</span><span style='color:#E6EDF3;font-weight:700'>{answered_n}</span></div>
            <div style='display:flex;justify-content:space-between;padding:.2rem 0'><span style='color:#EAB308'>🔖 Review</span><span style='color:#E6EDF3;font-weight:700'>{len(review)}</span></div>
            <div style='display:flex;justify-content:space-between;padding:.2rem 0'><span style='color:#64748B'>⬜ Not Attempted</span><span style='color:#E6EDF3;font-weight:700'>{total-answered_n}</span></div>
        </div>""", unsafe_allow_html=True)

    # ══ TOP BAR ══
    c_timer, c_lang, c_del, c_sub = st.columns([2.5, 2, 1.5, 1])

    with c_timer:
        # JS timer — zero flicker!
        components.html(f"""
        <div style="background:linear-gradient(135deg,#0D1117,#1C2128);border:1px solid #30363D;
        border-radius:14px;padding:.7rem 1.25rem;text-align:center">
            <div style="font-size:.6rem;color:#8B949E;font-weight:700;letter-spacing:.1em;text-transform:uppercase;margin-bottom:.2rem">⏱ Time Remaining</div>
            <div id="cbt-timer" style="font-size:1.9rem;font-weight:900;font-family:'Courier New',monospace;color:#58A6FF;letter-spacing:3px">{init_time_str}</div>
        </div>
        <script>
        (function(){{
            var secs={remaining_secs};var el=document.getElementById('cbt-timer');
            function fmt(n){{return n<10?'0'+n:String(n);}}
            function tick(){{
                if(secs<=0){{el.textContent='00:00:00';el.style.color='#EF4444';return;}}
                secs--;
                var h=Math.floor(secs/3600),m=Math.floor((secs%3600)/60),s=secs%60;
                el.textContent=fmt(h)+':'+fmt(m)+':'+fmt(s);
                if(secs<300){{el.style.color='#EF4444';el.style.animation='cbt-pulse .8s infinite';}}
                else if(secs<600){{el.style.color='#F59E0B';}}
                else{{el.style.color='#58A6FF';}}
            }}
            setInterval(tick,1000);
        }})();
        </script>
        <style>@keyframes cbt-pulse{{0%,100%{{opacity:1}}50%{{opacity:.3}}}}</style>
        """, height=80)

    with c_lang:
        # User-facing language switcher IN exam
        new_lang = st.selectbox(
            "Language", list(LANG_OPTIONS.keys()),
            index=list(LANG_OPTIONS.keys()).index(lang),
            format_func=lambda x: LANG_OPTIONS[x],
            key="exam_lang_select", label_visibility="visible"
        )
        if new_lang != lang: ss_set("exam_lang", new_lang); st.rerun()

    with c_del:
        if st.button("🗑 Delete Exam", use_container_width=True):
            if ss("confirm_delete"): delete_exam()
            else:
                ss_set("confirm_delete", True)
                st.warning("Click **Delete Exam** again to confirm")

    with c_sub:
        if st.button("🚩 Submit", type="primary", use_container_width=True):
            ss_set("confirm_delete", False); submit_exam()

    recycled_note = ss("exam_recycled_note", [])
    if recycled_note:
        st.markdown(f'<div class="recycle-box">♻️ Recycled questions: {", ".join(recycled_note)}</div>', unsafe_allow_html=True)

    # ══ QUESTION ══
    q_text = get_question_in_lang(q_data, lang)
    subj = q_data.get("_subject", ""); subj_label = SUBJECT_LABELS.get(subj, subj)
    subj_color = SUBJECT_COLORS.get(subj, "#58A6FF")
    diff = q_data.get("difficulty", "medium")
    diff_colors = {"medium":("#DBEAFE","#1E40AF"),"hard":("#FEF3C7","#92400E"),"very_hard":("#FEE2E2","#991B1B")}
    diff_bg, diff_fc = diff_colors.get(diff, diff_colors["medium"])
    diff_label = {"medium":"Medium","hard":"Hard","very_hard":"Very Hard"}.get(diff, diff)

    if q_data.get("_from_recycle"):
        st.markdown('<div class="recycle-box">♻️ From your recycled pool (previously deleted exam)</div>', unsafe_allow_html=True)
    if not q_text.get("lang_available", True) and lang != "en" and not q_text.get("question", ""):
        st.markdown(f'<div class="warn-box">⚠️ Not yet translated to {LANG_OPTIONS.get(lang, lang)} — showing English</div>', unsafe_allow_html=True)

    st.markdown(f"""<div class="qcard">
        <div class="qnum">
            Q{idx+1}/{total} &nbsp;·&nbsp;
            <span style='background:{subj_color}22;color:{subj_color};padding:.15rem .55rem;border-radius:5px;font-size:.72rem;font-weight:700'>{subj_label}</span>
            &nbsp;
            <span style='background:{diff_bg};color:{diff_fc};padding:.15rem .55rem;border-radius:5px;font-size:.72rem;font-weight:700'>{diff_label}</span>
        </div>
        <div class="qtext">{q_text['question']}</div>
    </div>""", unsafe_allow_html=True)

    opts = [q_text['option_a'], q_text['option_b'], q_text['option_c'], q_text['option_d']]
    cur = responses.get(qb_id)
    selected = st.radio(
        "Select your answer:", ["A","B","C","D"],
        format_func=lambda x: f"**{x}.**  {opts['ABCD'.index(x)]}",
        index=["A","B","C","D"].index(cur) if cur else None,
        key=f"radio_{qb_id}", label_visibility="collapsed"
    )

    st.markdown("<div style='height:.3rem'></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        if st.button("💾 Save & Next", type="primary", use_container_width=True):
            if selected: responses[qb_id] = selected; ss_set("exam_responses", responses)
            if idx+1 < total: ss_set("exam_current_idx", idx+1)
            st.rerun()
    with c2:
        marked = idx in review
        if st.button("🔖 "+("Unmark" if marked else "Mark Review"), use_container_width=True):
            (review.discard if marked else review.add)(idx)
            if selected: responses[qb_id] = selected; ss_set("exam_responses", responses)
            ss_set("exam_review", review); st.rerun()
    with c3:
        if st.button("⬅ Previous", use_container_width=True, disabled=(idx==0)):
            if selected: responses[qb_id] = selected; ss_set("exam_responses", responses)
            ss_set("exam_current_idx", idx-1); st.rerun()
    with c4:
        if st.button("Next ➡", use_container_width=True, disabled=(idx==total-1)):
            if selected: responses[qb_id] = selected; ss_set("exam_responses", responses)
            ss_set("exam_current_idx", idx+1); st.rerun()

    # ✅ NO time.sleep() / st.rerun() — timer is JS-based, zero flicker!

# ══════════════════════════════════════════════════════════════════════════════
# DELETE → RECYCLE
# ══════════════════════════════════════════════════════════════════════════════

def delete_exam():
    questions = ss("exam_questions",[]); uid = ss("user_id",1); recycled = {}
    for q in questions:
        qb_id = q["qb_id"]; subj = q.get("_subject", q.get("subject",""))
        add_to_recycle_pool(uid, qb_id, subj, source="deleted_exam")
        recycled[subj] = recycled.get(subj, 0) + 1
    ss_set("exam_deleted", True); ss_set("exam_recycled_summary", recycled)
    ss_set("confirm_delete", False); st.rerun()

def show_exam_deleted():
    recycled = ss("exam_recycled_summary",{}); total_r = sum(recycled.values())
    st.markdown(f"""<div class="result-hero">
        <div style="font-size:4rem">♻️</div>
        <h1 style="color:#E6EDF3">Exam Deleted — {total_r} Questions Recycled</h1>
        <p style="color:#8B949E">Questions saved to your personal recycle pool</p>
    </div>""", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.info("**What this means:**\n- NOT counted as 'seen'\n- Added to ♻️ pool\n- Auto-used when fresh questions are low\n- Labeled ♻️ when reused")
    with c2:
        st.markdown("**Recycled by Subject:**")
        for subj, count in recycled.items():
            sc = SUBJECT_COLORS.get(subj,"#58A6FF")
            st.markdown(f"<div style='background:#21262D;border-left:3px solid {sc};border-radius:6px;padding:.4rem .8rem;margin-bottom:.3rem;display:flex;justify-content:space-between'><span style='color:#E6EDF3'>{SUBJECT_LABELS.get(subj,subj)}</span><span style='color:{sc};font-weight:700'>{count} Q</span></div>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏠 Back to Dashboard", type="primary", use_container_width=True):
            for k in ["exam_active","exam_deleted","exam_submitted","exam_questions",
                      "exam_responses","exam_review","exam_visited","exam_current_idx","exam_recycled_note","confirm_delete"]:
                st.session_state.pop(k, None)
            ss_set("view","dashboard"); st.rerun()
    with c2:
        if st.button("🔄 Start New Exam", use_container_width=True):
            et = ss("exam_type","NEET"); el = ss("exam_lang","en")
            for k in ["exam_active","exam_deleted","exam_submitted","exam_questions",
                      "exam_responses","exam_review","exam_visited","exam_current_idx"]:
                st.session_state.pop(k, None)
            start_exam(et, el)

# ══════════════════════════════════════════════════════════════════════════════
# SUBMIT & RESULTS
# ══════════════════════════════════════════════════════════════════════════════

def submit_exam():
    questions = ss("exam_questions",[]); responses = ss("exam_responses",{})
    cfg = ss("exam_cfg",{}); uid = ss("user_id",1)
    mc = cfg.get("marks_correct",4); mw = cfg.get("marks_wrong",-1)
    correct = wrong = unattempted = 0; total_score = 0.0; by_subject = {}; detailed = []
    for q in questions:
        qb_id = q["qb_id"]; ca = q["correct_answer"]; ga = responses.get(qb_id)
        subj = q.get("_subject", q.get("subject",""))
        if subj not in by_subject:
            by_subject[subj] = {"correct":0,"wrong":0,"unattempted":0,"score":0.0,"total":0}
        by_subject[subj]["total"] += 1
        if ga is None: unattempted += 1; by_subject[subj]["unattempted"] += 1; score = 0
        elif ga == ca: correct += 1; by_subject[subj]["correct"] += 1; score = mc
        else: wrong += 1; by_subject[subj]["wrong"] += 1; score = mw
        total_score += score; by_subject[subj]["score"] += score
        detailed.append({"qb_id":qb_id,"question":q.get("question_en","")[:100],
                          "correct_answer":ca,"given_answer":ga,"subject":subj,
                          "difficulty":q.get("difficulty",""),"score":score})
    for subj in cfg.get("subjects",[]):
        q_ids = [q["qb_id"] for q in questions if q.get("_subject")==subj or q.get("subject")==subj]
        mark_questions_seen(uid, q_ids, subj)
    conn = _bank_conn()
    for q in questions:
        if q.get("_from_recycle"):
            with _bank_lock:
                conn.execute("UPDATE exam_recycle_pool SET is_available=0 WHERE user_id=? AND qb_id=? AND subject=?",
                             (str(uid),q["qb_id"],q.get("_subject",q.get("subject",""))))
    conn.commit()
    ss_set("exam_submitted",True); ss_set("exam_score",total_score)
    ss_set("exam_correct",correct); ss_set("exam_wrong",wrong)
    ss_set("exam_unattempted",unattempted); ss_set("exam_by_subject",by_subject)
    ss_set("exam_detailed",detailed); st.rerun()

def show_results():
    score=ss("exam_score",0); correct=ss("exam_correct",0); wrong=ss("exam_wrong",0)
    unattempted=ss("exam_unattempted",0); by_subject=ss("exam_by_subject",{})
    detailed=ss("exam_detailed",[]); cfg=ss("exam_cfg",{})
    total_q=cfg.get("total_q",len(detailed)); max_score=total_q*cfg.get("marks_correct",4)
    pct=round(score/max_score*100,1) if max_score>0 else 0
    grade="🏆 Excellent!" if pct>=75 else("👍 Good Job!" if pct>=55 else("📈 Keep Going!" if pct>=40 else "📚 More Practice"))
    sc="#34D399" if pct>=60 else("#FBBF24" if pct>=40 else "#F87171")
    st.markdown(f"""<div class="result-hero">
        <h1 style="color:#E6EDF3">Exam Complete! 🎉</h1>
        <div class="score-big" style="color:{sc}">{score:.0f}</div>
        <div style="color:#8B949E;margin:.3rem 0">out of {max_score:.0f} &nbsp;·&nbsp; {pct}%</div>
        <h2 style="color:#E6EDF3">{grade}</h2></div>""", unsafe_allow_html=True)
    c1,c2,c3,c4=st.columns(4)
    acc=round(correct/(correct+wrong)*100,1) if (correct+wrong)>0 else 0
    for col,icon,val,label in[(c1,"✅",correct,"Correct"),(c2,"❌",wrong,"Wrong"),(c3,"⬜",unattempted,"Skipped"),(c4,"🎯",f"{acc}%","Accuracy")]:
        with col: st.metric(f"{icon} {label}",val)
    st.markdown("<br>### 📊 Subject Analysis")
    for subj,data in by_subject.items():
        label=SUBJECT_LABELS.get(subj,subj); tot=data.get("total",1)
        sp=round(data["correct"]/tot*100,1) if tot>0 else 0
        sc_bar="#34D399" if sp>=60 else("#FBBF24" if sp>=40 else "#F87171")
        subj_col=SUBJECT_COLORS.get(subj,"#58A6FF")
        c1,c2,c3=st.columns([4,1,1])
        with c1:
            st.markdown(f"""<div style='background:#161B22;border:1px solid #30363D;border-radius:10px;padding:.9rem 1rem;margin-bottom:.3rem'>
                <div style='display:flex;justify-content:space-between;margin-bottom:.4rem'><span style='color:{subj_col};font-weight:700'>{label}</span><span style='color:#E6EDF3;font-weight:700'>{sp}%</span></div>
                <div class="pbar-wrap"><div class="pbar-fill" style="width:{sp}%;background:{sc_bar}"></div></div>
                <div style='color:#8B949E;font-size:.73rem;margin-top:.3rem'>✅ {data['correct']} &nbsp;·&nbsp; ❌ {data['wrong']} &nbsp;·&nbsp; ⬜ {data['unattempted']}</div>
            </div>""", unsafe_allow_html=True)
        with c2: st.metric("Score",f"{data['score']:.0f}")
        with c3: st.metric("Max",f"{tot*cfg.get('marks_correct',4):.0f}")
    with st.expander("📋 Full Answer Key"):
        for i,item in enumerate(detailed):
            icon="✅" if item["given_answer"]==item["correct_answer"] else("❌" if item["given_answer"] else "⬜")
            ga=item["given_answer"] or "—"; sc2=SUBJECT_COLORS.get(item["subject"],"#58A6FF")
            st.markdown(f"<div style='padding:.4rem 0;border-bottom:1px solid #21262D'><span style='color:#8B949E'>{i+1}.</span> {item['question']}... {icon} Yours:<strong>{ga}</strong> Correct:<strong style='color:#34D399'>{item['correct_answer']}</strong> <span style='color:{sc2};font-size:.73rem'>({SUBJECT_LABELS.get(item['subject'],item['subject'])})</span></div>", unsafe_allow_html=True)
    c1,c2=st.columns(2)
    with c1:
        if st.button("🏠 Dashboard",type="primary",use_container_width=True):
            for k in ["exam_active","exam_submitted","exam_questions","exam_responses",
                      "exam_review","exam_visited","exam_current_idx","exam_score","exam_recycled_note","confirm_delete"]:
                st.session_state.pop(k,None)
            ss_set("view","dashboard"); st.rerun()
    with c2:
        if st.button("🔄 Another Exam",use_container_width=True):
            et=ss("exam_type","NEET"); el=ss("exam_lang","en")
            for k in ["exam_active","exam_submitted","exam_questions","exam_responses",
                      "exam_review","exam_visited","exam_current_idx","exam_score","exam_by_subject","exam_detailed","exam_recycled_note"]:
                st.session_state.pop(k,None)
            ss_set("preview_exam_type",et); ss_set("preview_lang",el); ss_set("view","preview"); st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
# ADMIN PANEL
# ══════════════════════════════════════════════════════════════════════════════


def show_user_recycle():
    """User-accessible recycle pool management — no admin required."""
    uid = ss("user_id", 1)
    conn = _bank_conn()
    c_back, _ = st.columns([1, 8])
    with c_back:
        if st.button("← Dashboard"): ss_set("view", "dashboard"); st.rerun()
    st.title("♻️ My Recycle Pool")
    st.markdown("Manage your personal question recycle pool. Recycled questions will be reused in future exams.")
    with _bank_lock:
        my_r = conn.execute("SELECT COUNT(*) FROM exam_recycle_pool WHERE is_available=1 AND user_id=?", (str(uid),)).fetchone()[0]
        used_r = conn.execute("SELECT COUNT(*) FROM exam_recycle_pool WHERE is_available=0 AND user_id=?", (str(uid),)).fetchone()[0]
        by_subj = conn.execute("SELECT subject,COUNT(*) FROM exam_recycle_pool WHERE is_available=1 AND user_id=? GROUP BY subject", (str(uid),)).fetchall()
    c1, c2 = st.columns(2)
    with c1: st.metric("♻️ Available in Pool", my_r)
    with c2: st.metric("✅ Already Reused", used_r)
    st.markdown("---")
    st.subheader("♻️ Add My Seen Questions to Pool")
    sel_subj = st.selectbox("Subject", ["-ALL-"] + ALL_SUBJECTS, format_func=lambda x: "All Subjects" if x == "-ALL-" else SUBJECT_LABELS.get(x, x), key="user_recycle_subj")
    if st.button("♻️ Recycle My Seen Questions", type="primary", use_container_width=True):
        subjects_to_recycle = ALL_SUBJECTS if sel_subj == "-ALL-" else [sel_subj]
        total_recycled = 0
        for subj in subjects_to_recycle:
            seen_ids = conn.execute("SELECT qb_id FROM student_q_history WHERE user_id=? AND subject=?", (str(uid), subj)).fetchall()
            for (qid,) in seen_ids:
                add_to_recycle_pool(uid, qid, subj, source="manual_recycle")
                total_recycled += 1
        st.success(f"✅ Added {total_recycled} questions to your recycle pool!")
        st.rerun()
    if by_subj:
        st.markdown("---")
        st.subheader("📊 Your Pool by Subject")
        for subj, cnt in by_subj:
            sc = SUBJECT_COLORS.get(subj, "#58A6FF")
            st.markdown(f"<div style='background:#161B22;border-left:3px solid {sc};border-radius:6px;padding:.5rem .8rem;margin-bottom:.3rem;display:flex;justify-content:space-between'><span style='color:{sc};font-weight:700'>{SUBJECT_LABELS.get(subj,subj)}</span><span style='color:#E6EDF3;font-weight:700'>{cnt}</span></div>", unsafe_allow_html=True)
    st.markdown("---")
    if st.button("🗑 Clear My Recycle Pool", use_container_width=True):
        if ss("confirm_clear_my_recycle"):
            with _bank_lock:
                conn.execute("DELETE FROM exam_recycle_pool WHERE user_id=?", (str(uid),))
            conn.commit()
            ss_set("confirm_clear_my_recycle", False)
            st.success("✅ Your recycle pool cleared!"); st.rerun()
        else:
            ss_set("confirm_clear_my_recycle", True)
            st.error("Click again to confirm — this will delete all your recycled questions")

def show_admin():
    if not ss("user",{}).get("is_admin"): st.error("⛔ Admin access only"); return
    c_back,_=st.columns([1,8])
    with c_back:
        if st.button("← Dashboard"): ss_set("view","dashboard"); st.rerun()
    st.title("🛠️ Admin Panel")
    tab1,tab2,tab3=st.tabs(["📊 Bank Stats","🌐 Translation","♻️ Recycle Pool"])
    with tab1:
        stats=get_bank_stats(); st.metric("Total Questions",f"{stats['total']:,}")
        for subj in ALL_SUBJECTS:
            count=get_subject_count(subj); sc=SUBJECT_COLORS.get(subj,"#58A6FF")
            st.markdown(f"<div style='background:#161B22;border:1px solid #30363D;border-radius:8px;padding:.6rem 1rem;margin-bottom:.3rem;display:flex;justify-content:space-between'><span style='color:{sc};font-weight:700'>{SUBJECT_LABELS.get(subj,subj)}</span><span style='color:#E6EDF3;font-weight:700'>{count:,}</span></div>", unsafe_allow_html=True)
        st.caption("Run `python seed_to_40000.py` to add more questions")
    with tab2:
        st.subheader("🌐 Translation Status")
        try:
            ts = get_all_translation_stats()
            total_q = ts["total"]
            all_pcts = [d["pct"] for d in ts["languages"].values()]
            overall_pct = round(sum(all_pcts) / len(all_pcts), 1) if all_pcts else 0
            overall_color = "#34D399" if overall_pct >= 90 else ("#FBBF24" if overall_pct >= 50 else "#F87171")
            st.markdown(f"""
            <div style='background:#1C1C2E;border:2px solid {overall_color}40;border-radius:12px;padding:1rem 1.5rem;margin-bottom:1rem;display:flex;justify-content:space-between;align-items:center'>
                <div><span style='color:#E6EDF3;font-size:1rem;font-weight:700'>📊 Overall Translation Coverage</span><br>
                <span style='color:#8B949E;font-size:.8rem'>{total_q:,} questions × 8 languages</span></div>
                <span style='font-size:1.8rem;font-weight:900;color:{overall_color}'>{overall_pct}%</span>
            </div>""", unsafe_allow_html=True)
            cols = st.columns(2)
            for i, (lc, data) in enumerate(ts["languages"].items()):
                pct = data["pct"]
                bc = "#34D399" if pct >= 90 else ("#FBBF24" if pct >= 50 else "#F87171")
                with cols[i % 2]:
                    st.markdown(f"""<div style='background:#161B22;border:1px solid #30363D;border-radius:8px;padding:.7rem 1rem;margin-bottom:.4rem'>
                        <div style='display:flex;justify-content:space-between;margin-bottom:.3rem'>
                            <span style='color:#E6EDF3;font-weight:600'>{data["native"]} <span style="color:#8B949E;font-size:.8rem">({data["name"]})</span></span>
                            <span style='color:{bc};font-weight:700'>{pct}%</span>
                        </div>
                        <div class='pbar-wrap'><div class='pbar-fill' style='width:{pct}%;background:{bc}'></div></div>
                        <div style='color:#8B949E;font-size:.72rem;margin-top:.25rem'>{data["translated"]:,} / {total_q:,} &nbsp;·&nbsp; {data["remaining"]:,} remaining</div>
                    </div>""", unsafe_allow_html=True)
        except Exception as e:
            st.warning(f"Stats error: {e}")
            total_q = 0

        st.markdown("---")
        st.markdown("### ⚡ Translate All Questions (Offline — No API)")
        st.info(f"💡 **{total_q:,} questions** translated offline at ~2,000/sec using built-in phrase dictionaries. All 8 languages in ~5 minutes.")

        c_all, c_sel = st.columns(2)
        with c_all:
            if st.button("🌏 Translate ALL 8 Languages (Recommended)", type="primary", use_container_width=True):
                import time as _time
                t_start = _time.time()
                for lc in list(SUPPORTED_LANGS.keys()):
                    rem = get_untranslated_count(lc)
                    if rem == 0:
                        st.success(f"✅ {SUPPORTED_LANGS[lc]['name']}: already complete!")
                        continue
                    lang_name = SUPPORTED_LANGS[lc]["name"]
                    prog = st.progress(0.0, text=f"🔄 Translating {lang_name}...")
                    while True:
                        res = translate_batch(lc, batch_size=2000)
                        if res["translated"] == 0:
                            break
                        now_t = get_translated_count(lc)
                        pct_val = min(1.0, now_t / max(1, total_q))
                        prog.progress(pct_val, text=f"🔄 {lang_name}: {now_t:,}/{total_q:,} ({round(pct_val*100,1)}%)")
                    prog.empty()
                    st.success(f"✅ {lang_name}: {get_translated_count(lc):,}/{total_q:,} done!")
                elapsed = _time.time() - t_start
                st.balloons()
                st.success(f"🎉 All translations complete in {elapsed:.0f}s!")
                st.rerun()
        with c_sel:
            sel_langs = st.multiselect("Select specific languages", list(SUPPORTED_LANGS.keys()),
                format_func=lambda x: f"{SUPPORTED_LANGS[x]['native']} ({SUPPORTED_LANGS[x]['name']})", default=["hi"])
            if st.button("▶️ Translate Selected", use_container_width=True) and sel_langs:
                for lc in sel_langs:
                    rem = get_untranslated_count(lc)
                    if rem == 0:
                        st.success(f"✅ {SUPPORTED_LANGS[lc]['name']}: complete!")
                        continue
                    lang_name = SUPPORTED_LANGS[lc]["name"]
                    prog = st.progress(0.0, text=f"🔄 {lang_name}...")
                    while True:
                        res = translate_batch(lc, batch_size=2000)
                        if res["translated"] == 0:
                            break
                        now_t = get_translated_count(lc)
                        prog.progress(min(1.0, now_t / max(1, total_q)), text=f"🔄 {lang_name}: {now_t:,}/{total_q:,}")
                    prog.empty()
                    st.success(f"✅ {lang_name}: done!")
                st.rerun()

    with tab3:
        conn=_bank_conn()
        uid=ss("user_id",1)
        with _bank_lock:
            total_r=conn.execute("SELECT COUNT(*) FROM exam_recycle_pool WHERE is_available=1").fetchone()[0]
            my_r=conn.execute("SELECT COUNT(*) FROM exam_recycle_pool WHERE is_available=1 AND user_id=?",(str(uid),)).fetchone()[0]
            by_subj=conn.execute("SELECT subject,COUNT(*) FROM exam_recycle_pool WHERE is_available=1 GROUP BY subject").fetchall()
            used_total=conn.execute("SELECT COUNT(*) FROM exam_recycle_pool WHERE is_available=0").fetchone()[0]
        c1,c2,c3=st.columns(3)
        with c1: st.metric("♻️ Pool (All Users)",total_r)
        with c2: st.metric("♻️ Your Pool",my_r)
        with c3: st.metric("✅ Reused",used_total)
        st.markdown("---")
        st.subheader("♻️ Manual Recycle Controls")
        rc1,rc2=st.columns(2)
        with rc1:
            st.markdown("**Add your seen questions to recycle pool:**")
            sel_subj=st.selectbox("Subject",["-ALL-"]+ALL_SUBJECTS,format_func=lambda x:"All Subjects" if x=="-ALL-" else SUBJECT_LABELS.get(x,x),key="admin_recycle_subj")
            if st.button("♻️ Recycle My Seen Questions",type="primary",use_container_width=True):
                subjects_to_recycle=ALL_SUBJECTS if sel_subj=="-ALL-" else [sel_subj]
                total_recycled=0
                for subj in subjects_to_recycle:
                    seen_ids=conn.execute("SELECT qb_id FROM student_q_history WHERE user_id=? AND subject=?",(str(uid),subj)).fetchall()
                    for (qid,) in seen_ids:
                        add_to_recycle_pool(uid,qid,subj,source="manual_recycle")
                        total_recycled+=1
                st.success(f"✅ Added {total_recycled} questions to your recycle pool!")
                st.rerun()
        with rc2:
            st.markdown("**Clear all recycled data (Admin only):**")
            st.warning("Clears the entire global recycle pool.")
            if st.button("🗑 Clear Recycle Pool (Admin)",use_container_width=True):
                if ss("confirm_clear_recycle"):
                    with _bank_lock:
                        conn.execute("DELETE FROM exam_recycle_pool")
                    conn.commit(); ss_set("confirm_clear_recycle",False)
                    st.success("✅ Recycle pool cleared!"); st.rerun()
                else:
                    ss_set("confirm_clear_recycle",True)
                    st.error("Click again to confirm")
        st.markdown("---")
        st.subheader("📊 Pool by Subject")
        for subj,cnt in by_subj:
            sc=SUBJECT_COLORS.get(subj,"#58A6FF")
            st.markdown(f"<div style='background:#161B22;border-left:3px solid {sc};border-radius:6px;padding:.5rem .8rem;margin-bottom:.3rem;display:flex;justify-content:space-between'><span style='color:{sc};font-weight:700'>{SUBJECT_LABELS.get(subj,subj)}</span><span style='color:#E6EDF3;font-weight:700'>{cnt}</span></div>",unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    user=ss("user")
    if not user: show_login(); return
    view=ss("view","dashboard")
    if view=="admin": show_admin()
    elif view=="recycle": show_user_recycle()
    elif view=="preview": show_exam_preview()
    elif ss("exam_active"): show_exam()
    else: show_dashboard()

if __name__=="__main__":
    main()
