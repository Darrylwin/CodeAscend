"use client";
//import node modules libraries
import { ColumnDef } from "@tanstack/react-table";
import { Badge, Dropdown } from "react-bootstrap";
import { IconDotsVertical } from "@tabler/icons-react";

//import custom typs
import { PopularQuizType } from "types/DashboardTypes";

//import custom components
import ActionMenu from "components/common/ActionMenu";
import CustomProgressBar from "components/common/CustomProgressBar";

export const PopularQuizColumns: ColumnDef<PopularQuizType>[] = [
  {
    accessorKey: "title",
    header: "Quiz",
    cell: ({ row }) => {
      const title = row.original.title;
      return <div className="fw-bold">{title}</div>;
    },
  },
  {
    accessorKey: "attempts",
    header: "Participations",
    cell: ({ row }) => {
      const attempts = row.original.attempts;
      return <div className="fw-bold fs-4">{attempts}</div>;
    },
  },
  {
    accessorKey: "avg_score",
    header: "Score Moyen",
    cell: ({ row }) => {
      const score = row.original.avg_score;
      const variant = score >= 80 ? "success" : score >= 50 ? "warning" : "danger";
      return (
        <div className="d-flex align-items-center">
          <div className="me-2 text-dark fw-bold">{score}%</div>
          <div className="w-100">
            <CustomProgressBar variant={variant} now={score} className="mb-0" style={{ height: "6px" }} />
          </div>
        </div>
      );
    },
  },
  {
    header: "Actions",
    cell: () => {
      return (
        <ActionMenu
          toggleButton={<IconDotsVertical size={20} />}
          className="btn btn-ghost btn-icon btn-sm rounded-circle"
          drop="start"
          align="start"
        >
          <Dropdown.Item>Voir détails</Dropdown.Item>
        </ActionMenu>
      );
    },
  },
];
