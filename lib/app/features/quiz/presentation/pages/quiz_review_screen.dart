import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../../core/routing/app_router.dart';

import '../../../../core/di/service_locator.dart';
import '../../../../core/themes/colors/app_color.dart';
import '../../domain/usecases/quiz_usecases.dart';
import '../../domain/entities/quiz_entity.dart';
import '../../domain/entities/quiz_attempt_entity.dart';
import '../../domain/entities/question_entity.dart';

/// Écran de révision détaillée des réponses
class QuizReviewScreen extends StatefulWidget {
  final String? quizId;
  final String attemptId;
  final bool cameFromHistory;

  const QuizReviewScreen({
    super.key,
    this.quizId,
    required this.attemptId,
    this.cameFromHistory = false,
  });

  @override
  State<QuizReviewScreen> createState() => _QuizReviewScreenState();
}

class _QuizReviewScreenState extends State<QuizReviewScreen> {
  late final GetAttemptByIdUseCase _getAttemptUseCase;

  QuizEntity? _quiz;
  QuizAttemptEntity? _attempt;
  List<QuestionEntity>? _questions;
  bool _isLoading = true;
  String? _errorMessage;

  @override
  void initState() {
    super.initState();
    _getAttemptUseCase = sl<GetAttemptByIdUseCase>();
    _loadData();
  }

  Future<void> _loadData() async {
    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    final result = await _getAttemptUseCase(widget.attemptId);

    result.fold(
      (failure) {
        if (mounted) {
          setState(() {
            _isLoading = false;
            _errorMessage = failure.message;
          });
        }
      },
      (data) {
        if (mounted) {
          setState(() {
            _attempt = data.attempt;
            _quiz = data.quiz;
            _questions = data.questions;
            _isLoading = false;
          });
        }
      },
    );
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

    return Scaffold(
      appBar: AppBar(
        title: const Text('Révision'),
        backgroundColor: primaryColor,
        foregroundColor: colorScheme.onPrimary,
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
                onPressed: _loadData,
                child: const Text('Réessayer'),
              ),
              const SizedBox(height: 16),
              OutlinedButton(
                onPressed: () {
                  if (widget.cameFromHistory) {
                    context.go(AppRouter.history);
                  } else {
                    context.pop();
                  }
                },
                child: const Text('Retour'),
              ),
            ],
          ),
        ),
      );
    }

    if (_quiz == null || _attempt == null || _questions == null) {
      return Center(
        child: Text(
          'Données non disponibles',
          style: theme.textTheme.bodyLarge?.copyWith(
            color: colorScheme.onSurface,
          ),
        ),
      );
    }

    final quiz = _quiz!;
    final attempt = _attempt!;
    final questions = _questions!;

    if (questions.isEmpty) {
      return Center(
        child: Padding(
          padding: const EdgeInsets.all(24.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.quiz_outlined,
                size: 80,
                color: greyColor,
              ),
              const SizedBox(height: 16),
              Text(
                'Aucune question à réviser',
                style: theme.textTheme.titleLarge?.copyWith(
                  color: colorScheme.onSurface,
                ),
              ),
              const SizedBox(height: 24),
              ElevatedButton(
                onPressed: () {
                  if (widget.cameFromHistory) {
                    context.go(AppRouter.history);
                  } else {
                    context.pop();
                  }
                },
                child: const Text('Retour'),
              ),
            ],
          ),
        ),
      );
    }

    return Column(
      children: [
        // Header avec score
        Container(
          width: double.infinity,
          padding: const EdgeInsets.all(16.0),
          decoration: BoxDecoration(
            gradient: attempt.passed
                ? AppColors.successGradient
                : LinearGradient(
                    colors: [errorColor, errorColor.withOpacity(0.7)],
                  ),
          ),
          child: SafeArea(
            bottom: false,
            child: Column(
              children: [
                Text(
                  quiz.title,
                  style: theme.textTheme.titleLarge?.copyWith(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                  ),
                  textAlign: TextAlign.center,
                ),
                const SizedBox(height: 8),
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 8,
                      ),
                      decoration: BoxDecoration(
                        color: Colors.white.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Text(
                        'Score: ${attempt.score.round()}%',
                        style: theme.textTheme.titleMedium?.copyWith(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 8,
                      ),
                      decoration: BoxDecoration(
                        color: Colors.white.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: Text(
                        '${attempt.correctAnswersCount}/${attempt.totalQuestions}',
                        style: theme.textTheme.titleMedium?.copyWith(
                          color: Colors.white,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),

        // Liste des questions
        Expanded(
          child: ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: questions.length,
            itemBuilder: (context, index) {
              final question = questions[index];
              final userAnswer = attempt.answers.firstWhere(
                (a) => a.questionId == question.id,
                orElse: () => UserAnswer(
                  questionId: question.id,
                  selectedAnswerIds: [],
                ),
              );

              // Vérifier si la réponse est correcte
              final correctAnswerIds = question.answers
                  .where((a) => a.isCorrect)
                  .map((a) => a.id)
                  .toSet();
              final selectedIds = userAnswer.selectedAnswerIds.toSet();
              final isCorrect = correctAnswerIds.containsAll(selectedIds) &&
                  selectedIds.containsAll(correctAnswerIds);

              return Card(
                margin: const EdgeInsets.only(bottom: 16),
                color: colorScheme.surface,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(12),
                  side: BorderSide(
                    color: isCorrect
                        ? successColor.withOpacity(0.5)
                        : errorColor.withOpacity(0.5),
                    width: 2,
                  ),
                ),
                child: Padding(
                  padding: const EdgeInsets.all(16.0),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      // En-tête question
                      Row(
                        children: [
                          Container(
                            width: 32,
                            height: 32,
                            decoration: BoxDecoration(
                              color: isCorrect ? successColor : errorColor,
                              shape: BoxShape.circle,
                            ),
                            child: Center(
                              child: Text(
                                '${index + 1}',
                                style: theme.textTheme.titleSmall?.copyWith(
                                  color: Colors.white,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                          ),
                          const SizedBox(width: 12),
                          Expanded(
                            child: Text(
                              question.text,
                              style: theme.textTheme.titleMedium?.copyWith(
                                fontWeight: FontWeight.w600,
                                color: colorScheme.onSurface,
                              ),
                            ),
                          ),
                          Icon(
                            isCorrect ? Icons.check_circle : Icons.cancel,
                            color: isCorrect ? successColor : errorColor,
                            size: 28,
                          ),
                        ],
                      ),

                      const SizedBox(height: 16),

                      // Liste des réponses
                      ...question.answers.map((answer) {
                        final wasSelected = selectedIds.contains(answer.id);
                        final isCorrectAnswer = answer.isCorrect;

                        Color backgroundColor;
                        Color borderColor;
                        IconData? icon;

                        if (wasSelected && isCorrectAnswer) {
                          // Bonne réponse sélectionnée
                          backgroundColor = successColor.withOpacity(0.1);
                          borderColor = successColor;
                          icon = Icons.check_circle;
                        } else if (wasSelected && !isCorrectAnswer) {
                          // Mauvaise réponse sélectionnée
                          backgroundColor = errorColor.withOpacity(0.1);
                          borderColor = errorColor;
                          icon = Icons.cancel;
                        } else if (!wasSelected && isCorrectAnswer) {
                          // Bonne réponse non sélectionnée
                          backgroundColor = successColor.withOpacity(0.05);
                          borderColor = successColor.withOpacity(0.5);
                          icon = Icons.check_circle_outline;
                        } else {
                          // Mauvaise réponse non sélectionnée
                          backgroundColor = Colors.transparent;
                          borderColor = greyColor;
                          icon = null;
                        }

                        return Container(
                          margin: const EdgeInsets.only(bottom: 8),
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: backgroundColor,
                            borderRadius: BorderRadius.circular(8),
                            border: Border.all(color: borderColor, width: 2),
                          ),
                          child: Row(
                            children: [
                              if (icon != null) ...[
                                Icon(
                                  icon,
                                  color: isCorrectAnswer
                                      ? successColor
                                      : errorColor,
                                  size: 20,
                                ),
                                const SizedBox(width: 8),
                              ],
                              Expanded(
                                child: Text(
                                  answer.text,
                                  style: theme.textTheme.bodyMedium?.copyWith(
                                    fontWeight: (wasSelected || isCorrectAnswer)
                                        ? FontWeight.w600
                                        : FontWeight.normal,
                                    color: colorScheme.onSurface,
                                  ),
                                ),
                              ),
                            ],
                          ),
                        );
                      }),
                    ],
                  ),
                ),
              );
            },
          ),
        ),

        // Bottom return button
        SafeArea(
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: ElevatedButton(
              onPressed: () {
                context.pop();
              },
              style: ElevatedButton.styleFrom(
                padding: const EdgeInsets.symmetric(vertical: 16),
                minimumSize: const Size(double.infinity, 0),
                backgroundColor: primaryColor,
                foregroundColor: colorScheme.onPrimary,
              ),
              child: Text(widget.cameFromHistory
                  ? 'Retour à l\'historique'
                  : 'Retour aux résultats'),
            ),
          ),
        ),
      ],
    );
  }
}
