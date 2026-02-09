import 'package:equatable/equatable.dart';
import '../../domain/entities/user_progression_entity.dart';

/// States pour le UserStatsBloc
abstract class UserStatsState extends Equatable {
  const UserStatsState();

  @override
  List<Object?> get props => [];
}

// ============================================================================
// INITIAL
// ============================================================================

/// State initial
class UserStatsInitial extends UserStatsState {
  const UserStatsInitial();
}

// ============================================================================
// LOADING
// ============================================================================

/// State: Chargement en cours
class UserStatsLoading extends UserStatsState {
  const UserStatsLoading();
}

// ============================================================================
// LOADED
// ============================================================================

/// State: Statistiques chargées avec succès
class UserStatsLoaded extends UserStatsState {
  final UserProgressionEntity progression;
  final bool isRefreshing;

  const UserStatsLoaded({
    required this.progression,
    this.isRefreshing = false,
  });

  @override
  List<Object?> get props => [progression, isRefreshing];

  /// CopyWith pour créer une nouvelle instance
  UserStatsLoaded copyWith({
    UserProgressionEntity? progression,
    bool? isRefreshing,
  }) {
    return UserStatsLoaded(
      progression: progression ?? this.progression,
      isRefreshing: isRefreshing ?? this.isRefreshing,
    );
  }
}

// ============================================================================
// ERROR
// ============================================================================

/// State: Erreur lors du chargement
class UserStatsError extends UserStatsState {
  final String message;

  const UserStatsError(this.message);

  @override
  List<Object?> get props => [message];
}
