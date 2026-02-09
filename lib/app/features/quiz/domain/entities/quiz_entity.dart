import 'package:equatable/equatable.dart';
import 'question_entity.dart';

/// Entity représentant un Quiz (métier)
class QuizEntity extends Equatable {
  final String id;
  final String categoryId;
  final String title;
  final String level; // 'debutant' | 'intermediaire' | 'avance'
  final int questionCount;
  final String status; // 'draft' | 'published'
  final DateTime createdAt;
  final List<QuestionEntity> questions;

  const QuizEntity({
    required this.id,
    required this.categoryId,
    required this.title,
    required this.level,
    required this.questionCount,
    required this.status,
    required this.createdAt,
    this.questions = const [],
  });

  @override
  List<Object?> get props => [
        id,
        categoryId,
        title,
        level,
        questionCount,
        status,
        createdAt,
        questions
      ];

  @override
  String toString() => 'QuizEntity(id: $id, title: $title, level: $level)';
}
