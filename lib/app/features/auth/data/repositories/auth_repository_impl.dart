import 'package:dartz/dartz.dart';
import 'package:dio/dio.dart';
import '../../../../core/error/failures.dart';
import '../../domain/entities/user_entity.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/auth_local_data_source.dart';
import '../datasources/auth_remote_data_source.dart';

/// Implémentation du AuthRepository
///
/// Responsabilités:
/// - Orchestrer les data sources (remote + local)
/// - Convertir les exceptions en Failures
/// - Gérer le cache et la synchronisation
/// 
class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource _remoteDataSource;
  final AuthLocalDataSource _localDataSource;

  AuthRepositoryImpl({
    required AuthRemoteDataSource remoteDataSource,
    required AuthLocalDataSource localDataSource,
  })  : _remoteDataSource = remoteDataSource,
        _localDataSource = localDataSource;

  @override
  Future<Either<Failure, (UserEntity, String)>> login({
    required String email,
    required String password,
  }) async {
    try {
      // 1. Appel API
      final result = await _remoteDataSource.login(
        email: email,
        password: password,
      );

      // 2. Sauvegarder le token localement
      await _localDataSource.saveToken(result.token);

      // 3. Sauvegarder l'user en cache
      await _localDataSource.cacheUser(result.user);

      // 4. Retourner le succès
      return Right((result.user, result.token));
    } on DioException catch (e) {
      // Convertir les erreurs Dio en Failures
      return Left(_handleDioException(e));
    } catch (e) {
      return Left(UnknownFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, (UserEntity, String)>> register({
    required String name,
    required String email,
    required String password,
  }) async {
    try {
      // Validation locale (économise un appel API)
      if (name.length < 2) {
        return const Left(
            ValidationFailure('Le nom doit contenir au moins 2 caractères'));
      }
      if (password.length < 8) {
        return const Left(ValidationFailure(
            'Le mot de passe doit contenir au moins 8 caractères'));
      }

      // 1. Appel API
      final result = await _remoteDataSource.register(
        name: name,
        email: email,
        password: password,
      );

      // 2. Sauvegarder le token
      await _localDataSource.saveToken(result.token);

      // 3. Sauvegarder l'user en cache
      await _localDataSource.cacheUser(result.user);

      return Right((result.user, result.token));
    } on DioException catch (e) {
      return Left(_handleDioException(e));
    } catch (e) {
      return Left(UnknownFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, void>> logout() async {
    try {
      // 1. Appel API (peut échouer, ce n'est pas grave)
      await _remoteDataSource.logout();

      // 2. Supprimer tout en local (IMPORTANT)
      await _localDataSource.clearAll();

      return const Right(null);
    } catch (e) {
      // Même si l'API échoue, on supprime le cache local
      await _localDataSource.clearAll();
      return const Right(null);
    }
  }

  @override
  Future<Either<Failure, UserEntity>> getCurrentUser() async {
    try {
      // 1. Essayer de récupérer depuis le cache
      final cachedUser = await _localDataSource.getCachedUser();

      if (cachedUser != null) {
        return Right(cachedUser);
      }

      // 2. Si pas de cache, appel API
      final token = await _localDataSource.getToken();

      if (token == null) {
        return const Left(UnauthorizedFailure('Aucun utilisateur connecté'));
      }

      final user = await _remoteDataSource.getCurrentUser();

      // 3. Mettre en cache
      await _localDataSource.cacheUser(user);

      return Right(user);
    } on DioException catch (e) {
      // Si 401, supprimer le token invalide
      if (e.response?.statusCode == 401) {
        await _localDataSource.clearAll();
      }
      return Left(_handleDioException(e));
    } catch (e) {
      return Left(UnknownFailure(e.toString()));
    }
  }

  @override
  Future<bool> isAuthenticated() async {
    try {
      final token = await _localDataSource.getToken();
      return token != null && token.isNotEmpty;
    } catch (e) {
      return false;
    }
  }

  @override
  Future<String?> getToken() async {
    try {
      return await _localDataSource.getToken();
    } catch (e) {
      return null;
    }
  }

  /// Convertit les DioException en Failures appropriés
  /// 
  /// 
  /// Codes HTTP selon la doc API:
  /// - 400: Validation Error
  /// - 401: Unauthorized (token invalide/expiré)
  /// - 403: Forbidden
  /// - 404: Not Found
  /// - 409: Conflict (email déjà existant)
  /// - 422: Validation Error (identifiants incorrects ou validation FastAPI)
  /// - 500+: Server Error
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
        final message = _extractErrorMessage(e.response?.data);

        switch (statusCode) {
          case 400:
            return ValidationFailure(message ?? 'Données invalides');
            
          case 401:
            return UnauthorizedFailure(message ?? 'Session expirée. Reconnectez-vous');
            
          case 403:
            return ForbiddenFailure(message ?? 'Accès refusé');
            
          case 404:
            return NotFoundFailure(message ?? 'Ressource introuvable');
            
          case 409:
            // Email déjà utilisé (Conflict)
            return EmailAlreadyExistsFailure(message ?? 'Cet email est déjà utilisé');
            
          case 422:
            // 422 peut être identifiants incorrects OU validation FastAPI
            // On détecte selon le message
            if (message != null) {
              final lowerMessage = message.toLowerCase();
              if (lowerMessage.contains('email') || 
                  lowerMessage.contains('password') ||
                  lowerMessage.contains('credentials') ||
                  lowerMessage.contains('incorrect')) {
                return InvalidCredentialsFailure(message);
              }
            }
            return ValidationFailure(message ?? 'Données invalides');
            
          case 500:
          case 502:
          case 503:
            return ServerFailure(message ?? 'Erreur serveur. Réessayez plus tard');
            
          default:
            return UnknownFailure('Erreur $statusCode: ${message ?? 'Inconnue'}');
        }

      default:
        return UnknownFailure(e.message ?? 'Erreur inconnue');
    }
  }

  /// Extraction intelligente du message d'erreur
  /// 
  /// 
  /// Formats supportés :
  /// - FastAPI 422 validation: { "detail": [{"loc": [...], "msg": "...", "type": "..."}] }
  /// - FastAPI simple: { "detail": "Message d'erreur" }
  /// - Custom format: { "message": "...", "error": "..." }
  /// - String directement
  String? _extractErrorMessage(dynamic data) {
    if (data == null) return null;
    
    // 1. Si c'est directement un string
    if (data is String) return data;
    
    // 2. Si c'est un Map (objet JSON)
    if (data is Map<String, dynamic>) {
      // 2a. Vérifier 'detail' (standard FastAPI)
      final detail = data['detail'];
      
      // 2b. Si 'detail' est une liste (erreurs de validation FastAPI 422)
      // Format: [{"loc": ["body", "email"], "msg": "field required", "type": "value_error.missing"}]
      if (detail is List && detail.isNotEmpty) {
        final errors = <String>[];
        for (final error in detail) {
          if (error is Map<String, dynamic>) {
            final msg = error['msg'];
            final loc = error['loc'];
            
            if (msg != null) {
              // Ajouter le champ concerné si disponible
              if (loc is List && loc.length > 1) {
                final field = loc[1];
                errors.add('$field: $msg');
              } else {
                errors.add(msg.toString());
              }
            }
          }
        }
        
        if (errors.isNotEmpty) {
          // Retourner la première erreur (ou toutes séparées par des virgules)
          return errors.first; // OU: errors.join(', ')
        }
      }
      
      // 2c. Si 'detail' est un string simple
      if (detail is String) return detail;
      
      // 2d. Fallback sur 'message' ou 'error' (formats custom)
      final message = data['message'] as String?;
      if (message != null) return message;
      
      final error = data['error'] as String?;
      if (error != null) return error;
    }
    
    // 3. Si aucun format reconnu
    return null;
  }
}