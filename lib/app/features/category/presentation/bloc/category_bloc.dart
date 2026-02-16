import 'package:flutter_bloc/flutter_bloc.dart';
import '../../domain/usecases/category_usecases.dart';
import '../../data/datasources/category_remote_data_source.dart';
import '../../../../core/error/failures.dart';
import 'category_event.dart';
import 'category_state.dart';

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
    on<InvalidateCategoryCache>(_onInvalidateCache);
  }

  Future<void> _onFetchCategories(
    FetchCategories event,
    Emitter<CategoryState> emit,
  ) async {
    // Skip uniquement si déjà chargé ET pas de forceRefresh
    if (state is CategoriesLoaded && !event.forceRefresh) return;
    if (state is CategoryLoading) return;

    emit(const CategoryLoading());

    final result = await _getCategoriesUseCase(
      GetCategoriesParams(isActive: event.isActive),
    );

    result.fold(
      (failure) => emit(CategoryError(_mapFailureToMessage(failure))),
      (categories) => emit(CategoriesLoaded(categories)),
    );
  }

  Future<void> _onFetchCategoryById(
    FetchCategoryById event,
    Emitter<CategoryState> emit,
  ) async {
    // Ne skip que si même catégorie déjà chargée ET pas de forceRefresh
    if (!event.forceRefresh &&
        state is CategoryLoaded &&
        (state as CategoryLoaded).category.id == event.id) {
      return;
    }

    emit(const CategoryLoading());

    try {
      final categoryResult = await _getCategoryByIdUseCase(event.id);

      await categoryResult.fold(
        (failure) async {
          emit(CategoryError(_mapFailureToMessage(failure)));
        },
        (categoryEntity) async {
          try {
            final quizzes =
                await _remoteDataSource.getAvailableQuizzes(event.id);
            emit(CategoryLoaded(category: categoryEntity, quizzes: quizzes));
          } catch (_) {
            // On émet quand même la catégorie sans quizzes
            emit(CategoryLoaded(category: categoryEntity, quizzes: const []));
          }
        },
      );
    } catch (e) {
      emit(CategoryError('Erreur lors du chargement de la catégorie: $e'));
    }
  }

  void _onInvalidateCache(
    InvalidateCategoryCache event,
    Emitter<CategoryState> emit,
  ) {
    emit(const CategoryInitial());
  }

  String _mapFailureToMessage(Failure failure) => failure.message;
}