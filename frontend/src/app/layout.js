import './globals.css';
import Sidebar from '@/components/layout/Sidebar';

export default function RootLayout({ children }) {
  return (
    <html lang="fr" className="h-full bg-slate-50">
      <body className="h-full flex text-slate-800 antialiased font-sans">
        <Sidebar />
        <div className="flex-1 flex flex-col min-w-0 overflow-y-auto">
          {children}
        </div>
      </body>
    </html>
  );
}
