import 'package:equatable/equatable.dart';
import 'answer_entity.dart';

/// Entity représentant une question d'un quiz
class QuestionEntity extends Equatable {
  final String id;
  final String quizId;
  final String text;
  final int order;
  final bool allowsMultipleAnswers;
  final List<AnswerEntity> answers;

  const QuestionEntity({
    required this.id,
    required this.quizId,
    required this.text,
    required this.order,
    required this.allowsMultipleAnswers,
    required this.answers,
  });

  @override
  List<Object?> get props =>
      [id, quizId, text, order, allowsMultipleAnswers, answers];

  @override
  String toString() =>
      'QuestionEntity(id: $id, text: $text, answers: ${answers.length})';
}
