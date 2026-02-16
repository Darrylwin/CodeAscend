import 'dart:async';

import 'package:flutter/material.dart' show debugPrint;
import 'package:flutter_bloc/flutter_bloc.dart';

import '../../domain/usecases/quiz_usecases.dart';
import '../../domain/entities/quiz_entity.dart';
import '../../../quiz/data/datasources/quiz_local_data_source.dart';
import '../../../quiz/data/datasources/quiz_remote_data_source.dart';
import '../../../quiz/data/models/user_answer_model.dart';
import '../../../quiz/data/models/quiz_attempt_model.dart';
import '../../../../core/di/service_locator.dart';
import '../../../auth/data/datasources/auth_local_data_source.dart';
import '../../../attempts/presentation/bloc/attempts_bloc.dart';
import '../../../attempts/presentation/bloc/attempts_event.dart';
import 'quiz_event.dart';
import 'quiz_state.dart';

class QuizBloc extends Bloc<QuizEvent, QuizState> {
  final SubmitQuizUseCase _submitQuiz;
  final FlushPendingSubmissionsUseCase _flushPending;
  final QuizLocalDataSource _local;
  final QuizRemoteDataSource _remote;

  QuizBloc({
    required GetQuizByIdUseCase getQuizByIdUseCase,
    required StartQuizUseCase startQuizUseCase,
    required SubmitQuizUseCase submitQuizUseCase,
    required FlushPendingSubmissionsUseCase flushPendingUseCase,
    required QuizLocalDataSource localDataSource,
    required QuizRemoteDataSource remoteDataSource,
  })  : _submitQuiz = submitQuizUseCase,
        _flushPending = flushPendingUseCase,
        _local = localDataSource,
        _remote = remoteDataSource,
        super(const QuizInitial()) {
    on<QuizLoadRequested>(_onLoadRequested);
    on<QuizRestoreRequested>(_onRestoreRequested);
    on<QuizAnswerUpdated>(_onAnswerUpdated);
    on<QuizSubmitRequested>(_onSubmitRequested);
    on<QuizFlushPendingRequested>(_onFlushPendingRequested);
  }

  Future<void> _onLoadRequested(
      QuizLoadRequested event, Emitter<QuizState> emit) async {
    emit(const QuizLoading());

    try {
      final result = await _remote.startQuiz(quizId: event.quizId);

      final quizWithQuestions = QuizEntity(
        id: result.quiz.id,
        categoryId: result.quiz.categoryId,
        title: result.quiz.title,
        level: result.quiz.level,
        questionCount: result.questions.length,
        status: result.quiz.status,
        createdAt: result.quiz.createdAt,
        questions: result.questions,
      );

      final authLocal = sl<AuthLocalDataSource>();
      final userId = await authLocal.getCurrentUserId() ?? '';

      final localAttempt = QuizAttemptModel(
        localId: 'local_${DateTime.now().millisecondsSinceEpoch}',
        remoteAttemptId: result.attemptId,
        quizId: event.quizId,
        userId: userId,
        answers: [],
        status: AttemptStatus.inProgress,
      );

      await _local.saveInProgressAttempt(localAttempt);

      if (emit.isDone) return;

      emit(QuizInProgress(
        quiz: quizWithQuestions,
        localAttempt: localAttempt,
        currentQuestionIndex: 0,
      ));
    } catch (e) {
      if (emit.isDone) return;
      emit(QuizError('Erreur lors du chargement du quiz: $e'));
    }
  }

  Future<void> _onRestoreRequested(
      QuizRestoreRequested event, Emitter<QuizState> emit) async {
    emit(const QuizLoading());

    try {
      final existingAttempt = await _local.getInProgressAttempt(event.quizId);

      final result = await _remote.startQuiz(quizId: event.quizId);

      final quizWithQuestions = QuizEntity(
        id: result.quiz.id,
        categoryId: result.quiz.categoryId,
        title: result.quiz.title,
        level: result.quiz.level,
        questionCount: result.questions.length,
        status: result.quiz.status,
        createdAt: result.quiz.createdAt,
        questions: result.questions,
      );

      if (existingAttempt != null && existingAttempt.remoteAttemptId != null) {
        final currentQuestionIndex = existingAttempt.answers.length
            .clamp(0, result.questions.length - 1);

        if (emit.isDone) return;

        emit(QuizInProgress(
          quiz: quizWithQuestions,
          localAttempt: existingAttempt,
          currentQuestionIndex: currentQuestionIndex,
        ));
      } else {
        final authLocal = sl<AuthLocalDataSource>();
        final userId = await authLocal.getCurrentUserId() ?? '';

        final localAttempt = QuizAttemptModel(
          localId: 'local_${DateTime.now().millisecondsSinceEpoch}',
          remoteAttemptId: result.attemptId,
          quizId: event.quizId,
          userId: userId,
          answers: [],
          status: AttemptStatus.inProgress,
        );

        await _local.saveInProgressAttempt(localAttempt);

        if (emit.isDone) return;

        emit(QuizInProgress(
          quiz: quizWithQuestions,
          localAttempt: localAttempt,
          currentQuestionIndex: 0,
        ));
      }
    } catch (e) {
      if (emit.isDone) return;
      emit(QuizError('Erreur lors de la restauration: $e'));
    }
  }

  Future<void> _onAnswerUpdated(
      QuizAnswerUpdated event, Emitter<QuizState> emit) async {
    final current = state;
    if (current is! QuizInProgress) return;

    final attempt = current.localAttempt;
    if (attempt == null) return;

    final updatedAnswers = List<UserAnswerModel>.from(attempt.answers);
    final index =
        updatedAnswers.indexWhere((a) => a.questionId == event.questionId);

    if (index >= 0) {
      updatedAnswers[index] = UserAnswerModel(
        questionId: event.questionId,
        selectedAnswerIds: event.selectedAnswerIds,
      );
    } else {
      updatedAnswers.add(UserAnswerModel(
        questionId: event.questionId,
        selectedAnswerIds: event.selectedAnswerIds,
      ));
    }

    final updatedAttempt = QuizAttemptModel(
      localId: attempt.localId,
      remoteAttemptId: attempt.remoteAttemptId,
      quizId: attempt.quizId,
      userId: attempt.userId,
      answers: updatedAnswers,
      status: attempt.status,
      score: attempt.score,
      passed: attempt.passed,
      createdAt: attempt.createdAt,
      updatedAt: DateTime.now(),
      completedAt: attempt.completedAt,
    );

    await _local.saveInProgressAttempt(updatedAttempt);

    if (emit.isDone) return;

    emit(QuizInProgress(
      quiz: current.quiz,
      localAttempt: updatedAttempt,
      currentQuestionIndex: current.currentQuestionIndex,
    ));
  }

  Future<void> _onSubmitRequested(
      QuizSubmitRequested event, Emitter<QuizState> emit) async {
    emit(const QuizSubmitting());

    final submitEither = await _submitQuiz.call(
      attemptId: event.attemptId,
      quizId: event.quizId,
      answers: event.answers,
    );

    if (emit.isDone) return;

    submitEither.fold(
      (failure) => emit(QuizError(failure.message)),
      (attemptEntity) {
        emit(QuizSubmitted(result: attemptEntity, queued: false));

        // Nettoyer le cache local
        _local.clearInProgressAttempt(attemptEntity.quizId).catchError((_) {});

        // Invalider le cache AttemptsBloc pour forcer un refresh
        // au prochain affichage de l'historique ou du détail catégorie
        try {
          if (sl.isRegistered<AttemptsBloc>()) {
            sl<AttemptsBloc>()
                .add(const InvalidateAttempts(forceReload: false));
            debugPrint('🗑️ QuizBloc: AttemptsBloc invalidé après soumission');
          }
        } catch (e) {
          debugPrint('⚠️ QuizBloc: impossible d\'invalider AttemptsBloc: $e');
        }
      },
    );
  }

  Future<void> _onFlushPendingRequested(
      QuizFlushPendingRequested event, Emitter<QuizState> emit) async {
    final result = await _flushPending.call();
    result.fold(
      (failure) => debugPrint('❌ Échec flush pending: ${failure.message}'),
      (count) {
        if (count > 0) debugPrint('✅ $count tentative(s) synchronisée(s)');
      },
    );
  }

  @override
  Future<void> close() => super.close();
}
