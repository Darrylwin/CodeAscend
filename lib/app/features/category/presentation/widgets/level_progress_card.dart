import 'package:flutter/material.dart';
import '../../../../core/themes/colors/app_color.dart';
import '../../../../core/utils/app_extensions.dart';

/// Carte améliorée pour afficher un niveau avec progression
class LevelProgressCard extends StatelessWidget {
  final String title;
  final String level; // 'debutant' | 'intermediaire' | 'avance'
  final bool accessible;
  final int attempts;
  final double? bestScore;
  final bool passed;
  final bool inProgress;
  final VoidCallback? onStart;

  const LevelProgressCard({
    super.key,
    required this.title,
    required this.level,
    required this.accessible,
    this.attempts = 0,
    this.bestScore,
    this.passed = false,
    this.inProgress = false,
    this.onStart,
  });

  Color _getLevelColor(BuildContext context) {
    final theme = Theme.of(context);
    final isDarkMode = theme.brightness == Brightness.dark;

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
        return Theme.of(context).colorScheme.primary;
    }
  }

  Color _getStatusColor(BuildContext context) {
    final levelColor = _getLevelColor(context);

    if (inProgress) return AppColors.info;
    if (passed) return AppColors.success;
    if (accessible) return levelColor;

    final theme = Theme.of(context);
    final isDarkMode = theme.brightness == Brightness.dark;
    return isDarkMode ? AppColors.grey600 : AppColors.locked;
  }

  IconData get _statusIcon {
    if (inProgress) return Icons.play_circle_filled;
    if (passed) return Icons.check_circle;
    if (accessible) return Icons.play_circle_outline;
    return Icons.lock;
  }

  String get _buttonText {
    if (!accessible) return 'Bloqué';
    if (inProgress) return 'Continuer';
    if (attempts > 0) return 'Réessayer';
    return 'Commencer';
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final isDarkMode = theme.brightness == Brightness.dark;

    final levelColor = _getLevelColor(context);
    final statusColor = _getStatusColor(context);
    final warningColor = isDarkMode ? AppColors.warning : Color(0xFFFF9800);

    return Card(
      elevation: 2,
      color: colorScheme.surface,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(
          color: statusColor.withOpacity(0.3),
          width: 1.5,
        ),
      ),
      child: InkWell(
        borderRadius: BorderRadius.circular(16),
        onTap: accessible ? onStart : null,
        child: Padding(
          padding: const EdgeInsets.all(14.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Header compact
              Row(
                children: [
                  // Icône réduite
                  Container(
                    width: 40,
                    height: 40,
                    decoration: BoxDecoration(
                      color: statusColor.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(10),
                    ),
                    child: Icon(
                      _statusIcon,
                      color: statusColor,
                      size: 24,
                    ),
                  ),

                  const SizedBox(width: 12),

                  // Titre simplifié
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          title,
                          style: theme.textTheme.titleMedium?.copyWith(
                            fontWeight: FontWeight.bold,
                            color: accessible
                                ? colorScheme.onSurface
                                : colorScheme.onSurface.withOpacity(0.4),
                          ),
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                        ),
                        const SizedBox(height: 4),
                        // Badge de statut unique
                        _buildStatusBadge(context, levelColor, statusColor),
                      ],
                    ),
                  ),

                  const SizedBox(width: 8),

                  // Bouton d'action compact
                  _buildActionButton(context, statusColor),
                ],
              ),

              // Stats compactes (uniquement si pertinent)
              if (accessible &&
                  !inProgress &&
                  (attempts > 0 || bestScore != null)) ...[
                const SizedBox(height: 12),
                Container(
                  padding:
                      const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
                  decoration: BoxDecoration(
                    color: colorScheme.surfaceVariant.withOpacity(0.5),
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      if (attempts > 0)
                        _buildCompactStat(
                          context,
                          icon: Icons.replay,
                          value: '$attempts',
                          label: 'essai${attempts > 1 ? 's' : ''}',
                          levelColor: levelColor,
                        ),
                      if (bestScore != null && attempts > 0)
                        Container(
                          width: 1,
                          height: 24,
                          color: colorScheme.outline.withOpacity(0.3),
                        ),
                      if (bestScore != null)
                        _buildCompactStat(
                          context,
                          icon: null,
                          value: '${bestScore!.round()}%',
                          label: 'meilleur',
                          levelColor: levelColor,
                        ),
                    ],
                  ),
                ),
              ],

              // Message d'info (seulement si nécessaire)
              if (!accessible && !inProgress) ...[
                const SizedBox(height: 12),
                Row(
                  children: [
                    Icon(
                      Icons.info_outline,
                      size: 16,
                      color: warningColor,
                    ),
                    const SizedBox(width: 6),
                    Expanded(
                      child: Text(
                        'Réussissez le niveau précédent (≥80%)',
                        style: theme.textTheme.bodySmall?.copyWith(
                          color: warningColor,
                          fontSize: 11,
                        ),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ],
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStatusBadge(
      BuildContext context, Color levelColor, Color statusColor) {
    String badgeText;
    Color badgeColor;
    IconData? badgeIcon;

    if (inProgress) {
      badgeText = 'En cours';
      badgeColor = AppColors.info;
      badgeIcon = Icons.access_time;
    } else if (passed) {
      badgeText = 'Validé';
      badgeColor = AppColors.success;
      badgeIcon = Icons.check;
    } else {
      badgeText = level.capitalize;
      badgeColor = levelColor;
      badgeIcon = null;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 3),
      decoration: BoxDecoration(
        color: badgeColor.withOpacity(0.12),
        borderRadius: BorderRadius.circular(6),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (badgeIcon != null) ...[
            Icon(badgeIcon, size: 10, color: badgeColor),
            const SizedBox(width: 4),
          ],
          Text(
            badgeText,
            style: context.textTheme.labelSmall?.copyWith(
              color: badgeColor,
              fontWeight: FontWeight.w600,
              fontSize: 11,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActionButton(BuildContext context, Color statusColor) {
    final theme = Theme.of(context);
    final isDarkMode = theme.brightness == Brightness.dark;
    final lockedColor = isDarkMode ? AppColors.grey600 : AppColors.locked;

    if (!accessible) {
      return Container(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
        decoration: BoxDecoration(
          color: lockedColor.withOpacity(0.1),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Icon(Icons.lock, size: 16, color: lockedColor),
      );
    }

    return ElevatedButton(
      onPressed: onStart,
      style: ElevatedButton.styleFrom(
        backgroundColor: statusColor,
        foregroundColor: Colors.white,
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        minimumSize: Size.zero,
        tapTargetSize: MaterialTapTargetSize.shrinkWrap,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(8),
        ),
        elevation: 0,
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            inProgress
                ? Icons.play_arrow
                : (attempts > 0 ? Icons.replay : Icons.arrow_forward),
            size: 16,
          ),
          const SizedBox(width: 4),
          Text(
            _buttonText,
            style: const TextStyle(
              fontWeight: FontWeight.w600,
              fontSize: 13,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildCompactStat(
    BuildContext context, {
    required IconData? icon,
    required String value,
    required String label,
    required Color levelColor,
  }) {
    final colorScheme = Theme.of(context).colorScheme;

    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        if (icon != null) Icon(icon, size: 14, color: levelColor),
        const SizedBox(width: 6),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisSize: MainAxisSize.min,
          children: [
            Text(
              value,
              style: context.textTheme.labelLarge?.copyWith(
                fontWeight: FontWeight.bold,
                color: levelColor,
                fontSize: 13,
              ),
            ),
            Text(
              label,
              style: context.textTheme.labelSmall?.copyWith(
                color: colorScheme.onSurface.withOpacity(0.5),
                fontSize: 10,
              ),
            ),
          ],
        ),
      ],
    );
  }
}
