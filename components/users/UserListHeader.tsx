//import node modules libraries
import { Row, Col, Button } from "react-bootstrap";
import { IconUserPlus } from "@tabler/icons-react";

//import custom components
import Flex from "components/common/Flex";
import DasherBreadcrumb from "components/common/DasherBreadcrumb";

const UserListHeader = () => {
    return (
        <Row>
            <Col lg={12} md={12}>
                <Flex
                    className="mb-8"
                    breakpoint="md"
                    justifyContent="between"
                    alignItems="center"
                >
                    <div>
                        <h1 className="mb-3 h2">Utilisateurs</h1>
                        <DasherBreadcrumb />
                    </div>
                    <div>
                        {/* 
            <Button
              href="#"
              variant="primary"
              className="d-md-flex align-items-center gap-1"
            >
              <IconUserPlus size={18} />
              Nouvel Utilisateur
            </Button>
             */}
                    </div>
                </Flex>
            </Col>
        </Row>
    );
};

export default UserListHeader;
