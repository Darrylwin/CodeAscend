import 'package:equatable/equatable.dart';
import '../../domain/entities/quiz_attempt_entity.dart';

/// Events pour le QuizBloc
abstract class QuizEvent extends Equatable {
  const QuizEvent();

  @override
  List<Object?> get props => [];
}

/// Charger le quiz (questions + préparer la tentative)
class QuizLoadRequested extends QuizEvent {
  final String quizId;

  const QuizLoadRequested(this.quizId);

  @override
  List<Object?> get props => [quizId];
}

/// Restaurer une tentative en cours si présente (par quizId)
class QuizRestoreRequested extends QuizEvent {
  final String quizId;

  const QuizRestoreRequested(this.quizId);

  @override
  List<Object?> get props => [quizId];
}

/// L'utilisateur sélectionne/modifie des réponses pour une question
class QuizAnswerUpdated extends QuizEvent {
  final String questionId;
  final List<String> selectedAnswerIds;

  const QuizAnswerUpdated({
    required this.questionId,
    required this.selectedAnswerIds,
  });

  @override
  List<Object?> get props => [questionId, selectedAnswerIds];
}

/// Soumettre la tentative courante
/// Maintenant inclut explicitement la liste des réponses (UserAnswer domain)
class QuizSubmitRequested extends QuizEvent {
  final String attemptId; // localId ou remoteAttemptId
  final String quizId; // nécessaire pour la navigation et le cache
  final List<UserAnswer> answers;

  const QuizSubmitRequested({
    required this.attemptId,
    required this.quizId,
    required this.answers,
  });

  @override
  List<Object?> get props => [attemptId, quizId, answers];
}

/// Forcer l'envoi des submissions pendantes
class QuizFlushPendingRequested extends QuizEvent {
  const QuizFlushPendingRequested();
}
