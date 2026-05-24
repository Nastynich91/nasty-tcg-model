# 🃏 The Nasty Model

Screener TCG Pokémon · Top movers · NPS upside · Valeurs en C$

## Déploiement en 3 étapes

### 1. Créer le repo GitHub
1. Va sur [github.com/new](https://github.com/new)
2. Nom du repo : `nasty-model`
3. Public ✅ → **Create repository**
4. Upload tous les fichiers de ce dossier (drag & drop)

### 2. Déployer sur Streamlit Cloud (gratuit)
1. Va sur [share.streamlit.io](https://share.streamlit.io)
2. Connecte ton compte GitHub
3. Clique **New app**
4. Repo : `ton-username/nasty-model`
5. Branch : `main`
6. Main file : `app.py`
7. Clique **Deploy** → ton app est live en 2 minutes ✅

### 3. URL finale
`https://nasty-model-XXXXXXX.streamlit.app`

---

## Structure des fichiers
```
nasty-model/
├── app.py              # App principale
├── requirements.txt    # Dépendances Python
├── .streamlit/
│   └── config.toml     # Thème dark
├── data/
│   └── cards.json      # Base de données (auto-créée)
└── README.md
```

## Ajouter des cartes
- **Manuellement** : section "Ajouter une carte" dans l'app
- **Import CSV** : format `id, name, set, rarity, tier, price, p7, p30, sat, arb`

## NPS — Nasty Potential Score
Score 0–100 calculé sur 10 variables :
| Variable | Poids |
|----------|-------|
| Print Status (OOP) | 25% |
| PSA10 Saturation | 20% |
| JP/EN Arbitrage | 18% |
| Market Velocity | 15% |
| Icon Tier | 12% |
| Reprint Risk | 10% |
| Price Stability | 8% |
| Whale Activity | 6% |
| Cross-Media | 5% |
| Social Volume | 4% |
