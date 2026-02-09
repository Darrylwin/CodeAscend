import 'package:flutter/material.dart';
import '../../../../core/themes/colors/app_color.dart';
import '../../../../core/utils/app_extensions.dart';
import '../../domain/entities/attempt_summary_entity.dart';

/// Carte représentant une tentative de quiz
class AttemptCard extends StatelessWidget {
  final AttemptSummaryEntity attempt;
  final VoidCallback onTap;

  const AttemptCard({
    super.key,
    required this.attempt,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final isDarkMode = theme.brightness == Brightness.dark;

    final infoColor =
        isDarkMode ? AppColors.darkPrimaryVariant : AppColors.info;
    final successColor = AppColors.success;
    final errorColor =
        isDarkMode ? AppColors.darkSecondaryVariant : AppColors.secondary;

    return Card(
      margin: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
      elevation: 0,
      color: colorScheme.surface,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(
          color:
              _getBorderColor(colorScheme, infoColor, successColor, errorColor),
          width: 1.5,
        ),
      ),
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header: Badge + Date
              Row(
                children: [
                  // Badge réussite/échec/en cours
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color: _getStatusColor(
                              colorScheme, infoColor, successColor, errorColor)
                          .withOpacity(0.12),
                      borderRadius: BorderRadius.circular(20),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          _getStatusIcon(),
                          size: 16,
                          color: _getStatusColor(
                              colorScheme, infoColor, successColor, errorColor),
                        ),
                        const SizedBox(width: 6),
                        Text(
                          _getStatusLabel(),
                          style: context.textTheme.labelMedium?.copyWith(
                            color: _getStatusColor(colorScheme, infoColor,
                                successColor, errorColor),
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ],
                    ),
                  ),

                  const Spacer(),

                  // Date
                  Row(
                    children: [
                      Icon(
                        Icons.access_time_rounded,
                        size: 14,
                        color: colorScheme.onSurface.withOpacity(0.6),
                      ),
                      const SizedBox(width: 4),
                      Text(
                        attempt.formattedDate,
                        style: context.textTheme.bodySmall?.copyWith(
                          color: colorScheme.onSurface.withOpacity(0.6),
                          fontWeight: FontWeight.w500,
                        ),
                      ),
                    ],
                  ),
                ],
              ),

              const SizedBox(height: 14),

              // Titre du quiz
              Text(
                attempt.quizTitle,
                style: context.textTheme.titleMedium?.copyWith(
                  fontWeight: FontWeight.bold,
                  color: colorScheme.onSurface,
                ),
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
              ),

              const SizedBox(height: 10),

              // Catégorie + Niveau
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: [
                  // Catégorie
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 10,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color: colorScheme.primary.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          Icons.category_rounded,
                          size: 14,
                          color: colorScheme.primary,
                        ),
                        const SizedBox(width: 6),
                        Text(
                          attempt.categoryName,
                          style: context.textTheme.labelSmall?.copyWith(
                            color: colorScheme.primary,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ],
                    ),
                  ),

                  // Niveau
                  Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 10,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      color:
                          _getLevelColor(attempt.level, colorScheme, isDarkMode)
                              .withOpacity(0.1),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          _getLevelIcon(attempt.level),
                          size: 14,
                          color: _getLevelColor(
                              attempt.level, colorScheme, isDarkMode),
                        ),
                        const SizedBox(width: 6),
                        Text(
                          attempt.level.capitalize,
                          style: context.textTheme.labelSmall?.copyWith(
                            color: _getLevelColor(
                                attempt.level, colorScheme, isDarkMode),
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),

              const SizedBox(height: 14),

              // Score avec barre de progression (si terminé) OU Section "En cours"
              if (attempt.isInProgress)
                _buildInProgressSection(context, colorScheme, infoColor)
              else
                _buildCompletedSection(
                    context, colorScheme, successColor, errorColor),

              // Badge "Récent" si moins de 24h et terminé
              if (attempt.isRecent && !attempt.isInProgress)
                Padding(
                  padding: const EdgeInsets.only(top: 10),
                  child: Container(
                    padding: const EdgeInsets.symmetric(
                      horizontal: 10,
                      vertical: 6,
                    ),
                    decoration: BoxDecoration(
                      gradient: LinearGradient(
                        colors: [
                          colorScheme.primary,
                          colorScheme.primary.withOpacity(0.7),
                        ],
                      ),
                      borderRadius: BorderRadius.circular(8),
                      boxShadow: [
                        BoxShadow(
                          color: colorScheme.primary.withOpacity(0.3),
                          blurRadius: 8,
                          offset: const Offset(0, 2),
                        ),
                      ],
                    ),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Icon(
                          Icons.new_releases_rounded,
                          size: 14,
                          color: colorScheme.onPrimary,
                        ),
                        const SizedBox(width: 6),
                        Text(
                          'Nouveau',
                          style: context.textTheme.labelSmall?.copyWith(
                            color: colorScheme.onPrimary,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ],
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }

  /// Section pour quiz en cours
  Widget _buildInProgressSection(
      BuildContext context, ColorScheme colorScheme, Color infoColor) {
    return Container(
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: infoColor.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: infoColor.withOpacity(0.3),
        ),
      ),
      child: Row(
        children: [
          Icon(
            Icons.play_circle_filled_rounded,
            color: infoColor,
            size: 32,
          ),
          const SizedBox(width: 12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Quiz non terminé',
                  style: context.textTheme.titleSmall?.copyWith(
                    fontWeight: FontWeight.w600,
                    color: infoColor,
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  'Cliquez pour continuer',
                  style: context.textTheme.bodySmall?.copyWith(
                    color: colorScheme.onSurface.withOpacity(0.6),
                  ),
                ),
              ],
            ),
          ),
          Icon(
            Icons.arrow_forward_ios_rounded,
            size: 16,
            color: infoColor,
          ),
        ],
      ),
    );
  }

  /// Section pour quiz terminé
  Widget _buildCompletedSection(BuildContext context, ColorScheme colorScheme,
      Color successColor, Color errorColor) {
    final statusColor = attempt.passed ? successColor : errorColor;

    return Row(
      children: [
        // Score
        Text(
          '${attempt.scoreInt}%',
          style: context.textTheme.headlineSmall?.copyWith(
            color: statusColor,
            fontWeight: FontWeight.bold,
          ),
        ),

        const SizedBox(width: 14),

        // Barre de progression
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(10),
                child: LinearProgressIndicator(
                  value: attempt.score / 100,
                  minHeight: 8,
                  backgroundColor: colorScheme.surfaceVariant,
                  valueColor: AlwaysStoppedAnimation<Color>(statusColor),
                ),
              ),
              const SizedBox(height: 6),
              Text(
                attempt.passed
                    ? 'Niveau débloqué ✓'
                    : 'Niveau bloqué (min. 80%)',
                style: context.textTheme.bodySmall?.copyWith(
                  color: colorScheme.onSurface.withOpacity(0.6),
                  fontSize: 10,
                  fontWeight: FontWeight.w500,
                ),
              ),
            ],
          ),
        ),

        const SizedBox(width: 12),

        // Icône de navigation
        Icon(
          Icons.arrow_forward_ios_rounded,
          size: 16,
          color: colorScheme.onSurface.withOpacity(0.6),
        ),
      ],
    );
  }

  Color _getBorderColor(ColorScheme colorScheme, Color infoColor,
      Color successColor, Color errorColor) {
    if (attempt.isInProgress) return infoColor.withOpacity(0.2);
    if (attempt.passed) return successColor.withOpacity(0.2);
    return errorColor.withOpacity(0.2);
  }

  Color _getStatusColor(ColorScheme colorScheme, Color infoColor,
      Color successColor, Color errorColor) {
    if (attempt.isInProgress) return infoColor;
    if (attempt.passed) return successColor;
    return errorColor;
  }

  IconData _getStatusIcon() {
    if (attempt.isInProgress) return Icons.play_circle_outline_rounded;
    if (attempt.passed) return Icons.check_circle_rounded;
    return Icons.cancel_rounded;
  }

  String _getStatusLabel() {
    if (attempt.isInProgress) return 'En cours';
    if (attempt.passed) return 'Réussi';
    return 'Échoué';
  }

  Color _getLevelColor(String level, ColorScheme colorScheme, bool isDarkMode) {
    switch (level.toLowerCase()) {
      case 'debutant':
        return isDarkMode ? AppColors.success : AppColors.levelBeginner;
      case 'intermediaire':
        return isDarkMode
            ? AppColors.darkPrimaryVariant
            : AppColors.levelIntermediate;
      case 'avance':
        return isDarkMode
            ? AppColors.darkSecondaryVariant
            : AppColors.levelAdvanced;
      default:
        return colorScheme.primary;
    }
  }

  IconData _getLevelIcon(String level) {
    switch (level.toLowerCase()) {
      case 'debutant':
        return Icons.looks_one_rounded;
      case 'intermediaire':
        return Icons.looks_two_rounded;
      case 'avance':
        return Icons.looks_3_rounded;
      default:
        return Icons.star_rounded;
    }
  }
}
