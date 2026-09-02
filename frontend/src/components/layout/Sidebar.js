'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

const navItems = [
  { name: 'Tableau de bord', href: '/', icon: '📊' },
  { name: 'Base d\'Applications', href: '/applications', icon: '📱' },
  { name: 'Sources de Données', href: '/data-sources', icon: '🗄️' },
  { name: 'Stratégie IAM & Sécurité Network', href: '/iam-security', icon: '🔒' },
];

export default function Sidebar({ open, setOpen }) {
  const pathname = usePathname();

  return (
    <>
      {/* Mobile overlay – visible only when sidebar is open */}
      {open && (
        <div
          className="fixed inset-0 z-30 bg-black/50 md:hidden"
          onClick={() => setOpen(false)}
        />
      )}

      <aside
        className={`
          fixed inset-y-0 left-0 z-40 w-64 bg-slate-900 text-slate-100 flex flex-col
          border-r border-slate-800 transition-transform duration-300 ease-in-out
          transform -translate-x-full
          ${open ? 'translate-x-0' : ''}
          md:static md:translate-x-0 md:z-auto md:min-h-screen md:shrink-0
        `}
      >
        {/* Sidebar content unchanged */}
        <div className="p-5 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-lg bg-indigo-600 flex items-center justify-center font-bold text-lg text-white shadow-md">
              A
            </div>
            <div>
              <h1 className="font-bold text-base text-white leading-tight">AdoptAI</h1>
              <p className="text-xs text-slate-400">App Knowledge Base</p>
            </div>
          </div>
        </div>

        <div className="px-3 py-4 text-xs font-semibold uppercase tracking-wider text-slate-400">
          Navigation
        </div>

        <nav className="flex-1 px-3 space-y-1">
          {navItems.map((item) => {
            const isActive = pathname === item.href || (item.href !== '/' && pathname.startsWith(item.href));
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setOpen(false)} // close sidebar after navigation on mobile
                className={`flex items-center gap-3 px-3 py-2.5 rounded-md text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-indigo-600 text-white shadow'
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                }`}
              >
                <span className="text-base">{item.icon}</span>
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>

        <div className="p-4 border-t border-slate-800 text-xs text-slate-400">
          <p className="font-semibold text-slate-300">Cahier des Charges v0.1</p>
          <p>Manager : Khadija Boukhatem</p>
          <p className="mt-1 text-[11px] text-slate-500">Réseau AHDIGITAL • IAM Monitoring</p>
        </div>
      </aside>
    </>
  );
}