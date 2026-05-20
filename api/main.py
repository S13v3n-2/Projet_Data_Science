"""
API REST - Prédiction de churn et estimation du revenu à risque

Cette API expose le modèle ML champion sélectionné après comparaison dans MLflow.
Elle est déployée via Docker et consommée par le dashboard Streamlit.

Endpoints :
- GET  /health      : vérification du statut du service
- POST /predict     : prédiction pour un client
- GET  /model-info  : informations sur le modèle actuellement chargé
- GET  /stats       : statistiques agregees du dataset pour le dashboard
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from schemas import ClientFeatures, PredictionResponse, HealthResponse, ModelInfoResponse
from model_loader import model_service
from stats import compute_stats

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestionnaire de cycle de vie de l'application.
    Le modèle est chargé une seule fois au démarrage du serveur,
    pas à chaque requête - indispensable pour des temps de réponse acceptables.
    """
    logger.info("Démarrage de l'API - chargement du modèle...")
    success = model_service.load()
    if success:
        logger.info(f"Modèle prêt : {model_service.model_info.get('model_name', 'inconnu')}")
    else:
        logger.warning("Aucun modèle chargé. Les prédictions ne seront pas disponibles.")
    yield
    logger.info("Arrêt de l'API.")


app = FastAPI(
    title="Churn Prediction API",
    description=(
        "API de prédiction de churn client et d'estimation du revenu à risque. "
        "Développée dans le cadre du Projet M1 Data Science - Rétention Client."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS ouvert pour les appels depuis le dashboard Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse, tags=["Monitoring"])
def health_check():
    """
    Vérifie l'état opérationnel du service.
    Utilisé par Docker pour les health checks et par le dashboard pour afficher
    l'indicateur de disponibilité de l'API.
    """
    return HealthResponse(
        status="ok" if model_service.is_loaded else "degraded",
        model_loaded=model_service.is_loaded,
        model_name=model_service.model_info.get("model_name"),
    )


@app.post("/predict", response_model=PredictionResponse, tags=["Prédiction"])
def predict(client: ClientFeatures):
    """
    Prédit la probabilité de churn et estime le revenu à risque pour un client.

    Le corps de la requête doit contenir les caractéristiques du client
    telles que définies dans le schéma ClientFeatures.
    """
    if not model_service.is_loaded:
        raise HTTPException(
            status_code=503,
            detail="Le service de prédiction n'est pas disponible. "
                   "Aucun modèle n'a pu être chargé depuis MLflow ou les fichiers locaux.",
        )

    try:
        features_dict = client.model_dump()
        result = model_service.predict(features_dict)
        return PredictionResponse(**result)

    except Exception as e:
        logger.error(f"Erreur lors de la prédiction : {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Erreur interne lors du calcul de la prédiction : {str(e)}",
        )


@app.get("/stats", tags=["Statistiques"])
def get_stats():
    """
    Retourne les statistiques agregees du dataset : KPIs, distributions,
    correlations et repartitions par segment.
    Mis en cache memoire - recalcul uniquement au redemarrage.
    """
    try:
        return compute_stats()
    except FileNotFoundError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Erreur calcul statistiques : {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Erreur lors du calcul des statistiques.")


@app.get("/model-info", response_model=ModelInfoResponse, tags=["Monitoring"])
def model_info():
    """
    Retourne les métadonnées du modèle actuellement chargé :
    nom, version, métriques de performance, hyperparamètres.
    """
    if not model_service.is_loaded:
        raise HTTPException(
            status_code=503,
            detail="Aucun modèle chargé.",
        )

    info = model_service.model_info
    return ModelInfoResponse(
        model_name=info.get("model_name", "inconnu"),
        run_id=info.get("run_id", "N/A"),
        metrics=info.get("metrics", {}),
        params=info.get("params", {}),
        framework=info.get("framework", "sklearn"),
    )
