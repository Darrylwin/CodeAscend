/// Constantes globales de l'application
class AppConstants {
  AppConstants._(); // Constructeur privé pour empêcher l'instanciation

  // ========================================================================
  // API
  // ========================================================================

  static const String baseUrl = 'https://backend-quiz-0ab2.onrender.com';

  // Timeouts
  static const Duration connectTimeout = Duration(seconds: 15);
  static const Duration receiveTimeout = Duration(seconds: 15);

  // ========================================================================
  // STORAGE (SharedPreferences)
  // ========================================================================

  // Clés de SharedPreferences centralisées — à utiliser partout
  static const String tokenKey = 'auth_token';
  static const String userKey = 'user_data';
  static const String themeKey = 'theme_mode';

  // Key pour le cache des catégories (JSON list)
  static const String categoriesKey = 'categories_cache';

  // Keys pour la feature Quiz (SharedPreferences)
  // Tentative en cours par quiz: quiz_attempt_in_progress_{quizId}
  static const String quizAttemptInProgressKeyPrefix =
      'quiz_attempt_in_progress_';

  // File d'attente des tentatives pending (liste JSON)
  static const String quizPendingSubmissionsKey = 'quiz_pending_submissions';

  // Historique local (optionnel)
  static const String quizAttemptsCacheKey = 'quiz_attempts_cache';

  // ========================================================================
  // NIVEAUX DE QUIZ
  // ========================================================================

  static const String levelBeginner = 'debutant';
  static const String levelIntermediate = 'intermediaire';
  static const String levelAdvanced = 'avance';
}
