export interface QuizType {
    id: string;
    category_id: string;
    title: string;
    level: "debutant" | "intermediaire" | "avance";
    status: "draft" | "published";
    created_at: string;
    updated_at: string | null;
    // Optional UI helper fields (fetched separately or joined)
    category_name?: string;
    questions_count?: number;
}

export interface AnswerType {
    id?: string; // Optional for new answers before save
    answer_text: string;
    is_correct: boolean;
    order: number;
}

export interface QuestionType {
    id?: string; // Optional for new questions before save
    quiz_id?: string;
    question_text: string;
    order: number;
    answers: AnswerType[];
}
