import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/attempt_summary_entity.dart';

/// Repository Attempts (CONTRAT/INTERFACE)
///
/// Responsabilité: Gérer les tentatives de quiz de l'utilisateur
abstract class AttemptsRepository {
  /// Récupérer toutes les tentatives de l'utilisateur
  ///
  /// Returns:
  /// - Left(Failure) si erreur
  /// - Right(List<AttemptSummaryEntity>) si succès
  Future<Either<Failure, List<AttemptSummaryEntity>>> getUserAttempts();

  /// Récupérer les statistiques globales de l'utilisateur
  ///
  /// Calcule:
  /// - Total de tentatives
  /// - Taux de réussite
  /// - Score moyen
  /// - Meilleure série
  ///
  /// Returns:
  /// - Left(Failure) si erreur
  /// - Right(AttemptStatistics) si succès
  Future<Either<Failure, AttemptStatistics>> getStatistics();
}

/// Statistiques des tentatives
class AttemptStatistics {
  final int totalAttempts;
  final int passedAttempts;
  final int failedAttempts;
  final double averageScore;
  final int bestStreak; // Meilleure série de réussites consécutives
  final int currentStreak; // Série actuelle

  const AttemptStatistics({
    required this.totalAttempts,
    required this.passedAttempts,
    required this.failedAttempts,
    required this.averageScore,
    required this.bestStreak,
    required this.currentStreak,
  });

  /// Taux de réussite (0-100)
  double get successRate {
    if (totalAttempts == 0) return 0.0;
    return (passedAttempts / totalAttempts) * 100;
  }

  /// Score moyen arrondi
  int get averageScoreInt => averageScore.round();

  /// Vérifie si l'utilisateur a au moins une tentative
  bool get hasAttempts => totalAttempts > 0;
}
