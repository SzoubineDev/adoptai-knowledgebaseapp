export function Badge({ children, variant = 'default' }) {
  const styles = {
    default: 'bg-slate-100 text-slate-700 border-slate-200',
    primary: 'bg-indigo-50 text-indigo-700 border-indigo-200',
    success: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    warning: 'bg-amber-50 text-amber-700 border-amber-200',
    danger: 'bg-rose-50 text-rose-700 border-rose-200',
    critical: 'bg-red-100 text-red-800 border-red-300 font-semibold'
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${styles[variant] || styles.default}`}>
      {children}
    </span>
  );
}

export function Card({ title, subtitle, children, className = '', headerAction }) {
  return (
    <div className={`bg-white rounded-xl border border-slate-200 shadow-sm p-5 ${className}`}>
      {(title || subtitle || headerAction) && (
        <div className="flex items-center justify-between pb-3 mb-4 border-b border-slate-100">
          <div>
            {title && <h3 className="text-base font-semibold text-slate-800">{title}</h3>}
            {subtitle && <p className="text-xs text-slate-500 mt-0.5">{subtitle}</p>}
          </div>
          {headerAction && <div>{headerAction}</div>}
        </div>
      )}
      {children}
    </div>
  );
}

export function StatCard({ title, value, icon, change, changeType = 'positive', description }) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-5 flex flex-col justify-between">
      <div className="flex items-center justify-between">
        <span className="text-xs font-medium text-slate-500 uppercase tracking-wider">{title}</span>
        {icon && <span className="text-xl">{icon}</span>}
      </div>
      <div className="my-2">
        <span className="text-2xl font-bold text-slate-900">{value}</span>
      </div>
      {(change || description) && (
        <div className="flex items-center text-xs text-slate-500">
          {change && (
            <span className={`font-semibold mr-1.5 ${changeType === 'positive' ? 'text-emerald-600' : 'text-rose-600'}`}>
              {change}
            </span>
          )}
          {description}
        </div>
      )}
    </div>
  );
}
