"""
Script pour ajouter les quiz Go/Golang (débutant, intermédiaire, avancé).
Utilisation: python seed_go_quizzes.py
"""
import uuid
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine, Base
from app.models import Category, Quiz, Question, Answer, QuizLevel, QuizStatus

Base.metadata.create_all(bind=engine)
db: Session = SessionLocal()

GO_QUIZ_DATA = {
    "category": {
        "name": "Go",
        "description": "Quiz pour maîtriser le langage Go (Golang) et ses concepts",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/go/go-original.svg",
        "is_active": True,
    },
    "quizzes": {
        "debutant": {
            "title": "Go - Débutant",
            "level": QuizLevel.debutant,
            "status": QuizStatus.published,
            "questions": [
                {"text": "Comment déclarer et initialiser une variable en Go?", "answers": [{"text": "x := 10", "is_correct": True}, {"text": "var x = 10", "is_correct": False}, {"text": "let x = 10", "is_correct": False}, {"text": "int x = 10", "is_correct": False}]},
                {"text": "Quel est le package d'entrée obligatoire de tout programme Go?", "answers": [{"text": "package main", "is_correct": True}, {"text": "package app", "is_correct": False}, {"text": "import main", "is_correct": False}, {"text": "module main", "is_correct": False}]},
                {"text": "Comment afficher du texte en Go?", "answers": [{"text": "fmt.Println('Hello')", "is_correct": True}, {"text": "print('Hello')", "is_correct": False}, {"text": "console.log('Hello')", "is_correct": False}, {"text": "System.out.println('Hello')", "is_correct": False}]},
                {"text": "Quel est le type de données Go pour une chaîne?", "answers": [{"text": "string", "is_correct": True}, {"text": "str", "is_correct": False}, {"text": "String", "is_correct": False}, {"text": "char*", "is_correct": False}]},
                {"text": "Comment créer une fonction en Go?", "answers": [{"text": "func maFonction() {}", "is_correct": True}, {"text": "def maFonction() {}", "is_correct": False}, {"text": "function maFonction() {}", "is_correct": False}, {"text": "fn maFonction() {}", "is_correct": False}]},
                {"text": "Comment importer le package fmt en Go?", "answers": [{"text": "import \"fmt\"", "is_correct": True}, {"text": "use fmt", "is_correct": False}, {"text": "require fmt", "is_correct": False}, {"text": "include fmt", "is_correct": False}]},
                {"text": "Quel mot-clé crée une boucle en Go?", "answers": [{"text": "for", "is_correct": True}, {"text": "while", "is_correct": False}, {"text": "loop", "is_correct": False}, {"text": "each", "is_correct": False}]},
                {"text": "Comment créer une slice de strings en Go?", "answers": [{"text": "[]string{}", "is_correct": True}, {"text": "string[]", "is_correct": False}, {"text": "slice<string>", "is_correct": False}, {"text": "new Slice(string)", "is_correct": False}]},
                {"text": "Comment retourner plusieurs valeurs en Go?", "answers": [{"text": "func fn() (int, error) { return 1, nil }", "is_correct": True}, {"text": "func fn() [int, error] { return [1, nil] }", "is_correct": False}, {"text": "func fn() { return 1, nil }", "is_correct": False}, {"text": "Go ne supporte pas les retours multiples", "is_correct": False}]},
                {"text": "Que signifie ':=' en Go?", "answers": [{"text": "Déclaration et affectation courte d'une nouvelle variable", "is_correct": True}, {"text": "Comparaison stricte", "is_correct": False}, {"text": "Affectation d'une variable existante", "is_correct": False}, {"text": "Déclaration d'une constante", "is_correct": False}]},
            ],
        },
        "intermediaire": {
            "title": "Go - Intermédiaire",
            "level": QuizLevel.intermediaire,
            "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce qu'une goroutine?", "answers": [{"text": "Un thread léger géré par le runtime Go pour la concurrence", "is_correct": True}, {"text": "Une fonction récursive optimisée", "is_correct": False}, {"text": "Une coroutine Python portée en Go", "is_correct": False}, {"text": "Un module Go indépendant", "is_correct": False}]},
                {"text": "Qu'est-ce qu'un channel en Go?", "answers": [{"text": "Un mécanisme de communication typé entre goroutines", "is_correct": True}, {"text": "Un canal de communication HTTP", "is_correct": False}, {"text": "Un buffer mémoire partagé", "is_correct": False}, {"text": "Un handler d'événements", "is_correct": False}]},
                {"text": "Comment Go gère-t-il les erreurs?", "answers": [{"text": "En retournant des valeurs error en dernier paramètre et en les vérifiant explicitement", "is_correct": True}, {"text": "Avec des exceptions try/catch", "is_correct": False}, {"text": "Via un système de Result<T, E>", "is_correct": False}, {"text": "Avec des callbacks onError", "is_correct": False}]},
                {"text": "Qu'est-ce qu'une interface en Go?", "answers": [{"text": "Un ensemble de signatures de méthodes; une struct l'implémente implicitement si elle a toutes ces méthodes", "is_correct": True}, {"text": "Un contrat qu'une struct doit déclarer explicitement implémenter", "is_correct": False}, {"text": "Un type abstrait avec des méthodes concrètes", "is_correct": False}, {"text": "Un module Go exporté", "is_correct": False}]},
                {"text": "Que fait defer en Go?", "answers": [{"text": "Reporte l'exécution d'une fonction à la fin de la fonction courante (LIFO)", "is_correct": True}, {"text": "Retarde l'exécution d'une goroutine", "is_correct": False}, {"text": "Différence l'évaluation d'une expression", "is_correct": False}, {"text": "Exécute une fonction après un délai en ms", "is_correct": False}]},
                {"text": "Quelle est la différence entre make() et new() en Go?", "answers": [{"text": "make() initialise les types slice/map/chan, new() alloue de la mémoire et retourne un pointeur", "is_correct": True}, {"text": "new() est plus récent et remplace make()", "is_correct": False}, {"text": "make() retourne un pointeur, new() retourne une valeur", "is_correct": False}, {"text": "Aucune différence pour les slices", "is_correct": False}]},
                {"text": "Qu'est-ce qu'un struct en Go?", "answers": [{"text": "Un type composite qui regroupe des champs nommés de types différents", "is_correct": True}, {"text": "Une classe Go sans méthodes", "is_correct": False}, {"text": "Un type immuable en Go", "is_correct": False}, {"text": "Un module encapsulant plusieurs packages", "is_correct": False}]},
                {"text": "Comment créer un map en Go?", "answers": [{"text": "m := make(map[string]int)", "is_correct": True}, {"text": "m := map<string, int>{}", "is_correct": False}, {"text": "m := new Map(string, int)", "is_correct": False}, {"text": "var m map = string:int", "is_correct": False}]},
                {"text": "Que fait panic() en Go?", "answers": [{"text": "Arrête l'exécution normale et remonte la pile (récupérable avec recover())", "is_correct": True}, {"text": "Affiche un message d'erreur et continue", "is_correct": False}, {"text": "Lance une goroutine de gestion d'erreur", "is_correct": False}, {"text": "Équivalent à un throw d'exception", "is_correct": False}]},
                {"text": "Qu'est-ce que go.mod?", "answers": [{"text": "Le fichier qui définit le module Go et ses dépendances", "is_correct": True}, {"text": "La configuration du compilateur Go", "is_correct": False}, {"text": "Un fichier de constantes globales", "is_correct": False}, {"text": "Le fichier principal du programme Go", "is_correct": False}]},
            ],
        },
        "avance": {
            "title": "Go - Avancé",
            "level": QuizLevel.avance,
            "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que le select statement en Go?", "answers": [{"text": "Attend sur plusieurs opérations de channels et exécute la première prête", "is_correct": True}, {"text": "Un switch optimisé pour les types Go", "is_correct": False}, {"text": "Un outil de sélection de goroutines", "is_correct": False}, {"text": "Une requête SQL intégrée dans Go", "is_correct": False}]},
                {"text": "Comment implémenter un worker pool en Go?", "answers": [{"text": "Avec un channel de jobs, plusieurs goroutines workers et un channel de résultats", "is_correct": True}, {"text": "Avec la bibliothèque threadpool de la stdlib", "is_correct": False}, {"text": "Avec sync.Pool uniquement", "is_correct": False}, {"text": "Avec le package workers de Go", "is_correct": False}]},
                {"text": "Qu'est-ce que sync.WaitGroup?", "answers": [{"text": "Un compteur pour attendre qu'un groupe de goroutines termine leur exécution", "is_correct": True}, {"text": "Un mutex pour synchroniser l'accès à une variable", "is_correct": False}, {"text": "Un groupe de goroutines avec communication par channel", "is_correct": False}, {"text": "Un outil de synchronisation entre processus OS", "is_correct": False}]},
                {"text": "Qu'est-ce que context.Context en Go?", "answers": [{"text": "Un objet qui transporte des deadlines, annulations et valeurs entre goroutines et API", "is_correct": True}, {"text": "Le contexte d'exécution du programme Go", "is_correct": False}, {"text": "Un gestionnaire de configuration d'application", "is_correct": False}, {"text": "Un type pour les variables de contexte HTTP", "is_correct": False}]},
                {"text": "Qu'est-ce que l'embedding en Go?", "answers": [{"text": "Inclure un type dans un autre pour hériter de ses méthodes sans héritage classique", "is_correct": True}, {"text": "Intégrer du code C dans Go avec cgo", "is_correct": False}, {"text": "Incorporer des assets dans le binaire Go", "is_correct": False}, {"text": "Un mécanisme de composition de channels", "is_correct": False}]},
                {"text": "Que fait //go:generate?", "answers": [{"text": "Une directive pour exécuter des outils de génération de code via 'go generate'", "is_correct": True}, {"text": "Un commentaire pour la documentation godoc", "is_correct": False}, {"text": "Une instruction pour compiler conditionnellement", "is_correct": False}, {"text": "Une macro Go exécutée à la compilation", "is_correct": False}]},
                {"text": "Qu'est-ce que les build tags en Go?", "answers": [{"text": "Des directives (//go:build) qui contrôlent quels fichiers sont inclus à la compilation selon des conditions", "is_correct": True}, {"text": "Des tags de versioning du module", "is_correct": False}, {"text": "Des métadonnées pour go doc", "is_correct": False}, {"text": "Des labels pour identifier les goroutines", "is_correct": False}]},
                {"text": "Qu'est-ce que sync.Mutex vs sync.RWMutex?", "answers": [{"text": "RWMutex permet plusieurs lecteurs simultanés mais un seul écrivain; Mutex bloque tout accès concurrent", "is_correct": True}, {"text": "RWMutex est une version améliorée de Mutex toujours préférable", "is_correct": False}, {"text": "Mutex est pour les goroutines, RWMutex pour les threads OS", "is_correct": False}, {"text": "Aucune différence de performance", "is_correct": False}]},
                {"text": "Qu'est-ce que unsafe.Pointer en Go?", "answers": [{"text": "Un type qui permet de contourner le système de types Go pour manipuler la mémoire directement", "is_correct": True}, {"text": "Un pointeur nullable comme en C", "is_correct": False}, {"text": "Un type pour les opérations bit à bit", "is_correct": False}, {"text": "Un pointeur vers un type interface{}", "is_correct": False}]},
                {"text": "Comment profiler un programme Go?", "answers": [{"text": "Avec le package pprof via net/http/pprof ou runtime/pprof pour CPU, mémoire et goroutines", "is_correct": True}, {"text": "Avec l'outil go profile uniquement", "is_correct": False}, {"text": "En activant -debug=true à la compilation", "is_correct": False}, {"text": "Go n'a pas d'outils de profiling intégrés", "is_correct": False}]},
            ],
        },
    },
}


def add_go_quizzes():
    try:
        category_name = GO_QUIZ_DATA["category"]["name"]
        existing_category = db.query(Category).filter(Category.name == category_name).first()
        if existing_category:
            print(f"✓ Catégorie '{category_name}' existe déjà (ID: {existing_category.id})")
            category = existing_category
        else:
            category = Category(id=str(uuid.uuid4()), name=GO_QUIZ_DATA["category"]["name"], description=GO_QUIZ_DATA["category"]["description"], icon_url=GO_QUIZ_DATA["category"]["icon_url"], is_active=GO_QUIZ_DATA["category"]["is_active"])
            db.add(category)
            db.commit()
            print(f"✓ Catégorie '{category_name}' créée avec succès (ID: {category.id})")

        for level_name, quiz_data in GO_QUIZ_DATA["quizzes"].items():
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

        print("\n✅ Tous les quiz Go ont été ajoutés avec succès!")
    except Exception as e:
        db.rollback()
        print(f"❌ Erreur: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Ajout des quiz Go (débutant, intermédiaire, avancé)...\n")
    add_go_quizzes()