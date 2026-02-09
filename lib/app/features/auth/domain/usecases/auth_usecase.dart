import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/user_entity.dart';
import '../repositories/auth_repository.dart';

// ============================================================================
// USE CASE: LOGIN
// ============================================================================

/// Use Case: Connexion d'un utilisateur
///
/// Chaque use case fait UNE SEULE CHOSE
/// C'est le principe de responsabilité unique (SOLID)
class LoginUseCase {
  final AuthRepository _repository;

  LoginUseCase(this._repository);

  /// Exécuter le use case
  ///
  /// Params: LoginParams (email + password)
  /// Returns: Either<Failure, (UserEntity, String)>
  Future<Either<Failure, (UserEntity, String)>> call(LoginParams params) {
    return _repository.login(
      email: params.email,
      password: params.password,
    );
  }
}

/// Paramètres pour le login
class LoginParams {
  final String email;
  final String password;

  const LoginParams({
    required this.email,
    required this.password,
  });
}

// ============================================================================
// USE CASE: REGISTER
// ============================================================================

/// Use Case: Inscription d'un nouvel utilisateur
class RegisterUseCase {
  final AuthRepository _repository;

  RegisterUseCase(this._repository);

  Future<Either<Failure, (UserEntity, String)>> call(RegisterParams params) {
    return _repository.register(
      name: params.name,
      email: params.email,
      password: params.password,
    );
  }
}

/// Paramètres pour le register
class RegisterParams {
  final String name;
  final String email;
  final String password;

  const RegisterParams({
    required this.name,
    required this.email,
    required this.password,
  });
}

// ============================================================================
// USE CASE: LOGOUT
// ============================================================================

/// Use Case: Déconnexion
class LogoutUseCase {
  final AuthRepository _repository;

  LogoutUseCase(this._repository);

  /// Pas de params nécessaires pour le logout
  Future<Either<Failure, void>> call() {
    return _repository.logout();
  }
}

// ============================================================================
// USE CASE: GET CURRENT USER
// ============================================================================

/// Use Case: Récupérer l'utilisateur connecté
class GetCurrentUserUseCase {
  final AuthRepository _repository;

  GetCurrentUserUseCase(this._repository);

  Future<Either<Failure, UserEntity>> call() {
    return _repository.getCurrentUser();
  }
}

// ============================================================================
// USE CASE: CHECK AUTHENTICATION
// ============================================================================

/// Use Case: Vérifier si un utilisateur est connecté
class CheckAuthenticationUseCase {
  final AuthRepository _repository;

  CheckAuthenticationUseCase(this._repository);

  Future<bool> call() {
    return _repository.isAuthenticated();
  }
}

// ============================================================================
// USE CASE: GET TOKEN
// ============================================================================

/// Use Case: Récupérer le token JWT
///
/// Utile pour debug ou pour l'afficher dans les settings
class GetTokenUseCase {
  final AuthRepository _repository;

  GetTokenUseCase(this._repository);

  Future<String?> call() {
    return _repository.getToken();
  }
}
