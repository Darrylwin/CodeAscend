import 'package:equatable/equatable.dart';

/// Events pour le UserStatsBloc
abstract class UserStatsEvent extends Equatable {
  const UserStatsEvent();

  @override
  List<Object?> get props => [];
}

// ============================================================================
// LOAD USER STATS
// ============================================================================

/// Event: Charger les statistiques de l'utilisateur
class LoadUserStats extends UserStatsEvent {
  const LoadUserStats();
}

// ============================================================================
// REFRESH USER STATS
// ============================================================================

/// Event: Rafraîchir les statistiques (pull-to-refresh)
class RefreshUserStats extends UserStatsEvent {
  const RefreshUserStats();
}
