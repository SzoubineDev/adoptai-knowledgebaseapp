import { Card } from './Cards';
import Spinner from '../Spinner';

export function PageStatus({ loading, error, children }) {
  if (loading) {
    return (
      <main className="p-8">
        <Card className="text-center py-12">
          <Spinner />
        </Card>
      </main>
    );
  }

  if (error) {
    return (
      <main className="p-8">
        <Card className="text-center py-12">
          <h2 className="text-xl font-bold text-slate-800 mb-2">Impossible de joindre l&apos;API</h2>
          <p className="text-sm text-slate-500">{error}</p>
          <p className="text-xs text-slate-400 mt-3">
            Vérifiez que FastAPI tourne sur le port 8000 (uvicorn app.main:app).
          </p>
        </Card>
      </main>
    );
  }

  return children;
}