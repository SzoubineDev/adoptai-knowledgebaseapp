-- Import service_sap (66 lignes)
-- id_application laisse NULL (aucun recoupement de nom entre SAP et ServiceNow, constat deja etabli)
INSERT INTO service_sap (nom_service, version, numero_workflow, id_application, id_processus, id_serveur, id_departement, id_module)
SELECT 'MM Core Service', '10.7', '495', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Master Data Governance'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-90-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'IT'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP MM')
UNION ALL
SELECT 'GRC Core Service', '3.6', '871', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Payroll Management'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-91-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'IT'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP GRC')
UNION ALL
SELECT 'SCM Core Service', '9.0', '752', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Expense Reporting'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-57-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'IT'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP SCM')
UNION ALL
SELECT 'BW/4HANA Core Service', '6.4', '214', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Financial Dashboards'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-87-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'Juridique'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP BW/4HANA')
UNION ALL
SELECT 'PM Core Service', '3.7', '304', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Financial Dashboards'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-87-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Support'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP PM')
UNION ALL
SELECT 'HCM Core Service', '9.3', '596', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Expense Reporting'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-11-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Manufacturing'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP HCM')
UNION ALL
SELECT 'Fieldglass Core Service', '7.5', '862', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Expense Reporting'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-50-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'Juridique'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP Fieldglass')
UNION ALL
SELECT 'SCM Core Service', '12.8', '766', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Production Scheduling'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-14-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Supply Chain'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP SCM')
UNION ALL
SELECT 'Ariba Core Service', '7.7', '323', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Lead Generation'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-77-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'IT'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP Ariba')
UNION ALL
SELECT 'SCM Core Service', '2.5', '895', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Order Routing'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-78-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'Design'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP SCM')
UNION ALL
SELECT 'MDG Core Service', '1.0', '349', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Talent Acquisition'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-68-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'RH'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP MDG')
UNION ALL
SELECT 'MM Core Service', '12.0', '155', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Order Routing'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-49-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Support'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP MM')
UNION ALL
SELECT 'IBP Core Service', '7.4', '851', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Production Scheduling'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-46-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'Design'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP IBP')
UNION ALL
SELECT 'BW/4HANA Core Service', '6.1', '169', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Equipment Maintenance'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-92-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP BW/4HANA')
UNION ALL
SELECT 'SD Core Service', '3.9', '195', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Onboarding'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-16-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'Marketing'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP SD')
UNION ALL
SELECT 'SD Core Service', '8.2', '592', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Fleet Logistics'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-52-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'R&D'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP SD')
UNION ALL
SELECT 'GRC Core Service', '8.1', '143', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Quality Checks'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-32-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'Support'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP GRC')
UNION ALL
SELECT 'PP Core Service', '6.3', '121', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Equipment Maintenance'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-48-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'Supply Chain'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP PP')
UNION ALL
SELECT 'EWM Core Service', '5.4', '354', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Supplier Contracting'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-25-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'R&D'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP EWM')
UNION ALL
SELECT 'QM Core Service', '12.8', '573', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Onboarding'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-74-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'Manufacturing'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP QM')
UNION ALL
SELECT 'HCM Core Service', '1.3', '474', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Payroll Management'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-74-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'Supply Chain'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP HCM')
UNION ALL
SELECT 'Ariba Core Service', '6.7', '375', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Risk Assessment'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-27-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'RH'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP Ariba')
UNION ALL
SELECT 'SD Core Service', '1.7', '821', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Talent Acquisition'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-83-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'Marketing'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP SD')
UNION ALL
SELECT 'QM Core Service', '5.3', '192', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Supplier Contracting'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-14-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Commercial'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP QM')
UNION ALL
SELECT 'GRC Core Service', '4.5', '382', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Invoice Processing'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-24-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'IT'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP GRC')
UNION ALL
SELECT 'PS Core Service', '12.3', '287', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Budget Allocation'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-28-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP PS')
UNION ALL
SELECT 'BW/4HANA Core Service', '2.0', '270', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Inventory Audits'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-87-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'R&D'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP BW/4HANA')
UNION ALL
SELECT 'Concur Core Service', '9.4', '626', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Talent Acquisition'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-72-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'Direction'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP Concur')
UNION ALL
SELECT 'Concur Core Service', '7.1', '126', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Budget Allocation'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-77-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Support'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP Concur')
UNION ALL
SELECT 'HCM Core Service', '5.1', '489', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Asset Tracking'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-65-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP HCM')
UNION ALL
SELECT 'FI-CO Core Service', '2.3', '891', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Quality Checks'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-48-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Commercial'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP FI-CO')
UNION ALL
SELECT 'CRM Core Service', '5.8', '395', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Invoice Processing'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-42-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'Support'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP CRM')
UNION ALL
SELECT 'HANA Core Service', '2.2', '932', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Onboarding'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-36-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP HANA')
UNION ALL
SELECT 'Concur Core Service', '2.2', '297', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Payroll Management'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-94-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Design'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP Concur')
UNION ALL
SELECT 'PS Core Service', '4.7', '703', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Supplier Contracting'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-61-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'R&D'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP PS')
UNION ALL
SELECT 'PLM Core Service', '7.3', '879', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Budget Allocation'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-54-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'Supply Chain'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP PLM')
UNION ALL
SELECT 'HCM Core Service', '4.8', '280', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Master Data Governance'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-78-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'Supply Chain'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP HCM')
UNION ALL
SELECT 'QM Core Service', '5.0', '666', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Order Routing'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-20-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'Juridique'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP QM')
UNION ALL
SELECT 'GRC Core Service', '5.1', '714', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Master Data Governance'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-39-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Juridique'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP GRC')
UNION ALL
SELECT 'PS Core Service', '3.9', '883', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Budget Allocation'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-64-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Opérations'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP PS')
UNION ALL
SELECT 'PM Core Service', '4.8', '772', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Onboarding'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-35-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'Juridique'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP PM')
UNION ALL
SELECT 'Ariba Core Service', '6.1', '636', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Order Routing'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-75-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Support'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP Ariba')
UNION ALL
SELECT 'MDG Core Service', '8.3', '603', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Talent Acquisition'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-81-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Finance'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP MDG')
UNION ALL
SELECT 'GRC Core Service', '3.9', '659', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Fleet Logistics'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-85-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'IT'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP GRC')
UNION ALL
SELECT 'SCM Core Service', '5.0', '672', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Fleet Logistics'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-48-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'IT'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP SCM')
UNION ALL
SELECT 'IBP Core Service', '3.6', '219', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Order Routing'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-20-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Opérations'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP IBP')
UNION ALL
SELECT 'FI-CO Core Service', '12.6', '610', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Master Data Governance'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-49-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'Design'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP FI-CO')
UNION ALL
SELECT 'PM Core Service', '9.7', '119', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Inventory Audits'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-81-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP PM')
UNION ALL
SELECT 'GRC Core Service', '1.4', '161', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Expense Reporting'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-15-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'R&D'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP GRC')
UNION ALL
SELECT 'HCM Core Service', '7.2', '533', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Master Data Governance'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-94-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'Engineering'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP HCM')
UNION ALL
SELECT 'PP Core Service', '11.3', '446', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Payroll Management'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-27-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'Opérations'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP PP')
UNION ALL
SELECT 'HANA Core Service', '4.5', '616', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Lead Generation'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-33-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'Commercial'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP HANA')
UNION ALL
SELECT 'SD Core Service', '8.7', '325', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Equipment Maintenance'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-60-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Support'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP SD')
UNION ALL
SELECT 'HANA Core Service', '6.5', '677', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Payroll Management'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-80-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'RH'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP HANA')
UNION ALL
SELECT 'MM Core Service', '9.1', '689', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Risk Assessment'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-37-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'Juridique'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP MM')
UNION ALL
SELECT 'MDG Core Service', '3.9', '452', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Invoice Processing'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-67-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'RH'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP MDG')
UNION ALL
SELECT 'MM Core Service', '2.7', '790', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Production Scheduling'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-89-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'Marketing'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP MM')
UNION ALL
SELECT 'GRC Core Service', '1.9', '275', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Risk Assessment'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-73-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Opérations'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP GRC')
UNION ALL
SELECT 'Concur Core Service', '11.6', '220', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Payroll Management'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-10-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'Direction'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP Concur')
UNION ALL
SELECT 'PS Core Service', '12.7', '131', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Expense Reporting'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-20-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Commercial'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP PS')
UNION ALL
SELECT 'Fiori Core Service', '7.0', '152', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Asset Tracking'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-17-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'Direction'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP Fiori')
UNION ALL
SELECT 'EWM Core Service', '8.3', '624', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Supplier Contracting'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-40-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'Opérations'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP EWM')
UNION ALL
SELECT 'Fiori Core Service', '6.6', '901', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Invoice Processing'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-94-PROD'), (SELECT id_departement FROM departement WHERE nom_departement = 'Opérations'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP Fiori')
UNION ALL
SELECT 'IBP Core Service', '6.4', '299', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Quality Checks'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-25-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'Supply Chain'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP IBP')
UNION ALL
SELECT 'SCM Core Service', '2.5', '486', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Talent Acquisition'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-77-DEV'), (SELECT id_departement FROM departement WHERE nom_departement = 'Design'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP SCM')
UNION ALL
SELECT 'SuccessFactors Core Service', '6.4', '300', NULL::INT, (SELECT id_processus FROM processus_metier WHERE nom_processus = 'Master Data Governance'), (SELECT id_serveur FROM serveur WHERE nom_noeud = 'NODE-26-QA'), (SELECT id_departement FROM departement WHERE nom_departement = 'IT'), (SELECT id_module FROM module_sap WHERE nom_module = 'SAP SuccessFactors');
