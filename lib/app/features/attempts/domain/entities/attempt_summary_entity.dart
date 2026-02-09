import 'package:equatable/equatable.dart';

/// Entity représentant un résumé de tentative de quiz
///
/// Utilisé dans la liste d'historique (version allégée sans les détails)
class AttemptSummaryEntity extends Equatable {
  final String id;
  final String quizId;
  final String quizTitle;
  final String categoryName;
  final String level; // 'debutant' | 'intermediaire' | 'avance'
  final double score; // 0-100
  final bool passed;
  final DateTime completedAt;
  final bool isInProgress;

  const AttemptSummaryEntity({
    required this.id,
    required this.quizId,
    required this.quizTitle,
    required this.categoryName,
    required this.level,
    required this.score,
    required this.passed,
    required this.completedAt,
    this.isInProgress = false,
  });

  /// Score arrondi pour l'affichage
  int get scoreInt => score.round();

  /// Vérifie si la tentative date de moins de 24h
  bool get isRecent {
    final now = DateTime.now();
    final difference = now.difference(completedAt);
    return difference.inHours < 24;
  }

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
      // Format: 30 Jan 2026
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
  List<Object?> get props => [
        id,
        quizId,
        quizTitle,
        categoryName,
        level,
        score,
        passed,
        completedAt,
        isInProgress,
      ];

  @override
  String toString() =>
      'AttemptSummaryEntity(id: $id, quizTitle: $quizTitle, score: $score, passed: $passed, isInProgress: $isInProgress)';
}
