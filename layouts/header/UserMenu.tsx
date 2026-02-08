//import node modules libraries
import React, { useEffect, useState } from "react";
import { Dropdown, Image } from "react-bootstrap";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { IconLogin2 } from "@tabler/icons-react";

//import routes files
import { UserMenuItem } from "routes/HeaderRoute";

//import custom components
import { Avatar } from "components/common/Avatar";

interface UserToggleProps {
  children?: React.ReactNode;
  onClick?: (e: React.MouseEvent<HTMLAnchorElement, MouseEvent>) => void;
}
const CustomToggle = React.forwardRef<HTMLAnchorElement, UserToggleProps>(
  ({ children, onClick }, ref) => (
    <Link
      ref={ref}
      href="#"
      onClick={(e) => {
        e.preventDefault();
        onClick?.(e);
      }}
    >
      {children}
    </Link>
  )
);

CustomToggle.displayName = 'CustomToggle';

interface UserData {
  id: string;
  name: string;
  email: string;
  role: string;
}

const UserMenu = () => {
  const router = useRouter();
  const [user, setUser] = useState<UserData | null>(null);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const token = localStorage.getItem('access_token');
        if (!token) return;

        const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/me`, {
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });

        if (response.ok) {
          const data = await response.json();
          setUser(data);
        }
      } catch (error) {
        console.error("Failed to fetch user data:", error);
      }
    };

    fetchUser();
  }, []);

  const handleLogout = async (e: React.MouseEvent) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('access_token');
      if (token) {
        await fetch(`${process.env.NEXT_PUBLIC_API_URL}/auth/logout`, {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${token}`
          }
        });
        localStorage.removeItem('access_token');
        document.cookie = "access_token=; path=/; max-age=0"; // Clear cookie
      }

      router.push("/sign-in");
      router.refresh();
    } catch (error) {
      console.error("Logout failed:", error);
      // Fallback logout even if API fails
      localStorage.removeItem('access_token');
      document.cookie = "access_token=; path=/; max-age=0"; // Clear cookie on fallback
      router.push("/sign-in");
    }
  };

  return (
    <Dropdown>
      <Dropdown.Toggle as={CustomToggle}>
        <Avatar
          type="image"
          src="/images/avatar/avatar-1.jpg"
          size="sm"
          alt="User Avatar"
          className="rounded-circle"
        />
      </Dropdown.Toggle>
      <Dropdown.Menu align="end" className="p-0 dropdown-menu-md">
        <div className="d-flex gap-3 align-items-center border-dashed border-bottom px-4 py-4">
          <Image
            src="/images/avatar/avatar-1.jpg"
            alt=""
            className="avatar avatar-md rounded-circle"
          />
          <div>
            <h4 className="mb-0 fs-5">{user?.name || "User"}</h4>
            <p className="mb-0 text-secondary small">{user?.email || ""}</p>
          </div>
        </div>
        <div className="p-3 d-flex flex-column gap-1">
          {UserMenuItem.map((item) => (
            <Dropdown.Item
              key={item.id}
              className="d-flex align-items-center gap-2"
            >
              <span>{item.icon}</span>
              <span>{item.title}</span>
            </Dropdown.Item>
          ))}
        </div>
        <div className="border-dashed border-top mb-4 pt-4 px-6">
          <Link
            href="#"
            onClick={handleLogout}
            className="text-secondary d-flex align-items-center gap-2"
          >
            <span>
              <IconLogin2 size={20} strokeWidth={1.5} />
            </span>
            <span>Logout</span>
          </Link>
        </div>
      </Dropdown.Menu>
    </Dropdown>
  );
};

export default UserMenu;
