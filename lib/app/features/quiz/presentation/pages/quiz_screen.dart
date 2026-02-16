import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:go_router/go_router.dart';

import '../../../../core/utils/app_extensions.dart';
import '../../../../core/themes/colors/app_color.dart';
import '../bloc/quiz_bloc.dart';
import '../bloc/quiz_event.dart';
import '../bloc/quiz_state.dart';
import '../../../quiz/domain/entities/quiz_attempt_entity.dart';
import '../../../quiz/data/models/user_answer_model.dart';

/// Écran de quiz avec navigation question par question
class QuizScreen extends StatefulWidget {
  final String quizId;

  const QuizScreen({super.key, required this.quizId});

  @override
  State<QuizScreen> createState() => _QuizScreenState();
}

class _QuizScreenState extends State<QuizScreen> {
  int _currentIndex = 0;
  bool _hasInitializedIndex = false;

  @override
  void initState() {
    super.initState();
  }

  void _onSelectAnswer(
    QuizBloc bloc,
    String questionId,
    List<String> selected,
  ) {
    bloc.add(QuizAnswerUpdated(
      questionId: questionId,
      selectedAnswerIds: selected,
    ));
  }

  void _onNext() {
    setState(() {
      _currentIndex += 1;
    });
  }

  void _onPrevious() {
    setState(() {
      _currentIndex = (_currentIndex - 1).clamp(0, _currentIndex);
    });
  }

  /// Vérifie si la question actuelle a une réponse
  bool _hasCurrentAnswer(QuizInProgress state) {
    final localAttempt = state.localAttempt;
    if (localAttempt == null) return false;

    final currentQuestion = state.quiz.questions[_currentIndex];

    try {
      final userAnswer = localAttempt.answers.firstWhere(
        (a) => a.questionId == currentQuestion.id,
      );
      return userAnswer.selectedAnswerIds.isNotEmpty;
    } catch (_) {
      return false;
    }
  }

  /// Soumettre le quiz avec le BON attemptId
  void _onSubmit(QuizBloc bloc, QuizInProgress state) {
    final localAttempt = state.localAttempt;

    if (localAttempt == null) {
      context.showErrorSnackBar('Erreur: tentative non trouvée');
      return;
    }

    final attemptId = localAttempt.remoteAttemptId ?? localAttempt.localId;

    if (attemptId.isEmpty) {
      context.showErrorSnackBar('Erreur: ID de tentative manquant');
      return;
    }

    final quiz = state.quiz;
    final allQuestions = quiz.questions;

    final answers = allQuestions.map((question) {
      try {
        final userAnswer = localAttempt.answers.firstWhere(
          (a) => a.questionId == question.id,
        );
        return UserAnswer(
          questionId: question.id,
          selectedAnswerIds: userAnswer.selectedAnswerIds,
        );
      } catch (_) {
        return UserAnswer(
          questionId: question.id,
          selectedAnswerIds: [],
        );
      }
    }).toList();

    debugPrint('🚀 Soumission du quiz avec attemptId: $attemptId');
    debugPrint('📝 Nombre de questions: ${answers.length}');

    bloc.add(QuizSubmitRequested(
      attemptId: attemptId,
      quizId: quiz.id,
      answers: answers,
    ));
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final colorScheme = theme.colorScheme;
    final isDarkMode = theme.brightness == Brightness.dark;

    return Scaffold(
      appBar: AppBar(
        title: BlocBuilder<QuizBloc, QuizState>(
          builder: (context, state) {
            if (state is QuizInProgress) {
              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  Text(
                    'Quiz',
                    style: TextStyle(
                      color: colorScheme.onPrimary,
                      fontSize: 16,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                  Text(
                    state.quiz.title,
                    style: TextStyle(
                      color: colorScheme.onPrimary.withOpacity(0.8),
                      fontSize: 12,
                      fontWeight: FontWeight.normal,
                    ),
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                  ),
                ],
              );
            }
            return const Text('Quiz');
          },
        ),
        backgroundColor: colorScheme.primary,
        foregroundColor: colorScheme.onPrimary,
        automaticallyImplyLeading: false,
      ),
      body: BlocConsumer<QuizBloc, QuizState>(
        listener: (context, state) {
          if (state is QuizSubmitted) {
            context.pushReplacement(
              '/quiz/${state.result.quizId}/result?attemptId=${state.result.id}',
            );
          } else if (state is QuizError) {
            context.showErrorSnackBar(state.message);
          }
        },
        builder: (context, state) {
          if (state is QuizLoading || state is QuizInitial) {
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

          if (state is QuizInProgress) {
            if (!_hasInitializedIndex) {
              _currentIndex = state.currentQuestionIndex;
              _hasInitializedIndex = true;
            }

            final quiz = state.quiz;
            final questions = quiz.questions;

            if (questions.isEmpty) {
              return Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      Icons.error_outline,
                      size: 64,
                      color: colorScheme.error,
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'Aucune question disponible',
                      style: context.textTheme.titleLarge?.copyWith(
                        color: colorScheme.onSurface,
                      ),
                    ),
                    const SizedBox(height: 24),
                    ElevatedButton(
                      onPressed: () => context.go('/home'),
                      child: const Text('Retour à l\'accueil'),
                    ),
                  ],
                ),
              );
            }

            if (_currentIndex >= questions.length) {
              _currentIndex = questions.length - 1;
            }

            final q = questions[_currentIndex];
            final localAttempt = state.localAttempt;

            List<String> selected = [];
            if (localAttempt != null) {
              try {
                final found = localAttempt.answers.firstWhere(
                  (a) => a.questionId == q.id,
                  orElse: () => UserAnswerModel(
                    questionId: q.id,
                    selectedAnswerIds: [],
                  ),
                );
                selected = found.selectedAnswerIds;
              } catch (_) {
                selected = [];
              }
            }

            final progress = (_currentIndex + 1) / questions.length;
            final bloc = context.read<QuizBloc>();
            final hasAnswer = _hasCurrentAnswer(state);
            final infoColor =
                isDarkMode ? AppColors.darkPrimaryVariant : AppColors.info;

            return Column(
              children: [
                // Barre de progression
                Container(
                  height: 6,
                  color: colorScheme.surfaceVariant,
                  child: LinearProgressIndicator(
                    value: progress,
                    backgroundColor: Colors.transparent,
                    valueColor: AlwaysStoppedAnimation<Color>(
                      colorScheme.primary,
                    ),
                  ),
                ),
                // Header
                Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 12,
                          vertical: 6,
                        ),
                        decoration: BoxDecoration(
                          color: colorScheme.primary.withOpacity(0.1),
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Text(
                          'Question ${_currentIndex + 1}/${questions.length}',
                          style: context.textTheme.titleSmall?.copyWith(
                            color: colorScheme.primary,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 12,
                          vertical: 6,
                        ),
                        decoration: BoxDecoration(
                          color: _getLevelColor(quiz.level, context)
                              .withOpacity(0.1),
                          borderRadius: BorderRadius.circular(20),
                        ),
                        child: Text(
                          quiz.level.capitalize,
                          style: context.textTheme.labelLarge?.copyWith(
                            color: _getLevelColor(quiz.level, context),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 32),

                Expanded(
                  child: Center(
                    child: SingleChildScrollView(
                      padding: const EdgeInsets.all(16.0),
                      child: ConstrainedBox(
                        constraints: const BoxConstraints(maxWidth: 600),
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            // Question
                            Text(
                              q.text,
                              textAlign: TextAlign.center,
                              style: context.textTheme.titleLarge?.copyWith(
                                fontWeight: FontWeight.w600,
                                color: colorScheme.onSurface,
                              ),
                            ),

                            const SizedBox(height: 8),

                            // Indicateur de réponses multiples
                            if (q.allowsMultipleAnswers)
                              Text(
                                'Plusieurs réponses possibles',
                                textAlign: TextAlign.center,
                                style: context.textTheme.bodySmall?.copyWith(
                                  color: infoColor,
                                  fontStyle: FontStyle.italic,
                                ),
                              ),

                            const SizedBox(height: 32),

                            // Réponses
                            ListView.separated(
                              shrinkWrap: true,
                              physics: const NeverScrollableScrollPhysics(),
                              itemCount: q.answers.length,
                              separatorBuilder: (_, __) =>
                                  const SizedBox(height: 8),
                              itemBuilder: (context, index) {
                                final ans = q.answers[index];
                                final isSelected = selected.contains(ans.id);

                                if (q.allowsMultipleAnswers) {
                                  return _buildCheckboxAnswer(
                                    bloc: bloc,
                                    answer: ans,
                                    isSelected: isSelected,
                                    questionId: q.id,
                                    currentSelected: selected,
                                    colorScheme: colorScheme,
                                  );
                                } else {
                                  return _buildRadioAnswer(
                                    bloc: bloc,
                                    answer: ans,
                                    isSelected: isSelected,
                                    questionId: q.id,
                                    currentSelected: selected,
                                    colorScheme: colorScheme,
                                  );
                                }
                              },
                            ),

                            const SizedBox(height: 32),
                          ],
                        ),
                      ),
                    ),
                  ),
                ),

                // Navigation
                Padding(
                  padding: const EdgeInsets.all(20.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      if (_currentIndex > 0)
                        OutlinedButton.icon(
                          onPressed: _onPrevious,
                          icon: const Icon(Icons.arrow_back),
                          label: const Text('Précédent'),
                          style: OutlinedButton.styleFrom(
                            foregroundColor: colorScheme.primary,
                          ),
                        )
                      else
                        const SizedBox.shrink(),
                      if (_currentIndex < questions.length - 1)
                        ElevatedButton.icon(
                          onPressed: hasAnswer ? _onNext : null,
                          icon: const Icon(Icons.arrow_forward),
                          label: const Text('Suivant'),
                        )
                      else
                        ElevatedButton.icon(
                          onPressed:
                              hasAnswer ? () => _onSubmit(bloc, state) : null,
                          style: ElevatedButton.styleFrom(
                            backgroundColor: AppColors.success,
                          ),
                          icon: const Icon(Icons.check_circle),
                          label: const Text('Terminer'),
                        ),
                    ],
                  ),
                ),
              ],
            );
          }

          if (state is QuizSubmitting) {
            return Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Image.asset(
                    'assets/animations/loading.gif',
                    width: 48,
                    height: 48,
                    fit: BoxFit.contain,
                    color: colorScheme.primary,
                  ),
                  const SizedBox(height: 16),
                  Text(
                    'Envoi des réponses...',
                    style: context.textTheme.titleMedium?.copyWith(
                      color: colorScheme.onSurface,
                    ),
                  ),
                ],
              ),
            );
          }

          if (state is QuizError) {
            return Center(
              child: Padding(
                padding: const EdgeInsets.all(24.0),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(
                      Icons.error_outline,
                      size: 64,
                      color: colorScheme.error,
                    ),
                    const SizedBox(height: 16),
                    Text(
                      'Erreur',
                      style: context.textTheme.headlineSmall?.copyWith(
                        color: colorScheme.onSurface,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      state.message,
                      textAlign: TextAlign.center,
                      style: context.textTheme.bodyMedium?.copyWith(
                        color: colorScheme.onSurface.withOpacity(0.7),
                      ),
                    ),
                    const SizedBox(height: 24),
                    ElevatedButton(
                      onPressed: () => context.go('/home'),
                      child: const Text('Retour à l\'accueil'),
                    ),
                  ],
                ),
              ),
            );
          }

          return const SizedBox.shrink();
        },
      ),
    );
  }

  Widget _buildCheckboxAnswer({
    required QuizBloc bloc,
    required dynamic answer,
    required bool isSelected,
    required String questionId,
    required List<String> currentSelected,
    required ColorScheme colorScheme,
  }) {
    return Card(
      elevation: isSelected ? 4 : 1,
      color: colorScheme.surface,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(
          color: isSelected
              ? colorScheme.primary
              : colorScheme.outline.withOpacity(0.2),
          width: 2,
        ),
      ),
      child: CheckboxListTile(
        value: isSelected,
        title: Text(
          answer.text,
          style: TextStyle(color: colorScheme.onSurface),
        ),
        controlAffinity: ListTileControlAffinity.leading,
        activeColor: colorScheme.primary,
        onChanged: (val) {
          final nextSelected = List<String>.from(currentSelected);
          if (val == true) {
            nextSelected.add(answer.id);
          } else {
            nextSelected.remove(answer.id);
          }
          _onSelectAnswer(bloc, questionId, nextSelected);
        },
      ),
    );
  }

  Widget _buildRadioAnswer({
    required QuizBloc bloc,
    required dynamic answer,
    required bool isSelected,
    required String questionId,
    required List<String> currentSelected,
    required ColorScheme colorScheme,
  }) {
    return Card(
      elevation: isSelected ? 4 : 1,
      color: colorScheme.surface,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(
          color: isSelected
              ? colorScheme.primary
              : colorScheme.outline.withOpacity(0.2),
          width: 2,
        ),
      ),
      child: RadioListTile<String>(
        value: answer.id,
        groupValue: currentSelected.isNotEmpty ? currentSelected.first : null,
        title: Text(
          answer.text,
          style: TextStyle(color: colorScheme.onSurface),
        ),
        activeColor: colorScheme.primary,
        onChanged: (val) {
          _onSelectAnswer(bloc, questionId, val != null ? [val] : []);
        },
      ),
    );
  }

  Color _getLevelColor(String level, BuildContext context) {
    final theme = Theme.of(context);
    final isDarkMode = theme.brightness == Brightness.dark;

    switch (level.toLowerCase()) {
      case 'debutant':
        return isDarkMode ? AppColors.success : AppColors.levelBeginner;
      case 'intermediaire':
        return isDarkMode
            ? AppColors.darkPrimaryVariant
            : AppColors.levelIntermediate;
      case 'avance':
        return isDarkMode
            ? AppColors.darkSecondaryVariant
            : AppColors.levelAdvanced;
      default:
        return Theme.of(context).colorScheme.primary;
    }
  }
}
