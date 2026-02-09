import 'package:equatable/equatable.dart';

/// Entity représentant la progression globale de l'utilisateur
/// Simplifié pour correspondre exactement à la réponse API
class UserProgressionEntity extends Equatable {
  final int totalAttempts;
  final double averageScore;
  final int categoriesMastered;
  final List<RecentAttemptEntity> recentAttempts;

  const UserProgressionEntity({
    required this.totalAttempts,
    required this.averageScore,
    required this.categoriesMastered,
    required this.recentAttempts,
  });

  /// Score moyen arrondi
  int get averageScoreInt => averageScore.round();

  /// Vérifie si l'utilisateur a au moins une tentative
  bool get hasAttempts => totalAttempts > 0;

  /// Nombre de tentatives récentes réussies
  int get recentPassedCount => recentAttempts.where((a) => a.passed).length;

  /// Nombre de tentatives récentes échouées
  int get recentFailedCount => recentAttempts.where((a) => !a.passed).length;

  /// Série actuelle (calculée depuis les tentatives récentes)
  int get currentStreak {
    int streak = 0;
    for (final attempt in recentAttempts) {
      if (attempt.passed) {
        streak++;
      } else {
        break;
      }
    }
    return streak;
  }

  /// Vérifie si l'utilisateur a une série active
  bool get hasActiveStreak => currentStreak > 0;

  @override
  List<Object?> get props => [
        totalAttempts,
        averageScore,
        categoriesMastered,
        recentAttempts,
      ];

  @override
  String toString() =>
      'UserProgressionEntity(totalAttempts: $totalAttempts, averageScore: $averageScoreInt%)';
}

/// Entity représentant une tentative récente
class RecentAttemptEntity extends Equatable {
  final String id;
  final String quizTitle;
  final double score;
  final bool passed;
  final DateTime completedAt;

  const RecentAttemptEntity({
    required this.id,
    required this.quizTitle,
    required this.score,
    required this.passed,
    required this.completedAt,
  });

  /// Score arrondi
  int get scoreInt => score.round();

  /// Retourne une description formatée de la date
  String get formattedDate {
    final now = DateTime.now();
    final difference = now.difference(completedAt);

    if (difference.inMinutes < 1) {
      return 'À l\'instant';
    } else if (difference.inMinutes < 60) {
      return 'Il y a ${difference.inMinutes} min';
    } else if (difference.inHours < 24) {
      return 'Il y a ${difference.inHours}h';
    } else if (difference.inDays == 1) {
      return 'Hier';
    } else if (difference.inDays < 7) {
      return 'Il y a ${difference.inDays} jours';
    } else {
      final months = [
        'Jan',
        'Fév',
        'Mar',
        'Avr',
        'Mai',
        'Juin',
        'Juil',
        'Aoû',
        'Sep',
        'Oct',
        'Nov',
        'Déc'
      ];
      return '${completedAt.day} ${months[completedAt.month - 1]} ${completedAt.year}';
    }
  }

  @override
  List<Object?> get props => [id, quizTitle, score, passed, completedAt];

  @override
  String toString() =>
      'RecentAttemptEntity(id: $id, quizTitle: $quizTitle, score: $scoreInt%, passed: $passed)';
}
