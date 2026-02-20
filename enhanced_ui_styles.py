"""
Enhanced UI Styles - ULTIMATE Professional Design
=================================================
Beautiful, modern, professional UI components
"""

# ══════════════════════════════════════════════════════════════════════════════
# ENHANCED CSS STYLES
# ══════════════════════════════════════════════════════════════════════════════

ENHANCED_CSS = """
<style>
/* ══════════════════════════════════════════════════════════════════════════
   GLOBAL STYLES & UTILITIES
   ══════════════════════════════════════════════════════════════════════════ */

/* Hide Streamlit branding and unnecessary elements */
#MainMenu, footer, .stDeployButton { 
    display: none !important; 
    visibility: hidden !important;
}

/* Hide anchor link icons */
h1 a, h2 a, h3 a, h4 a, h5 a, h6 a,
a[data-testid="stMarkdownAnchorLink"],
a.anchor-link, .anchor-link,
[data-testid="stMarkdown"] h1 a,
[data-testid="stMarkdown"] h2 a,
[data-testid="stMarkdown"] h3 a {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* Global font */
html, body, [class*="css"] {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Inter", sans-serif !important;
}

/* Smooth scrolling */
html {
    scroll-behavior: smooth;
}

/* ══════════════════════════════════════════════════════════════════════════
   ENHANCED HEADER & TITLES
   ══════════════════════════════════════════════════════════════════════════ */

.main-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    text-align: center;
}

.main-header h1 {
    color: white !important;
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    margin: 0 !important;
    text-shadow: 0 2px 10px rgba(0,0,0,0.2);
}

.main-header p {
    color: rgba(255,255,255,0.9) !important;
    font-size: 1.1rem !important;
    margin-top: 0.5rem !important;
}

/* Section Headers */
.section-header {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    padding: 1.5rem;
    border-radius: 12px;
    margin: 1.5rem 0 1rem 0;
    box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);
}

.section-header h2 {
    color: white !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    margin: 0 !important;
}

/* ══════════════════════════════════════════════════════════════════════════
   BEAUTIFUL CARDS & CONTAINERS
   ══════════════════════════════════════════════════════════════════════════ */

.info-card {
    background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
    border: 2px solid #667eea44;
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
    backdrop-filter: blur(10px);
    transition: all 0.3s ease;
}

.info-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
    border-color: #667eea;
}

.success-card {
    background: linear-gradient(135deg, #84fab022 0%, #8fd3f422 100%);
    border: 2px solid #84fab044;
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.warning-card {
    background: linear-gradient(135deg, #fa709a22 0%, #fee14022 100%);
    border: 2px solid #fa709a44;
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
}

.error-card {
    background: linear-gradient(135deg, #ff616122 0%, #ff575c22 100%);
    border: 2px solid #ff616144;
    border-radius: 16px;
    padding: 1.5rem;
    margin: 1rem 0;
}

/* ══════════════════════════════════════════════════════════════════════════
   ENHANCED TABS
   ══════════════════════════════════════════════════════════════════════════ */

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    border-radius: 16px;
    padding: 8px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 12px !important;
    padding: 12px 24px !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    transition: all 0.3s ease !important;
    border: 2px solid transparent !important;
}

.stTabs [data-baseweb="tab"]:hover {
    background: rgba(59, 130, 246, 0.1) !important;
    color: #60a5fa !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
    transform: translateY(-2px);
}

/* ══════════════════════════════════════════════════════════════════════════
   ENHANCED INPUTS & FORMS
   ══════════════════════════════════════════════════════════════════════════ */

.stTextInput input, .stNumberInput input, .stSelectbox select {
    border-radius: 12px !important;
    border: 2px solid #334155 !important;
    background: linear-gradient(135deg, #1e293b 0%, #334155 100%) !important;
    color: #f1f5f9 !important;
    padding: 12px 16px !important;
    font-size: 15px !important;
    transition: all 0.3s ease !important;
}

.stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 4px rgba(59, 130, 246, 0.2) !important;
    transform: translateY(-1px);
}

.stTextInput input:hover, .stNumberInput input:hover {
    border-color: #475569 !important;
}

/* ══════════════════════════════════════════════════════════════════════════
   BEAUTIFUL BUTTONS
   ══════════════════════════════════════════════════════════════════════════ */

/* Primary Buttons (Form Submit) */
[data-testid="stFormSubmitButton"] button {
    border-radius: 12px !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    padding: 14px !important;
    background: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%) !important;
    border: none !important;
    color: white !important;
    width: 100% !important;
    box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4) !important;
    transition: all 0.3s ease !important;
    cursor: pointer !important;
}

[data-testid="stFormSubmitButton"] button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(59, 130, 246, 0.5) !important;
    background: linear-gradient(135deg, #2563eb 0%, #4f46e5 100%) !important;
}

[data-testid="stFormSubmitButton"] button:active {
    transform: translateY(0) !important;
    box-shadow: 0 2px 10px rgba(59, 130, 246, 0.3) !important;
}

/* Regular Buttons */
.stButton button {
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 10px 20px !important;
    transition: all 0.3s ease !important;
    border: 2px solid transparent !important;
}

.stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
}

/* Success Button */
.success-button button {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(16, 185, 129, 0.4) !important;
}

.success-button button:hover {
    background: linear-gradient(135deg, #059669 0%, #047857 100%) !important;
}

/* Danger Button */
.danger-button button {
    background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%) !important;
    color: white !important;
    box-shadow: 0 4px 15px rgba(239, 68, 68, 0.4) !important;
}

.danger-button button:hover {
    background: linear-gradient(135deg, #dc2626 0%, #b91c1c 100%) !important;
}

/* ══════════════════════════════════════════════════════════════════════════
   ENHANCED METRICS & STATS
   ══════════════════════════════════════════════════════════════════════════ */

.stMetric {
    background: linear-gradient(135deg, #667eea22 0%, #764ba222 100%);
    border-radius: 16px;
    padding: 1.5rem !important;
    border: 2px solid #667eea44;
    transition: all 0.3s ease;
}

.stMetric:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    border-color: #667eea;
}

.stMetric label {
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    color: #94a3b8 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.stMetric [data-testid="stMetricValue"] {
    font-size: 2.5rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
}

/* ══════════════════════════════════════════════════════════════════════════
   PROGRESS BARS & INDICATORS
   ══════════════════════════════════════════════════════════════════════════ */

/* Track (background) */
.stProgress > div {
    background: #1e293b !important;
    border-radius: 10px !important;
    height: 12px !important;
    overflow: hidden !important;
}

/* Fill bar — only the ::before / the inner progress element */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #3b82f6 0%, #6366f1 100%) !important;
    border-radius: 10px !important;
    height: 12px !important;
    transition: width 0.4s ease !important;
}

/* Loading Spinner */
.stSpinner > div {
    border-top-color: #3b82f6 !important;
    border-right-color: #6366f1 !important;
}

/* ══════════════════════════════════════════════════════════════════════════
   ALERTS & NOTIFICATIONS
   ══════════════════════════════════════════════════════════════════════════ */

.stAlert {
    border-radius: 12px !important;
    border-width: 2px !important;
    padding: 1rem 1.5rem !important;
    backdrop-filter: blur(10px) !important;
}

/* Success Alert */
[data-baseweb="notification"][kind="success"] {
    background: linear-gradient(135deg, #10b98122 0%, #05966922 100%) !important;
    border-color: #10b981 !important;
}

/* Info Alert */
[data-baseweb="notification"][kind="info"] {
    background: linear-gradient(135deg, #3b82f622 0%, #6366f122 100%) !important;
    border-color: #3b82f6 !important;
}

/* Warning Alert */
[data-baseweb="notification"][kind="warning"] {
    background: linear-gradient(135deg, #f59e0b22 0%, #d9770622 100%) !important;
    border-color: #f59e0b !important;
}

/* ── st.status() widget styling ───────────────────────────────────────────── */
[data-testid="stStatusWidget"] {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
}

[data-testid="stStatusWidget"] [data-testid="stStatusWidgetLabel"] {
    font-weight: 700 !important;
    font-size: 15px !important;
}

/* Running state — blue glow */
[data-testid="stStatusWidget"][data-state="running"] {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 1px #3b82f622 !important;
}

/* Complete state — green glow */
[data-testid="stStatusWidget"][data-state="complete"] {
    border-color: #10b981 !important;
    box-shadow: 0 0 0 1px #10b98122 !important;
}

/* Error state — red glow */
[data-testid="stStatusWidget"][data-state="error"] {
    border-color: #ef4444 !important;
    box-shadow: 0 0 0 1px #ef444422 !important;
}

/* Error Alert */
[data-baseweb="notification"][kind="error"] {
    background: linear-gradient(135deg, #ef444422 0%, #dc262622 100%) !important;
    border-color: #ef4444 !important;
}

/* ══════════════════════════════════════════════════════════════════════════
   TABLES & DATA DISPLAY
   ══════════════════════════════════════════════════════════════════════════ */

.stDataFrame {
    border-radius: 12px !important;
    overflow: hidden !important;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
}

table {
    border-collapse: separate !important;
    border-spacing: 0 !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}

thead tr {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
}

thead th {
    padding: 12px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
    font-size: 0.85rem !important;
}

tbody tr {
    transition: all 0.2s ease !important;
}

tbody tr:hover {
    background: rgba(102, 126, 234, 0.1) !important;
    transform: scale(1.01);
}

tbody td {
    padding: 10px 12px !important;
    border-bottom: 1px solid #334155 !important;
}

/* ══════════════════════════════════════════════════════════════════════════
   SIDEBAR ENHANCEMENTS
   ══════════════════════════════════════════════════════════════════════════ */

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%) !important;
    border-right: 1px solid #334155 !important;
}

[data-testid="stSidebar"] .stMarkdown {
    color: #f1f5f9 !important;
}

/* ══════════════════════════════════════════════════════════════════════════
   CUSTOM UTILITY CLASSES
   ══════════════════════════════════════════════════════════════════════════ */

.gradient-text {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}

.status-badge {
    display: inline-block;
    padding: 6px 16px;
    border-radius: 20px;
    font-weight: 600;
    font-size: 0.85rem;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.status-active {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    box-shadow: 0 2px 10px rgba(16, 185, 129, 0.3);
}

.status-pending {
    background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
    color: white;
    box-shadow: 0 2px 10px rgba(245, 158, 11, 0.3);
}

.status-inactive {
    background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%);
    color: white;
    box-shadow: 0 2px 10px rgba(107, 114, 128, 0.3);
}

/* ══════════════════════════════════════════════════════════════════════════
   ANIMATIONS
   ══════════════════════════════════════════════════════════════════════════ */

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { transform: translateX(-20px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

.fade-in {
    animation: fadeIn 0.5s ease-out;
}

.slide-in {
    animation: slideIn 0.4s ease-out;
}

.pulse-animation {
    animation: pulse 2s ease-in-out infinite;
}

/* ══════════════════════════════════════════════════════════════════════════
   RESPONSIVE DESIGN
   ══════════════════════════════════════════════════════════════════════════ */

@media (max-width: 768px) {
    .main-header h1 { font-size: 2rem !important; }
    .section-header h2 { font-size: 1.5rem !important; }
    .stMetric [data-testid="stMetricValue"] { font-size: 2rem !important; }
}

/* ══════════════════════════════════════════════════════════════════════════
   DARK MODE OPTIMIZATION
   ══════════════════════════════════════════════════════════════════════════ */

.stApp {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%) !important;
}

/* ══════════════════════════════════════════════════════════════════════════
   SCROLLBAR STYLING
   ══════════════════════════════════════════════════════════════════════════ */

::-webkit-scrollbar {
    width: 10px;
    height: 10px;
}

::-webkit-scrollbar-track {
    background: #1e293b;
    border-radius: 10px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 10px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

</style>
"""

# ══════════════════════════════════════════════════════════════════════════════
# ENHANCED HTML COMPONENTS
# ══════════════════════════════════════════════════════════════════════════════

def create_header(title: str, subtitle: str = "") -> str:
    """Create beautiful main header"""
    subtitle_html = f'<p>{subtitle}</p>' if subtitle else ''
    return f"""
    <div class="main-header fade-in">
        <h1>🎓 {title}</h1>
        {subtitle_html}
    </div>
    """

def create_section_header(title: str, icon: str = "📋") -> str:
    """Create section header"""
    return f"""
    <div class="section-header slide-in">
        <h2>{icon} {title}</h2>
    </div>
    """

def create_info_card(content: str, title: str = "") -> str:
    """Create info card"""
    title_html = f'<h3 style="margin-top:0; color:#667eea;">{title}</h3>' if title else ''
    return f"""
    <div class="info-card fade-in">
        {title_html}
        <div>{content}</div>
    </div>
    """

def create_success_card(content: str) -> str:
    """Create success card"""
    return f"""
    <div class="success-card fade-in">
        <div style="color:#10b981; font-weight:600;">✅ {content}</div>
    </div>
    """

def create_warning_card(content: str) -> str:
    """Create warning card"""
    return f"""
    <div class="warning-card fade-in">
        <div style="color:#f59e0b; font-weight:600;">⚠️ {content}</div>
    </div>
    """

def create_error_card(content: str) -> str:
    """Create error card"""
    return f"""
    <div class="error-card fade-in">
        <div style="color:#ef4444; font-weight:600;">❌ {content}</div>
    </div>
    """

def create_status_badge(status: str, type: str = "active") -> str:
    """Create status badge"""
    return f'<span class="status-badge status-{type}">{status}</span>'

def create_gradient_text(text: str) -> str:
    """Create gradient text"""
    return f'<span class="gradient-text">{text}</span>'

# ══════════════════════════════════════════════════════════════════════════════
# PROGRESS INDICATORS
# ══════════════════════════════════════════════════════════════════════════════

def create_loading_message(message: str) -> str:
    """Create animated loading message"""
    return f"""
    <div class="info-card pulse-animation">
        <div style="text-align:center; padding:1rem;">
            <div style="font-size:2rem; margin-bottom:0.5rem;">⏳</div>
            <div style="font-weight:600; color:#667eea;">{message}</div>
        </div>
    </div>
    """

# ══════════════════════════════════════════════════════════════════════════════
# EXAM TYPE CARDS
# ══════════════════════════════════════════════════════════════════════════════

EXAM_CARDS = {
    "JEE": {
        "gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
        "icon": "🎯",
        "title": "JEE Main",
        "desc": "Engineering Entrance • 75 Questions • 300 Marks"
    },
    "NEET": {
        "gradient": "linear-gradient(135deg, #f093fb 0%, #f5576c 100%)",
        "icon": "🩺",
        "title": "NEET UG",
        "desc": "Medical Entrance • 180 Questions • 720 Marks"
    },
    "CUET": {
        "gradient": "linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)",
        "icon": "🎓",
        "title": "CUET Domain",
        "desc": "University Entrance • Subject-wise • NCERT Based"
    },
    "CUET_GT": {
        "gradient": "linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)",
        "icon": "📘",
        "title": "CUET General Test",
        "desc": "Aptitude • 50 Questions • 250 Marks"
    }
}

def create_exam_card(exam_type: str) -> str:
    """Create beautiful exam type card"""
    card = EXAM_CARDS.get(exam_type, EXAM_CARDS["JEE"])
    return f"""
    <div style="
        background: {card['gradient']};
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        cursor: pointer;
        margin: 1rem 0;
    " class="fade-in">
        <div style="font-size: 3rem; margin-bottom: 0.5rem;">{card['icon']}</div>
        <h2 style="color: white; margin: 0.5rem 0;">{card['title']}</h2>
        <p style="color: rgba(255,255,255,0.9); margin: 0;">{card['desc']}</p>
    </div>
    """
