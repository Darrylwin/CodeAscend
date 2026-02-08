//import node modules libraries
import { Fragment } from "react";
import { Metadata } from "next";

//import custom components
import UserListHeader from "components/users/UserListHeader";
import UserList from "components/users/UserList";

export const metadata: Metadata = {
    title: "Utilisateurs | Admin Dashboard",
    description: "User Management",
};

const UsersPage = () => {
    return (
        <Fragment>
            <UserListHeader />
            <UserList />
        </Fragment>
    );
};

export default UsersPage;
