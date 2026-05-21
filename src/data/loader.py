"""
Chargement et validation initiale du dataset client.
Ce module est le point d'entrée unique pour accéder aux données brutes et
aux données prétraitées. Centraliser la lecture ici évite les chemins
codés en dur dans chaque notebook.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split


# Chemins relatifs à la racine du projet.
# On remonte de src/data/ jusqu'à la racine avec deux parents.
PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "customer_churn.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# Colonnes qu'on sait être catégorielles d'après l'exploration initiale.
# Les lister ici permet au preprocessor de les traiter sans re-détecter.
CATEGORICAL_COLS = [
    "gender",
    "country",
    "city",
    "customer_segment",
    "signup_channel",
    "contract_type",
    "payment_method",
    "discount_applied",
    "price_increase_last_3m",
    "complaint_type",
    "survey_response",
]

# La colonne identifiant unique client - on la retire avant la modélisation
# pour éviter qu'elle soit prise comme feature prédictive.
ID_COL = "customer_id"

# Variables cibles pour les deux tâches prédictives du projet.
TARGET_CLASSIFICATION = "churn"
TARGET_REGRESSION = "revenue_at_risk"


def load_raw() -> pd.DataFrame:
    """Charge le CSV brut et renvoie le DataFrame sans modification."""
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Le dataset est introuvable à l'emplacement attendu : {RAW_DATA_PATH}\n"
            "Lancez d'abord le script de téléchargement ou vérifiez le chemin."
        )

    df = pd.read_csv(RAW_DATA_PATH)
    print(f"Dataset chargé : {df.shape[0]:,} lignes, {df.shape[1]} colonnes")
    return df


def load_processed(filename: str) -> pd.DataFrame:
    """Charge un fichier prétraité depuis data/processed/."""
    path = PROCESSED_DIR / filename
    if not path.exists():
        raise FileNotFoundError(
            f"Fichier prétraité introuvable : {path}\n"
            "Exécutez d'abord le notebook 02_preprocessing.ipynb."
        )
    return pd.read_csv(path)


def split_features_target(df: pd.DataFrame, target: str) -> tuple[pd.DataFrame, pd.Series]:
    """
    Sépare le DataFrame en features (X) et variable cible (y).
    Retire l'identifiant client et la colonne cible de X.
    """
    cols_to_drop = [target, ID_COL]

    # On retire aussi l'autre variable cible si elle est présente,
    # pour éviter une fuite de données entre les deux tâches.
    other_targets = [TARGET_CLASSIFICATION, TARGET_REGRESSION]
    for col in other_targets:
        if col != target and col in df.columns:
            cols_to_drop.append(col)

    X = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    y = df[target]
    return X, y


def make_train_test_split(
    df: pd.DataFrame,
    target: str,
    test_size: float = 0.2,
    random_state: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """
    Effectue un split stratifié 80/20 sur le DataFrame fourni.
    La stratification sur la variable cible est essentielle ici car le churn
    représente seulement ~10% des observations : sans stratification, le jeu de
    test pourrait sous-représenter les churners et biaiser l'évaluation.
    """
    X, y = split_features_target(df, target)

    # On stratifie uniquement pour la classification binaire.
    # Pour la régression (revenue_at_risk), la stratification n'a pas de sens.
    stratify = y if target == TARGET_CLASSIFICATION else None

    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=test_size,
        random_state=random_state,
        stratify=stratify,
    )

    print(f"Train : {X_train.shape[0]:,} lignes | Test : {X_test.shape[0]:,} lignes")
    if stratify is not None:
        print(f"Taux de churn train : {y_train.mean():.3f} | test : {y_test.mean():.3f}")

    return X_train, X_test, y_train, y_test


def get_feature_groups() -> dict[str, list[str]]:
    """
    Retourne les features regroupées par nature métier.
    Utile pour l'EDA et pour documenter les choix de feature engineering.
    """
    return {
        "identite": ["age", "gender", "country", "city", "customer_segment"],
        "contrat": ["tenure_months", "signup_channel", "contract_type"],
        "engagement": [
            "monthly_logins", "weekly_active_days", "avg_session_time",
            "features_used", "usage_growth_rate", "last_login_days_ago",
        ],
        "financier": [
            "monthly_fee", "total_revenue", "payment_method",
            "payment_failures", "discount_applied", "price_increase_last_3m",
        ],
        "support": [
            "support_tickets", "avg_resolution_time", "complaint_type",
            "csat_score", "escalations",
        ],
        "marketing": [
            "email_open_rate", "marketing_click_rate", "nps_score",
            "survey_response", "referral_count",
        ],
    }
