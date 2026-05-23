"""
SEISWATCH — Global Seismic Intelligence Platform v3.0
Streamlit single-file app — deployable on Streamlit Cloud
"""

import time, math, random, json, io, csv
from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SEISWATCH — Seismic Intelligence",
    page_icon="🌋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Colour palette ──────────────────────────────────────────────────────────
RED    = "#dc2626"
ORANGE = "#ea580c"
AMBER  = "#d97706"
YELLOW = "#eab308"
GREEN  = "#16a34a"
BG     = "#060606"
CARD   = "#0f0f0f"
BORDER = "#1e0a00"
TEXT   = "#f0e8d8"
MUTED  = "#5a3a1a"
DIM    = "#3a2010"

# ── Global CSS injection ────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Share Tech Mono', monospace !important;
    background-color: #060606;
    color: #f0e8d8;
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0.8rem 1.2rem 2rem; max-width: 100%; }

div[data-testid="metric-container"] {
    background: #0f0f0f;
    border: 1px solid #1e0a00;
    border-radius: 8px;
    padding: 10px 14px;
    transition: box-shadow 0.3s ease, transform 0.2s ease, border-color 0.3s ease;
}
div[data-testid="metric-container"]:hover {
    box-shadow: 0 0 14px rgba(234,88,12,0.35), 0 0 30px rgba(234,88,12,0.12) !important;
    border-color: rgba(234,88,12,0.55) !important;
    transform: translateY(-2px);
}
div[data-testid="metric-container"] label {
    color: #5a3a1a !important;
    font-size: 9px !important;
    letter-spacing: 0.12em;
    text-transform: uppercase;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    font-size: 22px !important;
    font-weight: 700 !important;
}

div[data-testid="stTabs"] button {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.12em !important;
    color: #5a3a1a !important;
    background: transparent !important;
    border: none !important;
    padding: 6px 14px !important;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #ea580c !important;
    border-bottom: 2px solid #ea580c !important;
}
div[data-testid="stTabs"] {
    border-bottom: 1px solid #1a0800;
    background: #0b0b0b;
}

div[data-testid="stButton"] button {
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 10px !important;
    font-weight: 700 !important;
    letter-spacing: 0.1em !important;
    border-radius: 5px !important;
    background: transparent !important;
    border: 1px solid #ea580c !important;
    color: #ea580c !important;
    transition: all 0.2s !important;
}
div[data-testid="stButton"] button:hover {
    background: rgba(234,88,12,0.12) !important;
}

div[data-testid="stSlider"] { padding: 4px 0; }
div[data-testid="stSlider"] > div > div > div { background: #ea580c !important; }

div[data-testid="stSelectbox"] > div {
    background: #0f0f0f;
    border: 1px solid #1e0a00;
    border-radius: 4px;
    color: #f0e8d8;
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
}

div[data-testid="stTextInput"] input {
    background: #0a0a0a;
    border: 1px solid #1e0a00;
    color: #f0e8d8;
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
    border-radius: 4px;
}

div[data-testid="stChatMessage"] {
    background: #0f0f0f;
    border: 1px solid #1e0a00;
    border-radius: 7px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 12px;
}

div[data-testid="stDataFrame"] {
    background: #0f0f0f;
    border: 1px solid #1e0a00;
    border-radius: 7px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 10px;
}

section[data-testid="stSidebar"] {
    background: #0b0b0b;
    border-right: 1px solid #1e0a00;
}

div[data-testid="stExpander"] {
    background: #0f0f0f;
    border: 1px solid #1e0a00;
    border-radius: 7px;
}

::-webkit-scrollbar { width: 3px; }
::-webkit-scrollbar-track { background: #080808; }
::-webkit-scrollbar-thumb { background: #2a1400; border-radius: 2px; }

/* ═══════════════════════════════════════
   PHASE 1 — FEATURE 1: ANIMATED BACKGROUND
   ═══════════════════════════════════════ */
body::before {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    z-index: -2;
    background:
        radial-gradient(ellipse 80% 40% at 20% 60%, rgba(220,38,38,0.05) 0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 20%, rgba(234,88,12,0.04) 0%, transparent 60%),
        radial-gradient(ellipse 40% 30% at 50% 80%, rgba(217,119,6,0.03) 0%, transparent 55%),
        #060606;
    animation: bgShift 14s ease-in-out infinite alternate;
}
@keyframes bgShift {
    0%   { opacity: 0.6; }
    50%  { opacity: 1.0; }
    100% { opacity: 0.7; }
}
body::after {
    content: '';
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    background-image:
        linear-gradient(rgba(234,88,12,0.018) 1px, transparent 1px),
        linear-gradient(90deg, rgba(234,88,12,0.018) 1px, transparent 1px);
    background-size: 44px 44px;
    z-index: -1;
    pointer-events: none;
    animation: gridPulse 9s ease-in-out infinite;
}
@keyframes gridPulse {
    0%, 100% { opacity: 0.35; }
    50%       { opacity: 0.9; }
}

/* ═══════════════════════════════════════
   PHASE 1 — FEATURE 2: GLOW CARDS
   ═══════════════════════════════════════ */
.card {
    background: #0f0f0f;
    border: 1px solid #1e0a00;
    border-radius: 9px;
    padding: 14px;
    margin-bottom: 10px;
    transition: box-shadow 0.3s ease, border-color 0.3s ease, transform 0.2s ease;
    position: relative;
    overflow: hidden;
}
.card::after {
    content: '';
    position: absolute;
    top: 0; left: -100%;
    width: 50%; height: 100%;
    background: linear-gradient(90deg, transparent, rgba(234,88,12,0.04), transparent);
    animation: cardShimmer 5s ease-in-out infinite;
    pointer-events: none;
}
@keyframes cardShimmer {
    0%   { left: -100%; }
    60%  { left: 160%; }
    100% { left: 160%; }
}
.card:hover {
    box-shadow: 0 0 18px rgba(234,88,12,0.25), 0 0 36px rgba(220,38,38,0.08) !important;
    border-color: rgba(234,88,12,0.5) !important;
    transform: translateY(-1px);
}
.card-title {
    color: #5a3a1a;
    font-size: 9px;
    text-transform: uppercase;
    letter-spacing: 0.14em;
    margin-bottom: 8px;
}
.qrow {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 10px;
    background: #0f0f0f;
    border: 1px solid #1e0a00;
    border-radius: 6px;
    margin-bottom: 4px;
    cursor: pointer;
    transition: box-shadow 0.2s ease, border-color 0.2s ease, transform 0.15s ease;
}
.qrow:hover {
    border-color: rgba(234,88,12,0.4);
    box-shadow: 0 0 10px rgba(234,88,12,0.18);
    transform: translateX(2px);
}
.glow-red    { box-shadow: 0 0 18px rgba(220,38,38,0.55),  0 0 36px rgba(220,38,38,0.18) !important; }
.glow-orange { box-shadow: 0 0 18px rgba(234,88,12,0.50),  0 0 36px rgba(234,88,12,0.15) !important; }
.glow-amber  { box-shadow: 0 0 14px rgba(217,119,6,0.45),  0 0 28px rgba(217,119,6,0.12) !important; }

/* ═══════════════════════════════════════
   PHASE 1 — FEATURE 3: FLASH ALERTS
   ═══════════════════════════════════════ */
@keyframes alertFlash {
    from { border-color: #dc2626; background: rgba(220,38,38,0.12); }
    to   { border-color: rgba(220,38,38,0.35); background: rgba(220,38,38,0.04); }
}
@keyframes alertGlowPulse {
    0%, 100% { box-shadow: 0 0 8px rgba(220,38,38,0.25), inset 0 0 6px rgba(220,38,38,0.04); }
    50%       { box-shadow: 0 0 28px rgba(220,38,38,0.7), inset 0 0 18px rgba(220,38,38,0.12); }
}
@keyframes alertSlideIn {
    from { transform: translateY(-12px); opacity: 0; }
    to   { transform: translateY(0);     opacity: 1; }
}
@keyframes alertTextFlicker {
    0%, 88%, 100% { opacity: 1;   }
    92%, 96%      { opacity: 0.2; }
}
.alert-banner {
    border: 1px solid #dc2626;
    border-radius: 8px;
    padding: 10px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 14px;
    animation:
        alertFlash 1.2s ease-in-out infinite alternate,
        alertGlowPulse 2.2s ease-in-out infinite,
        alertSlideIn 0.5s ease-out !important;
}
.alert-banner div:first-of-type {
    animation: alertTextFlicker 4s ease-in-out infinite;
}
.notif-item {
    padding: 8px 12px;
    border-radius: 6px;
    margin-bottom: 6px;
    display: flex;
    align-items: flex-start;
    gap: 10px;
    border: 1px solid;
    animation: alertSlideIn 0.35s ease-out;
}

/* ═══════════════════════════════════════
   PHASE 1 — FEATURE 4: RADAR ANIMATION
   ═══════════════════════════════════════ */
@keyframes radarPing {
    0%   { transform: scale(1);   opacity: 0.9; }
    65%  { transform: scale(2.8); opacity: 0.2; }
    100% { transform: scale(3.2); opacity: 0;   }
}
@keyframes radarBlink {
    0%, 100% { opacity: 1;   }
    50%       { opacity: 0.15; }
}
.pulse {
    animation: radarPing 1.8s ease-out infinite !important;
    display: inline-block;
}
.sensor-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    display: inline-block;
    margin-right: 6px;
    animation: radarBlink 2.2s ease-in-out infinite;
}

/* ═══════════════════════════════════════
   TICKER / HEADER / EMERGENCY
   ═══════════════════════════════════════ */
.ticker-wrap {
    overflow: hidden;
    background: #0d0d0d;
    border-bottom: 1px solid #1e0a00;
    border-top: 1px solid #1e0a00;
    padding: 4px 0;
    margin-bottom: 10px;
}
.ticker-inner {
    display: inline-flex;
    gap: 40px;
    white-space: nowrap;
    animation: tickerScroll 30s linear infinite;
}
@keyframes tickerScroll {
    0%   { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}
.ticker-item { font-size: 9px; display: inline-flex; align-items: center; gap: 6px; }

.ebar {
    background: #b91c1c;
    color: white;
    text-align: center;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 0.22em;
    padding: 5px;
    animation: emergencyFlash 0.35s ease-in-out infinite alternate,
               alertGlowPulse 1s ease-in-out infinite;
}
@keyframes emergencyFlash { from{opacity:1} to{opacity:0.45} }

.risk-bar-wrap { margin-bottom: 9px; }
.risk-bar-label { display: flex; justify-content: space-between; margin-bottom: 2px; font-size: 10px; }
.risk-bar-bg { height: 5px; background: #1a0800; border-radius: 3px; overflow: hidden; }
.risk-bar-fill { height: 100%; border-radius: 3px; transition: width 1s ease; }

@keyframes pulseDot {
    0%  { transform: scale(1);   opacity: 0.8; }
    50% { transform: scale(1.6); opacity: 0.3; }
    100%{ transform: scale(1);   opacity: 0.8; }
}

</style>
""", unsafe_allow_html=True)

# ── Static data ─────────────────────────────────────────────────────────────
NOW_MS = int(time.time() * 1000)

QUAKES = [
    {"id":1,  "lat":35.68,  "lng":139.69,  "mag":6.8, "depth":34, "place":"Tokyo, Japan",          "time": NOW_MS-120000,   "type":"major"},
    {"id":2,  "lat":37.77,  "lng":-122.42, "mag":4.2, "depth":12, "place":"San Francisco, CA",     "time": NOW_MS-300000,   "type":"moderate"},
    {"id":3,  "lat":-33.87, "lng":151.21,  "mag":3.1, "depth":8,  "place":"Sydney, Australia",     "time": NOW_MS-600000,   "type":"minor"},
    {"id":4,  "lat":41.90,  "lng":12.50,   "mag":5.5, "depth":22, "place":"Rome, Italy",           "time": NOW_MS-900000,   "type":"moderate"},
    {"id":5,  "lat":-8.41,  "lng":115.19,  "mag":7.2, "depth":55, "place":"Bali, Indonesia",       "time": NOW_MS-1800000,  "type":"major"},
    {"id":6,  "lat":19.43,  "lng":-99.13,  "mag":4.9, "depth":18, "place":"Mexico City, Mexico",   "time": NOW_MS-3600000,  "type":"moderate"},
    {"id":7,  "lat":34.05,  "lng":-118.24, "mag":2.8, "depth":7,  "place":"Los Angeles, CA",       "time": NOW_MS-7200000,  "type":"minor"},
    {"id":8,  "lat":60.17,  "lng":24.94,   "mag":2.1, "depth":5,  "place":"Helsinki, Finland",     "time": NOW_MS-14400000, "type":"minor"},
    {"id":9,  "lat":28.61,  "lng":77.21,   "mag":5.8, "depth":28, "place":"New Delhi, India",      "time": NOW_MS-18000000, "type":"moderate"},
    {"id":10, "lat":-13.16, "lng":-72.54,  "mag":6.1, "depth":38, "place":"Cusco, Peru",           "time": NOW_MS-21600000, "type":"major"},
]

RISK_ZONES = [
    {"region":"Pacific Ring of Fire",  "risk":94, "trend":"+2.3%"},
    {"region":"Himalayan Belt",        "risk":78, "trend":"+1.1%"},
    {"region":"Mediterranean",         "risk":61, "trend":"-0.4%"},
    {"region":"Mid-Atlantic Ridge",    "risk":45, "trend":"+0.8%"},
    {"region":"East African Rift",     "risk":38, "trend":"+3.2%"},
]

SENSORS = [
    {"id":"TKY-01","name":"Tokyo-NIED-01",  "loc":"Tokyo, Japan",         "status":"ONLINE",   "lat":"98.2%"},
    {"id":"CAS-07","name":"USGS-CAS-07",    "loc":"Cascadia Zone, USA",   "status":"ONLINE",   "lat":"99.1%"},
    {"id":"ROM-03","name":"INGV-ROM-03",    "loc":"Rome, Italy",          "status":"ONLINE",   "lat":"97.4%"},
    {"id":"DEL-12","name":"NCS-DEL-12",     "loc":"New Delhi, India",     "status":"DEGRADED", "lat":"71.2%"},
    {"id":"BAL-05","name":"BMKG-BAL-05",    "loc":"Bali, Indonesia",      "status":"ONLINE",   "lat":"99.8%"},
    {"id":"MEX-09","name":"SSN-MEX-09",     "loc":"Mexico City, Mexico",  "status":"DEGRADED", "lat":"63.5%"},
    {"id":"EUR-22","name":"GFZ-EUR-22",     "loc":"Helsinki, Finland",    "status":"ONLINE",   "lat":"98.9%"},
    {"id":"CUS-04","name":"IGP-CUS-04",     "loc":"Cusco, Peru",          "status":"OFFLINE",  "lat":"0.0%"},
    {"id":"LA-14", "name":"USGS-LA-14",     "loc":"Los Angeles, CA",      "status":"ONLINE",   "lat":"97.7%"},
    {"id":"SYD-08","name":"GSB-SYD-08",     "loc":"Sydney, Australia",    "status":"ONLINE",   "lat":"99.0%"},
]

ADMIN_LOG = [
    {"time":"14:32:01","event":"M7.2 earthquake detected — Bali, Indonesia",    "level":"CRITICAL","color":RED},
    {"time":"14:28:44","event":"Tsunami watch issued — Indian Ocean",            "level":"WARNING", "color":ORANGE},
    {"time":"14:15:22","event":"XGBoost model retrained — accuracy 84.3%",      "level":"INFO",    "color":GREEN},
    {"time":"13:58:09","event":"Seismic station offline — Cusco, Peru",         "level":"ALERT",   "color":AMBER},
    {"time":"13:44:33","event":"M6.8 aftershock — Tokyo region",                "level":"SEVERE",  "color":ORANGE},
    {"time":"12:30:00","event":"Daily USGS data sync completed",                 "level":"INFO",    "color":GREEN},
]

MONTHLY_FREQ = [127,98,145,112,167,134,189,203,156,178,142,195]
MONTH_LABELS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
YEARLY_DATA  = [1497,1554,1609,1436,1528,1489,1612,1673,1589,1721]
YEARLY_LABELS= ["2015","2016","2017","2018","2019","2020","2021","2022","2023","2024"]

STRONGEST_RECORDS = [
    {"rank":1,"name":"Great Chilean Earthquake",       "mag":9.5,"year":1960,"deaths":"~5,700"},
    {"rank":2,"name":"Good Friday Earthquake, Alaska", "mag":9.2,"year":1964,"deaths":"~131"},
    {"rank":3,"name":"2004 Indian Ocean Earthquake",   "mag":9.1,"year":2004,"deaths":"~228,000"},
    {"rank":4,"name":"Tōhoku Earthquake, Japan",       "mag":9.0,"year":2011,"deaths":"~20,000"},
    {"rank":5,"name":"Kamchatka Earthquake",           "mag":9.0,"year":1952,"deaths":"~2,336"},
]

# ── Helpers ──────────────────────────────────────────────────────────────────
def mag_color(m):
    if m >= 7:   return RED
    if m >= 5.5: return ORANGE
    if m >= 4:   return AMBER
    if m >= 2.5: return YELLOW
    return GREEN

def mag_label(m):
    if m >= 7:   return "CRITICAL"
    if m >= 5.5: return "SEVERE"
    if m >= 4:   return "HIGH"
    if m >= 2.5: return "MODERATE"
    return "LOW"

def time_ago(ts_ms):
    s = int((time.time() * 1000 - ts_ms) / 1000)
    if s < 60:   return f"{s}s ago"
    if s < 3600: return f"{s//60}m ago"
    return f"{s//3600}h ago"

def calc_risk(mag, depth, freq, accel, tec, hist):
    return min(99, int(mag*8 + (100-depth)*0.2 + freq*4 + accel*20 + tec*0.3 + hist*0.2))

def plotly_dark(margin=None):
    d = dict(
        plot_bgcolor=CARD, paper_bgcolor=CARD,
        font=dict(family="Share Tech Mono, monospace", color=TEXT, size=10),
        xaxis=dict(gridcolor=BORDER, linecolor=BORDER, zerolinecolor=BORDER),
        yaxis=dict(gridcolor=BORDER, linecolor=BORDER, zerolinecolor=BORDER),
    )
    d["margin"] = margin if margin else dict(l=30, r=10, t=30, b=30)
    return d

# ── Session state ────────────────────────────────────────────────────────────
if "chat_history"   not in st.session_state: st.session_state.chat_history   = []
if "notifications"  not in st.session_state: st.session_state.notifications  = [
    {"type":"SYSTEM ONLINE", "msg":"SEISWATCH v3.0 initialized — All sensors nominal",        "color":GREEN,  "time": datetime.now().strftime("%H:%M:%S")},
    {"type":"SEISMIC ALERT", "msg":"M7.2 detected — Bali, Indonesia — Tsunami watch active", "color":RED,    "time": datetime.now().strftime("%H:%M:%S")},
    {"type":"MODEL UPDATE",  "msg":"XGBoost retrained — accuracy 84.3%",                      "color":AMBER,  "time": datetime.now().strftime("%H:%M:%S")},
]
if "siren"          not in st.session_state: st.session_state.siren          = False
if "danger_level"   not in st.session_state: st.session_state.danger_level   = 70
if "selected_quake" not in st.session_state: st.session_state.selected_quake = QUAKES[0]

# ── Header ───────────────────────────────────────────────────────────────────
utc_now    = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
new_notifs = len(st.session_state.notifications)

st.markdown(f"""
<div style="background:#0b0b0b;border-bottom:1px solid #2a1400;padding:10px 0 6px;margin-bottom:0">
  <div style="display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:8px">
    <div style="display:flex;align-items:center;gap:12px">
      <div style="width:36px;height:36px;background:#1a0800;border:1px solid {RED};border-radius:6px;
                  display:flex;align-items:center;justify-content:center;font-size:18px;
                  animation:alertGlowPulse 3s ease-in-out infinite">🌋</div>
      <div>
        <div style="font-size:16px;font-weight:700;letter-spacing:.2em">SEISWATCH</div>
        <div style="font-size:8px;color:#4a2a0a;letter-spacing:.2em">GLOBAL SEISMIC INTELLIGENCE PLATFORM v3.0</div>
      </div>
    </div>
    <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap">
      <span style="padding:3px 10px;border-radius:12px;font-size:8px;font-weight:700;border:1px solid rgba(22,163,74,.3);background:#0a160a;color:{GREEN}">● LIVE</span>
      <span style="padding:3px 10px;border-radius:12px;font-size:8px;font-weight:700;border:1px solid rgba(220,38,38,.3);background:#160a0a;color:{RED}">⚠ 3 ALERTS</span>
      <span style="padding:3px 10px;border-radius:12px;font-size:8px;font-weight:700;border:1px solid #1e0a00;color:#d97706">{new_notifs} NOTIFS</span>
      <span style="padding:3px 10px;border-radius:12px;font-size:8px;border:1px solid #1e0a00;color:#4a2a0a;cursor:default">{utc_now}</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

if st.session_state.siren:
    st.markdown('<div class="ebar">⚠ SEISMIC EMERGENCY ACTIVE — M7.2 DETECTED — BALI, INDONESIA — TSUNAMI WARNING — SEEK HIGH GROUND ⚠</div>', unsafe_allow_html=True)

ticker_items = " ".join([
    f'<span class="ticker-item"><span style="color:{mag_color(q["mag"])};font-weight:700">M{q["mag"]}</span>'
    f'<span style="color:#5a3a1a">{q["place"]}</span>'
    f'<span style="color:#3a2010">{time_ago(q["time"])}</span></span>'
    for q in QUAKES * 2
])
st.markdown(f'<div class="ticker-wrap"><div class="ticker-inner">{ticker_items}</div></div>', unsafe_allow_html=True)

# ── Main tabs ────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "📊 DASHBOARD","🗺️ SEISMIC MAP","🤖 AI PREDICTION","📈 LSTM FORECAST",
    "🌊 DATA VIZ","🚨 EMERGENCY","📉 ANALYTICS","📡 SENSORS",
    "🔔 NOTIFICATIONS","⚙️ ADMIN","💬 SEISMIC AI",
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — DASHBOARD
# ════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    st.markdown(f"""
    <div class="alert-banner">
      <span style="font-size:20px">⚠</span>
      <div style="flex:1">
        <div style="color:{RED};font-size:12px;font-weight:700;letter-spacing:.1em">SEISMIC ALERT — M7.2 DETECTED</div>
        <div style="font-size:10px;margin-top:2px">Bali, Indonesia · Depth 55km · 30min ago · TSUNAMI WATCH ACTIVE</div>
      </div>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Active Events (24h)", "7",      delta="↑ 12%")
    c2.metric("Strongest Today",     "M7.2",   delta="Bali, Indonesia")
    c3.metric("Monitoring Stations", "1,847",  delta="89 countries")
    c4.metric("Evacuation Score",    "72/100", delta="Readiness")

    st.markdown("<br>", unsafe_allow_html=True)

    fc1, fc2, fc3, fc4 = st.columns([2,1,1,1])
    search  = fc1.text_input("🔍 Search location", placeholder="Type city or country...")
    min_mag = fc2.slider("Min Magnitude", 0.0, 7.0, 0.0, 0.5)
    type_f  = fc3.selectbox("Event Type", ["ALL","major","moderate","minor"])
    fc4.markdown("<br>", unsafe_allow_html=True)

    filtered = [
        q for q in QUAKES
        if (not search or search.lower() in q["place"].lower())
        and q["mag"] >= min_mag
        and (type_f == "ALL" or q["type"] == type_f)
    ]

    left, right = st.columns([1.5, 1])

    with left:
        st.markdown('<div class="card-title">RECENT SEISMIC EVENTS</div>', unsafe_allow_html=True)
        if not filtered:
            st.markdown('<div style="color:#3a2010;font-size:11px;padding:14px;text-align:center">No events match filter</div>', unsafe_allow_html=True)
        for q in filtered:
            c = mag_color(q["mag"])
            sel = f"border-color:{c};box-shadow:0 0 10px {c}44;" if st.session_state.selected_quake["id"] == q["id"] else ""
            st.markdown(f"""
            <div class="qrow" style="{sel}">
              <div style="width:38px;height:38px;border-radius:50%;background:{c}18;border:2px solid {c};
                          display:flex;align-items:center;justify-content:center;flex-shrink:0">
                <span style="color:{c};font-size:12px;font-weight:800">{q["mag"]}</span>
              </div>
              <div style="flex:1;min-width:0">
                <div style="font-size:11px;font-weight:600;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{q["place"]}</div>
                <div style="font-size:9px;color:#5a3a1a;margin-top:1px">Depth: {q["depth"]}km · {time_ago(q["time"])}</div>
              </div>
              <div style="text-align:right;flex-shrink:0">
                <div style="color:{c};font-size:8px;font-weight:700">{mag_label(q["mag"])}</div>
                <div class="pulse" style="width:7px;height:7px;border-radius:50%;background:{c};display:inline-block"></div>
              </div>
            </div>""", unsafe_allow_html=True)

    with right:
        q = st.session_state.selected_quake
        c = mag_color(q["mag"])
        glow_cls = "glow-red" if q["mag"]>=7 else "glow-orange" if q["mag"]>=5.5 else "glow-amber"
        st.markdown(f"""
        <div class="card {glow_cls}" style="border-color:{c}55">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:10px">
            <div>
              <div style="color:{c};font-size:40px;font-weight:800;line-height:1">M{q["mag"]}</div>
              <div style="color:{c};font-size:10px;font-weight:700">{mag_label(q["mag"])}</div>
            </div>
            <div class="pulse" style="width:12px;height:12px;border-radius:50%;background:{c};margin-top:4px"></div>
          </div>
          <div style="font-size:13px;font-weight:600;margin-bottom:8px">{q["place"]}</div>
          <div style="font-size:10px">
            <div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #1a0800">
              <span style="color:#5a3a1a">Depth</span><span style="font-weight:600">{q["depth"]} km</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #1a0800">
              <span style="color:#5a3a1a">Coordinates</span><span style="font-weight:600">{q["lat"]}°, {q["lng"]}°</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #1a0800">
              <span style="color:#5a3a1a">Occurred</span><span style="font-weight:600">{time_ago(q["time"])}</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:4px 0;border-bottom:1px solid #1a0800">
              <span style="color:#5a3a1a">Tsunami Risk</span>
              <span style="font-weight:600;color:{'#dc2626' if q['mag']>=7 else '#16a34a'}">{'POSSIBLE' if q['mag']>=7 else 'LOW'}</span>
            </div>
            <div style="display:flex;justify-content:space-between;padding:4px 0">
              <span style="color:#5a3a1a">Aftershock</span>
              <span style="font-weight:600;color:{ORANGE}">{'HIGH (68%)' if q['mag']>=6 else 'MOD (34%)' if q['mag']>=4 else 'LOW (12%)'}</span>
            </div>
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown('<div class="card-title" style="margin-top:8px">P-WAVE SIGNATURE</div>', unsafe_allow_html=True)
        xs = list(range(100))
        # PHASE 1 FEATURE 5: moving wave with time offset
        t_off = (time.time() % 100) * 0.5
        wave_y = [math.sin(i*0.5 + t_off)*14 + math.sin(i*1.3 + t_off*0.7)*6 + random.gauss(0,2.5) for i in xs]
        fig_w = go.Figure(go.Scatter(x=xs, y=wave_y, mode="lines",
                          line=dict(color=c, width=1.5), fill="tozeroy",
                          fillcolor=f"rgba({int(c[1:3],16)},{int(c[3:5],16)},{int(c[5:7],16)},0.06)"))
        fig_w.add_hline(y=0, line_color=BORDER, line_width=0.5, line_dash="dot")
        fig_w.update_layout(
            **{k:v for k,v in plotly_dark(margin=dict(l=0,r=0,t=4,b=4)).items() if k not in ("xaxis","yaxis")},
            height=90, showlegend=False,
            xaxis=dict(visible=False), yaxis=dict(visible=False))
        st.plotly_chart(fig_w, width='stretch', config={"displayModeBar":False})

        st.markdown('<div class="card-title" style="margin-top:4px">REGIONAL RISK INDEX</div>', unsafe_allow_html=True)
        for z in RISK_ZONES:
            rc = RED if z["risk"]>80 else ORANGE if z["risk"]>60 else AMBER if z["risk"]>40 else YELLOW
            tu = z["trend"].startswith("+")
            st.markdown(f"""
            <div class="risk-bar-wrap">
              <div class="risk-bar-label">
                <span style="font-size:10px">{z["region"]}</span>
                <div style="display:flex;gap:8px">
                  <span style="color:{'#dc2626' if tu else '#16a34a'};font-size:9px">{z["trend"]}</span>
                  <span style="color:{rc};font-weight:700;font-size:11px">{z["risk"]}%</span>
                </div>
              </div>
              <div class="risk-bar-bg"><div class="risk-bar-fill" style="width:{z['risk']}%;background:{rc}"></div></div>
            </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — SEISMIC MAP
# ════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    st.markdown('<div class="card-title">GLOBAL SEISMIC ACTIVITY — REAL-TIME</div>', unsafe_allow_html=True)
    fig_map = go.Figure()
    fault_lats = [25,35,45,55,60,55,45,None,-10,-5,0,5,10,None,30,25,20,15]
    fault_lons = [120,130,140,150,160,170,180,None,-80,-75,-70,-65,-60,None,-110,-105,-100,-95]
    fig_map.add_trace(go.Scattergeo(lat=fault_lats, lon=fault_lons, mode="lines",
        line=dict(color="rgba(255,68,0,0.4)", width=1, dash="dash"), showlegend=False))
    for q in QUAKES:
        c = mag_color(q["mag"])
        fig_map.add_trace(go.Scattergeo(lat=[q["lat"]], lon=[q["lng"]], mode="markers",
            marker=dict(size=max(8,q["mag"]*4), color=c, opacity=0.85, line=dict(color="white",width=0.8)),
            text=f"M{q['mag']} — {mag_label(q['mag'])}<br>{q['place']}<br>Depth: {q['depth']}km · {time_ago(q['time'])}",
            hovertemplate="%{text}<extra></extra>", showlegend=False))
        fig_map.add_trace(go.Scattergeo(lat=[q["lat"]], lon=[q["lng"]], mode="markers",
            marker=dict(size=max(8,q["mag"]*4)+8, color="rgba(0,0,0,0)", line=dict(color=c,width=1.2)),
            showlegend=False, hoverinfo="skip"))
    fig_map.update_geos(projection_type="natural earth",
        showland=True, landcolor="#0c1a0c", showocean=True, oceancolor="#06100a",
        showcoastlines=True, coastlinecolor="#142014", coastlinewidth=0.6,
        showframe=False, bgcolor=CARD, showlakes=False, showrivers=False,
        showcountries=True, countrycolor="#1a2a1a", countrywidth=0.3)
    fig_map.update_layout(
        **{k:v for k,v in plotly_dark(margin=dict(l=0,r=0,t=0,b=0)).items() if k not in ("xaxis","yaxis")},
        height=440, geo=dict(bgcolor=CARD))
    st.plotly_chart(fig_map, width='stretch', config={"displayModeBar":False})
    lcols = st.columns(4)
    for i,(lbl,col) in enumerate([("LOW <2.5",GREEN),("MOD 2.5-4",YELLOW),("HIGH 4-5.5",ORANGE),("CRIT 7+",RED)]):
        lcols[i].markdown(f'<div style="padding:4px 8px;border:1px solid {col}44;border-radius:10px;color:{col};font-size:9px;font-weight:700;text-align:center">● {lbl}</div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    qcols = st.columns(4)
    for i,q in enumerate(QUAKES[:4]):
        c = mag_color(q["mag"])
        qcols[i].markdown(f"""
        <div style="background:#0f0f0f;border:1px solid {c}33;border-radius:7px;padding:10px 12px;transition:box-shadow 0.3s">
          <div style="color:{c};font-weight:800;font-size:18px">M{q["mag"]}</div>
          <div style="font-size:11px;margin-top:2px">{q["place"].split(",")[0]}</div>
          <div style="color:#5a3a1a;font-size:9px;margin-top:1px">{time_ago(q["time"])}</div>
        </div>""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — AI PREDICTION
# ════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    st.markdown('<div style="color:#2a1200;font-size:9px;margin-bottom:12px">Random Forest + XGBoost Ensemble · USGS 1900–2024 · 847,293 events</div>', unsafe_allow_html=True)
    p1, p2 = st.columns(2)
    with p1:
        st.markdown('<div class="card-title">INPUT PARAMETERS</div>', unsafe_allow_html=True)
        mag_p  = st.slider("Magnitude (Mw)",      1.0, 9.0,  5.0, 0.1,  key="pmag")
        dep_p  = st.slider("Depth (km)",           1,   150,  20,  1,    key="pdep")
        freq_p = st.slider("Vibration Freq (Hz)",  0.1, 20.0, 3.5, 0.1,  key="pfreq")
        acc_p  = st.slider("Ground Accel (g)",     0.0, 2.0,  0.4, 0.01, key="pacc")
        tec_p  = st.slider("Tectonic Stress (%)",  0,   100,  65,  1,    key="ptec")
        hist_p = st.slider("Historical Rate (%)",  0,   100,  45,  1,    key="phist")
        run_pred = st.button("▶ RUN PREDICTION MODEL", use_container_width=True)
    with p2:
        st.markdown('<div class="card-title">PREDICTION OUTPUT</div>', unsafe_allow_html=True)
        if run_pred:
            with st.spinner("Running ML pipeline..."):
                time.sleep(1.6)
            risk   = calc_risk(mag_p, dep_p, freq_p, acc_p, tec_p, hist_p)
            aft    = min(95, int(risk*0.68+15))
            conf   = random.randint(72, 92)
            intens = "VIII–IX" if mag_p>=7 else "VI–VII" if mag_p>=5.5 else "IV–V" if mag_p>=4 else "II–III"
            rad    = int(mag_p*12)
            rc     = RED if risk>75 else ORANGE if risk>50 else AMBER
            rl     = "HIGH DANGER" if risk>75 else "ELEVATED RISK" if risk>50 else "MODERATE RISK"
            fig_g  = go.Figure(go.Indicator(
                mode="gauge+number", value=risk,
                title=dict(text="RISK PROBABILITY %", font=dict(color=MUTED, size=10, family="Share Tech Mono")),
                gauge=dict(axis=dict(range=[0,100], tickcolor=MUTED, tickfont=dict(size=8,color=MUTED)),
                           bar=dict(color=rc, thickness=0.7), bgcolor=BORDER, borderwidth=0,
                           steps=[dict(range=[0,40],color="#0a0800"),dict(range=[40,70],color="#100800"),dict(range=[70,100],color="#180800")],
                           threshold=dict(line=dict(color=RED,width=3), thickness=0.8, value=risk)),
                number=dict(font=dict(color=rc, size=44, family="Share Tech Mono"), suffix="%")))
            fig_g.update_layout(**{k:v for k,v in plotly_dark(margin=dict(l=20,r=20,t=30,b=10)).items() if k not in ("xaxis","yaxis")}, height=220)
            st.plotly_chart(fig_g, width='stretch', config={"displayModeBar":False})
            st.markdown(f'<div style="text-align:center;color:{rc};font-size:13px;font-weight:700;margin-bottom:10px">{rl}</div>', unsafe_allow_html=True)
            for label,val,col in [("Aftershock Probability",f"{aft}%",ORANGE),("Model Confidence",f"{conf}%",AMBER),("Predicted Intensity",intens,YELLOW),("Impact Radius",f"{rad} km",TEXT)]:
                st.markdown(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:6px 10px;background:#0a0a0a;border-radius:4px;margin-bottom:3px;border:1px solid #1e0a00;font-size:11px"><span style="color:#5a3a1a">{label}</span><span style="color:{col};font-weight:700">{val}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div style="padding:7px 10px;background:#0d0900;border-radius:5px;margin-top:7px;border:1px solid #2a1400"><div style="color:{RED};font-size:9px;font-weight:700">ML: Random Forest + XGBoost Ensemble</div><div style="color:#2a1400;font-size:8px;margin-top:2px">USGS 1900–2024 · 847,293 events · Accuracy: 84.3%</div></div>', unsafe_allow_html=True)
            st.session_state.notifications.insert(0,{"type":"PREDICTION RUN","msg":f"Risk model scored {risk}% — {rl}","color":ORANGE,"time":datetime.now().strftime("%H:%M:%S")})
        else:
            st.markdown('<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:240px;gap:10px"><div style="font-size:34px;color:#2a1200">⚡</div><div style="color:#4a2a0a;font-size:12px;text-align:center">Configure parameters and run the model</div></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — LSTM FORECAST
# ════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown('<div style="color:#2a1200;font-size:9px;margin-bottom:10px">LSTM Neural Network · 3-layer stacked · 30-day lookback · Simulated forecast</div>', unsafe_allow_html=True)
    regen    = st.button("↺ REGENERATE FORECAST")
    seed_val = int(time.time()) if regen else 42
    rng      = np.random.default_rng(seed_val)
    base_mags= [3.8,4.1,3.6,5.2,4.8,4.3,5.9,6.1,5.4,4.9,5.3,5.8,6.2,5.7]
    jitter   = rng.uniform(-0.3, 0.3, 14)
    base     = [round(max(1.5,min(9.0,b+j)),2) for b,j in zip(base_mags,jitter)]
    upper    = [round(b+0.8,2) for b in base]
    lower    = [round(max(1.0,b-0.7),2) for b in base]
    days     = [(datetime.now()+timedelta(days=i)).strftime("%b %d") for i in range(14)]
    fig_lstm = go.Figure()
    fig_lstm.add_trace(go.Scatter(x=days,y=upper,fill=None,mode="lines",line=dict(color="rgba(217,119,6,0.3)",width=1,dash="dot"),showlegend=False))
    fig_lstm.add_trace(go.Scatter(x=days,y=lower,fill="tonexty",mode="lines",line=dict(color="rgba(217,119,6,0.3)",width=1,dash="dot"),fillcolor="rgba(217,119,6,0.08)",name="Confidence Band"))
    fig_lstm.add_trace(go.Scatter(x=days,y=base,mode="lines+markers",line=dict(color=ORANGE,width=2.5),marker=dict(color=ORANGE,size=6),name="Predicted Magnitude"))
    fig_lstm.add_hline(y=6.0,line_color=RED,line_width=1.5,line_dash="dash",annotation_text="Alert Threshold M6.0",annotation_font_color=RED,annotation_font_size=9)
    # PHASE 1 FEATURE 5: animated transition
    fig_lstm.update_layout(**plotly_dark(), height=280,
        legend=dict(font=dict(size=9,color=MUTED)),
        transition=dict(duration=800, easing="cubic-in-out"))
    st.plotly_chart(fig_lstm, width='stretch', config={"displayModeBar":False})
    s1, s2 = st.columns(2)
    with s1:
        st.markdown('<div class="card-title">FORECAST SUMMARY</div>', unsafe_allow_html=True)
        breach = sum(1 for b in base if b >= 6.0)
        for k,v,c in [("Peak Forecast",f"M{max(base):.1f}",RED),("Forecast Window","14 days",TEXT),("Model Confidence","79%",AMBER),("Threshold Breach",f"{breach} days",ORANGE),("LSTM Layers","3 stacked",TEXT),("Lookback Window","30 days",TEXT)]:
            st.markdown(f'<div style="display:flex;justify-content:space-between;padding:5px 0;border-bottom:1px solid #1a0800;font-size:10px"><span style="color:#5a3a1a">{k}</span><span style="color:{c};font-weight:700">{v}</span></div>', unsafe_allow_html=True)
    with s2:
        st.markdown('<div class="card-title">MODEL ARCHITECTURE</div>', unsafe_allow_html=True)
        for k,v in [("Input Layer","30-day window, 6 features"),("LSTM Layer 1","128 units, dropout 0.2"),("LSTM Layer 2","64 units, dropout 0.2"),("LSTM Layer 3","32 units"),("Dense Layer","16 units, ReLU"),("Output Layer","1 unit, Linear"),("Optimizer","Adam, lr=0.001"),("Loss Fn","Mean Squared Error")]:
            st.markdown(f'<div style="display:flex;gap:8px;font-size:9px;margin-bottom:2px"><span style="color:#3a2010;width:90px;flex-shrink:0">{k}</span><span style="color:#a07040">{v}</span></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — DATA VIZ
# ════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    # PHASE 1 FEATURE 5: auto-refresh toggle for moving waves
    viz_refresh = st.toggle("⟳ Auto-refresh waves (live motion)", value=False, key="viz_autorefresh")

    v1, v2 = st.columns(2)
    with v1:
        st.markdown('<div class="card-title">LIVE P-WAVE / S-WAVE MONITOR</div>', unsafe_allow_html=True)
        xs    = list(range(80))
        # Time-offset makes wave shift on each render
        t_off = (time.time() % 100) * 0.5
        p_wave = [math.sin(i*0.4 + t_off)*25 + math.sin(i*0.9 + t_off*0.7)*12 + random.gauss(0,4) for i in xs]
        s_wave = [math.cos(i*0.25 + t_off)*18 + math.sin(i*0.6 + t_off*0.5)*9 + random.gauss(0,3) for i in xs]
        fig_w2 = go.Figure()
        fig_w2.add_trace(go.Scatter(x=xs,y=p_wave,mode="lines",name="P-Wave",line=dict(color=ORANGE,width=1.8)))
        fig_w2.add_trace(go.Scatter(x=xs,y=s_wave,mode="lines",name="S-Wave",line=dict(color=YELLOW,width=1.8,dash="dot")))
        fig_w2.update_layout(**plotly_dark(), height=170,
            legend=dict(font=dict(size=9,color=MUTED),orientation="h",y=1.1),
            transition=dict(duration=500, easing="linear"))
        st.plotly_chart(fig_w2, width='stretch', config={"displayModeBar":False})
    with v2:
        st.markdown('<div class="card-title">MAGNITUDE VS DEPTH SCATTER</div>', unsafe_allow_html=True)
        fig_sc = go.Figure()
        for q in QUAKES:
            c = mag_color(q["mag"])
            fig_sc.add_trace(go.Scatter(x=[q["depth"]],y=[q["mag"]],mode="markers",
                marker=dict(size=q["mag"]*3.5,color=c,opacity=0.85,line=dict(color=BORDER,width=1)),
                text=f"M{q['mag']} @ {q['depth']}km — {q['place']}",
                hovertemplate="%{text}<extra></extra>",showlegend=False))
        fig_sc.update_layout(**{k:v for k,v in plotly_dark().items() if k not in ("xaxis","yaxis")},height=170,
            xaxis=dict(title="Depth (km)",gridcolor=BORDER,linecolor=BORDER),
            yaxis=dict(title="Magnitude",gridcolor=BORDER,linecolor=BORDER,range=[1,8]))
        st.plotly_chart(fig_sc, width='stretch', config={"displayModeBar":False})

    st.markdown('<div class="card-title" style="margin-top:4px">TECTONIC PRESSURE GAUGES — MAJOR PLATES</div>', unsafe_allow_html=True)
    plates = [("Pacific Plate",84,RED),("Eurasian Plate",52,ORANGE),("Indo-Australian",71,AMBER),("North American",39,YELLOW)]
    gcols  = st.columns(4)
    for i,(name,pres,col) in enumerate(plates):
        fig_g2 = go.Figure(go.Indicator(mode="gauge+number",value=pres,
            title=dict(text=name,font=dict(color=MUTED,size=8,family="Share Tech Mono")),
            number=dict(font=dict(color=col,size=20,family="Share Tech Mono"),suffix=" MPa"),
            gauge=dict(axis=dict(range=[0,100],tickfont=dict(size=7,color=MUTED)),
                       bar=dict(color=col,thickness=0.7),bgcolor=BORDER,borderwidth=0)))
        fig_g2.update_layout(**{k:v for k,v in plotly_dark(margin=dict(l=10,r=10,t=20,b=10)).items() if k not in ("xaxis","yaxis")},height=140)
        gcols[i].plotly_chart(fig_g2, width='stretch', config={"displayModeBar":False})

    st.markdown('<div class="card-title">TREMOR HISTORY TIMELINE (LAST 72H)</div>', unsafe_allow_html=True)
    for ts,m,place in [(NOW_MS-600000,2.1,"Pacific Ocean"),(NOW_MS-1800000,4.3,"Japan Trench"),(NOW_MS-3600000,3.7,"Cascadia Zone"),(NOW_MS-7200000,5.9,"Andes, Peru"),(NOW_MS-10800000,2.4,"Iceland Ridge"),(NOW_MS-14400000,6.8,"Tokyo, Japan"),(NOW_MS-21600000,3.2,"Turkey Fault"),(NOW_MS-43200000,5.1,"Philippines Sea")]:
        c = mag_color(m)
        st.markdown(f'<div style="display:flex;align-items:center;gap:10px;padding:5px 0;border-bottom:1px solid #1a0800;font-size:10px"><div style="width:8px;height:8px;border-radius:50%;background:{c};flex-shrink:0"></div><div style="color:#5a3a1a;width:60px">{time_ago(ts)}</div><div style="color:{c};font-weight:700;width:34px">M{m}</div><div style="flex:1">{place}</div><div style="color:{c};font-size:9px;width:70px">{mag_label(m)}</div></div>', unsafe_allow_html=True)

    st.markdown('<div class="card-title" style="margin-top:10px">FREQUENCY SPECTRUM ANALYSIS (0–20 HZ)</div>', unsafe_allow_html=True)
    freqs  = list(range(1,21))
    amps   = [math.exp(-f*0.18)*40 + random.gauss(0,4) + math.sin(f*0.8)*5 for f in freqs]
    cols_f = [RED if f<5 else ORANGE if f<10 else AMBER if f<15 else DIM for f in freqs]
    fig_f  = go.Figure(go.Bar(x=[f"{f}Hz" for f in freqs],y=amps,marker_color=cols_f))
    fig_f.update_layout(**plotly_dark(margin=dict(l=20,r=10,t=10,b=30)),height=150,showlegend=False)
    st.plotly_chart(fig_f, width='stretch', config={"displayModeBar":False})

    st.markdown('<div style="color:#3a2010;font-size:8px;text-align:right;margin-top:4px">● LIVE DATA — toggle auto-refresh above for continuous motion</div>', unsafe_allow_html=True)
    if viz_refresh:
        time.sleep(2)
        st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# TAB 6 — EMERGENCY
# ════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    e1, e2 = st.columns(2)
    with e1:
        st.markdown('<div class="card-title">DANGER LEVEL GAUGE</div>', unsafe_allow_html=True)
        danger = st.slider("Danger Level", 0, 100, st.session_state.danger_level, key="danger_slider")
        st.session_state.danger_level = danger
        dc = RED if danger>75 else ORANGE if danger>50 else AMBER
        fig_dg = go.Figure(go.Indicator(mode="gauge+number",value=danger,
            title=dict(text="DANGER LEVEL",font=dict(color=MUTED,size=10,family="Share Tech Mono")),
            number=dict(font=dict(color=dc,size=40,family="Share Tech Mono"),suffix="%"),
            gauge=dict(axis=dict(range=[0,100],tickfont=dict(size=8,color=MUTED)),
                       bar=dict(color=dc,thickness=0.75),bgcolor=BORDER,borderwidth=0,
                       steps=[dict(range=[0,40],color="#0a0800"),dict(range=[40,70],color="#100800"),dict(range=[70,100],color="#180800")])))
        fig_dg.update_layout(**{k:v for k,v in plotly_dark(margin=dict(l=20,r=20,t=30,b=10)).items() if k not in ("xaxis","yaxis")},height=240)
        st.plotly_chart(fig_dg, width='stretch', config={"displayModeBar":False})
        st.markdown('<div class="card-title" style="margin-top:6px">VOICE ALERT BROADCAST</div>', unsafe_allow_html=True)
        bc1,bc2,bc3 = st.columns(3)
        if bc1.button("🔴 M7+ WARN"):  st.warning("MAGNITUDE 7+ EARTHQUAKE DETECTED. SEEK SHELTER IMMEDIATELY. TSUNAMI WARNING IN EFFECT.")
        if bc2.button("🟠 M5+ ALERT"): st.warning("MODERATE EARTHQUAKE DETECTED. REMAIN ALERT. AFTERSHOCKS POSSIBLE.")
        if bc3.button("🟢 ALL CLEAR"): st.success("ALL CLEAR. SEISMIC ACTIVITY HAS SUBSIDED. RESUME NORMAL OPERATIONS.")
        st.markdown('<div class="card-title" style="margin-top:10px">SIREN SYSTEM</div>', unsafe_allow_html=True)
        siren_toggle = st.toggle("Activate Emergency Siren", value=st.session_state.siren)
        if siren_toggle != st.session_state.siren:
            st.session_state.siren = siren_toggle
            st.rerun()
        if st.session_state.siren:
            st.markdown(f'<div style="color:{RED};font-size:11px;font-weight:700">🔴 SIREN ACTIVE — BROADCASTING EMERGENCY ALERTS</div>', unsafe_allow_html=True)
    with e2:
        st.markdown('<div class="card-title">EVACUATION READINESS SCORE</div>', unsafe_allow_html=True)
        fig_ev = go.Figure(go.Indicator(mode="gauge+number",value=70,
            title=dict(text="READINESS SCORE",font=dict(color=MUTED,size=10,family="Share Tech Mono")),
            number=dict(font=dict(color=AMBER,size=40,family="Share Tech Mono"),suffix="/100"),
            gauge=dict(axis=dict(range=[0,100],tickfont=dict(size=8,color=MUTED)),
                       bar=dict(color=AMBER,thickness=0.75),bgcolor=BORDER,borderwidth=0)))
        fig_ev.update_layout(**{k:v for k,v in plotly_dark(margin=dict(l=20,r=20,t=30,b=10)).items() if k not in ("xaxis","yaxis")},height=200)
        st.plotly_chart(fig_ev, width='stretch', config={"displayModeBar":False})
        ec1,ec2 = st.columns(2)
        for col,(lbl,val,col2) in zip([ec1,ec2,ec1,ec2],[("Routes Clear","84%",GREEN),("Shelters Ready","61%",AMBER),("Comms Active","92%",GREEN),("Med Units","47%",ORANGE)]):
            col.markdown(f'<div style="background:#0a0a0a;border:1px solid #1e0a00;border-radius:5px;padding:8px;text-align:center;margin-bottom:6px"><div style="color:#5a3a1a;font-size:9px">{lbl}</div><div style="color:{col2};font-weight:700;font-size:15px">{val}</div></div>', unsafe_allow_html=True)
        st.markdown('<div class="card-title" style="margin-top:8px">ACTIVE ALERT ZONES</div>', unsafe_allow_html=True)
        for name,level,mag,c,t in [("Bali, Indonesia","CRITICAL",7.2,RED,"30m ago"),("Tokyo, Japan","SEVERE",6.8,ORANGE,"2h ago"),("New Delhi, India","HIGH",5.8,AMBER,"5h ago"),("Rome, Italy","MODERATE",5.5,YELLOW,"15m ago")]:
            st.markdown(f'<div style="display:flex;align-items:center;gap:8px;padding:7px 10px;background:{c}10;border:1px solid {c}44;border-radius:5px;margin-bottom:5px"><div class="pulse" style="width:9px;height:9px;border-radius:50%;background:{c};flex-shrink:0"></div><div style="flex:1"><div style="font-size:10px;font-weight:600">{name}</div><div style="font-size:9px;color:#5a3a1a">M{mag} · {t}</div></div><span style="color:{c};font-size:8px;font-weight:700;border:1px solid {c};border-radius:3px;padding:2px 6px">{level}</span></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════════════
# TAB 7 — ANALYTICS
# ════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    a1,a2,a3 = st.columns(3)
    a1.metric("Strongest Recorded","M9.5",   delta="Valdivia, Chile 1960")
    a2.metric("Annual Avg M5+",    "1,500",  delta="Global estimate")
    a3.metric("Active Fault Lines","312",    delta="Currently monitored")
    st.markdown("<br>", unsafe_allow_html=True)
    an1,an2 = st.columns(2)
    with an1:
        st.markdown('<div class="card-title">MONTHLY FREQUENCY 2024</div>', unsafe_allow_html=True)
        fig_mf = go.Figure(go.Bar(x=MONTH_LABELS,y=MONTHLY_FREQ,
            marker_color=[RED if v>190 else ORANGE if v>160 else AMBER if v>130 else YELLOW for v in MONTHLY_FREQ],
            text=MONTHLY_FREQ,textposition="outside",textfont=dict(size=8,color=MUTED)))
        # PHASE 1 FEATURE 5: animated transition
        fig_mf.update_layout(**plotly_dark(),height=220,showlegend=False,
            transition=dict(duration=600, easing="cubic-in-out"))
        st.plotly_chart(fig_mf, width='stretch', config={"displayModeBar":False})
    with an2:
        st.markdown('<div class="card-title">YEARLY TREND 2015–2024</div>', unsafe_allow_html=True)
        fig_yt = go.Figure(go.Scatter(x=YEARLY_LABELS,y=YEARLY_DATA,mode="lines+markers",
            line=dict(color=ORANGE,width=2.5),marker=dict(color=ORANGE,size=6),
            fill="tozeroy",fillcolor="rgba(234,88,12,0.08)"))
        # PHASE 1 FEATURE 5: animated transition
        fig_yt.update_layout(**plotly_dark(),height=220,
            transition=dict(duration=700, easing="cubic-in-out"))
        st.plotly_chart(fig_yt, width='stretch', config={"displayModeBar":False})
    an3,an4 = st.columns(2)
    with an3:
        st.markdown('<div class="card-title">REGION-WISE COMPARISON</div>', unsafe_allow_html=True)
        fig_rb = go.Figure(go.Bar(y=["Pacific Ring","Himalayan","Mediterr.","Atlantic","E. Africa"],
            x=[890,342,218,165,134],orientation="h",marker_color=[RED,ORANGE,AMBER,YELLOW,"#ca8a04"],
            text=[890,342,218,165,134],textposition="outside",textfont=dict(size=9,color=MUTED)))
        fig_rb.update_layout(**{k:v for k,v in plotly_dark().items() if k not in ("xaxis","yaxis")},height=230,showlegend=False,
            xaxis=dict(gridcolor=BORDER,linecolor=BORDER),
            yaxis=dict(tickfont=dict(color=MUTED),gridcolor=BORDER,linecolor=BORDER))
        st.plotly_chart(fig_rb, width='stretch', config={"displayModeBar":False})
    with an4:
        st.markdown('<div class="card-title">PREDICTIVE HEAT ZONES</div>', unsafe_allow_html=True)
        hdata = np.random.default_rng(7).integers(10,100,size=(5,6))
        fig_hm = go.Figure(go.Heatmap(z=hdata,x=["Jan","Mar","May","Jul","Sep","Nov"],
            y=["Pacific","Himalaya","Mediterr.","Atlantic","E.Africa"],
            colorscale=[[0,"#0a1a0a"],[0.25,"#eab308"],[0.6,"#ea580c"],[1,"#dc2626"]],
            showscale=False,text=hdata,texttemplate="%{text}",textfont=dict(size=8,color=TEXT)))
        fig_hm.update_layout(**{k:v for k,v in plotly_dark().items() if k not in ("xaxis","yaxis")},height=230,
            xaxis=dict(tickfont=dict(size=9,color=MUTED),gridcolor=BORDER),
            yaxis=dict(tickfont=dict(size=9,color=MUTED),gridcolor=BORDER))
        st.plotly_chart(fig_hm, width='stretch', config={"displayModeBar":False})
    st.markdown('<div class="card-title">STRONGEST RECORDED EVENTS</div>', unsafe_allow_html=True)
    df_rec = pd.DataFrame(STRONGEST_RECORDS)
    df_rec["mag"] = df_rec["mag"].apply(lambda m: f"M{m}")
    df_rec.columns = ["Rank","Event","Magnitude","Year","Deaths"]
    st.dataframe(df_rec.set_index("Rank"),use_container_width=True,
        column_config={"Magnitude":st.column_config.TextColumn(width="small"),"Deaths":st.column_config.TextColumn(width="medium")})

# ════════════════════════════════════════════════════════════════════════════
# TAB 8 — SENSORS
# ════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    ss1,ss2,ss3,ss4 = st.columns(4)
    ss1.metric("Total Stations","1,847")
    ss2.metric("Online","1,743",delta="94.4%")
    ss3.metric("Degraded","68",delta="-3.7%")
    ss4.metric("Offline","36",delta="-1.9%")
    st.markdown("<br>", unsafe_allow_html=True)
    sl,sr = st.columns([1.4,1])
    with sl:
        st.markdown('<div class="card-title">STATION STATUS LOG</div>', unsafe_allow_html=True)
        sc = {"ONLINE":GREEN,"DEGRADED":YELLOW,"OFFLINE":RED}
        for s in SENSORS:
            c = sc.get(s["status"],MUTED)
            st.markdown(f'<div style="display:flex;align-items:center;gap:8px;padding:6px 0;border-bottom:1px solid #1a0800;font-size:10px"><span class="sensor-dot" style="background:{c}"></span><div style="flex:1"><div style="font-weight:700;font-size:10px">{s["name"]}</div><div style="color:#5a3a1a;font-size:9px">{s["loc"]}</div></div><div style="text-align:right"><div style="color:{c};font-size:9px;font-weight:700">{s["status"]}</div><div style="color:#3a2010;font-size:8px">{s["lat"]}</div></div></div>', unsafe_allow_html=True)
    with sr:
        st.markdown('<div class="card-title">NETWORK COVERAGE</div>', unsafe_allow_html=True)
        fig_pie = go.Figure(go.Pie(labels=["Online","Degraded","Offline"],values=[1743,68,36],hole=0.65,
            marker=dict(colors=[GREEN,YELLOW,RED],line=dict(color=CARD,width=2)),textinfo="none"))
        fig_pie.update_layout(**{k:v for k,v in plotly_dark().items() if k not in ("xaxis","yaxis")},height=240,showlegend=True,
            legend=dict(font=dict(size=9,color=MUTED),orientation="h",y=-0.05))
        st.plotly_chart(fig_pie, width='stretch', config={"displayModeBar":False})

# ════════════════════════════════════════════════════════════════════════════
# TAB 9 — NOTIFICATIONS
# ════════════════════════════════════════════════════════════════════════════
with tabs[8]:
    nc1,nc2 = st.columns([3,1])
    nc1.markdown('<div class="card-title">NOTIFICATION CENTER</div>', unsafe_allow_html=True)
    with nc2:
        if st.button("CLEAR ALL",key="clear_notifs"):
            st.session_state.notifications = []
            st.rerun()
        if st.button("+ TEST ALERT",key="test_notif"):
            st.session_state.notifications.insert(0,{"type":"TEST ALERT","msg":"Simulated M5.3 event — Test Region","color":ORANGE,"time":datetime.now().strftime("%H:%M:%S")})
            st.rerun()
    if not st.session_state.notifications:
        st.markdown('<div style="color:#3a2010;text-align:center;padding:24px;font-size:11px">No notifications</div>', unsafe_allow_html=True)
    else:
        for i,n in enumerate(st.session_state.notifications):
            c = n["color"]
            cols = st.columns([12,1])
            with cols[0]:
                st.markdown(f'<div class="notif-item" style="border-color:{c}44;background:{c}10"><div style="width:8px;height:8px;border-radius:50%;background:{c};flex-shrink:0;margin-top:3px"></div><div style="flex:1"><div style="color:{c};font-size:9px;font-weight:700">{n["type"]}</div><div style="font-size:10px;margin-top:1px">{n["msg"]}</div><div style="color:#5a3a1a;font-size:8px;margin-top:1px">{n["time"]}</div></div></div>', unsafe_allow_html=True)
            with cols[1]:
                if st.button("✕",key=f"dn_{i}"):
                    st.session_state.notifications.pop(i)
                    st.rerun()

# ════════════════════════════════════════════════════════════════════════════
# TAB 10 — ADMIN
# ════════════════════════════════════════════════════════════════════════════
with tabs[9]:
    adm_c1,adm_c2 = st.columns([3,1])
    adm_c1.markdown('<div class="card-title">ADMIN ANALYTICS PANEL</div>', unsafe_allow_html=True)
    with adm_c2:
        report_lines = ["SEISWATCH SEISMIC INTELLIGENCE REPORT",f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}","","=== ACTIVE EVENTS ===",*[f"M{q['mag']} | {q['place']} | Depth {q['depth']}km | {time_ago(q['time'])}" for q in QUAKES],"","=== RISK ZONES ===",*[f"{z['region']}: {z['risk']}% ({z['trend']})" for z in RISK_ZONES],"","=== ML MODEL STATUS ===","Random Forest: 82% accuracy","XGBoost: 86% accuracy","LSTM: 78% accuracy","","NOTE: For demonstration purposes only."]
        st.download_button("⬇ REPORT","\n".join(report_lines),file_name=f"seiswatch_report_{int(time.time())}.txt",mime="text/plain",use_container_width=True)
        buf = io.StringIO()
        writer = csv.DictWriter(buf,fieldnames=["id","mag","depth","place","lat","lng","time","type"])
        writer.writeheader()
        writer.writerows(QUAKES)
        st.download_button("⬇ CSV",buf.getvalue(),file_name=f"seiswatch_data_{int(time.time())}.csv",mime="text/csv",use_container_width=True)
    adm_m1,adm_m2,adm_m3,adm_m4 = st.columns(4)
    adm_m1.metric("Data Points Today","2.4M")
    adm_m2.metric("API Uptime","99.8%")
    adm_m3.metric("Alerts Sent","847")
    adm_m4.metric("Models Active","12")
    st.markdown("<br>", unsafe_allow_html=True)
    log_col,ml_col = st.columns(2)
    with log_col:
        st.markdown('<div class="card-title">SYSTEM EVENT LOG</div>', unsafe_allow_html=True)
        for l in ADMIN_LOG:
            st.markdown(f'<div style="display:flex;align-items:center;gap:8px;padding:5px 0;border-bottom:1px solid #1a0800;font-size:9px"><span style="color:#3a2010;width:58px;flex-shrink:0">{l["time"]}</span><span style="flex:1">{l["event"]}</span><span style="color:{l["color"]};font-size:8px;font-weight:700;flex-shrink:0">{l["level"]}</span></div>', unsafe_allow_html=True)
    with ml_col:
        st.markdown('<div class="card-title">ML MODEL PERFORMANCE</div>', unsafe_allow_html=True)
        cats  = ["Accuracy","Precision","Recall","F1","Speed","Coverage"]
        fig_r = go.Figure()
        # PHASE 1 FEATURE 4: animated radar rotation
        radar_rotation = int(time.time() * 20) % 360

        def hex_to_rgba(h, a=0.08):
            return f"rgba({int(h[1:3],16)},{int(h[3:5],16)},{int(h[5:7],16)},{a})"

        for name,vals,col in [("Random Forest",[82,79,84,81,90,75],ORANGE),("XGBoost",[86,88,82,85,78,82],YELLOW),("LSTM",[78,75,81,78,60,88],RED)]:
            fig_r.add_trace(go.Scatterpolar(r=vals+[vals[0]],theta=cats+[cats[0]],fill="toself",name=name,
                line=dict(color=col,width=2),fillcolor=hex_to_rgba(col)))
        layout_r = {k:v for k,v in plotly_dark().items() if k not in ("xaxis","yaxis","margin")}
        layout_r.update(dict(height=260,margin=dict(l=20,r=20,t=20,b=30),
            polar=dict(bgcolor=CARD,
                radialaxis=dict(visible=False,range=[0,100]),
                angularaxis=dict(tickfont=dict(size=8,color=MUTED),linecolor=BORDER,gridcolor=BORDER,
                                 rotation=radar_rotation)),  # ← rotates each render
            legend=dict(font=dict(size=9,color=MUTED),orientation="h",y=-0.08)))
        fig_r.update_layout(**layout_r)
        st.plotly_chart(fig_r, width='stretch', config={"displayModeBar":False})

# ════════════════════════════════════════════════════════════════════════════
# TAB 11 — SEISMIC AI CHAT
# ════════════════════════════════════════════════════════════════════════════
with tabs[10]:
    st.markdown('<div style="color:#2a1200;font-size:9px;margin-bottom:10px">Powered by Claude · Geological intelligence · Emergency response guidance</div>', unsafe_allow_html=True)
    suggestions = ["What causes earthquakes?","Ring of Fire risks","P vs S wave differences","Tsunami warning signs","Aftershock predictions","Earthquake preparedness","Richter vs moment magnitude","How does LSTM forecast seismic activity?"]
    sug_cols = st.columns(4)
    for i,s in enumerate(suggestions):
        if sug_cols[i%4].button(s,key=f"sug_{i}",use_container_width=True):
            st.session_state.chat_history.append({"role":"user","content":s})
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"],avatar="🌋" if msg["role"]=="assistant" else "👤"):
            if msg["role"]=="assistant":
                st.markdown(f'<span style="color:{AMBER};font-size:8px;font-weight:700;letter-spacing:.1em">SEISMIC AI</span>', unsafe_allow_html=True)
            st.write(msg["content"])
    if prompt := st.chat_input("Ask about fault lines, risk zones, wave propagation, emergency protocols..."):
        st.session_state.chat_history.append({"role":"user","content":prompt})
        with st.chat_message("user",avatar="👤"):
            st.write(prompt)
        with st.chat_message("assistant",avatar="🌋"):
            st.markdown(f'<span style="color:{AMBER};font-size:8px;font-weight:700;letter-spacing:.1em">SEISMIC AI</span>', unsafe_allow_html=True)
            with st.spinner("Analyzing seismic data..."):
                try:
                    import anthropic
                    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
                    response = client.messages.create(
                        model="claude-sonnet-4-20250514",max_tokens=400,
                        system="You are SEISMIC AI, an expert earthquake and geological intelligence assistant for an emergency monitoring platform. Deep expertise in seismology, tectonic plates, P/S waves, USGS data, tsunami risk, LSTM forecasting, and emergency response. Be concise (2-4 sentences), technical but accessible. Plain text only.",
                        messages=[{"role":m["role"],"content":m["content"]} for m in st.session_state.chat_history[-8:]])
                    reply = response.content[0].text
                except Exception as e:
                    reply = f"Seismic AI offline. Please add ANTHROPIC_API_KEY to Streamlit secrets. ({type(e).__name__})"
            st.write(reply)
            st.session_state.chat_history.append({"role":"assistant","content":reply})

# ── Footer ───────────────────────────────────────────────────────────────────
st.markdown(f'<div style="border-top:1px solid #1a0800;padding:8px 0;margin-top:16px;display:flex;justify-content:space-between;font-size:8px;color:#2a1200"><span>SEISWATCH v3.0 · Data: USGS, EMSC, JMA · {datetime.now().year}</span><span>FOR DEMONSTRATION PURPOSES ONLY · NOT FOR EMERGENCY USE</span></div>', unsafe_allow_html=True)