"use client";

import { usePathname } from "next/navigation";
import Navbar from "@/components/navbar";

export default function NavbarWrapper() {
  const pathname = usePathname();

  const hideNavbarRoutes = ["/chatbot", "/contact"];
  const hideNavbar = hideNavbarRoutes.includes(pathname || "");

  if (hideNavbar) return null;

  return <Navbar />;
}