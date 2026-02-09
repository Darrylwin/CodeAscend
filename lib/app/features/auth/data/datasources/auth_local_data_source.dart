import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/user_model.dart';
import '../../../../core/utils/app_constants.dart';

/// Local DataSource pour l'authentification
///
/// Responsabilité: Gérer le cache local (SharedPreferences)
/// - Sauvegarder/récupérer le token JWT
/// - Sauvegarder/récupérer les données user
abstract class AuthLocalDataSource {
  /// Sauvegarder le token JWT
  Future<void> saveToken(String token);

  /// Récupérer le token JWT
  Future<String?> getToken();

  /// Supprimer le token JWT
  Future<void> deleteToken();

  /// Sauvegarder l'utilisateur en cache
  Future<void> cacheUser(UserModel user);

  /// Récupérer l'utilisateur du cache
  Future<UserModel?> getCachedUser();

  /// Supprimer l'utilisateur du cache
  Future<void> deleteCachedUser();

  /// Tout supprimer (logout complet)
  Future<void> clearAll();

  /// Récupérer l'ID de l'utilisateur connecté
  /// 
  /// Méthode helper pour accéder rapidement au userId
  /// sans avoir à récupérer tout l'objet user.
  /// 
  /// Returns:
  /// - String userId si utilisateur en cache
  /// - null si pas d'utilisateur
  Future<String?> getCurrentUserId();
}

/// Implémentation du local data source
class AuthLocalDataSourceImpl implements AuthLocalDataSource {
  final SharedPreferences _prefs;

  AuthLocalDataSourceImpl(this._prefs);

  @override
  Future<void> saveToken(String token) async {
    await _prefs.setString(AppConstants.tokenKey, token);
  }

  @override
  Future<String?> getToken() async {
    return _prefs.getString(AppConstants.tokenKey);
  }

  @override
  Future<void> deleteToken() async {
    await _prefs.remove(AppConstants.tokenKey);
  }

  @override
  Future<void> cacheUser(UserModel user) async {
    // Convertir l'user en JSON string pour le stocker
    final userJson = json.encode(user.toJson());
    await _prefs.setString(AppConstants.userKey, userJson);
  }

  @override
  Future<UserModel?> getCachedUser() async {
    try {
      final userJson = _prefs.getString(AppConstants.userKey);

      if (userJson == null) return null;

      final userMap = json.decode(userJson) as Map<String, dynamic>;
      return UserModel.fromJson(userMap);
    } catch (e) {
      // Si erreur de parsing, supprimer le cache corrompu
      await deleteCachedUser();
      return null;
    }
  }

  @override
  Future<void> deleteCachedUser() async {
    await _prefs.remove(AppConstants.userKey);
  }

  @override
  Future<void> clearAll() async {
    await Future.wait([
      deleteToken(),
      deleteCachedUser(),
    ]);
  }

  /// Implémentation de getCurrentUserId
  @override
  Future<String?> getCurrentUserId() async {
    try {
      final user = await getCachedUser();
      return user?.id;
    } catch (_) {
      return null;
    }
  }
}