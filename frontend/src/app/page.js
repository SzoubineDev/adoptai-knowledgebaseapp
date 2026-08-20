'use client';

import Header from '@/components/layout/Header';
import { StatCard, Card, Badge } from '@/components/ui/Cards';
import { DATA_SOURCES, MOCK_APPLICATIONS, IAM_STATS, NETWORK_STATS } from '@/services/dataService';
import Link from 'next/link';

export default function DashboardPage() {
  return (
    <>
      <Header
        title="Tableau de Bord — App Knowledge Base"
        subtitle="Vue synthétique des applications, sources de données (Apple, SAP, ServiceNow, HelpDesk) et sécurité AHDIGITAL"
      />

      <main className="p-8 space-y-8">
        {/* KPI Section */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          <StatCard
            title="Applications Inventoriées"
            value={MOCK_APPLICATIONS.length}
            icon="📱"
            change="+2"
            description="ajoutées ce mois"
          />
          <StatCard
            title="Sources de Données"
            value={DATA_SOURCES.length}
            icon="🗄️"
            description="Apple, SAP, ServiceNow, HelpDesk"
          />
          <StatCard
            title="Comptes IAM Synchronisés"
            value={IAM_STATS.totalAccounts}
            icon="👥"
            change={IAM_STATS.mfaEnforcedRate}
            description="avec MFA appliqué"
          />
          <StatCard
            title="Filtrage AHDIGITAL (24h)"
            value={NETWORK_STATS.inspectedPackets24h}
            icon="🛡️"
            change={`${NETWORK_STATS.blockedThreats24h} bloqués`}
            changeType="positive"
            description="paquets inspectés"
          />
        </div>

        {/* Data Sources Grid */}
        <div>
          <h2 className="text-lg font-bold text-slate-800 mb-4">Sources de Données Connectées (Phase 0 & 0')</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
            {DATA_SOURCES.map((source) => (
              <Card key={source.id} className="hover:border-slate-300 transition-all">
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-bold text-slate-900">{source.name}</h3>
                  <Badge variant="success">{source.status}</Badge>
                </div>
                <p className="text-xs text-slate-500 mb-3">{source.description}</p>
                <div className="flex items-center justify-between text-xs pt-3 border-t border-slate-100 text-slate-600">
                  <span>Enregistrements : <strong>{source.count}</strong></span>
                  <span className="text-[11px] text-slate-400">Sync: {source.lastSync.split(' ')[1]}</span>
                </div>
              </Card>
            ))}
          </div>
        </div>

        {/* Applications Highlights */}
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
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-600">
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
                {MOCK_APPLICATIONS.slice(0, 4).map((app) => (
                  <tr key={app.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3 px-4 font-medium text-slate-900">
                      <Link href={`/applications/${app.id}`} className="hover:underline text-indigo-600">
                        {app.name}
                      </Link>
                      <p className="text-xs text-slate-400">{app.id} • {app.category}</p>
                    </td>
                    <td className="py-3 px-4">
                      <Badge variant="primary">{app.source}</Badge>
                    </td>
                    <td className="py-3 px-4 text-xs">{app.owner}</td>
                    <td className="py-3 px-4">
                      <Badge
                        variant={
                          app.criticality === 'Critique'
                            ? 'critical'
                            : app.criticality === 'Élevée'
                            ? 'danger'
                            : 'warning'
                        }
                      >
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
    </>
  );
}
