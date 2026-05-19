"""
Page 4 — Simulation et prédiction en temps réel

Cette page permet à un responsable marketing ou CRM d'entrer les caractéristiques
d'un client spécifique et d'obtenir immédiatement sa probabilité de churn
et son revenu à risque estimé, via l'API FastAPI.
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import os

st.set_page_config(page_title="Simulation client", layout="wide")
st.title("Simulation — Prédiction Client en Temps Réel")

API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

# Vérification de la disponibilité de l'API
try:
    health = requests.get(f"{API_BASE_URL}/health", timeout=3)
    api_ok = health.status_code == 200
    if api_ok:
        st.success("API disponible et opérationnelle")
    else:
        st.warning("L'API répond mais retourne un statut inattendu")
        api_ok = False
except Exception:
    st.error(f"API inaccessible à {API_BASE_URL}. Démarrez le service avec docker-compose up api")
    api_ok = False

st.markdown("---")
st.subheader("Paramètres du client à analyser")

st.markdown("Ajustez les valeurs ci-dessous pour simuler le profil d'un client :")

# Formulaire en deux colonnes
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**Profil & Contrat**")
    age = st.number_input("Âge", min_value=18, max_value=80, value=35)
    tenure_months = st.slider("Ancienneté (mois)", 1, 120, 24)
    contract_type = st.selectbox("Type de contrat", ["Monthly", "Annual", "Two-Year"])
    customer_segment = st.selectbox("Segment client", ["SMB", "Enterprise", "Startup", "Consumer"])
    gender = st.selectbox("Genre", ["Male", "Female"])

with col2:
    st.markdown("**Engagement & Utilisation**")
    monthly_logins = st.slider("Connexions / mois", 0, 60, 15)
    weekly_active_days = st.slider("Jours actifs / semaine", 0, 7, 3)
    avg_session_time = st.number_input("Durée session moyenne (min)", 0.0, 300.0, 30.0)
    features_used = st.slider("Fonctionnalités utilisées", 0, 20, 8)
    last_login_days_ago = st.slider("Dernière connexion (jours)", 0, 90, 7)
    nps_score = st.slider("NPS Score", -100, 100, 20)

with col3:
    st.markdown("**Finances & Support**")
    monthly_fee = st.number_input("Frais mensuels (€)", 10, 500, 79)
    total_revenue = st.number_input("Revenu total (€)", 100, 50000, 2500)
    payment_failures = st.slider("Échecs de paiement (12 mois)", 0, 10, 0)
    support_tickets = st.slider("Tickets support (12 mois)", 0, 20, 1)
    csat_score = st.slider("CSAT Score", 0.0, 10.0, 7.0)
    escalations = st.slider("Escalades", 0, 5, 0)

# Champs complémentaires dans un expandeur
with st.expander("Paramètres supplémentaires"):
    col4, col5 = st.columns(2)
    with col4:
        payment_method = st.selectbox("Méthode de paiement", ["Credit Card", "Bank Transfer", "PayPal"])
        discount_applied = st.selectbox("Remise appliquée", ["No", "Yes"])
        price_increase_last_3m = st.selectbox("Hausse de prix (3 derniers mois)", ["No", "Yes"])
    with col5:
        email_open_rate = st.slider("Taux ouverture emails", 0.0, 1.0, 0.3)
        marketing_click_rate = st.slider("Taux clic marketing", 0.0, 1.0, 0.1)
        referral_count = st.slider("Nombre de parrainages", 0, 10, 0)
        usage_growth_rate = st.number_input("Taux de croissance d'usage (%)", -100.0, 200.0, 5.0)
        avg_resolution_time = st.number_input("Temps de résolution moyen (h)", 0.0, 72.0, 4.0)

st.markdown("---")

if st.button("Calculer la probabilité de churn", type="primary", disabled=not api_ok):
    payload = {
        "age": age,
        "gender": gender,
        "tenure_months": tenure_months,
        "contract_type": contract_type,
        "customer_segment": customer_segment,
        "monthly_logins": monthly_logins,
        "weekly_active_days": weekly_active_days,
        "avg_session_time": avg_session_time,
        "features_used": features_used,
        "usage_growth_rate": usage_growth_rate,
        "last_login_days_ago": last_login_days_ago,
        "monthly_fee": monthly_fee,
        "total_revenue": total_revenue,
        "payment_method": payment_method,
        "payment_failures": payment_failures,
        "discount_applied": discount_applied,
        "price_increase_last_3m": price_increase_last_3m,
        "support_tickets": support_tickets,
        "avg_resolution_time": avg_resolution_time,
        "complaint_type": None,
        "csat_score": csat_score,
        "escalations": escalations,
        "email_open_rate": email_open_rate,
        "marketing_click_rate": marketing_click_rate,
        "nps_score": nps_score,
        "survey_response": "Neutral",
        "referral_count": referral_count,
        "signup_channel": "Online",
        "country": "France",
        "city": "Paris",
    }

    with st.spinner("Calcul en cours..."):
        try:
            response = requests.post(f"{API_BASE_URL}/predict", json=payload, timeout=10)
            result = response.json()

            churn_proba = result["churn_probability"]
            revenue_risk = result["revenue_at_risk"]
            risk_level = result["risk_level"]

            # Affichage du résultat
            st.markdown("---")
            st.subheader("Résultat de l'analyse")

            res_col1, res_col2, res_col3 = st.columns(3)

            color_map = {"Faible": "normal", "Modéré": "inverse", "Élevé": "inverse"}
            res_col1.metric(
                "Probabilité de churn",
                f"{churn_proba:.1%}",
                delta=risk_level,
            )
            res_col2.metric(
                "Revenu à risque",
                f"{revenue_risk:,.0f} €",
            )
            res_col3.metric(
                "Niveau de risque",
                risk_level,
            )

            # Jauge visuelle
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=churn_proba * 100,
                domain={"x": [0, 1], "y": [0, 1]},
                title={"text": "Probabilité de churn (%)"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": "tomato" if churn_proba > 0.5 else "steelblue"},
                    "steps": [
                        {"range": [0, 30], "color": "lightgreen"},
                        {"range": [30, 60], "color": "lightyellow"},
                        {"range": [60, 100], "color": "lightsalmon"},
                    ],
                    "threshold": {
                        "line": {"color": "red", "width": 4},
                        "thickness": 0.75,
                        "value": 50,
                    },
                },
            ))
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)

            if risk_level == "Élevé":
                st.error("Ce client présente un risque de churn élevé. Une action de rétention est recommandée.")
            elif risk_level == "Modéré":
                st.warning("Risque modéré. Un suivi proactif est conseillé.")
            else:
                st.success("Faible probabilité de churn. Le client semble satisfait.")

        except Exception as e:
            st.error(f"Erreur lors de l'appel à l'API : {e}")

elif not api_ok:
    st.markdown("*Le bouton de prédiction sera disponible une fois l'API démarrée.*")
