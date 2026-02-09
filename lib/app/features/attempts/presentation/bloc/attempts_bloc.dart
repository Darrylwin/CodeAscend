import 'package:flutter_bloc/flutter_bloc.dart';
import '../../domain/entities/attempt_summary_entity.dart';
import '../../domain/usecases/attempts_usecases.dart';
import 'attempts_event.dart';
import 'attempts_state.dart';

/// Bloc pour gérer l'historique des tentatives
///
/// Fonctionnalités:
/// - Chargement des tentatives
/// - Filtrage (toutes/réussies/échouées)
/// - Tri (date/score/catégorie)
/// - Recherche par titre
/// - Pull-to-refresh
/// - Calcul des statistiques
class AttemptsBloc extends Bloc<AttemptsEvent, AttemptsState> {
  final GetUserAttemptsUseCase _getUserAttemptsUseCase;
  final GetAttemptStatisticsUseCase _getAttemptStatisticsUseCase;

  AttemptsBloc({
    required GetUserAttemptsUseCase getUserAttemptsUseCase,
    required GetAttemptStatisticsUseCase getAttemptStatisticsUseCase,
  })  : _getUserAttemptsUseCase = getUserAttemptsUseCase,
        _getAttemptStatisticsUseCase = getAttemptStatisticsUseCase,
        super(const AttemptsInitial()) {
    on<LoadAttempts>(_onLoadAttempts);
    on<RefreshAttempts>(_onRefreshAttempts);
    on<FilterAttempts>(_onFilterAttempts);
    on<SortAttempts>(_onSortAttempts);
    on<SearchAttempts>(_onSearchAttempts);
    on<ClearSearch>(_onClearSearch);
  }

  // ==========================================================================
  // LOAD ATTEMPTS
  // ==========================================================================

  Future<void> _onLoadAttempts(
    LoadAttempts event,
    Emitter<AttemptsState> emit,
  ) async {
    emit(const AttemptsLoading());

    // 1. Récupérer les tentatives
    final attemptsResult = await _getUserAttemptsUseCase();

    await attemptsResult.fold(
      (failure) async {
        emit(AttemptsError(failure.message));
      },
      (attempts) async {
        // 2. Récupérer les statistiques
        final statsResult = await _getAttemptStatisticsUseCase();

        statsResult.fold(
          (failure) => emit(AttemptsError(failure.message)),
          (stats) {
            // 3. Trier par défaut (date décroissante)
            final sorted = _sortAttempts(attempts, AttemptSort.dateDesc);

            emit(AttemptsLoaded(
              allAttempts: attempts,
              filteredAttempts: sorted,
              statistics: stats,
            ));
          },
        );
      },
    );
  }

  // ==========================================================================
  // REFRESH ATTEMPTS
  // ==========================================================================

  Future<void> _onRefreshAttempts(
    RefreshAttempts event,
    Emitter<AttemptsState> emit,
  ) async {
    final currentState = state;

    // Marquer comme en cours de refresh
    if (currentState is AttemptsLoaded) {
      emit(currentState.copyWith(isRefreshing: true));
    }

    // Recharger les données
    final attemptsResult = await _getUserAttemptsUseCase();

    await attemptsResult.fold(
      (failure) async {
        // En cas d'erreur, garder les données actuelles
        if (currentState is AttemptsLoaded) {
          emit(currentState.copyWith(isRefreshing: false));
        } else {
          emit(AttemptsError(failure.message));
        }
      },
      (attempts) async {
        final statsResult = await _getAttemptStatisticsUseCase();

        statsResult.fold(
          (failure) {
            if (currentState is AttemptsLoaded) {
              emit(currentState.copyWith(isRefreshing: false));
            }
          },
          (stats) {
            // Réappliquer les filtres/tri/recherche actuels
            if (currentState is AttemptsLoaded) {
              final filtered = _applyFiltersAndSearch(
                attempts,
                currentState.currentFilter,
                currentState.searchQuery,
              );
              final sorted = _sortAttempts(filtered, currentState.currentSort);

              emit(AttemptsLoaded(
                allAttempts: attempts,
                filteredAttempts: sorted,
                statistics: stats,
                currentFilter: currentState.currentFilter,
                currentSort: currentState.currentSort,
                searchQuery: currentState.searchQuery,
                isRefreshing: false,
              ));
            } else {
              final sorted = _sortAttempts(attempts, AttemptSort.dateDesc);
              emit(AttemptsLoaded(
                allAttempts: attempts,
                filteredAttempts: sorted,
                statistics: stats,
                isRefreshing: false,
              ));
            }
          },
        );
      },
    );
  }

  // ==========================================================================
  // FILTER ATTEMPTS
  // ==========================================================================

  void _onFilterAttempts(
    FilterAttempts event,
    Emitter<AttemptsState> emit,
  ) {
    final currentState = state;
    if (currentState is! AttemptsLoaded) return;

    // Appliquer le filtre
    final filtered = _applyFiltersAndSearch(
      currentState.allAttempts,
      event.filter,
      currentState.searchQuery,
    );

    // Trier
    final sorted = _sortAttempts(filtered, currentState.currentSort);

    emit(currentState.copyWith(
      filteredAttempts: sorted,
      currentFilter: event.filter,
    ));
  }

  // ==========================================================================
  // SORT ATTEMPTS
  // ==========================================================================

  void _onSortAttempts(
    SortAttempts event,
    Emitter<AttemptsState> emit,
  ) {
    final currentState = state;
    if (currentState is! AttemptsLoaded) return;

    // Trier les tentatives actuellement affichées
    final sorted = _sortAttempts(currentState.filteredAttempts, event.sortBy);

    emit(currentState.copyWith(
      filteredAttempts: sorted,
      currentSort: event.sortBy,
    ));
  }

  // ==========================================================================
  // SEARCH ATTEMPTS
  // ==========================================================================

  void _onSearchAttempts(
    SearchAttempts event,
    Emitter<AttemptsState> emit,
  ) {
    final currentState = state;
    if (currentState is! AttemptsLoaded) return;

    // Appliquer le filtre et la recherche
    final filtered = _applyFiltersAndSearch(
      currentState.allAttempts,
      currentState.currentFilter,
      event.query,
    );

    // Trier
    final sorted = _sortAttempts(filtered, currentState.currentSort);

    emit(currentState.copyWith(
      filteredAttempts: sorted,
      searchQuery: event.query,
    ));
  }

  // ==========================================================================
  // CLEAR SEARCH
  // ==========================================================================

  void _onClearSearch(
    ClearSearch event,
    Emitter<AttemptsState> emit,
  ) {
    final currentState = state;
    if (currentState is! AttemptsLoaded) return;

    // Réappliquer juste le filtre sans recherche
    final filtered = _applyFiltersAndSearch(
      currentState.allAttempts,
      currentState.currentFilter,
      '',
    );

    final sorted = _sortAttempts(filtered, currentState.currentSort);

    emit(currentState.copyWith(
      filteredAttempts: sorted,
      searchQuery: '',
    ));
  }

  // ==========================================================================
  // HELPER METHODS
  // ==========================================================================

  /// Applique le filtre et la recherche

  List<AttemptSummaryEntity> _applyFiltersAndSearch(
    List<AttemptSummaryEntity> attempts,
    AttemptFilter filter,
    String searchQuery,
  ) {
    var result = List<AttemptSummaryEntity>.from(attempts);

    // 1. Appliquer le filtre
    switch (filter) {
      case AttemptFilter.inProgress:
        // Afficher uniquement les tentatives en cours
        result = result.where((a) => a.isInProgress).toList();
        break;
      case AttemptFilter.passed:
        // Afficher uniquement les tentatives réussies (et terminées)
        result = result.where((a) => a.passed && !a.isInProgress).toList();
        break;
      case AttemptFilter.failed:
        // Afficher uniquement les tentatives échouées (et terminées)
        result = result.where((a) => !a.passed && !a.isInProgress).toList();
        break;
      case AttemptFilter.all:
        // Pas de filtre
        break;
    }

    // 2. Appliquer la recherche
    if (searchQuery.isNotEmpty) {
      final lowerQuery = searchQuery.toLowerCase();
      result = result.where((a) {
        return a.quizTitle.toLowerCase().contains(lowerQuery) ||
            a.categoryName.toLowerCase().contains(lowerQuery);
      }).toList();
    }

    return result;
  }

  /// Trie la liste selon le critère
  List<AttemptSummaryEntity> _sortAttempts(
    List<AttemptSummaryEntity> attempts,
    AttemptSort sortBy,
  ) {
    final sorted = List<AttemptSummaryEntity>.from(attempts);

    switch (sortBy) {
      case AttemptSort.dateDesc:
        sorted.sort((a, b) => b.completedAt.compareTo(a.completedAt));
        break;

      case AttemptSort.dateAsc:
        sorted.sort((a, b) => a.completedAt.compareTo(b.completedAt));
        break;

      case AttemptSort.scoreDesc:
        sorted.sort((a, b) => b.score.compareTo(a.score));
        break;

      case AttemptSort.scoreAsc:
        sorted.sort((a, b) => a.score.compareTo(b.score));
        break;

      case AttemptSort.categoryAsc:
        sorted.sort((a, b) => a.categoryName.compareTo(b.categoryName));
        break;
    }

    return sorted;
  }
}
