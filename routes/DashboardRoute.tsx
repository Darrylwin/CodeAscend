//import node modules libraries
import { v4 as uuid } from "uuid";
import {
  IconFiles,
  IconShoppingBag,
  IconNews,
  IconFileText,
  IconUser,
} from "@tabler/icons-react";

//import custom type
import { MenuItemType } from "types/menuTypes";

export const DashboardMenu: MenuItemType[] = [
  {
    id: uuid(),
    title: "Dashboard",
    link: "/",
    icon: <IconFiles size={20} strokeWidth={1.5} />,
  },
  {
    id: uuid(),
    title: "Catégories",
    link: "/categories",
    icon: <IconShoppingBag size={20} strokeWidth={1.5} />,
  },
  {
    id: uuid(),
    title: "Quiz",
    link: "/quiz",
    icon: <IconFileText size={20} strokeWidth={1.5} />,
  },
  {
    id: uuid(),
    title: "Utilisateurs",
    link: "/users",
    icon: <IconUser size={20} strokeWidth={1.5} />,
  },

];
