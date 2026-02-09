import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/quiz_entity.dart';
import '../entities/question_entity.dart';
import '../entities/quiz_attempt_entity.dart';
import '../repositories/quiz_repository.dart';

/// UseCase: Récupérer un quiz par id
class GetQuizByIdUseCase {
  final QuizRepository _repository;

  GetQuizByIdUseCase(this._repository);

  Future<Either<Failure, QuizEntity>> call(String id) {
    return _repository.getQuizById(id);
  }
}

/// UseCase: Récupérer la liste de quizzes disponibles par catégorie
class GetAvailableQuizzesUseCase {
  final QuizRepository _repository;

  GetAvailableQuizzesUseCase(this._repository);

  Future<Either<Failure, List<QuizEntity>>> call(String categoryId) {
    return _repository.getAvailableQuizzes(categoryId: categoryId);
  }
}

/// UseCase: Démarrer un quiz (créer une tentative)
class StartQuizUseCase {
  final QuizRepository _repository;

  StartQuizUseCase(this._repository);

  Future<Either<Failure, String>> call(String quizId) {
    return _repository.startQuiz(quizId: quizId);
  }
}

/// UseCase: Soumettre une tentative et obtenir le résultat
class SubmitQuizUseCase {
  final QuizRepository _repository;

  SubmitQuizUseCase(this._repository);

  Future<Either<Failure, QuizAttemptEntity>> call({
    required String attemptId,
    required String quizId,
    required List<UserAnswer> answers,
  }) {
    return _repository.submitQuiz(
      attemptId: attemptId,
      quizId: quizId,
      answers: answers,
    );
  }
}

/// UseCase: Récupérer une tentative par id
///
/// Retourne un record contenant:
/// - attempt: QuizAttemptEntity (score, réponses utilisateur)
/// - quiz: QuizEntity (métadonnées du quiz)
/// - questions: List<QuestionEntity> (questions avec bonnes réponses)
class GetAttemptByIdUseCase {
  final QuizRepository _repository;

  GetAttemptByIdUseCase(this._repository);

  Future<
      Either<
          Failure,
          ({
            QuizAttemptEntity attempt,
            QuizEntity quiz,
            List<QuestionEntity> questions
          })>> call(String attemptId) {
    return _repository.getAttemptById(attemptId);
  }
}

/// UseCase: Récupérer les tentatives de l'utilisateur
class GetUserAttemptsUseCase {
  final QuizRepository _repository;

  GetUserAttemptsUseCase(this._repository);

  Future<Either<Failure, List<QuizAttemptEntity>>> call() {
    return _repository.getUserAttempts();
  }
}

/// UseCase pour envoyer les tentatives pending (flush)
///
/// Utilise maintenant la méthode officielle du repository
/// au lieu d'un cast dynamic dangereux.
class FlushPendingSubmissionsUseCase {
  final QuizRepository _repository;

  FlushPendingSubmissionsUseCase(this._repository);

  /// Tente d'envoyer toutes les soumissions en attente
  ///
  /// Returns:
  /// - Either<Failure, int> : nombre de soumissions envoyées avec succès
  Future<Either<Failure, int>> call() {
    return _repository.flushPendingSubmissions();
  }
}
