import 'package:equatable/equatable.dart';

/// Entity représentant une réponse (Answer)
/// Partie pure du domaine
class AnswerEntity extends Equatable {
  final String id;
  final String questionId;
  final String text;
  final int order;
  final bool
      isCorrect; // Présent côté domaine (utile pour le scoring server-side / comparaison locale)

  const AnswerEntity({
    required this.id,
    required this.questionId,
    required this.text,
    required this.order,
    required this.isCorrect,
  });

  @override
  List<Object?> get props => [id, questionId, text, order, isCorrect];

  @override
  String toString() =>
      'AnswerEntity(id: $id, questionId: $questionId, text: $text, isCorrect: $isCorrect)';
}
