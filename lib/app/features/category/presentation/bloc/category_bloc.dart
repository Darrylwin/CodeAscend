import 'package:flutter_bloc/flutter_bloc.dart';
import '../../domain/usecases/category_usecases.dart';
import '../../data/datasources/category_remote_data_source.dart';
import '../../../../core/error/failures.dart';
import 'category_event.dart';
import 'category_state.dart';

/// Bloc pour gérer la feature Category (liste + détail)
/// 
/// Responsabilités :
/// - Écouter les events (FetchCategories, FetchCategoryById)
/// - Appeler les usecases correspondants
/// - Émettre les states (CategoriesLoaded, CategoryLoaded, CategoryError, ...)
class CategoryBloc extends Bloc<CategoryEvent, CategoryState> {
  final GetCategoriesUseCase _getCategoriesUseCase;
  final GetCategoryByIdUseCase _getCategoryByIdUseCase;
  final CategoryRemoteDataSource _remoteDataSource;

  CategoryBloc({
    required GetCategoriesUseCase getCategoriesUseCase,
    required GetCategoryByIdUseCase getCategoryByIdUseCase,
    required CategoryRemoteDataSource remoteDataSource,
  })  : _getCategoriesUseCase = getCategoriesUseCase,
        _getCategoryByIdUseCase = getCategoryByIdUseCase,
        _remoteDataSource = remoteDataSource,
        super(const CategoryInitial()) {
    on<FetchCategories>(_onFetchCategories);
    on<FetchCategoryById>(_onFetchCategoryById);
  }

  /// Handler: Récupère la liste des catégories
  Future<void> _onFetchCategories(
    FetchCategories event,
    Emitter<CategoryState> emit,
  ) async {
    // Si déjà chargé et pas de force refresh, ne pas recharger
    if (state is CategoriesLoaded && !event.forceRefresh) {
      return;
    }
    
    // Si on est en train de charger, ne pas relancer
    if (state is! CategoryLoading) {
      emit(const CategoryLoading());
    }

    final result = await _getCategoriesUseCase(
      GetCategoriesParams(
        isActive: event.isActive,
      ),
    );

    result.fold(
      (failure) => emit(CategoryError(_mapFailureToMessage(failure))),
      (categories) => emit(CategoriesLoaded(categories)),
    );
  }

  /// 1. GET /categories/{id} → Catégorie
  /// 2. GET /categories/{id}/quizzes/available → Quizzes
  Future<void> _onFetchCategoryById(
    FetchCategoryById event,
    Emitter<CategoryState> emit,
  ) async {
    // Si cette catégorie est déjà chargée, ne pas recharger
    if (state is CategoryLoaded && (state as CategoryLoaded).category.id == event.id) {
      return;
    }
    
    emit(const CategoryLoading());

    try {
      // 1. Récupérer la catégorie (Entity) via le usecase
      final categoryResult = await _getCategoryByIdUseCase(event.id);

      await categoryResult.fold(
        (failure) async {
          emit(CategoryError(_mapFailureToMessage(failure)));
        },
        (categoryEntity) async {
          // 2. Récupérer les quizzes disponibles via le remote data source
          try {
            final quizzes = await _remoteDataSource.getAvailableQuizzes(event.id);

            // 3. Émettre le state avec Entity + Quizzes
            emit(CategoryLoaded(
              category: categoryEntity,
              quizzes: quizzes,
            ));
          } catch (quizzesError) {
            // Si erreur lors de la récupération des quizzes,
            // on émet quand même la catégorie sans quizzes
            // pour ne pas bloquer l'UX
            print('Erreur récupération des quizzes: $quizzesError');
            
            emit(CategoryLoaded(
              category: categoryEntity,
              quizzes: const [],
            ));
          }
        },
      );
    } catch (e) {
      emit(CategoryError('Erreur lors du chargement de la catégorie: $e'));
    }
  }

  /// Convertit un Failure en message d'erreur lisible
  String _mapFailureToMessage(Failure failure) {
    return failure.message;
  }
}