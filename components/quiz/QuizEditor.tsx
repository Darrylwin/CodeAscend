"use client";
import { useState, Fragment, useEffect } from "react";
import {
    Row,
    Col,
    Card,
    Form,
    Button,
    Badge,
    InputGroup,
    Accordion,
    Spinner
} from "react-bootstrap";
import {
    IconPlus,
    IconTrash,
    IconDeviceFloppy,
    IconSend,
} from "@tabler/icons-react";
import Flex from "components/common/Flex";
import Link from 'next/link';
import { useSearchParams, useRouter } from "next/navigation";
import { CategoryType } from "types/EcommerceType";
import ConfirmModal from "components/common/ConfirmModal";
import { AnswerType, QuestionType } from "types/QuizType";

const QuizEditor = () => {
    const searchParams = useSearchParams();
    const router = useRouter();
    const quizId = searchParams.get("id");

    // --- STATE MANAGEMENT ---
    const [isLoading, setIsLoading] = useState(false);
    const [isFetching, setIsFetching] = useState(true);
    const [categories, setCategories] = useState<CategoryType[]>([]);

    // Form State
    const [title, setTitle] = useState("");
    const [category, setCategory] = useState("");
    const [level, setLevel] = useState("debutant");
    const [status, setStatus] = useState("draft");

    // Questions State
    const [questions, setQuestions] = useState<QuestionType[]>([
        {
            id: `temp_${Date.now()}`,
            question_text: "",
            order: 1,
            answers: [
                { id: `temp_a_${Date.now()}_1`, answer_text: "", is_correct: false, order: 1 },
                { id: `temp_a_${Date.now()}_2`, answer_text: "", is_correct: false, order: 2 },
            ],
        },
    ]);

    // Track initial questions IDs to handle deletions if needed (for simplicity we might just list current)
    // A better way for deletion is: when removing a generic question, if it has a real ID, add it to a "deletedQuestions" list.
    const [deletedQuestionIds, setDeletedQuestionIds] = useState<string[]>([]);

    const [modal, setModal] = useState({ show: false, title: "", message: "", type: "alert" as any, callback: undefined as any });

    // --- DATA LOADING ---
    useEffect(() => {
        const loadData = async () => {
            setIsFetching(true);
            try {
                const token = localStorage.getItem("access_token");
                const headers = { 'Authorization': `Bearer ${token}` };

                // 1. Fetch Categories
                const catRes = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/categories`, { headers });
                if (catRes.ok) {
                    const cats = await catRes.json();
                    setCategories(cats);
                    if (cats.length > 0 && !category) setCategory(cats[0].id);
                }

                // 2. If editing, fetch Quiz and Questions
                if (quizId) {
                    const quizRes = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/quizzes/${quizId}`, { headers });
                    if (!quizRes.ok) throw new Error("Quiz introuvable");
                    const quizData = await quizRes.json();

                    setTitle(quizData.title);
                    setCategory(quizData.category_id);
                    setLevel(quizData.level);
                    setStatus(quizData.status);

                    // Fetch Questions
                    const qRes = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/questions?quiz_id=${quizId}`, { headers });
                    if (qRes.ok) {
                        const qData = await qRes.json();
                        // Sort by order/id
                        const formattedQuestions: QuestionType[] = qData.map((q: any) => ({
                            id: q.id,
                            quiz_id: q.quiz_id,
                            question_text: q.question_text,
                            order: q.order,
                            answers: q.answers.map((a: any) => ({
                                id: a.id,
                                answer_text: a.answer_text,
                                is_correct: a.is_correct,
                                order: a.order
                            }))
                        }));
                        setQuestions(formattedQuestions.length > 0 ? formattedQuestions : questions);
                    }
                }
            } catch (error: any) {
                console.error(error);
                setModal({ show: true, title: "Erreur", message: error.message, type: "alert", callback: undefined });
            } finally {
                setIsFetching(false);
            }
        };
        loadData();
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [quizId]);


    // --- HELPERS & HANDLERS ---
    const generateId = () => Math.random().toString(36).substr(2, 9);

    const addQuestion = () => {
        if (questions.length >= 10) return;
        setQuestions([
            ...questions,
            {
                id: `temp_q_${generateId()}`,
                question_text: "",
                order: questions.length + 1,
                answers: [
                    { id: `temp_a_${generateId()}`, answer_text: "", is_correct: false, order: 1 },
                    { id: `temp_a_${generateId()}`, answer_text: "", is_correct: false, order: 2 },
                ],
            },
        ]);
    };

    const removeQuestion = (qId: string) => {
        // If it's an existing question (not temp), mark for deletion
        if (!qId.startsWith("temp_")) {
            setDeletedQuestionIds([...deletedQuestionIds, qId]);
        }
        setQuestions(questions.filter((q) => q.id !== qId));
    };

    const updateQuestionText = (qId: string, text: string) => {
        setQuestions(questions.map((q) => (q.id === qId ? { ...q, question_text: text } : q)));
    };

    const addAnswer = (qId: string) => {
        setQuestions(questions.map((q) => {
            if (q.id === qId && q.answers.length < 6) {
                return {
                    ...q,
                    answers: [
                        ...q.answers,
                        { id: `temp_a_${generateId()}`, answer_text: "", is_correct: false, order: q.answers.length + 1 },
                    ],
                };
            }
            return q;
        }));
    };

    const removeAnswer = (qId: string, aId: string) => {
        setQuestions(questions.map((q) => {
            if (q.id === qId) {
                if (q.answers.length <= 2) return q;
                return {
                    ...q,
                    answers: q.answers.filter((a) => a.id !== aId),
                };
            }
            return q;
        }));
    };

    const updateAnswerText = (qId: string, aId: string, text: string) => {
        setQuestions(questions.map((q) => {
            if (q.id === qId) {
                return {
                    ...q,
                    answers: q.answers.map((a) => a.id === aId ? { ...a, answer_text: text } : a),
                };
            }
            return q;
        }));
    };

    const toggleCorrectAnswer = (qId: string, aId: string) => {
        setQuestions(questions.map(q => {
            if (q.id === qId) {
                return {
                    ...q,
                    answers: q.answers.map(a =>
                        a.id === aId ? { ...a, is_correct: !a.is_correct } : a
                    )
                }
            }
            return q;
        }));
    }


    // --- ACTION: SAVE / PUBLISH ---
    const handleSave = async (targetStatus?: string) => {
        setIsLoading(true);
        try {
            const token = localStorage.getItem("access_token");
            const headers = { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` };

            const finalStatus = targetStatus || status;

            // 1. Create/Update Quiz
            const quizBody = {
                category_id: category,
                title,
                level,
                status: finalStatus
            };

            let currentQuizId = quizId;
            let method = quizId ? "PUT" : "POST";
            let url = quizId ? `${process.env.NEXT_PUBLIC_API_URL}/quizzes/${quizId}` : `${process.env.NEXT_PUBLIC_API_URL}/quizzes`;

            const quizResponse = await fetch(url, {
                method,
                headers,
                body: JSON.stringify(quizBody)
            });

            if (!quizResponse.ok) throw new Error("Erreur lors de l'enregistrement du quiz");
            const savedQuiz = await quizResponse.json();
            currentQuizId = savedQuiz.id;

            // 2. Handle Deletions (only if editing)
            if (deletedQuestionIds.length > 0) {
                await Promise.all(deletedQuestionIds.map(id =>
                    fetch(`${process.env.NEXT_PUBLIC_API_URL}/questions/${id}`, { method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` } })
                ));
            }

            // 3. Handle Questions (Create or Update)
            // We process sequentially or parallel. 
            // Warning: React state might not match DB exactly for Questions if we don't reload.
            // For now, simple logic:
            // - If question has temp ID -> POST /quizzes/{id}/questions
            // - If question has real ID -> PUT /questions/{id} 
            // Note: API doc says PUT /questions/{id} replaces answers logic.

            for (const [index, q] of questions.entries()) {
                const questionBody = {
                    question_text: q.question_text,
                    order: index + 1,
                    answers: q.answers.map((a, i) => ({
                        answer_text: a.answer_text,
                        is_correct: a.is_correct,
                        order: i + 1
                    }))
                };

                if (q.id && q.id.startsWith("temp_")) {
                    // Create
                    await fetch(`${process.env.NEXT_PUBLIC_API_URL}/quizzes/${currentQuizId}/questions`, {
                        method: "POST",
                        headers,
                        body: JSON.stringify(questionBody)
                    });
                } else {
                    // Update
                    await fetch(`${process.env.NEXT_PUBLIC_API_URL}/questions/${q.id}`, {
                        method: "PUT",
                        headers,
                        body: JSON.stringify(questionBody)
                    });
                }
            }

            setModal({
                show: true,
                title: "Succès",
                message: "Le quiz a été enregistré avec succès",
                type: "alert",
                callback: () => router.push("/quiz")
            });

        } catch (err: any) {
            console.error(err);
            setModal({
                show: true,
                title: "Erreur",
                message: err.message || "Une erreur est survenue",
                type: "alert",
                callback: undefined
            });
        } finally {
            setIsLoading(false);
        }
    };

    // --- VALIDATION ---
    const isValid = () => {
        if (!title.trim() || !category) return false;
        const allQuestionsValid = questions.every(q => {
            const hasText = q.question_text.trim().length > 0;
            const hasCorrectAnswer = q.answers.some(a => a.is_correct);
            const allAnswersHaveText = q.answers.every(a => a.answer_text.trim().length > 0);
            return hasText && hasCorrectAnswer && allAnswersHaveText;
        });
        return questions.length > 0 && allQuestionsValid;
    };

    if (isFetching) {
        return <div className="text-center p-5"><Spinner animation="border" variant="primary" /></div>;
    }

    return (
        <Fragment>
            {/* HEADER ACTIONS */}
            <Row>
                <Col lg={12}>
                    <Flex justifyContent="between" alignItems="center" className="mb-8" breakpoint="md">
                        <div className="mb-3 mb-md-0">
                            <h1 className="h2 mb-0 fw-bold">Éditeur de Quiz</h1>
                            <p className="mb-0 text-muted">Création et modification</p>
                        </div>
                        <div className="d-flex gap-2">
                            <Link href="/quiz">
                                <Button variant="ghost">Annuler</Button>
                            </Link>
                            <Button
                                variant="outline-primary"
                                className="d-flex align-items-center gap-2"
                                onClick={() => handleSave("draft")}
                                disabled={isLoading || !isValid()}
                            >
                                <IconDeviceFloppy size={18} />
                                {isLoading ? "Enregistrement..." : "Enregistrer brouillon"}
                            </Button>
                            <Button
                                variant="primary"
                                className="d-flex align-items-center gap-2"
                                onClick={() => handleSave("published")}
                                disabled={isLoading || !isValid()}
                            >
                                <IconSend size={18} />
                                {isLoading ? "Publication..." : "Publier le Quiz"}
                            </Button>
                        </div>
                    </Flex>
                </Col>
            </Row>

            <Row>
                {/* LEFT COLUMN: GENERAL INFO */}
                <Col xl={3} lg={4}>
                    <Card className="mb-4">
                        <Card.Header><h4 className="mb-0">Informations</h4></Card.Header>
                        <Card.Body>
                            <Form>
                                <div className="mb-3">
                                    <Form.Label>Titre du quiz</Form.Label>
                                    <Form.Control
                                        type="text"
                                        placeholder="Ex: Introduction à React"
                                        value={title}
                                        onChange={(e) => setTitle(e.target.value)}
                                    />
                                </div>
                                <div className="mb-3">
                                    <Form.Label>Catégorie</Form.Label>
                                    <Form.Select
                                        value={category}
                                        onChange={(e) => setCategory(e.target.value)}
                                    >
                                        <option value="" disabled>Choisir une catégorie</option>
                                        {categories.map(c => (
                                            <option key={c.id} value={c.id}>{c.name}</option>
                                        ))}
                                    </Form.Select>
                                </div>
                                <div className="mb-3">
                                    <Form.Label>Niveau</Form.Label>
                                    <Form.Select
                                        value={level}
                                        onChange={(e) => setLevel(e.target.value)}
                                    >
                                        <option value="debutant">Débutant</option>
                                        <option value="intermediaire">Intermédiaire</option>
                                        <option value="avance">Avancé</option>
                                    </Form.Select>
                                </div>
                                <div className="mb-3">
                                    <Form.Label>Statut</Form.Label>
                                    <div className="d-flex align-items-center gap-2">
                                        <Badge
                                            bg={status === "published" ? "success-subtle" : "warning-subtle"}
                                            text={status === "published" ? "success" : "warning"}
                                            className="fs-6"
                                        >
                                            {status === "published" ? "Publié" : "Brouillon"}
                                        </Badge>
                                    </div>
                                </div>
                            </Form>
                        </Card.Body>
                    </Card>

                    <Card>
                        <Card.Header><h4 className="mb-0">Règles</h4></Card.Header>
                        <Card.Body>
                            <ul className="list-unstyled mb-0 text-muted fs-6 d-flex flex-column gap-2">
                                <li className={questions.length > 10 ? "text-danger" : ""}>• Max 10 questions ({questions.length}/10)</li>
                                <li>• Min 2 réponses par question</li>
                                <li>• Max 6 réponses par question</li>
                                <li>• Min 1 bonne réponse requise</li>
                            </ul>
                        </Card.Body>
                    </Card>
                </Col>

                {/* RIGHT COLUMN: QUESTIONS EDITOR */}
                <Col xl={9} lg={8}>
                    <div className="mb-4 d-flex justify-content-between align-items-center">
                        <h3 className="mb-0">Questions ({questions.length})</h3>
                        <Button
                            variant="outline-primary"
                            size="sm"
                            onClick={addQuestion}
                            disabled={questions.length >= 10}
                        >
                            <IconPlus size={16} className="me-1" /> Ajouter une question
                        </Button>
                    </div>

                    {questions.length === 0 && (
                        <Card className="text-center p-5 border-dashed">
                            <div className="text-muted">Ajoutez votre première question pour commencer le quiz.</div>
                        </Card>
                    )}

                    <Accordion defaultActiveKey="0" alwaysOpen>
                        {questions.map((q, qIndex) => (
                            <Accordion.Item eventKey={qIndex.toString()} key={q.id} className="mb-3 border rounded shadow-sm overflow-hidden">
                                <Accordion.Header>
                                    <div className="d-flex align-items-center gap-2 w-100 me-3">
                                        <span className="fw-bold text-primary">Q{qIndex + 1}.</span>
                                        <span className="text-truncate flex-grow-1 fst-italic">
                                            {q.question_text || "Nouvelle question..."}
                                        </span>
                                        {(q.answers.filter(a => a.is_correct).length === 0) && (
                                            <Badge bg="danger-subtle" text="danger" className="ms-auto me-2">Invalid</Badge>
                                        )}
                                    </div>
                                </Accordion.Header>
                                <Accordion.Body className="bg-light-subtle">
                                    <div className="mb-4">
                                        <Form.Label className="fw-bold">Intitulé de la question</Form.Label>
                                        <div className="d-flex gap-2">
                                            <Form.Control
                                                type="text"
                                                placeholder="Posez votre question ici..."
                                                value={q.question_text}
                                                onChange={(e) => updateQuestionText(q.id!, e.target.value)}
                                            />
                                            <Button
                                                variant="ghost text-danger pt-2"
                                                size="sm"
                                                onClick={() => removeQuestion(q.id!)}
                                                title="Supprimer la question"
                                            >
                                                <IconTrash size={18} />
                                            </Button>
                                        </div>
                                    </div>

                                    <div className="mb-3">
                                        <Form.Label className="fw-bold d-flex justify-content-between">
                                            Réponses
                                            <span className="text-muted fs-6 fw-normal">Cochez la/les bonne(s) réponse(s)</span>
                                        </Form.Label>

                                        <div className="d-flex flex-column gap-2">
                                            {q.answers.map((a, aIndex) => (
                                                <InputGroup key={a.id}>
                                                    <InputGroup.Checkbox
                                                        aria-label="Checkbox for correct answer"
                                                        checked={a.is_correct}
                                                        onChange={() => toggleCorrectAnswer(q.id!, a.id!)}
                                                    />
                                                    <Form.Control
                                                        type="text"
                                                        placeholder={`Réponse option ${aIndex + 1}`}
                                                        value={a.answer_text}
                                                        onChange={(e) => updateAnswerText(q.id!, a.id!, e.target.value)}
                                                        className={a.is_correct ? "bg-success-subtle text-success-emphasis fw-medium" : ""}
                                                    />
                                                    <Button
                                                        variant="outline-secondary"
                                                        onClick={() => removeAnswer(q.id!, a.id!)}
                                                        disabled={q.answers.length <= 2}
                                                    >
                                                        <IconTrash size={16} />
                                                    </Button>
                                                </InputGroup>
                                            ))}
                                        </div>

                                        {q.answers.length < 6 && (
                                            <Button
                                                variant="ghost"
                                                size="sm"
                                                className="mt-2 text-primary"
                                                onClick={() => addAnswer(q.id!)}
                                            >
                                                <IconPlus size={16} className="me-1" /> Ajouter une réponse
                                            </Button>
                                        )}
                                    </div>
                                </Accordion.Body>
                            </Accordion.Item>
                        ))}
                    </Accordion>
                </Col>
            </Row>

            <ConfirmModal
                show={modal.show}
                onHide={() => {
                    setModal(prev => ({ ...prev, show: false }));
                    if (modal.callback) modal.callback();
                }}
                title={modal.title}
                message={modal.message}
                type={modal.type}
            />
        </Fragment>
    );
};

export default QuizEditor;
