-- Import application (18 lignes issues du catalogue ServiceNow)
INSERT INTO application (nom_canonique, description, type, criticite, statut, date_derniere_maj, id_departement)
SELECT 'Intranet Entreprise', 'Communication interne et actualités', 'Interne', 'Moyenne', 'Actif', '2025-12-25'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'Marketing')
UNION ALL
SELECT 'Outil de Gestion des Stocks', 'Suivi des stocks et approvisionnements', 'Interne', 'Moyenne', 'Actif', '2024-12-24'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'Opérations')
UNION ALL
SELECT 'Intranet Entreprise', 'Communication interne et actualités', 'Legacy', 'Moyenne', 'Obsolète', '2026-02-15'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'Marketing')
UNION ALL
SELECT 'CRM Commercial', 'Suivi des clients et opportunités', 'Legacy', 'Haute', 'En fin de vie', '2026-02-15'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'Commercial')
UNION ALL
SELECT 'Outil de Ticketing IT', 'Gestion des demandes de support interne', 'Interne', 'Haute', 'Actif', '2025-11-06'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'IT')
UNION ALL
SELECT 'Plateforme de Formation en Ligne', 'Formations et certifications internes', 'Interne', 'Basse', 'Obsolète', '2025-11-23'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'RH')
UNION ALL
SELECT 'Portail RH Interne', 'Gestion des congés, absences et paie', 'Legacy', 'Haute', 'Actif', '2024-11-05'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'RH')
UNION ALL
SELECT 'Outil de Gestion des Accès', 'Attribution des droits utilisateurs', 'SaaS', 'Haute', 'Actif', '2025-05-31'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'IT')
UNION ALL
SELECT 'Système de Paie Externalisé', 'Traitement de la paie mensuelle', 'Legacy', 'Haute', 'Actif', '2025-09-15'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'Finance')
UNION ALL
SELECT 'Portail RH Interne', 'Gestion des congés, absences et paie', 'Interne', 'Haute', 'En fin de vie', '2025-02-20'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'RH')
UNION ALL
SELECT 'Outil de Facturation', 'Émission et suivi des factures clients', 'SaaS', 'Haute', 'Actif', '2026-06-24'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'Finance')
UNION ALL
SELECT 'Plateforme de Formation en Ligne', 'Formations et certifications internes', 'SaaS', 'Basse', 'Actif', '2026-03-04'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'RH')
UNION ALL
SELECT 'CRM Commercial', 'Suivi des clients et opportunités', 'SaaS', 'Haute', 'Actif', '2026-02-23'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'Commercial')
UNION ALL
SELECT 'Plateforme Marketing Automation', 'Campagnes email et suivi des leads', 'SaaS', 'Moyenne', 'Obsolète', '2026-01-27'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'Marketing')
UNION ALL
SELECT 'Outil de Signature Électronique', 'Signature de documents et contrats', 'Interne', 'Moyenne', 'En fin de vie', '2026-01-22'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'Juridique')
UNION ALL
SELECT 'Outil de Gestion des Accès', 'Attribution des droits utilisateurs', 'Interne', 'Haute', 'En fin de vie', '2024-12-08'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'IT')
UNION ALL
SELECT 'CRM Commercial', 'Suivi des clients et opportunités', 'Legacy', 'Haute', 'Actif', '2025-03-12'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'Commercial')
UNION ALL
SELECT 'Plateforme Marketing Automation', 'Campagnes email et suivi des leads', 'Legacy', 'Moyenne', 'Actif', '2025-12-23'::DATE, (SELECT id_departement FROM departement WHERE nom_departement = 'Marketing');
