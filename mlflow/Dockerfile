FROM python:3.11-slim

# On installe MLflow en correspondance exacte avec la version du .venv local
# pour éviter toute incompatibilité d'API entre le client (notebooks) et le serveur.
# psycopg2-binary est nécessaire pour se connecter à PostgreSQL comme backend.
RUN pip install --no-cache-dir mlflow==3.12.0 psycopg2-binary==2.9.9

EXPOSE 5000

ENTRYPOINT ["mlflow"]
