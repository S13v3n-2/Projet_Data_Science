# Retention Client et Risque de Revenus -- M1 Data Engineering

Projet de groupe M1 DE -- Carlot Steven  
Tutrice : Sarah MALAEB

Prediction du churn client sur 10 000 observations (dataset Kaggle). Quatre modeles de
classification, un modele de regression revenue, une API FastAPI, un dashboard React et
un tracking MLflow complet.

---

## Demarrage

```bash
docker compose up -d
```

| Service    | URL                        |
|------------|----------------------------|
| Dashboard  | http://localhost:80         |
| API        | http://localhost:8000/docs  |
| MLflow UI  | http://localhost:5000       |
| PostgreSQL | localhost:5432              |

---

## Notebooks -- ordre d'execution

Activer l'environnement local avant de lancer Jupyter :

```bash
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS
jupyter lab notebooks/
```

| Notebook | Contenu |
|----------|---------|
| 01_exploration | EDA, distributions, correlations |
| 02_preprocessing | Pipeline sklearn, feature engineering, split 80/20 |
| 03_logistic_regression | Baseline, seuil optimal F1 = 0.5645 |
| 04_random_forest | **Modele champion**, seuil optimise = 0.3780 |
| 05_xgboost | XGBoost base + tuned (RandomizedSearchCV), seuil = 0.50 |
| 06_mlp_classification | MLP PyTorch + Focal Loss, seuil = 0.2874 |
| 07_regression_revenue | Regression revenu a risque (Ridge, RF, XGB, MLP) |
| 08_model_comparison | Comparaison, SHAP, permutation importance, eco-score |

---

## Resultats des modeles

Metriques au seuil optimise pour le recall :

| Modele | AUC-ROC | Seuil | Recall churn | F1 churn |
|--------|---------|-------|--------------|----------|
| Random Forest (champion) | 0.8093 | 0.3780 | 0.642 | 0.404 |
| XGBoost tuned | 0.8142 | 0.50 | 0.828 | 0.376 |
| MLP PyTorch | 0.7492 | 0.2874 | 0.593 | 0.342 |
| Logistic Regression | 0.7245 | 0.5645 | 0.588 | 0.320 |

Le Random Forest est selectionne comme modele de production pour sa stabilite en
validation croisee (CV 5 plis : 0.800 +/- 0.015) et sa reproductibilite sans tuning.

---

## API -- endpoints

Documentation interactive disponible sur http://localhost:8000/docs

### POST /predict

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "tenure_months": 3,
    "contract_type": "Monthly",
    "customer_segment": "Standard",
    "monthly_logins": 2,
    "weekly_active_days": 1,
    "avg_session_time": 15.0,
    "features_used": 3,
    "usage_growth_rate": -0.3,
    "last_login_days_ago": 20,
    "monthly_fee": 200.0,
    "total_revenue": 2000.0,
    "payment_method": "Credit Card",
    "payment_failures": 3,
    "support_tickets": 5,
    "avg_resolution_time": 72.0,
    "csat_score": 1,
    "escalations": 2,
    "email_open_rate": 0.05,
    "marketing_click_rate": 0.01,
    "nps_score": -30,
    "referral_count": 0,
    "gender": "Female",
    "complaint_type": "Technical"
  }'
```

```json
{
  "churn_probability": 0.847,
  "churn_prediction": 1,
  "risk_level": "Eleve",
  "revenue_at_risk": 1694.0,
  "model_name": "random_forest"
}
```

### GET /clients-at-risk

Scoring batch de tous les clients avec filtres et pagination.

```bash
curl "http://localhost:8000/clients-at-risk?min_prob=0.7&segment=Premium&page=1"
```

### GET /clients-at-risk/export

Telechargement CSV du resultat filtre (StreamingResponse, sans ecriture disque).

```bash
curl "http://localhost:8000/clients-at-risk/export?min_prob=0.5" -o clients.csv
```

### Autres endpoints

| Endpoint | Description |
|----------|-------------|
| GET /health | Etat du service et du modele charge |
| GET /model-info | Nom, version, metriques du modele en production |
| GET /stats | Statistiques agregees pour le dashboard Overview |

---

## Structure du projet

```
Projet_Data_Science/
|-- api/
|   |-- main.py             # FastAPI, lifespan, endpoints
|   |-- model_loader.py     # Chargement avec fallback 3 niveaux
|   |-- stats.py            # compute_stats(), get_clients_at_risk()
|-- data/
|   |-- raw/                # Dataset Kaggle (CSV, non versionne)
|   |-- processed/          # Modeles .joblib, figures, seuils JSON
|-- frontend/               # React 18 + Vite + Tailwind + Recharts
|-- notebooks/              # 01 a 08, un par etape
|-- src/
|   |-- data/               # loader.py, preprocessor.py
|   |-- models/             # mlflow_utils.py
|   |-- evaluation/         # metrics.py
|-- docker-compose.yml
|-- requirements.txt
|-- justification.md        # Justifications techniques detaillees
```

---

## Installation locale (hors Docker)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Dependances principales : `scikit-learn`, `xgboost`, `torch`, `mlflow`, `fastapi`,
`shap`, `pandas`, `matplotlib`.
