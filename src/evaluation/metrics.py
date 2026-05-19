"""
Calcul des métriques d'évaluation pour les deux tâches prédictives.

Ce module centralise toutes les métriques afin que chaque notebook utilise
exactement les mêmes formules et les mêmes noms — indispensable pour comparer
les modèles de façon équitable dans MLflow et dans le rapport.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from sklearn.metrics import (
    roc_auc_score,
    f1_score,
    precision_score,
    recall_score,
    accuracy_score,
    log_loss,
    confusion_matrix,
    classification_report,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
    RocCurveDisplay,
    ConfusionMatrixDisplay,
)


def compute_classification_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: np.ndarray,
) -> dict[str, float]:
    """
    Calcule l'ensemble des métriques de classification pour un modèle.

    Pourquoi ces métriques et pas seulement l'accuracy ?
    Le dataset est fortement déséquilibré (~10% de churn). Un modèle qui prédit
    toujours "pas de churn" atteindrait 90% d'accuracy sans aucune valeur.
    L'AUC-ROC est la métrique principale car elle mesure la capacité de
    discrimination du modèle indépendamment du seuil de décision.
    Le recall sur la classe churn est critique : manquer un churner coûte plus
    cher qu'un faux positif (déclencher une action de rétention inutile).
    """
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "auc_roc": roc_auc_score(y_true, y_proba),
        "f1_weighted": f1_score(y_true, y_pred, average="weighted"),
        "f1_churn": f1_score(y_true, y_pred, pos_label=1, average="binary"),
        "precision_churn": precision_score(y_true, y_pred, pos_label=1, zero_division=0),
        "recall_churn": recall_score(y_true, y_pred, pos_label=1, zero_division=0),
        "log_loss": log_loss(y_true, y_proba),
    }
    return metrics


def compute_regression_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
) -> dict[str, float]:
    """
    Calcule les métriques de régression pour l'estimation du revenu à risque.

    RMSE : pénalise les grosses erreurs plus que MAE. Dans un contexte financier,
    sous-estimer le revenu à risque pour un gros client est plus coûteux que
    sous-estimer pour un petit client — RMSE capture cet aspect.
    MAE : interprétable directement en euros.
    R² : part de variance expliquée, utile pour comparer entre modèles.
    """
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    metrics = {
        "mae": mean_absolute_error(y_true, y_pred),
        "rmse": rmse,
        "r2": r2_score(y_true, y_pred),
    }
    return metrics


def compute_business_metrics(
    y_true_churn: np.ndarray,
    y_pred_churn: np.ndarray,
    total_revenue: np.ndarray,
    monthly_fee: np.ndarray,
) -> dict[str, float]:
    """
    Métriques orientées impact business, complémentaires aux métriques ML.

    Ces métriques permettent de communiquer les résultats aux équipes métier
    qui ne connaissent pas forcément l'AUC ou le F1.
    """
    tp_mask = (y_true_churn == 1) & (y_pred_churn == 1)
    fn_mask = (y_true_churn == 1) & (y_pred_churn == 0)

    revenue_detected = total_revenue[tp_mask].sum()
    revenue_missed = total_revenue[fn_mask].sum()
    monthly_fee_at_risk = monthly_fee[y_pred_churn == 1].sum()

    return {
        "revenue_correctly_flagged": float(revenue_detected),
        "revenue_missed_churn": float(revenue_missed),
        "monthly_fee_at_risk_flagged": float(monthly_fee_at_risk),
        "n_churners_detected": int(tp_mask.sum()),
        "n_churners_missed": int(fn_mask.sum()),
    }


def print_classification_report(y_true, y_pred, model_name: str):
    """Affiche un rapport de classification formaté."""
    print(f"\nRapport de classification — {model_name}")
    print("-" * 50)
    print(classification_report(y_true, y_pred, target_names=["Non-Churn", "Churn"]))


def plot_roc_curve(model, X_test, y_test, model_name: str, ax=None) -> plt.Axes:
    """Trace la courbe ROC pour un modèle sklearn."""
    if ax is None:
        _, ax = plt.subplots(figsize=(7, 5))

    RocCurveDisplay.from_estimator(model, X_test, y_test, ax=ax, name=model_name)
    ax.set_title(f"Courbe ROC — {model_name}")
    ax.plot([0, 1], [0, 1], "k--", lw=1, label="Classifieur aléatoire")
    ax.legend()
    return ax


def plot_confusion_matrix(y_true, y_pred, model_name: str, ax=None) -> plt.Axes:
    """Trace la matrice de confusion avec des labels clairs."""
    if ax is None:
        _, ax = plt.subplots(figsize=(5, 4))

    cm = confusion_matrix(y_true, y_pred)
    disp = ConfusionMatrixDisplay(cm, display_labels=["Non-Churn", "Churn"])
    disp.plot(ax=ax, colorbar=False, cmap="Blues")
    ax.set_title(f"Matrice de confusion — {model_name}")
    return ax


def plot_feature_importance(
    importance_values: np.ndarray,
    feature_names: list[str],
    model_name: str,
    top_n: int = 20,
) -> plt.Figure:
    """
    Trace un graphique horizontal des features les plus importantes.
    Limité aux top_n features pour la lisibilité.
    """
    indices = np.argsort(importance_values)[-top_n:]
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.barh(
        [feature_names[i] for i in indices],
        importance_values[indices],
        color="steelblue",
    )
    ax.set_xlabel("Importance")
    ax.set_title(f"Top {top_n} features — {model_name}")
    plt.tight_layout()
    return fig


def plot_regression_scatter(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    model_name: str,
) -> plt.Figure:
    """Nuage de points valeurs réelles vs prédites pour la régression."""
    fig, ax = plt.subplots(figsize=(7, 6))
    ax.scatter(y_true, y_pred, alpha=0.3, s=10, color="steelblue")
    lims = [min(y_true.min(), y_pred.min()), max(y_true.max(), y_pred.max())]
    ax.plot(lims, lims, "r--", lw=1.5, label="Prédiction parfaite")
    ax.set_xlabel("Valeurs réelles (€)")
    ax.set_ylabel("Valeurs prédites (€)")
    ax.set_title(f"Réel vs Prédit — {model_name}")
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}€"))
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}€"))
    ax.legend()
    plt.tight_layout()
    return fig
