import '../../domain/entities/attempt_summary_entity.dart';

/// Model AttemptSummary (hérite de AttemptSummaryEntity)
///
/// Responsabilité: Conversion JSON ↔ Entity
class AttemptSummaryModel extends AttemptSummaryEntity {
  const AttemptSummaryModel({
    required super.id,
    required super.quizId,
    required super.quizTitle,
    required super.categoryName,
    required super.level,
    required super.score,
    required super.passed,
    required super.completedAt,
    required super.isInProgress,
  });

  /// Factory: Créer depuis JSON (API response)
  ///
  /// Format attendu GET /users/me/attempts:
  /// {
  ///   "id": "attempt-001",
  ///   "quiz_id": "quiz-123",
  ///   "quiz_title": "Flutter Basics",
  ///   "category_name": "Flutter",
  ///   "level": "debutant",
  ///   "score": 80.0,
  ///   "passed": true,
  ///   "completed_at": "2026-01-30T14:30:00Z"
  /// }
  factory AttemptSummaryModel.fromJson(Map<String, dynamic> json) {
    // détecter si la tentative est en cours
    // (score null ET completed_at null = tentative en cours)
    final isInProgress = json['score'] == null && json['completed_at'] == null;

    return AttemptSummaryModel(
      id: json['id'] as String,
      quizId: json['quiz_id']?.toString() ?? '',
      quizTitle: json['quiz_title'] as String? ?? '',
      categoryName: json['category_name']?.toString() ?? '',
      level: json['level']?.toString() ?? 'debutant',
      score: _parseScore(json['score']),
      passed: json['passed'] as bool? ?? false,
      completedAt: _parseDateTime(json['completed_at']),
      isInProgress: isInProgress,
    );
  }

  /// Parse le score de manière sécurisée
  static double _parseScore(dynamic value) {
    if (value == null) return 0.0;
    if (value is num) return value.toDouble();
    if (value is String) {
      return double.tryParse(value) ?? 0.0;
    }
    return 0.0;
  }

  /// Parse la date de manière sécurisée
  static DateTime _parseDateTime(dynamic value) {
    if (value == null) return DateTime.now();
    if (value is String) {
      try {
        return DateTime.parse(value);
      } catch (e) {
        return DateTime.now();
      }
    }
    return DateTime.now();
  }

  /// Convertir vers JSON (pour cache local)
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'quiz_id': quizId,
      'quiz_title': quizTitle,
      'category_name': categoryName,
      'level': level,
      'score': score,
      'passed': passed,
      'completed_at': completedAt.toIso8601String(),
      'is_in_progress': isInProgress,
    };
  }

  /// Factory: Créer depuis Entity
  factory AttemptSummaryModel.fromEntity(AttemptSummaryEntity entity) {
    return AttemptSummaryModel(
      id: entity.id,
      quizId: entity.quizId,
      quizTitle: entity.quizTitle,
      categoryName: entity.categoryName,
      level: entity.level,
      score: entity.score,
      passed: entity.passed,
      completedAt: entity.completedAt,
      isInProgress: entity.isInProgress,
    );
  }

  /// Convertir vers Entity
  AttemptSummaryEntity toEntity() {
    return AttemptSummaryEntity(
      id: id,
      quizId: quizId,
      quizTitle: quizTitle,
      categoryName: categoryName,
      level: level,
      score: score,
      passed: passed,
      completedAt: completedAt,
      isInProgress: isInProgress,
    );
  }
}
