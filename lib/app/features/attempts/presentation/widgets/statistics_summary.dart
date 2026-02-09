import 'package:flutter/material.dart';
import '../../../../core/themes/colors/app_color.dart';
import '../../../../core/utils/app_extensions.dart';
import '../../domain/repositories/attempts_repository.dart';

/// Widget affichant les statistiques globales de l'utilisateur
class StatisticsSummary extends StatelessWidget {
  final AttemptStatistics statistics;

  const StatisticsSummary({
    super.key,
    required this.statistics,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isDarkMode = theme.brightness == Brightness.dark;

    final primaryColor =
        isDarkMode ? AppColors.darkPrimaryVariant : AppColors.primary;
    final gradient =
        isDarkMode ? AppColors.darkPrimaryGradient : AppColors.primaryGradient;
    final textColor = isDarkMode ? AppColors.darkTextPrimary : Colors.white;

    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        gradient: gradient,
        boxShadow: [
          BoxShadow(
            color: primaryColor.withOpacity(0.2),
            blurRadius: 12,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Titre compact
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(6),
                decoration: BoxDecoration(
                  color: textColor.withOpacity(0.2),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Icon(
                  Icons.bar_chart_rounded,
                  color: textColor,
                  size: 18,
                ),
              ),
              const SizedBox(width: 8),
              Text(
                'Statistiques',
                style: context.textTheme.titleMedium?.copyWith(
                  color: textColor,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
          ),

          const SizedBox(height: 12),

          // Compact grid: 4 small stats in a single row
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Expanded(
                child: _buildStatCard(
                  icon: Icons.quiz_rounded,
                  label: 'Total',
                  value: '${statistics.totalAttempts}',
                  subtitle: 'tent.',
                  context: context,
                  textColor: textColor,
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: _buildStatCard(
                  icon: Icons.check_circle_rounded,
                  label: 'Réussite',
                  value: '${statistics.successRate.round()}%',
                  subtitle: '${statistics.passedAttempts}',
                  context: context,
                  textColor: textColor,
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: _buildStatCard(
                  icon: Icons.trending_up_rounded,
                  label: 'Moyenne',
                  value: '${statistics.averageScoreInt}%',
                  subtitle: 'score',
                  context: context,
                  textColor: textColor,
                ),
              ),
              const SizedBox(width: 8),
              Expanded(
                child: _buildStatCard(
                  icon: Icons.local_fire_department_rounded,
                  label: 'Série',
                  value: '${statistics.currentStreak}',
                  subtitle: statistics.currentStreak > 0 ? '🔥' : '-',
                  context: context,
                  textColor: textColor,
                  highlight: statistics.currentStreak > 0,
                ),
              ),
            ],
          ),
        ],
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
    bool highlight = false,
  }) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
      decoration: BoxDecoration(
        color: highlight
            ? textColor.withOpacity(0.22)
            : textColor.withOpacity(0.15),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: textColor.withOpacity(highlight ? 0.4 : 0.3),
          width: 1,
        ),
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Icône
          Container(
            width: 32,
            height: 32,
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

          // Valeur
          Text(
            value,
            style: context.textTheme.titleLarge?.copyWith(
              color: textColor,
              fontWeight: FontWeight.bold,
              fontSize: 16,
            ),
          ),

          const SizedBox(height: 2),

          // Label
          Text(
            label,
            style: context.textTheme.bodySmall?.copyWith(
              color: textColor.withOpacity(0.9),
              fontSize: 11,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }
}
