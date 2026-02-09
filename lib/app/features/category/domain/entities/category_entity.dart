import 'package:equatable/equatable.dart';

/// Entity représentant une catégorie de quiz
///
/// Cette classe se trouve dans la couche "domain" et ne contient
/// QUE des données/logic métier pures (pas de JSON, pas de dépendances externes).
class CategoryEntity extends Equatable {
  final String id;
  final String name;
  final String? description;
  final String? iconUrl;
  final bool isActive;
  final DateTime createdAt;

  const CategoryEntity({
    required this.id,
    required this.name,
    this.description,
    this.iconUrl,
    required this.isActive,
    required this.createdAt,
  });

  /// Crée une copie avec des champs modifiés
  CategoryEntity copyWith({
    String? id,
    String? name,
    String? description,
    String? iconUrl,
    bool? isActive,
    DateTime? createdAt,
  }) {
    return CategoryEntity(
      id: id ?? this.id,
      name: name ?? this.name,
      description: description ?? this.description,
      iconUrl: iconUrl ?? this.iconUrl,
      isActive: isActive ?? this.isActive,
      createdAt: createdAt ?? this.createdAt,
    );
  }

  @override
  List<Object?> get props => [id, name, description, iconUrl, isActive, createdAt];

  @override
  String toString() {
    return 'CategoryEntity(id: $id, name: $name, isActive: $isActive)';
  }
}