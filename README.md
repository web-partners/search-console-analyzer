# Search Console Data Analyzer

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-beta-yellow)

Un outil Python pour collecter, analyser et exporter les données de Google Search Console. Générez facilement des rapports Excel détaillés à partir de vos données de référencement.

## 🎯 Fonctionnalités

- ✨ Authentification sécurisée via compte de service Google
- 📊 Collecte automatisée des données de Search Console
- 📈 Traitement et analyse des métriques clés (clics, impressions, CTR, position)
- 📑 Export automatique vers Excel avec tableaux de bord
- 🔄 Gestion intelligente des limites d'API et des reprises
- 📝 Logging détaillé des opérations
- 🎯 Filtrage avancé par nombre d'impressions et position
- 📊 Tri automatique des résultats par importance
- 🌐 **NOUVEAU** : Export multi-domaines avec la commande `all`
- 📁 **NOUVEAU** : Gestion automatique des dossiers de sortie
- 📈 **NOUVEAU** : Correction du calcul du CTR pour éviter les divisions par zéro
- 🌍 **NOUVEAU** : Filtrage des résultats par pays
- 📋 **NOUVEAU** : Inclusion des filtres dans le nom des fichiers d'export

## 🔧 Prérequis

- Python 3.8 ou supérieur
- Compte Google Search Console avec accès propriétaire
- Compte de service Google avec les autorisations appropriées
- Fichier de credentials du compte de service ([voir guide de configuration](docs/google-cloud-setup.md))

## 📦 Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/web-partners/search-console-analyzer.git
cd search-console-analyzer
```

2. Créez un environnement virtuel :
```bash
python -m venv sca-venv
source sca-venv/bin/activate  # Linux/Mac
# ou
sca-venv\Scripts\activate  # Windows
```

3. Installez les dépendances :
```bash
pip install -r requirements.txt
```

4. Configurez vos identifiants Google Cloud :
   - Suivez le [guide détaillé de configuration](docs/google-cloud-setup.md)
   - Placez votre fichier `credentials.json` dans le dossier `config/`

## 🚀 Utilisation

1. Exécutez le script avec les arguments requis :
```bash
python path/to/src/main.py https://votredomaine.com/ 2024-01-01 2024-01-31 path/to/config/credentials.json
```

Arguments :
- `domain` : URL du site à analyser
- `start_date` : Date de début (YYYY-MM-DD)
- `end_date` : Date de fin (YYYY-MM-DD)
- `credentials_path` : Chemin vers le fichier de credentials

Arguments optionnels :
- `--output` : Nom du fichier Excel de sortie
- `--min-impressions` : Nombre minimum d'impressions pour inclure une page (ex: 100)
- `--max-position` : Position maximale à inclure (ex: 10.0 pour la première page)
- `--country` : [Code pays à trois lettres](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3) pour filtrer les résultats (ex: fra, usa, deu)

Exemples d'utilisation :

```bash
# Analyse basique
python path/to/src/main.py https://votredomaine.com/ 2024-01-01 2024-01-31 path/to/config/credentials.json

# Avec filtres
python path/to/src/main.py https://votredomaine.com/ 2024-01-01 2024-01-31 path/to/config/credentials.json --min-impressions 100 --max-position 10.0

# Avec filtre par pays
python path/to/src/main.py https://votredomaine.com/ 2024-01-01 2024-01-31 path/to/config/credentials.json --country fra


# Avec nom de fichier personnalisé
python path/to/src/main.py https://votredomaine.com/ 2024-01-01 2024-01-31 path/to/config/credentials.json --output path/to/whatever.xlsx

# Export de tous les domaines autorisés
python path/to/src/main.py all 2024-01-01 2024-01-31 path/to/config/credentials.json

# Export multi-domaines avec nom de fichier personnalisé
python path/to/src/main.py all 2024-01-01 2024-01-31 path/to/config/credentials.json --output path/to/rapports/analyse.xlsx

# Export multi-domaines avec filtre par pays
python path/to/src/main.py all 2024-01-01 2024-01-31 path/to/config/credentials.json --country fra
```

Points importants à vérifier :

1. Forme du SITE_URL :
- Pour des propriétés de type « domaine », utilisez la syntaxe "sc-domain:example.com"
- Pour des propriétés de type « URL », utilisez l'URL de base (ex. "https://www.example.com/")
- Vérifiez la façon dont votre propriété est déclarée dans la Search Console

2. Périmètre des dates :
- L'API Search Console retourne des données sur une période glissante (max ~16 mois)
- Assurez-vous de demander une plage de dates disponible dans la Search Console

3. Authentification :
- Suivez le [guide de configuration des identifiants](docs/google-cloud-setup.md)
- Vérifiez que le compte de service a bien accès à votre propriété Search Console. Vous devez partager l'accès à votre propriété Search Console au compte de service (l'adresse e-mail affichée dans votre fichier JSON) dans l'interface Search Console.

## 📁 Structure du Projet

```
search-console-analyzer/
├── src/
│   ├── __init__.py
│   ├── main.py           # Point d'entrée
│   ├── auth.py          # Authentification Google
│   ├── data_collector.py # Collecte des données
│   ├── data_processor.py # Traitement des données
│   └── excel_generator.py # Génération des rapports
├── config/              # Configuration et credentials
├── docs/               # Documentation détaillée
├── logs/               # Fichiers de logs
├── requirements.txt     # Dépendances
└── README.md
```

## ⚙️ Configuration

1. Créez un projet dans Google Cloud Console
2. Activez l'API Search Console
3. Créez un compte de service et téléchargez les credentials
4. Ajoutez le compte de service comme propriétaire dans Search Console

Pour plus de détails, consultez le [guide de configuration](docs/google-cloud-setup.md).

## 🤝 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/amelioration`)
3. Committez vos changements (`git commit -m 'Ajout de fonctionnalité'`)
4. Pushez vers la branche (`git push origin feature/amelioration`)
5. Ouvrez une Pull Request

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 🙏 Crédits

- Google Search Console API
- Pandas pour le traitement des données
- OpenPyXL pour la génération Excel
- Loguru pour le logging

## 📧 Contact

Pour toute question ou suggestion, n'hésitez pas à :
- Ouvrir une issue
- Me contacter sur [LinkedIn](https://www.linkedin.com/in/emmanuel-fourcade-a802a5114/)
- M'envoyer un email à search-console-analyzer@webpartners.agency

---
Dernière mise à jour : Janvier 2025
Développé avec ❤️ par Web Partners