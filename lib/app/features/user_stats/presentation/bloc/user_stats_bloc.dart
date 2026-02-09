import 'package:flutter_bloc/flutter_bloc.dart';
import '../../domain/usecases/get_user_progression_usecase.dart';
import 'user_stats_event.dart';
import 'user_stats_state.dart';

/// Bloc pour gérer les statistiques de l'utilisateur
///
/// Fonctionnalités:
/// - Chargement de la progression
/// - Rafraîchissement (pull-to-refresh)
/// - Cache automatique
class UserStatsBloc extends Bloc<UserStatsEvent, UserStatsState> {
  final GetUserProgressionUseCase _getUserProgressionUseCase;

  UserStatsBloc({
    required GetUserProgressionUseCase getUserProgressionUseCase,
  })  : _getUserProgressionUseCase = getUserProgressionUseCase,
        super(const UserStatsInitial()) {
    on<LoadUserStats>(_onLoadUserStats);
    on<RefreshUserStats>(_onRefreshUserStats);
  }

  // ==========================================================================
  // LOAD USER STATS
  // ==========================================================================

  Future<void> _onLoadUserStats(
    LoadUserStats event,
    Emitter<UserStatsState> emit,
  ) async {
    emit(const UserStatsLoading());

    final result = await _getUserProgressionUseCase();

    result.fold(
      (failure) => emit(UserStatsError(failure.message)),
      (progression) => emit(UserStatsLoaded(progression: progression)),
    );
  }

  // ==========================================================================
  // REFRESH USER STATS
  // ==========================================================================

  Future<void> _onRefreshUserStats(
    RefreshUserStats event,
    Emitter<UserStatsState> emit,
  ) async {
    final currentState = state;

    // Marquer comme en cours de refresh
    if (currentState is UserStatsLoaded) {
      emit(currentState.copyWith(isRefreshing: true));
    }

    // Recharger les données
    final result = await _getUserProgressionUseCase();

    result.fold(
      (failure) {
        // En cas d'erreur, garder les données actuelles
        if (currentState is UserStatsLoaded) {
          emit(currentState.copyWith(isRefreshing: false));
        } else {
          emit(UserStatsError(failure.message));
        }
      },
      (progression) {
        emit(UserStatsLoaded(
          progression: progression,
          isRefreshing: false,
        ));
      },
    );
  }
}
