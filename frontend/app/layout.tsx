"use client";

import type { Metadata } from "next";
import Navbar from "@/components/navbar";
import style from "./style/layout.module.css";
import "./globals.css";
import { usePathname } from "next/navigation";

export const metadata: Metadata = {
  title: "Dreelio",
  description: "For Your Needed",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();

  const hideNavbarRoutes = ["/chatbot", "/contact"];
  const hideNavbar = hideNavbarRoutes.includes(pathname || "");

  return (
    <html lang="en">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
      </head>
      <body className={style.body}>
        {!hideNavbar && <Navbar />}
        <main>{children}</main>
      </body>
    </html>
  );
}