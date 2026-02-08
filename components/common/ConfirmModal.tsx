
import { Modal, Button } from "react-bootstrap";
import { IconAlertTriangle, IconCheck, IconTrash, IconAlertCircle } from "@tabler/icons-react";

interface ConfirmModalProps {
    show: boolean;
    onHide: () => void;
    onConfirm?: () => void;
    title: string;
    message: string;
    variant?: "primary" | "secondary" | "success" | "danger" | "warning" | "info" | "light" | "dark";
    confirmText?: string;
    cancelText?: string;
    type?: "confirm" | "alert" | "delete";
}

const ConfirmModal = ({
    show,
    onHide,
    onConfirm,
    title,
    message,
    variant = "primary",
    confirmText = "Confirmer",
    cancelText = "Annuler",
    type = "confirm"
}: ConfirmModalProps) => {

    const renderIcon = () => {
        if (type === "delete") return <div className="avatar avatar-lg rounded-circle bg-danger-subtle text-danger mb-3 mx-auto flex-center"><IconTrash size={24} /></div>;
        if (variant === "danger" || type === "alert") return <div className="avatar avatar-lg rounded-circle bg-danger-subtle text-danger mb-3 mx-auto flex-center"><IconAlertCircle size={24} /></div>;
        if (variant === "success") return <div className="avatar avatar-lg rounded-circle bg-success-subtle text-success mb-3 mx-auto flex-center"><IconCheck size={24} /></div>;
        return <div className="avatar avatar-lg rounded-circle bg-warning-subtle text-warning mb-3 mx-auto flex-center"><IconAlertTriangle size={24} /></div>;
    };

    // Add custom flex-center helper class or style if not available globally, but bootstrap has d-flex justify-content-center align-items-center
    const iconWrapper = (icon: React.ReactNode, bgClass: string, textClass: string) => (
        <div className={`avatar avatar-xl rounded-circle ${bgClass} ${textClass} mb-4 mx-auto d-flex justify-content-center align-items-center`}>
            {icon}
        </div>
    );

    const getIcon = () => {
        if (type === "delete") return iconWrapper(<IconTrash size={40} />, "bg-danger-subtle", "text-danger");
        if (variant === "danger") return iconWrapper(<IconAlertCircle size={40} />, "bg-danger-subtle", "text-danger");
        if (variant === "success") return iconWrapper(<IconCheck size={40} />, "bg-success-subtle", "text-success");
        // Default warning/alert
        return iconWrapper(<IconAlertTriangle size={40} />, "bg-warning-subtle", "text-warning");
    };

    return (
        <Modal show={show} onHide={onHide} centered className="confirmation-modal">
            <Modal.Body className="text-center p-5">
                {getIcon()}
                <h3 className="mb-2">{title}</h3>
                <p className="mb-4 text-muted">{message}</p>
                <div className="d-flex justify-content-center gap-2">
                    {type !== "alert" && (
                        <Button variant="light" onClick={onHide}>
                            {cancelText}
                        </Button>
                    )}
                    <Button
                        variant={type === "delete" ? "danger" : variant}
                        onClick={() => {
                            if (onConfirm) onConfirm();
                            if (type === "alert") onHide(); // Auto close on alert confirm
                        }}
                    >
                        {type === "alert" ? "OK" : confirmText}
                    </Button>
                </div>
            </Modal.Body>
        </Modal>
    );
};

export default ConfirmModal;
