
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
