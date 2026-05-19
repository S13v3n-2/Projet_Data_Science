"""
Page 1 — Vue d'ensemble et KPIs globaux

Cette page donne une lecture immédiate de la situation :
combien de clients sont à risque, quel revenu est exposé,
et quelle est l'évolution du taux de churn par segment.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os
import requests

st.set_page_config(page_title="Vue d'ensemble", layout="wide")
st.title("Vue d'ensemble — Indicateurs Clés")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
DATA_PATH = "/app/data/raw/customer_churn.csv"


@st.cache_data(ttl=300)
def load_data():
    """Charge les données brutes. Le cache de 5 minutes évite les re-lectures répétées."""
    try:
        df = pd.read_csv(DATA_PATH)
        return df
    except FileNotFoundError:
        # Chemin alternatif pour exécution locale hors Docker
        local_path = "../data/raw/customer_churn.csv"
        return pd.read_csv(local_path)


df = load_data()

# 1. Métriques globales
st.subheader("Indicateurs globaux")

total_clients = len(df)
churners = df[df["churn"] == 1]
churn_rate = len(churners) / total_clients
total_revenue = df["total_revenue"].sum()
revenue_at_risk = churners["total_revenue"].sum()
monthly_risk = churners["monthly_fee"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="Total clients",
    value=f"{total_clients:,}",
)
col2.metric(
    label="Taux de churn",
    value=f"{churn_rate:.1%}",
    delta=None,
    help="Proportion de clients ayant churné dans le dataset",
)
col3.metric(
    label="Revenu total à risque",
    value=f"{revenue_at_risk:,.0f} €",
    help="Somme du revenu total des clients churners",
)
col4.metric(
    label="Perte mensuelle estimée",
    value=f"{monthly_risk:,.0f} € / mois",
    help="Frais mensuels des clients churners",
)

st.markdown("---")

# 2. Distribution du risque par segment
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Taux de churn par type de contrat")
    churn_by_contract = (
        df.groupby("contract_type")["churn"]
        .agg(["sum", "count"])
        .rename(columns={"sum": "churners", "count": "total"})
        .assign(churn_rate=lambda x: x["churners"] / x["total"] * 100)
        .reset_index()
    )
    fig = px.bar(
        churn_by_contract,
        x="contract_type",
        y="churn_rate",
        color="churn_rate",
        color_continuous_scale="RdYlGn_r",
        labels={"churn_rate": "Taux de churn (%)", "contract_type": "Type de contrat"},
        title="Taux de churn par type de contrat",
    )
    fig.update_traces(texttemplate="%{y:.1f}%", textposition="outside")
    fig.update_layout(showlegend=False, height=380)
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("Revenu à risque par segment client")
    risk_by_segment = (
        df[df["churn"] == 1]
        .groupby("customer_segment")["total_revenue"]
        .sum()
        .reset_index()
        .rename(columns={"total_revenue": "revenu_risque"})
        .sort_values("revenu_risque", ascending=True)
    )
    fig2 = px.bar(
        risk_by_segment,
        x="revenu_risque",
        y="customer_segment",
        orientation="h",
        color="revenu_risque",
        color_continuous_scale="Oranges",
        labels={"revenu_risque": "Revenu à risque (€)", "customer_segment": "Segment"},
        title="Revenu exposé par segment client",
    )
    fig2.update_layout(showlegend=False, height=380)
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# 3. Distribution des scores d'engagement
st.subheader("Distribution par indicateurs comportementaux")

col_a, col_b = st.columns(2)

with col_a:
    fig3 = px.histogram(
        df,
        x="nps_score",
        color=df["churn"].map({0: "Non-Churn", 1: "Churn"}),
        barmode="overlay",
        nbins=30,
        labels={"nps_score": "NPS Score", "color": "Statut"},
        title="Distribution du NPS Score par statut de churn",
        color_discrete_map={"Non-Churn": "steelblue", "Churn": "tomato"},
        opacity=0.7,
    )
    fig3.update_layout(height=350)
    st.plotly_chart(fig3, use_container_width=True)

with col_b:
    fig4 = px.histogram(
        df,
        x="tenure_months",
        color=df["churn"].map({0: "Non-Churn", 1: "Churn"}),
        barmode="overlay",
        nbins=30,
        labels={"tenure_months": "Ancienneté (mois)", "color": "Statut"},
        title="Distribution de l'ancienneté par statut de churn",
        color_discrete_map={"Non-Churn": "steelblue", "Churn": "tomato"},
        opacity=0.7,
    )
    fig4.update_layout(height=350)
    st.plotly_chart(fig4, use_container_width=True)

# 4. Top 5 facteurs de risque
st.subheader("Facteurs les plus associés au churn")

num_cols = [
    "payment_failures", "support_tickets", "escalations",
    "nps_score", "csat_score", "tenure_months", "monthly_fee"
]
corr_with_churn = (
    df[num_cols + ["churn"]]
    .corr()["churn"]
    .drop("churn")
    .abs()
    .sort_values(ascending=False)
)

fig5 = px.bar(
    x=corr_with_churn.index,
    y=corr_with_churn.values,
    labels={"x": "Feature", "y": "Corrélation absolue avec le churn"},
    title="Corrélation des variables numériques avec le churn",
    color=corr_with_churn.values,
    color_continuous_scale="Blues",
)
fig5.update_layout(showlegend=False, height=350)
st.plotly_chart(fig5, use_container_width=True)
