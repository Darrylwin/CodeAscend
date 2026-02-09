import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/user_entity.dart';

/// Repository Auth (CONTRAT/INTERFACE)
///
/// Le domain définit CE QUE l'on veut faire
/// Le data layer implémente COMMENT on le fait
///
/// Either<Failure, Success> vient de dartz:
/// - Left(Failure) → Échec
/// - Right(Success) → Succès
/// Permet de gérer les erreurs de manière fonctionnelle
abstract class AuthRepository {
  /// Connexion utilisateur
  ///
  /// Params:
  /// - email: Email de l'utilisateur
  /// - password: Mot de passe
  ///
  /// Returns:
  /// - Left(Failure) si erreur
  /// - Right((UserEntity, String)) si succès (user + token)
  Future<Either<Failure, (UserEntity, String)>> login({
    required String email,
    required String password,
  });

  /// Inscription utilisateur
  ///
  /// Params:
  /// - name: Nom complet
  /// - email: Email
  /// - password: Mot de passe (min 8 caractères)
  ///
  /// Returns:
  /// - Left(Failure) si erreur
  /// - Right((UserEntity, String)) si succès (user + token)
  Future<Either<Failure, (UserEntity, String)>> register({
    required String name,
    required String email,
    required String password,
  });

  /// Déconnexion
  ///
  /// Supprime le token local et notifie le serveur
  ///
  /// Returns:
  /// - Left(Failure) si erreur
  /// - Right(void) si succès
  Future<Either<Failure, void>> logout();

  /// Récupérer l'utilisateur actuellement connecté
  ///
  /// Depuis le cache local ou depuis l'API si le token est valide
  ///
  /// Returns:
  /// - Left(Failure) si pas d'utilisateur ou token invalide
  /// - Right(UserEntity) si succès
  Future<Either<Failure, UserEntity>> getCurrentUser();

  /// Vérifier si un utilisateur est connecté
  ///
  /// Vérifie la présence d'un token valide
  ///
  /// Returns:
  /// - true si token présent et valide
  /// - false sinon
  Future<bool> isAuthenticated();

  /// Récupérer le token JWT stocké localement
  ///
  /// Returns:
  /// - null si pas de token
  /// - String token si présent
  Future<String?> getToken();
}
