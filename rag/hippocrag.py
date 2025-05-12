from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
import os
import requests

class HippocRAG_FAISS:
    def __init__(self, config):
        self.config = config
        self.model = SentenceTransformer(config.rag.model.name)
        self.normalize = config.rag.model.normalize_embeddings
        self.index_path = config.rag.index.faiss_path
        self.json_path = config.rag.index.json_path
        self.top_k = config.rag.index.top_k
        self.llm_endpoint = config.rag.llm.endpoint
        self.llm_model = config.rag.llm.model

        self.index = None
        self.documents = []
        if config.rag.index.build_on_startup:
            self.build_index()


    def build_index(self):
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.documents = json.load(f)
        texts = [doc["text"] for doc in self.documents]
        embeddings = self.model.encode(texts, normalize_embeddings=self.normalize)
        self.index = faiss.IndexFlatL2(embeddings.shape[1])
        self.index.add(np.array(embeddings, dtype=np.float32))
        faiss.write_index(self.index, self.index_path)

    def load_index(self):
        if self.index is None:
            self.index = faiss.read_index(self.index_path)
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.documents = json.load(f)

    def search(self, query):
        self.load_index()
        embedding = self.model.encode([query], normalize_embeddings=self.normalize)
        D, I = self.index.search(np.array(embedding, dtype=np.float32), self.top_k)
        return [self.documents[i] for i in I[0]]

    def generate(self, question, passages):
        context = "\n".join([p["text"] for p in passages])

        prompt = f"""
                Vous êtes un expert en aphorismes d'Hippocrate. Répondez à la question suivante en vous basant uniquement sur le contexte fourni. Si le contexte ne contient pas assez d'informations, indiquez-le clairement.

                **Question** : {question}
                **Contexte** : {context}

                Répondez en français de manière concise et précise dans un format HTML structuré et lisible.
                N'utilise QUE les balises suivantes :
                    - Titres : <h4>, <h5>
                    - Paragraphes : <p>
                    - Listes : <ul>, <li>
                    - Emphase : <em>, <strong>
                    - Citations ou réflexions : <blockquote>

                N'inclue AUCUNE balise dangereuse comme : <script>, <style>, <iframe>, <img>, <button>, <form>, etc.
                Ne met AUCUN attribut JavaScript (ex: onclick, onerror).
                Utilise un ton socratique, pédagogique et en phase avec la médecine hippocratique.
                """

        payload = {
            "model": self.llm_model,
            "prompt": prompt,
            "stream": False
        }
        response = requests.post(self.llm_endpoint, json=payload)
        if response.ok:
            return response.json().get("response", "")
        return "Erreur de génération"