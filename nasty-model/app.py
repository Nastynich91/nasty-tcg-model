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

USD_CAD    = 1.364
CACHE_FILE = "data/cards_cache.json"
CACHE_TTL  = 12  # hours
API_KEY    = "tcg_live_2b62c19d32e9a3e7314ab4c7b44c617828a130ec"
BASE_URL   = "https://api.tcgapi.dev/v1"

TARGET_RARITIES = {
    "Special Illustration Rare","Illustration Rare",
    "Hyper Rare","Ultra Rare","Secret Rare",
    "Shiny Rare","Shiny Ultra Rare","Double Rare",
    "Trainer Gallery Rare Holo","Radiant Rare",
    "Gold Rare","Amazing Rare","ACE SPEC Rare",
    "Rainbow Rare","Full Art","Secret","Promo",
}
RARITY_SHORT = {
    "Special Illustration Rare":"SIR","Illustration Rare":"IR",
    "Hyper Rare":"HR","Ultra Rare":"UR","Secret Rare":"Secret",
    "Shiny Rare":"Shiny","Shiny Ultra Rare":"SHV","Double Rare":"RR",
    "Trainer Gallery Rare Holo":"TG","Radiant Rare":"Radiant",
    "Gold Rare":"Gold","Amazing Rare":"AR","ACE SPEC Rare":"ACE",
    "Rainbow Rare":"RR","Full Art":"FA","Secret":"Secret","Promo":"Promo",
}

def load_json(p, d):
    if os.path.exists(p):
        with open(p) as f: return json.load(f)
    return d

def save_json(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w") as f: json.dump(d, f, ensure_ascii=False)

def cache_fresh():
    if not os.path.exists(CACHE_FILE): return False
    c = load_json(CACHE_FILE, {})
    ts = c.get("ts")
    if not ts: return False
    return (datetime.now() - datetime.fromisoformat(ts)).total_seconds() / 3600 < CACHE_TTL

def headers():
    return {"Authorization": f"Bearer {API_KEY}", "Accept": "application/json"}

@st.cache_data(ttl=43200, show_spinner=False)
def fetch_pokemon_sets():
    """Get all Pokemon sets from tcgapi.dev"""
    try:
        r = requests.get(f"{BASE_URL}/sets", params={"game": "pokemon", "limit": 200},
                        headers=headers(), timeout=20)
        if r.status_code == 200:
            body = r.json()
            return body if isinstance(body, list) else body.get("data", body.get("sets", []))
    except: pass
    return []

@st.cache_data(ttl=43200, show_spinner=False)
def fetch_set_cards(set_id, set_name, set_year):
    """Fetch all valuable cards for one set"""
    try:
        r = requests.get(f"{BASE_URL}/cards",
                        params={"set": set_id, "game": "pokemon", "limit": 500},
                        headers=headers(), timeout=25)
        if r.status_code != 200: return []
        body = r.json()
        cards = body if isinstance(body, list) else body.get("data", body.get("cards", []))

        results = []
        for c in cards:
            rarity = (c.get("rarity") or c.get("rarityName") or "")

            # Extract price USD
            price_usd = None
            for f in ["price","marketPrice","market_price","tcgPlayerPrice","value"]:
                v = c.get(f)
                if v:
                    try:
                        fv = float(str(v).replace("$","").replace(",",""))
                        if fv > 0.5: price_usd = fv; break
                    except: pass
            if not price_usd:
                for obj_k in ["pricing","prices","tcgplayer","market"]:
                    obj = c.get(obj_k, {})
                    if isinstance(obj, dict):
                        for sub in ["market","marketPrice","mid","price","usd"]:
                            v = obj.get(sub)
                            if v:
                                try:
                                    fv = float(str(v).replace("$",""))
                                    if fv > 0.5: price_usd = fv; break
                                except: pass
                    if price_usd: break
            if not price_usd: continue

            # Skip commons under $5
            if price_usd < 5 and rarity not in TARGET_RARITIES: continue

            price_cad = round(price_usd * USD_CAD, 2)

            # Price changes
            chg1 = chg7 = chg30 = 0.0
            for pc_k in ["price_change","priceChange","change","changes","price_changes"]:
                pc = c.get(pc_k)
                if isinstance(pc, dict):
                    def safe(v): 
                        try: return float(v or 0)
                        except: return 0.0
                    chg1  = safe(pc.get("24h") or pc.get("1d") or pc.get("day"))
                    chg7  = safe(pc.get("7d")  or pc.get("7")  or pc.get("week"))
                    chg30 = safe(pc.get("30d") or pc.get("30") or pc.get("month"))
                    break

            # Image
            img = ""
            for img_k in ["image","imageUrl","img","image_url","large"]:
                v = c.get(img_k, "")
                if isinstance(v,str) and v.startswith("http"): img=v; break
            if not img:
                imgs = c.get("images",{})
                img = imgs.get("large") or imgs.get("small","")

            results.append({
                "id":       str(c.get("id","")),
                "name":     c.get("name",""),
                "set_id":   set_id,
                "set_name": set_name,
                "set_year": set_year,
                "rarity":   RARITY_SHORT.get(rarity, rarity) if rarity else "—",
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
    m={"SIR":"p-sir","IR":"p-ir","Shiny":"p-shv","SHV":"p-shv","HR":"p-rr",
       "UR":"p-alt","Secret":"p-gold","RR":"p-rr","Gold":"p-gold",
       "TG":"p-fa","ACE":"p-ir","Radiant":"p-ir","AR":"p-alt","FA":"p-fa"}
    return f'<span class="pill {m.get(r,"p-def")}">{r}</span>'

def fmt_chg(v):
    if v >  0.5: return f'<span style="color:#10b981;font-size:11px;font-weight:600">▲ +{v:.1f}%</span>'
    if v < -0.5: return f'<span style="color:#ef4444;font-size:11px;font-weight:600">▼ {v:.1f}%</span>'
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
    set_opts = ["Tous les sets"] + st.session_state.set_names
    set_filter = st.selectbox("", set_opts, label_visibility="collapsed")

    st.markdown('<span class="sb-section">Prix C$</span>', unsafe_allow_html=True)
    ca, cb = st.columns(2)
    with ca: prix_min = st.number_input("Min", min_value=0, value=0,    step=5)
    with cb: prix_max = st.number_input("Max", min_value=0, value=5000, step=25)

    st.markdown('<span class="sb-section">Recherche</span>', unsafe_allow_html=True)
    search = st.text_input("", placeholder="Nom de la carte...", label_visibility="collapsed")

    st.markdown("---")
    n = len(st.session_state.all_cards)
    st.markdown(f'<div style="font-size:11px;color:#2d3748;text-align:center;margin-bottom:8px">{n} cartes · tcgapi.dev</div>', unsafe_allow_html=True)
    if st.button("🔄  Forcer rechargement", type="primary"):
        st.session_state.all_cards    = []
        st.session_state.loading_done = False
        st.session_state.set_names    = []
        fetch_pokemon_sets.clear()
        fetch_set_cards.clear()
        if os.path.exists(CACHE_FILE): os.remove(CACHE_FILE)
        st.rerun()

# ════ LOAD ════
if not st.session_state.loading_done:
    # Try cache first
    if cache_fresh():
        c = load_json(CACHE_FILE, {})
        if c.get("cards"):
            st.session_state.all_cards    = c["cards"]
            st.session_state.loading_done = True
            st.session_state.set_names    = sorted(set(x["set_name"] for x in c["cards"]))

if not st.session_state.loading_done:
    prog = st.progress(0, text="Connexion à tcgapi.dev...")

    # Step 1: get all Pokemon sets
    sets = fetch_pokemon_sets()

    if not sets:
        st.error("❌ Impossible de charger les sets depuis tcgapi.dev. Vérifie la clé API.")
        st.write(f"**Debug:** Tentative sur `{BASE_URL}/sets?game=pokemon`")
        st.stop()

    prog.progress(5, text=f"{len(sets)} sets Pokémon trouvés...")

    all_cards = []
    total = len(sets)

    for i, s in enumerate(sets):
        sid      = s.get("id") or s.get("setId") or s.get("code","")
        sname    = s.get("name","")
        syear    = 0
        rd       = str(s.get("releaseDate","") or s.get("release_date","") or "")
        if len(rd) >= 4:
            try: syear = int(rd[:4])
            except: pass

        cards = fetch_set_cards(sid, sname, syear)
        all_cards.extend(cards)

        pct = min(99, int(5 + (i+1)/total*94))
        prog.progress(pct, text=f"{sname} — {len(all_cards)} cartes ({i+1}/{total})")

    prog.progress(100, text=f"✓ {len(all_cards)} cartes chargées")
    prog.empty()

    st.session_state.all_cards    = all_cards
    st.session_state.loading_done = True
    st.session_state.set_names    = sorted(set(x["set_name"] for x in all_cards))
    save_json(CACHE_FILE, {"cards": all_cards, "ts": datetime.now().isoformat()})
    st.rerun()

# ════ MAIN ════
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;padding:1rem 0 1.25rem;border-bottom:1px solid #1a1f35;margin-bottom:1.25rem">
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:40px;height:40px;background:linear-gradient(135deg,#06b6d4,#0891b2);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px">🃏</div>
    <div>
      <div style="font-size:20px;font-weight:800;color:#f1f5f9;letter-spacing:-.03em">The Nasty Model</div>
      <div style="font-size:11px;color:#2d3748">tcgapi.dev · TCGPlayer prices · C$ · {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
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
    st.info("Aucune carte. Clique Forcer rechargement.")
    st.stop()

# Filters
if show_day:        df = df[df[chg_key] >= 10]
if prix_min > 0:    df = df[df["price"] >= prix_min]
if prix_max < 5000: df = df[df["price"] <= prix_max]
if search:          df = df[df["name"].str.lower().str.contains(search.lower(), na=False)]
if set_filter != "Tous les sets":
    df = df[df["set_name"] == set_filter]

df = df.sort_values(chg_key, ascending=False).reset_index(drop=True)

# Show Day banner
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
        chg   = row[chg_key]
        up    = chg >  0.5
        dn    = chg < -0.5
        clr   = "#10b981" if up else ("#ef4444" if dn else "#64748b")
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

# Export + settings
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
    if st.button("🗑️  Vider cache & tout recharger"):
        st.session_state.all_cards=[]; st.session_state.loading_done=False
        st.session_state.set_names=[]; fetch_pokemon_sets.clear(); fetch_set_cards.clear()
        if os.path.exists(CACHE_FILE): os.remove(CACHE_FILE)
        st.rerun()
