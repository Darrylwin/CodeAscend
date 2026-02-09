import 'package:equatable/equatable.dart';
import '../../domain/entities/user_entity.dart';

/// States pour le AuthBloc
///
/// Un state = un état de l'application
abstract class AuthState extends Equatable {
  const AuthState();

  @override
  List<Object?> get props => [];
}

// ============================================================================
// INITIAL
// ============================================================================

/// State initial (au lancement de l'app)
class AuthInitial extends AuthState {
  const AuthInitial();
}

// ============================================================================
// CHECKING
// ============================================================================

/// State: Vérification d'authentification en cours (au démarrage)
class AuthChecking extends AuthState {
  const AuthChecking();
}

// ============================================================================
// LOADING
// ============================================================================

/// State: Chargement en cours (login, register, logout)
class AuthLoading extends AuthState {
  const AuthLoading();
}

// ============================================================================
// AUTHENTICATED
// ============================================================================

/// State: Utilisateur connecté
class Authenticated extends AuthState {
  final UserEntity user;
  final String token;

  const Authenticated({
    required this.user,
    required this.token,
  });

  @override
  List<Object?> get props => [user, token];
}

// ============================================================================
// UNAUTHENTICATED
// ============================================================================

/// State: Utilisateur non connecté
class Unauthenticated extends AuthState {
  const Unauthenticated();
}

// ============================================================================
// ERROR
// ============================================================================

/// State: Erreur d'authentification
class AuthError extends AuthState {
  final String message;

  const AuthError(this.message);

  @override
  List<Object?> get props => [message];
}
