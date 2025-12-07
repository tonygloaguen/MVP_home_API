# HomeDash – Dashboard domestique TV-friendly (FastAPI + SQLite)

HomeDash est un **tableau de bord domestique** affichable sur une TV ou un navigateur, développé en **FastAPI**.

L’objectif : regrouper sur **une seule page lisible à plusieurs mètres** les informations utiles du quotidien :

- 🌡️ Météo locale
- 🌅 Éphémérides (lever / coucher du soleil, durée du jour)
- 📰 Infos régionales via flux RSS
- (À venir) 🚌 Transports / bus, 🟠 alertes météo, etc.

Ce projet sert à la fois de **dashboard perso** et de **projet full stack** pour GitHub (backend + frontend + persistance).

---

## ✨ Fonctionnalités

### MVP actuel

- **Backend FastAPI**
  - Endpoints `/api/weather`, `/api/ephemerides`, `/api/news`, `/api/dashboard`
  - Intégration d’API externes :
    - OpenWeatherMap (météo)
    - sunrise-sunset.org (éphémérides)
    - Flux RSS configurable (news)
- **Stockage en base**
  - Base **SQLite** (simple à déployer, fichier unique)
  - Historisation :
    - `WeatherSnapshot` (météo)
    - `Ephemerides`
    - `RegionalNews`
- **Dashboard HTML “TV-friendly”**
  - Une seule page `/` :
    - gros textes
    - contraste élevé
    - mise en page optimisée pour TV ou grand écran
  - Rafraîchissement automatique via `/api/dashboard` (JavaScript)

### Roadmap (idées d’évolution)

- 🚌 Bloc **Transports / bus** (API locale ou GTFS)
- ⚠️ Bloc **Alertes météo / vigilance**
- 🧱 Système de **widgets modulaires** (activer/désactiver des sections)
- 👤 Page /admin pour la configuration (ville, région, flux RSS, etc.)
- 🐳 Dockerisation complète (image prête à déployer sur un Raspberry Pi / NAS)

---

## 🧱 Stack technique

- **Backend :** FastAPI (Python)
- **Modèles / ORM :** SQLModel (SQLite)
- **Validation :** Pydantic v2
- **Config :** pydantic-settings + `.env`
- **Frontend :**
  - Templates Jinja2 (`index.html`, `base.html`)
  - CSS custom (sans framework lourd)
  - JavaScript vanilla (`dashboard.js`) pour consommer `/api/dashboard`
- **Base de données :** SQLite (fichier `homedash.db`)

---

## 📁 Structure du projet

```text
.
├─ app/
│  ├─ main.py           # point d'entrée FastAPI
│  ├─ config.py         # gestion de la configuration (.env)
│  ├─ db.py             # moteur SQLModel + init DB
│  │
│  ├─ models/           # modèles ORM (SQLModel)
│  │  ├─ weather.py
│  │  ├─ ephemerides.py
│  │  └─ news.py
│  │
│  ├─ schemas/          # schémas Pydantic (I/O API)
│  │  ├─ weather.py
│  │  ├─ ephemerides.py
│  │  └─ news.py
│  │
│  ├─ services/         # logique métier + appels aux APIs externes
│  │  ├─ weather_service.py
│  │  ├─ ephemerides_service.py
│  │  └─ news_service.py
│  │
│  ├─ routers/          # routes FastAPI (endpoints REST)
│  │  ├─ weather.py
│  │  ├─ ephemerides.py
│  │  ├─ news.py
│  │  └─ dashboard.py
│  │
│  ├─ templates/        # frontend (Jinja2)
│  │  ├─ base.html
│  │  └─ index.html
│  │
│  └─ static/           # assets statiques (CSS / JS / images)
│     ├─ css/
│     │  └─ style.css
│     └─ js/
│        └─ dashboard.js
│
├─ .env.example         # exemple de configuration
├─ requirements.txt     # dépendances Python
├─ .gitignore
└─ README.md
