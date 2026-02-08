import { cookies } from "next/headers";
import { redirect } from "next/navigation";

//import custom components
import Header from "layouts/header/Header";
import Sidebar from "layouts/Sidebar";

interface DashboardProps {
  children: React.ReactNode;
}

const DashboardLayout = async ({ children }: DashboardProps) => {
  // Check for authentication token
  const cookieStore = await cookies();
  const token = cookieStore.get("access_token");

  if (!token) {
    redirect("/sign-in");
  }

  return (
    <div>
      <Sidebar hideLogo={false} containerId="miniSidebar" />
      <div id="content" className="position-relative h-100">
        <Header />
        <div className="custom-container">{children}</div>
      </div>
    </div>
  );
};

export default DashboardLayout;
