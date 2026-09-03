'use client';

import { useEffect, useState } from 'react';
import Header from '@/components/layout/Header';
import { Card, Badge } from '@/components/ui/Cards';
import { PageStatus } from '@/components/ui/PageStatus';
import Spinner from '@/components/Spinner';
import { fetchDataSources } from '@/services/dataService';

export default function DataSourcesPage() {
  const [dataSources, setDataSources] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    fetchDataSources()
      .then((sources) => {
        if (cancelled) return;
        setDataSources(sources);
        setLoading(false);
      })
      .catch((err) => {
        if (cancelled) return;
        setError(err.message || 'Erreur inattendue');
        setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <>
      <main className="p-8 space-y-6">
        <Card className="bg-slate-900 text-white border-none">
          <div className="flex items-start justify-between">
            <div>
              <Badge variant="primary">Phase de Découverte (Étapes 0 & 0')</Badge>
              <h2 className="text-lg font-bold text-white mt-2">Périmètre de collecte et extraction des données</h2>
              <p className="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">
                Les étapes 0 et 0' regroupent l'extraction des bases existantes et la formalisation du template standard de recueil. Estimation globale : 6 jours.
              </p>
            </div>
            <span className="text-3xl">🗄️</span>
          </div>
        </Card>

        <PageStatus loading={loading} error={error}>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {dataSources.map((source) => (
              <Card key={source.id} title={source.name} subtitle={source.type}>
                <p className="text-xs text-slate-600 mb-4">{source.description}</p>

                <div className="space-y-2 text-xs">
                  <div className="flex justify-between py-1 border-b border-slate-100">
                    <span className="text-slate-500">Statut de synchronisation</span>
                    <Badge variant="success">{source.status}</Badge>
                  </div>
                  <div className="flex justify-between py-1 border-b border-slate-100">
                    <span className="text-slate-500">Enregistrements extraits</span>
                    <span className="font-bold text-slate-800">{source.count} entités</span>
                  </div>
                  <div className="flex justify-between py-1">
                    <span className="text-slate-500">Dernière mise à jour</span>
                    <span className="font-mono text-slate-600">{source.lastSync}</span>
                  </div>
                </div>
              </Card>
            ))}
          </div>
        </PageStatus>
      </main>
    </>
  );
}
