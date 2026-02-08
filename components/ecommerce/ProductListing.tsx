"use client";
//import node modules libraries
import { Fragment, useState, useMemo } from "react";
import {
  Row,
  Col,
  Card,
  CardHeader,
  FormControl,
  Button,
  Dropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  Image,
  Badge
} from "react-bootstrap";
import { IconFilter, IconEdit, IconTrash } from "@tabler/icons-react";
import Link from 'next/link';

//import custom components
import Flex from "components/common/Flex";
import TanstackTable from "components/table/TanstackTable";
import DasherTippy from "components/common/DasherTippy";
import Checkbox from "components/table/Checkbox";
import CategoryModal from "./CategoryModal";

//import custom types
import { CategoryType } from "types/EcommerceType";
import { ColumnDef } from "@tanstack/react-table";



const ProductListing = ({
  data,
  onEdit,
  onDelete
}: {
  data: CategoryType[],
  onEdit: (cat: CategoryType) => void,
  onDelete: (id: string) => void
}) => {
  const columns = useMemo<ColumnDef<CategoryType>[]>(
    () => [
      {
        id: "select",
        header: ({ table }) => (
          <Checkbox
            {...{
              checked: table.getIsAllRowsSelected(),
              indeterminate: table.getIsSomeRowsSelected(),
              onChange: table.getToggleAllRowsSelectedHandler(),
            }}
          />
        ),
        cell: ({ row }) => (
          <div className="px-1">
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
              {row.original.icon_url ? (
                <Image
                  src={row.original.icon_url}
                  alt=""
                  className="rounded-3"
                  width="40"
                  onError={(e) => {
                    // Fallback if image fails
                    e.currentTarget.style.display = 'none';
                    e.currentTarget.nextElementSibling?.classList.remove('d-none');
                  }}
                />
              ) : null}
              {/* Fallback icon div if URL is missing or broken (handled via onError above ideally, simplified here) */}
              <div className={`icon-shape icon-md bg-light text-primary rounded-3 ${row.original.icon_url ? 'd-none' : ''}`}>
                {/* Default icon or first letter */}
                {row.original.name.charAt(0)}
              </div>

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
        accessorKey: "is_active",
        header: "Statut",
        cell: ({ row }) => {
          const isActive = row.original.is_active;
          return (
            <Badge
              bg={`${isActive ? "success-subtle" : "danger-subtle"}`}
              text={`${isActive ? "success-emphasis" : "danger-emphasis"}`}
              pill={true}
            >
              {isActive ? "Actif" : "Inactif"}
            </Badge>
          );
        },
      },
      {
        id: "actions",
        header: "Action",
        cell: ({ row }) => {
          return (
            <Fragment>
              <DasherTippy content="Modifier">
                <Button
                  variant="ghost btn-icon"
                  size="sm"
                  className="rounded-circle"
                  onClick={() => onEdit(row.original)}
                >
                  <IconEdit size={16} />
                </Button>
              </DasherTippy>
              <DasherTippy content="Supprimer">
                <Button
                  variant="ghost btn-icon"
                  size="sm"
                  className="rounded-circle"
                  onClick={() => onDelete(row.original.id)}
                >
                  <IconTrash size={16} />
                </Button>
              </DasherTippy>
            </Fragment>
          );
        },
      },
    ],
    [onEdit, onDelete]
  );

  return (
    <Fragment>
      <Row>
        <Col>
          <Card className="card-lg" id="categoryList">
            <CardHeader className="border-bottom-0">
              <Row className="g-4">
                <Col lg={4}>
                  <FormControl
                    type="search"
                    className="listjs-search"
                    placeholder="Rechercher..."
                  />
                </Col>
                <Col lg={8} className="d-flex justify-content-end">
                  <Flex alignItems="center" breakpoint="lg" className="gap-2">
                    <div>
                      <Button variant="white" className="d-flex align-items-center gap-2">
                        <IconFilter size={16} /> Filtres
                      </Button>
                    </div>
                  </Flex>
                </Col>
              </Row>
            </CardHeader>

            {/* Category List Table */}
            <TanstackTable
              data={data}
              columns={columns}
              pagination={true}
              isSortable
            />
          </Card>
        </Col>
      </Row>
    </Fragment>
  );
};

export default ProductListing;
