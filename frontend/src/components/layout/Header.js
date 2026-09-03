'use client';

export default function Header({ title, subtitle }) {
  return (
    <header className="bg-white border-b border-slate-200 px-8 py-4 flex items-center justify-between shrink-0">
      <div>
        <h1 className="text-xl font-bold text-slate-800">{title}</h1>
        {subtitle && <p className="text-xs text-slate-500 mt-0.5">{subtitle}</p>}
      </div>

      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-full text-xs font-medium text-emerald-700">
          <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          AHDIGITAL Network : Opérationnel
        </div>

        <div className="flex items-center gap-3 border-l border-slate-200 pl-4">
          <div className="w-8 h-8 rounded-full bg-slate-800 text-white font-medium text-xs flex items-center justify-center">
            KB
          </div>
          <div className="text-xs">
            <p className="font-semibold text-slate-800">Khadija Boukhatem</p>
            <p className="text-slate-500">Superviseur IT / IAM</p>
          </div>
        </div>
      </div>
    </header>
  );
}
