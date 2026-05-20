"""
Page 3 - Comparaison des modèles MLflow

Cette page lit directement les runs depuis le serveur MLflow
pour afficher une comparaison visuelle des performances des modèles entraînés.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Comparaison des modèles", layout="wide")
st.title("Comparaison des Modèles ML")

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")


@st.cache_data(ttl=60)
def fetch_mlflow_runs(experiment_name: str) -> pd.DataFrame:
    """
    Récupère les runs MLflow pour une expérience donnée.
    Le TTL de 60s permet de voir les nouveaux runs sans recharger la page.
    """
    try:
        import mlflow
        mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
        client = mlflow.tracking.MlflowClient()
        exp = client.get_experiment_by_name(experiment_name)
        if exp is None:
            return pd.DataFrame()
        runs = client.search_runs(experiment_ids=[exp.experiment_id])
        records = []
        for run in runs:
            record = {
                "model": run.data.tags.get("model_type", "inconnu"),
                "run_id": run.info.run_id[:8],
            }
            record.update(run.data.metrics)
            records.append(record)
        if not records:
            return pd.DataFrame()
        df = pd.DataFrame(records)
        # En cas de runs multiples pour un même modèle, on garde le meilleur par AUC-ROC
        if "auc_roc" in df.columns:
            df = df.sort_values("auc_roc", ascending=False).drop_duplicates(subset=["model"])
        else:
            df = df.drop_duplicates(subset=["model"])
        return df.set_index("model")
    except Exception as e:
        st.warning(f"Connexion MLflow impossible : {e}\nAssurez-vous que le serveur MLflow est démarré.")
        return pd.DataFrame()


st.subheader("Classification - Prédiction du churn")

clf_df = fetch_mlflow_runs("churn_classification")

if clf_df.empty:
    st.info("Aucun run de classification trouvé. Exécutez les notebooks 03 à 06 d'abord.")
else:
    # Tableau comparatif
    display_metrics = ["auc_roc", "f1_churn", "recall_churn", "precision_churn", "accuracy", "log_loss"]
    available = [m for m in display_metrics if m in clf_df.columns]

    st.markdown("**Résultats sur le jeu de test :**")
    styled_df = clf_df[available].style.background_gradient(
        subset=["auc_roc", "f1_churn", "recall_churn"], cmap="Greens"
    ).background_gradient(subset=["log_loss"], cmap="Reds_r")
    st.dataframe(styled_df.format("{:.4f}"), use_container_width=True)

    # Graphique radar pour visualiser les compromis entre métriques
    st.markdown("---")
    st.subheader("Profil de performance - Graphique radar")

    radar_metrics = ["auc_roc", "f1_churn", "recall_churn", "precision_churn"]
    radar_available = [m for m in radar_metrics if m in clf_df.columns]

    if radar_available:
        fig = go.Figure()
        colors = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]
        for i, (model_name, row) in enumerate(clf_df[radar_available].iterrows()):
            values = list(row.values) + [row.values[0]]
            labels = radar_available + [radar_available[0]]
            fig.add_trace(go.Scatterpolar(
                r=values,
                theta=labels,
                fill="toself",
                name=model_name,
                line=dict(color=colors[i % len(colors)]),
                opacity=0.7,
            ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
            showlegend=True,
            title="Profil de performance par modèle",
            height=480,
        )
        st.plotly_chart(fig, use_container_width=True)

    # Graphique en barres côte à côte
    st.markdown("---")
    st.subheader("Comparaison des métriques clés")

    bar_metrics = ["auc_roc", "f1_churn", "recall_churn"]
    bar_available = [m for m in bar_metrics if m in clf_df.columns]

    if bar_available:
        df_melted = clf_df[bar_available].reset_index().melt(
            id_vars="model", var_name="métrique", value_name="valeur"
        )
        fig2 = px.bar(
            df_melted,
            x="métrique",
            y="valeur",
            color="model",
            barmode="group",
            labels={"valeur": "Score", "métrique": "Métrique"},
            title="AUC-ROC, F1 et Recall (classe churn) par modèle",
            color_discrete_sequence=px.colors.qualitative.Set2,
        )
        fig2.update_layout(height=420, yaxis=dict(range=[0, 1.05]))
        st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.subheader("Régression - Estimation du revenu à risque")

reg_df = fetch_mlflow_runs("revenue_at_risk_regression")

if reg_df.empty:
    st.info("Aucun run de régression trouvé. Exécutez le notebook 07 d'abord.")
else:
    reg_display = ["rmse", "mae", "r2"]
    reg_available = [m for m in reg_display if m in reg_df.columns]

    st.dataframe(
        reg_df[reg_available].style.background_gradient(subset=["r2"], cmap="Greens")
        .background_gradient(subset=["rmse", "mae"], cmap="Reds_r")
        .format("{:.4f}"),
        use_container_width=True,
    )

# Lien vers l'UI MLflow
st.markdown("---")
st.markdown(f"[Ouvrir l'interface MLflow complète]({MLFLOW_TRACKING_URI})")
