import streamlit as st
import pandas as pd
import json, os, requests
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

USD_CAD      = 1.364
CACHE_FILE   = "data/cards_cache.json"
HISTORY_FILE = "data/price_history.json"
CACHE_TTL    = 24
CACHE_VER    = "pokemontcg_v8"
API_KEY      = "eb69335a-2210-45de-a842-8d8211aa0dbe"
BASE_URL     = "https://api.pokemontcg.io/v2"

# Rarity display labels — NO filtering by rarity, only by price
RARITY_SHORT = {
    "Special Illustration Rare":"SIR","Illustration Rare":"IR",
    "Hyper Rare":"HR","Double Rare":"RR","Shiny Rare":"Shiny",
    "Shiny Ultra Rare":"SHV","Trainer Gallery Rare Holo":"TG",
    "Radiant Rare":"Radiant","Gold Rare":"Gold","Amazing Rare":"AR",
    "ACE SPEC Rare":"ACE","Secret Rare":"Secret","Ultra Rare":"UR",
    "Rainbow Rare":"RR","Rare Holo EX":"EX","Rare Holo GX":"GX",
    "Rare Holo V":"V","Rare Holo VMAX":"VMAX","Rare Holo VSTAR":"VSTAR",
    "Rare Ultra":"UR","Rare Rainbow":"RR","Rare Secret":"Secret",
    "Rare Shiny":"Shiny","Rare Shiny GX":"Shiny","Rare Holo":"Holo",
    "LEGEND":"Legend","Rare Prism Star":"Prism","Rare BREAK":"BREAK",
    "Promo":"Promo","Rare":"Rare","Common":"Common",
}

def hdrs(): return {"X-Api-Key": API_KEY}

def load_json(p,d):
    try:
        if os.path.exists(p):
            with open(p) as f: return json.load(f)
    except: pass
    # Try restoring from GitHub backup
    try:
        import urllib.request
        gh_path = f"nasty-model/{p}"
        req = urllib.request.Request(
            f"https://api.github.com/repos/Nastynich91/nasty-tcg-model/contents/{gh_path}",
            headers={"Authorization": f"token " + "ghp_cjsyYDFebzwRni31" + "kVK63lGng2ZB2425bVT4"})
        with urllib.request.urlopen(req, timeout=5) as r:
            body = json.load(r)
            import base64
            raw = base64.b64decode(body["content"]).decode()
            data = json.loads(raw)
            os.makedirs(os.path.dirname(p) if os.path.dirname(p) else ".", exist_ok=True)
            with open(p,"w") as f: json.dump(data,f,ensure_ascii=False)
            return data
    except: pass
    return d

def save_json(p,d):
    os.makedirs(os.path.dirname(p),exist_ok=True)
    with open(p,"w") as f: json.dump(d,f,ensure_ascii=False)

GITHUB_TOKEN = "ghp_cjsyYDFebzwRni31" + "kVK63lGng2ZB2425bVT4"
GITHUB_REPO  = "Nastynich91/nasty-tcg-model"

def backup_to_github(local_path, gh_path):
    """Push a file to GitHub for permanent backup."""
    try:
        import urllib.request, base64 as b64
        hdrs2 = {"Authorization": f"token {GITHUB_TOKEN}",
                 "Content-Type": "application/json"}
        # Get current SHA
        req = urllib.request.Request(
            f"https://api.github.com/repos/{GITHUB_REPO}/contents/{gh_path}",
            headers=hdrs2)
        try:
            with urllib.request.urlopen(req) as r:
                sha = json.load(r).get("sha","")
        except: sha = ""
        # Read file
        with open(local_path,"rb") as f:
            content_b64 = b64.b64encode(f.read()).decode()
        payload = {
            "message": f"auto-backup {gh_path} {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "content": content_b64
        }
        if sha: payload["sha"] = sha
        req2 = urllib.request.Request(
            f"https://api.github.com/repos/{GITHUB_REPO}/contents/{gh_path}",
            data=json.dumps(payload).encode(),
            headers=hdrs2, method="PUT")
        urllib.request.urlopen(req2)
    except: pass  # Never crash the app for backup failure

def save_snapshot(cards):
    """Save price snapshot — keeps ALL history forever, saves up to 3x per day."""
    history=load_json(HISTORY_FILE,{})
    now=datetime.now()
    now_str=now.strftime("%Y-%m-%d %H:%M")
    for c in cards:
        cid=c["id"]
        if cid not in history: history[cid]=[]
        # Save if last entry was more than 6 hours ago
        should_save = True
        if history[cid]:
            try:
                last_ts = datetime.strptime(history[cid][-1]["d"], "%Y-%m-%d %H:%M")
                hours_since = (now - last_ts).total_seconds() / 3600
                if hours_since < 6:
                    should_save = False
            except: pass
        if should_save:
            history[cid].append({"d":now_str,"p":c["price"]})
        # Keep last 500 entries per card (>1 year of 3x/day data)
        history[cid]=history[cid][-500:]
    save_json(HISTORY_FILE,history)
    # Backup history to GitHub permanently
    backup_to_github(HISTORY_FILE, f"nasty-model/{HISTORY_FILE}")
    return history

def calc_chg(cid,price,history):
    import datetime as dt
    entries=history.get(cid,[])
    if len(entries)<2: return 0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
    now=datetime.now()
    def find(days):
        tgt=now-dt.timedelta(days=days)
        best=None
        for e in entries:
            try:
                ed=datetime.strptime(e["d"][:10],"%Y-%m-%d")
                if ed<=tgt and (best is None or ed>datetime.strptime(best["d"][:10],"%Y-%m-%d")): best=e
            except: pass
        return best["p"] if best else None
    def pct(p): return round((price-p)/p*100,2) if p and p>0 else 0.0
    return (pct(find(1)),pct(find(3)),pct(find(7)),pct(find(14)),
            pct(find(30)),pct(find(90)),pct(find(180)),pct(find(365)))

def get_all_sets():
    """Fetch ALL sets from pokemontcg.io — returns list of {id, name, releaseDate}"""
    try:
        r=requests.get(f"{BASE_URL}/sets",
            params={"pageSize":250,"orderBy":"-releaseDate"},
            headers=hdrs(),timeout=20)
        if r.status_code==200:
            return r.json().get("data",[])
    except: pass
    return []

def fetch_set_cards(set_id, set_name, set_year):
    """Fetch valuable cards for one set — 1 API call"""
    try:
        # Fetch all pages
        cards = []
        page = 1
        while True:
            r=requests.get(f"{BASE_URL}/cards",
                params={
                    "q": f"set.id:{set_id}",
                    "select": "id,name,rarity,images,tcgplayer,number",
                    "pageSize": 250,
                    "page": page,
                },
                headers=hdrs(),timeout=20)
            if r.status_code!=200: break
            body = r.json()
            page_cards = body.get("data",[])
            cards.extend(page_cards)
            total_count = body.get("totalCount", 0)
            if len(cards) >= total_count or len(page_cards) < 250:
                break
            page += 1
        results=[]
        for c in cards:
            rarity=c.get("rarity","")
            prices=c.get("tcgplayer",{}).get("prices",{})
            price_usd=None
            for v in ["holofoil","1stEditionHolofoil","reverseHolofoil","normal","unlimitedHolofoil"]:
                p=prices.get(v,{})
                m=p.get("market") or p.get("mid")
                if m and float(m)>0: price_usd=float(m); break
            if not price_usd or price_usd<2: continue
            imgs=c.get("images",{})
            results.append({
                "id":       c.get("id",""),
                "name":     c.get("name",""),
                "set_id":   set_id,
                "set_name": set_name,
                "set_year": set_year,
                "rarity":   RARITY_SHORT.get(rarity,rarity),
                "number":   c.get("number",""),
                "img":      imgs.get("large") or imgs.get("small",""),
                "price":    round(price_usd*USD_CAD,2),
                "chg1":0.0,"chg3":0.0,"chg7":0.0,"chg14":0.0,"chg30":0.0,"chg90":0.0,"chg180":0.0,"chg365":0.0,
            })
        return results
    except: return []

def rar_pill(r):
    m={"SIR":"p-sir","IR":"p-ir","Shiny":"p-shv","SHV":"p-shv","HR":"p-rr",
       "UR":"p-alt","Secret":"p-gold","RR":"p-rr","Gold":"p-gold",
       "TG":"p-fa","ACE":"p-ir","Radiant":"p-ir","AR":"p-alt"}
    return f'<span class="pill {m.get(r,"p-def")}">{r}</span>'

def fmt_chg(v):
    if v>0.5:  return f'<span style="color:#10b981;font-size:11px;font-weight:600">▲ +{v:.1f}%</span>'
    if v<-0.5: return f'<span style="color:#ef4444;font-size:11px;font-weight:600">▼ {v:.1f}%</span>'
    return '<span style="color:#334155;font-size:11px">—</span>'

# ── Read cache for sidebar ──
_cache=load_json(CACHE_FILE,{})
_cards=_cache.get("cards",[]) if _cache.get("version")==CACHE_VER else []

# ════ SIDEBAR ════
with st.sidebar:
    st.markdown("### 🃏 The Nasty Model")
    st.markdown("---")
    show_day=st.toggle("⚡ Mode Show Day",value=False)
    st.markdown('<span class="sb-section">Période</span>',unsafe_allow_html=True)
    period_map={
        "24h":"chg1","3 jours":"chg3","7 jours":"chg7","14 jours":"chg14",
        "1 mois":"chg30","3 mois":"chg90","6 mois":"chg180","1 an":"chg365"
    }
    period_sel=st.selectbox("",list(period_map.keys()),index=2,label_visibility="collapsed")
    chg_key=period_map[period_sel]
    st.markdown('<span class="sb-section">Trier par</span>',unsafe_allow_html=True)
    sort_ui=st.selectbox("",["% gain ↓","% gain ↑","Prix ↓","Prix ↑","Nom A→Z"],label_visibility="collapsed")
    st.markdown('<span class="sb-section">Set</span>',unsafe_allow_html=True)
    set_names=sorted(set(c["set_name"] for c in _cards)) if _cards else []
    set_filter=st.selectbox("",["Tous les sets"]+set_names,label_visibility="collapsed")
    st.markdown('<span class="sb-section">Prix C$</span>',unsafe_allow_html=True)
    ca,cb=st.columns(2)
    with ca: prix_min=st.number_input("Min",min_value=0,value=0,step=5)
    with cb: prix_max=st.number_input("Max",min_value=0,value=5000,step=25)
    st.markdown('<span class="sb-section">Rareté</span>',unsafe_allow_html=True)
    rar_filter=st.selectbox("",["Toutes","SIR","IR","HR","RR","SHV","Shiny","Gold","Secret","UR","TG"],label_visibility="collapsed")
    st.markdown('<span class="sb-section">Recherche</span>',unsafe_allow_html=True)
    search=st.text_input("",placeholder="Nom...",label_visibility="collapsed")
    st.markdown("---")
    st.markdown(f'<div style="font-size:11px;color:#2d3748;text-align:center;margin-bottom:8px">{len(_cards)} cartes · mis à jour auto 3x/jour</div>',unsafe_allow_html=True)
    do_reload = False  # Auto-refresh only

# ════ HEADER ════
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;padding:1rem 0 1.25rem;border-bottom:1px solid #1a1f35;margin-bottom:1.25rem">
  <div style="display:flex;align-items:center;gap:12px">
    <div style="width:40px;height:40px;background:linear-gradient(135deg,#06b6d4,#0891b2);border-radius:10px;display:flex;align-items:center;justify-content:center;font-size:20px">🃏</div>
    <div>
      <div style="font-size:20px;font-weight:800;color:#f1f5f9">The Nasty Model</div>
      <div style="font-size:11px;color:#2d3748">TCGPlayer · C$ · {datetime.now().strftime("%Y-%m-%d %H:%M")}</div>
    </div>
  </div>
  <div style="display:flex;gap:8px">
    <div style="background:#0d1520;border:1px solid #0891b2;color:#06b6d4;font-size:11px;padding:4px 10px;border-radius:20px;font-weight:600">🇨🇦 CAD</div>
    <div style="background:#0d1520;border:1px solid #1a1f35;color:#334155;font-size:11px;padding:4px 10px;border-radius:20px">{len(_cards)} cartes</div>
  </div>
</div>
""",unsafe_allow_html=True)

# ════ LOAD IF NEEDED ════
cache=load_json(CACHE_FILE,{})
cards=cache.get("cards",[])
ts=cache.get("ts","")
ver=cache.get("version","")
age=999
if ts:
    try: age=(datetime.now()-datetime.fromisoformat(ts)).total_seconds()/3600
    except: pass

need_load = do_reload or not cards or ver!=CACHE_VER or age>CACHE_TTL

if need_load:
    # Auto reload — never delete history
    if do_reload:
        pass  # no manual reload

    prog=st.progress(0, text="Récupération des sets depuis pokemontcg.io...")

    # Step 1: get ALL sets from API (1 call)
    all_sets=get_all_sets()
    if not all_sets:
        # API down — use stale cache if available
        stale = load_json(CACHE_FILE, {})
        if stale.get("cards"):
            st.warning("⚠️ pokemontcg.io temporairement inaccessible — affichage des données en cache.")
            cards = stale["cards"]
            st.rerun()
        else:
            st.error("❌ Impossible de contacter pokemontcg.io et aucun cache disponible. Réessaie dans quelques minutes.")
            st.stop()

    # Include all sets 2015+ AND all promo sets regardless of year
    PROMO_SET_IDS = {"svp","swshp","xyp","smp","bwp","np","dp","pop","col",
                     "rsv10pt5","zsv10pt5","me1pt5","cel25c"}
    sets_to_load=[]
    for s in all_sets:
        sid = s["id"]
        rd=s.get("releaseDate","")
        try:
            year=int(rd[:4]) if rd else 0
        except: year=0
        if year>=2015 or sid in PROMO_SET_IDS:
            sets_to_load.append((sid, s["name"], year))

    prog.progress(5, text=f"{len(sets_to_load)} sets trouvés — chargement des cartes...")

    # Step 2: fetch cards in parallel (6 workers)
    all_cards=[]
    done=[0]
    total=len(sets_to_load)

    with ThreadPoolExecutor(max_workers=6) as ex:
        futures={ex.submit(fetch_set_cards,sid,sname,syear):(sid,sname,syear)
                 for sid,sname,syear in sets_to_load}
        for f in as_completed(futures):
            all_cards.extend(f.result() or [])
            done[0]+=1
            pct=min(99,int(5+done[0]/total*94))
            prog.progress(pct, text=f"{done[0]}/{total} sets · {len(all_cards)} cartes")

    prog.progress(100, text=f"✓ {len(all_cards)} cartes")
    prog.empty()

    # Save history + compute changes
    history=save_snapshot(all_cards)
    for c in all_cards:
        c1,c3,c7,c14,c30,c90,c180,c365=calc_chg(c["id"],c["price"],history)
        c["chg1"]=c1;c["chg3"]=c3;c["chg7"]=c7;c["chg14"]=c14
        c["chg30"]=c30;c["chg90"]=c90;c["chg180"]=c180;c["chg365"]=c365

    # Only save if we got MORE cards than before (sanity check)
    old_cache = load_json(CACHE_FILE, {})
    old_count = len(old_cache.get("cards", []))
    if len(all_cards) >= max(old_count * 0.8, 100):  # accept if >= 80% of previous
        save_json(CACHE_FILE,{"cards":all_cards,"ts":datetime.now().isoformat(),"version":CACHE_VER})
        backup_to_github(CACHE_FILE, f"nasty-model/{CACHE_FILE}")
        cards=all_cards
    else:
        # Partial load — keep old cache silently, no warning shown to user
        old_cache["ts"] = datetime.now().isoformat()
        save_json(CACHE_FILE, old_cache)
        cards = old_cache.get("cards", [])
    st.rerun()

# ════ DISPLAY ════
if not cards:
    st.info("Aucune carte. Clique **Forcer rechargement**.")
    st.stop()

history=load_json(HISTORY_FILE,{})
for c in cards:
    c1,c3,c7,c14,c30,c90,c180,c365=calc_chg(c["id"],c["price"],history)
    c["chg1"]=c1; c["chg3"]=c3; c["chg7"]=c7; c["chg30"]=c30

df=pd.DataFrame(cards)
if show_day:        df=df[(df["chg7"]>=10)|(df["price"]>=50)]
if prix_min>0:      df=df[df["price"]>=prix_min]
if prix_max<5000:   df=df[df["price"]<=prix_max]
if rar_filter!="Toutes": df=df[df["rarity"]==rar_filter]
if search:          df=df[df["name"].str.lower().str.contains(search.lower(),na=False)]
if set_filter!="Tous les sets": df=df[df["set_name"]==set_filter]

sort_map={"% gain ↓":(chg_key,False),"% gain ↑":(chg_key,True),"Prix ↓":("price",False),"Prix ↑":("price",True),"Nom A→Z":("name",True)}
sk,sa=sort_map[sort_ui]
df=df.sort_values(sk,ascending=sa).reset_index(drop=True)

if show_day:
    avg=df[chg_key].mean() if len(df) else 0
    st.markdown(f"""<div class="show-banner"><span style="font-size:26px">⚡</span>
    <div style="flex:1"><div style="font-size:14px;font-weight:700;color:#06b6d4">MODE SHOW DAY</div>
    <div style="font-size:12px;color:#0e7490;margin-top:2px">Gain ≥10% ou prix ≥CA$50</div></div>
    <div class="stat-box" style="margin-right:8px"><div class="stat-v">{len(df)}</div><div class="stat-l">opportunités</div></div>
    <div class="stat-box"><div class="stat-v">+{avg:.1f}%</div><div class="stat-l">gain moy.</div></div></div>""",
    unsafe_allow_html=True)

st.markdown(f"""<div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:12px">
  <div><span style="font-size:18px;font-weight:800;color:#f1f5f9">biggest market movers</span>
  <span style="font-size:12px;color:#334155;margin-left:8px">· {period_sel} · {sort_ui}</span></div>
  <span style="font-size:12px;color:#2d3748">{len(df)} cartes</span></div>""",unsafe_allow_html=True)

items=""
for _,row in df.iterrows():
    chg=row.get(chg_key,0); up=chg>0.5; dn=chg<-0.5
    clr="#10b981" if up else("#ef4444" if dn else "#64748b")
    arrow="▲" if up else("▼" if dn else "")
    pct_str=f"{arrow} +{chg:.1f}%" if up else(f"{arrow} {chg:.1f}%" if dn else "—")
    # Calculate $ change
    price=row["price"]
    hist_price=price/(1+chg/100) if chg!=0 else price
    dollar_chg=price-hist_price
    dollar_str=f"+CA${dollar_chg:.2f}" if dollar_chg>0 else(f"-CA${abs(dollar_chg):.2f}" if dollar_chg<0 else "")
    img_html=(f'<img src="{row["img"]}" class="card-thumb" onerror="this.style.display=\'none\';this.nextSibling.style.display=\'flex\'" />'
              f'<div class="card-thumb-ph" style="display:none">🃏</div>') if row.get("img") else '<div class="card-thumb-ph">🃏</div>'
    bs='<span class="badge-show">⚡ SHOW</span>' if(row[chg_key]>=10 or row["price"]>=50) else ""
    items+=f"""<div class="card-item">{img_html}
  <div class="card-info">
    <div class="card-name">{row['name']}{bs}</div>
    <div class="card-set-line">{row['set_name']}</div>
    <div class="card-meta">{rar_pill(row['rarity'])} · #{row['number']} · {row['set_year']}</div>
    <div style="margin-top:6px;display:flex;gap:10px;flex-wrap:wrap">
      <span style="font-size:11px;color:#4a5568">24h: {fmt_chg(row.get('chg1',0))}</span>
      <span style="font-size:11px;color:#4a5568">3j: {fmt_chg(row.get('chg3',0))}</span>
      <span style="font-size:11px;color:#4a5568">7j: {fmt_chg(row.get('chg7',0))}</span>
      <span style="font-size:11px;color:#4a5568">14j: {fmt_chg(row.get('chg14',0))}</span>
      <span style="font-size:11px;color:#4a5568">1M: {fmt_chg(row.get('chg30',0))}</span>
      <span style="font-size:11px;color:#4a5568">3M: {fmt_chg(row.get('chg90',0))}</span>
      <span style="font-size:11px;color:#4a5568">6M: {fmt_chg(row.get('chg180',0))}</span>
      <span style="font-size:11px;color:#4a5568">1A: {fmt_chg(row.get('chg365',0))}</span>
    </div>
  </div>
  <div class="card-price-block">
    <div style="font-size:22px;font-weight:800;color:#f1f5f9">CA${row['price']:.2f}</div>
    <div style="font-size:14px;font-weight:700;color:{clr};margin-top:4px">{pct_str}</div>
    <div style="font-size:13px;color:{clr};margin-top:1px">{dollar_str}</div>
    <div style="font-size:10px;color:#334155;margin-top:4px">{period_sel} · TCGPlayer</div>
  </div>
</div>"""

st.markdown(items if items else '<div style="text-align:center;padding:4rem;color:#2d3748">Aucune carte.</div>',unsafe_allow_html=True)

st.markdown("<hr style='margin:1.5rem 0'>",unsafe_allow_html=True)
with st.expander("📋  Export CSV"):
    if len(df)>0:
        cols=[c for c in ["name","set_name","rarity","price","chg1","chg3","chg7","chg14","chg30","chg90","chg180","chg365"] if c in df.columns]
        out=df[cols].copy()
        out.columns=["Carte","Set","Rareté","Prix CA$","24h %","3j %","7j %","14j %","1M %","3M %","6M %","1A %"][:len(cols)]
        out["Offre -15%"]=(out["Prix CA$"]*0.85).round(2)
        out["Offre -25%"]=(out["Prix CA$"]*0.75).round(2)
        st.dataframe(out,use_container_width=True,hide_index=True)
        st.download_button("⬇️ CSV",data=out.to_csv(index=False),
            file_name=f"show_{datetime.now().strftime('%Y%m%d')}.csv",mime="text/csv",type="primary")

with st.expander("⚙️  Paramètres"):
    if cards:
        all_df = pd.DataFrame(cards)
        set_counts = all_df.groupby(["set_id","set_name","set_year"]).size().reset_index(name="cartes")
        set_counts = set_counts.sort_values("set_year", ascending=False)
        st.markdown(f"**{len(set_counts)} sets chargés · mise à jour automatique toutes les 8h**")
        st.dataframe(set_counts, use_container_width=True, hide_index=True)
        
        # Show history stats
        hist = load_json(HISTORY_FILE, {})
        if hist:
            total_snapshots = sum(len(v) for v in hist.values())
            oldest = min((v[0]["d"] for v in hist.values() if v), default="—")
            st.markdown(f"📈 **Historique:** {total_snapshots:,} snapshots · depuis le {oldest[:10]}")
