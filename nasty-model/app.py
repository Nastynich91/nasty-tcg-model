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
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  .stApp { background-color: #0f1117; color: #e8e8e8; }
  section[data-testid="stSidebar"] { background-color: #0f1117; }
  .block-container { padding: 1.5rem 2rem; max-width: 1600px; }
  h1,h2,h3 { color: #ffffff; }
  div[data-testid="metric-container"] {
    background: #1a1d2e; border: 0.5px solid #2a2d3e;
    border-radius: 8px; padding: 0.65rem 1rem;
  }
  div[data-testid="metric-container"] label { color: #6b7280 !important; font-size: 12px; }
  div[data-testid="metric-container"] [data-testid="stMetricValue"] { color: #ffffff; font-size: 20px; }
  .stTextInput>div>div>input, .stNumberInput>div>div>input,
  .stSelectbox>div>div { background:#1a1d2e !important; color:#e8e8e8 !important; border-color:#2a2d3e !important; }
  .stButton>button { background:#1a1d2e; color:#e8e8e8; border:0.5px solid #2a2d3e; border-radius:8px; font-size:13px; }
  .stButton>button:hover { background:#2a2d3e; }
  hr { border-color: #1e2130; }
  [data-testid="stExpander"] { background:#1a1d2e; border:0.5px solid #2a2d3e; border-radius:8px; }
  table.nasty { width:100%; border-collapse:collapse; }
  table.nasty th { font-size:11px; color:#4b5563; font-weight:500; text-align:left; padding:7px 10px; border-bottom:0.5px solid #1e2130; letter-spacing:.04em; }
  table.nasty td { padding:8px 10px; border-bottom:0.5px solid #161820; vertical-align:middle; font-size:13px; }
  table.nasty tr:hover td { background:#1a1d2e; }
  .pill-green  { background:#14532d; color:#4ade80; padding:2px 9px; border-radius:20px; font-size:10px; font-weight:500; }
  .pill-red    { background:#450a0a; color:#f87171; padding:2px 9px; border-radius:20px; font-size:10px; font-weight:500; }
  .pill-amber  { background:#451a03; color:#fbbf24; padding:2px 9px; border-radius:20px; font-size:10px; font-weight:500; }
  .pill-blue   { background:#0c1a3a; color:#60a5fa; padding:2px 9px; border-radius:20px; font-size:10px; font-weight:500; }
  .pill-purple { background:#2e1065; color:#c084fc; padding:2px 9px; border-radius:20px; font-size:10px; font-weight:500; }
  .pill-gray   { background:#1f2937; color:#9ca3af; padding:2px 9px; border-radius:20px; font-size:10px; font-weight:500; }
  .pill-teal   { background:#042f2e; color:#2dd4bf; padding:2px 9px; border-radius:20px; font-size:10px; font-weight:500; }
  .nps-green { color:#4ade80; font-weight:600; font-size:14px; }
  .nps-amber { color:#fbbf24; font-weight:600; font-size:14px; }
  .nps-red   { color:#f87171; font-weight:600; font-size:14px; }
  .gain-pos  { color:#4ade80; font-weight:500; }
  .gain-neg  { color:#f87171; font-weight:500; }
  .gain-neu  { color:#9ca3af; }
  .upside-card { background:#1a1d2e; border:0.5px solid #2a2d3e; border-radius:10px; padding:.85rem 1rem; margin-bottom:8px; }
  .upside-top  { background:#1a1d2e; border:1.5px solid #1d4ed8; border-radius:10px; padding:.85rem 1rem; margin-bottom:8px; }
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
    st   = SETS.get(c["set"],{}).get("status","in")
    pv   = PRINT_SCORE.get(st,0.2)
    tv   = TIER_SCORE.get(c["tier"],0.3)
    sat  = max(0.01,c["sat"])
    w    = ((1-sat)*0.20+c["arb"]*0.18+c["vel"]*0.15+pv*0.25+
             tv*0.12+(1-c["rep"])*0.10+c["stab"]*0.08+
             c["whale"]*0.06+c["cross"]*0.05+c["soc"]*0.04)
    hype = 1+c["cross"]*0.20+c["soc"]*0.15
    return min(100,int((w/sat)*hype*35))

def calc_signal(nps,gain_pct,status):
    pv   = PRINT_SCORE.get(status,0.2)
    fund = (nps/100)*0.6+pv*0.4
    if fund>0.72 and gain_pct<8:  return "sous"
    if fund<0.40 and gain_pct>15: return "sur"
    return "juste"

def get_gain(c,days):
    past = c.get(f"p{days}",c["price"])
    if past and past>0:
        return round((c["price"]-past)/past*100,2), round(c["price"]-past,2)
    return 0.0,0.0

if "cards" not in st.session_state:
    st.session_state.cards = load_cards()

cards = st.session_state.cards

# ── Header ───────────────────────────────────
st.markdown("""
<div style="display:flex;align-items:center;gap:14px;margin-bottom:1.25rem">
  <div style="width:46px;height:46px;background:#1e2130;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0">🃏</div>
  <div>
    <h1 style="margin:0;font-size:22px">The Nasty Model</h1>
    <p style="color:#6b7280;margin:0;font-size:13px">Screener TCG · Top movers · NPS upside · Valeurs en C$</p>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Controls ──────────────────────────────────
c1,c2,c3,c4,c5,c6 = st.columns([3,2,1.5,1.8,1.8,1.5])
with c1:
    search = st.text_input("","",placeholder="🔍  Rechercher carte, set, rareté...",label_visibility="collapsed")
with c2:
    set_opts = ["Tous les sets"] + [f"{v['name']} ({k})" for k,v in SETS.items()]
    set_filter = st.selectbox("Set",set_opts,label_visibility="collapsed")
with c3:
    rar_filter = st.selectbox("Rareté",["Toutes","SIR","ALT","IR","GG","SHV","SHINING","CLASSIC","FA","RR","GOLD","HOLO","EX","OTHER"],label_visibility="collapsed")
with c4:
    sig_filter = st.selectbox("Signal",["Tous","Sous-évaluées","Surévaluées","Prix juste"],label_visibility="collapsed")
with c5:
    period     = st.selectbox("Période",["1 jour","7 jours","30 jours"],index=1,label_visibility="collapsed")
with c6:
    sort_by    = st.selectbox("Trier",["% gain","$ gain","NPS","Prix","Nom"],label_visibility="collapsed")

days     = {"1 jour":1,"7 jours":7,"30 jours":30}[period]
sort_key = {"% gain":"gain_pct","$ gain":"gain_cad","NPS":"nps","Prix":"price","Nom":"name"}[sort_by]

# ── Build data ────────────────────────────────
rows = []
for c in cards:
    nps      = calc_nps(c)
    gp,gc    = get_gain(c,days)
    st_code  = SETS.get(c["set"],{}).get("status","in")
    signal   = calc_signal(nps,gp,st_code)
    set_name = SETS.get(c["set"],{}).get("name",c["set"])
    rows.append({**c,"nps":nps,"gain_pct":gp,"gain_cad":gc,"signal":signal,"set_name":set_name,"status":st_code})

df = pd.DataFrame(rows)

# Filters
if search:
    q = search.lower()
    df = df[df["name"].str.lower().str.contains(q)|
            df["set"].str.lower().str.contains(q)|
            df["set_name"].str.lower().str.contains(q)|
            df["rarity"].str.lower().str.contains(q)]
if set_filter!="Tous les sets":
    code = set_filter.split("(")[-1].rstrip(")")
    df = df[df["set"]==code]
if rar_filter!="Toutes":
    if rar_filter=="OTHER":
        known = ["SIR","ALT","IR","GG","SHV","SHINING","CLASSIC","FA","RR","GOLD","HOLO","EX"]
        df = df[~df["rarity"].isin(known)]
    else:
        df = df[df["rarity"]==rar_filter]
sig_map = {"Sous-évaluées":"sous","Surévaluées":"sur","Prix juste":"juste"}
if sig_filter!="Tous":
    df = df[df["signal"]==sig_map[sig_filter]]

asc = sort_key=="name"
df  = df.sort_values(sort_key,ascending=asc).reset_index(drop=True)

# ── Stats ─────────────────────────────────────
m1,m2,m3,m4,m5 = st.columns(5)
m1.metric("cartes",len(df))
m2.metric("sous-évaluées 🟢",int((df["signal"]=="sous").sum()))
m3.metric("surévaluées 🔴",  int((df["signal"]=="sur").sum()))
m4.metric("prix juste 🟡",   int((df["signal"]=="juste").sum()))
m5.metric("NPS moyen",       int(df["nps"].mean()) if len(df) else 0)
st.markdown("---")

# ── Helpers ───────────────────────────────────
def signal_html(s):
    if s=="sous": return '<span class="pill-green">SOUS-ÉV.</span>'
    if s=="sur":  return '<span class="pill-red">SUR-ÉV.</span>'
    return '<span class="pill-amber">PRIX JUSTE</span>'

def tier_html(t):
    m={"S":"pill-purple","A":"pill-blue","B":"pill-teal","C":"pill-gray"}
    return f'<span class="{m.get(t,"pill-gray")}">{t}</span>'

def rar_html(r):
    m={"SIR":"pill-purple","ALT":"pill-blue","IR":"pill-teal","GG":"pill-blue",
       "SHV":"pill-amber","SHINING":"pill-amber","CLASSIC":"pill-amber",
       "FA":"pill-gray","RR":"pill-red","GOLD":"pill-amber"}
    return f'<span class="{m.get(r,"pill-gray")}">{r}</span>'

def nps_html(n):
    c="nps-green" if n>=85 else "nps-amber" if n>=65 else "nps-red"
    return f'<span class="{c}">{n}</span>'

def gain_html(v,sfx):
    if v>0:  return f'<span class="gain-pos">+{v:.1f}{sfx}</span>'
    if v<0:  return f'<span class="gain-neg">{v:.1f}{sfx}</span>'
    return f'<span class="gain-neu">0.0{sfx}</span>'

# ── Table ─────────────────────────────────────
rows_html=""
for i,row in df.iterrows():
    rows_html+=f"""<tr>
      <td style="color:#4b5563;font-size:11px">{i+1}</td>
      <td>
        <div style="font-weight:500;color:#fff;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:240px">{row['name']}</div>
        <div style="font-size:10px;color:#4b5563">{row['set_name']} · {rar_html(row['rarity'])} · {tier_html(row['tier'])}</div>
      </td>
      <td style="text-align:right;font-weight:500;color:#fff;white-space:nowrap">C${row['price']:.0f}</td>
      <td style="text-align:right">{gain_html(row['gain_pct'],'%')}</td>
      <td style="text-align:right">{gain_html(row['gain_cad'],' C$')}</td>
      <td style="text-align:center">{signal_html(row['signal'])}</td>
      <td style="text-align:right">{nps_html(row['nps'])}</td>
    </tr>"""

st.markdown(f"""
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
</table>""",unsafe_allow_html=True)

# ── Upside ────────────────────────────────────
st.markdown("---")
st.markdown("### 🚀 Upside potential")
upside = df[df["gain_pct"]>0].sort_values("nps",ascending=False).head(5)

for i,(_,row) in enumerate(upside.iterrows()):
    cls  = "upside-top" if i==0 else "upside-card"
    badge= '<span class="pill-blue" style="background:#0c1a3a;color:#60a5fa;padding:2px 9px;border-radius:20px;font-size:10px;font-weight:500">meilleur upside</span> ' if i==0 else ""
    nc   = "#4ade80" if row["nps"]>=85 else "#fbbf24" if row["nps"]>=65 else "#f87171"
    bars = [
        ("PSA10 sat.", round((1-row["sat"])*100),"#60a5fa"),
        ("JP/EN arb.", round(row["arb"]*100),     "#4ade80"),
        ("print",      round(PRINT_SCORE.get(row["status"],0.2)*100),"#fbbf24"),
        ("whales",     round(row["whale"]*100),   "#c084fc"),
    ]
    bars_html="".join([
        f'<div style="display:flex;align-items:center;gap:6px;margin-bottom:3px">'
        f'<span style="font-size:11px;color:#4b5563;min-width:70px">{l}</span>'
        f'<div style="flex:1;background:#0f1117;border-radius:3px;height:4px;overflow:hidden">'
        f'<div style="width:{v}%;height:100%;background:{c};border-radius:3px"></div></div>'
        f'<span style="font-size:10px;color:#4b5563;min-width:26px;text-align:right">{v}%</span></div>'
        for l,v,c in bars])
    st.markdown(f"""<div class="{cls}">
      <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin-bottom:6px">
        {badge}<span style="font-size:13px;font-weight:500;color:#fff;flex:1">{row['name']} <span style="color:#4b5563;font-size:11px;font-weight:400">{row['set']}</span></span>
        <span style="color:#4ade80;font-size:12px">+{row['gain_pct']:.1f}%</span>
        <span style="font-size:16px;font-weight:600;color:{nc}">{row['nps']}<span style="font-size:11px;color:#4b5563;font-weight:400">/100</span></span>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:0 14px">{bars_html}</div>
    </div>""",unsafe_allow_html=True)

# ── Add / Import / Settings ───────────────────
st.markdown("---")
with st.expander("➕  Ajouter une carte manuellement"):
    a1,a2 = st.columns(2)
    with a1:
        nn  = st.text_input("Nom")
        ns  = st.selectbox("Set",list(SETS.keys()),format_func=lambda k:f"{SETS[k]['name']} ({k})")
        nr  = st.selectbox("Rareté",["SIR","ALT","IR","GG","SHV","SHINING","CLASSIC","FA","RR","GOLD","HOLO","EX","OTHER"])
        nt  = st.selectbox("Tier",["S","A","B","C"])
    with a2:
        np_ = st.number_input("Prix C$",min_value=0.0,step=0.5)
        np7 = st.number_input("Prix 7j C$",min_value=0.0,step=0.5)
        np30= st.number_input("Prix 30j C$",min_value=0.0,step=0.5)
        nsat= st.number_input("Saturation PSA10",min_value=0.0,max_value=1.0,value=0.06,step=0.01)
        narb= st.number_input("Arbitrage JP/EN",min_value=0.0,max_value=1.0,value=0.50,step=0.01)
    if st.button("Ajouter",type="primary"):
        if nn and np_>0:
            st.session_state.cards.append({
                "id":f"custom-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "name":nn,"set":ns,"rarity":nr,"tier":nt,
                "price":np_,"p1":np_*0.998,
                "p7":np7 if np7>0 else np_,
                "p30":np30 if np30>0 else np_,
                "sat":nsat,"arb":narb,
                "vel":0.50,"whale":0.45,"cross":0.52,"soc":0.50,"rep":0.25,"stab":0.55
            })
            save_cards(st.session_state.cards)
            st.success(f"✅ {nn} ajoutée !"); st.rerun()
        else:
            st.error("Remplis le nom et le prix.")

with st.expander("📂  Importer un CSV"):
    st.markdown("**Format :** `id, name, set, rarity, tier, price, p7, p30, sat, arb`")
    up = st.file_uploader("CSV",type=["csv"])
    if up:
        try:
            idf = pd.read_csv(up,skipinitialspace=True)
            idf.columns = idf.columns.str.strip().str.lower()
            added=0
            for _,r in idf.iterrows():
                st.session_state.cards.append({
                    "id":str(r.get("id",f"imp-{added}")),
                    "name":str(r.get("name","Unknown")),
                    "set":str(r.get("set","UNK")),
                    "rarity":str(r.get("rarity","—")),
                    "tier":str(r.get("tier","B")),
                    "price":float(r.get("price",0)),
                    "p1":float(r.get("price",0))*0.998,
                    "p7":float(r.get("p7",r.get("price",0))),
                    "p30":float(r.get("p30",r.get("price",0))),
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
    col1,col2 = st.columns(2)
    with col1:
        if st.button("Réinitialiser toutes les cartes"):
            st.session_state.cards = ALL_CARDS.copy()
            save_cards(st.session_state.cards)
            st.success("Base réinitialisée."); st.rerun()
    with col2:
        st.download_button("Exporter JSON",
            data=json.dumps(st.session_state.cards,indent=2,ensure_ascii=False),
            file_name="nasty_model_cards.json",mime="application/json")

st.markdown(f'<p style="color:#2a2d3e;font-size:11px;text-align:center;margin-top:1.5rem">The Nasty Model · {len(st.session_state.cards)} cartes · USD/CAD {USD_CAD}</p>',unsafe_allow_html=True)
