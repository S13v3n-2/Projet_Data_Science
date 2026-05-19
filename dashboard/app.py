"""
Dashboard décisionnel — Rétention Client & Risque de Revenus

Ce dashboard est destiné aux équipes marketing, CRM et direction financière.
Il transforme les prédictions du modèle ML en informations actionnables :
quels clients contacter, combien de revenu est exposé, quels leviers actionner.
"""

import streamlit as st

st.set_page_config(
    page_title="Rétention Client — Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Style personnalisé minimaliste
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        border-radius: 8px;
        padding: 16px;
        text-align: center;
    }
    .risk-high { color: #d32f2f; font-weight: bold; }
    .risk-low  { color: #388e3c; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("Système de Rétention Client")
st.markdown(
    "Plateforme de pilotage de la rétention et d'évaluation du risque de revenus. "
    "Utilisez la navigation dans le menu latéral pour accéder aux différentes sections."
)

st.markdown("---")

col1, col2, col3 = st.columns(3)
with col1:
    st.info("**Vue d'ensemble**\n\nKPIs globaux et distribution du risque")
with col2:
    st.warning("**Analyse du risque**\n\nClients à risque et revenu exposé")
with col3:
    st.success("**Simulation**\n\nPrédiction en temps réel pour un client")

st.markdown("""
---

**Navigation :**
- **01 Vue d'ensemble** — indicateurs globaux, taux de churn, revenu total à risque
- **02 Analyse du risque** — liste des clients prioritaires, segmentation par risque
- **03 Comparaison des modèles** — performances MLflow des modèles entraînés
- **04 Simulation** — entrez les caractéristiques d'un client pour obtenir sa probabilité de churn
""")
