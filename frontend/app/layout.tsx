import type { Metadata } from "next";
import style from "./style/layout.module.css";
import "./globals.css";
import NavbarWrapper from "@/components/navbarWrapper";

export const metadata: Metadata = {
  title: "GaniSaid",
  description: "For Your Needed",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className={style.body}>
        <NavbarWrapper />
        <main>{children}</main>
      </body>
    </html>
  );
}