import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/attempt_summary_model.dart';

/// Local DataSource pour Attempts (cache)
abstract class AttemptsLocalDataSource {
  /// Sauvegarder la liste des tentatives en cache
  Future<void> cacheAttempts(List<AttemptSummaryModel> attempts);

  /// Récupérer la liste des tentatives depuis le cache
  Future<List<AttemptSummaryModel>?> getCachedAttempts();

  /// Supprimer le cache des tentatives
  Future<void> clearCache();
}

class AttemptsLocalDataSourceImpl implements AttemptsLocalDataSource {
  final SharedPreferences _prefs;
  static const String _cacheKey = 'cached_attempts';

  AttemptsLocalDataSourceImpl(this._prefs);

  @override
  Future<void> cacheAttempts(List<AttemptSummaryModel> attempts) async {
    final jsonList = attempts.map((a) => a.toJson()).toList();
    final jsonString = jsonEncode(jsonList);
    await _prefs.setString(_cacheKey, jsonString);
  }

  @override
  Future<List<AttemptSummaryModel>?> getCachedAttempts() async {
    try {
      final jsonString = _prefs.getString(_cacheKey);

      if (jsonString == null) return null;

      final jsonList = jsonDecode(jsonString) as List<dynamic>;

      return jsonList
          .cast<Map<String, dynamic>>()
          .map((json) => AttemptSummaryModel.fromJson(json))
          .toList();
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
