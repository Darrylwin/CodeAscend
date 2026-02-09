import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/user_progression_entity.dart';

/// Repository UserStats (CONTRAT/INTERFACE)
///
/// Responsabilité: Gérer les statistiques et la progression de l'utilisateur
abstract class UserStatsRepository {
  /// Récupérer la progression globale de l'utilisateur
  ///
  /// Inclut:
  /// - Statistiques globales
  /// - Stats par catégorie
  /// - Progression par niveau
  ///
  /// Returns:
  /// - Left(Failure) si erreur
  /// - Right(UserProgressionEntity) si succès
  Future<Either<Failure, UserProgressionEntity>> getUserProgression();
}
