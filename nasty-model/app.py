import streamlit as st
import pandas as pd
import json, os, requests
from datetime import datetime
from cards_data import ALL_CARDS

st.set_page_config(page_title="The Nasty Model", page_icon="🃏", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background: #0a0c12; color: #e2e8f0; }
.block-container { padding: 1.5rem 2rem 3rem; max-width: 1400px; }

/* Sidebar */
section[data-testid="stSidebar"] { background: #0d0f1c !important; border-right: 1px solid #1a1f35; }
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p { color: #4a5568 !important; font-size: 11px !important; }
section[data-testid="stSidebar"] h3 { color: #e2e8f0 !important; }
section[data-testid="stSidebar"] .stSelectbox > div > div,
section[data-testid="stSidebar"] .stTextInput > div > div > input,
section[data-testid="stSidebar"] .stNumberInput > div > div > input {
  background: #12152a !important; border: 1px solid #1a1f35 !important;
  color: #e2e8f0 !important; border-radius: 8px !important; font-size: 13px !important;
}
.stButton > button {
  background: #12152a; color: #64748b; border: 1px solid #1a1f35;
  border-radius: 8px; font-size: 12px; font-weight: 500; width: 100%;
}
.stButton > button:hover { background: #1a1f35; color: #e2e8f0; }
.stButton > button[kind="primary"] {
  background: linear-gradient(135deg, #06b6d4, #0891b2);
  border: none; color: #fff; font-weight: 700;
}
[data-testid="stExpander"] { background: #0d0f1c; border: 1px solid #1a1f35; border-radius: 12px; }
hr { border: none; border-top: 1px solid #1a1f35; }

/* Card item — exact Collectr style */
.card-item {
  display: flex;
  align-items: center;
  gap: 18px;
  padding: 16px 20px;
  background: #0d0f1c;
  border-radius: 14px;
  margin-bottom: 8px;
  border: 1px solid #1a1f35;
  transition: border-color .15s, background .15s;
}
.card-item:hover { background: #0f1222; border-color: #2a3050; }

.card-thumb {
  width: 70px;
  height: 98px;
  object-fit: cover;
  border-radius: 7px;
  flex-shrink: 0;
  box-shadow: 0 4px 16px rgba(0,0,0,.6);
}
.card-thumb-ph {
  width: 70px; height: 98px; border-radius: 7px; flex-shrink: 0;
  background: #12152a; display: flex; align-items: center; justify-content: center;
  font-size: 28px; border: 1px solid #1a1f35;
}
.card-info { flex: 1; min-width: 0; }
.card-name {
  font-size: 17px; font-weight: 700; color: #f1f5f9;
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  margin-bottom: 4px;
}
.card-set-link {
  font-size: 12px; color: #06b6d4; font-weight: 500;
  text-decoration: none; display: block; margin-bottom: 3px;
}
.card-meta-line { font-size: 12px; color: #4a5568; line-height: 1.6; }

.card-price-block { text-align: right; flex-shrink: 0; min-width: 160px; }
.card-price-main {
  font-size: 22px; font-weight: 800; color: #10b981;
  display: flex; align-items: center; justify-content: flex-end; gap: 6px;
}
.price-arrow { font-size: 14px; }
.price-arrow.up { color: #10b981; }
.price-arrow.dn { color: #ef4444; }
.card-price-change { font-size: 13px; font-weight: 500; margin-top: 2px; }
.chg-up { color: #10b981; }
.chg-dn { color: #ef4444; }
.chg-fl { color: #4a5568; }
.card-price-qty { font-size: 11px; color: #334155; margin-top: 4px; }

.badge-pump { display:inline-block; font-size:9px; padding:2px 7px; border-radius:8px; font-weight:700; margin-left:6px; vertical-align:middle; background:rgba(239,68,68,.15); color:#ef4444; border:1px solid rgba(239,68,68,.25); }
.badge-show { display:inline-block; font-size:9px; padding:2px 7px; border-radius:8px; font-weight:700; margin-left:6px; vertical-align:middle; background:rgba(6,182,212,.12); color:#06b6d4; border:1px solid rgba(6,182,212,.25); }

.pill { display:inline-block; font-size:10px; padding:2px 7px; border-radius:10px; font-weight:600; margin-right:3px; }
.p-sir { background:rgba(139,92,246,.15); color:#a78bfa; border:1px solid rgba(139,92,246,.2); }
.p-alt { background:rgba(59,130,246,.15); color:#60a5fa; border:1px solid rgba(59,130,246,.2); }
.p-ir  { background:rgba(20,184,166,.15); color:#2dd4bf; border:1px solid rgba(20,184,166,.2); }
.p-shv { background:rgba(245,158,11,.15); color:#fbbf24; border:1px solid rgba(245,158,11,.2); }
.p-fa  { background:rgba(100,116,139,.15); color:#64748b; border:1px solid rgba(100,116,139,.2); }
.p-rr  { background:rgba(239,68,68,.15); color:#f87171; border:1px solid rgba(239,68,68,.2); }
.p-gold{ background:rgba(234,179,8,.15); color:#facc15; border:1px solid rgba(234,179,8,.2); }
.p-def { background:rgba(71,85,105,.12); color:#475569; border:1px solid rgba(71,85,105,.18); }

.show-banner {
  background: linear-gradient(135deg, #0a1a2e, #0d1f3c);
  border: 1px solid #0891b2; border-radius: 14px; padding: 14px 20px;
  display: flex; align-items: center; gap: 16px; margin-bottom: 1rem;
}
.sb-section {
  font-size: 10px; font-weight: 700; color: #2d3748 !important;
  text-transform: uppercase; letter-spacing: .08em;
  margin: 14px 0 5px; display: block;
}
.section-title {
  font-size: 20px; font-weight: 800; color: #f1f5f9; letter-spacing: -.02em;
}
.section-sub { font-size: 12px; color: #334155; margin-left: 10px; }
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

def load_json(p, d):
    if os.path.exists(p):
        with open(p) as f: return json.load(f)
    return d

def save_json(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f: json.dump(d, f, indent=2, ensure_ascii=False)

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_card_api(name, set_code):
    tcg_id = SETS.get(set_code, {}).get("tcg_id", "")
    if not tcg_id: return None
    try:
        clean = name.split("(")[0].strip()
        for suffix in [" SIR"," Alt Art"," IR"," Rainbow"," Full Art"," Shiny"," VMAX"," VSTAR"," ex"," EX"," GX"]:
            clean = clean.replace(suffix,"").strip()
        r = requests.get(f'https://api.pokemontcg.io/v2/cards?q=name:"{clean}" set.id:{tcg_id}&pageSize=8', timeout=8)
        if r.status_code == 200:
            cards = r.json().get("data", [])
            if cards: return cards[0]
    except: pass
    return None

def get_tcg_price(ac):
    if not ac: return None
    prices = ac.get("tcgplayer", {}).get("prices", {})
    for pt in ["holofoil","1stEditionHolofoil","reverseHolofoil","normal","unlimitedHolofoil"]:
        p = prices.get(pt, {}); m = p.get("market") or p.get("mid")
        if m and m > 0: return round(m * USD_CAD, 2)
    return None

def get_img(ac):
    if ac: return ac.get("images", {}).get("large") or ac.get("images", {}).get("small")
    return None

def get_gain(c, days):
    past = c.get(f"p{days}", c.get("price", 0))
    if past and past > 0: return round((c["price"]-past)/past*100, 2), round(c["price"]-past, 2)
    return 0.0, 0.0

def rar_pill(r):
    m = {"SIR":"p-sir","ALT":"p-alt","IR":"p-ir","GG":"p-alt","SHV":"p-shv",
         "SHINING":"p-shv","CLASSIC":"p-gold","FA":"p-fa","RR":"p-rr","GOLD":"p-gold"}
    return f'<span class="pill {m.get(r,"p-def")}">{r}</span>'

# ── Session ──
if "cards"     not in st.session_state: st.session_state.cards = load_json(DATA_FILE, ALL_CARDS.copy())
if "api_cache" not in st.session_state: st.session_state.api_cache = load_json(CACHE_FILE, {})

# ════ SIDEBAR ════
with st.sidebar:
    st.markdown("### 🃏 The Nasty Model")
    st.markdown("---")

    show_day = st.toggle("⚡ Mode Show Day", value=False,
        help="Affiche seulement les cartes dont le gain % est ≥ 10% sur la période choisie")

    st.markdown('<span class="sb-section">Trier & afficher par</span>', unsafe_allow_html=True)
    period_map  = {"24 heures":1, "3 jours":3, "7 jours":7, "1 mois":30, "3 mois":90, "6 mois":180}
    period_sel  = st.selectbox("", list(period_map.keys()), index=2, label_visibility="collapsed")
    days        = period_map[period_sel]

    st.markdown('<span class="sb-section">Set</span>', unsafe_allow_html=True)
    set_opts    = ["Tous les sets"] + [f"{v['name']} ({k})" for k,v in SETS.items()]
    set_filter  = st.selectbox("", set_opts, label_visibility="collapsed")

    st.markdown('<span class="sb-section">Prix C$</span>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a: prix_min = st.number_input("Min", min_value=0, value=0, step=5, label_visibility="visible")
    with col_b: prix_max = st.number_input("Max", min_value=0, value=5000, step=25, label_visibility="visible")

    st.markdown('<span class="sb-section">Recherche</span>', unsafe_allow_html=True)
    search = st.text_input("", placeholder="Nom de la carte...", label_visibility="collapsed")

    st.markdown("---")
    st.markdown(f'<div style="font-size:11px;color:#2d3748;text-align:center;margin-bottom:8px">{len(st.session_state.cards)} cartes dans la base</div>', unsafe_allow_html=True)
    if st.button("🔄  Refresh données live", type="primary"):
        st.cache_data.clear(); st.session_state.api_cache = {}
        save_json(CACHE_FILE, {}); st.rerun()

# ════ MAIN ════

# Header
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;padding:1rem 0 1.25rem;border-bottom:1px solid #1a1f35;margin-bottom:1.25rem">
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:40px;height:40px;background:linear-gradient(135deg,#06b6d4,#0891b2);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px">🃏</div>
    <div>
      <div style="font-size:20px;font-weight:800;color:#f1f5f9;letter-spacing:-.03em">The Nasty Model</div>
      <div style="font-size:11px;color:#2d3748">market intelligence · pokémon TCG · C$</div>
    </div>
  </div>
  <div style="display:flex;align-items:center;gap:8px">
    <div style="background:#0d1520;border:1px solid #0891b2;color:#06b6d4;font-size:11px;padding:4px 10px;border-radius:20px;font-weight:600">🇨🇦 CAD</div>
    <div style="background:#0d1520;border:1px solid #1a1f35;color:#334155;font-size:11px;padding:4px 10px;border-radius:20px">{datetime.now().strftime("%Y-%m-%d")}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Fetch
prog = st.empty()
rows = []
for idx, c in enumerate(st.session_state.cards):
    key = f"{c['id']}_{c['set']}"
    if key not in st.session_state.api_cache:
        prog.markdown(f'<div style="color:#2d3748;font-size:12px">⏳ Chargement {idx+1}/{len(st.session_state.cards)}...</div>', unsafe_allow_html=True)
        ac = fetch_card_api(c["id"], c["set"])
        st.session_state.api_cache[key] = {"img": get_img(ac), "live_price": get_tcg_price(ac), "ts": datetime.now().isoformat()}
        save_json(CACHE_FILE, st.session_state.api_cache)
    cached = st.session_state.api_cache[key]
    price  = cached.get("live_price") or c.get("price", 0)
    if price <= 0: price = c.get("price", 0)
    c2 = {**c, "price": price}
    gp, gc   = get_gain(c2, days)
    gp1, _   = get_gain(c2, 1)
    gp7, _   = get_gain(c2, 7)
    gp30, _  = get_gain(c2, 30)
    rows.append({**c2, "img_url": cached.get("img",""),
                 "gain_pct": gp, "gain_cad": gc,
                 "gp1": gp1, "gp7": gp7, "gp30": gp30,
                 "set_name": SETS.get(c["set"],{}).get("name", c["set"]),
                 "live": cached.get("live_price") is not None})
prog.empty()
df = pd.DataFrame(rows)

# Filters
if show_day:    df = df[df["gain_pct"] >= 10]
if prix_min > 0:   df = df[df["price"] >= prix_min]
if prix_max < 5000: df = df[df["price"] <= prix_max]
if search:
    q = search.lower()
    df = df[df["name"].str.lower().str.contains(q) | df["rarity"].str.lower().str.contains(q)]
if set_filter != "Tous les sets":
    df = df[df["set"] == set_filter.split("(")[-1].rstrip(")")]

df = df.sort_values("gain_pct", ascending=False).reset_index(drop=True)
period_lbl = {1:"24h", 3:"3j", 7:"7j", 30:"1M", 90:"3M", 180:"6M"}[days]

# Show Day banner
if show_day:
    avg = df["gain_pct"].mean() if len(df) else 0
    st.markdown(f"""
    <div class="show-banner">
      <span style="font-size:26px">⚡</span>
      <div style="flex:1">
        <div style="font-size:14px;font-weight:700;color:#06b6d4">MODE SHOW DAY — {period_lbl}</div>
        <div style="font-size:12px;color:#0e7490;margin-top:2px">Cartes avec gain ≥ 10% — vendeurs pas encore repriced</div>
      </div>
      <div style="text-align:center;background:rgba(6,182,212,.1);border:1px solid rgba(6,182,212,.2);border-radius:10px;padding:8px 18px;margin-right:8px">
        <div style="font-size:22px;font-weight:800;color:#06b6d4">{len(df)}</div>
        <div style="font-size:10px;color:#0e7490;text-transform:uppercase;letter-spacing:.06em">opportunités</div>
      </div>
      <div style="text-align:center;background:rgba(6,182,212,.1);border:1px solid rgba(6,182,212,.2);border-radius:10px;padding:8px 18px">
        <div style="font-size:22px;font-weight:800;color:#06b6d4">+{avg:.1f}%</div>
        <div style="font-size:10px;color:#0e7490;text-transform:uppercase;letter-spacing:.06em">gain moy.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

# Section title
st.markdown(f"""
<div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:14px">
  <div>
    <span class="section-title">biggest market movers</span>
    <span class="section-sub">· trié par % de gain · {period_sel}</span>
  </div>
  <span style="font-size:12px;color:#2d3748">{len(df)} cartes</span>
</div>
""", unsafe_allow_html=True)

# Cards list
if len(df) == 0:
    st.markdown('<div style="text-align:center;padding:5rem;color:#2d3748;font-size:15px">Aucune carte ne correspond aux filtres.</div>', unsafe_allow_html=True)
else:
    items_html = ""
    for _, row in df.iterrows():
        gp  = row["gain_pct"]
        gc  = row["gain_cad"]
        up  = gp >= 0
        price_color = "#10b981" if up else "#ef4444"
        arrow       = "▲" if up else "▼"
        arrow_cls   = "up" if up else "dn"
        gc_str      = f'+CA${gc:.2f}' if gc >= 0 else f'−CA${abs(gc):.2f}'
        pct_str     = f'+{gp:.2f}%' if gp >= 0 else f'{gp:.2f}%'
        img_tag     = f'<img src="{row["img_url"]}" class="card-thumb" onerror="this.style.display=\'none\';this.nextSibling.style.display=\'flex\'" /><div class="card-thumb-ph" style="display:none">🃏</div>' if row.get("img_url") else '<div class="card-thumb-ph">🃏</div>'
        bp  = '<span class="badge-pump">🔥 +24h</span>' if row["gp1"] > 5 else ""
        bs  = '<span class="badge-show">⚡ SHOW</span>' if row["gp7"] >= 10 else ""
        dot = f'<span style="color:{price_color};font-size:9px;margin-right:4px">●</span>' if row.get("live") else ""
        set_year = SETS.get(row["set"],{}).get("year","")

        items_html += f"""
<div class="card-item">
  {img_tag}
  <div class="card-info">
    <div class="card-name">{dot}{row['name']}{bp}{bs}</div>
    <div class="card-set-link">{row['set_name']}</div>
    <div class="card-meta-line">{rar_pill(row['rarity'])}</div>
    <div class="card-meta-line" style="margin-top:3px;color:#2d3748">{row['set']} · {set_year}</div>
  </div>
  <div class="card-price-block">
    <div class="card-price-main" style="color:{price_color}">
      <span class="price-arrow {arrow_cls}">{arrow}</span>
      CA${row['price']:.2f}
    </div>
    <div class="card-price-change {'chg-up' if up else 'chg-dn'}">{gc_str} ({pct_str})</div>
    <div class="card-price-qty">{period_lbl} · {'live' if row.get('live') else 'estimé'}</div>
  </div>
</div>"""

    st.markdown(items_html, unsafe_allow_html=True)

# Export
st.markdown("<hr style='margin:1.5rem 0'>", unsafe_allow_html=True)
with st.expander("📋  Liste d'achat — export CSV"):
    ex_df = df[df["gain_pct"] >= 10].copy() if not show_day else df.copy()
    if len(ex_df) > 0:
        out = ex_df[["name","set_name","rarity","price","gain_pct","gp7","gp30"]].copy()
        out.columns = ["Carte","Set","Rareté","Prix CA$",f"Gain {period_lbl} %","Gain 7j %","Gain 30j %"]
        out["Offre -15%"] = (out["Prix CA$"] * 0.85).round(2)
        out["Offre -25%"] = (out["Prix CA$"] * 0.75).round(2)
        st.dataframe(out, use_container_width=True, hide_index=True)
        st.download_button("⬇️ Télécharger CSV", data=out.to_csv(index=False),
            file_name=f"show_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", type="primary")
    else:
        st.info("Active le Mode Show Day pour générer ta liste.")

with st.expander("➕  Ajouter une carte"):
    a1, a2 = st.columns(2)
    with a1:
        nn  = st.text_input("Nom de la carte")
        ns  = st.selectbox("Set", list(SETS.keys()), format_func=lambda k: f"{SETS[k]['name']} ({k})")
        nr  = st.selectbox("Rareté", ["SIR","ALT","IR","GG","SHV","FA","RR","GOLD","HOLO","EX","Autre"])
    with a2:
        np_  = st.number_input("Prix actuel CA$", min_value=0.0, step=0.5)
        np1  = st.number_input("Prix 24h CA$",    min_value=0.0, step=0.5)
        np7  = st.number_input("Prix 7j CA$",     min_value=0.0, step=0.5)
        np30 = st.number_input("Prix 30j CA$",    min_value=0.0, step=0.5)
        np90 = st.number_input("Prix 3M CA$",     min_value=0.0, step=0.5)
    if st.button("Ajouter la carte", type="primary"):
        if nn and np_ > 0:
            st.session_state.cards.append({
                "id": f"c-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "name": nn, "set": ns, "rarity": nr, "tier": "A",
                "price": np_,
                "p1":   np1  if np1  > 0 else np_ * 0.999,
                "p3":   np_  * 0.998,
                "p7":   np7  if np7  > 0 else np_,
                "p30":  np30 if np30 > 0 else np_,
                "p90":  np90 if np90 > 0 else np_,
                "p180": np_,
                "sat": 0.06, "arb": 0.50, "vel": 0.50,
                "whale": 0.45, "cross": 0.52, "soc": 0.50, "rep": 0.25, "stab": 0.55
            })
            save_json(DATA_FILE, st.session_state.cards)
            st.success(f"✅ {nn} ajoutée !"); st.rerun()
        else:
            st.error("Remplis le nom et le prix.")

with st.expander("📂  Importer un CSV"):
    st.markdown("""
    **Format attendu :** `name, set, rarity, price, p1, p7, p30, p90`
    
    Tu peux exporter depuis Collectr et adapter les colonnes.
    """)
    up = st.file_uploader("Fichier CSV", type=["csv"])
    if up:
        try:
            idf = pd.read_csv(up, skipinitialspace=True)
            idf.columns = idf.columns.str.strip().str.lower()
            added = 0
            for _, r in idf.iterrows():
                st.session_state.cards.append({
                    "id": f"imp-{added}-{datetime.now().strftime('%H%M%S')}",
                    "name": str(r.get("name","?")), "set": str(r.get("set","UNK")),
                    "rarity": str(r.get("rarity","—")), "tier": str(r.get("tier","B")),
                    "price": float(r.get("price",0)),
                    "p1":   float(r.get("p1",   r.get("price",0))),
                    "p7":   float(r.get("p7",   r.get("price",0))),
                    "p30":  float(r.get("p30",  r.get("price",0))),
                    "p90":  float(r.get("p90",  r.get("price",0))),
                    "p180": float(r.get("p180", r.get("price",0))),
                    "sat": 0.06, "arb": 0.45, "vel": 0.50,
                    "whale": 0.45, "cross": 0.52, "soc": 0.50, "rep": 0.25, "stab": 0.55
                })
                added += 1
            save_json(DATA_FILE, st.session_state.cards)
            st.success(f"✅ {added} cartes importées !"); st.rerun()
        except Exception as e:
            st.error(f"Erreur : {e}")

with st.expander("⚙️  Paramètres"):
    p1, p2 = st.columns(2)
    with p1:
        if st.button("Réinitialiser cartes"): st.session_state.cards=ALL_CARDS.copy(); save_json(DATA_FILE,st.session_state.cards); st.rerun()
        if st.button("Vider cache prix"):     st.session_state.api_cache={}; save_json(CACHE_FILE,{}); st.cache_data.clear(); st.rerun()
    with p2:
        st.download_button("Exporter JSON", data=json.dumps(st.session_state.cards,indent=2,ensure_ascii=False), file_name="nasty_model.json", mime="application/json")
