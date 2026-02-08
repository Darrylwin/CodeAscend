//import node module libraries
import { Fragment } from "react";
import { ColumnDef } from "@tanstack/react-table";
import { IconEdit, IconEye, IconTrash } from "@tabler/icons-react";
import { Badge, Button, Image } from "react-bootstrap";
import Link from "next/link";

//import custom types
import { CategoryType } from "types/EcommerceType";

//import custom components
import DasherTippy from "components/common/DasherTippy";
import Checkbox from "components/table/Checkbox";

export const categoryColumns: ColumnDef<CategoryType>[] = [
  {
    id: "select",
    header: ({ table }) => {
      return (
        <Checkbox
          {...{
            checked: table.getIsAllRowsSelected(),
            indeterminate: table.getIsSomeRowsSelected(),
            onChange: table.getToggleAllRowsSelectedHandler(),
          }}
        />
      );
    },
    cell: ({ row }) => (
      <div>
        <Checkbox
          {...{
            checked: row.getIsSelected(),
            disabled: !row.getCanSelect(),
            indeterminate: row.getIsSomeSelected(),
            onChange: row.getToggleSelectedHandler(),
          }}
        />
      </div>
    ),
  },
  {
    accessorKey: "name",
    header: "Catégorie",
    cell: ({ row }) => {
      return (
        <div className="d-flex align-items-center">
          <Image
            src={row.original.icon_url}
            alt=""
            className="rounded-3"
            width="40"
          />
          <div className="ms-3 d-flex flex-column">
            <Link href="#!" className="text-inherit fw-semibold">
              {row.original.name}
            </Link>
          </div>
        </div>
      );
    },
  },
  {
    accessorKey: "description",
    header: "Description",
  },
  {
    accessorKey: "status",
    header: "Statut",
    cell: ({ row }) => {
      const statusText = row.original.status;
      return (
        <Badge
          bg={`${statusText === "Actif" ? "success-subtle" : "danger-subtle"}`}
          text={`${statusText === "Actif" ? "success-emphasis" : "danger-emphasis"
            }`}
          pill={true}
        >
          {statusText}
        </Badge>
      );
    },
  },
  {
    accessorKey: "",
    header: "Action",
    cell: () => {
      return (
        <Fragment>
          <DasherTippy content="View">
            <Button
              href=""
              variant="ghost btn-icon"
              size="sm"
              className="rounded-circle"
            >
              <IconEye size={16} />
              <div id="eyeThree" className="d-none">
                <span>View</span>
              </div>
            </Button>
          </DasherTippy>
          <DasherTippy content="Modifier">
            <Button
              href=""
              variant="ghost btn-icon"
              size="sm"
              className="rounded-circle"
            >
              <IconEdit size={16} />
            </Button>
          </DasherTippy>
          <DasherTippy content="Supprimer">
            <Button
              href=""
              variant="ghost btn-icon"
              size="sm"
              className="rounded-circle"
            >
              <IconTrash size={16} />
            </Button>
          </DasherTippy>
        </Fragment>
      );
    },
  },
];
