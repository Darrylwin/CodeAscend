import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';
import '../../../../core/utils/app_constants.dart';
import '../models/quiz_attempt_model.dart';

/// Interface pour le local datasource Quiz
abstract class QuizLocalDataSource {
  Future<void> saveInProgressAttempt(QuizAttemptModel attempt);
  Future<QuizAttemptModel?> getInProgressAttempt(String quizId);
  Future<void> clearInProgressAttempt(String quizId);

  Future<void> addPendingSubmission(QuizAttemptModel attempt);
  Future<List<QuizAttemptModel>> getPendingSubmissions();
  Future<void> removePendingSubmission(String localId);

  Future<void> cacheAttemptHistory(QuizAttemptModel attempt);
}

class QuizLocalDataSourceImpl implements QuizLocalDataSource {
  final SharedPreferences _prefs;

  QuizLocalDataSourceImpl(this._prefs);

  String _inProgressKey(String quizId) =>
      '${AppConstants.quizAttemptInProgressKeyPrefix}$quizId';

  @override
  Future<void> saveInProgressAttempt(QuizAttemptModel attempt) async {
    final key = _inProgressKey(attempt.quizId);
    final jsonString = jsonEncode(attempt.toJson());
    await _prefs.setString(key, jsonString);
  }

  @override
  Future<QuizAttemptModel?> getInProgressAttempt(String quizId) async {
    final key = _inProgressKey(quizId);
    final jsonString = _prefs.getString(key);
    if (jsonString == null) return null;
    try {
      final map = jsonDecode(jsonString) as Map<String, dynamic>;
      return QuizAttemptModel.fromJson(map);
    } catch (e) {
      await clearInProgressAttempt(quizId);
      return null;
    }
  }

  @override
  Future<void> clearInProgressAttempt(String quizId) async {
    final key = _inProgressKey(quizId);
    await _prefs.remove(key);
  }

  // Pending submissions queue stored as JSON list
  @override
  Future<void> addPendingSubmission(QuizAttemptModel attempt) async {
    final jsonString = _prefs.getString(AppConstants.quizPendingSubmissionsKey);
    final List<dynamic> list =
        jsonString != null ? jsonDecode(jsonString) as List<dynamic> : [];
    list.add(attempt.toJson());
    await _prefs.setString(
        AppConstants.quizPendingSubmissionsKey, jsonEncode(list));
  }

  @override
  Future<List<QuizAttemptModel>> getPendingSubmissions() async {
    final jsonString = _prefs.getString(AppConstants.quizPendingSubmissionsKey);
    if (jsonString == null) return [];
    try {
      final list = jsonDecode(jsonString) as List<dynamic>;
      return list
          .cast<Map<String, dynamic>>()
          .map((m) => QuizAttemptModel.fromJson(m))
          .toList();
    } catch (e) {
      await _prefs.remove(AppConstants.quizPendingSubmissionsKey);
      return [];
    }
  }

  @override
  Future<void> removePendingSubmission(String localId) async {
    final jsonString = _prefs.getString(AppConstants.quizPendingSubmissionsKey);
    if (jsonString == null) return;
    try {
      final list = (jsonDecode(jsonString) as List<dynamic>)
          .cast<Map<String, dynamic>>();
      final remaining =
          list.where((m) => (m['local_id'] as String) != localId).toList();
      await _prefs.setString(
          AppConstants.quizPendingSubmissionsKey, jsonEncode(remaining));
    } catch (e) {
      await _prefs.remove(AppConstants.quizPendingSubmissionsKey);
    }
  }

  @override
  Future<void> cacheAttemptHistory(QuizAttemptModel attempt) async {
    // Simple implementation: append to a list under quizAttemptsCacheKey
    final jsonString = _prefs.getString(AppConstants.quizAttemptsCacheKey);
    final List<dynamic> list =
        jsonString != null ? jsonDecode(jsonString) as List<dynamic> : [];
    list.add(attempt.toJson());
    await _prefs.setString(AppConstants.quizAttemptsCacheKey, jsonEncode(list));
  }
}
