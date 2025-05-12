
# 🏛️ Assistant Hippocratique : RAG basé sur les Aphorismes d'Hippocrate

> “Je jure par Apollon médecin, par Asclépios, Hygie et Panacée…”  
> — Serment d’Hippocrate

## 📌 À propos

Ce projet est une **application web interactive utilisant un système RAG (Retrieval-Augmented Generation)** basé sur les célèbres **Aphorismes d'Hippocrate**, destinée à explorer et se familiariser avec ces textes anciens fondements antique à grace à l'intelligence artificielle.

Il permet à tout utilisateur de poser des questions liées aux aphorismes, et reçoit une réponse contextuelle construite à partir des textes originaux enrichis par un modèle de langage (ex: Mistral).

---

## 🔍 Objectifs du projet

- ✨ Explorer une base historique de textes hippocratiques anciens
- 🧠 Utiliser le RAG pour améliorer l'apprentissage interactif
- 📚 Mettre en avant les principes hippocratiques dans un format numérique moderne
- 🧑‍⚕️ Inspirer une approche pédagogique de la redécouverte des textes de la médécine ancienne

---

## ⚖️ Enjeux pédagogiques et éducatifs

### 🧑‍🏫 1. Vulgarisation des textes fondamentaux de la médécine hippocratique

- Permet aux utilisateur de d'explorer et de se familiariser avec les fondements historiques de la médécine.
- Favorise l’apprentissage critique grâce à l'ancrage dans des textes fondateurs.
- Ouvre à une réflexion sur l’évolution de la pensée médicale depuis l’Antiquité.

### 📚 2. Apprentissage interactif

- Introduit une méthode pédagogique active où l’utilisateur pose des questions et reçoit des réponses contextualisées.
- Permet de travailler la compétence "recherche documentaire + synthèse" via un assistant IA.
- Encourage l'autonomie dans l'apprentissage avec suivi personnalisé.

### 🧠 3. Référentiel Sémantique Médical Ancien

- Exploration d’un corpus ancien par des techniques modernes de traitement du langage naturel.
- Première étape vers la création de référentiels médicaux anciens accessibles par NLP.
- Application potentielle à d’autres textes médicaux classiques (Galien, Avicenne, etc.)

### 4. Exemple pratique d'implémentation d'un RAG
- Exemple pédagogique de conception et de mise en oeuvre d'un RAG basé sur un document pdf.

---

## 🤖 Fonctionnement technique

### 🧠 1. Base de connaissances

Les **Aphorismes d'Hippocrate** sont :
    - Extraits du pdf livre ancien "Aphorismes d'Hippocrate traduit en français, .. par E. Littré, Paris, Chez J.B. Baillère, 1844. Source : 
    - Découpé et stockés dans un fichier JSON (`data/hippocrate_rag_data.json`) 
    - et intégrés dans un index FAISS après encodage sémantique avec un modèle de type **Sentence-BERT (camembert-large)**.

### 🔍 2. Recherche vectorielle

À chaque question posée :
1. La requête est encodée en vecteur avec le même modèle.
2. Une recherche par plus proches voisins est effectuée dans l’index FAISS.
3. Les passages les plus pertinents sont récupérés.

### 🧾 3. Génération de réponse

La réponse est générée par un **modèle LLM open-source (Mistral)** via **Ollama**, qui reformule la réponse en français, sur la base des extraits trouvés.

---

## 🧰 Technologies utilisées

| Technologie | Utilisation |
|------------|-------------|
| Flask      | Backend API web |
| Bootstrap 5.3 | Interface responsive |
| Sentence-BERT | Encodage sémantique |
| FAISS      | Indexation vectorielle |
| Mistral (Ollama) | Génération de réponses |
| Docker     | Déploiement portable |
| Bleach     | Sécurisation HTML |

---

## 📦 Prérequis

- Python 3.9+
- Docker (optionnel mais recommandé)
- Accès à Ollama (ou autre serveur LLM compatible)

---

## 🚀 Démarrage rapide

### Avec Docker Compose (recommandé)

```bash
docker-compose up --build
```

L’application sera accessible à l’adresse : [http://localhost:5000](http://localhost:5000)

```bash
docker exec -it my-ollama ollama run mistral
```

### Ou en mode développement local

préparer l'environnement virtual
```bash
python -m venv .venv
```
Sous mac os / linux : 
```bash
source .venv/bin/activate
```
Sous windows CMD :
```bash
.venv\Scripts\activate
```
Installer les librairies nécessaires pour le projet
```bash
pip install -r requirements.txt
```

Assurer vous que ollama est installé et démarrer ollama
```bash
ollama serve
```

Démarrer le modele LLM qui sera appelé par le RAG (mistral dans ce projet)
```bash
ollama run mistral
```

lancer l'assitant IA hippocratique
```bash
python app.py
```

Accéder à l'interface de l"'assistant IA Hippocratique à l'adresse
[http://localhost:5000](http://localhost:5000)

---

## 🗂 Structure du projet

```
.
├── data/
│   ├── aphorisms_extracted.json    # Corpus des aphorismes
│   ├── hippocrates_questions.json  # Questions prédéfinies (pour UI)
│   └── hippocrate_rag_data.json    # Corpus des aphorismes
├── models/
│   └── config_schema.py            # Schéma de configuration Pydantic pour le RAG
├── prepare_corpus/
│   └── process_pdf.ipynb           # Notebook qui prépare le Corpus du RAG à partir du document pdf sur les Aphorismes d'Hippocrate
├── rag/
│   └── hippocrate.py               # Construction de l'index FAISS, fonction de recherche dans l'index, fonction d'appel du LLM
├── templates/
│   └── index.html                  # Template Jinja
├── app.py                          # Point d'entrée Flask
├── config_loader.py                # Loader of rag configuration yaml file
├── Dockerfile                      # Docker
├── docker-compose.yml              # Orchestration
├── rag_config.yaml                 # Configuration file of the RAG (Flask application, embedding model, llm, data path, security, ...)
└── requirements.txt                # Dépendances Python
```

---

## Préparation du corpus pour le RAG hippocratique: prepare_corpus/process_pdf.ipynb

Dans le cadre de la mise en place d’un système de **RAG (Retrieval-Augmented Generation)** centré sur les *Aphorismes d’Hippocrate*, il est essentiel de préparer un **corpus textuel structuré, propre et adapté** aux exigences techniques des modèles de recherche sémantique et de génération.

### 📄 Source du corpus
Les données proviennent d’une édition ancienne numérisée :
- **Titre** : *Aphorismes d'Hippocrate*, traduits par Émile Littré  
- **Format numérique** : PDF issu de l’archive [archive.org](https://archive.org/details/aphorismesdhippo00hipp)  
- **Pages concernées** : 96 à 260, correspondant à la traduction française principale  

### 🔧 Étapes de préparation

1. **Téléchargement et stockage local du PDF**
   - Le document a été téléchargé depuis son adresse source et sauvegardé localement dans le répertoire `km/aphorismes_hippocrate.pdf`.
   - Ce téléchargement automatisé facilite la reproductibilité du pipeline.

2. **Extraction du texte brut**
   - À l’aide de la bibliothèque **PyMuPDF (fitz)**, chaque page pertinente a été analysée pour extraire son contenu textuel.
   - Les paragraphes ont été segmentés grâce à l’analyse des espacements verticaux entre lignes, permettant d’éviter l’intégration des notes de bas de page.

3. **Nettoyage du texte**
   - Suppression des tirets en fin de ligne pour fusionner les mots coupés.
   - Correction automatique des erreurs de numérotation (remplacement des virgules par des points après les chiffres).
   - Normalisation des titres de sections (`PREMIÈRE SECTION` → `SECTION.1`, etc.).

4. **Extraction structurée des aphorismes**
   - Chaque aphorisme a été identifié par son numéro (ex. `01`, `23`) et extrait sous forme d’un objet JSON contenant :
     - Numéro de l’aphorisme
     - Texte associé
     - Page source
     - Section thématique
   - Gestion fine des cas où un aphorisme est coupé sur deux pages consécututives.

5. **Segmentation adaptée au RAG (Chunking)**
   - Afin de répondre aux contraintes techniques des modèles d’embedding et de LLM :
     - Les aphorismes courts (< 450 caractères) sont conservés tels quels.
     - Les aphorismes moyens (450–800 caractères) sont découpés en deux segments.
     - Les plus longs (> 800 caractères) sont divisés en trois parties avec un léger chevauchement.
   - Cette segmentation assure une bonne couverture contextuelle lors du retrieval.

6. **Format final pour le RAG**
   - Un document type inclut :
     - Un identifiant unique (`s1.aph_01.p100`)
     - Le texte segmenté
     - Des métadonnées précises (section, page, source)
   - Une introduction contextuelle a également été ajoutée pour enrichir les réponses générées.

### ✅ Résultat final
Le corpus est désormais prêt à être intégré dans un moteur de recherche vectorielle (comme FAISS, Chroma ou Elasticsearch), suivi d’une phase de génération assistée par un modèle de langage (LLM). Il constitue une base solide pour interpréter, analyser et dialoguer avec les *Aphorismes d’Hippocrate* à travers une approche moderne de traitement du langage naturel.

---

## 🛠️ Configuration du système RAG Hippocratique

Le fichier `rag_config.yaml` centralise tous les paramètres de configuration du système **HippocRAG**, permettant une gestion modulaire et flexible des différents composants : application web, moteur de recherche sémantique (RAG), modèle de langage (LLM) et règles de sécurité.

---

### 🖥️ Configuration de l'application Flask

| Paramètre        | Valeur par défaut                   | Description |
|------------------|-------------------------------------|-------------|
| `name`           | `"HippocRAG"`                       | Nom de l’application |
| `debug`          | `true`                              | Active le mode debug pour le développement |
| `host`           | `"0.0.0.0"`                         | Hôte d’écoute (pour déploiement externe) |
| `port`           | `5000`                              | Port d’écoute de l’application |
| `secret_key`     | `"change_this_secret"`              | Clé secrète utilisée par Flask pour les sessions |
| `data_dir`       | `"data"`                            | Répertoire contenant les données textuelles |
| `cache_dir`      | `"cache"`                           | Dossier utilisé pour le cache des réponses générées |
| `question_cache_file` | `"questions_cache.json"`     | Fichier JSON stockant les réponses déjà traitées |

---

### 🔍 Configuration du moteur RAG

| Paramètre             | Valeur par défaut                                  | Description |
|-----------------------|----------------------------------------------------|-------------|
| `model.name`          | `"dangvantuan/sentence-camembert-large"`         | Modèle SentenceTransformer pour les embeddings |
| `normalize_embeddings`| `true`                                             | Normalisation des vecteurs avant indexation |
| `index.json_path`     | `"data/hippocrate_rag_data.json"`                | Chemin vers le corpus segmenté |
| `faiss_path`          | `"hippocrate.index"`                             | Emplacement de l’index FAISS pré-entraîné |
| `build_on_startup`    | `true`                                             | Reconstruit l’index au démarrage si activé |
| `top_k`               | `6`                                                | Nombre de documents récupérés pour chaque requête |

> 💡 Le modèle `"sentence-camembert-large"` est particulièrement adapté au français ancien et moderne, ce qui en fait un choix pertinent pour l’analyse des *Aphorismes d’Hippocrate*.

---

### 🤖 Configuration du LLM (Modèle de Génération)

| Paramètre   | Valeur par défaut                          | Description |
|-------------|--------------------------------------------|-------------|
| `provider`  | `"ollama"`                                 | Système d’exécution des modèles locaux |
| `endpoint`  | `"http://localhost:11434/api/generate"`   | API REST d’Ollama pour générer des réponses |
| `model`     | `"mistral"`                                | Modèle de langage utilisé pour la génération |

> 📌 Ce projet est conçu pour fonctionner avec un LLM en local via [Ollama](https://ollama.com), mais peut être adapté à d'autres fournisseurs comme OpenAI, HuggingFace ou LlamaCPP.

---

### 🔐 Sécurité

| Paramètre           | Valeur                                                                 | Description |
|---------------------|------------------------------------------------------------------------|-------------|
| `allowed_tags`      | Liste de balises HTML autorisées : `<p>`, `<h4>`, `<ul>`, `<em>`, etc. | Contrôle strict du format de sortie HTML généré par le LLM |

Cette liste blanche empêche toute injection de code malveillant dans les réponses HTML, notamment en interdisant les balises `<script>`, `<iframe>`, etc.

---

### ✅ Utilisation

Ce fichier YAML doit être présent à la racine du projet ou dans un dossier `config/`. Il est chargé automatiquement au démarrage de l’application via `config_loader.py` et validé grâce à un schéma Pydantic (`GlobalConfig`).

---

### 🔄 Adaptabilité

La modularité de cette configuration permet :
- De changer facilement de modèle d’embedding ou de LLM.
- D’ajouter des fournisseurs ou backends supplémentaires.
- De personnaliser les balises HTML autorisées selon le contexte d’utilisation.

---

Ce fichier constitue donc une base solide pour configurer et déployer rapidement un système RAG centré sur les textes médicaux classiques, tout en garantissant sécurité, performance et extensibilité.

---

## 🧠 Implémentation du moteur RAG Hippocratique : rag/hippocrag.py

Ce module implémente un système **RAG (Retrieval-Augmented Generation)** basé sur les *Aphorismes d’Hippocrate*, utilisant une approche combinée de **recherche sémantique avec FAISS** et de **génération assistée par modèle de langage**. Il est conçu pour répondre à des questions médicales ou philosophiques en s'appuyant uniquement sur les textes historiques préparés au préalable.

### 🔧 Fonctionnalités principales

- **Recherche sémantique** : encode les aphorismes avec un modèle de transformation en embeddings vectoriels (`SentenceTransformer`).
- **Indexation efficace** : utilise la bibliothèque **FAISS** pour stocker et interroger rapidement les vecteurs.
- **Génération contextuelle** : appelle un **LLM externe** via une API REST pour formuler une réponse à partir des fragments pertinents trouvés.
- **Support de configuration** : tout est configurable via un objet `config`, permettant de changer facilement de modèle, d'index ou d’endpoint LLM.

---

### 📦 Dépendances utilisées

```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os
import requests
```

---

### 🏗️ Classe principale : `HippocRAG_FAISS`

#### Initialisation
Prend une configuration en entrée qui définit :
- Le modèle d’embedding (`model.name`)
- Si les embeddings doivent être normalisés
- Chemins vers l’index FAISS et le fichier JSON des documents
- Paramètres du LLM (endpoint et modèle)

Si configuré, il construit automatiquement l’index à l’initialisation.

#### Méthodes clés

| Méthode | Description |
|--------|-------------|
| `build_index()` | Encode tous les textes du corpus et sauvegarde l'index FAISS |
| `load_index()` | Charge l’index FAISS et les documents si pas déjà chargés |
| `search(query)` | Recherche les `top_k` documents les plus proches de la requête |
| `generate(question, passages)` | Génère une réponse HTML structurée à partir des passages trouvés |

---

### 💬 Exemple de prompt pour génération

La classe génère un prompt détaillé pour le LLM, lui demandant de :
- Répondre en français
- Utiliser uniquement les balises HTML spécifiées
- Adopter un ton socratique et pédagogique
- Se baser exclusivement sur le contexte fourni

Cela garantit que les réponses restent fidèles à l’esprit des *Aphorismes*.

---

### 📁 Les fichiers en inputs

Le système s'appuit sur les fichiers suivants :

- `data/hippocrate_rag_data.json` : corpus segmenté et prêt pour le RAG  
- `index/hippocrate.faiss` : index FAISS binaire précalculé  

---

### ✅ Utilisation typique

```python
rag = HippocRAG_FAISS(config)
results = rag.search("Quel est le rôle du régime dans la santé ?")
answer = rag.generate("Quel est le rôle du régime dans la santé ?", results)
print(answer)
```
---

## 🌐 API et Interface Web pour le RAG Hippocratique

Ce module implémente une **application web légère** basée sur **Flask**, permettant d’interfacer le système **RAG sur les Aphorismes d’Hippocrate** via une interface utilisateur simple. L’objectif est de rendre accessible la recherche et l’interprétation des textes médicaux classiques à travers un navigateur, tout en conservant un contrôle strict sur la sécurité et les performances.

---

### 🔧 Fonctionnalités principales

- **Interface utilisateur HTML/Flask** : formulaire interactif pour poser des questions.
- **Gestion par thèmes** : liste de questions préchargées organisées thématiquement.
- **Cache de réponses** : évite de recalculer les réponses déjà générées.
- **Nettoyage HTML** : protection contre injections XSS grâce à `bleach`.
- **API légère** : endpoint `/api/questions` pour charger dynamiquement des questions par thème.
- **Configuration centralisée** : utilise un fichier YAML + schéma Pydantic (`GlobalConfig`) pour gérer tous les paramètres.

---

### 📦 Dépendances utilisées

```python
from flask import Flask, render_template, request, jsonify, redirect, url_for
import yaml
import json
import os
import bleach
from datetime import datetime
from config_loader import load_config
from models.config_schema import GlobalConfig
from rag.hippocrag import HippocRAG_FAISS
```

---

### 🏗️ Architecture globale

#### 1. **Initialisation**
- La configuration est chargée depuis un fichier YAML et validée avec Pydantic.
- Le moteur RAG (`HippocRAG_FAISS`) est instancié au démarrage.
- Les questions prédéfinies sont chargées depuis un fichier JSON.

#### 2. **Moteur de cache**
- Les réponses générées sont stockées localement dans un fichier JSON.
- Réduit les appels inutiles au LLM et améliore les temps de réponse.

#### 3. **Sécurité**
- Utilisation de `bleach` pour nettoyer toute réponse HTML générée par le LLM.
- Liste blanche des balises autorisées (configurable).

#### 4. **Routes principales**

| Route | Méthode | Description |
|-------|---------|-------------|
| `/` | GET/POST | Page principale avec formulaire de question |
| `/api/questions` | GET | Retourne les questions associées à un thème |
| `/reset-cache` | POST | Permet de vider le cache des réponses |

---

### 📁 Fichiers en input

Le projet s'appuie sur les fichers suivants :

- **Fichiers de données** :
  - `data/hippocrates_questions.json` : questions prédéfinies organisées par thème
- **Fichiers de configuration** :
  - `config/config.yaml` : paramètres globaux
- **Modèles de données** :
  - `models/config_schema.py` : définition du schéma de configuration
- **Templates Jinja2** :
  - `templates/index.html` : page d’accueil interactive

---

### 💬 Exemple de fonctionnement

Un utilisateur peut :
1. Choisir un thème médical (ex. "Prognostic", "Épidémies")
2. Sélectionner ou formuler une question personnalisée
3. Obtenir une réponse structurée en HTML, issue du RAG
4. Voir les fragments de texte ayant servi à générer cette réponse

---

### 🔄 Perspectives d’évolution

- Ajout d’un système de feedback utilisateur pour affiner les réponses
- Génération de fiches imprimables (PDF) des réponses
- Intégration d’une version historique des textes en grec ancien
- Support multilingue (anglais, grec moderne)
- Interface admin pour enrichir les thèmes et questions

---

### 🚀 Démarrage rapide

Pour exécuter l'application :

```bash
python app.py
```

Puis accéder à l’interface via : [http://localhost:5000](http://localhost:5000)

---

Ce module constitue une **couche applicative claire et modulaire**, permettant d’exposer les capacités du moteur RAG aux utilisateurs finaux, qu'ils soient chercheurs, enseignants ou étudiants en histoire de la médecine.

---
## 📢 Contributions

Toute contribution visant à enrichir :
- Le corpus (nouvelles traductions, annotations)
- Les questions prédéfinies
- La documentation pédagogique  
est la bienvenue !

---

## 📄 Licence

MIT License – Voir le fichier [LICENSE](LICENSE)

---

## 🧑‍💻 Auteur

*micheldpd*
Ingénieur ML passionné par l’Histoire de la Médecine
