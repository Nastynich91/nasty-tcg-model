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
.block-container { padding: 0 2rem 2rem; max-width: 1700px; }
section[data-testid="stSidebar"] { background: #0d0f1a !important; border-right: 1px solid #1e2235; width: 280px !important; }
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span { color: #94a3b8 !important; font-size: 12px !important; }
section[data-testid="stSidebar"] h2 { color: #f1f5f9 !important; font-size: 16px !important; font-weight: 700 !important; }
section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stTextInput > div > div > input,
section[data-testid="stSidebar"] .stNumberInput > div > div > input {
  background: #161928 !important; border: 1px solid #2a3050 !important;
  color: #e2e8f0 !important; border-radius: 8px !important; font-size: 13px !important;
}
section[data-testid="stSidebar"] .stSlider { padding: 0 4px; }
.stTextInput > div > div > input { background: #161928 !important; color: #e2e8f0 !important; border: 1px solid #2a3050 !important; border-radius: 8px !important; }
.stSelectbox > div > div { background: #161928 !important; color: #e2e8f0 !important; border: 1px solid #2a3050 !important; border-radius: 8px !important; }
.stNumberInput > div > div > input { background: #161928 !important; color: #e2e8f0 !important; border: 1px solid #2a3050 !important; }
.stButton > button { background: #161928; color: #94a3b8; border: 1px solid #2a3050; border-radius: 8px; font-size: 12px; font-weight: 500; transition: all .15s; }
.stButton > button:hover { background: #1e2235; color: #e2e8f0; border-color: #3a4060; }
.stButton > button[kind="primary"] { background: linear-gradient(135deg,#6366f1,#8b5cf6); border: none; color: #fff; font-weight: 600; }
.stButton > button[kind="primary"]:hover { background: linear-gradient(135deg,#4f52d9,#7c3aed); }
div[data-testid="metric-container"] { background: #0d0f1a; border: 1px solid #1e2235; border-radius: 12px; padding: .85rem 1.1rem; }
div[data-testid="metric-container"] label { color: #475569 !important; font-size: 10px !important; letter-spacing: .08em; text-transform: uppercase; font-weight: 600; }
div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #f1f5f9; font-size: 22px; font-weight: 700; }
[data-testid="stExpander"] { background: #0d0f1a; border: 1px solid #1e2235; border-radius: 12px; }
hr { border: none; border-top: 1px solid #1e2235; margin: 1.25rem 0; }

/* ── NAV BAR ── */
.nav-bar { display:flex; align-items:center; justify-content:space-between; padding:1rem 0 1.5rem; border-bottom:1px solid #1e2235; margin-bottom:1.5rem; }
.nav-logo { display:flex; align-items:center; gap:10px; }
.nav-logo-icon { width:38px; height:38px; background:linear-gradient(135deg,#6366f1,#8b5cf6); border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:18px; }
.nav-title { font-size:18px; font-weight:800; color:#f1f5f9; letter-spacing:-.02em; }
.nav-sub { font-size:11px; color:#475569; font-weight:500; }
.nav-badge { background:#0d1a2e; border:1px solid #1e3a5f; color:#60a5fa; font-size:11px; padding:4px 10px; border-radius:20px; font-weight:600; }

/* ── SHOW DAY BANNER ── */
.show-banner { background:linear-gradient(135deg,#1a0a3e,#1e1040); border:1px solid #6366f1; border-radius:14px; padding:14px 20px; margin-bottom:1.25rem; display:flex; align-items:center; gap:14px; }
.show-banner-icon { font-size:28px; }
.show-banner-title { font-size:15px; font-weight:700; color:#a78bfa; }
.show-banner-sub { font-size:12px; color:#7c3aed; margin-top:2px; }
.show-stat { background:rgba(99,102,241,.15); border:1px solid rgba(99,102,241,.3); border-radius:8px; padding:6px 14px; text-align:center; }
.show-stat-v { font-size:18px; font-weight:700; color:#a78bfa; }
.show-stat-l { font-size:10px; color:#7c3aed; text-transform:uppercase; letter-spacing:.06em; }

/* ── TABLE ── */
.tbl-wrap { background:#0d0f1a; border:1px solid #1e2235; border-radius:16px; overflow:hidden; }
.tbl-hdr { display:grid; grid-template-columns:70px 1fr 100px 85px 80px 80px 85px 85px 85px 115px 78px; gap:0 6px; padding:10px 16px; background:#080910; border-bottom:1px solid #1e2235; }
.tbl-hdr-cell { font-size:10px; color:#334155; font-weight:700; letter-spacing:.07em; text-transform:uppercase; }
.tbl-hdr-cell.r { text-align:right; }
.tbl-hdr-cell.c { text-align:center; }
.tbl-row { display:grid; grid-template-columns:70px 1fr 100px 85px 80px 80px 85px 85px 85px 115px 78px; gap:0 6px; padding:10px 16px; border-bottom:1px solid #0f1118; align-items:center; transition:background .1s; cursor:default; }
.tbl-row:last-child { border-bottom:none; }
.tbl-row:hover { background:#111320; }

/* Card cell */
.card-img { width:48px; height:67px; object-fit:cover; border-radius:5px; box-shadow:0 2px 8px rgba(0,0,0,.5); }
.card-ph { width:48px; height:67px; border-radius:5px; background:#161928; display:flex; align-items:center; justify-content:center; font-size:20px; border:1px solid #1e2235; }
.card-name { font-weight:600; color:#f1f5f9; font-size:13px; line-height:1.3; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; max-width:200px; }
.card-meta { font-size:11px; color:#475569; margin-top:2px; }
.demand-row { display:flex; align-items:center; gap:5px; margin-top:4px; }
.demand-track { flex:1; height:3px; background:#1e2235; border-radius:2px; overflow:hidden; }
.demand-fill { height:100%; border-radius:2px; }
.demand-lbl { font-size:10px; font-weight:600; min-width:26px; text-align:right; }

/* Price & change cells */
.price-cell { font-size:14px; font-weight:700; color:#f1f5f9; text-align:right; }
.price-sub { font-size:10px; color:#334155; text-align:right; margin-top:1px; }
.chg { font-size:12px; font-weight:600; text-align:right; }
.chg.up { color:#22c55e; }
.chg.dn { color:#ef4444; }
.chg.fl { color:#334155; }

/* Sparkline container */
.spark-cell { display:flex; align-items:center; justify-content:flex-start; }

/* Badges */
.pill { display:inline-block; font-size:10px; padding:2px 7px; border-radius:20px; font-weight:600; white-space:nowrap; margin-right:2px; }
.p-sir { background:rgba(139,92,246,.2); color:#a78bfa; border:1px solid rgba(139,92,246,.3); }
.p-alt { background:rgba(59,130,246,.2); color:#60a5fa; border:1px solid rgba(59,130,246,.3); }
.p-ir  { background:rgba(20,184,166,.2); color:#2dd4bf; border:1px solid rgba(20,184,166,.3); }
.p-shv { background:rgba(245,158,11,.2); color:#fbbf24; border:1px solid rgba(245,158,11,.3); }
.p-fa  { background:rgba(100,116,139,.2); color:#94a3b8; border:1px solid rgba(100,116,139,.3); }
.p-rr  { background:rgba(239,68,68,.2); color:#f87171; border:1px solid rgba(239,68,68,.3); }
.p-gold{ background:rgba(234,179,8,.2); color:#facc15; border:1px solid rgba(234,179,8,.3); }
.p-gg  { background:rgba(59,130,246,.2); color:#60a5fa; border:1px solid rgba(59,130,246,.3); }
.p-def { background:rgba(100,116,139,.15); color:#64748b; border:1px solid rgba(100,116,139,.2); }
.p-s   { background:rgba(139,92,246,.2); color:#a78bfa; border:1px solid rgba(139,92,246,.3); }
.p-a   { background:rgba(59,130,246,.2); color:#60a5fa; border:1px solid rgba(59,130,246,.3); }
.p-b   { background:rgba(20,184,166,.2); color:#2dd4bf; border:1px solid rgba(20,184,166,.3); }
.p-c   { background:rgba(100,116,139,.15); color:#64748b; border:1px solid rgba(100,116,139,.2); }

.sig-pill { display:inline-block; font-size:10px; padding:4px 10px; border-radius:20px; font-weight:700; white-space:nowrap; }
.sous  { background:rgba(34,197,94,.15); color:#22c55e; border:1px solid rgba(34,197,94,.25); }
.sur   { background:rgba(239,68,68,.15); color:#ef4444; border:1px solid rgba(239,68,68,.25); }
.juste { background:rgba(234,179,8,.15); color:#eab308; border:1px solid rgba(234,179,8,.25); }

.nps-cell { font-size:14px; font-weight:800; text-align:right; }
.nps-hi { color:#22c55e; }
.nps-md { color:#eab308; }
.nps-lo { color:#ef4444; }

.badge-pump { background:rgba(239,68,68,.2); color:#ef4444; border:1px solid rgba(239,68,68,.35); font-size:9px; padding:1px 6px; border-radius:10px; font-weight:700; margin-left:4px; vertical-align:middle; }
.badge-show { background:rgba(99,102,241,.2); color:#818cf8; border:1px solid rgba(99,102,241,.35); font-size:9px; padding:1px 6px; border-radius:10px; font-weight:700; margin-left:4px; vertical-align:middle; }
.badge-live { background:rgba(34,197,94,.15); color:#22c55e; border:1px solid rgba(34,197,94,.25); font-size:9px; padding:1px 5px; border-radius:8px; font-weight:700; }

/* Supply badge (like Collectrics) */
.supply-tight { background:rgba(239,68,68,.15); color:#ef4444; border:1px solid rgba(239,68,68,.3); font-size:10px; padding:4px 10px; border-radius:20px; font-weight:700; }
.supply-loose { background:rgba(100,116,139,.15); color:#64748b; border:1px solid rgba(100,116,139,.2); font-size:10px; padding:4px 10px; border-radius:20px; font-weight:600; }

/* Sidebar */
.sb-section { font-size:11px; font-weight:700; color:#475569 !important; text-transform:uppercase; letter-spacing:.07em; margin:16px 0 8px; display:block; }
</style>
""", unsafe_allow_html=True)

USD_CAD    = 1.364
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
PRINT_SCORE={"oop":1.0,"soon":0.80,"in":0.20}
TIER_SCORE={"S":1.0,"A":0.75,"B":0.50,"C":0.30,"D":0.10}

def load_json(p,d):
    if os.path.exists(p):
        with open(p) as f: return json.load(f)
    return d
def save_json(p,d):
    os.makedirs(os.path.dirname(p),exist_ok=True)
    with open(p,"w") as f: json.dump(d,f,indent=2,ensure_ascii=False)

@st.cache_data(ttl=3600,show_spinner=False)
def fetch_card_api(name,set_code):
    tcg_id=SETS.get(set_code,{}).get("tcg_id","")
    if not tcg_id: return None
    try:
        clean=name.replace(" (SIR)","").replace(" (Alt Art)","").replace(" (IR)","").replace(" (Rainbow)","").replace(" (Full Art)","").replace(" (Shiny)","").split("(")[0].strip()
        r=requests.get(f'https://api.pokemontcg.io/v2/cards?q=name:"{clean}" set.id:{tcg_id}&pageSize=5',timeout=8)
        if r.status_code==200:
            cards=r.json().get("data",[])
            if cards: return cards[0]
    except: pass
    return None

def get_tcg_price(ac):
    if not ac: return None
    prices=ac.get("tcgplayer",{}).get("prices",{})
    for pt in ["holofoil","1stEditionHolofoil","reverseHolofoil","normal","unlimitedHolofoil"]:
        p=prices.get(pt,{}); m=p.get("market") or p.get("mid")
        if m and m>0: return round(m*USD_CAD,2)
    return None

def get_img(ac):
    if ac: return ac.get("images",{}).get("large") or ac.get("images",{}).get("small")
    return None

def calc_nps(c):
    st_=SETS.get(c["set"],{}).get("status","in"); pv=PRINT_SCORE.get(st_,0.2); tv=TIER_SCORE.get(c.get("tier","B"),0.3); sat=max(0.01,c.get("sat",0.07))
    w=((1-sat)*0.20+c.get("arb",0.5)*0.18+c.get("vel",0.5)*0.15+pv*0.25+tv*0.12+(1-c.get("rep",0.3))*0.10+c.get("stab",0.6)*0.08+c.get("whale",0.4)*0.06+c.get("cross",0.5)*0.05+c.get("soc",0.5)*0.04)
    return min(100,int((w/sat)*(1+c.get("cross",0.5)*0.20+c.get("soc",0.5)*0.15)*35))

def calc_signal(nps,gp,status):
    pv=PRINT_SCORE.get(status,0.2); fund=(nps/100)*0.6+pv*0.4
    if fund>0.72 and gp<8: return "sous"
    if fund<0.40 and gp>15: return "sur"
    return "juste"

def get_gain(c,days):
    past=c.get(f"p{days}",c.get("price",0))
    if past and past>0: return round((c["price"]-past)/past*100,2),round(c["price"]-past,2)
    return 0.0,0.0

def sparkline_svg(vals, color="#22c55e", w=80, h=28):
    vals=[v for v in vals if v and v>0]
    if len(vals)<2: return ""
    mn,mx=min(vals),max(vals)
    rng=mx-mn if mx!=mn else 1
    pts=[]
    for i,v in enumerate(vals):
        x=round(4+(w-8)*i/(len(vals)-1),1)
        y=round(h-4-(h-8)*(v-mn)/rng,1)
        pts.append(f"{x},{y}")
    path=" ".join(f"{'M' if i==0 else 'L'}{p}" for i,p in enumerate(pts))
    fill_pts=pts+[f"{w-4},{h-2}","4,{h-2}"]
    fill_path=path+f" L{w-4},{h-2} L4,{h-2} Z"
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="overflow:visible"><defs><linearGradient id="g{abs(hash(str(vals)))%9999}" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="{color}" stop-opacity=".25"/><stop offset="100%" stop-color="{color}" stop-opacity="0"/></linearGradient></defs><path d="{fill_path}" fill="url(#g{abs(hash(str(vals)))%9999})"/><path d="{path}" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'

def rar_pill(r):
    m={"SIR":"p-sir","ALT":"p-alt","IR":"p-ir","GG":"p-gg","SHV":"p-shv","SHINING":"p-shv","CLASSIC":"p-gold","FA":"p-fa","RR":"p-rr","GOLD":"p-gold"}
    return f'<span class="pill {m.get(r,"p-def")}">{r}</span>'
def tier_pill(t):
    return f'<span class="pill p-{t.lower()}">{t}</span>'
def chg_cell(v):
    if v>0:  return f'<div class="chg up">▲ +{v:.1f}%</div>'
    if v<0:  return f'<div class="chg dn">▼ {v:.1f}%</div>'
    return '<div class="chg fl">— 0%</div>'
def sig_pill(s):
    labels={"sous":"● Sous-évalué","sur":"● Sur-évalué","juste":"● Prix juste"}
    return f'<span class="sig-pill {s}">{labels[s]}</span>'
def nps_cell(n):
    c="nps-hi" if n>=85 else "nps-md" if n>=65 else "nps-lo"
    return f'<div class="nps-cell {c}">{n}</div>'
def supply_badge(gp7, gp30):
    if gp7 > 15 or (gp7 > 8 and gp30 > 20):
        return '<span class="supply-tight">Very Tight</span>'
    if gp7 > 5:
        return '<span class="supply-tight" style="background:rgba(234,179,8,.12);color:#eab308;border-color:rgba(234,179,8,.25)">Tight</span>'
    return '<span class="supply-loose">Normal</span>'

# ── Session state ──
if "cards"     not in st.session_state: st.session_state.cards=load_json(DATA_FILE,ALL_CARDS.copy())
if "period"    not in st.session_state: st.session_state.period=7
if "api_cache" not in st.session_state: st.session_state.api_cache=load_json(CACHE_FILE,{})

# ════════ SIDEBAR ════════
with st.sidebar:
    st.markdown("## 🎯 The Nasty Model")
    st.markdown("---")

    show_day = st.toggle("⚡ Mode Show Day", value=False, help="Cartes qui ont pumpé ≥10% en 7j et pas encore repriced")

    st.markdown('<span class="sb-section">Période affichée</span>', unsafe_allow_html=True)
    period_map={"24h":1,"3 jours":3,"7 jours":7,"1 mois":30,"3 mois":90,"6 mois":180}
    period_sel=st.radio("",list(period_map.keys()),index=2,horizontal=False,label_visibility="collapsed")
    days=period_map[period_sel]

    st.markdown('<span class="sb-section">Prix C$</span>', unsafe_allow_html=True)
    prix_min=st.number_input("Min C$",min_value=0,value=0,step=5,label_visibility="collapsed")
    prix_max=st.number_input("Max C$",min_value=0,value=5000,step=25,label_visibility="collapsed")

    st.markdown('<span class="sb-section">% de gain minimum</span>', unsafe_allow_html=True)
    gain_min=st.slider("",0,150,0,1,label_visibility="collapsed",format="+%d%%")

    st.markdown('<span class="sb-section">Filtres</span>', unsafe_allow_html=True)
    search=st.text_input("",placeholder="🔍  Carte, set, rareté...",label_visibility="collapsed")
    set_opts=["Tous les sets"]+[f"{v['name']} ({k})" for k,v in SETS.items()]
    set_filter=st.selectbox("",set_opts,label_visibility="collapsed")
    rar_filter=st.selectbox("",["Toutes rarétés","SIR","ALT","IR","GG","SHV","FA","RR","GOLD","HOLO","EX"],label_visibility="collapsed")
    tier_filter=st.selectbox("",["Tous tiers","S","A","B","C"],label_visibility="collapsed")
    sig_filter=st.selectbox("",["Tous signaux","Sous-évaluées","Surévaluées","Prix juste"],label_visibility="collapsed")

    st.markdown('<span class="sb-section">Tri</span>', unsafe_allow_html=True)
    sort_ui=st.selectbox("",["% gain ↓","$ gain ↓","NPS ↓","Prix ↓","Prix ↑","Nom"],label_visibility="collapsed")

    st.markdown("---")
    if st.button("🔄  Refresh données live",type="primary",use_container_width=True):
        st.cache_data.clear(); st.session_state.api_cache={}; save_json(CACHE_FILE,{}); st.rerun()
    st.markdown(f'<div style="text-align:center;margin-top:8px;font-size:10px;color:#334155">{len(st.session_state.cards)} cartes · MAJ {datetime.now().strftime("%H:%M")}</div>',unsafe_allow_html=True)

# ════════ MAIN ════════

# Nav bar
st.markdown(f"""
<div class="nav-bar">
  <div class="nav-logo">
    <div class="nav-logo-icon">🃏</div>
    <div>
      <div class="nav-title">The Nasty Model</div>
      <div class="nav-sub">market intelligence · pokémon TCG · C$</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:10px">
    <span class="nav-badge">🇨🇦 CAD</span>
    <span class="nav-badge">live · TCGPlayer</span>
    <span class="nav-badge">{datetime.now().strftime("%Y-%m-%d")}</span>
  </div>
</div>
""",unsafe_allow_html=True)

# ── Fetch data ──
prog=st.empty()
rows=[]
for idx,c in enumerate(st.session_state.cards):
    key=f"{c['id']}_{c['set']}"
    if key not in st.session_state.api_cache:
        prog.markdown(f'<div style="color:#475569;font-size:12px;padding:4px 0">⏳ Chargement données... {idx+1}/{len(st.session_state.cards)}</div>',unsafe_allow_html=True)
        ac=fetch_card_api(c["id"],c["set"])
        st.session_state.api_cache[key]={"img":get_img(ac),"live_price":get_tcg_price(ac),"ts":datetime.now().isoformat()}
        save_json(CACHE_FILE,st.session_state.api_cache)
    cached=st.session_state.api_cache[key]
    price=cached.get("live_price") or c.get("price",0)
    if price<=0: price=c.get("price",0)
    c2={**c,"price":price}
    nps=calc_nps(c); st_=SETS.get(c["set"],{}).get("status","in")
    gp,gc=get_gain(c2,days); gp1,_=get_gain(c2,1); gp7,_=get_gain(c2,7); gp30,_=get_gain(c2,30); gp90,_=get_gain(c2,90)
    signal=calc_signal(nps,gp,st_); demand=min(99,int(nps*0.82+c.get("vel",0.5)*18))
    spark_vals=[c2.get("p180",price),c2.get("p90",price),c2.get("p30",price),c2.get("p7",price),c2.get("p1",price),price]
    rows.append({**c2,"img_url":cached.get("img",""),"nps":nps,"gain_pct":gp,"gain_cad":gc,
                 "gp1":gp1,"gp7":gp7,"gp30":gp30,"gp90":gp90,"signal":signal,"status":st_,
                 "set_name":SETS.get(c["set"],{}).get("name",c["set"]),"demand":demand,
                 "spark":spark_vals,"live":cached.get("live_price") is not None})
prog.empty()
df=pd.DataFrame(rows)

# ── Filters ──
if show_day: df=df[(df["gp7"]>=10)&(df["signal"]=="sous")]
if prix_min>0: df=df[df["price"]>=prix_min]
if prix_max<5000: df=df[df["price"]<=prix_max]
if gain_min>0: df=df[df["gain_pct"]>=gain_min]
if search:
    q=search.lower(); df=df[df["name"].str.lower().str.contains(q)|df["set"].str.lower().str.contains(q)|df["set_name"].str.lower().str.contains(q)|df["rarity"].str.lower().str.contains(q)]
if set_filter!="Tous les sets":
    df=df[df["set"]==set_filter.split("(")[-1].rstrip(")")]
if rar_filter!="Toutes rarétés": df=df[df["rarity"]==rar_filter]
if tier_filter!="Tous tiers": df=df[df["tier"]==tier_filter]
sig_map={"Sous-évaluées":"sous","Surévaluées":"sur","Prix juste":"juste"}
if sig_filter!="Tous signaux": df=df[df["signal"]==sig_map[sig_filter]]
sort_map={"% gain ↓":("gain_pct",False),"$ gain ↓":("gain_cad",False),"NPS ↓":("nps",False),"Prix ↓":("price",False),"Prix ↑":("price",True),"Nom":("name",True)}
sk,sa=sort_map[sort_ui]; df=df.sort_values(sk,ascending=sa).reset_index(drop=True)

# ── Metrics ──
pl=period_sel; c1,c2_,c3,c4,c5,c6=st.columns(6)
c1.metric("Cartes",len(df))
c2_.metric("Sous-évaluées",int((df["signal"]=="sous").sum()))
c3.metric("Surévaluées",int((df["signal"]=="sur").sum()))
c4.metric("Pump 24h",int((df["gp1"]>5).sum()))
c5.metric("NPS moyen",int(df["nps"].mean()) if len(df) else 0)
c6.metric("Prix live",f"{int(df['live'].sum())}/{len(df)}" if len(df) else "0/0")

# ── Show Day banner ──
if show_day:
    total_val=df["price"].sum(); avg_gain=df["gp7"].mean() if len(df) else 0
    st.markdown(f"""
    <div class="show-banner">
      <div class="show-banner-icon">⚡</div>
      <div style="flex:1">
        <div class="show-banner-title">MODE SHOW DAY ACTIVÉ</div>
        <div class="show-banner-sub">Cartes avec gain 7j ≥ 10% et signal sous-évalué — opportunités que les vendeurs n'ont pas encore repriced</div>
      </div>
      <div class="show-stat"><div class="show-stat-v">{len(df)}</div><div class="show-stat-l">opportunités</div></div>
      <div class="show-stat"><div class="show-stat-v">+{avg_gain:.1f}%</div><div class="show-stat-l">gain moy. 7j</div></div>
      <div class="show-stat"><div class="show-stat-v">C${total_val:,.0f}</div><div class="show-stat-l">valeur totale</div></div>
    </div>
    """,unsafe_allow_html=True)
else:
    st.markdown("<div style='height:8px'></div>",unsafe_allow_html=True)

# ── Section title ──
period_lbl={1:"24h",3:"3j",7:"7j",30:"1M",90:"3M",180:"6M"}[days]
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:10px">
  <div>
    <span style="font-size:18px;font-weight:700;color:#f1f5f9">biggest market movers</span>
    <span style="font-size:12px;color:#475569;margin-left:10px">triés par {sort_ui} · période {period_lbl}</span>
  </div>
  <span style="font-size:11px;color:#334155">{len(df)} résultats</span>
</div>
""",unsafe_allow_html=True)

if len(df)==0:
    st.markdown('<div style="text-align:center;padding:4rem;color:#334155;font-size:14px">Aucune carte ne correspond aux filtres.</div>',unsafe_allow_html=True)
else:
    # Header
    st.markdown(f"""
    <div class="tbl-wrap">
    <div class="tbl-hdr">
      <div class="tbl-hdr-cell"></div>
      <div class="tbl-hdr-cell">carte</div>
      <div class="tbl-hdr-cell r">prix C$</div>
      <div class="tbl-hdr-cell c">tendance</div>
      <div class="tbl-hdr-cell r">% {period_lbl}</div>
      <div class="tbl-hdr-cell r">C$ {period_lbl}</div>
      <div class="tbl-hdr-cell r">24h</div>
      <div class="tbl-hdr-cell r">7j</div>
      <div class="tbl-hdr-cell r">1M</div>
      <div class="tbl-hdr-cell c">signal</div>
      <div class="tbl-hdr-cell r">NPS</div>
    </div>
    """,unsafe_allow_html=True)

    rows_html=""
    for i,(_,row) in enumerate(df.iterrows()):
        gc_str=f'+C${row["gain_cad"]:.0f}' if row["gain_cad"]>=0 else f'−C${abs(row["gain_cad"]):.0f}'
        gc_clr="#22c55e" if row["gain_cad"]>=0 else "#ef4444"
        dc="#22c55e" if row["demand"]>75 else "#eab308" if row["demand"]>50 else "#ef4444"
        img_html=f'<img src="{row["img_url"]}" class="card-img" onerror="this.style.display=\'none\';this.nextSibling.style.display=\'flex\'" /><div class="card-ph" style="display:none">🃏</div>' if row.get("img_url") else '<div class="card-ph">🃏</div>'
        bp='<span class="badge-pump">🔥 +24h</span>' if row["gp1"]>5 else ""
        bs='<span class="badge-show">⚡ SHOW</span>' if row["gp7"]>=10 and row["signal"]=="sous" else ""
        live_dot='<span class="badge-live">●</span> ' if row.get("live") else ""
        sp_color="#22c55e" if row["gain_pct"]>=0 else "#ef4444"
        spark=sparkline_svg(row["spark"],sp_color)
        supply=supply_badge(row["gp7"],row["gp30"])

        rows_html+=f"""
<div class="tbl-row">
  <div>{img_html}</div>
  <div>
    <div class="card-name">{live_dot}{row['name']}{bp}{bs}</div>
    <div class="card-meta">{row['set_name']} · {rar_pill(row['rarity'])} · {tier_pill(row['tier'])}</div>
    <div class="demand-row">
      <div class="demand-track"><div class="demand-fill" style="width:{row['demand']}%;background:{dc}"></div></div>
      <span class="demand-lbl" style="color:{dc}">{row['demand']}%</span>
    </div>
  </div>
  <div>
    <div class="price-cell">C${row['price']:.0f}</div>
    <div style="margin-top:3px">{supply}</div>
  </div>
  <div class="spark-cell">{spark}</div>
  <div>{chg_cell(row['gain_pct'])}</div>
  <div style="text-align:right;font-size:12px;font-weight:600;color:{gc_clr}">{gc_str}</div>
  <div>{chg_cell(row['gp1'])}</div>
  <div>{chg_cell(row['gp7'])}</div>
  <div>{chg_cell(row['gp30'])}</div>
  <div style="text-align:center">{sig_pill(row['signal'])}</div>
  {nps_cell(row['nps'])}
</div>"""

    st.markdown(rows_html+"</div>",unsafe_allow_html=True)

# ── Export + Tools ──
st.markdown("<hr>",unsafe_allow_html=True)
with st.expander("📋  Liste d'achat show — export CSV"):
    show_df=df[(df["gp7"]>=10)&(df["signal"]=="sous")].copy() if not show_day else df.copy()
    if len(show_df)>0:
        ex=show_df[["name","set_name","rarity","tier","price","gp7","gp30","nps"]].copy()
        ex.columns=["Carte","Set","Rareté","Tier","Prix C$","Gain 7j %","Gain 30j %","NPS"]
        ex["Offre cible (-15%)"]=(ex["Prix C$"]*0.85).round(0).astype(int)
        ex["Offre agressive (-25%)"]=(ex["Prix C$"]*0.75).round(0).astype(int)
        st.dataframe(ex,use_container_width=True,hide_index=True)
        st.download_button("⬇️ Télécharger CSV",data=ex.to_csv(index=False),file_name=f"show_{datetime.now().strftime('%Y%m%d')}.csv",mime="text/csv",type="primary")
    else:
        st.info("Active le Mode Show Day ou applique des filtres pour générer ta liste.")

with st.expander("➕  Ajouter une carte"):
    a1,a2=st.columns(2)
    with a1:
        nn=st.text_input("Nom"); ns=st.selectbox("Set",list(SETS.keys()),format_func=lambda k:f"{SETS[k]['name']} ({k})"); nr=st.selectbox("Rareté",["SIR","ALT","IR","GG","SHV","FA","RR","GOLD","HOLO","EX"]); nt=st.selectbox("Tier",["S","A","B","C"])
    with a2:
        np_=st.number_input("Prix C$",min_value=0.0,step=0.5); np7=st.number_input("Prix 7j C$",min_value=0.0,step=0.5); np30=st.number_input("Prix 30j C$",min_value=0.0,step=0.5); np90=st.number_input("Prix 90j C$",min_value=0.0,step=0.5)
        nsat=st.number_input("Saturation PSA10",0.0,1.0,0.06,0.01); narb=st.number_input("Arbitrage JP/EN",0.0,1.0,0.50,0.01)
    if st.button("Ajouter",type="primary"):
        if nn and np_>0:
            st.session_state.cards.append({"id":f"c-{datetime.now().strftime('%Y%m%d%H%M%S')}","name":nn,"set":ns,"rarity":nr,"tier":nt,"price":np_,"p1":np_*0.998,"p3":np_,"p7":np7 if np7>0 else np_,"p30":np30 if np30>0 else np_,"p90":np90 if np90>0 else np_,"p180":np_,"sat":nsat,"arb":narb,"vel":0.50,"whale":0.45,"cross":0.52,"soc":0.50,"rep":0.25,"stab":0.55})
            save_json(DATA_FILE,st.session_state.cards); st.success(f"✅ {nn} ajoutée !"); st.rerun()

with st.expander("⚙️  Paramètres"):
    p1,p2=st.columns(2)
    with p1:
        if st.button("Réinitialiser cartes"): st.session_state.cards=ALL_CARDS.copy(); save_json(DATA_FILE,st.session_state.cards); st.rerun()
        if st.button("Vider cache prix"): st.session_state.api_cache={}; save_json(CACHE_FILE,{}); st.cache_data.clear(); st.rerun()
    with p2:
        st.download_button("Exporter JSON",data=json.dumps(st.session_state.cards,indent=2,ensure_ascii=False),file_name="nasty_model.json",mime="application/json")
