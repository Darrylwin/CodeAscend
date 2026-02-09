import 'package:flutter/material.dart';
import '../../../../core/themes/colors/app_color.dart';
import '../../../../core/utils/app_extensions.dart';
import '../../domain/entities/user_progression_entity.dart';

/// Widget affichant la liste des tentatives récentes
class RecentAttemptsList extends StatelessWidget {
  final List<RecentAttemptEntity> attempts;

  const RecentAttemptsList({
    super.key,
    required this.attempts,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: attempts.map((attempt) {
        return _buildAttemptCard(context, attempt);
      }).toList(),
    );
  }

  Widget _buildAttemptCard(BuildContext context, RecentAttemptEntity attempt) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final isDarkMode = theme.brightness == Brightness.dark;

    const successColor = AppColors.success;
    final errorColor =
        isDarkMode ? AppColors.darkSecondaryVariant : AppColors.error;
    final textSecondaryColor = colorScheme.onSurface.withOpacity(0.6);
    final onSurfaceColor = colorScheme.onSurface;

    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 2,
      color: colorScheme.surface,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(
          color: attempt.passed
              ? successColor.withOpacity(0.3)
              : errorColor.withOpacity(0.3),
          width: 1,
        ),
      ),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Row(
          children: [
            // Icône de statut
            Container(
              width: 48,
              height: 48,
              decoration: BoxDecoration(
                color: attempt.passed
                    ? successColor.withOpacity(0.1)
                    : errorColor.withOpacity(0.1),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(
                attempt.passed ? Icons.check_circle : Icons.cancel,
                color: attempt.passed ? successColor : errorColor,
                size: 28,
              ),
            ),

            const SizedBox(width: 16),

            // Infos
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  // Titre du quiz
                  Text(
                    attempt.quizTitle,
                    style: context.textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                      color: onSurfaceColor,
                    ),
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                  ),

                  const SizedBox(height: 6),

                  // Date
                  Row(
                    children: [
                      Icon(
                        Icons.access_time,
                        size: 14,
                        color: textSecondaryColor,
                      ),
                      const SizedBox(width: 4),
                      Text(
                        attempt.formattedDate,
                        style: context.textTheme.bodySmall?.copyWith(
                          color: textSecondaryColor,
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),

            const SizedBox(width: 12),

            // Score
            Column(
              children: [
                Container(
                  padding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 8,
                  ),
                  decoration: BoxDecoration(
                    gradient: attempt.passed
                        ? AppColors.successGradient
                        : LinearGradient(
                            colors: [errorColor, errorColor.withOpacity(0.7)],
                          ),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: Text(
                    '${attempt.scoreInt}%',
                    style: context.textTheme.titleMedium?.copyWith(
                      color: Colors.white,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  attempt.passed ? 'Réussi' : 'Échoué',
                  style: context.textTheme.bodySmall?.copyWith(
                    color: attempt.passed ? successColor : errorColor,
                    fontWeight: FontWeight.w600,
                    fontSize: 10,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
