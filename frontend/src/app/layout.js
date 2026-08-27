import "./globals.css";
import { Inter } from "next/font/google";

import Sidebar from "@/components/layout/Sidebar";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
});

export default function RootLayout({ children }) {
  return (
    <html lang="fr" className="h-full bg-slate-50">
      <body
        className={`${inter.variable} h-full flex text-slate-800 antialiased font-sans`}
      >
        <Sidebar />

        <div className="flex-1 flex flex-col min-w-0 overflow-y-auto">
          {children}
        </div>
      </body>
    </html>
  );
}