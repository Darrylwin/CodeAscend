import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

// ============================================================================
// EXTENSIONS SUR STRING
// ============================================================================

extension StringExtensions on String {
  /// Capitalise la première lettre
  String get capitalize {
    if (isEmpty) return this;
    return '${this[0].toUpperCase()}${substring(1)}';
  }

  /// Vérifie si c'est un email valide
  bool get isValidEmail {
    final emailRegex = RegExp(
      r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
    );
    return emailRegex.hasMatch(this);
  }

  /// Vérifie si le mot de passe est valide (min 8 caractères)
  bool get isValidPassword {
    return length >= 8;
  }

  /// Tronque le texte avec '...'
  String truncate(int maxLength) {
    if (length <= maxLength) return this;
    return '${substring(0, maxLength)}...';
  }

  /// Mapping intelligent des catégories vers des images
  String get categoryIconUrl {
    final nameLower = toLowerCase().trim();
    
    // Langages de programmation
    if (nameLower.contains('python')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg';
    }
    if (nameLower.contains('javascript') || nameLower.contains('js')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg';
    }
    if (nameLower.contains('typescript') || nameLower.contains('ts')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/typescript/typescript-original.svg';
    }
    if (nameLower.contains('java') && !nameLower.contains('script')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/java/java-original.svg';
    }
    if (nameLower.contains('c++') || nameLower.contains('cpp')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/cplusplus/cplusplus-original.svg';
    }
    if (nameLower == 'c' || nameLower.contains('langage c')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/c/c-original.svg';
    }
    if (nameLower.contains('c#') || nameLower.contains('csharp')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/csharp/csharp-original.svg';
    }
    if (nameLower.contains('php')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/php/php-original.svg';
    }
    if (nameLower.contains('ruby')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/ruby/ruby-original.svg';
    }
    if (nameLower.contains('go') || nameLower.contains('golang')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/go/go-original.svg';
    }
    if (nameLower.contains('rust')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/rust/rust-plain.svg';
    }
    if (nameLower.contains('swift')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/swift/swift-original.svg';
    }
    if (nameLower.contains('kotlin')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/kotlin/kotlin-original.svg';
    }
    if (nameLower.contains('dart')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/dart/dart-original.svg';
    }
    if (nameLower.contains('scala')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/scala/scala-original.svg';
    }
    if (nameLower.contains('perl')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/perl/perl-original.svg';
    }
    if (nameLower.contains('r') || nameLower.contains('langage r')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/r/r-original.svg';
    }
    if (nameLower.contains('matlab')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/matlab/matlab-original.svg';
    }

    // Frameworks Web
    if (nameLower.contains('react')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg';
    }
    if (nameLower.contains('vue')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/vuejs/vuejs-original.svg';
    }
    if (nameLower.contains('angular')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/angularjs/angularjs-original.svg';
    }
    if (nameLower.contains('svelte')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/svelte/svelte-original.svg';
    }
    if (nameLower.contains('next')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nextjs/nextjs-original.svg';
    }
    if (nameLower.contains('nuxt')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nuxtjs/nuxtjs-original.svg';
    }

    // Frameworks Backend
    if (nameLower.contains('django')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/django/django-plain.svg';
    }
    if (nameLower.contains('flask')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flask/flask-original.svg';
    }
    if (nameLower.contains('fastapi')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original.svg';
    }
    if (nameLower.contains('express')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/express/express-original.svg';
    }
    if (nameLower.contains('nest')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nestjs/nestjs-plain.svg';
    }
    if (nameLower.contains('laravel')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/laravel/laravel-plain.svg';
    }
    if (nameLower.contains('symfony')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/symfony/symfony-original.svg';
    }
    if (nameLower.contains('spring')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/spring/spring-original.svg';
    }
    if (nameLower.contains('rails') || nameLower.contains('ruby on rails')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/rails/rails-plain.svg';
    }

    // Mobile
    if (nameLower.contains('flutter')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/flutter/flutter-original.svg';
    }
    if (nameLower.contains('react native')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/react/react-original.svg';
    }
    if (nameLower.contains('android')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/android/android-original.svg';
    }
    if (nameLower.contains('ios')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/apple/apple-original.svg';
    }

    // Bases de données
    if (nameLower.contains('sql') || nameLower.contains('mysql')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mysql/mysql-original.svg';
    }
    if (nameLower.contains('postgresql') || nameLower.contains('postgres')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/postgresql/postgresql-original.svg';
    }
    if (nameLower.contains('mongodb') || nameLower.contains('mongo')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original.svg';
    }
    if (nameLower.contains('redis')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/redis/redis-original.svg';
    }
    if (nameLower.contains('firebase')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/firebase/firebase-plain.svg';
    }
    if (nameLower.contains('oracle')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/oracle/oracle-original.svg';
    }

    // DevOps / Outils
    if (nameLower.contains('docker')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg';
    }
    if (nameLower.contains('kubernetes') || nameLower.contains('k8s')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/kubernetes/kubernetes-plain.svg';
    }
    if (nameLower.contains('git')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/git/git-original.svg';
    }
    if (nameLower.contains('jenkins')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/jenkins/jenkins-original.svg';
    }
    if (nameLower.contains('aws')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/amazonwebservices/amazonwebservices-original.svg';
    }
    if (nameLower.contains('azure')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/azure/azure-original.svg';
    }
    if (nameLower.contains('gcp') || nameLower.contains('google cloud')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/googlecloud/googlecloud-original.svg';
    }

    // Web technologies
    if (nameLower.contains('html')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg';
    }
    if (nameLower.contains('css')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/css3/css3-original.svg';
    }
    if (nameLower.contains('sass') || nameLower.contains('scss')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/sass/sass-original.svg';
    }
    if (nameLower.contains('tailwind')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tailwindcss/tailwindcss-plain.svg';
    }
    if (nameLower.contains('bootstrap')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/bootstrap/bootstrap-original.svg';
    }

    // Autres
    if (nameLower.contains('node')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/nodejs/nodejs-original.svg';
    }
    if (nameLower.contains('graphql')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/graphql/graphql-plain.svg';
    }
    if (nameLower.contains('webpack')) {
      return 'https://cdn.jsdelivr.net/gh/devicons/devicon/icons/webpack/webpack-original.svg';
    }
    if (nameLower.contains('vite')) {
      return 'https://vitejs.dev/logo.svg';
    }

    // Fallback: icône générique (pas d'URL, sera géré par le widget)
    return '';
  }

  /// Vérifie si une catégorie a une icône mappée
  bool get hasCategoryIcon {
    return categoryIconUrl.isNotEmpty;
  }
}

// ============================================================================
// EXTENSIONS SUR INT
// ============================================================================

extension IntExtensions on int {
  /// Convertit un score en pourcentage (0-100)
  String get toPercentage => '$this%';

  /// Ajoute un padding de zéros (ex: 5 -> "05")
  String zeroPad([int width = 2]) {
    return toString().padLeft(width, '0');
  }
}

// ============================================================================
// EXTENSIONS SUR DOUBLE
// ============================================================================

extension DoubleExtensions on double {
  /// Arrondit à n décimales
  double roundTo(int decimals) {
    final factor = 10 * decimals;
    return (this * factor).round() / factor;
  }

  /// Convertit en pourcentage formaté
  String toPercentageString([int decimals = 0]) {
    return '${roundTo(decimals).toStringAsFixed(decimals)}%';
  }
}

// ============================================================================
// EXTENSIONS SUR DATETIME
// ============================================================================

extension DateTimeExtensions on DateTime {
  /// Formate en "10 jan. 2026"
  String get formatShort {
    try {
      return DateFormat('d MMM yyyy', 'fr_FR').format(this);
    } catch (_) {
      // Fallback si fr_FR n'est pas initialisé
      return DateFormat('d MMM yyyy').format(this);
    }
  }

  /// Formate en "10 janvier 2026"
  String get formatLong {
    try {
      return DateFormat('d MMMM yyyy', 'fr_FR').format(this);
    } catch (_) {
      return DateFormat('d MMMM yyyy').format(this);
    }
  }

  /// Formate en "10/01/2026"
  String get formatNumeric {
    return DateFormat('dd/MM/yyyy').format(this);
  }

  /// Formate avec l'heure "10 jan. à 14:30"
  String get formatWithTime {
    try {
      return DateFormat('d MMM à HH:mm', 'fr_FR').format(this);
    } catch (_) {
      return DateFormat('d MMM à HH:mm').format(this);
    }
  }

  /// Retourne un libellé relatif (ex: "il y a 5 min")
  String get timeAgo {
    final now = DateTime.now();
    final difference = now.difference(this);

    if (difference.inSeconds < 60) {
      return 'À l\'instant';
    } else if (difference.inMinutes < 60) {
      return 'il y a ${difference.inMinutes} min';
    } else if (difference.inHours < 24) {
      return 'il y a ${difference.inHours}h';
    } else if (difference.inDays == 1) {
      return 'Hier';
    } else if (difference.inDays < 7) {
      return 'il y a ${difference.inDays} jours';
    } else {
      // Format: 30 Jan 2026
      final months = [
        'Jan',
        'Fév',
        'Mar',
        'Avr',
        'Mai',
        'Juin',
        'Juil',
        'Aoû',
        'Sep',
        'Oct',
        'Nov',
        'Déc'
      ];
      return '$day ${months[month - 1]} $year';
    }
  }
}

// ============================================================================
// EXTENSIONS SUR BUILDCONTEXT
// ============================================================================

extension BuildContextExtensions on BuildContext {
  /// Accès rapide au thème
  ThemeData get theme => Theme.of(this);
  TextTheme get textTheme => theme.textTheme;
  ColorScheme get colors => theme.colorScheme;

  /// Accès aux dimensions de l'écran
  Size get screenSize => MediaQuery.of(this).size;
  double get screenWidth => screenSize.width;
  double get screenHeight => screenSize.height;

  /// Vérifie si c'est un petit écran (mobile)
  bool get isSmallScreen => screenWidth < 600;

  /// Vérifie si c'est un écran moyen (tablette)
  bool get isMediumScreen => screenWidth >= 600 && screenWidth < 1200;

  /// Vérifie si c'est un grand écran (desktop)
  bool get isLargeScreen => screenWidth >= 1200;

  /// Afficher un SnackBar avec message de succès
  void showSuccessSnackBar(String message) {
    ScaffoldMessenger.of(this).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            const Icon(Icons.check_circle, color: Colors.white),
            const SizedBox(width: 12),
            Expanded(child: Text(message)),
          ],
        ),
        backgroundColor: Colors.green,
        behavior: SnackBarBehavior.floating,
        duration: const Duration(seconds: 3),
      ),
    );
  }

  /// Afficher un SnackBar avec message d'erreur
  void showErrorSnackBar(String message) {
    ScaffoldMessenger.of(this).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            const Icon(Icons.error, color: Colors.white),
            const SizedBox(width: 12),
            Expanded(child: Text(message)),
          ],
        ),
        backgroundColor: Colors.red,
        behavior: SnackBarBehavior.floating,
        duration: const Duration(seconds: 4),
      ),
    );
  }

  /// Afficher un SnackBar avec message d'info
  void showInfoSnackBar(String message) {
    ScaffoldMessenger.of(this).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            const Icon(Icons.info, color: Colors.white),
            const SizedBox(width: 12),
            Expanded(child: Text(message)),
          ],
        ),
        backgroundColor: Colors.blue,
        behavior: SnackBarBehavior.floating,
        duration: const Duration(seconds: 3),
      ),
    );
  }

  /// Afficher un dialog de confirmation
  Future<bool> showConfirmDialog({
    required String title,
    required String message,
    String confirmText = 'Confirmer',
    String cancelText = 'Annuler',
  }) async {
    final result = await showDialog<bool>(
      context: this,
      builder: (context) => AlertDialog(
        title: Text(title),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(false),
            child: Text(cancelText),
          ),
          ElevatedButton(
            onPressed: () => Navigator.of(context).pop(true),
            child: Text(confirmText),
          ),
        ],
      ),
    );
    return result ?? false;
  }

  /// Fermer le clavier
  void hideKeyboard() {
    FocusScope.of(this).unfocus();
  }
}