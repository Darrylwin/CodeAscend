import '../../domain/entities/user_progression_entity.dart';

// ============================================================================
// USER PROGRESSION MODEL
// ============================================================================

/// Model UserProgression
/// Parse exactement le format de l'API /users/me/stats
class UserProgressionModel extends UserProgressionEntity {
  const UserProgressionModel({
    required super.totalAttempts,
    required super.averageScore,
    required super.categoriesMastered,
    required super.recentAttempts,
  });

  /// Parse le format de l'API:
  /// {
  ///   "total_attempts": 13,
  ///   "average_score": 76.92,
  ///   "categories_mastered": 2,
  ///   "recent_attempts": [...]
  /// }
  factory UserProgressionModel.fromJson(Map<String, dynamic> json) {
    final recentAttemptsJson =
        (json['recent_attempts'] as List<dynamic>?) ?? [];

    final recentAttempts = recentAttemptsJson
        .cast<Map<String, dynamic>>()
        .map((a) => RecentAttemptModel.fromJson(a))
        .toList();

    return UserProgressionModel(
      totalAttempts: json['total_attempts'] as int? ?? 0,
      averageScore: (json['average_score'] as num?)?.toDouble() ?? 0.0,
      categoriesMastered: json['categories_mastered'] as int? ?? 0,
      recentAttempts: recentAttempts,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'total_attempts': totalAttempts,
      'average_score': averageScore,
      'categories_mastered': categoriesMastered,
      'recent_attempts': recentAttempts
          .map((a) => (a as RecentAttemptModel).toJson())
          .toList(),
    };
  }
}

// ============================================================================
// RECENT ATTEMPT MODEL
// ============================================================================

/// Model RecentAttempt
class RecentAttemptModel extends RecentAttemptEntity {
  const RecentAttemptModel({
    required super.id,
    required super.quizTitle,
    required super.score,
    required super.passed,
    required super.completedAt,
  });

  factory RecentAttemptModel.fromJson(Map<String, dynamic> json) {
    return RecentAttemptModel(
      id: json['id'] as String,
      quizTitle: json['quiz_title'] as String,
      score: (json['score'] as num).toDouble(),
      passed: json['passed'] as bool,
      completedAt: DateTime.parse(json['completed_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'quiz_title': quizTitle,
      'score': score,
      'passed': passed,
      'completed_at': completedAt.toIso8601String(),
    };
  }
}
