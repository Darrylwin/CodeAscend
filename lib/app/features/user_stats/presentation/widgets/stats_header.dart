import 'package:flutter/material.dart';
import '../../../../core/themes/colors/app_color.dart';
import '../../../../core/utils/app_extensions.dart';
import '../../domain/entities/user_progression_entity.dart';

/// Widget affichant l'en-tête avec les statistiques globales
class StatsHeader extends StatelessWidget {
  final UserProgressionEntity progression;

  const StatsHeader({
    super.key,
    required this.progression,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDarkMode = theme.brightness == Brightness.dark;

    final gradient =
        isDarkMode ? AppColors.darkPrimaryGradient : AppColors.primaryGradient;
    final primaryColor =
        isDarkMode ? AppColors.darkPrimaryVariant : AppColors.primary;
    final successColor = AppColors.success;
    final errorColor =
        isDarkMode ? AppColors.darkSecondaryVariant : AppColors.error;
    final textColor = isDarkMode ? AppColors.darkTextPrimary : Colors.white;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
      decoration: BoxDecoration(
        gradient: gradient,
        boxShadow: [
          BoxShadow(
            color: primaryColor.withOpacity(0.2),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: SafeArea(
        bottom: false,
        child: Column(
          children: [
            // Titre
            Row(
              children: [
                Icon(
                  Icons.analytics,
                  color: textColor,
                  size: 28,
                ),
                const SizedBox(width: 12),
                Text(
                  'Vue d\'ensemble',
                  style: context.textTheme.headlineSmall?.copyWith(
                    color: textColor,
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),

            const SizedBox(height: 20),

            // Première ligne: Total, Catégories, Moyenne
            Row(
              children: [
                Expanded(
                  child: _buildStatCard(
                    icon: Icons.quiz,
                    label: 'Total',
                    value: '${progression.totalAttempts}',
                    subtitle:
                        'tentative${progression.totalAttempts > 1 ? 's' : ''}',
                    context: context,
                    textColor: textColor,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _buildStatCard(
                    icon: Icons.category,
                    label: 'Catégories',
                    value: '${progression.categoriesMastered}',
                    subtitle:
                        'maîtrisée${progression.categoriesMastered > 1 ? 's' : ''}',
                    context: context,
                    textColor: textColor,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _buildStatCard(
                    icon: Icons.trending_up,
                    label: 'Moyenne',
                    value: '${progression.averageScoreInt}%',
                    subtitle: 'score moyen',
                    context: context,
                    textColor: textColor,
                  ),
                ),
              ],
            ),

            const SizedBox(height: 12),

            // Deuxième ligne: Série actuelle et Tentatives récentes
            Row(
              children: [
                Expanded(
                  child: _buildStreakCard(
                    icon: Icons.local_fire_department,
                    label: 'Série actuelle',
                    value: progression.currentStreak,
                    isActive: progression.hasActiveStreak,
                    context: context,
                    textColor: textColor,
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _buildInfoCard(
                    icon: Icons.history,
                    label: 'Récentes',
                    passed: progression.recentPassedCount,
                    failed: progression.recentFailedCount,
                    context: context,
                    textColor: textColor,
                    successColor: successColor,
                    errorColor: errorColor,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatCard({
    required IconData icon,
    required String label,
    required String value,
    required String subtitle,
    required BuildContext context,
    required Color textColor,
  }) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: textColor.withOpacity(0.15),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: textColor.withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Column(
        children: [
          // Icône
          Container(
            width: 36,
            height: 36,
            decoration: BoxDecoration(
              color: textColor.withOpacity(0.2),
              shape: BoxShape.circle,
            ),
            child: Icon(
              icon,
              color: textColor,
              size: 18,
            ),
          ),

          const SizedBox(height: 6),

          // Label
          Text(
            label,
            style: context.textTheme.bodySmall?.copyWith(
              color: textColor.withOpacity(0.9),
              fontSize: 10,
            ),
          ),

          const SizedBox(height: 2),

          // Valeur
          Text(
            value,
            style: context.textTheme.titleLarge?.copyWith(
              color: textColor,
              fontWeight: FontWeight.bold,
            ),
          ),

          const SizedBox(height: 2),

          // Sous-titre
          Text(
            subtitle,
            style: context.textTheme.bodySmall?.copyWith(
              color: textColor.withOpacity(0.7),
              fontSize: 9,
            ),
            textAlign: TextAlign.center,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ],
      ),
    );
  }

  Widget _buildStreakCard({
    required IconData icon,
    required String label,
    required int value,
    required bool isActive,
    required BuildContext context,
    required Color textColor,
  }) {
    final streakColor = isActive ? Colors.orange : textColor;

    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: isActive
            ? streakColor.withOpacity(0.2)
            : textColor.withOpacity(0.15),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: isActive
              ? streakColor.withOpacity(0.5)
              : textColor.withOpacity(0.3),
          width: isActive ? 2 : 1,
        ),
      ),
      child: Row(
        children: [
          // Icône
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: isActive
                  ? streakColor.withOpacity(0.3)
                  : textColor.withOpacity(0.2),
              shape: BoxShape.circle,
            ),
            child: Icon(
              icon,
              color: isActive ? Colors.orange.shade100 : textColor,
              size: 20,
            ),
          ),

          const SizedBox(width: 12),

          // Texte
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  label,
                  style: context.textTheme.bodySmall?.copyWith(
                    color: textColor.withOpacity(0.9),
                    fontSize: 11,
                  ),
                ),
                const SizedBox(height: 2),
                Row(
                  children: [
                    Text(
                      '$value',
                      style: context.textTheme.headlineSmall?.copyWith(
                        color: textColor,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    if (isActive) ...[
                      const SizedBox(width: 4),
                      const Text(
                        '🔥',
                        style: TextStyle(fontSize: 16),
                      ),
                    ],
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildInfoCard({
    required IconData icon,
    required String label,
    required int passed,
    required int failed,
    required BuildContext context,
    required Color textColor,
    required Color successColor,
    required Color errorColor,
  }) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: textColor.withOpacity(0.15),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: textColor.withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Row(
        children: [
          // Icône
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: textColor.withOpacity(0.2),
              shape: BoxShape.circle,
            ),
            child: Icon(
              icon,
              color: textColor,
              size: 20,
            ),
          ),

          const SizedBox(width: 12),

          // Texte
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  label,
                  style: context.textTheme.bodySmall?.copyWith(
                    color: textColor.withOpacity(0.9),
                    fontSize: 11,
                  ),
                ),
                const SizedBox(height: 2),
                Row(
                  children: [
                    // Réussies
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 6,
                        vertical: 2,
                      ),
                      decoration: BoxDecoration(
                        color: successColor.withOpacity(0.3),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(
                            Icons.check,
                            size: 12,
                            color: textColor,
                          ),
                          const SizedBox(width: 2),
                          Text(
                            '$passed',
                            style: TextStyle(
                              color: textColor,
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                    ),

                    const SizedBox(width: 6),

                    // Échouées
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 6,
                        vertical: 2,
                      ),
                      decoration: BoxDecoration(
                        color: errorColor.withOpacity(0.3),
                        borderRadius: BorderRadius.circular(8),
                      ),
                      child: Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(
                            Icons.close,
                            size: 12,
                            color: textColor,
                          ),
                          const SizedBox(width: 2),
                          Text(
                            '$failed',
                            style: TextStyle(
                              color: textColor,
                              fontSize: 12,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
