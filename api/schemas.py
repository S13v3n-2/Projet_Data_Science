"""
Schémas Pydantic pour la validation des données entrantes et sortantes de l'API.

Pydantic garantit que les données envoyées à /predict correspondent bien
au format attendu par le modèle, avec des messages d'erreur clairs.
"""

from pydantic import BaseModel, Field
from typing import Optional


class ClientFeatures(BaseModel):
    """
    Représente toutes les caractéristiques d'un client nécessaires pour la prédiction.
    Les champs correspondent aux colonnes du dataset après avoir retiré customer_id et churn.
    Les valeurs par défaut correspondent aux médianes observées dans les données.
    """

    # Profil démographique
    age: int = Field(..., ge=18, le=100, description="Âge du client")
    gender: str = Field(..., description="Genre : Male ou Female")
    country: Optional[str] = Field(default="Unknown")
    city: Optional[str] = Field(default="Unknown")
    customer_segment: str = Field(..., description="Segment : SMB, Enterprise, Startup, Consumer")

    # Informations de contrat
    tenure_months: int = Field(..., ge=0, le=240, description="Ancienneté en mois")
    signup_channel: Optional[str] = Field(default="Online")
    contract_type: str = Field(..., description="Type de contrat : Monthly, Annual, Two-Year")

    # Engagement et utilisation
    monthly_logins: int = Field(..., ge=0)
    weekly_active_days: int = Field(..., ge=0, le=7)
    avg_session_time: float = Field(..., ge=0.0)
    features_used: int = Field(..., ge=0)
    usage_growth_rate: float = Field(default=0.0)
    last_login_days_ago: int = Field(..., ge=0)

    # Données financières
    monthly_fee: float = Field(..., ge=0.0)
    total_revenue: float = Field(..., ge=0.0)
    payment_method: str = Field(..., description="Mode de paiement")
    payment_failures: int = Field(default=0, ge=0)
    discount_applied: Optional[str] = Field(default="No")
    price_increase_last_3m: Optional[str] = Field(default="No")

    # Support client
    support_tickets: int = Field(default=0, ge=0)
    avg_resolution_time: float = Field(default=0.0, ge=0.0)
    complaint_type: Optional[str] = Field(default=None)
    csat_score: float = Field(default=7.0, ge=0.0, le=10.0)
    escalations: int = Field(default=0, ge=0)

    # Marketing et engagement externe
    email_open_rate: float = Field(default=0.3, ge=0.0, le=1.0)
    marketing_click_rate: float = Field(default=0.1, ge=0.0, le=1.0)
    nps_score: int = Field(default=20, ge=-100, le=100)
    survey_response: Optional[str] = Field(default="Neutral")
    referral_count: int = Field(default=0, ge=0)

    class Config:
        json_schema_extra = {
            "example": {
                "age": 35,
                "gender": "Male",
                "country": "France",
                "city": "Paris",
                "customer_segment": "SMB",
                "tenure_months": 24,
                "signup_channel": "Online",
                "contract_type": "Monthly",
                "monthly_logins": 8,
                "weekly_active_days": 3,
                "avg_session_time": 25.0,
                "features_used": 6,
                "usage_growth_rate": 2.0,
                "last_login_days_ago": 10,
                "monthly_fee": 79,
                "total_revenue": 2500,
                "payment_method": "Credit Card",
                "payment_failures": 2,
                "discount_applied": "No",
                "price_increase_last_3m": "Yes",
                "support_tickets": 3,
                "avg_resolution_time": 6.0,
                "complaint_type": None,
                "csat_score": 5.5,
                "escalations": 1,
                "email_open_rate": 0.2,
                "marketing_click_rate": 0.05,
                "nps_score": -10,
                "survey_response": "Negative",
                "referral_count": 0,
            }
        }


class PredictionResponse(BaseModel):
    """Réponse de l'endpoint /predict."""

    churn_probability: float = Field(..., description="Probabilité de churn entre 0 et 1")
    churn_prediction: int = Field(..., description="Décision binaire (0=Non-Churn, 1=Churn)")
    risk_level: str = Field(..., description="Niveau de risque : Faible, Modéré ou Élevé")
    revenue_at_risk: float = Field(..., description="Revenu estimé à risque en euros")
    model_name: str = Field(..., description="Nom du modèle utilisé pour la prédiction")


class HealthResponse(BaseModel):
    """Réponse de l'endpoint /health."""
    status: str
    model_loaded: bool
    model_name: Optional[str] = None


class ModelInfoResponse(BaseModel):
    """Réponse de l'endpoint /model-info."""
    model_name: str
    run_id: str
    metrics: dict
    params: dict
    framework: str
