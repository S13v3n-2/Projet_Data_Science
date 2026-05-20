"""
Chargement et gestion du modèle ML depuis MLflow.

Ce module est responsable de charger le modèle champion au démarrage de l'API
et de fournir une interface de prédiction cohérente indépendamment du framework
sous-jacent (sklearn vs PyTorch).
"""

import os
import logging
import numpy as np
import pandas as pd
import joblib
import mlflow
import mlflow.sklearn
import mlflow.pytorch
from pathlib import Path

logger = logging.getLogger(__name__)

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MODEL_NAME = os.getenv("MODEL_NAME", "churn_classifier")

# Colonnes attendues par le préprocesseur, dans le même ordre que lors de l'entraînement
FEATURE_COLUMNS = [
    "age", "tenure_months", "monthly_logins", "weekly_active_days",
    "avg_session_time", "features_used", "usage_growth_rate",
    "last_login_days_ago", "monthly_fee", "total_revenue",
    "payment_failures", "support_tickets", "avg_resolution_time",
    "csat_score", "escalations", "email_open_rate", "marketing_click_rate",
    "nps_score", "referral_count", "gender", "country", "city",
    "customer_segment", "signup_channel", "contract_type", "payment_method",
    "discount_applied", "price_increase_last_3m", "complaint_type",
    "survey_response",
]


class ModelService:
    """
    Service de prédiction encapsulant le modèle et son préprocesseur.

    On charge le modèle et le pipeline sklearn une seule fois au démarrage
    de l'API pour éviter la latence de chargement à chaque requête.
    """

    def __init__(self):
        self.model = None
        self.preprocessor = None
        self.model_info = {}
        self._loaded = False

    def load(self) -> bool:
        """
        Tente de charger le modèle depuis MLflow, puis depuis les fichiers locaux en fallback.
        Retourne True si le chargement a réussi.
        """
        if self._try_load_from_mlflow():
            return True
        if self._try_load_from_local():
            return True
        logger.error("Impossible de charger le modèle depuis MLflow ou les fichiers locaux.")
        return False

    def _try_load_from_mlflow(self) -> bool:
        """Charge la dernière version du modèle depuis le Model Registry MLflow."""
        try:
            mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
            client = mlflow.tracking.MlflowClient()

            # On cherche la dernière version du modèle dans le Registry
            versions = client.search_model_versions(f"name='{MODEL_NAME}'")
            if not versions:
                logger.info(f"Modèle '{MODEL_NAME}' non trouvé dans le Registry MLflow.")
                return False

            latest = sorted(versions, key=lambda v: int(v.version), reverse=True)[0]

            # Les modèles ont été sauvegardés via joblib.dump + mlflow.log_artifact
            # (et non mlflow.sklearn.log_model), donc on télécharge le fichier brut.
            import tempfile
            run = client.get_run(latest.run_id)
            with tempfile.TemporaryDirectory() as tmp_dir:
                local_path = client.download_artifacts(latest.run_id, "model/model.joblib", tmp_dir)
                self.model = joblib.load(local_path)
                self.model_info["framework"] = "sklearn"
            self.model_info.update({
                "model_name": MODEL_NAME,
                "version": latest.version,
                "run_id": latest.run_id,
                "metrics": run.data.metrics,
                "params": run.data.params,
            })

            logger.info(f"Modèle chargé depuis MLflow : {MODEL_NAME} v{latest.version}")
            self._load_preprocessor()
            self._loaded = True
            return True

        except Exception as e:
            logger.warning(f"Chargement MLflow échoué : {e}")
            return False

    def _try_load_from_local(self) -> bool:
        """Fallback : charge le modèle depuis les fichiers joblib locaux."""
        local_paths = [
            Path("/app/data/processed/model_xgboost.joblib"),
            Path("/app/data/processed/model_random_forest.joblib"),
            Path("/app/data/processed/model_logistic_regression.joblib"),
        ]

        for path in local_paths:
            if path.exists():
                try:
                    self.model = joblib.load(path)
                    self.model_info = {
                        "model_name": path.stem,
                        "framework": "sklearn",
                        "run_id": "local",
                        "metrics": {},
                        "params": {},
                    }
                    logger.info(f"Modèle chargé localement : {path.name}")
                    self._load_preprocessor()
                    self._loaded = True
                    return True
                except Exception as e:
                    logger.warning(f"Impossible de charger {path.name} : {e}")

        return False

    def _load_preprocessor(self):
        """Charge le pipeline de prétraitement sérialisé lors du notebook 02."""
        preprocessor_path = Path("/app/data/processed/preprocessing_pipeline.joblib")
        if preprocessor_path.exists():
            self.preprocessor = joblib.load(preprocessor_path)
            logger.info("Pipeline de prétraitement chargé.")
        else:
            logger.warning("Pipeline de prétraitement introuvable.")

    def predict(self, features_dict: dict) -> dict:
        """
        Effectue une prédiction pour un client.
        Retourne la probabilité de churn et les métriques dérivées.
        """
        if not self._loaded:
            raise RuntimeError("Le modèle n'est pas chargé. Appelez load() d'abord.")

        df = pd.DataFrame([features_dict])

        if self.preprocessor is not None:
            X = self.preprocessor.transform(df)
        else:
            # Si le pipeline n'est pas disponible, on sélectionne les colonnes numériques
            num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            X = df[num_cols].values

        if self.model_info.get("framework") == "pytorch":
            import torch
            self.model.eval()
            with torch.no_grad():
                tensor = torch.tensor(X.astype(np.float32))
                churn_proba = self.model(tensor).item()
        else:
            churn_proba = self.model.predict_proba(X)[0, 1]

        churn_pred = int(churn_proba >= 0.5)
        total_revenue = features_dict.get("total_revenue", 0)
        revenue_at_risk = total_revenue * churn_proba

        if churn_proba < 0.3:
            risk_level = "Faible"
        elif churn_proba < 0.6:
            risk_level = "Modéré"
        else:
            risk_level = "Élevé"

        return {
            "churn_probability": round(float(churn_proba), 4),
            "churn_prediction": churn_pred,
            "risk_level": risk_level,
            "revenue_at_risk": round(float(revenue_at_risk), 2),
            "model_name": self.model_info.get("model_name", "inconnu"),
        }

    @property
    def is_loaded(self) -> bool:
        return self._loaded


# Instance singleton - partagée entre tous les workers FastAPI via lifespan
model_service = ModelService()
