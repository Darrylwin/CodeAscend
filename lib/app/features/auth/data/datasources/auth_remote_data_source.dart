import 'package:dio/dio.dart';
import '../models/user_model.dart';

/// Remote DataSource pour l'authentification
///
/// Responsabilité: Faire les appels API
/// Ne gère PAS les erreurs métier (c'est le rôle du repository)
/// Lance des exceptions si problème technique
abstract class AuthRemoteDataSource {
  /// POST /auth/login puis GET /auth/me
  ///
  /// Throws:
  /// - DioException si problème réseau
  /// - Exception si réponse invalide
  Future<({UserModel user, String token})> login({
    required String email,
    required String password,
  });

  /// POST /auth/register puis login automatique
  ///
  /// Throws:
  /// - DioException si problème réseau
  /// - Exception si email déjà utilisé
  Future<({UserModel user, String token})> register({
    required String name,
    required String email,
    required String password,
  });

  /// POST /auth/logout
  ///
  /// Throws:
  /// - DioException si problème réseau
  Future<void> logout();

  /// GET /auth/me
  ///
  /// Récupère l'utilisateur connecté depuis l'API
  ///
  /// Throws:
  /// - DioException si problème réseau
  /// - Exception si token invalide (401)
  Future<UserModel> getCurrentUser();
}

/// Implémentation du remote data source
class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final Dio _dio;

  AuthRemoteDataSourceImpl(this._dio);

  @override
  Future<({UserModel user, String token})> login({
    required String email,
    required String password,
  }) async {
    try {
      // 1. Login
      final loginResponse = await _dio.post(
        '/auth/login',
        data: {'email': email, 'password': password},
      );

      final token = loginResponse.data['access_token'] as String;

      // 2. Appeler /auth/me AVEC le token dans les headers
      final meResponse = await _dio.get(
        '/auth/me',
        options: Options(
          headers: {'Authorization': 'Bearer $token'},
        ),
      );

      final user = UserModel.fromJson(meResponse.data);

      return (user: user, token: token);
    } on DioException catch (e) {
      rethrow;
    } catch (e) {
      throw Exception('Erreur lors du parsing de la réponse: $e');
    }
  }

  @override
  Future<({UserModel user, String token})> register({
    required String name,
    required String email,
    required String password,
  }) async {
    try {
      // 1. Appeler POST /auth/register
      // Format réponse: { "message": "Utilisateur créé avec succès", "user_id": "..." }
      await _dio.post(
        '/auth/register',
        data: {
          'name': name,
          'email': email,
          'password': password,
        },
      );

      // 2. L'API ne retourne PAS directement le user complet
      //    Il faut se connecter pour obtenir le token
      final loginResponse = await _dio.post(
        '/auth/login',
        data: {
          'email': email,
          'password': password,
        },
      );

      final token = loginResponse.data['access_token'] as String;

      // 3. Récupérer le user complet via /auth/me avec le token
      final meResponse = await _dio.get(
        '/auth/me',
        options: Options(
          headers: {'Authorization': 'Bearer $token'},
        ),
      );

      final user = UserModel.fromJson(meResponse.data);

      return (user: user, token: token);
    } on DioException catch (e) {
      rethrow;
    } catch (e) {
      throw Exception('Erreur lors du parsing de la réponse: $e');
    }
  }

  @override
  Future<void> logout() async {
    try {
      await _dio.post('/auth/logout');
    } on DioException catch (e) {
      // Même si le logout API échoue, on continue
      // Le token sera supprimé localement
      print('Erreur logout API: $e');
    }
  }

  @override
  Future<UserModel> getCurrentUser() async {
    try {
      // GET /auth/me retourne directement l'objet user
      // Format: { "id": "...", "name": "...", "email": "...", "role": "...", "created_at": "..." }
      final response = await _dio.get('/auth/me');

      return UserModel.fromJson(response.data);
    } on DioException catch (e) {
      rethrow;
    } catch (e) {
      throw Exception('Erreur lors du parsing de la réponse: $e');
    }
  }
}
