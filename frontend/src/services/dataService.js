// Mock dataset aggregating Apple, SAP, ServiceNow, and HelpDesk sources

export const DATA_SOURCES = [
  {
    id: 'apple',
    name: 'Apple Infrastructure',
    type: 'Hardware & OS Inventory',
    count: 24,
    status: 'Active',
    lastSync: '2026-08-19 14:30',
    description: 'Parc de devices et terminaux Apple (MacBook, iMac, iOS) sous supervision MDM.'
  },
  {
    id: 'sap',
    name: 'SAP Enterprise ERP',
    type: 'ERP & Business Modules',
    count: 18,
    status: 'Active',
    lastSync: '2026-08-19 12:00',
    description: 'Modules cœurs SAP (FI/CO, MM, SD, HR, S/4HANA) et intégrations métiers.'
  },
  {
    id: 'servicenow',
    name: 'ServiceNow ITSM',
    type: 'IT Service Catalog & Incidents',
    count: 32,
    status: 'Active',
    lastSync: '2026-08-19 15:10',
    description: 'Catalogue des services IT, gestion des tickets, workflows de demande de comptes.'
  },
  {
    id: 'helpdesk',
    name: 'HelpDesk Internal',
    type: 'Support & Tickets',
    count: 15,
    status: 'Active',
    lastSync: '2026-08-19 11:45',
    description: 'Base d\'incidents N1/N2 et demandes d\'assistance utilisateurs locaux.'
  }
];

export const MOCK_APPLICATIONS = [
  {
    id: 'APP-001',
    name: 'SAP S/4HANA Finance (FI/CO)',
    category: 'ERP / Finance',
    source: 'SAP',
    owner: 'Direction Financière',
    techLead: 'Marc Dupont',
    criticality: 'Critique',
    iamStatus: 'SAML 2.0 / SSO OK',
    networkPolicy: 'Filtrage strict AHDIGITAL (Port 443/3200)',
    environment: 'Production',
    description: 'Gestion comptable, contrôle de gestion et clôtures financières du groupe.',
    version: '2023.2',
    usersCount: 140
  },
  {
    id: 'APP-002',
    name: 'Apple Jamf Pro MDM',
    category: 'Gestion de Parc / IAM',
    source: 'Apple',
    owner: 'Équipe Infrastructure IT',
    techLead: 'Khadija Boukhatem',
    criticality: 'Élevée',
    iamStatus: 'Azure AD / Entra ID Sync',
    networkPolicy: 'Monitoring paquets HTTPS / Token cert',
    environment: 'Production',
    description: 'Gestion centralisée des terminaux macOS et iOS, déploiement des profils de sécurité.',
    version: '10.48',
    usersCount: 450
  },
  {
    id: 'APP-003',
    name: 'ServiceNow Service Portal',
    category: 'ITSM',
    source: 'ServiceNow',
    owner: 'Support IT & Ops',
    techLead: 'Antoine Martin',
    criticality: 'Élevée',
    iamStatus: 'OIDC / Okta Federation',
    networkPolicy: 'Accès filtré Reverse Proxy AHDIGITAL',
    environment: 'Production',
    description: 'Portail de souscription de comptes IAM, demandes d\'accès et suivi d\'incidents.',
    version: 'Utah Patch 4',
    usersCount: 1200
  },
  {
    id: 'APP-004',
    name: 'HelpDesk Ticketing Platform',
    category: 'Support Client',
    source: 'HelpDesk',
    owner: 'Centre de Services',
    techLead: 'Sarah Bennis',
    criticality: 'Moyenne',
    iamStatus: 'Local Auth / En cours de migration SSO',
    networkPolicy: 'VLAN Interne filtré',
    environment: 'Production',
    description: 'Gestion des demandes d\'assistance de niveau 1 et 2 pour le réseau AHDIGITAL.',
    version: '4.2.1',
    usersCount: 85
  },
  {
    id: 'APP-005',
    name: 'SAP SuccessFactors',
    category: 'RH & Talent Management',
    source: 'SAP',
    owner: 'Direction RH',
    techLead: 'Claire Lefebvre',
    criticality: 'Élevée',
    iamStatus: 'SAML 2.0 / Auto-provisioning',
    networkPolicy: 'Filtrage IP Whitelist & AHDIGITAL VPN',
    environment: 'Production',
    description: 'Portail RH pour les évaluations, congés, formations et fiches collaborateurs.',
    version: 'Cloud v2405',
    usersCount: 650
  },
  {
    id: 'APP-006',
    name: 'Apple Business Manager (ABM)',
    category: 'Gestion Flotte & Licensing',
    source: 'Apple',
    owner: 'Achats IT & SecOps',
    techLead: 'Khadija Boukhatem',
    criticality: 'Moyenne',
    iamStatus: 'Managed Apple IDs',
    networkPolicy: 'HTTPS Restreint',
    environment: 'Production',
    description: 'Déploiement automatisé (DEP/VPP) des équipements Apple neufs.',
    version: 'SaaS Apple',
    usersCount: 12
  }
];

export const IAM_STATS = {
  totalAccounts: 1850,
  ssoEnabled: 1620,
  pendingAudits: 42,
  mfaEnforcedRate: '94%'
};

export const NETWORK_STATS = {
  vlan: 'AHDIGITAL-SEC-01',
  inspectedPackets24h: '4.2 M',
  blockedThreats24h: 128,
  activeFirewallRules: 312
};
