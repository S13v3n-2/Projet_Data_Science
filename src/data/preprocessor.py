"""
Pipeline de prétraitement des données clients.

Ce module construit et exporte le pipeline sklearn complet :
encodage des variables catégorielles + normalisation des variables numériques.
L'utilisation d'un Pipeline sklearn garantit qu'on n'applique pas de fit()
sur le jeu de test, ce qui serait une fuite de données classique.
"""

import numpy as np
import pandas as pd
import joblib
from pathlib import Path

from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.impute import SimpleImputer

from src.data.loader import (
    PROCESSED_DIR,
    CATEGORICAL_COLS,
    ID_COL,
    TARGET_CLASSIFICATION,
)


PIPELINE_PATH = PROCESSED_DIR / "preprocessing_pipeline.joblib"

# complaint_type est la seule colonne avec des valeurs manquantes (~20% manquants).
# Ces valeurs manquantes correspondent aux clients sans historique de plainte,
# donc le NA est informatif — on le remplace par "no_complaint" plutôt que
# par la modalité la plus fréquente pour préserver ce signal.
COMPLAINT_FILL = "no_complaint"


def add_revenue_at_risk(df: pd.DataFrame, churn_proba: np.ndarray = None) -> pd.DataFrame:
    """
    Calcule la variable cible pour la tâche de régression.

    revenue_at_risk = total_revenue * probabilité_de_churn

    Quand les probabilités de churn ne sont pas encore disponibles (avant
    l'entraînement du premier modèle), on utilise un proxy basé sur les
    variables comportementales disponibles pour construire un score préliminaire.
    Ce proxy est remplacé par la vraie proba dans le notebook 07.
    """
    df = df.copy()

    if churn_proba is not None:
        df["revenue_at_risk"] = df["total_revenue"] * churn_proba
    else:
        # Proxy conservateur : on suppose un risque uniforme de 10%
        # (taux de churn observé dans les données) pour initialiser la colonne.
        # Ce n'est utilisé que pour les besoins structurels du notebook 02.
        df["revenue_at_risk"] = df["total_revenue"] * 0.10

    return df


def add_engagement_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Construit un score d'engagement composite (0 à 1) à partir des
    variables comportementales, selon la formule proposée dans la consigne.

    Ce score synthétise cinq dimensions d'engagement client. Il peut servir
    de feature supplémentaire pour les modèles de classification, mais aussi
    comme variable cible d'une tâche prédictive complémentaire.
    """
    df = df.copy()

    from sklearn.preprocessing import MinMaxScaler
    scaler = MinMaxScaler()

    cols_to_scale = [
        "monthly_logins", "weekly_active_days", "avg_session_time",
        "features_used", "usage_growth_rate", "last_login_days_ago",
    ]
    scaled = scaler.fit_transform(df[cols_to_scale])
    scaled_df = pd.DataFrame(scaled, columns=cols_to_scale, index=df.index)

    df["engagement_score"] = (
        0.25 * scaled_df["monthly_logins"]
        + 0.20 * scaled_df["weekly_active_days"]
        + 0.20 * scaled_df["avg_session_time"]
        + 0.10 * scaled_df["features_used"]
        + 0.10 * scaled_df["usage_growth_rate"]
        # On inverse last_login_days_ago : plus c'est élevé, moins l'engagement est bon
        + 0.10 * (1 - scaled_df["last_login_days_ago"])
    )

    return df


def get_feature_lists(df: pd.DataFrame) -> tuple[list[str], list[str]]:
    """
    Identifie les colonnes numériques et catégorielles à inclure dans le pipeline.
    On exclut l'ID client, les variables cibles et les colonnes techniques.
    """
    exclude = {
        ID_COL,
        TARGET_CLASSIFICATION,
        "revenue_at_risk",
        "engagement_score",
    }

    cat_features = [
        c for c in CATEGORICAL_COLS
        if c in df.columns and c not in exclude
    ]

    num_features = [
        c for c in df.columns
        if c not in exclude
        and c not in cat_features
        and df[c].dtype in [np.float64, np.int64, float, int]
    ]

    return num_features, cat_features


def build_preprocessing_pipeline(num_features: list[str], cat_features: list[str]) -> ColumnTransformer:
    """
    Construit le ColumnTransformer sklearn pour le prétraitement.

    Choix techniques :
    - Numériques : StandardScaler (moyenne 0, écart-type 1).
      Les algorithmes basés sur les distances (régression logistique, MLP)
      sont sensibles à l'échelle des features. XGBoost et Random Forest n'en
      ont pas besoin, mais la normalisation ne nuit pas à leurs performances.
    - Catégorielles : OneHotEncoder avec handle_unknown='ignore'.
      L'encodage ordinal serait problématique ici car il introduirait un ordre
      artificiel entre des modalités qui n'en ont pas (ex. gender, payment_method).
      handle_unknown='ignore' évite les erreurs si le jeu de test contient
      une modalité rare absente du jeu d'entraînement.
    - complaint_type a des NaN (20% des clients) → on les remplace avant l'encodage.
    """
    numeric_pipeline = Pipeline([
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="constant", fill_value=COMPLAINT_FILL)),
        ("encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ("num", numeric_pipeline, num_features),
            ("cat", categorical_pipeline, cat_features),
        ],
        remainder="drop",
    )

    return preprocessor


def fit_and_save_pipeline(X_train: pd.DataFrame, num_features: list, cat_features: list) -> ColumnTransformer:
    """Entraîne le pipeline sur X_train et le sérialise sur disque."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    preprocessor = build_preprocessing_pipeline(num_features, cat_features)
    preprocessor.fit(X_train)

    joblib.dump(preprocessor, PIPELINE_PATH)
    print(f"Pipeline sauvegardé : {PIPELINE_PATH}")

    return preprocessor


def load_pipeline() -> ColumnTransformer:
    """Charge le pipeline prétraitement depuis le disque."""
    if not PIPELINE_PATH.exists():
        raise FileNotFoundError(
            "Pipeline introuvable. Exécutez d'abord le notebook 02_preprocessing.ipynb."
        )
    return joblib.load(PIPELINE_PATH)


def get_feature_names_after_encoding(preprocessor: ColumnTransformer, num_features: list, cat_features: list) -> list[str]:
    """
    Reconstruit la liste des noms de colonnes après OneHotEncoding.
    Indispensable pour l'interprétabilité (feature importance, SHAP).
    """
    ohe = preprocessor.named_transformers_["cat"]["encoder"]
    cat_names = list(ohe.get_feature_names_out(cat_features))
    return num_features + cat_names
