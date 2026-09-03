'use client';

import { useEffect, useState } from 'react';
import { StatCard, Card, Badge } from '@/components/ui/Cards';
import { PageStatus } from '@/components/ui/PageStatus';
import {
  fetchApplications,
  fetchDataSources,
  fetchStats,
  criticalityVariant,
} from '@/services/dataService';
import Link from 'next/link';

export default function DashboardPage() {
  const [applications, setApplications] = useState([]);
  const [dataSources, setDataSources] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;

    Promise.all([fetchApplications(4), fetchDataSources(), fetchStats()])
      .then(([apps, sources, dashboardStats]) => {
        if (cancelled) return;
        setApplications(apps);
        setDataSources(sources);
        setStats(dashboardStats);
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
    <PageStatus loading={loading} error={error}>
      <main className="p-4 md:p-8 space-y-6 md:space-y-8">
        {/* Cartes statistiques : 1 col mobile, 2 col tablette, 4 col desktop */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-5">
          <StatCard
            title="Applications Inventoriées"
            value={stats?.applicationCount ?? 0}
            icon="📱"
            description="dans le catalogue"
          />
          <StatCard
            title="Sources de Données"
            value={dataSources.length}
            icon="🗄️"
            description="Apple, SAP, ServiceNow, HelpDesk"
          />
          <StatCard
            title="Comptes IAM Synchronisés"
            value={stats?.iam.totalAccounts ?? 0}
            icon="👥"
            change={stats?.iam.mfaEnforcedRate}
            description="avec identité liée"
          />
          <StatCard
            title="Filtrage AHDIGITAL"
            value={stats?.network.inspectedPackets24h ?? 0}
            icon="🛡️"
            change={`${stats?.network.blockedThreats24h ?? 0} ouverts`}
            changeType="positive"
            description="installations recensées"
          />
        </div>

        <div>
          <h2 className="text-base md:text-lg font-bold text-slate-800 mb-4">
            Sources de Données Connectées (Phase 0 & 0')
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-5">
            {dataSources.map((source) => (
              <Card key={source.id} className="hover:border-slate-300 transition-all">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-bold text-slate-900">{source.name}</h3>
                  <Badge variant="success">{source.status}</Badge>
                </div>
                <p className="text-xs text-slate-500 mb-3">{source.description}</p>
                <div className="flex items-center justify-between text-xs pt-3 border-t border-slate-100 text-slate-600">
                  <span>Enregistrements : <strong>{source.count}</strong></span>
                  <span className="text-[11px] text-slate-400">
                    Sync: {source.lastSync || '—'}
                  </span>
                </div>
              </Card>
            ))}
          </div>
        </div>

        <Card
          title="Applications Récentes dans la Knowledge Base"
          subtitle="Cartographie consolidée issues des flux SAP, Apple, ServiceNow et HelpDesk"
          headerAction={
            <Link
              href="/applications"
              className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 transition-colors"
            >
              Voir toutes les applications →
            </Link>
          }
        >
          {/* Table : scroll horizontal sur mobile */}
          <div className="overflow-x-auto -mx-4 md:mx-0">
            <table className="w-full min-w-[600px] md:min-w-0 text-left text-sm text-slate-600">
              <thead className="bg-slate-50 text-xs uppercase text-slate-500 border-y border-slate-200">
                <tr>
                  <th className="py-3 px-4">Code / Nom</th>
                  <th className="py-3 px-4">Source</th>
                  <th className="py-3 px-4">Responsable</th>
                  <th className="py-3 px-4">Criticité</th>
                  <th className="py-3 px-4">Statut IAM</th>
                  <th className="py-3 px-4">Réseau AHDIGITAL</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {applications.map((app) => (
                  <tr key={app.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3 px-4 font-medium text-slate-900">
                      <Link href={`/applications/${app.id}`} className="hover:underline text-indigo-600">
                        {app.name}
                      </Link>
                      <p className="text-xs text-slate-400">{app.code} • {app.category}</p>
                    </td>
                    <td className="py-3 px-4">
                      <Badge variant="primary">{app.source}</Badge>
                    </td>
                    <td className="py-3 px-4 text-xs">{app.owner}</td>
                    <td className="py-3 px-4">
                      <Badge variant={criticalityVariant(app.criticality)}>
                        {app.criticality}
                      </Badge>
                    </td>
                    <td className="py-3 px-4 text-xs font-mono text-slate-600">{app.iamStatus}</td>
                    <td className="py-3 px-4 text-xs text-slate-500">{app.networkPolicy}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </Card>
      </main>
    </PageStatus>
  );
}