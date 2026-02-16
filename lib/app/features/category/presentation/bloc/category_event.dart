import 'package:equatable/equatable.dart';

abstract class CategoryEvent extends Equatable {
  const CategoryEvent();

  @override
  List<Object?> get props => [];
}

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

class FetchCategoryById extends CategoryEvent {
  final String id;
  final bool forceRefresh;

  const FetchCategoryById(this.id, {this.forceRefresh = false});

  @override
  List<Object?> get props => [id, forceRefresh];
}

/// Remet le bloc à son état initial pour forcer un rechargement complet.
class InvalidateCategoryCache extends CategoryEvent {
  const InvalidateCategoryCache();
}
