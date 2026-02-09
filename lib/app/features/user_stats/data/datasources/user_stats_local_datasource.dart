import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';

import '../models/user_stats_model.dart';

/// Local DataSource pour UserStats (cache)
abstract class UserStatsLocalDataSource {
  /// Sauvegarder la progression en cache
  Future<void> cacheProgression(UserProgressionModel progression);

  /// Récupérer la progression depuis le cache
  Future<UserProgressionModel?> getCachedProgression();

  /// Supprimer le cache
  Future<void> clearCache();
}

class UserStatsLocalDataSourceImpl implements UserStatsLocalDataSource {
  final SharedPreferences _prefs;
  static const String _cacheKey = 'cached_user_progression';

  UserStatsLocalDataSourceImpl(this._prefs);

  @override
  Future<void> cacheProgression(UserProgressionModel progression) async {
    final jsonString = jsonEncode(progression.toJson());
    await _prefs.setString(_cacheKey, jsonString);
  }

  @override
  Future<UserProgressionModel?> getCachedProgression() async {
    try {
      final jsonString = _prefs.getString(_cacheKey);

      if (jsonString == null) return null;

      final jsonMap = jsonDecode(jsonString) as Map<String, dynamic>;

      return UserProgressionModel.fromJson(jsonMap);
    } catch (e) {
      // Si erreur de parsing, supprimer le cache corrompu
      await clearCache();
      return null;
    }
  }

  @override
  Future<void> clearCache() async {
    await _prefs.remove(_cacheKey);
  }
}
