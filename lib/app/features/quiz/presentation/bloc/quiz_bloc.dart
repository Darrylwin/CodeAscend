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
import 'quiz_event.dart';
import 'quiz_state.dart';

/// Bloc qui gère le déroulé d'un quiz (chargement, réponses, sauvegarde locale, soumission)
class QuizBloc extends Bloc<QuizEvent, QuizState> {
  final GetQuizByIdUseCase _getQuizById;
  final StartQuizUseCase _startQuiz;
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
  })  : _getQuizById = getQuizByIdUseCase,
        _startQuiz = startQuizUseCase,
        _submitQuiz = submitQuizUseCase,
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
      // Appeler directement le remote data source pour obtenir quiz + questions + attemptId
      final result = await _remote.startQuiz(quizId: event.quizId);

      // Créer le QuizEntity complet avec les questions
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

      // Créer ou mettre à jour la tentative locale avec le BON attemptId
      final authLocal = sl<AuthLocalDataSource>();
      final userId = await authLocal.getCurrentUserId() ?? '';

      final localAttempt = QuizAttemptModel(
        localId: 'local_${DateTime.now().millisecondsSinceEpoch}',
        remoteAttemptId:
            result.attemptId, // ← IMPORTANT: Utiliser l'attemptId de l'API
        quizId: event.quizId,
        userId: userId,
        answers: [],
        status: AttemptStatus.inProgress,
      );

      // Sauvegarder la tentative
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
      // Vérifier si une tentative en cours existe en local
      final existingAttempt = await _local.getInProgressAttempt(event.quizId);

      if (existingAttempt != null && existingAttempt.remoteAttemptId != null) {
        // Récupérer le quiz avec les questions
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

        // Calculer l'index de la question actuelle
        // = nombre de questions déjà répondues
        final currentQuestionIndex = existingAttempt.answers.length;

        if (emit.isDone) return;

        emit(QuizInProgress(
          quiz: quizWithQuestions,
          localAttempt: existingAttempt,
          currentQuestionIndex: currentQuestionIndex, // Position exacte
        ));
      } else {
        // Pas de tentative, démarrer une nouvelle
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
          currentQuestionIndex: 0, // Démarrer à 0
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

    // Créer une nouvelle liste d'answers
    final updatedAnswers = List<UserAnswerModel>.from(attempt.answers);

    // Update or add the answer
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

    // Créer une NOUVELLE instance de QuizAttemptModel
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

    if (submitEither.isLeft()) {
      final failure = submitEither.fold((l) => l, (_) => throw Exception());
      emit(QuizError(failure.message));
      return;
    }

    final attemptEntity = submitEither.fold((_) => throw Exception(), (r) => r);

    emit(QuizSubmitted(result: attemptEntity, queued: false));

    // Nettoyer le cache local
    try {
      await _local.clearInProgressAttempt(attemptEntity.quizId);
    } catch (_) {
      // Ignorer les erreurs de nettoyage
    }
  }

  Future<void> _onFlushPendingRequested(
      QuizFlushPendingRequested event, Emitter<QuizState> emit) async {
    final result = await _flushPending.call();

    result.fold(
      (failure) {
        debugPrint('Échec flush pending: ${failure.message}');
      },
      (count) {
        if (count > 0) {
          debugPrint('✅ $count tentative(s) synchronisée(s)');
        }
      },
    );
  }

  @override
  Future<void> close() {
    return super.close();
  }
}
