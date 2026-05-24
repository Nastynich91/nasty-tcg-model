import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import requests
from datetime import datetime
from cards_data import ALL_CARDS

st.set_page_config(page_title="The Nasty Model", page_icon="🃏", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background-color: #0d0f18; color: #e8e8e8; }
  .block-container { padding: 1.5rem 2rem; max-width: 1600px; }
  section[data-testid="stSidebar"] { background:#111320 !important; border-right:0.5px solid #252840; }
  section[data-testid="stSidebar"] * { color:#e8e8e8 !important; }
  section[data-testid="stSidebar"] .stSelectbox>div>div,
  section[data-testid="stSidebar"] .stTextInput>div>div>input,
  section[data-testid="stSidebar"] .stNumberInput>div>div>input { background:#161928 !important; border-color:#252840 !important; }
  h1,h2,h3 { color:#fff; }
  div[data-testid="metric-container"] { background:#161928; border:0.5px solid #252840; border-radius:10px; padding:.65rem 1rem; }
  div[data-testid="metric-container"] label { color:#6b7280 !important; font-size:11px; letter-spacing:.04em; text-transform:uppercase; }
  div[data-testid="metric-container"] [data-testid="stMetricValue"] { color:#fff; font-size:20px; font-weight:600; }
  .stTextInput>div>div>input { background:#161928 !important; color:#e8e8e8 !important; border-color:#252840 !important; border-radius:8px !important; }
  .stSelectbox>div>div { background:#161928 !important; color:#e8e8e8 !important; border-color:#252840 !important; }
  .stNumberInput>div>div>input { background:#161928 !important; color:#e8e8e8 !important; border-color:#252840 !important; }
  .stSlider { color:#e8e8e8; }
  .stButton>button { background:#161928; color:#e8e8e8; border:0.5px solid #252840; border-radius:8px; font-size:12px; }
  .stButton>button:hover { background:#252840; }
  .stButton>button[kind="primary"] { background:#1d4ed8; border-color:#1d4ed8; color:#fff; }
  [data-testid="stExpander"] { background:#161928; border:0.5px solid #252840; border-radius:10px; }
  hr { border-color:#1a1d2e; }
  .card-row { display:grid; grid-template-columns:64px 1fr 95px 80px 75px 75px 75px 75px 75px 105px 72px; align-items:center; gap:0 8px; padding:8px 14px; border-bottom:0.5px solid #13151f; transition:background .1s; }
  .card-row:hover { background:#161928; border-radius:6px; }
  .card-row.hdr { font-size:10px; color:#4b5563; font-weight:500; letter-spacing:.05em; text-transform:uppercase; padding:7px 14px; border-bottom:0.5px solid #252840; }
  .cimg { width:56px; height:78px; object-fit:cover; border-radius:5px; }
  .cimg-ph { width:56px; height:78px; border-radius:5px; background:#1a1d2e; display:flex; align-items:center; justify-content:center; font-size:18px; }
  .cname { font-weight:600; color:#fff; font-size:13px; line-height:1.3; }
  .csub { font-size:11px; color:#6b7280; margin-top:1px; }
  .cprice { font-weight:600; color:#fff; font-size:14px; text-align:right; white-space:nowrap; }
  .pos { color:#4ade80; font-weight:500; font-size:12px; text-align:right; }
  .neg { color:#f87171; font-weight:500; font-size:12px; text-align:right; }
  .neu { color:#4b5563; font-size:12px; text-align:right; }
  .dem-wrap { display:flex; align-items:center; gap:4px; margin-top:3px; }
  .dem-bg { flex:1; background:#1a1d2e; border-radius:3px; height:3px; overflow:hidden; }
  .dem-fg { height:100%; border-radius:3px; }
  .dem-pct { font-size:10px; font-weight:500; min-width:24px; text-align:right; }
  .sig { display:inline-block; font-size:10px; padding:3px 8px; border-radius:20px; font-weight:600; white-space:nowrap; }
  .sous { background:#14532d; color:#4ade80; }
  .sur  { background:#450a0a; color:#f87171; }
  .juste{ background:#451a03; color:#fbbf24; }
  .npsv { font-weight:700; font-size:13px; text-align:right; }
  .ng{color:#4ade80;} .na{color:#fbbf24;} .nr{color:#f87171;}
  .pill { display:inline-block; font-size:10px; padding:1px 6px; border-radius:10px; font-weight:500; margin-right:2px; }
  .p-sir{background:#2e1065;color:#c084fc;} .p-alt{background:#0c1a3a;color:#60a5fa;} .p-ir{background:#042f2e;color:#2dd4bf;}
  .p-shv{background:#451a03;color:#fbbf24;} .p-fa{background:#1f2937;color:#9ca3af;} .p-rr{background:#450a0a;color:#f87171;}
  .p-gold{background:#451a03;color:#fbbf24;} .p-gg{background:#0c1a3a;color:#60a5fa;} .p-def{background:#1f2937;color:#9ca3af;}
  .p-s{background:#2e1065;color:#c084fc;} .p-a{background:#0c1a3a;color:#60a5fa;} .p-b{background:#042f2e;color:#2dd4bf;} .p-c{background:#1f2937;color:#9ca3af;}
  .show-badge { display:inline-block; background:#7c3aed; color:#fff; font-size:10px; padding:2px 8px; border-radius:10px; font-weight:700; margin-left:6px; vertical-align:middle; }
  .pump-badge { display:inline-block; background:#dc2626; color:#fff; font-size:10px; padding:2px 8px; border-radius:10px; font-weight:700; margin-left:4px; vertical-align:middle; }
  .sidebar-title { font-size:13px; font-weight:600; color:#fff !important; margin-bottom:4px; margin-top:12px; display:block; }
  .sidebar-sep { border:none; border-top:0.5px solid #252840; margin:14px 0; }
</style>
""", unsafe_allow_html=True)

USD_CAD   = 1.364
CACHE_FILE = "data/price_cache.json"
DATA_FILE  = "data/cards.json"

SETS = {
    "XY":{"name":"XY Base","year":2014,"status":"oop","tcg_id":"xy1"},
    "FLF":{"name":"Flashfire","year":2014,"status":"oop","tcg_id":"xy2"},
    "ROS":{"name":"Roaring Skies","year":2015,"status":"oop","tcg_id":"xy6"},
    "AOR":{"name":"Ancient Origins","year":2015,"status":"oop","tcg_id":"xy7"},
    "BKT":{"name":"BREAKthrough","year":2015,"status":"oop","tcg_id":"xy8"},
    "BKP":{"name":"BREAKpoint","year":2016,"status":"oop","tcg_id":"xy9"},
    "FCO":{"name":"Fates Collide","year":2016,"status":"oop","tcg_id":"xy10"},
    "STS":{"name":"Steam Siege","year":2016,"status":"oop","tcg_id":"xy11"},
    "EVO":{"name":"Evolutions","year":2016,"status":"oop","tcg_id":"xy12"},
    "SUM":{"name":"Sun & Moon","year":2017,"status":"oop","tcg_id":"sm1"},
    "GRI":{"name":"Guardians Rising","year":2017,"status":"oop","tcg_id":"sm2"},
    "BUS":{"name":"Burning Shadows","year":2017,"status":"oop","tcg_id":"sm3"},
    "SHL":{"name":"Shining Legends","year":2017,"status":"oop","tcg_id":"sm35"},
    "CRI":{"name":"Crimson Invasion","year":2017,"status":"oop","tcg_id":"sm4"},
    "UPR":{"name":"Ultra Prism","year":2018,"status":"oop","tcg_id":"sm5"},
    "FLI":{"name":"Forbidden Light","year":2018,"status":"oop","tcg_id":"sm6"},
    "CES":{"name":"Celestial Storm","year":2018,"status":"oop","tcg_id":"sm7"},
    "LOT":{"name":"Lost Thunder","year":2018,"status":"oop","tcg_id":"sm8"},
    "TEU":{"name":"Team Up","year":2019,"status":"oop","tcg_id":"sm9"},
    "UNB":{"name":"Unbroken Bonds","year":2019,"status":"oop","tcg_id":"sm10"},
    "UNM":{"name":"Unified Minds","year":2019,"status":"oop","tcg_id":"sm11"},
    "HIF":{"name":"Hidden Fates","year":2019,"status":"oop","tcg_id":"hif"},
    "CEC":{"name":"Cosmic Eclipse","year":2019,"status":"oop","tcg_id":"sm12"},
    "RCL":{"name":"Rebel Clash","year":2020,"status":"oop","tcg_id":"swsh2"},
    "DAA":{"name":"Darkness Ablaze","year":2020,"status":"oop","tcg_id":"swsh3"},
    "VIV":{"name":"Vivid Voltage","year":2020,"status":"oop","tcg_id":"swsh4"},
    "SHF":{"name":"Shining Fates","year":2021,"status":"oop","tcg_id":"shf"},
    "BST":{"name":"Battle Styles","year":2021,"status":"oop","tcg_id":"swsh5"},
    "CRE":{"name":"Chilling Reign","year":2021,"status":"oop","tcg_id":"swsh6"},
    "EVS":{"name":"Evolving Skies","year":2021,"status":"oop","tcg_id":"swsh7"},
    "FST":{"name":"Fusion Strike","year":2021,"status":"oop","tcg_id":"swsh8"},
    "CEL":{"name":"Celebrations","year":2021,"status":"oop","tcg_id":"cel25"},
    "BRS":{"name":"Brilliant Stars","year":2022,"status":"oop","tcg_id":"swsh9"},
    "ASR":{"name":"Astral Radiance","year":2022,"status":"oop","tcg_id":"swsh10"},
    "PGO":{"name":"Pokémon GO","year":2022,"status":"oop","tcg_id":"pgo"},
    "LOR":{"name":"Lost Origin","year":2022,"status":"oop","tcg_id":"swsh11"},
    "SIT":{"name":"Silver Tempest","year":2022,"status":"oop","tcg_id":"swsh12"},
    "CRZ":{"name":"Crown Zenith","year":2023,"status":"oop","tcg_id":"swsh125"},
    "SVI":{"name":"Scarlet & Violet","year":2023,"status":"oop","tcg_id":"sv1"},
    "PAL":{"name":"Paldea Evolved","year":2023,"status":"oop","tcg_id":"sv2"},
    "OBF":{"name":"Obsidian Flames","year":2023,"status":"oop","tcg_id":"sv3"},
    "MEW":{"name":"Pokémon 151","year":2023,"status":"oop","tcg_id":"sv3pt5"},
    "PAR":{"name":"Paradox Rift","year":2023,"status":"oop","tcg_id":"sv4"},
    "PAF":{"name":"Paldean Fates","year":2024,"status":"oop","tcg_id":"sv4pt5"},
    "TEF":{"name":"Temporal Forces","year":2024,"status":"oop","tcg_id":"sv5"},
    "TWM":{"name":"Twilight Masquerade","year":2024,"status":"oop","tcg_id":"sv6"},
    "SFA":{"name":"Shrouded Fable","year":2024,"status":"oop","tcg_id":"sv6pt5"},
    "SCR":{"name":"Stellar Crown","year":2024,"status":"oop","tcg_id":"sv7"},
    "SSP":{"name":"Surging Sparks","year":2024,"status":"soon","tcg_id":"sv8"},
    "PRE":{"name":"Prismatic Evolutions","year":2025,"status":"oop","tcg_id":"sv8pt5"},
    "JTG":{"name":"Journey Together","year":2025,"status":"soon","tcg_id":"sv9"},
    "DRI":{"name":"Destined Rivals","year":2025,"status":"in","tcg_id":"sv9pt5"},
    "MEG":{"name":"Mega Evolution","year":2025,"status":"in","tcg_id":"sv10"},
    "PHF":{"name":"Phantasmal Flames","year":2025,"status":"in","tcg_id":"sv10pt5"},
    "ASH":{"name":"Ascended Heroes","year":2026,"status":"in","tcg_id":"sv11"},
    "PFO":{"name":"Perfect Order","year":2026,"status":"in","tcg_id":"sv11pt5"},
    "CRS":{"name":"Chaos Rising","year":2026,"status":"in","tcg_id":"sv12"},
}

PRINT_SCORE = {"oop":1.0,"soon":0.80,"in":0.20}
TIER_SCORE  = {"S":1.0,"A":0.75,"B":0.50,"C":0.30,"D":0.10}

def load_json(path, default):
    if os.path.exists(path):
        with open(path,"r") as f: return json.load(f)
    return default

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,"w") as f: json.dump(data, f, indent=2, ensure_ascii=False)

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_card_api(card_name, set_code):
    tcg_id = SETS.get(set_code,{}).get("tcg_id","")
    if not tcg_id: return None
    try:
        clean = card_name.replace(" (SIR)","").replace(" (Alt Art)","").replace(" (IR)","").replace(" (Rainbow)","").replace(" (Full Art)","").replace(" (Shiny)","").split("(")[0].strip()
        url = f"https://api.pokemontcg.io/v2/cards?q=name:\"{clean}\" set.id:{tcg_id}&pageSize=5"
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            cards = r.json().get("data",[])
            if cards: return cards[0]
    except: pass
    return None

def get_tcg_price(api_card):
    if not api_card: return None
    prices = api_card.get("tcgplayer",{}).get("prices",{})
    for pt in ["holofoil","1stEditionHolofoil","reverseHolofoil","normal","unlimitedHolofoil"]:
        p = prices.get(pt,{})
        m = p.get("market") or p.get("mid")
        if m and m > 0: return round(m * USD_CAD, 2)
    return None

def get_img(api_card):
    if api_card: return api_card.get("images",{}).get("large") or api_card.get("images",{}).get("small")
    return None

def calc_nps(c):
    st_ = SETS.get(c["set"],{}).get("status","in")
    pv  = PRINT_SCORE.get(st_,0.2); tv = TIER_SCORE.get(c.get("tier","B"),0.3)
    sat = max(0.01,c.get("sat",0.07))
    w   = ((1-sat)*0.20+c.get("arb",0.5)*0.18+c.get("vel",0.5)*0.15+pv*0.25+tv*0.12+
            (1-c.get("rep",0.3))*0.10+c.get("stab",0.6)*0.08+c.get("whale",0.4)*0.06+
            c.get("cross",0.5)*0.05+c.get("soc",0.5)*0.04)
    return min(100,int((w/sat)*(1+c.get("cross",0.5)*0.20+c.get("soc",0.5)*0.15)*35))

def calc_signal(nps, gp, status):
    pv = PRINT_SCORE.get(status,0.2); fund=(nps/100)*0.6+pv*0.4
    if fund>0.72 and gp<8: return "sous"
    if fund<0.40 and gp>15: return "sur"
    return "juste"

def get_gain(c, days):
    past = c.get(f"p{days}", c.get("price",0))
    if past and past>0: return round((c["price"]-past)/past*100,2), round(c["price"]-past,2)
    return 0.0,0.0

def rar_pill(r):
    m={"SIR":"p-sir","ALT":"p-alt","IR":"p-ir","GG":"p-gg","SHV":"p-shv","SHINING":"p-shv","CLASSIC":"p-gold","FA":"p-fa","RR":"p-rr","GOLD":"p-gold"}
    return f'<span class="pill {m.get(r,"p-def")}">{r}</span>'
def tier_pill(t):
    return f'<span class="pill p-{t.lower()}">{t}</span>'
def clr(v):
    if v>0:  return f'<span class="pos">+{v:.1f}%</span>'
    if v<0:  return f'<span class="neg">{v:.1f}%</span>'
    return '<span class="neu">—</span>'
def signal_pill(s):
    labels={"sous":"SOUS-ÉV.","sur":"SUR-ÉV.","juste":"PRIX JUSTE"}
    return f'<span class="sig {s}">{labels[s]}</span>'
def nps_cell(n):
    c="ng" if n>=85 else "na" if n>=65 else "nr"
    return f'<div class="npsv {c}">{n}</div>'

# ── Session state ────────────────────────────
if "cards"      not in st.session_state: st.session_state.cards = load_json(DATA_FILE, ALL_CARDS.copy())
if "period"     not in st.session_state: st.session_state.period = 7
if "api_cache"  not in st.session_state: st.session_state.api_cache = load_json(CACHE_FILE, {})

# ════════════════════════════════════════════
# SIDEBAR — tous les filtres
# ════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🎯 Filtres Show Day")
    st.markdown("---")

    # MODE SHOW DAY
    show_day_mode = st.toggle("⚡ Mode Show Day", value=False,
        help="Affiche seulement les cartes qui ont pumpé et que les vendeurs n'ont pas encore repriced")

    st.markdown('<span class="sidebar-title">📅 Période de gains</span>', unsafe_allow_html=True)
    period_labels = ["24h","3j","7j","1M","3M","6M"]
    period_days   = [1,3,7,30,90,180]
    period_sel = st.radio("Période", period_labels,
                          index=period_labels.index("7j"),
                          horizontal=True, label_visibility="collapsed")
    days = period_days[period_labels.index(period_sel)]

    st.markdown('<hr class="sidebar-sep">', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-title">💰 Filtre par prix (C$)</span>', unsafe_allow_html=True)

    prix_min = st.number_input("Prix minimum C$", min_value=0, value=0, step=5)
    prix_max = st.number_input("Prix maximum C$", min_value=0, value=5000, step=25)

    st.markdown('<hr class="sidebar-sep">', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-title">📈 Filtre par % de gain</span>', unsafe_allow_html=True)

    gain_min = st.slider("Gain minimum %", min_value=0, max_value=100, value=0, step=1)
    gain_max = st.slider("Gain maximum %", min_value=0, max_value=200, value=200, step=5)

    st.markdown('<hr class="sidebar-sep">', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-title">🔍 Autres filtres</span>', unsafe_allow_html=True)

    search = st.text_input("Rechercher", placeholder="Nom, set, rareté...")
    set_opts = ["Tous"] + [f"{v['name']} ({k})" for k,v in SETS.items()]
    set_filter = st.selectbox("Set", set_opts)
    rar_filter = st.selectbox("Rareté", ["Toutes","SIR","ALT","IR","GG","SHV","FA","RR","GOLD","HOLO","EX"])
    tier_filter = st.selectbox("Tier", ["Tous","S","A","B","C"])
    sig_filter = st.selectbox("Signal", ["Tous","Sous-évaluées","Surévaluées","Prix juste"])

    st.markdown('<hr class="sidebar-sep">', unsafe_allow_html=True)
    st.markdown('<span class="sidebar-title">🔢 Tri</span>', unsafe_allow_html=True)
    sort_ui = st.selectbox("Trier par", ["% gain","$ gain","NPS","Prix ↑","Prix ↓","Nom"])

    st.markdown('<hr class="sidebar-sep">', unsafe_allow_html=True)
    if st.button("🔄 Refresh prix live", type="primary", use_container_width=True):
        st.cache_data.clear()
        st.session_state.api_cache = {}
        save_json(CACHE_FILE, {})
        st.rerun()

# ════════════════════════════════════════════
# MAIN — Header
# ════════════════════════════════════════════
st.markdown("""
<div style="display:flex;align-items:center;gap:14px;margin-bottom:1rem">
  <div style="width:48px;height:48px;background:#161928;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:22px;border:0.5px solid #252840">🃏</div>
  <div>
    <h1 style="margin:0;font-size:22px;font-weight:700">The Nasty Model</h1>
    <p style="color:#6b7280;margin:0;font-size:12px">Screener TCG · Prix live TCGPlayer · Valeurs en C$</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Fetch + build data ───────────────────────
prog = st.empty()
rows = []
total = len(st.session_state.cards)

for idx, c in enumerate(st.session_state.cards):
    key = f"{c['id']}_{c['set']}"
    if key not in st.session_state.api_cache:
        prog.markdown(f'<div style="color:#6b7280;font-size:12px">⏳ Chargement données live... {idx+1}/{total}</div>', unsafe_allow_html=True)
        api_card = fetch_card_api(c["id"], c["set"])
        st.session_state.api_cache[key] = {
            "img": get_img(api_card),
            "live_price": get_tcg_price(api_card),
            "ts": datetime.now().isoformat()
        }
        save_json(CACHE_FILE, st.session_state.api_cache)
    cached    = st.session_state.api_cache[key]
    img_url   = cached.get("img","")
    live_price= cached.get("live_price")
    price     = live_price if live_price and live_price > 0 else c.get("price",0)

    nps     = calc_nps(c)
    st_code = SETS.get(c["set"],{}).get("status","in")
    gp,gc   = get_gain({**c,"price":price}, days)
    gp1,_   = get_gain({**c,"price":price}, 1)
    gp7,_   = get_gain({**c,"price":price}, 7)
    gp30,_  = get_gain({**c,"price":price}, 30)
    gp90,_  = get_gain({**c,"price":price}, 90)
    signal  = calc_signal(nps, gp, st_code)
    demand  = min(99, int(nps*0.82 + c.get("vel",0.5)*18))

    rows.append({**c, "price":price, "img_url":img_url, "nps":nps,
                 "gain_pct":gp, "gain_cad":gc, "gp1":gp1, "gp7":gp7, "gp30":gp30, "gp90":gp90,
                 "signal":signal, "status":st_code,
                 "set_name":SETS.get(c["set"],{}).get("name",c["set"]),
                 "demand":demand, "live": live_price is not None and live_price > 0})

prog.empty()
df = pd.DataFrame(rows)

# ── Apply filters ────────────────────────────

# Mode Show Day : gain 7j > 10% + signal sous-évalué
if show_day_mode:
    df = df[(df["gp7"] >= 10) & (df["signal"] == "sous")]

# Prix
if prix_min > 0:   df = df[df["price"] >= prix_min]
if prix_max < 5000: df = df[df["price"] <= prix_max]

# % gain
if gain_min > 0:   df = df[df["gain_pct"] >= gain_min]
if gain_max < 200: df = df[df["gain_pct"] <= gain_max]

# Recherche texte
if search:
    q = search.lower()
    df = df[df["name"].str.lower().str.contains(q) | df["set"].str.lower().str.contains(q) |
            df["set_name"].str.lower().str.contains(q) | df["rarity"].str.lower().str.contains(q)]

if set_filter != "Tous":
    code = set_filter.split("(")[-1].rstrip(")")
    df = df[df["set"]==code]
if rar_filter != "Toutes": df = df[df["rarity"]==rar_filter]
if tier_filter != "Tous":  df = df[df["tier"]==tier_filter]
sig_map={"Sous-évaluées":"sous","Surévaluées":"sur","Prix juste":"juste"}
if sig_filter != "Tous":   df = df[df["signal"]==sig_map[sig_filter]]

sort_map={"% gain":("gain_pct",False),"$ gain":("gain_cad",False),"NPS":("nps",False),"Prix ↑":("price",True),"Prix ↓":("price",False),"Nom":("name",True)}
sk,sa = sort_map[sort_ui]
df = df.sort_values(sk,ascending=sa).reset_index(drop=True)

# ── Stats ─────────────────────────────────────
m1,m2,m3,m4,m5 = st.columns(5)
m1.metric("CARTES", len(df))
m2.metric("SOUS-ÉV. 🟢", int((df["signal"]=="sous").sum()))
m3.metric("SUR-ÉV. 🔴",  int((df["signal"]=="sur").sum()))
m4.metric("NPS MOYEN", int(df["nps"].mean()) if len(df) else 0)
live_pct = int(df["live"].sum()/len(df)*100) if len(df) else 0
m5.metric("PRIX LIVE", f"{live_pct}%")

if show_day_mode:
    total_cad = df["price"].sum()
    st.markdown(f"""
    <div style="background:#1a0a3e;border:1px solid #7c3aed;border-radius:10px;padding:12px 16px;margin:10px 0;display:flex;align-items:center;gap:12px">
      <span style="font-size:22px">⚡</span>
      <div>
        <div style="font-weight:700;color:#c084fc;font-size:14px">MODE SHOW DAY ACTIVÉ</div>
        <div style="color:#a78bfa;font-size:12px">{len(df)} cartes avec gain 7j ≥ 10% et signal sous-évalué · Valeur totale: C${total_cad:,.0f}</div>
      </div>
    </div>""", unsafe_allow_html=True)

st.markdown("<div style='height:6px'></div>",unsafe_allow_html=True)

# ── Column headers ─────────────────────────
period_label = {1:"24h",3:"3j",7:"7j",30:"1M",90:"3M",180:"6M"}[days]
st.markdown(f"""
<div class="card-row hdr">
  <div></div><div>CARTE</div>
  <div style="text-align:right">PRIX C$</div>
  <div style="text-align:right">% {period_label}</div>
  <div style="text-align:right">C$ {period_label}</div>
  <div style="text-align:right">% 24H</div>
  <div style="text-align:right">% 7J</div>
  <div style="text-align:right">% 1M</div>
  <div style="text-align:right">% 3M</div>
  <div style="text-align:center">SIGNAL</div>
  <div style="text-align:right">NPS</div>
</div>""", unsafe_allow_html=True)

# ── Card rows ──────────────────────────────
def make_row(row, rank):
    gc_str = f'+C${row["gain_cad"]:.0f}' if row["gain_cad"]>=0 else f'-C${abs(row["gain_cad"]):.0f}'
    gc_clr = "#4ade80" if row["gain_cad"]>=0 else "#f87171"
    dc     = "#4ade80" if row["demand"]>75 else "#fbbf24" if row["demand"]>50 else "#f87171"
    img_html = f'<img src="{row["img_url"]}" class="cimg" onerror="this.style.display=\'none\';this.nextSibling.style.display=\'flex\'" /><div class="cimg-ph" style="display:none">🃏</div>' if row["img_url"] else '<div class="cimg-ph">🃏</div>'
    pump_badge = '<span class="pump-badge">🔥 PUMP</span>' if row["gp1"] > 5 else ""
    show_badge = '<span class="show-badge">⚡ SHOW</span>' if row["gp7"] >= 10 and row["signal"]=="sous" else ""
    return f"""
<div class="card-row">
  <div>{img_html}</div>
  <div>
    <div class="cname">{row['name']}{pump_badge}{show_badge}</div>
    <div class="csub">{row['set_name']} · {rar_pill(row['rarity'])} · {tier_pill(row['tier'])}</div>
    <div class="dem-wrap"><div class="dem-bg"><div class="dem-fg" style="width:{row['demand']}%;background:{dc}"></div></div><span class="dem-pct" style="color:{dc}">{row['demand']}%</span></div>
  </div>
  <div class="cprice">C${row['price']:.0f}</div>
  <div>{clr(row['gain_pct'])}</div>
  <div style="text-align:right;font-size:12px;color:{gc_clr}">{gc_str}</div>
  <div>{clr(row['gp1'])}</div>
  <div>{clr(row['gp7'])}</div>
  <div>{clr(row['gp30'])}</div>
  <div>{clr(row['gp90'])}</div>
  <div style="text-align:center">{signal_pill(row['signal'])}</div>
  {nps_cell(row['nps'])}
</div>"""

if len(df) == 0:
    st.markdown('<div style="text-align:center;padding:3rem;color:#4b5563;font-size:14px">Aucune carte ne correspond aux filtres sélectionnés.</div>', unsafe_allow_html=True)
else:
    html = "".join(make_row(r, i+1) for i,(_,r) in enumerate(df.iterrows()))
    st.markdown(f'<div style="background:#0d0f18;border-radius:12px;border:0.5px solid #252840;overflow:hidden">{html}</div>', unsafe_allow_html=True)

# ── Export liste show ──────────────────────
st.markdown("<hr>",unsafe_allow_html=True)
with st.expander("📋  Exporter liste d'achat show"):
    show_cards = df[(df["gp7"] >= 10) & (df["signal"]=="sous")].copy() if not show_day_mode else df.copy()
    if len(show_cards) > 0:
        export_df = show_cards[["name","set_name","rarity","tier","price","gp7","gp30","nps","signal"]].copy()
        export_df.columns = ["Carte","Set","Rareté","Tier","Prix C$","Gain 7j %","Gain 30j %","NPS","Signal"]
        export_df["Prix cible (offre -15%)"] = (export_df["Prix C$"] * 0.85).round(0).astype(int)
        st.dataframe(export_df, use_container_width=True)
        csv = export_df.to_csv(index=False)
        st.download_button("⬇️ Télécharger CSV", data=csv, file_name=f"show_list_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv")
    else:
        st.info("Active le Mode Show Day ou ajuste les filtres pour générer ta liste.")

with st.expander("➕  Ajouter une carte"):
    a1,a2=st.columns(2)
    with a1:
        nn=st.text_input("Nom"); ns=st.selectbox("Set",list(SETS.keys()),format_func=lambda k:f"{SETS[k]['name']} ({k})")
        nr=st.selectbox("Rareté",["SIR","ALT","IR","GG","SHV","FA","RR","GOLD","HOLO","EX"]); nt=st.selectbox("Tier",["S","A","B","C"])
    with a2:
        np_=st.number_input("Prix C$",min_value=0.0,step=0.5); np7=st.number_input("Prix 7j C$",min_value=0.0,step=0.5)
        np30=st.number_input("Prix 30j C$",min_value=0.0,step=0.5); np90=st.number_input("Prix 90j C$",min_value=0.0,step=0.5)
        nsat=st.number_input("Saturation PSA10",0.0,1.0,0.06,0.01); narb=st.number_input("Arbitrage JP/EN",0.0,1.0,0.50,0.01)
    if st.button("Ajouter",type="primary"):
        if nn and np_>0:
            st.session_state.cards.append({"id":f"c-{datetime.now().strftime('%Y%m%d%H%M%S')}","name":nn,"set":ns,"rarity":nr,"tier":nt,
                "price":np_,"p1":np_*0.998,"p3":np_,"p7":np7 if np7>0 else np_,
                "p30":np30 if np30>0 else np_,"p90":np90 if np90>0 else np_,"p180":np_,
                "sat":nsat,"arb":narb,"vel":0.50,"whale":0.45,"cross":0.52,"soc":0.50,"rep":0.25,"stab":0.55})
            save_json(DATA_FILE, st.session_state.cards)
            st.success(f"✅ {nn} ajoutée !"); st.rerun()

with st.expander("⚙️  Paramètres"):
    cc1,cc2=st.columns(2)
    with cc1:
        if st.button("Réinitialiser cartes"):
            st.session_state.cards=ALL_CARDS.copy(); save_json(DATA_FILE,st.session_state.cards); st.rerun()
        if st.button("Vider cache"):
            st.session_state.api_cache={}; save_json(CACHE_FILE,{}); st.cache_data.clear(); st.rerun()
    with cc2:
        st.download_button("Exporter JSON",data=json.dumps(st.session_state.cards,indent=2,ensure_ascii=False),file_name="nasty_model.json",mime="application/json")

st.markdown(f'<p style="color:#1a1d2e;font-size:11px;text-align:center;margin-top:1rem">The Nasty Model · {len(st.session_state.cards)} cartes · C$ · {datetime.now().strftime("%Y-%m-%d")}</p>',unsafe_allow_html=True)
