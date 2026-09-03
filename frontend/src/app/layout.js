import "./globals.css";
import { Open_Sans } from "next/font/google";
import AppShell from "@/components/layout/AppShell";

const openSans = Open_Sans({
  subsets: ["latin"],
  variable: "--font-open-sans",
  weight: ["400", "500", "600", "700"],
});

export default function RootLayout({ children }) {
  return (
    <html lang="fr" className={`h-full ${openSans.variable}`}>
      <body className="h-full flex text-slate-800 antialiased" style={{ fontFamily: 'var(--font-open-sans)' }}>
        <AppShell>{children}</AppShell>
      </body>
    </html>
  );
}