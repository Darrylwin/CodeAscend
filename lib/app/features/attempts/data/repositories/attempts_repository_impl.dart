import 'package:dartz/dartz.dart';
import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import '../../../../core/error/failures.dart';
import '../../domain/entities/attempt_summary_entity.dart';
import '../../domain/repositories/attempts_repository.dart';
import '../datasources/attempts_remote_datasource.dart';
import '../datasources/attempts_local_datasource.dart';

/// Implémentation du AttemptsRepository
///
/// Stratégie:
/// - Cache-first pour getUserAttempts (affichage rapide)
/// - Fetch en arrière-plan pour refresh
/// - Affichage des tentatives
/// - Calcul local des statistiques
class AttemptsRepositoryImpl implements AttemptsRepository {
  final AttemptsRemoteDataSource _remoteDataSource;
  final AttemptsLocalDataSource _localDataSource;

  AttemptsRepositoryImpl({
    required AttemptsRemoteDataSource remoteDataSource,
    required AttemptsLocalDataSource localDataSource,
  })  : _remoteDataSource = remoteDataSource,
        _localDataSource = localDataSource;

  @override
  Future<Either<Failure, List<AttemptSummaryEntity>>> getUserAttempts() async {
    try {
      // 1. Essayer de récupérer depuis le cache pour affichage immédiat
      final cachedAttempts = await _localDataSource.getCachedAttempts();

      // 2. Fetch depuis l'API
      try {
        final remoteAttempts = await _remoteDataSource.getUserAttempts();

        debugPrint('✅ ${remoteAttempts.length} tentative(s) récupérée(s)');

        // Compter les tentatives en cours et terminées
        final inProgress = remoteAttempts.where((a) => a.isInProgress).length;
        final completed = remoteAttempts.length - inProgress;
        debugPrint('📊 $completed terminée(s), $inProgress en cours');

        // 3. Mettre en cache TOUTES les tentatives
        try {
          await _localDataSource.cacheAttempts(remoteAttempts);
        } catch (cacheError) {
          debugPrint('⚠️ Erreur lors de la mise en cache: $cacheError');
        }

        // 4. Retourner TOUTES les tentatives (en cours + terminées)
        return Right(remoteAttempts.map((m) => m.toEntity()).toList());
      } on DioException catch (e) {
        debugPrint('❌ Erreur réseau getUserAttempts: ${e.message}');

        // Si erreur réseau mais on a le cache, retourner le cache
        if (cachedAttempts != null && cachedAttempts.isNotEmpty) {
          debugPrint(
              '✅ Utilisation du cache (${cachedAttempts.length} tentatives)');
          return Right(cachedAttempts.map((m) => m.toEntity()).toList());
        }

        // Sinon, retourner l'erreur
        return Left(_handleDioException(e));
      } catch (e, stackTrace) {
        debugPrint('❌ Erreur inattendue getUserAttempts: $e');
        debugPrint('Stack trace: $stackTrace');

        // En cas d'erreur de parsing, essayer de retourner le cache
        if (cachedAttempts != null && cachedAttempts.isNotEmpty) {
          debugPrint('✅ Utilisation du cache après erreur de parsing');
          return Right(cachedAttempts.map((m) => m.toEntity()).toList());
        }

        return Left(UnknownFailure('Erreur lors du chargement: $e'));
      }
    } catch (e, stackTrace) {
      debugPrint('❌ Erreur critique getUserAttempts: $e');
      debugPrint('Stack trace: $stackTrace');
      return Left(UnknownFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, AttemptStatistics>> getStatistics() async {
    try {
      // 1. Récupérer les tentatives (depuis cache ou API)
      final attemptsResult = await getUserAttempts();

      return attemptsResult.fold(
        (failure) => Left(failure),
        (attempts) {
          // Filtrer uniquement les tentatives TERMINÉES pour les stats
          // (on ne compte pas les "en cours" dans les statistiques)
          final completedAttempts =
              attempts.where((a) => !a.isInProgress).toList();

          // 2. Calculer les statistiques localement
          final stats = _calculateStatistics(completedAttempts);
          return Right(stats);
        },
      );
    } catch (e, stackTrace) {
      debugPrint('❌ Erreur getStatistics: $e');
      debugPrint('Stack trace: $stackTrace');
      return Left(UnknownFailure(e.toString()));
    }
  }

  /// Calcule les statistiques à partir de la liste des tentatives
  AttemptStatistics _calculateStatistics(List<AttemptSummaryEntity> attempts) {
    if (attempts.isEmpty) {
      return const AttemptStatistics(
        totalAttempts: 0,
        passedAttempts: 0,
        failedAttempts: 0,
        averageScore: 0.0,
        bestStreak: 0,
        currentStreak: 0,
      );
    }

    // Trier par date (plus récent en premier)
    final sortedAttempts = List<AttemptSummaryEntity>.from(attempts)
      ..sort((a, b) => b.completedAt.compareTo(a.completedAt));

    // Total
    final total = attempts.length;

    // Réussies et échouées
    final passed = attempts.where((a) => a.passed).length;
    final failed = total - passed;

    // Score moyen
    final totalScore = attempts.fold<double>(0.0, (sum, a) => sum + a.score);
    final average = totalScore / total;

    // Calculer les séries (streak)
    int currentStreak = 0;
    int bestStreak = 0;
    int tempStreak = 0;

    for (final attempt in sortedAttempts) {
      if (attempt.passed) {
        tempStreak++;
        if (tempStreak > bestStreak) {
          bestStreak = tempStreak;
        }
      } else {
        tempStreak = 0;
      }
    }

    // Current streak = série depuis la plus récente tentative
    for (final attempt in sortedAttempts) {
      if (attempt.passed) {
        currentStreak++;
      } else {
        break; // Arrêter dès qu'on trouve un échec
      }
    }

    return AttemptStatistics(
      totalAttempts: total,
      passedAttempts: passed,
      failedAttempts: failed,
      averageScore: average,
      bestStreak: bestStreak,
      currentStreak: currentStreak,
    );
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
            return const NotFoundFailure('Tentatives introuvables');
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
