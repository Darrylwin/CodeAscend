import 'package:dio/dio.dart';
import '../models/category_model.dart';

/// Remote DataSource pour les catégories
abstract class CategoryRemoteDataSource {
  /// GET /categories
  ///
  /// Query params: ?is_active=true
  ///
  /// Response (Array direct):
  /// [
  ///   {
  ///     "id": "cat-001",
  ///     "name": "Flutter",
  ///     "description": "Maîtrisez Flutter",
  ///     "icon_url": null,
  ///     "is_active": true,
  ///     "created_at": "2026-01-15T10:00:00Z"
  ///   }
  /// ]
  Future<List<CategoryModel>> getCategories({
    bool? isActive,
  });

  /// GET /categories/{id}
  ///
  /// Response (Objet direct):
  /// {
  ///   "id": "cat-001",
  ///   "name": "Flutter",
  ///   "description": "Maîtrisez Flutter",
  ///   "icon_url": null,
  ///   "is_active": true,
  ///   "created_at": "2026-01-15T10:00:00Z"
  /// }
  Future<CategoryModel> getCategoryById(String id);

  /// GET /categories/{id}/quizzes/available
  ///
  /// Response (Objet avec data):
  /// {
  ///   "data": [
  ///     {
  ///       "id": "quiz-001",
  ///       "title": "Flutter Basics",
  ///       "level": "debutant",
  ///       "category_id": "cat-001",
  ///       "status": "published",
  ///       "is_accessible": true
  ///     }
  ///   ],
  ///   "meta": {},
  ///   "message": "Quiz disponibles récupérés avec succès"
  /// }
  Future<List<QuizSummaryModel>> getAvailableQuizzes(String categoryId);
}

class CategoryRemoteDataSourceImpl implements CategoryRemoteDataSource {
  final Dio _dio;

  CategoryRemoteDataSourceImpl(this._dio);

  @override
  Future<List<CategoryModel>> getCategories({
    bool? isActive,
  }) async {
    // Construction des query parameters
    final queryParameters = <String, dynamic>{};

    if (isActive != null) {
      queryParameters['is_active'] = isActive;
    }

    try {
      final response = await _dio.get(
        '/categories/',
        queryParameters: queryParameters.isNotEmpty ? queryParameters : null,
      );

      final data = response.data;

      if (data is! List) {
        throw Exception('Format de réponse API inattendu pour /categories: '
            'attendu List, reçu ${data.runtimeType}');
      }

      return data
          .cast<Map<String, dynamic>>()
          .map((e) => CategoryModel.fromJson(e))
          .toList();
    } on DioException {
      // Laisser le repository gérer la conversion en Failure
      rethrow;
    } catch (e) {
      throw Exception('Erreur lors du parsing des catégories: $e');
    }
  }

  @override
  Future<CategoryModel> getCategoryById(String id) async {
    try {
      final response = await _dio.get('/categories/$id');

      final data = response.data;

      if (data is! Map<String, dynamic>) {
        throw Exception('Format de réponse API inattendu pour /categories/$id: '
            'attendu Map, reçu ${data.runtimeType}');
      }

      return CategoryModel.fromJson(data);
    } on DioException {
      rethrow;
    } catch (e) {
      throw Exception('Erreur lors du parsing de la catégorie: $e');
    }
  }

  @override
  Future<List<QuizSummaryModel>> getAvailableQuizzes(String categoryId) async {
    try {
      final response = await _dio.get(
        '/categories/$categoryId/quizzes/available',
      );

      final data = response.data;

      // L'API retourne un objet avec "data", pas directement un array
      if (data is Map<String, dynamic>) {
        // Extraire le tableau "data"
        final quizzesData = data['data'];

        if (quizzesData is! List) {
          throw Exception(
              'Format de réponse API inattendu pour /categories/$categoryId/quizzes/available: '
              'attendu data: List, reçu data: ${quizzesData.runtimeType}');
        }

        return quizzesData
            .cast<Map<String, dynamic>>()
            .map((e) => QuizSummaryModel.fromJson(e))
            .toList();
      }
      // Fallback: Si l'API retourne directement un array (ancien format)
      else if (data is List) {
        return data
            .cast<Map<String, dynamic>>()
            .map((e) => QuizSummaryModel.fromJson(e))
            .toList();
      } else {
        throw Exception(
            'Format de réponse API inattendu pour /categories/$categoryId/quizzes/available: '
            'attendu Map ou List, reçu ${data.runtimeType}');
      }
    } on DioException {
      rethrow;
    } catch (e) {
      throw Exception('Erreur lors du parsing des quizzes: $e');
    }
  }
}
