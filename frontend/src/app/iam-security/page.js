'use client';

import Header from '@/components/layout/Header';
import { Card, StatCard, Badge } from '@/components/ui/Cards';
import { IAM_STATS, NETWORK_STATS } from '@/services/dataService';

export default function IamSecurityPage() {
  return (
    <>
      <Header
        title="Stratégie IAM & Sécurité Réseau AHDIGITAL"
        subtitle="Gestion des comptes, contrôle d'accès et filtrage/monitoring des paquets"
      />

      <main className="p-8 space-y-8">
        {/* Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-5">
          <StatCard
            title="Comptes IAM Actifs"
            value={IAM_STATS.totalAccounts}
            icon="🆔"
            description="sur l'ensemble des périmètres"
          />
          <StatCard
            title="Taux MFA Enforced"
            value={IAM_STATS.mfaEnforcedRate}
            icon="🔑"
            change="Conforme"
            changeType="positive"
            description="politique de sécurité"
          />
          <StatCard
            title="VLAN Sécurisé"
            value={NETWORK_STATS.vlan}
            icon="🌐"
            description="Zone AHDIGITAL"
          />
          <StatCard
            title="Règles Firewall"
            value={NETWORK_STATS.activeFirewallRules}
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
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 flex items-center justify-between">
                <div>
                  <p className="font-semibold text-slate-800">Fédération SSO & Identity Provider</p>
                  <p className="text-slate-500">Mise en conformité OIDC / SAML 2.0 sur le réseau AHDIGITAL</p>
                </div>
                <Badge variant="success font-mono">92% Migré</Badge>
              </div>

              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 flex items-center justify-between">
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
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 flex items-center justify-between">
                <div>
                  <p className="font-semibold text-slate-800">Inspection Deep Packet (DPI)</p>
                  <p className="text-slate-500">4.2M paquets analysés au cours des dernières 24 heures</p>
                </div>
                <Badge variant="primary">Actif</Badge>
              </div>

              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 flex items-center justify-between">
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
    </>
  );
}
