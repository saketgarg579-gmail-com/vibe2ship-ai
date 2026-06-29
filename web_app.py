import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_calendar import calendar
from email_manager import EmailManager
from ai_processor import AIProcessor
from action_engine import ActionEngine
from db_manager import DBManager
from datetime import datetime, timezone
import time
import math

# --- Page Configuration ---
st.set_page_config(page_title="Vibe2Ship AI Assistant", page_icon="🚀", layout="wide")

# ============================================================
# PREMIUM CSS DESIGN SYSTEM
# ============================================================
st.markdown("""
<style>
/* ---- Google Fonts ---- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap');

/* ---- Root Variables ---- */
:root {
    --bg-primary: #06081a;
    --bg-secondary: #0d1137;
    --bg-card: rgba(15, 20, 60, 0.55);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-bg: rgba(255, 255, 255, 0.04);
    --text-primary: #e8eaff;
    --text-secondary: #8b8fb0;
    --accent-indigo: #667eea;
    --accent-violet: #764ba2;
    --accent-cyan: #00d2ff;
    --accent-red: #ff6b6b;
    --accent-orange: #ffa64d;
    --accent-green: #4ade80;
    --accent-purple: #a855f7;
    --accent-blue: #3b82f6;
    --gradient-main: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    --gradient-hot: linear-gradient(135deg, #ff6b6b 0%, #ffa64d 100%);
    --gradient-cool: linear-gradient(135deg, #00d2ff 0%, #667eea 100%);
    --shadow-glow: 0 0 30px rgba(102, 126, 234, 0.15);
    --radius: 16px;
    --radius-sm: 10px;
    --radius-xs: 6px;
}

/* ---- Global Overrides ---- */
html, body, [data-testid="stAppViewContainer"], .main, [data-testid="stApp"] {
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background:
        radial-gradient(ellipse 80% 60% at 10% 20%, rgba(102, 126, 234, 0.12) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 90% 80%, rgba(118, 75, 162, 0.10) 0%, transparent 60%),
        radial-gradient(ellipse 50% 40% at 50% 50%, rgba(0, 210, 255, 0.05) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* ---- Header / Top Bar ---- */
header[data-testid="stHeader"] {
    background: rgba(6, 8, 26, 0.85) !important;
    backdrop-filter: blur(16px) !important;
    border-bottom: 1px solid var(--glass-border) !important;
}

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0f2e 0%, #0d1137 50%, #06081a 100%) !important;
    border-right: 1px solid var(--glass-border) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}
[data-testid="stSidebar"] .stMarkdown p {
    color: var(--text-secondary) !important;
}
[data-testid="stSidebar"] hr {
    border-color: var(--glass-border) !important;
}

/* ---- Custom Scrollbar ---- */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: rgba(102, 126, 234, 0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(102, 126, 234, 0.5); }

/* ---- Buttons ---- */
.stButton > button,
.stFormSubmitButton > button,
button[data-testid="stFormSubmitButton"],
button[kind="primaryFormSubmit"],
[data-testid="stFormSubmitButton"] > button {
    background: var(--gradient-main) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
}
.stButton > button:hover,
.stFormSubmitButton > button:hover,
button[data-testid="stFormSubmitButton"]:hover,
button[kind="primaryFormSubmit"]:hover,
[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(102, 126, 234, 0.45) !important;
    filter: brightness(1.1) !important;
}
.stButton > button:active,
.stFormSubmitButton > button:active {
    transform: translateY(0) !important;
}

/* Link buttons */
.stLinkButton > a {
    background: var(--gradient-cool) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(0, 210, 255, 0.25) !important;
}
.stLinkButton > a:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0, 210, 255, 0.4) !important;
}

/* ---- Text Inputs ---- */
.stTextInput > div > div > input,
.stTextInput input,
input[data-testid="stTextInput"] {
    background: rgba(15, 20, 60, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: var(--radius-sm) !important;
    color: #ffffff !important;
    caret-color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
    padding: 0.6rem 0.8rem !important;
}
.stTextInput > div > div > input:focus,
.stTextInput input:focus {
    border-color: var(--accent-indigo) !important;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2) !important;
    background: rgba(15, 20, 60, 0.85) !important;
    color: #ffffff !important;
    caret-color: #ffffff !important;
}

/* ---- Select Boxes ---- */
.stSelectbox > div > div,
[data-testid="stSelectbox"] > div > div,
.stSelectbox [data-baseweb="select"] {
    background: rgba(15, 20, 60, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: var(--radius-sm) !important;
    transition: border-color 0.3s ease, box-shadow 0.3s ease !important;
}
/* Ensure all nested input elements have visible text */
[data-testid="stTextInput"] input,
[data-testid="stTextInput"] div input,
.stTextInput div[data-baseweb] input {
    color: #ffffff !important;
    caret-color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
/* Input labels */
.stTextInput label,
.stSelectbox label,
[data-testid="stWidgetLabel"] {
    color: var(--text-secondary) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 500 !important;
}
/* Placeholder text */
.stTextInput input::placeholder {
    color: rgba(139, 143, 176, 0.6) !important;
    -webkit-text-fill-color: rgba(139, 143, 176, 0.6) !important;
}
/* Ultra-aggressive wildcard override for selectbox text visibility */
.stSelectbox,
.stSelectbox *,
[data-testid="stSelectbox"],
[data-testid="stSelectbox"] * {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}
.stSelectbox [data-baseweb="select"] {
    background: rgba(15, 20, 60, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: var(--radius-sm) !important;
}
/* Dropdown menu items */
[data-baseweb="popover"],
[data-baseweb="menu"],
[data-baseweb="popover"] ul,
[data-baseweb="menu"] ul {
    background: rgba(13, 17, 55, 0.95) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: var(--radius-sm) !important;
}
[data-baseweb="menu"] li,
[data-baseweb="menu"] [role="option"],
[data-baseweb="popover"] li,
[data-baseweb="popover"] [role="option"] {
    color: #ffffff !important;
    background: transparent !important;
}
[data-baseweb="menu"] li:hover,
[data-baseweb="menu"] [role="option"]:hover,
[data-baseweb="menu"] [aria-selected="true"] {
    background: rgba(102, 126, 234, 0.2) !important;
    color: #ffffff !important;
}
/* Select arrow/chevron icon */
.stSelectbox svg {
    fill: var(--text-secondary) !important;
}
/* Password eye icon */
.stTextInput button {
    color: var(--text-secondary) !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
}
.stTextInput button:hover {
    color: var(--accent-indigo) !important;
    transform: none !important;
    box-shadow: none !important;
}

/* ---- Forms ---- */
[data-testid="stForm"] {
    background: rgba(13, 17, 55, 0.5) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 20px !important;
    padding: 2rem !important;
}

/* ---- Metrics ---- */
[data-testid="stMetric"] {
    background: var(--bg-card) !important;
    backdrop-filter: blur(12px) !important;
    border: 1px solid var(--glass-border) !important;
    border-radius: var(--radius) !important;
    padding: 1.2rem !important;
    transition: all 0.3s ease !important;
}
[data-testid="stMetric"]:hover {
    border-color: rgba(102, 126, 234, 0.3) !important;
    box-shadow: var(--shadow-glow) !important;
}
[data-testid="stMetricLabel"] {
    color: var(--text-secondary) !important;
}
[data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
}

/* ---- Alerts / Info / Success / Warning ---- */
.stAlert {
    background: var(--bg-card) !important;
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--glass-border) !important;
}

/* ============================================================
   CUSTOM COMPONENT STYLES
   ============================================================ */

/* ---- Floating Orbs (Login Background) ---- */
@keyframes float-orb {
    0%, 100% { transform: translate(0, 0) scale(1); opacity: 0.6; }
    25% { transform: translate(30px, -50px) scale(1.1); opacity: 0.8; }
    50% { transform: translate(-20px, -80px) scale(0.95); opacity: 0.5; }
    75% { transform: translate(40px, -30px) scale(1.05); opacity: 0.7; }
}

.orb-container {
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    pointer-events: none;
    z-index: 0;
    overflow: hidden;
}
.orb {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    animation: float-orb 12s ease-in-out infinite;
}
.orb-1 { width: 400px; height: 400px; background: rgba(102, 126, 234, 0.2); top: 10%; left: 5%; animation-delay: 0s; }
.orb-2 { width: 350px; height: 350px; background: rgba(118, 75, 162, 0.18); top: 60%; right: 10%; animation-delay: -4s; }
.orb-3 { width: 300px; height: 300px; background: rgba(0, 210, 255, 0.12); bottom: 10%; left: 40%; animation-delay: -8s; }

/* ---- Login Card ---- */
.login-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 70vh;
    position: relative;
    z-index: 1;
}

.login-hero {
    text-align: center;
    margin-bottom: 2rem;
    animation: fadeSlideUp 0.8s ease-out;
}

.login-hero h1 {
    font-family: 'Outfit', sans-serif !important;
    font-size: 3rem !important;
    font-weight: 800 !important;
    background: linear-gradient(135deg, #667eea 0%, #00d2ff 50%, #764ba2 100%);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s ease-in-out infinite;
    margin-bottom: 0.5rem;
}

.login-hero .tagline {
    color: var(--text-secondary);
    font-size: 1.1rem;
    font-weight: 300;
    letter-spacing: 0.05em;
}

.login-card {
    background: rgba(13, 17, 55, 0.7);
    backdrop-filter: blur(24px);
    -webkit-backdrop-filter: blur(24px);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 24px;
    padding: 2.5rem;
    max-width: 480px;
    width: 100%;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4), 0 0 40px rgba(102, 126, 234, 0.08);
    animation: fadeSlideUp 1s ease-out 0.2s both;
}

.login-card h2 {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.5rem !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    margin-bottom: 0.3rem !important;
}

.login-card .subtitle {
    color: var(--text-secondary);
    font-size: 0.9rem;
    margin-bottom: 1.5rem;
}

/* ---- Dashboard Header ---- */
.dash-header {
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.12) 0%, rgba(118, 75, 162, 0.08) 100%);
    backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius);
    padding: 1.8rem 2rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1.2rem;
    animation: fadeSlideUp 0.6s ease-out;
}

.dash-avatar {
    width: 56px;
    height: 56px;
    border-radius: 50%;
    background: var(--gradient-main);
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    font-size: 1.3rem;
    color: white;
    flex-shrink: 0;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.35);
}

.dash-info h1 {
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    margin: 0 !important;
    color: var(--text-primary) !important;
}

.dash-info .dash-sub {
    color: var(--text-secondary);
    font-size: 0.95rem;
    margin-top: 4px;
}

.role-badge {
    display: inline-block;
    background: var(--gradient-main);
    color: white;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 3px 12px;
    border-radius: 20px;
    margin-left: 8px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.status-live {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    color: var(--accent-green);
    font-size: 0.85rem;
    font-weight: 500;
    margin-left: 12px;
}
.status-dot {
    width: 8px;
    height: 8px;
    background: var(--accent-green);
    border-radius: 50%;
    animation: pulse-dot 2s ease-in-out infinite;
}

/* ---- Section Titles ---- */
.section-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.3rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-title .icon {
    font-size: 1.4rem;
}

/* ---- Stats Card Row ---- */
.stats-row {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
    animation: fadeSlideUp 0.7s ease-out 0.1s both;
}
.stat-card {
    background: var(--bg-card);
    backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}
.stat-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 3px;
    border-radius: var(--radius) var(--radius) 0 0;
}
.stat-card:hover {
    border-color: rgba(102, 126, 234, 0.25);
    transform: translateY(-3px);
    box-shadow: var(--shadow-glow);
}
.stat-card .stat-icon { font-size: 1.6rem; margin-bottom: 0.5rem; }
.stat-card .stat-value {
    font-family: 'Outfit', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text-primary);
}
.stat-card .stat-label {
    font-size: 0.8rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-top: 2px;
}
.stat-card.indigo::before { background: var(--gradient-main); }
.stat-card.cyan::before { background: var(--gradient-cool); }
.stat-card.orange::before { background: var(--gradient-hot); }
.stat-card.green::before { background: linear-gradient(135deg, #4ade80, #22d3ee); }

/* ---- Task Cards ---- */
.task-card-v2 {
    background: var(--bg-card);
    backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-left: 4px solid transparent;
    border-radius: var(--radius);
    padding: 1.4rem 1.6rem;
    margin-bottom: 1rem;
    transition: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
    animation: fadeSlideUp 0.5s ease-out both;
    position: relative;
}
.task-card-v2:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 35px rgba(0, 0, 0, 0.3);
    border-color: rgba(255, 255, 255, 0.12);
}
.task-card-v2.cat-assignment { border-left-color: var(--accent-red); }
.task-card-v2.cat-interview { border-left-color: var(--accent-purple); }
.task-card-v2.cat-meeting { border-left-color: var(--accent-blue); }
.task-card-v2.cat-commitment { border-left-color: var(--accent-green); }

/* Urgency glow for < 24 hours */
.task-card-v2.urgent {
    box-shadow: 0 0 20px rgba(255, 107, 107, 0.15), inset 0 0 20px rgba(255, 107, 107, 0.03);
    animation: fadeSlideUp 0.5s ease-out both, urgency-pulse 3s ease-in-out infinite;
}

.task-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.6rem;
}

.task-category-chip {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    font-size: 0.72rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}
.chip-assignment { background: rgba(255, 107, 107, 0.15); color: var(--accent-red); }
.chip-interview { background: rgba(168, 85, 247, 0.15); color: var(--accent-purple); }
.chip-meeting { background: rgba(59, 130, 246, 0.15); color: var(--accent-blue); }
.chip-commitment { background: rgba(74, 222, 128, 0.15); color: var(--accent-green); }

.task-countdown {
    font-size: 0.78rem;
    font-weight: 600;
    padding: 4px 12px;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.06);
    color: var(--text-secondary);
}
.task-countdown.hot {
    background: rgba(255, 107, 107, 0.15);
    color: var(--accent-red);
}

.task-summary {
    font-family: 'Inter', sans-serif;
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.5rem;
    line-height: 1.4;
}

.task-deadline-row {
    display: flex;
    align-items: center;
    gap: 8px;
    color: var(--text-secondary);
    font-size: 0.85rem;
    margin-bottom: 0.5rem;
}

.task-pointer {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(74, 222, 128, 0.08);
    border: 1px solid rgba(74, 222, 128, 0.15);
    color: var(--accent-green);
    font-size: 0.82rem;
    padding: 6px 14px;
    border-radius: var(--radius-xs);
    margin-top: 0.4rem;
    line-height: 1.4;
}

/* ---- Calendar Container ---- */
.calendar-container {
    background: var(--bg-card);
    backdrop-filter: blur(12px);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius);
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    animation: fadeSlideUp 0.6s ease-out;
}

/* ---- Sidebar Styled ---- */
.sidebar-header {
    text-align: center;
    padding: 1rem 0;
    border-bottom: 1px solid var(--glass-border);
    margin-bottom: 1.5rem;
}
.sidebar-header h2 {
    font-family: 'Outfit', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    background: var(--gradient-main);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.3rem;
}
.sidebar-header .sidebar-sub {
    color: var(--text-secondary);
    font-size: 0.8rem;
}

.sidebar-info-card {
    background: rgba(15, 20, 60, 0.5);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-sm);
    padding: 0.9rem 1rem;
    margin-bottom: 0.8rem;
}
.sidebar-info-card .label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-secondary);
    margin-bottom: 3px;
}
.sidebar-info-card .value {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--text-primary);
    word-break: break-all;
}

.sidebar-sync-badge {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 0.7rem 1rem;
    background: rgba(74, 222, 128, 0.08);
    border: 1px solid rgba(74, 222, 128, 0.15);
    border-radius: var(--radius-sm);
    margin-bottom: 1rem;
    font-size: 0.85rem;
    color: var(--accent-green);
    font-weight: 500;
}

/* ---- Footer ---- */
.premium-footer {
    text-align: center;
    padding: 2rem 0 1rem 0;
    border-top: 1px solid var(--glass-border);
    margin-top: 3rem;
}
.premium-footer .footer-brand {
    font-family: 'Outfit', sans-serif;
    font-size: 0.9rem;
    font-weight: 600;
    background: var(--gradient-main);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.premium-footer .footer-sub {
    color: var(--text-secondary);
    font-size: 0.75rem;
    margin-top: 4px;
}

/* ---- Empty State ---- */
.empty-state {
    text-align: center;
    padding: 3rem 2rem;
    color: var(--text-secondary);
}
.empty-state .empty-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
    opacity: 0.6;
}
.empty-state h3 {
    font-family: 'Outfit', sans-serif;
    color: var(--text-primary);
    font-size: 1.2rem;
    margin-bottom: 0.5rem;
}
.empty-state p {
    font-size: 0.9rem;
}

/* ---- Animations ---- */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}
@keyframes shimmer {
    0%, 100% { background-position: 0% center; }
    50% { background-position: 200% center; }
}
@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.4); }
}
@keyframes urgency-pulse {
    0%, 100% { box-shadow: 0 0 20px rgba(255, 107, 107, 0.12); }
    50% { box-shadow: 0 0 35px rgba(255, 107, 107, 0.25); }
}

/* ---- Responsive ---- */
@media (max-width: 768px) {
    .stats-row { grid-template-columns: repeat(2, 1fr); }
    .dash-header { flex-direction: column; text-align: center; }
    .login-hero h1 { font-size: 2rem !important; }
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_relative_date(date_str):
    """Converts ISO date to 'Today', 'Tomorrow', etc."""
    try:
        dt = datetime.fromisoformat(date_str)
        if dt.tzinfo:
            dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
        now = datetime.now()
        target = dt.date()
        diff = (target - now.date()).days
        if diff == 0: return "Today"
        if diff == 1: return "Tomorrow"
        if diff == -1: return "Yesterday"
        return date_str[:10]
    except:
        return "Unknown"


def get_countdown(date_str):
    """Returns a human-readable countdown string and urgency flag."""
    try:
        dt = datetime.fromisoformat(date_str)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        diff = (dt - now).total_seconds()
        if diff <= 0:
            return "Overdue!", True
        minutes = diff / 60
        hours = minutes / 60
        days = hours / 24
        if days >= 2:
            return f"{int(days)}d {int(hours % 24)}h left", False
        elif hours >= 1:
            is_urgent = hours < 24
            return f"{int(hours)}h {int(minutes % 60)}m left", is_urgent
        else:
            return f"{int(minutes)}m left", True
    except:
        return "No deadline", False


def get_category_class(category):
    """Returns CSS class name for a category."""
    cat = category.lower() if category else "unknown"
    mapping = {
        'assignment': 'assignment',
        'interview': 'interview',
        'meeting': 'meeting',
        'commitment': 'commitment',
    }
    return mapping.get(cat, 'meeting')


def get_category_icon(category):
    """Returns an emoji icon for a category."""
    cat = category.lower() if category else "unknown"
    mapping = {
        'assignment': '📝',
        'interview': '💼',
        'meeting': '🎯',
        'commitment': '🤝',
    }
    return mapping.get(cat, '📌')


def check_and_trigger_alerts(email, tasks, action_eng, db):
    """Checks deadlines and triggers SMS/Calls based on time thresholds."""
    now = datetime.now(timezone.utc)
    alert_triggered = False
    for task in tasks:
        deadline_str = task.get('deadline')
        if deadline_str:
            try:
                # Parse date and ensure it is timezone-aware (UTC)
                try:
                    deadline_dt = datetime.fromisoformat(deadline_str)
                except:
                    deadline_dt = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")

                if deadline_dt.tzinfo is None:
                    deadline_dt = deadline_dt.replace(tzinfo=timezone.utc)
                else:
                    deadline_dt = deadline_dt.astimezone(timezone.utc)

                diff = (deadline_dt - now).total_seconds() / 60

                # 1. SMS Alert at 24 Hours (1440 mins)
                if 1430 <= diff <= 1450 and not task.get('sms_24h', False):
                    action_eng.send_sms(task.get('category', 'Event'), 1440)
                    # Update DB to prevent repeat SMS
                    db.save_task(email, {**task, "sms_24h": True})
                    alert_triggered = True

                # 2. SMS & Voice Call Alert at 30 Minutes
                if diff <= 30 and not task.get('called', False):
                    category = task.get('category', 'Meeting')
                    action_eng.send_sms(category, diff)  # SMS alert
                    action_eng.trigger_phone_call(category, diff)  # Voice call

                    # Mark as called in DB
                    db.mark_as_called(email, task['summary'])
                    alert_triggered = True
            except Exception as e:
                print(f"Alert Logic Error: {e}")
    return alert_triggered


# ============================================================
# SESSION STATE
# ============================================================
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False


# ============================================================
# 1. LOGIN PAGE
# ============================================================
if not st.session_state.authenticated:
    # Floating orbs background
    st.markdown("""
    <div class="orb-container">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
    </div>
    """, unsafe_allow_html=True)

    # Hero section
    st.markdown("""
    <div class="login-wrapper">
        <div class="login-hero">
            <h1>🚀 Vibe2Ship AI</h1>
            <p class="tagline">Your Proactive AI Academic Guardian</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Centered login form
    col_a, col_b, col_c = st.columns([1.2, 2, 1.2])
    with col_b:
        st.markdown("""
        <div class="login-card">
            <h2>Welcome Aboard 👋</h2>
            <p class="subtitle">Connect your inbox and let AI handle the rest.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            name = st.text_input("👤 Your Name", placeholder="e.g. Saket Garg")
            email = st.text_input("📧 Gmail Address", placeholder="you@gmail.com")
            app_pass = st.text_input("🔑 Gmail App Password", type="password", placeholder="Your app-specific password")
            phone = st.text_input("📱 Phone Number", placeholder="+91XXXXXXXXXX")
            role = st.selectbox("🎓 I am a...", ["Student", "Professor"])

            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("🚀 Launch Assistant")
            if submit and name and email and app_pass and phone:
                st.session_state.user_info = {"name": name, "email": email, "pass": app_pass, "phone": phone, "role": role}
                st.session_state.authenticated = True
                st.rerun()
            elif submit:
                st.error("⚠️ Please fill in all required fields to continue.")


# ============================================================
# 2. MAIN DASHBOARD
# ============================================================
else:
    user = st.session_state.user_info
    email_mgr = EmailManager(user['email'], user['pass'])
    ai_proc = AIProcessor()
    action_eng = ActionEngine(user['phone'])
    db = DBManager()

    # AUTO-REFRESH: Every 1 minute to sync emails and check deadlines
    st_autorefresh(interval=60 * 1000, key="datarefresh")

    # ---- Fetch Data ----
    tasks = db.get_tasks(user['email'])
    if check_and_trigger_alerts(user['email'], tasks, action_eng, db):
        st.toast("📞 Proactive Alert Triggered!", icon="🔔")

    # ---- Dashboard Header ----
    user_name = user.get('name', 'User')
    initials = user_name[0].upper() if user_name else "U"
    st.markdown(f"""
    <div class="dash-header">
        <div class="dash-avatar">{initials}</div>
        <div class="dash-info">
            <h1>
                Hey, {user_name}!
                <span class="role-badge">{user['role']}</span>
                <span class="status-live"><span class="status-dot"></span> Monitoring</span>
            </h1>
            <div class="dash-sub">Welcome back — your AI assistant is watching your inbox.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- Sidebar ----
    with st.sidebar:
        st.markdown(f"""
        <div class="sidebar-header">
            <h2>🚀 Vibe2Ship AI</h2>
            <div class="sidebar-sub">Proactive Academic Assistant</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="sidebar-info-card">
            <div class="label">Role</div>
            <div class="value">🎓 {user['role']}</div>
        </div>
        <div class="sidebar-info-card">
            <div class="label">Phone</div>
            <div class="value">📱 {user['phone']}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div class="sidebar-sync-badge">
            <span class="status-dot" style="background: #4ade80;"></span>
            Auto-sync active • every 60s
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        if st.button("🔍 Sync Inbox Now"):
            with st.spinner("🤖 AI analyzing your inbox..."):
                raw_emails = email_mgr.fetch_unread_emails()
                if raw_emails:
                    new_count = 0
                    for em in raw_emails:
                        full_text = f"Subject: {em['subject']}\nBody: {em['body']}"
                        analysis = ai_proc.analyze_email(full_text)
                        if isinstance(analysis, dict) and analysis.get('category', 'Promotional') != 'Promotional':
                            analysis['email'] = user['email']
                            analysis['called'] = False
                            analysis['sms_24h'] = False
                            db.save_task(user['email'], analysis)
                            new_count += 1
                    if new_count > 0:
                        st.success(f"✅ Synced {new_count} new tasks!")
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.info("No new urgent tasks found.")
                else:
                    st.warning("No unread emails in your inbox.")

        if st.button("🗑️ Clear All Tasks"):
            db.clear_tasks(user['email'])
            st.rerun()

        st.markdown("---")

        if st.button("🚪 Logout"):
            st.session_state.authenticated = False
            st.rerun()

    # ---- Stats Bar ----
    role = user['role']
    filtered_tasks = []
    for t in tasks:
        cat = t.get('category', 'Promotional')
        if role == "Student":
            if cat in ['Assignment', 'Interview', 'Commitment']:
                filtered_tasks.append(t)
        else:
            if cat not in ['Assignment', 'Interview']:
                filtered_tasks.append(t)

    filtered_tasks.sort(key=lambda x: x.get('deadline', '9999-12-31'))

    # Compute stats
    total_tasks = len(filtered_tasks)
    alerts_sent = sum(1 for t in filtered_tasks if t.get('called', False))
    categories_found = list(set(t.get('category', 'Unknown') for t in filtered_tasks))

    # Next deadline
    next_deadline_str = "None"
    for t in filtered_tasks:
        dl = t.get('deadline')
        if dl:
            try:
                dt = datetime.fromisoformat(dl)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                if dt > datetime.now(timezone.utc):
                    countdown_text, _ = get_countdown(dl)
                    next_deadline_str = countdown_text
                    break
            except:
                pass

    cat_chips_html = ""
    for c in categories_found:
        icon = get_category_icon(c)
        cat_chips_html += f'<span style="background:rgba(255,255,255,0.06);padding:3px 10px;border-radius:12px;font-size:0.75rem;margin-right:4px;">{icon} {c}</span>'
    if not cat_chips_html:
        cat_chips_html = '<span style="color:var(--text-secondary);font-size:0.8rem;">—</span>'

    st.markdown(f"""
    <div class="stats-row">
        <div class="stat-card indigo">
            <div class="stat-icon">📧</div>
            <div class="stat-value">{total_tasks}</div>
            <div class="stat-label">Tasks Tracked</div>
        </div>
        <div class="stat-card cyan">
            <div class="stat-icon">⏱️</div>
            <div class="stat-value" style="font-size:1.1rem;">{next_deadline_str}</div>
            <div class="stat-label">Next Deadline</div>
        </div>
        <div class="stat-card orange">
            <div class="stat-icon">🔔</div>
            <div class="stat-value">{alerts_sent}</div>
            <div class="stat-label">Alerts Sent</div>
        </div>
        <div class="stat-card green">
            <div class="stat-icon">📊</div>
            <div class="stat-value" style="font-size:0.9rem;">{cat_chips_html}</div>
            <div class="stat-label">Categories</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- Calendar View ----
    st.markdown('<div class="section-title"><span class="icon">🗓️</span> Timeline Overview</div>', unsafe_allow_html=True)
    st.markdown('<div class="calendar-container">', unsafe_allow_html=True)
    calendar_events = []
    for t in tasks:
        calendar_events.append({
            "title": t.get('summary', 'Untitled'),
            "start": t.get('deadline'),
            "end": t.get('deadline'),
            "url": t.get('link')
        })
    calendar(events=calendar_events)
    st.markdown('</div>', unsafe_allow_html=True)

    # ---- Task List ----
    st.markdown('<div class="section-title"><span class="icon">🎯</span> Prioritized Deadlines</div>', unsafe_allow_html=True)

    if not filtered_tasks:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">✨</div>
            <h3>All Clear!</h3>
            <p>Your dashboard is clean. Hit <strong>Sync Inbox</strong> to check for new tasks.</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        for idx, task in enumerate(filtered_tasks):
            category = task.get('category', 'Unknown')
            summary = task.get('summary', 'No summary')
            deadline = task.get('deadline', 'No deadline')
            link = task.get('link')
            pointers = task.get('study_pointers', '')

            cat_class = get_category_class(category)
            cat_icon = get_category_icon(category)
            rel_date = get_relative_date(deadline)
            countdown_text, is_urgent = get_countdown(deadline)

            urgent_class = "urgent" if is_urgent else ""
            countdown_hot = "hot" if is_urgent else ""

            # Build the card HTML
            pointer_html = ""
            if pointers:
                pointer_html = f'<div class="task-pointer">💡 {pointers}</div>'

            card_html = f"""
            <div class="task-card-v2 cat-{cat_class} {urgent_class}" style="animation-delay: {idx * 0.08}s;">
                <div class="task-header">
                    <span class="task-category-chip chip-{cat_class}">{cat_icon} {category}</span>
                    <span class="task-countdown {countdown_hot}">⏱ {countdown_text}</span>
                </div>
                <div class="task-summary">{summary}</div>
                <div class="task-deadline-row">
                    <span>📅 {rel_date}</span>
                    <span>•</span>
                    <span>{deadline}</span>
                </div>
                {pointer_html}
            </div>
            """
            st.markdown(card_html, unsafe_allow_html=True)

            if link:
                btn_txt = "🔗 Join Meeting" if category in ['Interview', 'Meeting'] else "🔗 Open Portal"
                st.link_button(btn_txt, link)

    # ---- Footer ----
    st.markdown("""
    <div class="premium-footer">
        <div class="footer-brand">✦ Vibe2Ship AI — Proactive Academic Intelligence ✦</div>
        <div class="footer-sub">Built for Vibe2Ship Hackathon • Powered by Gemini AI, Twilio & MongoDB</div>
    </div>
    """, unsafe_allow_html=True)
