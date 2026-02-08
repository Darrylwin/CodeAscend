"use client";
import { Card, CardHeader, CardFooter, Button } from "react-bootstrap";
import TanstackTable from "components/table/TanstackTable";
import { PopularQuizColumns } from "components/dashboard/ColumnDefination";
import { PopularQuizType } from "types/DashboardTypes";

interface PopularQuizzesProps {
  data: PopularQuizType[];
}

const PopularQuizzes = ({ data }: PopularQuizzesProps) => {
  return (
    <Card className="card-lg mb-6">
      <CardHeader className="border-bottom-0">
        <h5 className="mb-0">Quiz les plus passés</h5>
      </CardHeader>
      <div>
        <TanstackTable data={data} columns={PopularQuizColumns} />
      </div>
      <CardFooter className=" border-dashed border-top text-center">
        <Button href="/quiz" variant="link">
          Voir tous les quiz
        </Button>
      </CardFooter>
    </Card>
  );
};

export default PopularQuizzes;
