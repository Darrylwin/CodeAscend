"""
Script pour ajouter les quiz SQL (débutant, intermédiaire, avancé)
avec 10 questions chacun et les catégories correspondantes.

Utilisation:
    python seed_sql_quizzes.py
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
# Données des quiz SQL
# ============================================================================

SQL_QUIZ_DATA = {
    "category": {
        "name": "SQL",
        "description": "Quiz pour maîtriser SQL et la gestion de bases de données relationnelles",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg",
        "is_active": True,
    },
    "quizzes": {
        "debutant": {
            "title": "SQL - Débutant",
            "level": QuizLevel.debutant,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Quelle commande SQL sélectionne toutes les colonnes d'une table?",
                    "answers": [
                        {"text": "SELECT * FROM table", "is_correct": True},
                        {"text": "GET ALL FROM table", "is_correct": False},
                        {"text": "FETCH * FROM table", "is_correct": False},
                        {"text": "READ table", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle commande SQL insère une nouvelle ligne?",
                    "answers": [
                        {"text": "INSERT INTO table VALUES (...)", "is_correct": True},
                        {"text": "ADD INTO table VALUES (...)", "is_correct": False},
                        {"text": "PUT INTO table VALUES (...)", "is_correct": False},
                        {"text": "CREATE ROW IN table VALUES (...)", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment filtrer les résultats d'une requête SQL?",
                    "answers": [
                        {"text": "SELECT * FROM table WHERE condition", "is_correct": True},
                        {"text": "SELECT * FROM table FILTER condition", "is_correct": False},
                        {"text": "SELECT * FROM table IF condition", "is_correct": False},
                        {"text": "SELECT * FROM table HAVING condition", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle commande SQL met à jour des données existantes?",
                    "answers": [
                        {"text": "UPDATE table SET colonne = valeur WHERE condition", "is_correct": True},
                        {"text": "MODIFY table SET colonne = valeur", "is_correct": False},
                        {"text": "CHANGE table colonne = valeur", "is_correct": False},
                        {"text": "EDIT table SET colonne = valeur", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle commande SQL supprime des lignes?",
                    "answers": [
                        {"text": "DELETE FROM table WHERE condition", "is_correct": True},
                        {"text": "REMOVE FROM table WHERE condition", "is_correct": False},
                        {"text": "DROP FROM table WHERE condition", "is_correct": False},
                        {"text": "ERASE FROM table WHERE condition", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment trier les résultats par ordre croissant?",
                    "answers": [
                        {"text": "ORDER BY colonne ASC", "is_correct": True},
                        {"text": "SORT BY colonne ASC", "is_correct": False},
                        {"text": "ORDER colonne ASCENDING", "is_correct": False},
                        {"text": "GROUP BY colonne ASC", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle clause SQL limite le nombre de résultats?",
                    "answers": [
                        {"text": "LIMIT n", "is_correct": True},
                        {"text": "TOP n", "is_correct": False},
                        {"text": "MAX n", "is_correct": False},
                        {"text": "FETCH n", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle fonction SQL compte le nombre de lignes?",
                    "answers": [
                        {"text": "COUNT(*)", "is_correct": True},
                        {"text": "SUM(*)", "is_correct": False},
                        {"text": "TOTAL(*)", "is_correct": False},
                        {"text": "NUMBER(*)", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment créer une table en SQL?",
                    "answers": [
                        {"text": "CREATE TABLE nom (colonne type, ...)", "is_correct": True},
                        {"text": "NEW TABLE nom (colonne type, ...)", "is_correct": False},
                        {"text": "ADD TABLE nom (colonne type, ...)", "is_correct": False},
                        {"text": "MAKE TABLE nom (colonne type, ...)", "is_correct": False},
                    ],
                },
                {
                    "text": "Que signifie NULL en SQL?",
                    "answers": [
                        {"text": "L'absence de valeur", "is_correct": True},
                        {"text": "La valeur zéro", "is_correct": False},
                        {"text": "Une chaîne vide", "is_correct": False},
                        {"text": "Une valeur fausse", "is_correct": False},
                    ],
                },
            ],
        },
        "intermediaire": {
            "title": "SQL - Intermédiaire",
            "level": QuizLevel.intermediaire,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Quelle est la différence entre INNER JOIN et LEFT JOIN?",
                    "answers": [
                        {"text": "LEFT JOIN retourne toutes les lignes de la table gauche, même sans correspondance à droite", "is_correct": True},
                        {"text": "INNER JOIN est plus rapide que LEFT JOIN", "is_correct": False},
                        {"text": "LEFT JOIN ne peut s'appliquer qu'à deux tables", "is_correct": False},
                        {"text": "INNER JOIN retourne toutes les lignes des deux tables", "is_correct": False},
                    ],
                },
                {
                    "text": "À quoi sert GROUP BY en SQL?",
                    "answers": [
                        {"text": "Regrouper des lignes partageant une valeur commune pour appliquer des fonctions d'agrégation", "is_correct": True},
                        {"text": "Trier les résultats par groupe", "is_correct": False},
                        {"text": "Fusionner plusieurs tables", "is_correct": False},
                        {"text": "Filtrer les groupes avant agrégation", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle est la différence entre WHERE et HAVING?",
                    "answers": [
                        {"text": "WHERE filtre avant agrégation, HAVING filtre après (sur les groupes)", "is_correct": True},
                        {"text": "HAVING est plus performant que WHERE", "is_correct": False},
                        {"text": "WHERE ne peut pas utiliser des sous-requêtes", "is_correct": False},
                        {"text": "HAVING s'applique uniquement aux colonnes indexées", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'une clé étrangère (FOREIGN KEY)?",
                    "answers": [
                        {"text": "Une colonne qui référence la clé primaire d'une autre table pour maintenir l'intégrité référentielle", "is_correct": True},
                        {"text": "Une clé de chiffrement pour sécuriser les données", "is_correct": False},
                        {"text": "Un index sur une colonne d'une table externe", "is_correct": False},
                        {"text": "Une clé partagée entre plusieurs bases de données", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'une sous-requête (subquery)?",
                    "answers": [
                        {"text": "Une requête imbriquée dans une autre requête SQL", "is_correct": True},
                        {"text": "Une requête partielle sur un sous-ensemble de colonnes", "is_correct": False},
                        {"text": "Une requête exécutée sur un serveur secondaire", "is_correct": False},
                        {"text": "Une partie d'une procédure stockée", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment renommer une colonne dans le résultat d'une requête?",
                    "answers": [
                        {"text": "SELECT colonne AS alias FROM table", "is_correct": True},
                        {"text": "SELECT colonne RENAME alias FROM table", "is_correct": False},
                        {"text": "SELECT colonne = alias FROM table", "is_correct": False},
                        {"text": "SELECT alias(colonne) FROM table", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait DISTINCT dans une requête SQL?",
                    "answers": [
                        {"text": "Élimine les doublons des résultats", "is_correct": True},
                        {"text": "Trie les résultats par ordre alphabétique", "is_correct": False},
                        {"text": "Sélectionne uniquement les colonnes différentes", "is_correct": False},
                        {"text": "Filtre les valeurs NULL", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un index en SQL?",
                    "answers": [
                        {"text": "Une structure de données qui accélère les recherches sur une colonne", "is_correct": True},
                        {"text": "Un identifiant unique de chaque ligne", "is_correct": False},
                        {"text": "Une clé primaire sur plusieurs colonnes", "is_correct": False},
                        {"text": "Un compteur automatique de lignes", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle fonction SQL retourne la valeur maximale d'une colonne?",
                    "answers": [
                        {"text": "MAX(colonne)", "is_correct": True},
                        {"text": "HIGHEST(colonne)", "is_correct": False},
                        {"text": "TOP(colonne)", "is_correct": False},
                        {"text": "GREATEST(colonne)", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait UNION en SQL?",
                    "answers": [
                        {"text": "Combine les résultats de deux requêtes en supprimant les doublons", "is_correct": True},
                        {"text": "Fusionne deux tables en une seule", "is_correct": False},
                        {"text": "Effectue une jointure entre deux tables", "is_correct": False},
                        {"text": "Combine deux colonnes en une seule", "is_correct": False},
                    ],
                },
            ],
        },
        "avance": {
            "title": "SQL - Avancé",
            "level": QuizLevel.avance,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Qu'est-ce qu'une Window Function (fonction de fenêtre) en SQL?",
                    "answers": [
                        {"text": "Une fonction qui effectue un calcul sur un ensemble de lignes liées à la ligne courante sans les regrouper", "is_correct": True},
                        {"text": "Une fonction qui s'exécute dans une fenêtre de temps définie", "is_correct": False},
                        {"text": "Une fonction qui crée une vue temporaire", "is_correct": False},
                        {"text": "Une fonction qui pagine les résultats en fenêtres", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un CTE (Common Table Expression)?",
                    "answers": [
                        {"text": "Une table temporaire nommée définie avec WITH pour être utilisée dans la requête principale", "is_correct": True},
                        {"text": "Une table permanente partagée entre plusieurs bases de données", "is_correct": False},
                        {"text": "Un type de vue matérialisée", "is_correct": False},
                        {"text": "Une expression pour créer des colonnes calculées", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment créer un CTE récursif?",
                    "answers": [
                        {"text": "WITH RECURSIVE cte AS (partie_ancre UNION ALL partie_récursive)", "is_correct": True},
                        {"text": "WITH cte RECURSIVE AS (requête)", "is_correct": False},
                        {"text": "CREATE RECURSIVE VIEW cte AS (requête)", "is_correct": False},
                        {"text": "WITH cte AS (LOOP requête END LOOP)", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle est la différence entre une vue (VIEW) et une vue matérialisée?",
                    "answers": [
                        {"text": "La vue matérialisée stocke physiquement le résultat pour de meilleures performances en lecture", "is_correct": True},
                        {"text": "La vue est plus lente mais prend moins d'espace", "is_correct": False},
                        {"text": "La vue matérialisée est mise à jour en temps réel", "is_correct": False},
                        {"text": "La vue classique stocke les données, la matérialisée non", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que l'isolation des transactions SERIALIZABLE?",
                    "answers": [
                        {"text": "Le niveau le plus strict - les transactions semblent s'exécuter séquentiellement sans interférence", "is_correct": True},
                        {"text": "Les transactions sont sérialisées en JSON avant exécution", "is_correct": False},
                        {"text": "Les transactions sont journalisées pour permettre la récupération", "is_correct": False},
                        {"text": "Les transactions utilisent un seul thread d'exécution", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait ROW_NUMBER() OVER (PARTITION BY col ORDER BY col2)?",
                    "answers": [
                        {"text": "Attribue un numéro de ligne séquentiel dans chaque partition ordonnée", "is_correct": True},
                        {"text": "Compte le nombre de lignes dans chaque groupe", "is_correct": False},
                        {"text": "Retourne le numéro de la première ligne de chaque partition", "is_correct": False},
                        {"text": "Crée un identifiant unique global pour chaque ligne", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle est la différence entre DELETE et TRUNCATE?",
                    "answers": [
                        {"text": "TRUNCATE est plus rapide et non journalisé, DELETE supporte WHERE et peut être rollback", "is_correct": True},
                        {"text": "TRUNCATE supprime la table, DELETE supprime les lignes", "is_correct": False},
                        {"text": "DELETE est plus rapide car il utilise un index", "is_correct": False},
                        {"text": "TRUNCATE supporte les conditions WHERE", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que le problème N+1 en base de données?",
                    "answers": [
                        {"text": "Exécuter 1 requête pour une liste puis N requêtes supplémentaires pour chaque item", "is_correct": True},
                        {"text": "Une table avec N+1 colonnes qui dépasse la limite du SGBD", "is_correct": False},
                        {"text": "N transactions simultanées qui causent un deadlock", "is_correct": False},
                        {"text": "Un index qui nécessite N+1 lectures pour trouver une valeur", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment fonctionne un index composite (multi-colonnes)?",
                    "answers": [
                        {"text": "Efficace pour les requêtes sur le préfixe gauche des colonnes indexées (leftmost prefix rule)", "is_correct": True},
                        {"text": "Efficace uniquement si toutes les colonnes de l'index sont dans la requête", "is_correct": False},
                        {"text": "Crée autant d'index séparés que de colonnes", "is_correct": False},
                        {"text": "Indexe les colonnes dans n'importe quel ordre de requête", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un deadlock en base de données?",
                    "answers": [
                        {"text": "Deux transactions qui s'attendent mutuellement pour libérer des verrous - aucune ne peut avancer", "is_correct": True},
                        {"text": "Une transaction qui s'exécute indéfiniment sans terminer", "is_correct": False},
                        {"text": "Un verrou posé sur une table entière bloquant toutes les lectures", "is_correct": False},
                        {"text": "Une requête qui dépasse le timeout défini par le SGBD", "is_correct": False},
                    ],
                },
            ],
        },
    },
}


def add_sql_quizzes():
    """Ajoute la catégorie SQL et les quiz avec toutes les questions"""

    try:
        category_name = SQL_QUIZ_DATA["category"]["name"]
        existing_category = (
            db.query(Category).filter(Category.name == category_name).first()
        )

        if existing_category:
            print(f"✓ Catégorie '{category_name}' existe déjà (ID: {existing_category.id})")
            category = existing_category
        else:
            category = Category(
                id=str(uuid.uuid4()),
                name=SQL_QUIZ_DATA["category"]["name"],
                description=SQL_QUIZ_DATA["category"]["description"],
                icon_url=SQL_QUIZ_DATA["category"]["icon_url"],
                is_active=SQL_QUIZ_DATA["category"]["is_active"],
            )
            db.add(category)
            db.commit()
            print(f"✓ Catégorie '{category_name}' créée avec succès (ID: {category.id})")

        for level_name, quiz_data in SQL_QUIZ_DATA["quizzes"].items():
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

        print("\n✅ Tous les quiz SQL ont été ajoutés avec succès!")

    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de l'ajout des quiz: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Ajout des quiz SQL (débutant, intermédiaire, avancé)...\n")
    add_sql_quizzes()