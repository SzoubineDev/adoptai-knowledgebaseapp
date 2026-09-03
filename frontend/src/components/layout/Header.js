'use client';

export default function Header({ title, subtitle, onMenuClick }) {
  return (
      <header className="sticky top-0 z-20 bg-white border-b border-slate-200 px-4 py-3 md:px-8 flex items-center justify-between shrink-0">
      <div className="flex items-center gap-4">
        {/* Bouton hamburger */}
        <button
          onClick={onMenuClick}
          className="md:hidden inline-flex items-center justify-center p-2 rounded-md text-slate-600 hover:bg-slate-100"
          aria-label="Toggle sidebar"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>

        <div>
          <h1 className="text-lg md:text-xl font-bold text-slate-800">{title}</h1>
          {subtitle && <p className="text-xs text-slate-500 mt-0.5 hidden sm:block">{subtitle}</p>}
        </div>
      </div>

      {/* Partie droite : statut + info utilisateur */}
      <div className="flex items-center gap-4">
        <div className="hidden sm:flex items-center gap-2 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-full text-xs font-medium text-emerald-700">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          AHDIGITAL Network : Opérationnel
        </div>

        <div className="flex items-center gap-3 border-l border-slate-200 pl-4">
          <div className="w-8 h-8 rounded-full bg-slate-800 text-white font-medium text-xs flex items-center justify-center">
            KB
          </div>
          <div className="hidden md:block text-xs">
            <p className="font-semibold text-slate-800">Khadija Boukhatem</p>
            <p className="text-slate-500">Superviseur IT / IAM</p>
          </div>
        </div>
      </div>
    </header>
  );
}