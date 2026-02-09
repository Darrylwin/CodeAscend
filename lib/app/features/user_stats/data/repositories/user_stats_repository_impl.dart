import 'package:dartz/dartz.dart';
import 'package:dio/dio.dart';
import '../../../../core/error/failures.dart';
import '../../domain/entities/user_progression_entity.dart';
import '../../domain/repositories/user_stats_repository.dart';
import '../datasources/user_stats_remote_datasource.dart';
import '../datasources/user_stats_local_datasource.dart';

/// Implémentation du UserStatsRepository
/// 
/// Stratégie:
/// - Cache-first pour affichage rapide
/// - Fetch en arrière-plan
/// - Mise en cache automatique
class UserStatsRepositoryImpl implements UserStatsRepository {
  final UserStatsRemoteDataSource _remoteDataSource;
  final UserStatsLocalDataSource _localDataSource;

  UserStatsRepositoryImpl({
    required UserStatsRemoteDataSource remoteDataSource,
    required UserStatsLocalDataSource localDataSource,
  })  : _remoteDataSource = remoteDataSource,
        _localDataSource = localDataSource;

  @override
  Future<Either<Failure, UserProgressionEntity>> getUserProgression() async {
    try {
      // 1. Essayer le cache pour affichage rapide
      final cachedProgression = await _localDataSource.getCachedProgression();

      // 2. Fetch depuis l'API
      try {
        final remoteProgression = await _remoteDataSource.getUserProgression();
        
        // 3. Mettre en cache
        await _localDataSource.cacheProgression(remoteProgression);
        
        // 4. Retourner les données fraîches
        return Right(remoteProgression);
      } on DioException catch (e) {
        // Si erreur réseau mais on a le cache, retourner le cache
        if (cachedProgression != null) {
          return Right(cachedProgression);
        }
        
        return Left(_handleDioException(e));
      }
    } catch (e) {
      return Left(UnknownFailure(e.toString()));
    }
  }

  /// Convertit les DioException en Failures
  Failure _handleDioException(DioException e) {
    switch (e.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return const TimeoutFailure();

      case DioExceptionType.connectionError:
        return const ConnectionFailure();

      case DioExceptionType.badResponse:
        final statusCode = e.response?.statusCode;

        switch (statusCode) {
          case 401:
            return const UnauthorizedFailure('Session expirée');
          case 403:
            return const ForbiddenFailure('Accès refusé');
          case 404:
            return const NotFoundFailure('Progression introuvable');
          case 500:
          case 502:
          case 503:
            return const ServerFailure('Erreur serveur');
          default:
            return UnknownFailure('Erreur $statusCode');
        }

      default:
        return UnknownFailure(e.message ?? 'Erreur inconnue');
    }
  }
}