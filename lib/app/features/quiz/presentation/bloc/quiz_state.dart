import 'package:equatable/equatable.dart';
import '../../../quiz/domain/entities/quiz_entity.dart';
import '../../../quiz/domain/entities/quiz_attempt_entity.dart';
import '../../../quiz/data/models/quiz_attempt_model.dart'
    show QuizAttemptModel;

/// États du QuizBloc
abstract class QuizState extends Equatable {
  const QuizState();

  @override
  List<Object?> get props => [];
}

/// Initial
class QuizInitial extends QuizState {
  const QuizInitial();
}

/// Chargement en cours (quiz + tentative)
class QuizLoading extends QuizState {
  const QuizLoading();
}

/// Quiz prêt / en cours
class QuizInProgress extends QuizState {
  final QuizEntity quiz;
  final QuizAttemptModel? localAttempt;
  final int currentQuestionIndex;

  const QuizInProgress({
    required this.quiz,
    this.localAttempt,
    this.currentQuestionIndex = 0,
  });

  @override
  List<Object?> get props => [
        quiz,
        localAttempt?.localId,
        localAttempt?.updatedAt.millisecondsSinceEpoch,
        localAttempt?.answers.length,
        currentQuestionIndex
      ];
}

/// Soumission en cours
class QuizSubmitting extends QuizState {
  const QuizSubmitting();
}

/// Tentative soumise (résultat reçu ou tentative mise en file)
class QuizSubmitted extends QuizState {
  final QuizAttemptEntity result;
  final bool queued; // true si envoyé en file d'attente (offline)

  const QuizSubmitted({
    required this.result,
    this.queued = false,
  });

  @override
  List<Object?> get props => [result, queued];
}

/// Erreur
class QuizError extends QuizState {
  final String message;

  const QuizError(this.message);

  @override
  List<Object?> get props => [message];
}
