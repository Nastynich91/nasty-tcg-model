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
</style>
""", unsafe_allow_html=True)

USD_CAD   = 1.364
CACHE_FILE = "data/cards_cache.json"
CACHE_TTL  = 12
API_KEY    = "tcg_live_2b62c19d32e9a3e7314ab4c7b44c617828a130ec"
BASE_URL   = "https://api.tcgapi.dev/v1"

# Correct header format from docs: X-API-Key
def hdrs():
    return {"X-API-Key": API_KEY, "Accept": "application/json"}

# Pokemon set IDs on tcgapi.dev (from their numeric IDs)
# We use /search to find cards directly — more reliable than /sets
POKEMON_SETS = [
    # Recent high-value sets
    ("Prismatic Evolutions", 2025, "sv8pt5"),
    ("Surging Sparks", 2024, "sv8"),
    ("Stellar Crown", 2024, "sv7"),
    ("Twilight Masquerade", 2024, "sv6"),
    ("Shrouded Fable", 2024, "sv6pt5"),
    ("Temporal Forces", 2024, "sv5"),
    ("Paldean Fates", 2024, "sv4pt5"),
    ("Paradox Rift", 2023, "sv4"),
    ("Pokemon 151", 2023, "sv3pt5"),
    ("Obsidian Flames", 2023, "sv3"),
    ("Paldea Evolved", 2023, "sv2"),
    ("Scarlet & Violet", 2023, "sv1"),
    ("Crown Zenith", 2023, "swsh125"),
    ("Silver Tempest", 2022, "swsh12"),
    ("Lost Origin", 2022, "swsh11"),
    ("Pokemon GO", 2022, "pgo"),
    ("Astral Radiance", 2022, "swsh10"),
    ("Brilliant Stars", 2022, "swsh9"),
    ("Celebrations", 2021, "cel25"),
    ("Fusion Strike", 2021, "swsh8"),
    ("Evolving Skies", 2021, "swsh7"),
    ("Chilling Reign", 2021, "swsh6"),
    ("Battle Styles", 2021, "swsh5"),
    ("Shining Fates", 2021, "shf"),
    ("Vivid Voltage", 2020, "swsh4"),
    ("Darkness Ablaze", 2020, "swsh3"),
    ("Rebel Clash", 2020, "swsh2"),
    ("Cosmic Eclipse", 2019, "sm12"),
    ("Hidden Fates", 2019, "hif"),
    ("Unified Minds", 2019, "sm11"),
    ("Unbroken Bonds", 2019, "sm10"),
    ("Team Up", 2019, "sm9"),
    ("Lost Thunder", 2018, "sm8"),
    ("Celestial Storm", 2018, "sm7"),
    ("Forbidden Light", 2018, "sm6"),
    ("Ultra Prism", 2018, "sm5"),
    ("Burning Shadows", 2017, "sm3"),
    ("Guardians Rising", 2017, "sm2"),
    ("Shining Legends", 2017, "sm35"),
    ("Evolutions", 2016, "xy12"),
    ("Steam Siege", 2016, "xy11"),
    ("Fates Collide", 2016, "xy10"),
    ("Roaring Skies", 2015, "xy6"),
    ("Ancient Origins", 2015, "xy7"),
    # 2026 sets
    ("Destined Rivals", 2025, "sv9pt5"),
    ("Journey Together", 2025, "sv9"),
    ("Ascended Heroes", 2026, "sv11"),
    ("Perfect Order", 2026, "sv11pt5"),
    ("Chaos Rising", 2026, "sv12"),
]

TARGET_RARITIES = {
    "Special Illustration Rare", "Illustration Rare",
    "Hyper Rare", "Ultra Rare", "Secret Rare",
    "Shiny Rare", "Shiny Ultra Rare", "Double Rare",
    "Trainer Gallery Rare Holo", "Radiant Rare",
    "Gold Rare", "Amazing Rare", "ACE SPEC Rare",
    "Rainbow Rare", "Full Art",
}
RARITY_SHORT = {
    "Special Illustration Rare":"SIR","Illustration Rare":"IR",
    "Hyper Rare":"HR","Ultra Rare":"UR","Secret Rare":"Secret",
    "Shiny Rare":"Shiny","Shiny Ultra Rare":"SHV","Double Rare":"RR",
    "Trainer Gallery Rare Holo":"TG","Radiant Rare":"Radiant",
    "Gold Rare":"Gold","Amazing Rare":"AR","ACE SPEC Rare":"ACE",
    "Rainbow Rare":"RR","Full Art":"FA",
}

def load_json(p,d):
    if os.path.exists(p):
        with open(p) as f: return json.load(f)
    return d

def save_json(p,d):
    os.makedirs(os.path.dirname(p),exist_ok=True)
    with open(p,"w") as f: json.dump(d,f,ensure_ascii=False)

def cache_fresh():
    if not os.path.exists(CACHE_FILE): return False
    c=load_json(CACHE_FILE,{})
    ts=c.get("ts")
    if not ts: return False
    return (datetime.now()-datetime.fromisoformat(ts)).total_seconds()/3600 < CACHE_TTL

@st.cache_data(ttl=43200, show_spinner=False)
def fetch_set_prices(set_code, set_name, set_year):
    """
    Use tcgapi.dev /search with set filter.
    Paginate through all cards, filter by rarity and price.
    """
    results = []
    try:
        offset = 0
        limit  = 100
        while True:
            r = requests.get(f"{BASE_URL}/search",
                            params={
                                "game":   "pokemon",
                                "set":    set_name,
                                "limit":  limit,
                                "offset": offset,
                            },
                            headers=hdrs(), timeout=20)
            if r.status_code != 200: break
            body  = r.json()
            cards = body.get("results", body.get("data", body if isinstance(body,list) else []))
            if not cards: break

            for c in cards:
                # Only individual cards (not sealed products)
                if any(w in c.get("name","").lower() for w in
                       ["booster","elite trainer","etb","case","tin","collection box","bundle","pack"]): continue

                rarity    = c.get("rarity","")
                price_usd = None

                for f in ["market_price","marketPrice","price","foil_market_price","normal_market_price"]:
                    v = c.get(f)
                    if v:
                        try:
                            fv = float(str(v).replace("$","").replace(",",""))
                            if fv > 0: price_usd = fv; break
                        except: pass

                if not price_usd or price_usd < 3: continue
                price_cad = round(price_usd * USD_CAD, 2)

                # Price changes
                def safe_float(v):
                    try: return float(v or 0)
                    except: return 0.0

                chg1  = safe_float(c.get("price_change_24h") or c.get("change_24h") or c.get("change_1d"))
                chg7  = safe_float(c.get("price_change_7d")  or c.get("change_7d")  or c.get("change_7"))
                chg30 = safe_float(c.get("price_change_30d") or c.get("change_30d") or c.get("change_30"))

                img = c.get("image","") or c.get("image_url","") or c.get("img","")
                if not img:
                    imgs = c.get("images",{})
                    img  = imgs.get("large","") or imgs.get("small","") if isinstance(imgs,dict) else ""

                results.append({
                    "id":       str(c.get("id","")),
                    "name":     c.get("name",""),
                    "set_id":   set_code,
                    "set_name": set_name,
                    "set_year": set_year,
                    "rarity":   RARITY_SHORT.get(rarity, rarity[:8]) if rarity else "—",
                    "number":   str(c.get("number", c.get("collector_number", c.get("card_number","")))),
                    "img":      img,
                    "price":    price_cad,
                    "chg1":     chg1,
                    "chg7":     chg7,
                    "chg30":    chg30,
                })

            # Check if more pages
            total = body.get("total", body.get("count", len(cards)))
            offset += limit
            if offset >= total or len(cards) < limit: break
            if offset > 500: break  # safety cap

    except Exception as e:
        pass
    return results

def _parse_prices(prices, set_name, set_year, set_code):
    """Parse /sets/{id}/prices response"""
    results = []
    for p in prices:
        rarity = p.get("rarity","")
        price_usd = p.get("market_price") or p.get("foil_market_price") or p.get("price")
        if not price_usd: continue
        try: price_usd = float(price_usd)
        except: continue
        if price_usd < 3: continue

        price_cad = round(price_usd * USD_CAD, 2)
        chg1  = float(p.get("change_24h", p.get("price_change_24h", 0)) or 0)
        chg7  = float(p.get("change_7d",  p.get("price_change_7d",  0)) or 0)
        chg30 = float(p.get("change_30d", p.get("price_change_30d", 0)) or 0)

        img = p.get("image","") or p.get("image_url","")

        results.append({
            "id":       str(p.get("card_id", p.get("id",""))),
            "name":     p.get("card_name", p.get("name","")),
            "set_id":   set_code,
            "set_name": set_name,
            "set_year": set_year,
            "rarity":   RARITY_SHORT.get(rarity, rarity) if rarity else "—",
            "number":   str(p.get("number", p.get("collector_number",""))),
            "img":      img,
            "price":    price_cad,
            "chg1":     chg1,
            "chg7":     chg7,
            "chg30":    chg30,
        })
    return results

def _parse_search_results(cards, set_name, set_year, set_code):
    """Parse /search response"""
    results = []
    for c in cards:
        # Only cards from this set
        if c.get("set_name","").lower() not in [set_name.lower(), set_code.lower()]:
            continue
        rarity = c.get("rarity","")
        price_usd = c.get("market_price") or c.get("price")
        if not price_usd: continue
        try: price_usd = float(price_usd)
        except: continue
        if price_usd < 3: continue

        price_cad = round(price_usd * USD_CAD, 2)
        chg7  = float(c.get("change_7d",  c.get("price_change_7d",  0)) or 0)
        chg30 = float(c.get("change_30d", c.get("price_change_30d", 0)) or 0)

        img = c.get("image","") or c.get("image_url","")
        imgs = c.get("images",{})
        if not img and imgs: img = imgs.get("large","") or imgs.get("small","")

        results.append({
            "id":       str(c.get("id","")),
            "name":     c.get("name",""),
            "set_id":   set_code,
            "set_name": set_name,
            "set_year": set_year,
            "rarity":   RARITY_SHORT.get(rarity, rarity) if rarity else "—",
            "number":   str(c.get("number", c.get("collector_number",""))),
            "img":      img,
            "price":    price_cad,
            "chg1":     0.0,
            "chg7":     chg7,
            "chg30":    chg30,
        })
    return results

def rar_pill(r):
    m={"SIR":"p-sir","IR":"p-ir","Shiny":"p-shv","SHV":"p-shv","HR":"p-rr",
       "UR":"p-alt","Secret":"p-gold","RR":"p-rr","Gold":"p-gold",
       "TG":"p-fa","ACE":"p-ir","Radiant":"p-ir","AR":"p-alt","FA":"p-fa"}
    return f'<span class="pill {m.get(r,"p-def")}">{r}</span>'

def fmt_chg(v):
    if v>0.5:  return f'<span style="color:#10b981;font-size:11px;font-weight:600">▲ +{v:.1f}%</span>'
    if v<-0.5: return f'<span style="color:#ef4444;font-size:11px;font-weight:600">▼ {v:.1f}%</span>'
    return '<span style="color:#334155;font-size:11px">—</span>'

# ── Session ──
if "all_cards"    not in st.session_state: st.session_state.all_cards    = []
if "loading_done" not in st.session_state: st.session_state.loading_done = False
if "set_names"    not in st.session_state: st.session_state.set_names    = []

# ════ SIDEBAR ════
with st.sidebar:
    st.markdown("### 🃏 The Nasty Model")
    st.markdown("---")
    show_day = st.toggle("⚡ Mode Show Day", value=False)

    st.markdown('<span class="sb-section">Période</span>', unsafe_allow_html=True)
    period_map     = {"24 heures":"chg1","7 jours":"chg7","30 jours":"chg30"}
    period_lbl_map = {"24 heures":"24h","7 jours":"7j","30 jours":"30j"}
    period_sel = st.selectbox("", list(period_map.keys()), index=1, label_visibility="collapsed")
    chg_key    = period_map[period_sel]
    period_lbl = period_lbl_map[period_sel]

    st.markdown('<span class="sb-section">Set</span>', unsafe_allow_html=True)
    set_opts   = ["Tous les sets"] + ([s[0] for s in POKEMON_SETS])
    set_filter = st.selectbox("", set_opts, label_visibility="collapsed")

    st.markdown('<span class="sb-section">Prix C$</span>', unsafe_allow_html=True)
    ca,cb = st.columns(2)
    with ca: prix_min = st.number_input("Min",min_value=0,value=0,step=5)
    with cb: prix_max = st.number_input("Max",min_value=0,value=5000,step=25)

    st.markdown('<span class="sb-section">Recherche</span>', unsafe_allow_html=True)
    search = st.text_input("",placeholder="Nom de la carte...",label_visibility="collapsed")

    st.markdown("---")
    n = len(st.session_state.all_cards)
    st.markdown(f'<div style="font-size:11px;color:#2d3748;text-align:center;margin-bottom:8px">{n} cartes · tcgapi.dev</div>', unsafe_allow_html=True)
    if st.button("🔄  Forcer rechargement", type="primary"):
        st.session_state.all_cards=[]; st.session_state.loading_done=False
        st.session_state.set_names=[]; fetch_set_prices.clear()
        if os.path.exists(CACHE_FILE): os.remove(CACHE_FILE)
        st.rerun()

# ════ LOAD ════
if not st.session_state.loading_done:
    if cache_fresh():
        c=load_json(CACHE_FILE,{})
        if c.get("cards"):
            st.session_state.all_cards=c["cards"]
            st.session_state.loading_done=True
            st.session_state.set_names=[s[0] for s in POKEMON_SETS]

if not st.session_state.loading_done:
    prog  = st.progress(0, text="Chargement des prix TCGPlayer...")
    total = len(POKEMON_SETS)
    all_cards = []

    for i,(sname,syear,scode) in enumerate(POKEMON_SETS):
        cards = fetch_set_prices(scode, sname, syear)
        all_cards.extend(cards)
        pct = min(99, int((i+1)/total*100))
        prog.progress(pct, text=f"{sname} — {len(all_cards)} cartes ({i+1}/{total})")

    prog.progress(100, text=f"✓ {len(all_cards)} cartes")
    prog.empty()
    st.session_state.all_cards    = all_cards
    st.session_state.loading_done = True
    st.session_state.set_names    = [s[0] for s in POKEMON_SETS]
    save_json(CACHE_FILE, {"cards": all_cards, "ts": datetime.now().isoformat()})
    st.rerun()

# ════ MAIN ════
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
    <div style="background:#0d1520;border:1px solid #1a1f35;color:#334155;font-size:11px;padding:4px 10px;border-radius:20px">{len(st.session_state.all_cards)} cartes</div>
  </div>
</div>
""", unsafe_allow_html=True)

df = pd.DataFrame(st.session_state.all_cards) if st.session_state.all_cards else pd.DataFrame()

if df.empty:
    # Debug: test API directly
    st.warning("Aucune carte chargée — test de l'API en cours...")
    try:
        r = requests.get(f"{BASE_URL}/sets/sv8pt5/prices", headers=hdrs(), timeout=10)
        st.write(f"**`/sets/sv8pt5/prices` → HTTP {r.status_code}**")
        st.code(r.text[:600])
        r2 = requests.get(f"{BASE_URL}/search", params={"q":"Umbreon","game":"pokemon","limit":2}, headers=hdrs(), timeout=10)
        st.write(f"**`/search?q=Umbreon` → HTTP {r2.status_code}**")
        st.code(r2.text[:600])
    except Exception as e:
        st.error(f"Erreur: {e}")
    st.stop()

# Filters
if show_day:        df=df[df[chg_key]>=10]
if prix_min>0:      df=df[df["price"]>=prix_min]
if prix_max<5000:   df=df[df["price"]<=prix_max]
if search:          df=df[df["name"].str.lower().str.contains(search.lower(),na=False)]
if set_filter!="Tous les sets": df=df[df["set_name"]==set_filter]
df = df.sort_values(chg_key,ascending=False).reset_index(drop=True)

if show_day:
    avg=df[chg_key].mean() if len(df) else 0
    st.markdown(f"""<div class="show-banner"><span style="font-size:26px">⚡</span>
    <div style="flex:1"><div style="font-size:14px;font-weight:700;color:#06b6d4">MODE SHOW DAY — {period_sel}</div>
    <div style="font-size:12px;color:#0e7490;margin-top:2px">Cartes ≥ 10% · vendeurs pas encore repriced</div></div>
    <div class="stat-box" style="margin-right:8px"><div class="stat-v">{len(df)}</div><div class="stat-l">opportunités</div></div>
    <div class="stat-box"><div class="stat-v">+{avg:.1f}%</div><div class="stat-l">gain moy.</div></div></div>""",
    unsafe_allow_html=True)

st.markdown(f"""<div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:12px">
  <div><span style="font-size:18px;font-weight:800;color:#f1f5f9">biggest market movers</span>
  <span style="font-size:12px;color:#334155;margin-left:8px">· {period_sel} · trié par % de gain</span></div>
  <span style="font-size:12px;color:#2d3748">{len(df)} cartes</span></div>""",unsafe_allow_html=True)

items=""
for _,row in df.iterrows():
    chg=row[chg_key]; up=chg>0.5; dn=chg<-0.5
    clr="#10b981" if up else ("#ef4444" if dn else "#64748b")
    arrow="▲" if up else ("▼" if dn else "")
    pct_str=f"{arrow} +{chg:.1f}%" if up else (f"{arrow} {chg:.1f}%" if dn else "—")
    img_html=f'<img src="{row["img"]}" class="card-thumb" onerror="this.style.display=\'none\';this.nextSibling.style.display=\'flex\'" /><div class="card-thumb-ph" style="display:none">🃏</div>' if row.get("img") else '<div class="card-thumb-ph">🃏</div>'
    bp='<span class="badge-pump">🔥 24h</span>' if row["chg1"]>5 else ""
    bs='<span class="badge-show">⚡ SHOW</span>' if row["chg7"]>=10 else ""
    items+=f"""<div class="card-item">{img_html}
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

st.markdown(items if items else '<div style="text-align:center;padding:4rem;color:#2d3748">Aucune carte.</div>', unsafe_allow_html=True)

st.markdown("<hr style='margin:1.5rem 0'>", unsafe_allow_html=True)
with st.expander("📋  Export CSV"):
    ex=df[df[chg_key]>=10].copy() if not show_day else df.copy()
    if len(ex)>0:
        out=ex[["name","set_name","rarity","price","chg1","chg7","chg30"]].copy()
        out.columns=["Carte","Set","Rareté","Prix CA$","24h %","7j %","30j %"]
        out["Offre -15%"]=(out["Prix CA$"]*0.85).round(2)
        out["Offre -25%"]=(out["Prix CA$"]*0.75).round(2)
        st.dataframe(out,use_container_width=True,hide_index=True)
        st.download_button("⬇️ CSV",data=out.to_csv(index=False),
            file_name=f"show_{datetime.now().strftime('%Y%m%d')}.csv",mime="text/csv",type="primary")

with st.expander("⚙️  Paramètres"):
    if st.button("🗑️  Vider cache & recharger"):
        st.session_state.all_cards=[]; st.session_state.loading_done=False
        fetch_set_prices.clear()
        if os.path.exists(CACHE_FILE): os.remove(CACHE_FILE)
        st.rerun()
