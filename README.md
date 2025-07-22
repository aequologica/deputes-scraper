# 🏛️ Téléchargeur de la liste des députés français

Ce projet vous permet de télécharger et analyser la liste des députés de l'Assemblée nationale française depuis plusieurs sources de données ouvertes.

## ⚡ Status des scripts (Juillet 2025)
- ✅ `simple_deputes_script.py` : **Fonctionnel** (618 députés + 586 avec stats)
- ✅ `deputes_downloader.py` : **Fonctionnel** (multi-sources, logging détaillé)
- ⚠️ `deputes_analysis_example.py` : **À vérifier** (dépend des données téléchargées)
- 📝 CSV endpoints NosDéputés temporairement vides → scripts automatiquement basculés sur JSON

## 🚀 Installation rapide

```bash
# 1. Cloner ou télécharger les scripts
# 2. Installer les dépendances
pip install pandas requests matplotlib seaborn

# 3. Exécuter le script simple
python simple_deputes_script.py
```

## 📊 Sources de données

### 1. **NosDéputés.fr** (Recommandé)
- **Source**: Regards Citoyens
- **URL**: `https://www.nosdeputes.fr/deputes/json` (CSV endpoint actuellement vide)
- **Avantages**: Données complètes, bien structurées, régulièrement mises à jour
- **Formats**: JSON (recommandé), XML

### 2. **Données enrichies NosDéputés**
- **Source**: NosDéputés.fr/synthese
- **URL**: `https://www.nosdeputes.fr/synthese/data/json`
- **Avantages**: Scores calculés, analyses statistiques (alternative à Datan)

### 3. **Assemblée nationale officielle**
- **Source**: data.assemblee-nationale.fr
- **Avantages**: Source officielle gouvernementale
- **Statut**: URLs officielles temporairement indisponibles (utilise NosDéputés comme alternative)

## 📋 Scripts disponibles

### 🔹 Script simple (`simple_deputes_script.py`)
```python
# Téléchargement rapide en une ligne
python simple_deputes_script.py
```
**Sortie**: `deputes_france.csv` (618 députés) et `deputes_statistiques.csv` (586 députés avec stats)

### 🔹 Script complet (`deputes_downloader.py`)
```python
# Téléchargement depuis toutes les sources avec comparaison
python deputes_downloader.py
```
**Fonctionnalités**:
- Téléchargement multi-sources (618 députés depuis 4 sources)
- Comparaison des datasets avec logging détaillé
- Dataset unifié dans `data_deputes/`
- Gestion d'erreurs avancée et URLs de secours

### 🔹 Script d'analyse (`deputes_analysis_example.py`)
```python
# Analyse des données téléchargées
python deputes_analysis_example.py
```
**Fonctionnalités**:
- Statistiques descriptives
- Graphiques automatiques
- Recherche de députés
- Export par parti

## 💡 Exemples d'utilisation

### Téléchargement basique
```python
import pandas as pd
import requests

# Télécharger directement depuis NosDéputés.fr (JSON)
url = "https://www.nosdeputes.fr/deputes/json"
response = requests.get(url)
data = response.json()

# Convertir en DataFrame
deputes_data = []
for depute_info in data['deputes']:
    depute = depute_info['depute']
    deputes_data.append(depute)

df = pd.DataFrame(deputes_data)
print(f"Nombre de députés: {len(df)}")
print(df.head())
```

### Recherche d'un député
```python
# Chercher un député par nom
resultat = df[df['nom'].str.contains('Macron', case=False)]
print(resultat[['nom', 'parti_ratt_financier', 'nom_circo']])
```

### Analyse par parti
```python
# Compter par parti
partis = df['parti_ratt_financier'].value_counts()
print(partis.head(10))
```

### Télécharger les détails d'un député
```python
import requests

# Détails complets d'un député
slug = "emmanuel-macron"  # Remplacer par le slug du député
url = f"https://www.nosdeputes.fr/{slug}/json"
response = requests.get(url)
details = response.json()
```

## 📁 Structure des données

### Colonnes principales (NosDéputés.fr)
- `nom`: Nom complet du député
- `nom_circo`: Circonscription
- `parti_ratt_financier`: Parti politique
- `profession`: Profession avant le mandat
- `sexe`: Sexe (H/F)
- `date_naissance`: Date de naissance
- `lieu_naissance`: Lieu de naissance
- `nb_mandats`: Nombre de mandats
- `twitter`: Compte Twitter (si disponible)

### Colonnes enrichies (Datan)
- `scoreParticipation`: Taux de participation aux votes
- `scoreLoyaute`: Fidélité au parti
- `scoreMajorite`: Proximité avec la majorité
- `age`: Âge calculé
- `women`: Indicateur femme/homme

## 🔧 Configuration avancée

### Personnaliser le téléchargement
```python
from deputes_downloader import DeputesDownloader

downloader = DeputesDownloader(output_dir="mes_donnees")

# Télécharger seulement depuis NosDéputés
df = downloader.download_from_nosdeputes('csv')

# Ou depuis toutes les sources
results = downloader.download_all_sources()
```

### Gestion des erreurs
```python
try:
    df = pd.read_csv(url, sep=';', encoding='utf-8')
except Exception as e:
    print(f"Erreur de téléchargement: {e}")
    # Solution de secours
    df = pd.read_csv("sauvegarde_locale.csv")
```

## 📊 Analyses possibles

1. **Démographie**: Répartition par âge, sexe, profession
2. **Géographie**: Députés par département, région
3. **Politique**: Composition de l'Assemblée par parti
4. **Activité**: Scores de participation (avec données Datan)
5. **Évolution**: Comparaison entre législatures

## 🤝 APIs complémentaires

### NosDéputés.fr API
- **Liste complète**: `https://www.nosdeputes.fr/deputes/json` (618 députés)
- **Député individuel**: `https://www.nosdeputes.fr/{slug}/json`
- **Synthèse enrichie**: `https://www.nosdeputes.fr/synthese/data/json` (586 avec stats)

### Recherche avancée
```python
# Recherche dans les interventions
search_url = "https://www.nosdeputes.fr/recherche/climat?format=json"
```

## 📝 Licence et utilisation

- **NosDéputés.fr**: Licence CC-BY-SA et ODbL
- **Assemblée nationale**: Licence Ouverte
- **Attribution requise**: Mentionner les sources

### Citation recommandée
```
Données issues de NosDéputés.fr par Regards Citoyens 
à partir de l'Assemblée nationale et du Journal Officiel
```

## 🆘 Résolution de problèmes

### CSV endpoint vide
```python
# Si le CSV est vide, utiliser le JSON
try:
    df = pd.read_csv(url, sep=';', encoding='utf-8')
except pd.errors.EmptyDataError:
    # Alternative JSON
    import requests
    response = requests.get("https://www.nosdeputes.fr/deputes/json")
    data = response.json()
    deputes_data = [d['depute'] for d in data['deputes']]
    df = pd.DataFrame(deputes_data)
```

### Timeout de téléchargement
```python
import requests

session = requests.Session()
session.headers.update({'User-Agent': 'Python-Script/1.0'})
response = session.get(url, timeout=30)
```

### Données manquantes
```python
# Vérifier la qualité des données
print(f"Valeurs manquantes:\n{df.isnull().sum()}")
```

## 🔄 Mise à jour automatique

```python
import schedule
import time

def update_data():
    # Code de téléchargement
    downloader = DeputesDownloader()
    downloader.download_all_sources()

# Mise à jour quotidienne
schedule.every().day.at("08:00").do(update_data)

while True:
    schedule.run_pending()
    time.sleep(3600)  # Vérifier chaque heure
```

## 📞 Support

- **Issues NosDéputés**: [GitHub Regards Citoyens](https://github.com/regardscitoyens/nosdeputes.fr)
- **Documentation API**: [API NosDéputés](https://github.com/regardscitoyens/nosdeputes.fr/blob/master/doc/api.md)
- **Données officielles**: [data.assemblee-nationale.fr](https://data.assemblee-nationale.fr/)

---

**Dernière mise à jour**: Juillet 2025  
**Compatibilité**: Python 3.7+