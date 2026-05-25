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
.card-price-block{text-align:right;flex-shrink:0;min-width:180px}
.price-main{font-size:22px;font-weight:800;color:#f1f5f9;display:flex;align-items:center;justify-content:flex-end;gap:6px}
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
</style>
""", unsafe_allow_html=True)

EUR_CAD = 1.55   # EUR → CAD
USD_CAD = 1.364  # USD → CAD
CACHE_FILE = "data/cards_cache.json"
CACHE_TTL_HOURS = 12  # Refresh prices every 12 hours

# TCGdex set IDs — maps our set codes to TCGdex IDs
SETS = {
    "xy1":    {"name":"XY Base","year":2014},
    "xy2":    {"name":"Flashfire","year":2014},
    "xy6":    {"name":"Roaring Skies","year":2015},
    "xy7":    {"name":"Ancient Origins","year":2015},
    "xy8":    {"name":"BREAKthrough","year":2015},
    "xy9":    {"name":"BREAKpoint","year":2016},
    "xy10":   {"name":"Fates Collide","year":2016},
    "xy11":   {"name":"Steam Siege","year":2016},
    "xy12":   {"name":"Evolutions","year":2016},
    "sm1":    {"name":"Sun & Moon","year":2017},
    "sm2":    {"name":"Guardians Rising","year":2017},
    "sm3":    {"name":"Burning Shadows","year":2017},
    "sm35":   {"name":"Shining Legends","year":2017},
    "sm4":    {"name":"Crimson Invasion","year":2017},
    "sm5":    {"name":"Ultra Prism","year":2018},
    "sm6":    {"name":"Forbidden Light","year":2018},
    "sm7":    {"name":"Celestial Storm","year":2018},
    "sm8":    {"name":"Lost Thunder","year":2018},
    "sm9":    {"name":"Team Up","year":2019},
    "sm10":   {"name":"Unbroken Bonds","year":2019},
    "sm11":   {"name":"Unified Minds","year":2019},
    "hif":    {"name":"Hidden Fates","year":2019},
    "sm12":   {"name":"Cosmic Eclipse","year":2019},
    "swsh2":  {"name":"Rebel Clash","year":2020},
    "swsh3":  {"name":"Darkness Ablaze","year":2020},
    "swsh4":  {"name":"Vivid Voltage","year":2020},
    "shf":    {"name":"Shining Fates","year":2021},
    "swsh5":  {"name":"Battle Styles","year":2021},
    "swsh6":  {"name":"Chilling Reign","year":2021},
    "swsh7":  {"name":"Evolving Skies","year":2021},
    "swsh8":  {"name":"Fusion Strike","year":2021},
    "cel25":  {"name":"Celebrations","year":2021},
    "swsh9":  {"name":"Brilliant Stars","year":2022},
    "swsh10": {"name":"Astral Radiance","year":2022},
    "pgo":    {"name":"Pokémon GO","year":2022},
    "swsh11": {"name":"Lost Origin","year":2022},
    "swsh12": {"name":"Silver Tempest","year":2022},
    "swsh125":{"name":"Crown Zenith","year":2023},
    "sv1":    {"name":"Scarlet & Violet","year":2023},
    "sv2":    {"name":"Paldea Evolved","year":2023},
    "sv3":    {"name":"Obsidian Flames","year":2023},
    "sv3pt5": {"name":"Pokémon 151","year":2023},
    "sv4":    {"name":"Paradox Rift","year":2023},
    "sv4pt5": {"name":"Paldean Fates","year":2024},
    "sv5":    {"name":"Temporal Forces","year":2024},
    "sv6":    {"name":"Twilight Masquerade","year":2024},
    "sv6pt5": {"name":"Shrouded Fable","year":2024},
    "sv7":    {"name":"Stellar Crown","year":2024},
    "sv8":    {"name":"Surging Sparks","year":2024},
    "sv8pt5": {"name":"Prismatic Evolutions","year":2025},
    "sv9":    {"name":"Journey Together","year":2025},
    "sv9pt5": {"name":"Destined Rivals","year":2025},
    "sv10":   {"name":"Mega Evolution","year":2025},
    "sv10pt5":{"name":"Phantasmal Flames","year":2025},
    "sv11":   {"name":"Ascended Heroes","year":2026},
    "sv11pt5":{"name":"Perfect Order","year":2026},
    "sv12":   {"name":"Chaos Rising","year":2026},
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
    """Check if cache is less than CACHE_TTL_HOURS old"""
    if not os.path.exists(CACHE_FILE): return False
    cached = load_json(CACHE_FILE, {})
    ts = cached.get("ts")
    if not ts: return False
    age = (datetime.now() - datetime.fromisoformat(ts)).total_seconds() / 3600
    return age < CACHE_TTL_HOURS

def fetch_set_tcgdex(set_id):
    """
    Fetch a full set from TCGdex in TWO calls:
    1. GET /sets/{id} → list of card IDs
    2. GET /cards in bulk (parallel mini-batches)
    
    TCGdex includes avg1/avg7/avg30 from Cardmarket AND TCGPlayer prices.
    This gives us real price history without extra API calls.
    """
    set_info = SETS.get(set_id, {})
    results  = []
    headers  = {"User-Agent": "NastyModel/2.0", "Accept": "application/json"}

    try:
        # Step 1: get card list for this set
        r = requests.get(f"https://api.tcgdex.net/v2/en/sets/{set_id}",
                         timeout=15, headers=headers)
        if r.status_code != 200: return []
        card_briefs = r.json().get("cards", [])

        # Step 2: fetch cards in parallel mini-batches of 10
        def fetch_card(brief):
            cid = brief.get("id","")
            if not cid: return None
            try:
                cr = requests.get(f"https://api.tcgdex.net/v2/en/cards/{cid}",
                                  timeout=10, headers=headers)
                if cr.status_code == 200: return cr.json()
            except: pass
            return None

        with ThreadPoolExecutor(max_workers=10) as ex:
            futures = [ex.submit(fetch_card, b) for b in card_briefs]
            cards   = [f.result() for f in as_completed(futures) if f.result()]

        for c in cards:
            rarity = c.get("rarity","")
            if rarity not in TARGET_RARITIES: continue

            pricing = c.get("pricing", {})
            tcgp    = pricing.get("tcgplayer", {})
            cm      = pricing.get("cardmarket", {})

            # --- ONE source for price AND history to avoid currency mixing ---
            # Cardmarket: has avg1/avg7/avg30 history in EUR -> consistent comparisons
            # TCGPlayer: no history in TCGdex -> use as fallback, no % change

            price_cad = None
            chg1 = chg7 = chg30 = 0.0

            def cm_val(key):
                for k in [key, key + "-holo"]:
                    v = cm.get(k)
                    if v:
                        try:
                            fv = float(v)
                            if fv > 0.5: return fv
                        except: pass
                return None

            cm_now = cm_val("trend") or cm_val("avg")

            if cm_now:
                # Use Cardmarket for everything — same EUR base, consistent history
                price_cad = round(cm_now * EUR_CAD, 2)
                p1  = cm_val("avg1")
                p7  = cm_val("avg7")
                p30 = cm_val("avg30")

                def pct(past_eur):
                    if past_eur and cm_now and past_eur > 0:
                        return round((cm_now - past_eur) / past_eur * 100, 2)
                    return 0.0

                chg1  = pct(p1)
                chg7  = pct(p7)
                chg30 = pct(p30)
            else:
                # TCGPlayer USD fallback — no history available
                for variant in ["holofoil","1stEditionHolofoil","reverseHolofoil","normal","unlimitedHolofoil"]:
                    v = tcgp.get(variant, {})
                    m = v.get("marketPrice") or v.get("midPrice")
                    if m:
                        try:
                            fv = float(m)
                            if fv > 0.5:
                                price_cad = round(fv * USD_CAD, 2)
                                break
                        except: pass

            if not price_cad or price_cad < 1.0: continue

            # Image
            img = c.get("image","")
            if img: img = img + "/high.png"

            results.append({
                "id":       c.get("id",""),
                "name":     c.get("name",""),
                "set_id":   set_id,
                "set_name": set_info.get("name", set_id),
                "set_year": set_info.get("year", 0),
                "rarity":   RARITY_SHORT.get(rarity, rarity),
                "number":   c.get("localId",""),
                "img":      img,
                "price":    price_cad,
                "p1":       p1  or price_cad,
                "p7":       p7  or price_cad,
                "p30":      p30 or price_cad,
                "chg1":     chg1,
                "chg7":     chg7,
                "chg30":    chg30,
            })
    except Exception as e:
        pass
    return results

def load_all_sets(set_ids):
    """Load all sets in parallel. No st.* calls inside threads."""
    all_cards = []
    with ThreadPoolExecutor(max_workers=6) as ex:
        futures = {ex.submit(fetch_set_tcgdex, sid): sid for sid in set_ids}
        for f in as_completed(futures):
            all_cards.extend(f.result() or [])
    return all_cards

def rar_pill(r):
    m = {"SIR":"p-sir","IR":"p-ir","Shiny":"p-shv","SHV":"p-shv",
         "HR":"p-rr","UR":"p-alt","Secret":"p-gold","RR":"p-alt",
         "Gold":"p-gold","TG":"p-fa","ACE":"p-ir","Radiant":"p-ir","AR":"p-alt"}
    return f'<span class="pill {m.get(r,"p-def")}">{r}</span>'

def fmt_chg(v):
    if v >  0.5: return f'<span style="color:#10b981;font-size:11px;font-weight:600">▲ +{v:.1f}%</span>'
    if v < -0.5: return f'<span style="color:#ef4444;font-size:11px;font-weight:600">▼ {v:.1f}%</span>'
    return '<span style="color:#334155;font-size:11px">—</span>'

# ── Session state ──
if "all_cards"    not in st.session_state: st.session_state.all_cards    = []
if "loading_done" not in st.session_state: st.session_state.loading_done = False

# ════ SIDEBAR ════
with st.sidebar:
    st.markdown("### 🃏 The Nasty Model")
    st.markdown("---")

    show_day = st.toggle("⚡ Mode Show Day", value=False,
        help="Gain ≥ 10% sur la période choisie")

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
    st.markdown(f'<div style="font-size:11px;color:#2d3748;text-align:center;margin-bottom:8px">{n} cartes · {len(SETS)} sets · cache {CACHE_TTL_HOURS}h</div>', unsafe_allow_html=True)
    if st.button("🔄  Forcer rechargement", type="primary"):
        st.session_state.all_cards    = []
        st.session_state.loading_done = False
        if os.path.exists(CACHE_FILE): os.remove(CACHE_FILE)
        st.rerun()

# ════ LOAD DATA ════

# Try fresh cache first
if not st.session_state.loading_done:
    if cache_is_fresh():
        cached = load_json(CACHE_FILE, {})
        cards  = cached.get("cards", [])
        if cards:
            st.session_state.all_cards    = cards
            st.session_state.loading_done = True

# If no fresh cache → load everything
if not st.session_state.loading_done:
    st.markdown("""
    <div style="background:#0d0f1c;border:1px solid #1a1f35;border-radius:14px;padding:20px 24px;margin-bottom:1rem">
      <div style="font-size:15px;font-weight:700;color:#f1f5f9;margin-bottom:4px">⏳ Chargement en cours...</div>
      <div style="font-size:12px;color:#4a5568;margin-bottom:12px">Tous les sets chargés en parallèle avec prix réels (TCGPlayer + Cardmarket).<br>~1–2 minutes la première fois, puis instantané pendant 12h.</div>
    </div>
    """, unsafe_allow_html=True)

    prog = st.progress(0, text="Connexion aux APIs...")
    cards = load_all_sets(list(SETS.keys()))
    prog.progress(100, text=f"✓ {len(cards)} cartes chargées")

    st.session_state.all_cards    = cards
    st.session_state.loading_done = True
    save_json(CACHE_FILE, {"cards": cards, "ts": datetime.now().isoformat()})
    st.rerun()

# ════ MAIN ════
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;padding:1rem 0 1.25rem;border-bottom:1px solid #1a1f35;margin-bottom:1.25rem">
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:40px;height:40px;background:linear-gradient(135deg,#06b6d4,#0891b2);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px">🃏</div>
    <div>
      <div style="font-size:20px;font-weight:800;color:#f1f5f9;letter-spacing:-.03em">The Nasty Model</div>
      <div style="font-size:11px;color:#2d3748">TCGPlayer · Cardmarket · C$ · {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
    </div>
  </div>
  <div style="display:flex;gap:8px">
    <div style="background:#0d1520;border:1px solid #0891b2;color:#06b6d4;font-size:11px;padding:4px 10px;border-radius:20px;font-weight:600">🇨🇦 CAD</div>
    <div style="background:#0d1520;border:1px solid #1a1f35;color:#334155;font-size:11px;padding:4px 10px;border-radius:20px">{len(st.session_state.all_cards)} cartes</div>
  </div>
</div>
""", unsafe_allow_html=True)

df = pd.DataFrame(st.session_state.all_cards) if st.session_state.all_cards else pd.DataFrame()

if not df.empty:
    if show_day:        df = df[df[chg_key] >= 10]
    if prix_min > 0:    df = df[df["price"] >= prix_min]
    if prix_max < 5000: df = df[df["price"] <= prix_max]
    if search:          df = df[df["name"].str.lower().str.contains(search.lower(), na=False)]
    if set_filter != "Tous les sets":
        sid = set_filter.split("(")[-1].rstrip(")")
        df  = df[df["set_id"] == sid]

    df = df.sort_values(chg_key, ascending=False).reset_index(drop=True)

    if show_day:
        avg = df[chg_key].mean() if len(df) else 0
        st.markdown(f"""
        <div class="show-banner">
          <span style="font-size:26px">⚡</span>
          <div style="flex:1">
            <div style="font-size:14px;font-weight:700;color:#06b6d4">MODE SHOW DAY — {period_sel}</div>
            <div style="font-size:12px;color:#0e7490;margin-top:2px">Cartes ≥ 10% · les vendeurs n'ont pas encore repriced</div>
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
        st.markdown('<div style="text-align:center;padding:4rem;color:#2d3748">Aucune carte ne correspond aux filtres.</div>', unsafe_allow_html=True)
    else:
        items = ""
        for _, row in df.iterrows():
            chg = row[chg_key]
            up  = chg > 0.5
            dn  = chg < -0.5
            arrow = "▲" if up else ("▼" if dn else "")
            clr   = "#10b981" if up else ("#ef4444" if dn else "#64748b")
            pct_str = f'{arrow} +{chg:.1f}%' if up else (f'{arrow} {chg:.1f}%' if dn else "—")
            price_str = f"CA${row['price']:.2f}"
            img_html = f'<img src="{row["img"]}" class="card-thumb" onerror="this.style.display=\'none\';this.nextSibling.style.display=\'flex\'" /><div class="card-thumb-ph" style="display:none">🃏</div>' if row.get("img") else '<div class="card-thumb-ph">🃏</div>'
            bp = '<span class="badge-pump">🔥 24h</span>'  if row["chg1"] > 5  else ""
            bs = '<span class="badge-show">⚡ SHOW</span>' if row["chg7"] >= 10 else ""

            items += f"""
<div class="card-item">
  {img_html}
  <div class="card-info">
    <div class="card-name">{row['name']}{bp}{bs}</div>
    <div class="card-set-line">{row['set_name']}</div>
    <div class="card-meta">{rar_pill(row['rarity'])} · #{row['number']} · {row['set_id'].upper()} · {row['set_year']}</div>
    <div style="margin-top:7px;display:flex;gap:16px">
      <span style="font-size:11px;color:#4a5568">24h: {fmt_chg(row['chg1'])}</span>
      <span style="font-size:11px;color:#4a5568">7j: {fmt_chg(row['chg7'])}</span>
      <span style="font-size:11px;color:#4a5568">30j: {fmt_chg(row['chg30'])}</span>
    </div>
  </div>
  <div class="card-price-block">
    <div class="price-main">{price_str}</div>
    <div class="price-change" style="color:{clr}">{pct_str}</div>
    <div class="price-source">TCGPlayer + Cardmarket · C$</div>
  </div>
</div>"""
        st.markdown(items, unsafe_allow_html=True)

    st.markdown("<hr style='margin:1.5rem 0'>", unsafe_allow_html=True)
    with st.expander("📋  Liste d'achat — export CSV"):
        ex = df[df[chg_key] >= 10].copy() if not show_day else df.copy()
        if len(ex) > 0:
            out = ex[["name","set_name","rarity","price","chg1","chg7","chg30"]].copy()
            out.columns = ["Carte","Set","Rareté","Prix CA$","24h %","7j %","30j %"]
            out["Offre -15%"] = (out["Prix CA$"]*0.85).round(2)
            out["Offre -25%"] = (out["Prix CA$"]*0.75).round(2)
            st.dataframe(out, use_container_width=True, hide_index=True)
            st.download_button("⬇️ Télécharger CSV", data=out.to_csv(index=False),
                file_name=f"show_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", type="primary")
        else:
            st.info("Active le Mode Show Day pour générer ta liste.")

    with st.expander("⚙️  Paramètres"):
        if st.button("🗑️  Vider cache & recharger tout"):
            st.session_state.all_cards    = []
            st.session_state.loading_done = False
            if os.path.exists(CACHE_FILE): os.remove(CACHE_FILE)
            st.rerun()
