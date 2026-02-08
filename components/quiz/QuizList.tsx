"use client";
import React, { Fragment, useState, useEffect, useMemo, useCallback } from "react";
import { Row, Col, Card, Form, Nav, Tab, Badge, Alert } from "react-bootstrap";
import TanstackTable from "components/table/TanstackTable";
import { getQuizListColumns } from "./QuizColumnDefinitions";
import { QuizType } from "types/QuizType";
import { CategoryType } from "types/EcommerceType";
import ConfirmModal from "components/common/ConfirmModal";
import Link from "next/link";
import { IconPlus } from "@tabler/icons-react";

const QuizList = () => {
    // State for data
    const [quizzes, setQuizzes] = useState<QuizType[]>([]);
    const [categories, setCategories] = useState<CategoryType[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    // State for filters
    const [searchTerm, setSearchTerm] = useState("");
    const [levelFilter, setLevelFilter] = useState("All");
    const [categoryFilter, setCategoryFilter] = useState("All");

    // Modal state
    const [confirmModal, setConfirmModal] = useState({
        show: false,
        title: "",
        message: "",
        type: "confirm" as "confirm" | "alert" | "delete",
        onConfirm: undefined as (() => void) | undefined,
    });

    const fetchData = useCallback(async () => {
        setIsLoading(true);
        try {
            const token = localStorage.getItem("access_token");
            const headers = { 'Authorization': `Bearer ${token}` };

            // Parallel fetch
            const [quizzesRes, categoriesRes] = await Promise.all([
                fetch(`${process.env.NEXT_PUBLIC_API_URL}/quizzes`, { headers }),
                fetch(`${process.env.NEXT_PUBLIC_API_URL}/categories`, { headers })
            ]);

            if (!quizzesRes.ok || !categoriesRes.ok) {
                throw new Error("Erreur de chargement des données");
            }

            const quizzesData = await quizzesRes.json();
            const categoriesData = await categoriesRes.json();

            setCategories(categoriesData);

            // Enhance quizzes with category names (API returns IDs)
            const enhancedQuizzes = quizzesData.map((quiz: QuizType) => {
                const cat = categoriesData.find((c: CategoryType) => c.id === quiz.category_id);
                return {
                    ...quiz,
                    category_name: cat ? cat.name : "Inconnu"
                };
            });

            setQuizzes(enhancedQuizzes);
        } catch (err: any) {
            console.error(err);
            setError(err.message || "Impossible de charger les quiz");
        } finally {
            setIsLoading(false);
        }
    }, []);

    useEffect(() => {
        fetchData();
    }, [fetchData]);

    const handleDelete = (id: string) => {
        setConfirmModal({
            show: true,
            title: "Supprimer le quiz",
            message: "Êtes-vous sûr de vouloir supprimer ce quiz ? Cette action est irréversible.",
            type: "delete",
            onConfirm: async () => {
                try {
                    const token = localStorage.getItem("access_token");
                    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/quizzes/${id}`, {
                        method: "DELETE",
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });

                    if (!response.ok) {
                        const err = await response.json();
                        throw new Error(err.detail || "Erreur lors de la suppression");
                    }

                    // Optimistic update or refetch
                    fetchData();
                } catch (err: any) {
                    setConfirmModal(prev => ({
                        ...prev,
                        show: true,
                        title: "Erreur",
                        message: err.message,
                        type: "alert",
                        onConfirm: undefined
                    }));
                }
            }
        });
    };

    // Columns with delete handler
    const columns = useMemo(() => getQuizListColumns(handleDelete), [handleDelete]);

    // Filtering logic (Client side for now as API filters might be partial)
    const filteredData = useMemo(() => {
        return quizzes.filter((quiz) => {
            const matchesSearch = quiz.title.toLowerCase().includes(searchTerm.toLowerCase());

            // Map labels to values stored in DB (API uses lowercase enum values)
            // level: debutant, intermediaire, avance
            // UI Filter: Débutant (label) -> match against mapped value
            const levelMap: Record<string, string> = {
                "Débutant": "debutant",
                "Intermédiaire": "intermediaire",
                "Avancé": "avance"
            };
            const mappedLevelFilter = levelFilter !== "All" ? levelMap[levelFilter] : "All";
            const matchesLevel = levelFilter === "All" ? true : quiz.level === mappedLevelFilter;

            // categoryFilter stores Category ID or "All"
            const matchesCategory = categoryFilter === "All" ? true : quiz.category_id === categoryFilter;

            // Status: draft, published
            // We use status for tabs, so general filter might not need this if we filter by list logic below
            return matchesSearch && matchesLevel && matchesCategory;
        });
    }, [quizzes, searchTerm, levelFilter, categoryFilter]);

    const allQuiz = filteredData;
    const publishedQuiz = filteredData.filter(q => q.status === "published");
    const draftQuiz = filteredData.filter(q => q.status === "draft");

    const FilterComponent = () => (
        <Row className="justify-content-between gy-2 mb-4">
            <Col lg={4} md={6}>
                <Form.Control
                    type="search"
                    className="listjs-search"
                    placeholder="Rechercher par titre..."
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                />
            </Col>
            <Col lg={8} md={6} className="d-flex gap-2 justify-content-md-end">
                <Form.Select
                    className="w-auto"
                    value={categoryFilter}
                    onChange={(e) => setCategoryFilter(e.target.value)}
                >
                    <option value="All">Toutes Catégories</option>
                    {categories.map(cat => (
                        <option key={cat.id} value={cat.id}>{cat.name}</option>
                    ))}
                </Form.Select>
                <Form.Select
                    className="w-auto"
                    value={levelFilter}
                    onChange={(e) => setLevelFilter(e.target.value)}
                >
                    <option value="All">Tous Niveaux</option>
                    <option value="Débutant">Débutant</option>
                    <option value="Intermédiaire">Intermédiaire</option>
                    <option value="Avancé">Avancé</option>
                </Form.Select>
                <Link href="/quiz/editor" className="btn btn-primary d-flex align-items-center gap-2">
                    <IconPlus size={18} />
                    Nouveau Quiz
                </Link>
            </Col>
        </Row>
    );

    const renderTable = (data: QuizType[]) => {
        if (isLoading) {
            return (
                <div className="text-center p-5">
                    <div className="spinner-border text-primary" role="status">
                        <span className="visually-hidden">Loading...</span>
                    </div>
                </div>
            );
        }
        if (data.length === 0) {
            return <div className="text-center p-5 text-muted">Aucun quiz trouvé.</div>;
        }
        return <TanstackTable data={data} columns={columns} pagination />;
    };

    return (
        <Fragment>
            {error && <Alert variant="danger">{error}</Alert>}
            <Row>
                <Col lg={12}>
                    <Tab.Container defaultActiveKey={"all"}>
                        <Card>
                            <Card.Header className="border-bottom-0 pb-0">
                                <Nav className="nav-lb-tab border-bottom-0" id="tab-quiz">
                                    <Nav.Item>
                                        <Nav.Link eventKey="all" className="mb-sm-3 mb-md-0">
                                            Tous
                                            <Badge bg="light" text="dark" className="ms-2">{isLoading ? "-" : allQuiz.length}</Badge>
                                        </Nav.Link>
                                    </Nav.Item>
                                    <Nav.Item>
                                        <Nav.Link eventKey="published" className="mb-sm-3 mb-md-0">
                                            Publiés
                                            <Badge bg="success-subtle" text="success" className="ms-2">{isLoading ? "-" : publishedQuiz.length}</Badge>
                                        </Nav.Link>
                                    </Nav.Item>
                                    <Nav.Item>
                                        <Nav.Link eventKey="drafts" className="mb-sm-3 mb-md-0">
                                            Brouillons
                                            <Badge bg="secondary-subtle" text="dark" className="ms-2">{isLoading ? "-" : draftQuiz.length}</Badge>
                                        </Nav.Link>
                                    </Nav.Item>
                                </Nav>
                            </Card.Header>
                            <Card.Body className="p-0">
                                <div className="p-4">
                                    <FilterComponent />
                                </div>
                                <Tab.Content>
                                    <Tab.Pane eventKey="all" className="pb-4">
                                        {renderTable(allQuiz)}
                                    </Tab.Pane>
                                    <Tab.Pane eventKey="published" className="pb-4">
                                        {renderTable(publishedQuiz)}
                                    </Tab.Pane>
                                    <Tab.Pane eventKey="drafts" className="pb-4">
                                        {renderTable(draftQuiz)}
                                    </Tab.Pane>
                                </Tab.Content>
                            </Card.Body>
                        </Card>
                    </Tab.Container>
                </Col>
            </Row>

            <ConfirmModal
                show={confirmModal.show}
                onHide={() => setConfirmModal(prev => ({ ...prev, show: false }))}
                title={confirmModal.title}
                message={confirmModal.message}
                type={confirmModal.type}
                onConfirm={confirmModal.onConfirm}
                confirmText={confirmModal.type === "delete" ? "Supprimer" : "OK"}
            />
        </Fragment>
    );
};

export default QuizList;
