from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for
)
import yaml
import json
import os
import bleach
from datetime import datetime
from config_loader import load_config

# Import des schémas de configuration
from models.config_schema import GlobalConfig

# === Chargement et validation de la configuration ===
raw_config = load_config() 
CONFIG = GlobalConfig(**raw_config)

# Importer la classe principale du RAG
from rag.hippocrag import HippocRAG_FAISS

# === Initialisation de l'application Flask ===
def create_app():
    app = Flask(__name__)
    
    # Configuration Flask basée sur le fichier
    app.config['SECRET_KEY'] = CONFIG.app.secret_key
    
    # === Initialisation du système RAG ===
    rag = HippocRAG_FAISS(CONFIG)
    
    # === Chargement des données statiques ===
    def load_questions(path=os.path.join(CONFIG.app.data_dir, "hippocrates_questions.json")):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    all_questions = load_questions()

    # === Cache de réponses ===
    cache_dir = CONFIG.app.cache_dir
    question_cache_file = os.path.join(cache_dir, CONFIG.app.question_cache_file)
    
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)

    try:
        with open(question_cache_file, "r", encoding="utf-8") as f:
            question_cache = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        question_cache = {}

    def save_to_cache(question, answer):
        question_cache[question] = answer
        with open(question_cache_file, "w", encoding="utf-8") as f:
            json.dump(question_cache, f, ensure_ascii=False, indent=2)

    # === Nettoyage HTML ===
    def sanitize_html(html_content):
        allowed_tags = CONFIG.security.allowed_tags
        cleaned = bleach.clean(
            html_content,
            tags=allowed_tags,
            attributes={},
            protocols=[],  # Bloque protocoles JS dans liens
            strip=True
        )
        return cleaned.strip()

    # === Routes ===
    @app.route("/", methods=["GET", "POST"])
    def index():
        current_year = datetime.now().year
        selected_theme = None
        selected_question = None
        custom_question = ""
        questions = []
        final_question = None
        answer_html = None
        contexts = []

        if request.method == "POST":
            selected_theme = request.form.get("theme")
            selected_question = request.form.get("question")
            custom_question = request.form.get("custom_question")

            if custom_question:
                final_question = custom_question.strip()
            elif selected_question:
                final_question = selected_question.strip()

            if final_question:
                if final_question in question_cache:
                    answer_html = question_cache[final_question]
                    contexts = []
                else:
                    # Recherche des passages pertinents
                    passages = rag.search(final_question)
                    # Génération de la réponse
                    raw_answer = rag.generate(final_question, passages)
                    
                    # Extraction des contextes
                    contexts = [p["text"] for p in passages]
                    
                    # Nettoyage de la réponse
                    answer_html = sanitize_html(raw_answer)
                    
                    # Gestion des erreurs
                    if not answer_html or "aucune réponse générée" in answer_html.lower() or "erreur" in answer_html.lower():
                        answer_html = "<p>⚠️ Aucune information trouvée dans les aphorismes pour répondre à cette question.</p>"
                    else:
                        # Mise en cache uniquement des bonnes réponses
                        save_to_cache(final_question, answer_html)

                # Optionnel : vider champ personnalisé après soumission
                custom_question = ""

        # Filtrer les questions par thème sélectionné
        if selected_theme:
            questions = [q for q in all_questions if q["theme"] == selected_theme]

        return render_template(
            "index.html",
            themes=sorted(set(q["theme"] for q in all_questions)),
            selected_theme=selected_theme,
            questions=questions,
            selected_question=selected_question,
            custom_question=custom_question,
            final_question=final_question,
            answer=answer_html,
            contexts=contexts,
            current_year=current_year
        )

    @app.route("/api/questions")
    def get_questions_by_theme():
        theme = request.args.get("theme", "")
        filtered = [q for q in all_questions if q["theme"] == theme]
        return jsonify(filtered)

    @app.route("/reset-cache", methods=["POST"])
    def reset_cache():
        """Endpoint sécurisé pour purger le cache de réponses"""
        question_cache.clear()
        save_to_cache("", "")  # Sauvegarde fichier vide
        return redirect(url_for("index"))

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=CONFIG.app.debug, host=CONFIG.app.host, port=CONFIG.app.port)