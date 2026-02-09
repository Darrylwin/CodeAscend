import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/attempt_summary_entity.dart';
import '../repositories/attempts_repository.dart';

// ============================================================================
// USE CASE: GET USER ATTEMPTS
// ============================================================================

/// UseCase: Récupérer toutes les tentatives de l'utilisateur
class GetUserAttemptsUseCase {
  final AttemptsRepository _repository;

  GetUserAttemptsUseCase(this._repository);

  /// Pas de paramètres nécessaires
  Future<Either<Failure, List<AttemptSummaryEntity>>> call() {
    return _repository.getUserAttempts();
  }
}

// ============================================================================
// USE CASE: GET ATTEMPT STATISTICS
// ============================================================================

/// UseCase: Récupérer les statistiques globales
class GetAttemptStatisticsUseCase {
  final AttemptsRepository _repository;

  GetAttemptStatisticsUseCase(this._repository);

  Future<Either<Failure, AttemptStatistics>> call() {
    return _repository.getStatistics();
  }
}
