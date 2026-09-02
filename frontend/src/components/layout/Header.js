'use client';

export default function Header({ title, subtitle, onMenuClick }) {
  return (
    <header className="sticky top-0 z-20 bg-white/80 backdrop-blur border-b border-slate-200 px-4 py-3 md:px-8">
      <div className="flex items-center gap-4">
        {/* Hamburger button – visible only on mobile */}
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
          <h1 className="text-lg md:text-2xl font-bold">{title}</h1>
          {subtitle && <p className="text-xs md:text-sm text-slate-500">{subtitle}</p>}
        </div>
      </div>
    </header>
  );
}