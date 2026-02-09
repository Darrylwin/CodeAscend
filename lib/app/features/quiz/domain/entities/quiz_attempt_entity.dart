import 'package:equatable/equatable.dart';

/// Représente la réponse d'utilisateur pour une question (envoi au serveur)
class UserAnswer {
  final String questionId;
  final List<String> selectedAnswerIds;

  const UserAnswer({
    required this.questionId,
    required this.selectedAnswerIds,
  });

  @override
  String toString() =>
      'UserAnswer(questionId: $questionId, selected: $selectedAnswerIds)';
}

/// Entity représentant une tentative de quiz (résultat)
class QuizAttemptEntity extends Equatable {
  final String id;
  final String quizId;
  final String userId;
  final double score; // 0-100
  final bool passed;
  final DateTime completedAt;
  final List<UserAnswer> answers; // ce que l'utilisateur a soumis
  final int correctAnswersCount;
  final int totalQuestions;

  const QuizAttemptEntity({
    required this.id,
    required this.quizId,
    required this.userId,
    required this.score,
    required this.passed,
    required this.completedAt,
    required this.answers,
    required this.correctAnswersCount,
    required this.totalQuestions,
  });

  @override
  List<Object?> get props => [
        id,
        quizId,
        userId,
        score,
        passed,
        completedAt,
        answers,
        correctAnswersCount,
        totalQuestions
      ];

  @override
  String toString() =>
      'QuizAttemptEntity(id: $id, quizId: $quizId, score: $score, passed: $passed)';
}
