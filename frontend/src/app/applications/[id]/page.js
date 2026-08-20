'use client';

import { use } from 'react';
import Header from '@/components/layout/Header';
import { Card, Badge } from '@/components/ui/Cards';
import { MOCK_APPLICATIONS } from '@/services/dataService';
import Link from 'next/link';

export default function ApplicationDetailPage({ params }) {
  const resolvedParams = use(params);
  const app = MOCK_APPLICATIONS.find((a) => a.id === resolvedParams.id);

  if (!app) {
    return (
      <main className="p-8">
        <Card className="text-center py-12">
          <h2 className="text-xl font-bold text-slate-800 mb-2">Application introuvable</h2>
          <p className="text-sm text-slate-500 mb-4">L'identifiant spécifié ({resolvedParams.id}) n'existe pas dans la base.</p>
          <Link href="/applications" className="text-sm font-semibold text-indigo-600 hover:underline">
            ← Retour à la liste
          </Link>
        </Card>
      </main>
    );
  }

  return (
    <>
      <Header
        title={`${app.name} (${app.id})`}
        subtitle={`Application de la source ${app.source} — Catégorie : ${app.category}`}
      />

      <main className="p-8 space-y-6">
        <div>
          <Link
            href="/applications"
            className="inline-flex items-center text-xs font-semibold text-slate-500 hover:text-slate-800 transition-colors"
          >
            ← Retour au catalogue des applications
          </Link>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <Card title="Fiche Métier & Description" className="lg:col-span-2">
            <p className="text-sm text-slate-600 leading-relaxed mb-6">{app.description}</p>

            <div className="grid grid-cols-2 gap-4 text-xs">
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                <span className="text-slate-400 block font-medium">Propriétaire Métier</span>
                <span className="font-semibold text-slate-800 text-sm">{app.owner}</span>
              </div>
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                <span className="text-slate-400 block font-medium">Responsable Technique</span>
                <span className="font-semibold text-slate-800 text-sm">{app.techLead}</span>
              </div>
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                <span className="text-slate-400 block font-medium">Environnement</span>
                <span className="font-semibold text-slate-800 text-sm">{app.environment}</span>
              </div>
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-100">
                <span className="text-slate-400 block font-medium">Utilisateurs Actifs</span>
                <span className="font-semibold text-slate-800 text-sm">{app.usersCount} utilisateurs</span>
              </div>
            </div>
          </Card>

          <Card title="Spécifications Techniques & Sécurité">
            <div className="space-y-4 text-xs">
              <div>
                <span className="text-slate-400 block font-medium">Source d'Origine</span>
                <div className="mt-1"><Badge variant="primary">{app.source}</Badge></div>
              </div>

              <div>
                <span className="text-slate-400 block font-medium">Niveau de Criticité</span>
                <div className="mt-1">
                  <Badge variant={app.criticality === 'Critique' ? 'critical' : 'danger'}>
                    {app.criticality}
                  </Badge>
                </div>
              </div>

              <div className="pt-3 border-t border-slate-100">
                <span className="text-slate-400 block font-medium mb-1">Authentification & IAM</span>
                <p className="font-mono bg-slate-50 p-2 rounded text-slate-700 border border-slate-200">
                  {app.iamStatus}
                </p>
              </div>

              <div>
                <span className="text-slate-400 block font-medium mb-1">Politique Réseau AHDIGITAL</span>
                <p className="font-mono bg-slate-50 p-2 rounded text-slate-700 border border-slate-200">
                  {app.networkPolicy}
                </p>
              </div>
            </div>
          </Card>
        </div>
      </main>
    </>
  );
}
