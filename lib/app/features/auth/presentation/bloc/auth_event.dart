import 'package:equatable/equatable.dart';

/// Events pour le AuthBloc
///
/// Un event = une action utilisateur
abstract class AuthEvent extends Equatable {
  const AuthEvent();

  @override
  List<Object?> get props => [];
}

// ============================================================================
// LOGIN
// ============================================================================

/// Event: L'utilisateur tente de se connecter
class LoginRequested extends AuthEvent {
  final String email;
  final String password;

  const LoginRequested({
    required this.email,
    required this.password,
  });

  @override
  List<Object?> get props => [email, password];
}

// ============================================================================
// REGISTER
// ============================================================================

/// Event: L'utilisateur tente de s'inscrire
class RegisterRequested extends AuthEvent {
  final String name;
  final String email;
  final String password;

  const RegisterRequested({
    required this.name,
    required this.email,
    required this.password,
  });

  @override
  List<Object?> get props => [name, email, password];
}

// ============================================================================
// LOGOUT
// ============================================================================

/// Event: L'utilisateur se déconnecte
class LogoutRequested extends AuthEvent {
  const LogoutRequested();
}

// ============================================================================
// CHECK AUTH
// ============================================================================

/// Event: Vérifier si l'utilisateur est déjà connecté (au démarrage)
class AuthCheckRequested extends AuthEvent {
  const AuthCheckRequested();
}

// ============================================================================
// AUTO LOGOUT (session expirée)
// ============================================================================

/// Event: Déconnexion automatique (token expiré, 401)
class AutoLogoutTriggered extends AuthEvent {
  const AutoLogoutTriggered();
}
