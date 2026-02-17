"""
Script pour ajouter les quiz JavaScript (débutant, intermédiaire, avancé)
avec 10 questions chacun et les catégories correspondantes.

Utilisation:
    python seed_javascript_quizzes.py
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
# Données des quiz JavaScript
# ============================================================================

JAVASCRIPT_QUIZ_DATA = {
    "category": {
        "name": "JavaScript",
        "description": "Quiz pour maîtriser la programmation JavaScript",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg",
        "is_active": True,
    },
    "quizzes": {
        "debutant": {
            "title": "JavaScript - Débutant",
            "level": QuizLevel.debutant,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Quel mot-clé déclare une variable en JavaScript (moderne)?",
                    "answers": [
                        {"text": "let", "is_correct": True},
                        {"text": "var", "is_correct": False},
                        {"text": "dim", "is_correct": False},
                        {"text": "variable", "is_correct": False},
                    ],
                },
                {
                    "text": "Que retourne typeof 42?",
                    "answers": [
                        {"text": "'number'", "is_correct": True},
                        {"text": "'integer'", "is_correct": False},
                        {"text": "'string'", "is_correct": False},
                        {"text": "42", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment afficher un message dans la console?",
                    "answers": [
                        {"text": "console.log('message')", "is_correct": True},
                        {"text": "print('message')", "is_correct": False},
                        {"text": "echo 'message'", "is_correct": False},
                        {"text": "log('message')", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle est la différence entre == et ===?",
                    "answers": [
                        {"text": "=== compare la valeur ET le type", "is_correct": True},
                        {"text": "== compare la valeur ET le type", "is_correct": False},
                        {"text": "Aucune différence", "is_correct": False},
                        {"text": "=== est plus lent", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment créer un tableau en JavaScript?",
                    "answers": [
                        {"text": "const arr = [1, 2, 3]", "is_correct": True},
                        {"text": "const arr = (1, 2, 3)", "is_correct": False},
                        {"text": "const arr = {1, 2, 3}", "is_correct": False},
                        {"text": "const arr = new Array[1, 2, 3]", "is_correct": False},
                    ],
                },
                {
                    "text": "Que retourne Boolean('') en JavaScript?",
                    "answers": [
                        {"text": "false", "is_correct": True},
                        {"text": "true", "is_correct": False},
                        {"text": "null", "is_correct": False},
                        {"text": "undefined", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment définir une fonction fléchée?",
                    "answers": [
                        {"text": "const fn = () => {}", "is_correct": True},
                        {"text": "const fn = function => {}", "is_correct": False},
                        {"text": "const fn -> {}", "is_correct": False},
                        {"text": "def fn() {}", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle méthode ajoute un élément à la fin d'un tableau?",
                    "answers": [
                        {"text": "push()", "is_correct": True},
                        {"text": "append()", "is_correct": False},
                        {"text": "add()", "is_correct": False},
                        {"text": "insert()", "is_correct": False},
                    ],
                },
                {
                    "text": "Que signifie NaN en JavaScript?",
                    "answers": [
                        {"text": "Not a Number", "is_correct": True},
                        {"text": "Null and Nothing", "is_correct": False},
                        {"text": "New and Null", "is_correct": False},
                        {"text": "Non-Assigned Node", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment accéder à la longueur d'un tableau?",
                    "answers": [
                        {"text": "arr.length", "is_correct": True},
                        {"text": "arr.size()", "is_correct": False},
                        {"text": "len(arr)", "is_correct": False},
                        {"text": "arr.count", "is_correct": False},
                    ],
                },
            ],
        },
        "intermediaire": {
            "title": "JavaScript - Intermédiaire",
            "level": QuizLevel.intermediaire,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Que retourne [1, 2, 3].map(x => x * 2)?",
                    "answers": [
                        {"text": "[2, 4, 6]", "is_correct": True},
                        {"text": "[1, 2, 3]", "is_correct": False},
                        {"text": "6", "is_correct": False},
                        {"text": "[3, 4, 5]", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que le hoisting en JavaScript?",
                    "answers": [
                        {"text": "Remontée des déclarations en haut du scope", "is_correct": True},
                        {"text": "Copier une variable", "is_correct": False},
                        {"text": "Supprimer une variable", "is_correct": False},
                        {"text": "Optimiser le code", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle méthode permet de filtrer un tableau?",
                    "answers": [
                        {"text": "filter()", "is_correct": True},
                        {"text": "find()", "is_correct": False},
                        {"text": "select()", "is_correct": False},
                        {"text": "where()", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment destructurer un objet en JavaScript?",
                    "answers": [
                        {"text": "const { a, b } = obj", "is_correct": True},
                        {"text": "const [a, b] = obj", "is_correct": False},
                        {"text": "const a, b = obj", "is_correct": False},
                        {"text": "let a = obj.a, b = obj.b", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait l'opérateur spread (...)?",
                    "answers": [
                        {"text": "Étale les éléments d'un itérable", "is_correct": True},
                        {"text": "Crée une copie profonde", "is_correct": False},
                        {"text": "Fusionne deux types", "is_correct": False},
                        {"text": "Déclare un rest parameter", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'une Promise en JavaScript?",
                    "answers": [
                        {"text": "Un objet représentant une opération asynchrone", "is_correct": True},
                        {"text": "Une fonction synchrone", "is_correct": False},
                        {"text": "Un type de variable", "is_correct": False},
                        {"text": "Une méthode de tableau", "is_correct": False},
                    ],
                },
                {
                    "text": "Que retourne Object.keys({ a: 1, b: 2 })?",
                    "answers": [
                        {"text": "['a', 'b']", "is_correct": True},
                        {"text": "[1, 2]", "is_correct": False},
                        {"text": "['a: 1', 'b: 2']", "is_correct": False},
                        {"text": "{a: 1, b: 2}", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment fusionner deux objets en JavaScript?",
                    "answers": [
                        {"text": "{ ...obj1, ...obj2 }", "is_correct": True},
                        {"text": "obj1 + obj2", "is_correct": False},
                        {"text": "obj1.merge(obj2)", "is_correct": False},
                        {"text": "Object.join(obj1, obj2)", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle méthode enchaîne sur une Promise résolue?",
                    "answers": [
                        {"text": ".then()", "is_correct": True},
                        {"text": ".next()", "is_correct": False},
                        {"text": ".resolve()", "is_correct": False},
                        {"text": ".success()", "is_correct": False},
                    ],
                },
                {
                    "text": "Que retourne [1, 2, 3].reduce((acc, x) => acc + x, 0)?",
                    "answers": [
                        {"text": "6", "is_correct": True},
                        {"text": "3", "is_correct": False},
                        {"text": "[1, 2, 3]", "is_correct": False},
                        {"text": "0", "is_correct": False},
                    ],
                },
            ],
        },
        "avance": {
            "title": "JavaScript - Avancé",
            "level": QuizLevel.avance,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Qu'est-ce que la closure en JavaScript?",
                    "answers": [
                        {"text": "Une fonction qui retient l'accès à son scope lexical", "is_correct": True},
                        {"text": "Une fonction qui se ferme après exécution", "is_correct": False},
                        {"text": "Un objet immuable", "is_correct": False},
                        {"text": "Une méthode de classe privée", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que l'event loop en JavaScript?",
                    "answers": [
                        {"text": "Mécanisme gérant l'exécution asynchrone via une file de callbacks", "is_correct": True},
                        {"text": "Une boucle for spéciale pour les événements DOM", "is_correct": False},
                        {"text": "Un pattern de design pattern", "is_correct": False},
                        {"text": "Le moteur de rendu du navigateur", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait Object.freeze()?",
                    "answers": [
                        {"text": "Rend un objet immuable (ne peut plus être modifié)", "is_correct": True},
                        {"text": "Copie un objet en profondeur", "is_correct": False},
                        {"text": "Supprime toutes les propriétés", "is_correct": False},
                        {"text": "Convertit en chaîne JSON", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle est la différence entre call() et apply()?",
                    "answers": [
                        {"text": "call() passe les args un à un, apply() via un tableau", "is_correct": True},
                        {"text": "apply() est plus rapide", "is_correct": False},
                        {"text": "call() retourne une fonction, apply() l'exécute", "is_correct": False},
                        {"text": "Aucune différence", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un WeakMap?",
                    "answers": [
                        {"text": "Un Map dont les clés sont des références faibles (objets uniquement)", "is_correct": True},
                        {"text": "Un Map moins performant", "is_correct": False},
                        {"text": "Un Map pour les types primitifs", "is_correct": False},
                        {"text": "Un Map immuable", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment fonctionne le Proxy en JavaScript?",
                    "answers": [
                        {"text": "Il intercepte et redéfinit les opérations fondamentales d'un objet", "is_correct": True},
                        {"text": "Il clone un objet", "is_correct": False},
                        {"text": "Il crée un serveur proxy", "is_correct": False},
                        {"text": "Il masque les propriétés privées", "is_correct": False},
                    ],
                },
                {
                    "text": "Que retourne Promise.all([p1, p2, p3]) si p2 échoue?",
                    "answers": [
                        {"text": "La Promise globale est rejetée immédiatement", "is_correct": True},
                        {"text": "Les autres Promises continuent et retournent leurs valeurs", "is_correct": False},
                        {"text": "Retourne null pour p2 et les autres valeurs", "is_correct": False},
                        {"text": "Retourne un tableau partiel", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que le Temporal Dead Zone (TDZ)?",
                    "answers": [
                        {"text": "La zone où une variable let/const est déclarée mais pas encore initialisée", "is_correct": True},
                        {"text": "Une zone mémoire réservée au garbage collector", "is_correct": False},
                        {"text": "Un état des Promises en attente", "is_correct": False},
                        {"text": "Une erreur de timeout", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment implémenter un itérateur personnalisé?",
                    "answers": [
                        {"text": "En définissant Symbol.iterator sur l'objet", "is_correct": True},
                        {"text": "En étendant la classe Iterator", "is_correct": False},
                        {"text": "En utilisant Object.iterate()", "is_correct": False},
                        {"text": "En définissant une méthode .next() seule", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle est la particularité de async/await vs .then()/.catch()?",
                    "answers": [
                        {"text": "Syntaxe synchrone pour code asynchrone, même comportement sous le capot", "is_correct": True},
                        {"text": "async/await est plus performant", "is_correct": False},
                        {"text": "async/await bloque le thread principal", "is_correct": False},
                        {"text": ".then() ne supporte pas les erreurs", "is_correct": False},
                    ],
                },
            ],
        },
    },
}


def add_javascript_quizzes():
    """Ajoute la catégorie JavaScript et les quiz avec toutes les questions"""

    try:
        # 1. Créer ou récupérer la catégorie JavaScript
        category_name = JAVASCRIPT_QUIZ_DATA["category"]["name"]
        existing_category = (
            db.query(Category).filter(Category.name == category_name).first()
        )

        if existing_category:
            print(f"✓ Catégorie '{category_name}' existe déjà (ID: {existing_category.id})")
            category = existing_category
        else:
            category = Category(
                id=str(uuid.uuid4()),
                name=JAVASCRIPT_QUIZ_DATA["category"]["name"],
                description=JAVASCRIPT_QUIZ_DATA["category"]["description"],
                icon_url=JAVASCRIPT_QUIZ_DATA["category"]["icon_url"],
                is_active=JAVASCRIPT_QUIZ_DATA["category"]["is_active"],
            )
            db.add(category)
            db.commit()
            print(f"✓ Catégorie '{category_name}' créée avec succès (ID: {category.id})")

        # 2. Créer les quizzes pour chaque niveau
        for level_name, quiz_data in JAVASCRIPT_QUIZ_DATA["quizzes"].items():
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

        print("\n✅ Tous les quiz JavaScript ont été ajoutés avec succès!")

    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de l'ajout des quiz: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Ajout des quiz JavaScript (débutant, intermédiaire, avancé)...\n")
    add_javascript_quizzes()