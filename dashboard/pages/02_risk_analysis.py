"""
Page 2 — Analyse du risque et clients prioritaires

Cette page permet aux équipes CRM de filtrer et prioriser les clients
à contacter dans leurs campagnes de rétention.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
import os

st.set_page_config(page_title="Analyse du risque", layout="wide")
st.title("Analyse du Risque Client")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
DATA_PATH = "/app/data/raw/customer_churn.csv"


@st.cache_data(ttl=300)
def load_data():
    try:
        return pd.read_csv(DATA_PATH)
    except FileNotFoundError:
        return pd.read_csv("../data/raw/customer_churn.csv")


df = load_data()

# 1. Filtres de sélection
st.sidebar.subheader("Filtres")

segments = ["Tous"] + sorted(df["customer_segment"].unique().tolist())
selected_segment = st.sidebar.selectbox("Segment client", segments)

contracts = ["Tous"] + sorted(df["contract_type"].unique().tolist())
selected_contract = st.sidebar.selectbox("Type de contrat", contracts)

min_revenue = st.sidebar.slider(
    "Revenu minimum (€)",
    min_value=int(df["total_revenue"].min()),
    max_value=int(df["total_revenue"].max()),
    value=int(df["total_revenue"].quantile(0.5)),
    step=1000,
)

# Filtre sur le churn connu (pour l'analyse, on montre les churners réels)
show_only_churners = st.sidebar.checkbox("Afficher uniquement les churners", value=True)

# Application des filtres
filtered = df.copy()
if selected_segment != "Tous":
    filtered = filtered[filtered["customer_segment"] == selected_segment]
if selected_contract != "Tous":
    filtered = filtered[filtered["contract_type"] == selected_contract]
filtered = filtered[filtered["total_revenue"] >= min_revenue]
if show_only_churners:
    filtered = filtered[filtered["churn"] == 1]

st.markdown(f"**{len(filtered):,} clients correspondent aux critères sélectionnés**")

# 2. KPIs filtrés
col1, col2, col3 = st.columns(3)
col1.metric("Clients affichés", f"{len(filtered):,}")
col2.metric("Revenu à risque", f"{filtered['total_revenue'].sum():,.0f} €")
col3.metric("Perte mensuelle", f"{filtered['monthly_fee'].sum():,.0f} € / mois")

st.markdown("---")

# 3. Top clients par revenu à risque
st.subheader("Top 20 clients prioritaires (revenu total décroissant)")

display_cols = [
    "customer_id", "customer_segment", "contract_type",
    "tenure_months", "monthly_fee", "total_revenue",
    "payment_failures", "support_tickets", "nps_score", "churn"
]
available_cols = [c for c in display_cols if c in filtered.columns]
top20 = filtered[available_cols].sort_values("total_revenue", ascending=False).head(20)

st.dataframe(
    top20.style.background_gradient(subset=["total_revenue"], cmap="Oranges")
              .background_gradient(subset=["payment_failures", "support_tickets"], cmap="Reds"),
    use_container_width=True,
)

# 4. Matrice risque × valeur
st.markdown("---")
st.subheader("Matrice Risque × Valeur client")
st.markdown("Les clients en haut à droite sont les plus urgents à contacter.")

fig = px.scatter(
    filtered,
    x="payment_failures",
    y="total_revenue",
    color="support_tickets",
    size="monthly_fee",
    hover_data=["customer_id", "customer_segment", "contract_type"],
    labels={
        "payment_failures": "Échecs de paiement (risque)",
        "total_revenue": "Revenu total (valeur €)",
        "support_tickets": "Tickets support",
    },
    title="Matrice risque (x) × valeur (y) des clients sélectionnés",
    color_continuous_scale="RdYlGn_r",
)
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# 5. Distribution du revenu à risque par pays
if "country" in filtered.columns:
    st.markdown("---")
    st.subheader("Revenu à risque par pays")

    by_country = (
        filtered.groupby("country")["total_revenue"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )

    fig2 = px.bar(
        by_country,
        x="country",
        y="total_revenue",
        color="total_revenue",
        color_continuous_scale="Reds",
        labels={"total_revenue": "Revenu total à risque (€)", "country": "Pays"},
        title="Top 10 pays par revenu exposé",
    )
    fig2.update_layout(showlegend=False, height=380)
    st.plotly_chart(fig2, use_container_width=True)
