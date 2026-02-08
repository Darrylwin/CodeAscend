"use client"
//import node module libraries
import { useState } from "react";
import { Row, Col, Button } from "react-bootstrap";
import { IconPlus } from "@tabler/icons-react";

//import custom components
import Flex from "components/common/Flex";
import DasherBreadcrumb from "components/common/DasherBreadcrumb";
import CategoryModal from "./CategoryModal";

const EcommerceHeader = ({ onAddClick }: { onAddClick: () => void }) => {
  return (
    <Row>
      <Col>
        <Flex
          justifyContent="between"
          alignItems="center"
          className="mb-8 w-100"
          breakpoint="md"
        >
          <div>
            <h1 className="mb-3 h2">Catégories</h1>
            <DasherBreadcrumb />
          </div>
          <div>
            <Button
              variant="primary"
              className="d-md-flex align-items-center gap-2"
              onClick={onAddClick}
            >
              <IconPlus size={18} />
              Nouvelle Catégorie
            </Button>
          </div>
        </Flex>
      </Col>
    </Row>
  );
};

export default EcommerceHeader;
