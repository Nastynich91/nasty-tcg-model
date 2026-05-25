import streamlit as st
import pandas as pd
import json, os, requests, time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

st.set_page_config(page_title="The Nasty Model", page_icon="🃏", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
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
.badge-show{font-size:9px;padding:2px 7px;border-radius:8px;font-weight:700;margin-left:6px;vertical-align:middle;background:rgba(6,182,212,.12);color:#06b6d4;border:1px solid rgba(6,182,212,.25)}
.show-banner{background:linear-gradient(135deg,#0a1a2e,#0d1f3c);border:1px solid #0891b2;border-radius:14px;padding:14px 20px;display:flex;align-items:center;gap:16px;margin-bottom:1rem}
.sb-section{font-size:10px;font-weight:700;color:#2d3748!important;text-transform:uppercase;letter-spacing:.08em;margin:14px 0 5px;display:block}
.stat-box{text-align:center;background:rgba(6,182,212,.1);border:1px solid rgba(6,182,212,.2);border-radius:10px;padding:8px 18px}
.stat-v{font-size:22px;font-weight:800;color:#06b6d4}
.stat-l{font-size:10px;color:#0e7490;text-transform:uppercase;letter-spacing:.06em}
</style>
""", unsafe_allow_html=True)

USD_CAD    = 1.364
CACHE_FILE    = "data/cards_cache.json"
HISTORY_FILE  = "data/price_history.json"
CACHE_TTL     = 12  # hours — refresh prices every 12h
API_KEY    = "eb69335a-2210-45de-a842-8d8211aa0dbe"
BASE_URL   = "https://api.pokemontcg.io/v2"

# High-value rarities only
TARGET_RARITIES = {
    "Special Illustration Rare", "Illustration Rare",
    "Hyper Rare", "Double Rare", "Shiny Rare",
    "Shiny Ultra Rare", "Trainer Gallery Rare Holo",
    "Radiant Rare", "Gold Rare", "Amazing Rare",
    "ACE SPEC Rare", "Secret Rare", "Ultra Rare",
    "Rainbow Rare", "Full Art", "LEGEND",
}
RARITY_SHORT = {
    "Special Illustration Rare":"SIR","Illustration Rare":"IR",
    "Hyper Rare":"HR","Double Rare":"RR","Shiny Rare":"Shiny",
    "Shiny Ultra Rare":"SHV","Trainer Gallery Rare Holo":"TG",
    "Radiant Rare":"Radiant","Gold Rare":"Gold","Amazing Rare":"AR",
    "ACE SPEC Rare":"ACE","Secret Rare":"Secret","Ultra Rare":"UR",
    "Rainbow Rare":"RR","Full Art":"FA","LEGEND":"Legend",
}

# All sets — verified pokemontcg.io set IDs
# Mega Evolution is its own series separate from SV
# SV10 = Destined Rivals, SV9 = Journey Together
SETS = [
    # ── Mega Evolution series (2025-2026) ──
    ("me3pt5","Perfect Order",2026),
    ("me3","Chaos Rising",2026),
    ("me2pt5","Ascended Heroes",2026),
    ("me2","Phantasmal Flames",2025),
    ("me1pt5","White Flare & Black Bolt",2025),
    ("me1","Mega Evolution",2025),
    # ── Scarlet & Violet series ──
    ("sv10","Destined Rivals",2025),
    ("sv9","Journey Together",2025),
    ("sv8pt5","Prismatic Evolutions",2025),
    ("sv8","Surging Sparks",2024),
    ("sv7","Stellar Crown",2024),
    ("sv6pt5","Shrouded Fable",2024),
    ("sv6","Twilight Masquerade",2024),
    ("sv5","Temporal Forces",2024),
    ("sv4pt5","Paldean Fates",2024),
    ("sv4","Paradox Rift",2023),
    ("sv3pt5","Pokemon 151",2023),
    ("sv3","Obsidian Flames",2023),
    ("sv2","Paldea Evolved",2023),
    ("sv1","Scarlet & Violet",2023),
    # ── Sword & Shield series ──
    ("swsh125","Crown Zenith",2023),
    ("swsh12","Silver Tempest",2022),
    ("swsh11","Lost Origin",2022),
    ("pgo","Pokemon GO",2022),
    ("swsh10","Astral Radiance",2022),
    ("swsh9","Brilliant Stars",2022),
    ("cel25","Celebrations",2021),
    ("swsh8","Fusion Strike",2021),
    ("swsh7","Evolving Skies",2021),
    ("swsh6","Chilling Reign",2021),
    ("swsh5","Battle Styles",2021),
    ("shf","Shining Fates",2021),
    ("swsh4","Vivid Voltage",2020),
    ("swsh3","Darkness Ablaze",2020),
    ("swsh2","Rebel Clash",2020),
    # ── Sun & Moon series ──
    ("sm12","Cosmic Eclipse",2019),
    ("hif","Hidden Fates",2019),
    ("sm11","Unified Minds",2019),
    ("sm10","Unbroken Bonds",2019),
    ("sm9","Team Up",2019),
    ("sm8","Lost Thunder",2018),
    ("sm7","Celestial Storm",2018),
    ("sm35","Shining Legends",2017),
    ("sm3","Burning Shadows",2017),
    # ── XY series ──
    ("xy12","Evolutions",2016),
    ("xy7","Ancient Origins",2015),
    ("xy6","Roaring Skies",2015),
]

def load_json(p, d):
    if os.path.exists(p):
        with open(p) as f: return json.load(f)
    return d

def save_json(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f: json.dump(d, f, ensure_ascii=False)

def save_price_snapshot(cards):
    """Save a timestamped price snapshot for each card. Keep 30 days of history."""
    history = load_json(HISTORY_FILE, {})
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    today   = datetime.now().strftime("%Y-%m-%d")

    for c in cards:
        cid = c["id"]
        if cid not in history:
            history[cid] = []
        # Add today's price if not already recorded today
        existing_dates = [e["d"][:10] for e in history[cid]]
        if today not in existing_dates:
            history[cid].append({"d": now_str, "p": c["price"]})
        # Keep only last 35 entries
        history[cid] = history[cid][-35:]

    save_json(HISTORY_FILE, history)
    return history

def calc_changes(card_id, current_price, history):
    """Calculate % price change over different periods."""
    entries = history.get(card_id, [])
    if not entries or len(entries) < 2:
        return 0.0, 0.0, 0.0, 0.0, 0.0

    now = datetime.now()

    def find_price_days_ago(days):
        target = now - __import__("datetime").timedelta(days=days)
        # Find closest entry at or before target date
        best = None
        for e in entries:
            try:
                ed = datetime.strptime(e["d"][:10], "%Y-%m-%d")
                if ed <= target:
                    if best is None or ed > datetime.strptime(best["d"][:10], "%Y-%m-%d"):
                        best = e
            except: pass
        return best["p"] if best else None

    def pct(past):
        if past and past > 0:
            return round((current_price - past) / past * 100, 2)
        return 0.0

    p1   = find_price_days_ago(1)
    p3   = find_price_days_ago(3)
    p7   = find_price_days_ago(7)
    p30  = find_price_days_ago(30)
    # Use oldest available as 6M proxy if we don't have 180 days
    p_old = entries[0]["p"] if entries else None

    return pct(p1), pct(p3), pct(p7), pct(p30), pct(p_old)

def cache_fresh():
    if not os.path.exists(CACHE_FILE): return False
    c = load_json(CACHE_FILE, {})
    ts = c.get("ts")
    if not ts: return False
    return (datetime.now() - datetime.fromisoformat(ts)).total_seconds() / 3600 < CACHE_TTL

def fetch_set(set_id, set_name, set_year):
    """
    Fetch all valuable cards for a set from pokemontcg.io.
    - 1000 req/day free with API key
    - Includes TCGPlayer prices (market, mid, low, high)
    - Includes card images
    - One paginated call per set
    """
    hdrs = {"X-Api-Key": API_KEY}
    results = []
    page = 1
    page_size = 250

    while True:
        try:
            r = requests.get(
                f"{BASE_URL}/cards",
                params={
                    "q": f"set.id:{set_id}",
                    "select": "id,name,rarity,images,tcgplayer,number,set",
                    "pageSize": page_size,
                    "page": page,
                },
                headers=hdrs,
                timeout=20
            )
            if r.status_code == 429:
                time.sleep(2)
                continue
            if r.status_code != 200:
                break

            body  = r.json()
            cards = body.get("data", [])
            total = body.get("totalCount", 0)

            for c in cards:
                rarity = c.get("rarity", "")
                if rarity not in TARGET_RARITIES:
                    continue

                # Extract best price from TCGPlayer
                prices    = c.get("tcgplayer", {}).get("prices", {})
                price_usd = None
                for variant in ["holofoil", "1stEditionHolofoil", "reverseHolofoil", "normal", "unlimitedHolofoil"]:
                    p = prices.get(variant, {})
                    m = p.get("market") or p.get("mid")
                    if m and float(m) > 0:
                        price_usd = float(m)
                        break

                if not price_usd or price_usd < 2:
                    continue

                price_cad = round(price_usd * USD_CAD, 2)

                # Image
                imgs = c.get("images", {})
                img  = imgs.get("large") or imgs.get("small", "")

                results.append({
                    "id":       c.get("id", ""),
                    "name":     c.get("name", ""),
                    "set_id":   set_id,
                    "set_name": set_name,
                    "set_year": set_year,
                    "rarity":   RARITY_SHORT.get(rarity, rarity),
                    "number":   c.get("number", ""),
                    "img":      img,
                    "price":    price_cad,
                    # pokemontcg.io doesn't have historical data
                    # We calculate pseudo-changes from updatedAt
                    "chg1":  0.0,
                    "chg7":  0.0,
                    "chg30": 0.0,
                    "tcg_updated": c.get("tcgplayer", {}).get("updatedAt", ""),
                })

            if page * page_size >= total or len(cards) < page_size:
                break
            page += 1

        except Exception:
            break

    return results

def rar_pill(r):
    m = {"SIR":"p-sir","IR":"p-ir","Shiny":"p-shv","SHV":"p-shv","HR":"p-rr",
         "UR":"p-alt","Secret":"p-gold","RR":"p-rr","Gold":"p-gold",
         "TG":"p-fa","ACE":"p-ir","Radiant":"p-ir","AR":"p-alt","FA":"p-fa"}
    return f'<span class="pill {m.get(r,"p-def")}">{r}</span>'

# ── Session ──
if "all_cards"    not in st.session_state: st.session_state.all_cards    = []
if "loading_done" not in st.session_state: st.session_state.loading_done = False

# ════ SIDEBAR ════
with st.sidebar:
    st.markdown("### 🃏 The Nasty Model")
    st.markdown("---")
    show_day = st.toggle("⚡ Mode Show Day", value=False, help="Prix les plus élevés et haut potentiel")

    st.markdown('<span class="sb-section">Trier par</span>', unsafe_allow_html=True)
    st.markdown('<span class="sb-section">Période</span>', unsafe_allow_html=True)
    period_map = {"24h":"chg1","3 jours":"chg3","7 jours":"chg7","1 mois":"chg30"}
    period_sel = st.selectbox("", list(period_map.keys()), index=2, label_visibility="collapsed")
    chg_key    = period_map[period_sel]

    st.markdown('<span class="sb-section">Trier par</span>', unsafe_allow_html=True)
    sort_ui = st.selectbox("", ["% gain ↓","Prix ↓","Prix ↑","Nom A→Z"], label_visibility="collapsed")

    st.markdown('<span class="sb-section">Set</span>', unsafe_allow_html=True)
    set_opts   = ["Tous les sets"] + sorted(set(s[1] for s in SETS))
    set_filter = st.selectbox("", set_opts, label_visibility="collapsed")

    st.markdown('<span class="sb-section">Prix C$</span>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca: prix_min = st.number_input("Min", min_value=0, value=0,    step=5)
    with cb: prix_max = st.number_input("Max", min_value=0, value=5000, step=25)

    st.markdown('<span class="sb-section">Rareté</span>', unsafe_allow_html=True)
    rar_filter = st.selectbox("", ["Toutes","SIR","IR","HR","RR","SHV","Shiny","Gold","FA","Secret","UR"], label_visibility="collapsed")

    st.markdown('<span class="sb-section">Recherche</span>', unsafe_allow_html=True)
    search = st.text_input("", placeholder="Nom de la carte...", label_visibility="collapsed")

    st.markdown("---")
    n = len(st.session_state.all_cards)
    st.markdown(f'<div style="font-size:11px;color:#2d3748;text-align:center;margin-bottom:8px">{n} cartes · pokemontcg.io</div>', unsafe_allow_html=True)
    if st.button("🔄  Forcer rechargement", type="primary"):
        st.session_state.all_cards    = []
        st.session_state.loading_done = False
        if os.path.exists(CACHE_FILE): os.remove(CACHE_FILE)
        st.rerun()

# ════ LOAD ════
if not st.session_state.loading_done:
    if cache_fresh():
        c = load_json(CACHE_FILE, {})
        if c.get("cards"):
            # Re-apply history to cached cards (in case history grew since last cache)
            history = load_json(HISTORY_FILE, {})
            for card in c["cards"]:
                c1,c3,c7,c30,cold = calc_changes(card["id"], card["price"], history)
                card["chg1"]=c1; card["chg3"]=c3; card["chg7"]=c7
                card["chg30"]=c30; card["chg_old"]=cold
            st.session_state.all_cards    = c["cards"]
            st.session_state.loading_done = True

if not st.session_state.loading_done:
    prog = st.progress(0, text="Connexion à pokemontcg.io...")
    all_cards = []
    total = len(SETS)
    done_count = [0]

    def load_one(args):
        sid, sname, syear = args
        cards = fetch_set(sid, sname, syear)
        done_count[0] += 1
        return cards

    # Parallel load with 6 workers — much faster than sequential
    with ThreadPoolExecutor(max_workers=6) as ex:
        futures = {ex.submit(load_one, s): s for s in SETS}
        for f in as_completed(futures):
            result = f.result() or []
            all_cards.extend(result)
            pct = min(99, int(done_count[0] / total * 100))
            prog.progress(pct, text=f"{done_count[0]}/{total} sets · {len(all_cards)} cartes chargées")

    prog.progress(100, text=f"✓ {len(all_cards)} cartes")
    prog.empty()

    # Save price snapshot for historical tracking
    history = save_price_snapshot(all_cards)

    # Compute price changes from history
    for c in all_cards:
        c1, c3, c7, c30, c_old = calc_changes(c["id"], c["price"], history)
        c["chg1"]  = c1
        c["chg3"]  = c3
        c["chg7"]  = c7
        c["chg30"] = c30
        c["chg_old"] = c_old

    st.session_state.all_cards    = all_cards
    st.session_state.loading_done = True
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
    st.warning("Aucune carte chargée. Clique **Forcer rechargement**.")
    st.stop()

# Filters
if show_day:
    # Show Day = cartes avec gain >= 10% sur 7j OU prix > 50$
    if "chg7" in df.columns:
        df = df[(df["chg7"] >= 10) | (df["price"] >= 50)]
    else:
        df = df[df["price"] >= 50]
if prix_min > 0:    df = df[df["price"] >= prix_min]
if prix_max < 5000: df = df[df["price"] <= prix_max]
if rar_filter != "Toutes": df = df[df["rarity"] == rar_filter]
if search:          df = df[df["name"].str.lower().str.contains(search.lower(), na=False)]
if set_filter != "Tous les sets": df = df[df["set_name"] == set_filter]

sort_map = {"% gain ↓":(chg_key,False),"Prix ↓":("price",False),"Prix ↑":("price",True),"Nom A→Z":("name",True)}
sk, sa = sort_map[sort_ui]
df = df.sort_values(sk, ascending=sa).reset_index(drop=True)

if show_day:
    st.markdown(f"""
    <div class="show-banner">
      <span style="font-size:26px">⚡</span>
      <div style="flex:1">
        <div style="font-size:14px;font-weight:700;color:#06b6d4">MODE SHOW DAY — cartes > CA$50</div>
        <div style="font-size:12px;color:#0e7490;margin-top:2px">Les cartes les plus précieuses — priorité aux achats au show</div>
      </div>
      <div class="stat-box"><div class="stat-v">{len(df)}</div><div class="stat-l">cartes cibles</div></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:12px">
  <div>
    <span style="font-size:18px;font-weight:800;color:#f1f5f9">biggest market movers</span>
    <span style="font-size:12px;color:#334155;margin-left:8px">· {period_sel} · trié par {sort_ui}</span>
  </div>
  <span style="font-size:12px;color:#2d3748">{len(df)} cartes</span>
</div>
""", unsafe_allow_html=True)

if len(df) == 0:
    st.markdown('<div style="text-align:center;padding:4rem;color:#2d3748">Aucune carte.</div>', unsafe_allow_html=True)
else:
    items = ""
    for _, row in df.iterrows():
        img_html = f'<img src="{row["img"]}" class="card-thumb" onerror="this.style.display=\'none\';this.nextSibling.style.display=\'flex\'" /><div class="card-thumb-ph" style="display:none">🃏</div>' if row.get("img") else '<div class="card-thumb-ph">🃏</div>'

        def chg_span(v):
            if v > 0.5:  return f'<span style="color:#10b981;font-weight:600">▲ +{v:.1f}%</span>'
            if v < -0.5: return f'<span style="color:#ef4444;font-weight:600">▼ {v:.1f}%</span>'
            return '<span style="color:#334155">—</span>'

        c1=row.get("chg1",0); c3=row.get("chg3",0); c7=row.get("chg7",0); c30=row.get("chg30",0)
        active_chg = row.get(chg_key, 0)
        bs  = '<span class="badge-show">⚡ SHOW</span>' if c7 >= 10 or row["price"] >= 50 else ""
        clr = "#10b981" if active_chg > 0.5 else "#ef4444" if active_chg < -0.5 else "#64748b"
        pct_str = f"▲ +{active_chg:.1f}%" if active_chg > 0.5 else (f"▼ {active_chg:.1f}%" if active_chg < -0.5 else "—")

        items += f"""
<div class="card-item">
  {img_html}
  <div class="card-info">
    <div class="card-name">{row['name']}{bs}</div>
    <div class="card-set-line">{row['set_name']}</div>
    <div class="card-meta">{rar_pill(row['rarity'])} · #{row['number']} · {row['set_year']}</div>
    <div style="margin-top:6px;display:flex;gap:14px">
      <span style="font-size:11px;color:#4a5568">24h: {chg_span(c1)}</span>
      <span style="font-size:11px;color:#4a5568">3j: {chg_span(c3)}</span>
      <span style="font-size:11px;color:#4a5568">7j: {chg_span(c7)}</span>
      <span style="font-size:11px;color:#4a5568">1M: {chg_span(c30)}</span>
    </div>
  </div>
  <div class="card-price-block">
    <div class="price-main">CA${row['price']:.2f}</div>
    <div class="price-change" style="color:{clr}">{pct_str}</div>
    <div class="price-source">TCGPlayer · USD→CAD</div>
  </div>
</div>"""

    st.markdown(items, unsafe_allow_html=True)

# Export + Settings
st.markdown("<hr style='margin:1.5rem 0'>", unsafe_allow_html=True)

# Show which sets are empty (debug tool)
with st.expander("🔍  Sets disponibles dans pokemontcg.io"):
    if st.session_state.all_cards:
        df_sets = pd.DataFrame(st.session_state.all_cards)
        set_counts = df_sets.groupby(["set_id","set_name"]).size().reset_index(name="cartes")
        set_counts = set_counts.sort_values("set_name")
        all_set_ids = {s[0]: s[1] for s in SETS}
        st.markdown("**Sets avec cartes :**")
        st.dataframe(set_counts, use_container_width=True, hide_index=True)
        empty = [(sid, sname) for sid, sname, _ in SETS 
                 if sid not in df_sets["set_id"].values]
        if empty:
            st.markdown("**Sets vides (ID introuvable dans pokemontcg.io) :**")
            for sid, sname in empty:
                st.markdown(f"- `{sid}` → {sname}")

with st.expander("📋  Export liste d'achat CSV"):
    ex = df[df["price"] >= 50].copy() if not show_day else df.copy()
    if len(ex) > 0:
        out = ex[["name","set_name","rarity","price","number"]].copy()
        out.columns = ["Carte","Set","Rareté","Prix CA$","#"]
        out["Offre -15%"] = (out["Prix CA$"]*0.85).round(2)
        out["Offre -25%"] = (out["Prix CA$"]*0.75).round(2)
        st.dataframe(out, use_container_width=True, hide_index=True)
        st.download_button("⬇️ CSV", data=out.to_csv(index=False),
            file_name=f"show_{datetime.now().strftime('%Y%m%d')}.csv", mime="text/csv", type="primary")

with st.expander("⚙️  Paramètres"):
    if st.button("🗑️  Vider cache & recharger"):
        st.session_state.all_cards=[]; st.session_state.loading_done=False
        if os.path.exists(CACHE_FILE): os.remove(CACHE_FILE)
        st.rerun()
