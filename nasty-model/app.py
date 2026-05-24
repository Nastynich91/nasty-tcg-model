import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="The Nasty Model",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Dark theme CSS ──────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background-color: #0f1117; color: #e8e8e8; }
  section[data-testid="stSidebar"] { background-color: #0f1117; }
  .block-container { padding: 1.5rem 2rem; max-width: 1400px; }
  h1, h2, h3 { color: #ffffff; }
  .stDataFrame { background: #1a1d2e; }
  div[data-testid="metric-container"] {
    background: #1a1d2e; border: 0.5px solid #2a2d3e;
    border-radius: 8px; padding: 0.75rem 1rem;
  }
  div[data-testid="metric-container"] label { color: #6b7280 !important; font-size: 12px; }
  div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #ffffff; font-size: 22px; }
  .stTextInput > div > div > input, .stNumberInput > div > div > input,
  .stSelectbox > div > div { background: #1a1d2e !important; color: #e8e8e8 !important; border-color: #2a2d3e !important; }
  .stButton > button {
    background: #1a1d2e; color: #e8e8e8; border: 0.5px solid #2a2d3e;
    border-radius: 8px; font-size: 13px;
  }
  .stButton > button:hover { background: #2a2d3e; border-color: #374151; }
  hr { border-color: #1e2130; }
  .pill-green  { background:#14532d; color:#4ade80; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:500; }
  .pill-red    { background:#450a0a; color:#f87171; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:500; }
  .pill-amber  { background:#451a03; color:#fbbf24; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:500; }
  .pill-blue   { background:#0c1a3a; color:#60a5fa; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:500; }
  .pill-purple { background:#2e1065; color:#c084fc; padding:2px 10px; border-radius:20px; font-size:11px; font-weight:500; }
  .nps-green  { color:#4ade80; font-weight:600; font-size:15px; }
  .nps-amber  { color:#fbbf24; font-weight:600; font-size:15px; }
  .nps-red    { color:#f87171; font-weight:600; font-size:15px; }
  .card-name  { font-weight:500; color:#ffffff; font-size:14px; }
  .card-sub   { color:#6b7280; font-size:12px; }
  .upside-card { background:#1a1d2e; border:0.5px solid #2a2d3e; border-radius:10px; padding:1rem 1.2rem; margin-bottom:10px; }
  .upside-top  { background:#1a1d2e; border:1.5px solid #1d4ed8; border-radius:10px; padding:1rem 1.2rem; margin-bottom:10px; }
  table.nasty { width:100%; border-collapse:collapse; }
  table.nasty th { font-size:11px; color:#4b5563; font-weight:500; text-align:left; padding:8px 10px; border-bottom:0.5px solid #1e2130; letter-spacing:.04em; }
  table.nasty td { padding:9px 10px; border-bottom:0.5px solid #161820; vertical-align:middle; font-size:13px; }
  table.nasty tr:hover td { background:#1a1d2e; }
  .header-bar { display:flex; align-items:center; gap:14px; margin-bottom:1.5rem; }
  .logo-circle { width:46px; height:46px; background:#1e2130; border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:22px; flex-shrink:0; }
  .gain-pos { color:#4ade80; font-weight:500; }
  .gain-neg { color:#f87171; font-weight:500; }
  .gain-neu { color:#9ca3af; }
  [data-testid="stExpander"] { background:#1a1d2e; border:0.5px solid #2a2d3e; border-radius:8px; }
</style>
""", unsafe_allow_html=True)

USD_CAD = 1.364

# ── Sets database ─────────────────────────────────────────────────────────
SETS = {
    "EVS": {"name": "Evolving Skies",      "year": 2021, "status": "oop"},
    "FST": {"name": "Fusion Strike",        "year": 2021, "status": "oop"},
    "CEL": {"name": "Celebrations",         "year": 2021, "status": "oop"},
    "SIT": {"name": "Silver Tempest",       "year": 2022, "status": "oop"},
    "SVI": {"name": "Scarlet & Violet",     "year": 2023, "status": "oop"},
    "PAL": {"name": "Paldea Evolved",       "year": 2023, "status": "oop"},
    "OBF": {"name": "Obsidian Flames",      "year": 2023, "status": "oop"},
    "MEW": {"name": "Pokémon 151",          "year": 2023, "status": "oop"},
    "PAR": {"name": "Paradox Rift",         "year": 2023, "status": "oop"},
    "PAF": {"name": "Paldean Fates",        "year": 2024, "status": "oop"},
    "TEF": {"name": "Temporal Forces",      "year": 2024, "status": "oop"},
    "TWM": {"name": "Twilight Masquerade",  "year": 2024, "status": "oop"},
    "SFA": {"name": "Shrouded Fable",       "year": 2024, "status": "oop"},
    "SCR": {"name": "Stellar Crown",        "year": 2024, "status": "oop"},
    "SSP": {"name": "Surging Sparks",       "year": 2024, "status": "soon"},
    "PRE": {"name": "Prismatic Evolutions", "year": 2025, "status": "oop"},
    "JTG": {"name": "Journey Together",     "year": 2025, "status": "soon"},
    "DRI": {"name": "Destined Rivals",      "year": 2025, "status": "in"},
    "BLK": {"name": "Black Bolt",           "year": 2025, "status": "in"},
    "WHT": {"name": "White Flare",          "year": 2025, "status": "in"},
    "MEG": {"name": "Mega Evolution",       "year": 2025, "status": "in"},
    "PHF": {"name": "Phantasmal Flames",    "year": 2025, "status": "in"},
    "ASH": {"name": "Ascended Heroes",      "year": 2026, "status": "in"},
    "PFO": {"name": "Perfect Order",        "year": 2026, "status": "in"},
    "CRS": {"name": "Chaos Rising",         "year": 2026, "status": "in"},
}

PRINT_SCORE = {"oop": 1.0, "soon": 0.80, "in": 0.20}
TIER_SCORE  = {"S": 1.0, "A": 0.75, "B": 0.50, "C": 0.30, "D": 0.10}

def u(v): return round(v * USD_CAD, 2)

# ── Default card database ────────────────────────────────────────────────
DEFAULT_CARDS = [
    {"id":"EVS-215","name":"Umbreon VMAX Alt Art","set":"EVS","rarity":"ALT","tier":"S","price":u(310),"p1":u(308),"p7":u(285),"p30":u(218),"sat":0.02,"arb":0.90,"vel":0.60,"whale":0.90,"cross":0.55,"soc":0.80,"rep":0.05,"stab":0.90},
    {"id":"EVS-217","name":"Rayquaza VMAX Alt Art","set":"EVS","rarity":"ALT","tier":"S","price":u(282),"p1":u(280),"p7":u(255),"p30":u(198),"sat":0.03,"arb":0.80,"vel":0.55,"whale":0.85,"cross":0.70,"soc":0.72,"rep":0.05,"stab":0.85},
    {"id":"OBF-201","name":"Charizard ex SIR","set":"OBF","rarity":"SIR","tier":"S","price":u(422),"p1":u(420),"p7":u(395),"p30":u(310),"sat":0.04,"arb":0.72,"vel":0.85,"whale":0.80,"cross":0.85,"soc":0.75,"rep":0.20,"stab":0.78},
    {"id":"MEW-205","name":"Mew ex SIR","set":"MEW","rarity":"SIR","tier":"S","price":u(145),"p1":u(143),"p7":u(130),"p30":u(98),"sat":0.05,"arb":0.65,"vel":0.60,"whale":0.65,"cross":0.80,"soc":0.75,"rep":0.10,"stab":0.72},
    {"id":"MEW-202","name":"Charizard ex SIR (151)","set":"MEW","rarity":"SIR","tier":"S","price":u(210),"p1":u(208),"p7":u(195),"p30":u(155),"sat":0.04,"arb":0.70,"vel":0.65,"whale":0.75,"cross":0.85,"soc":0.78,"rep":0.08,"stab":0.80},
    {"id":"PAR-245","name":"Roaring Moon ex Alt Art","set":"PAR","rarity":"ALT","tier":"A","price":u(92),"p1":u(90),"p7":u(82),"p30":u(60),"sat":0.06,"arb":0.58,"vel":0.55,"whale":0.55,"cross":0.65,"soc":0.62,"rep":0.15,"stab":0.65},
    {"id":"PAF-086","name":"Pikachu ex SIR","set":"PAF","rarity":"SIR","tier":"S","price":u(98),"p1":u(96),"p7":u(88),"p30":u(68),"sat":0.08,"arb":0.45,"vel":0.95,"whale":0.50,"cross":0.90,"soc":0.85,"rep":0.40,"stab":0.55},
    {"id":"TWM-167","name":"Ogerpon ex SIR","set":"TWM","rarity":"SIR","tier":"A","price":u(88),"p1":u(86),"p7":u(78),"p30":u(58),"sat":0.07,"arb":0.50,"vel":0.60,"whale":0.50,"cross":0.70,"soc":0.65,"rep":0.20,"stab":0.62},
    {"id":"SCR-185","name":"Gardevoir ex SIR","set":"SCR","rarity":"SIR","tier":"A","price":u(72),"p1":u(70),"p7":u(65),"p30":u(50),"sat":0.06,"arb":0.55,"vel":0.58,"whale":0.52,"cross":0.65,"soc":0.60,"rep":0.22,"stab":0.68},
    {"id":"SSP-260","name":"Pikachu ex SIR (Surging)","set":"SSP","rarity":"SIR","tier":"S","price":u(115),"p1":u(112),"p7":u(102),"p30":u(78),"sat":0.07,"arb":0.48,"vel":0.80,"whale":0.60,"cross":0.88,"soc":0.82,"rep":0.35,"stab":0.58},
    {"id":"SSP-240","name":"Raichu ex Alt Art","set":"SSP","rarity":"ALT","tier":"A","price":u(68),"p1":u(66),"p7":u(60),"p30":u(45),"sat":0.06,"arb":0.45,"vel":0.55,"whale":0.45,"cross":0.70,"soc":0.60,"rep":0.25,"stab":0.60},
    {"id":"PRE-161","name":"Umbreon ex SIR (Sunbreon)","set":"PRE","rarity":"SIR","tier":"S","price":u(820),"p1":u(810),"p7":u(740),"p30":u(520),"sat":0.02,"arb":0.92,"vel":0.70,"whale":0.95,"cross":0.60,"soc":0.90,"rep":0.05,"stab":0.88},
    {"id":"PRE-162","name":"Espeon ex SIR","set":"PRE","rarity":"SIR","tier":"A","price":u(285),"p1":u(280),"p7":u(250),"p30":u(180),"sat":0.03,"arb":0.82,"vel":0.60,"whale":0.80,"cross":0.55,"soc":0.78,"rep":0.08,"stab":0.82},
    {"id":"PRE-163","name":"Glaceon ex SIR","set":"PRE","rarity":"SIR","tier":"A","price":u(175),"p1":u(172),"p7":u(155),"p30":u(110),"sat":0.04,"arb":0.75,"vel":0.55,"whale":0.70,"cross":0.50,"soc":0.72,"rep":0.10,"stab":0.78},
    {"id":"PRE-164","name":"Sylveon ex SIR","set":"PRE","rarity":"SIR","tier":"A","price":u(155),"p1":u(152),"p7":u(138),"p30":u(98),"sat":0.04,"arb":0.72,"vel":0.58,"whale":0.68,"cross":0.58,"soc":0.70,"rep":0.10,"stab":0.76},
    {"id":"PRE-165","name":"Flareon ex SIR","set":"PRE","rarity":"SIR","tier":"A","price":u(95),"p1":u(93),"p7":u(84),"p30":u(62),"sat":0.05,"arb":0.65,"vel":0.52,"whale":0.58,"cross":0.50,"soc":0.65,"rep":0.12,"stab":0.72},
    {"id":"JTG-185","name":"Charizard ex SIR","set":"JTG","rarity":"SIR","tier":"S","price":u(135),"p1":u(132),"p7":u(118),"p30":u(88),"sat":0.06,"arb":0.55,"vel":0.70,"whale":0.65,"cross":0.85,"soc":0.75,"rep":0.25,"stab":0.62},
    {"id":"DRI-198","name":"Mewtwo ex SIR","set":"DRI","rarity":"SIR","tier":"S","price":u(95),"p1":u(93),"p7":u(87),"p30":u(68),"sat":0.07,"arb":0.48,"vel":0.68,"whale":0.58,"cross":0.80,"soc":0.72,"rep":0.30,"stab":0.58},
    {"id":"DRI-199","name":"Gengar ex Alt Art","set":"DRI","rarity":"ALT","tier":"A","price":u(62),"p1":u(61),"p7":u(57),"p30":u(44),"sat":0.06,"arb":0.42,"vel":0.52,"whale":0.45,"cross":0.60,"soc":0.58,"rep":0.22,"stab":0.60},
    {"id":"MEG-198","name":"Mega Charizard Y ex SIR","set":"MEG","rarity":"SIR","tier":"S","price":u(180),"p1":u(175),"p7":u(158),"p30":u(110),"sat":0.05,"arb":0.68,"vel":0.75,"whale":0.78,"cross":0.90,"soc":0.85,"rep":0.15,"stab":0.68},
    {"id":"MEG-200","name":"Mega Gengar ex SIR","set":"MEG","rarity":"SIR","tier":"A","price":u(88),"p1":u(86),"p7":u(78),"p30":u(58),"sat":0.06,"arb":0.52,"vel":0.60,"whale":0.55,"cross":0.72,"soc":0.68,"rep":0.18,"stab":0.62},
    {"id":"MEG-201","name":"Mega Blastoise ex SIR","set":"MEG","rarity":"SIR","tier":"A","price":u(72),"p1":u(70),"p7":u(64),"p30":u(48),"sat":0.07,"arb":0.48,"vel":0.55,"whale":0.50,"cross":0.70,"soc":0.62,"rep":0.20,"stab":0.60},
    {"id":"PHF-185","name":"Dragapult ex SIR","set":"PHF","rarity":"SIR","tier":"A","price":u(55),"p1":u(54),"p7":u(50),"p30":u(38),"sat":0.07,"arb":0.40,"vel":0.50,"whale":0.42,"cross":0.58,"soc":0.55,"rep":0.28,"stab":0.55},
    {"id":"ASH-200","name":"Mega Dragonite ex SIR","set":"ASH","rarity":"SIR","tier":"A","price":u(78),"p1":u(74),"p7":u(65),"p30":u(45),"sat":0.05,"arb":0.60,"vel":0.72,"whale":0.62,"cross":0.75,"soc":0.70,"rep":0.15,"stab":0.60},
    {"id":"ASH-201","name":"Mega Charizard Y ex Alt Art","set":"ASH","rarity":"ALT","tier":"S","price":u(220),"p1":u(210),"p7":u(185),"p30":u(120),"sat":0.04,"arb":0.72,"vel":0.80,"whale":0.78,"cross":0.92,"soc":0.85,"rep":0.12,"stab":0.65},
    {"id":"ASH-202","name":"Mega Mewtwo Y ex SIR","set":"ASH","rarity":"SIR","tier":"S","price":u(155),"p1":u(148),"p7":u(130),"p30":u(85),"sat":0.04,"arb":0.68,"vel":0.75,"whale":0.72,"cross":0.85,"soc":0.80,"rep":0.12,"stab":0.62},
    {"id":"ASH-203","name":"N's Zekrom SIR","set":"ASH","rarity":"SIR","tier":"A","price":u(68),"p1":u(65),"p7":u(58),"p30":u(40),"sat":0.06,"arb":0.50,"vel":0.60,"whale":0.52,"cross":0.65,"soc":0.68,"rep":0.20,"stab":0.58},
    {"id":"ASH-204","name":"Mega Venusaur ex SIR","set":"ASH","rarity":"SIR","tier":"A","price":u(65),"p1":u(63),"p7":u(56),"p30":u(38),"sat":0.06,"arb":0.48,"vel":0.58,"whale":0.50,"cross":0.68,"soc":0.62,"rep":0.18,"stab":0.58},
    {"id":"PFO-185","name":"Mega Meganium ex SIR","set":"PFO","rarity":"SIR","tier":"B","price":u(45),"p1":u(44),"p7":u(40),"p30":u(30),"sat":0.08,"arb":0.38,"vel":0.48,"whale":0.38,"cross":0.60,"soc":0.52,"rep":0.25,"stab":0.52},
    {"id":"CRS-190","name":"Mega Rayquaza ex SIR","set":"CRS","rarity":"SIR","tier":"S","price":u(185),"p1":u(178),"p7":u(155),"p30":u(95),"sat":0.04,"arb":0.70,"vel":0.82,"whale":0.78,"cross":0.88,"soc":0.82,"rep":0.12,"stab":0.65},
    {"id":"CRS-191","name":"Mega Salamence ex Alt Art","set":"CRS","rarity":"ALT","tier":"A","price":u(72),"p1":u(69),"p7":u(62),"p30":u(42),"sat":0.06,"arb":0.52,"vel":0.62,"whale":0.55,"cross":0.68,"soc":0.62,"rep":0.18,"stab":0.60},
    {"id":"FST-268","name":"Mew VMAX SIR","set":"FST","rarity":"SIR","tier":"A","price":u(130),"p1":u(128),"p7":u(120),"p30":u(92),"sat":0.07,"arb":0.40,"vel":0.45,"whale":0.45,"cross":0.70,"soc":0.55,"rep":0.25,"stab":0.60},
    {"id":"SIT-217","name":"Lugia V Alt Art","set":"SIT","rarity":"ALT","tier":"A","price":u(183),"p1":u(181),"p7":u(168),"p30":u(135),"sat":0.06,"arb":0.55,"vel":0.50,"whale":0.60,"cross":0.65,"soc":0.60,"rep":0.15,"stab":0.65},
]

DATA_FILE = "data/cards.json"

# ── Persistence ──────────────────────────────────────────────────────────
def load_cards():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return DEFAULT_CARDS.copy()

def save_cards(cards):
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(cards, f, indent=2, ensure_ascii=False)

# ── NPS calculation ──────────────────────────────────────────────────────
def calc_nps(c):
    st   = SETS.get(c["set"], {}).get("status", "in")
    pv   = PRINT_SCORE.get(st, 0.2)
    tv   = TIER_SCORE.get(c["tier"], 0.3)
    sat  = max(0.01, c["sat"])
    w    = ((1-sat)*0.20 + c["arb"]*0.18 + c["vel"]*0.15 + pv*0.25 +
             tv*0.12 + (1-c["rep"])*0.10 + c["stab"]*0.08 +
             c["whale"]*0.06 + c["cross"]*0.05 + c["soc"]*0.04)
    hype = 1 + c["cross"]*0.20 + c["soc"]*0.15
    return min(100, int((w / sat) * hype * 35))

def calc_signal(nps, gain_pct, status):
    pv = PRINT_SCORE.get(status, 0.2)
    fund = (nps/100)*0.6 + pv*0.4
    if fund > 0.72 and gain_pct < 8:  return "sous"
    if fund < 0.40 and gain_pct > 15: return "sur"
    return "juste"

def get_gain(c, days):
    past = c.get(f"p{days}", c["price"])
    if past and past > 0:
        pct = (c["price"] - past) / past * 100
        cad = c["price"] - past
        return round(pct, 2), round(cad, 2)
    return 0.0, 0.0

# ── Session state ────────────────────────────────────────────────────────
if "cards" not in st.session_state:
    st.session_state.cards = load_cards()
if "period" not in st.session_state:
    st.session_state.period = 7
if "sort_by" not in st.session_state:
    st.session_state.sort_by = "gain_pct"

cards = st.session_state.cards

# ── Header ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-bar">
  <div class="logo-circle">🃏</div>
  <div>
    <h1 style="margin:0;font-size:24px">The Nasty Model</h1>
    <p style="color:#6b7280;margin:0;font-size:13px">Screener TCG · Top movers · NPS upside · Valeurs en C$</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Controls row ─────────────────────────────────────────────────────────
col_s, col_set, col_sig, col_per, col_srt = st.columns([3, 2, 2, 1.5, 2])
with col_s:
    search = st.text_input("", placeholder="🔍 Rechercher une carte, un set...", label_visibility="collapsed")
with col_set:
    set_options = ["Tous les sets"] + [f"{v['name']} ({k})" for k, v in SETS.items()]
    set_filter = st.selectbox("Set", set_options, label_visibility="collapsed")
with col_sig:
    sig_filter = st.selectbox("Signal", ["Tous les signaux", "Sous-évaluées", "Surévaluées", "Prix juste"], label_visibility="collapsed")
with col_per:
    period = st.selectbox("Période", ["1 jour", "7 jours", "30 jours"], index=1, label_visibility="collapsed")
with col_srt:
    sort_by = st.selectbox("Trier par", ["% gain", "$ gain", "NPS", "Prix"], label_visibility="collapsed")

days_map = {"1 jour": 1, "7 jours": 7, "30 jours": 30}
sort_map  = {"% gain": "gain_pct", "$ gain": "gain_cad", "NPS": "nps", "Prix": "price"}
days = days_map[period]
sort_key = sort_map[sort_by]

# ── Build enriched dataframe ─────────────────────────────────────────────
rows = []
for c in cards:
    nps = calc_nps(c)
    gp, gc = get_gain(c, days)
    st_code = SETS.get(c["set"], {}).get("status", "in")
    signal  = calc_signal(nps, gp, st_code)
    set_name = SETS.get(c["set"], {}).get("name", c["set"])
    rows.append({
        **c,
        "nps": nps,
        "gain_pct": gp,
        "gain_cad": gc,
        "signal": signal,
        "set_name": set_name,
        "status": st_code,
    })

df = pd.DataFrame(rows)

# Apply filters
if search:
    mask = (df["name"].str.lower().str.contains(search.lower()) |
            df["set"].str.lower().str.contains(search.lower()) |
            df["set_name"].str.lower().str.contains(search.lower()))
    df = df[mask]

if set_filter != "Tous les sets":
    code = set_filter.split("(")[-1].rstrip(")")
    df = df[df["set"] == code]

sig_map_filter = {"Sous-évaluées": "sous", "Surévaluées": "sur", "Prix juste": "juste"}
if sig_filter != "Tous les signaux":
    df = df[df["signal"] == sig_map_filter[sig_filter]]

df = df.sort_values(sort_key, ascending=False).reset_index(drop=True)

# ── Stats row ─────────────────────────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.metric("cartes", len(df))
m2.metric("sous-évaluées 🟢", int((df["signal"]=="sous").sum()))
m3.metric("surévaluées 🔴",   int((df["signal"]=="sur").sum()))
m4.metric("prix juste 🟡",    int((df["signal"]=="juste").sum()))

st.markdown("---")

# ── Main table ─────────────────────────────────────────────────────────
def signal_html(s):
    if s == "sous": return '<span class="pill-green">SOUS-ÉV.</span>'
    if s == "sur":  return '<span class="pill-red">SUR-ÉV.</span>'
    return '<span class="pill-amber">PRIX JUSTE</span>'

def tier_html(t):
    cls = {"S":"pill-purple","A":"pill-blue","B":"pill-green","C":"pill-amber"}.get(t,"pill-gray")
    return f'<span class="{cls}">{t}</span>'

def nps_html(n):
    cls = "nps-green" if n >= 85 else "nps-amber" if n >= 65 else "nps-red"
    return f'<span class="{cls}">{n}</span>'

def gain_html(v, suffix):
    if v > 0:  return f'<span class="gain-pos">+{v:.1f}{suffix}</span>'
    if v < 0:  return f'<span class="gain-neg">{v:.1f}{suffix}</span>'
    return f'<span class="gain-neu">{v:.1f}{suffix}</span>'

rows_html = ""
for i, row in df.iterrows():
    rows_html += f"""
    <tr>
      <td style="color:#4b5563">{i+1}</td>
      <td>
        <div class="card-name">{row['name']}</div>
        <div class="card-sub">{row['set_name']} · {row['rarity']} · {tier_html(row['tier'])}</div>
      </td>
      <td style="text-align:right;font-weight:500;color:#fff">C${row['price']:.0f}</td>
      <td style="text-align:right">{gain_html(row['gain_pct'], '%')}</td>
      <td style="text-align:right">{gain_html(row['gain_cad'], ' C$')}</td>
      <td style="text-align:center">{signal_html(row['signal'])}</td>
      <td style="text-align:right">{nps_html(row['nps'])}</td>
    </tr>"""

table_html = f"""
<table class="nasty">
  <thead><tr>
    <th style="width:32px">#</th>
    <th>carte</th>
    <th style="text-align:right">prix C$</th>
    <th style="text-align:right">% gain</th>
    <th style="text-align:right">gain C$</th>
    <th style="text-align:center">signal</th>
    <th style="text-align:right">NPS</th>
  </tr></thead>
  <tbody>{rows_html}</tbody>
</table>"""

st.markdown(table_html, unsafe_allow_html=True)

# ── Upside section ────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🚀 Upside potential — parmi les movers, qui peut encore monter ?")

upside_df = df[df["gain_pct"] > 0].sort_values("nps", ascending=False).head(5)

for i, (_, row) in enumerate(upside_df.iterrows()):
    card_class = "upside-top" if i == 0 else "upside-card"
    badge = '<span class="pill-blue" style="padding:2px 10px;border-radius:20px;font-size:10px;font-weight:500;background:#0c1a3a;color:#60a5fa">meilleur upside</span> ' if i == 0 else ""
    nps_c = "#4ade80" if row["nps"] >= 85 else "#fbbf24" if row["nps"] >= 65 else "#f87171"

    bars = [
        ("saturation PSA10", round((1-row["sat"])*100), "#60a5fa"),
        ("arbitrage JP/EN",  round(row["arb"]*100),     "#4ade80"),
        ("print status",     round(PRINT_SCORE.get(row["status"],0.2)*100), "#fbbf24"),
        ("whale activity",   round(row["whale"]*100),   "#c084fc"),
    ]
    bars_html = "".join([
        f'<div style="display:flex;align-items:center;gap:8px;margin-bottom:4px">'
        f'<span style="font-size:11px;color:#4b5563;min-width:90px">{lbl}</span>'
        f'<div style="flex:1;background:#0f1117;border-radius:3px;height:4px;overflow:hidden">'
        f'<div style="width:{val}%;height:100%;background:{clr};border-radius:3px"></div></div>'
        f'<span style="font-size:11px;color:#4b5563;min-width:28px;text-align:right">{val}%</span>'
        f'</div>'
        for lbl, val, clr in bars
    ])

    st.markdown(f"""
    <div class="{card_class}">
      <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:8px">
        {badge}
        <span style="font-size:13px;font-weight:500;color:#fff;flex:1">{row['name']} <span style="color:#4b5563;font-size:11px;font-weight:400">{row['set']}</span></span>
        <span style="color:#4ade80;font-size:12px">+{row['gain_pct']:.1f}%</span>
        <span style="font-size:16px;font-weight:600;color:{nps_c}">{row['nps']}<span style="font-size:11px;color:#4b5563;font-weight:400">/100</span></span>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 16px">{bars_html}</div>
    </div>""", unsafe_allow_html=True)

# ── Add card section ──────────────────────────────────────────────────────
st.markdown("---")
with st.expander("➕  Ajouter une carte manuellement"):
    c1, c2 = st.columns(2)
    with c1:
        new_name  = st.text_input("Nom de la carte")
        new_set   = st.selectbox("Set", list(SETS.keys()), format_func=lambda k: f"{SETS[k]['name']} ({k})")
        new_rar   = st.selectbox("Rareté", ["SIR", "ALT", "IR", "RH", "PROMO", "Gold", "Autre"])
        new_tier  = st.selectbox("Tier", ["S", "A", "B", "C"])
    with c2:
        new_price = st.number_input("Prix actuel C$", min_value=0.0, step=0.5)
        new_p7    = st.number_input("Prix il y a 7 jours C$", min_value=0.0, step=0.5)
        new_p30   = st.number_input("Prix il y a 30 jours C$", min_value=0.0, step=0.5)
        new_sat   = st.number_input("Saturation PSA10 (0–1)", min_value=0.0, max_value=1.0, value=0.06, step=0.01)
        new_arb   = st.number_input("Arbitrage JP/EN (0–1)", min_value=0.0, max_value=1.0, value=0.50, step=0.01)

    if st.button("Ajouter la carte", type="primary"):
        if new_name and new_price > 0:
            new_card = {
                "id": f"custom-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "name": new_name, "set": new_set, "rarity": new_rar, "tier": new_tier,
                "price": new_price,
                "p1": new_price * 0.998,
                "p7": new_p7 if new_p7 > 0 else new_price,
                "p30": new_p30 if new_p30 > 0 else new_price,
                "sat": new_sat, "arb": new_arb,
                "vel": 0.50, "whale": 0.45, "cross": 0.52,
                "soc": 0.50, "rep": 0.25, "stab": 0.55,
            }
            st.session_state.cards.append(new_card)
            save_cards(st.session_state.cards)
            st.success(f"✅ {new_name} ajoutée !")
            st.rerun()
        else:
            st.error("Remplis au minimum le nom et le prix.")

# ── Import CSV ────────────────────────────────────────────────────────────
with st.expander("📂  Importer un CSV"):
    st.markdown("""
    **Format attendu :** `id, name, set, rarity, tier, price, p7, p30, sat, arb`  
    Exemple : `OBF-201, Charizard ex SIR, OBF, SIR, S, 575, 540, 420, 0.04, 0.72`
    """)
    uploaded = st.file_uploader("Choisir un fichier CSV", type=["csv"])
    if uploaded:
        try:
            import_df = pd.read_csv(uploaded, skipinitialspace=True)
            import_df.columns = import_df.columns.str.strip().str.lower()
            added = 0
            for _, row in import_df.iterrows():
                card = {
                    "id": str(row.get("id", f"imp-{added}")),
                    "name": str(row.get("name", "Unknown")),
                    "set": str(row.get("set", "UNK")),
                    "rarity": str(row.get("rarity", "—")),
                    "tier": str(row.get("tier", "B")),
                    "price": float(row.get("price", 0)),
                    "p1": float(row.get("price", 0)) * 0.998,
                    "p7": float(row.get("p7", row.get("price", 0))),
                    "p30": float(row.get("p30", row.get("price", 0))),
                    "sat": float(row.get("sat", 0.06)),
                    "arb": float(row.get("arb", 0.45)),
                    "vel": 0.50, "whale": 0.45, "cross": 0.52,
                    "soc": 0.50, "rep": 0.25, "stab": 0.55,
                }
                st.session_state.cards.append(card)
                added += 1
            save_cards(st.session_state.cards)
            st.success(f"✅ {added} cartes importées !")
            st.rerun()
        except Exception as e:
            st.error(f"Erreur : {e}")

# ── Reset ────────────────────────────────────────────────────────────────
with st.expander("⚙️  Paramètres"):
    col_r1, col_r2 = st.columns(2)
    with col_r1:
        if st.button("Réinitialiser toutes les cartes"):
            st.session_state.cards = DEFAULT_CARDS.copy()
            save_cards(st.session_state.cards)
            st.success("Base de données réinitialisée.")
            st.rerun()
    with col_r2:
        export_data = json.dumps(st.session_state.cards, indent=2, ensure_ascii=False)
        st.download_button("Exporter JSON", data=export_data, file_name="nasty_model_cards.json", mime="application/json")

st.markdown(f'<p style="color:#2a2d3e;font-size:11px;text-align:center;margin-top:2rem">The Nasty Model · {len(st.session_state.cards)} cartes · USD/CAD {USD_CAD}</p>', unsafe_allow_html=True)
