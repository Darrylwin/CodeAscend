import 'package:flutter/material.dart';

/// Palette de couleurs de l'application
class AppColors {
  AppColors._();

  // ============================================================================
  // COULEURS PRINCIPALES
  // ============================================================================

  static const Color primary = Color(0xFF0D0B9D); // Bleu profond
  static const Color primaryDark = Color(0xFF0A0875);
  static const Color primaryLight = Color(0xFF4845FF);

  static const Color secondary = Color(0xFFC9353F); // Rouge/Rose
  static const Color secondaryDark = Color(0xFFA02930);
  static const Color secondaryLight =
      Color(0xFFE57373); // Plus clair pour sombre

  // Accent
  static const Color accent = Color(0xFF292621); // Noir chaud
  static const Color accentLight = Color(0xFF5C5C5C);

  // ============================================================================
  // COULEURS DE STATUT
  // ============================================================================

  static const Color success = Color(0xFF4CAF50); // Vert - Quiz réussi
  static const Color error =
      Color(0xFFC9353F); // Rouge - Quiz échoué (secondary)
  static const Color warning = Color(0xFFFF9800); // Orange - Attention
  static const Color info = Color(0xFF0D0B9D); // Bleu profond - Info

  // ============================================================================
  // COULEURS POUR THÈME SOMBRE
  // ============================================================================

  static const Color darkBackground =
      Color(0xFF121212); // Fond principal sombre
  static const Color darkSurface = Color(0xFF1E1E1E); // Surfaces sombres
  static const Color darkSurfaceElevated =
      Color(0xFF2D2D2D); // Surfaces élevées
  static const Color darkCard = Color(0xFF242424); // Cartes sombres
  static const Color darkDivider = Color(0xFF383838); // Séparateurs sombres
  static const Color darkBorder = Color(0xFF404040); // Bordures sombres
  static const Color darkTextPrimary =
      Color(0xFFF5F5F5); // Texte principal sombre
  static const Color darkTextSecondary =
      Color(0xFFB0B0B0); // Texte secondaire sombre
  static const Color darkTextDisabled =
      Color(0xFF6D6D6D); // Texte désactivé sombre
  static const Color darkPrimaryVariant =
      Color(0xFF3A36B3); // Variante primaire pour sombre - BLEU
  static const Color darkSecondaryVariant =
      Color(0xFFE64A4A); // Variante secondaire pour sombre - ROUGE CLAIR

  // ============================================================================
  // NIVEAUX DE QUIZ (badges)
  // ============================================================================

  static const Color levelBeginner = Color(0xFF4CAF50); // Vert
  static const Color levelIntermediate = Color(0xFF0D0B9D); // Bleu profond
  static const Color levelAdvanced = Color(0xFFC9353F); // Rouge/Rose

  // ============================================================================
  // NEUTRALS (gris)
  // ============================================================================

  static const Color black = Color(0xFF000000);
  static const Color white = Color(0xFFFFFFFF);

  static const Color grey50 = Color(0xFFFAFAFA);
  static const Color grey100 = Color(0xFFF5F5F5);
  static const Color grey200 = Color(0xFFEEEEEE);
  static const Color grey300 = Color(0xFFE0E0E0);
  static const Color grey400 = Color(0xFFBDBDBD);
  static const Color grey500 = Color(0xFF9E9E9E);
  static const Color grey600 = Color(0xFF757575);
  static const Color grey700 = Color(0xFF616161);
  static const Color grey800 = Color(0xFF424242);
  static const Color grey900 = Color(0xFF212121);

  // ============================================================================
  // BACKGROUNDS
  // ============================================================================

  static const Color background = Color(0xFFF5EDE2); // Beige clair
  static const Color surface = Color(0xFFFFFFFF);
  static const Color scaffoldBackground = Color(0xFFF5EDE2);

  // ============================================================================
  // TEXTS
  // ============================================================================

  static const Color textPrimary = Color(0xFF292621); // Noir chaud
  static const Color textSecondary = Color(0xFF5C5C5C);
  static const Color textDisabled = Color(0xFFBDBDBD);
  static const Color textOnPrimary = Color(0xFFFFFFFF);

  // ============================================================================
  // DIVIDERS & BORDERS
  // ============================================================================

  static const Color divider = Color(0xFFE0E0E0);
  static const Color border = Color(0xFFE0E0E0);

  // ============================================================================
  // SPECIAL (locked, disabled, etc.)
  // ============================================================================

  static const Color locked = Color(0xFFBDBDBD); // Niveau bloqué
  static const Color disabled = Color(0xFFE0E0E0); // Éléments désactivés

  // ============================================================================
  // QUIZ PROGRESS BAR
  // ============================================================================

  static const Color progressBackground = Color(0xFFE0E0E0);
  static const Color progressFill = Color(0xFF0D0B9D);

  // ============================================================================
  // GRADIENT (pour les cartes et fonds)
  // ============================================================================

  static const LinearGradient primaryGradient = LinearGradient(
    colors: [Color(0xFF0D0B9D), Color(0xFF4845FF)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const LinearGradient successGradient = LinearGradient(
    colors: [Color(0xFF66BB6A), Color(0xFF43A047)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const LinearGradient accentGradient = LinearGradient(
    colors: [Color(0xFF292621), Color(0xFF5C5C5C)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  // Gradients pour thème sombre
  static const LinearGradient darkPrimaryGradient = LinearGradient(
    colors: [Color(0xFF0D0B9D), Color(0xFF3A36B3)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  static const LinearGradient darkAccentGradient = LinearGradient(
    colors: [Color(0xFF2D2B4A), Color(0xFF1A1938)],
    begin: Alignment.topLeft,
    end: Alignment.bottomRight,
  );

  // ============================================================================
  // SHADOWS
  // ============================================================================

  static List<BoxShadow> cardShadow = [
    BoxShadow(
      color: grey300.withOpacity(0.5),
      blurRadius: 8,
      offset: const Offset(0, 2),
    ),
  ];

  static List<BoxShadow> elevatedShadow = [
    BoxShadow(
      color: grey400.withOpacity(0.3),
      blurRadius: 12,
      offset: const Offset(0, 4),
    ),
  ];

  // Ombres pour thème sombre
  static List<BoxShadow> darkCardShadow = [
    BoxShadow(
      color: Colors.black.withOpacity(0.3),
      blurRadius: 10,
      offset: const Offset(0, 3),
    ),
  ];
}
