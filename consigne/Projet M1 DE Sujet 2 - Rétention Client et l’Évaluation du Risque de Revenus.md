# **Projet Data Science**

## **Projet 2 - Système Intelligent Multi-Modèles pour la Rétention Client et l'Évaluation du Risque de Revenus**

*Epreuve certifiante RNCP40875 Expert en ingénierie de données (Bloc de compétences à valider : Bloc 2)* 

Vous devez soumettre vos livrables sur **MOODLE**, en respectant la date limite fixée par votre enseignant.

Soumettez votre travail personnel. Toute tricherie ne sera pas tolérée et sera sanctionnée. Ce projet peut être réalisé en binôme.

## **Cadre Théorique et Rôle du Projet Machine Learning Supervisé, Deep Learning, Dashboarding et API**

# **Machine Learning Supervisé : Fondements, Méthodes et Rôle dans le Projet**

Le Machine Learning supervisé constitue l'un des piliers fondamentaux de l'intelligence artificielle appliquée. Il repose sur un principe simple mais puissant : apprendre automatiquement une fonction de prédiction à partir de données d'entrée (features) associées à une variable cible connue (label). Contrairement à une approche purement statistique descriptive, l'objectif n'est pas seulement de comprendre le passé, mais de généraliser à des situations futures jamais observées.

Dans un contexte business et marketing, cette capacité prédictive devient stratégique. Les entreprises SaaS, télécom ou e-commerce collectent en permanence des données relatives à leurs clients : données démographiques, fréquence d'utilisation du service, durée des sessions, historique de paiement, interactions avec le support client, satisfaction (NPS), tickets ouverts, remises appliquées, etc.

Ces informations contiennent des signaux comportementaux parfois subtils pouvant annoncer une probabilité élevée de résiliation (churn) ou une baisse significative de revenu.

Le Machine Learning supervisé permet d'exploiter ces données pour :

- Prédire la probabilité qu'un client résilie son abonnement (classification binaire),
- Identifier des segments de clients à risque (classification),
- Estimer le revenu à risque associé à un client (régression),

•

• Prédire la valeur vie client (Customer Lifetime Value CLV) (régression).

Ainsi, le modèle ne se contente pas d'analyser le passé ; il devient un outil stratégique d'aide à la décision permettant de prioriser les actions de fidélisation et d'optimiser les campagnes de rétention.

Contrairement à une simple corrélation statistique, le Machine Learning :

- apprend automatiquement des relations complexes entre comportements clients et churn,
- capture des interactions non linéaires invisibles à l'œil humain,

- s'adapte à des profils clients hétérogènes,
- permet une prise de décision automatisée et scalable à grande échelle.

Dans ce projet, vous ne devez pas vous limiter à un seul algorithme. Un des objectifs pédagogiques majeurs est de comprendre que chaque modèle possède ses hypothèses, ses forces et ses limites. Par exemple :

- Une régression logistique peut être robuste et interprétable,
- Un Random Forest peut capturer des comportements non linéaires,
- Un Gradient Boosting peut offrir de meilleures performances prédictives,
- Un réseau neuronal peut modéliser des interactions complexes entre variables comportementales.

Vous devrez comparer ces approches de manière rigoureuse afin d'identifier :

- Le modèle le plus performant,
- Le modèle le plus stable,
- Le modèle le plus interprétable,
- Le meilleur compromis performance / complexité dans un contexte business.

L'objectif n'est pas uniquement d'obtenir le meilleur score, mais de comprendre pourquoi un modèle fonctionne mieux qu'un autre dans un contexte de rétention client.

# **Deep Learning : Rôle, Intérêt et Analyse Critique**

Le Deep Learning représente une évolution du Machine Learning classique, reposant sur des réseaux de neurones artificiels multicouches capables d'apprendre des représentations hiérarchiques des données.

Dans un environnement industriel, les relations entre capteurs et événements de panne peuvent être hautement non linéaires et dépendre de combinaisons complexes de signaux. Les réseaux de neurones (MLP Multi Layer Perceptron) permettent de capturer ces interactions sans nécessiter une ingénierie de features excessive.

Dans ce projet, vous devrez obligatoirement intégrer :

- Un modèle Deep Learning telque le MLP pour une tâche de classification, ou
- Un modèle Deep Learning pour une tâche de régression.

Cependant, l'intégration du Deep Learning ne doit pas être automatique ou dogmatique. Elle doit être justifiée. Vous devrez analyser :

- Quand un modèle simple est suffisant,
- Quand un modèle plus complexe apporte un gain réel,
- Le compromis biais / variance,
- Le risque d'overfitting,
- Le coût computationnel.

Un réseau neuronal mal paramétré peut sur-apprendre et devenir instable. À l'inverse, un modèle trop simple peut sous-apprendre et ne pas capturer les dynamiques clients. L'objectif pédagogique est donc de :

1. Comprendre que le Deep Learning n'est pas toujours supérieur.

2. Apprendre à comparer scientifiquement les performances dans un contexte marketing réel.

# **Dashboarding et Data Visualization : De la Prédiction à la Décision**

Un modèle performant mais incompréhensible n'a que peu de valeur en entreprise. Dans un contexte business réel, les décideurs (CMO, responsables marketing, responsables CRM, direction financière) ont besoin d'outils visuels clairs et interactifs.

C'est pourquoi ce projet intègre obligatoirement la conception d'un dashboard décisionnel. Le dashboard n'est pas un simple affichage graphique. Il doit permettre :

- La visualisation des distributions des profils clients,
- L'analyse des facteurs influençant le churn,
- La comparaison des performances des modèles,
- La simulation d'un scénario client (ex. augmentation de la fréquence d'utilisation),
- L'obtention d'une probabilité de churn en temps réel,
- L'estimation du revenu à risque,
- L'analyse des variables les plus influentes dans la décision,
- Etc.

Vous devrez adopter une approche orientée utilisateur métier. Posez-vous les questions suivantes :

- Si j'étais responsable marketing, quelles informations seraient prioritaires ?
- Comment visualiser clairement le revenu à risque global ?
- Comment prioriser les clients à contacter ?
- Comment expliquer pourquoi un client est classé à haut risque ?

L'interface devra être développée avec Streamlit (recommandé) ou Dash. L'objectif est de transformer un modèle académique en outil stratégique de pilotage de la rétention.

#### (Cette partie est proposée à titre optionnelle)

Dans le monde professionnel, un modèle de Machine Learning n'est pas utilisé directement dans un notebook. Il peut être intégré dans une architecture logicielle plus large : CRM, plateforme marketing automation, application interne, etc.

Cette intégration passe par la mise en place d'une API REST.

Une API permet à d'autres systèmes d'interagir avec votre modèle. Par exemple :

- Un CRM pour scorer automatiquement les clients,
- Une plateforme d'emailing pour cibler les campagnes,
- Un système décisionnel interne.

Si vous choisissez cette option, vous développerez une API REST (FastAPI ou Flask) comprenant :

- Un endpoint /predict recevant les données client,
- Un endpoint /health vérifiant l'état du service,
- Optionnel : /model-info fournissant des informations sur le modèle.

L'objectif pédagogique est d'introduire la notion d'industrialisation :

- Séparation modèle / interface,
- Sérialisation du modèle,
- Gestion des erreurs,
- Structuration d'un service IA.

Cette partie reste optionnelle mais valorisante.

## **Rôle Global du Projet**

Ce projet ne consiste pas uniquement à entraîner un modèle. Il s'agit de concevoir un système intelligent complet, comprenant :

- 1. Préparation des données clients,
- 2. Modélisation multi-algorithmes,
- 3. Évaluation comparative,
- 4. Interprétabilité,
- 5. Interface utilisateur décisionnelle,
- 6. API déployable (optionnelle).

Vous adoptez ainsi une posture d'ingénieur IA ou de consultant Data capable de passer : Des données clients brutes à une plateforme stratégique d'aide à la décision pour la rétention et l'optimisation du revenu.

## **Objectifs Pédagogiques du Projet**

En réalisant ce projet, vous apprendrez à :

- Préparer un dataset réel multi-cibles
- Implémenter plusieurs algorithmes supervisés
- Comparer Machine vs Deep Learning
- Interpréter des modèles via feature importance
- Construire un pipeline complet Data / Modèle / API / Dashboard
- Travailler en équipe dans une logique projet
- Présenter une solution comme un consultant IA

# **Compétences RNCP visées (RNCP40875 - Bloc 2)**

Ce projet Data Science constitue l'un des projets majeurs de l'année.

**Ce projet permet de valider certaines compétences du Bloc 2 : BC2 - Piloter et implémenter des solutions d'IA en s'aidant notamment de l'IA générative du référentiel RNCP40875.**

Selon le référentiel, ce bloc couvre notamment :

Compétences principales évaluées :

- Collecter et préparer des données industrielles
- Concevoir et entraîner plusieurs modèles ML/DL
- Évaluer et comparer des performances

- Prototyper une solution IA complète
- Développer une API d'inférence
- Concevoir un dashboard décisionnel
- Documenter et justifier les choix techniques

#### Compétences transverses :

- Travail collaboratif
- Rigueur méthodologique
- Capacité d'analyse critique
- Présentation professionnelle

### **Veuillez consulter la grille de notation détaillée afin d'avoir une vision globale de l'ensemble des compétences, critères d'évaluation et modalités de notation.**

#### **Voici la liste des compétences de votre certification RNCP évaluées avec ce projet :**

| REFERENTIEL<br>D'ACTIVITES                                                                  | REFERENTIEL DE<br>COMPETENCES                                                                                                                                                                                                                                                                                                                                                            | CRITÈRES D'ÉVALUATION                                                                                                               |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |  |  |  |
|---------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--|--|--|
| Bloc 2 : Piloter et implémenter des solutions d'IA en s'aidant notamment de l'IA générative |                                                                                                                                                                                                                                                                                                                                                                                          |                                                                                                                                     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |  |  |  |
| A.3 -<br>Préparation et<br>visualisation de<br>données                                      | C3.1 Préparer les données en<br>les transformant et en les<br>nettoyant, en utilisant des<br>outils appropriés, en<br>collaboration avec les<br>gestionnaires et les analystes<br>de données, afin d'assurer une<br>qualité optimale et<br>universellement accessible de<br>ces dernières pour les<br>différents besoins métiers dont<br>l'analyse et le reporting.                      | Les données sont<br>préparées de<br>manière<br>qualitatives et<br>optimale.                                                         | C1 : Les outils de transformation et nettoyage des<br>données sont mobilisés efficacement ;<br>C2 : Les données transformées respectent les exigences<br>de qualité et sont adaptées aux besoins métiers ;<br>C3 : Les étapes de préparation sont bien expliquées et<br>documentées ;<br>C4 : Les données transformées sont prêtes pour<br>l'analyse et permettent l'apprentissage automatique.                                                                                                    |  |  |  |
|                                                                                             | C3.2 Élaborer une<br>communication infographique<br>visuelle inclusive en<br>construisant des tableaux de<br>bord interactifs en<br>collaboration avec les équipes<br>métiers et les data analystes<br>afin de communiquer les<br>résultats d'analyses, d'assurer<br>l'extraction de connaissances<br>en temps réel et favoriser la<br>prise de décision éclairée par la<br>gouvernance. | La communication<br>infographique<br>visuelle est<br>cohérente et<br>adaptée, et intègre<br>l'inclusivité.                          | C1 : Les visualisations créée en collaboration avec les<br>équipes métiers et les data analystes sont informatives,<br>claires, inclusives et adaptées aux besoins de la<br>gouvernance ;<br>C2 : Les graphiques sont interactifs et affichés en temps<br>réel dans le tableau de bord ;<br>C3 : Les fonctionnalités avancées des logiciels de<br>visualisation (ex. filtres, drill-down) sont exploitées ;<br>C4 : Le tableau de bord est responsif et facilite la prise<br>de décision éclairée. |  |  |  |
|                                                                                             | C3.3 Mettre en place des<br>processus d'analyse<br>exploratoire de données en<br>utilisant des techniques<br>statistiques et des outils<br>adaptés, en collaboration avec<br>les équipes métiers, pour<br>générer des insights<br>exploitables pour les décisions<br>stratégiques.                                                                                                       | Des processus<br>d'analyse<br>exploratoire de<br>données sont mis<br>en place en<br>collaboration avec<br>les parties<br>prenantes. | C1 : Les techniques statistiques et outils mobilisés sont<br>adaptés et efficaces ;<br>C2 : Les insights générés sont pertinents pour les<br>besoins métiers ;<br>C3 : Les étapes d'analyse sont bien documentées et<br>alignées sur les objectifs stratégiques.                                                                                                                                                                                                                                   |  |  |  |
| A.4 -<br>Implémentation                                                                     | C4.1 Définir une stratégie<br>d'intégration de l'IA en                                                                                                                                                                                                                                                                                                                                   | Une stratégie<br>d'intégration de l'IA                                                                                              | C1 : Les cas d'usage identifiés sont pertinents et alignés<br>avec les processus métiers ;                                                                                                                                                                                                                                                                                                                                                                                                         |  |  |  |

| d'algorithmes | identifiant les cas d'usage                                     | cohérente et                                                                                                                                         | C2 : L'impact des cas d'usage sur les processus métier                           |
|---------------|-----------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------|
| de machine    | pertinents et en évaluant leur                                  | réalisable est                                                                                                                                       | est clairement évalué et expliqué ;                                              |
| Learning      | impact sur les processus                                        | définie.                                                                                                                                             |                                                                                  |
|               | métiers, en concertation avec                                   |                                                                                                                                                      | C3 : La stratégie d'intégration est matérialisée par une                         |
|               | les responsables IA et les                                      |                                                                                                                                                      | feuille de route réalisable et répond aux objectifs de                           |
|               | responsables métiers, afin                                      |                                                                                                                                                      | transformation numérique fixés par la gouvernance.                               |
|               | d'aligner les objectifs de l'IA                                 |                                                                                                                                                      |                                                                                  |
|               | aux exigences de l'écosystème,                                  |                                                                                                                                                      |                                                                                  |
|               | aux parties prenantes ainsi                                     |                                                                                                                                                      |                                                                                  |
|               | qu'aux objectifs de la                                          |                                                                                                                                                      |                                                                                  |
|               | gouvernance.                                                    |                                                                                                                                                      |                                                                                  |
|               | C4.2 Développer des modèles                                     | Un modèle prédictif<br>efficace et<br>cohérent est                                                                                                   | C1 : Les données sont bien prétraitées et adaptées pour                          |
|               | prédictifs dont du "machine                                     |                                                                                                                                                      | la modélisation prédictive ;                                                     |
|               | learning" pour identifier de                                    |                                                                                                                                                      |                                                                                  |
|               | nouveaux comportements et                                       | développé.                                                                                                                                           | C2 : Les algorithmes de machine learning mobilisés sont<br>testés et justifiés ; |
|               | usages en collaboration avec<br>les équipes métiers et les Ops, |                                                                                                                                                      |                                                                                  |
|               |                                                                 |                                                                                                                                                      | C3 : Les codes implémentés sont fonctionnels et sans                             |
|               | afin de fournir des insights                                    |                                                                                                                                                      | erreur.;                                                                         |
|               | exploitables pour la prise de<br>décision par la gouvernance.   |                                                                                                                                                      |                                                                                  |
|               |                                                                 |                                                                                                                                                      | C4 : Les résultats du modèle prédictif répondent aux                             |
|               |                                                                 |                                                                                                                                                      | objectifs du cas métier.                                                         |
|               |                                                                 |                                                                                                                                                      |                                                                                  |
|               | C4.3 Évaluer la performance                                     | Une comparaison<br>de plusieurs<br>modèles a été<br>effectuée de<br>manière complète<br>et cohérente et<br>prenant en compte<br>l'écoresponsabilité. | C1 : Plusieurs modèles sont développés et comparés                               |
|               | des modèles de prédiction                                       |                                                                                                                                                      | avec des métriques appropriées ;                                                 |
|               | développés en analysant leurs                                   |                                                                                                                                                      | C2 : Les améliorations proposées sont pertinentes et                             |
|               | résultats à l'aide de métriques                                 |                                                                                                                                                      | expliquées (ex. gestion du surapprentissage).;                                   |
|               | adaptées ainsi que leur degré<br>d'écoresponsabilité, en les    |                                                                                                                                                      |                                                                                  |
|               | comparant avec d'autres                                         |                                                                                                                                                      | C3 : Le modèle final choisi est validé par les parties                           |
|               | modèles et en prenant en                                        |                                                                                                                                                      | prenantes comme étant le plus adapté au problème                                 |
|               | compte les besoins et attentes                                  |                                                                                                                                                      | métier et présentant un degré d'écoresponsabilité                                |
|               | des parties prenantes, pour                                     |                                                                                                                                                      | cohérent avec les objectifs fixés.                                               |
|               | garantir l'efficacité et la                                     |                                                                                                                                                      |                                                                                  |
|               | pertinence du modèle retenu.                                    |                                                                                                                                                      |                                                                                  |
|               |                                                                 |                                                                                                                                                      |                                                                                  |

## **Cahier des Charges du Projet**

## **Description du projet**

Dans le cadre de ce projet, vous devez concevoir et développer une plateforme intelligente de rétention client capable d'exploiter des données issues d'un environnement business (SaaS, télécom, services par abonnement) afin d'anticiper le risque de résiliation (churn) et d'évaluer l'impact financier associé.

Le dataset utilisé simule un environnement business réaliste dans lequel différents profils clients génèrent en continu des données comportementales telles que la fréquence d'utilisation du service, la durée des sessions, l'historique de facturation, les incidents de paiement, les interactions avec le support client, les scores de satisfaction (CSAT, NPS), ou encore le type de contrat.

L'objectif est de transformer ces données clients en un système d'aide à la décision capable de détecter des patterns annonciateurs de résiliation ou de baisse de revenu. Le système que vous développerez pourra être capable d'effectuer plusieurs tâches prédictives complémentaires, reflétant les besoins réels d'un service marketing ou CRM :

- Prédire la probabilité qu'un client résilie son abonnement (classification binaire),
- Identifier des segments clients à haut risque (classification multi-classe ou segmentation supervisée),
- Estimer le revenu à risque associé à un client (régression),
- Prédire la valeur vie client (Customer Lifetime Value CLV) (régression),
- Etc.

Cependant, dans le cadre de ce projet pédagogique, vous n'êtes pas tenus de réaliser plusieurs tâches de prédiction.

Vous devez choisir une seule tâche de prédiction de votre choix (classification ou régression). Le jeu de données contient plusieurs variables pouvant servir de variables cibles, ce qui ouvre la possibilité à différentes problématiques prédictives.

Vous sélectionnerez donc une seule tâche et construirez une solution complète et rigoureuse autour de celle-ci.

Points Bonus : Pour plusieurs tâches de prédiction.

Conseil : en autonomie, si vous le souhaitez, vous pourrez par la suite enrichir votre système en développant des composantes complémentaires (autres tâches prédictives, optimisation, monitoring, etc.) afin d'approfondir vos compétences dans le domaine de la maintenance prédictive et de la Data Science appliquée au marketing et à l'analytics décisionnel.

Ainsi, votre solution ne sera pas un simple modèle isolé, mais un véritable système intelligent intégrant plusieurs modèles, plusieurs niveaux d'analyse, et plusieurs tâches (si vous le souhaitez).

Au-delà de la performance prédictive, la plateforme devra également intégrer une interface décisionnelle interactive permettant à un utilisateur métier (par exemple un responsable marketing, CRM ou direction financière) de visualiser les indicateurs clés, simuler des scénarios clients et obtenir des prédictions en temps réel.

Le projet adopte donc une approche complète allant de l'analyse des données jusqu'à la mise à disposition opérationnelle du modèle.

## **Attention :**

Les visualisations réalisées en tant que Data Scientist pour analyser les données (EDA) et évaluer la performance des quatre modèles testés ne sont pas destinées à être intégrées telles quelles dans le dashboard final.

Ces visuels ont pour objectif d'appuyer votre démarche méthodologique, de justifier vos choix de modélisation et de comparer rigoureusement les performances des différents modèles.

Le dashboard, en revanche, constitue un outil orienté utilisateur métier. Il sera conçu en fin de projet pour permettre à un responsable marketing ou CRM de :

- Visualiser les indicateurs clés de performance (KPI),
- Identifier le nombre de clients à risque,
- Estimer le revenu global à risque,
- Simuler des scénarios en modifiant certains paramètres client (ex. amélioration de l'engagement),
- Obtenir des prédictions en temps réel à partir de nouvelles données.

Il est donc essentiel de bien distinguer les visualisations d'analyse scientifique (destinées à votre rapport technique) et l'interface décisionnelle opérationnelle (destinée à l'utilisateur final).

# **Objectif**

L'objectif de ce projet est de concevoir un MVP (Minimum Viable Product) professionnel intégrant l'ensemble des briques fondamentales d'un système d'intelligence artificielle business.

Vous devrez combiner plusieurs dimensions complémentaires :

- Une dimension Data Science, incluant le nettoyage, la préparation des données, la modélisation supervisée et l'évaluation rigoureuse des performances.
- Une dimension comparative, imposant l'implémentation de plusieurs algorithmes de Machine Learning et de Deep Learning afin d'analyser leurs performances respectives et d'identifier le modèle le plus pertinent dans ce contexte business.
- Une dimension décisionnelle, matérialisée par le développement d'un dashboard interactif permettant d'exploiter les prédictions de manière claire et exploitable par un utilisateur métier.

#### (optionnel) :

- Enfin, une dimension d'industrialisation, via la mise en place d'une API REST permettant d'exposer le modèle sous forme de service, comme cela serait fait dans un environnement professionnel réel.

En résumé, ce projet vise à vous placer dans une posture d'ingénieur ou de consultant en intelligence artificielle, capable de concevoir non seulement un modèle performant, mais une solution complète, robuste, explicable et prête à être intégrée dans un système opérationnel.

## **Dataset**

Vous pouvez trouver le dataset sur Kaggle :

<https://www.kaggle.com/datasets/miadul/customer-churn-prediction-business-dataset> Il s'agit du *customer\_churn.csv* Dataset.

#### Caractéristiques :

- 10 000 enregistrements (clients)
- Variables numériques et catégorielles
- Variable cible principale : churn (0 = No, 1 = Yes)
- Données synthétiques mais générées selon une logique métier réaliste
- Corrélations cohérentes entre comportements clients et probabilité de churn

### Variables clés (exemples) :

- age
- gender
- tenure
- contract\_type
- monthly\_charges
- total\_revenue
- payment\_failures
- support\_tickets
- session\_duration
- login\_frequency
- nps\_score
- churn

Consultez Kaggle pour plus d'informations.

# **Problématiques prédictives possibles**

Avec les variables de ce dataset, vous pouvez construire plusieurs problématiques prédictives pertinentes, en classification et en régression, voire en scoring stratégique.

## **La tâche prédictive la plus naturelle du dataset est :**

**Prédiction du Churn (Classification Binaire) : Identifier les clients susceptibles de résilier leur abonnement.** 

(Variable cible : churn)

#### Intérêt business :

- Prioriser les actions de rétention
- Réduire le coût d'acquisition
- Stabiliser le chiffre d'affaires

## **Autres tâches prédictives possibles du dataset**

## **Estimation du Revenu à Risque (Régression) : Combien l'entreprise risque-t-elle de perdre si ces clients churnent ?**

(Nouvelle variable cible :

revenue\_at\_risk = total\_revenue \* proba\_churn ou expected\_loss = monthly\_fee \* probabilité\_churn) Intérêt business :

- Priorisation des clients à forte valeur
- Arbitrage budget marketing
- Optimisation des campagnes

### **Estimation du Revenu à Risque (Régression) : Combien l'entreprise risque-t-elle de perdre si ces clients churnent ?**

(Nouvelle variable cible possible : revenue\_at\_risk = total\_revenue \* proba\_churn Ou expected\_loss = monthly\_fee \* probabilité\_churn) Intérêt business :

- Priorisation des clients à forte valeur
- Arbitrage budget marketing
- Optimisation des campagnes

#### **Estimation de la Valeur Vie Client CLV (Régression) : Estimer la valeur future d'un client en fonction de son comportement.**

(Variable cible : total\_revenue)

Intérêt business :

- Identifier clients premium
- Adapter les offres
- Segmenter intelligemment

#### **Prédiction de l'Engagement Client (Régression ou Classification)**

**(Régression)** Créer un score d'engagement basé sur : monthly\_logins, weekly\_active\_days, avg\_session\_time, features\_used, usage\_growth\_rate

- Chaque variable doit être normalisée (MinMax ou StandardScaler).
- e.g. de formule du score (continu entre 0 et 1) :

```
 =
          0.25 ∗ ℎ + 0.20 ∗ 
                                          + 0.20 ∗ 
          +0.1 ∗  + 0.1 ∗ ℎ
                                         + 0.10 ∗ (1 − ___)
     (N.B. On inverse last_login_days_ago car plus c'est élevé, moins l'engagement est fort.)
(Classification) ou prédire l'engagement (faible, moyen, fort)
```

## **Prérequis et exigences principales**

- L'analyse doit inclure au minimum 4 modèles différents
- Au moins 1 modèle Deep Learning
- Comparaison quantitative obligatoire
- Dashboard interactif obligatoire
- API fonctionnelle (optionnel)
- Interprétation de l'importance de features
- Interprétation du modèle
- Séparation train/test rigoureuse
- Cross-validation recommandée

## **Résultats attendus**

- Comparaison détaillée des performances
- Choix justifié du meilleur modèle
- Dashboard fonctionnel
- API accessible (optionnel)
- Rapport analytique structuré

## **Recommandations:**

La réussite de ce projet ne repose pas uniquement sur l'implémentation de modèles performants, mais sur une démarche méthodologique rigoureuse, structurée et défendable. L'objectif est que vous soyez capables de passer d'un dataset brut à une solution complète (analyse, modèles, évaluation et dashboard), tout en justifiant vos choix comme dans un contexte professionnel réel. Les recommandations ci-dessous vous guideront tout au long du projet.

Voici les recommandations essentielles pour vous guider tout au long du développement de votre solution :

## **Recommandations:**

La réussite de ce projet ne repose pas uniquement sur l'implémentation de modèles performants, mais sur une démarche méthodologique rigoureuse, structurée et défendable. L'objectif est que vous soyez capables de passer d'un dataset brut à une solution complète (analyse, modèles, évaluation et dashboard), tout en justifiant vos choix comme dans un contexte professionnel réel. Les recommandations ci-dessous vous guideront tout au long du projet.

Voici les recommandations essentielles pour vous guider tout au long du développement de votre solution :

#### **Commencez par une analyse exploratoire approfondie**

Avant toute modélisation, prenez le temps de comprendre vos données : distributions, valeurs extrêmes, cohérence des variables capteurs, présence de valeurs manquantes, éventuelles anomalies et relations entre variables. Une EDA bien menée vous permet de construire une intuition métier : par exemple, identifier quelles plages de vibration ou de température semblent associées à un risque plus élevé. Cette étape sert également à repérer des problèmes invisibles au premier regard (variables constantes, unités incohérentes, valeurs aberrantes, etc.), qui peuvent dégrader fortement les performances.

### **Vérifiez les distributions des classes**

Dans un problème de churn, il est fréquent que la classe churn = 1 soit minoritaire. Un modèle peut donc afficher une accuracy élevée tout en étant inefficace pour détecter les clients réellement à risque. Dans ce cas, un modèle peut afficher une accuracy élevée tout en étant mauvais pour détecter les churners. Vous devez donc analyser le déséquilibre des classes et privilégier des métriques adaptées (Recall, F1, PR-AUC), voire appliquer des stratégies

appropriées (stratified split, class\_weight, ajustement du seuil de décision). L'objectif est de produire un modèle utile dans un scénario réaliste, où les faux négatifs (churners non détectée) peuvent coûter très cher. L'objectif est de produire un modèle utile dans un scénario business réaliste, où manquer un client à forte valeur peut coûter très cher.

#### **Analysez la corrélation des variables et la redondance des variables**

L'étude des corrélations et des relations entre features est importante pour comprendre la structure des données, identifier les variables redondantes et limiter certains risques (multicolinéarité, surinterprétation de variables très liées). Parfois, une variable dérivée est plus pertinente qu'une variable brute (ex. ratio support\_tickets / tenure\_months, évolution d'usage via usage\_growth\_rate). L'objectif n'est pas de supprimer mécaniquement des variables, mais de comprendre leur rôle dans le comportement client.

### **Implémentez d'abord un modèle baseline simple, puis complexifiez progressivement**

Commencez par un modèle simple (e.g. régression logistique, régression linéaire, ou autre) pour établir un point de référence. Ce baseline vous permet de mesurer objectivement le gain apporté par des modèles plus complexes. Ensuite, introduisez progressivement d'autres modèles plus puissants (e.g. Random Forest, Gradient Boosting, Support Vector Machine, MLP, etc.). Cette progression est essentielle : elle vous aide à comprendre ce que chaque famille de modèles apporte, et à éviter de brûler les étapes en allant directement vers du deep learning sans justification.

### **Ajoutez progressivement des modèles plus complexes :**

### **Comparez systématiquement au moins 4 modèles et choisissez un modèle candidat final**

Un attendu clé du projet est la comparaison multi-modèles. Vous devez implémenter au minimum quatre modèles (ML classiques et au moins un modèle DL) et comparer leurs résultats de manière structurée. À l'issue de cette comparaison, vous devrez sélectionner un modèle candidat final, c'est-à-dire le modèle que vous recommanderiez dans un contexte réel. Ce choix doit être argumenté en prenant en compte plusieurs dimensions : performance, stabilité, interprétabilité, coût de calcul, facilité de déploiement et cohérence métier. Le meilleur modèle n'est pas forcément celui qui a le meilleur score, mais celui qui représente le meilleur compromis pour l'usage visé.

Utilisez des métriques adaptées à chaque tâche (classification ou régression). Présentez vos résultats sous forme de tableaux comparatifs et de visualisations claires. La comparaison doit être structurée et argumentée, et non simplement descriptive.

## **Évitez le data leakage : un impératif méthodologique**

Le data leakage est l'une des erreurs les plus fréquentes en Data Science. Vous devez garantir que les données de test ne contaminent jamais l'entraînement : les étapes de preprocessing (imputation, scaling, encodage) doivent être ajustées uniquement sur le train set puis appliquées au test set. L'usage de pipelines (sklearn.Pipeline, ColumnTransformer) est fortement recommandé pour sécuriser ce point. Un projet présentant une fuite de données compromet la validité des résultats.

#### **Utilisez la validation croisée si pertinent et évaluez la robustesse**

Lorsque c'est pertinent, utilisez une validation croisée (cross-validation) afin de rendre vos résultats plus robustes et moins dépendants d'un split unique. Cela permet aussi de mieux comparer les modèles, notamment si les données sont hétérogènes. L'objectif est de montrer que votre modèle généralise réellement et n'est pas performant uniquement sur un découpage favorable.

#### **Optimisez les hyperparamètres de manière raisonnable et justifiée**

Vous pouvez utiliser GridSearch ou RandomizedSearch, mais l'optimisation doit être maîtrisée : expliquez votre stratégie, sélectionnez des plages réalistes, et évitez les recherches excessives non justifiées. L'objectif n'est pas de "tuner" au maximum, mais de montrer une démarche rationnelle : améliorer la performance tout en gardant un modèle stable et reproductible**.**

#### **Analysez les erreurs : comprendre les limites fait partie du travail**

Ne vous contentez pas de scores globaux. Vous devez analyser les erreurs : matrices de confusion en classification, résidus en régression, exemples de cas mal prédits, et discussion des raisons possibles (bruit, variables insuffisantes, classes proches, etc.). Cette analyse est essentielle pour formuler des recommandations réalistes (ex. besoins en données supplémentaires, ajout de nouvelles features, ajustement du seuil d'alerte).

### **Travaillez l'interprétabilité : expliquer est souvent aussi important que prédire**

Utilisez des techniques d'importance des variables ou SHAP pour expliquer les décisions du modèle.

Dans un environnement orienté client, un modèle n'est pas évalué uniquement sur sa performance statistique. Il doit être compréhensible, justifiable et actionnable.

- ➢ Un responsable CRM ou marketing doit pouvoir répondre à des questions telles que :
- Pourquoi ce client est-il classé à haut risque de churn ?
- Quels facteurs expliquent cette probabilité élevée ?
- Est-ce lié au prix, à l'engagement, au support client ou à un problème de paiement ?
- Quelle action concrète peut être mise en place pour réduire ce risque ?
- ➢ C'est pourquoi vous devez intégrer des techniques d'explicabilité, telles que l'importance des variables (feature importance) ou, idéalement, SHAP.
- ➢ L'objectif est de produire des explications claires, exploitables et cohérentes avec la logique métier. Par exemple :
- Une forte baisse de l'activité récente augmente le risque de churn,
- Des échecs de paiement répétés sont un signal critique,
- Un faible NPS est un indicateur précurseur de départ,
- Un nombre élevé de tickets support combiné à un temps de résolution long peut accroître la probabilité de résiliation.
- ➢ Vous devez également être capables d'interpréter ces résultats de manière critique :
- Identifier les variables réellement déterminantes,
- Distinguer causalité et simple corrélation,
- Repérer des variables fortement corrélées entre elles,
- Discuter des limites de l'explication (dépendance au modèle choisi, instabilité selon les splits, influence du déséquilibre des classes).

Un bon modèle prédictif doit permettre non seulement d'anticiper le churn, mais aussi d'éclairer les décisions stratégiques : ciblage marketing, ajustement tarifaire, amélioration du support ou personnalisation des offres.

Ainsi, l'interprétabilité transforme un modèle statistique en véritable outil décisionnel.

### **N.B. : Quand applique-t-on les techniques d'explicabilité (Feature Importance, SHAP) ?**

Quand applique-t-on les techniques d'explicabilité (Feature Importance, SHAP) ? Les techniques d'explicabilité s'appliquent après l'entraînement du modèle, lors de la phase d'évaluation et d'interprétation des prédictions.

En effet, ces méthodes visent à expliquer les décisions d'un modèle déjà entraîné. Elles permettent de répondre à la question essentielle : Pourquoi le modèle a-t-il produit cette prédiction ?

Sans modèle entraîné et sans prédictions, il n'y a rien à interpréter.

| Technique              | Quand l'utiliser                | Niveau     |
|------------------------|---------------------------------|------------|
| feature_importances_   | Après entraînement              | Basique    |
| Permutation Importance | Après évaluation                | Recommandé |
| SHAP                   | Sur le modèle final sélectionné | Avancé     |

### **Feature Importance (importance globale)**

La Feature Importance permet d'identifier quelles variables influencent le plus le modèle dans son ensemble.

Elle Analyse le comportement général du modèle pour une vision globale (macro)

e.g : : le nombre d'échecs de paiement (payment\_failures) est la variable la plus influente dans la prédiction du churn.

## Plusieurs techniques possibles :

- Importance native des modèles basés sur les arbres (Random Forest, Gradient Boosting, XGBoost, LightGBM...)

model.feature\_importances\_

Ces modèles calculent automatiquement une importance basée sur la réduction d'impureté : Gini importance (classification), Gain / réduction de variance (régression)

- Permutation Importance (recommandée)

from sklearn.inspection import permutation\_importance Méthode agnostique au modèle (fonctionne avec tous les algorithmes).

#### Principe :

- 1. Mesurer la performance initiale du modèle
- 2. Mélanger (permuter) une variable
- 3. Recalculer la performance
- 4. Observer la perte de performance : Plus la performance chute, plus la variable est importante.

#### **SHAP (explicabilité locale et globale)**

SHAP est une méthode avancée d'explicabilité. Elle explique pourquoi une prédiction précise a été faite, pour aller plus loin que la Feature Importance classique. Elle permet de :

- expliquer une prédiction individuelle (vision locale) e.g. Pourquoi ce client précis a-t-il une probabilité de churn de 0.82 ? Est-ce dû à un faible usage récent, un NPS bas ou des échecs de paiement répétés ?
- obtenir une importance globale des variables : Quelles variables influencent le modèle en général ?
- identifier l'impact positif ou négatif de chaque variable sur une prédiction donnée.

e.g. Une augmentation des support\_tickets peut accroître la probabilité de churn. Un usage\_growth\_rate positif peut réduire le risque.

Une forte ancienneté (tenure\_months élevée) peut stabiliser le client.

#### **Structurez proprement votre code**

Organisez votre projet en modules (data preprocessing, modeling, evaluation, API, dashboard). Évitez un notebook monolithique désorganisé.

- ➢ Un projet Data Science professionnel ne se résume pas à un notebook unique. Vous devez organiser votre solution comme un mini-produit logiciel, avec une structure claire et maintenable.
- ➢ Séparez les responsabilités : préparation des données, entraînement, évaluation, visualisation/dashboard. Un notebook peut être conservé pour l'EDA et l'expérimentation, mais le pipeline final doit pouvoir être exécuté sans dépendre d'un notebook monolithique désorganisé. Cette structuration facilite aussi le travail en équipe et la reproductibilité.

#### **Versionnez votre travail régulièrement avec Git**

Cela vous permettra de suivre vos évolutions et d'éviter la perte de travail.

➢ Le versioning est une bonne pratique incontournable. Utiliser Git vous permet de garder une trace de vos évolutions, de revenir en arrière en cas d'erreur, de travailler efficacement en équipe, et de structurer la collaboration (branches, pull requests, revue de code). Vous devez effectuer des commits réguliers et explicites, reflétant l'avancement réel du projet : nettoyage, ajout d'un modèle, amélioration des features, ajout du dashboard, intégration API, etc. Un dépôt Git propre et vivant constitue un indicateur fort de maturité professionnelle.

#### **Dashboard : indépendant, exploitable, orienté décision**

Votre dashboard (Streamlit, Dash/Plotly...) doit être conçu comme un outil décisionnel autonome. Il doit permettre de visualiser les données, d'explorer des indicateurs clés, de comparer les modèles, et d'exécuter des prédictions sur des scénarios saisis par l'utilisateur. L'objectif est de rendre le projet utilisable par un profil métier, même si le code n'est pas exécuté dans un notebook. Le dashboard est donc une composante centrale, et non un simple bonus visuel.

# **(optionnel) Industrialisation via API : pour aller plus loin**

#### **Testez votre API indépendamment du dashboard**

Assurez-vous que vos endpoints fonctionnent correctement avant l'intégration dans l'interface.

- ➢ Avant d'intégrer votre modèle dans le dashboard, vous devez valider que votre API fonctionne parfaitement seule. Trop souvent, des projets échouent à la fin car l'API n'a jamais été testée sérieusement.
- ➢ Vérifiez donc vos endpoints dès le début : envoyez des requêtes avec Postman, curl, ou un script Python, et assurez-vous que /predict renvoie exactement ce qui est attendu, avec une gestion robuste des erreurs (champs manquants, types incorrects, valeurs incohérentes).
- ➢ Le dashboard ne doit être qu'une couche de présentation ; il ne doit pas compenser les faiblesses de l'API. Une API testée en amont vous garantit une intégration fluide, rapide et stable.

#### **Pourquoi industrialiser votre solution en l'exposant via une API REST**

Afin de rapprocher le projet d'un usage professionnel réel, votre modèle ne doit pas uniquement fonctionner dans un notebook. Vous devez l'industrialiser en l'exposant via une API REST (FastAPI ou Flask). Cette API jouera le rôle de service d'inférence : elle recevra des données en entrée, appliquera le pipeline de préparation, chargera le modèle entraîné, puis renverra la prédiction.

### L'API devra inclure au minimum :

- POST /predict : reçoit un JSON contenant les features (capteurs) et renvoie la prédiction (classe et/ou probabilité pour la classification, valeur pour la régression).
- GET /health : endpoint de santé permettant de vérifier que le service est actif et que le modèle est correctement chargé.
- Gestion des erreurs : validation des entrées (features manquantes, types incorrects, valeurs hors plage), message d'erreur clair et code HTTP approprié.
- Documentation minimale : description du format d'entrée/sortie (ex. exemple de requête et réponse), soit dans le README, soit via la doc auto (Swagger/FastAPI).

Important : le dashboard devra idéalement appeler l'API pour obtenir les prédictions (et non charger directement le modèle), afin de reproduire une architecture réaliste (Front / API / Modèle).

### **Adoptez une posture professionnelle**

Documentez vos choix, justifiez vos décisions, argumentez vos comparaisons. Votre rapport doit refléter une démarche scientifique structurée.

- ➢ Ce projet évalue aussi votre capacité à travailler comme un ingénieur IA ou un consultant Data. Votre rapport et votre présentation doivent refléter une démarche scientifique rigoureuse : expliquer vos choix, justifier vos décisions, comparer vos modèles de façon argumentée, et discuter les limites.
- ➢ Il ne s'agit pas d'aligner des scores, mais de raconter une analyse structurée : Pourquoi ces features ? Pourquoi ce modèle final ? Quels compromis entre performance, coût et interprétabilité ? Quels risques (biais, surapprentissage, dérive des données) ? Quelles recommandations opérationnelles ?
- ➢ Votre valeur ajoutée se mesure dans votre capacité à produire une solution claire, défendable, reproductible, et applicable dans un contexte réel.

En résumé, l'objectif n'est pas seulement d'obtenir le meilleur score possible, mais de démontrer votre capacité à construire une solution complète, robuste, explicable et exploitable. L'industrialisation par API est une extension optionnelle pour les groupes qui souhaitent approfondir et valoriser une approche plus proche des pratiques professionnelles.

# **Exigences Fonctionnelles Détaillées (EF)**

#### **EF1 : Acquisition et Préparation des Données**

Vous devez mettre en place un pipeline de préparation incluant : nettoyage des valeurs manquantes, encodage des variables catégorielles, normalisation/standardisation si nécessaire, et analyse exploratoire documentée.

#### **EF2 : Modélisation Multi-Algorithmes**

Vous devez entraîner et comparer au minimum 4 modèles (classification et/ou régression selon votre choix), incluant des modèles de référence et des modèles plus avancés. Vous devez sélectionner et justifier un modèle candidat final.

## **EF3 : Système d'Évaluation**

Vous devez utiliser des métriques adaptées (classification : Accuracy, Precision, Recall, F1, ROC-AUC ; régression : MAE, RMSE, R²...) et produire des comparatifs (tableaux et graphes) ainsi qu'une analyse d'erreurs.

### **EF4 : Dashboard Interactif (Obligatoire)**

Votre interface doit permettre la saisie d'un scénario, afficher la prédiction, comparer les modèles, montrer l'importance des variables et intégrer des graphiques interactifs. Framework conseillé : Streamlit (ou Dash/Plotly).

### **EF5 : API** (optionnelle)

Si vous choisissez l'option industrialisation, vous développerez une API REST exposant au minimum : POST /predict, GET /health, gestion des erreurs, et documentation minimale (README ou Swagger/FastAPI).

## **Livrables :**

- **Vous devez soumettre les livrables sur MOODLE et Git/GitHub** (optionnel) :
  - o **Code source de la solution fonctionnelle** (+ documentation technique en annexe (optionnel) )
  - o **Rapport du projet**
  - o **Support de Présentation du projet**
- Présentation et démonstration en classe **lors de la dernière séance du module** : Tous les membres du groupe doivent participer ; **Evaluation/Note individuelle**)
- Grille d'évaluation est partagée dans un document séparé.

**GOOD LUCK!**