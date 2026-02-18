import 'package:dio/dio.dart';

import '../../domain/entities/quiz_entity.dart';
import '../../domain/entities/question_entity.dart';
import '../../domain/entities/answer_entity.dart';
import '../../domain/entities/quiz_attempt_entity.dart';
import '../models/user_answer_model.dart';

/// Remote DataSource pour Quiz (appels API)
abstract class QuizRemoteDataSource {
  /// GET /quizzes/{id}
  /// IMPORTANT: Cet endpoint ne retourne PAS les questions
  Future<QuizEntity> getQuizById(String id);

  /// GET /categories/{categoryId}/quizzes/available
  Future<List<QuizEntity>> getAvailableQuizzes(String categoryId);

  /// POST /attempts/start/{quiz_id}
  /// Retourne { attempt_id, quiz, questions }
  /// C'est ICI qu'on récupère les questions !
  Future<({String attemptId, QuizEntity quiz, List<QuestionEntity> questions})>
      startQuiz({
    required String quizId,
  });

  /// POST /attempts/submit/{attempt_id}
  /// Retourne les détails de la tentative (score, passed, details)
  Future<QuizAttemptEntity> submitQuiz({
    required String attemptId,
    required List<UserAnswerModel> answers,
  });

  /// GET /attempts/{attempt_id}
  /// Retourne: attempt + quiz + questions_with_answers
  Future<
      ({
        QuizAttemptEntity attempt,
        QuizEntity quiz,
        List<QuestionEntity> questions
      })> getAttemptById(String attemptId);

  /// GET /users/me/attempts
  Future<List<QuizAttemptEntity>> getUserAttempts();
}

class QuizRemoteDataSourceImpl implements QuizRemoteDataSource {
  final Dio _dio;

  QuizRemoteDataSourceImpl(this._dio);

  @override
  Future<QuizEntity> getQuizById(String id) async {
    final response = await _dio.get('/quizzes/$id');

    final data = response.data as Map<String, dynamic>;

    // L'API ne retourne PAS les questions ici
    // On retourne juste les métadonnées du quiz
    return QuizEntity(
      id: data['id'] as String,
      categoryId: data['category_id'] as String,
      title: data['title'] as String,
      level: data['level'] as String,
      questionCount: 10, // Valeur par défaut selon les règles métier
      status: data['status'] as String? ?? 'published',
      createdAt: DateTime.parse(data['created_at'] as String),
      questions: const [], // Pas de questions dans cette réponse
    );
  }

  @override
  Future<List<QuizEntity>> getAvailableQuizzes(String categoryId) async {
    final response =
        await _dio.get('/categories/$categoryId/quizzes/available');

    final data = response.data as Map<String, dynamic>;
    final quizzesList = (data['data'] as List<dynamic>?) ?? [];

    return quizzesList.cast<Map<String, dynamic>>().map((q) {
      return QuizEntity(
        id: q['id'] as String,
        categoryId: q['category_id'] as String? ?? categoryId,
        title: q['title'] as String,
        level: q['level'] as String,
        questionCount: 10, // Valeur par défaut
        status: q['status'] as String? ?? 'published',
        createdAt: DateTime.parse(q['created_at'] as String),
        questions: const [], // Pas de détails ici, juste liste
      );
    }).toList();
  }

  @override
  Future<({String attemptId, QuizEntity quiz, List<QuestionEntity> questions})>
      startQuiz({
    required String quizId,
  }) async {
    final response = await _dio.post('/attempts/start/$quizId');

    final data = response.data as Map<String, dynamic>;

    final attemptId = data['attempt_id'] as String;

    // Parser le quiz
    final quizData = data['quiz'] as Map<String, dynamic>;
    final quiz = QuizEntity(
      id: quizData['id'] as String,
      categoryId: quizData['category_id'] as String,
      title: quizData['title'] as String,
      level: quizData['level'] as String,
      questionCount: 10,
      status: quizData['status'] as String? ?? 'published',
      createdAt: DateTime.parse(quizData['created_at'] as String),
      questions: const [],
    );

    // Parser les questions
    final questionsJson = (data['questions'] as List<dynamic>?) ?? [];
    final questions = questionsJson.cast<Map<String, dynamic>>().map((q) {
      final answersJson = (q['answers'] as List<dynamic>?) ?? [];
      final answers = answersJson.cast<Map<String, dynamic>>().map((a) {
        return AnswerEntity(
          id: a['id'] as String,
          questionId: q['id'] as String,
          text: a['answer_text'] as String,
          order: a['order'] as int? ?? 0,
          isCorrect: a['is_correct'] as bool? ?? false,
        );
      }).toList();

      // Détecter si plusieurs réponses correctes (QCM multiple)
      final correctCount = answers.where((a) => a.isCorrect).length;

      return QuestionEntity(
        id: q['id'] as String,
        quizId: quiz.id,
        text: q['question_text'] as String,
        order: q['order'] as int? ?? 0,
        allowsMultipleAnswers: correctCount > 1,
        answers: answers,
      );
    }).toList();

    return (attemptId: attemptId, quiz: quiz, questions: questions);
  }

  @override
  Future<QuizAttemptEntity> submitQuiz({
    required String attemptId,
    required List<UserAnswerModel> answers,
  }) async {
    final payload = {
      'answers': answers
          .map((a) => {
                'question_id': a.questionId,
                'answer_ids': a.selectedAnswerIds,
              })
          .toList(),
    };

    final response = await _dio.post(
      '/attempts/submit/$attemptId',
      data: payload,
    );

    final data = response.data as Map<String, dynamic>;

    // L'API ne retourne pas attempt_id, quiz_id, user_id, completed_at
    final score = (data['score'] as num).toDouble();
    final passed = data['passed'] as bool;
    final correctAnswers = data['correct_answers'] as int? ?? 0;
    final totalQuestions = data['total_questions'] as int? ?? 0;

    final detailsJson = (data['details'] as List<dynamic>?) ?? [];

    // Extraire les user_answers depuis les details
    final userAnswers = detailsJson.cast<Map<String, dynamic>>().map((d) {
      return UserAnswer(
        questionId: d['question_id'] as String,
        selectedAnswerIds:
            (d['user_answers'] as List<dynamic>?)?.cast<String>() ??
                (d['user_selected'] as List<dynamic>?)?.cast<String>() ??
                [],
      );
    }).toList();

    return QuizAttemptEntity(
      id: attemptId, // Utiliser l'attemptId du paramètre
      quizId: '', // Sera enrichi par le repository
      userId: '', // Sera enrichi par le repository
      score: score,
      passed: passed,
      completedAt: DateTime.now(), // Utiliser maintenant si non fourni
      answers: userAnswers.isNotEmpty
          ? userAnswers
          : answers
              .map((a) => UserAnswer(
                  questionId: a.questionId,
                  selectedAnswerIds: a.selectedAnswerIds))
              .toList(),
      correctAnswersCount: correctAnswers,
      totalQuestions: totalQuestions,
    );
  }

  @override
  Future<
      ({
        QuizAttemptEntity attempt,
        QuizEntity quiz,
        List<QuestionEntity> questions
      })> getAttemptById(String attemptId) async {
    final response = await _dio.get('/attempts/$attemptId');

    final responseData = response.data as Map<String, dynamic>;

    final data = responseData['data'] as Map<String, dynamic>;
    final attemptData = data['attempt'] as Map<String, dynamic>;
    final quizData = data['quiz'] as Map<String, dynamic>;
    final questionsData =
        (data['questions_with_answers'] as List<dynamic>?) ?? [];

    // Parser les informations de base
    final attemptIdRemote = attemptData['id'] as String;
    final score = (attemptData['score'] as num).toDouble();
    final passed = attemptData['passed'] as bool;
    final completedAt = DateTime.parse(attemptData['completed_at'] as String);

    final quizId = quizData['id'] as String;
    final userId = attemptData['user_id']?.toString() ?? '';

    // Parser le quiz
    final quiz = QuizEntity(
      id: quizData['id'] as String,
      categoryId: quizData['category_id'] as String,
      title: quizData['title'] as String,
      level: quizData['level'] as String,
      questionCount: questionsData.length,
      status: 'published',
      createdAt: DateTime.parse(quizData['created_at'] as String? ??
          DateTime.now().toIso8601String()),
      questions: const [], // Sera rempli après
    );

    // Parser les questions et réponses pour extraire les UserAnswer ET créer les QuestionEntity
    final answers = <UserAnswer>[];
    final questions = <QuestionEntity>[];

    int correctQuestionsCount = 0;

    for (final questionMap in questionsData.cast<Map<String, dynamic>>()) {
      final questionId = questionMap['id'] as String;
      final questionText = questionMap['question_text'] as String;
      final questionOrder = questionMap['order'] as int? ?? 0;
      final answersJson = (questionMap['answers'] as List<dynamic>?) ?? [];

      final selectedAnswerIds = <String>[];
      final correctAnswerIds = <String>[];
      final answerEntities = <AnswerEntity>[];

      for (final answerMap in answersJson.cast<Map<String, dynamic>>()) {
        final answerId = answerMap['id'] as String;
        final answerText = answerMap['answer_text'] as String;
        final isCorrect = answerMap['is_correct'] as bool? ?? false;
        final answerOrder = answerMap['order'] as int? ?? 0;
        final userSelected = answerMap['user_selected'] as bool? ?? false;

        // Créer l'AnswerEntity
        answerEntities.add(AnswerEntity(
          id: answerId,
          questionId: questionId,
          text: answerText,
          order: answerOrder,
          isCorrect: isCorrect,
        ));

        // Collecter les réponses sélectionnées et correctes
        if (userSelected) {
          selectedAnswerIds.add(answerId);
        }
        if (isCorrect) {
          correctAnswerIds.add(answerId);
        }
      }

      // Vérifier si cette question a été correctement répondue
      // (toutes les bonnes réponses sélectionnées ET aucune mauvaise)
      final selectedSet = selectedAnswerIds.toSet();
      final correctSet = correctAnswerIds.toSet();
      final isQuestionCorrect = selectedSet.length == correctSet.length &&
          selectedSet.containsAll(correctSet);

      if (isQuestionCorrect) {
        correctQuestionsCount++;
      }

      // Créer le UserAnswer pour cette question
      answers.add(UserAnswer(
        questionId: questionId,
        selectedAnswerIds: selectedAnswerIds,
      ));

      // Créer la QuestionEntity
      questions.add(QuestionEntity(
        id: questionId,
        quizId: quizId,
        text: questionText,
        order: questionOrder,
        allowsMultipleAnswers: correctAnswerIds.length > 1,
        answers: answerEntities,
      ));
    }

    // Créer l'attempt avec le nombre de QUESTIONS correctes
    final attempt = QuizAttemptEntity(
      id: attemptIdRemote,
      quizId: quizId,
      userId: userId,
      score: score,
      passed: passed,
      completedAt: completedAt,
      answers: answers,
      correctAnswersCount:
          correctQuestionsCount, // Nombre de questions correctes
      totalQuestions: questionsData.length,
    );

    return (attempt: attempt, quiz: quiz, questions: questions);
  }

  @override
  Future<List<QuizAttemptEntity>> getUserAttempts() async {
    final response = await _dio.get('/users/me/attempts');

    final list = response.data as List<dynamic>;

    return list.cast<Map<String, dynamic>>().map((item) {
      final id = item['id'] as String;
      final quizId = item['quiz_id'] as String;
      final userId = item['user_id'] as String? ?? '';
      final score = (item['score'] as num).toDouble();
      final passed = item['passed'] as bool;
      final completedAt = DateTime.parse(item['completed_at'] as String);

      // Les détails ne sont pas dans la liste, juste le résumé
      return QuizAttemptEntity(
        id: id,
        quizId: quizId,
        userId: userId,
        score: score,
        passed: passed,
        completedAt: completedAt,
        answers: const [], // Pas de détails dans la liste
        correctAnswersCount: 0, // Pas dans la réponse
        totalQuestions: 10, // Valeur par défaut
      );
    }).toList();
  }
}
