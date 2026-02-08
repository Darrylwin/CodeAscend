"use client";

//import node module libraries
import { Fragment, useState, useEffect, useCallback } from "react";
import { Alert, Spinner } from "react-bootstrap";
//import custom components
import ProductListing from "components/ecommerce/ProductListing";
import EcommerceHeader from "components/ecommerce/EcommerceHeader";
import CategoryModal from "components/ecommerce/CategoryModal";
import ConfirmModal from "components/common/ConfirmModal";
import { CategoryType } from "types/EcommerceType";

const Categories = () => {
  const [data, setData] = useState<CategoryType[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showModal, setShowModal] = useState(false);
  const [selectedCategory, setSelectedCategory] = useState<CategoryType | null>(null);
  const [confirmModal, setConfirmModal] = useState({
    show: false,
    title: "",
    message: "",
    type: "confirm" as "confirm" | "alert" | "delete",
    onConfirm: undefined as (() => void) | undefined,
  });

  const fetchData = useCallback(async () => {
    try {
      setIsLoading(true);
      const token = localStorage.getItem('access_token');
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/categories`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });

      if (!response.ok) {
        throw new Error('Failed to fetch categories');
      }

      const result = await response.json();
      setData(result);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleAddClick = () => {
    setSelectedCategory(null);
    setShowModal(true);
  };

  const handleEditClick = (category: CategoryType) => {
    setSelectedCategory(category);
    setShowModal(true);
  };

  const handleSave = async (formData: any) => {
    try {
      const token = localStorage.getItem('access_token');
      const headers = {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      };

      let response;
      if (selectedCategory) {
        // Update
        response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/categories/${selectedCategory.id}`, {
          method: 'PUT',
          headers,
          body: JSON.stringify(formData)
        });
      } else {
        // Create
        response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/categories`, {
          method: 'POST',
          headers,
          body: JSON.stringify(formData)
        });
      }

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || 'Opération échouée');
      }

      fetchData(); // Refresh list
    } catch (error: any) {
      setConfirmModal({
        show: true,
        title: "Erreur",
        message: error.message || "Une erreur est survenue",
        type: "alert",
        onConfirm: undefined
      });
    }
  };

  const handleDelete = (id: string) => {
    setConfirmModal({
      show: true,
      title: "Confirmer la suppression",
      message: "Voulez-vous vraiment supprimer cette catégorie ?",
      type: "delete",
      onConfirm: async () => {
        try {
          const token = localStorage.getItem('access_token');
          const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/categories/${id}`, {
            method: 'DELETE',
            headers: {
              'Authorization': `Bearer ${token}`
            }
          });

          if (!response.ok) {
            const errData = await response.json();
            setConfirmModal(prev => ({ // Show error modal instead
              ...prev,
              show: true,
              title: "Erreur",
              message: `Erreur: ${errData.detail || 'Impossible de supprimer'}`,
              type: "alert",
              onConfirm: undefined
            }));
            return;
          }

          fetchData();
        } catch (error) {
          console.error("Delete error", error);
          setConfirmModal(prev => ({
            ...prev,
            show: true,
            title: "Erreur",
            message: "Une erreur est survenue lors de la suppression",
            type: "alert",
            onConfirm: undefined
          }));
        }
      }
    });
  };

  return (
    <Fragment>
      <EcommerceHeader onAddClick={handleAddClick} />
      {error && <Alert variant="danger">{error}</Alert>}
      {isLoading ? (
        <div className="d-flex justify-content-center align-items-center" style={{ minHeight: "200px" }}>
          <Spinner animation="border" variant="primary" />
        </div>
      ) : (
        <ProductListing
          data={data}
          onEdit={handleEditClick}
          onDelete={handleDelete}
        />
      )}
      <CategoryModal
        show={showModal}
        onHide={() => setShowModal(false)}
        initialData={selectedCategory}
        onSave={handleSave}
      />
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

export default Categories;
