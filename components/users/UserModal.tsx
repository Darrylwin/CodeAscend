"use client";
import { Modal, Button, Form, Alert, Spinner } from "react-bootstrap";
import { UserType } from "types/UserType";
import { useState, useEffect } from "react";
import { IconDeviceFloppy } from "@tabler/icons-react";

interface UserModalProps {
    show: boolean;
    onHide: () => void;
    user: UserType | null;
    onSave: () => void; // Callback to refresh list
}

const UserModal = ({ show, onHide, user, onSave }: UserModalProps) => {
    const [name, setName] = useState("");
    const [email, setEmail] = useState("");
    const [role, setRole] = useState<"user" | "admin">("user");
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState("");

    useEffect(() => {
        if (user) {
            setName(user.name);
            setEmail(user.email);
            setRole(user.role);
            setError("");
        }
    }, [user]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!user) return;

        setIsLoading(true);
        setError("");

        try {
            const token = localStorage.getItem("access_token");
            const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/users/${user.id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({ name, email, role })
            });

            if (!response.ok) {
                const errData = await response.json();
                throw new Error(errData.detail || "Erreur lors de la mise à jour");
            }

            onSave();
            onHide();
        } catch (err: any) {
            console.error(err);
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    if (!user) return null;

    return (
        <Modal show={show} onHide={onHide} centered>
            <Modal.Header closeButton>
                <Modal.Title>Modifier Utilisateur</Modal.Title>
            </Modal.Header>
            <Form onSubmit={handleSubmit}>
                <Modal.Body>
                    {error && <Alert variant="danger">{error}</Alert>}

                    <Form.Group className="mb-3">
                        <Form.Label>Nom complet</Form.Label>
                        <Form.Control
                            type="text"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                            required
                        />
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Email</Form.Label>
                        <Form.Control
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </Form.Group>

                    <Form.Group className="mb-3">
                        <Form.Label>Rôle</Form.Label>
                        <Form.Select
                            value={role}
                            onChange={(e) => setRole(e.target.value as "user" | "admin")}
                        >
                            <option value="user">User</option>
                            <option value="admin">Admin</option>
                        </Form.Select>
                    </Form.Group>

                    <div className="text-muted small">
                        Créé le: {new Date(user.created_at).toLocaleDateString()}
                    </div>
                </Modal.Body>
                <Modal.Footer>
                    <Button variant="secondary" onClick={onHide}>Annuler</Button>
                    <Button variant="primary" type="submit" disabled={isLoading} className="d-flex align-items-center gap-2">
                        {isLoading ? <Spinner size="sm" animation="border" /> : <IconDeviceFloppy size={18} />}
                        Enregistrer
                    </Button>
                </Modal.Footer>
            </Form>
        </Modal>
    );
};

export default UserModal;
