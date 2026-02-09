import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../utils/app_constants.dart';

/// Cubit pour gérer le thème (clair/sombre)
class ThemeCubit extends Cubit<ThemeMode> {
  final SharedPreferences _prefs;

  ThemeCubit(this._prefs) : super(ThemeMode.system) {
    _loadTheme();
  }

  /// Charge le thème sauvegardé
  Future<void> _loadTheme() async {
    final themeName = _prefs.getString(AppConstants.themeKey);

    ThemeMode initialMode;
    
    if (themeName == null) {
      initialMode = ThemeMode.system;
    } else {
      switch (themeName) {
        case 'light':
          initialMode = ThemeMode.light;
          break;
        case 'dark':
          initialMode = ThemeMode.dark;
          break;
        case 'system':
        default:
          initialMode = ThemeMode.system;
          break;
      }
    }

    // Émettre le mode initial
    emit(initialMode);
  }

  /// Change le thème et le sauvegarde
  Future<void> setTheme(ThemeMode mode) async {
    String themeName;
    switch (mode) {
      case ThemeMode.light:
        themeName = 'light';
        break;
      case ThemeMode.dark:
        themeName = 'dark';
        break;
      case ThemeMode.system:
      default:
        themeName = 'system';
        break;
    }

    await _prefs.setString(AppConstants.themeKey, themeName);
    emit(mode);
  }

  /// Toggle entre clair/sombre (ignore system)
  Future<void> toggleTheme() async {
    final newMode = state == ThemeMode.light ? ThemeMode.dark : ThemeMode.light;
    await setTheme(newMode);
  }
}