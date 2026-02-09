import 'package:dartz/dartz.dart';
import 'package:dio/dio.dart';

import '../../../../core/error/failures.dart';
import '../../domain/entities/category_entity.dart';
import '../../domain/repositories/category_repository.dart';
import '../datasources/category_local_data_source.dart';
import '../datasources/category_remote_data_source.dart';

/// Implémentation du CategoryRepository (orchestration remote + local)
class CategoryRepositoryImpl implements CategoryRepository {
  final CategoryRemoteDataSource _remote;
  final CategoryLocalDataSource _local;

  CategoryRepositoryImpl({
    required CategoryRemoteDataSource remoteDataSource,
    required CategoryLocalDataSource localDataSource,
  })  : _remote = remoteDataSource,
        _local = localDataSource;

  @override
  Future<Either<Failure, List<CategoryEntity>>> getCategories({
    bool? isActive,
  }) async {
    try {
      // 1. Essayer l'API en priorité
      final remoteList = await _remote.getCategories(
        isActive: isActive,
      );

      // 2. Mettre en cache localement (silencieux)
      try {
        await _local.cacheCategories(remoteList);
      } catch (_) {
        // Ignorer les erreurs de cache
      }

      // 3. Convertir les Models en Entities
      final entities = remoteList.map((model) => model.toEntity()).toList();
      return Right<Failure, List<CategoryEntity>>(entities);
      
    } on DioException catch (e) {
      // 4. En cas d'erreur réseau, tenter de retourner le cache
      final cached = await _local.getCachedCategories();
      if (cached != null && cached.isNotEmpty) {
        // Convertir le cache en Entities
        final entities = cached.map((model) => model.toEntity()).toList();
        return Right<Failure, List<CategoryEntity>>(entities);
      }

      // 5. Aucun cache disponible : renvoyer une Failure spécifique
      return Left<Failure, List<CategoryEntity>>(
        _handleDioException(e),
      );
    } catch (e) {
      return Left<Failure, List<CategoryEntity>>(
        UnknownFailure(e.toString()),
      );
    }
  }

  @override
  Future<Either<Failure, CategoryEntity>> getCategoryById(String id) async {
    try {
      // 1. Essayer le cache local d'abord (fast UX)
      final cached = await _local.getCachedCategoryById(id);
      if (cached != null) {
        // Convertir en Entity
        return Right<Failure, CategoryEntity>(cached.toEntity());
      }

      // 2. Sinon appel remote
      final remote = await _remote.getCategoryById(id);

      // 3. Mettre à jour le cache (silencieux)
      try {
        final existing = (await _local.getCachedCategories()) ?? [];
        final merged = [
          ...existing.where((c) => c.id != remote.id),
          remote,
        ];
        await _local.cacheCategories(merged);
      } catch (_) {
        // Ignorer les erreurs de cache
      }

      // 4. Convertir en Entity
      return Right<Failure, CategoryEntity>(remote.toEntity());
      
    } on DioException catch (e) {
      // Si 404, renvoyer un CategoryNotFoundFailure
      if (e.response?.statusCode == 404) {
        return const Left<Failure, CategoryEntity>(
          CategoryNotFoundFailure(),
        );
      }

      // Autre erreur réseau
      return Left<Failure, CategoryEntity>(_handleDioException(e));
    } catch (e) {
      return Left<Failure, CategoryEntity>(
        UnknownFailure(e.toString()),
      );
    }
  }

  /// Mappe DioException -> Failure
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
        final message = _extractMessage(e);

        switch (statusCode) {
          case 400:
            return ValidationFailure(message ?? 'Données invalides');
          case 401:
            return UnauthorizedFailure(message ?? 'Session expirée');
          case 403:
            return ForbiddenFailure(message ?? 'Accès refusé');
          case 404:
            return CategoryNotFoundFailure(message ?? 'Catégorie introuvable');
          case 500:
          case 502:
          case 503:
            return ServerFailure(message ?? 'Erreur serveur');
          default:
            return UnknownFailure(
              'Erreur $statusCode: ${message ?? 'Inconnue'}',
            );
        }

      default:
        return UnknownFailure(e.message ?? 'Erreur inconnue');
    }
  }

  /// Extraction intelligente du message d'erreur FastAPI
  /// 
  /// Formats supportés:
  /// - String direct
  /// - { "detail": "message" }
  /// - { "detail": [{"msg": "...", "loc": [...]}] } (validation 422)
  /// - { "message": "..." }
  /// - { "error": "..." }
  String? _extractMessage(DioException e) {
    try {
      final data = e.response?.data;
      if (data == null) return null;

      // 1. String direct
      if (data is String) return data;

      // 2. Map (objet JSON)
      if (data is Map<String, dynamic>) {
        // 2a. Vérifier 'detail'
        final detail = data['detail'];
        
        // 2b. Si 'detail' est une liste (erreurs de validation FastAPI)
        if (detail is List && detail.isNotEmpty) {
          final errors = <String>[];
          for (final error in detail) {
            if (error is Map<String, dynamic>) {
              final msg = error['msg'];
              if (msg != null) {
                errors.add(msg.toString());
              }
            }
          }
          return errors.isNotEmpty ? errors.first : null;
        }
        
        // 2c. Si 'detail' est un string
        if (detail is String) return detail;
        
        // 2d. Fallback sur 'message' ou 'error'
        return data['message'] as String? ?? data['error'] as String?;
      }

      return null;
    } catch (_) {
      return null;
    }
  }
}