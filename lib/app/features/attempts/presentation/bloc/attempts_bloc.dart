import 'package:flutter/foundation.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../domain/entities/attempt_summary_entity.dart';
import '../../domain/usecases/attempts_usecases.dart';
import 'attempts_event.dart';
import 'attempts_state.dart';

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
    on<InvalidateAttempts>(_onInvalidateAttempts);
  }

  // ==========================================================================
  // LOAD
  // ==========================================================================

  Future<void> _onLoadAttempts(
    LoadAttempts event,
    Emitter<AttemptsState> emit,
  ) async {
    // Skip uniquement si déjà chargé ET pas de forceLoad
    if (state is AttemptsLoaded && !event.forceLoad) {
      debugPrint('⏭️ AttemptsBloc: déjà chargé, skip LoadAttempts');
      return;
    }
    if (state is AttemptsLoading) {
      debugPrint('⏭️ AttemptsBloc: chargement déjà en cours, skip');
      return;
    }

    debugPrint('📥 AttemptsBloc: LoadAttempts...');
    emit(const AttemptsLoading());
    await _fetchAndEmit(emit, previousState: null);
  }

  // ==========================================================================
  // REFRESH
  // ==========================================================================

  Future<void> _onRefreshAttempts(
    RefreshAttempts event,
    Emitter<AttemptsState> emit,
  ) async {
    final currentState = state;
    debugPrint('🔄 AttemptsBloc: RefreshAttempts...');

    if (currentState is AttemptsLoaded) {
      // Indiquer le refresh sans perdre les données actuelles
      emit(currentState.copyWith(isRefreshing: true));
      await _fetchAndEmit(emit, previousState: currentState);
    } else {
      // Pas encore de données → chargement complet
      emit(const AttemptsLoading());
      await _fetchAndEmit(emit, previousState: null);
    }
  }

  // ==========================================================================
  // INVALIDATE
  // ==========================================================================

  Future<void> _onInvalidateAttempts(
    InvalidateAttempts event,
    Emitter<AttemptsState> emit,
  ) async {
    debugPrint(
        '🗑️ AttemptsBloc: cache invalidé (forceReload=${event.forceReload})');
    emit(const AttemptsInitial());

    if (event.forceReload) {
      emit(const AttemptsLoading());
      await _fetchAndEmit(emit, previousState: null);
    }
  }

  // ==========================================================================
  // FILTER / SORT / SEARCH
  // ==========================================================================

  void _onFilterAttempts(FilterAttempts event, Emitter<AttemptsState> emit) {
    final s = state;
    if (s is! AttemptsLoaded) return;
    final filtered =
        _applyFiltersAndSearch(s.allAttempts, event.filter, s.searchQuery);
    final sorted = _sortAttempts(filtered, s.currentSort);
    emit(s.copyWith(filteredAttempts: sorted, currentFilter: event.filter));
  }

  void _onSortAttempts(SortAttempts event, Emitter<AttemptsState> emit) {
    final s = state;
    if (s is! AttemptsLoaded) return;
    final sorted = _sortAttempts(s.filteredAttempts, event.sortBy);
    emit(s.copyWith(filteredAttempts: sorted, currentSort: event.sortBy));
  }

  void _onSearchAttempts(SearchAttempts event, Emitter<AttemptsState> emit) {
    final s = state;
    if (s is! AttemptsLoaded) return;
    final filtered =
        _applyFiltersAndSearch(s.allAttempts, s.currentFilter, event.query);
    final sorted = _sortAttempts(filtered, s.currentSort);
    emit(s.copyWith(filteredAttempts: sorted, searchQuery: event.query));
  }

  void _onClearSearch(ClearSearch event, Emitter<AttemptsState> emit) {
    final s = state;
    if (s is! AttemptsLoaded) return;
    final filtered = _applyFiltersAndSearch(s.allAttempts, s.currentFilter, '');
    final sorted = _sortAttempts(filtered, s.currentSort);
    emit(s.copyWith(filteredAttempts: sorted, searchQuery: ''));
  }

  // ==========================================================================
  // HELPERS
  // ==========================================================================

  /// Logique de fetch centralisée — évite la duplication entre Load et Refresh.
  Future<void> _fetchAndEmit(
    Emitter<AttemptsState> emit, {
    required AttemptsLoaded? previousState,
  }) async {
    final attemptsResult = await _getUserAttemptsUseCase();

    await attemptsResult.fold(
      (failure) async {
        debugPrint('❌ AttemptsBloc fetch error: ${failure.message}');
        if (previousState != null) {
          // Garder les données existantes si erreur réseau
          emit(previousState.copyWith(isRefreshing: false));
        } else {
          emit(AttemptsError(failure.message));
        }
      },
      (attempts) async {
        final statsResult = await _getAttemptStatisticsUseCase();

        statsResult.fold(
          (failure) {
            if (previousState != null) {
              emit(previousState.copyWith(isRefreshing: false));
            } else {
              emit(AttemptsError(failure.message));
            }
          },
          (stats) {
            // Réappliquer les filtres/tri/recherche du state précédent
            final filter = previousState?.currentFilter ?? AttemptFilter.all;
            final sort = previousState?.currentSort ?? AttemptSort.dateDesc;
            final query = previousState?.searchQuery ?? '';

            final filtered = _applyFiltersAndSearch(attempts, filter, query);
            final sorted = _sortAttempts(filtered, sort);

            debugPrint(
                '✅ AttemptsBloc: ${attempts.length} tentative(s) chargée(s)');

            emit(AttemptsLoaded(
              allAttempts: attempts,
              filteredAttempts: sorted,
              statistics: stats,
              currentFilter: filter,
              currentSort: sort,
              searchQuery: query,
              isRefreshing: false,
            ));
          },
        );
      },
    );
  }

  List<AttemptSummaryEntity> _applyFiltersAndSearch(
    List<AttemptSummaryEntity> attempts,
    AttemptFilter filter,
    String searchQuery,
  ) {
    var result = List<AttemptSummaryEntity>.from(attempts);

    switch (filter) {
      case AttemptFilter.inProgress:
        result = result.where((a) => a.isInProgress).toList();
        break;
      case AttemptFilter.passed:
        result = result.where((a) => a.passed && !a.isInProgress).toList();
        break;
      case AttemptFilter.failed:
        result = result.where((a) => !a.passed && !a.isInProgress).toList();
        break;
      case AttemptFilter.all:
        break;
    }

    if (searchQuery.isNotEmpty) {
      final q = searchQuery.toLowerCase();
      result = result
          .where((a) =>
              a.quizTitle.toLowerCase().contains(q) ||
              a.categoryName.toLowerCase().contains(q))
          .toList();
    }

    return result;
  }

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
