"""
Script pour ajouter les quiz Git (débutant, intermédiaire, avancé)
avec 10 questions chacun et les catégories correspondantes.

Utilisation:
    python seed_git_quizzes.py
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
# Données des quiz Git
# ============================================================================

GIT_QUIZ_DATA = {
    "category": {
        "name": "Git",
        "description": "Quiz pour maîtriser Git et la gestion de versions",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg",
        "is_active": True,
    },
    "quizzes": {
        "debutant": {
            "title": "Git - Débutant",
            "level": QuizLevel.debutant,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Quelle commande initialise un nouveau dépôt Git?",
                    "answers": [
                        {"text": "git init", "is_correct": True},
                        {"text": "git start", "is_correct": False},
                        {"text": "git create", "is_correct": False},
                        {"text": "git new", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment ajouter tous les fichiers modifiés au staging area?",
                    "answers": [
                        {"text": "git add .", "is_correct": True},
                        {"text": "git stage all", "is_correct": False},
                        {"text": "git commit --all", "is_correct": False},
                        {"text": "git push all", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment créer un commit avec un message?",
                    "answers": [
                        {"text": "git commit -m 'mon message'", "is_correct": True},
                        {"text": "git save 'mon message'", "is_correct": False},
                        {"text": "git commit --message 'mon message'", "is_correct": False},
                        {"text": "git push -m 'mon message'", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle commande affiche l'historique des commits?",
                    "answers": [
                        {"text": "git log", "is_correct": True},
                        {"text": "git history", "is_correct": False},
                        {"text": "git commits", "is_correct": False},
                        {"text": "git show-all", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment créer une nouvelle branche?",
                    "answers": [
                        {"text": "git branch nom-branche", "is_correct": True},
                        {"text": "git new-branch nom-branche", "is_correct": False},
                        {"text": "git create branch nom-branche", "is_correct": False},
                        {"text": "git checkout new nom-branche", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment basculer sur une branche existante?",
                    "answers": [
                        {"text": "git checkout nom-branche", "is_correct": True},
                        {"text": "git switch-to nom-branche", "is_correct": False},
                        {"text": "git go nom-branche", "is_correct": False},
                        {"text": "git use nom-branche", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment envoyer les commits vers le dépôt distant?",
                    "answers": [
                        {"text": "git push origin nom-branche", "is_correct": True},
                        {"text": "git upload origin nom-branche", "is_correct": False},
                        {"text": "git send origin nom-branche", "is_correct": False},
                        {"text": "git sync origin nom-branche", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment récupérer et fusionner les changements distants?",
                    "answers": [
                        {"text": "git pull", "is_correct": True},
                        {"text": "git fetch --merge", "is_correct": False},
                        {"text": "git download", "is_correct": False},
                        {"text": "git sync", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment cloner un dépôt distant?",
                    "answers": [
                        {"text": "git clone url-du-depot", "is_correct": True},
                        {"text": "git copy url-du-depot", "is_correct": False},
                        {"text": "git download url-du-depot", "is_correct": False},
                        {"text": "git init url-du-depot", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle commande affiche le statut des fichiers?",
                    "answers": [
                        {"text": "git status", "is_correct": True},
                        {"text": "git check", "is_correct": False},
                        {"text": "git info", "is_correct": False},
                        {"text": "git show", "is_correct": False},
                    ],
                },
            ],
        },
        "intermediaire": {
            "title": "Git - Intermédiaire",
            "level": QuizLevel.intermediaire,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Quelle est la différence entre git merge et git rebase?",
                    "answers": [
                        {"text": "rebase réécrit l'historique en linéarisant les commits, merge crée un commit de fusion", "is_correct": True},
                        {"text": "merge est plus sécurisé car il ne modifie jamais l'historique", "is_correct": False},
                        {"text": "rebase fusionne uniquement les fichiers, merge fusionne les branches", "is_correct": False},
                        {"text": "Aucune différence de résultat, seulement de performance", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait git stash?",
                    "answers": [
                        {"text": "Sauvegarde temporairement les modifications non commitées pour nettoyer le working directory", "is_correct": True},
                        {"text": "Supprime toutes les modifications non commitées", "is_correct": False},
                        {"text": "Crée une branche temporaire avec les modifications", "is_correct": False},
                        {"text": "Archive les anciens commits", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un conflit de merge?",
                    "answers": [
                        {"text": "Quand deux branches ont modifié les mêmes lignes et Git ne peut pas fusionner automatiquement", "is_correct": True},
                        {"text": "Quand une branche est trop ancienne pour être fusionnée", "is_correct": False},
                        {"text": "Quand deux développeurs pushent en même temps", "is_correct": False},
                        {"text": "Quand le dépôt distant refuse la fusion", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment annuler le dernier commit en gardant les modifications?",
                    "answers": [
                        {"text": "git reset --soft HEAD~1", "is_correct": True},
                        {"text": "git undo last", "is_correct": False},
                        {"text": "git revert HEAD", "is_correct": False},
                        {"text": "git reset --hard HEAD~1", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait git cherry-pick?",
                    "answers": [
                        {"text": "Applique les modifications d'un commit spécifique sur la branche courante", "is_correct": True},
                        {"text": "Sélectionne les meilleurs commits pour un release", "is_correct": False},
                        {"text": "Fusionne sélectivement certains fichiers d'une branche", "is_correct": False},
                        {"text": "Copie une branche entière dans une autre", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment créer et basculer sur une branche en une seule commande?",
                    "answers": [
                        {"text": "git checkout -b nom-branche", "is_correct": True},
                        {"text": "git branch -m nom-branche", "is_correct": False},
                        {"text": "git new -b nom-branche", "is_correct": False},
                        {"text": "git branch --switch nom-branche", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un tag Git?",
                    "answers": [
                        {"text": "Un pointeur nommé vers un commit spécifique, souvent utilisé pour les releases", "is_correct": True},
                        {"text": "Un label sur une branche pour la retrouver facilement", "is_correct": False},
                        {"text": "Un commentaire attaché à un commit", "is_correct": False},
                        {"text": "Une branche permanente qui ne peut pas être supprimée", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait git fetch (sans merge)?",
                    "answers": [
                        {"text": "Télécharge les changements distants sans les fusionner dans la branche locale", "is_correct": True},
                        {"text": "Met à jour uniquement le fichier .gitconfig", "is_correct": False},
                        {"text": "Télécharge et applique automatiquement les changements", "is_correct": False},
                        {"text": "Synchronise uniquement les tags", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment voir les différences entre deux branches?",
                    "answers": [
                        {"text": "git diff branche1..branche2", "is_correct": True},
                        {"text": "git compare branche1 branche2", "is_correct": False},
                        {"text": "git show branche1 vs branche2", "is_correct": False},
                        {"text": "git branch --diff branche1 branche2", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un fichier .gitignore?",
                    "answers": [
                        {"text": "Un fichier listant les patterns de fichiers/dossiers que Git doit ignorer", "is_correct": True},
                        {"text": "Un fichier qui désactive Git dans un sous-dossier", "is_correct": False},
                        {"text": "Un fichier de configuration des droits d'accès", "is_correct": False},
                        {"text": "Un fichier qui liste les collaborateurs exclus", "is_correct": False},
                    ],
                },
            ],
        },
        "avance": {
            "title": "Git - Avancé",
            "level": QuizLevel.avance,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Quelle est la différence entre git reset --soft, --mixed et --hard?",
                    "answers": [
                        {"text": "--soft garde staging+working, --mixed réinitialise staging, --hard réinitialise tout", "is_correct": True},
                        {"text": "--soft est le plus destructif, --hard le plus sûr", "is_correct": False},
                        {"text": "--hard garde les modifications en stash, --soft les supprime", "is_correct": False},
                        {"text": "Les trois font la même chose avec des performances différentes", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un rebase interactif (git rebase -i)?",
                    "answers": [
                        {"text": "Permet de réécrire l'historique : réordonner, squash, edit, drop des commits", "is_correct": True},
                        {"text": "Lance un rebase avec confirmation pour chaque commit", "is_correct": False},
                        {"text": "Ouvre une interface graphique pour le rebase", "is_correct": False},
                        {"text": "Effectue un rebase en mode interactif entre deux dépôts", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que git reflog?",
                    "answers": [
                        {"text": "Un journal de tous les mouvements de HEAD permettant de récupérer des commits perdus", "is_correct": True},
                        {"text": "Un log des références distantes synchronisées", "is_correct": False},
                        {"text": "L'historique des modifications du fichier .gitconfig", "is_correct": False},
                        {"text": "Un log filtré des commits de références (tags)", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un submodule Git?",
                    "answers": [
                        {"text": "Un dépôt Git imbriqué dans un autre dépôt, référencé par un commit spécifique", "is_correct": True},
                        {"text": "Un sous-dossier avec ses propres règles .gitignore", "is_correct": False},
                        {"text": "Un module npm intégré dans le dépôt Git", "is_correct": False},
                        {"text": "Une branche qui agit comme un dépôt indépendant", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait git bisect?",
                    "answers": [
                        {"text": "Une recherche binaire dans l'historique pour trouver le commit ayant introduit un bug", "is_correct": True},
                        {"text": "Divise un commit en deux commits plus petits", "is_correct": False},
                        {"text": "Compare deux branches ligne par ligne", "is_correct": False},
                        {"text": "Crée deux branches symétriques à partir d'un commit", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment signer cryptographiquement un commit Git?",
                    "answers": [
                        {"text": "git commit -S -m 'message' avec une clé GPG configurée", "is_correct": True},
                        {"text": "git commit --sign -m 'message' avec un certificat SSL", "is_correct": False},
                        {"text": "git commit --verified -m 'message'", "is_correct": False},
                        {"text": "Les commits sont signés automatiquement avec le SSH key", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que git worktree?",
                    "answers": [
                        {"text": "Permet d'avoir plusieurs working directories pour différentes branches simultanément", "is_correct": True},
                        {"text": "Un outil pour gérer l'arborescence des fichiers du dépôt", "is_correct": False},
                        {"text": "Un visualiseur de l'arbre de commits", "is_correct": False},
                        {"text": "Un système de verrouillage de fichiers pour les équipes", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment squash plusieurs commits en un seul?",
                    "answers": [
                        {"text": "git rebase -i HEAD~n puis changer 'pick' en 'squash' pour les commits à fusionner", "is_correct": True},
                        {"text": "git merge --squash nom-branche", "is_correct": False},
                        {"text": "git commit --squash HEAD~n", "is_correct": False},
                        {"text": "git rebase --squash n", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un hook Git?",
                    "answers": [
                        {"text": "Des scripts exécutés automatiquement lors d'événements Git (pre-commit, post-push, etc.)", "is_correct": True},
                        {"text": "Un point d'ancrage pour connecter plusieurs dépôts entre eux", "is_correct": False},
                        {"text": "Un système de webhooks vers des services externes", "is_correct": False},
                        {"text": "Un mécanisme pour accrocher des branches à des tags", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait git filter-branch ou git filter-repo?",
                    "answers": [
                        {"text": "Réécrit l'historique Git en masse (supprimer un fichier sensible de tous les commits)", "is_correct": True},
                        {"text": "Filtre les branches selon des critères de nom", "is_correct": False},
                        {"text": "Applique des filtres de merge pour résoudre les conflits automatiquement", "is_correct": False},
                        {"text": "Crée un nouveau dépôt avec seulement les branches filtrées", "is_correct": False},
                    ],
                },
            ],
        },
    },
}


def add_git_quizzes():
    """Ajoute la catégorie Git et les quiz avec toutes les questions"""

    try:
        category_name = GIT_QUIZ_DATA["category"]["name"]
        existing_category = (
            db.query(Category).filter(Category.name == category_name).first()
        )

        if existing_category:
            print(f"✓ Catégorie '{category_name}' existe déjà (ID: {existing_category.id})")
            category = existing_category
        else:
            category = Category(
                id=str(uuid.uuid4()),
                name=GIT_QUIZ_DATA["category"]["name"],
                description=GIT_QUIZ_DATA["category"]["description"],
                icon_url=GIT_QUIZ_DATA["category"]["icon_url"],
                is_active=GIT_QUIZ_DATA["category"]["is_active"],
            )
            db.add(category)
            db.commit()
            print(f"✓ Catégorie '{category_name}' créée avec succès (ID: {category.id})")

        for level_name, quiz_data in GIT_QUIZ_DATA["quizzes"].items():
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

        print("\n✅ Tous les quiz Git ont été ajoutés avec succès!")

    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de l'ajout des quiz: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Ajout des quiz Git (débutant, intermédiaire, avancé)...\n")
    add_git_quizzes()