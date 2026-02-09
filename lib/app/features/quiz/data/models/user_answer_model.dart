/// Model pour représenter la réponse d'un utilisateur sur une question
class UserAnswerModel {
  final String questionId;
  final List<String> selectedAnswerIds;

  const UserAnswerModel({
    required this.questionId,
    required this.selectedAnswerIds,
  });

  factory UserAnswerModel.fromJson(Map<String, dynamic> json) {
    return UserAnswerModel(
      questionId: json['question_id'] as String,
      selectedAnswerIds: (json['answer_ids'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          (json['selected_answer_ids'] as List<dynamic>?)
              ?.map((e) => e as String)
              .toList() ??
          [],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'question_id': questionId,
      'answer_ids': selectedAnswerIds,
    };
  }
}
