"""
Script pour ajouter les quiz Docker (débutant, intermédiaire, avancé)
avec 10 questions chacun et les catégories correspondantes.

Utilisation:
    python seed_docker_quizzes.py
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
# Données des quiz Docker
# ============================================================================

DOCKER_QUIZ_DATA = {
    "category": {
        "name": "Docker",
        "description": "Quiz pour maîtriser Docker et la conteneurisation",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg",
        "is_active": True,
    },
    "quizzes": {
        "debutant": {
            "title": "Docker - Débutant",
            "level": QuizLevel.debutant,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Qu'est-ce qu'un conteneur Docker?",
                    "answers": [
                        {"text": "Un environnement d'exécution isolé et léger qui empaquette une application et ses dépendances", "is_correct": True},
                        {"text": "Une machine virtuelle légère", "is_correct": False},
                        {"text": "Un serveur dédié dans le cloud", "is_correct": False},
                        {"text": "Un fichier de configuration d'application", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'une image Docker?",
                    "answers": [
                        {"text": "Un template immuable servant de base pour créer des conteneurs", "is_correct": True},
                        {"text": "Une capture d'écran d'un conteneur en cours d'exécution", "is_correct": False},
                        {"text": "Une sauvegarde d'un conteneur arrêté", "is_correct": False},
                        {"text": "Un fichier de configuration Docker", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle commande lance un conteneur Docker?",
                    "answers": [
                        {"text": "docker run image-name", "is_correct": True},
                        {"text": "docker start image-name", "is_correct": False},
                        {"text": "docker launch image-name", "is_correct": False},
                        {"text": "docker exec image-name", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment lister les conteneurs en cours d'exécution?",
                    "answers": [
                        {"text": "docker ps", "is_correct": True},
                        {"text": "docker list", "is_correct": False},
                        {"text": "docker containers", "is_correct": False},
                        {"text": "docker show", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel fichier définit comment construire une image Docker?",
                    "answers": [
                        {"text": "Dockerfile", "is_correct": True},
                        {"text": "docker-config.yml", "is_correct": False},
                        {"text": "container.json", "is_correct": False},
                        {"text": "build.docker", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment construire une image depuis un Dockerfile?",
                    "answers": [
                        {"text": "docker build -t nom-image .", "is_correct": True},
                        {"text": "docker create -t nom-image .", "is_correct": False},
                        {"text": "docker compile nom-image .", "is_correct": False},
                        {"text": "docker make -t nom-image", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment arrêter un conteneur Docker?",
                    "answers": [
                        {"text": "docker stop container-id", "is_correct": True},
                        {"text": "docker kill container-id", "is_correct": False},
                        {"text": "docker end container-id", "is_correct": False},
                        {"text": "docker halt container-id", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle instruction Dockerfile définit l'image de base?",
                    "answers": [
                        {"text": "FROM", "is_correct": True},
                        {"text": "BASE", "is_correct": False},
                        {"text": "IMAGE", "is_correct": False},
                        {"text": "INHERIT", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment mapper un port du conteneur vers l'hôte?",
                    "answers": [
                        {"text": "docker run -p 8080:80 image-name", "is_correct": True},
                        {"text": "docker run --port 8080:80 image-name", "is_correct": False},
                        {"text": "docker run -map 8080:80 image-name", "is_correct": False},
                        {"text": "docker run --expose 8080:80 image-name", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle commande télécharge une image depuis Docker Hub?",
                    "answers": [
                        {"text": "docker pull nom-image", "is_correct": True},
                        {"text": "docker download nom-image", "is_correct": False},
                        {"text": "docker get nom-image", "is_correct": False},
                        {"text": "docker fetch nom-image", "is_correct": False},
                    ],
                },
            ],
        },
        "intermediaire": {
            "title": "Docker - Intermédiaire",
            "level": QuizLevel.intermediaire,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Qu'est-ce que Docker Compose?",
                    "answers": [
                        {"text": "Un outil pour définir et gérer des applications multi-conteneurs via un fichier YAML", "is_correct": True},
                        {"text": "Un éditeur de Dockerfile graphique", "is_correct": False},
                        {"text": "Un orchestrateur de conteneurs en production", "is_correct": False},
                        {"text": "Un outil pour optimiser la taille des images", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle est la différence entre COPY et ADD dans un Dockerfile?",
                    "answers": [
                        {"text": "ADD supporte les URLs et l'extraction d'archives tar, COPY est plus simple et préféré", "is_correct": True},
                        {"text": "COPY est plus rapide, ADD est plus complet", "is_correct": False},
                        {"text": "ADD copie depuis l'hôte, COPY depuis un autre conteneur", "is_correct": False},
                        {"text": "Aucune différence fonctionnelle", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un volume Docker?",
                    "answers": [
                        {"text": "Un mécanisme pour persister les données en dehors du cycle de vie du conteneur", "is_correct": True},
                        {"text": "La taille maximale allouée à un conteneur", "is_correct": False},
                        {"text": "Un système de fichiers partagé entre images", "is_correct": False},
                        {"text": "Un espace de stockage temporaire dans le conteneur", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait l'instruction ENTRYPOINT dans un Dockerfile?",
                    "answers": [
                        {"text": "Définit le processus principal qui s'exécute au démarrage du conteneur", "is_correct": True},
                        {"text": "Définit le répertoire de travail dans le conteneur", "is_correct": False},
                        {"text": "Expose un port du conteneur", "is_correct": False},
                        {"text": "Définit les variables d'environnement au démarrage", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment exécuter une commande dans un conteneur en cours d'exécution?",
                    "answers": [
                        {"text": "docker exec -it container-id bash", "is_correct": True},
                        {"text": "docker run container-id bash", "is_correct": False},
                        {"text": "docker attach container-id bash", "is_correct": False},
                        {"text": "docker connect container-id bash", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un réseau Docker (Docker network)?",
                    "answers": [
                        {"text": "Un espace réseau isolé permettant aux conteneurs de communiquer entre eux", "is_correct": True},
                        {"text": "La configuration réseau de l'hôte Docker", "is_correct": False},
                        {"text": "Un proxy réseau pour les conteneurs", "is_correct": False},
                        {"text": "Un pare-feu pour les conteneurs", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que le multi-stage build?",
                    "answers": [
                        {"text": "Utiliser plusieurs instructions FROM pour réduire la taille finale de l'image", "is_correct": True},
                        {"text": "Construire une image en plusieurs étapes parallèles", "is_correct": False},
                        {"text": "Déployer l'image sur plusieurs environnements simultanément", "is_correct": False},
                        {"text": "Versionner une image avec plusieurs tags", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle est la différence entre CMD et ENTRYPOINT?",
                    "answers": [
                        {"text": "ENTRYPOINT est le processus principal (difficilement remplaçable), CMD fournit les arguments par défaut (remplaçables)", "is_correct": True},
                        {"text": "CMD s'exécute au build, ENTRYPOINT au runtime", "is_correct": False},
                        {"text": "ENTRYPOINT permet plusieurs commandes, CMD une seule", "is_correct": False},
                        {"text": "Aucune différence, ils sont interchangeables", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment voir les logs d'un conteneur Docker?",
                    "answers": [
                        {"text": "docker logs container-id", "is_correct": True},
                        {"text": "docker output container-id", "is_correct": False},
                        {"text": "docker inspect container-id --logs", "is_correct": False},
                        {"text": "docker show-logs container-id", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment supprimer toutes les images Docker non utilisées?",
                    "answers": [
                        {"text": "docker image prune -a", "is_correct": True},
                        {"text": "docker rmi --all", "is_correct": False},
                        {"text": "docker clean images", "is_correct": False},
                        {"text": "docker remove unused", "is_correct": False},
                    ],
                },
            ],
        },
        "avance": {
            "title": "Docker - Avancé",
            "level": QuizLevel.avance,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Qu'est-ce que Docker Swarm?",
                    "answers": [
                        {"text": "Le mode d'orchestration natif de Docker pour gérer un cluster de nœuds", "is_correct": True},
                        {"text": "Un outil de monitoring pour les conteneurs Docker", "is_correct": False},
                        {"text": "Un gestionnaire de volumes distribués", "is_correct": False},
                        {"text": "Un système de load balancing pour une seule machine", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment fonctionne le cache des layers dans Docker?",
                    "answers": [
                        {"text": "Chaque instruction Dockerfile crée un layer ; si le layer n'a pas changé, Docker réutilise le cache", "is_correct": True},
                        {"text": "Docker cache uniquement la dernière image construite", "is_correct": False},
                        {"text": "Le cache est partagé entre tous les utilisateurs du système", "is_correct": False},
                        {"text": "Docker n'utilise pas de cache, il reconstruit toujours depuis zéro", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un Docker Registry?",
                    "answers": [
                        {"text": "Un serveur de stockage et distribution d'images Docker (public comme Docker Hub ou privé)", "is_correct": True},
                        {"text": "Le registre Windows pour les conteneurs Docker", "is_correct": False},
                        {"text": "Un outil de configuration centralisée pour les conteneurs", "is_correct": False},
                        {"text": "La base de données interne de Docker", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment limiter les ressources CPU et mémoire d'un conteneur?",
                    "answers": [
                        {"text": "docker run --memory='512m' --cpus='0.5' image-name", "is_correct": True},
                        {"text": "docker run --max-memory=512 --max-cpu=50% image-name", "is_correct": False},
                        {"text": "docker run --resources cpu=0.5,mem=512 image-name", "is_correct": False},
                        {"text": "docker run --limit '512m:0.5cpu' image-name", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que le namespacing dans Docker?",
                    "answers": [
                        {"text": "Un mécanisme Linux qui isole les ressources (PID, réseau, filesystem...) entre conteneurs", "is_correct": True},
                        {"text": "Un système de nommage des images et conteneurs", "is_correct": False},
                        {"text": "Un outil pour organiser les images par namespace dans un registry", "is_correct": False},
                        {"text": "Un mécanisme de routage réseau entre conteneurs", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment créer un secret Docker Swarm?",
                    "answers": [
                        {"text": "echo 'valeur' | docker secret create nom-secret -", "is_correct": True},
                        {"text": "docker secret add nom-secret 'valeur'", "is_correct": False},
                        {"text": "docker config create --secret nom-secret 'valeur'", "is_correct": False},
                        {"text": "docker env set SECRET=valeur", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que Docker BuildKit?",
                    "answers": [
                        {"text": "Un backend de build amélioré offrant de meilleures performances, cache et fonctionnalités (builds parallèles, secrets de build)", "is_correct": True},
                        {"text": "Un toolkit pour créer des images Docker depuis des scripts shell", "is_correct": False},
                        {"text": "Un plugin pour intégrer Docker dans les IDE", "is_correct": False},
                        {"text": "Un compilateur spécial pour optimiser les Dockerfile", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle est la différence entre un bind mount et un volume Docker?",
                    "answers": [
                        {"text": "Un bind mount pointe vers un chemin spécifique de l'hôte, un volume est géré par Docker (plus portable)", "is_correct": True},
                        {"text": "Un volume est temporaire, un bind mount est persistant", "is_correct": False},
                        {"text": "Un bind mount est plus performant que les volumes dans tous les cas", "is_correct": False},
                        {"text": "Les volumes existent uniquement dans Docker Swarm", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment inspecter les détails complets d'un conteneur?",
                    "answers": [
                        {"text": "docker inspect container-id", "is_correct": True},
                        {"text": "docker details container-id", "is_correct": False},
                        {"text": "docker info container-id", "is_correct": False},
                        {"text": "docker describe container-id", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que cgroups dans le contexte Docker?",
                    "answers": [
                        {"text": "Un mécanisme Linux de limitation et monitoring des ressources (CPU, mémoire, I/O) par groupe de processus", "is_correct": True},
                        {"text": "Un système de groupes de conteneurs dans Docker Compose", "is_correct": False},
                        {"text": "Un gestionnaire de groupes d'utilisateurs pour les permissions Docker", "is_correct": False},
                        {"text": "Un outil de clustering pour les conteneurs", "is_correct": False},
                    ],
                },
            ],
        },
    },
}


def add_docker_quizzes():
    """Ajoute la catégorie Docker et les quiz avec toutes les questions"""

    try:
        category_name = DOCKER_QUIZ_DATA["category"]["name"]
        existing_category = (
            db.query(Category).filter(Category.name == category_name).first()
        )

        if existing_category:
            print(f"✓ Catégorie '{category_name}' existe déjà (ID: {existing_category.id})")
            category = existing_category
        else:
            category = Category(
                id=str(uuid.uuid4()),
                name=DOCKER_QUIZ_DATA["category"]["name"],
                description=DOCKER_QUIZ_DATA["category"]["description"],
                icon_url=DOCKER_QUIZ_DATA["category"]["icon_url"],
                is_active=DOCKER_QUIZ_DATA["category"]["is_active"],
            )
            db.add(category)
            db.commit()
            print(f"✓ Catégorie '{category_name}' créée avec succès (ID: {category.id})")

        for level_name, quiz_data in DOCKER_QUIZ_DATA["quizzes"].items():
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

        print("\n✅ Tous les quiz Docker ont été ajoutés avec succès!")

    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de l'ajout des quiz: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Ajout des quiz Docker (débutant, intermédiaire, avancé)...\n")
    add_docker_quizzes()