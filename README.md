# BloodHub

BloodHub est une application web développée avec Dash qui permet de visualiser et prédire l'éligibilité au don de sang. L'application comprend trois principales sections : accueil, profil et prédiction IA.

## Fonctionnalités

- **Page d'accueil** : Visualisation de la distribution géographique des donneurs sur une carte interactive et statistiques sur les conditions médicales
- **Page Profil** : Analyse détaillée des profils des donneurs avec des graphiques interactifs
- **Page IA** : Prédiction de l'éligibilité au don de sang basée sur différents critères médicaux

## Structure du Projet

```
BloodHub/
├── api/
│   ├── model.pkl
│   └── predict.py
├── assets/
│   ├── front.svg
│   ├── back.svg
│   └── cameroon_map.html
├── data/
│   ├── data.csv
│   └── df_final.xlsx
├── pages/
│   ├── home.py
│   ├── profil.py
│   └── ai.py
├── app.py
├── requirements.txt
└── README.md
```

## Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)
- Environnement virtuel (recommandé)

## Installation

1. Cloner le dépôt :
```bash
git clone <url-du-repo>
cd BloodHub
```

2. Créer et activer un environnement virtuel (optionnel mais recommandé) :
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# ou
venv\Scripts\activate  # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Configuration

1. Assurez-vous que les fichiers de données sont présents dans le dossier `data/`
2. Le modèle ML doit être présent dans `api/model.pkl`

## Lancement de l'application

1. Démarrer l'API FastAPI :
```bash
uvicorn api.predict:app --reload
```

2. Dans un autre terminal, lancer l'application Dash :
```bash
python app.py
```

3. Accéder à l'application dans votre navigateur :
- Application principale : http://localhost:8050
- Documentation API : http://localhost:8000/docs

## Utilisation

### Page d'accueil
- Visualisation de la carte des donneurs
- Filtrage par arrondissement et quartier
- Statistiques sur les conditions médicales

### Profil Type
- Visualisation des statistiques démographiques
- Analyse par groupe d'âge et groupe sanguin
- Graphiques interactifs des types de donation

### Prédiction IA
- Formulaire de saisie des informations médicales
- Prédiction de l'éligibilité au don
- Visualisation des probabilités pour chaque catégorie

## Développement

- L'application utilise Dash pour l'interface utilisateur
- FastAPI pour l'API de prédiction
- Dash Bootstrap Components pour le style
- Plotly pour les visualisations
- Folium pour la carte interactive

## Licence

[À spécifier]

## Contact

[À spécifier]