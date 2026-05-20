"""
Calcul des statistiques agregees depuis le dataset brut.
Mise en cache memoire - recalcul uniquement au redemarrage du serveur.
"""

import logging
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)

# Chemins selon l'environnement (Docker ou local)
CSV_PATHS = [
    Path("/app/data/raw/customer_churn.csv"),
    Path(__file__).resolve().parents[1] / "data" / "raw" / "customer_churn.csv",
]

LABEL_MAP = {
    "csat_score": "Score CSAT",
    "tenure_months": "Anciennete",
    "payment_failures": "Echecs de paiement",
    "escalations": "Escalades support",
    "monthly_fee": "Frais mensuels",
    "nps_score": "Score NPS",
    "support_tickets": "Tickets support",
    "avg_resolution_time": "Temps de resolution",
    "age": "Age",
    "last_login_days_ago": "Jours sans connexion",
    "monthly_logins": "Connexions mensuelles",
    "weekly_active_days": "Jours actifs / semaine",
    "features_used": "Fonctionnalites utilisees",
    "total_revenue": "Revenu total",
    "email_open_rate": "Taux ouverture email",
    "marketing_click_rate": "Taux clic marketing",
    "referral_count": "Parrainages",
    "usage_growth_rate": "Croissance utilisation",
    "avg_session_time": "Duree session moyenne",
}


def _load_csv() -> pd.DataFrame:
    for path in CSV_PATHS:
        if path.exists():
            logger.info(f"Dataset charge depuis : {path}")
            return pd.read_csv(path)
    raise FileNotFoundError(
        "Dataset introuvable. Verifiez que le volume Docker est bien monte "
        "ou que data/raw/customer_churn.csv existe."
    )


def _distribution(df: pd.DataFrame, col: str, step: int) -> list[dict]:
    """Calcule la distribution d'une variable numerique par statut churn (bins reguliers)."""
    df = df.copy()
    df["_bin"] = (np.floor(df[col] / step) * step).astype(int)
    pivot = (
        df.groupby(["_bin", "churn"])
        .size()
        .unstack(fill_value=0)
    )
    for c in [0, 1]:
        if c not in pivot.columns:
            pivot[c] = 0
    return (
        pivot[[0, 1]]
        .rename(columns={0: "nonChurn", 1: "churn"})
        .reset_index()
        .rename(columns={"_bin": col})
        .to_dict(orient="records")
    )


@lru_cache(maxsize=1)
def compute_stats() -> dict:
    """
    Calcule toutes les statistiques necessaires au dashboard frontend.
    Appel unique au demarrage puis mis en cache.
    """
    df = _load_csv()
    churners = df[df["churn"] == 1]

    # --- KPIs globaux ---
    kpis = {
        "total_clients": int(len(df)),
        "churn_rate": round(float(df["churn"].mean()) * 100, 1),
        "total_revenue_exposed": int(churners["total_revenue"].sum()),
        "monthly_fee_at_risk": int(churners["monthly_fee"].sum()),
    }

    # --- Taux de churn par type de contrat ---
    churn_by_contract = (
        df.groupby("contract_type", observed=True)["churn"]
        .mean()
        .mul(100)
        .round(1)
        .reset_index()
        .rename(columns={"contract_type": "contract", "churn": "rate"})
        .sort_values("rate", ascending=False)
        .to_dict(orient="records")
    )

    # --- Revenu expose par segment client ---
    revenue_by_segment = (
        churners.groupby("customer_segment", observed=True)["total_revenue"]
        .sum()
        .astype(int)
        .reset_index()
        .rename(columns={"customer_segment": "segment", "total_revenue": "revenue"})
        .sort_values("revenue", ascending=False)
        .to_dict(orient="records")
    )

    # --- Distribution NPS par statut (bins de 10 points) ---
    nps_distribution = _distribution(df, "nps_score", 10)

    # --- Distribution anciennete par statut (bins de 5 mois) ---
    tenure_distribution = _distribution(df, "tenure_months", 5)

    # --- Correlations (valeur absolue) avec le churn ---
    num_cols = df.select_dtypes(include=[np.number]).columns.difference(["churn"])
    corr_series = df[num_cols].corrwith(df["churn"]).abs().dropna().sort_values(ascending=False)
    top_corr = corr_series.head(7).reset_index()
    top_corr.columns = ["feature", "corr"]
    top_corr["factor"] = top_corr["feature"].map(LABEL_MAP).fillna(top_corr["feature"])
    correlations = (
        top_corr[["factor", "corr"]]
        .assign(corr=lambda x: x["corr"].round(3))
        .to_dict(orient="records")
    )

    return {
        "kpis": kpis,
        "churn_by_contract": churn_by_contract,
        "revenue_by_segment": revenue_by_segment,
        "nps_distribution": nps_distribution,
        "tenure_distribution": tenure_distribution,
        "correlations": correlations,
    }
