# RetainIQ — Frontend

Plateforme SaaS de rétention client. Frontend React 18 + Vite + Tailwind branché sur l'API FastAPI du projet (`/predict`, `/health`, `/model-info`).

## Démarrage

```bash
cd frontend
npm install
npm run dev
```

L'application est ensuite disponible sur http://localhost:5173

## Variable d'environnement

Créez un fichier `.env` (ou `.env.local`) à la racine de `frontend/` :

```
VITE_API_URL=http://localhost:8000
```

Valeur par défaut : `http://localhost:8000`.

## Proxy de développement (CORS)

Le backend FastAPI autorise déjà toutes les origines (`allow_origins=["*"]`), donc aucun proxy n'est nécessaire en dev. Un proxy `/api → VITE_API_URL` est néanmoins configuré dans `vite.config.js` si vous souhaitez router les appels via le serveur Vite (utile derrière un reverse proxy ou pour contourner un blocage CORS futur). Dans ce cas, modifiez `src/api/client.js` pour pointer la `baseURL` sur `/api`.

## Stack

- React 18 + Vite 5
- React Router 6
- Tailwind CSS 3
- Recharts
- Axios
- Lucide React

## Structure

```
frontend/
├── src/
│   ├── api/client.js              # axios instance + predict / health / model-info
│   ├── components/
│   │   ├── layout/                # Sidebar, Layout
│   │   ├── overview/              # KPI bar + 5 charts
│   │   ├── simulation/            # Wizard 3 étapes + ResultPanel + RiskGauge
│   │   └── ui/                    # Card, Button, Badge, Input, Select, Slider, ToggleGroup
│   ├── hooks/useApiHealth.js      # polling /health toutes les 30 s
│   ├── pages/Overview.jsx         # /
│   ├── pages/Simulation.jsx       # /simulation
│   ├── App.jsx
│   └── main.jsx
├── index.html
├── tailwind.config.js
├── postcss.config.js
└── vite.config.js
```

## Pages

- **/** — Vue d'ensemble : 4 KPI + 5 graphiques (données mockées en dur).
- **/simulation** — Wizard 3 étapes (Profil & contrat / Engagement / Support & finances) avec panneau résultat sticky : jauge semi-circulaire, badge de niveau de risque, revenu exposé, facteurs déclenchants calculés côté frontend.

## Notes

- L'interface est en français, libellés orientés métier (aucun terme ML).
- Responsive desktop uniquement (min-width 1280px).
- Indicateur de statut API (point vert / rouge) en bas de la sidebar, rafraîchi toutes les 30 s.
- Erreurs `500` / `503` du `/predict` affichent un message clair dans le panneau résultat.
