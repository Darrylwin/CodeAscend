"""
Script pour ajouter les quiz TypeScript (débutant, intermédiaire, avancé)
avec 10 questions chacun et les catégories correspondantes.

Utilisation:
    python seed_typescript_quizzes.py
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
# Données des quiz TypeScript
# ============================================================================

TYPESCRIPT_QUIZ_DATA = {
    "category": {
        "name": "TypeScript",
        "description": "Quiz pour maîtriser TypeScript et le typage statique",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg",
        "is_active": True,
    },
    "quizzes": {
        "debutant": {
            "title": "TypeScript - Débutant",
            "level": QuizLevel.debutant,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Comment annoter le type d'une variable en TypeScript?",
                    "answers": [
                        {"text": "let age: number = 25", "is_correct": True},
                        {"text": "let age = number(25)", "is_correct": False},
                        {"text": "let age <number> = 25", "is_correct": False},
                        {"text": "number let age = 25", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel est le type TypeScript pour une chaîne de caractères?",
                    "answers": [
                        {"text": "string", "is_correct": True},
                        {"text": "String", "is_correct": False},
                        {"text": "str", "is_correct": False},
                        {"text": "char", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment définir un tableau de nombres en TypeScript?",
                    "answers": [
                        {"text": "number[]", "is_correct": True},
                        {"text": "Array<number>", "is_correct": True},
                        {"text": "[number]", "is_correct": False},
                        {"text": "numbers", "is_correct": False},
                    ],
                },
                {
                    "text": "Que signifie le type 'any' en TypeScript?",
                    "answers": [
                        {"text": "Accepte n'importe quel type, désactive le typage", "is_correct": True},
                        {"text": "Un type nullable", "is_correct": False},
                        {"text": "Un type générique", "is_correct": False},
                        {"text": "Un type optionnel", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment rendre une propriété optionnelle dans une interface?",
                    "answers": [
                        {"text": "name?: string", "is_correct": True},
                        {"text": "name: string?", "is_correct": False},
                        {"text": "optional name: string", "is_correct": False},
                        {"text": "name: string | null", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment définir une interface en TypeScript?",
                    "answers": [
                        {"text": "interface User { name: string }", "is_correct": True},
                        {"text": "type interface User = { name: string }", "is_correct": False},
                        {"text": "struct User { name: string }", "is_correct": False},
                        {"text": "class interface User { name: string }", "is_correct": False},
                    ],
                },
                {
                    "text": "Que représente le type 'void'?",
                    "answers": [
                        {"text": "Une fonction qui ne retourne rien", "is_correct": True},
                        {"text": "Une variable nulle", "is_correct": False},
                        {"text": "Un type indéfini", "is_correct": False},
                        {"text": "Un tableau vide", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment créer un type union en TypeScript?",
                    "answers": [
                        {"text": "string | number", "is_correct": True},
                        {"text": "string & number", "is_correct": False},
                        {"text": "string + number", "is_correct": False},
                        {"text": "string | | number", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle commande compile un fichier TypeScript?",
                    "answers": [
                        {"text": "tsc fichier.ts", "is_correct": True},
                        {"text": "ts-compile fichier.ts", "is_correct": False},
                        {"text": "node fichier.ts", "is_correct": False},
                        {"text": "build fichier.ts", "is_correct": False},
                    ],
                },
                {
                    "text": "Que retourne le type 'never'?",
                    "answers": [
                        {"text": "Une valeur qui ne se produit jamais (fonction qui throw toujours)", "is_correct": True},
                        {"text": "Une valeur nulle", "is_correct": False},
                        {"text": "Un type optionnel", "is_correct": False},
                        {"text": "Une fonction asynchrone", "is_correct": False},
                    ],
                },
            ],
        },
        "intermediaire": {
            "title": "TypeScript - Intermédiaire",
            "level": QuizLevel.intermediaire,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Quelle est la différence entre interface et type alias?",
                    "answers": [
                        {"text": "interface est extensible via declaration merging, type alias non", "is_correct": True},
                        {"text": "type alias est plus performant", "is_correct": False},
                        {"text": "interface ne supporte pas les unions", "is_correct": False},
                        {"text": "Aucune différence", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment utiliser un générique en TypeScript?",
                    "answers": [
                        {"text": "function identity<T>(arg: T): T { return arg; }", "is_correct": True},
                        {"text": "function identity(arg: generic): generic { return arg; }", "is_correct": False},
                        {"text": "function identity(arg: any): any { return arg; }", "is_correct": False},
                        {"text": "function identity<arg>(T: arg): arg { return T; }", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait l'opérateur 'as' en TypeScript?",
                    "answers": [
                        {"text": "Type assertion - force TypeScript à considérer un type spécifique", "is_correct": True},
                        {"text": "Convertit une valeur vers un autre type à l'exécution", "is_correct": False},
                        {"text": "Crée un alias de variable", "is_correct": False},
                        {"text": "Hérite d'une interface", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment définir un type intersection?",
                    "answers": [
                        {"text": "type AB = A & B", "is_correct": True},
                        {"text": "type AB = A | B", "is_correct": False},
                        {"text": "type AB = A + B", "is_correct": False},
                        {"text": "interface AB extends A, B {}", "is_correct": False},
                    ],
                },
                {
                    "text": "Que sont les Mapped Types en TypeScript?",
                    "answers": [
                        {"text": "Des types créés en itérant sur les propriétés d'un autre type", "is_correct": True},
                        {"text": "Des méthodes de transformation de tableaux typés", "is_correct": False},
                        {"text": "Des types pour les Map natifs JS", "is_correct": False},
                        {"text": "Des types génériques avec contraintes", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait le type utilitaire Partial<T>?",
                    "answers": [
                        {"text": "Rend toutes les propriétés de T optionnelles", "is_correct": True},
                        {"text": "Crée une copie partielle de T", "is_correct": False},
                        {"text": "Supprime certaines propriétés de T", "is_correct": False},
                        {"text": "Rend T readonly", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment contraindre un générique à un type spécifique?",
                    "answers": [
                        {"text": "function fn<T extends string>(arg: T)", "is_correct": True},
                        {"text": "function fn<T: string>(arg: T)", "is_correct": False},
                        {"text": "function fn<T implements string>(arg: T)", "is_correct": False},
                        {"text": "function fn<T = string>(arg: T)", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait le type utilitaire Required<T>?",
                    "answers": [
                        {"text": "Rend toutes les propriétés optionnelles de T obligatoires", "is_correct": True},
                        {"text": "Ajoute des propriétés requises à T", "is_correct": False},
                        {"text": "Valide que T est non-null", "is_correct": False},
                        {"text": "Rend T immuable", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment typer un enum en TypeScript?",
                    "answers": [
                        {"text": "enum Direction { Up, Down, Left, Right }", "is_correct": True},
                        {"text": "const Direction = enum { Up, Down }", "is_correct": False},
                        {"text": "type Direction = 'Up' | 'Down'", "is_correct": False},
                        {"text": "interface Direction { Up: number }", "is_correct": False},
                    ],
                },
                {
                    "text": "Que retourne keyof T?",
                    "answers": [
                        {"text": "Un union type de toutes les clés de T", "is_correct": True},
                        {"text": "Un tableau des clés de T", "is_correct": False},
                        {"text": "La première clé de T", "is_correct": False},
                        {"text": "Le nombre de propriétés de T", "is_correct": False},
                    ],
                },
            ],
        },
        "avance": {
            "title": "TypeScript - Avancé",
            "level": QuizLevel.avance,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Que sont les Conditional Types en TypeScript?",
                    "answers": [
                        {"text": "T extends U ? X : Y - types qui dépendent d'une condition", "is_correct": True},
                        {"text": "Des types avec des valeurs par défaut", "is_correct": False},
                        {"text": "Des types qui changent selon l'environnement", "is_correct": False},
                        {"text": "Des types optionnels avec fallback", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait le mot-clé infer dans les Conditional Types?",
                    "answers": [
                        {"text": "Il infère et capture un type dans une branche de condition", "is_correct": True},
                        {"text": "Il désactive l'inférence de type automatique", "is_correct": False},
                        {"text": "Il force TypeScript à déduire le type", "is_correct": False},
                        {"text": "Il crée un type temporaire", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait Awaited<T> en TypeScript 4.5+?",
                    "answers": [
                        {"text": "Extrait le type résolu d'une Promise imbriquée", "is_correct": True},
                        {"text": "Crée une Promise qui attend T ms", "is_correct": False},
                        {"text": "Rend T asynchrone", "is_correct": False},
                        {"text": "Transforme T en Observable", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que le declaration merging?",
                    "answers": [
                        {"text": "Deux déclarations d'interface avec le même nom fusionnent automatiquement", "is_correct": True},
                        {"text": "Fusionner deux fichiers .ts en un", "is_correct": False},
                        {"text": "Combiner deux modules en un", "is_correct": False},
                        {"text": "Étendre une classe avec une interface", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment créer un type Template Literal en TypeScript?",
                    "answers": [
                        {"text": "type Greeting = `Hello ${string}`", "is_correct": True},
                        {"text": "type Greeting = 'Hello ' + string", "is_correct": False},
                        {"text": "type Greeting = string.template('Hello')", "is_correct": False},
                        {"text": "type Greeting = Template<'Hello', string>", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait le type utilitaire ReturnType<T>?",
                    "answers": [
                        {"text": "Extrait le type de retour d'une fonction T", "is_correct": True},
                        {"text": "Force T à retourner un type spécifique", "is_correct": False},
                        {"text": "Rend le type de retour optionnel", "is_correct": False},
                        {"text": "Crée une fonction qui retourne T", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un Discriminated Union?",
                    "answers": [
                        {"text": "Un union type avec une propriété commune permettant de le discriminer", "is_correct": True},
                        {"text": "Un union type excluant certains types", "is_correct": False},
                        {"text": "Un union de types primitifs uniquement", "is_correct": False},
                        {"text": "Un type créé avec Exclude<>", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait le type utilitaire Extract<T, U>?",
                    "answers": [
                        {"text": "Extrait de T les types assignables à U", "is_correct": True},
                        {"text": "Extrait la valeur U de T", "is_correct": False},
                        {"text": "Supprime U de T", "is_correct": False},
                        {"text": "Crée un nouveau type à partir de T et U", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment utiliser un decorator de classe en TypeScript?",
                    "answers": [
                        {"text": "@decorator class MyClass {}", "is_correct": True},
                        {"text": "class MyClass @decorator {}", "is_correct": False},
                        {"text": "class @decorator MyClass {}", "is_correct": False},
                        {"text": "#decorator class MyClass {}", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait le type satisfies introduit en TypeScript 4.9?",
                    "answers": [
                        {"text": "Valide qu'une valeur satisfait un type sans perdre son type inféré précis", "is_correct": True},
                        {"text": "Remplace le mot-clé as pour les assertions", "is_correct": False},
                        {"text": "Force une valeur à correspondre exactement à un type", "is_correct": False},
                        {"text": "Crée un type conditionnel basé sur une valeur", "is_correct": False},
                    ],
                },
            ],
        },
    },
}


def add_typescript_quizzes():
    """Ajoute la catégorie TypeScript et les quiz avec toutes les questions"""

    try:
        category_name = TYPESCRIPT_QUIZ_DATA["category"]["name"]
        existing_category = (
            db.query(Category).filter(Category.name == category_name).first()
        )

        if existing_category:
            print(f"✓ Catégorie '{category_name}' existe déjà (ID: {existing_category.id})")
            category = existing_category
        else:
            category = Category(
                id=str(uuid.uuid4()),
                name=TYPESCRIPT_QUIZ_DATA["category"]["name"],
                description=TYPESCRIPT_QUIZ_DATA["category"]["description"],
                icon_url=TYPESCRIPT_QUIZ_DATA["category"]["icon_url"],
                is_active=TYPESCRIPT_QUIZ_DATA["category"]["is_active"],
            )
            db.add(category)
            db.commit()
            print(f"✓ Catégorie '{category_name}' créée avec succès (ID: {category.id})")

        for level_name, quiz_data in TYPESCRIPT_QUIZ_DATA["quizzes"].items():
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

        print("\n✅ Tous les quiz TypeScript ont été ajoutés avec succès!")

    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de l'ajout des quiz: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Ajout des quiz TypeScript (débutant, intermédiaire, avancé)...\n")
    add_typescript_quizzes()