import 'package:flutter/cupertino.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/utils/app_extensions.dart';
import '../../../../core/utils/route_observer.dart';
import '../bloc/attempts_bloc.dart';
import '../bloc/attempts_event.dart';
import '../bloc/attempts_state.dart';
import '../widgets/attempt_card.dart';
import '../widgets/statistics_summary.dart';
import '../widgets/filter_chips.dart';

class AttemptsHistoryPage extends StatefulWidget {
  const AttemptsHistoryPage({super.key});

  @override
  State<AttemptsHistoryPage> createState() => _AttemptsHistoryPageState();
}

class _AttemptsHistoryPageState extends State<AttemptsHistoryPage>
    with RouteAware {
  final _searchController = TextEditingController();
  bool _showSearch = false;
  bool _initialized = false;
  bool _isSubscribed = false;

  @override
  void initState() {
    super.initState();
    // Un seul point d'entrée : refresh à chaque ouverture de la page
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!_initialized && mounted) {
        _initialized = true;
        debugPrint('📥 AttemptsHistoryPage: refresh initial');
        context.read<AttemptsBloc>().add(const RefreshAttempts());
      }
    });
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    // Souscription RouteObserver uniquement — pas de chargement ici
    if (!_isSubscribed) {
      final modalRoute = ModalRoute.of(context);
      if (modalRoute is PageRoute) {
        routeObserver.subscribe(this, modalRoute);
        _isSubscribed = true;
      }
    }
  }

  @override
  void dispose() {
    routeObserver.unsubscribe(this);
    _searchController.dispose();
    super.dispose();
  }

  @override
  void didPopNext() {
    // Retour depuis une sous-page (ex: quiz review) → refresh
    debugPrint('🔄 AttemptsHistoryPage: retour détecté, refresh');
    context.read<AttemptsBloc>().add(const RefreshAttempts());
  }

  void _toggleSearch() {
    setState(() {
      _showSearch = !_showSearch;
      if (!_showSearch) {
        _searchController.clear();
        context.read<AttemptsBloc>().add(const ClearSearch());
      }
    });
  }

  void _showSortMenu() {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    showModalBottomSheet(
      context: context,
      backgroundColor: theme.cardColor,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(20)),
      ),
      builder: (context) {
        return Container(
          padding: const EdgeInsets.all(20),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: colorScheme.primary.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child:
                        Icon(Icons.sort, color: colorScheme.primary, size: 20),
                  ),
                  const SizedBox(width: 12),
                  Text(
                    'Trier par',
                    style: context.textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: colorScheme.onSurface,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 20),
              _buildSortOption(
                  icon: Icons.calendar_today,
                  title: 'Date (Plus récent)',
                  sort: AttemptSort.dateDesc),
              _buildSortOption(
                  icon: Icons.calendar_today_outlined,
                  title: 'Date (Plus ancien)',
                  sort: AttemptSort.dateAsc),
              _buildSortOption(
                  icon: Icons.trending_up,
                  title: 'Score (Plus élevé)',
                  sort: AttemptSort.scoreDesc),
              _buildSortOption(
                  icon: Icons.trending_down,
                  title: 'Score (Plus faible)',
                  sort: AttemptSort.scoreAsc),
              const SizedBox(height: 8),
            ],
          ),
        );
      },
    );
  }

  Widget _buildSortOption({
    required IconData icon,
    required String title,
    required AttemptSort sort,
  }) {
    final colorScheme = Theme.of(context).colorScheme;
    return ListTile(
      contentPadding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      leading: Container(
        padding: const EdgeInsets.all(8),
        decoration: BoxDecoration(
          color: colorScheme.primary.withOpacity(0.1),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Icon(icon, color: colorScheme.primary, size: 20),
      ),
      title: Text(title,
          style: TextStyle(
              fontWeight: FontWeight.w500, color: colorScheme.onSurface)),
      onTap: () {
        context.read<AttemptsBloc>().add(SortAttempts(sort));
        Navigator.pop(context);
      },
    );
  }

  @override
  Widget build(BuildContext context) {
    final colorScheme = Theme.of(context).colorScheme;
    final primaryColor = colorScheme.primary;
    final onPrimaryColor = colorScheme.onPrimary;

    return Scaffold(
      backgroundColor: colorScheme.background,
      appBar: AppBar(
        title: _showSearch
            ? TextField(
                controller: _searchController,
                autofocus: true,
                style: TextStyle(color: onPrimaryColor),
                decoration: InputDecoration(
                  hintText: 'Rechercher...',
                  hintStyle: TextStyle(color: onPrimaryColor.withOpacity(0.7)),
                  border: InputBorder.none,
                ),
                onChanged: (query) {
                  context.read<AttemptsBloc>().add(SearchAttempts(query));
                },
              )
            : const Text('Mon Historique'),
        backgroundColor: primaryColor,
        foregroundColor: onPrimaryColor,
        elevation: 0,
        actions: [
          IconButton(
            icon: Icon(_showSearch ? Icons.close : Icons.search),
            onPressed: _toggleSearch,
          ),
          IconButton(
            icon: const Icon(Icons.sort),
            onPressed: _showSortMenu,
          ),
        ],
      ),
      body: BlocBuilder<AttemptsBloc, AttemptsState>(
        builder: (context, state) {
          if (state is AttemptsLoading) {
            return Center(
              child: Image.asset(
                'assets/animations/loading.gif',
                width: 64,
                height: 64,
                fit: BoxFit.contain,
                color: primaryColor,
              ),
            );
          }
          if (state is AttemptsError) {
            return _buildErrorState(state.message);
          }
          if (state is AttemptsLoaded) {
            return _buildLoadedState(state);
          }
          return const SizedBox.shrink();
        },
      ),
    );
  }

  Widget _buildErrorState(String message) {
    final colorScheme = Theme.of(context).colorScheme;
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: const EdgeInsets.all(20),
              decoration: BoxDecoration(
                color: colorScheme.error.withOpacity(0.1),
                shape: BoxShape.circle,
              ),
              child:
                  Icon(Icons.error_outline, size: 64, color: colorScheme.error),
            ),
            const SizedBox(height: 24),
            Text('Erreur',
                style: context.textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold, color: colorScheme.onSurface)),
            const SizedBox(height: 8),
            Text(message,
                textAlign: TextAlign.center,
                style: context.textTheme.bodyMedium
                    ?.copyWith(color: colorScheme.onSurface.withOpacity(0.7))),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: () =>
                  context.read<AttemptsBloc>().add(const RefreshAttempts()),
              icon: const Icon(Icons.refresh),
              label: const Text('Réessayer'),
              style: ElevatedButton.styleFrom(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 24, vertical: 14)),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLoadedState(AttemptsLoaded state) {
    final primaryColor = Theme.of(context).colorScheme.primary;

    if (state.hasNoAttempts) return _buildEmptyState();

    return RefreshIndicator(
      onRefresh: () async {
        context.read<AttemptsBloc>().add(const RefreshAttempts());
        await Future.delayed(const Duration(milliseconds: 500));
      },
      color: primaryColor,
      child: Column(
        children: [
          StatisticsSummary(statistics: state.statistics),
          FilterChips(
            currentFilter: state.currentFilter,
            onFilterChanged: (filter) =>
                context.read<AttemptsBloc>().add(FilterAttempts(filter)),
          ),
          Expanded(
            child: state.isEmpty
                ? _buildNoResultsState()
                : ListView.builder(
                    padding: const EdgeInsets.only(bottom: 16, top: 8),
                    itemCount: state.filteredAttempts.length,
                    itemBuilder: (context, index) {
                      final attempt = state.filteredAttempts[index];
                      return AttemptCard(
                        attempt: attempt,
                        onTap: () {
                          if (attempt.isInProgress) {
                            if (attempt.quizId.isEmpty) {
                              context.showErrorSnackBar(
                                  'Impossible de reprendre ce quiz. Données manquantes.');
                              return;
                            }
                            context.push(
                                '/quiz/${attempt.quizId}?restore=true&from=history');
                          } else {
                            context.push(
                                '/attempt/${attempt.id}/review?from=history');
                          }
                        },
                      );
                    },
                  ),
          ),
        ],
      ),
    );
  }

  Widget _buildEmptyState() {
    final colorScheme = Theme.of(context).colorScheme;
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                  color: colorScheme.surfaceVariant, shape: BoxShape.circle),
              child: Icon(CupertinoIcons.question_circle,
                  size: 80, color: colorScheme.onSurfaceVariant),
            ),
            const SizedBox(height: 24),
            Text('Aucune tentative',
                style: context.textTheme.headlineSmall?.copyWith(
                    fontWeight: FontWeight.bold, color: colorScheme.onSurface)),
            const SizedBox(height: 8),
            Text('Passez votre premier quiz pour voir votre historique ici',
                textAlign: TextAlign.center,
                style: context.textTheme.bodyMedium
                    ?.copyWith(color: colorScheme.onSurface.withOpacity(0.7))),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: () => context.go('/home'),
              icon: const Icon(Icons.home),
              label: const Text('Découvrir les quiz'),
              style: ElevatedButton.styleFrom(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 24, vertical: 14)),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildNoResultsState() {
    final colorScheme = Theme.of(context).colorScheme;
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                  color: colorScheme.surfaceVariant, shape: BoxShape.circle),
              child: Icon(Icons.search_off,
                  size: 64, color: colorScheme.onSurfaceVariant),
            ),
            const SizedBox(height: 20),
            Text('Aucun résultat',
                style: context.textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold, color: colorScheme.onSurface)),
            const SizedBox(height: 8),
            Text('Aucune tentative ne correspond à vos filtres',
                textAlign: TextAlign.center,
                style: context.textTheme.bodyMedium
                    ?.copyWith(color: colorScheme.onSurface.withOpacity(0.7))),
            const SizedBox(height: 20),
            TextButton.icon(
              onPressed: () {
                context
                    .read<AttemptsBloc>()
                    .add(const FilterAttempts(AttemptFilter.all));
                context.read<AttemptsBloc>().add(const ClearSearch());
                if (_showSearch) _toggleSearch();
              },
              icon: const Icon(Icons.clear_all),
              label: const Text('Réinitialiser les filtres'),
            ),
          ],
        ),
      ),
    );
  }
}
