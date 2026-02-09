import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/di/service_locator.dart';
import '../../../../core/themes/colors/app_color.dart';
import '../../domain/usecases/quiz_usecases.dart';
import '../../domain/entities/quiz_attempt_entity.dart';
import '../../domain/entities/quiz_entity.dart';
import '../../../category/data/datasources/category_remote_data_source.dart';

/// Écran de résultats du quiz
class QuizResultScreen extends StatefulWidget {
  final String quizId;
  final String attemptId;
  final Map<String, String> queryParams;

  const QuizResultScreen({
    super.key,
    required this.quizId,
    required this.attemptId,
    this.queryParams = const {},
  });

  @override
  State<QuizResultScreen> createState() => _QuizResultScreenState();
}

class _QuizResultScreenState extends State<QuizResultScreen>
    with SingleTickerProviderStateMixin {
  late final GetAttemptByIdUseCase _getAttemptUseCase;
  late final CategoryRemoteDataSource _categoryRemoteDataSource;
  QuizAttemptEntity? _attempt;
  QuizEntity? _quiz;
  String? _nextQuizId;
  bool _isLoading = true;
  String? _errorMessage;
  late AnimationController _animationController;
  late Animation<double> _scaleAnimation;
  bool _didPrecache = false;

  bool get cameFromHistory => widget.queryParams['from'] == 'history';

  @override
  void initState() {
    super.initState();
    _getAttemptUseCase = sl<GetAttemptByIdUseCase>();
    _categoryRemoteDataSource = sl<CategoryRemoteDataSource>();
    _animationController = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 800),
    );
    _scaleAnimation = CurvedAnimation(
      parent: _animationController,
      curve: Curves.elasticOut,
    );
    _loadAttempt();
  }

  @override
  void dispose() {
    _animationController.dispose();
    super.dispose();
  }

  Future<void> _loadAttempt() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    final result = await _getAttemptUseCase(widget.attemptId);

    await result.fold(
      (failure) async {
        if (mounted) {
          setState(() {
            _isLoading = false;
            _errorMessage = failure.message;
          });
        }
      },
      (result) async {
        if (mounted) {
          setState(() {
            _attempt = result.attempt;
            _quiz = result.quiz;
            _isLoading = false;
          });
          _animationController.forward();

          if (result.attempt.passed) {
            await _loadNextQuiz(result.quiz);
          }

          if (!_didPrecache) {
            _didPrecache = true;
            precacheImage(
              const AssetImage('assets/animations/confetti.gif'),
              context,
            );
          }
        }
      },
    );
  }

  Future<void> _loadNextQuiz(QuizEntity currentQuiz) async {
    try {
      String? nextLevel;
      if (currentQuiz.level == 'debutant') {
        nextLevel = 'intermediaire';
      } else if (currentQuiz.level == 'intermediaire') {
        nextLevel = 'avance';
      }

      if (nextLevel == null) return;

      final quizzes = await _categoryRemoteDataSource
          .getAvailableQuizzes(currentQuiz.categoryId);

      final nextQuiz = quizzes.firstWhere(
        (q) => q.level == nextLevel && q.isAccessible,
        orElse: () => throw Exception('Aucun quiz suivant trouvé'),
      );

      if (mounted) {
        setState(() {
          _nextQuizId = nextQuiz.id;
        });
      }
    } catch (e) {
      debugPrint('Aucun quiz suivant: $e');
    }
  }

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    if (!_didPrecache) {
      _didPrecache = true;
      precacheImage(
          const AssetImage('assets/animations/confetti.gif'), context);
    }
  }

  void _retakeQuiz() {
    final fromQuery = cameFromHistory ? '?from=history' : '';
    context.pushReplacement('/quiz/${widget.quizId}$fromQuery');
  }

  void _startNextQuiz() {
    if (_nextQuizId != null) {
      final fromQuery = cameFromHistory ? '?from=history' : '';
      context.pushReplacement('/quiz/$_nextQuizId$fromQuery');
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final isDarkMode = theme.brightness == Brightness.dark;

    final primaryColor =
        isDarkMode ? AppColors.darkPrimaryVariant : AppColors.primary;
    final errorColor =
        isDarkMode ? AppColors.darkSecondaryVariant : AppColors.error;
    final successColor = AppColors.success;
    final textSecondaryColor =
        isDarkMode ? AppColors.darkTextSecondary : AppColors.textSecondary;
    final greyColor = isDarkMode ? AppColors.grey600 : AppColors.grey400;

    return WillPopScope(
      onWillPop: () async {
        if (cameFromHistory) {
          context.go('/home');
        } else if (_quiz != null) {
          context.go('/category/${_quiz!.categoryId}');
        } else {
          context.go('/home');
        }
        return false;
      },
      child: Scaffold(
        appBar: AppBar(
          title: const Text('Résultats'),
          backgroundColor: primaryColor,
          foregroundColor: colorScheme.onPrimary,
          automaticallyImplyLeading: false,
        ),
        backgroundColor: colorScheme.background,
        body: _buildBody(
          theme: theme,
          colorScheme: colorScheme,
          primaryColor: primaryColor,
          errorColor: errorColor,
          successColor: successColor,
          textSecondaryColor: textSecondaryColor,
          greyColor: greyColor,
        ),
      ),
    );
  }

  Widget _buildBody({
    required ThemeData theme,
    required ColorScheme colorScheme,
    required Color primaryColor,
    required Color errorColor,
    required Color successColor,
    required Color textSecondaryColor,
    required Color greyColor,
  }) {
    if (_isLoading) {
      return Center(
        child: Image.asset(
          'assets/animations/loading.gif',
          width: 64,
          height: 64,
          fit: BoxFit.contain,
          color: primaryColor,
        ),
      );
    }

    if (_errorMessage != null) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.error_outline,
                size: 64,
                color: errorColor,
              ),
              const SizedBox(height: 16),
              Text(
                'Erreur',
                style: theme.textTheme.headlineSmall?.copyWith(
                  color: colorScheme.onSurface,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                _errorMessage!,
                textAlign: TextAlign.center,
                style: theme.textTheme.bodyMedium?.copyWith(
                  color: textSecondaryColor,
                ),
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: _loadAttempt,
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

    if (_attempt == null || _quiz == null) {
      return Center(
        child: Text(
          'Aucun résultat disponible',
          style: theme.textTheme.bodyLarge?.copyWith(
            color: colorScheme.onSurface,
          ),
        ),
      );
    }

    final attempt = _attempt!;
    final passed = attempt.passed;
    final scoreInt = attempt.score.round();

    final correctAnswers =
        attempt.correctAnswersCount.clamp(0, attempt.totalQuestions);
    final wrongAnswers = (attempt.totalQuestions - correctAnswers)
        .clamp(0, attempt.totalQuestions);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(24.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Icon animé
          ScaleTransition(
            scale: _scaleAnimation,
            child: Container(
              width: 160,
              height: 160,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                gradient: passed
                    ? AppColors.successGradient
                    : LinearGradient(
                        colors: [errorColor, errorColor.withOpacity(0.7)],
                      ),
              ),
              child: Center(
                child: passed
                    ? Stack(
                        alignment: Alignment.center,
                        children: [
                          Image.asset(
                            'assets/animations/confetti.gif',
                            width: 160,
                            height: 160,
                            fit: BoxFit.cover,
                          ),
                        ],
                      )
                    : const Icon(
                        Icons.close,
                        size: 80,
                        color: Colors.white,
                      ),
              ),
            ),
          ),

          const SizedBox(height: 24),

          // Titre
          Text(
            passed ? 'Félicitations !' : 'Oups !',
            style: theme.textTheme.headlineLarge?.copyWith(
              fontWeight: FontWeight.bold,
              color: passed ? successColor : errorColor,
            ),
            textAlign: TextAlign.center,
          ),

          const SizedBox(height: 8),

          // Message
          Text(
            passed
                ? 'Vous avez réussi ce quiz avec brio !'
                : 'Continuez à vous entraîner, vous progressez !',
            style: theme.textTheme.bodyLarge?.copyWith(
              color: textSecondaryColor,
            ),
            textAlign: TextAlign.center,
          ),

          const SizedBox(height: 32),

          // Score
          Container(
            padding: const EdgeInsets.all(24.0),
            decoration: BoxDecoration(
              color: passed
                  ? successColor.withOpacity(0.1)
                  : errorColor.withOpacity(0.1),
              borderRadius: BorderRadius.circular(16),
              border: Border.all(
                color: passed
                    ? successColor.withOpacity(0.3)
                    : errorColor.withOpacity(0.3),
                width: 2,
              ),
            ),
            child: Column(
              children: [
                Text(
                  'Votre score',
                  style: theme.textTheme.titleMedium?.copyWith(
                    color: textSecondaryColor,
                  ),
                ),
                const SizedBox(height: 8),
                Text(
                  '$scoreInt%',
                  style: theme.textTheme.displayLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                    color: passed ? successColor : errorColor,
                  ),
                ),
              ],
            ),
          ),

          const SizedBox(height: 24),

          // Statistiques détaillées
          Row(
            children: [
              Expanded(
                child: _buildStatCard(
                  icon: Icons.check_circle,
                  label: 'Bonnes réponses',
                  value: '$correctAnswers/${attempt.totalQuestions}',
                  color: successColor,
                  theme: theme,
                ),
              ),
              const SizedBox(width: 16),
              Expanded(
                child: _buildStatCard(
                  icon: Icons.cancel,
                  label: 'Mauvaises réponses',
                  value: '$wrongAnswers/${attempt.totalQuestions}',
                  color: errorColor,
                  theme: theme,
                ),
              ),
            ],
          ),

          const SizedBox(height: 32),

          // Boutons d'action
          if (passed) ...[
            if (_nextQuizId != null) ...[
              ElevatedButton.icon(
                onPressed: _startNextQuiz,
                icon: const Icon(Icons.arrow_forward),
                label: const Text('Niveau suivant'),
                style: ElevatedButton.styleFrom(
                  backgroundColor: successColor,
                  foregroundColor: Colors.white,
                  padding: const EdgeInsets.symmetric(vertical: 16),
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                ),
              ),
              const SizedBox(height: 12),
            ],
            OutlinedButton.icon(
              onPressed: () {
                final from = cameFromHistory ? '&from=history' : '';
                context.push(
                  '/quiz/${widget.quizId}/review?attemptId=${widget.attemptId}$from',
                );
              },
              icon: const Icon(Icons.visibility),
              label: const Text('Voir les réponses'),
              style: OutlinedButton.styleFrom(
                foregroundColor: primaryColor,
                padding: const EdgeInsets.symmetric(vertical: 16),
                side: BorderSide(color: primaryColor, width: 2),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),
          ] else ...[
            ElevatedButton.icon(
              onPressed: _retakeQuiz,
              icon: const Icon(Icons.replay),
              label: const Text('Réessayer'),
              style: ElevatedButton.styleFrom(
                backgroundColor: primaryColor,
                foregroundColor: colorScheme.onPrimary,
                padding: const EdgeInsets.symmetric(vertical: 16),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),
            const SizedBox(height: 12),
            OutlinedButton.icon(
              onPressed: () {
                final from = cameFromHistory ? '&from=history' : '';
                context.push(
                  '/quiz/${widget.quizId}/review?attemptId=${widget.attemptId}$from',
                );
              },
              icon: const Icon(Icons.visibility),
              label: const Text('Voir les réponses'),
              style: OutlinedButton.styleFrom(
                foregroundColor: primaryColor,
                padding: const EdgeInsets.symmetric(vertical: 16),
                side: BorderSide(color: primaryColor, width: 2),
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                ),
              ),
            ),
          ],

          const SizedBox(height: 12),

          // Bouton adapté selon la provenance
          ElevatedButton(
            onPressed: () {
              if (cameFromHistory) {
                context.go('/home');
              } else if (_quiz != null) {
                context.go('/category/${_quiz!.categoryId}');
              } else {
                context.go('/home');
              }
            },
            style: ElevatedButton.styleFrom(
              backgroundColor: primaryColor,
              foregroundColor: colorScheme.onPrimary,
              padding: const EdgeInsets.symmetric(vertical: 16),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
              ),
            ),
            child: Text(
              cameFromHistory ? 'Retour à l\'accueil' : 'Retour à la catégorie',
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildStatCard({
    required IconData icon,
    required String label,
    required String value,
    required Color color,
    required ThemeData theme,
  }) {
    final isDarkMode = theme.brightness == Brightness.dark;
    final textSecondaryColor =
        isDarkMode ? AppColors.darkTextSecondary : AppColors.textSecondary;

    return Container(
      padding: const EdgeInsets.all(16.0),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(12),
        border: Border.all(
          color: color.withOpacity(0.3),
        ),
      ),
      child: Column(
        children: [
          Icon(icon, color: color, size: 32),
          const SizedBox(height: 8),
          Text(
            value,
            style: theme.textTheme.titleLarge?.copyWith(
              fontWeight: FontWeight.bold,
              color: color,
            ),
          ),
          const SizedBox(height: 4),
          Text(
            label,
            style: theme.textTheme.bodySmall?.copyWith(
              color: textSecondaryColor,
            ),
            textAlign: TextAlign.center,
          ),
        ],
      ),
    );
  }
}
