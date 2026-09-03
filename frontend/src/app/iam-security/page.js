'use client';

import { useState, useEffect } from 'react';
import { Card, StatCard, Badge } from '@/components/ui/Cards';
import { fetchIamStats, fetchNetworkStats } from '@/services/dataService';
import Spinner from '@/components/Spinner';

export default function IamSecurityPage() {
  const [iamStats, setIamStats] = useState(null);
  const [networkStats, setNetworkStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadStats() {
      try {
        const [iam, network] = await Promise.all([
          fetchIamStats(),
          fetchNetworkStats()
        ]);
        setIamStats(iam);
        setNetworkStats(network);
      } catch (error) {
        console.error('Failed to load stats:', error);
      } finally {
        setLoading(false);
      }
    }
    loadStats();
  }, []);

  if (loading || !iamStats || !networkStats) {
    return (
      <div className="p-4 md:p-8">
        <Spinner />
      </div>
    );
  }

  return (
    <main className="p-4 md:p-8 space-y-6 md:space-y-8">
      {/* Cartes statistiques : responsive */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-5">
        <StatCard
          title="Comptes IAM Actifs"
          value={iamStats.totalAccounts}
          icon="🆔"
          description="sur l'ensemble des périmètres"
        />
        <StatCard
          title="Taux MFA Enforced"
          value={iamStats.mfaEnforcedRate}
          icon="🔑"
          change="Conforme"
          changeType="positive"
          description="politique de sécurité"
        />
        <StatCard
          title="VLAN Sécurisé"
          value={networkStats.vlan}
          icon="🌐"
          description="Zone AHDIGITAL"
        />
        <StatCard
          title="Règles Firewall"
          value={networkStats.activeFirewallRules}
          icon="🛡️"
          description="politiques de filtrage"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card title="Gestion des Comptes & IAM" subtitle="Alignement SSO, Azure AD / Okta & SAML 2.0">
          <p className="text-xs text-slate-600 mb-4 leading-relaxed">
            La stratégie IAM vise à unifier les identités issues de ServiceNow et HelpDesk avec les accès aux applicatifs métiers (SAP, Apple Jamf Pro).
          </p>
          <div className="space-y-3 text-xs">
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <p className="font-semibold text-slate-800">Fédération SSO & Identity Provider</p>
                <p className="text-slate-500">Mise en conformité OIDC / SAML 2.0 sur le réseau AHDIGITAL</p>
              </div>
              <Badge variant="success font-mono">92% Migré</Badge>
            </div>

            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <p className="font-semibold text-slate-800">Provisioning automatique (Lifecycle Management)</p>
                <p className="text-slate-500">Création / Révocation de comptes automatisée via ITSM</p>
              </div>
              <Badge variant="warning font-mono">Phase Bêta</Badge>
            </div>
          </div>
        </Card>

        <Card title="Monitoring & Filtrage Paquets (Réseau AHDIGITAL)" subtitle="Inspection dynamique et sécurité périmétrique">
          <p className="text-xs text-slate-600 mb-4 leading-relaxed">
            Analyse continue des flux applicatifs circulant dans le réseau AHDIGITAL pour détecter les anomalies et appliquer le filtrage strict.
          </p>
          <div className="space-y-3 text-xs">
            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <p className="font-semibold text-slate-800">Inspection Deep Packet (DPI)</p>
                <p className="text-slate-500">4.2M paquets analysés au cours des dernières 24 heures</p>
              </div>
              <Badge variant="primary">Actif</Badge>
            </div>

            <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <p className="font-semibold text-slate-800">Blocage des Menaces & Intrusion Prevention</p>
                <p className="text-slate-500">128 tentatives d'accès non autorisés rejetées</p>
              </div>
              <Badge variant="danger">128 Bloqués</Badge>
            </div>
          </div>
        </Card>
      </div>
    </main>
  );
}