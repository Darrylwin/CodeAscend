"use client";
import { Fragment, useState, useEffect, useMemo } from "react";
import {
    Row,
    Col,
    Card,
    CardHeader,
    FormControl,
    Button,
    Badge,
    Dropdown,
    Spinner,
    Alert
} from "react-bootstrap";
import { IconFilter, IconEdit, IconTrash, IconDotsVertical } from "@tabler/icons-react";
import Link from 'next/link';

//import custom components
import TanstackTable from "components/table/TanstackTable";
import { Avatar } from "components/common/Avatar";
import UserModal from "./UserModal";
import ConfirmModal from "components/common/ConfirmModal";

//import custom types
import { UserType } from "types/UserType";
import { ColumnDef } from "@tanstack/react-table";

const UserList = () => {
    const [users, setUsers] = useState<UserType[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState("");
    const [searchTerm, setSearchTerm] = useState("");

    // Modal states
    const [showModal, setShowModal] = useState(false);
    const [selectedUser, setSelectedUser] = useState<UserType | null>(null);
    const [showConfirmModal, setShowConfirmModal] = useState(false);
    const [userToDelete, setUserToDelete] = useState<UserType | null>(null);

    const fetchUsers = async () => {
        setIsLoading(true);
        setError("");
        try {
            const token = localStorage.getItem("access_token");
            const queryParams = new URLSearchParams({
                per_page: "100" // Fetching more for client-side pagination for now
            });
            if (searchTerm) queryParams.append("search", searchTerm);

            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/users?${queryParams}`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                if (response.status === 401 || response.status === 403) {
                    throw new Error("Non autorisé. Vérifiez vos droits d'administrateur.");
                }
                throw new Error("Erreur lors du chargement des utilisateurs");
            }

            const data = await response.json();
            setUsers(data.data || []);
        } catch (err: any) {
            console.error(err);
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    // Debounce search
    useEffect(() => {
        const timer = setTimeout(() => {
            fetchUsers();
        }, 500);
        return () => clearTimeout(timer);
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [searchTerm]);

    const handleEdit = (user: UserType) => {
        setSelectedUser(user);
        setShowModal(true);
    };

    const handleDeleteClick = (user: UserType) => {
        setUserToDelete(user);
        setShowConfirmModal(true);
    };

    const confirmDelete = async () => {
        if (!userToDelete) return;
        try {
            const token = localStorage.getItem("access_token");
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/users/${userToDelete.id}`, {
                method: "DELETE",
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "Erreur lors de la suppression");
            }

            // Refresh list
            fetchUsers();
            setShowConfirmModal(false);
            setUserToDelete(null);
        } catch (err: any) {
            alert(err.message);
        }
    };

    const columns = useMemo<ColumnDef<UserType>[]>(
        () => [
            {
                accessorKey: "name",
                header: "Utilisateur",
                cell: ({ row }) => {
                    return (
                        <div className="d-flex align-items-center">
                            <div className="avatar avatar-md rounded-circle bg-primary-subtle text-primary mb-0 flex-center fw-bold">
                                {row.original.name.charAt(0).toUpperCase()}
                            </div>
                            <div className="ms-3">
                                <h5 className="mb-0">
                                    <Link href="#!" className="text-inherit" onClick={() => handleEdit(row.original)}>
                                        {row.original.name}
                                    </Link>
                                </h5>
                                <small className="text-muted">{row.original.email}</small>
                            </div>
                        </div>
                    );
                },
            },
            {
                accessorKey: "role",
                header: "Rôle",
                cell: ({ row }) => {
                    const role = row.original.role;
                    return (
                        <Badge
                            bg={role === "admin" ? "danger" : "primary"}
                            pill
                        >
                            {role === "admin" ? "Admin" : "Utilisateur"}
                        </Badge>
                    );
                },
            },
            {
                accessorKey: "created_at",
                header: "Inscrit le",
                cell: ({ row }) => {
                    return new Date(row.original.created_at).toLocaleDateString();
                }
            },
            {
                id: "actions",
                header: "Actions",
                cell: ({ row }) => {
                    return (
                        <Dropdown drop="start">
                            <Dropdown.Toggle variant="ghost" bsPrefix="rounded-circle btn-icon">
                                <IconDotsVertical size={20} />
                            </Dropdown.Toggle>
                            <Dropdown.Menu align={"end"}>
                                <Dropdown.Item onClick={() => handleEdit(row.original)} className="d-flex align-items-center gap-2">
                                    <IconEdit size={16} /> Modifier
                                </Dropdown.Item>
                                <Dropdown.Item onClick={() => handleDeleteClick(row.original)} className="d-flex align-items-center gap-2 text-danger">
                                    <IconTrash size={16} /> Supprimer
                                </Dropdown.Item>
                            </Dropdown.Menu>
                        </Dropdown>
                    );
                },
            },
        ],
        []
    );

    return (
        <Fragment>
            <Row>
                <Col>
                    <Card className="card-lg">
                        <CardHeader className="border-bottom-0">
                            <Row className="g-4">
                                <Col lg={4} md={6}>
                                    <FormControl
                                        type="search"
                                        className="listjs-search"
                                        placeholder="Rechercher un utilisateur (nom, email)..."
                                        value={searchTerm}
                                        onChange={(e) => setSearchTerm(e.target.value)}
                                    />
                                </Col>
                                <Col lg={8} md={6} className="d-flex justify-content-end">
                                </Col>
                            </Row>
                        </CardHeader>

                        {isLoading ? (
                            <div className="text-center p-5">
                                <Spinner animation="border" variant="primary" />
                            </div>
                        ) : error ? (
                            <div className="p-4">
                                <Alert variant="danger">{error}</Alert>
                            </div>
                        ) : (
                            <TanstackTable
                                data={users}
                                columns={columns}
                                pagination={true}
                                isSortable
                            />
                        )}
                    </Card>
                </Col>
            </Row>

            <UserModal
                show={showModal}
                onHide={() => setShowModal(false)}
                user={selectedUser}
                onSave={fetchUsers}
            />

            <ConfirmModal
                show={showConfirmModal}
                onHide={() => setShowConfirmModal(false)}
                onConfirm={confirmDelete}
                title="Supprimer l'utilisateur"
                message={`Êtes-vous sûr de vouloir supprimer définitivement ${userToDelete?.name} ? Cette action est irréversible.`}
                type="delete"
                confirmText="Supprimer"
            />
        </Fragment>
    );
};

export default UserList;
