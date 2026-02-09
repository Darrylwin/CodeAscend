import '../../../quiz/domain/entities/quiz_attempt_entity.dart';
import 'user_answer_model.dart';

/// Status possible d'une tentative locale
enum AttemptStatus {
  inProgress,
  pendingSubmission,
  submitting,
  submitted,
  failed,
}

extension AttemptStatusX on AttemptStatus {
  String get value {
    switch (this) {
      case AttemptStatus.inProgress:
        return 'in_progress';
      case AttemptStatus.pendingSubmission:
        return 'pending_submission';
      case AttemptStatus.submitting:
        return 'submitting';
      case AttemptStatus.submitted:
        return 'submitted';
      case AttemptStatus.failed:
        return 'failed';
    }
  }

  static AttemptStatus fromValue(String value) {
    switch (value) {
      case 'in_progress':
        return AttemptStatus.inProgress;
      case 'pending_submission':
        return AttemptStatus.pendingSubmission;
      case 'submitting':
        return AttemptStatus.submitting;
      case 'submitted':
        return AttemptStatus.submitted;
      case 'failed':
        return AttemptStatus.failed;
      default:
        return AttemptStatus.inProgress;
    }
  }
}

/// Model local pour stocker une tentative (SharedPreferences JSON)
class QuizAttemptModel {
  final String localId; // id locale (timestamp-based)
  String? remoteAttemptId; // id côté serveur (si connu)
  final String quizId;
  final String userId;
  List<UserAnswerModel> answers;
  AttemptStatus status;
  double? score;
  bool? passed;
  DateTime createdAt;
  DateTime updatedAt;
  DateTime? completedAt;

  QuizAttemptModel({
    required this.localId,
    this.remoteAttemptId,
    required this.quizId,
    required this.userId,
    this.answers = const [],
    this.status = AttemptStatus.inProgress,
    this.score,
    this.passed,
    DateTime? createdAt,
    DateTime? updatedAt,
    this.completedAt,
  })  : createdAt = createdAt ?? DateTime.now(),
        updatedAt = updatedAt ?? DateTime.now();

  factory QuizAttemptModel.fromJson(Map<String, dynamic> json) {
    return QuizAttemptModel(
      localId: json['local_id'] as String,
      remoteAttemptId: json['remote_attempt_id'] as String?,
      quizId: json['quiz_id'] as String,
      userId: json['user_id'] as String,
      answers: (json['answers'] as List<dynamic>?)
              ?.cast<Map<String, dynamic>>()
              .map((e) => UserAnswerModel.fromJson(e))
              .toList() ??
          [],
      status:
          AttemptStatusX.fromValue(json['status'] as String? ?? 'in_progress'),
      score: (json['score'] as num?)?.toDouble(),
      passed: json['passed'] as bool?,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
      completedAt: json['completed_at'] != null
          ? DateTime.parse(json['completed_at'] as String)
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'local_id': localId,
      'remote_attempt_id': remoteAttemptId,
      'quiz_id': quizId,
      'user_id': userId,
      'answers': answers.map((a) => a.toJson()).toList(),
      'status': status.value,
      'score': score,
      'passed': passed,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
      'completed_at': completedAt?.toIso8601String(),
    };
  }

  /// Convertir vers l'Entity de domaine (quand on veut exposer la tentative localement)
  QuizAttemptEntity toEntity() {
    final userAnswers = answers
        .map((a) => UserAnswer(
              questionId: a.questionId,
              selectedAnswerIds: a.selectedAnswerIds,
            ))
        .toList();

    return QuizAttemptEntity(
      id: localId,
      quizId: quizId,
      userId: userId,
      score: score ?? 0,
      passed: passed ?? false,
      completedAt: completedAt ?? createdAt,
      answers: userAnswers,
      correctAnswersCount: 0,
      totalQuestions: userAnswers.length,
    );
  }
}
