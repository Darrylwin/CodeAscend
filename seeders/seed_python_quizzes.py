"""
Script pour ajouter les quiz Python (débutant, intermédiaire, avancé)
avec 10 questions chacun et les catégories correspondantes.

Utilisation:
    python seed_python_quizzes.py
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
# Données des quiz Python
# ============================================================================

PYTHON_QUIZ_DATA = {
    "category": {
        "name": "Python",
        "description": "Quiz pour maîtriser la programmation Python",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/dart/dart-original.svg",
        "is_active": True,
    },
    "quizzes": {
        "debutant": {
            "title": "Python - Débutant",
            "level": QuizLevel.debutant,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Quel est le mot-clé pour définir une fonction en Python?",
                    "answers": [
                        {"text": "def", "is_correct": True},
                        {"text": "function", "is_correct": False},
                        {"text": "func", "is_correct": False},
                        {"text": "define", "is_correct": False},
                    ],
                },
                {
                    "text": "Que retourne la fonction len() sur une chaîne 'Hello'?",
                    "answers": [
                        {"text": "5", "is_correct": True},
                        {"text": "'Hello'", "is_correct": False},
                        {"text": "4", "is_correct": False},
                        {"text": "None", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment accéder au premier élément d'une liste?",
                    "answers": [
                        {"text": "liste[0]", "is_correct": True},
                        {"text": "liste[1]", "is_correct": False},
                        {"text": "liste.first()", "is_correct": False},
                        {"text": "liste[:]", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel type de données Python est immutable?",
                    "answers": [
                        {"text": "tuple", "is_correct": True},
                        {"text": "list", "is_correct": False},
                        {"text": "dict", "is_correct": False},
                        {"text": "set", "is_correct": False},
                    ],
                },
                {
                    "text": "Que affiche print('Python' * 2)?",
                    "answers": [
                        {"text": "PythonPython", "is_correct": True},
                        {"text": "Python2", "is_correct": False},
                        {"text": "Erreur", "is_correct": False},
                        {"text": "2", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment créer une liste vide en Python?",
                    "answers": [
                        {"text": "[]", "is_correct": True},
                        {"text": "{}", "is_correct": False},
                        {"text": "list()", "is_correct": True},
                        {"text": "new list", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel opérateur vérifie l'égalité en Python?",
                    "answers": [
                        {"text": "==", "is_correct": True},
                        {"text": "=", "is_correct": False},
                        {"text": "is", "is_correct": False},
                        {"text": "===", "is_correct": False},
                    ],
                },
                {
                    "text": "Que retourne 5 // 2 en Python?",
                    "answers": [
                        {"text": "2", "is_correct": True},
                        {"text": "2.5", "is_correct": False},
                        {"text": "3", "is_correct": False},
                        {"text": "Erreur", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment ajouter un élément à une liste?",
                    "answers": [
                        {"text": "liste.append(element)", "is_correct": True},
                        {"text": "liste.add(element)", "is_correct": False},
                        {"text": "liste.push(element)", "is_correct": False},
                        {"text": "liste.insert(element)", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel est le résultat de bool('False')?",
                    "answers": [
                        {"text": "True", "is_correct": True},
                        {"text": "False", "is_correct": False},
                        {"text": "None", "is_correct": False},
                        {"text": "Erreur", "is_correct": False},
                    ],
                },
            ],
        },
        "intermediaire": {
            "title": "Python - Intermédiaire",
            "level": QuizLevel.intermediaire,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Que retourne list(map(lambda x: x**2, [1,2,3]))?",
                    "answers": [
                        {"text": "[1, 4, 9]", "is_correct": True},
                        {"text": "[1, 2, 3]", "is_correct": False},
                        {"text": "[2, 4, 6]", "is_correct": False},
                        {"text": "Erreur", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle syntaxe crée un dictionnaire en Python?",
                    "answers": [
                        {"text": "{'clé': 'valeur'}", "is_correct": True},
                        {"text": "('clé': 'valeur')", "is_correct": False},
                        {"text": "['clé': 'valeur']", "is_correct": False},
                        {"text": "'clé': 'valeur'", "is_correct": False},
                    ],
                },
                {
                    "text": "Que retourne [x for x in range(5) if x % 2 == 0]?",
                    "answers": [
                        {"text": "[0, 2, 4]", "is_correct": True},
                        {"text": "[1, 3]", "is_correct": False},
                        {"text": "[0, 1, 2, 3, 4]", "is_correct": False},
                        {"text": "[2, 4]", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle méthode crée une copie d'une liste?",
                    "answers": [
                        {"text": "liste.copy()", "is_correct": True},
                        {"text": "liste.clone()", "is_correct": False},
                        {"text": "liste.duplicate()", "is_correct": False},
                        {"text": "copy(liste)", "is_correct": False},
                    ],
                },
                {
                    "text": "Que signifie *args dans une fonction?",
                    "answers": [
                        {"text": "Nombre variable d'arguments positionnels", "is_correct": True},
                        {"text": "Arguments nommés", "is_correct": False},
                        {"text": "Arguments optionnels", "is_correct": False},
                        {"text": "Arguments de liste", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment accéder au dernier élément d'une liste?",
                    "answers": [
                        {"text": "liste[-1]", "is_correct": True},
                        {"text": "liste[last]", "is_correct": False},
                        {"text": "liste.last()", "is_correct": False},
                        {"text": "liste[-0]", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel est le résultat de ''.join(['a', 'b', 'c'])?",
                    "answers": [
                        {"text": "'abc'", "is_correct": True},
                        {"text": "['a', 'b', 'c']", "is_correct": False},
                        {"text": "'a,b,c'", "is_correct": False},
                        {"text": "Erreur", "is_correct": False},
                    ],
                },
                {
                    "text": "Que retourne type([])?",
                    "answers": [
                        {"text": "<class 'list'>", "is_correct": True},
                        {"text": "list", "is_correct": False},
                        {"text": "'list'", "is_correct": False},
                        {"text": "array", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment vérifier si une clé existe dans un dictionnaire?",
                    "answers": [
                        {"text": "'clé' in dictionnaire", "is_correct": True},
                        {"text": "dictionnaire.has_key('clé')", "is_correct": False},
                        {"text": "find('clé') in dictionnaire", "is_correct": False},
                        {"text": "dictionnaire.contains('clé')", "is_correct": False},
                    ],
                },
                {
                    "text": "Que retourne dict.get('clé', 'défaut') si la clé n'existe pas?",
                    "answers": [
                        {"text": "'défaut'", "is_correct": True},
                        {"text": "None", "is_correct": False},
                        {"text": "KeyError", "is_correct": False},
                        {"text": "'clé'", "is_correct": False},
                    ],
                },
            ],
        },
        "avance": {
            "title": "Python - Avancé",
            "level": QuizLevel.avance,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Qu'est-ce que le décorateur @property?",
                    "answers": [
                        {"text": "Convertir une méthode en attribut", "is_correct": True},
                        {"text": "Créer une classe", "is_correct": False},
                        {"text": "Définir une constante", "is_correct": False},
                        {"text": "Importer un module", "is_correct": False},
                    ],
                },
                {
                    "text": "Que retourne next(iter([1,2,3]))?",
                    "answers": [
                        {"text": "1", "is_correct": True},
                        {"text": "[1,2,3]", "is_correct": False},
                        {"text": "2", "is_correct": False},
                        {"text": "Erreur", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel est le but du **kwargs?",
                    "answers": [
                        {"text": "Nombre variable d'arguments nommés", "is_correct": True},
                        {"text": "Arguments positionnels", "is_correct": False},
                        {"text": "Exponentiation", "is_correct": False},
                        {"text": "Commentaire", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment créer un générateur en Python?",
                    "answers": [
                        {"text": "Avec yield", "is_correct": True},
                        {"text": "Avec return", "is_correct": False},
                        {"text": "Avec Generator()", "is_correct": False},
                        {"text": "Avec gen()", "is_correct": False},
                    ],
                },
                {
                    "text": "Que signifie héritage multiple en Python?",
                    "answers": [
                        {"text": "Une classe hérite de plusieurs classes", "is_correct": True},
                        {"text": "Une classe hérite d'une seule classe", "is_correct": False},
                        {"text": "Copier une classe", "is_correct": False},
                        {"text": "Fusionner deux classes", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel est le rôle de __init__?",
                    "answers": [
                        {"text": "Initialiser les attributs d'une instance", "is_correct": True},
                        {"text": "Définir une variable globale", "is_correct": False},
                        {"text": "Importer un module", "is_correct": False},
                        {"text": "Créer une constante", "is_correct": False},
                    ],
                },
                {
                    "text": "Que retourne (lambda x: x + 1)(5)?",
                    "answers": [
                        {"text": "6", "is_correct": True},
                        {"text": "5", "is_correct": False},
                        {"text": "lambda", "is_correct": False},
                        {"text": "Erreur", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment gérer les exceptions en Python?",
                    "answers": [
                        {"text": "try/except", "is_correct": True},
                        {"text": "try/catch", "is_correct": False},
                        {"text": "if/except", "is_correct": False},
                        {"text": "handle/error", "is_correct": False},
                    ],
                },
                {
                    "text": "Que retourne hasattr(obj, 'attr')?",
                    "answers": [
                        {"text": "True/False selon que 'attr' existe", "is_correct": True},
                        {"text": "La valeur de l'attribut", "is_correct": False},
                        {"text": "L'objet", "is_correct": False},
                        {"text": "Erreur", "is_correct": False},
                    ],
                },
                {
                    "text": "Que signifie GIL en Python?",
                    "answers": [
                        {"text": "Global Interpreter Lock", "is_correct": True},
                        {"text": "Global Instance Library", "is_correct": False},
                        {"text": "General Interface Layer", "is_correct": False},
                        {"text": "Graph Iteration Logic", "is_correct": False},
                    ],
                },
            ],
        },
    },
}


def add_python_quizzes():
    """Ajoute la catégorie Python et les quiz avec toutes les questions"""

    try:
        # 1. Créer ou récupérer la catégorie Python
        category_name = PYTHON_QUIZ_DATA["category"]["name"]
        existing_category = (
            db.query(Category).filter(Category.name == category_name).first()
        )

        if existing_category:
            print(f"✓ Catégorie '{category_name}' existe déjà (ID: {existing_category.id})")
            category = existing_category
        else:
            category = Category(
                id=str(uuid.uuid4()),
                name=PYTHON_QUIZ_DATA["category"]["name"],
                description=PYTHON_QUIZ_DATA["category"]["description"],
                icon_url=PYTHON_QUIZ_DATA["category"]["icon_url"],
                is_active=PYTHON_QUIZ_DATA["category"]["is_active"],
            )
            db.add(category)
            db.commit()
            print(
                f"✓ Catégorie '{category_name}' créée avec succès (ID: {category.id})"
            )

        # 2. Créer les quizzes pour chaque niveau
        for level_name, quiz_data in PYTHON_QUIZ_DATA["quizzes"].items():
            # Vérifier si le quiz existe déjà
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

            # 3. Ajouter les questions et réponses
            for q_index, question_data in enumerate(quiz_data["questions"], 1):
                # Vérifier si la question existe
                existing_question = (
                    db.query(Question)
                    .filter(
                        Question.quiz_id == quiz.id,
                        Question.order == q_index,
                    )
                    .first()
                )

                if existing_question:
                    print(
                        f"    ✓ Question {q_index} existe déjà"
                    )
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

                # Ajouter les réponses
                for a_index, answer_data in enumerate(question_data["answers"], 1):
                    # Vérifier si la réponse existe
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

        print("\n✅ Tous les quiz Python ont été ajoutés avec succès!")

    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de l'ajout des quiz: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Ajout des quiz Python (débutant, intermédiaire, avancé)...\n")
    add_python_quizzes()
