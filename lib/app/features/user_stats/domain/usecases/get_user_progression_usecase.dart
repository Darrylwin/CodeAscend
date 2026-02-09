import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/user_progression_entity.dart';
import '../repositories/user_stats_repository.dart';

/// UseCase: Récupérer la progression globale de l'utilisateur
class GetUserProgressionUseCase {
  final UserStatsRepository _repository;

  GetUserProgressionUseCase(this._repository);

  /// Pas de paramètres nécessaires
  Future<Either<Failure, UserProgressionEntity>> call() {
    return _repository.getUserProgression();
  }
}
