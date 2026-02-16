import 'package:equatable/equatable.dart';

abstract class AttemptsEvent extends Equatable {
  const AttemptsEvent();

  @override
  List<Object?> get props => [];
}

class LoadAttempts extends AttemptsEvent {
  /// Si true, force le rechargement même si des données sont déjà présentes.
  final bool forceLoad;
  const LoadAttempts({this.forceLoad = false});

  @override
  List<Object?> get props => [forceLoad];
}

class RefreshAttempts extends AttemptsEvent {
  const RefreshAttempts();
}

class FilterAttempts extends AttemptsEvent {
  final AttemptFilter filter;
  const FilterAttempts(this.filter);

  @override
  List<Object?> get props => [filter];
}

enum AttemptFilter { all, inProgress, passed, failed }

class SortAttempts extends AttemptsEvent {
  final AttemptSort sortBy;
  const SortAttempts(this.sortBy);

  @override
  List<Object?> get props => [sortBy];
}

enum AttemptSort { dateDesc, dateAsc, scoreDesc, scoreAsc, categoryAsc }

class SearchAttempts extends AttemptsEvent {
  final String query;
  const SearchAttempts(this.query);

  @override
  List<Object?> get props => [query];
}

class ClearSearch extends AttemptsEvent {
  const ClearSearch();
}

/// Invalide le cache des tentatives.
/// Si [forceReload] est true, recharge immédiatement depuis l'API.
class InvalidateAttempts extends AttemptsEvent {
  final bool forceReload;
  const InvalidateAttempts({this.forceReload = false});

  @override
  List<Object?> get props => [forceReload];
}