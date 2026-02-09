import 'package:dartz/dartz.dart';
import '../../../../core/error/failures.dart';
import '../entities/category_entity.dart';

/// Contrat (interface) du repository Category — lecture seule pour l'application mobile.
abstract class CategoryRepository {
  /// Récupère la liste des catégories.
  ///
  /// - [isActive] : si fourni, filtre les catégories actives/inactives.
  Future<Either<Failure, List<CategoryEntity>>> getCategories({
    bool? isActive,
  });

  /// Récupère une catégorie par son [id].
  Future<Either<Failure, CategoryEntity>> getCategoryById(String id);
}
