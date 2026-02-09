import 'package:equatable/equatable.dart';

/// Events pour le AttemptsBloc
abstract class AttemptsEvent extends Equatable {
  const AttemptsEvent();

  @override
  List<Object?> get props => [];
}

// ============================================================================
// LOAD ATTEMPTS
// ============================================================================

/// Event: Charger toutes les tentatives de l'utilisateur
class LoadAttempts extends AttemptsEvent {
  const LoadAttempts();
}

// ============================================================================
// REFRESH ATTEMPTS
// ============================================================================

/// Event: Rafraîchir les tentatives (pull-to-refresh)
class RefreshAttempts extends AttemptsEvent {
  const RefreshAttempts();
}

// ============================================================================
// FILTER ATTEMPTS
// ============================================================================

/// Event: Filtrer les tentatives
class FilterAttempts extends AttemptsEvent {
  final AttemptFilter filter;

  const FilterAttempts(this.filter);

  @override
  List<Object?> get props => [filter];
}

/// Types de filtres
enum AttemptFilter {
  all, // Toutes les tentatives
  inProgress, // Seulement en cours
  passed, // Seulement les réussies
  failed, // Seulement les échouées
}

// ============================================================================
// SORT ATTEMPTS
// ============================================================================

/// Event: Trier les tentatives
class SortAttempts extends AttemptsEvent {
  final AttemptSort sortBy;

  const SortAttempts(this.sortBy);

  @override
  List<Object?> get props => [sortBy];
}

/// Types de tri
enum AttemptSort {
  dateDesc, // Date décroissante (plus récent en premier)
  dateAsc, // Date croissante
  scoreDesc, // Score décroissant
  scoreAsc, // Score croissant
  categoryAsc, // Catégorie A-Z
}

// ============================================================================
// SEARCH ATTEMPTS
// ============================================================================

/// Event: Rechercher dans les tentatives
class SearchAttempts extends AttemptsEvent {
  final String query;

  const SearchAttempts(this.query);

  @override
  List<Object?> get props => [query];
}

// ============================================================================
// CLEAR SEARCH
// ============================================================================

/// Event: Effacer la recherche
class ClearSearch extends AttemptsEvent {
  const ClearSearch();
}