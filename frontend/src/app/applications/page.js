'use client';

import { useEffect, useState } from 'react';
import { Card, Badge } from '@/components/ui/Cards';
import { PageStatus } from '@/components/ui/PageStatus';
import Link from 'next/link';
import { fetchApplications } from '@/services/dataService';
import ApplicationForm from '@/components/ui/ApplicationForm';
import { Pencil, Trash2 } from 'lucide-react';

export default function ApplicationsPage() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedSource, setSelectedSource] = useState('All');
  const [selectedCriticality, setSelectedCriticality] = useState('All');
  const [showForm, setShowForm] = useState(false);
  const [editingApp, setEditingApp] = useState(null);
  const [deletingApp, setDeletingApp] = useState(null);

  useEffect(() => {
    let cancelled = false;

    fetchApplications()
      .then((apps) => {
        if (cancelled) return;
        setApplications(apps);
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

  const filteredApps = applications.filter((app) => {
    const matchesSearch =
      app.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      app.id.toLowerCase().includes(searchTerm.toLowerCase()) ||
      app.description.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesSource = selectedSource === 'All' || app.source === selectedSource;
    const matchesCriticality =
      selectedCriticality === 'All' || app.criticality === selectedCriticality;

    return matchesSearch && matchesSource && matchesCriticality;
  });

  // Handle both add and edit
  const handleSaveApplication = (appData) => {
    if (editingApp) {
      // Update existing application
      setApplications((prev) =>
        prev.map((app) => (app.id === editingApp.id ? { ...app, ...appData } : app))
      );
    } else {
      // Add new application
      setApplications((prev) => [...prev, appData]);
    }
    setShowForm(false);
    setEditingApp(null);
  };

  const handleDeleteApplication = () => {
    if (deletingApp) {
      setApplications((prev) => prev.filter((app) => app.id !== deletingApp.id));
      setDeletingApp(null);
    }
  };

  return (
    <>
      <main className="p-8 space-y-6">
        {/* Filters and Controls */}
        <Card>
          <div className="flex flex-col md:flex-row md:items-end md:justify-between gap-4">
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4 flex-1">
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

            <button
              onClick={() => {
                setEditingApp(null);
                setShowForm(true);
              }}
              className="inline-flex items-center px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-medium rounded-lg transition-colors whitespace-nowrap"
            >
              <span className="mr-1">＋</span> Ajouter une application
            </button>
          </div>
        </Card>

        {/* Applications List */}
        <Card title={`Résultats (${filteredApps.length} application(s))`}>
          <PageStatus loading={loading} error={error}>
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
                        <div className="text-xs text-slate-400">{app.code} • {app.category}</div>
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
                   <td className="py-3.5 px-4">
  <div className="flex items-center justify-center gap-3">
    {/* Edit Button – Blue, larger */}
    <button
      onClick={() => {
        setEditingApp(app);
        setShowForm(true);
      }}
      className="p-2 text-blue-600 hover:text-blue-800 hover:bg-blue-50 rounded-lg transition-colors"
      title="Modifier"
    >
      <Pencil size={20} />
    </button>

    {/* Delete Button – Red, larger */}
    <button
      onClick={() => setDeletingApp(app)}
      className="p-2 text-red-600 hover:text-red-800 hover:bg-red-50 rounded-lg transition-colors"
      title="Supprimer"
    >
      <Trash2 size={20} />
    </button>

    {/* Détails Link (optionnel, gardé pour information) */}
    <Link
      href={`/applications/${app.id}`}
      className="px-2 py-1 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-md text-xs font-medium transition-colors"
    >
      Détails
    </Link>
  </div>
</td>
                    </tr>
                  ))}
                  {filteredApps.length === 0 && !loading && (
                    <tr>
                      <td colSpan="7" className="text-center py-8 text-slate-400 text-sm">
                        Aucune application ne correspond à vos critères de recherche.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </PageStatus>
        </Card>
      </main>

      {/* Application Form Modal (Add / Edit) */}
      {showForm && (
        <ApplicationForm
          onClose={() => {
            setShowForm(false);
            setEditingApp(null);
          }}
          onSubmit={handleSaveApplication}
          initialData={editingApp}
        />
      )}

      {/* Delete Confirmation Modal */}
      {deletingApp && (
        <div className="fixed inset-0 bg-black/30 backdrop-blur-sm flex items-center justify-center z-50 p-4">
          <Card className="w-full max-w-sm p-6">
            <h3 className="text-lg font-semibold text-slate-800 mb-2">Confirmer la suppression</h3>
            <p className="text-sm text-slate-600 mb-4">
              Voulez-vous vraiment supprimer l'application <strong>{deletingApp.name}</strong> ?
            </p>
            <div className="flex justify-end gap-3">
              <button
                onClick={() => setDeletingApp(null)}
                className="px-4 py-2 text-sm font-medium text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition-colors"
              >
                Annuler
              </button>
              <button
                onClick={handleDeleteApplication}
                className="px-4 py-2 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg transition-colors"
              >
                Supprimer
              </button>
            </div>
          </Card>
        </div>
      )}
    </>
  );
}