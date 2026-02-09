import '../../domain/entities/user_entity.dart';

/// Model User (hérite de UserEntity)
/// 
/// Responsabilité:
/// - Conversion JSON ↔ Entity
/// - Parsing des données API
class UserModel extends UserEntity {
  const UserModel({
    required super.id,
    required super.name,
    required super.email,
    required super.role,
    required super.createdAt,
  });

  /// Factory: Créer depuis JSON (API response)
  /// 
  /// Format attendu selon le cahier des charges:
  /// {
  ///   "id": "uuid",
  ///   "name": "User",
  ///   "email": "john@example.com",
  ///   "role": "user",
  ///   "created_at": "2026-01-10T12:00:00Z"
  /// }
  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['id'] as String,
      name: json['name'] as String,
      email: json['email'] as String,
      role: _parseRole(json['role'] as String),
      createdAt: DateTime.parse(json['created_at'] as String),
    );
  }

  /// Méthode statique pour parser le rôle depuis string
  static UserRole _parseRole(String value) {
    switch (value.toLowerCase()) {
      case 'admin':
        return UserRole.admin;
      case 'user':
        return UserRole.user;
      default:
        return UserRole.user;
    }
  }

  /// Méthode statique pour convertir rôle vers string
  static String _roleToString(UserRole role) {
    switch (role) {
      case UserRole.admin:
        return 'admin';
      case UserRole.user:
        return 'user';
    }
  }

  /// Convertir vers JSON (pour cache local)
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'email': email,
      'role': _roleToString(role),
      'created_at': createdAt.toIso8601String(),
    };
  }

  /// Factory: Créer depuis Entity
  factory UserModel.fromEntity(UserEntity entity) {
    return UserModel(
      id: entity.id,
      name: entity.name,
      email: entity.email,
      role: entity.role,
      createdAt: entity.createdAt,
    );
  }

  /// Convertir vers Entity
  UserEntity toEntity() {
    return UserEntity(
      id: id,
      name: name,
      email: email,
      role: role,
      createdAt: createdAt,
    );
  }

  /// CopyWith pour créer une copie avec des modifications
  UserModel copyWith({
    String? id,
    String? name,
    String? email,
    UserRole? role,
    DateTime? createdAt,
  }) {
    return UserModel(
      id: id ?? this.id,
      name: name ?? this.name,
      email: email ?? this.email,
      role: role ?? this.role,
      createdAt: createdAt ?? this.createdAt,
    );
  }
}