"""
Script pour ajouter les quiz Java (débutant, intermédiaire, avancé).
Utilisation: python seed_java_quizzes.py
"""
import uuid
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine, Base
from app.models import Category, Quiz, Question, Answer, QuizLevel, QuizStatus

Base.metadata.create_all(bind=engine)
db: Session = SessionLocal()

JAVA_QUIZ_DATA = {
    "category": {
        "name": "Java",
        "description": "Quiz pour maîtriser Java et la programmation orientée objet",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg",
        "is_active": True,
    },
    "quizzes": {
        "debutant": {
            "title": "Java - Débutant",
            "level": QuizLevel.debutant,
            "status": QuizStatus.published,
            "questions": [
                {"text": "Comment afficher du texte en Java?", "answers": [{"text": "System.out.println('Hello')", "is_correct": True}, {"text": "print('Hello')", "is_correct": False}, {"text": "console.log('Hello')", "is_correct": False}, {"text": "echo 'Hello'", "is_correct": False}]},
                {"text": "Quel mot-clé déclare une classe en Java?", "answers": [{"text": "class", "is_correct": True}, {"text": "struct", "is_correct": False}, {"text": "object", "is_correct": False}, {"text": "type", "is_correct": False}]},
                {"text": "Quel est le type Java pour un entier 32 bits?", "answers": [{"text": "int", "is_correct": True}, {"text": "integer", "is_correct": False}, {"text": "Int32", "is_correct": False}, {"text": "num", "is_correct": False}]},
                {"text": "Comment créer une instance de classe en Java?", "answers": [{"text": "new MaClasse()", "is_correct": True}, {"text": "create MaClasse()", "is_correct": False}, {"text": "MaClasse.create()", "is_correct": False}, {"text": "MaClasse()", "is_correct": False}]},
                {"text": "Quel mot-clé définit une constante en Java?", "answers": [{"text": "final", "is_correct": True}, {"text": "const", "is_correct": False}, {"text": "static", "is_correct": False}, {"text": "readonly", "is_correct": False}]},
                {"text": "Quelle est la méthode principale d'un programme Java?", "answers": [{"text": "public static void main(String[] args)", "is_correct": True}, {"text": "public void start()", "is_correct": False}, {"text": "static void run()", "is_correct": False}, {"text": "public main()", "is_correct": False}]},
                {"text": "Comment créer un tableau de 5 entiers en Java?", "answers": [{"text": "int[] arr = new int[5]", "is_correct": True}, {"text": "int arr[5]", "is_correct": False}, {"text": "Array<int> arr = new Array(5)", "is_correct": False}, {"text": "int[] arr = int[5]", "is_correct": False}]},
                {"text": "Quel est le type de données pour un caractère unique en Java?", "answers": [{"text": "char", "is_correct": True}, {"text": "character", "is_correct": False}, {"text": "string", "is_correct": False}, {"text": "letter", "is_correct": False}]},
                {"text": "Comment écrire un commentaire sur une ligne en Java?", "answers": [{"text": "// commentaire", "is_correct": True}, {"text": "# commentaire", "is_correct": False}, {"text": "/* commentaire", "is_correct": False}, {"text": "-- commentaire", "is_correct": False}]},
                {"text": "Quel opérateur Java vérifie l'inégalité?", "answers": [{"text": "!=", "is_correct": True}, {"text": "<>", "is_correct": False}, {"text": "=/=", "is_correct": False}, {"text": "not=", "is_correct": False}]},
            ],
        },
        "intermediaire": {
            "title": "Java - Intermédiaire",
            "level": QuizLevel.intermediaire,
            "status": QuizStatus.published,
            "questions": [
                {"text": "Quelle est la différence entre == et .equals() pour les String?", "answers": [{"text": "== compare les références, .equals() compare le contenu des chaînes", "is_correct": True}, {"text": "Aucune différence pour les String", "is_correct": False}, {"text": ".equals() compare les références, == le contenu", "is_correct": False}, {"text": "== est plus performant pour les String", "is_correct": False}]},
                {"text": "Qu'est-ce que le polymorphisme en Java?", "answers": [{"text": "La capacité d'un objet à prendre plusieurs formes selon son type réel", "is_correct": True}, {"text": "La capacité de créer plusieurs constructeurs", "is_correct": False}, {"text": "La capacité d'hériter de plusieurs classes", "is_correct": False}, {"text": "La capacité de définir plusieurs méthodes main()", "is_correct": False}]},
                {"text": "Qu'est-ce qu'une interface en Java?", "answers": [{"text": "Un contrat définissant des méthodes que les classes implémentant doivent fournir", "is_correct": True}, {"text": "Une classe qui ne peut pas être instanciée directement", "is_correct": False}, {"text": "Une classe avec uniquement des méthodes statiques", "is_correct": False}, {"text": "Un module Java pour l'interface graphique", "is_correct": False}]},
                {"text": "Qu'est-ce que le garbage collection en Java?", "answers": [{"text": "La gestion automatique de la mémoire qui libère les objets non référencés", "is_correct": True}, {"text": "Un outil pour supprimer les fichiers temporaires", "is_correct": False}, {"text": "Un mécanisme de nettoyage du code source", "is_correct": False}, {"text": "La suppression automatique des variables locales", "is_correct": False}]},
                {"text": "Quelle est la différence entre ArrayList et LinkedList?", "answers": [{"text": "ArrayList est basé sur un tableau (accès rapide), LinkedList sur des nœuds chaînés (insertion rapide)", "is_correct": True}, {"text": "ArrayList est thread-safe, LinkedList non", "is_correct": False}, {"text": "LinkedList supporte les types primitifs, ArrayList non", "is_correct": False}, {"text": "Aucune différence de performance", "is_correct": False}]},
                {"text": "Comment gérer les exceptions en Java?", "answers": [{"text": "try { } catch (Exception e) { } finally { }", "is_correct": True}, {"text": "try { } except Exception { }", "is_correct": False}, {"text": "handle { } catch (e) { }", "is_correct": False}, {"text": "begin { } rescue Exception { }", "is_correct": False}]},
                {"text": "Qu'est-ce qu'une classe abstraite en Java?", "answers": [{"text": "Une classe qui ne peut pas être instanciée et peut contenir des méthodes abstraites et concrètes", "is_correct": True}, {"text": "Une interface avec des méthodes implémentées", "is_correct": False}, {"text": "Une classe sans attributs", "is_correct": False}, {"text": "Une classe dont toutes les méthodes sont privées", "is_correct": False}]},
                {"text": "Que fait le mot-clé 'synchronized' en Java?", "answers": [{"text": "Permet à un seul thread d'accéder à une méthode/bloc à la fois (thread safety)", "is_correct": True}, {"text": "Synchronise une variable avec la base de données", "is_correct": False}, {"text": "Exécute une méthode de façon asynchrone", "is_correct": False}, {"text": "Synchronise deux objets Java", "is_correct": False}]},
                {"text": "Qu'est-ce que l'autoboxing en Java?", "answers": [{"text": "La conversion automatique entre types primitifs et leurs wrappers (int <-> Integer)", "is_correct": True}, {"text": "La création automatique de boîtes de dialogue", "is_correct": False}, {"text": "Le boxing automatique des tableaux en List", "is_correct": False}, {"text": "La sérialisation automatique des objets", "is_correct": False}]},
                {"text": "Que retourne Optional.empty().isPresent()?", "answers": [{"text": "false", "is_correct": True}, {"text": "true", "is_correct": False}, {"text": "null", "is_correct": False}, {"text": "Une exception", "is_correct": False}]},
            ],
        },
        "avance": {
            "title": "Java - Avancé",
            "level": QuizLevel.avance,
            "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que les Java Streams?", "answers": [{"text": "Une API pour traiter des séquences d'éléments de façon fonctionnelle (filter, map, reduce...)", "is_correct": True}, {"text": "Un système d'entrée/sortie pour les fichiers", "is_correct": False}, {"text": "Un mécanisme de communication réseau", "is_correct": False}, {"text": "Des threads Java optimisés pour le traitement de données", "is_correct": False}]},
                {"text": "Qu'est-ce qu'une lambda expression en Java?", "answers": [{"text": "Une fonction anonyme implémentant une interface fonctionnelle, syntaxe : (params) -> expression", "is_correct": True}, {"text": "Une variable qui peut changer de type", "is_correct": False}, {"text": "Un calcul mathématique optimisé par la JVM", "is_correct": False}, {"text": "Une méthode qui retourne une fonction", "is_correct": False}]},
                {"text": "Que sont les Records en Java (depuis Java 14)?", "answers": [{"text": "Des classes immuables concises avec constructeur, getters, equals, hashCode et toString auto-générés", "is_correct": True}, {"text": "Un type de base de données embarquée", "is_correct": False}, {"text": "Des enregistrements de logs structurés", "is_correct": False}, {"text": "Des classes de configuration immuables Spring", "is_correct": False}]},
                {"text": "Qu'est-ce que la JVM?", "answers": [{"text": "La machine virtuelle Java qui exécute le bytecode et abstrait le système d'exploitation", "is_correct": True}, {"text": "Le compilateur Java", "is_correct": False}, {"text": "Un gestionnaire de mémoire Java", "is_correct": False}, {"text": "L'IDE officiel Java", "is_correct": False}]},
                {"text": "Que sont les Sealed Classes en Java (depuis Java 17)?", "answers": [{"text": "Des classes qui restreignent quelles classes peuvent les étendre (permits clause)", "is_correct": True}, {"text": "Des classes dont les attributs sont tous final", "is_correct": False}, {"text": "Des classes inaccessibles depuis d'autres packages", "is_correct": False}, {"text": "Des classes sans constructeur public", "is_correct": False}]},
                {"text": "Qu'est-ce que le pattern Singleton en Java?", "answers": [{"text": "Un pattern qui garantit qu'une classe n'a qu'une seule instance dans toute l'application", "is_correct": True}, {"text": "Une classe avec un seul attribut", "is_correct": False}, {"text": "Une méthode qui retourne toujours la même valeur", "is_correct": False}, {"text": "Un thread qui gère une seule tâche", "is_correct": False}]},
                {"text": "Quelle est la différence entre Callable et Runnable?", "answers": [{"text": "Callable peut retourner un résultat et lancer des exceptions vérifiées, Runnable non", "is_correct": True}, {"text": "Runnable est plus récent que Callable", "is_correct": False}, {"text": "Callable est synchrone, Runnable asynchrone", "is_correct": False}, {"text": "Aucune différence fonctionnelle", "is_correct": False}]},
                {"text": "Qu'est-ce que CompletableFuture en Java?", "answers": [{"text": "Une classe pour la programmation asynchrone et la composition de tâches avec callbacks", "is_correct": True}, {"text": "Un Future qui se complète automatiquement après un timeout", "is_correct": False}, {"text": "Un thread pool géré automatiquement par la JVM", "is_correct": False}, {"text": "Une alternative aux threads classiques basée sur les coroutines", "is_correct": False}]},
                {"text": "Que sont les Virtual Threads (Project Loom, Java 21)?", "answers": [{"text": "Des threads légers gérés par la JVM permettant de créer des millions de threads concurrents", "is_correct": True}, {"text": "Des threads qui s'exécutent dans la JVM sans OS", "is_correct": False}, {"text": "Des threads simulés pour les tests unitaires", "is_correct": False}, {"text": "Des coroutines Kotlin compatibles Java", "is_correct": False}]},
                {"text": "Qu'est-ce que le Pattern Matching for switch (Java 21)?", "answers": [{"text": "Permet au switch d'utiliser des patterns de type et des gardes pour un code plus expressif", "is_correct": True}, {"text": "Un système de regex intégré dans les expressions switch", "is_correct": False}, {"text": "La possibilité d'utiliser des Strings dans les switch (existe depuis Java 7)", "is_correct": False}, {"text": "Un switch optimisé par le compilateur via le pattern matching", "is_correct": False}]},
            ],
        },
    },
}


def add_java_quizzes():
    try:
        category_name = JAVA_QUIZ_DATA["category"]["name"]
        existing_category = db.query(Category).filter(Category.name == category_name).first()
        if existing_category:
            print(f"✓ Catégorie '{category_name}' existe déjà (ID: {existing_category.id})")
            category = existing_category
        else:
            category = Category(id=str(uuid.uuid4()), name=JAVA_QUIZ_DATA["category"]["name"], description=JAVA_QUIZ_DATA["category"]["description"], icon_url=JAVA_QUIZ_DATA["category"]["icon_url"], is_active=JAVA_QUIZ_DATA["category"]["is_active"])
            db.add(category)
            db.commit()
            print(f"✓ Catégorie '{category_name}' créée avec succès (ID: {category.id})")

        for level_name, quiz_data in JAVA_QUIZ_DATA["quizzes"].items():
            existing_quiz = db.query(Quiz).filter(Quiz.category_id == category.id, Quiz.level == quiz_data["level"]).first()
            if existing_quiz:
                print(f"  ✓ Quiz '{existing_quiz.title}' existe déjà (ID: {existing_quiz.id})")
                quiz = existing_quiz
            else:
                quiz = Quiz(id=str(uuid.uuid4()), category_id=category.id, title=quiz_data["title"], level=quiz_data["level"], status=quiz_data["status"])
                db.add(quiz)
                db.commit()
                print(f"  ✓ Quiz '{quiz.title}' créé (ID: {quiz.id})")

            for q_index, question_data in enumerate(quiz_data["questions"], 1):
                existing_question = db.query(Question).filter(Question.quiz_id == quiz.id, Question.order == q_index).first()
                if existing_question:
                    print(f"    ✓ Question {q_index} existe déjà")
                    question = existing_question
                else:
                    question = Question(id=str(uuid.uuid4()), quiz_id=quiz.id, question_text=question_data["text"], order=q_index)
                    db.add(question)
                    db.commit()
                    print(f"    ✓ Question {q_index} ajoutée")

                for a_index, answer_data in enumerate(question_data["answers"], 1):
                    existing_answer = db.query(Answer).filter(Answer.question_id == question.id, Answer.order == a_index).first()
                    if not existing_answer:
                        db.add(Answer(id=str(uuid.uuid4()), question_id=question.id, answer_text=answer_data["text"], is_correct=answer_data["is_correct"], order=a_index))
                if not existing_question:
                    db.commit()

        print("\n✅ Tous les quiz Java ont été ajoutés avec succès!")
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Ajout des quiz Java (débutant, intermédiaire, avancé)...\n")
    add_java_quizzes()