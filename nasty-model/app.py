import streamlit as st
import pandas as pd
import json, os, requests
from datetime import datetime

st.set_page_config(page_title="The Nasty Model", page_icon="🃏", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"]{font-family:'Inter',sans-serif}
.stApp{background:#0a0c12;color:#e2e8f0}
.block-container{padding:1.5rem 2rem 3rem;max-width:1300px}
section[data-testid="stSidebar"]{background:#0d0f1c!important;border-right:1px solid #1a1f35}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p{color:#4a5568!important;font-size:11px!important}
section[data-testid="stSidebar"] .stSelectbox>div>div,
section[data-testid="stSidebar"] .stTextInput>div>div>input,
section[data-testid="stSidebar"] .stNumberInput>div>div>input{background:#12152a!important;border:1px solid #1a1f35!important;color:#e2e8f0!important;border-radius:8px!important;font-size:13px!important}
.stButton>button{background:#12152a;color:#64748b;border:1px solid #1a1f35;border-radius:8px;font-size:12px;font-weight:500;width:100%}
.stButton>button:hover{background:#1a1f35;color:#e2e8f0}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#06b6d4,#0891b2);border:none;color:#fff;font-weight:700}
[data-testid="stExpander"]{background:#0d0f1c;border:1px solid #1a1f35;border-radius:12px}
hr{border:none;border-top:1px solid #1a1f35}

.card-item{display:flex;align-items:center;gap:18px;padding:16px 20px;background:#0d0f1c;border-radius:14px;margin-bottom:8px;border:1px solid #1a1f35;transition:border-color .15s,background .15s}
.card-item:hover{background:#0f1222;border-color:#2a3050}
.card-thumb{width:68px;height:95px;object-fit:cover;border-radius:7px;flex-shrink:0;box-shadow:0 4px 16px rgba(0,0,0,.6)}
.card-thumb-ph{width:68px;height:95px;border-radius:7px;flex-shrink:0;background:#12152a;display:flex;align-items:center;justify-content:center;font-size:26px;border:1px solid #1a1f35}
.card-info{flex:1;min-width:0}
.card-name{font-size:17px;font-weight:700;color:#f1f5f9;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-bottom:4px}
.card-set-line{font-size:12px;color:#06b6d4;font-weight:500;margin-bottom:3px}
.card-meta{font-size:11px;color:#4a5568;line-height:1.7}
.card-price-block{text-align:right;flex-shrink:0;min-width:170px}
.price-main{font-size:22px;font-weight:800;display:flex;align-items:center;justify-content:flex-end;gap:5px}
.price-change{font-size:13px;font-weight:600;margin-top:2px}
.price-period{font-size:11px;color:#334155;margin-top:4px}
.up{color:#10b981}
.dn{color:#ef4444}
.fl{color:#4a5568}
.pill{display:inline-block;font-size:10px;padding:2px 7px;border-radius:10px;font-weight:600;margin-right:3px}
.p-sir{background:rgba(139,92,246,.15);color:#a78bfa;border:1px solid rgba(139,92,246,.2)}
.p-alt{background:rgba(59,130,246,.15);color:#60a5fa;border:1px solid rgba(59,130,246,.2)}
.p-ir{background:rgba(20,184,166,.15);color:#2dd4bf;border:1px solid rgba(20,184,166,.2)}
.p-shv{background:rgba(245,158,11,.15);color:#fbbf24;border:1px solid rgba(245,158,11,.2)}
.p-fa{background:rgba(100,116,139,.15);color:#64748b;border:1px solid rgba(100,116,139,.2)}
.p-rr{background:rgba(239,68,68,.15);color:#f87171;border:1px solid rgba(239,68,68,.2)}
.p-gold{background:rgba(234,179,8,.15);color:#facc15;border:1px solid rgba(234,179,8,.2)}
.p-def{background:rgba(71,85,105,.12);color:#475569;border:1px solid rgba(71,85,105,.18)}
.badge-pump{font-size:9px;padding:2px 7px;border-radius:8px;font-weight:700;margin-left:6px;vertical-align:middle;background:rgba(239,68,68,.15);color:#ef4444;border:1px solid rgba(239,68,68,.25)}
.badge-show{font-size:9px;padding:2px 7px;border-radius:8px;font-weight:700;margin-left:6px;vertical-align:middle;background:rgba(6,182,212,.12);color:#06b6d4;border:1px solid rgba(6,182,212,.25)}
.show-banner{background:linear-gradient(135deg,#0a1a2e,#0d1f3c);border:1px solid #0891b2;border-radius:14px;padding:14px 20px;display:flex;align-items:center;gap:16px;margin-bottom:1rem}
.sb-section{font-size:10px;font-weight:700;color:#2d3748!important;text-transform:uppercase;letter-spacing:.08em;margin:14px 0 5px;display:block}
.stat-box{text-align:center;background:rgba(6,182,212,.1);border:1px solid rgba(6,182,212,.2);border-radius:10px;padding:8px 18px}
.stat-v{font-size:22px;font-weight:800;color:#06b6d4}
.stat-l{font-size:10px;color:#0e7490;text-transform:uppercase;letter-spacing:.06em}
</style>
""", unsafe_allow_html=True)

USD_CAD    = 1.364
CACHE_FILE = "data/tcgdex_cache.json"

# TCGdex set ID mapping
SETS = {
    "xy1":{"name":"XY Base","code":"XY","year":2014},
    "xy2":{"name":"Flashfire","code":"FLF","year":2014},
    "xy6":{"name":"Roaring Skies","code":"ROS","year":2015},
    "xy7":{"name":"Ancient Origins","code":"AOR","year":2015},
    "xy8":{"name":"BREAKthrough","code":"BKT","year":2015},
    "xy9":{"name":"BREAKpoint","code":"BKP","year":2016},
    "xy10":{"name":"Fates Collide","code":"FCO","year":2016},
    "xy11":{"name":"Steam Siege","code":"STS","year":2016},
    "xy12":{"name":"Evolutions","code":"EVO","year":2016},
    "sm1":{"name":"Sun & Moon","code":"SUM","year":2017},
    "sm2":{"name":"Guardians Rising","code":"GRI","year":2017},
    "sm3":{"name":"Burning Shadows","code":"BUS","year":2017},
    "sm35":{"name":"Shining Legends","code":"SHL","year":2017},
    "sm4":{"name":"Crimson Invasion","code":"CRI","year":2017},
    "sm5":{"name":"Ultra Prism","code":"UPR","year":2018},
    "sm6":{"name":"Forbidden Light","code":"FLI","year":2018},
    "sm7":{"name":"Celestial Storm","code":"CES","year":2018},
    "sm8":{"name":"Lost Thunder","code":"LOT","year":2018},
    "sm9":{"name":"Team Up","code":"TEU","year":2019},
    "sm10":{"name":"Unbroken Bonds","code":"UNB","year":2019},
    "sm11":{"name":"Unified Minds","code":"UNM","year":2019},
    "hif":{"name":"Hidden Fates","code":"HIF","year":2019},
    "sm12":{"name":"Cosmic Eclipse","code":"CEC","year":2019},
    "swsh2":{"name":"Rebel Clash","code":"RCL","year":2020},
    "swsh3":{"name":"Darkness Ablaze","code":"DAA","year":2020},
    "swsh4":{"name":"Vivid Voltage","code":"VIV","year":2020},
    "shf":{"name":"Shining Fates","code":"SHF","year":2021},
    "swsh5":{"name":"Battle Styles","code":"BST","year":2021},
    "swsh6":{"name":"Chilling Reign","code":"CRE","year":2021},
    "swsh7":{"name":"Evolving Skies","code":"EVS","year":2021},
    "swsh8":{"name":"Fusion Strike","code":"FST","year":2021},
    "cel25":{"name":"Celebrations","code":"CEL","year":2021},
    "swsh9":{"name":"Brilliant Stars","code":"BRS","year":2022},
    "swsh10":{"name":"Astral Radiance","code":"ASR","year":2022},
    "pgo":{"name":"Pokémon GO","code":"PGO","year":2022},
    "swsh11":{"name":"Lost Origin","code":"LOR","year":2022},
    "swsh12":{"name":"Silver Tempest","code":"SIT","year":2022},
    "swsh125":{"name":"Crown Zenith","code":"CRZ","year":2023},
    "sv1":{"name":"Scarlet & Violet","code":"SVI","year":2023},
    "sv2":{"name":"Paldea Evolved","code":"PAL","year":2023},
    "sv3":{"name":"Obsidian Flames","code":"OBF","year":2023},
    "sv3pt5":{"name":"Pokémon 151","code":"MEW","year":2023},
    "sv4":{"name":"Paradox Rift","code":"PAR","year":2023},
    "sv4pt5":{"name":"Paldean Fates","code":"PAF","year":2024},
    "sv5":{"name":"Temporal Forces","code":"TEF","year":2024},
    "sv6":{"name":"Twilight Masquerade","code":"TWM","year":2024},
    "sv6pt5":{"name":"Shrouded Fable","code":"SFA","year":2024},
    "sv7":{"name":"Stellar Crown","code":"SCR","year":2024},
    "sv8":{"name":"Surging Sparks","code":"SSP","year":2024},
    "sv8pt5":{"name":"Prismatic Evolutions","code":"PRE","year":2025},
    "sv9":{"name":"Journey Together","code":"JTG","year":2025},
    "sv9pt5":{"name":"Destined Rivals","code":"DRI","year":2025},
    "sv10":{"name":"Mega Evolution","code":"MEG","year":2025},
    "sv10pt5":{"name":"Phantasmal Flames","code":"PHF","year":2025},
    "sv11":{"name":"Ascended Heroes","code":"ASH","year":2026},
    "sv11pt5":{"name":"Perfect Order","code":"PFO","year":2026},
    "sv12":{"name":"Chaos Rising","code":"CRS","year":2026},
}

# Rarities to track — high-value cards only
TARGET_RARITIES = {
    "Special Illustration Rare", "Illustration Rare",
    "Hyper Rare", "Ultra Rare", "Secret Rare",
    "Shiny Rare", "Shiny Ultra Rare",
    "Double Rare", "Trainer Gallery Rare Holo",
    "Radiant Rare", "LEGEND", "Gold Rare",
    "Amazing Rare", "Promo"
}

RARITY_DISPLAY = {
    "Special Illustration Rare": "SIR",
    "Illustration Rare": "IR",
    "Hyper Rare": "HR",
    "Ultra Rare": "UR",
    "Secret Rare": "Secret",
    "Shiny Rare": "Shiny",
    "Shiny Ultra Rare": "SHV",
    "Double Rare": "RR",
    "Trainer Gallery Rare Holo": "TG",
    "Radiant Rare": "Radiant",
    "Gold Rare": "Gold",
    "Amazing Rare": "AR",
    "Promo": "Promo",
}

def load_json(p, d):
    if os.path.exists(p):
        with open(p) as f: return json.load(f)
    return d

def save_json(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f: json.dump(d, f, indent=2, ensure_ascii=False)

@st.cache_data(ttl=86400, show_spinner=False)
def fetch_set_cards(set_id):
    """Fetch ALL cards for a set from TCGdex — includes prices + images, no API key"""
    try:
        url = f"https://api.tcgdex.net/v2/en/sets/{set_id}"
        r = requests.get(url, timeout=15, headers={"User-Agent": "NastyModel/2.0"})
        if r.status_code == 200:
            data = r.json()
            cards = data.get("cards", [])
            # Fetch each card detail for pricing
            results = []
            for card_brief in cards:
                card_id = card_brief.get("id", "")
                try:
                    cr = requests.get(f"https://api.tcgdex.net/v2/en/cards/{card_id}", timeout=8,
                                      headers={"User-Agent": "NastyModel/2.0"})
                    if cr.status_code == 200:
                        results.append(cr.json())
                except: pass
            return results
    except: pass
    return []

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_single_card(card_id):
    """Fetch a single card by TCGdex ID"""
    try:
        r = requests.get(f"https://api.tcgdex.net/v2/en/cards/{card_id}", timeout=8,
                         headers={"User-Agent": "NastyModel/2.0"})
        if r.status_code == 200:
            return r.json()
    except: pass
    return None

def extract_price_and_changes(card_data):
    """Extract price + historical changes from TCGdex response"""
    pricing = card_data.get("pricing", {})
    tcgp    = pricing.get("tcgplayer", {})
    cm      = pricing.get("cardmarket", {})

    # TCGPlayer USD → CAD
    price_usd = None
    for variant in ["holo","reverseHolo","normal","1stEditionHolo"]:
        v = tcgp.get(variant, {})
        mp = v.get("marketPrice") or v.get("midPrice")
        if mp and mp > 0:
            price_usd = mp
            break

    # Cardmarket EUR (fallback)
    if not price_usd:
        trend = cm.get("trend") or cm.get("avg")
        if trend and trend > 0:
            price_usd = trend * 1.10  # rough EUR→USD

    if not price_usd:
        return None

    price_cad = round(price_usd * USD_CAD, 2)

    # Historical: cardmarket avg1/avg7/avg30 → calculate % changes
    avg1  = cm.get("avg1",  cm.get("avg1-holo"))
    avg7  = cm.get("avg7",  cm.get("avg7-holo"))
    avg30 = cm.get("avg30", cm.get("avg30-holo"))

    def pct(past_eur):
        if past_eur and past_eur > 0:
            past_cad = past_eur * 1.10 * USD_CAD
            return round((price_cad - past_cad) / past_cad * 100, 2)
        return 0.0

    return {
        "price":  price_cad,
        "p1":     round(avg1  * 1.10 * USD_CAD, 2) if avg1  else price_cad,
        "p7":     round(avg7  * 1.10 * USD_CAD, 2) if avg7  else price_cad,
        "p30":    round(avg30 * 1.10 * USD_CAD, 2) if avg30 else price_cad,
        "chg1":   pct(avg1),
        "chg7":   pct(avg7),
        "chg30":  pct(avg30),
    }

def get_card_image(card_data):
    img = card_data.get("image", "")
    if img:
        return img + "/high.png"
    return ""

def rar_pill(r):
    m = {"SIR":"p-sir","IR":"p-ir","Shiny":"p-shv","SHV":"p-shv","HR":"p-rr",
         "UR":"p-alt","Secret":"p-gold","RR":"p-alt","Gold":"p-gold","TG":"p-fa"}
    return f'<span class="pill {m.get(r,"p-def")}">{r}</span>'

# ── Session ──
if "api_cache"   not in st.session_state: st.session_state.api_cache   = load_json(CACHE_FILE, {})
if "loaded_sets" not in st.session_state: st.session_state.loaded_sets = set()
if "all_cards"   not in st.session_state: st.session_state.all_cards   = []

# ════ SIDEBAR ════
with st.sidebar:
    st.markdown("### 🃏 The Nasty Model")
    st.markdown("---")

    show_day = st.toggle("⚡ Mode Show Day", value=False,
        help="Affiche seulement les cartes avec gain ≥ 10% sur la période choisie")

    st.markdown('<span class="sb-section">Période & tri</span>', unsafe_allow_html=True)
    period_map  = {"24 heures": "chg1", "7 jours": "chg7", "30 jours": "chg30"}
    period_lbl_map = {"24 heures":"24h","7 jours":"7j","30 jours":"1M"}
    period_sel  = st.selectbox("", list(period_map.keys()), index=1, label_visibility="collapsed")
    chg_key     = period_map[period_sel]
    period_lbl  = period_lbl_map[period_sel]

    st.markdown('<span class="sb-section">Set à charger</span>', unsafe_allow_html=True)
    set_opts    = ["Tous les sets chargés"] + [f"{v['name']} ({k})" for k,v in SETS.items()]
    set_filter  = st.selectbox("", set_opts, label_visibility="collapsed")

    st.markdown('<span class="sb-section">Charger un set</span>', unsafe_allow_html=True)
    sets_to_load = st.multiselect(
        "", [f"{v['name']} ({k})" for k,v in SETS.items()],
        default=["Surging Sparks (sv8)","Prismatic Evolutions (sv8pt5)","Ascended Heroes (sv11)"],
        label_visibility="collapsed"
    )

    st.markdown('<span class="sb-section">Prix C$</span>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a: prix_min = st.number_input("Min", min_value=0, value=0, step=5)
    with col_b: prix_max = st.number_input("Max", min_value=0, value=5000, step=25)

    st.markdown('<span class="sb-section">Recherche</span>', unsafe_allow_html=True)
    search = st.text_input("", placeholder="Nom...", label_visibility="collapsed")

    st.markdown("---")
    if st.button("📥  Charger les sets sélectionnés", type="primary"):
        for s_opt in sets_to_load:
            sid = s_opt.split("(")[-1].rstrip(")")
            if sid not in st.session_state.loaded_sets:
                with st.spinner(f"Chargement {SETS[sid]['name']}..."):
                    cards = fetch_set_cards(sid)
                    for c in cards:
                        rarity_full = c.get("rarity","")
                        if rarity_full in TARGET_RARITIES:
                            price_data = extract_price_and_changes(c)
                            if price_data:
                                st.session_state.all_cards.append({
                                    "id":       c.get("id",""),
                                    "name":     c.get("name",""),
                                    "set_id":   sid,
                                    "set_name": SETS[sid]["name"],
                                    "set_year": SETS[sid]["year"],
                                    "rarity":   RARITY_DISPLAY.get(rarity_full, rarity_full),
                                    "number":   c.get("localId",""),
                                    "img":      get_card_image(c),
                                    **price_data
                                })
                    st.session_state.loaded_sets.add(sid)
        save_json(CACHE_FILE, {"cards": st.session_state.all_cards, "sets": list(st.session_state.loaded_sets)})
        st.rerun()

    if st.button("🔄  Vider & recharger"):
        st.session_state.all_cards   = []
        st.session_state.loaded_sets = set()
        fetch_set_cards.clear()
        save_json(CACHE_FILE, {})
        st.rerun()

    loaded_count = len(st.session_state.loaded_sets)
    card_count   = len(st.session_state.all_cards)
    st.markdown(f'<div style="font-size:11px;color:#2d3748;text-align:center;margin-top:4px">{loaded_count} sets chargés · {card_count} cartes</div>', unsafe_allow_html=True)

# Load from disk cache on startup
if not st.session_state.all_cards and os.path.exists(CACHE_FILE):
    cached = load_json(CACHE_FILE, {})
    if "cards" in cached:
        st.session_state.all_cards   = cached["cards"]
        st.session_state.loaded_sets = set(cached.get("sets", []))

# ════ MAIN ════
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;padding:1rem 0 1.25rem;border-bottom:1px solid #1a1f35;margin-bottom:1.25rem">
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:40px;height:40px;background:linear-gradient(135deg,#06b6d4,#0891b2);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px">🃏</div>
    <div>
      <div style="font-size:20px;font-weight:800;color:#f1f5f9;letter-spacing:-.03em">The Nasty Model</div>
      <div style="font-size:11px;color:#2d3748">prix live TCGdex · C$ · {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
    </div>
  </div>
  <div style="display:flex;gap:8px">
    <div style="background:#0d1520;border:1px solid #0891b2;color:#06b6d4;font-size:11px;padding:4px 10px;border-radius:20px;font-weight:600">🇨🇦 CAD</div>
    <div style="background:#0d1520;border:1px solid #1a1f35;color:#334155;font-size:11px;padding:4px 10px;border-radius:20px">TCGdex · no API key</div>
  </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.all_cards:
    st.markdown("""
    <div style="text-align:center;padding:5rem 2rem;color:#334155">
      <div style="font-size:48px;margin-bottom:1rem">🃏</div>
      <div style="font-size:18px;font-weight:600;color:#64748b;margin-bottom:8px">Aucune carte chargée</div>
      <div style="font-size:14px">Sélectionne des sets dans la sidebar et clique <strong style="color:#06b6d4">Charger les sets</strong></div>
      <div style="font-size:12px;color:#2d3748;margin-top:8px">Les prix viennent de TCGdex (TCGPlayer + Cardmarket) · aucune clé API requise</div>
    </div>
    """, unsafe_allow_html=True)
else:
    df = pd.DataFrame(st.session_state.all_cards)

    # Filters
    if show_day:    df = df[df[chg_key] >= 10]
    if prix_min > 0:   df = df[df["price"] >= prix_min]
    if prix_max < 5000: df = df[df["price"] <= prix_max]
    if search:      df = df[df["name"].str.lower().str.contains(search.lower(), na=False)]
    if set_filter != "Tous les sets chargés":
        sid = set_filter.split("(")[-1].rstrip(")")
        df  = df[df["set_id"] == sid]

    df = df.sort_values(chg_key, ascending=False).reset_index(drop=True)

    # Show Day banner
    if show_day:
        avg = df[chg_key].mean() if len(df) else 0
        st.markdown(f"""
        <div class="show-banner">
          <span style="font-size:26px">⚡</span>
          <div style="flex:1">
            <div style="font-size:14px;font-weight:700;color:#06b6d4">MODE SHOW DAY — {period_sel}</div>
            <div style="font-size:12px;color:#0e7490;margin-top:2px">Cartes avec gain ≥ 10% — les vendeurs n'ont pas encore mis à jour leurs prix</div>
          </div>
          <div class="stat-box" style="margin-right:8px"><div class="stat-v">{len(df)}</div><div class="stat-l">opportunités</div></div>
          <div class="stat-box"><div class="stat-v">+{avg:.1f}%</div><div class="stat-l">gain moy.</div></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:12px">
      <div>
        <span style="font-size:18px;font-weight:800;color:#f1f5f9">biggest market movers</span>
        <span style="font-size:12px;color:#334155;margin-left:8px">· {period_sel} · trié par % de gain</span>
      </div>
      <span style="font-size:12px;color:#2d3748">{len(df)} cartes · {len(st.session_state.loaded_sets)} sets</span>
    </div>
    """, unsafe_allow_html=True)

    if len(df) == 0:
        st.markdown('<div style="text-align:center;padding:4rem;color:#2d3748;font-size:15px">Aucune carte ne correspond aux filtres.</div>', unsafe_allow_html=True)
    else:
        items = ""
        for _, row in df.iterrows():
            chg   = row[chg_key]
            up    = chg >= 0
            clr   = "#10b981" if up else "#ef4444"
            arrow = "▲" if up else "▼"
            price = row["price"]
            chg1  = row["chg1"]; chg7 = row["chg7"]; chg30 = row["chg30"]

            gc    = price - row.get("p7" if chg_key=="chg7" else "p1" if chg_key=="chg1" else "p30", price)
            gc_str= f'+CA${gc:.2f}' if gc >= 0 else f'−CA${abs(gc):.2f}'
            pct_str = f'+{chg:.2f}%' if chg >= 0 else f'{chg:.2f}%'

            def fmt_chg(v):
                if v > 0:  return f'<span style="color:#10b981;font-size:11px;font-weight:600">▲ +{v:.1f}%</span>'
                if v < 0:  return f'<span style="color:#ef4444;font-size:11px;font-weight:600">▼ {v:.1f}%</span>'
                return '<span style="color:#334155;font-size:11px">—</span>'

            img_html = f'<img src="{row["img"]}" class="card-thumb" onerror="this.style.display=\'none\';this.nextSibling.style.display=\'flex\'" /><div class="card-thumb-ph" style="display:none">🃏</div>' if row.get("img") else '<div class="card-thumb-ph">🃏</div>'
            bp = '<span class="badge-pump">🔥 +24h</span>' if chg1 > 5 else ""
            bs = '<span class="badge-show">⚡ SHOW</span>' if chg7 >= 10 else ""

            items += f"""
<div class="card-item">
  {img_html}
  <div class="card-info">
    <div class="card-name">{row['name']}{bp}{bs}</div>
    <div class="card-set-line">{row['set_name']}</div>
    <div class="card-meta">{rar_pill(row['rarity'])} &nbsp;#{row['number']} · {row['set_id'].upper()} · {row['set_year']}</div>
    <div style="margin-top:6px;display:flex;gap:12px">
      <span style="font-size:11px;color:#334155">24h: {fmt_chg(chg1)}</span>
      <span style="font-size:11px;color:#334155">7j: {fmt_chg(chg7)}</span>
      <span style="font-size:11px;color:#334155">30j: {fmt_chg(chg30)}</span>
    </div>
  </div>
  <div class="card-price-block">
    <div class="price-main" style="color:{clr}">
      <span style="font-size:14px">{arrow}</span> CA${price:.2f}
    </div>
    <div class="price-change" style="color:{clr}">{gc_str} ({pct_str})</div>
    <div class="price-period">{period_sel} · TCGdex live</div>
  </div>
</div>"""

        st.markdown(items, unsafe_allow_html=True)

    # Export
    st.markdown("<hr style='margin:1.5rem 0'>", unsafe_allow_html=True)
    with st.expander("📋  Liste d'achat — export CSV"):
        ex = df[df[chg_key] >= 10].copy() if not show_day else df.copy()
        if len(ex) > 0:
            out = ex[["name","set_name","rarity","price","chg1","chg7","chg30"]].copy()
            out.columns = ["Carte","Set","Rareté","Prix CA$","Gain 24h %","Gain 7j %","Gain 30j %"]
            out["Offre -15%"] = (out["Prix CA$"] * 0.85).round(2)
            out["Offre -25%"] = (out["Prix CA$"] * 0.75).round(2)
            st.dataframe(out, use_container_width=True, hide_index=True)
            st.download_button("⬇️ Télécharger CSV", data=out.to_csv(index=False),
                file_name=f"show_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", type="primary")
        else:
            st.info("Active le Mode Show Day pour générer ta liste.")

    with st.expander("⚙️  Paramètres"):
        if st.button("🗑️  Vider tous les sets & cache"):
            st.session_state.all_cards   = []
            st.session_state.loaded_sets = set()
            fetch_set_cards.clear()
            save_json(CACHE_FILE, {})
            st.rerun()
