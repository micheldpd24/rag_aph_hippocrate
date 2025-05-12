# Utilisation d'une image Python slim pour réduire la taille finale
FROM python:3.11-slim

# Répertoire de travail
WORKDIR /app

# Copie des fichiers nécessaires
COPY requirements.txt ./
COPY data data/
COPY templates templates/
COPY rag_config.yaml ./
COPY app.py ./
COPY config_loader.py ./
COPY models models/
COPY rag rag/
COPY hippocrate.index ./

# Installation des dépendances système
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc g++ && \
    rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Téléchargement optionnel du modèle SentenceTransformer (si pas présent localement)
RUN python -c "from sentence_transformers import SentenceTransformer; model = SentenceTransformer('dangvantuan/sentence-camembert-large');"

# Exposer le port Flask
EXPOSE 5000

# Commande de lancement
# CMD ["tail", "-f", "/dev/null"]
CMD ["python", "app.py"]