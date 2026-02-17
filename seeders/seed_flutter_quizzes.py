"""
Script pour ajouter les quiz Flutter (débutant, intermédiaire, avancé)
avec 10 questions chacun et les catégories correspondantes.

Utilisation:
    python seed_flutter_quizzes.py
"""

import uuid
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine, Base
from app.models import Category, Quiz, Question, Answer, QuizLevel, QuizStatus

# Créer les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

db: Session = SessionLocal()

# ============================================================================
# Données des quiz Flutter
# ============================================================================

FLUTTER_QUIZ_DATA = {
    "category": {
        "name": "Flutter",
        "description": "Quiz pour maîtriser Flutter et le développement mobile cross-platform",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flutter/flutter-original.svg",
        "is_active": True,
    },
    "quizzes": {
        "debutant": {
            "title": "Flutter - Débutant",
            "level": QuizLevel.debutant,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Quel langage de programmation Flutter utilise-t-il?",
                    "answers": [
                        {"text": "Dart", "is_correct": True},
                        {"text": "Kotlin", "is_correct": False},
                        {"text": "Swift", "is_correct": False},
                        {"text": "JavaScript", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un Widget en Flutter?",
                    "answers": [
                        {"text": "Le bloc de base pour construire l'interface utilisateur", "is_correct": True},
                        {"text": "Une bibliothèque externe", "is_correct": False},
                        {"text": "Un fichier de configuration", "is_correct": False},
                        {"text": "Un service d'arrière-plan", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle est la différence entre StatelessWidget et StatefulWidget?",
                    "answers": [
                        {"text": "StatefulWidget peut gérer un état qui change dans le temps", "is_correct": True},
                        {"text": "StatelessWidget est plus rapide dans tous les cas", "is_correct": False},
                        {"text": "StatefulWidget ne peut pas avoir de paramètres", "is_correct": False},
                        {"text": "StatelessWidget ne peut pas afficher de texte", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel widget Flutter affiche du texte?",
                    "answers": [
                        {"text": "Text", "is_correct": True},
                        {"text": "Label", "is_correct": False},
                        {"text": "Paragraph", "is_correct": False},
                        {"text": "TextView", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment centrer un widget dans Flutter?",
                    "answers": [
                        {"text": "Center(child: monWidget)", "is_correct": True},
                        {"text": "monWidget.align(center)", "is_correct": False},
                        {"text": "Align(position: center)", "is_correct": False},
                        {"text": "Container(center: true)", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel widget Flutter est utilisé pour une liste scrollable?",
                    "answers": [
                        {"text": "ListView", "is_correct": True},
                        {"text": "ScrollView", "is_correct": False},
                        {"text": "RecyclerView", "is_correct": False},
                        {"text": "TableView", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment lancer l'application Flutter en mode debug?",
                    "answers": [
                        {"text": "flutter run", "is_correct": True},
                        {"text": "flutter start", "is_correct": False},
                        {"text": "dart run main.dart", "is_correct": False},
                        {"text": "flutter debug", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel fichier contient les dépendances d'un projet Flutter?",
                    "answers": [
                        {"text": "pubspec.yaml", "is_correct": True},
                        {"text": "package.json", "is_correct": False},
                        {"text": "build.gradle", "is_correct": False},
                        {"text": "requirements.txt", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel widget Flutter permet d'empiler des widgets en colonne?",
                    "answers": [
                        {"text": "Column", "is_correct": True},
                        {"text": "Stack", "is_correct": False},
                        {"text": "VBox", "is_correct": False},
                        {"text": "LinearLayout", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment appeler setState() correctement?",
                    "answers": [
                        {"text": "setState(() { /* modifications */ })", "is_correct": True},
                        {"text": "this.state = nouvelEtat", "is_correct": False},
                        {"text": "updateState(nouvelEtat)", "is_correct": False},
                        {"text": "setState(nouvelEtat)", "is_correct": False},
                    ],
                },
            ],
        },
        "intermediaire": {
            "title": "Flutter - Intermédiaire",
            "level": QuizLevel.intermediaire,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Qu'est-ce que le BuildContext en Flutter?",
                    "answers": [
                        {"text": "Un handle vers la position du widget dans l'arbre de widgets", "is_correct": True},
                        {"text": "L'état actuel de l'application", "is_correct": False},
                        {"text": "Le contexte d'exécution Dart", "is_correct": False},
                        {"text": "Un objet de configuration du thème", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment naviguer vers un nouvel écran en Flutter?",
                    "answers": [
                        {"text": "Navigator.push(context, MaterialPageRoute(builder: (_) => NouvelEcran()))", "is_correct": True},
                        {"text": "Router.navigate(NouvelEcran())", "is_correct": False},
                        {"text": "context.push(NouvelEcran())", "is_correct": False},
                        {"text": "navigate(NouvelEcran())", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un FutureBuilder?",
                    "answers": [
                        {"text": "Un widget qui construit son UI selon l'état d'une Future", "is_correct": True},
                        {"text": "Un outil pour créer des animations", "is_correct": False},
                        {"text": "Un builder pour les listes asynchrones", "is_correct": False},
                        {"text": "Un générateur de code futur", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel widget Flutter superpose des widgets les uns sur les autres?",
                    "answers": [
                        {"text": "Stack", "is_correct": True},
                        {"text": "Column", "is_correct": False},
                        {"text": "Overlay", "is_correct": False},
                        {"text": "Layer", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment partager des données entre widgets avec InheritedWidget?",
                    "answers": [
                        {"text": "En plaçant l'InheritedWidget en parent et en y accédant via context", "is_correct": True},
                        {"text": "En passant les données via le constructeur de chaque widget", "is_correct": False},
                        {"text": "En utilisant une variable globale statique", "is_correct": False},
                        {"text": "En émettant des événements via EventBus", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que pubspec.lock?",
                    "answers": [
                        {"text": "Un fichier qui verrouille les versions exactes des dépendances installées", "is_correct": True},
                        {"text": "Un fichier qui bloque les modifications du pubspec.yaml", "is_correct": False},
                        {"text": "Un fichier de configuration de sécurité", "is_correct": False},
                        {"text": "Un fichier de logs de build", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel widget Flutter crée un bouton avec une élévation (Material)?",
                    "answers": [
                        {"text": "ElevatedButton", "is_correct": True},
                        {"text": "RaisedButton", "is_correct": False},
                        {"text": "ShadowButton", "is_correct": False},
                        {"text": "MaterialButton", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment gérer les erreurs dans un FutureBuilder?",
                    "answers": [
                        {"text": "Vérifier snapshot.hasError et afficher un widget d'erreur", "is_correct": True},
                        {"text": "Utiliser try/catch dans le builder", "is_correct": False},
                        {"text": "Ajouter un paramètre onError au FutureBuilder", "is_correct": False},
                        {"text": "Utiliser ErrorBoundary", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que le Hot Reload en Flutter?",
                    "answers": [
                        {"text": "Injecte les modifications du code dans la VM Dart sans redémarrer l'app", "is_correct": True},
                        {"text": "Redémarre complètement l'application", "is_correct": False},
                        {"text": "Recompile uniquement les fichiers modifiés", "is_correct": False},
                        {"text": "Synchronise l'app avec un serveur de développement", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel widget Flutter affiche une image depuis le réseau?",
                    "answers": [
                        {"text": "Image.network('url')", "is_correct": True},
                        {"text": "NetworkImage('url')", "is_correct": False},
                        {"text": "RemoteImage('url')", "is_correct": False},
                        {"text": "UrlImage('url')", "is_correct": False},
                    ],
                },
            ],
        },
        "avance": {
            "title": "Flutter - Avancé",
            "level": QuizLevel.avance,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Qu'est-ce que le State Management avec Riverpod?",
                    "answers": [
                        {"text": "Une solution de gestion d'état type-safe et réactive basée sur des providers", "is_correct": True},
                        {"text": "Un plugin de navigation pour Flutter", "is_correct": False},
                        {"text": "Un système de mise en cache HTTP", "is_correct": False},
                        {"text": "Une alternative à setState uniquement", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que le widget RepaintBoundary?",
                    "answers": [
                        {"text": "Crée un calque de peinture séparé pour isoler les repaints coûteux", "is_correct": True},
                        {"text": "Délimite une zone cliquable dans l'UI", "is_correct": False},
                        {"text": "Empêche le rebuild d'un sous-arbre de widgets", "is_correct": False},
                        {"text": "Crée une bordure autour d'un widget", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment fonctionne le mécanisme de keys en Flutter?",
                    "answers": [
                        {"text": "Elles permettent à Flutter d'identifier et préserver l'état des widgets lors de reconstructions", "is_correct": True},
                        {"text": "Elles servent uniquement d'identifiants pour les tests automatisés", "is_correct": False},
                        {"text": "Elles gèrent l'accès aux ressources chiffrées", "is_correct": False},
                        {"text": "Elles optimisent le rendu des listes statiques", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle est la différence entre GlobalKey et LocalKey?",
                    "answers": [
                        {"text": "GlobalKey est unique dans toute l'app, LocalKey dans un parent direct", "is_correct": True},
                        {"text": "GlobalKey est partagé entre toutes les instances, LocalKey non", "is_correct": False},
                        {"text": "LocalKey peut être utilisé pour accéder à l'état d'un widget, GlobalKey non", "is_correct": False},
                        {"text": "Aucune différence fonctionnelle", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un Isolate en Dart/Flutter?",
                    "answers": [
                        {"text": "Un thread séparé avec sa propre mémoire pour du calcul parallèle", "is_correct": True},
                        {"text": "Un widget isolé du reste de l'arbre", "is_correct": False},
                        {"text": "Un module de sécurité pour les données sensibles", "is_correct": False},
                        {"text": "Un état isolé pour les tests unitaires", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment optimiser les performances d'une ListView longue?",
                    "answers": [
                        {"text": "Utiliser ListView.builder qui crée les items à la demande", "is_correct": True},
                        {"text": "Pré-charger tous les items au démarrage", "is_correct": False},
                        {"text": "Utiliser un Column avec SingleChildScrollView", "is_correct": False},
                        {"text": "Diviser la liste en plusieurs widgets", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que le Bloc pattern en Flutter?",
                    "answers": [
                        {"text": "Business Logic Component - sépare la logique métier de l'UI via des Streams", "is_correct": True},
                        {"text": "Un pattern de navigation par blocs d'écrans", "is_correct": False},
                        {"text": "Un système de mise en cache basé sur des blocs de données", "is_correct": False},
                        {"text": "Un outil de gestion des animations complexes", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment créer un widget qui s'anime avec AnimationController?",
                    "answers": [
                        {"text": "En utilisant SingleTickerProviderStateMixin et en créant un AnimationController dans initState", "is_correct": True},
                        {"text": "En étendant AnimatedWidget directement", "is_correct": False},
                        {"text": "En wrappant le widget avec AnimationProvider", "is_correct": False},
                        {"text": "En utilisant setState avec un Timer", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que Dart Null Safety?",
                    "answers": [
                        {"text": "Un système de types qui distingue les types nullable et non-nullable à la compilation", "is_correct": True},
                        {"text": "Une vérification des null à l'exécution uniquement", "is_correct": False},
                        {"text": "Un mécanisme de gestion automatique des erreurs null", "is_correct": False},
                        {"text": "Une option de configuration du compilateur Dart", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait le widget Semantics en Flutter?",
                    "answers": [
                        {"text": "Fournit des informations d'accessibilité pour les lecteurs d'écran", "is_correct": True},
                        {"text": "Ajoute des métadonnées SEO à l'application web Flutter", "is_correct": False},
                        {"text": "Décrit le comportement métier d'un widget", "is_correct": False},
                        {"text": "Génère de la documentation automatique", "is_correct": False},
                    ],
                },
            ],
        },
    },
}


def add_flutter_quizzes():
    """Ajoute la catégorie Flutter et les quiz avec toutes les questions"""

    try:
        category_name = FLUTTER_QUIZ_DATA["category"]["name"]
        existing_category = (
            db.query(Category).filter(Category.name == category_name).first()
        )

        if existing_category:
            print(f"✓ Catégorie '{category_name}' existe déjà (ID: {existing_category.id})")
            category = existing_category
        else:
            category = Category(
                id=str(uuid.uuid4()),
                name=FLUTTER_QUIZ_DATA["category"]["name"],
                description=FLUTTER_QUIZ_DATA["category"]["description"],
                icon_url=FLUTTER_QUIZ_DATA["category"]["icon_url"],
                is_active=FLUTTER_QUIZ_DATA["category"]["is_active"],
            )
            db.add(category)
            db.commit()
            print(f"✓ Catégorie '{category_name}' créée avec succès (ID: {category.id})")

        for level_name, quiz_data in FLUTTER_QUIZ_DATA["quizzes"].items():
            existing_quiz = (
                db.query(Quiz)
                .filter(
                    Quiz.category_id == category.id,
                    Quiz.level == quiz_data["level"],
                )
                .first()
            )

            if existing_quiz:
                print(f"  ✓ Quiz '{existing_quiz.title}' existe déjà (ID: {existing_quiz.id})")
                quiz = existing_quiz
            else:
                quiz = Quiz(
                    id=str(uuid.uuid4()),
                    category_id=category.id,
                    title=quiz_data["title"],
                    level=quiz_data["level"],
                    status=quiz_data["status"],
                )
                db.add(quiz)
                db.commit()
                print(f"  ✓ Quiz '{quiz.title}' créé (ID: {quiz.id})")

            for q_index, question_data in enumerate(quiz_data["questions"], 1):
                existing_question = (
                    db.query(Question)
                    .filter(
                        Question.quiz_id == quiz.id,
                        Question.order == q_index,
                    )
                    .first()
                )

                if existing_question:
                    print(f"    ✓ Question {q_index} existe déjà")
                    question = existing_question
                else:
                    question = Question(
                        id=str(uuid.uuid4()),
                        quiz_id=quiz.id,
                        question_text=question_data["text"],
                        order=q_index,
                    )
                    db.add(question)
                    db.commit()
                    print(f"    ✓ Question {q_index} ajoutée")

                for a_index, answer_data in enumerate(question_data["answers"], 1):
                    existing_answer = (
                        db.query(Answer)
                        .filter(
                            Answer.question_id == question.id,
                            Answer.order == a_index,
                        )
                        .first()
                    )

                    if not existing_answer:
                        answer = Answer(
                            id=str(uuid.uuid4()),
                            question_id=question.id,
                            answer_text=answer_data["text"],
                            is_correct=answer_data["is_correct"],
                            order=a_index,
                        )
                        db.add(answer)

                if not existing_question:
                    db.commit()

        print("\n✅ Tous les quiz Flutter ont été ajoutés avec succès!")

    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de l'ajout des quiz: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Ajout des quiz Flutter (débutant, intermédiaire, avancé)...\n")
    add_flutter_quizzes()