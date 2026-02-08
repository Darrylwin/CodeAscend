"use client";
//import node module libraries
import { Fragment, useEffect, useState } from "react";
import { Col, Row, Spinner, Alert } from "react-bootstrap";
import Link from "next/link"; // Added Link import

//import custom components
import DashboardStats from "components/dashboard/DashboardStats";
import PopularQuizzes from "components/dashboard/ActiveProject";
import TaskProgress from "components/dashboard/TaskProgress";
import { AdminStatsType } from "types/DashboardTypes";

const HomePage = () => {
  const [stats, setStats] = useState<AdminStatsType | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const token = localStorage.getItem("access_token");
        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/stats`, {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });

        if (!response.ok) {
          throw new Error("Impossible de charger les statistiques");
        }

        const data = await response.json();
        setStats(data);
      } catch (err: any) {
        console.error(err);
        setError(err.message);
      } finally {
        setIsLoading(false);
      }
    };

    fetchStats();
  }, []);

  if (isLoading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ minHeight: "100vh" }}>
        <Spinner animation="border" variant="primary" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4">
        <Alert variant="danger">
          Erreur: {error}. Veuillez vérifier que vous êtes bien connecté en tant qu'administrateur.
        </Alert>
      </div>
    );
  }

  return (
    <Fragment>
      <div className="d-flex justify-content-between align-items-center mb-4">
        <div>
          <h3 className="mb-0 fw-bold">Tableau de bord</h3>
        </div>
        <div>
          <Link href="/quiz/editor" className="btn btn-primary">
            Créer un nouveau quiz
          </Link>
        </div>
      </div>

      <Row className="g-6 mb-6">
        <DashboardStats stats={stats} />
      </Row>
      <Row className="g-6 mb-6">
        <Col xl={8}>
          <PopularQuizzes data={stats?.popular_quizzes || []} />
        </Col>
        <Col xl={4}>
          <TaskProgress successRates={stats?.success_rates} />
        </Col>
      </Row>
    </Fragment>
  );
};

export default HomePage;
