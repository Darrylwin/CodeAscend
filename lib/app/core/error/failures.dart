import 'package:equatable/equatable.dart';

/// Classe de base pour tous les échecs
/// Permet de séparer les exceptions techniques des erreurs métier
abstract class Failure extends Equatable {
  final String message;

  const Failure(this.message);

  @override
  List<Object?> get props => [message];
}

// ============================================================================
// FAILURES RÉSEAU
// ============================================================================

/// Erreur serveur (5xx)
class ServerFailure extends Failure {
  const ServerFailure([String message = 'Erreur serveur. Réessayez plus tard'])
      : super(message);
}

/// Pas de connexion internet
class ConnectionFailure extends Failure {
  const ConnectionFailure(
      [String message = 'Vérifiez votre connexion internet'])
      : super(message);
}

/// Timeout de requête
class TimeoutFailure extends Failure {
  const TimeoutFailure([String message = 'La requête a expiré'])
      : super(message);
}

// ============================================================================
// FAILURES AUTHENTIFICATION
// ============================================================================

/// Token JWT invalide ou expiré
class UnauthorizedFailure extends Failure {
  const UnauthorizedFailure(
      [String message = 'Session expirée. Reconnectez-vous'])
      : super(message);
}

/// Identifiants incorrects
class InvalidCredentialsFailure extends Failure {
  const InvalidCredentialsFailure(
      [String message = 'Email ou mot de passe incorrect'])
      : super(message);
}

/// Email déjà utilisé
class EmailAlreadyExistsFailure extends Failure {
  const EmailAlreadyExistsFailure(
      [String message = 'Cet email est déjà utilisé'])
      : super(message);
}

// ============================================================================
// FAILURES VALIDATION
// ============================================================================

/// Données invalides (400)
class ValidationFailure extends Failure {
  const ValidationFailure([String message = 'Données invalides'])
      : super(message);
}

/// Ressource introuvable (404)
class NotFoundFailure extends Failure {
  const NotFoundFailure([String message = 'Ressource introuvable'])
      : super(message);
}

/// Action interdite (403)
class ForbiddenFailure extends Failure {
  const ForbiddenFailure([String message = 'Accès refusé']) : super(message);
}

// ============================================================================
// FAILURES MÉTIER (spécifiques à l'app quiz)
// ============================================================================

/// Quiz non accessible (niveau bloqué)
class QuizLockedFailure extends Failure {
  const QuizLockedFailure(
      [String message =
          'Complétez le niveau précédent avec ≥80% pour débloquer'])
      : super(message);
}

/// Quiz incomplet (< 10 questions)
class IncompleteQuizFailure extends Failure {
  const IncompleteQuizFailure(
      [String message = 'Ce quiz doit avoir exactement 10 questions'])
      : super(message);
}

/// Tentative de suppression avec contraintes
class DeleteConstraintFailure extends Failure {
  const DeleteConstraintFailure(
      [String message =
          'Impossible de supprimer : élément en cours d\'utilisation'])
      : super(message);
}

// ============================================================================
// FAILURES QUIZ (feature-specific)
// ============================================================================

class QuizStartFailure extends Failure {
  const QuizStartFailure([String message = 'Impossible de démarrer le quiz'])
      : super(message);
}

class QuizSubmitFailure extends Failure {
  const QuizSubmitFailure([String message = 'Impossible de soumettre le quiz'])
      : super(message);
}

class QuizOfflineFailure extends Failure {
  const QuizOfflineFailure(
      [String message =
          'Opération en mode hors-ligne — mise en file d\'attente'])
      : super(message);
}

class QuizNotFoundFailure extends Failure {
  const QuizNotFoundFailure([String message = 'Quiz introuvable'])
      : super(message);
}

// ============================================================================
// FAILURES CATEGORY (feature-specific)
// ============================================================================

/// Impossible de récupérer la liste des catégories (API down / erreur)
class CategoriesUnavailableFailure extends Failure {
  const CategoriesUnavailableFailure(
      [String message = 'Impossible de récupérer les catégories'])
      : super(message);
}

/// Catégorie non trouvée
class CategoryNotFoundFailure extends Failure {
  const CategoryNotFoundFailure([String message = 'Catégorie introuvable'])
      : super(message);
}

// ============================================================================
// FAILURES LOCALES
// ============================================================================

/// Erreur de cache local
class CacheFailure extends Failure {
  const CacheFailure([String message = 'Erreur de cache local'])
      : super(message);
}

/// Erreur générique
class UnknownFailure extends Failure {
  const UnknownFailure(
      [String message = 'Une erreur inattendue s\'est produite'])
      : super(message);
}
