import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/category_entity.dart';
import '../repositories/category_repository.dart';

/// UseCase: Récupérer la liste des catégories (lecture seule)
class GetCategoriesUseCase {
  final CategoryRepository _repository;

  GetCategoriesUseCase(this._repository);

  Future<Either<Failure, List<CategoryEntity>>> call(
    GetCategoriesParams params,
  ) {
    return _repository.getCategories(
      isActive: params.isActive,
    );
  }
}

/// Paramètres pour GetCategoriesUseCase
class GetCategoriesParams {
  final bool? isActive;

  const GetCategoriesParams({
    this.isActive,
  });
}

/// UseCase: Récupérer une catégorie par id
class GetCategoryByIdUseCase {
  final CategoryRepository _repository;

  GetCategoryByIdUseCase(this._repository);

  Future<Either<Failure, CategoryEntity>> call(String id) {
    return _repository.getCategoryById(id);
  }
}