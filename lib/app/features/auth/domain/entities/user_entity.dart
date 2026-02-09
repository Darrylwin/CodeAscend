import 'package:equatable/equatable.dart';

/// Entity User (objet métier pur)
class UserEntity extends Equatable {
  final String id;
  final String name;
  final String email;
  final UserRole role;
  final DateTime createdAt;

  const UserEntity({
    required this.id,
    required this.name,
    required this.email,
    required this.role,
    required this.createdAt,
  });

  /// Vérifie si l'utilisateur est admin
  bool get isAdmin => role == UserRole.admin;

  /// Vérifie si l'utilisateur est un user normal
  bool get isUser => role == UserRole.user;

  /// Retourne les initiales (pour avatar)
  String get initials {
    final parts = name.split(' ');
    if (parts.length >= 2) {
      return '${parts[0][0]}${parts[1][0]}'.toUpperCase();
    }
    return name.isNotEmpty ? name[0].toUpperCase() : '?';
  }

  @override
  List<Object?> get props => [id, name, email, role, createdAt];

  @override
  String toString() =>
      'UserEntity(id: $id, name: $name, email: $email, role: $role)';
}

/// Rôles utilisateur
enum UserRole {
  admin,
  user;
}