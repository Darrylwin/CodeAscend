import 'package:equatable/equatable.dart';
import '../../domain/entities/category_entity.dart';
import '../../data/models/category_model.dart';

/// States pour CategoryBloc
abstract class CategoryState extends Equatable {
  const CategoryState();

  @override
  List<Object?> get props => [];
}

/// Initial
class CategoryInitial extends CategoryState {
  const CategoryInitial();
}

/// Loading (utilisé pour les requêtes list & detail)
class CategoryLoading extends CategoryState {
  const CategoryLoading();
}

/// Liste des catégories chargée
class CategoriesLoaded extends CategoryState {
  final List<CategoryEntity> categories;

  const CategoriesLoaded(this.categories);

  @override
  List<Object?> get props => [categories];
}

/// Détail d'une catégorie avec ses quizzes
class CategoryLoaded extends CategoryState {
  final CategoryEntity category;
  final List<QuizSummaryModel> quizzes;

  const CategoryLoaded({
    required this.category,
    this.quizzes = const [],
  });

  @override
  List<Object?> get props => [category, quizzes];
}

/// Erreur
class CategoryError extends CategoryState {
  final String message;

  const CategoryError(this.message);

  @override
  List<Object?> get props => [message];
}