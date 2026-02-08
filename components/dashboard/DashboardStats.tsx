//import node modules libraries
import { Col, Card, CardBody } from "react-bootstrap";
import {
  IconBriefcase,
  IconListCheck,
  IconSnowboarding,
  IconUsers,
} from "@tabler/icons-react";
import { AdminStatsType } from "types/DashboardTypes";

interface DashboardStatsProps {
  stats: AdminStatsType | null;
}

const DashboardStats = ({ stats }: DashboardStatsProps) => {
  const data = [
    {
      id: 1,
      title: "Total Utilisateurs",
      value: stats?.total_users || 0,
      icon: <IconUsers size={24} strokeWidth={1.5} />,
      bgColor: "bg-light-primary",
      textColor: "text-primary",
    },
    {
      id: 2,
      title: "Total Quiz",
      value: stats?.total_quizzes || 0,
      icon: <IconListCheck size={24} strokeWidth={1.5} />,
      bgColor: "bg-light-info",
      textColor: "text-info",
    },
    {
      id: 3,
      title: "Total Catégories",
      value: stats?.total_categories || 0,
      icon: <IconSnowboarding size={24} strokeWidth={1.5} />,
      bgColor: "bg-light-warning",
      textColor: "text-warning",
    },
    {
      id: 4,
      title: "Taux de réussite (Débutant)",
      value: (stats?.success_rates?.debutant?.success_rate || 0) + "%",
      icon: <IconBriefcase size={24} strokeWidth={1.5} />, // Changed icon
      bgColor: "bg-light-success",
      textColor: "text-success",
    },
  ];

  return (
    <>
      {data.map((stat) => (
        <Col xl={3} md={6} key={stat.id}>
          <Card className={`card-lg border-0 shadow-sm`}>
            <CardBody className="p-4">
              <div className="d-flex justify-content-between align-items-center mb-4">
                <div>
                  <div className={`icon-shape icon-md rounded-3 ${stat.bgColor} ${stat.textColor}`}>
                    {stat.icon}
                  </div>
                </div>
              </div>
              <div>
                <h4 className="fw-bold mb-1">{stat.value}</h4>
                <span className="fs-6 text-muted">{stat.title}</span>
              </div>
            </CardBody>
          </Card>
        </Col>
      ))}
    </>
  );
};

export default DashboardStats;
