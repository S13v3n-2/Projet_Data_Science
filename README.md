# Système Intelligent de Rétention Client — M1 Data Engineering

Projet M1 Data Engineering — Sujet 2 : Système multi-modèles pour la prédiction du churn client
et l'évaluation du risque de revenus.

## Architecture

```
Notebooks (local .venv)  →  MLflow (Docker :5000)  →  PostgreSQL (Docker :5432)
                                    ↓
                           API FastAPI (Docker :8000)
                                    ↓
                         Dashboard Streamlit (Docker :8501)
```

## Démarrage rapide

### 1. Lancer l'infrastructure Docker

```bash
docker compose up -d
```

Services démarrés :
- MLflow UI : http://localhost:5000
- API FastAPI : http://localhost:8000
- Dashboard Streamlit : http://localhost:8501

### 2. Exécuter les notebooks (dans l'ordre)

```bash
# Activer l'environnement virtuel
.venv\Scripts\activate   # Windows
source .venv/bin/activate  # Linux/macOS

# Lancer Jupyter
jupyter lab notebooks/
```

Ordre d'exécution :
1. `01_exploration.ipynb` — EDA
2. `02_preprocessing.ipynb` — Pipeline de préparation
3. `03_logistic_regression.ipynb` — Modèle baseline
4. `04_random_forest.ipynb` — Random Forest
5. `05_xgboost.ipynb` — XGBoost + RandomizedSearch
6. `06_mlp_classification.ipynb` — MLP PyTorch (GPU)
7. `07_regression_revenue.ipynb` — Régression revenu à risque
8. `08_model_comparison.ipynb` — Comparaison, SHAP, écoresponsabilité

## API FastAPI — Documentation

Documentation interactive : http://localhost:8000/docs (Swagger UI)

### GET /health

Vérifie l'état du service et du modèle chargé.

```bash
curl http://localhost:8000/health
```

Réponse :
```json
{
  "status": "ok",
  "model_loaded": true,
  "model_name": "churn_classifier"
}
```

### POST /predict

Prédit la probabilité de churn et le revenu à risque pour un client.

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 35,
    "gender": "Male",
    "tenure_months": 24,
    "contract_type": "Monthly",
    "customer_segment": "SMB",
    "monthly_logins": 5,
    "weekly_active_days": 2,
    "avg_session_time": 15.0,
    "features_used": 3,
    "usage_growth_rate": -10.0,
    "last_login_days_ago": 30,
    "monthly_fee": 79,
    "total_revenue": 1896,
    "payment_method": "Credit Card",
    "payment_failures": 2,
    "discount_applied": "No",
    "price_increase_last_3m": "Yes",
    "support_tickets": 4,
    "avg_resolution_time": 24.0,
    "csat_score": 4.5,
    "escalations": 1,
    "email_open_rate": 0.1,
    "marketing_click_rate": 0.05,
    "nps_score": -20,
    "referral_count": 0,
    "signup_channel": "Online",
    "country": "France",
    "city": "Paris",
    "survey_response": "Negative"
  }'
```

Réponse :
```json
{
  "churn_probability": 0.7842,
  "churn_prediction": 1,
  "risk_level": "Élevé",
  "revenue_at_risk": 1487.65,
  "model_name": "churn_classifier"
}
```

### GET /model-info

Informations sur le modèle en production.

```bash
curl http://localhost:8000/model-info
```

Réponse :
```json
{
  "model_name": "churn_classifier",
  "framework": "sklearn",
  "version": "1",
  "metrics": {
    "auc_roc": 0.8093,
    "f1_churn": 0.2727,
    "recall_churn": 0.2059
  }
}
```

### Gestion des erreurs

L'API retourne des codes HTTP appropriés :

| Code | Situation |
|------|-----------|
| 200  | Prédiction réussie |
| 422  | Données invalides (champs manquants ou type incorrect) |
| 503  | Modèle non chargé |

Exemple d'erreur 422 (champ manquant) :
```json
{
  "detail": [
    {
      "loc": ["body", "age"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Modèles implémentés

| Modèle | AUC-ROC | F1 (churn) | Recall (churn) |
|--------|---------|------------|----------------|
| **Random Forest** (champion) | **0.8093** | 0.2727 | 0.2059 |
| XGBoost | 0.7661 | 0.2472 | 0.2157 |
| MLP PyTorch | 0.7560 | — | — |
| Logistic Regression | 0.7245 | 0.2851 | 0.6569 |

## Structure du projet

```
Projet_Data_Science/
├── data/
│   ├── raw/customer_churn.csv
│   └── processed/          # générés par le notebook 02
├── notebooks/              # 8 notebooks (01 à 08)
├── src/
│   ├── data/               # loader.py, preprocessor.py
│   ├── models/             # mlflow_utils.py
│   └── evaluation/         # metrics.py
├── dashboard/              # Streamlit (app.py + 4 pages)
├── api/                    # FastAPI (main.py, schemas.py, model_loader.py)
├── mlflow/                 # Dockerfile + .env
├── docker-compose.yml
├── justification.md        # Justifications techniques détaillées
└── requirements.txt        # Dépendances locales
```

## Dépendances

```bash
pip install -r requirements.txt
```

Principales : `mlflow==3.12.0`, `scikit-learn`, `xgboost`, `torch`, `shap`,
`fastapi`, `streamlit`, `pandas`, `numpy`, `matplotlib`, `plotly`.
