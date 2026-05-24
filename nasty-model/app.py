import streamlit as st
import pandas as pd
import numpy as np
import json
import os
import requests
import time
from datetime import datetime, timedelta
from cards_data import ALL_CARDS

st.set_page_config(
    page_title="The Nasty Model",
    page_icon="🃏",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background-color: #0d0f18; color: #e8e8e8; }
  .block-container { padding: 1.5rem 2rem; max-width: 1600px; }
  section[data-testid="stSidebar"] { background:#0d0f18; }
  h1,h2,h3 { color:#fff; }
  div[data-testid="metric-container"] {
    background:#161928; border:0.5px solid #252840; border-radius:10px; padding:.65rem 1rem;
  }
  div[data-testid="metric-container"] label { color:#6b7280 !important; font-size:11px; letter-spacing:.04em; text-transform:uppercase; }
  div[data-testid="metric-container"] [data-testid="stMetricValue"] { color:#fff; font-size:20px; font-weight:600; }
  .stTextInput>div>div>input { background:#161928 !important; color:#e8e8e8 !important; border-color:#252840 !important; border-radius:8px !important; }
  .stSelectbox>div>div { background:#161928 !important; color:#e8e8e8 !important; border-color:#252840 !important; }
  .stButton>button { background:#161928; color:#e8e8e8; border:0.5px solid #252840; border-radius:8px; font-size:12px; padding:5px 12px; }
  .stButton>button:hover { background:#252840; }
  .stButton>button[kind="primary"] { background:#1d4ed8; border-color:#1d4ed8; color:#fff; }
  [data-testid="stExpander"] { background:#161928; border:0.5px solid #252840; border-radius:10px; }
  hr { border-color:#1a1d2e; }

  .card-row {
    display:grid;
    grid-template-columns: 64px 1fr 100px 90px 80px 80px 80px 80px 80px 110px 80px;
    align-items:center; gap:0 10px; padding:8px 14px;
    border-bottom:0.5px solid #13151f; transition:background .1s;
  }
  .card-row:hover { background:#161928; border-radius:6px; }
  .card-row.hdr {
    font-size:11px; color:#4b5563; font-weight:500; letter-spacing:.05em;
    text-transform:uppercase; padding:7px 14px; border-bottom:0.5px solid #252840;
  }
  .cimg { width:56px; height:78px; object-fit:cover; border-radius:5px; }
  .cimg-ph { width:56px; height:78px; border-radius:5px; background:#1a1d2e; display:flex; align-items:center; justify-content:center; font-size:18px; }
  .cname { font-weight:600; color:#fff; font-size:13px; line-height:1.3; }
  .csub  { font-size:11px; color:#6b7280; margin-top:2px; }
  .cprice { font-weight:600; color:#fff; font-size:14px; text-align:right; white-space:nowrap; }
  .pos { color:#4ade80; font-weight:500; font-size:12px; text-align:right; }
  .neg { color:#f87171; font-weight:500; font-size:12px; text-align:right; }
  .neu { color:#6b7280; font-size:12px; text-align:right; }
  .dem-wrap { display:flex; align-items:center; gap:5px; margin-top:3px; }
  .dem-bg { flex:1; background:#1a1d2e; border-radius:3px; height:3px; overflow:hidden; }
  .dem-fg { height:100%; border-radius:3px; }
  .dem-pct { font-size:11px; font-weight:500; min-width:28px; text-align:right; }
  .sig { display:inline-block; font-size:10px; padding:3px 9px; border-radius:20px; font-weight:600; white-space:nowrap; }
  .sous { background:#14532d; color:#4ade80; }
  .sur  { background:#450a0a; color:#f87171; }
  .juste{ background:#451a03; color:#fbbf24; }
  .npsv { font-weight:700; font-size:14px; text-align:right; }
  .ng { color:#4ade80; } .na { color:#fbbf24; } .nr { color:#f87171; }
  .pill { display:inline-block; font-size:10px; padding:2px 6px; border-radius:10px; font-weight:500; margin-right:2px; }
  .p-sir  { background:#2e1065; color:#c084fc; }
  .p-alt  { background:#0c1a3a; color:#60a5fa; }
  .p-ir   { background:#042f2e; color:#2dd4bf; }
  .p-shv  { background:#451a03; color:#fbbf24; }
  .p-fa   { background:#1f2937; color:#9ca3af; }
  .p-rr   { background:#450a0a; color:#f87171; }
  .p-gold { background:#451a03; color:#fbbf24; }
  .p-gg   { background:#0c1a3a; color:#60a5fa; }
  .p-def  { background:#1f2937; color:#9ca3af; }
  .p-s    { background:#2e1065; color:#c084fc; }
  .p-a    { background:#0c1a3a; color:#60a5fa; }
  .p-b    { background:#042f2e; color:#2dd4bf; }
  .p-c    { background:#1f2937; color:#9ca3af; }
  .live-badge { display:inline-block; background:#14532d; color:#4ade80; font-size:10px; padding:2px 7px; border-radius:10px; font-weight:600; margin-left:8px; }
  .stale-badge { display:inline-block; background:#451a03; color:#fbbf24; font-size:10px; padding:2px 7px; border-radius:10px; font-weight:600; margin-left:8px; }
</style>
""", unsafe_allow_html=True)

USD_CAD = 1.364
CACHE_FILE = "data/price_cache.json"
CARD_DB_FILE = "data/card_db.json"
DATA_FILE = "data/cards.json"

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
        with open(path,"r") as f:
            return json.load(f)
    return default

def save_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,"w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ── Pokemon TCG API (no key = 1000 req/day free) ─────────────────────────
@st.cache_data(ttl=3600)
def fetch_card_from_api(card_name, set_code):
    """Fetch card data from pokemontcg.io — includes image + TCGPlayer prices"""
    tcg_id = SETS.get(set_code, {}).get("tcg_id", "")
    if not tcg_id:
        return None
    try:
        # Search by name + set
        clean_name = card_name.replace(" (SIR)","").replace(" (Alt Art)","").replace(" (IR)","").replace(" (Rainbow)","").replace(" (Full Art)","").replace(" (Shiny)","").split("(")[0].strip()
        url = f"https://api.pokemontcg.io/v2/cards?q=name:\"{clean_name}\" set.id:{tcg_id}&pageSize=10&orderBy=-tcgplayer.prices.holofoil.market"
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            cards = r.json().get("data", [])
            if cards:
                return cards[0]
    except Exception:
        pass
    return None

@st.cache_data(ttl=86400)
def fetch_all_cards_for_set(set_tcg_id):
    """Fetch all cards for a set — images + prices"""
    try:
        url = f"https://api.pokemontcg.io/v2/cards?q=set.id:{set_tcg_id}&pageSize=250"
        r = requests.get(url, timeout=15)
        if r.status_code == 200:
            return r.json().get("data", [])
    except Exception:
        pass
    return []

def get_tcg_price(api_card):
    """Extract best price from TCGPlayer data, convert to CAD"""
    if not api_card:
        return None
    prices = api_card.get("tcgplayer", {}).get("prices", {})
    # Try holofoil first, then normal, then 1stEditionHolofoil, then reverseHolofoil
    for ptype in ["holofoil","1stEditionHolofoil","reverseHolofoil","normal","unlimitedHolofoil"]:
        p = prices.get(ptype, {})
        market = p.get("market") or p.get("mid")
        if market and market > 0:
            return round(market * USD_CAD, 2)
    return None

def get_image_url(api_card):
    if api_card:
        return api_card.get("images", {}).get("large") or api_card.get("images", {}).get("small")
    return None

def calc_nps(c):
    st_   = SETS.get(c["set"],{}).get("status","in")
    pv    = PRINT_SCORE.get(st_,0.2)
    tv    = TIER_SCORE.get(c.get("tier","B"),0.3)
    sat   = max(0.01, c.get("sat",0.07))
    w     = ((1-sat)*0.20 + c.get("arb",0.5)*0.18 + c.get("vel",0.5)*0.15 + pv*0.25 +
              tv*0.12 + (1-c.get("rep",0.3))*0.10 + c.get("stab",0.6)*0.08 +
              c.get("whale",0.4)*0.06 + c.get("cross",0.5)*0.05 + c.get("soc",0.5)*0.04)
    hype  = 1 + c.get("cross",0.5)*0.20 + c.get("soc",0.5)*0.15
    return min(100, int((w/sat)*hype*35))

def calc_signal(nps, gain_pct, status):
    pv   = PRINT_SCORE.get(status, 0.2)
    fund = (nps/100)*0.6 + pv*0.4
    if fund > 0.72 and gain_pct < 8:  return "sous"
    if fund < 0.40 and gain_pct > 15: return "sur"
    return "juste"

def get_gain(c, days):
    key  = f"p{days}"
    past = c.get(key, c.get("price", 0))
    if past and past > 0:
        return round((c["price"]-past)/past*100, 2), round(c["price"]-past, 2)
    return 0.0, 0.0

def rar_pill(r):
    m={"SIR":"p-sir","ALT":"p-alt","IR":"p-ir","GG":"p-gg","SHV":"p-shv",
       "SHINING":"p-shv","CLASSIC":"p-gold","FA":"p-fa","RR":"p-rr","GOLD":"p-gold"}
    return f'<span class="pill {m.get(r,"p-def")}">{r}</span>'

def tier_pill(t):
    return f'<span class="pill p-{t.lower()}">{t}</span>'

def gain_cell(v, is_cad=False):
    sfx = " C$" if is_cad else "%"
    fmt = f"+{abs(v):.0f}" if is_cad else f"+{v:.1f}"
    if v > 0:  return f'<div class="pos">{fmt}{sfx}</div>'
    if v < 0:
        fmt2 = f"-{abs(v):.0f}" if is_cad else f"{v:.1f}"
        return f'<div class="neg">{fmt2}{sfx}</div>'
    return f'<div class="neu">0{"C$" if is_cad else "%"}</div>'

def signal_pill(s):
    labels={"sous":"SOUS-ÉV.","sur":"SUR-ÉV.","juste":"PRIX JUSTE"}
    return f'<span class="sig {s}">{labels[s]}</span>'

def nps_cell(n):
    c="ng" if n>=85 else "na" if n>=65 else "nr"
    return f'<div class="npsv {c}">{n}</div>'

# ── Session state ─────────────────────────────
if "cards" not in st.session_state:
    st.session_state.cards = load_json(DATA_FILE, ALL_CARDS.copy())
if "period" not in st.session_state:
    st.session_state.period = 7
if "api_cache" not in st.session_state:
    st.session_state.api_cache = load_json(CACHE_FILE, {})
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = None

# ── Header ────────────────────────────────────
col_h1, col_h2 = st.columns([4,1])
with col_h1:
    st.markdown("""
    <div style="display:flex;align-items:center;gap:14px;margin-bottom:1rem">
      <div style="width:48px;height:48px;background:#161928;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:22px;border:0.5px solid #252840">🃏</div>
      <div>
        <h1 style="margin:0;font-size:22px;font-weight:700">The Nasty Model</h1>
        <p style="color:#6b7280;margin:0;font-size:12px">Screener TCG · Prix live TCGPlayer · Valeurs en C$</p>
      </div>
    </div>
    """, unsafe_allow_html=True)

with col_h2:
    st.markdown("<div style='padding-top:8px'>",unsafe_allow_html=True)
    if st.button("🔄 Refresh prix live", type="primary"):
        st.cache_data.clear()
        st.session_state.api_cache = {}
        st.session_state.last_refresh = datetime.now().strftime("%H:%M")
        st.rerun()
    if st.session_state.last_refresh:
        st.markdown(f'<span class="live-badge">Live · {st.session_state.last_refresh}</span>', unsafe_allow_html=True)
    st.markdown("</div>",unsafe_allow_html=True)

# ── Controls ──────────────────────────────────
c1,c2,c3,c4 = st.columns([3,2,1.5,1.8])
with c1:
    search = st.text_input("","",placeholder="🔍  Rechercher carte, set, rareté...",label_visibility="collapsed")
with c2:
    set_opts = ["Tous les sets"] + [f"{v['name']} ({k})" for k,v in SETS.items()]
    set_filter = st.selectbox("Set",set_opts,label_visibility="collapsed")
with c3:
    rar_filter = st.selectbox("Rareté",["Toutes","SIR","ALT","IR","GG","SHV","SHINING","CLASSIC","FA","RR","GOLD","HOLO","EX"],label_visibility="collapsed")
with c4:
    sig_filter = st.selectbox("Signal",["Tous","Sous-évaluées","Surévaluées","Prix juste"],label_visibility="collapsed")

# Period selector
period_labels = ["24h","3j","7j","1M","3M","6M"]
period_days   = [1,3,7,30,90,180]
pcols = st.columns(len(period_labels)+4)
pcols[0].markdown('<span style="font-size:12px;color:#6b7280;line-height:2.2">Période:</span>',unsafe_allow_html=True)
for i,(lbl,d) in enumerate(zip(period_labels,period_days)):
    with pcols[i+1]:
        active = st.session_state.period == d
        if st.button(lbl, key=f"p{i}", type="primary" if active else "secondary"):
            st.session_state.period = d
            st.rerun()

sort_col = pcols[-3]
sort_ui = sort_col.selectbox("Trier",["% gain","$ gain","NPS","Prix ↑","Prix ↓","Nom"],label_visibility="collapsed")

days = st.session_state.period

# ── Fetch live data ───────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def get_live_card_data(card_id, card_name, set_code):
    """Returns (image_url, live_price_cad) or (None, None)"""
    api_card = fetch_card_from_api(card_name, set_code)
    if api_card:
        img = get_image_url(api_card)
        price = get_tcg_price(api_card)
        return img, price
    return None, None

# ── Build data ────────────────────────────────
progress_placeholder = st.empty()

rows = []
total = len(st.session_state.cards)
for idx, c in enumerate(st.session_state.cards):
    # Show loading progress for first run
    cache_key = f"{c['id']}_{c['set']}"

    if cache_key not in st.session_state.api_cache:
        progress_placeholder.markdown(
            f'<div style="color:#6b7280;font-size:12px">⏳ Chargement des données live... {idx+1}/{total}</div>',
            unsafe_allow_html=True
        )
        img_url, live_price = get_live_card_data(c["id"], c["name"], c["set"])
        st.session_state.api_cache[cache_key] = {
            "img": img_url,
            "live_price": live_price,
            "ts": datetime.now().isoformat()
        }
        save_json(CACHE_FILE, st.session_state.api_cache)
    else:
        cached = st.session_state.api_cache[cache_key]
        img_url    = cached.get("img")
        live_price = cached.get("live_price")

    # Use live price if available, otherwise fall back to manual price
    price = live_price if live_price and live_price > 0 else c.get("price", 0)

    nps      = calc_nps(c)
    st_code  = SETS.get(c["set"],{}).get("status","in")
    set_name = SETS.get(c["set"],{}).get("name", c["set"])
    demand   = min(99, int(nps*0.82 + c.get("vel",0.5)*18))

    # Build enriched card with live price
    card_enriched = {**c, "price": price, "img_url": img_url or ""}

    gp,gc = get_gain(card_enriched, days)
    signal = calc_signal(nps, gp, st_code)

    rows.append({
        **card_enriched,
        "nps": nps, "gain_pct": gp, "gain_cad": gc,
        "signal": signal, "set_name": set_name,
        "status": st_code, "demand": demand,
        "live": live_price is not None and live_price > 0
    })

progress_placeholder.empty()
df = pd.DataFrame(rows)

# Filters
if search:
    q=search.lower()
    df=df[df["name"].str.lower().str.contains(q)|df["set"].str.lower().str.contains(q)|
          df["set_name"].str.lower().str.contains(q)|df["rarity"].str.lower().str.contains(q)]
if set_filter != "Tous les sets":
    code = set_filter.split("(")[-1].rstrip(")")
    df = df[df["set"]==code]
if rar_filter != "Toutes":
    df = df[df["rarity"]==rar_filter]
sig_map={"Sous-évaluées":"sous","Surévaluées":"sur","Prix juste":"juste"}
if sig_filter != "Tous":
    df = df[df["signal"]==sig_map[sig_filter]]

sort_map={"% gain":("gain_pct",False),"$ gain":("gain_cad",False),"NPS":("nps",False),
          "Prix ↑":("price",True),"Prix ↓":("price",False),"Nom":("name",True)}
sk,sa = sort_map[sort_ui]
df = df.sort_values(sk,ascending=sa).reset_index(drop=True)

# ── Stats ─────────────────────────────────────
live_count = int(df["live"].sum()) if "live" in df.columns else 0
m1,m2,m3,m4,m5 = st.columns(5)
m1.metric("CARTES", len(df))
m2.metric("SOUS-ÉV. 🟢", int((df["signal"]=="sous").sum()))
m3.metric("SUR-ÉV. 🔴",  int((df["signal"]=="sur").sum()))
m4.metric("PRIX JUSTE 🟡",int((df["signal"]=="juste").sum()))
m5.metric("PRIX LIVE 🔵", f"{live_count}/{len(df)}")
st.markdown("<div style='height:12px'></div>",unsafe_allow_html=True)

# ── Column headers ────────────────────────────
period_label = {1:"24h",3:"3j",7:"7j",30:"1M",90:"3M",180:"6M"}[days]
st.markdown(f"""
<div class="card-row hdr">
  <div></div>
  <div>CARTE</div>
  <div style="text-align:right">PRIX C$</div>
  <div style="text-align:right">% {period_label}</div>
  <div style="text-align:right">C$ {period_label}</div>
  <div style="text-align:right">% 24h</div>
  <div style="text-align:right">% 7j</div>
  <div style="text-align:right">% 1M</div>
  <div style="text-align:right">% 3M</div>
  <div style="text-align:center">SIGNAL</div>
  <div style="text-align:right">NPS</div>
</div>
""",unsafe_allow_html=True)

# ── Rows ──────────────────────────────────────
def make_row(row):
    gp1,_   = get_gain(row,1)
    gp7,_   = get_gain(row,7)
    gp30,_  = get_gain(row,30)
    gp90,_  = get_gain(row,90)
    gpm,gcm = get_gain(row,days)

    def clr(v):
        if v>0:  return f'<span class="pos">+{v:.1f}%</span>'
        if v<0:  return f'<span class="neg">{v:.1f}%</span>'
        return '<span class="neu">—</span>'

    gc_str = f'+C${gcm:.0f}' if gcm>=0 else f'-C${abs(gcm):.0f}'
    gc_clr = "#4ade80" if gcm>=0 else "#f87171"
    dc     = "#4ade80" if row["demand"]>75 else "#fbbf24" if row["demand"]>50 else "#f87171"
    live_dot = '<span style="color:#4ade80;font-size:8px;vertical-align:middle">●</span> ' if row.get("live") else ""

    if row["img_url"]:
        img_html = f'<img src="{row["img_url"]}" class="cimg" onerror="this.style.display=\'none\';this.nextSibling.style.display=\'flex\'" /><div class="cimg-ph" style="display:none">🃏</div>'
    else:
        img_html = '<div class="cimg-ph">🃏</div>'

    return f"""
<div class="card-row">
  <div>{img_html}</div>
  <div>
    <div class="cname">{live_dot}{row['name']}</div>
    <div class="csub">{row['set_name']} · {rar_pill(row['rarity'])} · {tier_pill(row['tier'])}</div>
    <div class="dem-wrap">
      <div class="dem-bg"><div class="dem-fg" style="width:{row['demand']}%;background:{dc}"></div></div>
      <span class="dem-pct" style="color:{dc}">{row['demand']}%</span>
    </div>
  </div>
  <div class="cprice">C${row['price']:.0f}</div>
  <div>{clr(gpm)}</div>
  <div style="text-align:right;font-size:12px;color:{gc_clr}">{gc_str}</div>
  <div>{clr(gp1)}</div>
  <div>{clr(gp7)}</div>
  <div>{clr(gp30)}</div>
  <div>{clr(gp90)}</div>
  <div style="text-align:center">{signal_pill(row['signal'])}</div>
  {nps_cell(row['nps'])}
</div>"""

html = "".join(make_row(r) for _,r in df.iterrows())
st.markdown(f'<div style="background:#0d0f18;border-radius:12px;border:0.5px solid #252840;overflow:hidden">{html}</div>',unsafe_allow_html=True)

# ── Upside ────────────────────────────────────
st.markdown("<hr>",unsafe_allow_html=True)
st.markdown("### 🚀 Upside potential")
upside = df[df["gain_pct"]>0].sort_values("nps",ascending=False).head(5)
for i,(_,row) in enumerate(upside.iterrows()):
    cls  = "card-upside-top" if i==0 else "card-upside"
    border = "1.5px solid #1d4ed8" if i==0 else "0.5px solid #252840"
    badge = '<span style="background:#0c1a3a;color:#60a5fa;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:600">⭐ meilleur upside</span> ' if i==0 else ""
    nc = "#4ade80" if row["nps"]>=85 else "#fbbf24" if row["nps"]>=65 else "#f87171"
    bars=[("PSA10 sat.",round((1-row["sat"])*100),"#60a5fa"),("JP/EN arb.",round(row["arb"]*100),"#4ade80"),
          ("print",round(PRINT_SCORE.get(row["status"],0.2)*100),"#fbbf24"),("whales",round(row["whale"]*100),"#c084fc")]
    bh="".join([f'<div style="display:flex;align-items:center;gap:5px;margin-bottom:2px"><span style="font-size:11px;color:#4b5563;min-width:72px">{l}</span><div style="flex:1;background:#0d0f18;border-radius:3px;height:3px;overflow:hidden"><div style="width:{v}%;height:100%;background:{c};border-radius:3px"></div></div><span style="font-size:10px;color:#4b5563;min-width:24px;text-align:right">{v}%</span></div>' for l,v,c in bars])
    img_part = f'<img src="{row["img_url"]}" style="width:38px;height:52px;object-fit:cover;border-radius:4px;flex-shrink:0" onerror="this.style.display=\'none\'">' if row.get("img_url") else ""
    st.markdown(f'<div style="background:#161928;border:{border};border-radius:10px;padding:.85rem 1rem;margin-bottom:8px"><div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px">{badge}{img_part}<span style="font-size:13px;font-weight:600;color:#fff;flex:1">{row["name"]} <span style="color:#4b5563;font-weight:400;font-size:11px">{row["set_name"]}</span></span><span style="color:#4ade80;font-size:12px;font-weight:500">+{row["gain_pct"]:.1f}%</span><span style="font-size:17px;font-weight:700;color:{nc}">{row["nps"]}<span style="font-size:11px;color:#4b5563;font-weight:400">/100</span></span></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:0 14px">{bh}</div></div>',unsafe_allow_html=True)

# ── Add / Settings ────────────────────────────
st.markdown("<hr>",unsafe_allow_html=True)
with st.expander("➕  Ajouter une carte"):
    a1,a2=st.columns(2)
    with a1:
        nn=st.text_input("Nom"); ns=st.selectbox("Set",list(SETS.keys()),format_func=lambda k:f"{SETS[k]['name']} ({k})")
        nr=st.selectbox("Rareté",["SIR","ALT","IR","GG","SHV","FA","RR","GOLD","HOLO","EX"]); nt=st.selectbox("Tier",["S","A","B","C"])
    with a2:
        np_=st.number_input("Prix C$",min_value=0.0,step=0.5)
        np1=st.number_input("Prix 24h C$",min_value=0.0,step=0.5); np7=st.number_input("Prix 7j C$",min_value=0.0,step=0.5)
        np30=st.number_input("Prix 30j C$",min_value=0.0,step=0.5); np90=st.number_input("Prix 90j C$",min_value=0.0,step=0.5)
        nsat=st.number_input("Saturation PSA10",0.0,1.0,0.06,0.01); narb=st.number_input("Arbitrage JP/EN",0.0,1.0,0.50,0.01)
    if st.button("Ajouter",type="primary"):
        if nn and np_>0:
            st.session_state.cards.append({"id":f"c-{datetime.now().strftime('%Y%m%d%H%M%S')}","name":nn,"set":ns,"rarity":nr,"tier":nt,
                "price":np_,"p1":np1 if np1>0 else np_*0.998,"p3":np_,"p7":np7 if np7>0 else np_,
                "p30":np30 if np30>0 else np_,"p90":np90 if np90>0 else np_,"p180":np_,
                "sat":nsat,"arb":narb,"vel":0.50,"whale":0.45,"cross":0.52,"soc":0.50,"rep":0.25,"stab":0.55})
            save_json(DATA_FILE, st.session_state.cards)
            st.success(f"✅ {nn} ajoutée !"); st.rerun()

with st.expander("📂  Importer CSV"):
    st.markdown("`id, name, set, rarity, tier, price, p1, p7, p30, p90, sat, arb`")
    up=st.file_uploader("CSV",type=["csv"])
    if up:
        try:
            idf=pd.read_csv(up,skipinitialspace=True); idf.columns=idf.columns.str.strip().str.lower()
            added=0
            for _,r in idf.iterrows():
                st.session_state.cards.append({"id":str(r.get("id",f"i{added}")),"name":str(r.get("name","?")),"set":str(r.get("set","UNK")),"rarity":str(r.get("rarity","—")),"tier":str(r.get("tier","B")),
                    "price":float(r.get("price",0)),"p1":float(r.get("p1",r.get("price",0))),"p3":float(r.get("p3",r.get("price",0))),"p7":float(r.get("p7",r.get("price",0))),
                    "p30":float(r.get("p30",r.get("price",0))),"p90":float(r.get("p90",r.get("price",0))),"p180":float(r.get("p180",r.get("price",0))),
                    "sat":float(r.get("sat",0.06)),"arb":float(r.get("arb",0.45)),"vel":0.50,"whale":0.45,"cross":0.52,"soc":0.50,"rep":0.25,"stab":0.55}); added+=1
            save_json(DATA_FILE, st.session_state.cards)
            st.success(f"✅ {added} cartes importées !"); st.rerun()
        except Exception as e:
            st.error(f"Erreur: {e}")

with st.expander("⚙️  Paramètres"):
    cc1,cc2=st.columns(2)
    with cc1:
        if st.button("Réinitialiser cartes"):
            st.session_state.cards=ALL_CARDS.copy(); save_json(DATA_FILE,st.session_state.cards); st.success("OK"); st.rerun()
        if st.button("Vider cache prix"):
            st.session_state.api_cache={}; save_json(CACHE_FILE,{}); st.cache_data.clear(); st.success("Cache vidé"); st.rerun()
    with cc2:
        st.download_button("Exporter JSON",data=json.dumps(st.session_state.cards,indent=2,ensure_ascii=False),file_name="nasty_model.json",mime="application/json")

st.markdown(f'<p style="color:#1a1d2e;font-size:11px;text-align:center;margin-top:1.5rem">The Nasty Model · {len(st.session_state.cards)} cartes · TCGPlayer live · C$ · {datetime.now().strftime("%Y-%m-%d")}</p>',unsafe_allow_html=True)
