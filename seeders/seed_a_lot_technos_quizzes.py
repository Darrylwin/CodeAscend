"""
Script d'insertion massive de tous les quiz pour toutes les technologies.
Avec mélange aléatoire des réponses et organisation par catégories.

Utilisation:
    python seed_a_lot_quizzes.py
"""

import uuid
import random
from sqlalchemy.orm import Session
from app.db.session import SessionLocal, engine, Base
from app.models import Category, Quiz, Question, Answer, QuizLevel, QuizStatus

# Créer les tables si elles n'existent pas
Base.metadata.create_all(bind=engine)

# =============================================================================
# HELPER
# =============================================================================

def shuffle_answers(answers):
    """Mélange aléatoirement les réponses d'une question"""
    shuffled = answers.copy()
    random.shuffle(shuffled)
    return shuffled

def seed_category(db, data):
    """Fonction générique pour insérer une catégorie et ses quiz"""
    name = data["category"]["name"]
    cat = db.query(Category).filter(Category.name == name).first()
    if cat:
        print(f"✓ Catégorie '{name}' existe déjà")
    else:
        cat = Category(
            id=str(uuid.uuid4()),
            name=name,
            description=data["category"]["description"],
            icon_url=data["category"]["icon_url"],
            is_active=True
        )
        db.add(cat)
        db.commit()
        print(f"✓ Catégorie '{name}' créée (ID: {cat.id})")

    for level_name, quiz_data in data["quizzes"].items():
        qz = db.query(Quiz).filter(
            Quiz.category_id == cat.id,
            Quiz.level == quiz_data["level"]
        ).first()
        
        if qz:
            print(f"  ✓ Quiz '{qz.title}' existe déjà")
        else:
            qz = Quiz(
                id=str(uuid.uuid4()),
                category_id=cat.id,
                title=quiz_data["title"],
                level=quiz_data["level"],
                status=quiz_data["status"]
            )
            db.add(qz)
            db.commit()
            print(f"  ✓ Quiz '{qz.title}' créé")

        for q_i, qdata in enumerate(quiz_data["questions"], 1):
            existing_q = db.query(Question).filter(
                Question.quiz_id == qz.id,
                Question.order == q_i
            ).first()
            
            if existing_q:
                q = existing_q
            else:
                q = Question(
                    id=str(uuid.uuid4()),
                    quiz_id=qz.id,
                    question_text=qdata["text"],
                    order=q_i
                )
                db.add(q)
                db.commit()
                print(f"    ✓ Question {q_i} ajoutée")

            # Mélanger les réponses avant insertion
            shuffled_answers = shuffle_answers(qdata["answers"])
            
            for a_i, adata in enumerate(shuffled_answers, 1):
                if not db.query(Answer).filter(
                    Answer.question_id == q.id,
                    Answer.order == a_i
                ).first():
                    db.add(Answer(
                        id=str(uuid.uuid4()),
                        question_id=q.id,
                        answer_text=adata["text"],
                        is_correct=adata["is_correct"],
                        order=a_i
                    ))
            
            if not existing_q:
                db.commit()


# =============================================================================
# ORGANISATION PAR CATÉGORIES THÉMATIQUES
# =============================================================================

# 1. LANGAGES DE PROGRAMMATION
# -----------------------------------------------------------------------------

PYTHON_DATA = {
    "category": {
        "name": "Python",
        "description": "Quiz pour maîtriser la programmation Python",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Python - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Quel est le mot-clé pour définir une fonction en Python?", "answers": [
                    {"text": "def", "is_correct": True},
                    {"text": "function", "is_correct": False},
                    {"text": "func", "is_correct": False},
                    {"text": "define", "is_correct": False}
                ]},
                {"text": "Que retourne la fonction len() sur une chaîne 'Hello'?", "answers": [
                    {"text": "5", "is_correct": True},
                    {"text": "'Hello'", "is_correct": False},
                    {"text": "4", "is_correct": False},
                    {"text": "None", "is_correct": False}
                ]},
                {"text": "Comment accéder au premier élément d'une liste?", "answers": [
                    {"text": "liste[0]", "is_correct": True},
                    {"text": "liste[1]", "is_correct": False},
                    {"text": "liste.first()", "is_correct": False},
                    {"text": "liste[:]", "is_correct": False}
                ]},
                {"text": "Quel type de données Python est immutable?", "answers": [
                    {"text": "tuple", "is_correct": True},
                    {"text": "list", "is_correct": False},
                    {"text": "dict", "is_correct": False},
                    {"text": "set", "is_correct": False}
                ]},
                {"text": "Que affiche print('Python' * 2)?", "answers": [
                    {"text": "PythonPython", "is_correct": True},
                    {"text": "Python2", "is_correct": False},
                    {"text": "Erreur", "is_correct": False},
                    {"text": "2", "is_correct": False}
                ]},
                {"text": "Comment créer une liste vide en Python?", "answers": [
                    {"text": "[]", "is_correct": True},
                    {"text": "list()", "is_correct": True},
                    {"text": "{}", "is_correct": False},
                    {"text": "new list", "is_correct": False}
                ]},
                {"text": "Quel opérateur vérifie l'égalité en Python?", "answers": [
                    {"text": "==", "is_correct": True},
                    {"text": "=", "is_correct": False},
                    {"text": "is", "is_correct": False},
                    {"text": "===", "is_correct": False}
                ]},
                {"text": "Que retourne 5 // 2 en Python?", "answers": [
                    {"text": "2", "is_correct": True},
                    {"text": "2.5", "is_correct": False},
                    {"text": "3", "is_correct": False},
                    {"text": "Erreur", "is_correct": False}
                ]},
                {"text": "Comment ajouter un élément à une liste?", "answers": [
                    {"text": "liste.append(element)", "is_correct": True},
                    {"text": "liste.add(element)", "is_correct": False},
                    {"text": "liste.push(element)", "is_correct": False},
                    {"text": "liste.insert(element)", "is_correct": False}
                ]},
                {"text": "Quel est le résultat de bool('False')?", "answers": [
                    {"text": "True", "is_correct": True},
                    {"text": "False", "is_correct": False},
                    {"text": "None", "is_correct": False},
                    {"text": "Erreur", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Python - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Que retourne list(map(lambda x: x**2, [1,2,3]))?", "answers": [
                    {"text": "[1, 4, 9]", "is_correct": True},
                    {"text": "[1, 2, 3]", "is_correct": False},
                    {"text": "[2, 4, 6]", "is_correct": False},
                    {"text": "Erreur", "is_correct": False}
                ]},
                {"text": "Quelle syntaxe crée un dictionnaire en Python?", "answers": [
                    {"text": "{'clé': 'valeur'}", "is_correct": True},
                    {"text": "('clé': 'valeur')", "is_correct": False},
                    {"text": "['clé': 'valeur']", "is_correct": False},
                    {"text": "'clé': 'valeur'", "is_correct": False}
                ]},
                {"text": "Que retourne [x for x in range(5) if x % 2 == 0]?", "answers": [
                    {"text": "[0, 2, 4]", "is_correct": True},
                    {"text": "[1, 3]", "is_correct": False},
                    {"text": "[0, 1, 2, 3, 4]", "is_correct": False},
                    {"text": "[2, 4]", "is_correct": False}
                ]},
                {"text": "Quelle méthode crée une copie d'une liste?", "answers": [
                    {"text": "liste.copy()", "is_correct": True},
                    {"text": "liste.clone()", "is_correct": False},
                    {"text": "liste.duplicate()", "is_correct": False},
                    {"text": "copy(liste)", "is_correct": False}
                ]},
                {"text": "Que signifie *args dans une fonction?", "answers": [
                    {"text": "Nombre variable d'arguments positionnels", "is_correct": True},
                    {"text": "Arguments nommés", "is_correct": False},
                    {"text": "Arguments optionnels", "is_correct": False},
                    {"text": "Arguments de liste", "is_correct": False}
                ]},
                {"text": "Comment accéder au dernier élément d'une liste?", "answers": [
                    {"text": "liste[-1]", "is_correct": True},
                    {"text": "liste[last]", "is_correct": False},
                    {"text": "liste.last()", "is_correct": False},
                    {"text": "liste[-0]", "is_correct": False}
                ]},
                {"text": "Quel est le résultat de ''.join(['a', 'b', 'c'])?", "answers": [
                    {"text": "'abc'", "is_correct": True},
                    {"text": "['a', 'b', 'c']", "is_correct": False},
                    {"text": "'a,b,c'", "is_correct": False},
                    {"text": "Erreur", "is_correct": False}
                ]},
                {"text": "Que retourne type([])?", "answers": [
                    {"text": "<class 'list'>", "is_correct": True},
                    {"text": "list", "is_correct": False},
                    {"text": "'list'", "is_correct": False},
                    {"text": "array", "is_correct": False}
                ]},
                {"text": "Comment vérifier si une clé existe dans un dictionnaire?", "answers": [
                    {"text": "'clé' in dictionnaire", "is_correct": True},
                    {"text": "dictionnaire.has_key('clé')", "is_correct": False},
                    {"text": "find('clé') in dictionnaire", "is_correct": False},
                    {"text": "dictionnaire.contains('clé')", "is_correct": False}
                ]},
                {"text": "Que retourne dict.get('clé', 'défaut') si la clé n'existe pas?", "answers": [
                    {"text": "'défaut'", "is_correct": True},
                    {"text": "None", "is_correct": False},
                    {"text": "KeyError", "is_correct": False},
                    {"text": "'clé'", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Python - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que le décorateur @property?", "answers": [
                    {"text": "Convertir une méthode en attribut", "is_correct": True},
                    {"text": "Créer une classe", "is_correct": False},
                    {"text": "Définir une constante", "is_correct": False},
                    {"text": "Importer un module", "is_correct": False}
                ]},
                {"text": "Que retourne next(iter([1,2,3]))?", "answers": [
                    {"text": "1", "is_correct": True},
                    {"text": "[1,2,3]", "is_correct": False},
                    {"text": "2", "is_correct": False},
                    {"text": "Erreur", "is_correct": False}
                ]},
                {"text": "Quel est le but du **kwargs?", "answers": [
                    {"text": "Nombre variable d'arguments nommés", "is_correct": True},
                    {"text": "Arguments positionnels", "is_correct": False},
                    {"text": "Exponentiation", "is_correct": False},
                    {"text": "Commentaire", "is_correct": False}
                ]},
                {"text": "Comment créer un générateur en Python?", "answers": [
                    {"text": "Avec yield", "is_correct": True},
                    {"text": "Avec return", "is_correct": False},
                    {"text": "Avec Generator()", "is_correct": False},
                    {"text": "Avec gen()", "is_correct": False}
                ]},
                {"text": "Que signifie héritage multiple en Python?", "answers": [
                    {"text": "Une classe hérite de plusieurs classes", "is_correct": True},
                    {"text": "Une classe hérite d'une seule classe", "is_correct": False},
                    {"text": "Copier une classe", "is_correct": False},
                    {"text": "Fusionner deux classes", "is_correct": False}
                ]},
                {"text": "Quel est le rôle de __init__?", "answers": [
                    {"text": "Initialiser les attributs d'une instance", "is_correct": True},
                    {"text": "Définir une variable globale", "is_correct": False},
                    {"text": "Importer un module", "is_correct": False},
                    {"text": "Créer une constante", "is_correct": False}
                ]},
                {"text": "Que retourne (lambda x: x + 1)(5)?", "answers": [
                    {"text": "6", "is_correct": True},
                    {"text": "5", "is_correct": False},
                    {"text": "lambda", "is_correct": False},
                    {"text": "Erreur", "is_correct": False}
                ]},
                {"text": "Comment gérer les exceptions en Python?", "answers": [
                    {"text": "try/except", "is_correct": True},
                    {"text": "try/catch", "is_correct": False},
                    {"text": "if/except", "is_correct": False},
                    {"text": "handle/error", "is_correct": False}
                ]},
                {"text": "Que retourne hasattr(obj, 'attr')?", "answers": [
                    {"text": "True/False selon que 'attr' existe", "is_correct": True},
                    {"text": "La valeur de l'attribut", "is_correct": False},
                    {"text": "L'objet", "is_correct": False},
                    {"text": "Erreur", "is_correct": False}
                ]},
                {"text": "Que signifie GIL en Python?", "answers": [
                    {"text": "Global Interpreter Lock", "is_correct": True},
                    {"text": "Global Instance Library", "is_correct": False},
                    {"text": "General Interface Layer", "is_correct": False},
                    {"text": "Graph Iteration Logic", "is_correct": False}
                ]},
            ],
        },
    },
}

JAVASCRIPT_DATA = {
    "category": {
        "name": "JavaScript",
        "description": "Quiz pour maîtriser la programmation JavaScript",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "JavaScript - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Quel mot-clé déclare une variable en JavaScript (moderne)?", "answers": [
                    {"text": "let", "is_correct": True},
                    {"text": "var", "is_correct": False},
                    {"text": "dim", "is_correct": False},
                    {"text": "variable", "is_correct": False}
                ]},
                {"text": "Que retourne typeof 42?", "answers": [
                    {"text": "'number'", "is_correct": True},
                    {"text": "'integer'", "is_correct": False},
                    {"text": "'string'", "is_correct": False},
                    {"text": "42", "is_correct": False}
                ]},
                {"text": "Comment afficher un message dans la console?", "answers": [
                    {"text": "console.log('message')", "is_correct": True},
                    {"text": "print('message')", "is_correct": False},
                    {"text": "echo 'message'", "is_correct": False},
                    {"text": "log('message')", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre == et ===?", "answers": [
                    {"text": "=== compare la valeur ET le type", "is_correct": True},
                    {"text": "== compare la valeur ET le type", "is_correct": False},
                    {"text": "Aucune différence", "is_correct": False},
                    {"text": "=== est plus lent", "is_correct": False}
                ]},
                {"text": "Comment créer un tableau en JavaScript?", "answers": [
                    {"text": "const arr = [1, 2, 3]", "is_correct": True},
                    {"text": "const arr = (1, 2, 3)", "is_correct": False},
                    {"text": "const arr = {1, 2, 3}", "is_correct": False},
                    {"text": "const arr = new Array[1, 2, 3]", "is_correct": False}
                ]},
                {"text": "Que retourne Boolean('') en JavaScript?", "answers": [
                    {"text": "false", "is_correct": True},
                    {"text": "true", "is_correct": False},
                    {"text": "null", "is_correct": False},
                    {"text": "undefined", "is_correct": False}
                ]},
                {"text": "Comment définir une fonction fléchée?", "answers": [
                    {"text": "const fn = () => {}", "is_correct": True},
                    {"text": "const fn = function => {}", "is_correct": False},
                    {"text": "const fn -> {}", "is_correct": False},
                    {"text": "def fn() {}", "is_correct": False}
                ]},
                {"text": "Quelle méthode ajoute un élément à la fin d'un tableau?", "answers": [
                    {"text": "push()", "is_correct": True},
                    {"text": "append()", "is_correct": False},
                    {"text": "add()", "is_correct": False},
                    {"text": "insert()", "is_correct": False}
                ]},
                {"text": "Que signifie NaN en JavaScript?", "answers": [
                    {"text": "Not a Number", "is_correct": True},
                    {"text": "Null and Nothing", "is_correct": False},
                    {"text": "New and Null", "is_correct": False},
                    {"text": "Non-Assigned Node", "is_correct": False}
                ]},
                {"text": "Comment accéder à la longueur d'un tableau?", "answers": [
                    {"text": "arr.length", "is_correct": True},
                    {"text": "arr.size()", "is_correct": False},
                    {"text": "len(arr)", "is_correct": False},
                    {"text": "arr.count", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "JavaScript - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Que retourne [1, 2, 3].map(x => x * 2)?", "answers": [
                    {"text": "[2, 4, 6]", "is_correct": True},
                    {"text": "[1, 2, 3]", "is_correct": False},
                    {"text": "6", "is_correct": False},
                    {"text": "[3, 4, 5]", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le hoisting en JavaScript?", "answers": [
                    {"text": "Remontée des déclarations en haut du scope", "is_correct": True},
                    {"text": "Copier une variable", "is_correct": False},
                    {"text": "Supprimer une variable", "is_correct": False},
                    {"text": "Optimiser le code", "is_correct": False}
                ]},
                {"text": "Quelle méthode permet de filtrer un tableau?", "answers": [
                    {"text": "filter()", "is_correct": True},
                    {"text": "find()", "is_correct": False},
                    {"text": "select()", "is_correct": False},
                    {"text": "where()", "is_correct": False}
                ]},
                {"text": "Comment destructurer un objet en JavaScript?", "answers": [
                    {"text": "const { a, b } = obj", "is_correct": True},
                    {"text": "const [a, b] = obj", "is_correct": False},
                    {"text": "const a, b = obj", "is_correct": False},
                    {"text": "let a = obj.a, b = obj.b", "is_correct": False}
                ]},
                {"text": "Que fait l'opérateur spread (...)?", "answers": [
                    {"text": "Étale les éléments d'un itérable", "is_correct": True},
                    {"text": "Crée une copie profonde", "is_correct": False},
                    {"text": "Fusionne deux types", "is_correct": False},
                    {"text": "Déclare un rest parameter", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'une Promise en JavaScript?", "answers": [
                    {"text": "Un objet représentant une opération asynchrone", "is_correct": True},
                    {"text": "Une fonction synchrone", "is_correct": False},
                    {"text": "Un type de variable", "is_correct": False},
                    {"text": "Une méthode de tableau", "is_correct": False}
                ]},
                {"text": "Que retourne Object.keys({ a: 1, b: 2 })?", "answers": [
                    {"text": "['a', 'b']", "is_correct": True},
                    {"text": "[1, 2]", "is_correct": False},
                    {"text": "['a: 1', 'b: 2']", "is_correct": False},
                    {"text": "{a: 1, b: 2}", "is_correct": False}
                ]},
                {"text": "Comment fusionner deux objets en JavaScript?", "answers": [
                    {"text": "{ ...obj1, ...obj2 }", "is_correct": True},
                    {"text": "obj1 + obj2", "is_correct": False},
                    {"text": "obj1.merge(obj2)", "is_correct": False},
                    {"text": "Object.join(obj1, obj2)", "is_correct": False}
                ]},
                {"text": "Quelle méthode enchaîne sur une Promise résolue?", "answers": [
                    {"text": ".then()", "is_correct": True},
                    {"text": ".next()", "is_correct": False},
                    {"text": ".resolve()", "is_correct": False},
                    {"text": ".success()", "is_correct": False}
                ]},
                {"text": "Que retourne [1, 2, 3].reduce((acc, x) => acc + x, 0)?", "answers": [
                    {"text": "6", "is_correct": True},
                    {"text": "3", "is_correct": False},
                    {"text": "[1, 2, 3]", "is_correct": False},
                    {"text": "0", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "JavaScript - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que la closure en JavaScript?", "answers": [
                    {"text": "Une fonction qui retient l'accès à son scope lexical", "is_correct": True},
                    {"text": "Une fonction qui se ferme après exécution", "is_correct": False},
                    {"text": "Un objet immuable", "is_correct": False},
                    {"text": "Une méthode de classe privée", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que l'event loop en JavaScript?", "answers": [
                    {"text": "Mécanisme gérant l'exécution asynchrone via une file de callbacks", "is_correct": True},
                    {"text": "Une boucle for spéciale pour les événements DOM", "is_correct": False},
                    {"text": "Un pattern de design pattern", "is_correct": False},
                    {"text": "Le moteur de rendu du navigateur", "is_correct": False}
                ]},
                {"text": "Que fait Object.freeze()?", "answers": [
                    {"text": "Rend un objet immuable (ne peut plus être modifié)", "is_correct": True},
                    {"text": "Copie un objet en profondeur", "is_correct": False},
                    {"text": "Supprime toutes les propriétés", "is_correct": False},
                    {"text": "Convertit en chaîne JSON", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre call() et apply()?", "answers": [
                    {"text": "call() passe les args un à un, apply() via un tableau", "is_correct": True},
                    {"text": "apply() est plus rapide", "is_correct": False},
                    {"text": "call() retourne une fonction, apply() l'exécute", "is_correct": False},
                    {"text": "Aucune différence", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un WeakMap?", "answers": [
                    {"text": "Un Map dont les clés sont des références faibles (objets uniquement)", "is_correct": True},
                    {"text": "Un Map moins performant", "is_correct": False},
                    {"text": "Un Map pour les types primitifs", "is_correct": False},
                    {"text": "Un Map immuable", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le Proxy en JavaScript?", "answers": [
                    {"text": "Il intercepte et redéfinit les opérations fondamentales d'un objet", "is_correct": True},
                    {"text": "Il clone un objet", "is_correct": False},
                    {"text": "Il crée un serveur proxy", "is_correct": False},
                    {"text": "Il masque les propriétés privées", "is_correct": False}
                ]},
                {"text": "Que retourne Promise.all([p1, p2, p3]) si p2 échoue?", "answers": [
                    {"text": "La Promise globale est rejetée immédiatement", "is_correct": True},
                    {"text": "Les autres Promises continuent et retournent leurs valeurs", "is_correct": False},
                    {"text": "Retourne null pour p2 et les autres valeurs", "is_correct": False},
                    {"text": "Retourne un tableau partiel", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Temporal Dead Zone (TDZ)?", "answers": [
                    {"text": "La zone où une variable let/const est déclarée mais pas encore initialisée", "is_correct": True},
                    {"text": "Une zone mémoire réservée au garbage collector", "is_correct": False},
                    {"text": "Un état des Promises en attente", "is_correct": False},
                    {"text": "Une erreur de timeout", "is_correct": False}
                ]},
                {"text": "Comment implémenter un itérateur personnalisé?", "answers": [
                    {"text": "En définissant Symbol.iterator sur l'objet", "is_correct": True},
                    {"text": "En étendant la classe Iterator", "is_correct": False},
                    {"text": "En utilisant Object.iterate()", "is_correct": False},
                    {"text": "En définissant une méthode .next() seule", "is_correct": False}
                ]},
                {"text": "Quelle est la particularité de async/await vs .then()/.catch()?", "answers": [
                    {"text": "Syntaxe synchrone pour code asynchrone, même comportement sous le capot", "is_correct": True},
                    {"text": "async/await est plus performant", "is_correct": False},
                    {"text": "async/await bloque le thread principal", "is_correct": False},
                    {"text": ".then() ne supporte pas les erreurs", "is_correct": False}
                ]},
            ],
        },
    },
}

TYPESCRIPT_DATA = {
    "category": {
        "name": "TypeScript",
        "description": "Quiz pour maîtriser TypeScript et le typage statique",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "TypeScript - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Comment annoter le type d'une variable en TypeScript?", "answers": [
                    {"text": "let age: number = 25", "is_correct": True},
                    {"text": "let age = number(25)", "is_correct": False},
                    {"text": "let age <number> = 25", "is_correct": False},
                    {"text": "number let age = 25", "is_correct": False}
                ]},
                {"text": "Quel est le type TypeScript pour une chaîne de caractères?", "answers": [
                    {"text": "string", "is_correct": True},
                    {"text": "String", "is_correct": False},
                    {"text": "str", "is_correct": False},
                    {"text": "char", "is_correct": False}
                ]},
                {"text": "Comment définir un tableau de nombres en TypeScript?", "answers": [
                    {"text": "number[]", "is_correct": True},
                    {"text": "Array<number>", "is_correct": True},
                    {"text": "[number]", "is_correct": False},
                    {"text": "numbers", "is_correct": False}
                ]},
                {"text": "Que signifie le type 'any' en TypeScript?", "answers": [
                    {"text": "Accepte n'importe quel type, désactive le typage", "is_correct": True},
                    {"text": "Un type nullable", "is_correct": False},
                    {"text": "Un type générique", "is_correct": False},
                    {"text": "Un type optionnel", "is_correct": False}
                ]},
                {"text": "Comment rendre une propriété optionnelle dans une interface?", "answers": [
                    {"text": "name?: string", "is_correct": True},
                    {"text": "name: string?", "is_correct": False},
                    {"text": "optional name: string", "is_correct": False},
                    {"text": "name: string | null", "is_correct": False}
                ]},
                {"text": "Comment définir une interface en TypeScript?", "answers": [
                    {"text": "interface User { name: string }", "is_correct": True},
                    {"text": "type interface User = { name: string }", "is_correct": False},
                    {"text": "struct User { name: string }", "is_correct": False},
                    {"text": "class interface User { name: string }", "is_correct": False}
                ]},
                {"text": "Que représente le type 'void'?", "answers": [
                    {"text": "Une fonction qui ne retourne rien", "is_correct": True},
                    {"text": "Une variable nulle", "is_correct": False},
                    {"text": "Un type indéfini", "is_correct": False},
                    {"text": "Un tableau vide", "is_correct": False}
                ]},
                {"text": "Comment créer un type union en TypeScript?", "answers": [
                    {"text": "string | number", "is_correct": True},
                    {"text": "string & number", "is_correct": False},
                    {"text": "string + number", "is_correct": False},
                    {"text": "string | | number", "is_correct": False}
                ]},
                {"text": "Quelle commande compile un fichier TypeScript?", "answers": [
                    {"text": "tsc fichier.ts", "is_correct": True},
                    {"text": "ts-compile fichier.ts", "is_correct": False},
                    {"text": "node fichier.ts", "is_correct": False},
                    {"text": "build fichier.ts", "is_correct": False}
                ]},
                {"text": "Que retourne le type 'never'?", "answers": [
                    {"text": "Une valeur qui ne se produit jamais (fonction qui throw toujours)", "is_correct": True},
                    {"text": "Une valeur nulle", "is_correct": False},
                    {"text": "Un type optionnel", "is_correct": False},
                    {"text": "Une fonction asynchrone", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "TypeScript - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Quelle est la différence entre interface et type alias?", "answers": [
                    {"text": "interface est extensible via declaration merging, type alias non", "is_correct": True},
                    {"text": "type alias est plus performant", "is_correct": False},
                    {"text": "interface ne supporte pas les unions", "is_correct": False},
                    {"text": "Aucune différence", "is_correct": False}
                ]},
                {"text": "Comment utiliser un générique en TypeScript?", "answers": [
                    {"text": "function identity<T>(arg: T): T { return arg; }", "is_correct": True},
                    {"text": "function identity(arg: generic): generic { return arg; }", "is_correct": False},
                    {"text": "function identity(arg: any): any { return arg; }", "is_correct": False},
                    {"text": "function identity<arg>(T: arg): arg { return T; }", "is_correct": False}
                ]},
                {"text": "Que fait l'opérateur 'as' en TypeScript?", "answers": [
                    {"text": "Type assertion - force TypeScript à considérer un type spécifique", "is_correct": True},
                    {"text": "Convertit une valeur vers un autre type à l'exécution", "is_correct": False},
                    {"text": "Crée un alias de variable", "is_correct": False},
                    {"text": "Hérite d'une interface", "is_correct": False}
                ]},
                {"text": "Comment définir un type intersection?", "answers": [
                    {"text": "type AB = A & B", "is_correct": True},
                    {"text": "type AB = A | B", "is_correct": False},
                    {"text": "type AB = A + B", "is_correct": False},
                    {"text": "interface AB extends A, B {}", "is_correct": False}
                ]},
                {"text": "Que sont les Mapped Types en TypeScript?", "answers": [
                    {"text": "Des types créés en itérant sur les propriétés d'un autre type", "is_correct": True},
                    {"text": "Des méthodes de transformation de tableaux typés", "is_correct": False},
                    {"text": "Des types pour les Map natifs JS", "is_correct": False},
                    {"text": "Des types génériques avec contraintes", "is_correct": False}
                ]},
                {"text": "Que fait le type utilitaire Partial<T>?", "answers": [
                    {"text": "Rend toutes les propriétés de T optionnelles", "is_correct": True},
                    {"text": "Crée une copie partielle de T", "is_correct": False},
                    {"text": "Supprime certaines propriétés de T", "is_correct": False},
                    {"text": "Rend T readonly", "is_correct": False}
                ]},
                {"text": "Comment contraindre un générique à un type spécifique?", "answers": [
                    {"text": "function fn<T extends string>(arg: T)", "is_correct": True},
                    {"text": "function fn<T: string>(arg: T)", "is_correct": False},
                    {"text": "function fn<T implements string>(arg: T)", "is_correct": False},
                    {"text": "function fn<T = string>(arg: T)", "is_correct": False}
                ]},
                {"text": "Que fait le type utilitaire Required<T>?", "answers": [
                    {"text": "Rend toutes les propriétés optionnelles de T obligatoires", "is_correct": True},
                    {"text": "Ajoute des propriétés requises à T", "is_correct": False},
                    {"text": "Valide que T est non-null", "is_correct": False},
                    {"text": "Rend T immuable", "is_correct": False}
                ]},
                {"text": "Comment typer un enum en TypeScript?", "answers": [
                    {"text": "enum Direction { Up, Down, Left, Right }", "is_correct": True},
                    {"text": "const Direction = enum { Up, Down }", "is_correct": False},
                    {"text": "type Direction = 'Up' | 'Down'", "is_correct": False},
                    {"text": "interface Direction { Up: number }", "is_correct": False}
                ]},
                {"text": "Que retourne keyof T?", "answers": [
                    {"text": "Un union type de toutes les clés de T", "is_correct": True},
                    {"text": "Un tableau des clés de T", "is_correct": False},
                    {"text": "La première clé de T", "is_correct": False},
                    {"text": "Le nombre de propriétés de T", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "TypeScript - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Que sont les Conditional Types en TypeScript?", "answers": [
                    {"text": "T extends U ? X : Y - types qui dépendent d'une condition", "is_correct": True},
                    {"text": "Des types avec des valeurs par défaut", "is_correct": False},
                    {"text": "Des types qui changent selon l'environnement", "is_correct": False},
                    {"text": "Des types optionnels avec fallback", "is_correct": False}
                ]},
                {"text": "Que fait le mot-clé infer dans les Conditional Types?", "answers": [
                    {"text": "Il infère et capture un type dans une branche de condition", "is_correct": True},
                    {"text": "Il désactive l'inférence de type automatique", "is_correct": False},
                    {"text": "Il force TypeScript à déduire le type", "is_correct": False},
                    {"text": "Il crée un type temporaire", "is_correct": False}
                ]},
                {"text": "Que fait Awaited<T> en TypeScript 4.5+?", "answers": [
                    {"text": "Extrait le type résolu d'une Promise imbriquée", "is_correct": True},
                    {"text": "Crée une Promise qui attend T ms", "is_correct": False},
                    {"text": "Rend T asynchrone", "is_correct": False},
                    {"text": "Transforme T en Observable", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le declaration merging?", "answers": [
                    {"text": "Deux déclarations d'interface avec le même nom fusionnent automatiquement", "is_correct": True},
                    {"text": "Fusionner deux fichiers .ts en un", "is_correct": False},
                    {"text": "Combiner deux modules en un", "is_correct": False},
                    {"text": "Étendre une classe avec une interface", "is_correct": False}
                ]},
                {"text": "Comment créer un type Template Literal en TypeScript?", "answers": [
                    {"text": "type Greeting = `Hello ${string}`", "is_correct": True},
                    {"text": "type Greeting = 'Hello ' + string", "is_correct": False},
                    {"text": "type Greeting = string.template('Hello')", "is_correct": False},
                    {"text": "type Greeting = Template<'Hello', string>", "is_correct": False}
                ]},
                {"text": "Que fait le type utilitaire ReturnType<T>?", "answers": [
                    {"text": "Extrait le type de retour d'une fonction T", "is_correct": True},
                    {"text": "Force T à retourner un type spécifique", "is_correct": False},
                    {"text": "Rend le type de retour optionnel", "is_correct": False},
                    {"text": "Crée une fonction qui retourne T", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Discriminated Union?", "answers": [
                    {"text": "Un union type avec une propriété commune permettant de le discriminer", "is_correct": True},
                    {"text": "Un union type excluant certains types", "is_correct": False},
                    {"text": "Un union de types primitifs uniquement", "is_correct": False},
                    {"text": "Un type créé avec Exclude<>", "is_correct": False}
                ]},
                {"text": "Que fait le type utilitaire Extract<T, U>?", "answers": [
                    {"text": "Extrait de T les types assignables à U", "is_correct": True},
                    {"text": "Extrait la valeur U de T", "is_correct": False},
                    {"text": "Supprime U de T", "is_correct": False},
                    {"text": "Crée un nouveau type à partir de T et U", "is_correct": False}
                ]},
                {"text": "Comment utiliser un decorator de classe en TypeScript?", "answers": [
                    {"text": "@decorator class MyClass {}", "is_correct": True},
                    {"text": "class MyClass @decorator {}", "is_correct": False},
                    {"text": "class @decorator MyClass {}", "is_correct": False},
                    {"text": "#decorator class MyClass {}", "is_correct": False}
                ]},
                {"text": "Que fait le type satisfies introduit en TypeScript 4.9?", "answers": [
                    {"text": "Valide qu'une valeur satisfait un type sans perdre son type inféré précis", "is_correct": True},
                    {"text": "Remplace le mot-clé as pour les assertions", "is_correct": False},
                    {"text": "Force une valeur à correspondre exactement à un type", "is_correct": False},
                    {"text": "Crée un type conditionnel basé sur une valeur", "is_correct": False}
                ]},
            ],
        },
    },
}

DART_DATA = {
    "category": {
        "name": "Dart",
        "description": "Quiz pour maîtriser Dart, le langage de Flutter",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/dart/dart-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Dart - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Quel est le point d'entrée d'un programme Dart?", "answers": [
                    {"text": "void main() {}", "is_correct": True},
                    {"text": "int main() {}", "is_correct": False},
                    {"text": "main() {}", "is_correct": True},
                    {"text": "void start() {}", "is_correct": False}
                ]},
                {"text": "Comment déclarer une variable en Dart?", "answers": [
                    {"text": "var nom = 'valeur'", "is_correct": True},
                    {"text": "let nom = 'valeur'", "is_correct": False},
                    {"text": "String nom = 'valeur'", "is_correct": True},
                    {"text": "const nom = 'valeur'", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre final et const?", "answers": [
                    {"text": "final est initialisé à l'exécution (une fois), const à la compilation", "is_correct": True},
                    {"text": "const peut changer, final non", "is_correct": False},
                    {"text": "final est pour les classes, const pour les variables", "is_correct": False},
                    {"text": "Aucune différence", "is_correct": False}
                ]},
                {"text": "Comment créer une fonction en Dart?", "answers": [
                    {"text": "Type nom(paramètres) { }", "is_correct": True},
                    {"text": "function nom() { }", "is_correct": False},
                    {"text": "def nom():", "is_correct": False},
                    {"text": "func nom() { }", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les types optionnels en Dart (null safety)?", "answers": [
                    {"text": "Les types sont non-nullables par défaut, ? pour nullable", "is_correct": True},
                    {"text": "Tous les types sont nullables par défaut", "is_correct": False},
                    {"text": "Dart n'a pas de null safety", "is_correct": False},
                    {"text": "On utilise Optional<T> comme en Java", "is_correct": False}
                ]},
                {"text": "Comment créer une liste en Dart?", "answers": [
                    {"text": "var list = [1, 2, 3]", "is_correct": True},
                    {"text": "var list = List<int>()", "is_correct": True},
                    {"text": "var list = new Array(1, 2, 3)", "is_correct": False},
                    {"text": "var list = []", "is_correct": True}
                ]},
                {"text": "Qu'est-ce que les futures en Dart?", "answers": [
                    {"text": "Un objet qui représente un résultat asynchrone", "is_correct": True},
                    {"text": "Une classe pour les dates futures", "is_correct": False},
                    {"text": "Un type de variable temporaire", "is_correct": False},
                    {"text": "Une boucle infinie", "is_correct": False}
                ]},
                {"text": "Comment gérer les exceptions en Dart?", "answers": [
                    {"text": "try { } on Exception catch (e) { } finally { }", "is_correct": True},
                    {"text": "try { } catch (Exception e) { }", "is_correct": False},
                    {"text": "begin { } rescue { }", "is_correct": False},
                    {"text": "handle { }", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le cascade operator (..) en Dart?", "answers": [
                    {"text": "Permet d'enchaîner plusieurs opérations sur le même objet", "is_correct": True},
                    {"text": "Un opérateur de comparaison", "is_correct": False},
                    {"text": "Un opérateur de propagation", "is_correct": False},
                    {"text": "Un commentaire", "is_correct": False}
                ]},
                {"text": "Comment créer une classe en Dart?", "answers": [
                    {"text": "class MaClasse { }", "is_correct": True},
                    {"text": "interface MaClasse { }", "is_correct": False},
                    {"text": "struct MaClasse { }", "is_correct": False},
                    {"text": "MaClasse = class { }", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Dart - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que async/await en Dart?", "answers": [
                    {"text": "Permet d'écrire du code asynchrone de manière synchrone", "is_correct": True},
                    {"text": "Exécute du code en parallèle", "is_correct": False},
                    {"text": "Crée des threads", "is_correct": False},
                    {"text": "Gère les événements utilisateur", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un mixin en Dart?", "answers": [
                    {"text": "Une classe sans constructeur pour réutiliser du code dans plusieurs classes", "is_correct": True},
                    {"text": "Une interface avec implémentation", "is_correct": False},
                    {"text": "Un type de données", "is_correct": False},
                    {"text": "Une fonction d'ordre supérieur", "is_correct": False}
                ]},
                {"text": "Comment fonctionne l'héritage en Dart?", "answers": [
                    {"text": "extends pour une seule classe, implements pour les interfaces", "is_correct": True},
                    {"text": "Héritage multiple possible avec extends", "is_correct": False},
                    {"text": "Dart n'a pas d'héritage", "is_correct": False},
                    {"text": "with pour l'héritage", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les extensions en Dart?", "answers": [
                    {"text": "Ajouter des fonctionnalités à des classes existantes", "is_correct": True},
                    {"text": "Étendre une classe existante", "is_correct": False},
                    {"text": "Un fichier de configuration", "is_correct": False},
                    {"text": "Une bibliothèque externe", "is_correct": False}
                ]},
                {"text": "Comment utiliser les génériques en Dart?", "answers": [
                    {"text": "class MaClasse<T> { T value; }", "is_correct": True},
                    {"text": "class MaClasse(T) { }", "is_correct": False},
                    {"text": "class MaClasse<Type> { }", "is_correct": False},
                    {"text": "Dart n'a pas de génériques", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les isolates en Dart?", "answers": [
                    {"text": "Des threads indépendants avec leur propre mémoire", "is_correct": True},
                    {"text": "Des widgets isolés", "is_correct": False},
                    {"text": "Des classes privées", "is_correct": False},
                    {"text": "Un pattern de conception", "is_correct": False}
                ]},
                {"text": "Comment créer une factory constructor?", "answers": [
                    {"text": "factory MaClasse() { return instance; }", "is_correct": True},
                    {"text": "static MaClasse() { }", "is_correct": False},
                    {"text": "new MaClasse()", "is_correct": False},
                    {"text": "constructor MaClasse()", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les streams en Dart?", "answers": [
                    {"text": "Un flux de données asynchrones", "is_correct": True},
                    {"text": "Un type de fichier", "is_correct": False},
                    {"text": "Une connexion réseau", "is_correct": False},
                    {"text": "Un buffer mémoire", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le package manager pub?", "answers": [
                    {"text": "Gère les dépendances via pubspec.yaml", "is_correct": True},
                    {"text": "Compile le code Dart", "is_correct": False},
                    {"text": "Crée des projets Dart", "is_correct": False},
                    {"text": "Teste les applications", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les annotations en Dart?", "answers": [
                    {"text": "Des métadonnées pour les classes/méthodes (ex: @override)", "is_correct": True},
                    {"text": "Des commentaires spéciaux", "is_correct": False},
                    {"text": "Des décorateurs comme en Python", "is_correct": False},
                    {"text": "Des types de données", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Dart - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que le tree shaking en Dart?", "answers": [
                    {"text": "Supprime le code mort à la compilation", "is_correct": True},
                    {"text": "Optimise l'arbre des widgets", "is_correct": False},
                    {"text": "Une technique de garbage collection", "is_correct": False},
                    {"text": "Un algorithme de tri", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le AOT (Ahead Of Time) compilation?", "answers": [
                    {"text": "Compile le code Dart en code natif avant l'exécution", "is_correct": True},
                    {"text": "Compile à la volée pendant l'exécution", "is_correct": False},
                    {"text": "Interprète le code ligne par ligne", "is_correct": False},
                    {"text": "Génère du bytecode Java", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Dart DevTools?", "answers": [
                    {"text": "Une suite d'outils de debugging et profiling", "is_correct": True},
                    {"text": "Un IDE pour Dart", "is_correct": False},
                    {"text": "Un compilateur en ligne", "is_correct": False},
                    {"text": "Un gestionnaire de packages", "is_correct": False}
                ]},
                {"text": "Comment implémenter le pattern Singleton en Dart?", "answers": [
                    {"text": "factory constructor avec instance statique", "is_correct": True},
                    {"text": "class Singleton { }", "is_correct": False},
                    {"text": "static final instance = Singleton._();", "is_correct": True},
                    {"text": "Avec un mixin", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le zone en Dart?", "answers": [
                    {"text": "Un contexte d'exécution qui capture les opérations asynchrones", "is_correct": True},
                    {"text": "Une région mémoire", "is_correct": False},
                    {"text": "Un type de variable", "is_correct": False},
                    {"text": "Un fichier de configuration", "is_correct": False}
                ]},
                {"text": "Comment fonctionne la réflexion (mirrors) en Dart?", "answers": [
                    {"text": "Permet d'inspecter les types à l'exécution (mais limitée)", "is_correct": True},
                    {"text": "Refléter des images", "is_correct": False},
                    {"text": "Un pattern de design", "is_correct": False},
                    {"text": "Une bibliothèque graphique", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les callable classes en Dart?", "answers": [
                    {"text": "Classes avec méthode call() pouvant être appelées comme des fonctions", "is_correct": True},
                    {"text": "Classes sans constructeur", "is_correct": False},
                    {"text": "Classes abstraites", "is_correct": False},
                    {"text": "Classes avec callback", "is_correct": False}
                ]},
                {"text": "Comment gérer la mémoire avec les weak references?", "answers": [
                    {"text": "Expando pour attacher des données sans empêcher le GC", "is_correct": True},
                    {"text": "weak keyword", "is_correct": False},
                    {"text": "SoftReference<T>", "is_correct": False},
                    {"text": "Dart gère automatiquement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le sound null safety?", "answers": [
                    {"text": "Garantie que les types non-nullables ne seront jamais null à l'exécution", "is_correct": True},
                    {"text": "Un système audio", "is_correct": False},
                    {"text": "Une vérification de syntaxe", "is_correct": False},
                    {"text": "Un plugin de sécurité", "is_correct": False}
                ]},
                {"text": "Comment optimiser les performances avec const constructors?", "answers": [
                    {"text": "Crée des instances canoniques réutilisables à la compilation", "is_correct": True},
                    {"text": "Accélère l'exécution du code", "is_correct": False},
                    {"text": "Réduit la taille du binaire", "is_correct": False},
                    {"text": "Améliore le hot reload", "is_correct": False}
                ]},
            ],
        },
    },
}

JAVA_DATA = {
    "category": {
        "name": "Java",
        "description": "Quiz pour maîtriser Java et la programmation orientée objet",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Java - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Comment afficher du texte en Java?", "answers": [
                    {"text": "System.out.println('Hello')", "is_correct": True},
                    {"text": "print('Hello')", "is_correct": False},
                    {"text": "console.log('Hello')", "is_correct": False},
                    {"text": "echo 'Hello'", "is_correct": False}
                ]},
                {"text": "Quel mot-clé déclare une classe en Java?", "answers": [
                    {"text": "class", "is_correct": True},
                    {"text": "struct", "is_correct": False},
                    {"text": "object", "is_correct": False},
                    {"text": "type", "is_correct": False}
                ]},
                {"text": "Quel est le type Java pour un entier 32 bits?", "answers": [
                    {"text": "int", "is_correct": True},
                    {"text": "integer", "is_correct": False},
                    {"text": "Int32", "is_correct": False},
                    {"text": "num", "is_correct": False}
                ]},
                {"text": "Comment créer une instance de classe en Java?", "answers": [
                    {"text": "new MaClasse()", "is_correct": True},
                    {"text": "create MaClasse()", "is_correct": False},
                    {"text": "MaClasse.create()", "is_correct": False},
                    {"text": "MaClasse()", "is_correct": False}
                ]},
                {"text": "Quel mot-clé définit une constante en Java?", "answers": [
                    {"text": "final", "is_correct": True},
                    {"text": "const", "is_correct": False},
                    {"text": "static", "is_correct": False},
                    {"text": "readonly", "is_correct": False}
                ]},
                {"text": "Quelle est la méthode principale d'un programme Java?", "answers": [
                    {"text": "public static void main(String[] args)", "is_correct": True},
                    {"text": "public void start()", "is_correct": False},
                    {"text": "static void run()", "is_correct": False},
                    {"text": "public main()", "is_correct": False}
                ]},
                {"text": "Comment créer un tableau de 5 entiers en Java?", "answers": [
                    {"text": "int[] arr = new int[5]", "is_correct": True},
                    {"text": "int arr[5]", "is_correct": False},
                    {"text": "Array<int> arr = new Array(5)", "is_correct": False},
                    {"text": "int[] arr = int[5]", "is_correct": False}
                ]},
                {"text": "Quel est le type de données pour un caractère unique en Java?", "answers": [
                    {"text": "char", "is_correct": True},
                    {"text": "character", "is_correct": False},
                    {"text": "string", "is_correct": False},
                    {"text": "letter", "is_correct": False}
                ]},
                {"text": "Comment écrire un commentaire sur une ligne en Java?", "answers": [
                    {"text": "// commentaire", "is_correct": True},
                    {"text": "# commentaire", "is_correct": False},
                    {"text": "/* commentaire", "is_correct": False},
                    {"text": "-- commentaire", "is_correct": False}
                ]},
                {"text": "Quel opérateur Java vérifie l'inégalité?", "answers": [
                    {"text": "!=", "is_correct": True},
                    {"text": "<>", "is_correct": False},
                    {"text": "=/=", "is_correct": False},
                    {"text": "not=", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Java - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Quelle est la différence entre == et .equals() pour les String?", "answers": [
                    {"text": "== compare les références, .equals() compare le contenu des chaînes", "is_correct": True},
                    {"text": "Aucune différence pour les String", "is_correct": False},
                    {"text": ".equals() compare les références, == le contenu", "is_correct": False},
                    {"text": "== est plus performant pour les String", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le polymorphisme en Java?", "answers": [
                    {"text": "La capacité d'un objet à prendre plusieurs formes selon son type réel", "is_correct": True},
                    {"text": "La capacité de créer plusieurs constructeurs", "is_correct": False},
                    {"text": "La capacité d'hériter de plusieurs classes", "is_correct": False},
                    {"text": "La capacité de définir plusieurs méthodes main()", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'une interface en Java?", "answers": [
                    {"text": "Un contrat définissant des méthodes que les classes implémentant doivent fournir", "is_correct": True},
                    {"text": "Une classe qui ne peut pas être instanciée directement", "is_correct": False},
                    {"text": "Une classe avec uniquement des méthodes statiques", "is_correct": False},
                    {"text": "Un module Java pour l'interface graphique", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le garbage collection en Java?", "answers": [
                    {"text": "La gestion automatique de la mémoire qui libère les objets non référencés", "is_correct": True},
                    {"text": "Un outil pour supprimer les fichiers temporaires", "is_correct": False},
                    {"text": "Un mécanisme de nettoyage du code source", "is_correct": False},
                    {"text": "La suppression automatique des variables locales", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre ArrayList et LinkedList?", "answers": [
                    {"text": "ArrayList est basé sur un tableau (accès rapide), LinkedList sur des nœuds chaînés (insertion rapide)", "is_correct": True},
                    {"text": "ArrayList est thread-safe, LinkedList non", "is_correct": False},
                    {"text": "LinkedList supporte les types primitifs, ArrayList non", "is_correct": False},
                    {"text": "Aucune différence de performance", "is_correct": False}
                ]},
                {"text": "Comment gérer les exceptions en Java?", "answers": [
                    {"text": "try { } catch (Exception e) { } finally { }", "is_correct": True},
                    {"text": "try { } except Exception { }", "is_correct": False},
                    {"text": "handle { } catch (e) { }", "is_correct": False},
                    {"text": "begin { } rescue Exception { }", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'une classe abstraite en Java?", "answers": [
                    {"text": "Une classe qui ne peut pas être instanciée et peut contenir des méthodes abstraites et concrètes", "is_correct": True},
                    {"text": "Une interface avec des méthodes implémentées", "is_correct": False},
                    {"text": "Une classe sans attributs", "is_correct": False},
                    {"text": "Une classe dont toutes les méthodes sont privées", "is_correct": False}
                ]},
                {"text": "Que fait le mot-clé 'synchronized' en Java?", "answers": [
                    {"text": "Permet à un seul thread d'accéder à une méthode/bloc à la fois (thread safety)", "is_correct": True},
                    {"text": "Synchronise une variable avec la base de données", "is_correct": False},
                    {"text": "Exécute une méthode de façon asynchrone", "is_correct": False},
                    {"text": "Synchronise deux objets Java", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que l'autoboxing en Java?", "answers": [
                    {"text": "La conversion automatique entre types primitifs et leurs wrappers (int <-> Integer)", "is_correct": True},
                    {"text": "La création automatique de boîtes de dialogue", "is_correct": False},
                    {"text": "Le boxing automatique des tableaux en List", "is_correct": False},
                    {"text": "La sérialisation automatique des objets", "is_correct": False}
                ]},
                {"text": "Que retourne Optional.empty().isPresent()?", "answers": [
                    {"text": "false", "is_correct": True},
                    {"text": "true", "is_correct": False},
                    {"text": "null", "is_correct": False},
                    {"text": "Une exception", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Java - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que les Java Streams?", "answers": [
                    {"text": "Une API pour traiter des séquences d'éléments de façon fonctionnelle (filter, map, reduce...)", "is_correct": True},
                    {"text": "Un système d'entrée/sortie pour les fichiers", "is_correct": False},
                    {"text": "Un mécanisme de communication réseau", "is_correct": False},
                    {"text": "Des threads Java optimisés pour le traitement de données", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'une lambda expression en Java?", "answers": [
                    {"text": "Une fonction anonyme implémentant une interface fonctionnelle, syntaxe : (params) -> expression", "is_correct": True},
                    {"text": "Une variable qui peut changer de type", "is_correct": False},
                    {"text": "Un calcul mathématique optimisé par la JVM", "is_correct": False},
                    {"text": "Une méthode qui retourne une fonction", "is_correct": False}
                ]},
                {"text": "Que sont les Records en Java (depuis Java 14)?", "answers": [
                    {"text": "Des classes immuables concises avec constructeur, getters, equals, hashCode et toString auto-générés", "is_correct": True},
                    {"text": "Un type de base de données embarquée", "is_correct": False},
                    {"text": "Des enregistrements de logs structurés", "is_correct": False},
                    {"text": "Des classes de configuration immuables Spring", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que la JVM?", "answers": [
                    {"text": "La machine virtuelle Java qui exécute le bytecode et abstrait le système d'exploitation", "is_correct": True},
                    {"text": "Le compilateur Java", "is_correct": False},
                    {"text": "Un gestionnaire de mémoire Java", "is_correct": False},
                    {"text": "L'IDE officiel Java", "is_correct": False}
                ]},
                {"text": "Que sont les Sealed Classes en Java (depuis Java 17)?", "answers": [
                    {"text": "Des classes qui restreignent quelles classes peuvent les étendre (permits clause)", "is_correct": True},
                    {"text": "Des classes dont les attributs sont tous final", "is_correct": False},
                    {"text": "Des classes inaccessibles depuis d'autres packages", "is_correct": False},
                    {"text": "Des classes sans constructeur public", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le pattern Singleton en Java?", "answers": [
                    {"text": "Un pattern qui garantit qu'une classe n'a qu'une seule instance dans toute l'application", "is_correct": True},
                    {"text": "Une classe avec un seul attribut", "is_correct": False},
                    {"text": "Une méthode qui retourne toujours la même valeur", "is_correct": False},
                    {"text": "Un thread qui gère une seule tâche", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre Callable et Runnable?", "answers": [
                    {"text": "Callable peut retourner un résultat et lancer des exceptions vérifiées, Runnable non", "is_correct": True},
                    {"text": "Runnable est plus récent que Callable", "is_correct": False},
                    {"text": "Callable est synchrone, Runnable asynchrone", "is_correct": False},
                    {"text": "Aucune différence fonctionnelle", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que CompletableFuture en Java?", "answers": [
                    {"text": "Une classe pour la programmation asynchrone et la composition de tâches avec callbacks", "is_correct": True},
                    {"text": "Un Future qui se complète automatiquement après un timeout", "is_correct": False},
                    {"text": "Un thread pool géré automatiquement par la JVM", "is_correct": False},
                    {"text": "Une alternative aux threads classiques basée sur les coroutines", "is_correct": False}
                ]},
                {"text": "Que sont les Virtual Threads (Project Loom, Java 21)?", "answers": [
                    {"text": "Des threads légers gérés par la JVM permettant de créer des millions de threads concurrents", "is_correct": True},
                    {"text": "Des threads qui s'exécutent dans la JVM sans OS", "is_correct": False},
                    {"text": "Des threads simulés pour les tests unitaires", "is_correct": False},
                    {"text": "Des coroutines Kotlin compatibles Java", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Pattern Matching for switch (Java 21)?", "answers": [
                    {"text": "Permet au switch d'utiliser des patterns de type et des gardes pour un code plus expressif", "is_correct": True},
                    {"text": "Un système de regex intégré dans les expressions switch", "is_correct": False},
                    {"text": "La possibilité d'utiliser des Strings dans les switch (existe depuis Java 7)", "is_correct": False},
                    {"text": "Un switch optimisé par le compilateur via le pattern matching", "is_correct": False}
                ]},
            ],
        },
    },
}

GO_DATA = {
    "category": {
        "name": "Go",
        "description": "Quiz pour maîtriser le langage Go (Golang) et ses concepts",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/go/go-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Go - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Comment déclarer et initialiser une variable en Go?", "answers": [
                    {"text": "x := 10", "is_correct": True},
                    {"text": "var x = 10", "is_correct": False},
                    {"text": "let x = 10", "is_correct": False},
                    {"text": "int x = 10", "is_correct": False}
                ]},
                {"text": "Quel est le package d'entrée obligatoire de tout programme Go?", "answers": [
                    {"text": "package main", "is_correct": True},
                    {"text": "package app", "is_correct": False},
                    {"text": "import main", "is_correct": False},
                    {"text": "module main", "is_correct": False}
                ]},
                {"text": "Comment afficher du texte en Go?", "answers": [
                    {"text": "fmt.Println('Hello')", "is_correct": True},
                    {"text": "print('Hello')", "is_correct": False},
                    {"text": "console.log('Hello')", "is_correct": False},
                    {"text": "System.out.println('Hello')", "is_correct": False}
                ]},
                {"text": "Quel est le type de données Go pour une chaîne?", "answers": [
                    {"text": "string", "is_correct": True},
                    {"text": "str", "is_correct": False},
                    {"text": "String", "is_correct": False},
                    {"text": "char*", "is_correct": False}
                ]},
                {"text": "Comment créer une fonction en Go?", "answers": [
                    {"text": "func maFonction() {}", "is_correct": True},
                    {"text": "def maFonction() {}", "is_correct": False},
                    {"text": "function maFonction() {}", "is_correct": False},
                    {"text": "fn maFonction() {}", "is_correct": False}
                ]},
                {"text": "Comment importer le package fmt en Go?", "answers": [
                    {"text": "import \"fmt\"", "is_correct": True},
                    {"text": "use fmt", "is_correct": False},
                    {"text": "require fmt", "is_correct": False},
                    {"text": "include fmt", "is_correct": False}
                ]},
                {"text": "Quel mot-clé crée une boucle en Go?", "answers": [
                    {"text": "for", "is_correct": True},
                    {"text": "while", "is_correct": False},
                    {"text": "loop", "is_correct": False},
                    {"text": "each", "is_correct": False}
                ]},
                {"text": "Comment créer une slice de strings en Go?", "answers": [
                    {"text": "[]string{}", "is_correct": True},
                    {"text": "string[]", "is_correct": False},
                    {"text": "slice<string>", "is_correct": False},
                    {"text": "new Slice(string)", "is_correct": False}
                ]},
                {"text": "Comment retourner plusieurs valeurs en Go?", "answers": [
                    {"text": "func fn() (int, error) { return 1, nil }", "is_correct": True},
                    {"text": "func fn() [int, error] { return [1, nil] }", "is_correct": False},
                    {"text": "func fn() { return 1, nil }", "is_correct": False},
                    {"text": "Go ne supporte pas les retours multiples", "is_correct": False}
                ]},
                {"text": "Que signifie ':=' en Go?", "answers": [
                    {"text": "Déclaration et affectation courte d'une nouvelle variable", "is_correct": True},
                    {"text": "Comparaison stricte", "is_correct": False},
                    {"text": "Affectation d'une variable existante", "is_correct": False},
                    {"text": "Déclaration d'une constante", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Go - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce qu'une goroutine?", "answers": [
                    {"text": "Un thread léger géré par le runtime Go pour la concurrence", "is_correct": True},
                    {"text": "Une fonction récursive optimisée", "is_correct": False},
                    {"text": "Une coroutine Python portée en Go", "is_correct": False},
                    {"text": "Un module Go indépendant", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un channel en Go?", "answers": [
                    {"text": "Un mécanisme de communication typé entre goroutines", "is_correct": True},
                    {"text": "Un canal de communication HTTP", "is_correct": False},
                    {"text": "Un buffer mémoire partagé", "is_correct": False},
                    {"text": "Un handler d'événements", "is_correct": False}
                ]},
                {"text": "Comment Go gère-t-il les erreurs?", "answers": [
                    {"text": "En retournant des valeurs error en dernier paramètre et en les vérifiant explicitement", "is_correct": True},
                    {"text": "Avec des exceptions try/catch", "is_correct": False},
                    {"text": "Via un système de Result<T, E>", "is_correct": False},
                    {"text": "Avec des callbacks onError", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'une interface en Go?", "answers": [
                    {"text": "Un ensemble de signatures de méthodes; une struct l'implémente implicitement si elle a toutes ces méthodes", "is_correct": True},
                    {"text": "Un contrat qu'une struct doit déclarer explicitement implémenter", "is_correct": False},
                    {"text": "Un type abstrait avec des méthodes concrètes", "is_correct": False},
                    {"text": "Un module Go exporté", "is_correct": False}
                ]},
                {"text": "Que fait defer en Go?", "answers": [
                    {"text": "Reporte l'exécution d'une fonction à la fin de la fonction courante (LIFO)", "is_correct": True},
                    {"text": "Retarde l'exécution d'une goroutine", "is_correct": False},
                    {"text": "Différence l'évaluation d'une expression", "is_correct": False},
                    {"text": "Exécute une fonction après un délai en ms", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre make() et new() en Go?", "answers": [
                    {"text": "make() initialise les types slice/map/chan, new() alloue de la mémoire et retourne un pointeur", "is_correct": True},
                    {"text": "new() est plus récent et remplace make()", "is_correct": False},
                    {"text": "make() retourne un pointeur, new() retourne une valeur", "is_correct": False},
                    {"text": "Aucune différence pour les slices", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un struct en Go?", "answers": [
                    {"text": "Un type composite qui regroupe des champs nommés de types différents", "is_correct": True},
                    {"text": "Une classe Go sans méthodes", "is_correct": False},
                    {"text": "Un type immuable en Go", "is_correct": False},
                    {"text": "Un module encapsulant plusieurs packages", "is_correct": False}
                ]},
                {"text": "Comment créer un map en Go?", "answers": [
                    {"text": "m := make(map[string]int)", "is_correct": True},
                    {"text": "m := map<string, int>{}", "is_correct": False},
                    {"text": "m := new Map(string, int)", "is_correct": False},
                    {"text": "var m map = string:int", "is_correct": False}
                ]},
                {"text": "Que fait panic() en Go?", "answers": [
                    {"text": "Arrête l'exécution normale et remonte la pile (récupérable avec recover())", "is_correct": True},
                    {"text": "Affiche un message d'erreur et continue", "is_correct": False},
                    {"text": "Lance une goroutine de gestion d'erreur", "is_correct": False},
                    {"text": "Équivalent à un throw d'exception", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que go.mod?", "answers": [
                    {"text": "Le fichier qui définit le module Go et ses dépendances", "is_correct": True},
                    {"text": "La configuration du compilateur Go", "is_correct": False},
                    {"text": "Un fichier de constantes globales", "is_correct": False},
                    {"text": "Le fichier principal du programme Go", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Go - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que le select statement en Go?", "answers": [
                    {"text": "Attend sur plusieurs opérations de channels et exécute la première prête", "is_correct": True},
                    {"text": "Un switch optimisé pour les types Go", "is_correct": False},
                    {"text": "Un outil de sélection de goroutines", "is_correct": False},
                    {"text": "Une requête SQL intégrée dans Go", "is_correct": False}
                ]},
                {"text": "Comment implémenter un worker pool en Go?", "answers": [
                    {"text": "Avec un channel de jobs, plusieurs goroutines workers et un channel de résultats", "is_correct": True},
                    {"text": "Avec la bibliothèque threadpool de la stdlib", "is_correct": False},
                    {"text": "Avec sync.Pool uniquement", "is_correct": False},
                    {"text": "Avec le package workers de Go", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que sync.WaitGroup?", "answers": [
                    {"text": "Un compteur pour attendre qu'un groupe de goroutines termine leur exécution", "is_correct": True},
                    {"text": "Un mutex pour synchroniser l'accès à une variable", "is_correct": False},
                    {"text": "Un groupe de goroutines avec communication par channel", "is_correct": False},
                    {"text": "Un outil de synchronisation entre processus OS", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que context.Context en Go?", "answers": [
                    {"text": "Un objet qui transporte des deadlines, annulations et valeurs entre goroutines et API", "is_correct": True},
                    {"text": "Le contexte d'exécution du programme Go", "is_correct": False},
                    {"text": "Un gestionnaire de configuration d'application", "is_correct": False},
                    {"text": "Un type pour les variables de contexte HTTP", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que l'embedding en Go?", "answers": [
                    {"text": "Inclure un type dans un autre pour hériter de ses méthodes sans héritage classique", "is_correct": True},
                    {"text": "Intégrer du code C dans Go avec cgo", "is_correct": False},
                    {"text": "Incorporer des assets dans le binaire Go", "is_correct": False},
                    {"text": "Un mécanisme de composition de channels", "is_correct": False}
                ]},
                {"text": "Que fait //go:generate?", "answers": [
                    {"text": "Une directive pour exécuter des outils de génération de code via 'go generate'", "is_correct": True},
                    {"text": "Un commentaire pour la documentation godoc", "is_correct": False},
                    {"text": "Une instruction pour compiler conditionnellement", "is_correct": False},
                    {"text": "Une macro Go exécutée à la compilation", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les build tags en Go?", "answers": [
                    {"text": "Des directives (//go:build) qui contrôlent quels fichiers sont inclus à la compilation selon des conditions", "is_correct": True},
                    {"text": "Des tags de versioning du module", "is_correct": False},
                    {"text": "Des métadonnées pour go doc", "is_correct": False},
                    {"text": "Des labels pour identifier les goroutines", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que sync.Mutex vs sync.RWMutex?", "answers": [
                    {"text": "RWMutex permet plusieurs lecteurs simultanés mais un seul écrivain; Mutex bloque tout accès concurrent", "is_correct": True},
                    {"text": "RWMutex est une version améliorée de Mutex toujours préférable", "is_correct": False},
                    {"text": "Mutex est pour les goroutines, RWMutex pour les threads OS", "is_correct": False},
                    {"text": "Aucune différence de performance", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que unsafe.Pointer en Go?", "answers": [
                    {"text": "Un type qui permet de contourner le système de types Go pour manipuler la mémoire directement", "is_correct": True},
                    {"text": "Un pointeur nullable comme en C", "is_correct": False},
                    {"text": "Un type pour les opérations bit à bit", "is_correct": False},
                    {"text": "Un pointeur vers un type interface{}", "is_correct": False}
                ]},
                {"text": "Comment profiler un programme Go?", "answers": [
                    {"text": "Avec le package pprof via net/http/pprof ou runtime/pprof pour CPU, mémoire et goroutines", "is_correct": True},
                    {"text": "Avec l'outil go profile uniquement", "is_correct": False},
                    {"text": "En activant -debug=true à la compilation", "is_correct": False},
                    {"text": "Go n'a pas d'outils de profiling intégrés", "is_correct": False}
                ]},
            ],
        },
    },
}

RUST_DATA = {
    "category": {
        "name": "Rust",
        "description": "Quiz pour maîtriser Rust et la programmation système sûre",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/rust/rust-plain.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Rust - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Comment déclarer une variable immuable en Rust?", "answers": [
                    {"text": "let x = 5;", "is_correct": True},
                    {"text": "const x = 5;", "is_correct": False},
                    {"text": "var x = 5;", "is_correct": False},
                    {"text": "mut x = 5;", "is_correct": False}
                ]},
                {"text": "Comment rendre une variable mutable en Rust?", "answers": [
                    {"text": "let mut x = 5;", "is_correct": True},
                    {"text": "mutable x = 5;", "is_correct": False},
                    {"text": "var x = 5;", "is_correct": False},
                    {"text": "let x = mut 5;", "is_correct": False}
                ]},
                {"text": "Quelle est la fonction d'entrée d'un programme Rust?", "answers": [
                    {"text": "fn main() {}", "is_correct": True},
                    {"text": "def main() {}", "is_correct": False},
                    {"text": "func main() {}", "is_correct": False},
                    {"text": "void main() {}", "is_correct": False}
                ]},
                {"text": "Comment afficher du texte en Rust?", "answers": [
                    {"text": "println!(\"Hello\");", "is_correct": True},
                    {"text": "print(\"Hello\");", "is_correct": False},
                    {"text": "console.log(\"Hello\");", "is_correct": False},
                    {"text": "echo \"Hello\";", "is_correct": False}
                ]},
                {"text": "Quel concept Rust garantit la sécurité mémoire sans garbage collector?", "answers": [
                    {"text": "L'ownership (propriété)", "is_correct": True},
                    {"text": "Le garbage collection incrémental", "is_correct": False},
                    {"text": "Le comptage de références automatique", "is_correct": False},
                    {"text": "Les pointeurs intelligents obligatoires", "is_correct": False}
                ]},
                {"text": "Comment créer un vecteur en Rust?", "answers": [
                    {"text": "let v: Vec<i32> = Vec::new();", "is_correct": True},
                    {"text": "let v = new Vector<i32>();", "is_correct": False},
                    {"text": "let v: [i32] = [];", "is_correct": False},
                    {"text": "let v = List::new();", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le borrowing en Rust?", "answers": [
                    {"text": "Emprunter une référence à une valeur sans en prendre la propriété", "is_correct": True},
                    {"text": "Copier une valeur vers une autre variable", "is_correct": False},
                    {"text": "Transférer la propriété d'une valeur", "is_correct": False},
                    {"text": "Allouer de la mémoire heap", "is_correct": False}
                ]},
                {"text": "Quel outil gère les dépendances en Rust?", "answers": [
                    {"text": "Cargo", "is_correct": True},
                    {"text": "npm", "is_correct": False},
                    {"text": "pip", "is_correct": False},
                    {"text": "rustpkg", "is_correct": False}
                ]},
                {"text": "Comment définir une structure en Rust?", "answers": [
                    {"text": "struct Point { x: f64, y: f64 }", "is_correct": True},
                    {"text": "class Point { x: f64, y: f64 }", "is_correct": False},
                    {"text": "type Point = { x: f64, y: f64 }", "is_correct": False},
                    {"text": "record Point(x: f64, y: f64)", "is_correct": False}
                ]},
                {"text": "Comment gérer les erreurs avec le type Result en Rust?", "answers": [
                    {"text": "Avec match pour traiter Ok(val) et Err(e)", "is_correct": True},
                    {"text": "Avec try/catch", "is_correct": False},
                    {"text": "Avec if result.isOk()", "is_correct": False},
                    {"text": "Rust ne gère pas les erreurs explicitement", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Rust - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce qu'un lifetime en Rust?", "answers": [
                    {"text": "Une annotation qui garantit qu'une référence est valide pour une durée définie", "is_correct": True},
                    {"text": "La durée de vie d'un thread Rust", "is_correct": False},
                    {"text": "Le scope d'une variable locale", "is_correct": False},
                    {"text": "Un compteur de références automatique", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un trait en Rust?", "answers": [
                    {"text": "Un ensemble de méthodes qu'un type peut implémenter, similaire aux interfaces", "is_correct": True},
                    {"text": "Une caractéristique d'un type primitif", "is_correct": False},
                    {"text": "Un attribut de struct", "is_correct": False},
                    {"text": "Un module Rust exporté", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre String et &str en Rust?", "answers": [
                    {"text": "String est une chaîne possédée sur le heap, &str est une référence vers des données UTF-8", "is_correct": True},
                    {"text": "String est immuable, &str est mutable", "is_correct": False},
                    {"text": "&str est plus lente mais plus sûre", "is_correct": False},
                    {"text": "Aucune différence pratique", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le pattern matching avec match en Rust?", "answers": [
                    {"text": "Un construct puissant qui compare une valeur contre des patterns exhaustifs", "is_correct": True},
                    {"text": "Un switch simplifié", "is_correct": False},
                    {"text": "Un système de regex intégré", "is_correct": False},
                    {"text": "Une correspondance structurelle entre deux structs", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Option<T> en Rust?", "answers": [
                    {"text": "Un type qui représente soit Some(valeur) soit None - alternative sûre au null", "is_correct": True},
                    {"text": "Une option de configuration du compilateur", "is_correct": False},
                    {"text": "Un paramètre optionnel de fonction", "is_correct": False},
                    {"text": "Un type pour les valeurs optionnellement mutables", "is_correct": False}
                ]},
                {"text": "Que fait l'opérateur ? en Rust?", "answers": [
                    {"text": "Propage automatiquement une erreur (retourne Err si Result est Err)", "is_correct": True},
                    {"text": "Vérifie si une Option est Some", "is_correct": False},
                    {"text": "Indique un paramètre optionnel", "is_correct": False},
                    {"text": "Déréférence un pointeur intelligent", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Box<T> en Rust?", "answers": [
                    {"text": "Un pointeur intelligent qui alloue T sur le heap", "is_correct": True},
                    {"text": "Un conteneur générique similaire à Vec", "is_correct": False},
                    {"text": "Un wrapper pour les types primitifs", "is_correct": False},
                    {"text": "Un type pour les fermetures (closures)", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le mouvement (move) de valeur en Rust?", "answers": [
                    {"text": "Transférer la propriété d'une valeur, rendant l'original inutilisable", "is_correct": True},
                    {"text": "Copier une valeur vers un autre emplacement mémoire", "is_correct": False},
                    {"text": "Déplacer une variable dans un autre scope", "is_correct": False},
                    {"text": "Passer une valeur par référence", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'une closure en Rust?", "answers": [
                    {"text": "Une fonction anonyme qui peut capturer des variables de son environnement", "is_correct": True},
                    {"text": "Un module fermé (privé)", "is_correct": False},
                    {"text": "Une structure avec des champs privés", "is_correct": False},
                    {"text": "Un bloc de code exécuté à la fin du scope", "is_correct": False}
                ]},
                {"text": "Quelle est la règle de borrowing de Rust?", "answers": [
                    {"text": "Soit une référence mutable, soit plusieurs références immuables - jamais les deux simultanément", "is_correct": True},
                    {"text": "Une seule référence à la fois, mutable ou non", "is_correct": False},
                    {"text": "Illimité de références mutables dans le même scope", "is_correct": False},
                    {"text": "Les références ne peuvent pas traverser les fonctions", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Rust - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que async/await en Rust?", "answers": [
                    {"text": "Un système de programmation asynchrone basé sur des Futures, nécessitant un runtime comme Tokio", "is_correct": True},
                    {"text": "Un système de concurrence basé sur des threads OS", "is_correct": False},
                    {"text": "Une syntaxe pour les goroutines Rust", "is_correct": False},
                    {"text": "Des macros pour simplifier les callbacks", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Rc<T> vs Arc<T> en Rust?", "answers": [
                    {"text": "Rc est pour le thread unique (Reference Counting), Arc est thread-safe (Atomic Reference Counting)", "is_correct": True},
                    {"text": "Arc est plus lent mais plus sûr que Rc", "is_correct": False},
                    {"text": "Rc est pour le heap, Arc pour la stack", "is_correct": False},
                    {"text": "Ils sont identiques en termes de performance", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'une macro procédurale en Rust?", "answers": [
                    {"text": "Une macro qui opère sur le TokenStream Rust et génère du code à la compilation", "is_correct": True},
                    {"text": "Une macro qui s'exécute au runtime", "is_correct": False},
                    {"text": "Une macro définie avec macro_rules!", "is_correct": False},
                    {"text": "Un attribut de fonction sans paramètres", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le trait Send en Rust?", "answers": [
                    {"text": "Marque qu'un type peut être transféré entre threads en toute sécurité", "is_correct": True},
                    {"text": "Permet d'envoyer des données via un channel", "is_correct": False},
                    {"text": "Un trait pour la sérialisation réseau", "is_correct": False},
                    {"text": "Un trait pour les types copiables", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que la monomorphisation en Rust?", "answers": [
                    {"text": "Le compilateur génère des versions concrètes du code générique pour chaque type utilisé (zero-cost abstractions)", "is_correct": True},
                    {"text": "La conversion d'un type en un seul type monomique", "is_correct": False},
                    {"text": "L'optimisation des branches conditionnelles", "is_correct": False},
                    {"text": "La fusion de plusieurs traits en un seul", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que pin! / Pin<P> en Rust?", "answers": [
                    {"text": "Garantit qu'une valeur ne sera pas déplacée en mémoire, nécessaire pour les self-referential structs et les Futures", "is_correct": True},
                    {"text": "Épingle une variable à un registre CPU", "is_correct": False},
                    {"text": "Immobilise une référence dans le heap", "is_correct": False},
                    {"text": "Un type pour les pointeurs constants", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'unsafe Rust?", "answers": [
                    {"text": "Un bloc permettant des opérations que le compilateur ne peut pas vérifier (déréférencement de pointeurs bruts, FFI...)", "is_correct": True},
                    {"text": "Du code qui n'a pas été testé", "is_correct": False},
                    {"text": "Des opérations sans gestion d'erreur", "is_correct": False},
                    {"text": "Un mode de compilation sans optimisations de sécurité", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le trait Iterator en Rust?", "answers": [
                    {"text": "Un trait avec la méthode next() permettant d'utiliser les adaptateurs fonctionnels (map, filter, fold...)", "is_correct": True},
                    {"text": "Un pointeur qui parcourt des collections", "is_correct": False},
                    {"text": "Un type pour les boucles for", "is_correct": False},
                    {"text": "Un générateur de valeurs aléatoires", "is_correct": False}
                ]},
                {"text": "Comment implémenter un trait pour un type externe en Rust?", "answers": [
                    {"text": "Impossible directement (orphan rule) - il faut que le trait OU le type soit local au crate", "is_correct": True},
                    {"text": "Avec le mot-clé extern impl", "is_correct": False},
                    {"text": "En utilisant le pattern newtype wrapper", "is_correct": True},
                    {"text": "En ajoutant #[foreign_impl] au-dessus de l'impl", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que RAII en Rust?", "answers": [
                    {"text": "Resource Acquisition Is Initialization - les ressources sont libérées automatiquement via Drop quand elles sortent du scope", "is_correct": True},
                    {"text": "Un pattern de gestion des erreurs", "is_correct": False},
                    {"text": "Un système d'allocation de mémoire", "is_correct": False},
                    {"text": "Une convention de nommage Rust", "is_correct": False}
                ]},
            ],
        },
    },
}

CSHARP_DATA = {
    "category": {
        "name": "C#",
        "description": "Quiz pour maîtriser C# et l'écosystème .NET",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/csharp/csharp-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "C# - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Comment afficher du texte en C#?", "answers": [
                    {"text": "Console.WriteLine(\"Hello\");", "is_correct": True},
                    {"text": "print(\"Hello\");", "is_correct": False},
                    {"text": "System.out.println(\"Hello\");", "is_correct": False},
                    {"text": "echo \"Hello\";", "is_correct": False}
                ]},
                {"text": "Quel mot-clé déclare une variable en C#?", "answers": [
                    {"text": "var ou le type explicite (int, string...)", "is_correct": True},
                    {"text": "let", "is_correct": False},
                    {"text": "dim", "is_correct": False},
                    {"text": "define", "is_correct": False}
                ]},
                {"text": "Comment définir une méthode qui ne retourne rien en C#?", "answers": [
                    {"text": "void MaMethode() {}", "is_correct": True},
                    {"text": "null MaMethode() {}", "is_correct": False},
                    {"text": "none MaMethode() {}", "is_correct": False},
                    {"text": "MaMethode() {}", "is_correct": False}
                ]},
                {"text": "Quel est le type C# pour une chaîne?", "answers": [
                    {"text": "string", "is_correct": True},
                    {"text": "str", "is_correct": False},
                    {"text": "String16", "is_correct": False},
                    {"text": "char*", "is_correct": False}
                ]},
                {"text": "Comment créer une liste en C#?", "answers": [
                    {"text": "var liste = new List<int>();", "is_correct": True},
                    {"text": "var liste = new ArrayList();", "is_correct": False},
                    {"text": "int[] liste = new int[];", "is_correct": False},
                    {"text": "var liste = List<int>.Create();", "is_correct": False}
                ]},
                {"text": "Quel mot-clé crée une classe en C#?", "answers": [
                    {"text": "class", "is_correct": True},
                    {"text": "struct", "is_correct": False},
                    {"text": "object", "is_correct": False},
                    {"text": "type", "is_correct": False}
                ]},
                {"text": "Comment déclarer une propriété auto-implémentée en C#?", "answers": [
                    {"text": "public string Nom { get; set; }", "is_correct": True},
                    {"text": "public string Nom;", "is_correct": False},
                    {"text": "property string Nom;", "is_correct": False},
                    {"text": "public Nom: string;", "is_correct": False}
                ]},
                {"text": "Quel opérateur C# gère le null coalescing?", "answers": [
                    {"text": "??", "is_correct": True},
                    {"text": "?:", "is_correct": False},
                    {"text": "||", "is_correct": False},
                    {"text": "?/", "is_correct": False}
                ]},
                {"text": "Comment créer un tableau de 3 entiers en C#?", "answers": [
                    {"text": "int[] arr = new int[3];", "is_correct": True},
                    {"text": "int arr[3];", "is_correct": False},
                    {"text": "var arr = Array<int>(3);", "is_correct": False},
                    {"text": "int[] arr = int[3];", "is_correct": False}
                ]},
                {"text": "Quel mot-clé permet l'héritage en C#?", "answers": [
                    {"text": ": (ex: class Enfant : Parent)", "is_correct": True},
                    {"text": "extends", "is_correct": False},
                    {"text": "inherits", "is_correct": False},
                    {"text": "implements", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "C# - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que LINQ en C#?", "answers": [
                    {"text": "Language Integrated Query - des requêtes sur des collections et sources de données intégrées au langage", "is_correct": True},
                    {"text": "Un ORM pour SQL Server", "is_correct": False},
                    {"text": "Un framework de logging", "is_correct": False},
                    {"text": "Un système de sérialisation JSON", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un delegate en C#?", "answers": [
                    {"text": "Un type qui représente une référence à une méthode avec une signature spécifique", "is_correct": True},
                    {"text": "Un pattern de délégation de responsabilités", "is_correct": False},
                    {"text": "Un attribut de classe", "is_correct": False},
                    {"text": "Une interface avec une seule méthode", "is_correct": False}
                ]},
                {"text": "Que fait async/await en C#?", "answers": [
                    {"text": "Permet d'écrire du code asynchrone non-bloquant de façon synchrone et lisible", "is_correct": True},
                    {"text": "Lance un nouveau thread pour chaque opération async", "is_correct": False},
                    {"text": "Exécute du code en parallèle sur plusieurs CPU", "is_correct": False},
                    {"text": "Gère les callbacks imbriqués", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'une expression lambda en C#?", "answers": [
                    {"text": "Une fonction anonyme : (params) => expression", "is_correct": True},
                    {"text": "Une expression régulière intégrée", "is_correct": False},
                    {"text": "Un calcul mathématique optimisé", "is_correct": False},
                    {"text": "Un attribut de méthode", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre interface et classe abstraite en C#?", "answers": [
                    {"text": "Une classe ne peut hériter que d'une classe abstraite, mais implémenter plusieurs interfaces", "is_correct": True},
                    {"text": "Les interfaces peuvent avoir du code, les classes abstraites non", "is_correct": False},
                    {"text": "Les classes abstraites ne peuvent pas avoir de constructeur", "is_correct": False},
                    {"text": "Aucune différence depuis C# 8", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que IDisposable et using?", "answers": [
                    {"text": "IDisposable définit Dispose() pour libérer des ressources; using garantit l'appel automatique", "is_correct": True},
                    {"text": "using importe des namespaces, IDisposable n'est pas lié", "is_correct": False},
                    {"text": "using crée un scope isolé pour les variables", "is_correct": False},
                    {"text": "IDisposable est une interface pour les objets sérialisables", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un event en C#?", "answers": [
                    {"text": "Un mécanisme de notification basé sur des delegates permettant à des abonnés de réagir", "is_correct": True},
                    {"text": "Un événement DOM comme en JavaScript", "is_correct": False},
                    {"text": "Un log d'activité de l'application", "is_correct": False},
                    {"text": "Une exception gérée par le framework", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que record en C# 9+?", "answers": [
                    {"text": "Un type immuable avec égalité basée sur les valeurs, synthèse automatique de ToString/Equals", "is_correct": True},
                    {"text": "Un type de base de données", "is_correct": False},
                    {"text": "Un log structuré", "is_correct": False},
                    {"text": "Une classe avec seulement des propriétés publiques", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le garbage collector C#?", "answers": [
                    {"text": "Il libère automatiquement la mémoire des objets non référencés via un algorithme générationnel", "is_correct": True},
                    {"text": "Il libère immédiatement la mémoire dès qu'un objet sort du scope", "is_correct": False},
                    {"text": "Il utilise le comptage de références comme Swift", "is_correct": False},
                    {"text": "Le développeur doit appeler GC.Collect() manuellement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un extension method en C#?", "answers": [
                    {"text": "Une méthode statique qui s'utilise comme méthode d'instance sur un type existant", "is_correct": True},
                    {"text": "Une méthode ajoutée par héritage", "is_correct": False},
                    {"text": "Un plugin chargé dynamiquement", "is_correct": False},
                    {"text": "Une méthode définie dans une interface", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "C# - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que Span<T> en C#?", "answers": [
                    {"text": "Une vue stack-only sur des données contiguës permettant de manipuler la mémoire sans allocation", "is_correct": True},
                    {"text": "Un tableau redimensionnable haute performance", "is_correct": False},
                    {"text": "Un type pour les chaînes longues", "is_correct": False},
                    {"text": "Un wrapper pour les tableaux natifs", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Source Generators en C#?", "answers": [
                    {"text": "Un mécanisme de métaprogrammation qui génère du code C# à la compilation via Roslyn", "is_correct": True},
                    {"text": "Un outil pour générer des stubs de tests", "is_correct": False},
                    {"text": "Un système de templates pour ASPNET", "is_correct": False},
                    {"text": "Un générateur de documentation automatique", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que IAsyncEnumerable<T> en C#?", "answers": [
                    {"text": "Un énumérable asynchrone permettant de yield return depuis des méthodes async", "is_correct": True},
                    {"text": "Une liste asynchrone thread-safe", "is_correct": False},
                    {"text": "Un stream de données HTTP", "is_correct": False},
                    {"text": "Un Observable comme en RxJS", "is_correct": False}
                ]},
                {"text": "Que sont les Primary Constructors en C# 12?", "answers": [
                    {"text": "Des paramètres déclarés directement dans la signature de classe/struct, accessibles partout dans le type", "is_correct": True},
                    {"text": "Le constructeur avec le plus de paramètres", "is_correct": False},
                    {"text": "Le constructeur appelé avant les autres", "is_correct": False},
                    {"text": "Un constructeur généré automatiquement par le compilateur", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le pattern matching avancé en C# (switch expressions)?", "answers": [
                    {"text": "Des expressions switch qui matchent des patterns complexes : type, propriétés, tuples, relational", "is_correct": True},
                    {"text": "Un switch qui supporte les regex", "is_correct": False},
                    {"text": "Un switch amélioré supportant les strings uniquement", "is_correct": False},
                    {"text": "Un outil de matching basé sur LINQ", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que ValueTask<T> vs Task<T>?", "answers": [
                    {"text": "ValueTask évite l'allocation heap quand le résultat est souvent synchrone; Task alloue toujours", "is_correct": True},
                    {"text": "ValueTask est plus rapide dans tous les cas", "is_correct": False},
                    {"text": "Task est pour le parallélisme, ValueTask pour l'async", "is_correct": False},
                    {"text": "Aucune différence depuis .NET 6", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que NativeAOT en .NET?", "answers": [
                    {"text": "Compilation Ahead-of-Time en code natif produisant un exécutable standalone sans la JVM .NET", "is_correct": True},
                    {"text": "Une bibliothèque pour appeler du code C natif", "is_correct": False},
                    {"text": "Un mode de compilation optimisé pour ARM", "is_correct": False},
                    {"text": "Un runtime .NET allégé pour les containers", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le unsafe code en C#?", "answers": [
                    {"text": "Un bloc permettant d'utiliser des pointeurs et manipuler la mémoire directement", "is_correct": True},
                    {"text": "Du code non testé en production", "is_correct": False},
                    {"text": "Du code sans gestion d'exceptions", "is_correct": False},
                    {"text": "Des méthodes sans modificateur d'accès", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Roslyn?", "answers": [
                    {"text": "Le compilateur C#/VB open-source de Microsoft exposant des APIs d'analyse de code", "is_correct": True},
                    {"text": "Le framework web ASP.NET Core", "is_correct": False},
                    {"text": "L'IDE Visual Studio", "is_correct": False},
                    {"text": "Un ORM Microsoft pour .NET", "is_correct": False}
                ]},
                {"text": "Comment fonctionne la covariance et contravariance en C#?", "answers": [
                    {"text": "Covariance (out): retour de type dérivé OK; Contravariance (in): paramètre de type base OK - pour génériques", "is_correct": True},
                    {"text": "La covariance permet la conversion implicite entre types numériques", "is_correct": False},
                    {"text": "La contravariance est uniquement pour les tableaux", "is_correct": False},
                    {"text": "Ces concepts ne s'appliquent pas en C#", "is_correct": False}
                ]},
            ],
        },
    },
}

KOTLIN_DATA = {
    "category": {
        "name": "Kotlin",
        "description": "Quiz pour maîtriser Kotlin et le développement Android/multiplateforme",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/kotlin/kotlin-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Kotlin - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Comment déclarer une variable immuable en Kotlin?", "answers": [
                    {"text": "val x = 5", "is_correct": True},
                    {"text": "var x = 5", "is_correct": False},
                    {"text": "let x = 5", "is_correct": False},
                    {"text": "const x = 5", "is_correct": False}
                ]},
                {"text": "Comment déclarer une variable mutable en Kotlin?", "answers": [
                    {"text": "var x = 5", "is_correct": True},
                    {"text": "val x = 5", "is_correct": False},
                    {"text": "mut x = 5", "is_correct": False},
                    {"text": "let x = 5", "is_correct": False}
                ]},
                {"text": "Comment afficher du texte en Kotlin?", "answers": [
                    {"text": "println(\"Hello\")", "is_correct": True},
                    {"text": "print(\"Hello\")", "is_correct": False},
                    {"text": "System.out.println(\"Hello\")", "is_correct": False},
                    {"text": "console.log(\"Hello\")", "is_correct": False}
                ]},
                {"text": "Comment définir une fonction en Kotlin?", "answers": [
                    {"text": "fun maFonction() {}", "is_correct": True},
                    {"text": "function maFonction() {}", "is_correct": False},
                    {"text": "def maFonction() {}", "is_correct": False},
                    {"text": "func maFonction() {}", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que la null safety en Kotlin?", "answers": [
                    {"text": "Kotlin distingue les types nullable (String?) des non-nullable (String) au niveau du compilateur", "is_correct": True},
                    {"text": "Kotlin supprime automatiquement les valeurs null", "is_correct": False},
                    {"text": "Kotlin n'a pas de valeur null", "is_correct": False},
                    {"text": "Un plugin de gestion des NullPointerException", "is_correct": False}
                ]},
                {"text": "Comment créer une liste immuable en Kotlin?", "answers": [
                    {"text": "listOf(1, 2, 3)", "is_correct": True},
                    {"text": "mutableListOf(1, 2, 3)", "is_correct": False},
                    {"text": "ArrayList(1, 2, 3)", "is_correct": False},
                    {"text": "List.of(1, 2, 3)", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'une data class en Kotlin?", "answers": [
                    {"text": "Une classe dont le but est de stocker des données avec equals, hashCode, toString auto-générés", "is_correct": True},
                    {"text": "Une classe qui accède à une base de données", "is_correct": False},
                    {"text": "Une classe immuable Kotlin", "is_correct": False},
                    {"text": "Une interface pour les modèles de données", "is_correct": False}
                ]},
                {"text": "Comment utiliser les string templates en Kotlin?", "answers": [
                    {"text": "\"Bonjour $nom, tu as ${age + 1} ans\"", "is_correct": True},
                    {"text": "'Bonjour ' + nom + ', tu as ' + age + ' ans'", "is_correct": False},
                    {"text": "f\"Bonjour {nom}\"", "is_correct": False},
                    {"text": "`Bonjour ${nom}`", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que l'opérateur ?: (Elvis) en Kotlin?", "answers": [
                    {"text": "Retourne la valeur de gauche si non-null, sinon la valeur de droite", "is_correct": True},
                    {"text": "Un opérateur ternaire standard", "is_correct": False},
                    {"text": "Un opérateur de comparaison", "is_correct": False},
                    {"text": "Un opérateur de déstructuration", "is_correct": False}
                ]},
                {"text": "Comment créer un objet singleton en Kotlin?", "answers": [
                    {"text": "Avec object : object MonSingleton {}", "is_correct": True},
                    {"text": "Avec singleton class MonSingleton {}", "is_correct": False},
                    {"text": "@Singleton class MonSingleton {}", "is_correct": False},
                    {"text": "class MonSingleton { companion object {} }", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Kotlin - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que les extensions functions en Kotlin?", "answers": [
                    {"text": "Des fonctions ajoutées à un type existant sans modifier sa classe", "is_correct": True},
                    {"text": "Des fonctions héritées d'une classe parente", "is_correct": False},
                    {"text": "Des plugins Kotlin pour l'IDE", "is_correct": False},
                    {"text": "Des fonctions avec des paramètres supplémentaires", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les coroutines Kotlin?", "answers": [
                    {"text": "Des composants de concurrence légers permettant la programmation asynchrone de façon séquentielle", "is_correct": True},
                    {"text": "Des threads Kotlin optimisés", "is_correct": False},
                    {"text": "Des callbacks améliorés", "is_correct": False},
                    {"text": "Un système d'événements asynchrones", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre launch et async dans les coroutines Kotlin?", "answers": [
                    {"text": "launch lance une coroutine sans valeur de retour, async retourne un Deferred avec une valeur", "is_correct": True},
                    {"text": "async est synchrone, launch est asynchrone", "is_correct": False},
                    {"text": "launch attend la fin de la coroutine, async non", "is_correct": False},
                    {"text": "Aucune différence de comportement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un sealed class en Kotlin?", "answers": [
                    {"text": "Une classe dont toutes les sous-classes sont connues à la compilation (hiérarchie fermée)", "is_correct": True},
                    {"text": "Une classe immuable", "is_correct": False},
                    {"text": "Une classe sans constructeur public", "is_correct": False},
                    {"text": "Une classe singleton", "is_correct": False}
                ]},
                {"text": "Que fait la fonction let en Kotlin?", "answers": [
                    {"text": "Exécute un bloc sur un objet et retourne le résultat du bloc (souvent pour les opérations nullable)", "is_correct": True},
                    {"text": "Déclare une variable locale immuable", "is_correct": False},
                    {"text": "Crée un lambda expression", "is_correct": False},
                    {"text": "Convertit un type vers un autre", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un companion object en Kotlin?", "answers": [
                    {"text": "Un singleton associé à une classe, équivalent aux membres statiques Java", "is_correct": True},
                    {"text": "Un objet qui accompagne le cycle de vie d'une Activity Android", "is_correct": False},
                    {"text": "Un pattern d'accompagnement entre deux objets", "is_correct": False},
                    {"text": "Un objet immuable partagé entre instances", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les higher-order functions en Kotlin?", "answers": [
                    {"text": "Des fonctions qui prennent d'autres fonctions en paramètre ou retournent des fonctions", "is_correct": True},
                    {"text": "Des fonctions avec une priorité d'exécution plus haute", "is_correct": False},
                    {"text": "Des fonctions de la bibliothèque standard optimisées", "is_correct": False},
                    {"text": "Des méthodes de classe parente dans la hiérarchie", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Flows en Kotlin?", "answers": [
                    {"text": "Un stream de données asynchrone cold (démarré à la collecte), observable et cancellable", "is_correct": True},
                    {"text": "Un système de navigation entre écrans Android", "is_correct": False},
                    {"text": "Un stream de données similaire aux RxJava Observables (hot)", "is_correct": False},
                    {"text": "Un canal de communication entre composants Android", "is_correct": False}
                ]},
                {"text": "Comment déstructurer un objet en Kotlin?", "answers": [
                    {"text": "val (a, b) = monObjet (avec componentN() définis ou data class)", "is_correct": True},
                    {"text": "val {a, b} = monObjet", "is_correct": False},
                    {"text": "destructure(monObjet) into (a, b)", "is_correct": False},
                    {"text": "val a = monObjet.a; val b = monObjet.b", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que inline function en Kotlin?", "answers": [
                    {"text": "Le compilateur copie le corps de la fonction à chaque appel pour éviter l'overhead des lambdas", "is_correct": True},
                    {"text": "Une fonction définie dans le corps d'une autre", "is_correct": False},
                    {"text": "Une fonction exécutée immédiatement (IIFE)", "is_correct": False},
                    {"text": "Une fonction optimisée pour les opérations inline CSS", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Kotlin - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que Kotlin Multiplatform (KMP)?", "answers": [
                    {"text": "Un framework permettant de partager du code Kotlin entre Android, iOS, web et desktop", "is_correct": True},
                    {"text": "Un outil pour compiler Kotlin vers plusieurs langages", "is_correct": False},
                    {"text": "Un système de build multi-module", "is_correct": False},
                    {"text": "Une plateforme de CI/CD pour projets Kotlin", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que reified en Kotlin?", "answers": [
                    {"text": "Permet d'accéder au type générique T à l'exécution dans une inline function (sans erasure)", "is_correct": True},
                    {"text": "Rend une variable immuable après initialisation", "is_correct": False},
                    {"text": "Force la réification (création) d'un objet lazy", "is_correct": False},
                    {"text": "Un modificateur pour les propriétés calculées", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que StateFlow vs SharedFlow?", "answers": [
                    {"text": "StateFlow a toujours une valeur courante et rejoue le dernier état; SharedFlow est plus flexible (hot stream)", "is_correct": True},
                    {"text": "StateFlow est cold, SharedFlow est hot", "is_correct": False},
                    {"text": "SharedFlow est uniquement pour Android, StateFlow pour multiplatform", "is_correct": False},
                    {"text": "Ils sont identiques mais pour des usages différents par convention", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les context receivers en Kotlin?", "answers": [
                    {"text": "Un mécanisme pour déclarer des dépendances contextuelles multiples dans une fonction/classe", "is_correct": True},
                    {"text": "Des receivers pour les Android Context", "is_correct": False},
                    {"text": "Des paramètres implicites de coroutines", "is_correct": False},
                    {"text": "Une alternative aux extension functions pour les DSLs", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le DSL building avec les lambda with receiver?", "answers": [
                    {"text": "Créer des APIs fluentes où les lambdas ont accès aux méthodes d'un objet receiver", "is_correct": True},
                    {"text": "Construire des layouts XML Android en Kotlin", "is_correct": False},
                    {"text": "Générer des DSL à partir d'annotations", "is_correct": False},
                    {"text": "Créer des langages domain-spécifiques en utilisant des opérateurs", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que suspend functions en Kotlin?", "answers": [
                    {"text": "Des fonctions pouvant suspendre leur exécution sans bloquer le thread, utilisables dans les coroutines", "is_correct": True},
                    {"text": "Des fonctions exécutées avec un délai", "is_correct": False},
                    {"text": "Des fonctions qui mettent le thread en pause", "is_correct": False},
                    {"text": "Des fonctions désactivées temporairement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Channel en Kotlin?", "answers": [
                    {"text": "Un mécanisme de communication entre coroutines permettant d'envoyer et recevoir des valeurs", "is_correct": True},
                    {"text": "Un canal HTTP pour les requêtes réseau", "is_correct": False},
                    {"text": "Un bus d'événements entre composants Android", "is_correct": False},
                    {"text": "Une file d'attente thread-safe pour Java interop", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que delegation en Kotlin?", "answers": [
                    {"text": "Implémenter une interface en déléguant les appels à un autre objet avec 'by'", "is_correct": True},
                    {"text": "Un pattern de design spécifique à Kotlin", "is_correct": False},
                    {"text": "Déléguer des permissions Android", "is_correct": False},
                    {"text": "Passer une fonction comme paramètre", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Value Classes (Inline Classes) en Kotlin?", "answers": [
                    {"text": "Des wrappers autour d'un type sous-jacent qui sont optimisés par le compilateur pour éviter l'allocation", "is_correct": True},
                    {"text": "Des classes immuables avec des valeurs constantes", "is_correct": False},
                    {"text": "Des classes sans état (stateless)", "is_correct": False},
                    {"text": "Des data classes optimisées pour la performance", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le compilateur K2 de Kotlin?", "answers": [
                    {"text": "Une réécriture complète du frontend du compilateur Kotlin avec de meilleures performances et analyses", "is_correct": True},
                    {"text": "La deuxième version du compilateur Kotlin vers Kotlin/Native", "is_correct": False},
                    {"text": "Un compilateur Kotlin pour WASM", "is_correct": False},
                    {"text": "Un compilateur JIT pour Kotlin", "is_correct": False}
                ]},
            ],
        },
    },
}

SWIFT_DATA = {
    "category": {
        "name": "Swift",
        "description": "Quiz pour maîtriser Swift et le développement iOS/macOS",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/swift/swift-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Swift - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Comment déclarer une constante en Swift?", "answers": [
                    {"text": "let constante = 5", "is_correct": True},
                    {"text": "const constante = 5", "is_correct": False},
                    {"text": "var constante = 5", "is_correct": False},
                    {"text": "final constante = 5", "is_correct": False}
                ]},
                {"text": "Comment déclarer une variable en Swift?", "answers": [
                    {"text": "var variable = 5", "is_correct": True},
                    {"text": "let variable = 5", "is_correct": False},
                    {"text": "mutable variable = 5", "is_correct": False},
                    {"text": "val variable = 5", "is_correct": False}
                ]},
                {"text": "Quel est le type optionnel en Swift?", "answers": [
                    {"text": "String?", "is_correct": True},
                    {"text": "Optional<String>", "is_correct": True},
                    {"text": "String!", "is_correct": False},
                    {"text": "None<String>", "is_correct": False}
                ]},
                {"text": "Comment afficher du texte en Swift?", "answers": [
                    {"text": "print(\"Hello\")", "is_correct": True},
                    {"text": "println(\"Hello\")", "is_correct": False},
                    {"text": "NSLog(\"Hello\")", "is_correct": False},
                    {"text": "console.log(\"Hello\")", "is_correct": False}
                ]},
                {"text": "Comment définir une fonction en Swift?", "answers": [
                    {"text": "func maFonction() {}", "is_correct": True},
                    {"text": "function maFonction() {}", "is_correct": False},
                    {"text": "def maFonction() {}", "is_correct": False},
                    {"text": "fn maFonction() {}", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le déballage forcé d'un optionnel?", "answers": [
                    {"text": "variable! (dangereux si nil)", "is_correct": True},
                    {"text": "variable?", "is_correct": False},
                    {"text": "variable as! Type", "is_correct": False},
                    {"text": "variable.unwrap()", "is_correct": False}
                ]},
                {"text": "Comment créer un tableau en Swift?", "answers": [
                    {"text": "var arr = [1, 2, 3]", "is_correct": True},
                    {"text": "var arr = Array(1, 2, 3)", "is_correct": False},
                    {"text": "var arr = arrayOf(1, 2, 3)", "is_correct": False},
                    {"text": "var arr = []", "is_correct": False}
                ]},
                {"text": "Comment créer un dictionnaire en Swift?", "answers": [
                    {"text": "var dict = [\"key\": \"value\"]", "is_correct": True},
                    {"text": "var dict = Dictionary(key: value)", "is_correct": False},
                    {"text": "var dict = mapOf(\"key\" to \"value\")", "is_correct": False},
                    {"text": "var dict = {\"key\": \"value\"}", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le guard let en Swift?", "answers": [
                    {"text": "Déballage conditionnel qui sort de la portée si échoue (early exit)", "is_correct": True},
                    {"text": "Un garde-fou contre les erreurs de type", "is_correct": False},
                    {"text": "Un mot-clé pour la protection mémoire", "is_correct": False},
                    {"text": "Une assertion conditionnelle", "is_correct": False}
                ]},
                {"text": "Comment définir une classe en Swift?", "answers": [
                    {"text": "class MaClasse {}", "is_correct": True},
                    {"text": "class MaClasse: NSObject {}", "is_correct": False},
                    {"text": "struct MaClasse {}", "is_correct": False},
                    {"text": "interface MaClasse {}", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Swift - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Quelle est la différence entre struct et class en Swift?", "answers": [
                    {"text": "struct est un value type (copié), class est un reference type (partagé)", "is_correct": True},
                    {"text": "class est plus rapide que struct", "is_correct": False},
                    {"text": "struct supporte l'héritage, class non", "is_correct": False},
                    {"text": "Aucune différence fondamentale", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un protocol en Swift?", "answers": [
                    {"text": "Une interface définissant des méthodes et propriétés que les types peuvent implémenter", "is_correct": True},
                    {"text": "Un protocole réseau iOS", "is_correct": False},
                    {"text": "Une extension de classe cachée", "is_correct": False},
                    {"text": "Un type de données spécial", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le ARC (Automatic Reference Counting) en Swift?", "answers": [
                    {"text": "Comptage automatique de références pour gérer la mémoire des instances de classes", "is_correct": True},
                    {"text": "Un garbage collector comme Java", "is_correct": False},
                    {"text": "Un système de comptage pour les structs", "is_correct": False},
                    {"text": "Une API de référencement automatique", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le closure en Swift?", "answers": [
                    {"text": "Un bloc de code autonome, similaire aux lambdas, capturant les variables de l'environnement", "is_correct": True},
                    {"text": "Une fonction privée", "is_correct": False},
                    {"text": "Un type de boucle fermée", "is_correct": False},
                    {"text": "Un gestionnaire d'événements système", "is_correct": False}
                ]},
                {"text": "Comment gérer la mémoire avec weak et unowned?", "answers": [
                    {"text": "weak: optionnel, devient nil; unowned: non-optionnel, crash si nil - pour éviter les cycles de références", "is_correct": True},
                    {"text": "weak est plus fort que unowned", "is_correct": False},
                    {"text": "unowned est pour les classes, weak pour les structs", "is_correct": False},
                    {"text": "Les deux sont identiques", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le pattern matching avec switch en Swift?", "answers": [
                    {"text": "switch très puissant avec matching de valeurs, tuples, ranges, où clauses", "is_correct": True},
                    {"text": "un simple switch avec break implicite", "is_correct": False},
                    {"text": "un if amélioré", "is_correct": False},
                    {"text": "une boucle conditionnelle", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que async/await en Swift?", "answers": [
                    {"text": "Un système de concurrence pour écrire du code asynchrone de manière synchrone", "is_correct": True},
                    {"text": "Des fonctions qui tournent en parallèle", "is_correct": False},
                    {"text": "Un système de threading simplifié", "is_correct": False},
                    {"text": "Des callbacks améliorés", "is_correct": False}
                ]},
                {"text": "Comment implémenter une extension en Swift?", "answers": [
                    {"text": "extension Type { nouvelleFonction() }", "is_correct": True},
                    {"text": "class Type + extension { }", "is_correct": False},
                    {"text": "Type.extend { }", "is_correct": False},
                    {"text": "extend Type { }", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Combine framework?", "answers": [
                    {"text": "Un framework de programmation réactive avec Publishers et Subscribers (équivalent RxSwift)", "is_correct": True},
                    {"text": "Un framework de combinaison de données", "is_correct": False},
                    {"text": "Un outil de fusion de requêtes réseau", "is_correct": False},
                    {"text": "Une bibliothèque de tests unitaires", "is_correct": False}
                ]},
                {"text": "Comment créer une propriété calculée en Swift?", "answers": [
                    {"text": "var nom: Type { get { } set { } }", "is_correct": True},
                    {"text": "var nom: Type = { }", "is_correct": False},
                    {"text": "computed var nom: Type { }", "is_correct": False},
                    {"text": "func nom() -> Type { }", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Swift - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que le Swift Concurrency (Actors)?", "answers": [
                    {"text": "Des types qui protègent leurs données mutables contre l'accès simultané (data races)", "is_correct": True},
                    {"text": "Des acteurs du système iOS", "is_correct": False},
                    {"text": "Des gestionnaires d'événements concurrents", "is_correct": False},
                    {"text": "Des threads légers Swift", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Swift Macros?", "answers": [
                    {"text": "Du code généré à la compilation qui transforme la syntaxe Swift (Swift 5.9+)", "is_correct": True},
                    {"text": "Des macros C préprocesseur", "is_correct": False},
                    {"text": "Des fonctions d'extension", "is_correct": False},
                    {"text": "Des templates Swift", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le SwiftUI et sa philosophie?", "answers": [
                    {"text": "Un framework UI déclaratif avec des vues comme état du UI, data-driven", "is_correct": True},
                    {"text": "UIKit avec une couche Swift", "is_correct": False},
                    {"text": "Un interface builder programmatique", "is_correct": False},
                    {"text": "Un remplaçant de Storyboard", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le property wrapper @State dans SwiftUI?", "answers": [
                    {"text": "Gère l'état local d'une vue, déclenche un re-render quand modifié", "is_correct": True},
                    {"text": "Wrapper pour les propriétés de classe", "is_correct": False},
                    {"text": "Un décorateur d'état global", "is_correct": False},
                    {"text": "Un observateur de propriétés", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le KeyPath en Swift?", "answers": [
                    {"text": "Une référence typée à une propriété d'un type (ex: Person.nom)", "is_correct": True},
                    {"text": "Un chemin de clé pour les dictionnaires", "is_correct": False},
                    {"text": "Une route de navigation", "is_correct": False},
                    {"text": "Un identifiant de clé de cryptographie", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le dynamic member lookup dans Swift?", "answers": [
                    {"text": "@dynamicMemberLookup permet l'accès à des propriétés dynamiques avec subscript(dynamicMember:)", "is_correct": True},
                    {"text": "Une recherche de membres dans un protocol", "is_correct": False},
                    {"text": "Un lookup de méthodes à l'exécution", "is_correct": False},
                    {"text": "Une introspection de type", "is_correct": False}
                ]},
                {"text": "Comment fonctionne la gestion d'erreur avec Result type?", "answers": [
                    {"text": "enum Result<Success, Failure> pour retourner succès ou erreur explicitement", "is_correct": True},
                    {"text": "try/catch uniquement", "is_correct": False},
                    {"text": "OptionSet d'erreurs", "is_correct": False},
                    {"text": "Un type d'erreur générique", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les opaque types (some) en Swift?", "answers": [
                    {"text": "Un type concret masqué qui implémente un protocol spécifique (retourné par fonction)", "is_correct": True},
                    {"text": "Un type optionnel caché", "is_correct": False},
                    {"text": "Un type partiellement opaque à la compilation", "is_correct": False},
                    {"text": "Un type générique spécial", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Swift Package Manager (SPM)?", "answers": [
                    {"text": "Le gestionnaire de dépendances officiel de Swift pour compiler et gérer les modules", "is_correct": True},
                    {"text": "CocoaPods amélioré", "is_correct": False},
                    {"text": "Un manager de packages binaires", "is_correct": False},
                    {"text": "Un système de build pour Xcode", "is_correct": False}
                ]},
                {"text": "Comment tester avec XCTest en Swift?", "answers": [
                    {"text": "Créer des classes héritant de XCTestCase avec des méthodes test*() et des assertions", "is_correct": True},
                    {"text": "Avec des annotations @Test et @Assert", "is_correct": False},
                    {"text": "En écrivant des tests dans le playground", "is_correct": False},
                    {"text": "SwiftUI inclut son propre framework de test", "is_correct": False}
                ]},
            ],
        },
    },
}

PHP_DATA = {
    "category": {
        "name": "PHP",
        "description": "Quiz pour maîtriser PHP et le développement web côté serveur",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/php/php-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "PHP - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Comment ouvrir un bloc PHP?", "answers": [
                    {"text": "<?php", "is_correct": True},
                    {"text": "<php>", "is_correct": False},
                    {"text": "<%php", "is_correct": False},
                    {"text": "#{php}", "is_correct": False}
                ]},
                {"text": "Comment déclarer une variable en PHP?", "answers": [
                    {"text": "$maVariable = 'valeur';", "is_correct": True},
                    {"text": "var maVariable = 'valeur';", "is_correct": False},
                    {"text": "let maVariable = 'valeur';", "is_correct": False},
                    {"text": "maVariable = 'valeur';", "is_correct": False}
                ]},
                {"text": "Comment afficher du texte en PHP?", "answers": [
                    {"text": "echo 'Hello';", "is_correct": True},
                    {"text": "print('Hello');", "is_correct": True},
                    {"text": "console.log('Hello');", "is_correct": False},
                    {"text": "printf('Hello');", "is_correct": False}
                ]},
                {"text": "Comment créer un tableau en PHP?", "answers": [
                    {"text": "$arr = [1, 2, 3];", "is_correct": True},
                    {"text": "$arr = array(1, 2, 3);", "is_correct": True},
                    {"text": "$arr = {1, 2, 3};", "is_correct": False},
                    {"text": "$arr = (1, 2, 3);", "is_correct": False}
                ]},
                {"text": "Comment concaténer des chaînes en PHP?", "answers": [
                    {"text": "Avec l'opérateur . (point)", "is_correct": True},
                    {"text": "Avec l'opérateur +", "is_correct": False},
                    {"text": "Avec la fonction concat()", "is_correct": False},
                    {"text": "Avec l'opérateur &", "is_correct": False}
                ]},
                {"text": "Quel est le type de commentaire sur une ligne en PHP?", "answers": [
                    {"text": "// commentaire", "is_correct": True},
                    {"text": "# commentaire", "is_correct": True},
                    {"text": "/* commentaire */", "is_correct": False},
                    {"text": "-- commentaire", "is_correct": False}
                ]},
                {"text": "Comment définir une fonction en PHP?", "answers": [
                    {"text": "function maFonction() {}", "is_correct": True},
                    {"text": "def maFonction() {}", "is_correct": False},
                    {"text": "func maFonction() {}", "is_correct": False},
                    {"text": "fn maFonction() {}", "is_correct": False}
                ]},
                {"text": "Comment inclure un autre fichier PHP?", "answers": [
                    {"text": "include 'fichier.php';", "is_correct": True},
                    {"text": "require 'fichier.php';", "is_correct": True},
                    {"text": "import 'fichier.php';", "is_correct": False},
                    {"text": "use 'fichier.php';", "is_correct": False}
                ]},
                {"text": "Quelle superglobale contient les données POST?", "answers": [
                    {"text": "$_POST", "is_correct": True},
                    {"text": "$POST", "is_correct": False},
                    {"text": "$_REQUEST['post']", "is_correct": False},
                    {"text": "$request->post", "is_correct": False}
                ]},
                {"text": "Comment vérifier si une variable existe en PHP?", "answers": [
                    {"text": "isset($variable)", "is_correct": True},
                    {"text": "exists($variable)", "is_correct": False},
                    {"text": "$variable !== null", "is_correct": False},
                    {"text": "defined($variable)", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "PHP - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Quelle est la différence entre == et === en PHP?", "answers": [
                    {"text": "=== compare la valeur ET le type, == compare seulement la valeur (avec coercition)", "is_correct": True},
                    {"text": "Aucune différence", "is_correct": False},
                    {"text": "=== est plus lent mais plus précis", "is_correct": False},
                    {"text": "== compare les références des objets", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que la POO en PHP?", "answers": [
                    {"text": "Programmation Orientée Objet - classes, héritage, interfaces, traits, etc.", "is_correct": True},
                    {"text": "PHP Oriented Operations", "is_correct": False},
                    {"text": "Un style de programmation sans fonctions", "is_correct": False},
                    {"text": "Un design pattern PHP", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un trait PHP?", "answers": [
                    {"text": "Un mécanisme de réutilisation de code entre classes (comme un mixin)", "is_correct": True},
                    {"text": "Une interface avec implémentation partielle", "is_correct": False},
                    {"text": "Une caractéristique d'un type primitif", "is_correct": False},
                    {"text": "Un attribut de classe", "is_correct": False}
                ]},
                {"text": "Comment gérer les exceptions en PHP?", "answers": [
                    {"text": "try { } catch (Exception $e) { } finally { }", "is_correct": True},
                    {"text": "try { } except Exception { }", "is_correct": False},
                    {"text": "begin { } rescue { }", "is_correct": False},
                    {"text": "error_handler(function($e) {})", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Composer en PHP?", "answers": [
                    {"text": "Le gestionnaire de dépendances PHP (equivalent à npm pour JS)", "is_correct": True},
                    {"text": "Un framework PHP léger", "is_correct": False},
                    {"text": "Un outil de compilation PHP", "is_correct": False},
                    {"text": "Un générateur de code PHP", "is_correct": False}
                ]},
                {"text": "Comment créer un namespace en PHP?", "answers": [
                    {"text": "namespace App\\Controllers;", "is_correct": True},
                    {"text": "module App::Controllers", "is_correct": False},
                    {"text": "package App.Controllers;", "is_correct": False},
                    {"text": "scope App/Controllers;", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre require et require_once?", "answers": [
                    {"text": "require_once vérifie si le fichier a déjà été inclus et l'ignore si c'est le cas", "is_correct": True},
                    {"text": "require_once est plus performant", "is_correct": False},
                    {"text": "require lève une erreur si le fichier est absent, require_once non", "is_correct": False},
                    {"text": "Aucune différence", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que PDO en PHP?", "answers": [
                    {"text": "PHP Data Objects - une abstraction d'accès aux bases de données avec requêtes préparées", "is_correct": True},
                    {"text": "Un ORM PHP complet", "is_correct": False},
                    {"text": "Un protocole de connexion à MySQL", "is_correct": False},
                    {"text": "Un système de migration de base de données", "is_correct": False}
                ]},
                {"text": "Comment implémenter une interface en PHP?", "answers": [
                    {"text": "class MaClasse implements MonInterface {}", "is_correct": True},
                    {"text": "class MaClasse extends MonInterface {}", "is_correct": False},
                    {"text": "class MaClasse : MonInterface {}", "is_correct": False},
                    {"text": "class MaClasse use MonInterface {}", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les fonctions anonymes (closures) en PHP?", "answers": [
                    {"text": "Des fonctions sans nom assignables à des variables ou passées en argument", "is_correct": True},
                    {"text": "Des fonctions privées non accessibles depuis l'extérieur", "is_correct": False},
                    {"text": "Des fonctions qui se ferment après exécution", "is_correct": False},
                    {"text": "Des fonctions dans un namespace fermé", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "PHP - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que les Generators en PHP?", "answers": [
                    {"text": "Des fonctions utilisant yield pour produire des valeurs à la demande sans tout charger en mémoire", "is_correct": True},
                    {"text": "Des classes qui génèrent du code automatiquement", "is_correct": False},
                    {"text": "Un système de templating PHP", "is_correct": False},
                    {"text": "Des workers de traitement en arrière-plan", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Fibers en PHP 8.1?", "answers": [
                    {"text": "Des coroutines légères permettant la concurrence coopérative et la pause/reprise d'exécution", "is_correct": True},
                    {"text": "Des threads PHP natifs", "is_correct": False},
                    {"text": "Un système de cache de fibres", "is_correct": False},
                    {"text": "Des connexions de base de données persistantes", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le JIT en PHP 8?", "answers": [
                    {"text": "Just-In-Time compilation qui compile le bytecode en code machine à l'exécution pour de meilleures performances", "is_correct": True},
                    {"text": "Java Integrated Technology", "is_correct": False},
                    {"text": "Un système de cache d'opcode amélioré", "is_correct": False},
                    {"text": "Un compilateur PHP vers WebAssembly", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Attributes en PHP 8?", "answers": [
                    {"text": "Des métadonnées structurées ajoutées aux classes/méthodes/propriétés et lisibles via la Reflection API", "is_correct": True},
                    {"text": "Des propriétés de classe avec valeurs par défaut", "is_correct": False},
                    {"text": "Des décorateurs HTML pour les templates", "is_correct": False},
                    {"text": "Des annotations de documentation PHPDoc", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que l'union types en PHP 8?", "answers": [
                    {"text": "Un typage acceptant plusieurs types : function fn(int|string $param): int|null", "is_correct": True},
                    {"text": "Un type pour les unions SQL", "is_correct": False},
                    {"text": "La fusion de deux tableaux typés", "is_correct": False},
                    {"text": "Un type pour les valeurs numériques mixtes", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que named arguments en PHP 8?", "answers": [
                    {"text": "Passer les arguments par nom dans n'importe quel ordre : fn(name: 'Alice', age: 30)", "is_correct": True},
                    {"text": "Nommer les variables avec des alias", "is_correct": False},
                    {"text": "Des paramètres de configuration nommés", "is_correct": False},
                    {"text": "Des constantes de classe nommées", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le match expression en PHP 8?", "answers": [
                    {"text": "Un switch amélioré avec comparaison stricte, retournant une valeur, sans fallthrough", "is_correct": True},
                    {"text": "Un système de pattern matching sur les types", "is_correct": False},
                    {"text": "Un outil de correspondance de regex", "is_correct": False},
                    {"text": "Une fonction de comparaison de tableaux", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Intersection Types en PHP 8.1?", "answers": [
                    {"text": "Un type qui doit satisfaire plusieurs interfaces simultanément : TypeA&TypeB", "is_correct": True},
                    {"text": "La combinaison de deux types primitifs", "is_correct": False},
                    {"text": "Un type pour les valeurs à l'intersection de deux ensembles", "is_correct": False},
                    {"text": "Un opérateur de fusion de tableaux", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Nullsafe operator ?-> en PHP 8?", "answers": [
                    {"text": "Chaîne d'appels qui court-circuite et retourne null si un élément est null, sans erreur", "is_correct": True},
                    {"text": "Un opérateur pour créer des valeurs nullable", "is_correct": False},
                    {"text": "Une alternative à isset()", "is_correct": False},
                    {"text": "Un opérateur pour les requêtes SQL nullable", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Enum en PHP 8.1?", "answers": [
                    {"text": "Un type énuméré avec des cas nommés, pouvant être backed (int/string) et implémenter des interfaces", "is_correct": True},
                    {"text": "Une liste de constantes groupées dans une classe", "is_correct": False},
                    {"text": "Un type de données pour les options de configuration", "is_correct": False},
                    {"text": "Une extension de classe abstraite", "is_correct": False}
                ]},
            ],
        },
    },
}

CPLUSPLUS_DATA = {
    "category": {
        "name": "C++",
        "description": "Quiz pour maîtriser C++ et la programmation système",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/cplusplus/cplusplus-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "C++ - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Comment inclure une bibliothèque standard en C++?", "answers": [
                    {"text": "#include <iostream>", "is_correct": True},
                    {"text": "import iostream;", "is_correct": False},
                    {"text": "#include \"iostream.h\"", "is_correct": False},
                    {"text": "using iostream;", "is_correct": False}
                ]},
                {"text": "Quel est le point d'entrée d'un programme C++?", "answers": [
                    {"text": "int main() {}", "is_correct": True},
                    {"text": "void main() {}", "is_correct": False},
                    {"text": "int Main() {}", "is_correct": False},
                    {"text": "program main() {}", "is_correct": False}
                ]},
                {"text": "Comment afficher du texte en C++?", "answers": [
                    {"text": "std::cout << \"Hello\" << std::endl;", "is_correct": True},
                    {"text": "printf(\"Hello\");", "is_correct": False},
                    {"text": "Console.WriteLine(\"Hello\");", "is_correct": False},
                    {"text": "print(\"Hello\");", "is_correct": False}
                ]},
                {"text": "Comment déclarer une variable entière en C++?", "answers": [
                    {"text": "int x = 5;", "is_correct": True},
                    {"text": "integer x = 5;", "is_correct": False},
                    {"text": "var x = 5;", "is_correct": False},
                    {"text": "int x(5);", "is_correct": True}
                ]},
                {"text": "Qu'est-ce que l'opérateur new en C++?", "answers": [
                    {"text": "Alloue de la mémoire sur le heap", "is_correct": True},
                    {"text": "Crée un nouvel objet sur la stack", "is_correct": False},
                    {"text": "Instancie un template", "is_correct": False},
                    {"text": "Déclare une nouvelle variable", "is_correct": False}
                ]},
                {"text": "Comment créer une fonction en C++?", "answers": [
                    {"text": "int maFonction() { return 0; }", "is_correct": True},
                    {"text": "function maFonction() {}", "is_correct": False},
                    {"text": "def maFonction(): int", "is_correct": False},
                    {"text": "func maFonction() int", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre ++i et i++?", "answers": [
                    {"text": "++i pré-incrémente (incrémente puis utilise), i++ post-incrémente (utilise puis incrémente)", "is_correct": True},
                    {"text": "++i est plus rapide que i++", "is_correct": False},
                    {"text": "i++ est préférable dans les boucles", "is_correct": False},
                    {"text": "Aucune différence", "is_correct": False}
                ]},
                {"text": "Comment créer un commentaire en C++?", "answers": [
                    {"text": "// commentaire", "is_correct": True},
                    {"text": "/* commentaire */", "is_correct": True},
                    {"text": "# commentaire", "is_correct": False},
                    {"text": "' commentaire", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que std::vector en C++?", "answers": [
                    {"text": "Un tableau dynamique de la STL", "is_correct": True},
                    {"text": "Un vecteur mathématique", "is_correct": False},
                    {"text": "Un conteneur de pointeurs", "is_correct": False},
                    {"text": "Une classe de calcul vectoriel", "is_correct": False}
                ]},
                {"text": "Comment lire une entrée utilisateur en C++?", "answers": [
                    {"text": "std::cin >> variable;", "is_correct": True},
                    {"text": "scanf(\"%d\", &variable);", "is_correct": False},
                    {"text": "Console.ReadLine();", "is_correct": False},
                    {"text": "getline(std::cin, variable);", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "C++ - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que le RAII en C++?", "answers": [
                    {"text": "Resource Acquisition Is Initialization - lier la durée de vie des ressources à celle des objets", "is_correct": True},
                    {"text": "Un système de gestion des exceptions", "is_correct": False},
                    {"text": "Un pattern de conception", "is_correct": False},
                    {"text": "Une bibliothèque de threading", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre pointeur et référence?", "answers": [
                    {"text": "Référence: alias non-nullable, ne peut être réassignée; Pointeur: peut être null et réassigné", "is_correct": True},
                    {"text": "Pointeur est plus rapide que référence", "is_correct": False},
                    {"text": "Référence utilise moins de mémoire", "is_correct": False},
                    {"text": "Aucune différence", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que l'héritage multiple en C++?", "answers": [
                    {"text": "Une classe peut hériter de plusieurs classes de base (avec ambiguïtés possibles)", "is_correct": True},
                    {"text": "Un héritage sur plusieurs niveaux", "is_correct": False},
                    {"text": "Plusieurs classes héritent d'une même classe", "is_correct": False},
                    {"text": "Un concept inexistant en C++", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le polymorphisme en C++?", "answers": [
                    {"text": "Capacité à traiter des objets de types dérivés via des pointeurs/références de base (virtual)", "is_correct": True},
                    {"text": "Plusieurs formes pour une même fonction", "is_correct": False},
                    {"text": "Surcharge de fonctions uniquement", "is_correct": False},
                    {"text": "Templates C++", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les templates en C++?", "answers": [
                    {"text": "Génération de code paramétré par types (programmation générique)", "is_correct": True},
                    {"text": "Des modèles de classes préconçues", "is_correct": False},
                    {"text": "Un système de méta-programmation", "is_correct": False},
                    {"text": "Des classes virtuelles pures", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que la STL (Standard Template Library)?", "answers": [
                    {"text": "Conteneurs, algorithmes, itérateurs et foncteurs standards", "is_correct": True},
                    {"text": "Une bibliothèque de templates système", "is_correct": False},
                    {"text": "La librairie standard C uniquement", "is_correct": False},
                    {"text": "Un ensemble de classes pour l'UI", "is_correct": False}
                ]},
                {"text": "Comment fonctionne la gestion mémoire en C++?", "answers": [
                    {"text": "Manuelle avec new/delete, ou automatique avec RAII/smart pointers", "is_correct": True},
                    {"text": "Garbage collector automatique", "is_correct": False},
                    {"text": "ARC comme Swift", "is_correct": False},
                    {"text": "Tout est automatique", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que std::unique_ptr?", "answers": [
                    {"text": "Smart pointer avec propriété exclusive (non copiable, seulement movable)", "is_correct": True},
                    {"text": "Un pointeur unique vers un objet", "is_correct": False},
                    {"text": "Un pointeur qui ne peut être dupliqué", "is_correct": False},
                    {"text": "Un alias de pointeur", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le const correctness en C++?", "answers": [
                    {"text": "Marquer les paramètres/méthodes/variables comme const quand ils ne modifient pas l'état", "is_correct": True},
                    {"text": "Corriger les erreurs de compilation", "is_correct": False},
                    {"text": "Un outil de vérification de code", "is_correct": False},
                    {"text": "Une convention de nommage", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que l'opérateur de résolution de portée ::?", "answers": [
                    {"text": "Accéder à des membres de namespace, classe, ou global (::x)", "is_correct": True},
                    {"text": "Définir un espace de noms", "is_correct": False},
                    {"text": "L'opérateur de portée des boucles", "is_correct": False},
                    {"text": "Un opérateur de comparaison", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "C++ - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que le move semantics et std::move en C++11?", "answers": [
                    {"text": "Transférer les ressources d'un objet temporaire sans copie, via rvalue references (&&)", "is_correct": True},
                    {"text": "Déplacer un objet en mémoire", "is_correct": False},
                    {"text": "Changer l'emplacement d'un objet", "is_correct": False},
                    {"text": "Copier un objet rapidement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le SFINAE (Substitution Failure Is Not An Error)?", "answers": [
                    {"text": "Principe template où les instanciations invalides sont ignorées plutôt qu'erreurs", "is_correct": True},
                    {"text": "Un concept de méta-programmation avancée", "is_correct": False},
                    {"text": "Un outil de debugging template", "is_correct": False},
                    {"text": "Une bibliothèque de traits", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les concepts en C++20?", "answers": [
                    {"text": "Contraintes sur les paramètres template (named requirements) pour meilleurs messages d'erreur", "is_correct": True},
                    {"text": "Des idées abstraites en C++", "is_correct": False},
                    {"text": "Des classes conceptuelles", "is_correct": False},
                    {"text": "Un nouveau type de classe", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les coroutines en C++20?", "answers": [
                    {"text": "Fonctions pouvant suspendre/reprendre exécution, utiles pour l'asynchrone", "is_correct": True},
                    {"text": "Des threads légers", "is_correct": False},
                    {"text": "Des générateurs de code", "is_correct": False},
                    {"text": "Des fonctions parallèles", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le CRTP (Curiously Recurring Template Pattern)?", "answers": [
                    {"text": "Une classe dérivée passée comme paramètre template à sa base (polymorphisme statique)", "is_correct": True},
                    {"text": "Un pattern de récursion template", "is_correct": False},
                    {"text": "Un algorithme de tri", "is_correct": False},
                    {"text": "Un design pattern de création", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le multithreading en C++ moderne?", "answers": [
                    {"text": "std::thread, std::async, std::mutex, std::atomic, std::condition_variable", "is_correct": True},
                    {"text": "Avec pthreads uniquement", "is_correct": False},
                    {"text": "OpenMP seulement", "is_correct": False},
                    {"text": "Pas de support natif", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le type deduction avec auto et decltype?", "answers": [
                    {"text": "auto déduit le type d'une variable; decltype inspecte le type d'une expression", "is_correct": True},
                    {"text": "auto et decltype sont interchangeables", "is_correct": False},
                    {"text": "auto est pour les boucles, decltype pour les retours", "is_correct": False},
                    {"text": "Ce sont des mot-clés obsolètes", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le placement new en C++?", "answers": [
                    {"text": "Construit un objet à un emplacement mémoire déjà alloué (placement new)", "is_correct": True},
                    {"text": "Une nouvelle syntaxe pour new", "is_correct": False},
                    {"text": "Un opérateur de placement mémoire", "is_correct": False},
                    {"text": "Un allocateur personnalisé", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le type punning en C++?", "answers": [
                    {"text": "Interpréter la représentation mémoire d'un type comme un autre (via union, memcpy, ou reinterpret_cast)", "is_correct": True},
                    {"text": "Un jeu de mots en programmation", "is_correct": False},
                    {"text": "Une technique de casting", "is_correct": False},
                    {"text": "Un alias de type dangereux", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le modules en C++20?", "answers": [
                    {"text": "Alternative aux headers avec meilleure encapsulation et temps de compilation réduits", "is_correct": True},
                    {"text": "Des modules de code importables", "is_correct": False},
                    {"text": "Des namespaces améliorés", "is_correct": False},
                    {"text": "Une bibliothèque de modules", "is_correct": False}
                ]},
            ],
        },
    },
}

# 2. FRAMEWORKS WEB FRONTEND
# -----------------------------------------------------------------------------

REACT_DATA = {
    "category": {
        "name": "React",
        "description": "Quiz pour maîtriser React et le développement d'interfaces utilisateur",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "React - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que JSX?", "answers": [
                    {"text": "Une extension de syntaxe JavaScript permettant d'écrire du HTML dans JS", "is_correct": True},
                    {"text": "Un langage de programmation basé sur JavaScript", "is_correct": False},
                    {"text": "Un framework CSS pour React", "is_correct": False},
                    {"text": "Un gestionnaire de paquets JavaScript", "is_correct": False}
                ]},
                {"text": "Comment créer un composant fonctionnel React?", "answers": [
                    {"text": "const MonComposant = () => <div>Hello</div>", "is_correct": True},
                    {"text": "function MonComposant.render() { return <div>Hello</div> }", "is_correct": False},
                    {"text": "React.createComponent('MonComposant', () => <div>Hello</div>)", "is_correct": False},
                    {"text": "class MonComposant { render() { return <div>Hello</div> } }", "is_correct": False}
                ]},
                {"text": "Quel hook React gère l'état local d'un composant?", "answers": [
                    {"text": "useState", "is_correct": True},
                    {"text": "useEffect", "is_correct": False},
                    {"text": "useContext", "is_correct": False},
                    {"text": "useRef", "is_correct": False}
                ]},
                {"text": "Comment passer des données à un composant enfant?", "answers": [
                    {"text": "Via les props", "is_correct": True},
                    {"text": "Via setState", "is_correct": False},
                    {"text": "Via useContext uniquement", "is_correct": False},
                    {"text": "Via une variable globale", "is_correct": False}
                ]},
                {"text": "Que retourne useState(0)?", "answers": [
                    {"text": "[valeur, setValeur] - la valeur actuelle et une fonction de mise à jour", "is_correct": True},
                    {"text": "La valeur 0 directement", "is_correct": False},
                    {"text": "Un objet { state: 0, setState: fn }", "is_correct": False},
                    {"text": "Une référence mutable", "is_correct": False}
                ]},
                {"text": "À quoi sert la prop 'key' dans une liste React?", "answers": [
                    {"text": "Aider React à identifier les éléments modifiés, ajoutés ou supprimés", "is_correct": True},
                    {"text": "Donner accès à l'élément depuis le parent", "is_correct": False},
                    {"text": "Définir l'ordre d'affichage des éléments", "is_correct": False},
                    {"text": "Appliquer un style unique à chaque élément", "is_correct": False}
                ]},
                {"text": "Comment importer React dans un fichier?", "answers": [
                    {"text": "import React from 'react'", "is_correct": True},
                    {"text": "require('react')", "is_correct": False},
                    {"text": "import { React } from 'react'", "is_correct": False},
                    {"text": "include React from 'react'", "is_correct": False}
                ]},
                {"text": "Quel outil est recommandé pour créer un projet React rapidement?", "answers": [
                    {"text": "Create React App ou Vite", "is_correct": True},
                    {"text": "npm init react", "is_correct": False},
                    {"text": "react new mon-app", "is_correct": False},
                    {"text": "yarn create app", "is_correct": False}
                ]},
                {"text": "Comment afficher conditionnellement un élément en React?", "answers": [
                    {"text": "{condition && <Composant />}", "is_correct": True},
                    {"text": "<if condition={true}><Composant /></if>", "is_correct": False},
                    {"text": "React.showIf(condition, <Composant />)", "is_correct": False},
                    {"text": "conditional(<Composant />, condition)", "is_correct": False}
                ]},
                {"text": "Quelle méthode du cycle de vie est équivalente à useEffect(() => {}, []) ?", "answers": [
                    {"text": "componentDidMount", "is_correct": True},
                    {"text": "componentDidUpdate", "is_correct": False},
                    {"text": "componentWillMount", "is_correct": False},
                    {"text": "shouldComponentUpdate", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "React - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que useEffect et quand s'exécute-t-il?", "answers": [
                    {"text": "Un hook qui s'exécute après chaque rendu pour gérer les effets de bord", "is_correct": True},
                    {"text": "Un hook qui s'exécute avant le rendu du composant", "is_correct": False},
                    {"text": "Un hook qui remplace setState dans les composants fonctionnels", "is_correct": False},
                    {"text": "Un hook pour gérer les animations uniquement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Context API?", "answers": [
                    {"text": "Un mécanisme pour partager des données entre composants sans prop drilling", "is_correct": True},
                    {"text": "Une API REST fournie par React", "is_correct": False},
                    {"text": "Un système de routage intégré à React", "is_correct": False},
                    {"text": "Un outil de gestion des requêtes HTTP", "is_correct": False}
                ]},
                {"text": "Que fait useCallback?", "answers": [
                    {"text": "Mémoïse une fonction pour éviter sa recréation à chaque rendu", "is_correct": True},
                    {"text": "Crée une fonction asynchrone optimisée", "is_correct": False},
                    {"text": "Gère les callbacks d'événements DOM", "is_correct": False},
                    {"text": "Remplace useEffect pour les appels API", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le prop drilling?", "answers": [
                    {"text": "Passer des props à travers plusieurs niveaux de composants pour atteindre le bon enfant", "is_correct": True},
                    {"text": "Modifier les props reçues dans un composant enfant", "is_correct": False},
                    {"text": "Valider les props avec PropTypes", "is_correct": False},
                    {"text": "Déboguer les props dans les DevTools", "is_correct": False}
                ]},
                {"text": "Comment mémoïser un composant pour éviter les re-renders inutiles?", "answers": [
                    {"text": "React.memo(MonComposant)", "is_correct": True},
                    {"text": "React.cache(MonComposant)", "is_correct": False},
                    {"text": "useMemo(MonComposant, [])", "is_correct": False},
                    {"text": "MonComposant.pure()", "is_correct": False}
                ]},
                {"text": "Que fait useMemo?", "answers": [
                    {"text": "Mémoïse le résultat d'un calcul coûteux entre les rendus", "is_correct": True},
                    {"text": "Mémoïse un composant entier", "is_correct": False},
                    {"text": "Stocke une référence mutable", "is_correct": False},
                    {"text": "Mémoïse les appels API", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un custom hook?", "answers": [
                    {"text": "Une fonction commençant par 'use' qui réutilise de la logique avec des hooks React", "is_correct": True},
                    {"text": "Un hook fourni par une bibliothèque tierce", "is_correct": False},
                    {"text": "Un hook qui modifie le comportement de useState", "is_correct": False},
                    {"text": "Un hook propre aux composants de classe", "is_correct": False}
                ]},
                {"text": "Comment gérer un formulaire contrôlé en React?", "answers": [
                    {"text": "Lier la valeur à un état via value et onChange", "is_correct": True},
                    {"text": "Utiliser directement document.getElementById", "is_correct": False},
                    {"text": "Utiliser useRef sans état", "is_correct": False},
                    {"text": "Laisser le DOM gérer l'état du formulaire", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que useReducer?", "answers": [
                    {"text": "Un hook pour gérer un état complexe via une fonction reducer, alternative à useState", "is_correct": True},
                    {"text": "Un hook pour réduire la taille du bundle", "is_correct": False},
                    {"text": "Un hook qui combine plusieurs états en un", "is_correct": False},
                    {"text": "Une alternative à useEffect pour la logique asynchrone", "is_correct": False}
                ]},
                {"text": "Comment nettoyer un effet dans useEffect?", "answers": [
                    {"text": "Retourner une fonction de nettoyage depuis le callback de useEffect", "is_correct": True},
                    {"text": "Appeler useEffect.cleanup() après l'effet", "is_correct": False},
                    {"text": "Utiliser useLayoutEffect à la place", "is_correct": False},
                    {"text": "Passer un deuxième argument cleanup à useEffect", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "React - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que React Concurrent Mode?", "answers": [
                    {"text": "Un mode permettant à React de préparer plusieurs versions de l'UI simultanément", "is_correct": True},
                    {"text": "Un mode multi-thread pour React Native", "is_correct": False},
                    {"text": "Un mode pour gérer plusieurs contextes simultanément", "is_correct": False},
                    {"text": "Un mode de rendu côté serveur parallèle", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Suspense en React?", "answers": [
                    {"text": "Un composant permettant d'afficher un fallback pendant le chargement de contenu asynchrone", "is_correct": True},
                    {"text": "Un hook pour suspendre l'exécution d'un effet", "is_correct": False},
                    {"text": "Un outil de gestion des erreurs asynchrones", "is_correct": False},
                    {"text": "Un mécanisme pour différer le rendu des composants lourds", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Server Component en React 18+?", "answers": [
                    {"text": "Un composant qui s'exécute uniquement côté serveur, sans JS côté client", "is_correct": True},
                    {"text": "Un composant qui fetch des données depuis un serveur", "is_correct": False},
                    {"text": "Un composant SSR classique avec hydratation", "is_correct": False},
                    {"text": "Un composant partagé entre plusieurs serveurs", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le Virtual DOM de React?", "answers": [
                    {"text": "React compare l'ancien et le nouveau Virtual DOM (diffing) puis applique les changements minimaux au DOM réel", "is_correct": True},
                    {"text": "React remplace entièrement le DOM réel à chaque rendu", "is_correct": False},
                    {"text": "React manipule directement le DOM sans abstraction", "is_correct": False},
                    {"text": "React crée un DOM virtuel uniquement pour les animations", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que useTransition en React 18?", "answers": [
                    {"text": "Un hook pour marquer des mises à jour d'état comme non-urgentes afin de garder l'UI responsive", "is_correct": True},
                    {"text": "Un hook pour créer des transitions CSS animées", "is_correct": False},
                    {"text": "Un hook pour gérer les transitions de navigation", "is_correct": False},
                    {"text": "Un hook pour débouncer les mises à jour d'état", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Error Boundary?", "answers": [
                    {"text": "Un composant de classe qui capture les erreurs JS dans ses enfants et affiche un fallback", "is_correct": True},
                    {"text": "Un hook pour gérer les erreurs dans les composants fonctionnels", "is_correct": False},
                    {"text": "Un outil de linting pour React", "is_correct": False},
                    {"text": "Un wrapper autour de try/catch pour les hooks", "is_correct": False}
                ]},
                {"text": "Comment implémenter le code splitting avec React?", "answers": [
                    {"text": "React.lazy() avec Suspense pour charger les composants à la demande", "is_correct": True},
                    {"text": "En divisant manuellement le fichier bundle", "is_correct": False},
                    {"text": "En utilisant useImport() hook", "is_correct": False},
                    {"text": "En configurant webpack uniquement", "is_correct": False}
                ]},
                {"text": "Que fait useImperativeHandle?", "answers": [
                    {"text": "Personnalise les valeurs exposées par un composant via une ref (avec forwardRef)", "is_correct": True},
                    {"text": "Exécute du code impératif en dehors du cycle React", "is_correct": False},
                    {"text": "Accède au DOM de manière impérative", "is_correct": False},
                    {"text": "Remplace useEffect pour les effets impératifs", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le batching automatique en React 18?", "answers": [
                    {"text": "React regroupe automatiquement plusieurs setState en un seul re-render, même dans des callbacks async", "is_correct": True},
                    {"text": "React divise automatiquement le code en batch pour optimiser le bundle", "is_correct": False},
                    {"text": "React traite les requêtes API en batch", "is_correct": False},
                    {"text": "React group les composants similaires pour les réutiliser", "is_correct": False}
                ]},
                {"text": "Comment optimiser les re-renders causés par le Context?", "answers": [
                    {"text": "Séparer les contextes par domaine et mémoïser les valeurs avec useMemo", "is_correct": True},
                    {"text": "Utiliser useContext dans un seul composant racine", "is_correct": False},
                    {"text": "Éviter complètement useContext et utiliser Redux", "is_correct": False},
                    {"text": "Passer les valeurs du contexte via des props à la place", "is_correct": False}
                ]},
            ],
        },
    },
}

VUEJS_DATA = {
    "category": {
        "name": "Vue.js",
        "description": "Quiz pour maîtriser Vue.js et le développement frontend réactif",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vuejs/vuejs-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Vue.js - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Quelle directive Vue.js lie une valeur de données à l'affichage?", "answers": [
                    {"text": "v-bind ou les moustaches {{ }}", "is_correct": True},
                    {"text": "v-show", "is_correct": False},
                    {"text": "v-data", "is_correct": False},
                    {"text": "v-display", "is_correct": False}
                ]},
                {"text": "Quelle directive Vue.js gère les événements?", "answers": [
                    {"text": "v-on (ou @)", "is_correct": True},
                    {"text": "v-event", "is_correct": False},
                    {"text": "v-handle", "is_correct": False},
                    {"text": "v-listen", "is_correct": False}
                ]},
                {"text": "Comment afficher/cacher un élément conditionnellement en Vue.js?", "answers": [
                    {"text": "v-if et v-else", "is_correct": True},
                    {"text": "v-show et v-hide", "is_correct": False},
                    {"text": "v-display", "is_correct": False},
                    {"text": "v-condition", "is_correct": False}
                ]},
                {"text": "Quelle directive Vue.js boucle sur une liste?", "answers": [
                    {"text": "v-for", "is_correct": True},
                    {"text": "v-each", "is_correct": False},
                    {"text": "v-loop", "is_correct": False},
                    {"text": "v-repeat", "is_correct": False}
                ]},
                {"text": "Comment créer un binding bidirectionnel sur un input?", "answers": [
                    {"text": "v-model", "is_correct": True},
                    {"text": "v-bind:value + v-on:input", "is_correct": False},
                    {"text": "v-two-way", "is_correct": False},
                    {"text": "v-input", "is_correct": False}
                ]},
                {"text": "Comment déclarer un composant Vue.js en Composition API?", "answers": [
                    {"text": "defineComponent avec setup() ou <script setup>", "is_correct": True},
                    {"text": "Vue.component('nom', {})", "is_correct": False},
                    {"text": "createComponent({})", "is_correct": False},
                    {"text": "new Vue({})", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que ref() dans la Composition API Vue.js?", "answers": [
                    {"text": "Crée une référence réactive autour d'une valeur primitive", "is_correct": True},
                    {"text": "Référence un élément DOM", "is_correct": False},
                    {"text": "Crée une constante dans le composant", "is_correct": False},
                    {"text": "Importe une référence depuis un autre composant", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre v-if et v-show?", "answers": [
                    {"text": "v-if supprime/ajoute le DOM, v-show change seulement display:none", "is_correct": True},
                    {"text": "v-show est plus lent que v-if", "is_correct": False},
                    {"text": "v-if est pour les listes, v-show pour les éléments seuls", "is_correct": False},
                    {"text": "Aucune différence visuelle ou de performance", "is_correct": False}
                ]},
                {"text": "Comment passer des données à un composant enfant Vue.js?", "answers": [
                    {"text": "Via les props définies avec defineProps()", "is_correct": True},
                    {"text": "Via des variables globales", "is_correct": False},
                    {"text": "Via v-data sur le composant enfant", "is_correct": False},
                    {"text": "Via emit vers l'enfant", "is_correct": False}
                ]},
                {"text": "Comment émettre un événement depuis un composant enfant Vue.js?", "answers": [
                    {"text": "Avec emit() de defineEmits() ou this.$emit()", "is_correct": True},
                    {"text": "Avec v-emit sur l'élément", "is_correct": False},
                    {"text": "Avec dispatch() comme Redux", "is_correct": False},
                    {"text": "Avec trigger() sur le parent", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Vue.js - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que computed() dans Vue.js?", "answers": [
                    {"text": "Une valeur dérivée d'autres données réactives, mise en cache et recalculée seulement si les dépendances changent", "is_correct": True},
                    {"text": "Une méthode calculée à chaque rendu", "is_correct": False},
                    {"text": "Une propriété qui calcule une valeur une seule fois", "is_correct": False},
                    {"text": "Une fonction de traitement des événements", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que watch() dans Vue.js?", "answers": [
                    {"text": "Observe un(e) source/expression réactive et exécute un callback quand elle change", "is_correct": True},
                    {"text": "Surveille les performances du composant", "is_correct": False},
                    {"text": "Observe les événements DOM", "is_correct": False},
                    {"text": "Déclenche un re-render forcé", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que reactive() dans Vue.js?", "answers": [
                    {"text": "Crée un objet réactif (proxy) - pour les objets complexes, contrairement à ref() pour les primitives", "is_correct": True},
                    {"text": "Rend un composant réactif aux props", "is_correct": False},
                    {"text": "Un alias de ref() pour les objets", "is_correct": False},
                    {"text": "Crée un store Pinia local", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Pinia?", "answers": [
                    {"text": "Le gestionnaire d'état officiel de Vue.js (successeur de Vuex)", "is_correct": True},
                    {"text": "Un framework de tests pour Vue.js", "is_correct": False},
                    {"text": "Un router pour Vue.js", "is_correct": False},
                    {"text": "Une bibliothèque de composants UI", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un slot Vue.js?", "answers": [
                    {"text": "Un espace dans un composant où le parent peut injecter du contenu HTML/template", "is_correct": True},
                    {"text": "Un emplacement mémoire pour les données réactives", "is_correct": False},
                    {"text": "Une position dans la grille CSS", "is_correct": False},
                    {"text": "Un placeholder pour les images", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que provide/inject en Vue.js?", "answers": [
                    {"text": "Passer des données d'un ancêtre à des descendants sans prop drilling", "is_correct": True},
                    {"text": "Injecter des dépendances comme en NestJS", "is_correct": False},
                    {"text": "Fournir des plugins à l'application Vue", "is_correct": False},
                    {"text": "Injecter du CSS dans un composant", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les lifecycle hooks Vue.js?", "answers": [
                    {"text": "Des fonctions appelées aux différentes étapes du cycle de vie d'un composant (onMounted, onUnmounted...)", "is_correct": True},
                    {"text": "Des hooks pour les événements DOM", "is_correct": False},
                    {"text": "Des watchers automatiques sur les props", "is_correct": False},
                    {"text": "Des plugins d'extension du cycle de rendu", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Vue Router?", "answers": [
                    {"text": "Le routeur officiel de Vue.js pour créer des SPAs avec navigation entre vues", "is_correct": True},
                    {"text": "Un outil de navigation dans les tableaux Vue", "is_correct": False},
                    {"text": "Un gestionnaire de requêtes HTTP", "is_correct": False},
                    {"text": "Un plugin de navigation pour applications mobile", "is_correct": False}
                ]},
                {"text": "Comment créer un composant réutilisable sans markup avec la Composition API?", "answers": [
                    {"text": "Un composable : une fonction use*() qui retourne de la logique réactive", "is_correct": True},
                    {"text": "Un mixin Vue.js", "is_correct": False},
                    {"text": "Un composant sans template", "is_correct": False},
                    {"text": "Un plugin Vue.js", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Teleport dans Vue.js?", "answers": [
                    {"text": "Rend le contenu d'un composant dans une autre partie du DOM (ex: modals)", "is_correct": True},
                    {"text": "Transfert des props entre composants distants", "is_correct": False},
                    {"text": "Charge un composant de façon asynchrone", "is_correct": False},
                    {"text": "Téléporte un composant vers un autre route", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Vue.js - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que Nuxt.js et son rapport avec Vue.js?", "answers": [
                    {"text": "Un meta-framework Vue.js offrant SSR, SSG, routing automatique et optimisations", "is_correct": True},
                    {"text": "Un framework de tests pour Vue.js", "is_correct": False},
                    {"text": "Une version améliorée de Vue.js", "is_correct": False},
                    {"text": "Un gestionnaire de paquets Vue", "is_correct": False}
                ]},
                {"text": "Comment optimiser une liste longue en Vue.js?", "answers": [
                    {"text": "Avec la virtualisation (vue-virtual-scroller) ou en utilisant :key correctement", "is_correct": True},
                    {"text": "En utilisant v-once sur la liste", "is_correct": False},
                    {"text": "En divisant la liste en plusieurs composants", "is_correct": False},
                    {"text": "Vue optimise automatiquement toutes les listes", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Vapor Mode dans Vue 3?", "answers": [
                    {"text": "Un mode de compilation sans Virtual DOM qui génère du code impératif direct pour de meilleures performances", "is_correct": True},
                    {"text": "Un mode de rendu SSR haute performance", "is_correct": False},
                    {"text": "Un mode pour les applications temps réel", "is_correct": False},
                    {"text": "Un mode de compilation pour WebAssembly", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Render Functions en Vue.js?", "answers": [
                    {"text": "Des fonctions JavaScript qui retournent des VNodes directement, alternative au template", "is_correct": True},
                    {"text": "Des fonctions de rendu côté serveur", "is_correct": False},
                    {"text": "Des hooks de cycle de vie pour le rendu", "is_correct": False},
                    {"text": "Des fonctions pour optimiser le re-render", "is_correct": False}
                ]},
                {"text": "Comment implémenter un plugin Vue.js?", "answers": [
                    {"text": "Un objet ou fonction avec une méthode install(app) reçevant l'instance app de Vue", "is_correct": True},
                    {"text": "En étendant la classe Vue directement", "is_correct": False},
                    {"text": "Avec Vue.use() et un objet de configuration", "is_correct": False},
                    {"text": "En ajoutant des composants globaux via app.component()", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que watchEffect() vs watch()?", "answers": [
                    {"text": "watchEffect s'exécute immédiatement et détecte automatiquement les dépendances; watch observe explicitement", "is_correct": True},
                    {"text": "watchEffect est plus performant dans tous les cas", "is_correct": False},
                    {"text": "watch peut observer plusieurs sources, watchEffect non", "is_correct": False},
                    {"text": "watchEffect remplace complètement watch() en Vue 3", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que defineCustomElement() en Vue.js?", "answers": [
                    {"text": "Convertit un composant Vue en Web Component natif utilisable sans Vue", "is_correct": True},
                    {"text": "Crée un élément HTML personnalisé dans le template", "is_correct": False},
                    {"text": "Définit des attributs personnalisés sur un composant", "is_correct": False},
                    {"text": "Enregistre un composant globalement dans l'app", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que shallowRef() vs ref() en Vue.js?", "answers": [
                    {"text": "shallowRef ne rend réactif que la valeur de surface (pas les propriétés imbriquées)", "is_correct": True},
                    {"text": "shallowRef est une ref sans tracking de dépendances", "is_correct": False},
                    {"text": "shallowRef est pour les types primitifs uniquement", "is_correct": False},
                    {"text": "shallowRef crée une copie superficielle de l'objet", "is_correct": False}
                ]},
                {"text": "Comment tester un composant Vue.js?", "answers": [
                    {"text": "Avec Vue Test Utils (mount/shallowMount) et Jest ou Vitest", "is_correct": True},
                    {"text": "Avec le module de test intégré de Vue", "is_correct": False},
                    {"text": "Uniquement avec Cypress pour les tests E2E", "is_correct": False},
                    {"text": "Avec @testing-library/vue et React Testing Library", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que l'algorithme de diff du Virtual DOM Vue.js?", "answers": [
                    {"text": "Comparaison O(n) par niveau avec heuristiques pour minimiser les opérations DOM réelles", "is_correct": True},
                    {"text": "Un algorithme O(n²) comparant chaque nœud avec tous les autres", "is_correct": False},
                    {"text": "Un diff basé sur les sélecteurs CSS", "is_correct": False},
                    {"text": "Vue 3 n'utilise plus de Virtual DOM", "is_correct": False}
                ]},
            ],
        },
    },
}

ANGULAR_DATA = {
    "category": {
        "name": "Angular",
        "description": "Quiz pour maîtriser Angular et le développement frontend TypeScript",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/angularjs/angularjs-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Angular - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Quel langage Angular utilise-t-il principalement?", "answers": [
                    {"text": "TypeScript", "is_correct": True},
                    {"text": "JavaScript", "is_correct": False},
                    {"text": "Dart", "is_correct": False},
                    {"text": "CoffeeScript", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Component Angular?", "answers": [
                    {"text": "L'unité de base de l'UI Angular avec template, styles et logique", "is_correct": True},
                    {"text": "Un service Angular partagé", "is_correct": False},
                    {"text": "Un module Angular", "is_correct": False},
                    {"text": "Une directive Angular", "is_correct": False}
                ]},
                {"text": "Quel décorateur marque une classe comme composant Angular?", "answers": [
                    {"text": "@Component({})", "is_correct": True},
                    {"text": "@View({})", "is_correct": False},
                    {"text": "@NgComponent({})", "is_correct": False},
                    {"text": "@Widget({})", "is_correct": False}
                ]},
                {"text": "Quelle commande crée un nouveau projet Angular?", "answers": [
                    {"text": "ng new mon-projet", "is_correct": True},
                    {"text": "angular new mon-projet", "is_correct": False},
                    {"text": "ng create mon-projet", "is_correct": False},
                    {"text": "ng init mon-projet", "is_correct": False}
                ]},
                {"text": "Comment binder une propriété dans un template Angular?", "answers": [
                    {"text": "[propriete]=\"valeur\"", "is_correct": True},
                    {"text": "{{propriete}}=\"valeur\"", "is_correct": False},
                    {"text": "*propriete=\"valeur\"", "is_correct": False},
                    {"text": "(propriete)=\"valeur\"", "is_correct": False}
                ]},
                {"text": "Comment gérer les événements dans un template Angular?", "answers": [
                    {"text": "(click)=\"maMethode()\"", "is_correct": True},
                    {"text": "[click]=\"maMethode()\"", "is_correct": False},
                    {"text": "v-click=\"maMethode()\"", "is_correct": False},
                    {"text": "on-click=\"maMethode()\"", "is_correct": False}
                ]},
                {"text": "Quelle directive Angular boucle sur une liste?", "answers": [
                    {"text": "*ngFor=\"let item of items\"", "is_correct": True},
                    {"text": "*ngRepeat=\"let item of items\"", "is_correct": False},
                    {"text": "[ngFor]=\"items\"", "is_correct": False},
                    {"text": "*ngEach=\"item in items\"", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Service Angular?", "answers": [
                    {"text": "Une classe injectable qui partage de la logique et des données entre composants", "is_correct": True},
                    {"text": "Un endpoint API appelé par Angular", "is_correct": False},
                    {"text": "Un composant sans template", "is_correct": False},
                    {"text": "Un module de configuration", "is_correct": False}
                ]},
                {"text": "Comment lancer l'application Angular en développement?", "answers": [
                    {"text": "ng serve", "is_correct": True},
                    {"text": "ng start", "is_correct": False},
                    {"text": "ng run", "is_correct": False},
                    {"text": "ng dev", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Two-way data binding dans Angular?", "answers": [
                    {"text": "[(ngModel)] - synchronise le template et le composant dans les deux sens", "is_correct": True},
                    {"text": "[model] + (modelChange) séparément", "is_correct": False},
                    {"text": "{{variable}} dans le template", "is_correct": False},
                    {"text": "*ngBind=\"variable\"", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Angular - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que l'injection de dépendances dans Angular?", "answers": [
                    {"text": "Un pattern où Angular injecte automatiquement les services déclarés dans le constructeur", "is_correct": True},
                    {"text": "L'importation de modules externes dans Angular", "is_correct": False},
                    {"text": "Le chargement de données depuis une API", "is_correct": False},
                    {"text": "La configuration des providers dans app.module.ts", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que RxJS et les Observables dans Angular?", "answers": [
                    {"text": "Une bibliothèque de programmation réactive avec des flux de données asynchrones composables", "is_correct": True},
                    {"text": "Une bibliothèque de gestion d'état Angular", "is_correct": False},
                    {"text": "Un système de routing réactif", "is_correct": False},
                    {"text": "Un framework de tests Angular", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Guards Angular?", "answers": [
                    {"text": "Des services qui contrôlent l'accès aux routes (CanActivate, CanDeactivate, CanLoad)", "is_correct": True},
                    {"text": "Des composants qui protègent les données sensibles", "is_correct": False},
                    {"text": "Des directives de validation de formulaires", "is_correct": False},
                    {"text": "Des middleware HTTP Angular", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les HTTP Interceptors dans Angular?", "answers": [
                    {"text": "Des services qui interceptent les requêtes/réponses HTTP pour ajouter auth, logging, etc.", "is_correct": True},
                    {"text": "Des composants qui bloquent certaines requêtes HTTP", "is_correct": False},
                    {"text": "Des guards pour les appels API", "is_correct": False},
                    {"text": "Des middlewares entre Angular et le backend", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre Subject et BehaviorSubject dans RxJS?", "answers": [
                    {"text": "BehaviorSubject a une valeur initiale et rejoue la dernière valeur aux nouveaux abonnés; Subject non", "is_correct": True},
                    {"text": "Subject est plus performant que BehaviorSubject", "is_correct": False},
                    {"text": "BehaviorSubject est pour les événements, Subject pour les données", "is_correct": False},
                    {"text": "Aucune différence fonctionnelle", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Reactive Forms Angular?", "answers": [
                    {"text": "Des formulaires définis dans le composant TypeScript avec FormGroup, FormControl et validateurs", "is_correct": True},
                    {"text": "Des formulaires qui se mettent à jour en temps réel", "is_correct": False},
                    {"text": "Des formulaires avec double binding [(ngModel)]", "is_correct": False},
                    {"text": "Des formulaires basés sur les Observables uniquement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Lazy Loading dans Angular?", "answers": [
                    {"text": "Charger des modules Angular à la demande (lors de la navigation) pour réduire le bundle initial", "is_correct": True},
                    {"text": "Charger les images de façon asynchrone", "is_correct": False},
                    {"text": "Retarder l'initialisation des services", "is_correct": False},
                    {"text": "Charger les composants progressivement avec Intersection Observer", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que NgRx?", "answers": [
                    {"text": "Une bibliothèque de gestion d'état Angular basée sur Redux/RxJS avec Store, Actions, Reducers, Effects", "is_correct": True},
                    {"text": "Un framework de tests Angular", "is_correct": False},
                    {"text": "Un système de routing avancé", "is_correct": False},
                    {"text": "Un ORM Angular pour la DB", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Change Detection dans Angular?", "answers": [
                    {"text": "Le mécanisme qui détecte les changements dans les composants et met à jour le DOM", "is_correct": True},
                    {"text": "Un outil de debugging des changements de state", "is_correct": False},
                    {"text": "Un système de versioning de composants", "is_correct": False},
                    {"text": "Une détection des changements de route", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que ChangeDetectionStrategy.OnPush?", "answers": [
                    {"text": "Le composant ne se met à jour que si ses inputs changent, un Observable émet ou CD est déclenché manuellement", "is_correct": True},
                    {"text": "Le composant pousse les changements vers ses enfants automatiquement", "is_correct": False},
                    {"text": "Un CD qui vérifie uniquement sur les events utilisateur", "is_correct": False},
                    {"text": "Un mode qui désactive le CD pour les performances", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Angular - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que les Angular Signals?", "answers": [
                    {"text": "Un nouveau système de réactivité fine-grained (Angular 16+) pour remplacer ou compléter RxJS/Zone.js", "is_correct": True},
                    {"text": "Des événements personnalisés Angular", "is_correct": False},
                    {"text": "Des websocket signals Angular", "is_correct": False},
                    {"text": "Des signaux de changement de route", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Zone.js dans Angular?", "answers": [
                    {"text": "Une bibliothèque qui patche les APIs async pour notifier Angular quand déclencher la détection de changements", "is_correct": True},
                    {"text": "Un système de gestion des zones de l'application (headers, footers)", "is_correct": False},
                    {"text": "Un outil de gestion des fuseaux horaires", "is_correct": False},
                    {"text": "Un système d'isolation des composants", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le standalone component Angular (v14+)?", "answers": [
                    {"text": "Un composant qui n'appartient à aucun NgModule, important directement ses dépendances", "is_correct": True},
                    {"text": "Un composant qui s'initialise sans dépendances", "is_correct": False},
                    {"text": "Un composant qui fonctionne sans Angular CLI", "is_correct": False},
                    {"text": "Un web component autonome généré par Angular", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Server-Side Rendering avec Angular Universal?", "answers": [
                    {"text": "Rend l'application Angular côté serveur pour améliorer le SEO et le temps de premier affichage", "is_correct": True},
                    {"text": "Exécute Angular sur le serveur sans navigateur", "is_correct": False},
                    {"text": "Génère un site statique depuis Angular", "is_correct": False},
                    {"text": "Un mode de développement sans navigateur", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Content Projection dans Angular?", "answers": [
                    {"text": "Projeter du contenu HTML parent dans un composant enfant via <ng-content>", "is_correct": True},
                    {"text": "Projeter un composant dans la page principale", "is_correct": False},
                    {"text": "Charger du contenu depuis une API", "is_correct": False},
                    {"text": "Afficher des données projetées depuis le store", "is_correct": False}
                ]},
                {"text": "Comment optimiser les performances Angular avec trackBy?", "answers": [
                    {"text": "trackBy dans *ngFor fournit une fonction d'identité pour éviter de recréer les DOM nodes à chaque changement", "is_correct": True},
                    {"text": "trackBy trace les performances des composants", "is_correct": False},
                    {"text": "trackBy met en cache les résultats des pipes", "is_correct": False},
                    {"text": "trackBy optimise les appels HTTP", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Angular Elements?", "answers": [
                    {"text": "Des composants Angular empaquetés en Web Components standard utilisables hors Angular", "is_correct": True},
                    {"text": "Des éléments HTML personnalisés Angular", "is_correct": False},
                    {"text": "Des directives d'éléments de formulaire", "is_correct": False},
                    {"text": "Des composants partagés entre micro-frontends", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Effects dans Angular Signals?", "answers": [
                    {"text": "Des effets de bord qui s'exécutent automatiquement quand leurs signals dépendants changent", "is_correct": True},
                    {"text": "Les NgRx Effects portés sur les Signals", "is_correct": False},
                    {"text": "Des side effects CSS animés", "is_correct": False},
                    {"text": "Des hooks de cycle de vie basés sur les Signals", "is_correct": False}
                ]},
                {"text": "Comment implémenter un custom structural directive Angular?", "answers": [
                    {"text": "Avec @Directive, TemplateRef et ViewContainerRef pour manipuler le DOM conditionnellement", "is_correct": True},
                    {"text": "En étendant NgIf avec une logique personnalisée", "is_correct": False},
                    {"text": "Avec @StructuralDirective decorator", "is_correct": False},
                    {"text": "En créant un composant avec <ng-template>", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Deferrable Views (@defer) dans Angular 17?", "answers": [
                    {"text": "Un mécanisme de lazy loading déclaratif dans les templates avec conditions de chargement (@placeholder, @loading)", "is_correct": True},
                    {"text": "Un système de chargement différé des styles", "is_correct": False},
                    {"text": "Des vues qui se chargent après interaction utilisateur uniquement", "is_correct": False},
                    {"text": "Un système de pagination des composants", "is_correct": False}
                ]},
            ],
        },
    },
}

# 3. FRAMEWORKS WEB BACKEND
# -----------------------------------------------------------------------------

NESTJS_DATA = {
    "category": {
        "name": "NestJS",
        "description": "Quiz pour maîtriser NestJS et le développement backend Node.js",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nestjs/nestjs-plain.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "NestJS - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Sur quel runtime NestJS s'exécute-t-il?", "answers": [
                    {"text": "Node.js", "is_correct": True},
                    {"text": "Deno", "is_correct": False},
                    {"text": "Bun", "is_correct": False},
                    {"text": "PHP", "is_correct": False}
                ]},
                {"text": "Quel décorateur marque une classe comme contrôleur NestJS?", "answers": [
                    {"text": "@Controller()", "is_correct": True},
                    {"text": "@Route()", "is_correct": False},
                    {"text": "@Handler()", "is_correct": False},
                    {"text": "@Endpoint()", "is_correct": False}
                ]},
                {"text": "Quel décorateur NestJS définit un service injectable?", "answers": [
                    {"text": "@Injectable()", "is_correct": True},
                    {"text": "@Service()", "is_correct": False},
                    {"text": "@Provider()", "is_correct": False},
                    {"text": "@Singleton()", "is_correct": False}
                ]},
                {"text": "Comment déclarer une route GET dans un contrôleur NestJS?", "answers": [
                    {"text": "@Get('chemin')", "is_correct": True},
                    {"text": "@Route.get('chemin')", "is_correct": False},
                    {"text": "@Http.Get('chemin')", "is_correct": False},
                    {"text": "@GetMapping('chemin')", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Module en NestJS?", "answers": [
                    {"text": "Une classe annotée @Module() qui organise les composants de l'application", "is_correct": True},
                    {"text": "Un fichier de configuration", "is_correct": False},
                    {"text": "Un middleware", "is_correct": False},
                    {"text": "Un service partagé", "is_correct": False}
                ]},
                {"text": "Comment récupérer un paramètre d'URL dans NestJS?", "answers": [
                    {"text": "@Param('id') id: string", "is_correct": True},
                    {"text": "@UrlParam('id') id: string", "is_correct": False},
                    {"text": "req.params.id", "is_correct": False},
                    {"text": "@PathVariable('id') id: string", "is_correct": False}
                ]},
                {"text": "Quelle commande crée un nouveau projet NestJS?", "answers": [
                    {"text": "nest new nom-projet", "is_correct": True},
                    {"text": "nestjs create nom-projet", "is_correct": False},
                    {"text": "npx create-nest-app nom-projet", "is_correct": False},
                    {"text": "nest init nom-projet", "is_correct": False}
                ]},
                {"text": "Comment accéder au body d'une requête POST dans NestJS?", "answers": [
                    {"text": "@Body() body: CreateDto", "is_correct": True},
                    {"text": "@Request() req - puis req.body", "is_correct": False},
                    {"text": "@Payload() payload: CreateDto", "is_correct": False},
                    {"text": "@Data() data: CreateDto", "is_correct": False}
                ]},
                {"text": "Quel décorateur NestJS définit une route DELETE?", "answers": [
                    {"text": "@Delete(':id')", "is_correct": True},
                    {"text": "@Remove(':id')", "is_correct": False},
                    {"text": "@Http.Delete(':id')", "is_correct": False},
                    {"text": "@Destroy(':id')", "is_correct": False}
                ]},
                {"text": "Comment injecter un service dans un contrôleur NestJS?", "answers": [
                    {"text": "constructor(private readonly monService: MonService) {}", "is_correct": True},
                    {"text": "@Inject() monService: MonService", "is_correct": False},
                    {"text": "this.monService = new MonService()", "is_correct": False},
                    {"text": "useService(MonService)", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "NestJS - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce qu'un Guard en NestJS?", "answers": [
                    {"text": "Un composant qui détermine si une requête peut accéder à une route (autorisation)", "is_correct": True},
                    {"text": "Un middleware de validation des données", "is_correct": False},
                    {"text": "Un intercepteur pour transformer les réponses", "is_correct": False},
                    {"text": "Un filtre pour gérer les exceptions", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Pipe en NestJS?", "answers": [
                    {"text": "Un composant pour transformer et/ou valider les données entrantes", "is_correct": True},
                    {"text": "Un outil pour connecter deux services", "is_correct": False},
                    {"text": "Un middleware de logging", "is_correct": False},
                    {"text": "Un décorateur pour les propriétés de classe", "is_correct": False}
                ]},
                {"text": "Comment utiliser la validation DTO avec class-validator dans NestJS?", "answers": [
                    {"text": "En combinant @Body() avec ValidationPipe et des décorateurs comme @IsString()", "is_correct": True},
                    {"text": "En utilisant @Validate() sur le DTO", "is_correct": False},
                    {"text": "En appelant validate(dto) manuellement dans le contrôleur", "is_correct": False},
                    {"text": "En configurant validateSchema dans le module", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Interceptor en NestJS?", "answers": [
                    {"text": "Un composant qui intercepte les requêtes/réponses pour transformer, logger ou étendre le comportement", "is_correct": True},
                    {"text": "Un outil pour intercepter les erreurs HTTP uniquement", "is_correct": False},
                    {"text": "Un composant qui bloque certaines requêtes", "is_correct": False},
                    {"text": "Un middleware de compression des réponses", "is_correct": False}
                ]},
                {"text": "Comment créer un module NestJS avec la CLI?", "answers": [
                    {"text": "nest generate module nom", "is_correct": True},
                    {"text": "nest create module nom", "is_correct": False},
                    {"text": "nest add module nom", "is_correct": False},
                    {"text": "nestjs module create nom", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Exception Filter en NestJS?", "answers": [
                    {"text": "Un composant qui capture les exceptions et renvoie des réponses d'erreur appropriées", "is_correct": True},
                    {"text": "Un filtre pour bloquer certaines exceptions au niveau réseau", "is_correct": False},
                    {"text": "Un système de logging des erreurs uniquement", "is_correct": False},
                    {"text": "Un middleware qui catch les erreurs asynchrones", "is_correct": False}
                ]},
                {"text": "Comment configurer TypeORM dans un module NestJS?", "answers": [
                    {"text": "TypeOrmModule.forRoot(config) dans AppModule", "is_correct": True},
                    {"text": "OrmModule.register(config) dans AppModule", "is_correct": False},
                    {"text": "DatabaseModule.connect(config) dans AppModule", "is_correct": False},
                    {"text": "TypeORM.initialize(config) dans main.ts", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le scope d'un provider dans NestJS?", "answers": [
                    {"text": "La durée de vie du provider : DEFAULT (singleton), REQUEST ou TRANSIENT", "is_correct": True},
                    {"text": "La portée des imports autorisés dans le module", "is_correct": False},
                    {"text": "Le niveau d'accès (public/privé) du provider", "is_correct": False},
                    {"text": "La zone du code où le provider peut être injecté", "is_correct": False}
                ]},
                {"text": "Comment implémenter une authentification JWT avec NestJS?", "answers": [
                    {"text": "En utilisant @nestjs/jwt et @nestjs/passport avec JwtStrategy", "is_correct": True},
                    {"text": "En ajoutant le middleware jwt dans main.ts", "is_correct": False},
                    {"text": "En utilisant le décorateur @Authenticate() sur les routes", "is_correct": False},
                    {"text": "En configurant SecurityModule dans AppModule", "is_correct": False}
                ]},
                {"text": "Comment récupérer les query params dans NestJS?", "answers": [
                    {"text": "@Query('page') page: number", "is_correct": True},
                    {"text": "@QueryParam('page') page: number", "is_correct": False},
                    {"text": "@Search('page') page: number", "is_correct": False},
                    {"text": "req.query.page", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "NestJS - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que le système de microservices dans NestJS?", "answers": [
                    {"text": "Un ensemble de transports (TCP, Redis, NATS...) pour communication inter-services", "is_correct": True},
                    {"text": "Une architecture pour diviser le code en micro-modules", "is_correct": False},
                    {"text": "Un outil de déploiement automatique", "is_correct": False},
                    {"text": "Un système de monitoring des performances", "is_correct": False}
                ]},
                {"text": "Comment utiliser les CQRS dans NestJS?", "answers": [
                    {"text": "Avec @nestjs/cqrs via CommandBus, QueryBus, et les handlers correspondants", "is_correct": True},
                    {"text": "En séparant manuellement les contrôleurs en Command et Query", "is_correct": False},
                    {"text": "En utilisant le module @nestjs/command", "is_correct": False},
                    {"text": "En configurant deux bases de données séparées", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Dynamic Module en NestJS?", "answers": [
                    {"text": "Un module configurable via forRoot()/forFeature() qui retourne ses propres providers dynamiquement", "is_correct": True},
                    {"text": "Un module chargé à la demande (lazy loading)", "is_correct": False},
                    {"text": "Un module créé à l'exécution depuis une configuration externe", "is_correct": False},
                    {"text": "Un module qui change de comportement selon l'environnement", "is_correct": False}
                ]},
                {"text": "Comment implémenter un Custom Decorator dans NestJS?", "answers": [
                    {"text": "createParamDecorator((data, ctx) => ctx.switchToHttp().getRequest())", "is_correct": True},
                    {"text": "function MyDecorator(target, key, descriptor) { return descriptor; }", "is_correct": False},
                    {"text": "Nest.decorator((req) => req.user)", "is_correct": False},
                    {"text": "@CustomParam() dans le contrôleur directement", "is_correct": False}
                ]},
                {"text": "Que fait @nestjs/schedule et comment planifier une tâche?", "answers": [
                    {"text": "Gère les tâches planifiées via des décorateurs comme @Cron(), @Interval(), @Timeout()", "is_correct": True},
                    {"text": "Planifie des requêtes HTTP différées", "is_correct": False},
                    {"text": "Gère le scheduling des workers de microservices", "is_correct": False},
                    {"text": "Crée une queue de tâches asynchrones", "is_correct": False}
                ]},
                {"text": "Comment utiliser les Queues avec Bull dans NestJS?", "answers": [
                    {"text": "Avec @nestjs/bull, BullModule.registerQueue() et les décorateurs @Processor/@Process", "is_correct": True},
                    {"text": "En utilisant QueueModule.create() et les JobHandlers", "is_correct": False},
                    {"text": "En configurant Redis directement et en utilisant des Subscribers", "is_correct": False},
                    {"text": "Avec @nestjs/queue et le décorateur @QueueWorker", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que l'Execution Context dans NestJS?", "answers": [
                    {"text": "Un wrapper qui donne accès à la requête actuelle quel que soit le transport (HTTP, WS, RPC)", "is_correct": True},
                    {"text": "Le contexte d'exécution du moteur JavaScript", "is_correct": False},
                    {"text": "L'environnement dans lequel NestJS s'exécute", "is_correct": False},
                    {"text": "Le scope d'un interceptor appliqué globalement", "is_correct": False}
                ]},
                {"text": "Comment implémenter des WebSockets avec NestJS?", "answers": [
                    {"text": "Avec @WebSocketGateway() et les décorateurs @SubscribeMessage(), @WebSocketServer()", "is_correct": True},
                    {"text": "En utilisant SocketController() avec des @OnMessage() handlers", "is_correct": False},
                    {"text": "En configurant ws dans le AppModule directement", "is_correct": False},
                    {"text": "En utilisant @nestjs/realtime et RealtimeModule", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que la Circular Dependency et comment la résoudre dans NestJS?", "answers": [
                    {"text": "Deux modules/services qui se référencent mutuellement - résolu avec forwardRef()", "is_correct": True},
                    {"text": "Un import circulaire de fichiers - résolu en restructurant les modules", "is_correct": False},
                    {"text": "Une dépendance qui se réinstancie elle-même - résolu avec un Singleton pattern", "is_correct": False},
                    {"text": "Un provider qui s'injecte lui-même - désactivé par NestJS automatiquement", "is_correct": False}
                ]},
                {"text": "Comment tester unitairement un service NestJS?", "answers": [
                    {"text": "Avec Test.createTestingModule(), en mockant les dépendances via providers", "is_correct": True},
                    {"text": "En instanciant directement le service avec new MonService()", "is_correct": False},
                    {"text": "En utilisant NestFactory.createTest() dans les specs", "is_correct": False},
                    {"text": "Avec jest.mock() sur le fichier du service entier", "is_correct": False}
                ]},
            ],
        },
    },
}

EXPRESSJS_DATA = {
    "category": {
        "name": "Express.js",
        "description": "Quiz pour maîtriser Express.js et le développement backend Node.js",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/express/express-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Express.js - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Sur quoi Express.js est-il basé?", "answers": [
                    {"text": "Node.js", "is_correct": True},
                    {"text": "Deno", "is_correct": False},
                    {"text": "Bun", "is_correct": False},
                    {"text": "PHP", "is_correct": False}
                ]},
                {"text": "Comment créer une route GET avec Express?", "answers": [
                    {"text": "app.get('/route', (req, res) => res.send('Hello'))", "is_correct": True},
                    {"text": "app.route('GET', '/route', handler)", "is_correct": False},
                    {"text": "@Get('/route') handler(req, res) {}", "is_correct": False},
                    {"text": "express.get('/route', handler)", "is_correct": False}
                ]},
                {"text": "Comment démarrer un serveur Express sur le port 3000?", "answers": [
                    {"text": "app.listen(3000, () => console.log('Serveur démarré'))", "is_correct": True},
                    {"text": "app.start(3000)", "is_correct": False},
                    {"text": "app.run(3000)", "is_correct": False},
                    {"text": "express.listen(3000)", "is_correct": False}
                ]},
                {"text": "Comment envoyer une réponse JSON avec Express?", "answers": [
                    {"text": "res.json({ message: 'Hello' })", "is_correct": True},
                    {"text": "res.send({ message: 'Hello' })", "is_correct": False},
                    {"text": "res.response.json({ message: 'Hello' })", "is_correct": False},
                    {"text": "return JSON({ message: 'Hello' })", "is_correct": False}
                ]},
                {"text": "Comment accéder aux paramètres d'URL dans Express?", "answers": [
                    {"text": "req.params.id (pour /route/:id)", "is_correct": True},
                    {"text": "req.url.params.id", "is_correct": False},
                    {"text": "req.path.id", "is_correct": False},
                    {"text": "params.id depuis le handler", "is_correct": False}
                ]},
                {"text": "Comment parser le body JSON d'une requête POST dans Express?", "answers": [
                    {"text": "app.use(express.json())", "is_correct": True},
                    {"text": "app.use(bodyParser())", "is_correct": False},
                    {"text": "req.json() dans chaque route", "is_correct": False},
                    {"text": "app.use(express.parseBody())", "is_correct": False}
                ]},
                {"text": "Comment créer un middleware dans Express?", "answers": [
                    {"text": "app.use((req, res, next) => { /* logique */ next(); })", "is_correct": True},
                    {"text": "app.middleware((req, res) => { /* logique */ })", "is_correct": False},
                    {"text": "express.use(handler)", "is_correct": False},
                    {"text": "@Middleware class MonMiddleware {}", "is_correct": False}
                ]},
                {"text": "Comment accéder aux query parameters dans Express?", "answers": [
                    {"text": "req.query.page (pour ?page=1)", "is_correct": True},
                    {"text": "req.params.page", "is_correct": False},
                    {"text": "req.search.page", "is_correct": False},
                    {"text": "req.url.query.page", "is_correct": False}
                ]},
                {"text": "Comment définir le code de statut HTTP de la réponse Express?", "answers": [
                    {"text": "res.status(201).json(data)", "is_correct": True},
                    {"text": "res.statusCode = 201; res.json(data)", "is_correct": False},
                    {"text": "res.json(data, 201)", "is_correct": False},
                    {"text": "res.send(201, data)", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Express Router?", "answers": [
                    {"text": "Un mini-app Express pour grouper et organiser des routes dans des fichiers séparés", "is_correct": True},
                    {"text": "Le système de routing principal d'Express", "is_correct": False},
                    {"text": "Un outil de navigation entre pages", "is_correct": False},
                    {"text": "Un load balancer pour les routes Express", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Express.js - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Comment gérer les erreurs globalement dans Express?", "answers": [
                    {"text": "app.use((err, req, res, next) => res.status(500).json({error: err.message})) - middleware à 4 paramètres", "is_correct": True},
                    {"text": "app.error((err, req, res) => {})", "is_correct": False},
                    {"text": "try/catch autour de app.listen()", "is_correct": False},
                    {"text": "process.on('uncaughtException', handler)", "is_correct": False}
                ]},
                {"text": "Comment implémenter CORS dans Express?", "answers": [
                    {"text": "app.use(cors()) avec le package cors", "is_correct": True},
                    {"text": "app.enableCors()", "is_correct": False},
                    {"text": "app.use(express.cors())", "is_correct": False},
                    {"text": "Configurer les headers manuellement dans chaque route", "is_correct": False}
                ]},
                {"text": "Comment sécuriser une application Express?", "answers": [
                    {"text": "Avec helmet pour les headers HTTP de sécurité, cors, rate-limiting et validation des inputs", "is_correct": True},
                    {"text": "En activant express.secure() dans la config", "is_correct": False},
                    {"text": "Express est sécurisé par défaut", "is_correct": False},
                    {"text": "Avec le middleware express-shield uniquement", "is_correct": False}
                ]},
                {"text": "Comment structurer une grande application Express?", "answers": [
                    {"text": "Avec des Router modulaires, une séparation controllers/services/routes et une architecture en couches", "is_correct": True},
                    {"text": "Tout dans un seul fichier app.js pour la simplicité", "is_correct": False},
                    {"text": "En utilisant des namespaces Express", "is_correct": False},
                    {"text": "En créant une instance Express par module", "is_correct": False}
                ]},
                {"text": "Comment gérer les fichiers uploadés avec Express?", "answers": [
                    {"text": "Avec multer comme middleware de gestion des multipart/form-data", "is_correct": True},
                    {"text": "Avec express.upload()", "is_correct": False},
                    {"text": "En lisant le stream req directement", "is_correct": False},
                    {"text": "Avec le middleware busboy intégré à Express", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que app.set() dans Express?", "answers": [
                    {"text": "Configure des paramètres de l'application (view engine, port, env...)", "is_correct": True},
                    {"text": "Définit des variables globales", "is_correct": False},
                    {"text": "Configure des middlewares globaux", "is_correct": False},
                    {"text": "Définit les headers par défaut", "is_correct": False}
                ]},
                {"text": "Comment implémenter le rate limiting dans Express?", "answers": [
                    {"text": "Avec express-rate-limit comme middleware global ou par route", "is_correct": True},
                    {"text": "Avec app.rateLimit() intégré", "is_correct": False},
                    {"text": "Via nginx uniquement", "is_correct": False},
                    {"text": "Express gère le rate limiting nativement", "is_correct": False}
                ]},
                {"text": "Comment tester des routes Express avec Jest?", "answers": [
                    {"text": "Avec supertest pour faire des requêtes HTTP sur l'app Express sans vrai serveur", "is_correct": True},
                    {"text": "En démarrant l'app et faisant des appels fetch", "is_correct": False},
                    {"text": "Avec le module de test intégré d'Express", "is_correct": False},
                    {"text": "Avec Postman CLI uniquement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que express.static()?", "answers": [
                    {"text": "Un middleware qui sert des fichiers statiques (images, CSS, JS) depuis un dossier", "is_correct": True},
                    {"text": "Un déclarateur de variables statiques Express", "is_correct": False},
                    {"text": "Un générateur de pages HTML statiques", "is_correct": False},
                    {"text": "Un middleware pour les routes immuables", "is_correct": False}
                ]},
                {"text": "Comment valider les données d'entrée dans Express?", "answers": [
                    {"text": "Avec express-validator ou joi/zod dans un middleware de validation", "is_correct": True},
                    {"text": "Express valide automatiquement avec les types TypeScript", "is_correct": False},
                    {"text": "Avec app.validate() sur chaque route", "is_correct": False},
                    {"text": "Uniquement avec des vérifications if/else manuelles", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Express.js - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Quelle est la différence entre Express 4 et Express 5?", "answers": [
                    {"text": "Express 5 supporte nativement async/await avec propagation automatique des erreurs vers next()", "is_correct": True},
                    {"text": "Express 5 est réécrit en TypeScript", "is_correct": False},
                    {"text": "Express 5 abandonne le système de middleware", "is_correct": False},
                    {"text": "Express 5 intègre un ORM", "is_correct": False}
                ]},
                {"text": "Comment implémenter le clustering dans Node.js/Express?", "answers": [
                    {"text": "Avec le module cluster pour utiliser plusieurs processus sur les CPU disponibles", "is_correct": True},
                    {"text": "Avec express.cluster() nativement", "is_correct": False},
                    {"text": "Via Docker Swarm uniquement", "is_correct": False},
                    {"text": "Express gère automatiquement le multi-core", "is_correct": False}
                ]},
                {"text": "Comment implémenter du streaming SSE (Server-Sent Events) avec Express?", "answers": [
                    {"text": "res.setHeader('Content-Type', 'text/event-stream') et écrire avec res.write()", "is_correct": True},
                    {"text": "res.sse() intégré dans Express", "is_correct": False},
                    {"text": "Avec WebSockets simulés", "is_correct": False},
                    {"text": "Express ne supporte pas SSE", "is_correct": False}
                ]},
                {"text": "Comment optimiser les performances Express en production?", "answers": [
                    {"text": "Compression gzip, cache statique, clustering, reverse proxy nginx, NODE_ENV=production", "is_correct": True},
                    {"text": "Activer express.optimize(true)", "is_correct": False},
                    {"text": "Réduire le nombre de middlewares à zéro", "is_correct": False},
                    {"text": "Express est auto-optimisé en production", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un middleware d'agrégation d'erreurs dans Express?", "answers": [
                    {"text": "Un middleware final à 4 params (err, req, res, next) qui centralise la gestion de toutes les erreurs", "is_correct": True},
                    {"text": "Un middleware qui agrège plusieurs erreurs en une seule", "is_correct": False},
                    {"text": "Un try/catch global pour l'application", "is_correct": False},
                    {"text": "Un service de monitoring des erreurs", "is_correct": False}
                ]},
                {"text": "Comment implémenter WebSockets avec Express?", "answers": [
                    {"text": "Avec socket.io ou ws library en attachant au serveur HTTP sous-jacent", "is_correct": True},
                    {"text": "Avec express.ws() intégré", "is_correct": False},
                    {"text": "Express supporte les WebSockets nativement", "is_correct": False},
                    {"text": "Avec un serveur WebSocket séparé uniquement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que l'API de routing avancé d'Express (chainable routes)?", "answers": [
                    {"text": "app.route('/path').get(fn).post(fn).put(fn) - chaîner les handlers HTTP sur le même path", "is_correct": True},
                    {"text": "Chaîner les middlewares avec .pipe()", "is_correct": False},
                    {"text": "Créer des routes parentenfant enchaînées", "is_correct": False},
                    {"text": "Combiner plusieurs Router en un seul", "is_correct": False}
                ]},
                {"text": "Comment monitorer les performances d'une application Express?", "answers": [
                    {"text": "Avec des APM (New Relic, Datadog, prom-client pour Prometheus) ou des middleware de métriques", "is_correct": True},
                    {"text": "Avec express.monitor() natif", "is_correct": False},
                    {"text": "En lisant les logs Node.js uniquement", "is_correct": False},
                    {"text": "Express a un dashboard de monitoring intégré", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que graceful shutdown dans Express?", "answers": [
                    {"text": "Arrêter le serveur proprement en attendant la fin des requêtes en cours avant de s'éteindre", "is_correct": True},
                    {"text": "Éteindre Express sans perdre de données en DB", "is_correct": False},
                    {"text": "Redémarrer Express automatiquement en cas d'erreur", "is_correct": False},
                    {"text": "Fermer toutes les connexions WebSocket avant l'arrêt", "is_correct": False}
                ]},
                {"text": "Comment implémenter un middleware de logging avancé avec Express?", "answers": [
                    {"text": "Avec morgan pour le logging HTTP et winston/pino pour les logs applicatifs structurés", "is_correct": True},
                    {"text": "Express intègre morgan par défaut", "is_correct": False},
                    {"text": "Avec console.log() dans chaque route", "is_correct": False},
                    {"text": "Avec le décorateur @Log() sur les routes", "is_correct": False}
                ]},
            ],
        },
    },
}

DJANGO_DATA = {
    "category": {
        "name": "Django",
        "description": "Quiz pour maîtriser Django et le développement web Python full-stack",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Django - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Quel est le slogan de Django?", "answers": [
                    {"text": "The web framework for perfectionists with deadlines", "is_correct": True},
                    {"text": "Batteries included Python web framework", "is_correct": False},
                    {"text": "Fast, simple and scalable", "is_correct": False},
                    {"text": "The fullstack Python framework", "is_correct": False}
                ]},
                {"text": "Quelle commande crée un nouveau projet Django?", "answers": [
                    {"text": "django-admin startproject nom_projet", "is_correct": True},
                    {"text": "django new nom_projet", "is_correct": False},
                    {"text": "python django create nom_projet", "is_correct": False},
                    {"text": "manage.py startproject nom_projet", "is_correct": False}
                ]},
                {"text": "Quel fichier Django contient les URL patterns?", "answers": [
                    {"text": "urls.py", "is_correct": True},
                    {"text": "routes.py", "is_correct": False},
                    {"text": "paths.py", "is_correct": False},
                    {"text": "views.py", "is_correct": False}
                ]},
                {"text": "Quel design pattern Django utilise-t-il?", "answers": [
                    {"text": "MTV (Model-Template-View)", "is_correct": True},
                    {"text": "MVC (Model-View-Controller)", "is_correct": False},
                    {"text": "MVVM (Model-View-ViewModel)", "is_correct": False},
                    {"text": "MVP (Model-View-Presenter)", "is_correct": False}
                ]},
                {"text": "Comment créer une application dans un projet Django?", "answers": [
                    {"text": "python manage.py startapp nom_app", "is_correct": True},
                    {"text": "django-admin createapp nom_app", "is_correct": False},
                    {"text": "python manage.py createapp nom_app", "is_correct": False},
                    {"text": "django new-app nom_app", "is_correct": False}
                ]},
                {"text": "Quelle commande applique les migrations Django?", "answers": [
                    {"text": "python manage.py migrate", "is_correct": True},
                    {"text": "python manage.py db migrate", "is_correct": False},
                    {"text": "django migrate", "is_correct": False},
                    {"text": "python manage.py apply-migrations", "is_correct": False}
                ]},
                {"text": "Comment lancer le serveur de développement Django?", "answers": [
                    {"text": "python manage.py runserver", "is_correct": True},
                    {"text": "python manage.py serve", "is_correct": False},
                    {"text": "django start", "is_correct": False},
                    {"text": "python manage.py start", "is_correct": False}
                ]},
                {"text": "Quel ORM Django utilise-t-il par défaut?", "answers": [
                    {"text": "L'ORM Django intégré (Django ORM)", "is_correct": True},
                    {"text": "SQLAlchemy", "is_correct": False},
                    {"text": "Peewee", "is_correct": False},
                    {"text": "Tortoise ORM", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le fichier settings.py dans Django?", "answers": [
                    {"text": "Le fichier de configuration global du projet (DB, apps, middleware, etc.)", "is_correct": True},
                    {"text": "Le fichier de configuration des templates", "is_correct": False},
                    {"text": "Le fichier des paramètres de sécurité uniquement", "is_correct": False},
                    {"text": "Le fichier de configuration des modèles", "is_correct": False}
                ]},
                {"text": "Comment créer un superutilisateur Django?", "answers": [
                    {"text": "python manage.py createsuperuser", "is_correct": True},
                    {"text": "python manage.py createadmin", "is_correct": False},
                    {"text": "django-admin create-superuser", "is_correct": False},
                    {"text": "python manage.py adduser --admin", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Django - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que les Class-Based Views (CBV) dans Django?", "answers": [
                    {"text": "Des vues basées sur des classes Python avec héritage et mixins pour réutiliser la logique", "is_correct": True},
                    {"text": "Des vues générées automatiquement par l'ORM", "is_correct": False},
                    {"text": "Des vues pour les opérations CRUD uniquement", "is_correct": False},
                    {"text": "Des vues qui retournent des réponses JSON", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Django REST Framework (DRF)?", "answers": [
                    {"text": "Un framework puissant pour construire des API REST avec Django (serializers, viewsets, permissions)", "is_correct": True},
                    {"text": "La version Django pour les APIs REST natives", "is_correct": False},
                    {"text": "Un remplaçant de Django pour les APIs", "is_correct": False},
                    {"text": "Un outil de test d'API pour Django", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Serializer dans DRF?", "answers": [
                    {"text": "Convertit des instances de modèle en JSON et valide les données entrantes", "is_correct": True},
                    {"text": "Sérialise la session utilisateur", "is_correct": False},
                    {"text": "Compresse les réponses HTTP", "is_correct": False},
                    {"text": "Transforme les templates en HTML", "is_correct": False}
                ]},
                {"text": "Comment définir une relation ForeignKey dans Django?", "answers": [
                    {"text": "auteur = models.ForeignKey(User, on_delete=models.CASCADE)", "is_correct": True},
                    {"text": "auteur = models.RelatedField(User)", "is_correct": False},
                    {"text": "auteur = models.OneToManyField(User)", "is_correct": False},
                    {"text": "auteur = models.Reference(User)", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le système de signaux Django?", "answers": [
                    {"text": "Un mécanisme publisher/subscriber pour exécuter du code quand certains événements se produisent (pre_save, post_save...)", "is_correct": True},
                    {"text": "Un système de notifications push", "is_correct": False},
                    {"text": "Une API de gestion des logs Django", "is_correct": False},
                    {"text": "Un système de monitoring des vues", "is_correct": False}
                ]},
                {"text": "Comment sécuriser une vue Django contre le CSRF?", "answers": [
                    {"text": "Django le gère automatiquement avec le middleware CsrfViewMiddleware et le tag {% csrf_token %}", "is_correct": True},
                    {"text": "En ajoutant @csrf_secure sur chaque vue", "is_correct": False},
                    {"text": "En configurant CSRF_PROTECTION = True dans settings.py", "is_correct": False},
                    {"text": "En utilisant uniquement les méthodes POST", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les QuerySets Django?", "answers": [
                    {"text": "Des collections d'objets de la DB évalués paresseusement, chaînables et filtrables", "is_correct": True},
                    {"text": "Des requêtes SQL brutes encapsulées", "is_correct": False},
                    {"text": "Des vues de base de données Django", "is_correct": False},
                    {"text": "Des objets JSON retournés par les API views", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le cache dans Django?", "answers": [
                    {"text": "Un système de mise en cache multi-backend (memcached, redis, fichier) avec une API unifiée", "is_correct": True},
                    {"text": "Un cache de sessions utilisateur uniquement", "is_correct": False},
                    {"text": "Un cache de templates statiques", "is_correct": False},
                    {"text": "Un cache de QuerySets automatique", "is_correct": False}
                ]},
                {"text": "Comment gérer les fichiers uploadés dans Django?", "answers": [
                    {"text": "Via FileField/ImageField dans les modèles et MEDIA_ROOT/MEDIA_URL dans settings", "is_correct": True},
                    {"text": "En sauvegardant directement dans la DB en base64", "is_correct": False},
                    {"text": "Avec le middleware FileUploadMiddleware", "is_correct": False},
                    {"text": "En utilisant une S3 obligatoirement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Mixins dans Django?", "answers": [
                    {"text": "Des classes réutilisables qui ajoutent des fonctionnalités à des Class-Based Views par héritage multiple", "is_correct": True},
                    {"text": "Des fonctions décorées appliquées aux vues", "is_correct": False},
                    {"text": "Des middlewares légers pour les vues", "is_correct": False},
                    {"text": "Des helpers de template Django", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Django - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que Django Channels?", "answers": [
                    {"text": "Une extension Django pour gérer WebSockets, HTTP long-polling et autres protocoles async", "is_correct": True},
                    {"text": "Un système de channels de communication entre views", "is_correct": False},
                    {"text": "Un framework de microservices Django", "is_correct": False},
                    {"text": "Un outil de monitoring des connexions HTTP", "is_correct": False}
                ]},
                {"text": "Comment optimiser les queries Django avec select_related et prefetch_related?", "answers": [
                    {"text": "select_related pour ForeignKey/OneToOne (JOIN SQL), prefetch_related pour ManyToMany (2 requêtes)", "is_correct": True},
                    {"text": "select_related pour les relations inverse, prefetch_related pour les directes", "is_correct": False},
                    {"text": "Les deux font la même chose mais pour différents types de DB", "is_correct": False},
                    {"text": "prefetch_related charge en mémoire, select_related en cache Redis", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Database Transactions dans Django?", "answers": [
                    {"text": "Avec atomic() pour garantir qu'un groupe d'opérations DB réussit entièrement ou est rollback", "is_correct": True},
                    {"text": "Un système de réplication de base de données", "is_correct": False},
                    {"text": "Des transactions financières trackées dans Django", "is_correct": False},
                    {"text": "Un mécanisme de validation avant sauvegarde en DB", "is_correct": False}
                ]},
                {"text": "Comment personnaliser l'admin Django?", "answers": [
                    {"text": "En créant des classes ModelAdmin avec list_display, search_fields, actions personnalisées, etc.", "is_correct": True},
                    {"text": "En modifiant directement les templates de django.contrib.admin", "is_correct": False},
                    {"text": "En créant un nouveau module admin.py par application", "is_correct": False},
                    {"text": "L'admin Django ne peut pas être personnalisé", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Custom Management Commands Django?", "answers": [
                    {"text": "Des commandes manage.py personnalisées via management/commands/ma_commande.py avec BaseCommand", "is_correct": True},
                    {"text": "Des extensions de la CLI Django", "is_correct": False},
                    {"text": "Des commandes système Linux intégrées à Django", "is_correct": False},
                    {"text": "Des scripts Python lancés automatiquement au démarrage", "is_correct": False}
                ]},
                {"text": "Comment implémenter un backend d'authentification personnalisé?", "answers": [
                    {"text": "En créant une classe avec authenticate() et get_user() et l'ajoutant à AUTHENTICATION_BACKENDS", "is_correct": True},
                    {"text": "En surchargeant le modèle User uniquement", "is_correct": False},
                    {"text": "En ajoutant un middleware d'auth", "is_correct": False},
                    {"text": "Avec django-allauth uniquement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Annotate et Aggregate dans Django ORM?", "answers": [
                    {"text": "Annotate ajoute des champs calculés par objet; Aggregate calcule une valeur globale sur le QuerySet", "is_correct": True},
                    {"text": "Les deux font des agrégations SQL - Annotate est une alias d'Aggregate", "is_correct": False},
                    {"text": "Aggregate est pour les données numériques, Annotate pour les chaînes", "is_correct": False},
                    {"text": "Annotate filtre, Aggregate trie les résultats", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Content Type Framework Django?", "answers": [
                    {"text": "Un framework permettant des relations génériques vers n'importe quel modèle (GenericForeignKey)", "is_correct": True},
                    {"text": "Un système de gestion des types MIME", "is_correct": False},
                    {"text": "Un framework de validation des types de données", "is_correct": False},
                    {"text": "Un système de types pour les champs de modèle", "is_correct": False}
                ]},
                {"text": "Comment implémenter le multi-tenancy avec Django?", "answers": [
                    {"text": "Via django-tenant-schemas/django-tenants (schémas PostgreSQL) ou filtrage par tenant_id", "is_correct": True},
                    {"text": "Django supporte nativement le multi-tenancy", "is_correct": False},
                    {"text": "En créant une instance Django par client", "is_correct": False},
                    {"text": "Via les namespaces URL Django uniquement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Database Routers Django?", "answers": [
                    {"text": "Des classes qui décident quelle base de données utiliser pour chaque modèle (multi-DB)", "is_correct": True},
                    {"text": "Des load balancers pour les connexions DB", "is_correct": False},
                    {"text": "Des routers URL pour les API de base de données", "is_correct": False},
                    {"text": "Des caches de requêtes par base de données", "is_correct": False}
                ]},
            ],
        },
    },
}

LARAVEL_DATA = {
    "category": {
        "name": "Laravel",
        "description": "Quiz pour maîtriser Laravel et le développement web PHP élégant",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/laravel/laravel-plain.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Laravel - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Quel est le ORM de Laravel?", "answers": [
                    {"text": "Eloquent", "is_correct": True},
                    {"text": "Doctrine", "is_correct": False},
                    {"text": "Propel", "is_correct": False},
                    {"text": "Active Record", "is_correct": False}
                ]},
                {"text": "Quelle commande crée un contrôleur Laravel?", "answers": [
                    {"text": "php artisan make:controller NomController", "is_correct": True},
                    {"text": "php artisan create:controller NomController", "is_correct": False},
                    {"text": "laravel make controller NomController", "is_correct": False},
                    {"text": "artisan controller:make NomController", "is_correct": False}
                ]},
                {"text": "Quel moteur de templates Laravel utilise-t-il?", "answers": [
                    {"text": "Blade", "is_correct": True},
                    {"text": "Twig", "is_correct": False},
                    {"text": "Smarty", "is_correct": False},
                    {"text": "Mustache", "is_correct": False}
                ]},
                {"text": "Comment lancer le serveur de développement Laravel?", "answers": [
                    {"text": "php artisan serve", "is_correct": True},
                    {"text": "php artisan start", "is_correct": False},
                    {"text": "laravel serve", "is_correct": False},
                    {"text": "composer serve", "is_correct": False}
                ]},
                {"text": "Quelle commande crée une migration Laravel?", "answers": [
                    {"text": "php artisan make:migration create_users_table", "is_correct": True},
                    {"text": "php artisan migration:create create_users_table", "is_correct": False},
                    {"text": "php artisan db:migrate create_users_table", "is_correct": False},
                    {"text": "laravel migrate:new create_users_table", "is_correct": False}
                ]},
                {"text": "Quelle commande exécute les migrations Laravel?", "answers": [
                    {"text": "php artisan migrate", "is_correct": True},
                    {"text": "php artisan db:migrate", "is_correct": False},
                    {"text": "php artisan migration:run", "is_correct": False},
                    {"text": "laravel migrate", "is_correct": False}
                ]},
                {"text": "Quel fichier contient les routes web de Laravel?", "answers": [
                    {"text": "routes/web.php", "is_correct": True},
                    {"text": "app/routes.php", "is_correct": False},
                    {"text": "config/routes.php", "is_correct": False},
                    {"text": "routes/routes.php", "is_correct": False}
                ]},
                {"text": "Comment définir une route GET simple dans Laravel?", "answers": [
                    {"text": "Route::get('/chemin', [Controller::class, 'methode'])", "is_correct": True},
                    {"text": "@get('/chemin') function handler() {}", "is_correct": False},
                    {"text": "route('GET', '/chemin', handler)", "is_correct": False},
                    {"text": "Router::get('/chemin', 'Controller@methode')", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Seeders dans Laravel?", "answers": [
                    {"text": "Des classes pour peupler la base de données avec des données de test", "is_correct": True},
                    {"text": "Des scripts de migration automatiques", "is_correct": False},
                    {"text": "Des outils de génération de code", "is_correct": False},
                    {"text": "Des fichiers de configuration DB", "is_correct": False}
                ]},
                {"text": "Comment accéder à la variable d'environnement APP_KEY?", "answers": [
                    {"text": "env('APP_KEY') ou config('app.key')", "is_correct": True},
                    {"text": "$_ENV['APP_KEY']", "is_correct": False},
                    {"text": "getenv('APP_KEY')", "is_correct": False},
                    {"text": "Env::get('APP_KEY')", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Laravel - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que les Middleware dans Laravel?", "answers": [
                    {"text": "Des filtres qui interceptent les requêtes HTTP pour faire de l'auth, logging, validation, etc.", "is_correct": True},
                    {"text": "Des services injectés dans les contrôleurs", "is_correct": False},
                    {"text": "Des couches d'abstraction pour la DB", "is_correct": False},
                    {"text": "Des plugins Laravel", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Policies dans Laravel?", "answers": [
                    {"text": "Des classes organisant la logique d'autorisation par modèle (can, cannot)", "is_correct": True},
                    {"text": "Des règles de validation de formulaires", "is_correct": False},
                    {"text": "Des politiques de sécurité globales", "is_correct": False},
                    {"text": "Des gestionnaires de sessions", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Form Requests dans Laravel?", "answers": [
                    {"text": "Des classes gérant la validation et l'autorisation des données de formulaire", "is_correct": True},
                    {"text": "Des classes générant des formulaires HTML automatiquement", "is_correct": False},
                    {"text": "Des modèles pour les données POST", "is_correct": False},
                    {"text": "Des contrôleurs dédiés aux formulaires", "is_correct": False}
                ]},
                {"text": "Comment définir une relation HasMany en Eloquent?", "answers": [
                    {"text": "public function posts() { return $this->hasMany(Post::class); }", "is_correct": True},
                    {"text": "public function posts() { return $this->oneToMany(Post::class); }", "is_correct": False},
                    {"text": "public function posts() { return $this->relatesTo(Post::class, 'many'); }", "is_correct": False},
                    {"text": "public function posts() { return Post::where('user_id', $this->id)->get(); }", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Jobs et Queues dans Laravel?", "answers": [
                    {"text": "Des tâches déportées en arrière-plan via des workers pour ne pas bloquer les requêtes", "is_correct": True},
                    {"text": "Des tâches planifiées exécutées à intervalles", "is_correct": False},
                    {"text": "Des opérations parallèles sur la base de données", "is_correct": False},
                    {"text": "Des webhooks entrants traités en arrière-plan", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Service Container de Laravel?", "answers": [
                    {"text": "Un IoC container pour gérer les dépendances et l'injection de dépendances", "is_correct": True},
                    {"text": "Un container Docker pour Laravel", "is_correct": False},
                    {"text": "Un conteneur de services cloud", "is_correct": False},
                    {"text": "Un registre des services tiers intégrés", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Service Provider dans Laravel?", "answers": [
                    {"text": "La classe centrale pour bootstrapper les services de l'application (lier dans le container, events...)", "is_correct": True},
                    {"text": "Un fournisseur de services cloud intégré", "is_correct": False},
                    {"text": "Une classe pour les appels API externes", "is_correct": False},
                    {"text": "Un middleware de service discovery", "is_correct": False}
                ]},
                {"text": "Comment utiliser le système d'events dans Laravel?", "answers": [
                    {"text": "Créer un Event, un Listener et enregistrer dans EventServiceProvider, puis event(new MonEvent())", "is_correct": True},
                    {"text": "Avec dispatch() directement sur un objet", "is_correct": False},
                    {"text": "Avec Event::fire() sur l'event", "is_correct": False},
                    {"text": "En utilisant les signaux Laravel (similaires aux signaux Django)", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Cache dans Laravel?", "answers": [
                    {"text": "Un système de cache multi-driver (redis, memcached, file, array) avec une API unifiée", "is_correct": True},
                    {"text": "Un cache HTTP uniquement", "is_correct": False},
                    {"text": "Un cache de QuerySets Eloquent", "is_correct": False},
                    {"text": "Un cache de sessions uniquement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Observers Eloquent?", "answers": [
                    {"text": "Des classes qui groupent les event listeners pour un modèle (creating, created, updating, deleting...)", "is_correct": True},
                    {"text": "Des watchers sur les changements de base de données en temps réel", "is_correct": False},
                    {"text": "Des middlewares sur les queries Eloquent", "is_correct": False},
                    {"text": "Des outils de monitoring des modèles", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Laravel - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que Laravel Octane?", "answers": [
                    {"text": "Booste les performances en gardant l'app en mémoire avec Swoole ou RoadRunner (pas de bootstrap à chaque requête)", "is_correct": True},
                    {"text": "Un framework de microservices Laravel", "is_correct": False},
                    {"text": "Un CDN intégré à Laravel", "is_correct": False},
                    {"text": "Un compilateur Laravel vers bytecode", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Macros dans Laravel?", "answers": [
                    {"text": "Étendre des classes du framework avec des méthodes personnalisées via ::macro()", "is_correct": True},
                    {"text": "Des templates Blade réutilisables", "is_correct": False},
                    {"text": "Des commandes Artisan automatisées", "is_correct": False},
                    {"text": "Des raccourcis pour les routes groupées", "is_correct": False}
                ]},
                {"text": "Comment implémenter du multi-tenancy avec Laravel?", "answers": [
                    {"text": "Via des packages comme tenancyforlaravel ou stancl/tenancy avec une DB par tenant ou filtrage", "is_correct": True},
                    {"text": "Laravel supporte nativement le multi-tenancy", "is_correct": False},
                    {"text": "Avec des middleware de tenant uniquement", "is_correct": False},
                    {"text": "En créant une instance Artisan par tenant", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Model Scopes Eloquent?", "answers": [
                    {"text": "Des méthodes réutilisables de filtrage sur les QueryBuilder (local scopes) ou globaux (global scopes)", "is_correct": True},
                    {"text": "La portée de visibilité d'un modèle", "is_correct": False},
                    {"text": "Des permissions d'accès sur les modèles", "is_correct": False},
                    {"text": "Des scopes CSS dans les templates Blade", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Lazy Collections dans Laravel?", "answers": [
                    {"text": "Des collections évaluées paresseusement permettant de traiter des millions d'enregistrements sans saturer la mémoire", "is_correct": True},
                    {"text": "Des collections chargées de façon asynchrone", "is_correct": False},
                    {"text": "Des collections avec pagination automatique", "is_correct": False},
                    {"text": "Des collections immuables de Laravel", "is_correct": False}
                ]},
                {"text": "Comment tester des routes protégées par auth dans Laravel?", "answers": [
                    {"text": "Avec actingAs($user) pour simuler l'authentification dans les tests", "is_correct": True},
                    {"text": "En configurant AUTH_DISABLED=true dans le .env de test", "is_correct": False},
                    {"text": "En utilisant un middleware de test spécial", "is_correct": False},
                    {"text": "Les routes protégées ne peuvent pas être testées unitairement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Pipeline dans Laravel?", "answers": [
                    {"text": "Un pattern pour passer un objet à travers une série de stages/étapes transformatrices", "is_correct": True},
                    {"text": "Le pipeline CI/CD intégré à Laravel", "is_correct": False},
                    {"text": "Un système de processing de jobs en séquence", "is_correct": False},
                    {"text": "Une chaîne de middlewares pour une route", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Broadcasting dans Laravel?", "answers": [
                    {"text": "Un système pour diffuser des événements côté serveur vers le client via WebSockets (Pusher, Reverb)", "is_correct": True},
                    {"text": "Un système de newsletters intégré", "is_correct": False},
                    {"text": "Un système de diffusion de jobs à des workers", "is_correct": False},
                    {"text": "Un cache de réponses HTTP en broadcast", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Telescope de Laravel?", "answers": [
                    {"text": "Un outil de debugging et monitoring en temps réel des requêtes, queries, jobs, logs de l'app", "is_correct": True},
                    {"text": "Un outil de déploiement Laravel", "is_correct": False},
                    {"text": "Un observatoire de métriques de performance", "is_correct": False},
                    {"text": "Un IDE plugin pour Laravel", "is_correct": False}
                ]},
                {"text": "Comment optimiser les performances Eloquent N+1?", "answers": [
                    {"text": "Avec eager loading via with() ou load() pour précharger les relations", "is_correct": True},
                    {"text": "En activant le query cache dans config/database.php", "is_correct": False},
                    {"text": "En utilisant always_eager: true dans le modèle", "is_correct": False},
                    {"text": "Avec le package laravel-optimizer", "is_correct": False}
                ]},
            ],
        },
    },
}

FASTAPI_DATA = {
    "category": {
        "name": "FastAPI",
        "description": "Quiz pour maîtriser FastAPI et le développement d'API Python modernes",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "FastAPI - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Sur quel framework FastAPI est-il basé?", "answers": [
                    {"text": "Starlette (et Pydantic pour la validation)", "is_correct": True},
                    {"text": "Django", "is_correct": False},
                    {"text": "Flask", "is_correct": False},
                    {"text": "Tornado", "is_correct": False}
                ]},
                {"text": "Comment créer une route GET simple en FastAPI?", "answers": [
                    {"text": "@app.get('/') def ma_route(): return {'message': 'Hello'}", "is_correct": True},
                    {"text": "@app.route('/') def ma_route(): return {'message': 'Hello'}", "is_correct": False},
                    {"text": "@get('/') def ma_route(): return {'message': 'Hello'}", "is_correct": False},
                    {"text": "app.add_route('GET', '/', ma_route)", "is_correct": False}
                ]},
                {"text": "Quel serveur ASGI FastAPI recommande-t-il?", "answers": [
                    {"text": "Uvicorn", "is_correct": True},
                    {"text": "Gunicorn", "is_correct": False},
                    {"text": "uWSGI", "is_correct": False},
                    {"text": "Apache", "is_correct": False}
                ]},
                {"text": "Comment déclarer un paramètre de chemin en FastAPI?", "answers": [
                    {"text": "@app.get('/items/{item_id}') def get_item(item_id: int): ...", "is_correct": True},
                    {"text": "@app.get('/items/:item_id') def get_item(item_id): ...", "is_correct": False},
                    {"text": "@app.get('/items/<item_id>') def get_item(item_id): ...", "is_correct": False},
                    {"text": "@app.get('/items') def get_item(@Param item_id: int): ...", "is_correct": False}
                ]},
                {"text": "Comment valider le body d'une requête POST avec FastAPI?", "answers": [
                    {"text": "En définissant un modèle Pydantic et en le déclarant comme paramètre de la fonction", "is_correct": True},
                    {"text": "En accédant à request.json() manuellement", "is_correct": False},
                    {"text": "En utilisant le décorateur @validate_body", "is_correct": False},
                    {"text": "En définissant un JSON Schema dans le décorateur de route", "is_correct": False}
                ]},
                {"text": "Quelle bibliothèque FastAPI utilise pour la validation des données?", "answers": [
                    {"text": "Pydantic", "is_correct": True},
                    {"text": "Marshmallow", "is_correct": False},
                    {"text": "Cerberus", "is_correct": False},
                    {"text": "Voluptuous", "is_correct": False}
                ]},
                {"text": "Comment accéder à la documentation interactive de FastAPI?", "answers": [
                    {"text": "/docs (Swagger UI) ou /redoc", "is_correct": True},
                    {"text": "/api-docs", "is_correct": False},
                    {"text": "/documentation", "is_correct": False},
                    {"text": "/openapi", "is_correct": False}
                ]},
                {"text": "Comment retourner un code de statut HTTP personnalisé en FastAPI?", "answers": [
                    {"text": "@app.post('/item', status_code=201) def create(): ...", "is_correct": True},
                    {"text": "return Response(status=201)", "is_correct": False},
                    {"text": "raise HTTPException(201)", "is_correct": False},
                    {"text": "return {'status': 201, 'data': {}}", "is_correct": False}
                ]},
                {"text": "Comment déclarer un query parameter en FastAPI?", "answers": [
                    {"text": "def route(param: str = 'default'): ... (paramètre de fonction non dans le path)", "is_correct": True},
                    {"text": "def route(@Query param: str): ...", "is_correct": False},
                    {"text": "def route(request.query.param): ...", "is_correct": False},
                    {"text": "Query(param='default') dans le décorateur", "is_correct": False}
                ]},
                {"text": "Comment gérer les erreurs HTTP en FastAPI?", "answers": [
                    {"text": "raise HTTPException(status_code=404, detail='Not found')", "is_correct": True},
                    {"text": "return Error(404, 'Not found')", "is_correct": False},
                    {"text": "throw HttpError(404)", "is_correct": False},
                    {"text": "abort(404, 'Not found')", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "FastAPI - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Comment créer une route async en FastAPI?", "answers": [
                    {"text": "@app.get('/') async def ma_route(): await asyncio.sleep(0); return {}}", "is_correct": True},
                    {"text": "@app.get('/') @async def ma_route(): ...", "is_correct": False},
                    {"text": "@app.get('/', async=True) def ma_route(): ...", "is_correct": False},
                    {"text": "FastAPI ne supporte pas les routes async", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Depends() en FastAPI?", "answers": [
                    {"text": "Un système d'injection de dépendances pour partager de la logique entre routes (auth, DB...)", "is_correct": True},
                    {"text": "Un décorateur pour les dépendances npm", "is_correct": False},
                    {"text": "Un validateur de paramètres avancé", "is_correct": False},
                    {"text": "Un middleware FastAPI", "is_correct": False}
                ]},
                {"text": "Comment définir un modèle Pydantic avec validation?", "answers": [
                    {"text": "class Item(BaseModel): name: str; price: float = Field(gt=0)", "is_correct": True},
                    {"text": "class Item(Model): name: str; price: float", "is_correct": False},
                    {"text": "@validate class Item: name: str; price: float", "is_correct": False},
                    {"text": "Item = pydantic.create_model('Item', name=str, price=float)", "is_correct": False}
                ]},
                {"text": "Comment ajouter un middleware CORS en FastAPI?", "answers": [
                    {"text": "app.add_middleware(CORSMiddleware, allow_origins=['*'])", "is_correct": True},
                    {"text": "@app.middleware('cors') def cors(): ...", "is_correct": False},
                    {"text": "app.use(cors())", "is_correct": False},
                    {"text": "@app.cors(allow_all=True)", "is_correct": False}
                ]},
                {"text": "Comment utiliser les Background Tasks en FastAPI?", "answers": [
                    {"text": "def route(background_tasks: BackgroundTasks): background_tasks.add_task(fn, args)", "is_correct": True},
                    {"text": "asyncio.create_task(fn()) dans la route", "is_correct": False},
                    {"text": "@background def fn(): ... sur la fonction", "is_correct": False},
                    {"text": "threading.Thread(target=fn).start() dans la route", "is_correct": False}
                ]},
                {"text": "Comment organiser une grande application FastAPI?", "answers": [
                    {"text": "Avec APIRouter pour créer des sous-modules et include_router() dans l'app principale", "is_correct": True},
                    {"text": "Avec un seul fichier main.py sans séparation", "is_correct": False},
                    {"text": "En créant une nouvelle instance FastAPI par module", "is_correct": False},
                    {"text": "En utilisant Blueprint comme Flask", "is_correct": False}
                ]},
                {"text": "Comment gérer la session de base de données avec SQLAlchemy dans FastAPI?", "answers": [
                    {"text": "Avec une dépendance Depends(get_db) qui yield la session et la ferme après la requête", "is_correct": True},
                    {"text": "En créant une session globale accessible partout", "is_correct": False},
                    {"text": "En passant la session dans chaque paramètre de route", "is_correct": False},
                    {"text": "FastAPI gère automatiquement les sessions SQLAlchemy", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que lifespan en FastAPI (remplace on_startup/on_shutdown)?", "answers": [
                    {"text": "Un context manager async qui gère les événements de démarrage et d'arrêt de l'application", "is_correct": True},
                    {"text": "La durée de vie d'une connexion HTTP", "is_correct": False},
                    {"text": "Un gestionnaire de timeout pour les routes lentes", "is_correct": False},
                    {"text": "Un système de versioning de l'API", "is_correct": False}
                ]},
                {"text": "Comment tester une application FastAPI?", "answers": [
                    {"text": "Avec TestClient de fastapi.testclient (basé sur httpx) et pytest", "is_correct": True},
                    {"text": "Avec unittest uniquement", "is_correct": False},
                    {"text": "En lançant un vrai serveur et faisant des requêtes HTTP", "is_correct": False},
                    {"text": "FastAPI fournit son propre framework de tests", "is_correct": False}
                ]},
                {"text": "Comment définir des response models en FastAPI?", "answers": [
                    {"text": "@app.get('/', response_model=ItemResponse) pour filtrer et valider la sortie", "is_correct": True},
                    {"text": "En retournant directement le modèle Pydantic", "is_correct": False},
                    {"text": "@app.get('/', return=ItemResponse)", "is_correct": False},
                    {"text": "response_schema(ItemResponse) dans la route", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "FastAPI - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que les WebSockets en FastAPI?", "answers": [
                    {"text": "Des connexions bidirectionnelles persistantes via @app.websocket('/ws') et WebSocket object", "is_correct": True},
                    {"text": "Des routes HTTP qui restent ouvertes", "is_correct": False},
                    {"text": "Des Server-Sent Events FastAPI", "is_correct": False},
                    {"text": "Des webhooks entrants FastAPI", "is_correct": False}
                ]},
                {"text": "Comment implémenter l'authentification JWT dans FastAPI?", "answers": [
                    {"text": "Avec OAuth2PasswordBearer, python-jose et une dépendance Depends(get_current_user)", "is_correct": True},
                    {"text": "Avec @app.jwt_auth() décorateur", "is_correct": False},
                    {"text": "En utilisant Flask-JWT-Extended porté sur FastAPI", "is_correct": False},
                    {"text": "FastAPI gère JWT automatiquement via security.py", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que StreamingResponse en FastAPI?", "answers": [
                    {"text": "Retourne des données en streaming (générateur) pour les gros fichiers ou SSE", "is_correct": True},
                    {"text": "Une réponse JSON compressée en streaming", "is_correct": False},
                    {"text": "Une réponse qui se charge progressivement", "is_correct": False},
                    {"text": "Un WebSocket déguisé en réponse HTTP", "is_correct": False}
                ]},
                {"text": "Comment gérer les custom exception handlers en FastAPI?", "answers": [
                    {"text": "@app.exception_handler(MonException) async def handler(request, exc): return JSONResponse(...)", "is_correct": True},
                    {"text": "En surchargeant la méthode handle_exception de FastAPI", "is_correct": False},
                    {"text": "Avec @app.error_handler comme en Flask", "is_correct": False},
                    {"text": "En configurant error_handlers dans FastAPI()", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Custom Middleware en FastAPI?", "answers": [
                    {"text": "Des classes BaseHTTPMiddleware ou fonctions ASGI qui traitent toutes les requêtes/réponses", "is_correct": True},
                    {"text": "Des décorateurs appliqués sur des routes spécifiques", "is_correct": False},
                    {"text": "Des plugins Starlette installables", "is_correct": False},
                    {"text": "Des intercepteurs similaires aux guards NestJS", "is_correct": False}
                ]},
                {"text": "Comment déployer FastAPI en production?", "answers": [
                    {"text": "Uvicorn + Gunicorn (worker class uvicorn.workers.UvicornWorker) ou dans un container Docker", "is_correct": True},
                    {"text": "Avec le serveur de développement uvicorn --reload", "is_correct": False},
                    {"text": "Avec mod_wsgi sur Apache", "is_correct": False},
                    {"text": "FastAPI ne supporte pas le déploiement multi-worker", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Annotated dans les dépendances FastAPI modernes?", "answers": [
                    {"text": "Permet d'attacher des métadonnées (validators, Depends...) au type hint pour une meilleure lisibilité", "is_correct": True},
                    {"text": "Un décorateur pour documenter les paramètres", "is_correct": False},
                    {"text": "Un type générique pour les annotations de schema", "is_correct": False},
                    {"text": "Un remplaçant de Optional dans FastAPI v2", "is_correct": False}
                ]},
                {"text": "Comment implémenter la pagination avec FastAPI?", "answers": [
                    {"text": "Paramètres query skip/limit ou cursor, avec des dépendances réutilisables", "is_correct": True},
                    {"text": "Avec le module fastapi.pagination automatiquement", "is_correct": False},
                    {"text": "En configurant paginate=True dans le décorateur de route", "is_correct": False},
                    {"text": "Uniquement via la bibliothèque fastapi-pagination externe", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que FastAPI et Pydantic v2 apportent?", "answers": [
                    {"text": "Pydantic v2 est réécrit en Rust (pydantic-core) - performances 5-50x supérieures, nouvelle API", "is_correct": True},
                    {"text": "Pydantic v2 ajoute le support GraphQL", "is_correct": False},
                    {"text": "Pydantic v2 remplace FastAPI par un système de routing", "is_correct": False},
                    {"text": "Pydantic v2 ajoute seulement des types nouveaux", "is_correct": False}
                ]},
                {"text": "Comment implémenter des tests async avec FastAPI?", "answers": [
                    {"text": "Avec httpx.AsyncClient et pytest-asyncio : async with AsyncClient(app=app) as client: ...", "is_correct": True},
                    {"text": "TestClient supporte nativement l'async sans configuration", "is_correct": False},
                    {"text": "Avec asynctest.TestCase uniquement", "is_correct": False},
                    {"text": "FastAPI ne supporte pas les tests asynchrones", "is_correct": False}
                ]},
            ],
        },
    },
}

SPRING_DATA = {
    "category": {
        "name": "Spring Boot",
        "description": "Quiz pour maîtriser Spring Boot et l'écosystème Java",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Spring Boot - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Que facilite Spring Boot par rapport à Spring?", "answers": [
                    {"text": "Auto-configuration et starters pour démarrer rapidement", "is_correct": True},
                    {"text": "Meilleures performances", "is_correct": False},
                    {"text": "Support de plus de bases de données", "is_correct": False},
                    {"text": "Version gratuite de Spring", "is_correct": False}
                ]},
                {"text": "Quelle annotation marque une classe comme contrôleur REST?", "answers": [
                    {"text": "@RestController", "is_correct": True},
                    {"text": "@Controller", "is_correct": False},
                    {"text": "@Service", "is_correct": False},
                    {"text": "@Component", "is_correct": False}
                ]},
                {"text": "Comment mapper une requête GET sur /hello?", "answers": [
                    {"text": "@GetMapping(\"/hello\")", "is_correct": True},
                    {"text": "@RequestMapping(\"/hello\", method=GET)", "is_correct": False},
                    {"text": "@PostMapping(\"/hello\")", "is_correct": False},
                    {"text": "@Route(\"/hello\")", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que l'injection de dépendances dans Spring?", "answers": [
                    {"text": "@Autowired injecte automatiquement les beans", "is_correct": True},
                    {"text": "Créer manuellement les dépendances", "is_correct": False},
                    {"text": "Un pattern de conception", "is_correct": False},
                    {"text": "Un fichier XML", "is_correct": False}
                ]},
                {"text": "Quel fichier configure Spring Boot?", "answers": [
                    {"text": "application.properties ou application.yml", "is_correct": True},
                    {"text": "spring-config.xml", "is_correct": False},
                    {"text": "config.json", "is_correct": False},
                    {"text": "boot.ini", "is_correct": False}
                ]},
                {"text": "Comment créer un bean Spring?", "answers": [
                    {"text": "@Bean dans une classe @Configuration", "is_correct": True},
                    {"text": "@Component sur une classe", "is_correct": True},
                    {"text": "@Service ou @Repository", "is_correct": True},
                    {"text": "new Bean()", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Spring Data JPA?", "answers": [
                    {"text": "Abstraction pour les accès DB basée sur JPA", "is_correct": True},
                    {"text": "Un ORM alternatif à Hibernate", "is_correct": False},
                    {"text": "Un driver JDBC", "is_correct": False},
                    {"text": "Une base de données", "is_correct": False}
                ]},
                {"text": "Comment créer une interface repository?", "answers": [
                    {"text": "extends JpaRepository<Entité, ID>", "is_correct": True},
                    {"text": "@Repository annotation", "is_correct": False},
                    {"text": "implements CrudRepository", "is_correct": False},
                    {"text": "new Repository()", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Spring Security?", "answers": [
                    {"text": "Framework d'authentification et d'autorisation", "is_correct": True},
                    {"text": "Un firewall Java", "is_correct": False},
                    {"text": "Un gestionnaire de sessions", "is_correct": False},
                    {"text": "Un crypteur de mots de passe", "is_correct": False}
                ]},
                {"text": "Comment lancer une app Spring Boot?", "answers": [
                    {"text": "SpringApplication.run(MonApp.class, args)", "is_correct": True},
                    {"text": "new SpringApp().start()", "is_correct": False},
                    {"text": "BootApplication.launch()", "is_correct": False},
                    {"text": "mvn spring-boot:run", "is_correct": True}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Spring Boot - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que l'inversion de contrôle (IoC) dans Spring?", "answers": [
                    {"text": "Le conteneur Spring gère le cycle de vie des objets au lieu du code applicatif", "is_correct": True},
                    {"text": "Inverser l'ordre des méthodes appelées", "is_correct": False},
                    {"text": "Un pattern pour les contrôleurs inversés", "is_correct": False},
                    {"text": "Une configuration inverse de l'application", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Spring AOP (Aspect Oriented Programming)?", "answers": [
                    {"text": "Permet de séparer les préoccupations transversales (logging, sécurité, transactions) via des aspects", "is_correct": True},
                    {"text": "Une programmation orientée aspect pour les API", "is_correct": False},
                    {"text": "Un outil de profiling", "is_correct": False},
                    {"text": "Un framework de tests", "is_correct": False}
                ]},
                {"text": "Comment gérer les transactions avec Spring?", "answers": [
                    {"text": "@Transactional sur les méthodes ou classes services", "is_correct": True},
                    {"text": "En appelant commit() et rollback() manuellement", "is_correct": False},
                    {"text": "Avec un gestionnaire de transactions XML", "is_correct": False},
                    {"text": "Spring gère automatiquement sans annotation", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Spring Boot Actuator?", "answers": [
                    {"text": "Fournit des endpoints de monitoring et métriques sur l'application en production", "is_correct": True},
                    {"text": "Un outil pour activer les profils Spring", "is_correct": False},
                    {"text": "Un gestionnaire d'actuateurs de processus", "is_correct": False},
                    {"text": "Une bibliothèque de tests de charge", "is_correct": False}
                ]},
                {"text": "Comment implémenter la sécurité JWT avec Spring Security?", "answers": [
                    {"text": "En configurant un filtre JWT dans la chaîne de sécurité et un UserDetailsService", "is_correct": True},
                    {"text": "@EnableJWT sur la classe principale", "is_correct": False},
                    {"text": "Spring Security supporte JWT nativement sans configuration", "is_correct": False},
                    {"text": "Avec spring-security-jwt-starter uniquement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Spring Cloud?", "answers": [
                    {"text": "Un ensemble d'outils pour construire des architectures microservices (config, discovery, gateway)", "is_correct": True},
                    {"text": "Un déploiement Spring sur le cloud", "is_correct": False},
                    {"text": "Un ORM cloud pour Spring", "is_correct": False},
                    {"text": "Un service AWS pour Spring", "is_correct": False}
                ]},
                {"text": "Comment configurer un profile Spring?", "answers": [
                    {"text": "@Profile(\"dev\") ou spring.profiles.active dans application.properties", "is_correct": True},
                    {"text": "En créant un fichier profile.xml", "is_correct": False},
                    {"text": "Avec @ActiveProfile dans le code", "is_correct": False},
                    {"text": "Les profiles sont automatiquement détectés", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Spring Data REST?", "answers": [
                    {"text": "Expose automatiquement les repositories JPA comme des endpoints REST", "is_correct": True},
                    {"text": "Une API REST pour les data sources", "is_correct": False},
                    {"text": "Un client REST pour Spring Data", "is_correct": False},
                    {"text": "Un ORM RESTful", "is_correct": False}
                ]},
                {"text": "Comment tester un contrôleur Spring MVC?", "answers": [
                    {"text": "Avec @WebMvcTest et MockMvc pour tester les contrôleurs isolément", "is_correct": True},
                    {"text": "En démarrant l'application complète", "is_correct": False},
                    {"text": "Avec SpringBootTest sans isolation", "is_correct": False},
                    {"text": "Uniquement avec Postman", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Spring Boot DevTools?", "answers": [
                    {"text": "Fournit des fonctionnalités de développement comme le redémarrage automatique et LiveReload", "is_correct": True},
                    {"text": "Un IDE pour Spring", "is_correct": False},
                    {"text": "Un outil de déploiement", "is_correct": False},
                    {"text": "Une bibliothèque de debugging", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Spring Boot - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que Spring WebFlux?", "answers": [
                    {"text": "Un framework réactif non-bloquant pour construire des applications asynchrones", "is_correct": True},
                    {"text": "Une version améliorée de Spring MVC", "is_correct": False},
                    {"text": "Un framework pour les flux web", "is_correct": False},
                    {"text": "Un client HTTP réactif", "is_correct": False}
                ]},
                {"text": "Comment fonctionne Project Reactor dans Spring WebFlux?", "answers": [
                    {"text": "Avec Mono (0-1 élément) et Flux (0-N éléments) pour la programmation réactive", "is_correct": True},
                    {"text": "C'est un moteur de templates", "is_correct": False},
                    {"text": "Un ORM réactif", "is_correct": False},
                    {"text": "Un gestionnaire d'événements", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Spring Cloud Config?", "answers": [
                    {"text": "Un serveur centralisé de configuration pour les microservices", "is_correct": True},
                    {"text": "Une configuration cloud pour Spring", "is_correct": False},
                    {"text": "Un outil de configuration de déploiement", "is_correct": False},
                    {"text": "Un gestionnaire de secrets", "is_correct": False}
                ]},
                {"text": "Comment implémenter la résilience avec Spring Cloud Circuit Breaker?", "answers": [
                    {"text": "Avec @CircuitBreaker pour éviter les appels à des services défaillants", "is_correct": True},
                    {"text": "En créant un proxy manuellement", "is_correct": False},
                    {"text": "Avec un load balancer", "is_correct": False},
                    {"text": "Spring gère automatiquement la résilience", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Spring Batch?", "answers": [
                    {"text": "Un framework pour le traitement par lots de gros volumes de données", "is_correct": True},
                    {"text": "Un outil de batch processing pour les requêtes", "is_correct": False},
                    {"text": "Un système de jobs planifiés", "is_correct": False},
                    {"text": "Une bibliothèque de batch SQL", "is_correct": False}
                ]},
                {"text": "Comment fonctionne la sécurité méthodologique avec @PreAuthorize?", "answers": [
                    {"text": "Utilise des expressions SpEL pour autoriser l'accès aux méthodes", "is_correct": True},
                    {"text": "Pré-autorise toutes les méthodes d'un contrôleur", "is_correct": False},
                    {"text": "Une annotation pour les tests", "is_correct": False},
                    {"text": "Active la pré-autorisation globale", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Spring Integration?", "answers": [
                    {"text": "Un framework pour l'intégration d'applications via des patterns EIP (Enterprise Integration Patterns)", "is_correct": True},
                    {"text": "L'intégration de Spring avec d'autres frameworks", "is_correct": False},
                    {"text": "Un outil de CI/CD", "is_correct": False},
                    {"text": "Une API d'intégration continue", "is_correct": False}
                ]},
                {"text": "Comment optimiser les performances avec le caching Spring?", "answers": [
                    {"text": "@Cacheable, @CacheEvict, @CachePut avec des providers comme Redis ou Ehcache", "is_correct": True},
                    {"text": "En utilisant ConcurrentHashMap directement", "is_correct": False},
                    {"text": "Avec spring.cache.enabled=true", "is_correct": False},
                    {"text": "Le cache est automatique dans Spring", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Spring Native (Spring Boot 3)?", "answers": [
                    {"text": "Compile les applications Spring Boot en exécutables natifs avec GraalVM pour démarrage ultra-rapide", "is_correct": True},
                    {"text": "Une version native de Spring pour mobile", "is_correct": False},
                    {"text": "Un portage de Spring en C++", "is_correct": False},
                    {"text": "Un framework Spring sans JVM", "is_correct": False}
                ]},
                {"text": "Comment implémenter les WebSockets avec Spring?", "answers": [
                    {"text": "Avec @MessageMapping, SimpMessagingTemplate et STOMP pour les communications temps réel", "is_correct": True},
                    {"text": "En utilisant @WebSocket sur les contrôleurs", "is_correct": False},
                    {"text": "Avec spring-websocket-starter uniquement", "is_correct": False},
                    {"text": "Spring ne supporte pas les WebSockets", "is_correct": False}
                ]},
            ],
        },
    },
}

# 4. BASES DE DONNÉES
# -----------------------------------------------------------------------------

SQL_DATA = {
    "category": {
        "name": "SQL",
        "description": "Quiz pour maîtriser SQL et la gestion de bases de données relationnelles",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "SQL - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Quelle commande SQL sélectionne toutes les colonnes d'une table?", "answers": [
                    {"text": "SELECT * FROM table", "is_correct": True},
                    {"text": "GET ALL FROM table", "is_correct": False},
                    {"text": "FETCH * FROM table", "is_correct": False},
                    {"text": "READ table", "is_correct": False}
                ]},
                {"text": "Quelle commande SQL insère une nouvelle ligne?", "answers": [
                    {"text": "INSERT INTO table VALUES (...)", "is_correct": True},
                    {"text": "ADD INTO table VALUES (...)", "is_correct": False},
                    {"text": "PUT INTO table VALUES (...)", "is_correct": False},
                    {"text": "CREATE ROW IN table VALUES (...)", "is_correct": False}
                ]},
                {"text": "Comment filtrer les résultats d'une requête SQL?", "answers": [
                    {"text": "SELECT * FROM table WHERE condition", "is_correct": True},
                    {"text": "SELECT * FROM table FILTER condition", "is_correct": False},
                    {"text": "SELECT * FROM table IF condition", "is_correct": False},
                    {"text": "SELECT * FROM table HAVING condition", "is_correct": False}
                ]},
                {"text": "Quelle commande SQL met à jour des données existantes?", "answers": [
                    {"text": "UPDATE table SET colonne = valeur WHERE condition", "is_correct": True},
                    {"text": "MODIFY table SET colonne = valeur", "is_correct": False},
                    {"text": "CHANGE table colonne = valeur", "is_correct": False},
                    {"text": "EDIT table SET colonne = valeur", "is_correct": False}
                ]},
                {"text": "Quelle commande SQL supprime des lignes?", "answers": [
                    {"text": "DELETE FROM table WHERE condition", "is_correct": True},
                    {"text": "REMOVE FROM table WHERE condition", "is_correct": False},
                    {"text": "DROP FROM table WHERE condition", "is_correct": False},
                    {"text": "ERASE FROM table WHERE condition", "is_correct": False}
                ]},
                {"text": "Comment trier les résultats par ordre croissant?", "answers": [
                    {"text": "ORDER BY colonne ASC", "is_correct": True},
                    {"text": "SORT BY colonne ASC", "is_correct": False},
                    {"text": "ORDER colonne ASCENDING", "is_correct": False},
                    {"text": "GROUP BY colonne ASC", "is_correct": False}
                ]},
                {"text": "Quelle clause SQL limite le nombre de résultats?", "answers": [
                    {"text": "LIMIT n", "is_correct": True},
                    {"text": "TOP n", "is_correct": False},
                    {"text": "MAX n", "is_correct": False},
                    {"text": "FETCH n", "is_correct": False}
                ]},
                {"text": "Quelle fonction SQL compte le nombre de lignes?", "answers": [
                    {"text": "COUNT(*)", "is_correct": True},
                    {"text": "SUM(*)", "is_correct": False},
                    {"text": "TOTAL(*)", "is_correct": False},
                    {"text": "NUMBER(*)", "is_correct": False}
                ]},
                {"text": "Comment créer une table en SQL?", "answers": [
                    {"text": "CREATE TABLE nom (colonne type, ...)", "is_correct": True},
                    {"text": "NEW TABLE nom (colonne type, ...)", "is_correct": False},
                    {"text": "ADD TABLE nom (colonne type, ...)", "is_correct": False},
                    {"text": "MAKE TABLE nom (colonne type, ...)", "is_correct": False}
                ]},
                {"text": "Que signifie NULL en SQL?", "answers": [
                    {"text": "L'absence de valeur", "is_correct": True},
                    {"text": "La valeur zéro", "is_correct": False},
                    {"text": "Une chaîne vide", "is_correct": False},
                    {"text": "Une valeur fausse", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "SQL - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Quelle est la différence entre INNER JOIN et LEFT JOIN?", "answers": [
                    {"text": "LEFT JOIN retourne toutes les lignes de la table gauche, même sans correspondance à droite", "is_correct": True},
                    {"text": "INNER JOIN est plus rapide que LEFT JOIN", "is_correct": False},
                    {"text": "LEFT JOIN ne peut s'appliquer qu'à deux tables", "is_correct": False},
                    {"text": "INNER JOIN retourne toutes les lignes des deux tables", "is_correct": False}
                ]},
                {"text": "À quoi sert GROUP BY en SQL?", "answers": [
                    {"text": "Regrouper des lignes partageant une valeur commune pour appliquer des fonctions d'agrégation", "is_correct": True},
                    {"text": "Trier les résultats par groupe", "is_correct": False},
                    {"text": "Fusionner plusieurs tables", "is_correct": False},
                    {"text": "Filtrer les groupes avant agrégation", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre WHERE et HAVING?", "answers": [
                    {"text": "WHERE filtre avant agrégation, HAVING filtre après (sur les groupes)", "is_correct": True},
                    {"text": "HAVING est plus performant que WHERE", "is_correct": False},
                    {"text": "WHERE ne peut pas utiliser des sous-requêtes", "is_correct": False},
                    {"text": "HAVING s'applique uniquement aux colonnes indexées", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'une clé étrangère (FOREIGN KEY)?", "answers": [
                    {"text": "Une colonne qui référence la clé primaire d'une autre table pour maintenir l'intégrité référentielle", "is_correct": True},
                    {"text": "Une clé de chiffrement pour sécuriser les données", "is_correct": False},
                    {"text": "Un index sur une colonne d'une table externe", "is_correct": False},
                    {"text": "Une clé partagée entre plusieurs bases de données", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'une sous-requête (subquery)?", "answers": [
                    {"text": "Une requête imbriquée dans une autre requête SQL", "is_correct": True},
                    {"text": "Une requête partielle sur un sous-ensemble de colonnes", "is_correct": False},
                    {"text": "Une requête exécutée sur un serveur secondaire", "is_correct": False},
                    {"text": "Une partie d'une procédure stockée", "is_correct": False}
                ]},
                {"text": "Comment renommer une colonne dans le résultat d'une requête?", "answers": [
                    {"text": "SELECT colonne AS alias FROM table", "is_correct": True},
                    {"text": "SELECT colonne RENAME alias FROM table", "is_correct": False},
                    {"text": "SELECT colonne = alias FROM table", "is_correct": False},
                    {"text": "SELECT alias(colonne) FROM table", "is_correct": False}
                ]},
                {"text": "Que fait DISTINCT dans une requête SQL?", "answers": [
                    {"text": "Élimine les doublons des résultats", "is_correct": True},
                    {"text": "Trie les résultats par ordre alphabétique", "is_correct": False},
                    {"text": "Sélectionne uniquement les colonnes différentes", "is_correct": False},
                    {"text": "Filtre les valeurs NULL", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un index en SQL?", "answers": [
                    {"text": "Une structure de données qui accélère les recherches sur une colonne", "is_correct": True},
                    {"text": "Un identifiant unique de chaque ligne", "is_correct": False},
                    {"text": "Une clé primaire sur plusieurs colonnes", "is_correct": False},
                    {"text": "Un compteur automatique de lignes", "is_correct": False}
                ]},
                {"text": "Quelle fonction SQL retourne la valeur maximale d'une colonne?", "answers": [
                    {"text": "MAX(colonne)", "is_correct": True},
                    {"text": "HIGHEST(colonne)", "is_correct": False},
                    {"text": "TOP(colonne)", "is_correct": False},
                    {"text": "GREATEST(colonne)", "is_correct": False}
                ]},
                {"text": "Que fait UNION en SQL?", "answers": [
                    {"text": "Combine les résultats de deux requêtes en supprimant les doublons", "is_correct": True},
                    {"text": "Fusionne deux tables en une seule", "is_correct": False},
                    {"text": "Effectue une jointure entre deux tables", "is_correct": False},
                    {"text": "Combine deux colonnes en une seule", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "SQL - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce qu'une Window Function (fonction de fenêtre) en SQL?", "answers": [
                    {"text": "Une fonction qui effectue un calcul sur un ensemble de lignes liées à la ligne courante sans les regrouper", "is_correct": True},
                    {"text": "Une fonction qui s'exécute dans une fenêtre de temps définie", "is_correct": False},
                    {"text": "Une fonction qui crée une vue temporaire", "is_correct": False},
                    {"text": "Une fonction qui pagine les résultats en fenêtres", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un CTE (Common Table Expression)?", "answers": [
                    {"text": "Une table temporaire nommée définie avec WITH pour être utilisée dans la requête principale", "is_correct": True},
                    {"text": "Une table permanente partagée entre plusieurs bases de données", "is_correct": False},
                    {"text": "Un type de vue matérialisée", "is_correct": False},
                    {"text": "Une expression pour créer des colonnes calculées", "is_correct": False}
                ]},
                {"text": "Comment créer un CTE récursif?", "answers": [
                    {"text": "WITH RECURSIVE cte AS (partie_ancre UNION ALL partie_récursive)", "is_correct": True},
                    {"text": "WITH cte RECURSIVE AS (requête)", "is_correct": False},
                    {"text": "CREATE RECURSIVE VIEW cte AS (requête)", "is_correct": False},
                    {"text": "WITH cte AS (LOOP requête END LOOP)", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre une vue (VIEW) et une vue matérialisée?", "answers": [
                    {"text": "La vue matérialisée stocke physiquement le résultat pour de meilleures performances en lecture", "is_correct": True},
                    {"text": "La vue est plus lente mais prend moins d'espace", "is_correct": False},
                    {"text": "La vue matérialisée est mise à jour en temps réel", "is_correct": False},
                    {"text": "La vue classique stocke les données, la matérialisée non", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que l'isolation des transactions SERIALIZABLE?", "answers": [
                    {"text": "Le niveau le plus strict - les transactions semblent s'exécuter séquentiellement sans interférence", "is_correct": True},
                    {"text": "Les transactions sont sérialisées en JSON avant exécution", "is_correct": False},
                    {"text": "Les transactions sont journalisées pour permettre la récupération", "is_correct": False},
                    {"text": "Les transactions utilisent un seul thread d'exécution", "is_correct": False}
                ]},
                {"text": "Que fait ROW_NUMBER() OVER (PARTITION BY col ORDER BY col2)?", "answers": [
                    {"text": "Attribue un numéro de ligne séquentiel dans chaque partition ordonnée", "is_correct": True},
                    {"text": "Compte le nombre de lignes dans chaque groupe", "is_correct": False},
                    {"text": "Retourne le numéro de la première ligne de chaque partition", "is_correct": False},
                    {"text": "Crée un identifiant unique global pour chaque ligne", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre DELETE et TRUNCATE?", "answers": [
                    {"text": "TRUNCATE est plus rapide et non journalisé, DELETE supporte WHERE et peut être rollback", "is_correct": True},
                    {"text": "TRUNCATE supprime la table, DELETE supprime les lignes", "is_correct": False},
                    {"text": "DELETE est plus rapide car il utilise un index", "is_correct": False},
                    {"text": "TRUNCATE supporte les conditions WHERE", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le problème N+1 en base de données?", "answers": [
                    {"text": "Exécuter 1 requête pour une liste puis N requêtes supplémentaires pour chaque item", "is_correct": True},
                    {"text": "Une table avec N+1 colonnes qui dépasse la limite du SGBD", "is_correct": False},
                    {"text": "N transactions simultanées qui causent un deadlock", "is_correct": False},
                    {"text": "Un index qui nécessite N+1 lectures pour trouver une valeur", "is_correct": False}
                ]},
                {"text": "Comment fonctionne un index composite (multi-colonnes)?", "answers": [
                    {"text": "Efficace pour les requêtes sur le préfixe gauche des colonnes indexées (leftmost prefix rule)", "is_correct": True},
                    {"text": "Efficace uniquement si toutes les colonnes de l'index sont dans la requête", "is_correct": False},
                    {"text": "Crée autant d'index séparés que de colonnes", "is_correct": False},
                    {"text": "Indexe les colonnes dans n'importe quel ordre de requête", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un deadlock en base de données?", "answers": [
                    {"text": "Deux transactions qui s'attendent mutuellement pour libérer des verrous - aucune ne peut avancer", "is_correct": True},
                    {"text": "Une transaction qui s'exécute indéfiniment sans terminer", "is_correct": False},
                    {"text": "Un verrou posé sur une table entière bloquant toutes les lectures", "is_correct": False},
                    {"text": "Une requête qui dépasse le timeout défini par le SGBD", "is_correct": False}
                ]},
            ],
        },
    },
}

MONGODB_DATA = {
    "category": {
        "name": "MongoDB",
        "description": "Quiz pour maîtriser MongoDB et les bases de données NoSQL",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "MongoDB - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Quel type de base de données est MongoDB?", "answers": [
                    {"text": "NoSQL orienté documents", "is_correct": True},
                    {"text": "Relationnelle (SQL)", "is_correct": False},
                    {"text": "Base de données graphe", "is_correct": False},
                    {"text": "Clé-valeur", "is_correct": False}
                ]},
                {"text": "Comment MongoDB stocke-t-il les données?", "answers": [
                    {"text": "En documents JSON-like (BSON)", "is_correct": True},
                    {"text": "En tables et lignes", "is_correct": False},
                    {"text": "En XML", "is_correct": False},
                    {"text": "En fichiers CSV", "is_correct": False}
                ]},
                {"text": "Quelle commande affiche les bases de données?", "answers": [
                    {"text": "show dbs", "is_correct": True},
                    {"text": "list databases", "is_correct": False},
                    {"text": "db.show()", "is_correct": False},
                    {"text": "SHOW DATABASES", "is_correct": False}
                ]},
                {"text": "Comment sélectionner une base de données?", "answers": [
                    {"text": "use maBase", "is_correct": True},
                    {"text": "db.maBase", "is_correct": False},
                    {"text": "select maBase", "is_correct": False},
                    {"text": "connect maBase", "is_correct": False}
                ]},
                {"text": "Quelle commande insère un document dans une collection?", "answers": [
                    {"text": "db.collection.insertOne({nom: 'Alice'})", "is_correct": True},
                    {"text": "db.collection.add({nom: 'Alice'})", "is_correct": False},
                    {"text": "db.collection.push({nom: 'Alice'})", "is_correct": False},
                    {"text": "db.collection.save({nom: 'Alice'})", "is_correct": False}
                ]},
                {"text": "Comment trouver tous les documents d'une collection?", "answers": [
                    {"text": "db.collection.find()", "is_correct": True},
                    {"text": "db.collection.getAll()", "is_correct": False},
                    {"text": "db.collection.select()", "is_correct": False},
                    {"text": "db.collection.query()", "is_correct": False}
                ]},
                {"text": "Quel est l'équivalent d'une table SQL dans MongoDB?", "answers": [
                    {"text": "Collection", "is_correct": True},
                    {"text": "Document", "is_correct": False},
                    {"text": "Dataset", "is_correct": False},
                    {"text": "Bucket", "is_correct": False}
                ]},
                {"text": "Comment mettre à jour un document dans MongoDB?", "answers": [
                    {"text": "db.collection.updateOne({filtre}, {$set: {champ: valeur}})", "is_correct": True},
                    {"text": "db.collection.modify({filtre}, {champ: valeur})", "is_correct": False},
                    {"text": "db.collection.change({filtre}, {champ: valeur})", "is_correct": False},
                    {"text": "db.collection.edit({filtre}, {champ: valeur})", "is_correct": False}
                ]},
                {"text": "Comment supprimer un document?", "answers": [
                    {"text": "db.collection.deleteOne({filtre})", "is_correct": True},
                    {"text": "db.collection.remove({filtre})", "is_correct": False},
                    {"text": "db.collection.drop({filtre})", "is_correct": False},
                    {"text": "db.collection.erase({filtre})", "is_correct": False}
                ]},
                {"text": "Quel est le format de stockage interne de MongoDB?", "answers": [
                    {"text": "BSON (Binary JSON)", "is_correct": True},
                    {"text": "JSON pur", "is_correct": False},
                    {"text": "YAML", "is_correct": False},
                    {"text": "XML", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "MongoDB - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce qu'un index dans MongoDB?", "answers": [
                    {"text": "Une structure de données optimisant les requêtes sur certains champs", "is_correct": True},
                    {"text": "Un champ unique pour identifier les documents", "is_correct": False},
                    {"text": "Une table d'indexation", "is_correct": False},
                    {"text": "Un mécanisme de compression", "is_correct": False}
                ]},
                {"text": "Comment créer un index sur un champ?", "answers": [
                    {"text": "db.collection.createIndex({champ: 1})", "is_correct": True},
                    {"text": "db.collection.index({champ: 1})", "is_correct": False},
                    {"text": "db.collection.addIndex({champ: 1})", "is_correct": False},
                    {"text": "db.collection.ensureIndex({champ: 1})", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que l'agrégation MongoDB?", "answers": [
                    {"text": "Un pipeline de traitement de données (filter, group, sort, project) pour des analyses avancées", "is_correct": True},
                    {"text": "Une fonction d'agrégat SQL-like", "is_correct": False},
                    {"text": "Une jointure entre collections", "is_correct": False},
                    {"text": "Un calcul de moyennes simples", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un ObjectId dans MongoDB?", "answers": [
                    {"text": "L'identifiant unique par défaut (_id) généré automatiquement, incluant timestamp", "is_correct": True},
                    {"text": "Un type d'objet spécial", "is_correct": False},
                    {"text": "Un identifiant pour les objets BSON", "is_correct": False},
                    {"text": "Une référence à un autre document", "is_correct": False}
                ]},
                {"text": "Comment faire une jointure entre deux collections?", "answers": [
                    {"text": "Avec $lookup dans le pipeline d'agrégation", "is_correct": True},
                    {"text": "MongoDB ne supporte pas les jointures", "is_correct": False},
                    {"text": "Avec db.collection.join()", "is_correct": False},
                    {"text": "En utilisant des références manuelles", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le sharding dans MongoDB?", "answers": [
                    {"text": "Distribution horizontale des données sur plusieurs serveurs pour scaler", "is_correct": True},
                    {"text": "Une partition de disque", "is_correct": False},
                    {"text": "Un cache distribué", "is_correct": False},
                    {"text": "Un mécanisme de réplication", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que la réplication dans MongoDB?", "answers": [
                    {"text": "Copie des données sur plusieurs serveurs (replica set) pour haute disponibilité", "is_correct": True},
                    {"text": "Duplication des index", "is_correct": False},
                    {"text": "Sauvegarde automatique", "is_correct": False},
                    {"text": "Un système de cache", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le modèle de cohérence MongoDB?", "answers": [
                    {"text": "Cohérence éventuelle par défaut, mais réglable avec read/write concern", "is_correct": True},
                    {"text": "ACID strict comme SQL", "is_correct": False},
                    {"text": "BASE uniquement", "is_correct": False},
                    {"text": "Pas de cohérence garantie", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les transactions ACID dans MongoDB?", "answers": [
                    {"text": "Support des transactions multi-documents (depuis v4.0) avec atomicité et isolation", "is_correct": True},
                    {"text": "Pas de support de transactions", "is_correct": False},
                    {"text": "Transactions uniquement sur un document", "is_correct": False},
                    {"text": "Transactions avec rollback manuel", "is_correct": False}
                ]},
                {"text": "Comment optimiser les performances de lecture dans MongoDB?", "answers": [
                    {"text": "Index appropriés, projection limitée, hint(), éviter les requêtes sans index", "is_correct": True},
                    {"text": "Augmenter la RAM uniquement", "is_correct": False},
                    {"text": "Désactiver le journal", "is_correct": False},
                    {"text": "Utiliser des requêtes JavaScript", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "MongoDB - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que le Change Streams dans MongoDB?", "answers": [
                    {"text": "Un flux en temps réel des changements dans la base de données (insert, update, delete)", "is_correct": True},
                    {"text": "Un stream de logs d'erreurs", "is_correct": False},
                    {"text": "Un outil de migration de données", "is_correct": False},
                    {"text": "Un système de backup incrémental", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le stockage WiredTiger?", "answers": [
                    {"text": "Moteur de stockage par défaut avec compression, contrôle de concurrence MVCC, cache", "is_correct": True},
                    {"text": "Un système de fichiers distribué", "is_correct": False},
                    {"text": "Un moteur de recherche textuelle", "is_correct": False},
                    {"text": "Une interface de stockage cloud", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le MongoDB Atlas?", "answers": [
                    {"text": "Le service cloud managé MongoDB (DBaaS) avec backup, scaling, monitoring automatiques", "is_correct": True},
                    {"text": "Un outil de visualisation de données", "is_correct": False},
                    {"text": "Un client graphique pour MongoDB", "is_correct": False},
                    {"text": "Un serveur MongoDB on-premise", "is_correct": False}
                ]},
                {"text": "Comment fonctionne la sécurité dans MongoDB?", "answers": [
                    {"text": "Authentification (SCRAM, x.509), autorisation RBAC, TLS/SSL, audit, encryption-at-rest", "is_correct": True},
                    {"text": "MongoDB est sécurisé par défaut", "is_correct": False},
                    {"text": "Avec un firewall uniquement", "is_correct": False},
                    {"text": "Par l'isolation réseau seulement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que l'agrégation $facet dans MongoDB?", "answers": [
                    {"text": "Exécute plusieurs pipelines d'agrégation en parallèle sur les mêmes documents d'entrée", "is_correct": True},
                    {"text": "Une facette de recherche multicritère", "is_correct": False},
                    {"text": "Un groupement hiérarchique", "is_correct": False},
                    {"text": "Un opérateur de jointure", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le géospatial dans MongoDB?", "answers": [
                    {"text": "Support des requêtes géospatiales (GeoJSON, $near, $geoWithin, index 2dsphere)", "is_correct": True},
                    {"text": "MongoDB ne supporte pas le géospatial", "is_correct": False},
                    {"text": "Avec des plugins externes", "is_correct": False},
                    {"text": "Uniquement avec des coordonnées simples", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Bucket Pattern dans MongoDB?", "answers": [
                    {"text": "Design pattern pour optimiser le stockage de données temporelles en les regroupant", "is_correct": True},
                    {"text": "Un pattern de partitionnement", "is_correct": False},
                    {"text": "Une stratégie de sharding", "is_correct": False},
                    {"text": "Un format de document", "is_correct": False}
                ]},
                {"text": "Comment gérer les données relationnelles dans MongoDB?", "answers": [
                    {"text": "Par embedding (documents imbriqués) ou referencing (références manuelles ou DBRef)", "is_correct": True},
                    {"text": "MongoDB ne peut pas gérer de relations", "is_correct": False},
                    {"text": "Avec des jointures SQL", "is_correct": False},
                    {"text": "En créant des tables virtuelles", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Aggregation Pipeline Optimization?", "answers": [
                    {"text": "Optimisations automatiques (projection précoce, filtres push-down, utilisation d'index)", "is_correct": True},
                    {"text": "Une optimisation manuelle des requêtes", "is_correct": False},
                    {"text": "Un mode debug d'agrégation", "is_correct": False},
                    {"text": "Un cache de pipelines", "is_correct": False}
                ]},
                {"text": "Comment faire du full-text search dans MongoDB?", "answers": [
                    {"text": "Avec des index de texte et l'opérateur $text ($search)", "is_correct": True},
                    {"text": "MongoDB n'a pas de recherche textuelle", "is_correct": False},
                    {"text": "Avec des expressions régulières uniquement", "is_correct": False},
                    {"text": "Avec Atlas Search (Lucene intégré)", "is_correct": True}
                ]},
            ],
        },
    },
}

# 5. OUTILS ET INFRASTRUCTURE
# -----------------------------------------------------------------------------

GIT_DATA = {
    "category": {
        "name": "Git",
        "description": "Quiz pour maîtriser Git et la gestion de versions",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Git - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Quelle commande initialise un nouveau dépôt Git?", "answers": [
                    {"text": "git init", "is_correct": True},
                    {"text": "git start", "is_correct": False},
                    {"text": "git create", "is_correct": False},
                    {"text": "git new", "is_correct": False}
                ]},
                {"text": "Comment ajouter tous les fichiers modifiés au staging area?", "answers": [
                    {"text": "git add .", "is_correct": True},
                    {"text": "git stage all", "is_correct": False},
                    {"text": "git commit --all", "is_correct": False},
                    {"text": "git push all", "is_correct": False}
                ]},
                {"text": "Comment créer un commit avec un message?", "answers": [
                    {"text": "git commit -m 'mon message'", "is_correct": True},
                    {"text": "git save 'mon message'", "is_correct": False},
                    {"text": "git commit --message 'mon message'", "is_correct": False},
                    {"text": "git push -m 'mon message'", "is_correct": False}
                ]},
                {"text": "Quelle commande affiche l'historique des commits?", "answers": [
                    {"text": "git log", "is_correct": True},
                    {"text": "git history", "is_correct": False},
                    {"text": "git commits", "is_correct": False},
                    {"text": "git show-all", "is_correct": False}
                ]},
                {"text": "Comment créer une nouvelle branche?", "answers": [
                    {"text": "git branch nom-branche", "is_correct": True},
                    {"text": "git new-branch nom-branche", "is_correct": False},
                    {"text": "git create branch nom-branche", "is_correct": False},
                    {"text": "git checkout new nom-branche", "is_correct": False}
                ]},
                {"text": "Comment basculer sur une branche existante?", "answers": [
                    {"text": "git checkout nom-branche", "is_correct": True},
                    {"text": "git switch-to nom-branche", "is_correct": False},
                    {"text": "git go nom-branche", "is_correct": False},
                    {"text": "git use nom-branche", "is_correct": False}
                ]},
                {"text": "Comment envoyer les commits vers le dépôt distant?", "answers": [
                    {"text": "git push origin nom-branche", "is_correct": True},
                    {"text": "git upload origin nom-branche", "is_correct": False},
                    {"text": "git send origin nom-branche", "is_correct": False},
                    {"text": "git sync origin nom-branche", "is_correct": False}
                ]},
                {"text": "Comment récupérer et fusionner les changements distants?", "answers": [
                    {"text": "git pull", "is_correct": True},
                    {"text": "git fetch --merge", "is_correct": False},
                    {"text": "git download", "is_correct": False},
                    {"text": "git sync", "is_correct": False}
                ]},
                {"text": "Comment cloner un dépôt distant?", "answers": [
                    {"text": "git clone url-du-depot", "is_correct": True},
                    {"text": "git copy url-du-depot", "is_correct": False},
                    {"text": "git download url-du-depot", "is_correct": False},
                    {"text": "git init url-du-depot", "is_correct": False}
                ]},
                {"text": "Quelle commande affiche le statut des fichiers?", "answers": [
                    {"text": "git status", "is_correct": True},
                    {"text": "git check", "is_correct": False},
                    {"text": "git info", "is_correct": False},
                    {"text": "git show", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Git - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Quelle est la différence entre git merge et git rebase?", "answers": [
                    {"text": "rebase réécrit l'historique en linéarisant les commits, merge crée un commit de fusion", "is_correct": True},
                    {"text": "merge est plus sécurisé car il ne modifie jamais l'historique", "is_correct": False},
                    {"text": "rebase fusionne uniquement les fichiers, merge fusionne les branches", "is_correct": False},
                    {"text": "Aucune différence de résultat, seulement de performance", "is_correct": False}
                ]},
                {"text": "Que fait git stash?", "answers": [
                    {"text": "Sauvegarde temporairement les modifications non commitées pour nettoyer le working directory", "is_correct": True},
                    {"text": "Supprime toutes les modifications non commitées", "is_correct": False},
                    {"text": "Crée une branche temporaire avec les modifications", "is_correct": False},
                    {"text": "Archive les anciens commits", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un conflit de merge?", "answers": [
                    {"text": "Quand deux branches ont modifié les mêmes lignes et Git ne peut pas fusionner automatiquement", "is_correct": True},
                    {"text": "Quand une branche est trop ancienne pour être fusionnée", "is_correct": False},
                    {"text": "Quand deux développeurs pushent en même temps", "is_correct": False},
                    {"text": "Quand le dépôt distant refuse la fusion", "is_correct": False}
                ]},
                {"text": "Comment annuler le dernier commit en gardant les modifications?", "answers": [
                    {"text": "git reset --soft HEAD~1", "is_correct": True},
                    {"text": "git undo last", "is_correct": False},
                    {"text": "git revert HEAD", "is_correct": False},
                    {"text": "git reset --hard HEAD~1", "is_correct": False}
                ]},
                {"text": "Que fait git cherry-pick?", "answers": [
                    {"text": "Applique les modifications d'un commit spécifique sur la branche courante", "is_correct": True},
                    {"text": "Sélectionne les meilleurs commits pour un release", "is_correct": False},
                    {"text": "Fusionne sélectivement certains fichiers d'une branche", "is_correct": False},
                    {"text": "Copie une branche entière dans une autre", "is_correct": False}
                ]},
                {"text": "Comment créer et basculer sur une branche en une seule commande?", "answers": [
                    {"text": "git checkout -b nom-branche", "is_correct": True},
                    {"text": "git branch -m nom-branche", "is_correct": False},
                    {"text": "git new -b nom-branche", "is_correct": False},
                    {"text": "git branch --switch nom-branche", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un tag Git?", "answers": [
                    {"text": "Un pointeur nommé vers un commit spécifique, souvent utilisé pour les releases", "is_correct": True},
                    {"text": "Un label sur une branche pour la retrouver facilement", "is_correct": False},
                    {"text": "Un commentaire attaché à un commit", "is_correct": False},
                    {"text": "Une branche permanente qui ne peut pas être supprimée", "is_correct": False}
                ]},
                {"text": "Que fait git fetch (sans merge)?", "answers": [
                    {"text": "Télécharge les changements distants sans les fusionner dans la branche locale", "is_correct": True},
                    {"text": "Met à jour uniquement le fichier .gitconfig", "is_correct": False},
                    {"text": "Télécharge et applique automatiquement les changements", "is_correct": False},
                    {"text": "Synchronise uniquement les tags", "is_correct": False}
                ]},
                {"text": "Comment voir les différences entre deux branches?", "answers": [
                    {"text": "git diff branche1..branche2", "is_correct": True},
                    {"text": "git compare branche1 branche2", "is_correct": False},
                    {"text": "git show branche1 vs branche2", "is_correct": False},
                    {"text": "git branch --diff branche1 branche2", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un fichier .gitignore?", "answers": [
                    {"text": "Un fichier listant les patterns de fichiers/dossiers que Git doit ignorer", "is_correct": True},
                    {"text": "Un fichier qui désactive Git dans un sous-dossier", "is_correct": False},
                    {"text": "Un fichier de configuration des droits d'accès", "is_correct": False},
                    {"text": "Un fichier qui liste les collaborateurs exclus", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Git - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Quelle est la différence entre git reset --soft, --mixed et --hard?", "answers": [
                    {"text": "--soft garde staging+working, --mixed réinitialise staging, --hard réinitialise tout", "is_correct": True},
                    {"text": "--soft est le plus destructif, --hard le plus sûr", "is_correct": False},
                    {"text": "--hard garde les modifications en stash, --soft les supprime", "is_correct": False},
                    {"text": "Les trois font la même chose avec des performances différentes", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un rebase interactif (git rebase -i)?", "answers": [
                    {"text": "Permet de réécrire l'historique : réordonner, squash, edit, drop des commits", "is_correct": True},
                    {"text": "Lance un rebase avec confirmation pour chaque commit", "is_correct": False},
                    {"text": "Ouvre une interface graphique pour le rebase", "is_correct": False},
                    {"text": "Effectue un rebase en mode interactif entre deux dépôts", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que git reflog?", "answers": [
                    {"text": "Un journal de tous les mouvements de HEAD permettant de récupérer des commits perdus", "is_correct": True},
                    {"text": "Un log des références distantes synchronisées", "is_correct": False},
                    {"text": "L'historique des modifications du fichier .gitconfig", "is_correct": False},
                    {"text": "Un log filtré des commits de références (tags)", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un submodule Git?", "answers": [
                    {"text": "Un dépôt Git imbriqué dans un autre dépôt, référencé par un commit spécifique", "is_correct": True},
                    {"text": "Un sous-dossier avec ses propres règles .gitignore", "is_correct": False},
                    {"text": "Un module npm intégré dans le dépôt Git", "is_correct": False},
                    {"text": "Une branche qui agit comme un dépôt indépendant", "is_correct": False}
                ]},
                {"text": "Que fait git bisect?", "answers": [
                    {"text": "Une recherche binaire dans l'historique pour trouver le commit ayant introduit un bug", "is_correct": True},
                    {"text": "Divise un commit en deux commits plus petits", "is_correct": False},
                    {"text": "Compare deux branches ligne par ligne", "is_correct": False},
                    {"text": "Crée deux branches symétriques à partir d'un commit", "is_correct": False}
                ]},
                {"text": "Comment signer cryptographiquement un commit Git?", "answers": [
                    {"text": "git commit -S -m 'message' avec une clé GPG configurée", "is_correct": True},
                    {"text": "git commit --sign -m 'message' avec un certificat SSL", "is_correct": False},
                    {"text": "git commit --verified -m 'message'", "is_correct": False},
                    {"text": "Les commits sont signés automatiquement avec le SSH key", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que git worktree?", "answers": [
                    {"text": "Permet d'avoir plusieurs working directories pour différentes branches simultanément", "is_correct": True},
                    {"text": "Un outil pour gérer l'arborescence des fichiers du dépôt", "is_correct": False},
                    {"text": "Un visualiseur de l'arbre de commits", "is_correct": False},
                    {"text": "Un système de verrouillage de fichiers pour les équipes", "is_correct": False}
                ]},
                {"text": "Comment squash plusieurs commits en un seul?", "answers": [
                    {"text": "git rebase -i HEAD~n puis changer 'pick' en 'squash' pour les commits à fusionner", "is_correct": True},
                    {"text": "git merge --squash nom-branche", "is_correct": False},
                    {"text": "git commit --squash HEAD~n", "is_correct": False},
                    {"text": "git rebase --squash n", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un hook Git?", "answers": [
                    {"text": "Des scripts exécutés automatiquement lors d'événements Git (pre-commit, post-push, etc.)", "is_correct": True},
                    {"text": "Un point d'ancrage pour connecter plusieurs dépôts entre eux", "is_correct": False},
                    {"text": "Un système de webhooks vers des services externes", "is_correct": False},
                    {"text": "Un mécanisme pour accrocher des branches à des tags", "is_correct": False}
                ]},
                {"text": "Que fait git filter-branch ou git filter-repo?", "answers": [
                    {"text": "Réécrit l'historique Git en masse (supprimer un fichier sensible de tous les commits)", "is_correct": True},
                    {"text": "Filtre les branches selon des critères de nom", "is_correct": False},
                    {"text": "Applique des filtres de merge pour résoudre les conflits automatiquement", "is_correct": False},
                    {"text": "Crée un nouveau dépôt avec seulement les branches filtrées", "is_correct": False}
                ]},
            ],
        },
    },
}

DOCKER_DATA = {
    "category": {
        "name": "Docker",
        "description": "Quiz pour maîtriser Docker et la conteneurisation",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Docker - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce qu'un conteneur Docker?", "answers": [
                    {"text": "Une machine virtuelle légère", "is_correct": False},
                    {"text": "Un environnement d'exécution isolé et léger qui empaquette une application et ses dépendances", "is_correct": True},
                    {"text": "Un fichier de configuration d'application", "is_correct": False},
                    {"text": "Un serveur dédié dans le cloud", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'une image Docker?", "answers": [
                    {"text": "Un template immuable servant de base pour créer des conteneurs", "is_correct": True},
                    {"text": "Une capture d'écran d'un conteneur en cours d'exécution", "is_correct": False},
                    {"text": "Un fichier de configuration Docker", "is_correct": False},
                    {"text": "Une sauvegarde d'un conteneur arrêté", "is_correct": False}
                ]},
                {"text": "Quelle commande lance un conteneur Docker?", "answers": [
                    {"text": "docker run image-name", "is_correct": True},
                    {"text": "docker exec image-name", "is_correct": False},
                    {"text": "docker launch image-name", "is_correct": False},
                    {"text": "docker start image-name", "is_correct": False}
                ]},
                {"text": "Comment lister les conteneurs en cours d'exécution?", "answers": [
                    {"text": "docker ps", "is_correct": True},
                    {"text": "docker containers", "is_correct": False},
                    {"text": "docker list", "is_correct": False},
                    {"text": "docker show", "is_correct": False}
                ]},
                {"text": "Quel fichier définit comment construire une image Docker?", "answers": [
                    {"text": "Dockerfile", "is_correct": True},
                    {"text": "build.docker", "is_correct": False},
                    {"text": "docker-config.yml", "is_correct": False},
                    {"text": "container.json", "is_correct": False}
                ]},
                {"text": "Comment construire une image depuis un Dockerfile?", "answers": [
                    {"text": "docker build -t nom-image .", "is_correct": True},
                    {"text": "docker compile nom-image .", "is_correct": False},
                    {"text": "docker create -t nom-image .", "is_correct": False},
                    {"text": "docker make -t nom-image", "is_correct": False}
                ]},
                {"text": "Comment arrêter un conteneur Docker?", "answers": [
                    {"text": "docker stop container-id", "is_correct": True},
                    {"text": "docker halt container-id", "is_correct": False},
                    {"text": "docker kill container-id", "is_correct": False},
                    {"text": "docker end container-id", "is_correct": False}
                ]},
                {"text": "Quelle instruction Dockerfile définit l'image de base?", "answers": [
                    {"text": "FROM", "is_correct": True},
                    {"text": "BASE", "is_correct": False},
                    {"text": "INHERIT", "is_correct": False},
                    {"text": "IMAGE", "is_correct": False}
                ]},
                {"text": "Comment mapper un port du conteneur vers l'hôte?", "answers": [
                    {"text": "docker run -p 8080:80 image-name", "is_correct": True},
                    {"text": "docker run --expose 8080:80 image-name", "is_correct": False},
                    {"text": "docker run --port 8080:80 image-name", "is_correct": False},
                    {"text": "docker run -map 8080:80 image-name", "is_correct": False}
                ]},
                {"text": "Quelle commande télécharge une image depuis Docker Hub?", "answers": [
                    {"text": "docker pull nom-image", "is_correct": True},
                    {"text": "docker get nom-image", "is_correct": False},
                    {"text": "docker fetch nom-image", "is_correct": False},
                    {"text": "docker download nom-image", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Docker - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que Docker Compose?", "answers": [
                    {"text": "Un outil pour définir et gérer des applications multi-conteneurs via un fichier YAML", "is_correct": True},
                    {"text": "Un éditeur de Dockerfile graphique", "is_correct": False},
                    {"text": "Un orchestrateur de conteneurs en production", "is_correct": False},
                    {"text": "Un outil pour optimiser la taille des images", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre COPY et ADD dans un Dockerfile?", "answers": [
                    {"text": "ADD supporte les URLs et l'extraction d'archives tar, COPY est plus simple et préféré", "is_correct": True},
                    {"text": "COPY copie depuis l'hôte, ADD depuis un autre conteneur", "is_correct": False},
                    {"text": "Aucune différence fonctionnelle", "is_correct": False},
                    {"text": "COPY est plus rapide, ADD est plus complet", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un volume Docker?", "answers": [
                    {"text": "Un mécanisme pour persister les données en dehors du cycle de vie du conteneur", "is_correct": True},
                    {"text": "La taille maximale allouée à un conteneur", "is_correct": False},
                    {"text": "Un espace de stockage temporaire dans le conteneur", "is_correct": False},
                    {"text": "Un système de fichiers partagé entre images", "is_correct": False}
                ]},
                {"text": "Que fait l'instruction ENTRYPOINT dans un Dockerfile?", "answers": [
                    {"text": "Définit le processus principal qui s'exécute au démarrage du conteneur", "is_correct": True},
                    {"text": "Expose un port du conteneur", "is_correct": False},
                    {"text": "Définit le répertoire de travail dans le conteneur", "is_correct": False},
                    {"text": "Définit les variables d'environnement au démarrage", "is_correct": False}
                ]},
                {"text": "Comment exécuter une commande dans un conteneur en cours d'exécution?", "answers": [
                    {"text": "docker exec -it container-id bash", "is_correct": True},
                    {"text": "docker attach container-id bash", "is_correct": False},
                    {"text": "docker connect container-id bash", "is_correct": False},
                    {"text": "docker run container-id bash", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un réseau Docker (Docker network)?", "answers": [
                    {"text": "Un espace réseau isolé permettant aux conteneurs de communiquer entre eux", "is_correct": True},
                    {"text": "La configuration réseau de l'hôte Docker", "is_correct": False},
                    {"text": "Un pare-feu pour les conteneurs", "is_correct": False},
                    {"text": "Un proxy réseau pour les conteneurs", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le multi-stage build?", "answers": [
                    {"text": "Utiliser plusieurs instructions FROM pour réduire la taille finale de l'image", "is_correct": True},
                    {"text": "Déployer l'image sur plusieurs environnements simultanément", "is_correct": False},
                    {"text": "Versionner une image avec plusieurs tags", "is_correct": False},
                    {"text": "Construire une image en plusieurs étapes parallèles", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre CMD et ENTRYPOINT?", "answers": [
                    {"text": "ENTRYPOINT est le processus principal (difficilement remplaçable), CMD fournit les arguments par défaut (remplaçables)", "is_correct": True},
                    {"text": "CMD s'exécute au build, ENTRYPOINT au runtime", "is_correct": False},
                    {"text": "Aucune différence, ils sont interchangeables", "is_correct": False},
                    {"text": "ENTRYPOINT permet plusieurs commandes, CMD une seule", "is_correct": False}
                ]},
                {"text": "Comment voir les logs d'un conteneur Docker?", "answers": [
                    {"text": "docker logs container-id", "is_correct": True},
                    {"text": "docker inspect container-id --logs", "is_correct": False},
                    {"text": "docker show-logs container-id", "is_correct": False},
                    {"text": "docker output container-id", "is_correct": False}
                ]},
                {"text": "Comment supprimer toutes les images Docker non utilisées?", "answers": [
                    {"text": "docker image prune -a", "is_correct": True},
                    {"text": "docker remove unused", "is_correct": False},
                    {"text": "docker rmi --all", "is_correct": False},
                    {"text": "docker clean images", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Docker - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que Docker Swarm?", "answers": [
                    {"text": "Le mode d'orchestration natif de Docker pour gérer un cluster de nœuds", "is_correct": True},
                    {"text": "Un outil de monitoring pour les conteneurs Docker", "is_correct": False},
                    {"text": "Un gestionnaire de volumes distribués", "is_correct": False},
                    {"text": "Un système de load balancing pour une seule machine", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le cache des layers dans Docker?", "answers": [
                    {"text": "Chaque instruction Dockerfile crée un layer ; si le layer n'a pas changé, Docker réutilise le cache", "is_correct": True},
                    {"text": "Le cache est partagé entre tous les utilisateurs du système", "is_correct": False},
                    {"text": "Docker n'utilise pas de cache, il reconstruit toujours depuis zéro", "is_correct": False},
                    {"text": "Docker cache uniquement la dernière image construite", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Docker Registry?", "answers": [
                    {"text": "Un serveur de stockage et distribution d'images Docker (public comme Docker Hub ou privé)", "is_correct": True},
                    {"text": "Un outil de configuration centralisée pour les conteneurs", "is_correct": False},
                    {"text": "La base de données interne de Docker", "is_correct": False},
                    {"text": "Le registre Windows pour les conteneurs Docker", "is_correct": False}
                ]},
                {"text": "Comment limiter les ressources CPU et mémoire d'un conteneur?", "answers": [
                    {"text": "docker run --memory='512m' --cpus='0.5' image-name", "is_correct": True},
                    {"text": "docker run --resources cpu=0.5,mem=512 image-name", "is_correct": False},
                    {"text": "docker run --limit '512m:0.5cpu' image-name", "is_correct": False},
                    {"text": "docker run --max-memory=512 --max-cpu=50% image-name", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le namespacing dans Docker?", "answers": [
                    {"text": "Un mécanisme Linux qui isole les ressources (PID, réseau, filesystem...) entre conteneurs", "is_correct": True},
                    {"text": "Un système de nommage des images et conteneurs", "is_correct": False},
                    {"text": "Un mécanisme de routage réseau entre conteneurs", "is_correct": False},
                    {"text": "Un outil pour organiser les images par namespace dans un registry", "is_correct": False}
                ]},
                {"text": "Comment créer un secret Docker Swarm?", "answers": [
                    {"text": "echo 'valeur' | docker secret create nom-secret -", "is_correct": True},
                    {"text": "docker config create --secret nom-secret 'valeur'", "is_correct": False},
                    {"text": "docker env set SECRET=valeur", "is_correct": False},
                    {"text": "docker secret add nom-secret 'valeur'", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Docker BuildKit?", "answers": [
                    {"text": "Un backend de build amélioré offrant de meilleures performances, cache et fonctionnalités (builds parallèles, secrets de build)", "is_correct": True},
                    {"text": "Un toolkit pour créer des images Docker depuis des scripts shell", "is_correct": False},
                    {"text": "Un compilateur spécial pour optimiser les Dockerfile", "is_correct": False},
                    {"text": "Un plugin pour intégrer Docker dans les IDE", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre un bind mount et un volume Docker?", "answers": [
                    {"text": "Un bind mount pointe vers un chemin spécifique de l'hôte, un volume est géré par Docker (plus portable)", "is_correct": True},
                    {"text": "Les volumes existent uniquement dans Docker Swarm", "is_correct": False},
                    {"text": "Un bind mount est plus performant que les volumes dans tous les cas", "is_correct": False},
                    {"text": "Un volume est temporaire, un bind mount est persistant", "is_correct": False}
                ]},
                {"text": "Comment inspecter les détails complets d'un conteneur?", "answers": [
                    {"text": "docker inspect container-id", "is_correct": True},
                    {"text": "docker info container-id", "is_correct": False},
                    {"text": "docker details container-id", "is_correct": False},
                    {"text": "docker describe container-id", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que cgroups dans le contexte Docker?", "answers": [
                    {"text": "Un mécanisme Linux de limitation et monitoring des ressources (CPU, mémoire, I/O) par groupe de processus", "is_correct": True},
                    {"text": "Un système de groupes de conteneurs dans Docker Compose", "is_correct": False},
                    {"text": "Un outil de clustering pour les conteneurs", "is_correct": False},
                    {"text": "Un gestionnaire de groupes d'utilisateurs pour les permissions Docker", "is_correct": False}
                ]},
            ],
        },
    },
}

KUBERNETES_DATA = {
    "category": {
        "name": "Kubernetes",
        "description": "Quiz pour maîtriser Kubernetes et l'orchestration de conteneurs",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/kubernetes/kubernetes-plain.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Kubernetes - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que Kubernetes?", "answers": [
                    {"text": "Une plateforme open-source d'orchestration de conteneurs (déploiement, scaling, gestion)", "is_correct": True},
                    {"text": "Un gestionnaire de paquets Docker", "is_correct": False},
                    {"text": "Un cloud provider comme AWS", "is_correct": False},
                    {"text": "Un type de conteneur", "is_correct": False}
                ]},
                {"text": "Quelle est l'unité de déploiement de base dans Kubernetes?", "answers": [
                    {"text": "Pod", "is_correct": True},
                    {"text": "Container", "is_correct": False},
                    {"text": "Service", "is_correct": False},
                    {"text": "Node", "is_correct": False}
                ]},
                {"text": "Comment définir un déploiement Kubernetes?", "answers": [
                    {"text": "Avec un fichier YAML contenant kind: Deployment", "is_correct": True},
                    {"text": "Avec docker-compose.yml", "is_correct": False},
                    {"text": "Avec kubectl run", "is_correct": False},
                    {"text": "Avec un script shell", "is_correct": False}
                ]},
                {"text": "Quelle commande applique une configuration Kubernetes?", "answers": [
                    {"text": "kubectl apply -f fichier.yaml", "is_correct": True},
                    {"text": "kubectl create -f fichier.yaml", "is_correct": False},
                    {"text": "kubectl deploy -f fichier.yaml", "is_correct": False},
                    {"text": "kubectl run -f fichier.yaml", "is_correct": False}
                ]},
                {"text": "Comment lister tous les pods d'un namespace?", "answers": [
                    {"text": "kubectl get pods", "is_correct": True},
                    {"text": "kubectl list pods", "is_correct": False},
                    {"text": "kubectl show pods", "is_correct": False},
                    {"text": "kubectl describe pods", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Service dans Kubernetes?", "answers": [
                    {"text": "Une abstraction qui expose un ensemble de pods comme un service réseau", "is_correct": True},
                    {"text": "Un microservice déployé", "is_correct": False},
                    {"text": "Un service de monitoring", "is_correct": False},
                    {"text": "Une application métier", "is_correct": False}
                ]},
                {"text": "Quel composant gère le contrôle et l'état du cluster?", "answers": [
                    {"text": "Control Plane (API Server, etcd, Scheduler, Controller Manager)", "is_correct": True},
                    {"text": "Kubelet", "is_correct": False},
                    {"text": "Container Runtime", "is_correct": False},
                    {"text": "kube-proxy", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Namespace Kubernetes?", "answers": [
                    {"text": "Un mécanisme pour partitionner un cluster en sous-clusters virtuels", "is_correct": True},
                    {"text": "Un espace de noms DNS", "is_correct": False},
                    {"text": "Un namespace Linux", "is_correct": False},
                    {"text": "Un groupe de pods", "is_correct": False}
                ]},
                {"text": "Comment exposer un déploiement en externe?", "answers": [
                    {"text": "Créer un Service de type LoadBalancer ou NodePort", "is_correct": True},
                    {"text": "kubectl expose deployment", "is_correct": False},
                    {"text": "Avec un Ingress uniquement", "is_correct": False},
                    {"text": "Le déploiement est exposé par défaut", "is_correct": False}
                ]},
                {"text": "Quelle commande affiche les logs d'un pod?", "answers": [
                    {"text": "kubectl logs nom-pod", "is_correct": True},
                    {"text": "kubectl logs pod/nom-pod", "is_correct": False},
                    {"text": "docker logs nom-pod", "is_correct": False},
                    {"text": "kubectl get logs nom-pod", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Kubernetes - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Quelle est la différence entre Deployment et StatefulSet?", "answers": [
                    {"text": "StatefulSet donne des identités stables et ordre de démarrage/arrêt; Deployment pour apps stateless", "is_correct": True},
                    {"text": "Deployment est pour les bases de données, StatefulSet pour les apps web", "is_correct": False},
                    {"text": "StatefulSet est obsolète", "is_correct": False},
                    {"text": "Aucune différence majeure", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un ConfigMap?", "answers": [
                    {"text": "Une ressource pour stocker des configurations non sensibles (variables d'env, fichiers)", "is_correct": True},
                    {"text": "Une carte de configuration réseau", "is_correct": False},
                    {"text": "Un secret non chiffré", "is_correct": False},
                    {"text": "Un mapping de ports", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Ingress Controller?", "answers": [
                    {"text": "Un composant qui gère les règles Ingress pour router le trafic HTTP/HTTPS vers les Services", "is_correct": True},
                    {"text": "Un contrôleur d'entrée dans le cluster", "is_correct": False},
                    {"text": "Un load balancer interne", "is_correct": False},
                    {"text": "Un plugin de sécurité réseau", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le rolling update dans Kubernetes?", "answers": [
                    {"text": "Met à jour progressivement les pods avec stratégie RollingUpdate (max surge, max unavailable)", "is_correct": True},
                    {"text": "Supprime tous les pods puis recrée", "is_correct": False},
                    {"text": "Met à jour en parallèle sans interruption", "is_correct": False},
                    {"text": "Nécessite un arrêt manuel", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Probes (liveness, readiness, startup) dans Kubernetes?", "answers": [
                    {"text": "Des vérifications de santé pour savoir si un pod est vivant, prêt à servir, ou démarré", "is_correct": True},
                    {"text": "Des sondes de performance réseau", "is_correct": False},
                    {"text": "Des outils de débogage", "is_correct": False},
                    {"text": "Des métriques de monitoring", "is_correct": False}
                ]},
                {"text": "Comment gérer les secrets dans Kubernetes?", "answers": [
                    {"text": "Avec les ressources Secret (encodées en base64) et montées comme volumes ou variables d'env", "is_correct": True},
                    {"text": "En les stockant en clair dans ConfigMap", "is_correct": False},
                    {"text": "Avec un secret manager externe uniquement", "is_correct": False},
                    {"text": "Kubernetes ne gère pas les secrets", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Helm dans l'écosystème Kubernetes?", "answers": [
                    {"text": "Un package manager (chart) pour déployer des applications complexes facilement", "is_correct": True},
                    {"text": "Un outil de monitoring Kubernetes", "is_correct": False},
                    {"text": "Un gestionnaire de ressources Helm", "is_correct": False},
                    {"text": "Un shell pour Kubernetes", "is_correct": False}
                ]},
                {"text": "Comment faire du scaling automatique dans Kubernetes?", "answers": [
                    {"text": "Avec HorizontalPodAutoscaler (HPA) basé sur métriques CPU/mémoire ou custom", "is_correct": True},
                    {"text": "En modifiant manuellement le nombre de replicas", "is_correct": False},
                    {"text": "Avec un script cron", "is_correct": False},
                    {"text": "Le scaling est automatique par défaut", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le RBAC dans Kubernetes?", "answers": [
                    {"text": "Role-Based Access Control - gestion des permissions via rôles et bindings", "is_correct": True},
                    {"text": "Un contrôle d'accès réseau", "is_correct": False},
                    {"text": "Un système de routage", "is_correct": False},
                    {"text": "Une base de données d'authentification", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre NodePort, LoadBalancer et ClusterIP?", "answers": [
                    {"text": "ClusterIP: interne; NodePort: port fixe sur chaque node; LoadBalancer: expose via cloud LB", "is_correct": True},
                    {"text": "Ce sont tous des types de volumes", "is_correct": False},
                    {"text": "ClusterIP est obsolète", "is_correct": False},
                    {"text": "NodePort est le plus sécurisé", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Kubernetes - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que les Custom Resource Definitions (CRD) dans Kubernetes?", "answers": [
                    {"text": "Étendre l'API Kubernetes avec des ressources personnalisées pour gérer des applications custom", "is_correct": True},
                    {"text": "Des définitions de ressources système", "is_correct": False},
                    {"text": "Des templates de déploiement", "is_correct": False},
                    {"text": "Des configurations de quotas", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Operators dans Kubernetes?", "answers": [
                    {"text": "Des applications qui automatisent la gestion d'applications complexes via CRD et controllers", "is_correct": True},
                    {"text": "Des opérateurs mathématiques dans les labels", "is_correct": False},
                    {"text": "Des utilisateurs avec droits admin", "is_correct": False},
                    {"text": "Des scripts d'opération manuelle", "is_correct": False}
                ]},
                {"text": "Comment implémenter la sécurité réseau avec Network Policies?", "answers": [
                    {"text": "Définir des règles de trafic entrant/sortant entre pods basées sur labels et namespaces", "is_correct": True},
                    {"text": "Avec des pare-feu externes uniquement", "is_correct": False},
                    {"text": "En configurant iptables manuellement", "is_correct": False},
                    {"text": "Kubernetes a un firewall intégré par défaut", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le CSI (Container Storage Interface)?", "answers": [
                    {"text": "Une interface standard pour exposer des systèmes de stockage arbitraires aux conteneurs", "is_correct": True},
                    {"text": "Une interface de sécurité pour conteneurs", "is_correct": False},
                    {"text": "Un protocole de communication entre pods", "is_correct": False},
                    {"text": "Un système de fichiers distribué", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Service Mesh (comme Istio) dans Kubernetes?", "answers": [
                    {"text": "Une couche d'infrastructure pour gérer la communication service-to-service (traffic, security, observability)", "is_correct": True},
                    {"text": "Un maillage de services réseau", "is_correct": False},
                    {"text": "Un load balancer avancé", "is_correct": False},
                    {"text": "Un proxy pour les requêtes HTTP", "is_correct": False}
                ]},
                {"text": "Comment gérer les quotas de ressources dans un namespace?", "answers": [
                    {"text": "Avec ResourceQuota pour limiter CPU/mémoire total, nombre de pods, services, etc.", "is_correct": True},
                    {"text": "En limitant les utilisateurs RBAC", "is_correct": False},
                    {"text": "En définissant des requests/limits sur chaque pod", "is_correct": False},
                    {"text": "Kubernetes alloue automatiquement les ressources", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Vertical Pod Autoscaler (VPA)?", "answers": [
                    {"text": "Ajuste automatiquement les requests/limits CPU/mémoire des pods basé sur l'utilisation passée", "is_correct": True},
                    {"text": "Ajoute des pods verticalement (stack)", "is_correct": False},
                    {"text": "Un autoscaler pour les volumes", "is_correct": False},
                    {"text": "Un outil de scaling des nodes", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les PodDisruptionBudget (PDB)?", "answers": [
                    {"text": "Garantit un nombre minimum de pods disponibles lors d'événements disruptifs (maintenance)", "is_correct": True},
                    {"text": "Un budget pour les interruptions réseau", "is_correct": False},
                    {"text": "Une politique de disruption de pods", "is_correct": False},
                    {"text": "Un outil de planification de downtime", "is_correct": False}
                ]},
                {"text": "Comment fonctionne etcd dans Kubernetes?", "answers": [
                    {"text": "Le stockage clé-valeur distribué qui stocke toute la configuration et l'état du cluster", "is_correct": True},
                    {"text": "Une base de données pour les logs", "is_correct": False},
                    {"text": "Un cache distribué pour les secrets", "is_correct": False},
                    {"text": "Un système de fichiers etcd", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les PriorityClasses dans Kubernetes?", "answers": [
                    {"text": "Définir des priorités pour les pods, influençant l'ordonnancement et l'éviction", "is_correct": True},
                    {"text": "Des classes de priorité réseau", "is_correct": False},
                    {"text": "Un système de QoS avancé", "is_correct": False},
                    {"text": "Des niveaux d'accès RBAC", "is_correct": False}
                ]},
            ],
        },
    },
}

# 6. API ET COMMUNICATION
# -----------------------------------------------------------------------------

GRAPHQL_DATA = {
    "category": {
        "name": "GraphQL",
        "description": "Quiz pour maîtriser GraphQL et les API déclaratives",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/graphql/graphql-plain.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "GraphQL - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que GraphQL?", "answers": [
                    {"text": "Un langage de requête pour API et un runtime pour exécuter ces requêtes", "is_correct": True},
                    {"text": "Une base de données graphe", "is_correct": False},
                    {"text": "Un ORM pour bases de données relationnelles", "is_correct": False},
                    {"text": "Un protocole de communication réseau", "is_correct": False}
                ]},
                {"text": "Quel est l'avantage principal de GraphQL vs REST?", "answers": [
                    {"text": "Le client demande exactement les données dont il a besoin (pas d'over-fetching ni d'under-fetching)", "is_correct": True},
                    {"text": "GraphQL est toujours plus rapide que REST", "is_correct": False},
                    {"text": "GraphQL utilise moins de bande passante dans tous les cas", "is_correct": False},
                    {"text": "GraphQL fonctionne sans serveur", "is_correct": False}
                ]},
                {"text": "Comment s'appelle une requête de lecture en GraphQL?", "answers": [
                    {"text": "Query", "is_correct": True},
                    {"text": "GET", "is_correct": False},
                    {"text": "Fetch", "is_correct": False},
                    {"text": "Read", "is_correct": False}
                ]},
                {"text": "Comment s'appelle une opération de modification en GraphQL?", "answers": [
                    {"text": "Mutation", "is_correct": True},
                    {"text": "POST", "is_correct": False},
                    {"text": "Update", "is_correct": False},
                    {"text": "Write", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Schema en GraphQL?", "answers": [
                    {"text": "La définition des types, queries et mutations disponibles dans l'API", "is_correct": True},
                    {"text": "La configuration du serveur GraphQL", "is_correct": False},
                    {"text": "Le fichier de base de données", "is_correct": False},
                    {"text": "Le fichier de documentation de l'API", "is_correct": False}
                ]},
                {"text": "Sur quel protocole GraphQL fonctionne-t-il généralement?", "answers": [
                    {"text": "HTTP (généralement POST sur un seul endpoint /graphql)", "is_correct": True},
                    {"text": "TCP personnalisé", "is_correct": False},
                    {"text": "WebSocket uniquement", "is_correct": False},
                    {"text": "UDP pour la performance", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un resolver GraphQL?", "answers": [
                    {"text": "Une fonction qui retourne les données pour un champ spécifique du schema", "is_correct": True},
                    {"text": "Un outil de résolution des conflits de schema", "is_correct": False},
                    {"text": "Un middleware HTTP pour GraphQL", "is_correct": False},
                    {"text": "Un cache de requêtes GraphQL", "is_correct": False}
                ]},
                {"text": "Comment définir un type objet en GraphQL SDL?", "answers": [
                    {"text": "type User { id: ID! name: String! }", "is_correct": True},
                    {"text": "object User { id: ID, name: String }", "is_correct": False},
                    {"text": "class User { id: ID!, name: String! }", "is_correct": False},
                    {"text": "interface User { id: ID name: String }", "is_correct": False}
                ]},
                {"text": "Que signifie ! après un type en GraphQL?", "answers": [
                    {"text": "Le champ est non-null (obligatoire, ne peut pas être null)", "is_correct": True},
                    {"text": "Le champ est requis dans les mutations", "is_correct": False},
                    {"text": "Le champ est unique", "is_correct": False},
                    {"text": "Le champ est indexé", "is_correct": False}
                ]},
                {"text": "Comment s'appellent les mises à jour en temps réel en GraphQL?", "answers": [
                    {"text": "Subscriptions", "is_correct": True},
                    {"text": "Realtime Queries", "is_correct": False},
                    {"text": "LiveQueries", "is_correct": False},
                    {"text": "Events", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "GraphQL - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que le problème N+1 en GraphQL?", "answers": [
                    {"text": "Un resolver qui exécute N requêtes DB pour charger les enfants de N entités parentes", "is_correct": True},
                    {"text": "Dépasser le nombre maximum de champs dans une query", "is_correct": False},
                    {"text": "Une erreur de typage dans le schema", "is_correct": False},
                    {"text": "Un timeout après N requêtes simultanées", "is_correct": False}
                ]},
                {"text": "Quelle solution résout le problème N+1 en GraphQL?", "answers": [
                    {"text": "DataLoader - batch et cache des requêtes par clés", "is_correct": True},
                    {"text": "Pagination côté serveur", "is_correct": False},
                    {"text": "Mise en cache HTTP", "is_correct": False},
                    {"text": "Limiter la profondeur des requêtes", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Fragments GraphQL?", "answers": [
                    {"text": "Des unités réutilisables de champs partageables entre queries", "is_correct": True},
                    {"text": "Des parties de schema déclarées séparément", "is_correct": False},
                    {"text": "Des requêtes partielles optimisées", "is_correct": False},
                    {"text": "Des sous-resolvers de champs", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que l'introspection GraphQL?", "answers": [
                    {"text": "La capacité de GraphQL à répondre à des queries sur son propre schema", "is_correct": True},
                    {"text": "Un outil de débogage des resolvers", "is_correct": False},
                    {"text": "L'inspection du trafic réseau GraphQL", "is_correct": False},
                    {"text": "La vérification des types à l'exécution", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les directives GraphQL (@deprecated, @include...)?", "answers": [
                    {"text": "Des annotations sur le schema ou les requêtes qui modifient l'exécution ou la validation", "is_correct": True},
                    {"text": "Des commentaires dans le SDL", "is_correct": False},
                    {"text": "Des middlewares GraphQL", "is_correct": False},
                    {"text": "Des extensions du protocole HTTP pour GraphQL", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Variables en GraphQL?", "answers": [
                    {"text": "Des paramètres dynamiques passés séparément de la query pour éviter l'injection", "is_correct": True},
                    {"text": "Des variables JavaScript dans les resolvers", "is_correct": False},
                    {"text": "Des champs calculés dans le schema", "is_correct": False},
                    {"text": "Des constantes définies dans le schema", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Union Type en GraphQL?", "answers": [
                    {"text": "Un type qui peut être l'un de plusieurs types objets distincts", "is_correct": True},
                    {"text": "La fusion de deux types en un", "is_correct": False},
                    {"text": "Un type pour les valeurs mixtes (string | number)", "is_correct": False},
                    {"text": "Un type partagé entre plusieurs schemas", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que l'Apollo Client?", "answers": [
                    {"text": "Un client GraphQL complet avec cache, gestion d'état et hooks React", "is_correct": True},
                    {"text": "Un serveur GraphQL", "is_correct": False},
                    {"text": "Un framework de tests GraphQL", "is_correct": False},
                    {"text": "Un CLI pour GraphQL", "is_correct": False}
                ]},
                {"text": "Que sont les Input Types en GraphQL?", "answers": [
                    {"text": "Des types spéciaux utilisés comme arguments de mutation (pas pour les retours)", "is_correct": True},
                    {"text": "Les données reçues depuis le client HTTP", "is_correct": False},
                    {"text": "Des types pour les champs de formulaires", "is_correct": False},
                    {"text": "Des types identiques aux types objets standards", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Schema Stitching vs Federation?", "answers": [
                    {"text": "Stitching combine plusieurs schemas en un; Federation (Apollo) compose des sous-graphes distribués", "is_correct": True},
                    {"text": "Ce sont deux noms pour la même chose", "is_correct": False},
                    {"text": "Federation est obsolète, Stitching est recommandé", "is_correct": False},
                    {"text": "Stitching est pour les microservices, Federation pour les monolithes", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "GraphQL - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que la persisted queries en GraphQL?", "answers": [
                    {"text": "Stocker des queries côté serveur par hash pour réduire la taille des requêtes et améliorer la sécurité", "is_correct": True},
                    {"text": "Mettre en cache les résultats de queries dans Redis", "is_correct": False},
                    {"text": "Sauvegarder les queries favorites des utilisateurs", "is_correct": False},
                    {"text": "Précompiler les queries pour de meilleures performances", "is_correct": False}
                ]},
                {"text": "Comment implémenter la pagination cursor-based en GraphQL?", "answers": [
                    {"text": "Avec des connections (edges/nodes/pageInfo/cursor) suivant la spec Relay", "is_correct": True},
                    {"text": "Avec les paramètres page et limit standards", "is_correct": False},
                    {"text": "Avec offset et limit dans les arguments", "is_correct": False},
                    {"text": "En retournant un tableau paginé avec metadata", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que la Query Complexity Analysis?", "answers": [
                    {"text": "Calculer un score de complexité pour bloquer les queries trop coûteuses et prévenir les attaques DoS", "is_correct": True},
                    {"text": "Analyser les performances des resolvers", "is_correct": False},
                    {"text": "Valider la syntaxe d'une query GraphQL", "is_correct": False},
                    {"text": "Compter le nombre de champs dans une query", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Schema Directives custom en GraphQL?", "answers": [
                    {"text": "Des directives personnalisées avec logique custom pouvant transformer les types/fields/args au niveau schema", "is_correct": True},
                    {"text": "Des annotations de documentation personnalisées", "is_correct": False},
                    {"text": "Des permissions déclaratives sur le schema", "is_correct": False},
                    {"text": "Des middlewares déclarés dans le SDL", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Defer et Stream en GraphQL?", "answers": [
                    {"text": "@defer permet d'envoyer des parties non-critiques de la réponse plus tard; @stream pour les listes en streaming", "is_correct": True},
                    {"text": "Des directives pour mettre en cache les résultats", "is_correct": False},
                    {"text": "Des directives pour les opérations asynchrones", "is_correct": False},
                    {"text": "Des directives pour différer les mutations", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Apollo Federation?", "answers": [
                    {"text": "Une architecture pour composer plusieurs sous-graphes GraphQL en un supergraph distribué", "is_correct": True},
                    {"text": "Un système d'authentification pour Apollo Server", "is_correct": False},
                    {"text": "Un load balancer pour serveurs GraphQL", "is_correct": False},
                    {"text": "Un framework de tests de fédération de données", "is_correct": False}
                ]},
                {"text": "Comment sécuriser une API GraphQL?", "answers": [
                    {"text": "Authentification, autorisation par champ, query depth limiting, rate limiting, disable introspection en prod", "is_correct": True},
                    {"text": "Utiliser HTTPS uniquement", "is_correct": False},
                    {"text": "Activer le mode strict de GraphQL", "is_correct": False},
                    {"text": "Utiliser uniquement des mutations signées", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les Subscriptions avec WebSocket?", "answers": [
                    {"text": "Un canal WebSocket persistant où le serveur pousse des mises à jour quand des événements se produisent", "is_correct": True},
                    {"text": "Des queries qui se répètent automatiquement sur polling", "is_correct": False},
                    {"text": "Des Server-Sent Events déguisés en GraphQL", "is_correct": False},
                    {"text": "Des webhooks déclenchés par des mutations", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le concept 'schema-first' vs 'code-first' en GraphQL?", "answers": [
                    {"text": "Schema-first : SDL définit le schema en premier; Code-first : le schema est généré depuis le code", "is_correct": True},
                    {"text": "Schema-first est pour les petits projets, code-first pour les grands", "is_correct": False},
                    {"text": "Code-first est la seule approche recommandée", "is_correct": False},
                    {"text": "Ils sont identiques en termes de résultat final", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le caching en GraphQL avec Apollo?", "answers": [
                    {"text": "Cache normalisé côté client par identifiant d'entité; cache côté serveur par persisted queries ou réponse", "is_correct": True},
                    {"text": "Un cache HTTP standard comme pour REST", "is_correct": False},
                    {"text": "GraphQL ne supporte pas le caching", "is_correct": False},
                    {"text": "Cache uniquement possible avec Redis côté serveur", "is_correct": False}
                ]},
            ],
        },
    },
}

# 7. SYSTÈMES ET ADMINISTRATION
# -----------------------------------------------------------------------------

LINUX_DATA = {
    "category": {
        "name": "Linux",
        "description": "Quiz pour maîtriser Linux, le terminal et l'administration système",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/linux/linux-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Linux - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Quelle commande affiche le répertoire courant?", "answers": [
                    {"text": "pwd", "is_correct": True},
                    {"text": "cd", "is_correct": False},
                    {"text": "ls", "is_correct": False},
                    {"text": "dir", "is_correct": False}
                ]},
                {"text": "Quelle commande liste les fichiers d'un dossier?", "answers": [
                    {"text": "ls", "is_correct": True},
                    {"text": "list", "is_correct": False},
                    {"text": "dir", "is_correct": False},
                    {"text": "show", "is_correct": False}
                ]},
                {"text": "Quelle commande crée un dossier?", "answers": [
                    {"text": "mkdir nom_dossier", "is_correct": True},
                    {"text": "create nom_dossier", "is_correct": False},
                    {"text": "md nom_dossier", "is_correct": False},
                    {"text": "newdir nom_dossier", "is_correct": False}
                ]},
                {"text": "Quelle commande supprime un fichier?", "answers": [
                    {"text": "rm fichier", "is_correct": True},
                    {"text": "del fichier", "is_correct": False},
                    {"text": "delete fichier", "is_correct": False},
                    {"text": "erase fichier", "is_correct": False}
                ]},
                {"text": "Quelle commande affiche le contenu d'un fichier?", "answers": [
                    {"text": "cat fichier", "is_correct": True},
                    {"text": "read fichier", "is_correct": False},
                    {"text": "open fichier", "is_correct": False},
                    {"text": "show fichier", "is_correct": False}
                ]},
                {"text": "Comment changer de dossier?", "answers": [
                    {"text": "cd nom_dossier", "is_correct": True},
                    {"text": "go nom_dossier", "is_correct": False},
                    {"text": "move nom_dossier", "is_correct": False},
                    {"text": "enter nom_dossier", "is_correct": False}
                ]},
                {"text": "Quelle commande copie un fichier?", "answers": [
                    {"text": "cp source destination", "is_correct": True},
                    {"text": "copy source destination", "is_correct": False},
                    {"text": "mv source destination", "is_correct": False},
                    {"text": "dup source destination", "is_correct": False}
                ]},
                {"text": "Quelle commande déplace/renomme un fichier?", "answers": [
                    {"text": "mv source destination", "is_correct": True},
                    {"text": "cp source destination", "is_correct": False},
                    {"text": "move source destination", "is_correct": False},
                    {"text": "rename source destination", "is_correct": False}
                ]},
                {"text": "Quelle commande affiche les processus en cours?", "answers": [
                    {"text": "ps aux", "is_correct": True},
                    {"text": "processes", "is_correct": False},
                    {"text": "task list", "is_correct": False},
                    {"text": "running", "is_correct": False}
                ]},
                {"text": "Quelle commande affiche les premières lignes d'un fichier?", "answers": [
                    {"text": "head fichier", "is_correct": True},
                    {"text": "top fichier", "is_correct": False},
                    {"text": "first fichier", "is_correct": False},
                    {"text": "start fichier", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Linux - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Que fait la commande chmod 755 fichier?", "answers": [
                    {"text": "Donne rwx au propriétaire, r-x au groupe et aux autres", "is_correct": True},
                    {"text": "Donne tous les droits à tout le monde", "is_correct": False},
                    {"text": "Supprime tous les droits", "is_correct": False},
                    {"text": "Change le propriétaire du fichier", "is_correct": False}
                ]},
                {"text": "Quelle commande cherche un fichier par nom?", "answers": [
                    {"text": "find / -name 'fichier.txt'", "is_correct": True},
                    {"text": "search fichier.txt", "is_correct": False},
                    {"text": "locate -n fichier.txt", "is_correct": False},
                    {"text": "grep -f fichier.txt /", "is_correct": False}
                ]},
                {"text": "Que fait grep?", "answers": [
                    {"text": "Recherche des patterns (regex) dans des fichiers ou la sortie d'autres commandes", "is_correct": True},
                    {"text": "Compresse des fichiers", "is_correct": False},
                    {"text": "Gère les processus", "is_correct": False},
                    {"text": "Configure le réseau", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un pipe (|) en Linux?", "answers": [
                    {"text": "Redirige la sortie d'une commande vers l'entrée d'une autre", "is_correct": True},
                    {"text": "Compare deux fichiers", "is_correct": False},
                    {"text": "Exécute deux commandes en parallèle", "is_correct": False},
                    {"text": "Fusionne deux flux de données", "is_correct": False}
                ]},
                {"text": "Comment voir l'utilisation du disque?", "answers": [
                    {"text": "df -h", "is_correct": True},
                    {"text": "disk -show", "is_correct": False},
                    {"text": "storage -list", "is_correct": False},
                    {"text": "du /", "is_correct": False}
                ]},
                {"text": "Que fait la commande sudo?", "answers": [
                    {"text": "Exécute une commande avec les privilèges superutilisateur (root)", "is_correct": True},
                    {"text": "Change d'utilisateur", "is_correct": False},
                    {"text": "Vérifie les permissions d'une commande", "is_correct": False},
                    {"text": "Soumet une commande à la queue", "is_correct": False}
                ]},
                {"text": "Comment éditer un fichier avec vi/vim?", "answers": [
                    {"text": "vim fichier, i pour insérer, Esc puis :wq pour sauvegarder et quitter", "is_correct": True},
                    {"text": "vim fichier, puis écrire directement", "is_correct": False},
                    {"text": "vim fichier, Ctrl+S pour sauvegarder", "is_correct": False},
                    {"text": "vim fichier, puis :save pour sauvegarder", "is_correct": False}
                ]},
                {"text": "Que fait tar -czf archive.tar.gz dossier/?", "answers": [
                    {"text": "Crée une archive gzip compressée du dossier", "is_correct": True},
                    {"text": "Extrait une archive gzip", "is_correct": False},
                    {"text": "Liste le contenu d'une archive", "is_correct": False},
                    {"text": "Compresse uniquement sans archiver", "is_correct": False}
                ]},
                {"text": "Quelle commande affiche les variables d'environnement?", "answers": [
                    {"text": "env ou printenv", "is_correct": True},
                    {"text": "vars", "is_correct": False},
                    {"text": "environ", "is_correct": False},
                    {"text": "set -e", "is_correct": False}
                ]},
                {"text": "Comment tuer un processus par PID?", "answers": [
                    {"text": "kill PID ou kill -9 PID pour forcer", "is_correct": True},
                    {"text": "stop PID", "is_correct": False},
                    {"text": "terminate PID", "is_correct": False},
                    {"text": "remove PID", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Linux - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que systemd?", "answers": [
                    {"text": "Un système d'init et gestionnaire de services qui gère les processus, logs et dépendances au démarrage", "is_correct": True},
                    {"text": "Un démon de synchronisation système", "is_correct": False},
                    {"text": "Un compilateur système Linux", "is_correct": False},
                    {"text": "Un système de fichiers Linux avancé", "is_correct": False}
                ]},
                {"text": "Que fait awk?", "answers": [
                    {"text": "Un outil de traitement de texte par colonnes permettant du scripting puissant sur des fichiers structurés", "is_correct": True},
                    {"text": "Un outil de compression avancé", "is_correct": False},
                    {"text": "Un gestionnaire de packages", "is_correct": False},
                    {"text": "Un outil de monitoring réseau", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le sticky bit?", "answers": [
                    {"text": "Un permission bit sur un dossier qui empêche les utilisateurs de supprimer les fichiers des autres", "is_correct": True},
                    {"text": "Un bit qui rend un fichier persistant en mémoire", "is_correct": False},
                    {"text": "Un bit qui empêche la modification d'un fichier", "is_correct": False},
                    {"text": "Un bit qui marque un fichier comme exécutable", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que cron?", "answers": [
                    {"text": "Un planificateur de tâches qui exécute des commandes à des intervalles définis dans crontab", "is_correct": True},
                    {"text": "Un outil de chronométrage des processus", "is_correct": False},
                    {"text": "Un système de backup incrémental", "is_correct": False},
                    {"text": "Un gestionnaire de processus en temps réel", "is_correct": False}
                ]},
                {"text": "Que fait la commande strace?", "answers": [
                    {"text": "Trace les appels système effectués par un processus pour déboguer", "is_correct": True},
                    {"text": "Affiche la stack trace d'une erreur", "is_correct": False},
                    {"text": "Monitore l'utilisation CPU d'un processus", "is_correct": False},
                    {"text": "Suit les connexions réseau d'un processus", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que iptables?", "answers": [
                    {"text": "Un outil de configuration du pare-feu kernel Linux (netfilter) pour filtrer le trafic réseau", "is_correct": True},
                    {"text": "Un gestionnaire de tables de base de données", "is_correct": False},
                    {"text": "Un outil de monitoring réseau", "is_correct": False},
                    {"text": "Un service de routing réseau avancé", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que /proc en Linux?", "answers": [
                    {"text": "Un pseudo-filesystem qui expose des informations sur les processus et le kernel en temps réel", "is_correct": True},
                    {"text": "Le dossier des programmes système", "is_correct": False},
                    {"text": "Un dossier de procédures de configuration", "is_correct": False},
                    {"text": "Le dossier des processus arrêtés", "is_correct": False}
                ]},
                {"text": "Comment écrire un script bash avec une boucle for?", "answers": [
                    {"text": "for i in $(seq 1 10); do echo $i; done", "is_correct": True},
                    {"text": "foreach i in 1..10 { echo $i }", "is_correct": False},
                    {"text": "for i=1; i<=10; i++; do echo $i done", "is_correct": False},
                    {"text": "loop i from 1 to 10; echo $i; endloop", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le namespace Linux?", "answers": [
                    {"text": "Un mécanisme d'isolation du kernel (PID, réseau, mount...) utilisé par les conteneurs Docker", "is_correct": True},
                    {"text": "Un système de nommage des fichiers", "is_correct": False},
                    {"text": "Un système de gestion des utilisateurs et groupes", "is_correct": False},
                    {"text": "Un module de sécurité Linux", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que inode en Linux?", "answers": [
                    {"text": "Une structure de données qui stocke les métadonnées d'un fichier (permissions, taille, pointeurs vers blocs) sans le nom", "is_correct": True},
                    {"text": "Un nœud dans un réseau Linux", "is_correct": False},
                    {"text": "Un identifiant unique de processus", "is_correct": False},
                    {"text": "Un index dans le journal du système de fichiers", "is_correct": False}
                ]},
            ],
        },
    },
}

# 8. MOBILE ET MULTIPLATEFORME
# -----------------------------------------------------------------------------

FLUTTER_DATA = {
    "category": {
        "name": "Flutter",
        "description": "Quiz pour maîtriser Flutter et le développement mobile cross-platform",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flutter/flutter-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "Flutter - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Quel langage de programmation Flutter utilise-t-il?", "answers": [
                    {"text": "Dart", "is_correct": True},
                    {"text": "Kotlin", "is_correct": False},
                    {"text": "Swift", "is_correct": False},
                    {"text": "JavaScript", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Widget en Flutter?", "answers": [
                    {"text": "Le bloc de base pour construire l'interface utilisateur", "is_correct": True},
                    {"text": "Une bibliothèque externe", "is_correct": False},
                    {"text": "Un fichier de configuration", "is_correct": False},
                    {"text": "Un service d'arrière-plan", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre StatelessWidget et StatefulWidget?", "answers": [
                    {"text": "StatefulWidget peut gérer un état qui change dans le temps", "is_correct": True},
                    {"text": "StatelessWidget est plus rapide dans tous les cas", "is_correct": False},
                    {"text": "StatefulWidget ne peut pas avoir de paramètres", "is_correct": False},
                    {"text": "StatelessWidget ne peut pas afficher de texte", "is_correct": False}
                ]},
                {"text": "Quel widget Flutter affiche du texte?", "answers": [
                    {"text": "Text", "is_correct": True},
                    {"text": "Label", "is_correct": False},
                    {"text": "Paragraph", "is_correct": False},
                    {"text": "TextView", "is_correct": False}
                ]},
                {"text": "Comment centrer un widget dans Flutter?", "answers": [
                    {"text": "Center(child: monWidget)", "is_correct": True},
                    {"text": "monWidget.align(center)", "is_correct": False},
                    {"text": "Align(position: center)", "is_correct": False},
                    {"text": "Container(center: true)", "is_correct": False}
                ]},
                {"text": "Quel widget Flutter est utilisé pour une liste scrollable?", "answers": [
                    {"text": "ListView", "is_correct": True},
                    {"text": "ScrollView", "is_correct": False},
                    {"text": "RecyclerView", "is_correct": False},
                    {"text": "TableView", "is_correct": False}
                ]},
                {"text": "Comment lancer l'application Flutter en mode debug?", "answers": [
                    {"text": "flutter run", "is_correct": True},
                    {"text": "flutter start", "is_correct": False},
                    {"text": "dart run main.dart", "is_correct": False},
                    {"text": "flutter debug", "is_correct": False}
                ]},
                {"text": "Quel fichier contient les dépendances d'un projet Flutter?", "answers": [
                    {"text": "pubspec.yaml", "is_correct": True},
                    {"text": "package.json", "is_correct": False},
                    {"text": "build.gradle", "is_correct": False},
                    {"text": "requirements.txt", "is_correct": False}
                ]},
                {"text": "Quel widget Flutter permet d'empiler des widgets en colonne?", "answers": [
                    {"text": "Column", "is_correct": True},
                    {"text": "Stack", "is_correct": False},
                    {"text": "VBox", "is_correct": False},
                    {"text": "LinearLayout", "is_correct": False}
                ]},
                {"text": "Comment appeler setState() correctement?", "answers": [
                    {"text": "setState(() { /* modifications */ })", "is_correct": True},
                    {"text": "this.state = nouvelEtat", "is_correct": False},
                    {"text": "updateState(nouvelEtat)", "is_correct": False},
                    {"text": "setState(nouvelEtat)", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "Flutter - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que le BuildContext en Flutter?", "answers": [
                    {"text": "Un handle vers la position du widget dans l'arbre de widgets", "is_correct": True},
                    {"text": "L'état actuel de l'application", "is_correct": False},
                    {"text": "Le contexte d'exécution Dart", "is_correct": False},
                    {"text": "Un objet de configuration du thème", "is_correct": False}
                ]},
                {"text": "Comment naviguer vers un nouvel écran en Flutter?", "answers": [
                    {"text": "Navigator.push(context, MaterialPageRoute(builder: (_) => NouvelEcran()))", "is_correct": True},
                    {"text": "Router.navigate(NouvelEcran())", "is_correct": False},
                    {"text": "context.push(NouvelEcran())", "is_correct": False},
                    {"text": "navigate(NouvelEcran())", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un FutureBuilder?", "answers": [
                    {"text": "Un widget qui construit son UI selon l'état d'une Future", "is_correct": True},
                    {"text": "Un outil pour créer des animations", "is_correct": False},
                    {"text": "Un builder pour les listes asynchrones", "is_correct": False},
                    {"text": "Un générateur de code futur", "is_correct": False}
                ]},
                {"text": "Quel widget Flutter superpose des widgets les uns sur les autres?", "answers": [
                    {"text": "Stack", "is_correct": True},
                    {"text": "Column", "is_correct": False},
                    {"text": "Overlay", "is_correct": False},
                    {"text": "Layer", "is_correct": False}
                ]},
                {"text": "Comment partager des données entre widgets avec InheritedWidget?", "answers": [
                    {"text": "En plaçant l'InheritedWidget en parent et en y accédant via context", "is_correct": True},
                    {"text": "En passant les données via le constructeur de chaque widget", "is_correct": False},
                    {"text": "En utilisant une variable globale statique", "is_correct": False},
                    {"text": "En émettant des événements via EventBus", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que pubspec.lock?", "answers": [
                    {"text": "Un fichier qui verrouille les versions exactes des dépendances installées", "is_correct": True},
                    {"text": "Un fichier qui bloque les modifications du pubspec.yaml", "is_correct": False},
                    {"text": "Un fichier de configuration de sécurité", "is_correct": False},
                    {"text": "Un fichier de logs de build", "is_correct": False}
                ]},
                {"text": "Quel widget Flutter crée un bouton avec une élévation (Material)?", "answers": [
                    {"text": "ElevatedButton", "is_correct": True},
                    {"text": "RaisedButton", "is_correct": False},
                    {"text": "ShadowButton", "is_correct": False},
                    {"text": "MaterialButton", "is_correct": False}
                ]},
                {"text": "Comment gérer les erreurs dans un FutureBuilder?", "answers": [
                    {"text": "Vérifier snapshot.hasError et afficher un widget d'erreur", "is_correct": True},
                    {"text": "Utiliser try/catch dans le builder", "is_correct": False},
                    {"text": "Ajouter un paramètre onError au FutureBuilder", "is_correct": False},
                    {"text": "Utiliser ErrorBoundary", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Hot Reload en Flutter?", "answers": [
                    {"text": "Injecte les modifications du code dans la VM Dart sans redémarrer l'app", "is_correct": True},
                    {"text": "Redémarre complètement l'application", "is_correct": False},
                    {"text": "Recompile uniquement les fichiers modifiés", "is_correct": False},
                    {"text": "Synchronise l'app avec un serveur de développement", "is_correct": False}
                ]},
                {"text": "Quel widget Flutter affiche une image depuis le réseau?", "answers": [
                    {"text": "Image.network('url')", "is_correct": True},
                    {"text": "NetworkImage('url')", "is_correct": False},
                    {"text": "RemoteImage('url')", "is_correct": False},
                    {"text": "UrlImage('url')", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "Flutter - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que le State Management avec Riverpod?", "answers": [
                    {"text": "Une solution de gestion d'état type-safe et réactive basée sur des providers", "is_correct": True},
                    {"text": "Un plugin de navigation pour Flutter", "is_correct": False},
                    {"text": "Un système de mise en cache HTTP", "is_correct": False},
                    {"text": "Une alternative à setState uniquement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le widget RepaintBoundary?", "answers": [
                    {"text": "Crée un calque de peinture séparé pour isoler les repaints coûteux", "is_correct": True},
                    {"text": "Délimite une zone cliquable dans l'UI", "is_correct": False},
                    {"text": "Empêche le rebuild d'un sous-arbre de widgets", "is_correct": False},
                    {"text": "Crée une bordure autour d'un widget", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le mécanisme de keys en Flutter?", "answers": [
                    {"text": "Elles permettent à Flutter d'identifier et préserver l'état des widgets lors de reconstructions", "is_correct": True},
                    {"text": "Elles servent uniquement d'identifiants pour les tests automatisés", "is_correct": False},
                    {"text": "Elles gèrent l'accès aux ressources chiffrées", "is_correct": False},
                    {"text": "Elles optimisent le rendu des listes statiques", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre GlobalKey et LocalKey?", "answers": [
                    {"text": "GlobalKey est unique dans toute l'app, LocalKey dans un parent direct", "is_correct": True},
                    {"text": "GlobalKey est partagé entre toutes les instances, LocalKey non", "is_correct": False},
                    {"text": "LocalKey peut être utilisé pour accéder à l'état d'un widget, GlobalKey non", "is_correct": False},
                    {"text": "Aucune différence fonctionnelle", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un Isolate en Dart/Flutter?", "answers": [
                    {"text": "Un thread séparé avec sa propre mémoire pour du calcul parallèle", "is_correct": True},
                    {"text": "Un widget isolé du reste de l'arbre", "is_correct": False},
                    {"text": "Un module de sécurité pour les données sensibles", "is_correct": False},
                    {"text": "Un état isolé pour les tests unitaires", "is_correct": False}
                ]},
                {"text": "Comment optimiser les performances d'une ListView longue?", "answers": [
                    {"text": "Utiliser ListView.builder qui crée les items à la demande", "is_correct": True},
                    {"text": "Pré-charger tous les items au démarrage", "is_correct": False},
                    {"text": "Utiliser un Column avec SingleChildScrollView", "is_correct": False},
                    {"text": "Diviser la liste en plusieurs widgets", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Bloc pattern en Flutter?", "answers": [
                    {"text": "Business Logic Component - sépare la logique métier de l'UI via des Streams", "is_correct": True},
                    {"text": "Un pattern de navigation par blocs d'écrans", "is_correct": False},
                    {"text": "Un système de mise en cache basé sur des blocs de données", "is_correct": False},
                    {"text": "Un outil de gestion des animations complexes", "is_correct": False}
                ]},
                {"text": "Comment créer un widget qui s'anime avec AnimationController?", "answers": [
                    {"text": "En utilisant SingleTickerProviderStateMixin et en créant un AnimationController dans initState", "is_correct": True},
                    {"text": "En étendant AnimatedWidget directement", "is_correct": False},
                    {"text": "En wrappant le widget avec AnimationProvider", "is_correct": False},
                    {"text": "En utilisant setState avec un Timer", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Dart Null Safety?", "answers": [
                    {"text": "Un système de types qui distingue les types nullable et non-nullable à la compilation", "is_correct": True},
                    {"text": "Une vérification des null à l'exécution uniquement", "is_correct": False},
                    {"text": "Un mécanisme de gestion automatique des erreurs null", "is_correct": False},
                    {"text": "Une option de configuration du compilateur Dart", "is_correct": False}
                ]},
                {"text": "Que fait le widget Semantics en Flutter?", "answers": [
                    {"text": "Fournit des informations d'accessibilité pour les lecteurs d'écran", "is_correct": True},
                    {"text": "Ajoute des métadonnées SEO à l'application web Flutter", "is_correct": False},
                    {"text": "Décrit le comportement métier d'un widget", "is_correct": False},
                    {"text": "Génère de la documentation automatique", "is_correct": False}
                ]},
            ],
        },
    },
}

REACT_NATIVE_DATA = {
    "category": {
        "name": "React Native",
        "description": "Quiz pour maîtriser React Native et le développement mobile cross-platform",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "React Native - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que React Native?", "answers": [
                    {"text": "Un framework pour créer des applications mobiles natives avec JavaScript/React", "is_correct": True},
                    {"text": "Une version mobile de React", "is_correct": False},
                    {"text": "Un framework pour les PWA", "is_correct": False},
                    {"text": "Une bibliothèque UI pour React", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre React et React Native?", "answers": [
                    {"text": "React utilise des composants web, React Native des composants natifs", "is_correct": True},
                    {"text": "React Native est plus lent", "is_correct": False},
                    {"text": "React a plus de fonctionnalités", "is_correct": False},
                    {"text": "Aucune différence", "is_correct": False}
                ]},
                {"text": "Comment créer un composant de base dans React Native?", "answers": [
                    {"text": "import { View, Text } from 'react-native'", "is_correct": True},
                    {"text": "import { div, span } from 'react'", "is_correct": False},
                    {"text": "import { Container, Label } from 'react-native'", "is_correct": False},
                    {"text": "import React, { Component } from 'react'", "is_correct": False}
                ]},
                {"text": "Quel composant React Native est équivalent à <div> en HTML?", "answers": [
                    {"text": "<View>", "is_correct": True},
                    {"text": "<Div>", "is_correct": False},
                    {"text": "<Container>", "is_correct": False},
                    {"text": "<Box>", "is_correct": False}
                ]},
                {"text": "Comment styliser un composant en React Native?", "answers": [
                    {"text": "Avec la prop style et StyleSheet.create()", "is_correct": True},
                    {"text": "Avec des fichiers CSS", "is_correct": False},
                    {"text": "Avec className", "is_correct": False},
                    {"text": "Avec des inline styles uniquement", "is_correct": False}
                ]},
                {"text": "Quelle commande crée un nouveau projet React Native?", "answers": [
                    {"text": "npx react-native init MonProjet", "is_correct": True},
                    {"text": "npm create react-native-app", "is_correct": False},
                    {"text": "react-native new MonProjet", "is_correct": False},
                    {"text": "expo init MonProjet (avec Expo)", "is_correct": True}
                ]},
                {"text": "Comment gérer la navigation dans React Native?", "answers": [
                    {"text": "Avec React Navigation (stack, tabs, drawer)", "is_correct": True},
                    {"text": "Avec React Router", "is_correct": False},
                    {"text": "Avec des liens HTML", "is_correct": False},
                    {"text": "Navigation native automatique", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le bridge dans React Native?", "answers": [
                    {"text": "Le mécanisme de communication entre JS et le code natif", "is_correct": True},
                    {"text": "Un pont entre iOS et Android", "is_correct": False},
                    {"text": "Un outil de debugging", "is_correct": False},
                    {"text": "Une bibliothèque de composants", "is_correct": False}
                ]},
                {"text": "Comment lancer l'application sur un émulateur?", "answers": [
                    {"text": "npx react-native run-android ou run-ios", "is_correct": True},
                    {"text": "npm start android", "is_correct": False},
                    {"text": "react-native emulate", "is_correct": False},
                    {"text": "expo start", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le hot reload dans React Native?", "answers": [
                    {"text": "Recharge les modifications sans perdre l'état", "is_correct": True},
                    {"text": "Redémarre complètement l'app", "is_correct": False},
                    {"text": "Recompile tout le projet", "is_correct": False},
                    {"text": "Met à jour le bundle JS", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "React Native - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que les composants natifs personnalisés?", "answers": [
                    {"text": "Des composants écrits en code natif (Swift/Kotlin) exposés à JS", "is_correct": True},
                    {"text": "Des composants React avec styles natifs", "is_correct": False},
                    {"text": "Des composants de la communauté", "is_correct": False},
                    {"text": "Des composants générés automatiquement", "is_correct": False}
                ]},
                {"text": "Comment gérer les permissions sur iOS/Android?", "answers": [
                    {"text": "Avec des bibliothèques comme react-native-permissions", "is_correct": True},
                    {"text": "Les permissions sont automatiques", "is_correct": False},
                    {"text": "Uniquement via le code natif", "is_correct": False},
                    {"text": "React Native gère nativement", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Flexbox dans React Native?", "answers": [
                    {"text": "Le système de layout par défaut (inspiré du CSS Flexbox)", "is_correct": True},
                    {"text": "Une bibliothèque de composants flexibles", "is_correct": False},
                    {"text": "Un outil de debugging", "is_correct": False},
                    {"text": "Un framework CSS", "is_correct": False}
                ]},
                {"text": "Comment accéder aux APIs natives (caméra, GPS)?", "answers": [
                    {"text": "Avec des modules natifs ou des bibliothèques comme expo", "is_correct": True},
                    {"text": "Directement depuis JS", "is_correct": False},
                    {"text": "Avec fetch() vers l'API native", "is_correct": False},
                    {"text": "React Native inclut toutes les APIs", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le state management dans React Native?", "answers": [
                    {"text": "Redux, MobX, Zustand, ou Context API comme React", "is_correct": True},
                    {"text": "Un state manager spécifique mobile", "is_correct": False},
                    {"text": "AsyncStorage pour le state", "is_correct": False},
                    {"text": "Pas besoin de state management", "is_correct": False}
                ]},
                {"text": "Comment gérer les assets (images, fonts)?", "answers": [
                    {"text": "Avec require() ou import pour les assets locaux", "is_correct": True},
                    {"text": "Avec des URLs web uniquement", "is_correct": False},
                    {"text": "En les copiant dans le dossier assets", "is_correct": False},
                    {"text": "Automatiquement détectés", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que la différence entre Expo et React Native CLI?", "answers": [
                    {"text": "Expo offre plus de fonctionnalités prêtes à l'emploi mais moins de flexibilité", "is_correct": True},
                    {"text": "Expo est plus lent", "is_correct": False},
                    {"text": "React Native CLI est plus simple", "is_correct": False},
                    {"text": "Aucune différence", "is_correct": False}
                ]},
                {"text": "Comment optimiser les performances d'une FlatList?", "answers": [
                    {"text": "getItemLayout, keyExtractor, initialNumToRender", "is_correct": True},
                    {"text": "En utilisant ScrollView", "is_correct": False},
                    {"text": "En limitant le nombre d'items", "is_correct": False},
                    {"text": "Le caching automatique", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Hermes engine?", "answers": [
                    {"text": "Un moteur JS optimisé pour React Native (réduit le temps de démarrage)", "is_correct": True},
                    {"text": "Un éditeur de code", "is_correct": False},
                    {"text": "Une bibliothèque UI", "is_correct": False},
                    {"text": "Un compilateur TypeScript", "is_correct": False}
                ]},
                {"text": "Comment tester une application React Native?", "answers": [
                    {"text": "Avec Jest pour les tests unitaires et Detox pour les tests E2E", "is_correct": True},
                    {"text": "Uniquement sur appareil physique", "is_correct": False},
                    {"text": "Avec React Native Testing Library", "is_correct": False},
                    {"text": "Pas de tests possibles", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "React Native - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que le Native Modules?", "answers": [
                    {"text": "Du code natif (Java/Objective-C) exposé à JavaScript", "is_correct": True},
                    {"text": "Des composants React natifs", "is_correct": False},
                    {"text": "Des modules npm pour mobile", "is_correct": False},
                    {"text": "Des extensions Chrome", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le threading dans React Native?", "answers": [
                    {"text": "Thread JS, thread UI natif, thread de background", "is_correct": True},
                    {"text": "Un seul thread pour tout", "is_correct": False},
                    {"text": "Multi-threading automatique", "is_correct": False},
                    {"text": "Pas de threading", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le code push (CodePush)?", "answers": [
                    {"text": "Mettre à jour le bundle JS sans passer par l'App Store", "is_correct": True},
                    {"text": "Pousser du code vers GitHub", "is_correct": False},
                    {"text": "Déployer sur les stores", "is_correct": False},
                    {"text": "Un outil de CI/CD", "is_correct": False}
                ]},
                {"text": "Comment implémenter le deep linking?", "answers": [
                    {"text": "Avec Linking API et configuration des schémas d'URL", "is_correct": True},
                    {"text": "Avec des liens HTML", "is_correct": False},
                    {"text": "Automatique dans React Native", "is_correct": False},
                    {"text": "Uniquement avec Firebase", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Turbo Modules (New Architecture)?", "answers": [
                    {"text": "Nouvelle architecture plus performante pour les modules natifs", "is_correct": True},
                    {"text": "Des modules plus rapides", "is_correct": False},
                    {"text": "Un compilateur JIT", "is_correct": False},
                    {"text": "Une bibliothèque d'optimisation", "is_correct": False}
                ]},
                {"text": "Comment gérer le rendu côté serveur avec React Native?", "answers": [
                    {"text": "React Native n'a pas de SSR, mais peut utiliser Next.js pour le web", "is_correct": True},
                    {"text": "Avec React Native Web", "is_correct": False},
                    {"text": "SSR possible avec Expo", "is_correct": False},
                    {"text": "Avec des services cloud", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Fabric (New Architecture)?", "answers": [
                    {"text": "Le nouveau système de rendu (réécriture du UI manager)", "is_correct": True},
                    {"text": "Une bibliothèque UI", "is_correct": False},
                    {"text": "Un outil de fabrication", "is_correct": False},
                    {"text": "Un compilateur", "is_correct": False}
                ]},
                {"text": "Comment optimiser la taille de l'application?", "answers": [
                    {"text": "Hermes, ProGuard, suppression des librairies inutilisées, assets optimisés", "is_correct": True},
                    {"text": "React Native est déjà optimisé", "is_correct": False},
                    {"text": "En utilisant Expo", "is_correct": False},
                    {"text": "En compressant le bundle", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le JSI (JavaScript Interface)?", "answers": [
                    {"text": "Une interface plus performante entre JS et natif (sans bridge)", "is_correct": True},
                    {"text": "Un nouveau langage", "is_correct": False},
                    {"text": "Un standard JavaScript", "is_correct": False},
                    {"text": "Une bibliothèque de compatibilité", "is_correct": False}
                ]},
                {"text": "Comment gérer les mises à jour de l'application?", "answers": [
                    {"text": "CodePush pour les bundles JS, App Store/Play Store pour les binaires", "is_correct": True},
                    {"text": "Uniquement via les stores", "is_correct": False},
                    {"text": "Mise à jour automatique", "is_correct": False},
                    {"text": "Avec des scripts shell", "is_correct": False}
                ]},
            ],
        },
    },
}

# 9. CLOUD ET INFRASTRUCTURE
# -----------------------------------------------------------------------------

AWS_DATA = {
    "category": {
        "name": "AWS",
        "description": "Quiz pour maîtriser Amazon Web Services et le cloud computing",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/amazonwebservices/amazonwebservices-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "AWS - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Que signifie AWS?", "answers": [
                    {"text": "Amazon Web Services", "is_correct": True},
                    {"text": "Advanced Web Solutions", "is_correct": False},
                    {"text": "Amazon Worldwide Services", "is_correct": False},
                    {"text": "AWS Web System", "is_correct": False}
                ]},
                {"text": "Quel service AWS est utilisé pour les serveurs virtuels?", "answers": [
                    {"text": "EC2 (Elastic Compute Cloud)", "is_correct": True},
                    {"text": "S3", "is_correct": False},
                    {"text": "Lambda", "is_correct": False},
                    {"text": "RDS", "is_correct": False}
                ]},
                {"text": "Quel service AWS est utilisé pour le stockage d'objets?", "answers": [
                    {"text": "S3 (Simple Storage Service)", "is_correct": True},
                    {"text": "EBS", "is_correct": False},
                    {"text": "EFS", "is_correct": False},
                    {"text": "Glacier", "is_correct": False}
                ]},
                {"text": "Quel service AWS gère les bases de données relationnelles?", "answers": [
                    {"text": "RDS (Relational Database Service)", "is_correct": True},
                    {"text": "DynamoDB", "is_correct": False},
                    {"text": "Aurora", "is_correct": False},
                    {"text": "Redshift", "is_correct": False}
                ]},
                {"text": "Quel service AWS permet d'exécuter du code sans provisionner de serveurs?", "answers": [
                    {"text": "Lambda", "is_correct": True},
                    {"text": "EC2", "is_correct": False},
                    {"text": "ECS", "is_correct": False},
                    {"text": "Elastic Beanstalk", "is_correct": False}
                ]},
                {"text": "Comment s'appelle le load balancer AWS?", "answers": [
                    {"text": "ELB (Elastic Load Balancing)", "is_correct": True},
                    {"text": "CLB", "is_correct": False},
                    {"text": "ALB", "is_correct": False},
                    {"text": "NLB", "is_correct": False}
                ]},
                {"text": "Quel service AWS fournit un DNS scalable?", "answers": [
                    {"text": "Route 53", "is_correct": True},
                    {"text": "CloudFront", "is_correct": False},
                    {"text": "Direct Connect", "is_correct": False},
                    {"text": "VPC", "is_correct": False}
                ]},
                {"text": "Quel service AWS est un CDN (Content Delivery Network)?", "answers": [
                    {"text": "CloudFront", "is_correct": True},
                    {"text": "S3 Transfer Acceleration", "is_correct": False},
                    {"text": "Global Accelerator", "is_correct": False},
                    {"text": "Route 53", "is_correct": False}
                ]},
                {"text": "Comment s'appelle le service de monitoring AWS?", "answers": [
                    {"text": "CloudWatch", "is_correct": True},
                    {"text": "CloudTrail", "is_correct": False},
                    {"text": "AWS Config", "is_correct": False},
                    {"text": "Trusted Advisor", "is_correct": False}
                ]},
                {"text": "Quel service AWS gère l'autoscaling?", "answers": [
                    {"text": "Auto Scaling", "is_correct": True},
                    {"text": "EC2 Auto Scaling", "is_correct": False},
                    {"text": "Scaling Groups", "is_correct": False},
                    {"text": "AWS Scale", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "AWS - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Quelle est la différence entre Security Group et NACL?", "answers": [
                    {"text": "Security Group: stateful, au niveau instance; NACL: stateless, au niveau subnet", "is_correct": True},
                    {"text": "NACL est plus sécurisé que Security Group", "is_correct": False},
                    {"text": "Security Group est pour les VPC, NACL pour les EC2", "is_correct": False},
                    {"text": "Aucune différence", "is_correct": False}
                ]},
                {"text": "Qu'est-ce qu'un VPC dans AWS?", "answers": [
                    {"text": "Virtual Private Cloud - réseau virtuel isolé dans le cloud AWS", "is_correct": True},
                    {"text": "Un VPN pour connecter AWS à on-premise", "is_correct": False},
                    {"text": "Un service de calcul virtuel", "is_correct": False},
                    {"text": "Une base de données privée", "is_correct": False}
                ]},
                {"text": "Comment fonctionne IAM dans AWS?", "answers": [
                    {"text": "Identity and Access Management - gère utilisateurs, groupes, rôles et permissions", "is_correct": True},
                    {"text": "Un service de monitoring d'identité", "is_correct": False},
                    {"text": "Un outil de gestion des incidents", "is_correct": False},
                    {"text": "Une base de données d'utilisateurs", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que S3 storage classes?", "answers": [
                    {"text": "Différents niveaux de stockage (Standard, IA, Glacier, etc.) avec coûts/accès variables", "is_correct": True},
                    {"text": "Des classes de stockage pour EC2", "is_correct": False},
                    {"text": "Des types de buckets S3", "is_correct": False},
                    {"text": "Des catégories de permissions S3", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre EBS et EFS?", "answers": [
                    {"text": "EBS: block storage attaché à une seule instance; EFS: système de fichiers partagé (NFS)", "is_correct": True},
                    {"text": "EFS est plus rapide qu'EBS", "is_correct": False},
                    {"text": "EBS est pour le stockage objet, EFS pour le block", "is_correct": False},
                    {"text": "Aucune différence", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le AWS Well-Architected Framework?", "answers": [
                    {"text": "Un guide de bonnes pratiques pour construire des systèmes robustes (6 piliers)", "is_correct": True},
                    {"text": "Un framework de développement AWS", "is_correct": False},
                    {"text": "Une architecture de référence AWS", "is_correct": False},
                    {"text": "Un outil d'audit AWS", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le pricing AWS?", "answers": [
                    {"text": "Pay-as-you-go, avec tarifs à l'heure/seconde, réservations pour réduire coûts", "is_correct": True},
                    {"text": "Forfait mensuel fixe", "is_correct": False},
                    {"text": "Gratuit pour tous les services", "is_correct": False},
                    {"text": "Basé sur le nombre d'utilisateurs", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que CloudFormation dans AWS?", "answers": [
                    {"text": "Infrastructure as Code avec des templates YAML/JSON pour provisionner des ressources", "is_correct": True},
                    {"text": "Un service de formation AWS", "is_correct": False},
                    {"text": "Un outil de déploiement d'applications", "is_correct": False},
                    {"text": "Un générateur de cloud privé", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le serverless dans AWS?", "answers": [
                    {"text": "Lambda, API Gateway, DynamoDB, etc. - exécution sans gestion de serveurs", "is_correct": True},
                    {"text": "EC2 sans connexion SSH", "is_correct": False},
                    {"text": "Des serveurs virtuels sans OS", "is_correct": False},
                    {"text": "AWS sans infrastructure", "is_correct": False}
                ]},
                {"text": "Comment sécuriser une application AWS?", "answers": [
                    {"text": "IAM, Security Groups, NACL, encryption (KMS), WAF, Shield, CloudTrail, Config", "is_correct": True},
                    {"text": "Uniquement avec un mot de passe fort", "is_correct": False},
                    {"text": "Avec un VPN uniquement", "is_correct": False},
                    {"text": "AWS est sécurisé par défaut", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "AWS - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que le AWS Organizations?", "answers": [
                    {"text": "Gestion centralisée de plusieurs comptes AWS avec politiques consolidées et facturation", "is_correct": True},
                    {"text": "Un service d'organisation de projets", "is_correct": False},
                    {"text": "Un outil de gestion d'équipes", "is_correct": False},
                    {"text": "Un annuaire d'entreprises AWS", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le multi-AZ vs multi-region?", "answers": [
                    {"text": "Multi-AZ: haute disponibilité dans une région; Multi-region: disaster recovery global", "is_correct": True},
                    {"text": "Multi-region est moins cher", "is_correct": False},
                    {"text": "Multi-AZ est pour le scaling, multi-region pour la sauvegarde", "is_correct": False},
                    {"text": "Aucune différence", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le AWS Control Tower?", "answers": [
                    {"text": "Service pour configurer et gouverner un environnement multi-comptes sécurisé", "is_correct": True},
                    {"text": "Une tour de contrôle pour les instances EC2", "is_correct": False},
                    {"text": "Un outil de monitoring réseau", "is_correct": False},
                    {"text": "Un dashboard de gestion de coûts", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le AWS Transit Gateway?", "answers": [
                    {"text": "Hub central pour connecter VPCs et réseaux on-premise de manière scalable", "is_correct": True},
                    {"text": "Une passerelle de transit entre régions", "is_correct": False},
                    {"text": "Un NAT Gateway amélioré", "is_correct": False},
                    {"text": "Un routeur virtuel", "is_correct": False}
                ]},
                {"text": "Comment implémenter le blue/green deployment sur AWS?", "answers": [
                    {"text": "Avec Elastic Beanstalk, CodeDeploy, ou en basculant entre deux environnements", "is_correct": True},
                    {"text": "En changeant la couleur des instances", "is_correct": False},
                    {"text": "Avec Route 53 et des poids de trafic", "is_correct": False},
                    {"text": "En utilisant des tags de couleur", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le AWS Lambda@Edge?", "answers": [
                    {"text": "Exécute des fonctions Lambda aux edge locations de CloudFront pour personnaliser le contenu", "is_correct": True},
                    {"text": "Lambda pour les applications IoT", "is_correct": False},
                    {"text": "Une version edge de Lambda", "is_correct": False},
                    {"text": "Lambda pour les calculs en périphérie", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le DynamoDB Accelerator (DAX)?", "answers": [
                    {"text": "Cache in-memory pour DynamoDB avec microsecondes de latence", "is_correct": True},
                    {"text": "Un accélérateur de requêtes SQL", "is_correct": False},
                    {"text": "Un service de migration DynamoDB", "is_correct": False},
                    {"text": "Un outil d'optimisation de tables", "is_correct": False}
                ]},
                {"text": "Comment fonctionne le AWS Fargate?", "answers": [
                    {"text": "Moteur serverless pour conteneurs (ECS/EKS) sans gérer les instances sous-jacentes", "is_correct": True},
                    {"text": "Un service de calcul serverless", "is_correct": False},
                    {"text": "Un gestionnaire de tâches batch", "is_correct": False},
                    {"text": "Un orchestrateur de conteneurs", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le AWS Step Functions?", "answers": [
                    {"text": "Service d'orchestration de workflows serverless avec états et transitions", "is_correct": True},
                    {"text": "Des fonctions d'étape pour Lambda", "is_correct": False},
                    {"text": "Un outil de coordination de microservices", "is_correct": False},
                    {"text": "Un système de CI/CD", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le AWS SageMaker?", "answers": [
                    {"text": "Plateforme complète de machine learning (build, train, deploy models)", "is_correct": True},
                    {"text": "Un outil de visualisation de données", "is_correct": False},
                    {"text": "Un service de data labeling", "is_correct": False},
                    {"text": "Un notebook Jupyter managé", "is_correct": False}
                ]},
            ],
        },
    },
}

# 10. FONDATIONS DU WEB
# -----------------------------------------------------------------------------

CSS_HTML_DATA = {
    "category": {
        "name": "CSS / HTML",
        "description": "Quiz pour maîtriser HTML et CSS, les fondations du web",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg",
    },
    "quizzes": {
        "debutant": {
            "title": "CSS / HTML - Débutant", "level": QuizLevel.debutant, "status": QuizStatus.published,
            "questions": [
                {"text": "Que signifie HTML?", "answers": [
                    {"text": "HyperText Markup Language", "is_correct": True},
                    {"text": "High Text Markup Language", "is_correct": False},
                    {"text": "HyperText Modeling Language", "is_correct": False},
                    {"text": "Home Tool Markup Language", "is_correct": False}
                ]},
                {"text": "Quelle balise HTML crée un lien?", "answers": [
                    {"text": "<a href='...'>", "is_correct": True},
                    {"text": "<link>", "is_correct": False},
                    {"text": "<url>", "is_correct": False},
                    {"text": "<href>", "is_correct": False}
                ]},
                {"text": "Comment changer la couleur du texte en CSS?", "answers": [
                    {"text": "color: red;", "is_correct": True},
                    {"text": "text-color: red;", "is_correct": False},
                    {"text": "font-color: red;", "is_correct": False},
                    {"text": "foreground: red;", "is_correct": False}
                ]},
                {"text": "Quelle propriété CSS centre du texte horizontalement?", "answers": [
                    {"text": "text-align: center;", "is_correct": True},
                    {"text": "align: center;", "is_correct": False},
                    {"text": "horizontal-align: center;", "is_correct": False},
                    {"text": "center: text;", "is_correct": False}
                ]},
                {"text": "Quelle balise HTML crée un titre principal?", "answers": [
                    {"text": "<h1>", "is_correct": True},
                    {"text": "<title>", "is_correct": False},
                    {"text": "<header>", "is_correct": False},
                    {"text": "<heading>", "is_correct": False}
                ]},
                {"text": "Comment inclure une feuille de style CSS externe?", "answers": [
                    {"text": "<link rel='stylesheet' href='style.css'>", "is_correct": True},
                    {"text": "<style src='style.css'>", "is_correct": False},
                    {"text": "<css src='style.css'>", "is_correct": False},
                    {"text": "@import 'style.css' dans le HTML", "is_correct": False}
                ]},
                {"text": "Quelle propriété CSS définit la taille de la police?", "answers": [
                    {"text": "font-size", "is_correct": True},
                    {"text": "text-size", "is_correct": False},
                    {"text": "font-weight", "is_correct": False},
                    {"text": "size", "is_correct": False}
                ]},
                {"text": "Comment créer une liste non ordonnée en HTML?", "answers": [
                    {"text": "<ul> avec des <li>", "is_correct": True},
                    {"text": "<list> avec des <item>", "is_correct": False},
                    {"text": "<ol> avec des <li>", "is_correct": False},
                    {"text": "<ul> avec des <bullet>", "is_correct": False}
                ]},
                {"text": "Quelle propriété CSS ajoute un espace à l'intérieur d'un élément?", "answers": [
                    {"text": "padding", "is_correct": True},
                    {"text": "margin", "is_correct": False},
                    {"text": "spacing", "is_correct": False},
                    {"text": "inner-space", "is_correct": False}
                ]},
                {"text": "Comment afficher un élément HTML en flex?", "answers": [
                    {"text": "display: flex;", "is_correct": True},
                    {"text": "layout: flexbox;", "is_correct": False},
                    {"text": "flex: true;", "is_correct": False},
                    {"text": "type: flex;", "is_correct": False}
                ]},
            ],
        },
        "intermediaire": {
            "title": "CSS / HTML - Intermédiaire", "level": QuizLevel.intermediaire, "status": QuizStatus.published,
            "questions": [
                {"text": "Quelle propriété CSS Flexbox aligne les éléments sur l'axe principal?", "answers": [
                    {"text": "justify-content", "is_correct": True},
                    {"text": "align-items", "is_correct": False},
                    {"text": "flex-direction", "is_correct": False},
                    {"text": "align-content", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que la spécificité CSS?", "answers": [
                    {"text": "Un score qui détermine quelle règle CSS s'applique quand plusieurs règles ciblent le même élément", "is_correct": True},
                    {"text": "La rapidité d'application d'une règle CSS", "is_correct": False},
                    {"text": "Le niveau de précision d'un sélecteur CSS", "is_correct": False},
                    {"text": "La priorité des propriétés dans un bloc CSS", "is_correct": False}
                ]},
                {"text": "Quelle propriété CSS crée une grille?", "answers": [
                    {"text": "display: grid;", "is_correct": True},
                    {"text": "layout: grid;", "is_correct": False},
                    {"text": "display: table;", "is_correct": False},
                    {"text": "grid: true;", "is_correct": False}
                ]},
                {"text": "Comment créer une media query CSS pour mobile (max 768px)?", "answers": [
                    {"text": "@media (max-width: 768px) { ... }", "is_correct": True},
                    {"text": "@responsive mobile { ... }", "is_correct": False},
                    {"text": "@screen max(768px) { ... }", "is_correct": False},
                    {"text": "@media screen: mobile { ... }", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Box Model CSS?", "answers": [
                    {"text": "Content + Padding + Border + Margin - le modèle de dimensionnement de chaque élément", "is_correct": True},
                    {"text": "Un modèle de mise en page 3D", "is_correct": False},
                    {"text": "Un conteneur de display:block uniquement", "is_correct": False},
                    {"text": "Un framework CSS pour les boîtes", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que CSS Variables (Custom Properties)?", "answers": [
                    {"text": "Des variables définies avec --nom: valeur et utilisées avec var(--nom)", "is_correct": True},
                    {"text": "Des variables JavaScript dans le CSS", "is_correct": False},
                    {"text": "Des constantes CSS prédéfinies par le navigateur", "is_correct": False},
                    {"text": "Des preprocesseur SASS uniquement", "is_correct": False}
                ]},
                {"text": "Comment créer une transition CSS sur le hover?", "answers": [
                    {"text": ".elem { transition: all 0.3s ease; } .elem:hover { color: red; }", "is_correct": True},
                    {"text": ".elem:hover { animation: color 0.3s; }", "is_correct": False},
                    {"text": ".elem { on-hover: transition 0.3s; }", "is_correct": False},
                    {"text": "@hover .elem { transition: 0.3s; }", "is_correct": False}
                ]},
                {"text": "Quelle est la différence entre position absolute et fixed?", "answers": [
                    {"text": "absolute se positionne par rapport au parent positionné, fixed par rapport à la fenêtre", "is_correct": True},
                    {"text": "fixed est plus précis qu'absolute", "is_correct": False},
                    {"text": "absolute reste fixe au scroll, fixed non", "is_correct": False},
                    {"text": "Aucune différence visible", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le pseudo-élément ::before?", "answers": [
                    {"text": "Insère du contenu généré avant le contenu de l'élément ciblé", "is_correct": True},
                    {"text": "Cible l'élément précédant dans le DOM", "is_correct": False},
                    {"text": "Applique des styles avant l'animation", "is_correct": False},
                    {"text": "Définit les styles du premier enfant", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Flexbox flex-wrap?", "answers": [
                    {"text": "Permet aux éléments flex de se placer sur plusieurs lignes si nécessaire", "is_correct": True},
                    {"text": "Enroule du texte autour des images", "is_correct": False},
                    {"text": "Inverse l'ordre des éléments flex", "is_correct": False},
                    {"text": "Redimensionne les éléments pour tenir sur une ligne", "is_correct": False}
                ]},
            ],
        },
        "avance": {
            "title": "CSS / HTML - Avancé", "level": QuizLevel.avance, "status": QuizStatus.published,
            "questions": [
                {"text": "Qu'est-ce que CSS Cascade Layers (@layer)?", "answers": [
                    {"text": "Un mécanisme pour organiser la cascade CSS en couches avec des priorités explicites", "is_correct": True},
                    {"text": "Un système de z-index amélioré", "is_correct": False},
                    {"text": "Un outil de layering pour les animations", "is_correct": False},
                    {"text": "Un système de thèmes CSS par couches", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que Container Queries en CSS?", "answers": [
                    {"text": "Des requêtes qui s'adaptent à la taille du conteneur parent plutôt qu'à la viewport", "is_correct": True},
                    {"text": "Des queries pour les elements dans un grid", "is_correct": False},
                    {"text": "Des media queries appliquées aux conteneurs", "is_correct": False},
                    {"text": "Des queries JavaScript pour les containers", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que CSS Subgrid?", "answers": [
                    {"text": "Permet à un grid item d'utiliser les tracks de son parent grid pour aligner ses propres enfants", "is_correct": True},
                    {"text": "Un grid imbriqué dans un autre grid", "is_correct": False},
                    {"text": "Un alias de grid-template pour les sous-éléments", "is_correct": False},
                    {"text": "Un grid optimisé pour les sous-composants", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le CSS Houdini?", "answers": [
                    {"text": "Un ensemble d'APIs bas-niveau permettant aux développeurs d'étendre CSS (Paint, Layout, Typed OM...)", "is_correct": True},
                    {"text": "Un polyfill CSS pour les vieux navigateurs", "is_correct": False},
                    {"text": "Un framework CSS haute performance", "is_correct": False},
                    {"text": "Un compilateur CSS vers WASM", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que la propriété CSS contain?", "answers": [
                    {"text": "Indique au navigateur qu'un élément est indépendant pour optimiser les recalculs de layout/paint", "is_correct": True},
                    {"text": "Limite le overflow d'un conteneur", "is_correct": False},
                    {"text": "Définit le contexte de formatage d'un bloc", "is_correct": False},
                    {"text": "Contient les animations dans un élément", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que les CSS Logical Properties?", "answers": [
                    {"text": "Des propriétés indépendantes de la direction du texte (inline-start au lieu de left pour le support RTL)", "is_correct": True},
                    {"text": "Des propriétés calculées automatiquement", "is_correct": False},
                    {"text": "Des propriétés conditionnelles basées sur la média query", "is_correct": False},
                    {"text": "Des propriétés pour les animations logiques", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que :is() et :where() en CSS?", "answers": [
                    {"text": ":is() groupe des sélecteurs avec la spécificité du plus spécifique; :where() toujours 0 spécificité", "is_correct": True},
                    {"text": "Ce sont deux syntaxes identiques pour les sélecteurs groupés", "is_correct": False},
                    {"text": ":where() est plus puissant que :is()", "is_correct": False},
                    {"text": ":is() est pour les pseudo-classes, :where() pour les pseudo-éléments", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le HTML template element?", "answers": [
                    {"text": "Un élément pour définir du HTML inactif (non rendu) cloneable et instanciable via JavaScript", "is_correct": True},
                    {"text": "Un système de templates HTML côté serveur", "is_correct": False},
                    {"text": "L'ancêtre des Web Components", "is_correct": False},
                    {"text": "Un placeholder pour les données dynamiques", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que View Transitions API?", "answers": [
                    {"text": "Une API browser native pour créer des transitions animées entre deux états DOM (navigation SPA/MPA)", "is_correct": True},
                    {"text": "Une API pour les transitions CSS complexes", "is_correct": False},
                    {"text": "Un système de routing avec animations", "is_correct": False},
                    {"text": "Une API React pour les transitions de vues", "is_correct": False}
                ]},
                {"text": "Qu'est-ce que le Popover API HTML?", "answers": [
                    {"text": "Un attribut natif HTML pour créer des popovers accessibles sans JavaScript complexe (popover, popovertarget)", "is_correct": True},
                    {"text": "Une bibliothèque JS pour les tooltips", "is_correct": False},
                    {"text": "Un élément HTML <popover>", "is_correct": False},
                    {"text": "Une extension du dialog HTML", "is_correct": False}
                ]},
            ],
        },
    },
}


# =============================================================================
# EXÉCUTION DE TOUS LES SEEDERS
# =============================================================================

if __name__ == "__main__":
    print("=" * 80)
    print("🚀 INSERTION MASSIVE DE TOUS LES QUIZ")
    print("=" * 80)
    print()
    
    db = SessionLocal()
    
    # Organisation par catégories pour une meilleure lisibilité
    all_data = [
        # Langages de programmation
        PYTHON_DATA,
        JAVASCRIPT_DATA,
        TYPESCRIPT_DATA,
        DART_DATA,
        JAVA_DATA,
        GO_DATA,
        RUST_DATA,
        CSHARP_DATA,
        KOTLIN_DATA,
        SWIFT_DATA,
        PHP_DATA,
        CPLUSPLUS_DATA,
        
        # Frameworks web frontend
        REACT_DATA,
        VUEJS_DATA,
        ANGULAR_DATA,
        
        # Frameworks web backend
        NESTJS_DATA,
        EXPRESSJS_DATA,
        DJANGO_DATA,
        LARAVEL_DATA,
        FASTAPI_DATA,
        SPRING_DATA,
        
        # Bases de données
        SQL_DATA,
        MONGODB_DATA,
        
        # Outils et infrastructure
        GIT_DATA,
        DOCKER_DATA,
        KUBERNETES_DATA,
        
        # API et communication
        GRAPHQL_DATA,
        
        # Systèmes et administration
        LINUX_DATA,
        
        # Mobile et multiplateforme
        FLUTTER_DATA,
        REACT_NATIVE_DATA,
        
        # Cloud et infrastructure
        AWS_DATA,
        
        # Fondations du web
        CSS_HTML_DATA,
    ]
    
    total_categories = len(all_data)
    print(f"📊 Total: {total_categories} catégories de quiz à insérer\n")
    
    success_count = 0
    error_count = 0
    
    for i, data in enumerate(all_data, 1):
        category_name = data["category"]["name"]
        print(f"[{i}/{total_categories}] Traitement de la catégorie: {category_name}")
        
        try:
            seed_category(db, data)
            success_count += 1
            print(f"✅ Catégorie '{category_name}' traitée avec succès\n")
        except Exception as e:
            error_count += 1
            print(f"❌ Erreur sur {category_name}: {str(e)}")
            db.rollback()
            print("-" * 60)
            continue
    
    print("=" * 80)
    print(f"📊 RÉSUMÉ DE L'INSERTION")
    print("=" * 80)
    print(f"✅ Succès: {success_count} catégories")
    if error_count > 0:
        print(f"❌ Échecs: {error_count} catégories")
    print("=" * 80)
    print("\n🎉 Tous les quiz ont été traités!")
    
    db.close()