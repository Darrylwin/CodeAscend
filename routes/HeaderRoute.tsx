//import node modules libraries
import { v4 as uuid } from "uuid";
import {
  IconActivity,
  IconHome2,
  IconInbox,
  IconMessage,
  IconSettings,
} from "@tabler/icons-react";

export const UserMenuItem = [
  {
    id: uuid(),
    link: "#",
    title: "Account Settings",
    icon: <IconSettings size={20} strokeWidth={1.5} />,
  },
];
