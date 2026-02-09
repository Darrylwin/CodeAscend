import 'package:equatable/equatable.dart';
import '../../domain/entities/attempt_summary_entity.dart';
import '../../domain/repositories/attempts_repository.dart';
import 'attempts_event.dart';

/// States pour le AttemptsBloc
abstract class AttemptsState extends Equatable {
  const AttemptsState();

  @override
  List<Object?> get props => [];
}

// ============================================================================
// INITIAL
// ============================================================================

/// State initial
class AttemptsInitial extends AttemptsState {
  const AttemptsInitial();
}

// ============================================================================
// LOADING
// ============================================================================

/// State: Chargement en cours (première fois)
class AttemptsLoading extends AttemptsState {
  const AttemptsLoading();
}

// ============================================================================
// LOADED
// ============================================================================

/// State: Tentatives chargées avec succès
class AttemptsLoaded extends AttemptsState {
  final List<AttemptSummaryEntity>
      allAttempts; // Toutes les tentatives (non filtrées)
  final List<AttemptSummaryEntity>
      filteredAttempts; // Tentatives affichées (après filtrage/tri/recherche)
  final AttemptStatistics statistics;
  final AttemptFilter currentFilter;
  final AttemptSort currentSort;
  final String searchQuery;
  final bool isRefreshing; // Pour le pull-to-refresh

  const AttemptsLoaded({
    required this.allAttempts,
    required this.filteredAttempts,
    required this.statistics,
    this.currentFilter = AttemptFilter.all,
    this.currentSort = AttemptSort.dateDesc,
    this.searchQuery = '',
    this.isRefreshing = false,
  });

  /// Vérifie si des filtres sont actifs
  bool get hasActiveFilters =>
      currentFilter != AttemptFilter.all ||
      searchQuery.isNotEmpty ||
      currentSort != AttemptSort.dateDesc;

  /// Vérifie si aucune tentative n'est affichée
  bool get isEmpty => filteredAttempts.isEmpty;

  /// Vérifie si l'utilisateur n'a aucune tentative
  bool get hasNoAttempts => allAttempts.isEmpty;

  @override
  List<Object?> get props => [
        allAttempts,
        filteredAttempts,
        statistics,
        currentFilter,
        currentSort,
        searchQuery,
        isRefreshing,
      ];

  /// CopyWith pour créer une nouvelle instance avec modifications
  AttemptsLoaded copyWith({
    List<AttemptSummaryEntity>? allAttempts,
    List<AttemptSummaryEntity>? filteredAttempts,
    AttemptStatistics? statistics,
    AttemptFilter? currentFilter,
    AttemptSort? currentSort,
    String? searchQuery,
    bool? isRefreshing,
  }) {
    return AttemptsLoaded(
      allAttempts: allAttempts ?? this.allAttempts,
      filteredAttempts: filteredAttempts ?? this.filteredAttempts,
      statistics: statistics ?? this.statistics,
      currentFilter: currentFilter ?? this.currentFilter,
      currentSort: currentSort ?? this.currentSort,
      searchQuery: searchQuery ?? this.searchQuery,
      isRefreshing: isRefreshing ?? this.isRefreshing,
    );
  }
}

// ============================================================================
// ERROR
// ============================================================================

/// State: Erreur lors du chargement
class AttemptsError extends AttemptsState {
  final String message;

  const AttemptsError(this.message);

  @override
  List<Object?> get props => [message];
}
