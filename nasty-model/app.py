import streamlit as st
import pandas as pd
import numpy as np
import json, os, requests
from datetime import datetime
from cards_data import ALL_CARDS

st.set_page_config(page_title="The Nasty Model", page_icon="🃏", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0a0b0f; color: #e2e8f0; }
.block-container { padding: 1.5rem 2rem 3rem; max-width: 1600px; }
section[data-testid="stSidebar"] { background: #0d0f1a !important; border-right: 1px solid #1e2235; }
section[data-testid="stSidebar"] label, section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] p { color: #64748b !important; font-size: 12px !important; }
section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stTextInput > div > div > input,
section[data-testid="stSidebar"] .stNumberInput > div > div > input {
  background: #12141f !important; border: 1px solid #1e2235 !important;
  color: #e2e8f0 !important; border-radius: 8px !important; font-size: 13px !important; }
.stTextInput > div > div > input, .stSelectbox > div > div, .stNumberInput > div > div > input {
  background: #12141f !important; color: #e2e8f0 !important; border: 1px solid #1e2235 !important; border-radius: 8px !important; }
.stButton > button { background: #12141f; color: #64748b; border: 1px solid #1e2235; border-radius: 8px; font-size: 12px; font-weight: 500; }
.stButton > button:hover { background: #1a1d2e; color: #e2e8f0; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg,#6366f1,#8b5cf6); border: none; color: #fff; font-weight: 600; }
[data-testid="stExpander"] { background: #0d0f1a; border: 1px solid #1e2235; border-radius: 12px; }
hr { border: none; border-top: 1px solid #1e2235; }

.tbl-wrap { background: #0d0f1a; border: 1px solid #1e2235; border-radius: 16px; overflow: hidden; margin-top: 1rem; }
.tbl-hdr {
  display: grid;
  grid-template-columns: 60px 1fr 110px 90px 80px 80px 80px 80px;
  gap: 0 8px; padding: 10px 18px;
  background: #080910; border-bottom: 1px solid #1e2235;
}
.tbl-hdr span { font-size: 10px; color: #2d3748; font-weight: 700; letter-spacing: .07em; text-transform: uppercase; }
.tbl-hdr span.r { text-align: right; display: block; }
.tbl-hdr span.c { text-align: center; display: block; }
.tbl-row {
  display: grid;
  grid-template-columns: 60px 1fr 110px 90px 80px 80px 80px 80px;
  gap: 0 8px; padding: 10px 18px;
  border-bottom: 1px solid #0c0d14; align-items: center;
  transition: background .1s;
}
.tbl-row:last-child { border-bottom: none; }
.tbl-row:hover { background: #0f1120; }
.card-img  { width: 46px; height: 64px; object-fit: cover; border-radius: 5px; box-shadow: 0 2px 10px rgba(0,0,0,.6); }
.card-ph   { width: 46px; height: 64px; border-radius: 5px; background: #12141f; display: flex; align-items: center; justify-content: center; font-size: 18px; border: 1px solid #1e2235; }
.card-name { font-weight: 600; color: #f1f5f9; font-size: 13px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 220px; }
.card-sub  { font-size: 11px; color: #334155; margin-top: 2px; }
.price     { font-size: 15px; font-weight: 700; color: #f1f5f9; text-align: right; }
.chg-up    { color: #22c55e; font-size: 12px; font-weight: 600; text-align: right; display: block; }
.chg-dn    { color: #ef4444; font-size: 12px; font-weight: 600; text-align: right; display: block; }
.chg-fl    { color: #2d3748; font-size: 12px; text-align: right; display: block; }
.supply    { display: inline-block; font-size: 10px; padding: 3px 9px; border-radius: 20px; font-weight: 700; white-space: nowrap; }
.s-tight   { background: rgba(239,68,68,.12); color: #ef4444; border: 1px solid rgba(239,68,68,.25); }
.s-watch   { background: rgba(234,179,8,.12); color: #eab308; border: 1px solid rgba(234,179,8,.25); }
.s-normal  { background: rgba(45,55,72,.4); color: #475569; border: 1px solid #1e2235; }
.pill      { display: inline-block; font-size: 10px; padding: 1px 6px; border-radius: 10px; font-weight: 600; margin-right: 2px; }
.p-sir     { background: rgba(139,92,246,.15); color: #a78bfa; border: 1px solid rgba(139,92,246,.2); }
.p-alt     { background: rgba(59,130,246,.15); color: #60a5fa; border: 1px solid rgba(59,130,246,.2); }
.p-ir      { background: rgba(20,184,166,.15); color: #2dd4bf; border: 1px solid rgba(20,184,166,.2); }
.p-shv     { background: rgba(245,158,11,.15); color: #fbbf24; border: 1px solid rgba(245,158,11,.2); }
.p-fa      { background: rgba(100,116,139,.15); color: #64748b; border: 1px solid rgba(100,116,139,.2); }
.p-rr      { background: rgba(239,68,68,.15); color: #f87171; border: 1px solid rgba(239,68,68,.2); }
.p-gold    { background: rgba(234,179,8,.15); color: #facc15; border: 1px solid rgba(234,179,8,.2); }
.p-def     { background: rgba(71,85,105,.15); color: #475569; border: 1px solid rgba(71,85,105,.2); }
.badge-pump { font-size: 9px; padding: 1px 5px; border-radius: 8px; font-weight: 700; margin-left: 4px; vertical-align: middle; background: rgba(239,68,68,.15); color: #ef4444; border: 1px solid rgba(239,68,68,.25); }
.badge-show { font-size: 9px; padding: 1px 5px; border-radius: 8px; font-weight: 700; margin-left: 4px; vertical-align: middle; background: rgba(99,102,241,.15); color: #818cf8; border: 1px solid rgba(99,102,241,.25); }
.show-banner { background: linear-gradient(135deg,#12082e,#1a0f3e); border: 1px solid #4f46e5; border-radius: 14px; padding: 14px 20px; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 16px; }
.sb-section { font-size: 10px; font-weight: 700; color: #2d3748 !important; text-transform: uppercase; letter-spacing: .08em; margin: 16px 0 6px; display: block; }
</style>
""", unsafe_allow_html=True)

USD_CAD = 1.364
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

def load_json(p,d):
    if os.path.exists(p):
        with open(p) as f: return json.load(f)
    return d
def save_json(p,d):
    os.makedirs(os.path.dirname(p),exist_ok=True)
    with open(p,"w") as f: json.dump(d,f,indent=2,ensure_ascii=False)

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_card_api(name, set_code):
    tcg_id = SETS.get(set_code,{}).get("tcg_id","")
    if not tcg_id: return None
    try:
        clean = name.replace(" (SIR)","").replace(" (Alt Art)","").replace(" (IR)","").replace(" (Rainbow)","").replace(" (Full Art)","").replace(" (Shiny)","").split("(")[0].strip()
        r = requests.get(f'https://api.pokemontcg.io/v2/cards?q=name:"{clean}" set.id:{tcg_id}&pageSize=5', timeout=8)
        if r.status_code == 200:
            cards = r.json().get("data",[])
            if cards: return cards[0]
    except: pass
    return None

def get_tcg_price(ac):
    if not ac: return None
    prices = ac.get("tcgplayer",{}).get("prices",{})
    for pt in ["holofoil","1stEditionHolofoil","reverseHolofoil","normal","unlimitedHolofoil"]:
        p = prices.get(pt,{}); m = p.get("market") or p.get("mid")
        if m and m > 0: return round(m * USD_CAD, 2)
    return None

def get_img(ac):
    if ac: return ac.get("images",{}).get("large") or ac.get("images",{}).get("small")
    return None

def get_gain(c, days):
    past = c.get(f"p{days}", c.get("price",0))
    if past and past > 0: return round((c["price"]-past)/past*100,2), round(c["price"]-past,2)
    return 0.0, 0.0

def sparkline_svg(vals, color="#22c55e", w=80, h=30):
    vals = [v for v in vals if v and v > 0]
    if len(vals) < 2: return '<div style="width:80px"></div>'
    mn,mx = min(vals),max(vals); rng = mx-mn if mx != mn else 1
    pts = [f"{round(3+(w-6)*i/(len(vals)-1),1)},{round(h-3-(h-6)*(v-mn)/rng,1)}" for i,v in enumerate(vals)]
    path = " ".join(f"{'M' if i==0 else 'L'}{p}" for i,p in enumerate(pts))
    uid = abs(hash(str(vals))) % 99999
    fill = path + f" L{w-3},{h-1} L3,{h-1} Z"
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}"><defs><linearGradient id="g{uid}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{color}" stop-opacity=".3"/><stop offset="100%" stop-color="{color}" stop-opacity="0"/></linearGradient></defs><path d="{fill}" fill="url(#g{uid})"/><path d="{path}" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def rar_pill(r):
    m = {"SIR":"p-sir","ALT":"p-alt","IR":"p-ir","GG":"p-alt","SHV":"p-shv","SHINING":"p-shv","CLASSIC":"p-gold","FA":"p-fa","RR":"p-rr","GOLD":"p-gold"}
    return f'<span class="pill {m.get(r,"p-def")}">{r}</span>'

def chg(v):
    if v > 0:  return f'<span class="chg-up">▲ +{v:.1f}%</span>'
    if v < 0:  return f'<span class="chg-dn">▼ {v:.1f}%</span>'
    return '<span class="chg-fl">—</span>'

def supply_badge(gp7, gp30):
    if gp7 > 15 or (gp7 > 8 and gp30 > 25): return '<span class="supply s-tight">Very Tight</span>'
    if gp7 > 5: return '<span class="supply s-watch">Tight</span>'
    return '<span class="supply s-normal">Normal</span>'

# ── Session ──
if "cards"     not in st.session_state: st.session_state.cards = load_json(DATA_FILE, ALL_CARDS.copy())
if "api_cache" not in st.session_state: st.session_state.api_cache = load_json(CACHE_FILE, {})

# ════ SIDEBAR ════
with st.sidebar:
    st.markdown("### 🃏 The Nasty Model")
    st.markdown("---")
    show_day = st.toggle("⚡ Mode Show Day", value=False, help="Gain 7j ≥ 10% · signal sous-évalué")

    st.markdown('<span class="sb-section">Période</span>', unsafe_allow_html=True)
    period_map = {"24h":1,"3j":3,"7j":7,"1M":30,"3M":90,"6M":180}
    period_sel = st.radio("",list(period_map.keys()),index=2,horizontal=True,label_visibility="collapsed")
    days = period_map[period_sel]

    st.markdown('<span class="sb-section">Set</span>', unsafe_allow_html=True)
    set_opts = ["Tous"] + [f"{v['name']} ({k})" for k,v in SETS.items()]
    set_filter = st.selectbox("",set_opts,label_visibility="collapsed")

    st.markdown('<span class="sb-section">Prix C$</span>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a: prix_min = st.number_input("Min",min_value=0,value=0,step=5,label_visibility="visible")
    with col_b: prix_max = st.number_input("Max",min_value=0,value=5000,step=25,label_visibility="visible")

    st.markdown('<span class="sb-section">Recherche</span>', unsafe_allow_html=True)
    search = st.text_input("",placeholder="Nom de la carte...",label_visibility="collapsed")

    st.markdown("---")
    c_total = f'<div style="font-size:11px;color:#334155;text-align:center">{len(st.session_state.cards)} cartes dans la base</div>'
    st.markdown(c_total, unsafe_allow_html=True)
    st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)
    if st.button("🔄 Refresh live",type="primary",use_container_width=True):
        st.cache_data.clear(); st.session_state.api_cache={}; save_json(CACHE_FILE,{}); st.rerun()

# ════ MAIN ════
st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;padding:1.25rem 0 1rem;border-bottom:1px solid #1e2235;margin-bottom:1.25rem">
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:36px;height:36px;background:linear-gradient(135deg,#6366f1,#8b5cf6);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:18px">🃏</div>
    <div>
      <div style="font-size:18px;font-weight:800;color:#f1f5f9;letter-spacing:-.02em">The Nasty Model</div>
      <div style="font-size:11px;color:#334155">market intelligence · pokémon TCG · C$</div>
    </div>
  </div>
  <div style="font-size:11px;color:#334155">updated {date}</div>
</div>
""".replace("{date}", datetime.now().strftime("%Y-%m-%d")), unsafe_allow_html=True)

# ── Fetch ──
prog = st.empty()
rows = []
for idx,c in enumerate(st.session_state.cards):
    key = f"{c['id']}_{c['set']}"
    if key not in st.session_state.api_cache:
        prog.markdown(f'<div style="color:#334155;font-size:12px">⏳ {idx+1}/{len(st.session_state.cards)} — chargement...</div>', unsafe_allow_html=True)
        ac = fetch_card_api(c["id"], c["set"])
        st.session_state.api_cache[key] = {"img":get_img(ac),"live_price":get_tcg_price(ac),"ts":datetime.now().isoformat()}
        save_json(CACHE_FILE, st.session_state.api_cache)
    cached = st.session_state.api_cache[key]
    price  = cached.get("live_price") or c.get("price",0)
    if price <= 0: price = c.get("price",0)
    c2 = {**c,"price":price}
    gp,gc   = get_gain(c2,days)
    gp1,_   = get_gain(c2,1); gp7,_ = get_gain(c2,7); gp30,_ = get_gain(c2,30); gp90,_ = get_gain(c2,90)
    spark   = [c2.get("p180",price),c2.get("p90",price),c2.get("p30",price),c2.get("p7",price),c2.get("p1",price),price]
    rows.append({**c2,"img_url":cached.get("img",""),"gain_pct":gp,"gain_cad":gc,
                 "gp1":gp1,"gp7":gp7,"gp30":gp30,"gp90":gp90,
                 "set_name":SETS.get(c["set"],{}).get("name",c["set"]),"spark":spark,
                 "live":cached.get("live_price") is not None})
prog.empty()
df = pd.DataFrame(rows)

# ── Filters ──
if show_day: df = df[df["gp7"] >= 10]
if prix_min > 0:   df = df[df["price"] >= prix_min]
if prix_max < 5000: df = df[df["price"] <= prix_max]
if search:
    q = search.lower()
    df = df[df["name"].str.lower().str.contains(q) | df["rarity"].str.lower().str.contains(q)]
if set_filter != "Tous":
    df = df[df["set"] == set_filter.split("(")[-1].rstrip(")")]
df = df.sort_values("gp7", ascending=False).reset_index(drop=True)

# ── Show Day Banner ──
if show_day:
    avg7 = df["gp7"].mean() if len(df) else 0
    st.markdown(f"""
    <div class="show-banner">
      <span style="font-size:26px">⚡</span>
      <div style="flex:1">
        <div style="font-size:14px;font-weight:700;color:#a78bfa">MODE SHOW DAY</div>
        <div style="font-size:12px;color:#6d5bd0;margin-top:2px">Cartes avec gain 7j ≥ 10% — opportunités que les vendeurs n'ont pas encore repriced</div>
      </div>
      <div style="text-align:center;background:rgba(99,102,241,.12);border:1px solid rgba(99,102,241,.25);border-radius:10px;padding:8px 16px">
        <div style="font-size:20px;font-weight:700;color:#a78bfa">{len(df)}</div>
        <div style="font-size:10px;color:#6d5bd0;text-transform:uppercase;letter-spacing:.06em">opportunités</div>
      </div>
      <div style="text-align:center;background:rgba(99,102,241,.12);border:1px solid rgba(99,102,241,.25);border-radius:10px;padding:8px 16px">
        <div style="font-size:20px;font-weight:700;color:#a78bfa">+{avg7:.1f}%</div>
        <div style="font-size:10px;color:#6d5bd0;text-transform:uppercase;letter-spacing:.06em">gain moy. 7j</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Section header ──
period_lbl = {1:"24h",3:"3j",7:"7j",30:"1M",90:"3M",180:"6M"}[days]
st.markdown(f"""
<div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:6px">
  <div>
    <span style="font-size:17px;font-weight:700;color:#e2e8f0">biggest market movers</span>
    <span style="font-size:11px;color:#334155;margin-left:8px">triés par gain 7j · période {period_lbl}</span>
  </div>
  <span style="font-size:11px;color:#334155">{len(df)} cartes</span>
</div>
""", unsafe_allow_html=True)

# ── Table ──
if len(df) == 0:
    st.markdown('<div style="text-align:center;padding:4rem;color:#334155;font-size:14px">Aucune carte ne correspond aux filtres.</div>', unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="tbl-wrap">
    <div class="tbl-hdr">
      <span></span>
      <span>carte</span>
      <span class="r">prix C$</span>
      <span class="c">tendance</span>
      <span class="r">% {period_lbl}</span>
      <span class="r">24h</span>
      <span class="r">7j</span>
      <span class="r">1M</span>
    </div>
    """, unsafe_allow_html=True)

    rows_html = ""
    for i,(_,row) in enumerate(df.iterrows()):
        gc_str = f'+C${row["gain_cad"]:.0f}' if row["gain_cad"] >= 0 else f'−C${abs(row["gain_cad"]):.0f}'
        gc_clr = "#22c55e" if row["gain_cad"] >= 0 else "#ef4444"
        sp_clr = "#22c55e" if row["gain_pct"] >= 0 else "#ef4444"
        img_html = f'<img src="{row["img_url"]}" class="card-img" onerror="this.style.display=\'none\';this.nextSibling.style.display=\'flex\'" /><div class="card-ph" style="display:none">🃏</div>' if row.get("img_url") else '<div class="card-ph">🃏</div>'
        bp = '<span class="badge-pump">🔥 24h</span>' if row["gp1"] > 5 else ""
        bs = '<span class="badge-show">⚡ SHOW</span>' if row["gp7"] >= 10 else ""
        live_dot = '<span style="color:#22c55e;font-size:8px;margin-right:3px">●</span>' if row.get("live") else ""
        spark = sparkline_svg(row["spark"], sp_clr)
        supply = supply_badge(row["gp7"], row["gp30"])

        rows_html += f"""
<div class="tbl-row">
  <div>{img_html}</div>
  <div>
    <div class="card-name">{live_dot}{row['name']}{bp}{bs}</div>
    <div class="card-sub">{row['set_name']} · {rar_pill(row['rarity'])}</div>
    <div style="margin-top:4px">{supply}</div>
  </div>
  <div style="text-align:right">
    <div class="price">C${row['price']:.0f}</div>
    <div style="font-size:11px;color:{gc_clr};margin-top:2px">{gc_str}</div>
  </div>
  <div style="display:flex;align-items:center;justify-content:center">{spark}</div>
  <div>{chg(row['gain_pct'])}</div>
  <div>{chg(row['gp1'])}</div>
  <div>{chg(row['gp7'])}</div>
  <div>{chg(row['gp30'])}</div>
</div>"""

    st.markdown(rows_html + "</div>", unsafe_allow_html=True)

# ── Export ──
st.markdown("<hr style='margin:1.5rem 0'>", unsafe_allow_html=True)
with st.expander("📋  Liste d'achat — export"):
    ex_df = df[df["gp7"] >= 10].copy() if not show_day else df.copy()
    if len(ex_df) > 0:
        out = ex_df[["name","set_name","rarity","price","gp7","gp30"]].copy()
        out.columns = ["Carte","Set","Rareté","Prix C$","Gain 7j %","Gain 30j %"]
        out["Offre -15%"] = (out["Prix C$"] * 0.85).round(0).astype(int)
        out["Offre -25%"] = (out["Prix C$"] * 0.75).round(0).astype(int)
        st.dataframe(out, use_container_width=True, hide_index=True)
        st.download_button("⬇️ Télécharger CSV", data=out.to_csv(index=False),
            file_name=f"show_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", type="primary")
    else:
        st.info("Active le Mode Show Day ou applique des filtres pour générer ta liste.")

with st.expander("➕  Ajouter une carte"):
    a1,a2 = st.columns(2)
    with a1:
        nn=st.text_input("Nom"); ns=st.selectbox("Set",list(SETS.keys()),format_func=lambda k:f"{SETS[k]['name']} ({k})")
        nr=st.selectbox("Rareté",["SIR","ALT","IR","GG","SHV","FA","RR","GOLD","HOLO","EX"]); nt=st.selectbox("Tier",["S","A","B","C"])
    with a2:
        np_=st.number_input("Prix C$",min_value=0.0,step=0.5); np7=st.number_input("Prix 7j C$",min_value=0.0,step=0.5)
        np30=st.number_input("Prix 30j C$",min_value=0.0,step=0.5); np90=st.number_input("Prix 90j C$",min_value=0.0,step=0.5)
        nsat=st.number_input("Sat. PSA10",0.0,1.0,0.06,0.01); narb=st.number_input("Arb. JP/EN",0.0,1.0,0.50,0.01)
    if st.button("Ajouter",type="primary"):
        if nn and np_>0:
            st.session_state.cards.append({"id":f"c-{datetime.now().strftime('%Y%m%d%H%M%S')}","name":nn,"set":ns,"rarity":nr,"tier":nt,
                "price":np_,"p1":np_*0.998,"p3":np_,"p7":np7 if np7>0 else np_,
                "p30":np30 if np30>0 else np_,"p90":np90 if np90>0 else np_,"p180":np_,
                "sat":nsat,"arb":narb,"vel":0.50,"whale":0.45,"cross":0.52,"soc":0.50,"rep":0.25,"stab":0.55})
            save_json(DATA_FILE, st.session_state.cards); st.success(f"✅ {nn} ajoutée !"); st.rerun()

with st.expander("⚙️  Paramètres"):
    p1,p2 = st.columns(2)
    with p1:
        if st.button("Réinitialiser"): st.session_state.cards=ALL_CARDS.copy(); save_json(DATA_FILE,st.session_state.cards); st.rerun()
        if st.button("Vider cache"): st.session_state.api_cache={}; save_json(CACHE_FILE,{}); st.cache_data.clear(); st.rerun()
    with p2:
        st.download_button("Exporter JSON",data=json.dumps(st.session_state.cards,indent=2,ensure_ascii=False),file_name="nasty_model.json",mime="application/json")
