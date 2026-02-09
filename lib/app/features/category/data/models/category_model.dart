import '../../../../core/utils/app_constants.dart';
import '../../domain/entities/category_entity.dart';

/// Résumé d'un quiz (utilisé dans Category detail / quizzes list)
class QuizSummaryModel {
  final String id;
  final String title;
  final String level;
  final int questionCount;
  final String categoryId;
  final String status;
  final bool isAccessible;

  QuizSummaryModel({
    required this.id,
    required this.title,
    required this.level,
    required this.questionCount,
    required this.categoryId,
    required this.status,
    this.isAccessible = false,
  });

  /// Factory: Créer depuis JSON (API /categories/{id}/quizzes/available)
  ///
  /// Format attendu:
  /// {
  ///   "id": "quiz-001",
  ///   "title": "Flutter Basics",
  ///   "level": "debutant",
  ///   "question_count": 10,  // Peut être absent !
  ///   "category_id": "cat-001",
  ///   "status": "published",
  ///   "is_accessible": true
  /// }
  factory QuizSummaryModel.fromJson(Map<String, dynamic> json) {
    return QuizSummaryModel(
      id: json['id'] as String,
      title: json['title'] as String,
      level: json['level'] as String? ?? AppConstants.levelBeginner,
      // Gérer le cas où question_count est null ou absent
      // Par défaut, on met 10 (nombre standard de questions par quiz)
      questionCount: (json['question_count'] as int?) ?? 10,
      categoryId: json['category_id'] as String,
      status: json['status'] as String? ?? 'published',
      isAccessible: json['is_accessible'] as bool? ?? false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'level': level,
      'question_count': questionCount,
      'category_id': categoryId,
      'status': status,
      'is_accessible': isAccessible,
    };
  }

  @override
  String toString() {
    return 'QuizSummaryModel(id: $id, title: $title, level: $level, accessible: $isAccessible)';
  }
}

/// Model Category (DATA layer)
///
/// La catégorie et ses quizzes sont récupérés séparément
/// - GET /categories/{id} → Retourne la catégorie
/// - GET /categories/{id}/quizzes/available → Retourne les quizzes
class CategoryModel {
  final CategoryEntity entity;
  final List<QuizSummaryModel> quizzes;

  const CategoryModel({
    required this.entity,
    this.quizzes = const [],
  });

  // Getters pour accéder facilement aux propriétés de l'entity
  String get id => entity.id;
  String get name => entity.name;
  String? get description => entity.description;
  String? get iconUrl => entity.iconUrl;
  bool get isActive => entity.isActive;
  DateTime get createdAt => entity.createdAt;

  /// Format API:
  /// {
  ///   "id": "cat-001",
  ///   "name": "Flutter",
  ///   "description": "Maîtrisez Flutter",
  ///   "icon_url": null,
  ///   "is_active": true,
  ///   "created_at": "2026-01-15T10:00:00Z"
  /// }
  ///
  /// ATTENTION: Les quizzes NE SONT PAS dans cette réponse
  /// Ils doivent être récupérés séparément via /categories/{id}/quizzes/available
  factory CategoryModel.fromJson(Map<String, dynamic> json) {
    return CategoryModel(
      entity: CategoryEntity(
        id: json['id'] as String,
        name: json['name'] as String,
        description: json['description'] as String?,
        iconUrl: json['icon_url'] as String?,
        isActive: json['is_active'] as bool? ?? true,
        createdAt: DateTime.parse(json['created_at'] as String),
      ),
      quizzes: const [], // Les quizzes sont ajoutés séparément
    );
  }

  /// Factory: Créer depuis JSON avec quizzes inclus (pour le cache local)
  ///
  /// Utilisé quand on sauvegarde/récupère depuis le cache SharedPreferences
  factory CategoryModel.fromJsonWithQuizzes(Map<String, dynamic> json) {
    final quizzesJson = (json['quizzes'] as List<dynamic>?) ?? [];
    final quizzes = quizzesJson
        .cast<Map<String, dynamic>>()
        .map((e) => QuizSummaryModel.fromJson(e))
        .toList();

    return CategoryModel(
      entity: CategoryEntity(
        id: json['id'] as String,
        name: json['name'] as String,
        description: json['description'] as String?,
        iconUrl: json['icon_url'] as String?,
        isActive: json['is_active'] as bool? ?? true,
        createdAt: DateTime.parse(json['created_at'] as String),
      ),
      quizzes: quizzes,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': entity.id,
      'name': entity.name,
      'description': entity.description,
      'icon_url': entity.iconUrl,
      'is_active': entity.isActive,
      'created_at': entity.createdAt.toIso8601String(),
      'quizzes': quizzes.map((q) => q.toJson()).toList(),
    };
  }

  /// Convertir vers Entity (sans quizzes, car l'Entity ne les contient pas)
  CategoryEntity toEntity() => entity;

  /// CopyWith pour ajouter/modifier les quizzes
  CategoryModel copyWith({
    CategoryEntity? entity,
    List<QuizSummaryModel>? quizzes,
  }) {
    return CategoryModel(
      entity: entity ?? this.entity,
      quizzes: quizzes ?? this.quizzes,
    );
  }

  @override
  String toString() =>
      'CategoryModel(id: $id, name: $name, quizzes: ${quizzes.length})';
}
