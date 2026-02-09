import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/quiz_entity.dart';
import '../entities/question_entity.dart';
import '../entities/quiz_attempt_entity.dart';

/// Contrat du repository Quiz
abstract class QuizRepository {
  /// Récupère un quiz complet (avec questions) par son id
  Future<Either<Failure, QuizEntity>> getQuizById(String id);

  /// Récupère la liste des quizzes disponibles pour une catégorie
  /// L'API retourne déjà les quizzes filtrés selon la progression
  Future<Either<Failure, List<QuizEntity>>> getAvailableQuizzes({
    required String categoryId,
  });

  /// Démarrer une nouvelle tentative pour un quiz
  /// Retourne l'`attemptId` créé côté serveur (ou un Failure)
  Future<Either<Failure, String>> startQuiz({required String quizId});

  /// Soumettre une tentative (answers) et recevoir le résultat (score, passed, détails)
  Future<Either<Failure, QuizAttemptEntity>> submitQuiz({
    required String attemptId,
    required String quizId,
    required List<UserAnswer> answers,
  });

  /// Récupérer une tentative par id
  ///
  /// Retourne un record contenant:
  /// - attempt: QuizAttemptEntity (la tentative avec score, réponses utilisateur)
  /// - quiz: QuizEntity (les métadonnées du quiz)
  /// - questions: List<QuestionEntity> (les questions avec les bonnes réponses)
  Future<
      Either<
          Failure,
          ({
            QuizAttemptEntity attempt,
            QuizEntity quiz,
            List<QuestionEntity> questions
          })>> getAttemptById(String attemptId);

  /// Récupérer les tentatives de l'utilisateur
  Future<Either<Failure, List<QuizAttemptEntity>>> getUserAttempts();

  /// Envoyer les tentatives en attente (flush queue)
  ///
  /// Cette méthode tente d'envoyer toutes les soumissions pending
  /// qui ont été mises en queue lors de la perte de connexion.
  ///
  /// Appelée automatiquement lors de la reconnexion réseau.
  Future<Either<Failure, int>> flushPendingSubmissions();
}
