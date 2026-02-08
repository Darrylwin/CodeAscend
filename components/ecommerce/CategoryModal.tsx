import { useState, useEffect } from "react";
import { Modal, Button, Form } from "react-bootstrap";
import { InputText } from "primereact/inputtext";
import { InputTextarea } from "primereact/inputtextarea";
import { Checkbox } from "primereact/checkbox";
import { CategoryType } from "types/EcommerceType";

interface CategoryModalProps {
    show: boolean;
    onHide: () => void;
    initialData?: CategoryType | null;
    onSave: (data: any) => Promise<void>;
}

const CategoryModal = ({ show, onHide, initialData, onSave }: CategoryModalProps) => {
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");
    const [iconUrl, setIconUrl] = useState("");
    const [isActive, setIsActive] = useState(false);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (show && initialData) {
            setName(initialData.name);
            setDescription(initialData.description);
            setIconUrl(initialData.icon_url || "");
            setIsActive(initialData.is_active);
        } else if (show && !initialData) {
            // Reset for new entry
            setName("");
            setDescription("");
            setIconUrl("");
            setIsActive(true); // Default to active for new content usually? Or false? Let's say true.
        }
    }, [initialData, show]);

    const handleSubmit = async () => {
        setLoading(true);
        const data = {
            name,
            description,
            icon_url: iconUrl,
            is_active: isActive
        };

        try {
            await onSave(data);
            onHide();
        } catch (error) {
            console.error("Save failed", error);
            // Optionally handle error state here
        } finally {
            setLoading(false);
        }
    };

    return (
        <Modal show={show} onHide={onHide} centered className="category-modal">
            <Modal.Header closeButton className="border-0 pb-0">
                <Modal.Title className="h4">{initialData ? "Modifier la Catégorie" : "Créer une Catégorie"}</Modal.Title>
            </Modal.Header>
            <Modal.Body className="pt-3">
                <Form>
                    <div className="d-flex flex-column gap-3">
                        <div className="d-flex flex-column gap-2">
                            <label htmlFor="name" className="fw-medium text-dark">Nom</label>
                            <InputText
                                id="name"
                                value={name}
                                onChange={(e) => setName(e.target.value)}
                                placeholder="Nom de la catégorie"
                                className="p-inputtext-sm form-control shadow-none rounded-3"
                            />
                        </div>

                        <div className="d-flex flex-column gap-2">
                            <label htmlFor="description" className="fw-medium text-dark">Description</label>
                            <InputTextarea
                                id="description"
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                                rows={4}
                                placeholder="Description courte..."
                                className="p-inputtext-sm form-control shadow-none rounded-3"
                                autoResize
                            />
                        </div>

                        <div className="d-flex flex-column gap-2">
                            <label htmlFor="icon" className="fw-medium text-dark">URL de l'icone</label>
                            <InputText
                                id="icon"
                                value={iconUrl}
                                onChange={(e) => setIconUrl(e.target.value)}
                                placeholder="https://example.com/icon.png"
                                className="p-inputtext-sm form-control shadow-none rounded-3"
                            />
                        </div>

                        <div className="d-flex align-items-center gap-2 mt-2">
                            <Checkbox
                                inputId="status"
                                checked={isActive}
                                onChange={(e) => setIsActive(e.checked ?? false)}
                                icon={<></>}
                            />
                            <label htmlFor="status" className="cursor-pointer mb-0">Activer la catégorie</label>
                        </div>
                    </div>
                </Form>
            </Modal.Body>
            <Modal.Footer className="border-0">
                <Button variant="ghost" onClick={onHide} disabled={loading}>
                    Annuler
                </Button>
                <Button variant="primary" onClick={handleSubmit} disabled={loading}>
                    {loading ? "Enregistrement..." : (initialData ? "Sauvegarder" : "Créer")}
                </Button>
            </Modal.Footer>
        </Modal>
    );
};

export default CategoryModal;
