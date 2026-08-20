'use client';

import { useState } from 'react';
import Header from '@/components/layout/Header';
import { Card, Badge } from '@/components/ui/Cards';
import { MOCK_APPLICATIONS } from '@/services/dataService';
import Link from 'next/link';

export default function ApplicationsPage() {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSource, setSelectedSource] = useState('All');
  const [selectedCriticality, setSelectedCriticality] = useState('All');

  const filteredApps = MOCK_APPLICATIONS.filter((app) => {
    const matchesSearch =
      app.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      app.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      app.description.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesSource = selectedSource === 'All' || app.source === selectedSource;
    const matchesCriticality =
      selectedCriticality === 'All' || app.criticality === selectedCriticality;

    return matchesSearch && matchesSource && matchesCriticality;
  });

  return (
    <>
      <Header
        title="Inventaire des Applications — Knowledge Base"
        subtitle="Catalogue centralisé des applications avec informations IAM et règles de filtrage réseau"
      />

      <main className="p-8 space-y-6">
        {/* Filters and Controls */}
        <Card>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="md:col-span-2">
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Recherche globale
              </label>
              <input
                type="text"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Rechercher par nom, code ou description..."
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Source de Données
              </label>
              <select
                value={selectedSource}
                onChange={(e) => setSelectedSource(e.target.value)}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="All">Toutes les sources</option>
                <option value="SAP">SAP</option>
                <option value="Apple">Apple</option>
                <option value="ServiceNow">ServiceNow</option>
                <option value="HelpDesk">HelpDesk</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-600 mb-1">
                Niveau de Criticité
              </label>
              <select
                value={selectedCriticality}
                onChange={(e) => setSelectedCriticality(e.target.value)}
                className="w-full px-3 py-2 text-sm border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="All">Toutes les criticités</option>
                <option value="Critique">Critique</option>
                <option value="Élevée">Élevée</option>
                <option value="Moyenne">Moyenne</option>
              </select>
            </div>
          </div>
        </Card>

        {/* Applications List */}
        <Card title={`Résultats (${filteredApps.length} application(s))`}>
          <div className="overflow-x-auto">
            <table className="w-full text-left text-sm text-slate-600">
              <thead className="bg-slate-50 text-xs uppercase text-slate-500 border-y border-slate-200">
                <tr>
                  <th className="py-3 px-4">Code & Nom</th>
                  <th className="py-3 px-4">Source</th>
                  <th className="py-3 px-4">Responsable</th>
                  <th className="py-3 px-4">Tech Lead</th>
                  <th className="py-3 px-4">Criticité</th>
                  <th className="py-3 px-4">IAM / Access</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {filteredApps.map((app) => (
                  <tr key={app.id} className="hover:bg-slate-50/80 transition-colors">
                    <td className="py-3.5 px-4 font-medium text-slate-900">
                      <div className="font-semibold text-indigo-600">{app.name}</div>
                      <div className="text-xs text-slate-400">{app.id} • {app.category}</div>
                    </td>
                    <td className="py-3.5 px-4">
                      <Badge variant="primary">{app.source}</Badge>
                    </td>
                    <td className="py-3.5 px-4 text-xs font-medium text-slate-700">{app.owner}</td>
                    <td className="py-3.5 px-4 text-xs text-slate-600">{app.techLead}</td>
                    <td className="py-3.5 px-4">
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
                    <td className="py-3.5 px-4 text-xs font-mono">{app.iamStatus}</td>
                    <td className="py-3.5 px-4 text-right">
                      <Link
                        href={`/applications/${app.id}`}
                        className="inline-flex items-center px-3 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-md text-xs font-medium transition-colors"
                      >
                        Détails
                      </Link>
                    </td>
                  </tr>
                ))}
                {filteredApps.length === 0 && (
                  <tr>
                    <td colSpan="7" className="text-center py-8 text-slate-400 text-sm">
                      Aucune application ne correspond à vos critères de recherche.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </Card>
      </main>
    </>
  );
}
