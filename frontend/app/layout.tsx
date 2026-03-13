import type { Metadata } from "next";
import Navbar from "@/components/navbar"
import style from "./style/layout.module.css"
import "./globals.css";

export const metadata: Metadata = {
  title: "Dreelio",
  description: "For Your Needed",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return(
    <html lang="en">
      <head>
      </head>
      <body className={style.body}>
        <Navbar />
        <main>{children}</main>
      </body>
    </html>
  )
}