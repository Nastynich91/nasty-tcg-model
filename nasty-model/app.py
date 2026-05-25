import streamlit as st
import pandas as pd
import json, os, requests
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

st.set_page_config(page_title="The Nasty Model", page_icon="🃏", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html,body,[class*="css"]{font-family:'Inter',sans-serif}
.stApp{background:#0a0c12;color:#e2e8f0}
.block-container{padding:1.5rem 2rem 3rem;max-width:1300px}
section[data-testid="stSidebar"]{background:#0d0f1c!important;border-right:1px solid #1a1f35}
section[data-testid="stSidebar"] label,section[data-testid="stSidebar"] p{color:#4a5568!important;font-size:11px!important}
section[data-testid="stSidebar"] .stSelectbox>div>div,
section[data-testid="stSidebar"] .stTextInput>div>div>input,
section[data-testid="stSidebar"] .stNumberInput>div>div>input{background:#12152a!important;border:1px solid #1a1f35!important;color:#e2e8f0!important;border-radius:8px!important;font-size:13px!important}
.stButton>button{background:#12152a;color:#64748b;border:1px solid #1a1f35;border-radius:8px;font-size:12px;font-weight:500;width:100%}
.stButton>button:hover{background:#1a1f35;color:#e2e8f0}
.stButton>button[kind="primary"]{background:linear-gradient(135deg,#06b6d4,#0891b2);border:none;color:#fff;font-weight:700}
[data-testid="stExpander"]{background:#0d0f1c;border:1px solid #1a1f35;border-radius:12px}
hr{border:none;border-top:1px solid #1a1f35}
.card-item{display:flex;align-items:center;gap:18px;padding:16px 20px;background:#0d0f1c;border-radius:14px;margin-bottom:8px;border:1px solid #1a1f35;transition:border-color .15s}
.card-item:hover{background:#0f1222;border-color:#2a3050}
.card-thumb{width:68px;height:95px;object-fit:cover;border-radius:7px;flex-shrink:0;box-shadow:0 4px 16px rgba(0,0,0,.6)}
.card-thumb-ph{width:68px;height:95px;border-radius:7px;flex-shrink:0;background:#12152a;display:flex;align-items:center;justify-content:center;font-size:26px;border:1px solid #1a1f35}
.card-info{flex:1;min-width:0}
.card-name{font-size:17px;font-weight:700;color:#f1f5f9;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-bottom:4px}
.card-set-line{font-size:12px;color:#06b6d4;font-weight:500;margin-bottom:3px}
.card-meta{font-size:11px;color:#4a5568}
.card-price-block{text-align:right;flex-shrink:0;min-width:180px}
.price-main{font-size:22px;font-weight:800;color:#f1f5f9}
.price-change{font-size:13px;font-weight:600;margin-top:3px}
.price-source{font-size:10px;color:#334155;margin-top:4px}
.pill{display:inline-block;font-size:10px;padding:2px 7px;border-radius:10px;font-weight:600;margin-right:3px}
.p-sir{background:rgba(139,92,246,.15);color:#a78bfa;border:1px solid rgba(139,92,246,.2)}
.p-ir{background:rgba(20,184,166,.15);color:#2dd4bf;border:1px solid rgba(20,184,166,.2)}
.p-alt{background:rgba(59,130,246,.15);color:#60a5fa;border:1px solid rgba(59,130,246,.2)}
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
.api-key-box{background:#0d0f1c;border:1px solid #1a1f35;border-radius:14px;padding:24px;text-align:center;margin:2rem auto;max-width:500px}
</style>
""", unsafe_allow_html=True)

USD_CAD    = 1.364
CACHE_FILE = "data/cards_cache.json"
CACHE_TTL_HOURS = 12

SETS = {
    "xy1":    {"name":"XY Base","year":2014,"ppt_id":"xy1"},
    "xy2":    {"name":"Flashfire","year":2014,"ppt_id":"flashfire"},
    "xy6":    {"name":"Roaring Skies","year":2015,"ppt_id":"roaring-skies"},
    "xy7":    {"name":"Ancient Origins","year":2015,"ppt_id":"ancient-origins"},
    "xy8":    {"name":"BREAKthrough","year":2015,"ppt_id":"breakthrough"},
    "xy9":    {"name":"BREAKpoint","year":2016,"ppt_id":"breakpoint"},
    "xy10":   {"name":"Fates Collide","year":2016,"ppt_id":"fates-collide"},
    "xy11":   {"name":"Steam Siege","year":2016,"ppt_id":"steam-siege"},
    "xy12":   {"name":"Evolutions","year":2016,"ppt_id":"evolutions"},
    "sm1":    {"name":"Sun & Moon","year":2017,"ppt_id":"sun-moon"},
    "sm2":    {"name":"Guardians Rising","year":2017,"ppt_id":"guardians-rising"},
    "sm3":    {"name":"Burning Shadows","year":2017,"ppt_id":"burning-shadows"},
    "sm35":   {"name":"Shining Legends","year":2017,"ppt_id":"shining-legends"},
    "sm4":    {"name":"Crimson Invasion","year":2017,"ppt_id":"crimson-invasion"},
    "sm5":    {"name":"Ultra Prism","year":2018,"ppt_id":"ultra-prism"},
    "sm6":    {"name":"Forbidden Light","year":2018,"ppt_id":"forbidden-light"},
    "sm7":    {"name":"Celestial Storm","year":2018,"ppt_id":"celestial-storm"},
    "sm8":    {"name":"Lost Thunder","year":2018,"ppt_id":"lost-thunder"},
    "sm9":    {"name":"Team Up","year":2019,"ppt_id":"team-up"},
    "sm10":   {"name":"Unbroken Bonds","year":2019,"ppt_id":"unbroken-bonds"},
    "sm11":   {"name":"Unified Minds","year":2019,"ppt_id":"unified-minds"},
    "hif":    {"name":"Hidden Fates","year":2019,"ppt_id":"hidden-fates"},
    "sm12":   {"name":"Cosmic Eclipse","year":2019,"ppt_id":"cosmic-eclipse"},
    "swsh2":  {"name":"Rebel Clash","year":2020,"ppt_id":"rebel-clash"},
    "swsh3":  {"name":"Darkness Ablaze","year":2020,"ppt_id":"darkness-ablaze"},
    "swsh4":  {"name":"Vivid Voltage","year":2020,"ppt_id":"vivid-voltage"},
    "shf":    {"name":"Shining Fates","year":2021,"ppt_id":"shining-fates"},
    "swsh5":  {"name":"Battle Styles","year":2021,"ppt_id":"battle-styles"},
    "swsh6":  {"name":"Chilling Reign","year":2021,"ppt_id":"chilling-reign"},
    "swsh7":  {"name":"Evolving Skies","year":2021,"ppt_id":"evolving-skies"},
    "swsh8":  {"name":"Fusion Strike","year":2021,"ppt_id":"fusion-strike"},
    "cel25":  {"name":"Celebrations","year":2021,"ppt_id":"celebrations"},
    "swsh9":  {"name":"Brilliant Stars","year":2022,"ppt_id":"brilliant-stars"},
    "swsh10": {"name":"Astral Radiance","year":2022,"ppt_id":"astral-radiance"},
    "pgo":    {"name":"Pokémon GO","year":2022,"ppt_id":"pokemon-go"},
    "swsh11": {"name":"Lost Origin","year":2022,"ppt_id":"lost-origin"},
    "swsh12": {"name":"Silver Tempest","year":2022,"ppt_id":"silver-tempest"},
    "swsh125":{"name":"Crown Zenith","year":2023,"ppt_id":"crown-zenith"},
    "sv1":    {"name":"Scarlet & Violet","year":2023,"ppt_id":"scarlet-violet"},
    "sv2":    {"name":"Paldea Evolved","year":2023,"ppt_id":"paldea-evolved"},
    "sv3":    {"name":"Obsidian Flames","year":2023,"ppt_id":"obsidian-flames"},
    "sv3pt5": {"name":"Pokémon 151","year":2023,"ppt_id":"pokemon-151"},
    "sv4":    {"name":"Paradox Rift","year":2023,"ppt_id":"paradox-rift"},
    "sv4pt5": {"name":"Paldean Fates","year":2024,"ppt_id":"paldean-fates"},
    "sv5":    {"name":"Temporal Forces","year":2024,"ppt_id":"temporal-forces"},
    "sv6":    {"name":"Twilight Masquerade","year":2024,"ppt_id":"twilight-masquerade"},
    "sv6pt5": {"name":"Shrouded Fable","year":2024,"ppt_id":"shrouded-fable"},
    "sv7":    {"name":"Stellar Crown","year":2024,"ppt_id":"stellar-crown"},
    "sv8":    {"name":"Surging Sparks","year":2024,"ppt_id":"surging-sparks"},
    "sv8pt5": {"name":"Prismatic Evolutions","year":2025,"ppt_id":"prismatic-evolutions"},
    "sv9":    {"name":"Journey Together","year":2025,"ppt_id":"journey-together"},
    "sv9pt5": {"name":"Destined Rivals","year":2025,"ppt_id":"destined-rivals"},
    "sv10":   {"name":"Mega Evolution","year":2025,"ppt_id":"mega-evolution"},
    "sv10pt5":{"name":"Phantasmal Flames","year":2025,"ppt_id":"phantasmal-flames"},
    "sv11":   {"name":"Ascended Heroes","year":2026,"ppt_id":"ascended-heroes"},
    "sv11pt5":{"name":"Perfect Order","year":2026,"ppt_id":"perfect-order"},
    "sv12":   {"name":"Chaos Rising","year":2026,"ppt_id":"chaos-rising"},
}

TARGET_RARITIES = {
    "Special Illustration Rare","Illustration Rare",
    "Hyper Rare","Ultra Rare","Secret Rare",
    "Shiny Rare","Shiny Ultra Rare","Double Rare",
    "Trainer Gallery Rare Holo","Radiant Rare",
    "Gold Rare","Amazing Rare","ACE SPEC Rare",
}
RARITY_SHORT = {
    "Special Illustration Rare":"SIR","Illustration Rare":"IR",
    "Hyper Rare":"HR","Ultra Rare":"UR","Secret Rare":"Secret",
    "Shiny Rare":"Shiny","Shiny Ultra Rare":"SHV","Double Rare":"RR",
    "Trainer Gallery Rare Holo":"TG","Radiant Rare":"Radiant",
    "Gold Rare":"Gold","Amazing Rare":"AR","ACE SPEC Rare":"ACE",
}

def load_json(p, d):
    if os.path.exists(p):
        with open(p) as f: return json.load(f)
    return d

def save_json(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f: json.dump(d, f, ensure_ascii=False)

def cache_is_fresh():
    if not os.path.exists(CACHE_FILE): return False
    cached = load_json(CACHE_FILE, {})
    ts = cached.get("ts")
    if not ts: return False
    age = (datetime.now() - datetime.fromisoformat(ts)).total_seconds() / 3600
    return age < CACHE_TTL_HOURS

def get_all_set_ids(api_key):
    """Fetch all sets from PokemonPriceTracker.
    Valid params: language, search, series, sortBy, sortOrder, limit, offset
    """
    try:
        headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
        # No game filter — get all, then filter Pokemon by series/name
        r = requests.get("https://www.pokemonpricetracker.com/api/v2/sets",
                        params={"limit": 500, "sortBy": "releaseDate", "sortOrder": "desc"},
                        headers=headers, timeout=20)
        if r.status_code != 200:
            st.error(f"Sets API {r.status_code}: {r.text[:400]}")
            return []
        body = r.json()
        sets = body if isinstance(body, list) else body.get("data", body.get("sets", []))
        st.write(f"**Sets API:** {len(sets)} sets · Premier: {sets[0] if sets else 'none'}")
        return sets
    except Exception as e:
        st.error(f"Sets error: {e}")
        return []

def fetch_set_cards(set_tcg_id, set_name, set_year, api_key):
    """Fetch all cards for one set using tcgPlayerId."""
    try:
        headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
        # Correct param: tcgPlayerId for the set
        r = requests.get(
            "https://www.pokemonpricetracker.com/api/v2/cards",
            params={"set": set_tcg_id, "fetchAllInSet": "true"},
            headers=headers, timeout=25
        )
        if r.status_code == 401: return "INVALID_KEY"
        if r.status_code == 429: return "RATE_LIMIT"
        if r.status_code != 200: return []

        body = r.json()
        cards_raw = body if isinstance(body, list) else body.get("data", [])

        results = []
        for c in cards_raw:
            rarity = c.get("rarity","")
            if rarity not in TARGET_RARITIES: continue

            # Price — try all known field names
            price_usd = None
            for f in ["marketPrice","market_price","price","tcgPlayerPrice","marketValue"]:
                v = c.get(f)
                if v:
                    try:
                        fv = float(v)
                        if fv > 0.5: price_usd = fv; break
                    except: pass
            if not price_usd:
                for obj_k in ["pricing","prices","tcgplayer"]:
                    obj = c.get(obj_k, {})
                    if isinstance(obj, dict):
                        for sub in ["market","marketPrice","market_price","mid","midPrice"]:
                            v = obj.get(sub)
                            if v:
                                try:
                                    fv = float(v)
                                    if fv > 0.5: price_usd = fv; break
                                except: pass
                    if price_usd: break
            if not price_usd: continue

            price_cad = round(price_usd * USD_CAD, 2)

            # % changes
            chg1 = chg7 = chg30 = 0.0
            for pc_k in ["price_change","priceChange","change","price_changes","changes"]:
                pc = c.get(pc_k)
                if isinstance(pc, dict):
                    chg1  = float(pc.get("24h", pc.get("1d", pc.get("day",   0))) or 0)
                    chg7  = float(pc.get("7d",  pc.get("7",  pc.get("week",  0))) or 0)
                    chg30 = float(pc.get("30d", pc.get("30", pc.get("month", 0))) or 0)
                    break

            # Image
            img = ""
            for img_k in ["image","imageUrl","img","imageHiRes","large"]:
                v = c.get(img_k,"")
                if isinstance(v, str) and v.startswith("http"): img = v; break
            if not img:
                imgs = c.get("images",{})
                img = imgs.get("large") or imgs.get("small","")

            results.append({
                "id":       str(c.get("id", c.get("tcgPlayerId",""))),
                "name":     c.get("name",""),
                "set_id":   set_tcg_id,
                "set_name": set_name,
                "set_year": set_year,
                "rarity":   RARITY_SHORT.get(rarity, rarity),
                "number":   str(c.get("number", c.get("collectorNumber",""))),
                "img":      img,
                "price":    price_cad,
                "chg1":     chg1,
                "chg7":     chg7,
                "chg30":    chg30,
            })
        return results
    except: return []


def rar_pill(r):
    m = {"SIR":"p-sir","IR":"p-ir","Shiny":"p-shv","SHV":"p-shv",
         "HR":"p-rr","UR":"p-alt","Secret":"p-gold","RR":"p-alt",
         "Gold":"p-gold","TG":"p-fa","ACE":"p-ir","Radiant":"p-ir","AR":"p-alt"}
    return f'<span class="pill {m.get(r,"p-def")}">{r}</span>'

def fmt_chg(v):
    if v >  0.5: return f'<span style="color:#10b981;font-size:11px;font-weight:600">▲ +{v:.1f}%</span>'
    if v < -0.5: return f'<span style="color:#ef4444;font-size:11px;font-weight:600">▼ {v:.1f}%</span>'
    return '<span style="color:#334155;font-size:11px">—</span>'

# ── Session ──
if "all_cards"    not in st.session_state: st.session_state.all_cards    = []
if "loading_done" not in st.session_state: st.session_state.loading_done = False
if "api_key"      not in st.session_state: st.session_state.api_key      = load_json("data/api_key.json", {}).get("key","pokeprice_free_9ad6928851dc5dafc6242c5615da08b41773d0a4cbaab73c")

# ════ SIDEBAR ════
with st.sidebar:
    st.markdown("### 🃏 The Nasty Model")
    st.markdown("---")

    # API Key input
    st.markdown('<span class="sb-section">Clé API PokemonPriceTracker</span>', unsafe_allow_html=True)
    api_key_input = st.text_input("", value=st.session_state.api_key if st.session_state.api_key else "pokeprice_free_9ad6928851dc5dafc6242c5615da08b41773d0a4cbaab73c",
        placeholder="pokeprice_free_...", type="password",
        label_visibility="collapsed")
    if api_key_input != st.session_state.api_key:
        st.session_state.api_key = api_key_input
        save_json("data/api_key.json", {"key": api_key_input})
        st.session_state.all_cards    = []
        st.session_state.loading_done = False
        if os.path.exists(CACHE_FILE): os.remove(CACHE_FILE)

    st.markdown("---")
    show_day = st.toggle("⚡ Mode Show Day", value=False)

    st.markdown('<span class="sb-section">Période</span>', unsafe_allow_html=True)
    period_map     = {"24 heures":"chg1","7 jours":"chg7","30 jours":"chg30"}
    period_lbl_map = {"24 heures":"24h","7 jours":"7j","30 jours":"30j"}
    period_sel = st.selectbox("", list(period_map.keys()), index=1, label_visibility="collapsed")
    chg_key    = period_map[period_sel]
    period_lbl = period_lbl_map[period_sel]

    st.markdown('<span class="sb-section">Set</span>', unsafe_allow_html=True)
    set_opts   = ["Tous les sets"] + [f"{v['name']} ({k})" for k,v in SETS.items()]
    set_filter = st.selectbox("", set_opts, label_visibility="collapsed")

    st.markdown('<span class="sb-section">Prix C$</span>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca: prix_min = st.number_input("Min", min_value=0, value=0,    step=5)
    with cb: prix_max = st.number_input("Max", min_value=0, value=5000, step=25)

    st.markdown('<span class="sb-section">Recherche</span>', unsafe_allow_html=True)
    search = st.text_input("", placeholder="Nom de la carte...", label_visibility="collapsed")

    st.markdown("---")
    n = len(st.session_state.all_cards)
    st.markdown(f'<div style="font-size:11px;color:#2d3748;text-align:center;margin-bottom:8px">{n} cartes · {len(SETS)} sets</div>', unsafe_allow_html=True)
    if st.button("🔄  Forcer rechargement", type="primary"):
        st.session_state.all_cards    = []
        st.session_state.loading_done = False
        if os.path.exists(CACHE_FILE): os.remove(CACHE_FILE)
        st.rerun()

# ════ HEADER ════
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;padding:1rem 0 1.25rem;border-bottom:1px solid #1a1f35;margin-bottom:1.25rem">
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:40px;height:40px;background:linear-gradient(135deg,#06b6d4,#0891b2);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px">🃏</div>
    <div>
      <div style="font-size:20px;font-weight:800;color:#f1f5f9;letter-spacing:-.03em">The Nasty Model</div>
      <div style="font-size:11px;color:#2d3748">TCGPlayer · prix réels · C$ · {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
    </div>
  </div>
  <div style="display:flex;gap:8px">
    <div style="background:#0d1520;border:1px solid #0891b2;color:#06b6d4;font-size:11px;padding:4px 10px;border-radius:20px;font-weight:600">🇨🇦 CAD</div>
    <div style="background:#0d1520;border:1px solid #1a1f35;color:#334155;font-size:11px;padding:4px 10px;border-radius:20px">{n} cartes</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ════ NO API KEY ════
if not st.session_state.api_key:
    st.markdown("""
    <div class="api-key-box">
      <div style="font-size:32px;margin-bottom:12px">🔑</div>
      <div style="font-size:16px;font-weight:700;color:#f1f5f9;margin-bottom:8px">Clé API requise</div>
      <div style="font-size:13px;color:#64748b;margin-bottom:16px">
        Pour avoir les vrais prix TCGPlayer avec les % de changement 24h/7j/30j,<br>
        tu as besoin d'une clé API gratuite de PokemonPriceTracker.
      </div>
      <div style="font-size:12px;color:#4a5568;background:#080910;border-radius:8px;padding:12px;text-align:left;margin-bottom:12px">
        1. Va sur <strong style="color:#06b6d4">pokemonpricetracker.com</strong><br>
        2. Clique <strong>Sign Up</strong> — gratuit, 100 requêtes/jour<br>
        3. Copie ta clé API<br>
        4. Colle-la dans la sidebar à gauche
      </div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

# ════ LOAD DATA ════
if not st.session_state.loading_done:
    if cache_is_fresh():
        cached = load_json(CACHE_FILE, {})
        cards_cached = cached.get("cards", [])
        if cards_cached:  # only use cache if it actually has cards
            st.session_state.all_cards    = cards_cached
            st.session_state.loading_done = True

if not st.session_state.loading_done:
    prog = st.progress(0, text="Récupération des sets depuis PokemonPriceTracker...")
    all_cards = []

    # Step 1: get all sets from the API (uses their own set IDs)
    api_sets = get_all_set_ids(st.session_state.api_key)
    if not api_sets:
        st.error("❌ Impossible de récupérer les sets. Vérifie ta clé API.")
        st.stop()

    # Filter: only Pokemon sets
    poke_sets = [s for s in api_sets if "pokemon" in s.get("name","").lower() 
                 or s.get("game","").lower() in ["pokemon","pokémon"]
                 or "pok" in str(s.get("tcgPlayerId","")).lower()
                 or True]  # take all for now

    total = len(poke_sets)
    prog.progress(5, text=f"{total} sets trouvés — chargement des cartes...")

    stop_flag = False
    # Show first set structure for debugging
    if poke_sets:
        first = poke_sets[0]
        st.write(f"**Premier set:** {first}")

    for i, s in enumerate(poke_sets):
        if stop_flag: break
        set_tcg_id = s.get("tcgPlayerId") or s.get("id","")
        set_name   = s.get("name","")
        set_year   = 0
        try:
            import re
            yr = re.search(r"20\d\d", str(s.get("releaseDate","") or s.get("year","") or ""))
            if yr: set_year = int(yr.group())
        except: pass

        result = fetch_set_cards(set_tcg_id, set_name, set_year, st.session_state.api_key)
        if result == "INVALID_KEY":
            st.error("❌ Clé API invalide.")
            st.stop()
        if result == "RATE_LIMIT":
            st.warning(f"⚠️ Limite 100 req/jour atteinte après {i} sets. Les cartes chargées sont sauvegardées.")
            stop_flag = True
        elif isinstance(result, list):
            all_cards.extend(result)

        pct = min(99, int(5 + (i+1)/total*94))
        prog.progress(pct, text=f"{set_name} ({i+1}/{total}) — {len(all_cards)} cartes")

    prog.progress(100, text=f"✓ {len(all_cards)} cartes chargées")
    prog.empty()
    st.session_state.all_cards    = all_cards
    st.session_state.loading_done = True
    save_json(CACHE_FILE, {"cards": all_cards, "ts": datetime.now().isoformat()})
    st.rerun()

# ════ DISPLAY ════
df = pd.DataFrame(st.session_state.all_cards) if st.session_state.all_cards else pd.DataFrame()

if df.empty:
    st.info("Aucune carte chargée. Clique **Forcer rechargement** dans la sidebar.")
    st.stop()

if show_day:        df = df[df[chg_key] >= 10]
if prix_min > 0:    df = df[df["price"] >= prix_min]
if prix_max < 5000: df = df[df["price"] <= prix_max]
if search:          df = df[df["name"].str.lower().str.contains(search.lower(), na=False)]
if set_filter != "Tous les sets":
    sf = set_filter.split("(")[-1].rstrip(")")
    sf_name = SETS.get(sf, {}).get("ppt_id", "")
    df = df[df["set_id"] == sf_name]

df = df.sort_values(chg_key, ascending=False).reset_index(drop=True)

if show_day:
    avg = df[chg_key].mean() if len(df) else 0
    st.markdown(f"""
    <div class="show-banner">
      <span style="font-size:26px">⚡</span>
      <div style="flex:1">
        <div style="font-size:14px;font-weight:700;color:#06b6d4">MODE SHOW DAY — {period_sel}</div>
        <div style="font-size:12px;color:#0e7490;margin-top:2px">Cartes ≥ 10% · vendeurs pas encore repriced</div>
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
  <span style="font-size:12px;color:#2d3748">{len(df)} cartes</span>
</div>
""", unsafe_allow_html=True)

if len(df) == 0:
    st.markdown('<div style="text-align:center;padding:4rem;color:#2d3748">Aucune carte.</div>', unsafe_allow_html=True)
else:
    items = ""
    for _, row in df.iterrows():
        chg = row[chg_key]
        up  = chg > 0.5; dn = chg < -0.5
        clr = "#10b981" if up else ("#ef4444" if dn else "#64748b")
        arrow = "▲" if up else ("▼" if dn else "")
        pct_str = f"{arrow} +{chg:.1f}%" if up else (f"{arrow} {chg:.1f}%" if dn else "—")
        img_html = f'<img src="{row["img"]}" class="card-thumb" onerror="this.style.display=\'none\';this.nextSibling.style.display=\'flex\'" /><div class="card-thumb-ph" style="display:none">🃏</div>' if row.get("img") else '<div class="card-thumb-ph">🃏</div>'
        bp = '<span class="badge-pump">🔥 24h</span>'  if row["chg1"] > 5  else ""
        bs = '<span class="badge-show">⚡ SHOW</span>' if row["chg7"] >= 10 else ""
        items += f"""
<div class="card-item">
  {img_html}
  <div class="card-info">
    <div class="card-name">{row['name']}{bp}{bs}</div>
    <div class="card-set-line">{row['set_name']}</div>
    <div class="card-meta">{rar_pill(row['rarity'])} · #{row['number']} · {row['set_year']}</div>
    <div style="margin-top:7px;display:flex;gap:16px">
      <span style="font-size:11px;color:#4a5568">24h: {fmt_chg(row['chg1'])}</span>
      <span style="font-size:11px;color:#4a5568">7j: {fmt_chg(row['chg7'])}</span>
      <span style="font-size:11px;color:#4a5568">30j: {fmt_chg(row['chg30'])}</span>
    </div>
  </div>
  <div class="card-price-block">
    <div class="price-main">CA${row['price']:.2f}</div>
    <div class="price-change" style="color:{clr}">{pct_str}</div>
    <div class="price-source">TCGPlayer · USD→CAD</div>
  </div>
</div>"""
    st.markdown(items, unsafe_allow_html=True)

st.markdown("<hr style='margin:1.5rem 0'>", unsafe_allow_html=True)
with st.expander("📋  Export CSV"):
    ex = df[df[chg_key] >= 10].copy() if not show_day else df.copy()
    if len(ex) > 0:
        out = ex[["name","set_name","rarity","price","chg1","chg7","chg30"]].copy()
        out.columns = ["Carte","Set","Rareté","Prix CA$","24h %","7j %","30j %"]
        out["Offre -15%"] = (out["Prix CA$"]*0.85).round(2)
        out["Offre -25%"] = (out["Prix CA$"]*0.75).round(2)
        st.dataframe(out, use_container_width=True, hide_index=True)
        st.download_button("⬇️ CSV", data=out.to_csv(index=False),
            file_name=f"show_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", type="primary")

with st.expander("⚙️  Paramètres"):
    if st.button("🗑️  Vider cache"):
        st.session_state.all_cards=[]; st.session_state.loading_done=False
        if os.path.exists(CACHE_FILE): os.remove(CACHE_FILE)
        st.rerun()
