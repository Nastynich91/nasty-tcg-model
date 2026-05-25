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
EUR_CAD      = 1.55
CACHE_FILE   = "data/cards_cache.json"
HISTORY_FILE = "data/price_history.json"
CACHE_TTL    = 12
CACHE_VER    = "rapi2"
RAPI_KEY     = "2cc08eea61msh3a7f590a8538bb3p1ddae6jsn6b129d847fd4"
RAPI_HOST    = "pokemon-tcg-api.p.rapidapi.com"
BASE_URL     = f"https://{RAPI_HOST}"

RARITY_SHORT = {
    "Special Illustration Rare":"SIR","Illustration Rare":"IR",
    "Hyper Rare":"HR","Double Rare":"RR","Shiny Rare":"Shiny",
    "Shiny Ultra Rare":"SHV","Trainer Gallery Rare Holo":"TG",
    "Radiant Rare":"Radiant","Gold Rare":"Gold","Amazing Rare":"AR",
    "ACE SPEC Rare":"ACE","Secret Rare":"Secret","Ultra Rare":"UR",
    "Rainbow Rare":"RR","Full Art":"FA","Rare Secret":"Secret",
    "Rare Rainbow":"RR","Rare Ultra":"UR","Rare Shiny GX":"Shiny",
    "Rare Shiny":"Shiny",
}
MIN_PRICE_USD = 5.0

def hdrs():
    return {"x-rapidapi-key":RAPI_KEY,"x-rapidapi-host":RAPI_HOST}

def load_json(p,d):
    try:
        if os.path.exists(p):
            with open(p) as f: return json.load(f)
    except: pass
    return d

def save_json(p,d):
    os.makedirs(os.path.dirname(p),exist_ok=True)
    with open(p,"w") as f: json.dump(d,f,ensure_ascii=False)

def save_snapshot(cards):
    history=load_json(HISTORY_FILE,{})
    today=datetime.now().strftime("%Y-%m-%d")
    now_str=datetime.now().strftime("%Y-%m-%d %H:%M")
    for c in cards:
        cid=c["id"]
        if cid not in history: history[cid]=[]
        if today not in [e["d"][:10] for e in history[cid]]:
            history[cid].append({"d":now_str,"p":c["price"]})
        history[cid]=history[cid][-35:]
    save_json(HISTORY_FILE,history)
    return history

def calc_chg(cid,price,history):
    import datetime as dt
    entries=history.get(cid,[])
    if len(entries)<2: return 0.0,0.0,0.0,0.0
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
    return pct(find(1)),pct(find(3)),pct(find(7)),pct(find(30))

def load_all_cards():
    """Main load function — fetches all episodes then all cards."""
    # Step 1: get episodes list
    try:
        r=requests.get(f"{BASE_URL}/episodes",headers=hdrs(),timeout=20)
        if r.status_code!=200:
            return None, f"Episodes API error: HTTP {r.status_code} — {r.text[:300]}"
        episodes=r.json()
        if isinstance(episodes,dict): episodes=episodes.get("data",episodes.get("episodes",[]))
    except Exception as e:
        return None, f"Connection error: {e}"

    # Filter 2016+ only
    eps=[]
    for e in episodes:
        rd=str(e.get("release_date","") or e.get("releaseDate","") or "")
        year=int(rd[:4]) if len(rd)>=4 else 0
        if year>=2016:
            eps.append((e.get("id"),e.get("name",""),year))
    eps.sort(key=lambda x:x[2],reverse=True)

    # Step 2: fetch cards per episode in parallel
    all_cards=[]
    done=[0]

    def fetch_ep(args):
        eid,ename,eyear=args
        try:
            r2=requests.get(f"{BASE_URL}/episodes/{eid}/cards",
                params={"sort":"price_highest"},headers=hdrs(),timeout=20)
            if r2.status_code!=200: return []
            data=r2.json()
            cards=data if isinstance(data,list) else data.get("data",data.get("cards",[]))
            results=[]
            for c in cards:
                prices=c.get("prices",{})
                tcgp=prices.get("tcg_player",{})
                cm=prices.get("cardmarket",{})
                usd=tcgp.get("market_price") or tcgp.get("mid_price")
                cad=None
                if usd and float(usd)>=MIN_PRICE_USD:
                    cad=round(float(usd)*USD_CAD,2)
                elif cm.get("30d_average") and float(cm["30d_average"])>3:
                    cad=round(float(cm["30d_average"])*EUR_CAD,2)
                if not cad: continue
                img=c.get("image","")
                rarity=c.get("rarity","")
                results.append({
                    "id":str(c.get("id","")),
                    "name":c.get("name",""),
                    "set_id":str(eid),
                    "set_name":ename,
                    "set_year":eyear,
                    "rarity":RARITY_SHORT.get(rarity,rarity[:10] if rarity else "—"),
                    "number":str(c.get("card_number",c.get("number",""))),
                    "img":img if img and img.startswith("http") else "",
                    "price":cad,
                    "chg1":0.0,"chg3":0.0,"chg7":0.0,"chg30":0.0,
                })
            return results
        except: return []

    with ThreadPoolExecutor(max_workers=5) as ex:
        futures={ex.submit(fetch_ep,e):e for e in eps}
        for f in as_completed(futures):
            all_cards.extend(f.result() or [])
            done[0]+=1

    return all_cards, None

def rar_pill(r):
    m={"SIR":"p-sir","IR":"p-ir","Shiny":"p-shv","SHV":"p-shv","HR":"p-rr",
       "UR":"p-alt","Secret":"p-gold","RR":"p-rr","Gold":"p-gold",
       "TG":"p-fa","ACE":"p-ir","Radiant":"p-ir","AR":"p-alt","FA":"p-fa"}
    return f'<span class="pill {m.get(r,"p-def")}">{r}</span>'

def fmt_chg(v):
    if v>0.5:  return f'<span style="color:#10b981;font-size:11px;font-weight:600">▲ +{v:.1f}%</span>'
    if v<-0.5: return f'<span style="color:#ef4444;font-size:11px;font-weight:600">▼ {v:.1f}%</span>'
    return '<span style="color:#334155;font-size:11px">—</span>'

# ════ SIDEBAR ════
with st.sidebar:
    st.markdown("### 🃏 The Nasty Model")
    st.markdown("---")
    show_day=st.toggle("⚡ Mode Show Day",value=False)
    st.markdown('<span class="sb-section">Période</span>',unsafe_allow_html=True)
    period_map={"24h":"chg1","3 jours":"chg3","7 jours":"chg7","1 mois":"chg30"}
    period_sel=st.selectbox("",list(period_map.keys()),index=2,label_visibility="collapsed")
    chg_key=period_map[period_sel]
    st.markdown('<span class="sb-section">Trier par</span>',unsafe_allow_html=True)
    sort_ui=st.selectbox("",["Prix ↓","% gain ↓","Prix ↑","Nom A→Z"],label_visibility="collapsed")
    st.markdown('<span class="sb-section">Set</span>',unsafe_allow_html=True)

    # Load set names from cache for sidebar
    _cache=load_json(CACHE_FILE,{})
    _cards=_cache.get("cards",[]) if _cache.get("version")==CACHE_VER else []
    set_names=sorted(set(c["set_name"] for c in _cards)) if _cards else []
    set_filter=st.selectbox("",["Tous les sets"]+set_names,label_visibility="collapsed")

    st.markdown('<span class="sb-section">Prix C$</span>',unsafe_allow_html=True)
    ca,cb=st.columns(2)
    with ca: prix_min=st.number_input("Min",min_value=0,value=0,step=5)
    with cb: prix_max=st.number_input("Max",min_value=0,value=5000,step=25)
    st.markdown('<span class="sb-section">Rareté</span>',unsafe_allow_html=True)
    rar_filter=st.selectbox("",["Toutes","SIR","IR","HR","RR","SHV","Shiny","Gold","FA","Secret","UR","TG"],label_visibility="collapsed")
    st.markdown('<span class="sb-section">Recherche</span>',unsafe_allow_html=True)
    search=st.text_input("",placeholder="Nom...",label_visibility="collapsed")
    st.markdown("---")
    n=len(_cards)
    st.markdown(f'<div style="font-size:11px;color:#2d3748;text-align:center;margin-bottom:8px">{n} cartes · pokemon-api.com</div>',unsafe_allow_html=True)
    do_reload=st.button("🔄  Forcer rechargement",type="primary")

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
    <div style="background:#0d1520;border:1px solid #1a1f35;color:#334155;font-size:11px;padding:4px 10px;border-radius:20px">{n} cartes</div>
  </div>
</div>
""",unsafe_allow_html=True)

# ════ CHECK IF NEED TO LOAD ════
cache=load_json(CACHE_FILE,{})
cards=cache.get("cards",[])
ts=cache.get("ts","")
ver=cache.get("version","")
age=999
if ts:
    try: age=(datetime.now()-datetime.fromisoformat(ts)).total_seconds()/3600
    except: age=999

need_load = do_reload or not cards or ver!=CACHE_VER or age>CACHE_TTL

if need_load:
    if do_reload:
        try: os.remove(CACHE_FILE)
        except: pass

    prog=st.progress(0,text="🔌 Connexion à pokemon-api.com...")
    with st.spinner("Chargement de tous les sets..."):
        all_cards, err = load_all_cards()

    if err:
        st.error(f"❌ Erreur API: {err}")
        st.stop()

    if not all_cards:
        # Debug: show raw API responses
        try:
            r_ep = requests.get(f"{BASE_URL}/episodes", headers=hdrs(), timeout=20)
            st.error(f"❌ Episodes: HTTP {r_ep.status_code}")
            body = r_ep.json()
            eps_list = body if isinstance(body,list) else body.get("data", body.get("episodes",[]))
            st.write(f"**Episodes count:** {len(eps_list)}")
            if eps_list:
                st.write(f"**Premier épisode:** {eps_list[0]}")
                # Try fetching cards for first episode
                eid = eps_list[0].get("id")
                r_c = requests.get(f"{BASE_URL}/episodes/{eid}/cards", headers=hdrs(), timeout=20)
                st.write(f"**Cards for ep {eid}: HTTP {r_c.status_code}**")
                st.code(r_c.text[:500])
        except Exception as e2:
            st.error(f"Debug error: {e2}")
        st.stop()

    prog.progress(90,text="Sauvegarde du cache...")
    history=save_snapshot(all_cards)
    for c in all_cards:
        c1,c3,c7,c30=calc_chg(c["id"],c["price"],history)
        c["chg1"]=c1;c["chg3"]=c3;c["chg7"]=c7;c["chg30"]=c30

    save_json(CACHE_FILE,{"cards":all_cards,"ts":datetime.now().isoformat(),"version":CACHE_VER})
    prog.progress(100,text=f"✓ {len(all_cards)} cartes chargées")
    prog.empty()
    cards=all_cards
    st.rerun()

# ════ DISPLAY ════
if not cards:
    st.info("Aucune carte. Clique **Forcer rechargement**.")
    st.stop()

# Re-apply history changes
history=load_json(HISTORY_FILE,{})
for c in cards:
    c1,c3,c7,c30=calc_chg(c["id"],c["price"],history)
    c["chg1"]=c1;c["chg3"]=c3;c["chg7"]=c7;c["chg30"]=c30

df=pd.DataFrame(cards)
if show_day:        df=df[(df[chg_key]>=10)|(df["price"]>=50)]
if prix_min>0:      df=df[df["price"]>=prix_min]
if prix_max<5000:   df=df[df["price"]<=prix_max]
if rar_filter!="Toutes": df=df[df["rarity"]==rar_filter]
if search:          df=df[df["name"].str.lower().str.contains(search.lower(),na=False)]
if set_filter!="Tous les sets": df=df[df["set_name"]==set_filter]
sort_map={"Prix ↓":("price",False),"% gain ↓":(chg_key,False),"Prix ↑":("price",True),"Nom A→Z":("name",True)}
sk,sa=sort_map[sort_ui]
df=df.sort_values(sk,ascending=sa).reset_index(drop=True)

if show_day:
    avg=df[chg_key].mean() if len(df) else 0
    st.markdown(f"""<div class="show-banner"><span style="font-size:26px">⚡</span>
    <div style="flex:1"><div style="font-size:14px;font-weight:700;color:#06b6d4">MODE SHOW DAY</div>
    <div style="font-size:12px;color:#0e7490;margin-top:2px">Gain ≥10% ou prix ≥CA$50</div></div>
    <div class="stat-box" style="margin-right:8px"><div class="stat-v">{len(df)}</div><div class="stat-l">opportunités</div></div>
    <div class="stat-box"><div class="stat-v">+{avg:.1f}%</div><div class="stat-l">gain moy.</div></div></div>""",unsafe_allow_html=True)

st.markdown(f"""<div style="display:flex;align-items:baseline;justify-content:space-between;margin-bottom:12px">
  <div><span style="font-size:18px;font-weight:800;color:#f1f5f9">biggest market movers</span>
  <span style="font-size:12px;color:#334155;margin-left:8px">· {period_sel} · {sort_ui}</span></div>
  <span style="font-size:12px;color:#2d3748">{len(df)} cartes</span></div>""",unsafe_allow_html=True)

items=""
for _,row in df.iterrows():
    chg=row[chg_key]; up=chg>0.5; dn=chg<-0.5
    clr="#10b981" if up else("#ef4444" if dn else "#64748b")
    pct_str=f"▲ +{chg:.1f}%" if up else(f"▼ {chg:.1f}%" if dn else "—")
    img_html=f'<img src="{row["img"]}" class="card-thumb" onerror="this.style.display=\'none\';this.nextSibling.style.display=\'flex\'" /><div class="card-thumb-ph" style="display:none">🃏</div>' if row.get("img") else '<div class="card-thumb-ph">🃏</div>'
    bs='<span class="badge-show">⚡ SHOW</span>' if(row[chg_key]>=10 or row["price"]>=50) else ""
    items+=f"""<div class="card-item">{img_html}
  <div class="card-info">
    <div class="card-name">{row['name']}{bs}</div>
    <div class="card-set-line">{row['set_name']}</div>
    <div class="card-meta">{rar_pill(row['rarity'])} · #{row['number']} · {row['set_year']}</div>
    <div style="margin-top:6px;display:flex;gap:14px">
      <span style="font-size:11px;color:#4a5568">24h: {fmt_chg(row['chg1'])}</span>
      <span style="font-size:11px;color:#4a5568">7j: {fmt_chg(row['chg7'])}</span>
      <span style="font-size:11px;color:#4a5568">1M: {fmt_chg(row['chg30'])}</span>
    </div>
  </div>
  <div class="card-price-block">
    <div class="price-main">CA${row['price']:.2f}</div>
    <div class="price-change" style="color:{clr}">{pct_str}</div>
    <div class="price-source">TCGPlayer · USD→CAD</div>
  </div>
</div>"""

st.markdown(items if items else '<div style="text-align:center;padding:4rem;color:#2d3748">Aucune carte.</div>',unsafe_allow_html=True)

st.markdown("<hr style='margin:1.5rem 0'>",unsafe_allow_html=True)
with st.expander("📋  Export CSV"):
    if len(df)>0:
        out=df[["name","set_name","rarity","price","chg1","chg7","chg30"]].copy()
        out.columns=["Carte","Set","Rareté","Prix CA$","24h %","7j %","30j %"]
        out["Offre -15%"]=(out["Prix CA$"]*0.85).round(2)
        out["Offre -25%"]=(out["Prix CA$"]*0.75).round(2)
        st.dataframe(out,use_container_width=True,hide_index=True)
        st.download_button("⬇️ CSV",data=out.to_csv(index=False),
            file_name=f"show_{datetime.now().strftime('%Y%m%d')}.csv",mime="text/csv",type="primary")

with st.expander("⚙️  Paramètres"):
    if st.button("🗑️  Vider cache & recharger"):
        try: os.remove(CACHE_FILE)
        except: pass
        st.rerun()
