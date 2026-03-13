import type { Metadata } from "next";
import Navbar from "@/components/navbar"
import style from "./style/layout.module.css"

export const metadata: Metadata = {
  title: "Dreelio",
  description: "For Your Needed",
};

// navbar
export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return(
    <html>
      <body className={style.body}>
        <Navbar />
        <main>{children}</main>
      </body>
    </html>
  )
}
