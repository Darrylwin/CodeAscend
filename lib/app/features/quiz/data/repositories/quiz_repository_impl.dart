import 'dart:async';
import 'dart:math';

import 'package:dartz/dartz.dart';
import 'package:dio/dio.dart';

import '../../../../core/error/failures.dart';
import '../../../../core/di/service_locator.dart';
import '../../domain/entities/quiz_entity.dart';
import '../../domain/entities/question_entity.dart';
import '../../domain/entities/quiz_attempt_entity.dart';
import '../../domain/repositories/quiz_repository.dart';
import '../datasources/quiz_local_data_source.dart';
import '../datasources/quiz_remote_data_source.dart';
import '../models/quiz_attempt_model.dart';
import '../models/user_answer_model.dart';
import '../../../auth/data/datasources/auth_local_data_source.dart';

/// Implémentation du QuizRepository, supportant le mode hors-ligne via SharedPreferences.
class QuizRepositoryImpl implements QuizRepository {
  final QuizRemoteDataSource _remote;
  final QuizLocalDataSource _local;
  final AuthLocalDataSource _authLocal;
  final NetworkInfo _networkInfo;

  final StreamController<int> _flushController =
      StreamController<int>.broadcast();

  QuizRepositoryImpl({
    required QuizRemoteDataSource remoteDataSource,
    required QuizLocalDataSource localDataSource,
    required AuthLocalDataSource authLocalDataSource,
    required NetworkInfo networkInfo,
  })  : _remote = remoteDataSource,
        _local = localDataSource,
        _authLocal = authLocalDataSource,
        _networkInfo = networkInfo;

  /// Stream émettant le nombre d'éléments flushés après un flushPendingSubmissions
  Stream<int> get onFlushCompleted => _flushController.stream;

  @override
  Future<Either<Failure, QuizEntity>> getQuizById(String id) async {
    try {
      final quiz = await _remote.getQuizById(id);
      return Right(quiz);
    } on DioException catch (e) {
      return Left(_handleDioException(e));
    } catch (e) {
      return Left(UnknownFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, List<QuizEntity>>> getAvailableQuizzes({
    required String categoryId,
  }) async {
    try {
      final list = await _remote.getAvailableQuizzes(categoryId);
      return Right(list);
    } on DioException catch (e) {
      return Left(_handleDioException(e));
    } catch (e) {
      return Left(UnknownFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, String>> startQuiz({required String quizId}) async {
    try {
      final isConnected = await _networkInfo.isConnected;
      final localId = _generateLocalId();
      final currentUserId = await _getCurrentUserId();

      if (isConnected) {
        // Appel API qui retourne attemptId + quiz + questions
        final result = await _remote.startQuiz(quizId: quizId);

        final attempt = QuizAttemptModel(
          localId: localId,
          remoteAttemptId: result.attemptId,
          quizId: quizId,
          userId: currentUserId,
          answers: [],
          status: AttemptStatus.inProgress,
        );

        await _local.saveInProgressAttempt(attempt);
        return Right(result.attemptId);
      } else {
        // Mode offline
        final attempt = QuizAttemptModel(
          localId: localId,
          remoteAttemptId: null,
          quizId: quizId,
          userId: currentUserId,
          answers: [],
          status: AttemptStatus.inProgress,
        );

        await _local.saveInProgressAttempt(attempt);
        return Right(localId);
      }
    } on DioException catch (e) {
      return Left(_handleDioException(e));
    } catch (e) {
      return Left(UnknownFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, QuizAttemptEntity>> submitQuiz({
    required String attemptId,
    required String quizId,
    required List<UserAnswer> answers,
  }) async {
    try {
      final isConnected = await _networkInfo.isConnected;

      // Récupérer la tentative en cours avec le quizId
      QuizAttemptModel? localAttempt =
          await _local.getInProgressAttempt(quizId);

      // Mode offline: mise en file d'attente
      if (!isConnected) {
        final currentUserId = await _getCurrentUserId();

        final attemptToQueue = localAttempt ??
            QuizAttemptModel(
              localId: attemptId,
              remoteAttemptId: null,
              quizId: quizId,
              userId: currentUserId,
              answers: answers
                  .map((a) => UserAnswerModel(
                      questionId: a.questionId,
                      selectedAnswerIds: a.selectedAnswerIds))
                  .toList(),
              status: AttemptStatus.pendingSubmission,
            );

        await _local.addPendingSubmission(attemptToQueue);
        return Right(attemptToQueue.toEntity());
      }

      // Mode online: soumission
      String remoteAttemptId = attemptId;

      // Si pas de remoteAttemptId, utiliser l'attemptId du paramètre
      if (localAttempt != null &&
          localAttempt.remoteAttemptId != null &&
          localAttempt.remoteAttemptId!.isNotEmpty) {
        remoteAttemptId = localAttempt.remoteAttemptId!;
      }

      // Conversion des UserAnswer en UserAnswerModel
      final answerModels = answers
          .map((a) => UserAnswerModel(
              questionId: a.questionId, selectedAnswerIds: a.selectedAnswerIds))
          .toList();

      final result = await _remote.submitQuiz(
        attemptId: remoteAttemptId,
        answers: answerModels,
      );

      // Enrichir l'entity avec les infos locales (quizId, userId)
      final currentUserId = await _getCurrentUserId();
      final enrichedResult = QuizAttemptEntity(
        id: result.id,
        quizId: quizId, // Utiliser le quizId du paramètre
        userId: localAttempt?.userId ??
            currentUserId, // Depuis localAttempt ou auth
        score: result.score,
        passed: result.passed,
        completedAt: result.completedAt,
        answers: result.answers,
        correctAnswersCount: result.correctAnswersCount,
        totalQuestions: result.totalQuestions,
      );

      // Nettoyer le cache local
      if (localAttempt != null) {
        await _local.clearInProgressAttempt(localAttempt.quizId);
      }

      // Sauvegarder dans l'historique
      try {
        final attemptModel = QuizAttemptModel(
          localId: _generateLocalId(),
          remoteAttemptId: enrichedResult.id,
          quizId: enrichedResult.quizId,
          userId: enrichedResult.userId,
          answers: answerModels,
          status: AttemptStatus.submitted,
          score: enrichedResult.score,
          passed: enrichedResult.passed,
          completedAt: enrichedResult.completedAt,
        );
        await _local.cacheAttemptHistory(attemptModel);
      } catch (_) {
        // Ignorer erreur de cache
      }

      return Right(enrichedResult);
    } on DioException catch (e) {
      return Left(_handleDioException(e));
    } catch (e) {
      return Left(UnknownFailure(e.toString()));
    }
  }

  @override
  Future<
      Either<
          Failure,
          ({
            QuizAttemptEntity attempt,
            QuizEntity quiz,
            List<QuestionEntity> questions
          })>> getAttemptById(String attemptId) async {
    try {
      final result = await _remote.getAttemptById(attemptId);

      // Créer le QuizEntity avec les questions
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

      return Right((
        attempt: result.attempt,
        quiz: quizWithQuestions,
        questions: result.questions,
      ));
    } on DioException catch (e) {
      return Left(_handleDioException(e));
    } catch (e) {
      return Left(UnknownFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, List<QuizAttemptEntity>>> getUserAttempts() async {
    try {
      final attempts = await _remote.getUserAttempts();
      return Right(attempts);
    } on DioException catch (e) {
      return Left(_handleDioException(e));
    } catch (e) {
      return Left(UnknownFailure(e.toString()));
    }
  }

  @override
  Future<Either<Failure, int>> flushPendingSubmissions() async {
    try {
      final isConnected = await _networkInfo.isConnected;
      if (!isConnected) {
        return const Right(0); // Pas connecté, rien à faire
      }

      final pending = await _local.getPendingSubmissions();
      if (pending.isEmpty) {
        return const Right(0); // Rien à envoyer
      }

      int successCount = 0;
      final List<String> toRemove = [];

      for (final attempt in pending) {
        try {
          // Si pas de remoteAttemptId, essayer de démarrer la tentative
          String remoteId = attempt.remoteAttemptId ?? '';

          if (remoteId.isEmpty && attempt.quizId.isNotEmpty) {
            try {
              final startResult =
                  await _remote.startQuiz(quizId: attempt.quizId);
              remoteId = startResult.attemptId;
            } catch (_) {
              continue; // Skip cette tentative
            }
          }

          if (remoteId.isEmpty) {
            continue; // Skip
          }

          // Soumettre
          final answerModels = attempt.answers;
          await _remote.submitQuiz(
            attemptId: remoteId,
            answers: answerModels,
          );

          successCount++;
          toRemove.add(attempt.localId);

          // Nettoyer le cache in-progress si applicable
          if (attempt.quizId.isNotEmpty) {
            await _local.clearInProgressAttempt(attempt.quizId);
          }
        } catch (e) {
          // Échec pour cette tentative, continuer avec la suivante
          print('Échec flush tentative ${attempt.localId}: $e');
        }
      }

      // Supprimer les tentatives envoyées avec succès
      for (final localId in toRemove) {
        await _local.removePendingSubmission(localId);
      }

      // Émettre le résultat dans le stream
      _flushController.add(successCount);

      return Right(successCount);
    } catch (e) {
      return Left(UnknownFailure('Erreur flush: $e'));
    }
  }

  /// Récupère le userId depuis AuthLocalDataSource
  Future<String> _getCurrentUserId() async {
    try {
      final userId = await _authLocal.getCurrentUserId();
      return userId ?? '';
    } catch (_) {
      return '';
    }
  }

  /// Génère un ID local unique basé sur timestamp + random
  String _generateLocalId() {
    final timestamp = DateTime.now().millisecondsSinceEpoch;
    final random = Random().nextInt(9999).toString().padLeft(4, '0');
    return 'local_$timestamp$random';
  }

  /// Mappe DioException → Failure
  Failure _handleDioException(DioException e) {
    switch (e.type) {
      case DioExceptionType.connectionTimeout:
      case DioExceptionType.sendTimeout:
      case DioExceptionType.receiveTimeout:
        return const TimeoutFailure();

      case DioExceptionType.connectionError:
        return const ConnectionFailure();

      case DioExceptionType.badResponse:
        final statusCode = e.response?.statusCode;
        final message = _extractMessage(e);

        switch (statusCode) {
          case 400:
            return ValidationFailure(message ?? 'Données invalides');
          case 401:
            return UnauthorizedFailure(message ?? 'Session expirée');
          case 403:
            return ForbiddenFailure(message ?? 'Accès refusé');
          case 404:
            return QuizNotFoundFailure(message ?? 'Quiz introuvable');
          case 500:
          case 502:
          case 503:
            return ServerFailure(message ?? 'Erreur serveur');
          default:
            return UnknownFailure(
              'Erreur $statusCode: ${message ?? 'Inconnue'}',
            );
        }

      default:
        return UnknownFailure(e.message ?? 'Erreur inconnue');
    }
  }

  /// Extraction message d'erreur FastAPI
  String? _extractMessage(DioException e) {
    try {
      final data = e.response?.data;
      if (data == null) return null;

      if (data is String) return data;

      if (data is Map<String, dynamic>) {
        final detail = data['detail'];

        if (detail is List && detail.isNotEmpty) {
          final errors = <String>[];
          for (final error in detail) {
            if (error is Map<String, dynamic>) {
              final msg = error['msg'];
              if (msg != null) {
                errors.add(msg.toString());
              }
            }
          }
          return errors.isNotEmpty ? errors.first : null;
        }

        if (detail is String) return detail;

        return data['message'] as String? ?? data['error'] as String?;
      }

      return null;
    } catch (_) {
      return null;
    }
  }
}
