# Justifications des Choix Techniques

Ce document détaille et justifie l'ensemble des décisions techniques prises dans ce projet.
Chaque choix est argumenté à la fois sur un plan technique et sur un plan métier.


## 1. Choix du dataset et des tâches prédictives

**Dataset :** Customer Churn Prediction Business Dataset (Kaggle — miadul)

Le dataset contient 10 000 observations clients avec 32 variables couvrant des dimensions
comportementales, financières, de support et de marketing. Il a été choisi pour sa richesse
en variables métier directement actionnables par les équipes CRM.

**Tâche 1 — Prédiction du churn (classification binaire)**

C'est la tâche la plus naturelle et la plus stratégique : identifier les clients qui vont
partir avant qu'ils ne partent réellement. Le taux de churn observé est de 10.2%, ce qui
représente un déséquilibre modéré qu'on ne peut pas ignorer.

Intérêt business : déclencher des campagnes de rétention ciblées sur les profils les plus
à risque réduit le coût d'acquisition clients et stabilise le chiffre d'affaires.

**Tâche 2 — Estimation du revenu à risque (régression)**

La variable cible est construite comme suit :
`revenue_at_risk = total_revenue × probabilité_de_churn`

Cette formulation est plus fine que d'utiliser simplement le churn binaire, car elle
pondère chaque client par sa valeur financière réelle. Un client à 5 000€ de revenu
annuel avec 60% de probabilité de churn représente 3 000€ à risque, ce qui est
très différent d'un client à 500€ avec la même probabilité.

Ce calcul introduit un biais léger (la probabilité de churn dépend du classifieur),
mais c'est une pratique courante et acceptable en analytics marketing.

## 2. Choix des modèles de classification

La consigne impose au moins 4 modèles et au moins 1 modèle de Deep Learning.

**Modèle 1 — Régression Logistique**

Justification : c'est le modèle de référence (baseline) en classification binaire.
Ses coefficients sont directement interprétables comme l'impact marginal de chaque feature
sur le log-odds de churn, ce qui est précieux pour expliquer les résultats aux équipes métier.
Si XGBoost n'est que légèrement meilleur, la régression logistique sera préférable en production
pour sa simplicité et sa transparence.

Hyperparamètres :
- `C=1.0` : régularisation L2 par défaut, suffisante pour un premier essai
- `class_weight='balanced'` : compense le déséquilibre 90/10 automatiquement
- `solver='lbfgs'` : adapté aux datasets de taille moyenne avec features mixtes

**Modèle 2 — Random Forest**

Justification : le Random Forest est robuste aux valeurs aberrantes et aux features non
normalisées. Il construit 200 arbres indépendants sur des sous-échantillons aléatoires,
ce qui réduit la variance sans augmenter le biais. La feature importance calculée
(réduction moyenne de l'impureté de Gini) est intuitive et largement utilisée.

Hyperparamètres :
- `n_estimators=200` : compromis entre stabilité et temps de calcul
- `max_depth=15` : évite l'overfitting tout en capturant les interactions non linéaires
- `min_samples_leaf=5` : régularisation supplémentaire
- `max_features='sqrt'` : décorrèle les arbres pour réduire la variance

**Modèle 3 — XGBoost**

Justification : XGBoost est l'algorithme le plus performant sur les datasets tabulaires
de taille moyenne selon la littérature et les compétitions Kaggle. Il construit des arbres
séquentiellement, chaque arbre corrigeant les erreurs du précédent (gradient boosting).
La régularisation L1/L2 intégrée et le paramètre `scale_pos_weight` pour les données
déséquilibrées en font un choix très approprié ici.

Hyperparamètres :
- `learning_rate=0.1` avec `n_estimators=300` : compromis classique
- `subsample=0.8` et `colsample_bytree=0.8` : régularisation par stochastique
- `scale_pos_weight` = ratio négatifs/positifs ≈ 8.8 : équivalent de class_weight='balanced'

**Modèle 4 — MLP (PyTorch) — Deep Learning obligatoire**

Justification de l'inclusion :
Le MLP peut en théorie capturer des interactions non linéaires complexes entre features
que les modèles ensembles pourraient rater. Par exemple, la combinaison simultanée
d'un NPS bas, de plusieurs échecs de paiement et d'une ancienneté faible pourrait
créer un signal synergique non capturé par un arbre de décision.

Justification de l'architecture choisie (256 → 128 → 64) :
- Architecture en entonnoir progressif : chaque couche construit une représentation
  de plus en plus abstraite des features
- BatchNorm : stabilise l'entraînement en normalisant les activations à chaque couche,
  ce qui permet d'utiliser un learning rate plus élevé
- Dropout (0.3) : régularisation critique avec seulement 10 000 observations, évite
  que le réseau mémorise les données d'entraînement
- AdamW + ReduceLROnPlateau : gestion adaptative du learning rate, standard pour les MLP

Limitation attendue et justifiée :
Avec 10 000 observations, le Deep Learning est généralement désavantagé face aux méthodes
ensembles. Cette limitation sera documentée et analysée dans le notebook de comparaison,
ce qui constitue précisément l'objectif pédagogique de la consigne.


## 3. Métriques de suivi dans MLflow

**Pour la classification :**

| Métrique | Justification |
|---|---|
| AUC-ROC | Métrique principale. Mesure la capacité discriminante indépendamment du seuil. Robuste au déséquilibre des classes contrairement à l'accuracy. |
| F1-score (classe churn) | Équilibre précision et recall sur la classe minoritaire. Bonne synthèse pour un rapport. |
| Recall (classe churn) | Prioritaire business : manquer un churner (faux négatif) est plus coûteux que déclencher une action inutile (faux positif). |
| Précision (classe churn) | Évite de saturer les équipes CRM avec trop de faux positifs. |
| Accuracy | Conservée pour comparaison, mais non prioritaire en contexte déséquilibré. |
| Log Loss | Mesure la qualité des probabilités, pas seulement des décisions binaires. Critique pour le calcul de revenue_at_risk. |

**Pourquoi pas l'accuracy comme métrique principale ?**

Un modèle qui prédirait toujours "Non-Churn" obtiendrait 89.8% d'accuracy sans aucune valeur.
L'AUC-ROC est immune à ce problème car elle évalue le ranking des probabilités sur l'ensemble
des seuils possibles.

**Pour la régression :**

| Métrique | Justification |
|---|---|
| RMSE | Pénalise les grosses erreurs plus que la MAE. Dans un contexte financier, sous-estimer le risque d'un gros client est plus coûteux. |
| MAE | Directement interprétable en euros. |
| R² | Mesure la part de variance expliquée — utile pour comparer les modèles entre eux. |


## 4. Choix de MLflow + PostgreSQL comme backend

**Pourquoi MLflow ?**

MLflow est l'outil de référence pour le tracking d'expériences ML. Il permet de :
- Comparer visuellement les hyperparamètres et métriques de tous les modèles
- Sérialiser et versionner les modèles avec leurs métadonnées
- Exposer une API Python pour charger le meilleur modèle dans l'API FastAPI

**Pourquoi PostgreSQL plutôt que SQLite ?**

SQLite est suffisant pour un usage personnel, mais présente des limites :
- Il ne supporte pas les accès concurrents (plusieurs notebooks simultanés)
- Il est stocké localement dans le conteneur et perdu à sa destruction

PostgreSQL dans un conteneur dédié résout ces deux problèmes et simule une architecture
de production réaliste. C'est aussi cohérent avec les pratiques MLOps actuelles.

## 5. Architecture Docker Compose

Quatre services sont définis :

**postgres** : base de données relationnelle pour MLflow. Utilisée via un volume nommé
pour la persistance des données entre les redémarrages des conteneurs.

**mlflow** : serveur de tracking (port 5000). Dépend de postgres avec un healthcheck
pour s'assurer que la base est disponible avant de démarrer.

**api** : service FastAPI (port 8000). Charge le modèle au démarrage via le lifespan
FastAPI pour éviter la latence à chaque requête. Monte les artefacts MLflow en lecture seule.

**streamlit** : dashboard décisionnel (port 8501). Communique avec l'API pour les
prédictions en temps réel et avec MLflow pour la comparaison des modèles.


## 6. Choix de Streamlit pour le dashboard

**Streamlit vs Dash :**

Streamlit a été retenu pour sa rapidité de développement et sa syntaxe Python pure,
sans avoir besoin de callbacks et de composants React comme avec Dash.
Pour un MVP en contexte pédagogique, la courbe d'apprentissage est significativement
plus courte et le résultat visuel est immédiatement professionnel.

Plotly est utilisé pour les graphiques interactifs (filtres, hover, zoom), ce qui
est nécessaire pour l'usage métier.


## 7. Choix de FastAPI pour l'API REST

**FastAPI vs Flask :**

FastAPI a été préféré pour deux raisons principales :

1. La validation automatique des données via Pydantic : les schémas d'entrée/sortie
   sont définis en Python et la validation est effectuée automatiquement à chaque requête,
   avec des messages d'erreur clairs et une documentation Swagger générée automatiquement.

2. Les performances : FastAPI est basé sur ASGI (asynchrone) et est significativement
   plus rapide que Flask en charge. Pour une API de prédiction appelée depuis un dashboard
   en temps réel, c'est un avantage non négligeable.


## 8. Stratégie de split train/test et cross-validation

**Split 80/20 stratifié :**

La stratification sur la variable cible est indispensable avec 10% de churn.
Sans stratification, le jeu de test pourrait par malchance ne contenir que 5% de churners,
ce qui biaiserait toutes les métriques d'évaluation vers le bas.

**Cross-validation 5 plis StratifiedKFold :**

La cross-validation est effectuée uniquement sur le jeu d'entraînement pour deux raisons :
1. Évaluer la stabilité du modèle (variance de l'AUC entre les plis)
2. Comparer les modèles sur une métrique plus robuste qu'un simple test set

Le jeu de test reste un hold-out final utilisé seulement pour l'évaluation finale.


## 9. Gestion du déséquilibre des classes

Le taux de churn de 10.2% est un déséquilibre modéré mais réel. Deux stratégies ont été
appliquées selon le modèle :

- `class_weight='balanced'` (sklearn) et `scale_pos_weight` (XGBoost) : repondèrent
  les exemples dans la fonction de coût sans modifier les données. Simple et efficace.

- Pour le MLP PyTorch : utilisation d'une BCELoss avec pos_weight calculé comme le
  ratio négatifs/positifs, équivalent direct de class_weight='balanced'.

SMOTE (sur-échantillonnage synthétique) n'a pas été appliqué par défaut car avec
10 000 observations et un déséquilibre de 10%, les méthodes de repondération suffisent
et évitent de créer des exemples synthétiques potentiellement bruités.


## 10. Gestion de la valeur manquante de complaint_type

La colonne `complaint_type` contient environ 20% de NaN.
Ces valeurs manquantes ne sont pas des erreurs de données : elles correspondent à des clients
n'ayant jamais soumis de plainte, ce qui est une information métier précieuse.

Imputer ces NaN par la valeur la plus fréquente serait incorrect car cela supposerait
que ces clients ont effectivement eu un certain type de plainte.

La stratégie retenue est de remplacer les NaN par la chaîne `"no_complaint"` avant
l'encodage OneHot, ce qui crée une modalité explicite pour ces clients.
Cela préserve l'information (absence de plainte = signal positif) dans le modèle.

## 11. Feature engineering — Score d'engagement

Un score d'engagement composite (0 à 1) est calculé selon la formule de la consigne :

```
engagement_score = 0.25 × monthly_logins_norm
                 + 0.20 × weekly_active_days_norm
                 + 0.20 × avg_session_time_norm
                 + 0.10 × features_used_norm
                 + 0.10 × usage_growth_rate_norm
                 + 0.10 × (1 - last_login_days_ago_norm)
```

Ce score synthétise cinq dimensions d'engagement en une seule feature continue.
Il est utilisé comme feature supplémentaire dans les modèles de classification
et peut servir de variable cible pour une tâche optionnelle de prédiction d'engagement.

L'inversion de `last_login_days_ago` est intentionnelle : plus un client s'est connecté
récemment, plus son engagement est fort, donc la valeur doit croître quand les jours
s'écoulent sont faibles.
