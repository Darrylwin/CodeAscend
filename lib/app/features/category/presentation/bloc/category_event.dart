import 'package:equatable/equatable.dart';

/// Events pour CategoryBloc — actions utilisateur / lifecycle
abstract class CategoryEvent extends Equatable {
  const CategoryEvent();

  @override
  List<Object?> get props => [];
}

/// Demande de récupération de la liste des catégories
class FetchCategories extends CategoryEvent {
  final bool? isActive;
  final int page;
  final int perPage;
  final bool forceRefresh;

  const FetchCategories({
    this.isActive,
    this.page = 1,
    this.perPage = 20,
    this.forceRefresh = false,
  });

  @override
  List<Object?> get props => [isActive, page, perPage, forceRefresh];
}

/// Demande de récupération d'une catégorie par id
class FetchCategoryById extends CategoryEvent {
  final String id;

  const FetchCategoryById(this.id);

  @override
  List<Object?> get props => [id];
}