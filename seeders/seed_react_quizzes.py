"""
Script pour ajouter les quiz React (débutant, intermédiaire, avancé)
avec 10 questions chacun et les catégories correspondantes.

Utilisation:
    python seed_react_quizzes.py
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
# Données des quiz React
# ============================================================================

REACT_QUIZ_DATA = {
    "category": {
        "name": "React",
        "description": "Quiz pour maîtriser React et le développement d'interfaces utilisateur",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg",
        "is_active": True,
    },
    "quizzes": {
        "debutant": {
            "title": "React - Débutant",
            "level": QuizLevel.debutant,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Qu'est-ce que JSX?",
                    "answers": [
                        {"text": "Une extension de syntaxe JavaScript permettant d'écrire du HTML dans JS", "is_correct": True},
                        {"text": "Un langage de programmation basé sur JavaScript", "is_correct": False},
                        {"text": "Un framework CSS pour React", "is_correct": False},
                        {"text": "Un gestionnaire de paquets JavaScript", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment créer un composant fonctionnel React?",
                    "answers": [
                        {"text": "const MonComposant = () => <div>Hello</div>", "is_correct": True},
                        {"text": "function MonComposant.render() { return <div>Hello</div> }", "is_correct": False},
                        {"text": "React.createComponent('MonComposant', () => <div>Hello</div>)", "is_correct": False},
                        {"text": "class MonComposant { render() { return <div>Hello</div> } }", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel hook React gère l'état local d'un composant?",
                    "answers": [
                        {"text": "useState", "is_correct": True},
                        {"text": "useEffect", "is_correct": False},
                        {"text": "useContext", "is_correct": False},
                        {"text": "useRef", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment passer des données à un composant enfant?",
                    "answers": [
                        {"text": "Via les props", "is_correct": True},
                        {"text": "Via setState", "is_correct": False},
                        {"text": "Via useContext uniquement", "is_correct": False},
                        {"text": "Via une variable globale", "is_correct": False},
                    ],
                },
                {
                    "text": "Que retourne useState(0)?",
                    "answers": [
                        {"text": "[valeur, setValeur] - la valeur actuelle et une fonction de mise à jour", "is_correct": True},
                        {"text": "La valeur 0 directement", "is_correct": False},
                        {"text": "Un objet { state: 0, setState: fn }", "is_correct": False},
                        {"text": "Une référence mutable", "is_correct": False},
                    ],
                },
                {
                    "text": "À quoi sert la prop 'key' dans une liste React?",
                    "answers": [
                        {"text": "Aider React à identifier les éléments modifiés, ajoutés ou supprimés", "is_correct": True},
                        {"text": "Donner accès à l'élément depuis le parent", "is_correct": False},
                        {"text": "Définir l'ordre d'affichage des éléments", "is_correct": False},
                        {"text": "Appliquer un style unique à chaque élément", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment importer React dans un fichier?",
                    "answers": [
                        {"text": "import React from 'react'", "is_correct": True},
                        {"text": "require('react')", "is_correct": False},
                        {"text": "import { React } from 'react'", "is_correct": False},
                        {"text": "include React from 'react'", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel outil est recommandé pour créer un projet React rapidement?",
                    "answers": [
                        {"text": "Create React App ou Vite", "is_correct": True},
                        {"text": "npm init react", "is_correct": False},
                        {"text": "react new mon-app", "is_correct": False},
                        {"text": "yarn create app", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment afficher conditionnellement un élément en React?",
                    "answers": [
                        {"text": "{condition && <Composant />}", "is_correct": True},
                        {"text": "<if condition={true}><Composant /></if>", "is_correct": False},
                        {"text": "React.showIf(condition, <Composant />)", "is_correct": False},
                        {"text": "conditional(<Composant />, condition)", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle méthode du cycle de vie est équivalente à useEffect(() => {}, []) ?",
                    "answers": [
                        {"text": "componentDidMount", "is_correct": True},
                        {"text": "componentDidUpdate", "is_correct": False},
                        {"text": "componentWillMount", "is_correct": False},
                        {"text": "shouldComponentUpdate", "is_correct": False},
                    ],
                },
            ],
        },
        "intermediaire": {
            "title": "React - Intermédiaire",
            "level": QuizLevel.intermediaire,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Qu'est-ce que useEffect et quand s'exécute-t-il?",
                    "answers": [
                        {"text": "Un hook qui s'exécute après chaque rendu pour gérer les effets de bord", "is_correct": True},
                        {"text": "Un hook qui s'exécute avant le rendu du composant", "is_correct": False},
                        {"text": "Un hook qui remplace setState dans les composants fonctionnels", "is_correct": False},
                        {"text": "Un hook pour gérer les animations uniquement", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que le Context API?",
                    "answers": [
                        {"text": "Un mécanisme pour partager des données entre composants sans prop drilling", "is_correct": True},
                        {"text": "Une API REST fournie par React", "is_correct": False},
                        {"text": "Un système de routage intégré à React", "is_correct": False},
                        {"text": "Un outil de gestion des requêtes HTTP", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait useCallback?",
                    "answers": [
                        {"text": "Mémoïse une fonction pour éviter sa recréation à chaque rendu", "is_correct": True},
                        {"text": "Crée une fonction asynchrone optimisée", "is_correct": False},
                        {"text": "Gère les callbacks d'événements DOM", "is_correct": False},
                        {"text": "Remplace useEffect pour les appels API", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que le prop drilling?",
                    "answers": [
                        {"text": "Passer des props à travers plusieurs niveaux de composants pour atteindre le bon enfant", "is_correct": True},
                        {"text": "Modifier les props reçues dans un composant enfant", "is_correct": False},
                        {"text": "Valider les props avec PropTypes", "is_correct": False},
                        {"text": "Déboguer les props dans les DevTools", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment mémoïser un composant pour éviter les re-renders inutiles?",
                    "answers": [
                        {"text": "React.memo(MonComposant)", "is_correct": True},
                        {"text": "React.cache(MonComposant)", "is_correct": False},
                        {"text": "useMemo(MonComposant, [])", "is_correct": False},
                        {"text": "MonComposant.pure()", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait useMemo?",
                    "answers": [
                        {"text": "Mémoïse le résultat d'un calcul coûteux entre les rendus", "is_correct": True},
                        {"text": "Mémoïse un composant entier", "is_correct": False},
                        {"text": "Stocke une référence mutable", "is_correct": False},
                        {"text": "Mémoïse les appels API", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un custom hook?",
                    "answers": [
                        {"text": "Une fonction commençant par 'use' qui réutilise de la logique avec des hooks React", "is_correct": True},
                        {"text": "Un hook fourni par une bibliothèque tierce", "is_correct": False},
                        {"text": "Un hook qui modifie le comportement de useState", "is_correct": False},
                        {"text": "Un hook propre aux composants de classe", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment gérer un formulaire contrôlé en React?",
                    "answers": [
                        {"text": "Lier la valeur à un état via value et onChange", "is_correct": True},
                        {"text": "Utiliser directement document.getElementById", "is_correct": False},
                        {"text": "Utiliser useRef sans état", "is_correct": False},
                        {"text": "Laisser le DOM gérer l'état du formulaire", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que useReducer?",
                    "answers": [
                        {"text": "Un hook pour gérer un état complexe via une fonction reducer, alternative à useState", "is_correct": True},
                        {"text": "Un hook pour réduire la taille du bundle", "is_correct": False},
                        {"text": "Un hook qui combine plusieurs états en un", "is_correct": False},
                        {"text": "Une alternative à useEffect pour la logique asynchrone", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment nettoyer un effet dans useEffect?",
                    "answers": [
                        {"text": "Retourner une fonction de nettoyage depuis le callback de useEffect", "is_correct": True},
                        {"text": "Appeler useEffect.cleanup() après l'effet", "is_correct": False},
                        {"text": "Utiliser useLayoutEffect à la place", "is_correct": False},
                        {"text": "Passer un deuxième argument cleanup à useEffect", "is_correct": False},
                    ],
                },
            ],
        },
        "avance": {
            "title": "React - Avancé",
            "level": QuizLevel.avance,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Qu'est-ce que React Concurrent Mode?",
                    "answers": [
                        {"text": "Un mode permettant à React de préparer plusieurs versions de l'UI simultanément", "is_correct": True},
                        {"text": "Un mode multi-thread pour React Native", "is_correct": False},
                        {"text": "Un mode pour gérer plusieurs contextes simultanément", "is_correct": False},
                        {"text": "Un mode de rendu côté serveur parallèle", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que Suspense en React?",
                    "answers": [
                        {"text": "Un composant permettant d'afficher un fallback pendant le chargement de contenu asynchrone", "is_correct": True},
                        {"text": "Un hook pour suspendre l'exécution d'un effet", "is_correct": False},
                        {"text": "Un outil de gestion des erreurs asynchrones", "is_correct": False},
                        {"text": "Un mécanisme pour différer le rendu des composants lourds", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que le Server Component en React 18+?",
                    "answers": [
                        {"text": "Un composant qui s'exécute uniquement côté serveur, sans JS côté client", "is_correct": True},
                        {"text": "Un composant qui fetch des données depuis un serveur", "is_correct": False},
                        {"text": "Un composant SSR classique avec hydratation", "is_correct": False},
                        {"text": "Un composant partagé entre plusieurs serveurs", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment fonctionne le Virtual DOM de React?",
                    "answers": [
                        {"text": "React compare l'ancien et le nouveau Virtual DOM (diffing) puis applique les changements minimaux au DOM réel", "is_correct": True},
                        {"text": "React remplace entièrement le DOM réel à chaque rendu", "is_correct": False},
                        {"text": "React manipule directement le DOM sans abstraction", "is_correct": False},
                        {"text": "React crée un DOM virtuel uniquement pour les animations", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que useTransition en React 18?",
                    "answers": [
                        {"text": "Un hook pour marquer des mises à jour d'état comme non-urgentes afin de garder l'UI responsive", "is_correct": True},
                        {"text": "Un hook pour créer des transitions CSS animées", "is_correct": False},
                        {"text": "Un hook pour gérer les transitions de navigation", "is_correct": False},
                        {"text": "Un hook pour débouncer les mises à jour d'état", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un Error Boundary?",
                    "answers": [
                        {"text": "Un composant de classe qui capture les erreurs JS dans ses enfants et affiche un fallback", "is_correct": True},
                        {"text": "Un hook pour gérer les erreurs dans les composants fonctionnels", "is_correct": False},
                        {"text": "Un outil de linting pour React", "is_correct": False},
                        {"text": "Un wrapper autour de try/catch pour les hooks", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment implémenter le code splitting avec React?",
                    "answers": [
                        {"text": "React.lazy() avec Suspense pour charger les composants à la demande", "is_correct": True},
                        {"text": "En divisant manuellement le fichier bundle", "is_correct": False},
                        {"text": "En utilisant useImport() hook", "is_correct": False},
                        {"text": "En configurant webpack uniquement", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait useImperativeHandle?",
                    "answers": [
                        {"text": "Personnalise les valeurs exposées par un composant via une ref (avec forwardRef)", "is_correct": True},
                        {"text": "Exécute du code impératif en dehors du cycle React", "is_correct": False},
                        {"text": "Accède au DOM de manière impérative", "is_correct": False},
                        {"text": "Remplace useEffect pour les effets impératifs", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que le batching automatique en React 18?",
                    "answers": [
                        {"text": "React regroupe automatiquement plusieurs setState en un seul re-render, même dans des callbacks async", "is_correct": True},
                        {"text": "React divise automatiquement le code en batch pour optimiser le bundle", "is_correct": False},
                        {"text": "React traite les requêtes API en batch", "is_correct": False},
                        {"text": "React group les composants similaires pour les réutiliser", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment optimiser les re-renders causés par le Context?",
                    "answers": [
                        {"text": "Séparer les contextes par domaine et mémoïser les valeurs avec useMemo", "is_correct": True},
                        {"text": "Utiliser useContext dans un seul composant racine", "is_correct": False},
                        {"text": "Éviter complètement useContext et utiliser Redux", "is_correct": False},
                        {"text": "Passer les valeurs du contexte via des props à la place", "is_correct": False},
                    ],
                },
            ],
        },
    },
}


def add_react_quizzes():
    """Ajoute la catégorie React et les quiz avec toutes les questions"""

    try:
        category_name = REACT_QUIZ_DATA["category"]["name"]
        existing_category = (
            db.query(Category).filter(Category.name == category_name).first()
        )

        if existing_category:
            print(f"✓ Catégorie '{category_name}' existe déjà (ID: {existing_category.id})")
            category = existing_category
        else:
            category = Category(
                id=str(uuid.uuid4()),
                name=REACT_QUIZ_DATA["category"]["name"],
                description=REACT_QUIZ_DATA["category"]["description"],
                icon_url=REACT_QUIZ_DATA["category"]["icon_url"],
                is_active=REACT_QUIZ_DATA["category"]["is_active"],
            )
            db.add(category)
            db.commit()
            print(f"✓ Catégorie '{category_name}' créée avec succès (ID: {category.id})")

        for level_name, quiz_data in REACT_QUIZ_DATA["quizzes"].items():
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

        print("\n✅ Tous les quiz React ont été ajoutés avec succès!")

    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de l'ajout des quiz: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Ajout des quiz React (débutant, intermédiaire, avancé)...\n")
    add_react_quizzes()