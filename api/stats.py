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

    # KPIs globaux
    kpis = {
        "total_clients": int(len(df)),
        "churn_rate": round(float(df["churn"].mean()) * 100, 1),
        "total_revenue_exposed": int(churners["total_revenue"].sum()),
        "monthly_fee_at_risk": int(churners["monthly_fee"].sum()),
    }

    # Taux de churn par type de contrat
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

    # Revenu expose par segment client
    revenue_by_segment = (
        churners.groupby("customer_segment", observed=True)["total_revenue"]
        .sum()
        .astype(int)
        .reset_index()
        .rename(columns={"customer_segment": "segment", "total_revenue": "revenue"})
        .sort_values("revenue", ascending=False)
        .to_dict(orient="records")
    )

    # Distribution NPS par statut (bins de 10 points)
    nps_distribution = _distribution(df, "nps_score", 10)

    # Distribution anciennete par statut (bins de 5 mois)
    tenure_distribution = _distribution(df, "tenure_months", 5)

    # Correlations (valeur absolue) avec le churn
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


def get_clients_at_risk(
    model_service,
    segment: str | None = None,
    contract_type: str | None = None,
    min_prob: float = 0.3,
    page: int = 1,
    page_size: int = 50,
) -> dict:
    """
    Score tous les clients en batch et retourne ceux au-dessus du seuil min_prob.
    Pas de mise en cache car les filtres varient par requete.
    """
    df = _load_csv()

    # Colonnes categorielles encodees par le preprocesseur
    feature_cols = [c for c in df.columns if c not in ("churn", "customer_id")]
    X = df[feature_cols]

    # Scoring vectorise sur tout le dataset en une seule passe
    X_transformed = model_service.preprocessor.transform(X)
    probas = model_service.model.predict_proba(X_transformed)[:, 1]

    result = df[["customer_id", "customer_segment", "contract_type", "total_revenue"]].copy()
    result["churn_probability"] = probas
    result["revenue_at_risk"] = (result["total_revenue"] * probas).round(0).astype(int)

    # Filtres optionnels
    if segment:
        result = result[result["customer_segment"] == segment]
    if contract_type:
        result = result[result["contract_type"] == contract_type]
    result = result[result["churn_probability"] >= min_prob]

    result = result.sort_values("churn_probability", ascending=False)

    total = len(result)
    pages = max(1, -(-total // page_size))  # division entiere vers le haut
    start = (page - 1) * page_size
    page_data = result.iloc[start : start + page_size]

    records = []
    for _, row in page_data.iterrows():
        records.append({
            "customer_id": row["customer_id"],
            "segment": row["customer_segment"],
            "contract_type": row["contract_type"],
            "churn_probability": round(float(row["churn_probability"]), 3),
            "revenue_at_risk": int(row["revenue_at_risk"]),
        })

    return {
        "total": total,
        "page": page,
        "page_size": page_size,
        "pages": pages,
        "results": records,
    }


def get_clients_at_risk_csv(
    model_service,
    segment: str | None = None,
    contract_type: str | None = None,
    min_prob: float = 0.3,
) -> str:
    """Retourne tous les clients a risque au format CSV (sans pagination)."""
    # Reutilise get_clients_at_risk avec une page_size tres grande
    df = _load_csv()
    feature_cols = [c for c in df.columns if c not in ("churn", "customer_id")]
    X = df[feature_cols]
    X_transformed = model_service.preprocessor.transform(X)
    probas = model_service.model.predict_proba(X_transformed)[:, 1]

    result = df[["customer_id", "customer_segment", "contract_type", "total_revenue"]].copy()
    result["churn_probability"] = probas
    result["revenue_at_risk"] = (result["total_revenue"] * probas).round(0).astype(int)

    if segment:
        result = result[result["customer_segment"] == segment]
    if contract_type:
        result = result[result["contract_type"] == contract_type]
    result = result[result["churn_probability"] >= min_prob]
    result = result.sort_values("churn_probability", ascending=False)

    export = result[["customer_id", "customer_segment", "contract_type", "churn_probability", "revenue_at_risk"]].copy()
    export.columns = ["ID Client", "Segment", "Type contrat", "Probabilite churn", "Revenu a risque (EUR)"]
    export["Probabilite churn"] = export["Probabilite churn"].apply(lambda x: f"{x:.1%}")
    return export.to_csv(index=False)
