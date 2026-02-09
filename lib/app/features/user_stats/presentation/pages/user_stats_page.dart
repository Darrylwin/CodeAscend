import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/themes/colors/app_color.dart';
import '../../../../core/utils/app_extensions.dart';
import '../bloc/user_stats_bloc.dart';
import '../bloc/user_stats_event.dart';
import '../bloc/user_stats_state.dart';
import '../widgets/stats_header.dart';
import '../widgets/recent_attempts_list.dart';

/// Page affichant les statistiques de l'utilisateur
class UserStatsPage extends StatefulWidget {
  const UserStatsPage({super.key});

  @override
  State<UserStatsPage> createState() => _UserStatsPageState();
}

class _UserStatsPageState extends State<UserStatsPage> {
  @override
  void initState() {
    super.initState();

    // Charger les stats automatiquement
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final userStatsBloc = context.read<UserStatsBloc>();
      // Vérifier si les données sont déjà chargées
      if (userStatsBloc.state is! UserStatsLoaded) {
        userStatsBloc.add(const LoadUserStats());
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final isDarkMode = theme.brightness == Brightness.dark;

    final primaryColor =
        isDarkMode ? AppColors.darkPrimaryVariant : AppColors.primary;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Mes Statistiques'),
        backgroundColor: primaryColor,
        foregroundColor: colorScheme.onPrimary,
      ),
      backgroundColor: colorScheme.background,
      body: BlocConsumer<UserStatsBloc, UserStatsState>(
        listener: (context, state) {
          // Gérer les changements d'état si nécessaire
        },
        builder: (context, state) {
          if (state is UserStatsLoading) {
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

          if (state is UserStatsError) {
            return _buildErrorState(context, state.message);
          }

          if (state is UserStatsLoaded) {
            return _buildLoadedState(context, state);
          }

          // État initial ou autres états
          return Center(
            child: Image.asset(
              'assets/animations/loading.gif',
              width: 64,
              height: 64,
              fit: BoxFit.contain,
              color: primaryColor,
            ),
          );
        },
      ),
    );
  }

  Widget _buildErrorState(BuildContext context, String message) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final isDarkMode = theme.brightness == Brightness.dark;

    final errorColor =
        isDarkMode ? AppColors.darkSecondaryVariant : AppColors.error;
    final onSurfaceColor = colorScheme.onSurface;
    final textSecondaryColor =
        isDarkMode ? AppColors.darkTextSecondary : AppColors.textSecondary;

    return Center(
      child: Padding(
        padding: const EdgeInsets.all(24.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.error_outline,
              size: 80,
              color: errorColor,
            ),
            const SizedBox(height: 16),
            Text(
              'Erreur',
              style: context.textTheme.headlineSmall?.copyWith(
                fontWeight: FontWeight.bold,
                color: onSurfaceColor,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              message,
              textAlign: TextAlign.center,
              style: context.textTheme.bodyMedium?.copyWith(
                color: textSecondaryColor,
              ),
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: () {
                context.read<UserStatsBloc>().add(const LoadUserStats());
              },
              icon: const Icon(Icons.refresh),
              label: const Text('Réessayer'),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildLoadedState(BuildContext context, UserStatsLoaded state) {
    final progression = state.progression;
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    if (!progression.hasAttempts) {
      return _buildEmptyState(context);
    }

    return RefreshIndicator(
      onRefresh: () async {
        context.read<UserStatsBloc>().add(const RefreshUserStats());
        await Future.delayed(const Duration(milliseconds: 500));
      },
      color: colorScheme.primary,
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Header avec stats globales
            StatsHeader(progression: progression),

            const SizedBox(height: 24),

            // Tentatives récentes
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Tentatives Récentes',
                    style: context.textTheme.titleLarge?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: colorScheme.onSurface,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Text(
                    '${progression.recentAttempts.length} dernière${progression.recentAttempts.length > 1 ? 's' : ''}',
                    style: context.textTheme.bodyMedium?.copyWith(
                      color: colorScheme.onSurface.withOpacity(0.6),
                    ),
                  ),
                  const SizedBox(height: 12),
                  if (progression.recentAttempts.isNotEmpty)
                    RecentAttemptsList(attempts: progression.recentAttempts)
                  else
                    Center(
                      child: Padding(
                        padding: const EdgeInsets.all(32.0),
                        child: Text(
                          'Aucune tentative récente',
                          style: context.textTheme.bodyLarge?.copyWith(
                            color: colorScheme.onSurface.withOpacity(0.6),
                          ),
                        ),
                      ),
                    ),
                ],
              ),
            ),

            const SizedBox(height: 24),

            // Indicateur de refresh
            if (state.isRefreshing)
              Container(
                padding: const EdgeInsets.all(16),
                child: Center(
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      SizedBox(
                        width: 16,
                        height: 16,
                        child: CircularProgressIndicator(
                          strokeWidth: 2,
                          color: colorScheme.primary,
                        ),
                      ),
                      const SizedBox(width: 8),
                      Text(
                        'Actualisation...',
                        style: TextStyle(
                          color: colorScheme.onSurface,
                        ),
                      ),
                    ],
                  ),
                ),
              ),

            const SizedBox(height: 80), // Padding pour BottomNav
          ],
        ),
      ),
    );
  }

  Widget _buildEmptyState(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final isDarkMode = theme.brightness == Brightness.dark;

    final onSurfaceColor = colorScheme.onSurface;
    final textSecondaryColor = colorScheme.onSurface.withOpacity(0.6);
    final greyColor = isDarkMode ? AppColors.grey600 : AppColors.grey400;

    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.bar_chart_outlined,
              size: 100,
              color: greyColor,
            ),
            const SizedBox(height: 24),
            Text(
              'Aucune statistique',
              style: context.textTheme.headlineSmall?.copyWith(
                fontWeight: FontWeight.bold,
                color: onSurfaceColor,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Commencez à passer des quiz pour voir vos statistiques',
              textAlign: TextAlign.center,
              style: context.textTheme.bodyMedium?.copyWith(
                color: textSecondaryColor,
              ),
            ),
            const SizedBox(height: 24),
            ElevatedButton.icon(
              onPressed: () {
                context.go('/home');
              },
              icon: const Icon(Icons.home),
              label: const Text('Découvrir les quiz'),
            ),
          ],
        ),
      ),
    );
  }
}
