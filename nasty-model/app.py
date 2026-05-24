import streamlit as st
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime
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
  section[data-testid="stSidebar"] { background-color: #0d0f18; }
  h1,h2,h3 { color: #ffffff; }
  div[data-testid="metric-container"] {
    background: #161928; border: 0.5px solid #252840;
    border-radius: 10px; padding: 0.7rem 1rem;
  }
  div[data-testid="metric-container"] label { color: #6b7280 !important; font-size: 11px; letter-spacing:.04em; text-transform:uppercase; }
  div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #ffffff; font-size: 22px; font-weight:600; }
  .stTextInput>div>div>input { background:#161928 !important; color:#e8e8e8 !important; border-color:#252840 !important; border-radius:8px !important; }
  .stSelectbox>div>div { background:#161928 !important; color:#e8e8e8 !important; border-color:#252840 !important; }
  .stButton>button { background:#161928; color:#e8e8e8; border:0.5px solid #252840; border-radius:8px; font-size:13px; }
  .stButton>button:hover { background:#252840; }
  [data-testid="stExpander"] { background:#161928; border:0.5px solid #252840; border-radius:10px; }
  hr { border-color: #1a1d2e; }

  .card-row {
    display: grid;
    grid-template-columns: 64px 1fr 100px 90px 90px 90px 90px 90px 90px 110px 80px;
    align-items: center;
    gap: 0 12px;
    padding: 10px 16px;
    border-bottom: 0.5px solid #161928;
    transition: background .12s;
  }
  .card-row:hover { background: #161928; border-radius: 8px; }
  .card-row.header {
    font-size: 11px; color: #4b5563; font-weight: 500;
    letter-spacing: .05em; text-transform: uppercase;
    padding: 8px 16px; border-bottom: 0.5px solid #252840;
    cursor: pointer;
  }
  .card-img { width:56px; height:78px; object-fit:cover; border-radius:5px; background:#1a1d2e; }
  .card-img-placeholder { width:56px; height:78px; border-radius:5px; background:#1a1d2e; display:flex; align-items:center; justify-content:center; font-size:20px; }
  .card-name { font-weight:600; color:#fff; font-size:14px; line-height:1.3; }
  .card-set  { font-size:11px; color:#6b7280; margin-top:2px; }
  .card-price { font-weight:600; color:#fff; font-size:15px; text-align:right; }
  .pos { color:#4ade80; font-weight:500; font-size:13px; text-align:right; }
  .neg { color:#f87171; font-weight:500; font-size:13px; text-align:right; }
  .neu { color:#6b7280; font-size:13px; text-align:right; }
  .demand-wrap { display:flex; align-items:center; gap:6px; }
  .demand-bar-bg { flex:1; background:#1a1d2e; border-radius:3px; height:4px; overflow:hidden; }
  .demand-bar-fg { height:100%; border-radius:3px; }
  .demand-pct { font-size:12px; font-weight:500; min-width:32px; text-align:right; }
  .signal-pill { display:inline-block; font-size:10px; padding:3px 10px; border-radius:20px; font-weight:600; white-space:nowrap; }
  .sous { background:#14532d; color:#4ade80; }
  .sur  { background:#450a0a; color:#f87171; }
  .juste{ background:#451a03; color:#fbbf24; }
  .nps-val { font-weight:700; font-size:14px; text-align:right; }
  .nps-g { color:#4ade80; }
  .nps-a { color:#fbbf24; }
  .nps-r { color:#f87171; }

  .pill { display:inline-block; font-size:10px; padding:2px 7px; border-radius:12px; font-weight:500; }
  .p-sir    { background:#2e1065; color:#c084fc; }
  .p-alt    { background:#0c1a3a; color:#60a5fa; }
  .p-ir     { background:#042f2e; color:#2dd4bf; }
  .p-gg     { background:#0c1a3a; color:#60a5fa; }
  .p-shv    { background:#451a03; color:#fbbf24; }
  .p-fa     { background:#1f2937; color:#9ca3af; }
  .p-rr     { background:#450a0a; color:#f87171; }
  .p-gold   { background:#451a03; color:#fbbf24; }
  .p-other  { background:#1f2937; color:#9ca3af; }
  .p-s      { background:#2e1065; color:#c084fc; }
  .p-a      { background:#0c1a3a; color:#60a5fa; }
  .p-b      { background:#042f2e; color:#2dd4bf; }

  .period-btn { display:inline-block; font-size:12px; padding:4px 12px; border-radius:6px; background:#161928; border:0.5px solid #252840; color:#9ca3af; cursor:pointer; margin-right:4px; font-weight:500; }
  .period-btn.active { background:#252840; color:#fff; border-color:#374151; }
  .sort-indicator { color:#60a5fa; }

  .upside-card { background:#161928; border:0.5px solid #252840; border-radius:12px; padding:1rem 1.2rem; margin-bottom:10px; }
  .upside-top  { background:#161928; border:1.5px solid #1d4ed8; border-radius:12px; padding:1rem 1.2rem; margin-bottom:10px; }
</style>
""", unsafe_allow_html=True)

USD_CAD = 1.364

SETS = {
    "XY":  {"name":"XY Base","year":2014,"status":"oop"},
    "FLF": {"name":"Flashfire","year":2014,"status":"oop"},
    "ROS": {"name":"Roaring Skies","year":2015,"status":"oop"},
    "AOR": {"name":"Ancient Origins","year":2015,"status":"oop"},
    "BKT": {"name":"BREAKthrough","year":2015,"status":"oop"},
    "BKP": {"name":"BREAKpoint","year":2016,"status":"oop"},
    "FCO": {"name":"Fates Collide","year":2016,"status":"oop"},
    "STS": {"name":"Steam Siege","year":2016,"status":"oop"},
    "EVO": {"name":"Evolutions","year":2016,"status":"oop"},
    "SUM": {"name":"Sun & Moon","year":2017,"status":"oop"},
    "GRI": {"name":"Guardians Rising","year":2017,"status":"oop"},
    "BUS": {"name":"Burning Shadows","year":2017,"status":"oop"},
    "SHL": {"name":"Shining Legends","year":2017,"status":"oop"},
    "CRI": {"name":"Crimson Invasion","year":2017,"status":"oop"},
    "UPR": {"name":"Ultra Prism","year":2018,"status":"oop"},
    "FLI": {"name":"Forbidden Light","year":2018,"status":"oop"},
    "CES": {"name":"Celestial Storm","year":2018,"status":"oop"},
    "LOT": {"name":"Lost Thunder","year":2018,"status":"oop"},
    "TEU": {"name":"Team Up","year":2019,"status":"oop"},
    "UNB": {"name":"Unbroken Bonds","year":2019,"status":"oop"},
    "UNM": {"name":"Unified Minds","year":2019,"status":"oop"},
    "HIF": {"name":"Hidden Fates","year":2019,"status":"oop"},
    "CEC": {"name":"Cosmic Eclipse","year":2019,"status":"oop"},
    "RCL": {"name":"Rebel Clash","year":2020,"status":"oop"},
    "DAA": {"name":"Darkness Ablaze","year":2020,"status":"oop"},
    "VIV": {"name":"Vivid Voltage","year":2020,"status":"oop"},
    "SHF": {"name":"Shining Fates","year":2021,"status":"oop"},
    "BST": {"name":"Battle Styles","year":2021,"status":"oop"},
    "CRE": {"name":"Chilling Reign","year":2021,"status":"oop"},
    "EVS": {"name":"Evolving Skies","year":2021,"status":"oop"},
    "FST": {"name":"Fusion Strike","year":2021,"status":"oop"},
    "CEL": {"name":"Celebrations","year":2021,"status":"oop"},
    "BRS": {"name":"Brilliant Stars","year":2022,"status":"oop"},
    "ASR": {"name":"Astral Radiance","year":2022,"status":"oop"},
    "PGO": {"name":"Pokémon GO","year":2022,"status":"oop"},
    "LOR": {"name":"Lost Origin","year":2022,"status":"oop"},
    "SIT": {"name":"Silver Tempest","year":2022,"status":"oop"},
    "CRZ": {"name":"Crown Zenith","year":2023,"status":"oop"},
    "SVI": {"name":"Scarlet & Violet","year":2023,"status":"oop"},
    "PAL": {"name":"Paldea Evolved","year":2023,"status":"oop"},
    "OBF": {"name":"Obsidian Flames","year":2023,"status":"oop"},
    "MEW": {"name":"Pokémon 151","year":2023,"status":"oop"},
    "PAR": {"name":"Paradox Rift","year":2023,"status":"oop"},
    "PAF": {"name":"Paldean Fates","year":2024,"status":"oop"},
    "TEF": {"name":"Temporal Forces","year":2024,"status":"oop"},
    "TWM": {"name":"Twilight Masquerade","year":2024,"status":"oop"},
    "SFA": {"name":"Shrouded Fable","year":2024,"status":"oop"},
    "SCR": {"name":"Stellar Crown","year":2024,"status":"oop"},
    "SSP": {"name":"Surging Sparks","year":2024,"status":"soon"},
    "PRE": {"name":"Prismatic Evolutions","year":2025,"status":"oop"},
    "JTG": {"name":"Journey Together","year":2025,"status":"soon"},
    "DRI": {"name":"Destined Rivals","year":2025,"status":"in"},
    "MEG": {"name":"Mega Evolution","year":2025,"status":"in"},
    "PHF": {"name":"Phantasmal Flames","year":2025,"status":"in"},
    "ASH": {"name":"Ascended Heroes","year":2026,"status":"in"},
    "PFO": {"name":"Perfect Order","year":2026,"status":"in"},
    "CRS": {"name":"Chaos Rising","year":2026,"status":"in"},
}

PRINT_SCORE = {"oop":1.0,"soon":0.80,"in":0.20}
TIER_SCORE  = {"S":1.0,"A":0.75,"B":0.50,"C":0.30,"D":0.10}
DATA_FILE   = "data/cards.json"
TOKEN = os.environ.get("GITHUB_TOKEN", "")

def load_cards():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE,"r") as f:
            return json.load(f)
    return ALL_CARDS.copy()

def save_cards(cards):
    os.makedirs("data",exist_ok=True)
    with open(DATA_FILE,"w") as f:
        json.dump(cards,f,indent=2,ensure_ascii=False)

def calc_nps(c):
    st_   = SETS.get(c["set"],{}).get("status","in")
    pv    = PRINT_SCORE.get(st_,0.2)
    tv    = TIER_SCORE.get(c["tier"],0.3)
    sat   = max(0.01,c["sat"])
    w     = ((1-sat)*0.20+c["arb"]*0.18+c["vel"]*0.15+pv*0.25+
              tv*0.12+(1-c["rep"])*0.10+c["stab"]*0.08+
              c["whale"]*0.06+c["cross"]*0.05+c["soc"]*0.04)
    hype  = 1+c["cross"]*0.20+c["soc"]*0.15
    return min(100,int((w/sat)*hype*35))

def calc_signal(nps,gain_pct,status):
    pv   = PRINT_SCORE.get(status,0.2)
    fund = (nps/100)*0.6+pv*0.4
    if fund>0.72 and gain_pct<8:  return "sous"
    if fund<0.40 and gain_pct>15: return "sur"
    return "juste"

def get_gain(c,days):
    key  = f"p{days}"
    past = c.get(key, c["price"])
    if past and past>0:
        return round((c["price"]-past)/past*100,2), round(c["price"]-past,2)
    return 0.0,0.0

def get_image_url(card_id, card_name, set_code):
    # Use PokémonTCG API image pattern
    cid = card_id.lower().replace("-","")
    num = card_id.split("-")[-1] if "-" in card_id else ""
    set_lower = set_code.lower()
    return f"https://images.pokemontcg.io/{set_lower}/{num}_hires.png"

def rar_pill(r):
    m={"SIR":"p-sir","ALT":"p-alt","IR":"p-ir","GG":"p-gg","SHV":"p-shv",
       "SHINING":"p-shv","CLASSIC":"p-gold","FA":"p-fa","RR":"p-rr","GOLD":"p-gold"}
    return f'<span class="pill {m.get(r,"p-other")}">{r}</span>'

def tier_pill(t):
    m={"S":"p-s","A":"p-a","B":"p-b"}
    return f'<span class="pill {m.get(t,"p-other")}">{t}</span>'

def gain_cell(v, show_cad=False):
    if v>0:  return f'<div class="pos">+{v:.1f}{"C$" if show_cad else "%"}</div>'
    if v<0:  return f'<div class="neg">{v:.1f}{"C$" if show_cad else "%"}</div>'
    return f'<div class="neu">0.0{"C$" if show_cad else "%"}</div>'

def signal_pill(s):
    labels={"sous":"SOUS-ÉV.","sur":"SUR-ÉV.","juste":"PRIX JUSTE"}
    return f'<span class="signal-pill {s}">{labels[s]}</span>'

def nps_cell(n):
    c="nps-g" if n>=85 else "nps-a" if n>=65 else "nps-r"
    return f'<div class="nps-val {c}">{n}</div>'

if "cards" not in st.session_state:
    st.session_state.cards = load_cards()
if "period" not in st.session_state:
    st.session_state.period = 7
if "sort_col" not in st.session_state:
    st.session_state.sort_col = "gain_pct"
if "sort_asc" not in st.session_state:
    st.session_state.sort_asc = False

# ── Header ────────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:16px;margin-bottom:1.5rem">
  <div style="width:50px;height:50px;background:#161928;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:24px;border:0.5px solid #252840">🃏</div>
  <div>
    <h1 style="margin:0;font-size:24px;font-weight:700">The Nasty Model</h1>
    <p style="color:#6b7280;margin:0;font-size:13px">Screener TCG · Ranking intra-rareté · Valeurs en C$</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Controls ──────────────────────────────────
c1,c2,c3,c4,c5 = st.columns([3,2,1.5,1.8,1.5])
with c1:
    search = st.text_input("","",placeholder="🔍  Rechercher carte, set, rareté...",label_visibility="collapsed")
with c2:
    set_opts = ["Tous les sets"] + [f"{v['name']} ({k})" for k,v in SETS.items()]
    set_filter = st.selectbox("Set",set_opts,label_visibility="collapsed")
with c3:
    rar_filter = st.selectbox("Rareté",["Toutes","SIR","ALT","IR","GG","SHV","SHINING","CLASSIC","FA","RR","GOLD","HOLO","EX"],label_visibility="collapsed")
with c4:
    sig_filter = st.selectbox("Signal",["Tous","Sous-évaluées","Surévaluées","Prix juste"],label_visibility="collapsed")
with c5:
    sort_ui = st.selectbox("Trier par",["% gain","$ gain","NPS","Prix ↑","Prix ↓","Nom"],label_visibility="collapsed")

# Period selector
st.markdown("""
<div style="margin-bottom:1rem;display:flex;align-items:center;gap:8px">
  <span style="font-size:12px;color:#6b7280;margin-right:4px">Période :</span>
</div>
""", unsafe_allow_html=True)

period_cols = st.columns(6)
period_labels = ["24h","3 jours","7 jours","1 mois","3 mois","6 mois"]
period_days   = [1, 3, 7, 30, 90, 180]
period_keys   = ["p1","p3","p7","p30","p90","p180"]

for i,(col,lbl) in enumerate(zip(period_cols, period_labels)):
    with col:
        active = st.session_state.period == period_days[i]
        if st.button(lbl, key=f"per_{i}", type="primary" if active else "secondary"):
            st.session_state.period = period_days[i]
            st.rerun()

days = st.session_state.period

# ── Build data ────────────────────────────────
rows = []
for c in st.session_state.cards:
    nps       = calc_nps(c)
    gp,gc     = get_gain(c,days)
    st_code   = SETS.get(c["set"],{}).get("status","in")
    signal    = calc_signal(nps,gp,st_code)
    set_name  = SETS.get(c["set"],{}).get("name",c["set"])
    img_url   = get_image_url(c["id"], c["name"], c["set"])
    demand    = min(99, int(nps * 0.85 + c.get("vel",0.5)*15))
    rows.append({**c,"nps":nps,"gain_pct":gp,"gain_cad":gc,
                 "signal":signal,"set_name":set_name,"status":st_code,
                 "img_url":img_url,"demand":demand})

df = pd.DataFrame(rows)

# Filters
if search:
    q=search.lower()
    df=df[df["name"].str.lower().str.contains(q)|df["set"].str.lower().str.contains(q)|
          df["set_name"].str.lower().str.contains(q)|df["rarity"].str.lower().str.contains(q)]
if set_filter!="Tous les sets":
    code=set_filter.split("(")[-1].rstrip(")")
    df=df[df["set"]==code]
if rar_filter!="Toutes":
    df=df[df["rarity"]==rar_filter]
sig_map={"Sous-évaluées":"sous","Surévaluées":"sur","Prix juste":"juste"}
if sig_filter!="Tous":
    df=df[df["signal"]==sig_map[sig_filter]]

sort_map={"% gain":("gain_pct",False),"$ gain":("gain_cad",False),"NPS":("nps",False),
          "Prix ↑":("price",True),"Prix ↓":("price",False),"Nom":("name",True)}
sk,sa = sort_map[sort_ui]
df = df.sort_values(sk,ascending=sa).reset_index(drop=True)

# ── Stats ─────────────────────────────────────
m1,m2,m3,m4,m5 = st.columns(5)
m1.metric("CARTES", len(df))
m2.metric("SOUS-ÉV. 🟢", int((df["signal"]=="sous").sum()))
m3.metric("SUR-ÉV. 🔴",  int((df["signal"]=="sur").sum()))
m4.metric("PRIX JUSTE 🟡",int((df["signal"]=="juste").sum()))
m5.metric("NPS MOYEN",   int(df["nps"].mean()) if len(df) else 0)

st.markdown("<div style='margin-top:1rem'></div>",unsafe_allow_html=True)

# ── Column headers ────────────────────────────
period_label = {1:"24h",3:"3j",7:"7j",30:"1M",90:"3M",180:"6M"}[days]
st.markdown(f"""
<div class="card-row header">
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
    gp_24h,_  = get_gain(row, 1)
    gp_7d,_   = get_gain(row, 7)
    gp_30d,_  = get_gain(row, 30)
    gp_90d,_  = get_gain(row, 90)
    gp_main,gc_main = get_gain(row, days)

    def clr(v):
        if v>0: return f'<span style="color:#4ade80;font-size:13px">+{v:.1f}%</span>'
        if v<0: return f'<span style="color:#f87171;font-size:13px">{v:.1f}%</span>'
        return f'<span style="color:#6b7280;font-size:13px">0.0%</span>'

    gc_str = f'+C${gc_main:.0f}' if gc_main>=0 else f'-C${abs(gc_main):.0f}'
    gc_clr = "#4ade80" if gc_main>=0 else "#f87171"

    demand_clr = "#4ade80" if row['demand']>75 else "#fbbf24" if row['demand']>50 else "#f87171"

    img_html = f'<img src="{row["img_url"]}" class="card-img" onerror="this.style.display=\'none\';this.nextSibling.style.display=\'flex\'" /><div class="card-img-placeholder" style="display:none">🃏</div>'

    return f"""
<div class="card-row">
  <div style="position:relative">{img_html}</div>
  <div>
    <div class="card-name">{row['name']}</div>
    <div class="card-set">{row['set_name']} · {rar_pill(row['rarity'])} · {tier_pill(row['tier'])}</div>
    <div style="margin-top:4px">
      <div class="demand-wrap">
        <div class="demand-bar-bg"><div class="demand-bar-fg" style="width:{row['demand']}%;background:{demand_clr}"></div></div>
        <span class="demand-pct" style="color:{demand_clr}">{row['demand']}%</span>
      </div>
    </div>
  </div>
  <div class="card-price">C${row['price']:.0f}</div>
  <div>{clr(gp_main)}</div>
  <div style="text-align:right;font-size:13px;color:{gc_clr}">{gc_str}</div>
  <div>{clr(gp_24h)}</div>
  <div>{clr(gp_7d)}</div>
  <div>{clr(gp_30d)}</div>
  <div>{clr(gp_90d)}</div>
  <div style="text-align:center">{signal_pill(row['signal'])}</div>
  {nps_cell(row['nps'])}
</div>"""

html_rows = "".join(make_row(r) for _,r in df.iterrows())
st.markdown(f'<div style="background:#0d0f18;border-radius:12px;border:0.5px solid #252840;overflow:hidden">{html_rows}</div>',unsafe_allow_html=True)

# ── Upside section ────────────────────────────
st.markdown("<hr>",unsafe_allow_html=True)
st.markdown("### 🚀 Upside potential")
upside = df[df["gain_pct"]>0].sort_values("nps",ascending=False).head(5)

for i,(_,row) in enumerate(upside.iterrows()):
    cls  = "upside-top" if i==0 else "upside-card"
    badge= '<span style="background:#0c1a3a;color:#60a5fa;padding:2px 9px;border-radius:20px;font-size:10px;font-weight:600">⭐ meilleur upside</span> ' if i==0 else ""
    nc   = "#4ade80" if row["nps"]>=85 else "#fbbf24" if row["nps"]>=65 else "#f87171"
    bars = [
        ("PSA10 sat.",  round((1-row["sat"])*100),"#60a5fa"),
        ("JP/EN arb.",  round(row["arb"]*100),    "#4ade80"),
        ("print status",round(PRINT_SCORE.get(row["status"],0.2)*100),"#fbbf24"),
        ("whales",      round(row["whale"]*100),  "#c084fc"),
    ]
    bars_html="".join([
        f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:3px">'
        f'<span style="font-size:11px;color:#4b5563;min-width:80px">{l}</span>'
        f'<div style="flex:1;background:#0d0f18;border-radius:3px;height:4px;overflow:hidden">'
        f'<div style="width:{v}%;height:100%;background:{c};border-radius:3px"></div></div>'
        f'<span style="font-size:10px;color:#4b5563;min-width:26px;text-align:right">{v}%</span></div>'
        for l,v,c in bars])
    st.markdown(f"""<div class="{cls}">
      <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:8px">
        {badge}
        <img src="{row['img_url']}" style="width:40px;height:56px;object-fit:cover;border-radius:4px" onerror="this.style.display='none'">
        <span style="font-size:13px;font-weight:600;color:#fff;flex:1">{row['name']} <span style="color:#4b5563;font-size:11px;font-weight:400">{row['set_name']}</span></span>
        <span style="color:#4ade80;font-size:13px;font-weight:500">+{row['gain_pct']:.1f}%</span>
        <span style="font-size:18px;font-weight:700;color:{nc}">{row['nps']}<span style="font-size:11px;color:#4b5563;font-weight:400">/100</span></span>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 16px">{bars_html}</div>
    </div>""",unsafe_allow_html=True)

# ── Add / Import / Settings ───────────────────
st.markdown("<hr>",unsafe_allow_html=True)
with st.expander("➕  Ajouter une carte manuellement"):
    a1,a2 = st.columns(2)
    with a1:
        nn  = st.text_input("Nom")
        ns  = st.selectbox("Set",list(SETS.keys()),format_func=lambda k:f"{SETS[k]['name']} ({k})")
        nr  = st.selectbox("Rareté",["SIR","ALT","IR","GG","SHV","SHINING","CLASSIC","FA","RR","GOLD","HOLO","EX"])
        nt  = st.selectbox("Tier",["S","A","B","C"])
    with a2:
        np_ = st.number_input("Prix actuel C$",min_value=0.0,step=0.5)
        np1 = st.number_input("Prix 24h C$",min_value=0.0,step=0.5)
        np7 = st.number_input("Prix 7j C$",min_value=0.0,step=0.5)
        np30= st.number_input("Prix 30j C$",min_value=0.0,step=0.5)
        np90= st.number_input("Prix 90j C$",min_value=0.0,step=0.5)
        nsat= st.number_input("Saturation PSA10 (0–1)",min_value=0.0,max_value=1.0,value=0.06,step=0.01)
        narb= st.number_input("Arbitrage JP/EN (0–1)",min_value=0.0,max_value=1.0,value=0.50,step=0.01)
    if st.button("Ajouter",type="primary"):
        if nn and np_>0:
            st.session_state.cards.append({
                "id":f"custom-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "name":nn,"set":ns,"rarity":nr,"tier":nt,
                "price":np_,
                "p1":np1 if np1>0 else np_*0.998,
                "p3":np_*0.995,
                "p7":np7 if np7>0 else np_,
                "p30":np30 if np30>0 else np_,
                "p90":np90 if np90>0 else np_,
                "p180":np_,
                "sat":nsat,"arb":narb,
                "vel":0.50,"whale":0.45,"cross":0.52,"soc":0.50,"rep":0.25,"stab":0.55
            })
            save_cards(st.session_state.cards)
            st.success(f"✅ {nn} ajoutée !"); st.rerun()
        else:
            st.error("Remplis le nom et le prix.")

with st.expander("📂  Importer un CSV"):
    st.markdown("**Format :** `id, name, set, rarity, tier, price, p1, p7, p30, p90, sat, arb`")
    up = st.file_uploader("CSV",type=["csv"])
    if up:
        try:
            idf=pd.read_csv(up,skipinitialspace=True)
            idf.columns=idf.columns.str.strip().str.lower()
            added=0
            for _,r in idf.iterrows():
                st.session_state.cards.append({
                    "id":str(r.get("id",f"imp-{added}")),
                    "name":str(r.get("name","Unknown")),
                    "set":str(r.get("set","UNK")),
                    "rarity":str(r.get("rarity","—")),
                    "tier":str(r.get("tier","B")),
                    "price":float(r.get("price",0)),
                    "p1":float(r.get("p1",r.get("price",0))),
                    "p3":float(r.get("p3",r.get("price",0))),
                    "p7":float(r.get("p7",r.get("price",0))),
                    "p30":float(r.get("p30",r.get("price",0))),
                    "p90":float(r.get("p90",r.get("price",0))),
                    "p180":float(r.get("p180",r.get("price",0))),
                    "sat":float(r.get("sat",0.06)),
                    "arb":float(r.get("arb",0.45)),
                    "vel":0.50,"whale":0.45,"cross":0.52,"soc":0.50,"rep":0.25,"stab":0.55
                })
                added+=1
            save_cards(st.session_state.cards)
            st.success(f"✅ {added} cartes importées !"); st.rerun()
        except Exception as e:
            st.error(f"Erreur : {e}")

with st.expander("⚙️  Paramètres"):
    col1,col2=st.columns(2)
    with col1:
        if st.button("Réinitialiser toutes les cartes"):
            st.session_state.cards=ALL_CARDS.copy()
            save_cards(st.session_state.cards)
            st.success("Réinitialisé."); st.rerun()
    with col2:
        st.download_button("Exporter JSON",
            data=json.dumps(st.session_state.cards,indent=2,ensure_ascii=False),
            file_name="nasty_model_cards.json",mime="application/json")

st.markdown(f'<p style="color:#252840;font-size:11px;text-align:center;margin-top:2rem">The Nasty Model · {len(st.session_state.cards)} cartes · USD/CAD {USD_CAD}</p>',unsafe_allow_html=True)
