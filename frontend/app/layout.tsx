import type { Metadata } from "next";
import Navbar from "@/components/navbar"

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
      <body>
        <Navbar />
        <main>{children}</main>
      </body>
    </html>
  )
}
