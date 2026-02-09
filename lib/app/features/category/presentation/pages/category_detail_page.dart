import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_svg/flutter_svg.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/utils/app_extensions.dart';
import '../bloc/category_bloc.dart';
import '../bloc/category_event.dart';
import '../bloc/category_state.dart';
import '../../data/models/category_model.dart';
import '../../domain/entities/category_entity.dart';
import '../../../attempts/presentation/bloc/attempts_bloc.dart';
import '../../../attempts/presentation/bloc/attempts_event.dart';
import '../../../attempts/presentation/bloc/attempts_state.dart';
import '../widgets/level_progress_card.dart';

/// Détail d'une catégorie avec indicateurs de progression améliorés
class CategoryDetailPage extends StatefulWidget {
  final String categoryId;

  const CategoryDetailPage({super.key, required this.categoryId});

  @override
  State<CategoryDetailPage> createState() => _CategoryDetailPageState();
}

class _CategoryDetailPageState extends State<CategoryDetailPage>
    with RouteAware {
  bool _returningFromQuiz = false;
  bool _initialized = false;
  bool _isSubscribed = false;

  @override
  void initState() {
    super.initState();

    // Charger les données immédiatement dans initState
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (!_initialized) {
        _loadData();
        _initialized = true;
      }
    });
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();

    // Souscrire au RouteObserver une seule fois
    if (!_isSubscribed) {
      final modalRoute = ModalRoute.of(context);
      if (modalRoute is PageRoute) {
        routeObserver.subscribe(this, modalRoute);
        _isSubscribed = true;
      }
    }
  }

  @override
  void dispose() {
    routeObserver.unsubscribe(this);
    super.dispose();
  }

  @override
  void didPopNext() {
    // On revient sur cette page
    if (_returningFromQuiz) {
      debugPrint('🔄 CategoryDetailPage: Retour de quiz détecté, refresh...');
      _loadData();
      _returningFromQuiz = false;
    } else {
      debugPrint(
          '✅ CategoryDetailPage: Retour détecté, pas de refresh nécessaire');
    }
  }

  /// Force le rechargement (appelé après retour de quiz)
  void _loadData() {
    debugPrint('📥 CategoryDetailPage: _loadData() appelé');

    final attemptsBloc = context.read<AttemptsBloc>();
    final categoryBloc = context.read<CategoryBloc>();

    // Charger les attempts si pas déjà chargés
    if (attemptsBloc.state is! AttemptsLoaded) {
      debugPrint('  → Chargement des attempts...');
      attemptsBloc.add(const LoadAttempts());
    } else {
      debugPrint('  ✓ Attempts déjà chargés, skip');
    }

    // Charger la catégorie si nécessaire
    final categoryState = categoryBloc.state;
    if (categoryState is! CategoryLoaded ||
        categoryState.category.id != widget.categoryId) {
      debugPrint('  → Chargement de la catégorie ${widget.categoryId}...');
      categoryBloc.add(FetchCategoryById(widget.categoryId));
    } else {
      debugPrint('  ✓ Catégorie déjà chargée, skip');
    }
  }

  /// Récupère les données de progression pour un niveau
  Map<String, dynamic> _getLevelProgress(
    CategoryEntity category,
    String level,
    List<QuizSummaryModel> quizzes,
    AttemptsLoaded attemptsState,
  ) {
    try {
      if (quizzes.isEmpty) {
        return {
          'accessible': level == 'debutant',
          'attempts': 0,
          'bestScore': null,
          'passed': false,
          'inProgress': false,
          'quizId': null,
        };
      }

      final levelQuizzes = quizzes.where((q) => q.level == level).toList();

      if (levelQuizzes.isEmpty) {
        return {
          'accessible': level == 'debutant',
          'attempts': 0,
          'bestScore': null,
          'passed': false,
          'inProgress': false,
          'quizId': null,
        };
      }

      final firstQuiz = levelQuizzes.first;
      final levelQuizIds = levelQuizzes.map((q) => q.id).toSet();

      try {
        final inProgressAttempt = attemptsState.allAttempts.firstWhere(
          (a) => levelQuizIds.contains(a.quizId) && a.isInProgress,
        );

        return {
          'accessible': firstQuiz.isAccessible,
          'attempts': 0,
          'bestScore': null,
          'passed': false,
          'inProgress': true,
          'quizId': inProgressAttempt.quizId,
        };
      } catch (_) {}

      final levelAttempts = attemptsState.allAttempts
          .where((a) => levelQuizIds.contains(a.quizId) && !a.isInProgress)
          .toList();

      if (levelAttempts.isEmpty) {
        return {
          'accessible': firstQuiz.isAccessible,
          'attempts': 0,
          'bestScore': null,
          'passed': false,
          'inProgress': false,
          'quizId': firstQuiz.id,
        };
      }

      final bestScore =
          levelAttempts.map((a) => a.score).reduce((a, b) => a > b ? a : b);
      final passed = levelAttempts.any((a) => a.passed);

      return {
        'accessible': firstQuiz.isAccessible,
        'attempts': levelAttempts.length,
        'bestScore': bestScore,
        'passed': passed,
        'inProgress': false,
        'quizId': firstQuiz.id,
      };
    } catch (e) {
      debugPrint('❌ Erreur _getLevelProgress: $e');
      return {
        'accessible': level == 'debutant',
        'attempts': 0,
        'bestScore': null,
        'passed': false,
        'inProgress': false,
        'quizId': quizzes.isNotEmpty ? quizzes.first.id : null,
      };
    }
  }

  /// Calcule la progression globale (0-100%)
  double _calculateOverallProgress(
    CategoryEntity category,
    List<QuizSummaryModel> quizzes,
    AttemptsLoaded attemptsState,
  ) {
    final beginnerProgress =
        _getLevelProgress(category, 'debutant', quizzes, attemptsState);
    final intermediateProgress =
        _getLevelProgress(category, 'intermediaire', quizzes, attemptsState);
    final advancedProgress =
        _getLevelProgress(category, 'avance', quizzes, attemptsState);

    int completed = 0;
    if (beginnerProgress['passed'] == true) completed++;
    if (intermediateProgress['passed'] == true) completed++;
    if (advancedProgress['passed'] == true) completed++;

    return (completed / 3) * 100;
  }

  void _navigateToQuiz(String quizId, bool restore) {
    // Marquer qu'on va partir vers un quiz
    _returningFromQuiz = true;

    if (restore) {
      context.push('/quiz/$quizId?restore=true');
    } else {
      context.push('/quiz/$quizId');
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Détail Catégorie'),
        backgroundColor: colorScheme.primary,
        foregroundColor: colorScheme.onPrimary,
      ),
      body: BlocConsumer<AttemptsBloc, AttemptsState>(
        listener: (context, attemptsState) {
          // Gérer les changements d'état si nécessaire
        },
        builder: (context, attemptsState) {
          return BlocConsumer<CategoryBloc, CategoryState>(
            listener: (context, categoryState) {
              // Gérer les changements d'état si nécessaire
            },
            builder: (context, categoryState) {
              if (categoryState is CategoryLoading ||
                  categoryState is CategoryInitial ||
                  attemptsState is AttemptsLoading ||
                  attemptsState is AttemptsInitial) {
                return Center(
                  child: Image.asset(
                    'assets/animations/loading.gif',
                    width: 64,
                    height: 64,
                    fit: BoxFit.contain,
                    color: colorScheme.primary,
                  ),
                );
              }

              if (categoryState is CategoryError) {
                return Center(
                  child: Padding(
                    padding: const EdgeInsets.all(24.0),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.error_outline,
                            size: 64, color: colorScheme.error),
                        const SizedBox(height: 16),
                        Text('Erreur', style: context.textTheme.headlineSmall),
                        const SizedBox(height: 8),
                        Text(categoryState.message,
                            textAlign: TextAlign.center),
                        const SizedBox(height: 24),
                        ElevatedButton(
                          onPressed: _loadData,
                          child: const Text('Réessayer'),
                        ),
                        const SizedBox(height: 16),
                        OutlinedButton(
                          onPressed: () => context.go('/home'),
                          child: const Text('Retour à l\'accueil'),
                        ),
                      ],
                    ),
                  ),
                );
              }

              if (attemptsState is AttemptsError) {
                return Center(
                  child: Padding(
                    padding: const EdgeInsets.all(24.0),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.error_outline,
                            size: 64, color: colorScheme.error),
                        const SizedBox(height: 16),
                        Text('Erreur', style: context.textTheme.headlineSmall),
                        const SizedBox(height: 8),
                        Text(attemptsState.message,
                            textAlign: TextAlign.center),
                        const SizedBox(height: 24),
                        ElevatedButton(
                          onPressed: _loadData,
                          child: const Text('Réessayer'),
                        ),
                      ],
                    ),
                  ),
                );
              }

              if (categoryState is CategoryLoaded &&
                  attemptsState is AttemptsLoaded) {
                final category = categoryState.category;
                final quizzes = categoryState.quizzes;

                final overallProgress =
                    _calculateOverallProgress(category, quizzes, attemptsState);
                final beginnerProgress = _getLevelProgress(
                    category, 'debutant', quizzes, attemptsState);
                final intermediateProgress = _getLevelProgress(
                    category, 'intermediaire', quizzes, attemptsState);
                final advancedProgress = _getLevelProgress(
                    category, 'avance', quizzes, attemptsState);

                return RefreshIndicator(
                  onRefresh: () async {
                    _loadData();
                    await Future.delayed(const Duration(milliseconds: 500));
                  },
                  color: colorScheme.primary,
                  child: SingleChildScrollView(
                    physics: const AlwaysScrollableScrollPhysics(),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        // Header avec progression
                        Container(
                          width: double.infinity,
                          padding: const EdgeInsets.all(24.0),
                          decoration: BoxDecoration(
                            gradient: LinearGradient(
                              colors: [
                                colorScheme.primary,
                                colorScheme.primary.withOpacity(0.7),
                              ],
                            ),
                          ),
                          child: SafeArea(
                            bottom: false,
                            child: Column(
                              children: [
                                _buildCategoryIcon(category, colorScheme),
                                const SizedBox(height: 16),
                                Text(
                                  category.name,
                                  style: context.textTheme.headlineMedium
                                      ?.copyWith(
                                    color: colorScheme.onPrimary,
                                    fontWeight: FontWeight.bold,
                                  ),
                                  textAlign: TextAlign.center,
                                ),
                                const SizedBox(height: 8),
                                if (category.description != null)
                                  Text(
                                    category.description!,
                                    style:
                                        context.textTheme.bodyMedium?.copyWith(
                                      color: colorScheme.onPrimary
                                          .withOpacity(0.9),
                                    ),
                                    textAlign: TextAlign.center,
                                  ),
                                const SizedBox(height: 24),
                                Column(
                                  children: [
                                    Row(
                                      mainAxisAlignment:
                                          MainAxisAlignment.spaceBetween,
                                      children: [
                                        Text(
                                          'Progression globale',
                                          style: context.textTheme.titleSmall
                                              ?.copyWith(
                                            color: colorScheme.onPrimary,
                                            fontWeight: FontWeight.w600,
                                          ),
                                        ),
                                        Text(
                                          '${overallProgress.round()}%',
                                          style: context.textTheme.titleMedium
                                              ?.copyWith(
                                            color: colorScheme.onPrimary,
                                            fontWeight: FontWeight.bold,
                                          ),
                                        ),
                                      ],
                                    ),
                                    const SizedBox(height: 12),
                                    ClipRRect(
                                      borderRadius: BorderRadius.circular(10),
                                      child: LinearProgressIndicator(
                                        value: overallProgress / 100,
                                        minHeight: 12,
                                        backgroundColor: colorScheme.onPrimary
                                            .withOpacity(0.3),
                                        valueColor:
                                            AlwaysStoppedAnimation<Color>(
                                          colorScheme.onPrimary,
                                        ),
                                      ),
                                    ),
                                  ],
                                ),
                              ],
                            ),
                          ),
                        ),

                        // Liste des niveaux avec progression
                        Padding(
                          padding: const EdgeInsets.all(16.0),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                'Parcours d\'apprentissage',
                                style: context.textTheme.titleLarge?.copyWith(
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                              const SizedBox(height: 16),

                              // Niveau Débutant
                              LevelProgressCard(
                                title: 'Niveau Débutant',
                                level: 'debutant',
                                accessible: beginnerProgress['accessible'],
                                attempts: beginnerProgress['attempts'],
                                bestScore: beginnerProgress['bestScore'],
                                passed: beginnerProgress['passed'],
                                inProgress: beginnerProgress['inProgress'],
                                onStart: () {
                                  final quizId = beginnerProgress['quizId'];
                                  if (quizId != null) {
                                    _navigateToQuiz(quizId,
                                        beginnerProgress['inProgress'] == true);
                                  }
                                },
                              ),

                              const SizedBox(height: 16),

                              // Niveau Intermédiaire
                              LevelProgressCard(
                                title: 'Niveau Intermédiaire',
                                level: 'intermediaire',
                                accessible: intermediateProgress['accessible'],
                                attempts: intermediateProgress['attempts'],
                                bestScore: intermediateProgress['bestScore'],
                                passed: intermediateProgress['passed'],
                                inProgress: intermediateProgress['inProgress'],
                                onStart: intermediateProgress['accessible']
                                    ? () {
                                        final quizId =
                                            intermediateProgress['quizId'];
                                        if (quizId != null) {
                                          _navigateToQuiz(
                                              quizId,
                                              intermediateProgress[
                                                      'inProgress'] ==
                                                  true);
                                        }
                                      }
                                    : null,
                              ),

                              const SizedBox(height: 16),

                              // Niveau Avancé
                              LevelProgressCard(
                                title: 'Niveau Avancé',
                                level: 'avance',
                                accessible: advancedProgress['accessible'],
                                attempts: advancedProgress['attempts'],
                                bestScore: advancedProgress['bestScore'],
                                passed: advancedProgress['passed'],
                                inProgress: advancedProgress['inProgress'],
                                onStart: advancedProgress['accessible']
                                    ? () {
                                        final quizId =
                                            advancedProgress['quizId'];
                                        if (quizId != null) {
                                          _navigateToQuiz(
                                              quizId,
                                              advancedProgress['inProgress'] ==
                                                  true);
                                        }
                                      }
                                    : null,
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),
                );
              }

              return Center(
                child: Image.asset(
                  'assets/animations/loading.gif',
                  width: 64,
                  height: 64,
                  fit: BoxFit.contain,
                  color: colorScheme.primary,
                ),
              );
            },
          );
        },
      ),
    );
  }

  Widget _buildCategoryIcon(CategoryEntity category, ColorScheme colorScheme) {
    final iconUrl = category.iconUrl ?? category.name.categoryIconUrl;
    final hasIcon = iconUrl.isNotEmpty;

    if (!hasIcon) {
      return Container(
        width: 120,
        height: 120,
        decoration: BoxDecoration(
          color: colorScheme.onPrimary.withOpacity(0.2),
          shape: BoxShape.circle,
        ),
        child: Icon(
          Icons.code,
          color: colorScheme.onPrimary,
          size: 60,
        ),
      );
    }

    if (iconUrl.endsWith('.svg')) {
      return Container(
        width: 120,
        height: 120,
        padding: const EdgeInsets.all(20),
        decoration: BoxDecoration(
          color: colorScheme.surface,
          shape: BoxShape.circle,
          boxShadow: [
            BoxShadow(
              color: Colors.black.withOpacity(0.1),
              blurRadius: 8,
              offset: const Offset(0, 4),
            ),
          ],
        ),
        child: SvgPicture.network(
          iconUrl,
          fit: BoxFit.contain,
          placeholderBuilder: (context) => CircularProgressIndicator(
            strokeWidth: 2,
            valueColor: AlwaysStoppedAnimation<Color>(colorScheme.primary),
          ),
        ),
      );
    }

    return Container(
      width: 120,
      height: 120,
      decoration: BoxDecoration(
        color: colorScheme.surface,
        shape: BoxShape.circle,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 8,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: ClipOval(
        child: Image.network(
          iconUrl,
          fit: BoxFit.cover,
          errorBuilder: (_, __, ___) => Icon(
            Icons.code,
            color: colorScheme.primary,
            size: 60,
          ),
          loadingBuilder: (context, child, loadingProgress) {
            if (loadingProgress == null) return child;
            return Center(
              child: CircularProgressIndicator(
                strokeWidth: 2,
                valueColor: AlwaysStoppedAnimation<Color>(colorScheme.primary),
              ),
            );
          },
        ),
      ),
    );
  }
}

// RouteObserver global pour détecter les changements de route
final RouteObserver<ModalRoute<void>> routeObserver =
    RouteObserver<ModalRoute<void>>();
