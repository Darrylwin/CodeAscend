"use client";
import { ColumnDef } from "@tanstack/react-table";
import { IconDotsVertical, IconEdit, IconCopy, IconTrash, IconEye } from "@tabler/icons-react";
import { Image, Badge, Dropdown } from "react-bootstrap";
import Link from "next/link";
import { QuizType } from "types/QuizType";

const formatDate = (dateString: string) => {
    if (!dateString) return "";
    return new Date(dateString).toLocaleDateString("fr-FR", {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
};

const getLevelBadge = (level: string) => {
    switch (level) {
        case "avance":
            return { bg: "danger-subtle", text: "danger-emphasis", label: "Avancé" };
        case "intermediaire":
            return { bg: "warning-subtle", text: "warning-emphasis", label: "Intermédiaire" };
        default:
            return { bg: "primary-subtle", text: "primary-emphasis", label: "Débutant" };
    }
};

const getStatusBadge = (status: string) => {
    return status === "published"
        ? { bg: "success-subtle", text: "success-emphasis", label: "Publié" }
        : { bg: "secondary-subtle", text: "secondary-emphasis", label: "Brouillon" };
};

export const getQuizListColumns = (onDelete: (id: string) => void): ColumnDef<QuizType>[] => [
    {
        accessorKey: "title",
        header: "Titre du Quiz",
        cell: ({ row }) => {
            return (
                <div className="d-flex align-items-center gap-4">
                    {/* Placeholder image logic or fetch if available (API doesn't return image currently) */}
                    <div className="icon-shape icon-lg bg-light-primary text-primary rounded-3 flex-shrink-0">
                        {row.original.title.charAt(0).toUpperCase()}
                    </div>
                    <div>
                        <h5 className="mb-1 fs-6">
                            <Link href={`/quiz/editor?id=${row.original.id}`} className="text-inherit">
                                {row.original.title}
                            </Link>
                        </h5>
                        <div className="d-flex gap-3 text-secondary fs-6">
                            <span>{formatDate(row.original.created_at)}</span>
                        </div>
                    </div>
                </div>
            );
        },
    },
    {
        accessorKey: "category_name",
        header: "Catégorie",
        cell: ({ row }) => <span className="fw-semi-bold">{row.original.category_name || "N/A"}</span>
    },
    {
        accessorKey: "level",
        header: "Niveau",
        cell: ({ row }) => {
            const { bg, text, label } = getLevelBadge(row.original.level);
            return <Badge bg={bg} text={text}>{label}</Badge>
        }
    },
    // Progression column removed as requested
    {
        accessorKey: "status",
        header: "Statut",
        cell: ({ row }) => {
            const { bg, text, label } = getStatusBadge(row.original.status);
            return (
                <Badge bg={bg} text={text}>
                    {label}
                </Badge>
            );
        },
    },
    {
        id: "action",
        header: "Actions",
        cell: ({ row }) => {
            return (
                <Dropdown drop="start">
                    <Dropdown.Toggle variant="ghost" bsPrefix="rounded-circle btn-icon">
                        <IconDotsVertical size={20} />
                    </Dropdown.Toggle>
                    <Dropdown.Menu align={"end"}>
                        <Dropdown.Item href={`/quiz/editor?id=${row.original.id}`} className="d-flex align-items-center gap-2">
                            <IconEdit size={16} /> Éditer
                        </Dropdown.Item>
                        <Dropdown.Item
                            className="d-flex align-items-center gap-2 text-danger"
                            onClick={() => onDelete(row.original.id)}
                        >
                            <IconTrash size={16} /> Supprimer
                        </Dropdown.Item>
                    </Dropdown.Menu>
                </Dropdown>
            );
        },
    },
];
