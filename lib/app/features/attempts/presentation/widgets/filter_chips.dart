import 'package:flutter/material.dart';
import '../../../../core/themes/colors/app_color.dart';
import '../../../../core/utils/app_extensions.dart';
import '../bloc/attempts_event.dart';

/// Widget affichant les chips de filtrage
///
/// Filtres disponibles:
/// - Toutes les tentatives
/// - En cours
/// - Seulement les réussies
/// - Seulement les échouées
class FilterChips extends StatelessWidget {
  final AttemptFilter currentFilter;
  final ValueChanged<AttemptFilter> onFilterChanged;

  const FilterChips({
    super.key,
    required this.currentFilter,
    required this.onFilterChanged,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
      child: Row(
        children: [
          // Label
          Text(
            'Filtrer:',
            style: context.textTheme.labelLarge?.copyWith(
              color: colorScheme.onSurface.withOpacity(0.7),
              fontWeight: FontWeight.w600,
            ),
          ),

          const SizedBox(width: 12),

          // Chips
          Expanded(
            child: SingleChildScrollView(
              scrollDirection: Axis.horizontal,
              child: Row(
                children: [
                  _buildFilterChip(
                    label: 'Toutes',
                    icon: Icons.list,
                    filter: AttemptFilter.all,
                    context: context,
                  ),
                  const SizedBox(width: 8),
                  _buildFilterChip(
                    label: 'En cours',
                    icon: Icons.play_circle_outline,
                    filter: AttemptFilter.inProgress,
                    context: context,
                  ),
                  const SizedBox(width: 8),
                  _buildFilterChip(
                    label: 'Réussies',
                    icon: Icons.check_circle,
                    filter: AttemptFilter.passed,
                    context: context,
                  ),
                  const SizedBox(width: 8),
                  _buildFilterChip(
                    label: 'Échouées',
                    icon: Icons.cancel,
                    filter: AttemptFilter.failed,
                    context: context,
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildFilterChip({
    required String label,
    required IconData icon,
    required AttemptFilter filter,
    required BuildContext context,
  }) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final isSelected = currentFilter == filter;
    final filterColor = _getFilterColor(filter, theme);

    return FilterChip(
      label: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            icon,
            size: 16,
            color: isSelected ? colorScheme.onPrimary : filterColor,
          ),
          const SizedBox(width: 6),
          Text(
            label,
            style: TextStyle(
              fontSize: 13,
              fontWeight: isSelected ? FontWeight.w600 : FontWeight.w500,
              color: isSelected ? colorScheme.onPrimary : colorScheme.onSurface,
            ),
          ),
        ],
      ),
      selected: isSelected,
      onSelected: (selected) {
        if (selected) {
          onFilterChanged(filter);
        }
      },
      backgroundColor: colorScheme.surface,
      selectedColor: filterColor,
      checkmarkColor: colorScheme.onPrimary,
      labelStyle: TextStyle(
        color: isSelected ? colorScheme.onPrimary : colorScheme.onSurface,
      ),
      side: BorderSide(
        color: isSelected ? filterColor : filterColor.withOpacity(0.3),
        width: 1.5,
      ),
      elevation: isSelected ? 2 : 0,
      shadowColor: filterColor.withOpacity(0.3),
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(20),
      ),
    );
  }

  Color _getFilterColor(AttemptFilter filter, ThemeData theme) {
    final isDarkMode = theme.brightness == Brightness.dark;

    switch (filter) {
      case AttemptFilter.all:
        return isDarkMode ? AppColors.darkPrimaryVariant : AppColors.primary;
      case AttemptFilter.inProgress:
        return isDarkMode ? AppColors.darkPrimaryVariant : AppColors.info;
      case AttemptFilter.passed:
        return AppColors.success;
      case AttemptFilter.failed:
        return isDarkMode
            ? AppColors.darkSecondaryVariant
            : AppColors.secondary;
    }
  }
}
