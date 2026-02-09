import 'package:flutter/material.dart';
import 'package:flutter_svg/flutter_svg.dart';
import '../../../../core/themes/colors/app_color.dart';
import '../../../../core/utils/app_extensions.dart';
import '../../domain/entities/category_entity.dart';

/// Carte réutilisable pour afficher une catégorie dans la liste
class CategoryCard extends StatelessWidget {
  final CategoryEntity category;
  final VoidCallback? onTap;

  const CategoryCard({
    super.key,
    required this.category,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final isDarkMode = theme.brightness == Brightness.dark;

    final primaryColor =
        isDarkMode ? AppColors.darkPrimaryVariant : AppColors.primary;
    final gradient =
        isDarkMode ? AppColors.darkPrimaryGradient : AppColors.primaryGradient;

    // Utiliser le mapping intelligent
    final iconUrl = category.iconUrl ?? category.name.categoryIconUrl;
    final hasIcon = iconUrl.isNotEmpty;

    return Card(
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
      elevation: 4,
      color: colorScheme.surface,
      child: InkWell(
        borderRadius: BorderRadius.circular(12),
        onTap: onTap,
        child: Padding(
          padding: const EdgeInsets.all(12.0),
          child: Row(
            children: [
              // Icone / image
              Container(
                width: 64,
                height: 64,
                padding: hasIcon ? const EdgeInsets.all(8.0) : null,
                decoration: BoxDecoration(
                  gradient: hasIcon ? null : gradient,
                  color: hasIcon ? colorScheme.surface : null,
                  borderRadius: BorderRadius.circular(12),
                  boxShadow: [
                    BoxShadow(
                      color: Colors.black.withOpacity(0.1),
                      blurRadius: 4,
                      offset: const Offset(0, 2),
                    )
                  ],
                ),
                child: hasIcon
                    ? _buildIcon(iconUrl, primaryColor)
                    : Icon(Icons.code, color: colorScheme.onPrimary, size: 36),
              ),
              const SizedBox(width: 12),
              // Texte
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      category.name,
                      style: Theme.of(context).textTheme.titleLarge?.copyWith(
                            fontWeight: FontWeight.bold,
                            color: colorScheme.onSurface,
                          ),
                    ),
                    const SizedBox(height: 6),
                    Text(
                      category.description ?? 'Testez vos connaissances',
                      style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                            color: colorScheme.onSurface.withOpacity(0.7),
                          ),
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                  ],
                ),
              ),
              const SizedBox(width: 8),
              // Chevron pour indiquer qu'on peut cliquer
              Icon(
                Icons.chevron_right,
                color: primaryColor,
                size: 28,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildIcon(String iconUrl, Color primaryColor) {
    // Vérifier si c'est un SVG
    if (iconUrl.endsWith('.svg')) {
      return SvgPicture.network(
        iconUrl,
        fit: BoxFit.contain,
        placeholderBuilder: (context) => Center(
          child: CircularProgressIndicator(
            strokeWidth: 2,
            valueColor: AlwaysStoppedAnimation<Color>(primaryColor),
          ),
        ),
      );
    }

    // Sinon, image normale (PNG, JPG, etc.)
    return Image.network(
      iconUrl,
      fit: BoxFit.contain,
      errorBuilder: (_, __, ___) => Icon(
        Icons.code,
        color: primaryColor,
        size: 36,
      ),
      loadingBuilder: (context, child, loadingProgress) {
        if (loadingProgress == null) return child;
        return Center(
          child: CircularProgressIndicator(
            strokeWidth: 2,
            valueColor: AlwaysStoppedAnimation<Color>(primaryColor),
          ),
        );
      },
    );
  }
}
