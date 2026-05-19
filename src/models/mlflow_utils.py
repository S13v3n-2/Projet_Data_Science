"""
Utilitaires MLflow partagés entre tous les notebooks d'entraînement.

Centraliser ces fonctions évite de répéter le même code de logging dans
chaque notebook, et garantit une cohérence dans le nommage des métriques,
paramètres et tags, essentielle pour pouvoir comparer les runs dans l'UI.
"""

import os
import tempfile
import mlflow
import mlflow.sklearn
import mlflow.pytorch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import joblib
from pathlib import Path
from typing import Any


# URI par défaut : se connecte au serveur MLflow local (Docker sur port 5000).
# Pour travailler en local sans Docker, on peut pointer vers un fichier SQLite.
DEFAULT_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")

# Nom de l'expérience MLflow pour la tâche de classification.
EXPERIMENT_CHURN = "churn_classification"
# Nom de l'expérience MLflow pour la tâche de régression.
EXPERIMENT_REVENUE = "revenue_at_risk_regression"


def setup_mlflow(experiment_name: str, tracking_uri: str = DEFAULT_TRACKING_URI) -> str:
    """
    Initialise la connexion MLflow et retourne l'experiment_id.
    Crée l'expérience si elle n'existe pas encore.
    """
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(experiment_name)
    exp = mlflow.get_experiment_by_name(experiment_name)
    print(f"Expérience MLflow : '{experiment_name}' (id={exp.experiment_id})")
    return exp.experiment_id


def _log_sklearn_model_via_artifact(model):
    """
    Sauvegarde un modèle sklearn localement puis l'uploade via mlflow.log_artifact.

    On évite intentionnellement mlflow.sklearn.log_model() car en MLflow 3.x
    celui-ci utilise la nouvelle API logged-models qui tente d'écrire les artefacts
    directement sur le système de fichiers du serveur (/mlflow/artifacts), inaccessible
    depuis un notebook WSL. mlflow.log_artifact() passe par le proxy HTTP et fonctionne
    correctement dans une architecture client local / serveur Docker.
    """
    with tempfile.TemporaryDirectory() as tmp_dir:
        model_path = os.path.join(tmp_dir, "model.joblib")
        joblib.dump(model, model_path)
        mlflow.log_artifact(model_path, artifact_path="model")


def log_classification_run(
    model,
    model_name: str,
    params: dict[str, Any],
    metrics: dict[str, float],
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    feature_names: list[str] = None,
    extra_artifacts: dict[str, str] = None,
) -> str:
    """
    Enregistre un run complet pour un modèle de classification dans MLflow.
    Retourne le run_id pour pouvoir le référencer dans le notebook de comparaison.

    Paramètres enregistrés :
    - params : hyperparamètres du modèle (max_depth, n_estimators, etc.)
    - metrics : toutes les métriques d'évaluation calculées sur le jeu de test
    - model : modèle sérialisé via joblib uploadé comme artefact
    - tags : informations contextuelles (type de modèle, tailles des jeux, etc.)
    """
    with mlflow.start_run(run_name=model_name) as run:
        # On loggue les hyperparamètres en premier pour avoir une trace
        # complète même si le run échoue plus loin.
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)

        mlflow.set_tags({
            "model_type": model_name,
            "task": "classification",
            "target": "churn",
            "train_size": len(X_train),
            "test_size": len(X_test),
        })

        _log_sklearn_model_via_artifact(model)

        if extra_artifacts:
            for local_path, artifact_name in extra_artifacts.items():
                mlflow.log_artifact(local_path, artifact_path=artifact_name)

        run_id = run.info.run_id
        print(f"Run enregistré : {model_name} | run_id={run_id}")
        print(f"  AUC-ROC : {metrics.get('auc_roc', 'N/A'):.4f}")
        print(f"  F1 (classe 1) : {metrics.get('f1_churn', 'N/A'):.4f}")

    return run_id


def log_regression_run(
    model,
    model_name: str,
    params: dict[str, Any],
    metrics: dict[str, float],
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> str:
    """Enregistre un run complet pour un modèle de régression dans MLflow."""
    with mlflow.start_run(run_name=model_name) as run:
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)

        mlflow.set_tags({
            "model_type": model_name,
            "task": "regression",
            "target": "revenue_at_risk",
            "train_size": len(X_train),
            "test_size": len(X_test),
        })

        _log_sklearn_model_via_artifact(model)

        run_id = run.info.run_id
        print(f"Run enregistré : {model_name} | run_id={run_id}")
        print(f"  RMSE : {metrics.get('rmse', 'N/A'):.4f}")
        print(f"  R²   : {metrics.get('r2', 'N/A'):.4f}")

    return run_id


def log_pytorch_classification_run(
    model,
    model_name: str,
    params: dict[str, Any],
    metrics: dict[str, float],
    X_train: np.ndarray,
    X_test: np.ndarray,
    input_dim: int,
) -> str:
    """
    Variante pour les modèles PyTorch (MLP).
    On sauvegarde les poids via torch.save puis on uploade le fichier comme artefact.
    """
    import torch

    with mlflow.start_run(run_name=model_name) as run:
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)

        mlflow.set_tags({
            "model_type": model_name,
            "task": "classification",
            "target": "churn",
            "framework": "pytorch",
            "train_size": len(X_train),
            "test_size": len(X_test),
        })

        with tempfile.TemporaryDirectory() as tmp_dir:
            weights_path = os.path.join(tmp_dir, "model_weights.pth")
            torch.save(model.state_dict(), weights_path)
            mlflow.log_artifact(weights_path, artifact_path="model")

        run_id = run.info.run_id
        print(f"Run PyTorch enregistré : {model_name} | run_id={run_id}")
        print(f"  AUC-ROC : {metrics.get('auc_roc', 'N/A'):.4f}")

    return run_id


def get_best_run(experiment_name: str, metric: str = "auc_roc", tracking_uri: str = DEFAULT_TRACKING_URI) -> dict:
    """
    Récupère le meilleur run d'une expérience selon une métrique donnée.
    Utilisé dans le notebook de comparaison et par l'API pour charger le modèle champion.
    """
    mlflow.set_tracking_uri(tracking_uri)
    client = mlflow.tracking.MlflowClient()
    exp = client.get_experiment_by_name(experiment_name)

    if exp is None:
        raise ValueError(f"Expérience '{experiment_name}' introuvable dans MLflow.")

    runs = client.search_runs(
        experiment_ids=[exp.experiment_id],
        order_by=[f"metrics.{metric} DESC"],
        max_results=1,
    )

    if not runs:
        raise ValueError(f"Aucun run trouvé dans l'expérience '{experiment_name}'.")

    best = runs[0]
    print(f"Meilleur modèle : {best.data.tags.get('model_type', 'inconnu')}")
    print(f"  {metric} = {best.data.metrics.get(metric, 'N/A'):.4f}")
    print(f"  run_id = {best.info.run_id}")

    return {
        "run_id": best.info.run_id,
        "model_type": best.data.tags.get("model_type"),
        "metrics": best.data.metrics,
        "params": best.data.params,
        "artifact_uri": best.info.artifact_uri,
    }


def save_figure_for_mlflow(fig: plt.Figure, filename: str) -> str:
    """Sauvegarde une figure matplotlib dans un dossier temp et retourne son chemin."""
    tmp_dir = tempfile.mkdtemp()
    path = os.path.join(tmp_dir, filename)
    fig.savefig(path, bbox_inches="tight", dpi=150)
    plt.close(fig)
    return path
