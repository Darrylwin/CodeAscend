"use client";
//import node modules libraries
import { IconCircleCheck, IconCircleDashedCheck } from "@tabler/icons-react";
import { Row, Col, Card, CardBody } from "react-bootstrap";

//import custom components
import DasherTippy from "components/common/DasherTippy";
import CustomProgressBar from "components/common/CustomProgressBar";

interface SuccessRatesProps {
  successRates?: {
    [key: string]: {
      avg_score: number;
      success_rate: number;
    }
  };
}

const TaskProgress = ({ successRates }: SuccessRatesProps) => {
  const beginner = successRates?.debutant?.success_rate || 0;
  const intermediate = successRates?.intermediaire?.success_rate || 0;
  const advanced = successRates?.avance?.success_rate || 0;

  const average = Math.round(((beginner + intermediate + advanced) / 3) * 10) / 10;

  return (
    <Card className="card-lg mb-6">
      <CardBody>
        <div className="mb-4">
          <h5 className="mb-0">Taux de réussite par niveau</h5>
        </div>
        <div className="fs-1 fw-bold mb-3">{average}%</div>
        <div className="d-flex align-items-center gap-1 w-100 mb-4">
          <div className="w-100">
            <DasherTippy content="Débutant">
              <CustomProgressBar
                className="mb-2"
                now={beginner}
                style={{ height: "6px" }}
                variant="success"
              />
            </DasherTippy>
            {beginner}%
          </div>
          <div className="w-100">
            <DasherTippy content="Intermédiaire">
              <CustomProgressBar
                className="mb-2"
                now={intermediate}
                style={{ height: "6px" }}
                variant="warning"
              />
            </DasherTippy>
            {intermediate}%
          </div>
          <div className="w-100">
            <DasherTippy content="Avancé">
              <CustomProgressBar
                className="mb-2"
                now={advanced}
                style={{ height: "6px" }}
                variant="danger"
              />
            </DasherTippy>
            {advanced}%
          </div>
        </div>
        <div className="bg-gray-100 p-3 rounded-4">
          <Row className="g-3">
            <Col md={4}>
              <Card className="card-lg">
                <CardBody className="text-center p-3">
                  <div className="icon-shape icon-lg bg-success-subtle text-success-emphasis rounded-pill">
                    <IconCircleCheck size={20} />
                  </div>
                  <div className="lh-1 mt-4">
                    <div className="fs-4 fw-bold mb-1">{beginner}%</div>
                    <div className="text-secondary small">Débutant</div>
                  </div>
                </CardBody>
              </Card>
            </Col>
            <Col md={4}>
              <Card className="card-lg">
                <CardBody className="text-center p-3">
                  <div className="icon-shape icon-lg bg-warning-subtle text-warning-emphasis rounded-pill">
                    <IconCircleCheck size={20} />
                  </div>
                  <div className="lh-1 mt-4">
                    <div className="fs-4 fw-bold mb-1">{intermediate}%</div>
                    <div className="text-secondary small">Intermédiaire</div>
                  </div>
                </CardBody>
              </Card>
            </Col>
            <Col md={4}>
              <Card className="card-lg">
                <CardBody className="text-center p-3">
                  <div className="icon-shape icon-lg bg-danger-subtle text-danger-emphasis rounded-pill">
                    <IconCircleDashedCheck size={20} />
                  </div>
                  <div className="lh-1 mt-4">
                    <div className="fs-4 fw-bold mb-1">{advanced}%</div>
                    <div className="text-secondary small">Avancé</div>
                  </div>
                </CardBody>
              </Card>
            </Col>
          </Row>
        </div>
      </CardBody>
    </Card>
  );
};

export default TaskProgress;
