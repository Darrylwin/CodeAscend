"""
Script pour ajouter les quiz NestJS (débutant, intermédiaire, avancé)
avec 10 questions chacun et les catégories correspondantes.

Utilisation:
    python seed_nestjs_quizzes.py
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
# Données des quiz NestJS
# ============================================================================

NESTJS_QUIZ_DATA = {
    "category": {
        "name": "NestJS",
        "description": "Quiz pour maîtriser NestJS et le développement backend Node.js",
        "icon_url": "https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nestjs/nestjs-plain.svg",
        "is_active": True,
    },
    "quizzes": {
        "debutant": {
            "title": "NestJS - Débutant",
            "level": QuizLevel.debutant,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Sur quel runtime NestJS s'exécute-t-il?",
                    "answers": [
                        {"text": "Node.js", "is_correct": True},
                        {"text": "Deno", "is_correct": False},
                        {"text": "Bun", "is_correct": False},
                        {"text": "PHP", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel décorateur marque une classe comme contrôleur NestJS?",
                    "answers": [
                        {"text": "@Controller()", "is_correct": True},
                        {"text": "@Route()", "is_correct": False},
                        {"text": "@Handler()", "is_correct": False},
                        {"text": "@Endpoint()", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel décorateur NestJS définit un service injectable?",
                    "answers": [
                        {"text": "@Injectable()", "is_correct": True},
                        {"text": "@Service()", "is_correct": False},
                        {"text": "@Provider()", "is_correct": False},
                        {"text": "@Singleton()", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment déclarer une route GET dans un contrôleur NestJS?",
                    "answers": [
                        {"text": "@Get('chemin')", "is_correct": True},
                        {"text": "@Route.get('chemin')", "is_correct": False},
                        {"text": "@Http.Get('chemin')", "is_correct": False},
                        {"text": "@GetMapping('chemin')", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un Module en NestJS?",
                    "answers": [
                        {"text": "Une classe annotée @Module() qui organise les composants de l'application", "is_correct": True},
                        {"text": "Un fichier de configuration", "is_correct": False},
                        {"text": "Un middleware", "is_correct": False},
                        {"text": "Un service partagé", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment récupérer un paramètre d'URL dans NestJS?",
                    "answers": [
                        {"text": "@Param('id') id: string", "is_correct": True},
                        {"text": "@UrlParam('id') id: string", "is_correct": False},
                        {"text": "req.params.id", "is_correct": False},
                        {"text": "@PathVariable('id') id: string", "is_correct": False},
                    ],
                },
                {
                    "text": "Quelle commande crée un nouveau projet NestJS?",
                    "answers": [
                        {"text": "nest new nom-projet", "is_correct": True},
                        {"text": "nestjs create nom-projet", "is_correct": False},
                        {"text": "npx create-nest-app nom-projet", "is_correct": False},
                        {"text": "nest init nom-projet", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment accéder au body d'une requête POST dans NestJS?",
                    "answers": [
                        {"text": "@Body() body: CreateDto", "is_correct": True},
                        {"text": "@Request() req - puis req.body", "is_correct": False},
                        {"text": "@Payload() payload: CreateDto", "is_correct": False},
                        {"text": "@Data() data: CreateDto", "is_correct": False},
                    ],
                },
                {
                    "text": "Quel décorateur NestJS définit une route DELETE?",
                    "answers": [
                        {"text": "@Delete(':id')", "is_correct": True},
                        {"text": "@Remove(':id')", "is_correct": False},
                        {"text": "@Http.Delete(':id')", "is_correct": False},
                        {"text": "@Destroy(':id')", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment injecter un service dans un contrôleur NestJS?",
                    "answers": [
                        {"text": "constructor(private readonly monService: MonService) {}", "is_correct": True},
                        {"text": "@Inject() monService: MonService", "is_correct": False},
                        {"text": "this.monService = new MonService()", "is_correct": False},
                        {"text": "useService(MonService)", "is_correct": False},
                    ],
                },
            ],
        },
        "intermediaire": {
            "title": "NestJS - Intermédiaire",
            "level": QuizLevel.intermediaire,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Qu'est-ce qu'un Guard en NestJS?",
                    "answers": [
                        {"text": "Un composant qui détermine si une requête peut accéder à une route (autorisation)", "is_correct": True},
                        {"text": "Un middleware de validation des données", "is_correct": False},
                        {"text": "Un intercepteur pour transformer les réponses", "is_correct": False},
                        {"text": "Un filtre pour gérer les exceptions", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un Pipe en NestJS?",
                    "answers": [
                        {"text": "Un composant pour transformer et/ou valider les données entrantes", "is_correct": True},
                        {"text": "Un outil pour connecter deux services", "is_correct": False},
                        {"text": "Un middleware de logging", "is_correct": False},
                        {"text": "Un décorateur pour les propriétés de classe", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment utiliser la validation DTO avec class-validator dans NestJS?",
                    "answers": [
                        {"text": "En combinant @Body() avec ValidationPipe et des décorateurs comme @IsString()", "is_correct": True},
                        {"text": "En utilisant @Validate() sur le DTO", "is_correct": False},
                        {"text": "En appelant validate(dto) manuellement dans le contrôleur", "is_correct": False},
                        {"text": "En configurant validateSchema dans le module", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un Interceptor en NestJS?",
                    "answers": [
                        {"text": "Un composant qui intercepte les requêtes/réponses pour transformer, logger ou étendre le comportement", "is_correct": True},
                        {"text": "Un outil pour intercepter les erreurs HTTP uniquement", "is_correct": False},
                        {"text": "Un composant qui bloque certaines requêtes", "is_correct": False},
                        {"text": "Un middleware de compression des réponses", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment créer un module NestJS avec la CLI?",
                    "answers": [
                        {"text": "nest generate module nom", "is_correct": True},
                        {"text": "nest create module nom", "is_correct": False},
                        {"text": "nest add module nom", "is_correct": False},
                        {"text": "nestjs module create nom", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un Exception Filter en NestJS?",
                    "answers": [
                        {"text": "Un composant qui capture les exceptions et renvoie des réponses d'erreur appropriées", "is_correct": True},
                        {"text": "Un filtre pour bloquer certaines exceptions au niveau réseau", "is_correct": False},
                        {"text": "Un système de logging des erreurs uniquement", "is_correct": False},
                        {"text": "Un middleware qui catch les erreurs asynchrones", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment configurer TypeORM dans un module NestJS?",
                    "answers": [
                        {"text": "TypeOrmModule.forRoot(config) dans AppModule", "is_correct": True},
                        {"text": "OrmModule.register(config) dans AppModule", "is_correct": False},
                        {"text": "DatabaseModule.connect(config) dans AppModule", "is_correct": False},
                        {"text": "TypeORM.initialize(config) dans main.ts", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que le scope d'un provider dans NestJS?",
                    "answers": [
                        {"text": "La durée de vie du provider : DEFAULT (singleton), REQUEST ou TRANSIENT", "is_correct": True},
                        {"text": "La portée des imports autorisés dans le module", "is_correct": False},
                        {"text": "Le niveau d'accès (public/privé) du provider", "is_correct": False},
                        {"text": "La zone du code où le provider peut être injecté", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment implémenter une authentification JWT avec NestJS?",
                    "answers": [
                        {"text": "En utilisant @nestjs/jwt et @nestjs/passport avec JwtStrategy", "is_correct": True},
                        {"text": "En ajoutant le middleware jwt dans main.ts", "is_correct": False},
                        {"text": "En utilisant le décorateur @Authenticate() sur les routes", "is_correct": False},
                        {"text": "En configurant SecurityModule dans AppModule", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment récupérer les query params dans NestJS?",
                    "answers": [
                        {"text": "@Query('page') page: number", "is_correct": True},
                        {"text": "@QueryParam('page') page: number", "is_correct": False},
                        {"text": "@Search('page') page: number", "is_correct": False},
                        {"text": "req.query.page", "is_correct": False},
                    ],
                },
            ],
        },
        "avance": {
            "title": "NestJS - Avancé",
            "level": QuizLevel.avance,
            "status": QuizStatus.published,
            "questions": [
                {
                    "text": "Qu'est-ce que le système de microservices dans NestJS?",
                    "answers": [
                        {"text": "Un ensemble de transports (TCP, Redis, NATS...) pour communication inter-services", "is_correct": True},
                        {"text": "Une architecture pour diviser le code en micro-modules", "is_correct": False},
                        {"text": "Un outil de déploiement automatique", "is_correct": False},
                        {"text": "Un système de monitoring des performances", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment utiliser les CQRS dans NestJS?",
                    "answers": [
                        {"text": "Avec @nestjs/cqrs via CommandBus, QueryBus, et les handlers correspondants", "is_correct": True},
                        {"text": "En séparant manuellement les contrôleurs en Command et Query", "is_correct": False},
                        {"text": "En utilisant le module @nestjs/command", "is_correct": False},
                        {"text": "En configurant deux bases de données séparées", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce qu'un Dynamic Module en NestJS?",
                    "answers": [
                        {"text": "Un module configurable via forRoot()/forFeature() qui retourne ses propres providers dynamiquement", "is_correct": True},
                        {"text": "Un module chargé à la demande (lazy loading)", "is_correct": False},
                        {"text": "Un module créé à l'exécution depuis une configuration externe", "is_correct": False},
                        {"text": "Un module qui change de comportement selon l'environnement", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment implémenter un Custom Decorator dans NestJS?",
                    "answers": [
                        {"text": "createParamDecorator((data, ctx) => ctx.switchToHttp().getRequest())", "is_correct": True},
                        {"text": "function MyDecorator(target, key, descriptor) { return descriptor; }", "is_correct": False},
                        {"text": "Nest.decorator((req) => req.user)", "is_correct": False},
                        {"text": "@CustomParam() dans le contrôleur directement", "is_correct": False},
                    ],
                },
                {
                    "text": "Que fait @nestjs/schedule et comment planifier une tâche?",
                    "answers": [
                        {"text": "Gère les tâches planifiées via des décorateurs comme @Cron(), @Interval(), @Timeout()", "is_correct": True},
                        {"text": "Planifie des requêtes HTTP différées", "is_correct": False},
                        {"text": "Gère le scheduling des workers de microservices", "is_correct": False},
                        {"text": "Crée une queue de tâches asynchrones", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment utiliser les Queues avec Bull dans NestJS?",
                    "answers": [
                        {"text": "Avec @nestjs/bull, BullModule.registerQueue() et les décorateurs @Processor/@Process", "is_correct": True},
                        {"text": "En utilisant QueueModule.create() et les JobHandlers", "is_correct": False},
                        {"text": "En configurant Redis directement et en utilisant des Subscribers", "is_correct": False},
                        {"text": "Avec @nestjs/queue et le décorateur @QueueWorker", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que l'Execution Context dans NestJS?",
                    "answers": [
                        {"text": "Un wrapper qui donne accès à la requête actuelle quel que soit le transport (HTTP, WS, RPC)", "is_correct": True},
                        {"text": "Le contexte d'exécution du moteur JavaScript", "is_correct": False},
                        {"text": "L'environnement dans lequel NestJS s'exécute", "is_correct": False},
                        {"text": "Le scope d'un interceptor appliqué globalement", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment implémenter des WebSockets avec NestJS?",
                    "answers": [
                        {"text": "Avec @WebSocketGateway() et les décorateurs @SubscribeMessage(), @WebSocketServer()", "is_correct": True},
                        {"text": "En utilisant SocketController() avec des @OnMessage() handlers", "is_correct": False},
                        {"text": "En configurant ws dans le AppModule directement", "is_correct": False},
                        {"text": "En utilisant @nestjs/realtime et RealtimeModule", "is_correct": False},
                    ],
                },
                {
                    "text": "Qu'est-ce que la Circular Dependency et comment la résoudre dans NestJS?",
                    "answers": [
                        {"text": "Deux modules/services qui se référencent mutuellement - résolu avec forwardRef()", "is_correct": True},
                        {"text": "Un import circulaire de fichiers - résolu en restructurant les modules", "is_correct": False},
                        {"text": "Une dépendance qui se réinstancie elle-même - résolu avec un Singleton pattern", "is_correct": False},
                        {"text": "Un provider qui s'injecte lui-même - désactivé par NestJS automatiquement", "is_correct": False},
                    ],
                },
                {
                    "text": "Comment tester unitairement un service NestJS?",
                    "answers": [
                        {"text": "Avec Test.createTestingModule(), en mockant les dépendances via providers", "is_correct": True},
                        {"text": "En instanciant directement le service avec new MonService()", "is_correct": False},
                        {"text": "En utilisant NestFactory.createTest() dans les specs", "is_correct": False},
                        {"text": "Avec jest.mock() sur le fichier du service entier", "is_correct": False},
                    ],
                },
            ],
        },
    },
}


def add_nestjs_quizzes():
    """Ajoute la catégorie NestJS et les quiz avec toutes les questions"""

    try:
        category_name = NESTJS_QUIZ_DATA["category"]["name"]
        existing_category = (
            db.query(Category).filter(Category.name == category_name).first()
        )

        if existing_category:
            print(f"✓ Catégorie '{category_name}' existe déjà (ID: {existing_category.id})")
            category = existing_category
        else:
            category = Category(
                id=str(uuid.uuid4()),
                name=NESTJS_QUIZ_DATA["category"]["name"],
                description=NESTJS_QUIZ_DATA["category"]["description"],
                icon_url=NESTJS_QUIZ_DATA["category"]["icon_url"],
                is_active=NESTJS_QUIZ_DATA["category"]["is_active"],
            )
            db.add(category)
            db.commit()
            print(f"✓ Catégorie '{category_name}' créée avec succès (ID: {category.id})")

        for level_name, quiz_data in NESTJS_QUIZ_DATA["quizzes"].items():
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

        print("\n✅ Tous les quiz NestJS ont été ajoutés avec succès!")

    except Exception as e:
        db.rollback()
        print(f"❌ Erreur lors de l'ajout des quiz: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Ajout des quiz NestJS (débutant, intermédiaire, avancé)...\n")
    add_nestjs_quizzes()