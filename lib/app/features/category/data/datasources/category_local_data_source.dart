import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import '../../../../core/utils/app_constants.dart';
import '../models/category_model.dart';

/// Local DataSource (cache) pour les catégories
/// 
/// Utilise fromJsonWithQuizzes pour le cache
/// car le cache sauvegarde les quizzes avec les catégories
abstract class CategoryLocalDataSource {
  /// Met en cache la liste des catégories (JSON)
  Future<void> cacheCategories(List<CategoryModel> categories);

  /// Récupère la liste des catégories depuis le cache
  Future<List<CategoryModel>?> getCachedCategories();

  /// Récupère une catégorie du cache par id (ou null)
  Future<CategoryModel?> getCachedCategoryById(String id);

  /// Supprime le cache des catégories
  Future<void> clearCachedCategories();
}

class CategoryLocalDataSourceImpl implements CategoryLocalDataSource {
  final SharedPreferences _prefs;

  CategoryLocalDataSourceImpl(this._prefs);

  @override
  Future<void> cacheCategories(List<CategoryModel> categories) async {
    final jsonList = categories.map((e) => e.toJson()).toList();
    final jsonString = json.encode(jsonList);
    await _prefs.setString(AppConstants.categoriesKey, jsonString);
  }

  @override
  Future<List<CategoryModel>?> getCachedCategories() async {
    try {
      final jsonString = _prefs.getString(AppConstants.categoriesKey);
      if (jsonString == null) return null;

      final list =
          (json.decode(jsonString) as List).cast<Map<String, dynamic>>();
      
      // Utilise fromJsonWithQuizzes pour récupérer
      // les quizzes qui sont sauvegardés dans le cache
      return list.map((e) => CategoryModel.fromJsonWithQuizzes(e)).toList();
    } catch (e) {
      // Si parsing corrompu, nettoyer le cache
      await clearCachedCategories();
      return null;
    }
  }

  @override
  Future<CategoryModel?> getCachedCategoryById(String id) async {
    final categories = await getCachedCategories();
    if (categories == null) return null;
    try {
      return categories.firstWhere((c) => c.id == id);
    } catch (_) {
      return null;
    }
  }

  @override
  Future<void> clearCachedCategories() async {
    await _prefs.remove(AppConstants.categoriesKey);
  }
}